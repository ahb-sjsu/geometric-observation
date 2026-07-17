# Geometric Observation — Gate B (book): blind probe on a REAL Llama attention layer.
# Governed by prereg/GO-P-2026-020 (sealed 5cbffe27; registered commit 907d55a).
# PROSPECTIVE, real-model. Runs on Atlas GPU 1 (CUDA_VISIBLE_DEVICES=1). Recovers the
# read operator (query second moment) from the softmax consumer by a BLIND finite-
# difference probe, predicts the winning key-quantizer via tr(hat_P_C Sigma_delta),
# and verifies against the head's actual softmax-KL. MIT License.
"""Does the blind probe recover a real Llama layer's read operator and predict the winner?"""

from __future__ import annotations
import json
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.llama import modeling_llama

MODEL = "unsloth/Llama-3.2-3B"
LAYERS = [8, 16]
R_SUB, N_PROBE, H_FD, KREC = 16, 160, 1e-3, None  # N_PROBE>d=128 for the Jacobian solve
torch.manual_seed(0)

TEXT = (
    "It is a truth universally acknowledged, that a single man in possession of a good "
    "fortune, must be in want of a wife. However little known the feelings or views of "
    "such a man may be on his first entering a neighbourhood, this truth is so well fixed "
    "in the minds of the surrounding families, that he is considered as the rightful "
    "property of some one or other of their daughters. Call me Ishmael. Some years ago, "
    "never mind how long precisely, having little or no money in my purse, and nothing "
    "particular to interest me on shore, I thought I would sail about a little and see the "
    "watery part of the world. Whenever I find myself growing grim about the mouth; "
    "whenever it is a damp, drizzly November in my soul, then I account it high time to get "
    "to sea as soon as I can. The sky above the port was the color of television, tuned to "
    "a dead channel. All this happened, more or less. The war parts, anyway, are pretty "
    "much true. Happy families are all alike; every unhappy family is unhappy in its own "
    "way. In the beginning the Universe was created. This has made a lot of people very "
    "angry and been widely regarded as a bad move. Many years later, as he faced the "
    "firing squad, Colonel Aureliano Buendia was to remember that distant afternoon when "
    "his father took him to discover ice. "
)

_cap = {}
_ctr = {"i": 0}
_orig_rope = modeling_llama.apply_rotary_pos_emb
def _patched_rope(q, k, cos, sin, *a, **kw):
    q2, k2 = _orig_rope(q, k, cos, sin, *a, **kw)
    i = _ctr["i"]
    if i in LAYERS:
        _cap[i] = (q2.detach().float().cpu().numpy(), k2.detach().float().cpu().numpy())
    _ctr["i"] += 1
    return q2, k2
modeling_llama.apply_rotary_pos_emb = _patched_rope


def _softmax(z):
    z = z - z.max(-1, keepdims=True); e = np.exp(z); return e / e.sum(-1, keepdims=True)

def _uniform_asym(x, axis, bits=4):
    q = 2**bits - 1
    lo, hi = x.min(axis, keepdims=True), x.max(axis, keepdims=True)
    sc = np.where((hi - lo) > 0, (hi - lo) / q, 1.0)
    return (lo + np.clip(np.round((x - lo) / sc), 0, q) * sc).astype(np.float32)

def _consumer(K, Qset, d):
    """softmax attention outputs for each query over key set K (Mq, S)."""
    return _softmax((Qset @ K.T) / np.sqrt(d))

def _blind_probe(Kfn_shape, consumer, base_K, d, rng):
    """Recover read operator from consumer(K)->p by finite-diff Jacobian on key perturbations."""
    S = base_K.shape[0]
    M = np.zeros((d, d))
    probe_keys = rng.choice(S, min(12, S), replace=False)
    for s in probe_keys:
        U = rng.standard_normal((N_PROBE, d)); U /= np.linalg.norm(U, axis=1, keepdims=True) + 1e-9
        dC = np.empty((N_PROBE, consumer(base_K).size))
        base = consumer(base_K).ravel()
        for j in range(N_PROBE):
            Kp = base_K.copy(); Kp[s] = base_K[s] + H_FD * U[j]
            Km = base_K.copy(); Km[s] = base_K[s] - H_FD * U[j]
            dC[j] = (consumer(Kp).ravel() - consumer(Km).ravel()) / (2 * H_FD)
        Jt = np.linalg.pinv(U) @ dC            # (d, out)
        M += Jt @ Jt.T
    w, V = np.linalg.eigh(M)
    return M, V[:, -R_SUB:]                     # recovered operator, top-r eigvecs

def _overlap(U, Vt):
    return float(((U.T @ Vt) ** 2).sum() / U.shape[1])

def _across_item_cov(delta):
    dd = delta - delta.mean(0, keepdims=True)
    return dd.T @ dd / dd.shape[0]

def _softmax_kl(K, Kq, Qset, d):
    p = _consumer(K, Qset, d); pq = _consumer(Kq, Qset, d)
    return float((p * np.log((p + 1e-12) / (pq + 1e-12))).sum(-1).mean())


def main():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16).to(dev).eval()
    cfg = model.config
    d = getattr(cfg, "head_dim", cfg.hidden_size // cfg.num_attention_heads)
    n_kv = cfg.num_key_value_heads; grp = cfg.num_attention_heads // n_kv
    ids = tok(TEXT, return_tensors="pt").input_ids
    S = 256
    reps = int(np.ceil((8 * S) / ids.shape[1]))
    ids = ids.repeat(1, reps)[:, :8 * S].reshape(8, S).to(dev)
    _ctr["i"] = 0; _cap.clear()
    with torch.no_grad():
        model(ids)
    print(f"captured layers {list(_cap)}; d={d} n_kv={n_kv} grp={grp}", flush=True)

    rows = []
    for L in LAYERS:
        q, k = _cap[L]                          # q:(8,n_heads,S,d) k:(8,n_kv,S,d)
        b = 0
        for h in range(n_kv):
            K = k[b, h].astype(np.float32)       # (S,d) keys = representation
            Qset = q[b, h * grp:(h + 1) * grp].reshape(-1, d).astype(np.float32)  # (grp*S, d)
            Pc_true = Qset.T @ Qset / Qset.shape[0]
            _, Vtrue = np.linalg.eigh(Pc_true); Vtrue = Vtrue[:, -R_SUB:]
            cons = lambda Kx: _consumer(Kx, Qset, d)
            rng = np.random.default_rng(1000 * L + h)
            Phat, Vhat = _blind_probe(K.shape, cons, K, d, rng)
            overlap = _overlap(Vhat, Vtrue)
            chance = _overlap(np.linalg.qr(rng.standard_normal((d, R_SUB)))[0], Vtrue)
            # quantizers
            Ka = _uniform_asym(K, axis=0)        # per-channel (per-dim over tokens)
            Kb = _uniform_asym(K, axis=1)        # per-token (whole-vector over dims)
            Sda, Sdb = _across_item_cov(Ka - K), _across_item_cov(Kb - K)
            pred_a, pred_b = float(np.trace(Phat @ Sda)), float(np.trace(Phat @ Sdb))
            kl_a, kl_b = _softmax_kl(K, Ka, Qset, d), _softmax_kl(K, Kb, Qset, d)
            rec_a = float((np.linalg.norm(Ka - K, axis=1) / (np.linalg.norm(K, axis=1) + 1e-8)).mean())
            rec_b = float((np.linalg.norm(Kb - K, axis=1) / (np.linalg.norm(K, axis=1) + 1e-8)).mean())
            rows.append({"layer": L, "head": h, "overlap": overlap, "chance": chance,
                         "pred_adv_b_minus_a": pred_b - pred_a, "kl_adv_b_minus_a": kl_b - kl_a,
                         "recon_adv_b_minus_a": rec_b - rec_a, "kl_a": kl_a, "kl_b": kl_b})
            print(f"L{L} h{h} overlap={overlap:.3f} predΔ={pred_b-pred_a:+.2e} klΔ={kl_b-kl_a:+.2e} reconΔ={rec_b-rec_a:+.3f}", flush=True)

    n = len(rows)
    med_overlap = float(np.median([r["overlap"] for r in rows]))
    med_chance = float(np.median([r["chance"] for r in rows]))
    proj_hits = sum(1 for r in rows if np.sign(r["pred_adv_b_minus_a"]) == np.sign(r["kl_adv_b_minus_a"]))
    recon_hits = sum(1 for r in rows if np.sign(r["recon_adv_b_minus_a"]) == np.sign(r["kl_adv_b_minus_a"]))
    verdict = {
        "probe_recovery": bool(med_overlap >= 0.60),
        "blind_predicts_winner": bool(proj_hits >= np.ceil(0.75 * n)),
        "proj_beats_recon": bool(proj_hits > recon_hits),
    }
    out = {"claim": "Gate B: Observation Theory on Llama-3.2-3B", "prereg": "GO-P-2026-020",
           "model": MODEL, "n_instances": n, "median_overlap": med_overlap, "median_chance": med_chance,
           "proj_hits": proj_hits, "recon_hits": recon_hits, "rows": rows, "verdict": verdict}
    out["GateB_supported"] = all(verdict.values())
    print("===GATEB-JSON==="); print(json.dumps(out, indent=2)); print("===END===")


if __name__ == "__main__":
    main()
