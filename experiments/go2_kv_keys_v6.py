# Geometric Observation — GO-2 positive half on attention keys, v6 (instance-1 closer).
# Governed by prereg/GO-P-2026-006 (sealed 553035ce; registered commit 743c68c).
# Scopes the registered conjunction to EXACTLY the mechanism: the a-vs-b flip is
# governed by proj_var = tr(P_C Sigma_delta)/tr(P_C Sigma_0) and NOT by
# reconstruction. Anti-probe gap + full-4-arm Spearman are REPORTED diagnostics,
# not gates (r_sub=8 so the anti-probe naturally clears >=5). MIT License.
"""GO-2 v6: the consumer flip gated exactly; anti-probe & full-rank as diagnostics."""

from __future__ import annotations

import json

import numpy as np
from turboquant_pro import PerChannelKV

H, D = 8, 128
SEEDS = 12
S_TEST, N_Q, R_SUB = 512, 128, 8
T_TARGET = 1.5
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


def _subspace(k0):
    """Top-R_SUB right singular vectors of demeaned keys, per head: list of (R,D)."""
    Vs = []
    for h in range(H):
        _, _, Vt = np.linalg.svd(k0[h] - k0[h].mean(0, keepdims=True), full_matrices=False)
        Vs.append(Vt[:R_SUB])
    return Vs


def _queries(kind, Vs, seed):
    if kind == "iso":
        q = np.random.default_rng(300 + seed).standard_normal((N_Q, H, D)).astype(np.float32)
        return (q / (np.linalg.norm(q, axis=-1, keepdims=True) + 1e-8)).astype(np.float32)
    rng = np.random.default_rng(500 + seed)
    Q = np.empty((N_Q, H, D), dtype=np.float32)
    for h in range(H):
        q = rng.standard_normal((N_Q, R_SUB)).astype(np.float32) @ Vs[h]
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
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return 1.0 - 6.0 * float(((rx - ry) ** 2).sum()) / (4 * 15)


def _proj_var(delta, k0, Vs, kind):
    """proj_var = sum_h tr(P_C Sigma_delta) / sum_h tr(P_C Sigma_0), demeaned covariances."""
    num, den = 0.0, 0.0
    for h in range(H):
        dd = delta[h] - delta[h].mean(0, keepdims=True)   # (S,D)
        kk = k0[h] - k0[h].mean(0, keepdims=True)
        if kind == "iso":  # P ∝ I -> trace of covariance = ||.||_F^2 / S
            num += float((dd * dd).sum())
            den += float((kk * kk).sum())
        else:              # P = V^T V (top-R): energy in the subspace
            pd = dd @ Vs[h].T   # (S,R)
            pk = kk @ Vs[h].T
            num += float((pd * pd).sum())
            den += float((pk * pk).sum())
    return num / (den + 1e-12)


def main():
    KL = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    PV = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    RC = {a: [] for a in ARMS}
    maxprob = {C: [] for C in CONSUMERS}
    floor = {C: [] for C in CONSUMERS}
    sp_pv = {C: [] for C in CONSUMERS}
    sp_rc = {C: [] for C in CONSUMERS}

    for seed in range(SEEDS):
        test = _keys(S_TEST, 100 + seed)
        k0 = test[0]
        Vs = _subspace(k0)
        krs, recon, deltas = {}, {}, {}
        for a in ARMS:
            kr = _arm_recon(a, test)
            krs[a] = kr
            deltas[a] = kr - k0
            recon[a] = float((np.linalg.norm(deltas[a], axis=-1) / (np.linalg.norm(k0, axis=-1) + 1e-8)).mean())
            RC[a].append(recon[a])
        for C in CONSUMERS:
            Q = _queries(C, Vs, seed)
            l0 = np.einsum("qhd,hsd->qhs", Q, k0) / np.sqrt(D)
            g = T_TARGET / (float(np.median(l0.std(axis=2))) + 1e-8)
            p0 = _softmax(g * l0)
            maxprob[C].append(float(np.median(p0.max(-1))))
            p0f = _softmax(g * np.einsum("qhd,hsd->qhs", Q, k0.astype(np.float16).astype(np.float32)) / np.sqrt(D))
            floor[C].append(float((p0 * np.log((p0 + 1e-12) / (p0f + 1e-12))).sum(-1).mean()))
            kl_arms, pv_arms, rc_arms = [], [], []
            for a in ARMS:
                lr = np.einsum("qhd,hsd->qhs", Q, krs[a]) / np.sqrt(D)
                pr = _softmax(g * lr)
                KL[C][a].append(float((p0 * np.log((p0 + 1e-12) / (pr + 1e-12))).sum(-1).mean()))
                PV[C][a].append(_proj_var(deltas[a], k0, Vs, C))
                kl_arms.append(KL[C][a][-1]); pv_arms.append(PV[C][a][-1]); rc_arms.append(recon[a])
            sp_pv[C].append(_spearman4(pv_arms, kl_arms))
            sp_rc[C].append(_spearman4(rc_arms, kl_arms))

    def med(d):
        return {k: float(np.median(v)) for k, v in d.items()}

    a, b, c = ARMS[0], ARMS[1], ARMS[2]
    out = {"claim": "GO-2 kv-keys v6", "prereg": "GO-P-2026-006", "n_seeds": SEEDS, "arms": ARMS,
           "r_sub": R_SUB, "effective_bits": {k: round(v, 4) for k, v in EFF_BITS.items()},
           "eff_bits_spread": round(max(EFF_BITS.values()) - min(EFF_BITS.values()), 4),
           "median_recon": med(RC), "consumers": {}}
    for C in CONSUMERS:
        adv_kl = [np.log(KL[C][b][i] / KL[C][a][i]) for i in range(SEEDS)]
        adv_pv = [np.log(PV[C][b][i] / PV[C][a][i]) for i in range(SEEDS)]
        iso_flip = sum(1 for i in range(SEEDS) if KL[C][a][i] < KL[C][b][i])  # a<b count
        out["consumers"][C] = {
            "median_kl": med(KL[C]), "median_proj_var": med(PV[C]),
            "c_gap": med(KL[C])[c] / med(KL[C])[a],
            "median_adv_kl_logbovera": float(np.median(adv_kl)),
            "median_adv_projvar_logbovera": float(np.median(adv_pv)),
            "kl_a_lt_b_seeds": int(iso_flip),
            "proj_tracks_flip_seeds": int(sum(1 for i in range(SEEDS) if np.sign(adv_pv[i]) == np.sign(adv_kl[i]))),
            "median_spearman_projvar_kl": float(np.median(sp_pv[C])),
            "median_spearman_recon_kl": float(np.median(sp_rc[C])),
            "median_max_softmax_prob": float(np.median(maxprob[C])),
            "noise_floor_kl": float(np.median(floor[C])),
        }
    iso, sub = out["consumers"]["iso"], out["consumers"]["sub"]
    min_sp_pv = min(iso["median_spearman_projvar_kl"], sub["median_spearman_projvar_kl"])
    min_sp_rc = min(iso["median_spearman_recon_kl"], sub["median_spearman_recon_kl"])
    # GATED: exactly GO-2's positive-half claim (the flip governed by proj_var, not recon)
    verdict = {
        "audit_pass": bool(out["eff_bits_spread"] <= 0.5),
        "nondegeneracy": bool(iso["median_max_softmax_prob"] >= 3 / S_TEST and sub["median_max_softmax_prob"] >= 3 / S_TEST),
        "flip_decisive": bool(
            iso["median_adv_kl_logbovera"] >= np.log(1.3) and sub["median_adv_kl_logbovera"] <= -np.log(1.15)
            and iso["kl_a_lt_b_seeds"] >= 10 and (SEEDS - sub["kl_a_lt_b_seeds"]) >= 10),
        "proj_tracks_flip": bool(iso["proj_tracks_flip_seeds"] >= 11 and sub["proj_tracks_flip_seeds"] >= 11),
        "recon_fails": bool(min_sp_rc < min_sp_pv),
    }
    # REPORTED DIAGNOSTICS (not gated): anti-probe gap + full-4-arm Spearman (NEG-9 context)
    out["diagnostics"] = {
        "anti_probe_gap": {"iso": iso["c_gap"], "sub": sub["c_gap"], "both_ge_5": bool(iso["c_gap"] >= 5 and sub["c_gap"] >= 5)},
        "full_rank_spearman_projvar": {"iso": iso["median_spearman_projvar_kl"], "sub": sub["median_spearman_projvar_kl"]},
        "full_rank_spearman_recon": {"iso": iso["median_spearman_recon_kl"], "sub": sub["median_spearman_recon_kl"]},
    }
    out["min_spearman_projvar"] = min_sp_pv
    out["min_spearman_recon"] = min_sp_rc
    out["verdict"] = verdict
    out["GO2_positive_supported"] = all(verdict.values())
    print("===GO2V6-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
