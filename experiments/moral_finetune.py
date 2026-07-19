# Fine-tune a moral-COMPETENT consumer for the GO-P-2026-037 moral flip: frozen embeddings can't judge
# morality (LaBSE 0.60, BGE-M3 0.58 ~ chance on ETHICS), so fine-tune LaBSE end-to-end on ETHICS
# commonsense, then export the fine-tuned representation (pooler output) + the classifier head. The head
# is the CONSUMER; its weight direction is the moral read operator (recovered blind by the flip harness).
import os, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

DEV = "cuda:0"; MODEL = "bert-base-uncased"; OUT = "/home/claude/moral_cache/moral_ft.npz"


def load(n):
    T, Y = [], []
    for line in open("/archive/ethics-corpora/ethics/commonsense.jsonl", encoding="utf-8"):
        d = json.loads(line); T.append(d["text"][:400]); Y.append(int(d["label"]))
        if len(T) >= n:
            break
    idx = np.random.default_rng(0).permutation(len(T))            # SHUFFLE (mix train + hard sections)
    return [T[i] for i in idx], np.array(Y)[idx]


def acc_of(model, base, W, b, ids, mask, y):
    model.eval(); reps = []
    with torch.no_grad():
        for i in range(0, len(ids), 128):
            o = base(input_ids=ids[i:i + 128].to(DEV), attention_mask=mask[i:i + 128].to(DEV))
            p = o.pooler_output if o.pooler_output is not None else o.last_hidden_state[:, 0]
            reps.append(p.cpu().numpy())
    R = np.concatenate(reps).astype(np.float64)
    return float((np.argmax(R @ W.T + b, 1) == y).mean()), R


def main():
    os.makedirs("/home/claude/moral_cache", exist_ok=True)
    T, Y = load(24000); ntr = 20000
    tok = AutoTokenizer.from_pretrained(MODEL)
    enc = tok(T, truncation=True, max_length=128, padding="max_length", return_tensors="pt")
    ids, mask, ytt = enc["input_ids"], enc["attention_mask"], torch.tensor(Y)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2).to(DEV)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-5)
    tr = DataLoader(TensorDataset(ids[:ntr], mask[:ntr], ytt[:ntr]), batch_size=32, shuffle=True)
    base = model.bert
    for ep in range(4):
        model.train()
        for bi, bm, by in tr:
            opt.zero_grad()
            out = model(input_ids=bi.to(DEV), attention_mask=bm.to(DEV), labels=by.to(DEV))
            out.loss.backward(); opt.step()
        Wc = model.classifier.weight.detach().cpu().numpy().astype(np.float64)
        bc = model.classifier.bias.detach().cpu().numpy().astype(np.float64)
        tra, _ = acc_of(model, base, Wc, bc, ids[:2000], mask[:2000], Y[:2000])
        hoa, _ = acc_of(model, base, Wc, bc, ids[ntr:], mask[ntr:], Y[ntr:])
        print(f"epoch {ep}: train acc {tra:.3f}  held-out acc {hoa:.3f}", flush=True)
    W = model.classifier.weight.detach().cpu().numpy().astype(np.float64)      # (2, D)
    b = model.classifier.bias.detach().cpu().numpy().astype(np.float64)        # (2,)

    def extract(a, m):
        reps = []
        model.eval()
        with torch.no_grad():
            for i in range(0, len(a), 128):
                o = base(input_ids=a[i:i + 128].to(DEV), attention_mask=m[i:i + 128].to(DEV))
                pooled = o.pooler_output if o.pooler_output is not None else o.last_hidden_state[:, 0]
                reps.append(pooled.cpu().numpy())
        return np.concatenate(reps).astype(np.float64)

    Rtr = extract(ids[:ntr], mask[:ntr]); Rho = extract(ids[ntr:], mask[ntr:])
    Yho = Y[ntr:]
    acc = float((np.argmax(Rho @ W.T + b, 1) == Yho).mean())
    maj = float(max(Yho.mean(), 1 - Yho.mean()))
    print(f"FINE-TUNED consumer held-out acc = {acc:.3f} (majority {maj:.3f}); rep dim {Rtr.shape[1]}", flush=True)
    np.savez(OUT, Rtr=Rtr, Ytr=Y[:ntr], Rho=Rho, Yho=Yho, W=W, b=b)
    print(f"saved {OUT}", flush=True)


if __name__ == "__main__":
    main()
