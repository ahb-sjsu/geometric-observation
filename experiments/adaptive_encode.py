import os, sys, numpy as np, torch, warnings
warnings.filterwarnings("ignore")
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
sys.path.insert(0, "/home/claude/tqp")
from a2_probe_std import _consumer_scores, _spearman, _polar_proxy, _per_channel_proxy


def fit_ctx(Xcal, Qcal):
    mu = Xcal.mean(0); C = Xcal - mu; cov = (C.T @ C) / len(C)
    cov = cov + 1e-2 * (np.trace(cov) / cov.shape[0]) * np.eye(cov.shape[0])
    w, V = np.linalg.eigh(cov); w = np.maximum(w, 1e-12)
    Wm = V @ np.diag(1.0 / np.sqrt(w)) @ V.T; Wi = V @ np.diag(np.sqrt(w)) @ V.T
    qc = Qcal - Qcal.mean(0); _, _, Vq = np.linalg.svd(qc, full_matrices=False)
    return dict(mu=mu, Wm=Wm, Wi=Wi, Vq=Vq)


def wuni(X, bits, c):
    Kw = (X - c["mu"]) @ c["Wm"]; lo, hi = Kw.min(0, keepdims=True), Kw.max(0, keepdims=True)
    step = np.maximum((hi - lo) / (2 ** bits - 1), 1e-30)
    return (np.round((Kw - lo) / step) * step + lo) @ c["Wi"] + c["mu"]


def blindread(X, bits, c, r=16):                         # protect top-r query (read) subspace, drop rest
    V = c["Vq"][:r].T; cc = X @ V
    b = max(bits * X.shape[1] / r, 1.0)
    lo, hi = cc.min(0, keepdims=True), cc.max(0, keepdims=True)
    step = np.maximum((hi - lo) / (2 ** b - 1), 1e-30)
    return (np.round((cc - lo) / step) * step + lo) @ V.T


def _rng():
    return np.random.default_rng(0)


CANDS = {
    "generic-polar":   lambda X, b, c: _polar_proxy(X, b, _rng()),
    "per-channel":     lambda X, b, c: _per_channel_proxy(X, b),
    "whitened-unif":   lambda X, b, c: wuni(X, b, c),
    "whitened-polar":  lambda X, b, c: _polar_proxy((X - c["mu"]) @ c["Wm"], b, _rng()) @ c["Wi"] + c["mu"],
    "blind-read":      lambda X, b, c: blindread(X, b, c),
}


def agree(X, Q, consumer, Xq):
    e = _consumer_scores(X, Q, consumer); a = _consumer_scores(Xq, Q, consumer)
    return float(np.nanmean([_spearman(e[i], a[i]) for i in range(len(Q))]))


def adaptive(name, Xcal, Qcal, Xho, Qho, consumer, bits):
    ctx = fit_ctx(Xcal, Qcal)
    cal = {n: agree(Xcal, Qcal, consumer, f(Xcal, bits, ctx)) for n, f in CANDS.items()}
    pick = max(cal, key=cal.get)
    ho = {n: agree(Xho, Qho, consumer, f(Xho, bits, ctx)) for n, f in CANDS.items()}
    best_ho = max(ho, key=ho.get)
    print(f"{name} (consumer={consumer}, bits={bits}):", flush=True)
    print("   held-out: " + "  ".join(f"{n} {ho[n]:.3f}" for n in CANDS), flush=True)
    print(f"   -> ADAPTIVE picks '{pick}' (cal-best); held-out score {ho[pick]:.3f}"
          f"  [oracle best = '{best_ho}' {ho[best_ho]:.3f}]  match={pick==best_ho}", flush=True)


# KV-keys
from transformers import AutoTokenizer, AutoModelForCausalLM
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float16).to("cuda:0").eval()
cap = {}
model.model.layers[8].self_attn.k_proj.register_forward_hook(lambda m, i, o: cap.__setitem__("k", o.detach()))
model.model.layers[8].self_attn.q_proj.register_forward_hook(lambda m, i, o: cap.__setitem__("q", o.detach()))
text = ("The Commonwealth appeals the suppression order; we hold reasonable suspicion was lacking and affirm. ") * 60
ids = tok(text, return_tensors="pt", truncation=True, max_length=512).to("cuda:0")
with torch.no_grad():
    model(**ids)
HD = 128
K = cap["k"][0].float().cpu().numpy().reshape(-1, HD); Q = cap["q"][0].float().cpu().numpy().reshape(-1, HD)
h = len(K) // 2
adaptive("KV-keys", K[:h], Q[:64], K[h:], Q[64:128], "attention_logits", 2)

d = np.load("/home/claude/legal_cache/held.npz"); EA = d["A"].astype(float); EB = d["B"].astype(float)
h = len(EB) // 2
adaptive("LEGAL  ", EB[:h], EA[:64], EB[h:], EA[64:128], "cosine", 1)

dm = np.load("/home/claude/moral_cache/moral_ft.npz"); R = dm["Rho"].astype(float); W = dm["W"].astype(float)
wq = (W[1] - W[0])[None, :]; h = len(R) // 2
adaptive("MORAL  ", R[:h], wq, R[h:], wq, "attention_logits", 1)
