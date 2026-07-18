# Geometric Observation — GO-P-2026-026: making the omission FLOOR unconditional on a real
# Llama layer. Extends gateB_llama_rematch.py. The mismatch theorems (Appendix "The price of
# a misidentified observer", prereg GO-P-2026-024) are PROVED; this harness measures whether a
# TRAINED model's read operators exhibit the omission floor OPERATIONALLY, with the two
# projector-model assumptions removed: it uses the MEASURED read weights (eigenvalues the probe
# already computes) and the MEASURED key covariance Sigma_x = Cov(K) with the WHITENED kernel.
#
#   Floor (Thm omission):  D_floor = tr(P~ Pi),  P~ = Sx^{1/2} P Sx^{1/2},
#                          Pi = projector onto ker(Sx^{1/2} P_hat Sx^{1/2})  (whitened kernel).
#   Decisive operational gate: water-fill for the MISIDENTIFIED P_hat at rising rate; the true
#   read distortion tr(P_true Sigma_delta) and the downstream softmax-KL must FLOOR (stop
#   improving) for omission heads, while a correct-operator (P_true) control keeps improving.
#
# Two of the four conditionality bridges are already discharged by the GO-P-2026-021 probe audit
# (overlap is exactly mean-cos^2 = (1/r) tr(Pi_R Pi_R_hat); ranks matched). This harness removes
# the other two (weights, Sigma_x) and adds the operational sweep.
#
# CPU: runs the SYNTHETIC weight-recovery validation gate only (no model needed) and reports it.
# Atlas GPU 1 (CUDA_VISIBLE_DEVICES=1): also runs the Llama measurement + operational sweep.
# Pure numpy + (optionally) torch/transformers. MIT License. Governed by prereg GO-P-2026-026.
"""Is the omission distortion floor a real, rate-irreducible operational floor on trained Llama read operators?"""

from __future__ import annotations
import json
import numpy as np

R_SUB, N_PROBE, H_FD, PROBE_KEYS = 16, 160, 1e-3, 32
LAYERS = [8, 16]
MODEL = "unsloth/Llama-3.2-3B"


# ----------------------------------------------------------------------------- linear algebra
def _sym(M):
    return 0.5 * (M + M.T)

def _sqrtm_psd(M):
    w, U = np.linalg.eigh(_sym(M))
    w = np.clip(w, 0.0, None)
    return U @ np.diag(np.sqrt(w)) @ U.T

def _softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)

def _consumer(K, Qset, d):
    return _softmax((Qset @ K.T) / np.sqrt(d))

def _softmax_kl(K, Kq, Qset, d):
    p = _consumer(K, Qset, d)
    pq = _consumer(Kq, Qset, d)
    return float((p * np.log((p + 1e-12) / (pq + 1e-12))).sum(-1).mean())

def _spearman(a, b):
    """Spearman rank correlation, pure numpy (no scipy dependency)."""
    def rank(x):
        order = np.argsort(np.argsort(x))
        return order.astype(float)
    ra, rb = rank(np.asarray(a, float)), rank(np.asarray(b, float))
    ra -= ra.mean(); rb -= rb.mean()
    den = np.sqrt((ra @ ra) * (rb @ rb))
    return float(ra @ rb / den) if den > 0 else float("nan")


# ----------------------------------------------------------------------------- blind probe
def blind_probe(consumer, base_K, d, rng):
    """Recover the read operator M = sum_s J_s^T J_s from consumer(K)->p by finite-diff Jacobians.
    Returns (M, eigvals asc, eigvecs); the top-R_SUB eigvecs span R_hat, the eigvals are the
    blind read-WEIGHT estimates (the quantity the rematch harness discarded)."""
    S = base_K.shape[0]
    M = np.zeros((d, d))
    for s in rng.choice(S, min(PROBE_KEYS, S), replace=False):
        U = rng.standard_normal((N_PROBE, d))
        U /= np.linalg.norm(U, axis=1, keepdims=True) + 1e-9
        dC = np.empty((N_PROBE, consumer(base_K).size))
        for j in range(N_PROBE):
            Kp = base_K.copy(); Kp[s] = base_K[s] + H_FD * U[j]
            Km = base_K.copy(); Km[s] = base_K[s] - H_FD * U[j]
            dC[j] = (consumer(Kp).ravel() - consumer(Km).ravel()) / (2 * H_FD)
        Jt = np.linalg.pinv(U) @ dC
        M += Jt @ Jt.T
    w, V = np.linalg.eigh(_sym(M))
    return M, w, V


# ----------------------------------------------------------------------------- mismatch geometry
def rank_r_operator(w, V, r):
    """Rank-r operator from the top-r eigenpairs (the coder's estimate reads only these r modes)."""
    return V[:, -r:] @ np.diag(np.clip(w[-r:], 0.0, None)) @ V[:, -r:].T

def omission_floor(P_true, P_hat, Sx):
    """D_floor = tr(P~ Pi), Pi = projector onto the WHITENED kernel ker(Sx^{1/2} P_hat Sx^{1/2})."""
    Sh = _sqrtm_psd(Sx)
    Pt = Sh @ P_true @ Sh
    Pht = Sh @ P_hat @ Sh
    w, V = np.linalg.eigh(_sym(Pht))
    tol = 1e-9 * max(float(w.max()), 1.0)
    ker = V[:, w <= tol]
    Pi = ker @ ker.T
    return float(np.trace(Pt @ Pi)), Pi

def directed_miss(Vtrue_r, Vhat_r):
    """f_out = tr(Pi_R (I - Pi_R_hat)) / r: fraction of the true read subspace lying OUTSIDE R_hat."""
    r = Vtrue_r.shape[1]
    PiR = Vtrue_r @ Vtrue_r.T
    PiRh = Vhat_r @ Vhat_r.T
    return float(np.trace(PiR @ (np.eye(PiR.shape[0]) - PiRh)) / r)

def wf_sigma_delta(P_read, Sx, theta):
    """Water-fill error covariance for operator P_read at level theta, capped by Sx (Thm max-det).
    Sigma_delta = Sx^{1/2} V diag(min(1, theta/p_k)) V^T Sx^{1/2},  rate = 1/2 sum_{p_k>theta} ln(p_k/theta) nats."""
    Sh = _sqrtm_psd(Sx)
    Pt = _sym(Sh @ P_read @ Sh)
    p, V = np.linalg.eigh(Pt)
    p = np.clip(p, 0.0, None)
    s = np.where(p > 1e-12, np.minimum(1.0, theta / np.maximum(p, 1e-300)), 1.0)
    Sig = Sh @ (V @ np.diag(s) @ V.T) @ Sh
    active = p > theta
    rate = 0.5 * float(np.sum(np.log(p[active] / theta))) if active.any() else 0.0
    return _sym(Sig), rate


def rate_sweep(P_alloc, P_true, Sx, K, Qset, d, rng, n_levels=9, n_kl=4):
    """Sweep water levels for a coder allocating to P_alloc; report, at each rate:
    true read distortion tr(P_true Sigma_delta) and downstream softmax-KL (sampling the error)."""
    Sh = _sqrtm_psd(Sx)
    p = np.clip(np.linalg.eigvalsh(_sym(Sh @ P_alloc @ Sh)), 0.0, None)
    pmax = float(p.max()) if p.size else 1.0
    thetas = pmax * np.geomspace(0.9, 1e-3, n_levels)     # high theta -> low rate; low theta -> high rate
    out = []
    for th in thetas:
        Sig, rate = wf_sigma_delta(P_alloc, Sx, th)
        d_read = float(np.trace(P_true @ Sig))
        Ssq = _sqrtm_psd(Sig)
        kls = []
        for _ in range(n_kl):
            delta = rng.standard_normal(K.shape) @ Ssq.T       # per-token error, Cov = Sigma
            kls.append(_softmax_kl(K, K + delta.astype(K.dtype), Qset, d))
        out.append({"rate": rate, "d_read": d_read, "kl": float(np.mean(kls))})
    return out


# ----------------------------------------------------------------------------- synthetic gate
def synthetic_weight_recovery(n_instances=24, d=16, r=R_SUB, seed=7):
    """Plant a read operator via a query set (Pc_true = Q^T Q / n has planted weights); blind-probe
    it; check the recovered top-r spectrum rank-tracks the planted weights (Spearman >= 0.9).
    Guards the NEW dependency: that the probe's eigenVALUES, not just eigenvectors, are recoverable
    blind (GO-1 only claimed the subspace)."""
    rng = np.random.default_rng(seed)
    rhos = []
    for _ in range(n_instances):
        lam = np.sort(rng.uniform(0.3, 3.0, r))[::-1]                 # planted read weights
        Ud = np.linalg.qr(rng.standard_normal((d, d)))[0]
        Q = (rng.standard_normal((128, r)) * np.sqrt(lam)) @ Ud[:, :r].T   # Q^T Q/n ~ Ud diag(lam) Ud^T
        Qset = Q.astype(np.float64)
        Pc_true = Qset.T @ Qset / Qset.shape[0]
        true_w = np.sort(np.linalg.eigvalsh(Pc_true))[-r:]
        K0 = rng.standard_normal((96, d))
        cons = lambda Kx: _consumer(Kx, Qset, d)
        _, w_hat, _ = blind_probe(cons, K0, d, rng)
        rec_w = np.clip(w_hat[-r:], 0.0, None)
        rho = _spearman(true_w, rec_w)
        if np.isfinite(rho):
            rhos.append(float(rho))
    med = float(np.median(rhos)) if rhos else float("nan")
    return {"median_spearman": med, "n": len(rhos), "pass": bool(med >= 0.9)}


# ----------------------------------------------------------------------------- Llama measurement
def run_llama():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.models.llama import modeling_llama

    TEXT = ("It is a truth universally acknowledged, that a single man in possession of a good "
            "fortune, must be in want of a wife. Call me Ishmael. Some years ago, never mind how "
            "long precisely, having little or no money in my purse, I thought I would sail about a "
            "little and see the watery part of the world. The sky above the port was the color of "
            "television, tuned to a dead channel. Happy families are all alike; every unhappy "
            "family is unhappy in its own way. Many years later, as he faced the firing squad, "
            "Colonel Aureliano Buendia was to remember that distant afternoon. ")

    cap, ctr = {}, {"i": 0}
    orig = modeling_llama.apply_rotary_pos_emb
    def patched(q, k, cos, sin, *a, **kw):
        q2, k2 = orig(q, k, cos, sin, *a, **kw)
        if ctr["i"] in LAYERS:
            cap[ctr["i"]] = (q2.detach().float().cpu().numpy(), k2.detach().float().cpu().numpy())
        ctr["i"] += 1
        return q2, k2
    modeling_llama.apply_rotary_pos_emb = patched

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16).to(dev).eval()
    cfg = model.config
    d = getattr(cfg, "head_dim", cfg.hidden_size // cfg.num_attention_heads)
    n_kv = cfg.num_key_value_heads; grp = cfg.num_attention_heads // n_kv
    ids = tok(TEXT, return_tensors="pt").input_ids
    S = 256; reps = int(np.ceil((8 * S) / ids.shape[1]))
    ids = ids.repeat(1, reps)[:, :8 * S].reshape(8, S).to(dev)
    with torch.no_grad():
        model(ids)
    print(f"captured layers {list(cap)}; d={d} n_kv={n_kv} grp={grp}", flush=True)

    rows = []
    for L in LAYERS:
        q, k = cap[L]
        for h in range(n_kv):
            K = k[0, h].astype(np.float64)
            Qset = q[0, h * grp:(h + 1) * grp].reshape(-1, d).astype(np.float64)
            Pc_true = Qset.T @ Qset / Qset.shape[0]                 # true (full) read operator P
            Sx = np.cov(K, rowvar=False) + 1e-6 * np.eye(d)         # measured key covariance
            wt, Vt = np.linalg.eigh(_sym(Pc_true)); Vtrue_r = Vt[:, -R_SUB:]
            rng = np.random.default_rng(3000 + 1000 * L + h)
            cons = lambda Kx: _consumer(Kx, Qset, d)
            _, wh, Vh = blind_probe(cons, K, d, rng)
            Vhat_r = Vh[:, -R_SUB:]
            P_hat_r = rank_r_operator(wh, Vh, R_SUB)               # coder's rank-r estimate
            overlap = float(((Vhat_r.T @ Vtrue_r) ** 2).sum() / R_SUB)   # mean-cos^2 (audited)
            f_out = directed_miss(Vtrue_r, Vhat_r)
            D_floor, _ = omission_floor(Pc_true, P_hat_r, Sx)      # whitened-kernel, measured weights
            naive = float(np.trace(Pc_true @ (np.eye(d) - Vhat_r @ Vhat_r.T)))   # naive (Sx=I) reading
            sweep_hat = rate_sweep(P_hat_r, Pc_true, Sx, K, Qset, d, rng)         # misidentified
            sweep_ok = rate_sweep(Pc_true, Pc_true, Sx, K, Qset, d, rng)          # correct-operator control
            # floored? true read distortion at highest rate ~ D_floor; KL stops improving under P_hat
            d_read_hi = sweep_hat[-1]["d_read"]
            kl_mid, kl_hi = sweep_hat[len(sweep_hat) // 2]["kl"], sweep_hat[-1]["kl"]
            kl_improve_hat = (kl_mid - kl_hi) / (kl_mid + 1e-12)
            kl_ok_hi = sweep_ok[-1]["kl"]
            rows.append({"layer": L, "head": h, "overlap": overlap, "f_out": f_out,
                         "D_floor": D_floor, "D_floor_naive": naive,
                         "d_read_highrate": d_read_hi,
                         "floor_reached": bool(abs(d_read_hi - D_floor) <= max(0.5 * D_floor, 1e-9)),
                         "kl_improve_pastsat_hat": float(kl_improve_hat),
                         "kl_highrate_hat": kl_hi, "kl_highrate_correct": kl_ok_hi,
                         "omission": bool(D_floor > 1e-6),
                         "sweep_hat": sweep_hat, "sweep_correct": sweep_ok})
            print(f"L{L} h{h} overlap={overlap:.3f} f_out={f_out:.3f} D_floor={D_floor:.3e} "
                  f"(naive {naive:.3e}) d_read_hi={d_read_hi:.3e} KLimprove={kl_improve_hat:+.2f} "
                  f"KL_hat={kl_hi:.2e} KL_correct={kl_ok_hi:.2e}", flush=True)
    return rows, d


# ----------------------------------------------------------------------------- main
def main():
    print("=" * 74)
    print("[synthetic] blind read-WEIGHT recovery gate (must pass before trusting Llama numbers)")
    print("=" * 74)
    synth = synthetic_weight_recovery()
    print(f"  median Spearman(true weights, recovered spectrum) = {synth['median_spearman']:.3f} "
          f"over {synth['n']} planted operators  -> {'PASS' if synth['pass'] else 'FAIL'} (bar 0.9)")

    out = {"claim": "GO-P-2026-026: omission floor made unconditional on trained Llama read operators",
           "prereg": "GO-P-2026-026", "model": MODEL, "synthetic_weight_recovery": synth}

    try:
        import torch  # noqa
        have_cuda = torch.cuda.is_available()
    except Exception:
        have_cuda = False

    if have_cuda:
        print("\n" + "=" * 74)
        print("[llama] measured weighted floor + operational rate sweep (Atlas GPU 1)")
        print("=" * 74)
        rows, d = run_llama()
        om = [r for r in rows if r["omission"]]
        n_om = len(om)
        # DECISIVE operational gate, over omission heads:
        floor_hits = sum(1 for r in om if r["floor_reached"])
        kl_floored = sum(1 for r in om if r["kl_improve_pastsat_hat"] < 0.20)
        kl_beats_correct = sum(1 for r in om if r["kl_highrate_hat"] > 2 * r["kl_highrate_correct"])
        med_floor = float(np.median([r["D_floor"] for r in rows])) if rows else 0.0
        verdict = {
            "weight_recovery_ok": synth["pass"],
            "floor_reached_frac": (floor_hits, n_om),
            "kl_floored_frac": (kl_floored, n_om),
            "kl_beats_correct_frac": (kl_beats_correct, n_om),
            "operational_floor_supported": bool(
                synth["pass"] and n_om > 0
                and floor_hits >= np.ceil(0.75 * n_om)
                and kl_floored >= np.ceil(0.75 * n_om)
                and kl_beats_correct >= np.ceil(0.75 * n_om)),
        }
        out.update({"n_instances": len(rows), "n_omission": n_om,
                    "median_D_floor": med_floor, "rows": rows, "verdict": verdict})
        out["GateB_weighted_floor_supported"] = verdict["operational_floor_supported"]
        print("===GATEBWF-JSON==="); print(json.dumps(out, indent=2)); print("===END===")
        print("\nVERDICT:", "ALL PASS" if out["GateB_weighted_floor_supported"] else
              f"NOT SUPPORTED (see verdict: {verdict})")
    else:
        out["note"] = "CPU run: synthetic weight-recovery gate only; Llama measurement needs Atlas GPU 1."
        print("\n[llama] SKIPPED (no CUDA). Run on Atlas GPU 1 for the operational floor gate.")
        print("===GATEBWF-JSON==="); print(json.dumps(out, indent=2)); print("===END===")
        print("\nVERDICT:", "SYNTHETIC GATE PASS (Llama pending Atlas)" if synth["pass"]
              else "SYNTHETIC GATE FAIL")


if __name__ == "__main__":
    main()
