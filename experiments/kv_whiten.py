import os, sys, numpy as np, torch, warnings
warnings.filterwarnings("ignore")
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
sys.path.insert(0, "/home/claude/tqp")
from a2_probe_std import _consumer_scores, _spearman, _polar_proxy, _per_channel_proxy, displacement_decomposition


def whiten_fit(K):                       # ZCA / SPD-natural whitening (geometric-methods ch04/ch15)
    mu = K.mean(0); C = K - mu; cov = (C.T @ C) / len(C)
    cov = cov + 1e-2 * (np.trace(cov) / K.shape[1]) * np.eye(K.shape[1])
    w, V = np.linalg.eigh(cov); w = np.maximum(w, 1e-12)
    Wm = V @ np.diag(1.0 / np.sqrt(w)) @ V.T
    Wi = V @ np.diag(np.sqrt(w)) @ V.T
    return mu, Wm, Wi


def whitened_uniform(K, mu, Wm, Wi, bits):
    Kw = (K - mu) @ Wm
    lo, hi = Kw.min(0, keepdims=True), Kw.max(0, keepdims=True)
    step = np.maximum((hi - lo) / (2 ** bits - 1), 1e-30)
    return (np.round((Kw - lo) / step) * step + lo) @ Wi + mu


def agree(data, queries, consumer, qdata):
    exact = _consumer_scores(data, queries, consumer)
    approx = _consumer_scores(qdata, queries, consumer)
    return float(np.nanmean([_spearman(exact[i], approx[i]) for i in range(len(queries))]))


def compare(name, data, queries, consumer, bits):
    rng = np.random.default_rng(0)
    mu, Wm, Wi = whiten_fit(data)
    dd = displacement_decomposition(data)
    p = agree(data, queries, consumer, _polar_proxy(data, bits, rng))
    pc = agree(data, queries, consumer, _per_channel_proxy(data, bits))
    wu = agree(data, queries, consumer, whitened_uniform(data, mu, Wm, Wi, bits))
    wp = agree(data, queries, consumer, _polar_proxy((data - mu) @ Wm, bits, rng) @ Wi + mu)  # whitened THEN polar
    print(f"{name} (unit_disp {dd['median_tangential_fraction']:.2f}t, bits={bits}): "
          f"polar {p:.3f} | per_channel {pc:.3f} | WHITENED-uniform {wu:.3f} | whitened-polar {wp:.3f}", flush=True)


# ---- KV-keys: extract real post-projection keys/queries from Qwen ----
from transformers import AutoTokenizer, AutoModelForCausalLM
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float16).to("cuda:0").eval()
cap = {}
model.model.layers[8].self_attn.k_proj.register_forward_hook(lambda m, i, o: cap.__setitem__("k", o.detach()))
model.model.layers[8].self_attn.q_proj.register_forward_hook(lambda m, i, o: cap.__setitem__("q", o.detach()))
text = ("The Commonwealth appeals from the order granting the motion to suppress evidence. "
        "We hold that reasonable suspicion did not support the stop, and affirm. ") * 40
ids = tok(text, return_tensors="pt", truncation=True, max_length=512).to("cuda:0")
with torch.no_grad():
    model(**ids)
HD = 128
K = cap["k"][0].float().cpu().numpy().reshape(-1, HD)
Q = cap["q"][0].float().cpu().numpy().reshape(-1, HD)
print(f"Qwen L8 keys {K.shape} queries {Q.shape}", flush=True)
compare("KV-keys (attention_logits)", K, Q[:64], "attention_logits", bits=2)

# ---- legal ----
d = np.load("/home/claude/legal_cache/held.npz"); EA = d["A"].astype(float); EB = d["B"].astype(float)
compare("LEGAL     (cosine)         ", EB, EA[:64], "cosine", bits=1)
