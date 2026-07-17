# Geometric Observation — GO-2 instance 2': retrieval, reconstruction-matched probes.
# Governed by prereg/GO-P-2026-008 (sealed 93715130; registered commit 74b29a1).
# PROSPECTIVE. Tests whether, at IDENTICAL reconstruction, retrieval ranking flips
# with the consumer's read subspace -- tracked by proj_var, invisible to
# reconstruction -- in the recon-matched regime NEG-10 delimits. MIT License.
"""GO-2 instance 2': matched-distortion subspace probes on retrieval ranking."""

from __future__ import annotations

import json

import numpy as np

N, D = 1024, 128
SEEDS = 12
N_Q, R_LAT, R = 128, 16, 8
ARMS = ["a_err_in_A", "b_err_in_B", "c_polar_antiprobe", "d_periitem_uniform4"]
CONSUMERS = ["read_A", "read_B", "iso"]


def _embeddings(seed):
    dc = np.random.default_rng(1000 + seed).uniform(-6, 6, D).astype(np.float32)
    sc = np.random.default_rng(2000 + seed).uniform(0.2, 1.5, D).astype(np.float32)
    L = (np.random.default_rng(3000 + seed).standard_normal((D, R_LAT)) / np.sqrt(R_LAT)).astype(np.float32)
    F = np.random.default_rng(4000 + seed).standard_normal((N, R_LAT)).astype(np.float32)
    noise = np.random.default_rng(5000 + seed).standard_t(3, (N, D)).astype(np.float32)
    return (dc[None, :] + sc[None, :] * (F @ L.T + noise)).astype(np.float32)


def _periitem_uniform4(E, bits=4):
    q = 2**bits - 1
    lo, hi = E.min(1, keepdims=True), E.max(1, keepdims=True)
    scale = np.where((hi - lo) > 0, (hi - lo) / q, 1.0)
    return (lo + np.clip(np.round((E - lo) / scale), 0, q) * scale).astype(np.float32)


def _polar_antiprobe(E, bits=4):
    nrm = np.linalg.norm(E, axis=1, keepdims=True) + 1e-8
    u, q = E / nrm, 2**bits - 1
    uq = np.clip(np.round((u * 0.5 + 0.5) * q), 0, q) / q * 2 - 1
    return (uq * nrm).astype(np.float32)


def _inject(E, eps, Vsub, seed_off, seed):
    """Add a per-item random error of norm eps_i lying in span(Vsub) (rows orthonormal)."""
    u = np.random.default_rng(seed_off + seed).standard_normal((N, Vsub.shape[0])).astype(np.float32)
    u /= (np.linalg.norm(u, axis=1, keepdims=True) + 1e-8)
    delta = (u @ Vsub) * eps[:, None]        # (N,D), ||delta_i|| = eps_i, in span(Vsub)
    return (E + delta).astype(np.float32)


def _rank_rows(A):
    return np.argsort(np.argsort(A, axis=1), axis=1).astype(np.float64)


def _one_minus_spearman(S0, Sr):
    r0, rr = _rank_rows(S0), _rank_rows(Sr)
    r0 -= r0.mean(1, keepdims=True)
    rr -= rr.mean(1, keepdims=True)
    num = (r0 * rr).sum(1)
    den = np.sqrt((r0 * r0).sum(1) * (rr * rr).sum(1)) + 1e-12
    return float((1.0 - num / den).mean())


def _spearman4(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return 1.0 - 6.0 * float(((rx - ry) ** 2).sum()) / (4 * 15)


def _proj_var(delta, E, Vsub):
    dd = delta - delta.mean(0, keepdims=True)
    ee = E - E.mean(0, keepdims=True)
    pd, pe = dd @ Vsub.T, ee @ Vsub.T
    return float((pd * pd).sum() / ((pe * pe).sum() + 1e-12))


def main():
    dO = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    PV = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    RC = {a: [] for a in ARMS}
    floor = {C: [] for C in CONSUMERS}
    sp_pv = {C: [] for C in CONSUMERS}
    sp_rc = {C: [] for C in CONSUMERS}

    for seed in range(SEEDS):
        E = _embeddings(seed)
        Ec = E - E.mean(0, keepdims=True)
        _, _, Vt = np.linalg.svd(Ec, full_matrices=False)
        VA, VB = Vt[:R], Vt[R:2 * R]                       # read subspaces (R,D) each
        d_real = _periitem_uniform4(E)
        eps = np.linalg.norm(d_real - E, axis=1)           # per-item 4-bit distortion budget
        krs = {
            "a_err_in_A": _inject(E, eps, VA, 6000, seed),
            "b_err_in_B": _inject(E, eps, VB, 7000, seed),
            "c_polar_antiprobe": _polar_antiprobe(E),
            "d_periitem_uniform4": d_real,
        }
        recon = {}
        for a in ARMS:
            recon[a] = float((np.linalg.norm(krs[a] - E, axis=1) / (np.linalg.norm(E, axis=1) + 1e-8)).mean())
            RC[a].append(recon[a])
        Vmap = {"read_A": VA, "read_B": VB}
        for C in CONSUMERS:
            if C == "iso":
                Q = np.random.default_rng(300 + seed).standard_normal((N_Q, D)).astype(np.float32)
                Vc = VA  # proj_var reference subspace irrelevant for iso diagnostic; use VA
            else:
                Vc = Vmap[C]
                Q = np.random.default_rng(400 + seed).standard_normal((N_Q, R)).astype(np.float32) @ Vc
            Q = Q / (np.linalg.norm(Q, axis=1, keepdims=True) + 1e-8)
            S0 = Q @ E.T
            floor[C].append(_one_minus_spearman(S0, Q @ E.astype(np.float16).astype(np.float32).T))
            dO_arms, pv_arms, rc_arms = [], [], []
            for a in ARMS:
                dO[C][a].append(_one_minus_spearman(S0, Q @ krs[a].T))
                PV[C][a].append(_proj_var(krs[a] - E, E, Vc))
                dO_arms.append(dO[C][a][-1]); pv_arms.append(PV[C][a][-1]); rc_arms.append(recon[a])
            sp_pv[C].append(_spearman4(pv_arms, dO_arms))
            sp_rc[C].append(_spearman4(rc_arms, dO_arms))

    def med(d):
        return {k: float(np.median(v)) for k, v in d.items()}

    a, b, c = ARMS[0], ARMS[1], ARMS[2]
    out = {"claim": "GO-2 retrieval matched-distortion (instance 2')", "prereg": "GO-P-2026-008",
           "n_seeds": SEEDS, "arms": ARMS, "median_recon": med(RC), "consumers": {}}
    for C in CONSUMERS:
        adv_dO = [np.log(dO[C][b][i] / dO[C][a][i]) for i in range(SEEDS)]
        adv_pv = [np.log((PV[C][b][i] + 1e-12) / (PV[C][a][i] + 1e-12)) for i in range(SEEDS)]
        a_gt_b = sum(1 for i in range(SEEDS) if dO[C][a][i] > dO[C][b][i])
        out["consumers"][C] = {
            "median_dO": med(dO[C]), "median_proj_var": med(PV[C]),
            "median_adv_dO_logbovera": float(np.median(adv_dO)),
            "median_adv_projvar_logbovera": float(np.median(adv_pv)),
            "dO_a_gt_b_seeds": int(a_gt_b),
            "proj_tracks_flip_seeds": int(sum(1 for i in range(SEEDS) if np.sign(adv_pv[i]) == np.sign(adv_dO[i]))),
            "median_spearman_projvar_dO": float(np.median(sp_pv[C])),
            "median_spearman_recon_dO": float(np.median(sp_rc[C])),
            "median_noise_floor_dO": float(np.median(floor[C])),
            "anti_probe_gap": med(dO[C])[c] / med(dO[C])[a],
        }
    rA, rB, iso = out["consumers"]["read_A"], out["consumers"]["read_B"], out["consumers"]["iso"]
    min_sp_pv = min(rA["median_spearman_projvar_dO"], rB["median_spearman_projvar_dO"])
    min_sp_rc = min(rA["median_spearman_recon_dO"], rB["median_spearman_recon_dO"])
    min_arm_dO = min(min(rA["median_dO"].values()), min(rB["median_dO"].values()))
    max_floor = max(rA["median_noise_floor_dO"], rB["median_noise_floor_dO"])
    recon_gap = abs(out["median_recon"][a] - out["median_recon"][b]) / out["median_recon"][a]
    verdict = {
        "matched_distortion": bool(recon_gap <= 0.02),
        "snr": bool(min_arm_dO >= 10 * max_floor),
        "flip_decisive": bool(
            rA["median_adv_dO_logbovera"] <= -np.log(1.3) and rB["median_adv_dO_logbovera"] >= np.log(1.3)
            and rA["dO_a_gt_b_seeds"] >= 10 and rB["dO_a_gt_b_seeds"] <= (SEEDS - 10)),
        "proj_tracks_flip": bool(rA["proj_tracks_flip_seeds"] >= 11 and rB["proj_tracks_flip_seeds"] >= 11),
        "recon_fails": bool(min_sp_rc < min_sp_pv),
    }
    out["diagnostics"] = {
        "recon_gap_a_vs_b": recon_gap,
        "iso_adv_dO": iso["median_adv_dO_logbovera"],
        "anti_probe_gap": {"read_A": rA["anti_probe_gap"], "read_B": rB["anti_probe_gap"]},
        "full_rank_spearman_projvar": {"read_A": rA["median_spearman_projvar_dO"], "read_B": rB["median_spearman_projvar_dO"]},
        "full_rank_spearman_recon": {"read_A": rA["median_spearman_recon_dO"], "read_B": rB["median_spearman_recon_dO"]},
        "snr_min_arm_dO": min_arm_dO, "snr_max_floor": max_floor,
    }
    out["verdict"] = verdict
    out["GO2_mechanism_replicates"] = all(verdict.values())
    print("===GO2RM-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
