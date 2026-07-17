# Geometric Observation — GO-2 positive half on attention keys, v4.
# Governed by prereg/GO-P-2026-004 (sealed 4fd21a97; registered commit bde4172).
# Tests the MECHANISM: downstream distortion is governed by the error covariance
# projected onto the consumer's read subspace, tr(P_C Sigma_delta) -- so the a-vs-b
# ranking FLIPS between an isotropic and a structured consumer at fixed
# reconstruction, and tang_qproj (estimating tr(P_C Sigma_d)/tr(P_C Sigma_0))
# flips with it while reconstruction cannot. MIT License.
"""GO-2 v4: consumer-projected error covariance, rank/flip statistic, non-degenerate softmax."""

from __future__ import annotations

import json

import numpy as np
from turboquant_pro import PerChannelKV

H, D = 8, 128
SEEDS = 12
S_TEST, N_Q, R_SUB = 512, 128, 16
T_TARGET = 1.5  # target across-token logit std -> non-degenerate softmax
ARMS = ["a_demean_perchan_asym4", "b_wholevec_pertoken_uniform4", "c_polarquant", "d_perchan_uniform4"]
CONSUMERS = ["iso", "sub"]

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


def _queries(kind, k0, seed):
    if kind == "iso":
        q = np.random.default_rng(300 + seed).standard_normal((N_Q, H, D)).astype(np.float32)
        return (q / (np.linalg.norm(q, axis=-1, keepdims=True) + 1e-8)).astype(np.float32)
    rng = np.random.default_rng(500 + seed)  # structured: top-R subspace of demeaned keys per head
    Q = np.empty((N_Q, H, D), dtype=np.float32)
    for h in range(H):
        _, _, Vt = np.linalg.svd(k0[h] - k0[h].mean(0, keepdims=True), full_matrices=False)
        q = rng.standard_normal((N_Q, R_SUB)).astype(np.float32) @ Vt[:R_SUB]
        Q[:, h, :] = q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-8)
    return Q


def _uniform_asym(x, axis, bits=4):
    q = 2**bits - 1
    lo, hi = x.min(axis=axis, keepdims=True), x.max(axis=axis, keepdims=True)
    scale = np.where((hi - lo) > 0, (hi - lo) / q, 1.0)
    return (lo + np.clip(np.round((x - lo) / scale), 0, q) * scale).astype(np.float32)


def _polar_antiprobe(x, bits=4):
    nrm = np.linalg.norm(x, axis=-1, keepdims=True) + 1e-8
    u, q = x / nrm, 2**bits - 1
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


def _spearman4(x, y):
    """Spearman rho over 4 items (ranks of x vs y)."""
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    d2 = float(((rx - ry) ** 2).sum())
    return 1.0 - 6.0 * d2 / (4 * (16 - 1))


def main():
    # per (consumer, arm): lists across seeds of kl, tang, and per-arm recon (fixed)
    KL = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    TG = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    RC = {a: [] for a in ARMS}
    maxprob = {C: [] for C in CONSUMERS}
    floor = {C: [] for C in CONSUMERS}
    sp_tang = {C: [] for C in CONSUMERS}
    sp_recon = {C: [] for C in CONSUMERS}
    proj_frac = {"a": [], "b": []}  # tr(P_sub Sigma_delta)/tr(Sigma_delta), corroboration

    for seed in range(SEEDS):
        test = _keys(S_TEST, 100 + seed)
        k0 = test[0]
        recon = {}
        krs = {}
        for a in ARMS:
            kr = _arm_recon(a, test)
            krs[a] = kr
            delta = kr - k0
            recon[a] = float((np.linalg.norm(delta, axis=-1) / (np.linalg.norm(k0, axis=-1) + 1e-8)).mean())
            RC[a].append(recon[a])
        # covariance-projection corroboration on the structured subspace
        Qsub = _queries("sub", k0, seed)
        for lbl, a in [("a", ARMS[0]), ("b", ARMS[1])]:
            delta = krs[a] - k0
            num, den = 0.0, 0.0
            for h in range(H):
                dd = delta[h] - delta[h].mean(0, keepdims=True)  # (S,D) across-token
                Sig = dd.T @ dd / dd.shape[0]  # (D,D)
                _, _, Vt = np.linalg.svd(k0[h] - k0[h].mean(0, keepdims=True), full_matrices=False)
                P = Vt[:R_SUB].T @ Vt[:R_SUB]  # (D,D) projector
                num += float(np.trace(P @ Sig))
                den += float(np.trace(Sig))
            proj_frac[lbl].append(num / (den + 1e-12))

        for C in CONSUMERS:
            Q = _queries(C, k0, seed)
            l0 = np.einsum("qhd,hsd->qhs", Q, k0) / np.sqrt(D)
            g = T_TARGET / (float(np.median(l0.std(axis=2))) + 1e-8)  # sharpen: arm-independent
            p0 = _softmax(g * l0)
            maxprob[C].append(float(np.median(p0.max(-1))))
            floor[C].append(float((p0 * np.log((p0 + 1e-12) / (
                _softmax(g * np.einsum("qhd,hsd->qhs", Q, k0.astype(np.float16).astype(np.float32)) / np.sqrt(D))
                + 1e-12))).sum(-1).mean()))
            kl_arms, tg_arms, rc_arms = [], [], []
            for a in ARMS:
                lr = np.einsum("qhd,hsd->qhs", Q, krs[a]) / np.sqrt(D)
                pr = _softmax(g * lr)
                kl = float((p0 * np.log((p0 + 1e-12) / (pr + 1e-12))).sum(-1).mean())
                dl = lr - l0
                tang = float((dl.var(axis=2) / (l0.var(axis=2) + 1e-8)).mean())  # g-invariant
                KL[C][a].append(kl); TG[C][a].append(tang)
                kl_arms.append(kl); tg_arms.append(tang); rc_arms.append(recon[a])
            sp_tang[C].append(_spearman4(tg_arms, kl_arms))
            sp_recon[C].append(_spearman4(rc_arms, kl_arms))

    def med(d):
        return {k: float(np.median(v)) for k, v in d.items()}

    a, b, c = ARMS[0], ARMS[1], ARMS[2]
    out = {"claim": "GO-2 kv-keys v4", "prereg": "GO-P-2026-004", "n_seeds": SEEDS, "arms": ARMS,
           "effective_bits": {k: round(v, 4) for k, v in EFF_BITS.items()},
           "eff_bits_spread": round(max(EFF_BITS.values()) - min(EFF_BITS.values()), 4),
           "median_recon": med(RC), "consumers": {}}
    for C in CONSUMERS:
        mkl, mtg = med(KL[C]), med(TG[C])
        adv_kl = [np.log(KL[C][b][i] / KL[C][a][i]) for i in range(SEEDS)]
        adv_tg = [np.log(TG[C][b][i] / TG[C][a][i]) for i in range(SEEDS)]
        out["consumers"][C] = {
            "median_kl": mkl, "median_tang_qproj": mtg,
            "c_gap": mkl[c] / mkl[a],
            "median_adv_kl_logbovera": float(np.median(adv_kl)),
            "median_adv_tang_logbovera": float(np.median(adv_tg)),
            "signagree_tang_kl_seeds": int(sum(1 for i in range(SEEDS) if np.sign(adv_tg[i]) == np.sign(adv_kl[i]))),
            "median_spearman_tang_kl": float(np.median(sp_tang[C])),
            "median_spearman_recon_kl": float(np.median(sp_recon[C])),
            "median_max_softmax_prob": float(np.median(maxprob[C])),
            "noise_floor_kl": float(np.median(floor[C])),
        }
    out["proj_frac_subspace"] = {"a": float(np.median(proj_frac["a"])), "b": float(np.median(proj_frac["b"]))}

    iso, sub = out["consumers"]["iso"], out["consumers"]["sub"]
    min_sp_tang = min(iso["median_spearman_tang_kl"], sub["median_spearman_tang_kl"])
    min_sp_recon = min(iso["median_spearman_recon_kl"], sub["median_spearman_recon_kl"])
    verdict = {
        "audit_pass": bool(out["eff_bits_spread"] <= 0.5),
        "nondegeneracy": bool(iso["median_max_softmax_prob"] >= 3 / S_TEST and sub["median_max_softmax_prob"] >= 3 / S_TEST),
        "c_gap_both": bool(iso["c_gap"] >= 5.0 and sub["c_gap"] >= 5.0),
        "flip": bool(iso["median_adv_kl_logbovera"] > 0 and sub["median_adv_kl_logbovera"] < 0),
        "tang_tracks_flip": bool(
            np.sign(iso["median_adv_tang_logbovera"]) == np.sign(iso["median_adv_kl_logbovera"])
            and np.sign(sub["median_adv_tang_logbovera"]) == np.sign(sub["median_adv_kl_logbovera"])
            and iso["signagree_tang_kl_seeds"] >= 10 and sub["signagree_tang_kl_seeds"] >= 10),
        "tang_ranks_both": bool(iso["median_spearman_tang_kl"] >= 0.9 and sub["median_spearman_tang_kl"] >= 0.9),
        "recon_fails": bool(min_sp_recon < min_sp_tang),
    }
    out["min_spearman_tang"] = min_sp_tang
    out["min_spearman_recon"] = min_sp_recon
    out["verdict"] = verdict
    out["GO2_positive_supported"] = all(verdict.values())
    print("===GO2V4-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
