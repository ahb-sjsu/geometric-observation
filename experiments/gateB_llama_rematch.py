# Geometric Observation — Gate B REMATCH: recon-matched dissociation on a REAL Llama layer.
# Governed by prereg/GO-P-2026-021 (sealed; registered commit is the binding timestamp).
# Fixes NEG-12: GO-P-2026-020's registered quantizer pair was NOT reconstruction-matched,
# so plain reconstruction predicted the winner for free and proj_beats_recon could not fire.
# Here the two key-error arms are RECON-MATCHED BY CONSTRUCTION (identical per-token ||delta||,
# exact to machine precision) but differ in read-subspace content: arm A places the error in
# the top-r read subspace, arm B in its orthogonal complement. Reconstruction is therefore
# provably blind (tie); only the consumer-projected predictor tr(hat_P_C Sigma_delta) can
# resolve the flip. Blind probe recovers hat_P_C; ground truth is the real softmax-KL.
# Runs on Atlas GPU 1 (CUDA_VISIBLE_DEVICES=1). MIT License.
"""Does a blind probe on a real Llama layer predict a reconstruction-invisible key-error flip?"""

from __future__ import annotations
import json
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.llama import modeling_llama

MODEL = "unsloth/Llama-3.2-3B"
LAYERS = [8, 16]
R_SUB, N_PROBE, H_FD = 16, 160, 1e-3
PROBE_KEYS = 32                      # up from 12 in GO-P-2026-020 (better hat_P_C fidelity)
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
    return _softmax((Qset @ K.T) / np.sqrt(d))

def _blind_probe(consumer, base_K, d, rng):
    """Recover read operator from consumer(K)->p by finite-diff Jacobian on key perturbations."""
    S = base_K.shape[0]
    M = np.zeros((d, d))
    probe_keys = rng.choice(S, min(PROBE_KEYS, S), replace=False)
    for s in probe_keys:
        U = rng.standard_normal((N_PROBE, d)); U /= np.linalg.norm(U, axis=1, keepdims=True) + 1e-9
        base = consumer(base_K).ravel()
        dC = np.empty((N_PROBE, base.size))
        for j in range(N_PROBE):
            Kp = base_K.copy(); Kp[s] = base_K[s] + H_FD * U[j]
            Km = base_K.copy(); Km[s] = base_K[s] - H_FD * U[j]
            dC[j] = (consumer(Kp).ravel() - consumer(Km).ravel()) / (2 * H_FD)
        Jt = np.linalg.pinv(U) @ dC
        M += Jt @ Jt.T
    w, V = np.linalg.eigh(M)
    return M, V[:, -R_SUB:]

def _overlap(U, Vt):
    return float(((U.T @ Vt) ** 2).sum() / U.shape[1])

def _across_item_cov(delta):
    dd = delta - delta.mean(0, keepdims=True)
    return dd.T @ dd / dd.shape[0]

def _softmax_kl(K, Kq, Qset, d):
    p = _consumer(K, Qset, d); pq = _consumer(Kq, Qset, d)
    return float((p * np.log((p + 1e-12) / (pq + 1e-12))).sum(-1).mean())

def _recon_matched_arms(K, Vtrue, d):
    """Two key-error arms with IDENTICAL per-token norm but opposite read-subspace content.
    Base magnitude = real per-channel 4-bit quant error; arm A -> read subspace, B -> complement."""
    g = _uniform_asym(K, axis=0) - K              # realistic per-token error magnitude
    r = np.linalg.norm(g, axis=1, keepdims=True)  # (S,1) per-token norm to preserve
    Pread = Vtrue @ Vtrue.T                        # (d,d) projector onto top-r read subspace
    Pperp = np.eye(d) - Pread
    v_top, v_bot = Vtrue[:, -1], Vtrue[:, 0]       # top / (a complement) eigvec fallback
    def _place(P, vfb):
        comp = g @ P.T                             # (S,d) component of g in subspace
        n = np.linalg.norm(comp, axis=1, keepdims=True)
        u = np.where(n > 1e-8, comp / (n + 1e-12), vfb[None, :])
        return (r * u).astype(np.float32)
    dA = _place(Pread, v_top)                       # error in read subspace
    dB = _place(Pperp, v_bot)                       # error in complement
    return dA, dB


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
        q, k = _cap[L]
        b = 0
        for h in range(n_kv):
            K = k[b, h].astype(np.float32)
            Qset = q[b, h * grp:(h + 1) * grp].reshape(-1, d).astype(np.float32)
            Pc_true = Qset.T @ Qset / Qset.shape[0]
            _, Vtrue = np.linalg.eigh(Pc_true); Vtrue = Vtrue[:, -R_SUB:]
            cons = lambda Kx: _consumer(Kx, Qset, d)
            rng = np.random.default_rng(2000 + 1000 * L + h)
            Phat, Vhat = _blind_probe(cons, K, d, rng)
            overlap = _overlap(Vhat, Vtrue)
            chance = _overlap(np.linalg.qr(rng.standard_normal((d, R_SUB)))[0], Vtrue)
            # recon-matched arms
            dA, dB = _recon_matched_arms(K, Vtrue, d)
            SdA, SdB = _across_item_cov(dA), _across_item_cov(dB)
            pred_A, pred_B = float(np.trace(Phat @ SdA)), float(np.trace(Phat @ SdB))
            kl_A, kl_B = _softmax_kl(K, K + dA, Qset, d), _softmax_kl(K, K + dB, Qset, d)
            rec_A = float((np.linalg.norm(dA, axis=1) / (np.linalg.norm(K, axis=1) + 1e-8)).mean())
            rec_B = float((np.linalg.norm(dB, axis=1) / (np.linalg.norm(K, axis=1) + 1e-8)).mean())
            rel_kl_gap = abs(kl_A - kl_B) / (0.5 * (kl_A + kl_B) + 1e-12)
            rows.append({"layer": L, "head": h, "overlap": overlap, "chance": chance,
                         "pred_A": pred_A, "pred_B": pred_B, "kl_A": kl_A, "kl_B": kl_B,
                         "recon_A": rec_A, "recon_B": rec_B, "rel_kl_gap": rel_kl_gap})
            print(f"L{L} h{h} overlap={overlap:.3f} predA-B={pred_A-pred_B:+.2e} "
                  f"klA-B={kl_A-kl_B:+.2e} reconGap={abs(rec_A-rec_B):.1e}", flush=True)

    n = len(rows)
    med_overlap = float(np.median([r["overlap"] for r in rows]))
    med_chance = float(np.median([r["chance"] for r in rows]))
    recon_gap_max = float(max(abs(r["recon_A"] - r["recon_B"]) for r in rows))
    med_rel_kl_gap = float(np.median([r["rel_kl_gap"] for r in rows]))
    # winner = arm with the LARGER downstream KL (worse); predict via LARGER projected trace
    proj_hits = sum(1 for r in rows
                    if np.sign(r["pred_A"] - r["pred_B"]) == np.sign(r["kl_A"] - r["kl_B"]))
    recon_hits = sum(1 for r in rows
                     if np.sign(r["recon_A"] - r["recon_B"]) == np.sign(r["kl_A"] - r["kl_B"]))
    verdict = {
        "recon_tied": bool(recon_gap_max <= 1e-6),
        "arms_downstream_distinct": bool(med_rel_kl_gap >= 0.5),
        "blind_predicts_winner": bool(proj_hits >= np.ceil(0.75 * n)),
        "proj_beats_recon": bool(proj_hits > recon_hits),
        "probe_recovery_diag": bool(med_overlap >= 0.60),   # DIAGNOSTIC (reported, not gating)
    }
    out = {"claim": "Gate B rematch: recon-matched dissociation on Llama-3.2-3B",
           "prereg": "GO-P-2026-021", "model": MODEL, "n_instances": n,
           "median_overlap": med_overlap, "median_chance": med_chance,
           "recon_gap_max": recon_gap_max, "median_rel_kl_gap": med_rel_kl_gap,
           "proj_hits": proj_hits, "recon_hits": recon_hits, "rows": rows, "verdict": verdict}
    # Gate = recon provably tied AND arms genuinely differ downstream AND blind projection predicts.
    out["GateB_rematch_supported"] = bool(verdict["recon_tied"]
                                          and verdict["arms_downstream_distinct"]
                                          and verdict["blind_predicts_winner"]
                                          and verdict["proj_beats_recon"])
    print("===GATEB2-JSON==="); print(json.dumps(out, indent=2)); print("===END===")


if __name__ == "__main__":
    main()
