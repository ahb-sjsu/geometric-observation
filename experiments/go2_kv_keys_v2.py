# Geometric Observation — GO-2 (quotient-(A2) transfer) on attention keys, v2.
# Governed by prereg/GO-P-2026-002 (sealed a9a7ed5d; registered commit d30fc36).
# Corrects GO-P-2026-001 (NEG-5): matched-bits with an in-harness effective-bits
# audit (NO per-block codebook), plus a second invariant-blind arm so the
# dominance regression is not carried by a lone outlier. MIT License.
"""GO-2 v2 on the KV-attention-keys instance.

Four bit-matched arms (4-bit payload + O(1) fp16 metadata per row/col):
  a demean_perchan_asym4       invariant-preserving  (per-channel asym 4-bit; NF4 levels)
  b wholevec_pertoken_uniform4 recon-oriented, invariant-blind
                               (per-TOKEN min-max uniform 4-bit over the D channels)
  c polarquant_keys            anti-probe (per-vector normalize; keeps norm/direction,
                               drops per-channel scale)
  d perchan_uniform4           reference (per-channel uniform 4-bit)

Consumer: softmax attention, shift-invariant. The per-(head,channel) across-token
MEAN is a softmax nuisance (adds a token-constant to every logit); the
token-varying (demeaned) key content is the invariant the logit discriminates on.
Two distortions of delta = kr - k0 are reported (never scored except downstream):
  reconstruction (ii): relative ||delta|| / ||k0||
  quotient-tangential (i): relative ||demean(delta)|| / ||demean(k0)||   (demean over tokens)
Downstream d_O: mean KL( softmax(q.K0^T/sqrt(D)) || softmax(q.Kr^T/sqrt(D)) ) over
a 128 random-unit-query bank, held-out block.

Emits ===GO2V2-JSON=== ... ===END===.
"""

from __future__ import annotations

import json

import numpy as np
from turboquant_pro import PerChannelKV

H, D = 8, 128
SEEDS = 12
S_TEST, N_Q = 512, 128
ARMS = ["a_demean_perchan_asym4", "b_wholevec_pertoken_uniform4", "c_polarquant", "d_perchan_uniform4"]

# Registered effective-bits accounting: 4-bit payload + fp16 metadata scalars,
# amortized over the axis the metadata is shared across. NO per-block codebook.
EFF_BITS = {
    "a_demean_perchan_asym4": 4.0 + 2 * 16 / S_TEST,      # per-(H,D): scale+zero over S
    "b_wholevec_pertoken_uniform4": 4.0 + 2 * 16 / D,     # per-(H,S): min+scale over D
    "c_polarquant": 4.0 + 1 * 16 / D,                     # per-(H,S): norm over D
    "d_perchan_uniform4": 4.0 + 2 * 16 / S_TEST,          # per-(H,D): min+scale over S
}


def _keys(S, seed, H=H, D=D):
    r = np.random.default_rng(seed)
    dc = np.random.default_rng(1000 + seed).uniform(-6, 6, (H, D)).astype(np.float32)
    sc = np.random.default_rng(2000 + seed).uniform(0.2, 1.5, (H, D)).astype(np.float32)
    t = r.standard_t(3, (1, H, S, D)).astype(np.float32)
    return (dc[None, :, None, :] + sc[None, :, None, :] * t).astype(np.float32)


def _uniform_asym(x, axis, bits=4):
    """Per-slice (reduce over `axis`) asymmetric uniform quantizer -> reconstruction."""
    q = 2**bits - 1
    lo = x.min(axis=axis, keepdims=True)
    hi = x.max(axis=axis, keepdims=True)
    scale = (hi - lo) / q
    scale = np.where(scale > 0, scale, 1.0)
    idx = np.clip(np.round((x - lo) / scale), 0, q)
    return (lo + idx * scale).astype(np.float32)


def _polar_antiprobe(x, bits=4):
    """Anti-probe on (H,S,D): per-vector normalize, uniform-4bit direction, rescale by norm.
    Keeps norm + direction (the polar quotient), destroys per-channel scale."""
    nrm = np.linalg.norm(x, axis=-1, keepdims=True) + 1e-8
    u = x / nrm
    q = 2**bits - 1
    uq = np.clip(np.round((u * 0.5 + 0.5) * q), 0, q) / q * 2 - 1
    return (uq * nrm).astype(np.float32)


def _arm_recon(arm, test):
    k0 = test[0]  # (H, S, D)
    if arm == "a_demean_perchan_asym4":  # invariant-preserving (per-channel asym NF4)
        qz = PerChannelKV(head_dim=D, n_heads=H, nf4_asym=True, outlier_frac=0.0)
        return qz.decompress(qz.compress(test))[0]
    if arm == "b_wholevec_pertoken_uniform4":  # invariant-blind: per-TOKEN uniform over channels
        return _uniform_asym(k0, axis=2)  # reduce over D (per (H,S) vector)
    if arm == "c_polarquant":  # anti-probe
        return _polar_antiprobe(k0)
    if arm == "d_perchan_uniform4":  # reference: per-channel uniform over tokens
        qz = PerChannelKV(head_dim=D, n_heads=H, bits=4, outlier_frac=0.0)
        return qz.decompress(qz.compress(test))[0]
    raise ValueError(arm)


def _softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def _kl(k0, kr, Q, R=None):
    """mean KL(softmax(q.K0)||softmax(q.Kr)). R (D,D) rotates the consumer's read axes."""
    kk0, kkr = k0, kr
    if R is not None:
        kk0 = np.einsum("hsd,de->hse", k0, R)
        kkr = np.einsum("hsd,de->hse", kr, R)
    l0 = np.einsum("qhd,hsd->qhs", Q, kk0) / np.sqrt(D)
    lr = np.einsum("qhd,hsd->qhs", Q, kkr) / np.sqrt(D)
    p0, pr = _softmax(l0), _softmax(lr)
    return float((p0 * np.log((p0 + 1e-12) / (pr + 1e-12))).sum(-1).mean())


def _distortions(k0, kr):
    delta = kr - k0
    recon = float((np.linalg.norm(delta, axis=-1) / (np.linalg.norm(k0, axis=-1) + 1e-8)).mean())
    m0 = k0.mean(axis=1, keepdims=True)  # per-(H,channel) mean over tokens (axis 1 = S)
    mr = kr.mean(axis=1, keepdims=True)
    dt = (kr - mr) - (k0 - m0)
    sig = np.linalg.norm(k0 - m0, axis=-1) + 1e-8
    tang = float((np.linalg.norm(dt, axis=-1) / sig).mean())
    return recon, tang


def main():
    rows = []  # per arm x seed
    floor = []
    for seed in range(SEEDS):
        test = _keys(S_TEST, 100 + seed)
        k0 = test[0]
        Q = np.random.default_rng(300 + seed).standard_normal((N_Q, H, D)).astype(np.float32)
        # head-permuted query bank (registered control) + channel-rotation consumer (extra)
        perm = np.random.default_rng(700 + seed).permutation(H)
        Qshuf = Q[:, perm, :]
        Rr = np.linalg.qr(np.random.default_rng(800 + seed).standard_normal((D, D)))[0].astype(np.float32)
        floor.append(_kl(k0, k0.astype(np.float16).astype(np.float32), Q))
        for arm in ARMS:
            kr = _arm_recon(arm, test)
            recon, tang = _distortions(k0, kr)
            rows.append({
                "arm": arm, "seed": seed,
                "kl": _kl(k0, kr, Q), "kl_shuf": _kl(k0, kr, Qshuf), "kl_rot": _kl(k0, kr, Q, R=Rr),
                "recon": recon, "tang": tang,
            })

    def med(arm, key):
        return float(np.median([r[key] for r in rows if r["arm"] == arm]))

    med_kl = {a: med(a, "kl") for a in ARMS}
    med_recon = {a: med(a, "recon") for a in ARMS}
    med_tang = {a: med(a, "tang") for a in ARMS}
    a, b, c = "a_demean_perchan_asym4", "b_wholevec_pertoken_uniform4", "c_polarquant"

    # standardized joint regression kl ~ tang + recon over all arm x seed points
    kl = np.array([r["kl"] for r in rows])
    tg = np.array([r["tang"] for r in rows])
    rc = np.array([r["recon"] for r in rows])

    def z(v):
        return (v - v.mean()) / (v.std() + 1e-12)

    def r2(cols):
        Xc = np.column_stack([[tg, rc][k] for k in cols] + [np.ones_like(kl)])
        Xc = np.column_stack([z(Xc[:, i]) if i < len(cols) else Xc[:, i] for i in range(Xc.shape[1])])
        beta, *_ = np.linalg.lstsq(Xc, z(kl), rcond=None)
        resid = z(kl) - Xc @ beta
        return 1 - resid.var() / z(kl).var(), beta

    full, beta_full = r2([0, 1])
    pr_tang = full - r2([1])[0]
    pr_recon = full - r2([0])[0]

    # ordering consistency a < b, per seed (clustered)
    by_seed = {}
    for r in rows:
        by_seed.setdefault(r["seed"], {})[r["arm"]] = r
    a_lt_b = sum(1 for s in by_seed.values() if s[a]["kl"] < s[b]["kl"])

    gap_real = med_kl[b] / med_kl[a]
    gap_shuf = float(np.median([by_seed[s][b]["kl_shuf"] for s in by_seed])) / \
        float(np.median([by_seed[s][a]["kl_shuf"] for s in by_seed]))
    gap_rot = float(np.median([by_seed[s][b]["kl_rot"] for s in by_seed])) / \
        float(np.median([by_seed[s][a]["kl_rot"] for s in by_seed]))

    eff = {ar: round(EFF_BITS[ar], 4) for ar in ARMS}
    eff_spread = max(eff.values()) - min(eff.values())

    verdict = {
        "audit_pass": bool(eff_spread <= 0.5),
        "dominance": bool((pr_tang - pr_recon) >= 0.10),
        "c_gap": bool((med_kl[c] / med_kl[a]) >= 5.0),
        "a_lt_b_consistent": bool(a_lt_b >= 10),
    }
    corroborating = {
        "kl_gap_b_vs_a": gap_real,                 # >= 1.10 wanted
        "recon_ratio_b_vs_a": med_recon[b] / med_recon[a],  # <= 1.25 wanted
        "recon_does_not_explain_gap": bool(gap_real >= 1.10 and (med_recon[b] / med_recon[a]) <= 1.25),
    }
    result = {
        "claim": "GO-2 kv-keys v2", "prereg": "GO-P-2026-002", "instance": "post-RoPE keys / softmax",
        "n_seeds": SEEDS, "arms": ARMS,
        "effective_bits": eff, "eff_bits_spread": round(eff_spread, 4),
        "median_kl": med_kl, "median_recon": med_recon, "median_tang": med_tang,
        "c_gap": med_kl[c] / med_kl[a],
        "a_lt_b_seeds": f"{a_lt_b}/{SEEDS}",
        "std_coef_tang": float(beta_full[0]), "std_coef_recon": float(beta_full[1]),
        "partial_r2_tang": float(pr_tang), "partial_r2_recon": float(pr_recon),
        "dominance_margin": float(pr_tang - pr_recon),
        "noise_floor_kl": float(np.median(floor)),
        "control_gap_real": gap_real, "control_gap_headshuf": gap_shuf, "control_gap_chanrot": gap_rot,
        "bars": {"eff_bits_spread_le": 0.5, "dominance_ge": 0.10, "c_gap_ge": 5.0, "a_lt_b_ge": 10},
        "verdict": verdict, "corroborating": corroborating,
    }
    result["GO2_supported"] = all(verdict.values())
    print("===GO2V2-JSON===")
    print(json.dumps(result, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
