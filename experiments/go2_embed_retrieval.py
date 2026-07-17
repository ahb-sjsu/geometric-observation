# Geometric Observation — GO-2 instance 2: embedding retrieval, ranking consumer.
# Governed by prereg/GO-P-2026-007 (sealed 66fc8ab3; registered commit 1899d27).
# PROSPECTIVE test of whether the instance-1 mechanism (downstream distortion
# governed by tr(P_C Sigma_delta); consumer-driven a-vs-b flip untrackable by
# reconstruction) transfers to a DIFFERENT representation (low-rank embeddings)
# and a DIFFERENT consumer (retrieval RANKING, not softmax-KL). MIT License.
"""GO-2 instance 2: proj_var vs reconstruction on retrieval ranking distortion."""

from __future__ import annotations

import json

import numpy as np
from turboquant_pro import PerChannelKV

N, D = 1024, 128           # corpus items, dims
SEEDS = 12
N_Q, R_LAT, R_SUB = 128, 16, 8
ARMS = ["a_perdim_nf4", "b_wholevec_peritem_uniform4", "c_polar_antiprobe", "d_perdim_uniform4"]
CONSUMERS = ["iso", "sub"]

EFF_BITS = {                                   # 4-bit payload + fp16 metadata, amortized
    "a_perdim_nf4": 4.0 + 2 * 16 / N,          # per-dim: scale+zero over N items
    "b_wholevec_peritem_uniform4": 4.0 + 2 * 16 / D,   # per-item: min+scale over D
    "c_polar_antiprobe": 4.0 + 1 * 16 / D,     # per-item: norm over D
    "d_perdim_uniform4": 4.0 + 2 * 16 / N,     # per-dim: min+scale over N items
}


def _embeddings(seed):
    dc = np.random.default_rng(1000 + seed).uniform(-6, 6, D).astype(np.float32)
    sc = np.random.default_rng(2000 + seed).uniform(0.2, 1.5, D).astype(np.float32)
    L = (np.random.default_rng(3000 + seed).standard_normal((D, R_LAT)) / np.sqrt(R_LAT)).astype(np.float32)
    F = np.random.default_rng(4000 + seed).standard_normal((N, R_LAT)).astype(np.float32)
    noise = np.random.default_rng(5000 + seed).standard_t(3, (N, D)).astype(np.float32)
    return (dc[None, :] + sc[None, :] * (F @ L.T + noise)).astype(np.float32)  # (N, D)


def _uniform_asym(x, axis, bits=4):
    q = 2**bits - 1
    lo, hi = x.min(axis=axis, keepdims=True), x.max(axis=axis, keepdims=True)
    scale = np.where((hi - lo) > 0, (hi - lo) / q, 1.0)
    return (lo + np.clip(np.round((x - lo) / scale), 0, q) * scale).astype(np.float32)


def _polar_antiprobe(x, bits=4):  # per-item normalize over dims
    nrm = np.linalg.norm(x, axis=1, keepdims=True) + 1e-8
    u, q = x / nrm, 2**bits - 1
    uq = np.clip(np.round((u * 0.5 + 0.5) * q), 0, q) / q * 2 - 1
    return (uq * nrm).astype(np.float32)


def _arm_recon(arm, E):
    if arm == "a_perdim_nf4":               # per-dim NF4 (invariant-preserving)
        qz = PerChannelKV(head_dim=D, n_heads=1, nf4_asym=True, outlier_frac=0.0)
        return np.asarray(qz.decompress(qz.compress(E[None, None]))).reshape(N, D)
    if arm == "b_wholevec_peritem_uniform4":  # per-item uniform (invariant-blind)
        return _uniform_asym(E, axis=1)
    if arm == "c_polar_antiprobe":
        return _polar_antiprobe(E)
    if arm == "d_perdim_uniform4":          # per-dim uniform (reference)
        qz = PerChannelKV(head_dim=D, n_heads=1, bits=4, outlier_frac=0.0)
        return np.asarray(qz.decompress(qz.compress(E[None, None]))).reshape(N, D)
    raise ValueError(arm)


def _rank_rows(A):
    return np.argsort(np.argsort(A, axis=1), axis=1).astype(np.float64)


def _one_minus_spearman(S0, Sr):
    """mean over rows of (1 - Spearman(S0_row, Sr_row)); rows = queries, cols = items."""
    r0, rr = _rank_rows(S0), _rank_rows(Sr)
    r0 -= r0.mean(1, keepdims=True)
    rr -= rr.mean(1, keepdims=True)
    num = (r0 * rr).sum(1)
    den = np.sqrt((r0 * r0).sum(1) * (rr * rr).sum(1)) + 1e-12
    return float((1.0 - num / den).mean())


def _top_overlap_deficit(S0, Sr, k=10):
    t0 = np.argsort(-S0, axis=1)[:, :k]
    tr = np.argsort(-Sr, axis=1)[:, :k]
    ov = np.array([len(set(t0[i]) & set(tr[i])) / k for i in range(S0.shape[0])])
    return float((1.0 - ov).mean())


def _spearman4(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return 1.0 - 6.0 * float(((rx - ry) ** 2).sum()) / (4 * 15)


def _subspace(E):
    Ec = E - E.mean(0, keepdims=True)             # demean over items
    _, _, Vt = np.linalg.svd(Ec, full_matrices=False)
    return Vt[:R_SUB]                              # (R_SUB, D)


def _proj_var(delta, E, V, kind):
    dd = delta - delta.mean(0, keepdims=True)     # demean over items (N,D)
    ee = E - E.mean(0, keepdims=True)
    if kind == "iso":
        return float((dd * dd).sum() / ((ee * ee).sum() + 1e-12))
    pd, pe = dd @ V.T, ee @ V.T                    # project onto read subspace
    return float((pd * pd).sum() / ((pe * pe).sum() + 1e-12))


def main():
    dO = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    PV = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    RC = {a: [] for a in ARMS}
    floor = {C: [] for C in CONSUMERS}
    top = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    sp_pv = {C: [] for C in CONSUMERS}
    sp_rc = {C: [] for C in CONSUMERS}

    for seed in range(SEEDS):
        E = _embeddings(seed)
        V = _subspace(E)
        krs, recon = {}, {}
        for a in ARMS:
            Er = _arm_recon(a, E)
            krs[a] = Er
            recon[a] = float((np.linalg.norm(Er - E, axis=1) / (np.linalg.norm(E, axis=1) + 1e-8)).mean())
            RC[a].append(recon[a])
        for C in CONSUMERS:
            if C == "iso":
                Q = np.random.default_rng(300 + seed).standard_normal((N_Q, D)).astype(np.float32)
            else:
                Q = (np.random.default_rng(500 + seed).standard_normal((N_Q, R_SUB)).astype(np.float32) @ V)
            Q = Q / (np.linalg.norm(Q, axis=1, keepdims=True) + 1e-8)
            S0 = Q @ E.T
            floor[C].append(_one_minus_spearman(S0, Q @ E.astype(np.float16).astype(np.float32).T))
            dO_arms, pv_arms, rc_arms = [], [], []
            for a in ARMS:
                Sr = Q @ krs[a].T
                dO[C][a].append(_one_minus_spearman(S0, Sr))
                PV[C][a].append(_proj_var(krs[a] - E, E, V, C))
                top[C][a].append(_top_overlap_deficit(S0, Sr))
                dO_arms.append(dO[C][a][-1]); pv_arms.append(PV[C][a][-1]); rc_arms.append(recon[a])
            sp_pv[C].append(_spearman4(pv_arms, dO_arms))
            sp_rc[C].append(_spearman4(rc_arms, dO_arms))

    def med(d):
        return {k: float(np.median(v)) for k, v in d.items()}

    a, b, c = ARMS[0], ARMS[1], ARMS[2]
    out = {"claim": "GO-2 embedding-retrieval (instance 2)", "prereg": "GO-P-2026-007",
           "n_seeds": SEEDS, "arms": ARMS, "r_sub": R_SUB,
           "effective_bits": {k: round(v, 4) for k, v in EFF_BITS.items()},
           "eff_bits_spread": round(max(EFF_BITS.values()) - min(EFF_BITS.values()), 4),
           "median_recon": med(RC), "consumers": {}}
    for C in CONSUMERS:
        adv_dO = [np.log(dO[C][b][i] / dO[C][a][i]) for i in range(SEEDS)]
        adv_pv = [np.log(PV[C][b][i] / PV[C][a][i]) for i in range(SEEDS)]
        a_lt_b = sum(1 for i in range(SEEDS) if dO[C][a][i] < dO[C][b][i])
        out["consumers"][C] = {
            "median_dO": med(dO[C]), "median_proj_var": med(PV[C]), "median_top10_deficit": med(top[C]),
            "median_adv_dO_logbovera": float(np.median(adv_dO)),
            "median_adv_projvar_logbovera": float(np.median(adv_pv)),
            "dO_a_lt_b_seeds": int(a_lt_b),
            "proj_tracks_flip_seeds": int(sum(1 for i in range(SEEDS) if np.sign(adv_pv[i]) == np.sign(adv_dO[i]))),
            "median_spearman_projvar_dO": float(np.median(sp_pv[C])),
            "median_spearman_recon_dO": float(np.median(sp_rc[C])),
            "median_noise_floor_dO": float(np.median(floor[C])),
            "anti_probe_gap": med(dO[C])[c] / med(dO[C])[a],
        }
    iso, sub = out["consumers"]["iso"], out["consumers"]["sub"]
    min_sp_pv = min(iso["median_spearman_projvar_dO"], sub["median_spearman_projvar_dO"])
    min_sp_rc = min(iso["median_spearman_recon_dO"], sub["median_spearman_recon_dO"])
    min_arm_dO = min(min(iso["median_dO"].values()), min(sub["median_dO"].values()))
    max_floor = max(iso["median_noise_floor_dO"], sub["median_noise_floor_dO"])
    verdict = {
        "audit_pass": bool(out["eff_bits_spread"] <= 0.5),
        "snr": bool(min_arm_dO >= 10 * max_floor),
        "flip_decisive": bool(
            iso["median_adv_dO_logbovera"] >= np.log(1.3) and sub["median_adv_dO_logbovera"] <= -np.log(1.15)
            and iso["dO_a_lt_b_seeds"] >= 10 and (SEEDS - sub["dO_a_lt_b_seeds"]) >= 10),
        "proj_tracks_flip": bool(iso["proj_tracks_flip_seeds"] >= 11 and sub["proj_tracks_flip_seeds"] >= 11),
        "recon_fails": bool(min_sp_rc < min_sp_pv),
    }
    out["diagnostics"] = {
        "anti_probe_gap": {"iso": iso["anti_probe_gap"], "sub": sub["anti_probe_gap"]},
        "full_rank_spearman_projvar": {"iso": iso["median_spearman_projvar_dO"], "sub": sub["median_spearman_projvar_dO"]},
        "full_rank_spearman_recon": {"iso": iso["median_spearman_recon_dO"], "sub": sub["median_spearman_recon_dO"]},
        "snr_min_arm_dO": min_arm_dO, "snr_max_floor": max_floor,
    }
    out["verdict"] = verdict
    out["GO2_mechanism_replicates"] = all(verdict.values())
    print("===GO2EMB-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
