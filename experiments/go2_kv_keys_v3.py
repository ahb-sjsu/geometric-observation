# Geometric Observation — GO-2 (quotient-(A2) transfer) on attention keys, v3.
# Governed by prereg/GO-P-2026-003 (sealed afcc7ac6; registered commit 07d0201).
# Tests GO-2's POSITIVE half: the query-projected across-token variance of the
# logit kick, Var_s(q.delta), controls softmax-KL -- the quantity a magnitude
# scalar could not see (NEG-6). MIT License.
"""GO-2 v3 on the KV-attention-keys instance.

Same four bit-matched arms as v2 (a per-channel invariant-preserving; b per-token
whole-vector invariant-blind; c polar anti-probe; d per-channel uniform). Two
changes:
  1. Tangential quantity is query-projected + across-token:
       tang_qproj = mean_{q,h} Var_s(q.delta_{h,s}) / Var_s(q.k0_{h,s})
     (relative across-token variance of the logit perturbation), NOT a norm.
  2. Structured consumer: queries live in the top-16 singular subspace of each
     head's clean keys. Specificity control = a shift-sensitive LINEAR readout
     (relative MSE of raw logits q.k); the a-vs-b gap must collapse there.

Emits ===GO2V3-JSON=== ... ===END===.
"""

from __future__ import annotations

import json

import numpy as np
from turboquant_pro import PerChannelKV

H, D = 8, 128
SEEDS = 12
S_TEST, N_Q, R_SUB = 512, 128, 16
ARMS = ["a_demean_perchan_asym4", "b_wholevec_pertoken_uniform4", "c_polarquant", "d_perchan_uniform4"]

EFF_BITS = {
    "a_demean_perchan_asym4": 4.0 + 2 * 16 / S_TEST,
    "b_wholevec_pertoken_uniform4": 4.0 + 2 * 16 / D,
    "c_polarquant": 4.0 + 1 * 16 / D,
    "d_perchan_uniform4": 4.0 + 2 * 16 / S_TEST,
}


def _keys(S, seed, H=H, D=D):
    r = np.random.default_rng(seed)
    dc = np.random.default_rng(1000 + seed).uniform(-6, 6, (H, D)).astype(np.float32)
    sc = np.random.default_rng(2000 + seed).uniform(0.2, 1.5, (H, D)).astype(np.float32)
    t = r.standard_t(3, (1, H, S, D)).astype(np.float32)
    return (dc[None, :, None, :] + sc[None, :, None, :] * t).astype(np.float32)


def _structured_queries(k0, seed, r=R_SUB):
    """Per head, unit queries in the top-r right-singular subspace of the clean keys."""
    rng = np.random.default_rng(500 + seed)
    Q = np.empty((N_Q, H, D), dtype=np.float32)
    for h in range(H):
        # right singular vectors of k0[h] (S,D): columns of V are D-space directions
        _, _, Vt = np.linalg.svd(k0[h] - k0[h].mean(0, keepdims=True), full_matrices=False)
        Vr = Vt[:r]  # (r, D)
        coeff = rng.standard_normal((N_Q, r)).astype(np.float32)
        q = coeff @ Vr  # (N_Q, D)
        q /= np.linalg.norm(q, axis=1, keepdims=True) + 1e-8
        Q[:, h, :] = q
    return Q


def _iso_queries(seed):
    q = np.random.default_rng(300 + seed).standard_normal((N_Q, H, D)).astype(np.float32)
    return q / (np.linalg.norm(q, axis=-1, keepdims=True) + 1e-8)


def _uniform_asym(x, axis, bits=4):
    q = 2**bits - 1
    lo = x.min(axis=axis, keepdims=True)
    hi = x.max(axis=axis, keepdims=True)
    scale = np.where((hi - lo) > 0, (hi - lo) / q, 1.0)
    idx = np.clip(np.round((x - lo) / scale), 0, q)
    return (lo + idx * scale).astype(np.float32)


def _polar_antiprobe(x, bits=4):
    nrm = np.linalg.norm(x, axis=-1, keepdims=True) + 1e-8
    u = x / nrm
    q = 2**bits - 1
    uq = np.clip(np.round((u * 0.5 + 0.5) * q), 0, q) / q * 2 - 1
    return (uq * nrm).astype(np.float32)


def _arm_recon(arm, test):
    k0 = test[0]
    if arm == "a_demean_perchan_asym4":
        qz = PerChannelKV(head_dim=D, n_heads=H, nf4_asym=True, outlier_frac=0.0)
        return qz.decompress(qz.compress(test))[0]
    if arm == "b_wholevec_pertoken_uniform4":
        return _uniform_asym(k0, axis=2)
    if arm == "c_polarquant":
        return _polar_antiprobe(k0)
    if arm == "d_perchan_uniform4":
        qz = PerChannelKV(head_dim=D, n_heads=H, bits=4, outlier_frac=0.0)
        return qz.decompress(qz.compress(test))[0]
    raise ValueError(arm)


def _softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def _logits(Q, k):
    return np.einsum("qhd,hsd->qhs", Q, k) / np.sqrt(D)  # (N_Q, H, S)


def _kl(l0, lr):
    p0, pr = _softmax(l0), _softmax(lr)
    return float((p0 * np.log((p0 + 1e-12) / (pr + 1e-12))).sum(-1).mean())


def main():
    rows = []
    floor = []
    for seed in range(SEEDS):
        test = _keys(S_TEST, 100 + seed)
        k0 = test[0]
        Qs = _structured_queries(k0, seed)
        Qi = _iso_queries(seed)
        l0s, l0i = _logits(Qs, k0), _logits(Qi, k0)
        floor.append(_kl(l0s, _logits(Qs, k0.astype(np.float16).astype(np.float32))))
        for arm in ARMS:
            kr = _arm_recon(arm, test)
            delta = kr - k0
            recon = float((np.linalg.norm(delta, axis=-1) / (np.linalg.norm(k0, axis=-1) + 1e-8)).mean())
            lrs, lri = _logits(Qs, kr), _logits(Qi, kr)
            dl = lrs - l0s  # (N_Q, H, S) logit kick, structured bank
            # query-projected across-token variance, relative to signal logit variance
            tang_qproj = float((dl.var(axis=2) / (l0s.var(axis=2) + 1e-8)).mean())
            # shift-sensitive linear readout: relative logit MSE (structured bank)
            relmse_lin = float((dl**2).mean() / ((l0s**2).mean() + 1e-8))
            rows.append({
                "arm": arm, "seed": seed, "recon": recon, "tang": tang_qproj,
                "kl": _kl(l0s, lrs), "kl_iso": _kl(l0i, lri), "relmse_lin": relmse_lin,
            })

    def med(arm, key):
        return float(np.median([r[key] for r in rows if r["arm"] == arm]))

    med_kl = {a: med(a, "kl") for a in ARMS}
    med_recon = {a: med(a, "recon") for a in ARMS}
    med_tang = {a: med(a, "tang") for a in ARMS}
    a, b, c = "a_demean_perchan_asym4", "b_wholevec_pertoken_uniform4", "c_polarquant"

    kl = np.array([r["kl"] for r in rows])
    tg = np.array([r["tang"] for r in rows])
    rc = np.array([r["recon"] for r in rows])

    def z(v):
        return (v - v.mean()) / (v.std() + 1e-12)

    zt, zr, zk = z(tg), z(rc), z(kl)

    def r2(mat):
        X = np.column_stack(mat + [np.ones_like(kl)])
        beta, *_ = np.linalg.lstsq(X, zk, rcond=None)
        resid = zk - X @ beta
        return 1 - resid.var() / zk.var(), beta

    full, beta_full = r2([zt, zr])
    pr_tang = full - r2([zr])[0]
    pr_recon = full - r2([zt])[0]

    by_seed = {}
    for r in rows:
        by_seed.setdefault(r["seed"], {})[r["arm"]] = r
    a_lt_b = sum(1 for s in by_seed.values() if s[a]["kl"] < s[b]["kl"])

    gap_softmax = med_kl[b] / med_kl[a]
    gap_linear = med(b, "relmse_lin") / med(a, "relmse_lin")
    gap_iso = med(b, "kl_iso") / med(a, "kl_iso")

    eff = {ar: round(EFF_BITS[ar], 4) for ar in ARMS}
    eff_spread = max(eff.values()) - min(eff.values())

    verdict = {
        "audit_pass": bool(eff_spread <= 0.5),
        "dominance": bool((pr_tang - pr_recon) >= 0.10),
        "c_gap": bool((med_kl[c] / med_kl[a]) >= 5.0),
        "a_lt_b_consistent": bool(a_lt_b >= 10),
        "specificity": bool(gap_softmax >= 1.5 and gap_linear <= 1.25),
    }
    result = {
        "claim": "GO-2 kv-keys v3", "prereg": "GO-P-2026-003", "instance": "post-RoPE keys / structured softmax",
        "n_seeds": SEEDS, "arms": ARMS,
        "effective_bits": eff, "eff_bits_spread": round(eff_spread, 4),
        "median_kl": med_kl, "median_recon": med_recon, "median_tang_qproj": med_tang,
        "c_gap": med_kl[c] / med_kl[a], "a_lt_b_seeds": f"{a_lt_b}/{SEEDS}",
        "std_coef_tang": float(beta_full[0]), "std_coef_recon": float(beta_full[1]),
        "partial_r2_tang_qproj": float(pr_tang), "partial_r2_recon": float(pr_recon),
        "dominance_margin": float(pr_tang - pr_recon),
        "noise_floor_kl": float(np.median(floor)),
        "gap_softmax": gap_softmax, "gap_linear_shiftsensitive": gap_linear, "gap_softmax_isotropic": gap_iso,
        "bars": {"eff_bits_spread_le": 0.5, "dominance_ge": 0.10, "c_gap_ge": 5.0,
                 "a_lt_b_ge": 10, "gap_softmax_ge": 1.5, "gap_linear_le": 1.25},
        "verdict": verdict,
    }
    result["GO2_positive_supported"] = all(verdict.values())
    print("===GO2V3-JSON===")
    print(json.dumps(result, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
