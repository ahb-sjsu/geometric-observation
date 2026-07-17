# Geometric Observation — Gate B: gradient compression, curvature consumer.
# Governed by prereg/GO-P-2026-010 (sealed fcea7e24; registered commit d3860e9).
# PROSPECTIVE, out-of-sample (optimization, disjoint from Papers I-II). Tests
# whether the GO-2 mechanism (downstream governed by tr(P_C Sigma_delta), not
# reconstruction) generalizes when the read operator P_C is a HESSIAN: a
# compressed gradient's damage is read through the loss curvature. MIT License.
"""GO-2 Gate B: does curvature-metric update distortion flip with H, tracked by proj_var?"""

from __future__ import annotations

import json

import numpy as np

N, D = 1024, 128
SEEDS = 12
R_LAT, R = 16, 8
KAPPA, ETA = 20.0, 0.1
ARMS = ["a_err_in_A", "b_err_in_B", "c_polar_antiprobe", "d_percoord_uniform4"]
CONSUMERS = ["H_A", "H_B", "H_iso"]


def _gradients(seed):  # mean~0, no DC (unlike embeddings/keys)
    sc = np.random.default_rng(2000 + seed).uniform(0.2, 1.5, D).astype(np.float32)
    L = (np.random.default_rng(3000 + seed).standard_normal((D, R_LAT)) / np.sqrt(R_LAT)).astype(np.float32)
    F = np.random.default_rng(4000 + seed).standard_normal((N, R_LAT)).astype(np.float32)
    noise = np.random.default_rng(5000 + seed).standard_t(3, (N, D)).astype(np.float32)
    return (sc[None, :] * (F @ L.T + noise)).astype(np.float32)


def _uniform_asym(x, axis, bits=4):
    q = 2**bits - 1
    lo, hi = x.min(axis=axis, keepdims=True), x.max(axis=axis, keepdims=True)
    scale = np.where((hi - lo) > 0, (hi - lo) / q, 1.0)
    return (lo + np.clip(np.round((x - lo) / scale), 0, q) * scale).astype(np.float32)


def _polar_antiprobe(x, bits=4):
    nrm = np.linalg.norm(x, axis=1, keepdims=True) + 1e-8
    u, q = x / nrm, 2**bits - 1
    uq = np.clip(np.round((u * 0.5 + 0.5) * q), 0, q) / q * 2 - 1
    return (uq * nrm).astype(np.float32)


def _inject(g, eps, Vsub, seed_off, seed):
    """delta_i of norm eps_i: sqrt(1-ETA) in span(Vsub) + sqrt(ETA) in complement."""
    rng = np.random.default_rng(seed_off + seed)
    u = rng.standard_normal((N, Vsub.shape[0])).astype(np.float32)
    u /= (np.linalg.norm(u, axis=1, keepdims=True) + 1e-8)
    s = u @ Vsub
    h = rng.standard_normal((N, D)).astype(np.float32)
    h -= (h @ Vsub.T) @ Vsub
    h /= (np.linalg.norm(h, axis=1, keepdims=True) + 1e-8)
    delta = (np.sqrt(1 - ETA) * s + np.sqrt(ETA) * h) * eps[:, None]
    return (g + delta).astype(np.float32)


def _Hmul(X, Vs):
    """Apply H = I + KAPPA * P_{span(Vs)} to rows of X. Vs=None -> identity."""
    if Vs is None:
        return X
    return X + KAPPA * ((X @ Vs.T) @ Vs)


def _cos_H_distortion(gh, g, Vs):
    Hg, Hgh = _Hmul(g, Vs), _Hmul(gh, Vs)
    xHy = (gh * Hg).sum(1)
    xHx = (gh * Hgh).sum(1)
    yHy = (g * Hg).sum(1)
    cos = xHy / (np.sqrt(np.maximum(xHx, 1e-20) * np.maximum(yHy, 1e-20)) + 1e-20)
    return float((1.0 - cos).mean())


def _proj_var(delta, g, Vs):
    dd = delta - delta.mean(0, keepdims=True)
    gg = g - g.mean(0, keepdims=True)
    if Vs is None:
        return float((dd * dd).sum() / ((gg * gg).sum() + 1e-12))
    num = (dd * dd).sum() + KAPPA * (dd @ Vs.T * (dd @ Vs.T)).sum()
    den = (gg * gg).sum() + KAPPA * (gg @ Vs.T * (gg @ Vs.T)).sum()
    return float(num / (den + 1e-12))


def _spearman4(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return 1.0 - 6.0 * float(((rx - ry) ** 2).sum()) / (4 * 15)


def _tstep_excess(g_seed_rng, Vs, arm_subspace, epsrel, T=30):
    """30-step GD excess loss: compressed-gradient trajectory vs true, on L=0.5 th^T H th."""
    th0 = g_seed_rng.standard_normal(D).astype(np.float32)
    lr = 1.0 / (1.0 + KAPPA)
    def loss(th):
        return 0.5 * float(th @ _Hmul(th[None], Vs)[0])
    L0 = loss(th0)
    th_t, th_c = th0.copy(), th0.copy()
    for _ in range(T):
        gt = _Hmul(th_t[None], Vs)[0]
        th_t = th_t - lr * gt
        gc = _Hmul(th_c[None], Vs)[0]
        # inject eta-mix error of norm epsrel*||gc|| into arm_subspace
        u = g_seed_rng.standard_normal(R).astype(np.float32); u /= np.linalg.norm(u) + 1e-8
        s = u @ arm_subspace
        h = g_seed_rng.standard_normal(D).astype(np.float32)
        h -= (h @ arm_subspace.T) @ arm_subspace; h /= np.linalg.norm(h) + 1e-8
        d = (np.sqrt(1 - ETA) * s + np.sqrt(ETA) * h) * (epsrel * (np.linalg.norm(gc) + 1e-8))
        th_c = th_c - lr * (gc + d)
    return (loss(th_c) - loss(th_t)) / (L0 + 1e-12)


def main():
    dO = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    PV = {C: {a: [] for a in ARMS} for C in CONSUMERS}
    RC = {a: [] for a in ARMS}
    floor = {C: [] for C in CONSUMERS}
    sp_pv = {C: [] for C in CONSUMERS}
    sp_rc = {C: [] for C in CONSUMERS}
    tstep = {"a_H_A": [], "b_H_A": [], "a_H_B": [], "b_H_B": []}

    for seed in range(SEEDS):
        g = _gradients(seed)
        gc = g - g.mean(0, keepdims=True)
        _, _, Vt = np.linalg.svd(gc, full_matrices=False)
        VA, VB = Vt[:R], Vt[R:2 * R]
        d_real = _uniform_asym(g, axis=0)
        eps = np.linalg.norm(d_real - g, axis=1)
        krs = {
            "a_err_in_A": _inject(g, eps, VA, 6000, seed),
            "b_err_in_B": _inject(g, eps, VB, 7000, seed),
            "c_polar_antiprobe": _polar_antiprobe(g),
            "d_percoord_uniform4": d_real,
        }
        recon = {}
        for a in ARMS:
            recon[a] = float((np.linalg.norm(krs[a] - g, axis=1) / (np.linalg.norm(g, axis=1) + 1e-8)).mean())
            RC[a].append(recon[a])
        Vmap = {"H_A": VA, "H_B": VB, "H_iso": None}
        for C in CONSUMERS:
            Vs = Vmap[C]
            floor[C].append(_cos_H_distortion(g.astype(np.float16).astype(np.float32), g, Vs))
            dO_arms, pv_arms, rc_arms = [], [], []
            for a in ARMS:
                dO[C][a].append(_cos_H_distortion(krs[a], g, Vs))
                PV[C][a].append(_proj_var(krs[a] - g, g, Vs))
                dO_arms.append(dO[C][a][-1]); pv_arms.append(PV[C][a][-1]); rc_arms.append(recon[a])
            sp_pv[C].append(_spearman4(pv_arms, dO_arms))
            sp_rc[C].append(_spearman4(rc_arms, dO_arms))
        epsrel = float(np.median(np.linalg.norm(d_real - g, axis=1) / (np.linalg.norm(g, axis=1) + 1e-8)))
        for arm_lbl, Asub in [("a", VA), ("b", VB)]:
            for C_lbl, Vs in [("H_A", VA), ("H_B", VB)]:
                rng = np.random.default_rng(9000 + seed)
                tstep[f"{arm_lbl}_{C_lbl}"].append(_tstep_excess(rng, Vs, Asub, epsrel))

    def med(d):
        return {k: float(np.median(v)) for k, v in d.items()}

    a, b, c = ARMS[0], ARMS[1], ARMS[2]
    out = {"claim": "GO-2 Gate B: gradient curvature", "prereg": "GO-P-2026-010",
           "n_seeds": SEEDS, "kappa": KAPPA, "eta": ETA, "arms": ARMS, "median_recon": med(RC), "consumers": {}}
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
    HA, HB, Hi = out["consumers"]["H_A"], out["consumers"]["H_B"], out["consumers"]["H_iso"]
    min_sp_pv = min(HA["median_spearman_projvar_dO"], HB["median_spearman_projvar_dO"])
    min_sp_rc = min(HA["median_spearman_recon_dO"], HB["median_spearman_recon_dO"])
    loser_dO = {"H_A": max(HA["median_dO"][a], HA["median_dO"][b]), "H_B": max(HB["median_dO"][a], HB["median_dO"][b])}
    winner_dO = {"H_A": min(HA["median_dO"][a], HA["median_dO"][b]), "H_B": min(HB["median_dO"][a], HB["median_dO"][b])}
    max_floor = max(HA["median_noise_floor_dO"], HB["median_noise_floor_dO"])
    recon_gap = abs(out["median_recon"][a] - out["median_recon"][b]) / out["median_recon"][a]
    verdict = {
        "matched_distortion": bool(recon_gap <= 0.02),
        "snr_loser": bool(min(loser_dO.values()) >= 10 * max_floor),
        "flip_decisive": bool(
            HA["median_adv_dO_logbovera"] <= -np.log(1.3) and HB["median_adv_dO_logbovera"] >= np.log(1.3)
            and HA["dO_a_gt_b_seeds"] >= 10 and HB["dO_a_gt_b_seeds"] <= (SEEDS - 10)),
        "proj_tracks_flip": bool(HA["proj_tracks_flip_seeds"] >= 11 and HB["proj_tracks_flip_seeds"] >= 11),
        "recon_fails": bool(min_sp_rc < min_sp_pv),
    }
    out["diagnostics"] = {
        "recon_gap_a_vs_b": recon_gap, "loser_dO": loser_dO, "winner_dO_blind_arm": winner_dO,
        "iso_adv_dO": Hi["median_adv_dO_logbovera"],
        "anti_probe_gap": {"H_A": HA["anti_probe_gap"], "H_B": HB["anti_probe_gap"]},
        "full_rank_spearman_projvar": {"H_A": HA["median_spearman_projvar_dO"], "H_B": HB["median_spearman_projvar_dO"]},
        "full_rank_spearman_recon": {"H_A": HA["median_spearman_recon_dO"], "H_B": HB["median_spearman_recon_dO"]},
        "tstep_excess_loss": {k: float(np.median(v)) for k, v in tstep.items()},
        "snr_max_floor": max_floor,
    }
    out["verdict"] = verdict
    out["GO2_mechanism_generalizes"] = all(verdict.values())
    print("===GO2GB-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
