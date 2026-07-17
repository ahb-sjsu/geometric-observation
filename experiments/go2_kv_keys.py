# Geometric Observation — GO-2 (quotient-(A2) transfer) on attention keys.
# Governed by prereg/GO-P-2026-001. Uses the published turboquant-pro (Paper II).
# MIT License.
"""GO-2 workhorse on the KV-attention-keys instance.

Three-arm design (§3) + the (i)-tangential-dominates-(ii)-reconstruction
regression (§2). The consumer is softmax attention, which is shift-invariant:
a per-channel component **constant across tokens** is nuisance, so the
distinguishing (tangential) content is the **per-channel-demeaned** keys. We
therefore measure two distortions of the reconstruction error delta = kr - k0:

  reconstruction (ii): relative ||delta|| / ||k0||            (the full error)
  quotient-tangential (i): relative ||demean(delta)|| / ||demean(k0)||
                           where demean removes the per-(head,channel) mean over
                           tokens (the softmax common-mode nuisance).

Downstream metric d_O: mean KL( softmax(q.K0^T) || softmax(q.Kr^T) ) over a bank
of random unit queries, on a held-out block. Reconstruction is reported, never
scored. Arms:
  a asym_nf4_2pct    (invariant-preserving)   b lloyd_recon_opt (reconstruction-optimal)
  c polar_antiprobe  (anti-probe control)     d uniform_perchan (4th variant, regression)

Emits a sentinel-delimited result JSON (===GO2-JSON=== ... ===END===).
"""

from __future__ import annotations

import json

import numpy as np
from turboquant_pro import PerChannelKV

H, D = 8, 128
SEEDS = 12
S_TEST, N_Q = 512, 128


def _keys(S, seed, H=H, D=D):
    r = np.random.default_rng(seed)
    dc = np.random.default_rng(1000 + seed).uniform(-6, 6, (H, D)).astype(np.float32)
    sc = np.random.default_rng(2000 + seed).uniform(0.2, 1.5, (H, D)).astype(np.float32)
    t = r.standard_t(3, (1, H, S, D)).astype(np.float32)
    return (dc[None, :, None, :] + sc[None, :, None, :] * t).astype(np.float32)


def _polar_antiprobe(x, bits=4):
    """Anti-probe: per-vector normalize, quantize direction uniformly, rescale by
    norm. Preserves the nuisance (norm + direction) and destroys the invariant
    (per-channel scale) -- the wrong quotient, on purpose."""
    nrm = np.linalg.norm(x, axis=-1, keepdims=True) + 1e-8
    u = x / nrm
    q = 2**bits - 1
    uq = np.clip(np.round((u * 0.5 + 0.5) * q), 0, q) / q * 2 - 1  # uniform on [-1,1]
    return (uq * nrm).astype(np.float32)


def _lloyd_recon(x, bits=4, iters=15):
    """Reconstruction-optimal arm: per-(head,channel) Lloyd-Max codebook fit to
    the block itself (minimizes ||x - Q(x)|| at matched bits), inline so the book
    depends on no unreleased library feature."""
    k = x[0].astype(np.float64)  # (H, S, D)
    Hn, Sn, Dn = k.shape
    lev = 2**bits
    pooled = np.moveaxis(k, 1, -1).reshape(-1, Sn)  # (C=H*D, S)
    qs = np.linspace(0.0, 1.0, lev)
    lv = np.quantile(pooled, qs, axis=-1).T  # (C, L) init
    for _ in range(iters):
        idx = np.abs(pooled[:, None, :] - lv[:, :, None]).argmin(1)  # (C, S)
        newl = lv.copy()
        for level in range(lev):
            m = idx == level
            cnt, s = m.sum(1), (pooled * m).sum(1)
            newl[:, level] = np.where(cnt > 0, s / np.maximum(cnt, 1e-12), lv[:, level])
        lv = np.sort(newl, 1)
    idx = np.abs(pooled[:, None, :] - lv[:, :, None]).argmin(1)
    rec = np.take_along_axis(lv, idx, axis=1)  # (C, S)
    return np.moveaxis(rec.reshape(Hn, Dn, Sn), -1, 1).astype(np.float32)  # (H, S, D)


def _softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def _metrics(k0, kr, Q):
    d0 = D
    l0 = np.einsum("qhd,hsd->qhs", Q, k0) / np.sqrt(d0)
    lr = np.einsum("qhd,hsd->qhs", Q, kr) / np.sqrt(d0)
    p0, pr = _softmax(l0), _softmax(lr)
    kl = float((p0 * np.log((p0 + 1e-12) / (pr + 1e-12))).sum(-1).mean())
    delta = kr - k0
    recon = float((np.linalg.norm(delta, axis=-1) / (np.linalg.norm(k0, axis=-1) + 1e-8)).mean())
    m0 = k0.mean(axis=1, keepdims=True)  # per-(head,channel) mean over tokens (axis 1 = S here for (H,S,D))
    mr = kr.mean(axis=1, keepdims=True)
    dt = (kr - mr) - (k0 - m0)
    sig = np.linalg.norm(k0 - m0, axis=-1) + 1e-8
    tang = float((np.linalg.norm(dt, axis=-1) / sig).mean())
    return kl, recon, tang


def _arm_recon(arm, test):
    # matched at exactly 4-bit per-channel (no outliers) so the ONLY difference
    # between arms is the quotient each preserves.
    if arm == "a_asym_nf4":  # invariant-preserving: per-channel zero-point + NF4
        q = PerChannelKV(head_dim=D, n_heads=H, nf4_asym=True, outlier_frac=0.0)
        return q.decompress(q.compress(test))[0]
    if arm == "b_lloyd_recon":  # reconstruction-optimal (per-block Lloyd-Max)
        return _lloyd_recon(test)
    if arm == "c_polar_antiprobe":  # anti-probe: keep norm/direction, drop per-channel scale
        return _polar_antiprobe(test[0])
    if arm == "d_uniform":  # per-channel uniform
        q = PerChannelKV(head_dim=D, n_heads=H, bits=4, outlier_frac=0.0)
        return q.decompress(q.compress(test))[0]
    raise ValueError(arm)


def main():
    arms = ["a_asym_nf4", "b_lloyd_recon", "c_polar_antiprobe", "d_uniform"]
    rows = []  # (arm, seed, kl, recon, tang)
    floor = []
    for seed in range(SEEDS):
        test = _keys(S_TEST, 100 + seed)
        Q = np.random.default_rng(300 + seed).standard_normal((N_Q, H, D)).astype(np.float32)
        k0 = test[0]
        # noise floor: fp16-vs-fp16 KL is 0 by construction; use a tiny-perturbation
        # rerun as the practical floor (float round-trip through the pipeline)
        kl_floor, _, _ = _metrics(k0, k0.astype(np.float16).astype(np.float32), Q)
        floor.append(kl_floor)
        for arm in arms:
            kr = _arm_recon(arm, test)
            kl, recon, tang = _metrics(k0, kr, Q)
            rows.append({"arm": arm, "seed": seed, "kl": kl, "recon": recon, "tang": tang})

    def med(arm, key):
        v = [r[key] for r in rows if r["arm"] == arm]
        return float(np.median(v))

    order = {a: med(a, "kl") for a in arms}
    # standardized joint regression: kl ~ tang + recon across all arm x seed points
    kl = np.array([r["kl"] for r in rows])
    tg = np.array([r["tang"] for r in rows])
    rc = np.array([r["recon"] for r in rows])

    def z(v):
        return (v - v.mean()) / (v.std() + 1e-12)

    X = np.column_stack([z(tg), z(rc), np.ones_like(kl)])
    beta, *_ = np.linalg.lstsq(X, z(kl), rcond=None)
    # partial R^2 for each predictor (drop-one)
    def r2(cols):
        Xc = np.column_stack([X[:, c] for c in cols] + [np.ones_like(kl)])
        b, *_ = np.linalg.lstsq(Xc, z(kl), rcond=None)
        resid = z(kl) - Xc @ b
        return 1 - resid.var() / z(kl).var()
    full = r2([0, 1])
    pr_tang = full - r2([1])   # unique to tang
    pr_recon = full - r2([0])  # unique to recon
    # clustered ordering check: per-seed, is kl(a)<kl(b)<kl(c)?
    by_seed = {}
    for r in rows:
        by_seed.setdefault(r["seed"], {})[r["arm"]] = r["kl"]
    ord_hits = sum(
        1 for s in by_seed.values()
        if s["a_asym_nf4"] < s["b_lloyd_recon"] < s["c_polar_antiprobe"]
    )

    result = {
        "claim": "GO-2 kv-keys", "prereg": "GO-P-2026-001", "instance": "post-RoPE keys / softmax",
        "n_seeds": SEEDS, "arms": arms,
        "median_kl": order,
        "median_recon": {a: med(a, "recon") for a in arms},
        "median_tang": {a: med(a, "tang") for a in arms},
        "ordering_a_lt_b_lt_c_hits": f"{ord_hits}/{SEEDS}",
        "effect_a_vs_b": order["b_lloyd_recon"] / order["a_asym_nf4"],
        "effect_c_gap": order["c_polar_antiprobe"] / order["a_asym_nf4"],
        "std_coef_tang": float(beta[0]), "std_coef_recon": float(beta[1]),
        "partial_r2_tang": float(pr_tang), "partial_r2_recon": float(pr_recon),
        "dominance_margin": float(pr_tang - pr_recon),
        "noise_floor_kl": float(np.median(floor)),
        "bars": {
            "a_vs_b_ge": 1.10, "c_gap_ge": 5.0, "dominance_ge": 0.10, "ordering_hits": SEEDS,
        },
    }
    result["verdict"] = {
        "ordering": ord_hits == SEEDS,
        "a_vs_b_floor": result["effect_a_vs_b"] >= 1.10,
        "c_gap_floor": result["effect_c_gap"] >= 5.0,
        "tangential_dominates": result["dominance_margin"] >= 0.10,
    }
    result["GO2_supported"] = all(result["verdict"].values())
    print("===GO2-JSON===")
    print(json.dumps(result, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
