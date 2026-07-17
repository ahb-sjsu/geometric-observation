# Geometric Observation — GO-1: blinded-probe identifiability of the read subspace.
# Governed by prereg/GO-P-2026-011 (sealed 2ec99ec4; registered commit 73e03d3).
# PROSPECTIVE + BLINDED. Tests whether the consumer's invariant/nuisance split (its
# read operator P_C) is identifiable EX ANTE from the consumer functional alone: a
# black-box sensitivity probe queries C(.) and returns an estimated read subspace,
# never seeing the planted subspace, the compression arms, or d_O. MIT License.
"""GO-1: does a blind probe recover the consumer's read subspace, and does it predict the flip?"""

from __future__ import annotations

import json

import numpy as np

N, D = 512, 128
SEEDS = 12
R, ETA = 8, 0.1
N_BASE, N_PROBE, H_FD = 8, 256, 1e-2
ARMS = ["a_err_in_A", "b_err_in_B", "c_polar_antiprobe", "d_percoord_uniform4"]
CONSUMERS = ["C_A", "C_B"]


def _rep(seed):  # low-rank embeddings (representation distribution)
    dc = np.random.default_rng(1000 + seed).uniform(-6, 6, D).astype(np.float32)
    sc = np.random.default_rng(2000 + seed).uniform(0.2, 1.5, D).astype(np.float32)
    L = (np.random.default_rng(3000 + seed).standard_normal((D, 16)) / 4).astype(np.float32)
    F = np.random.default_rng(4000 + seed).standard_normal((N, 16)).astype(np.float32)
    noise = np.random.default_rng(5000 + seed).standard_t(3, (N, D)).astype(np.float32)
    return (dc[None, :] + sc[None, :] * (F @ L.T + noise)).astype(np.float32)


# ---- the BLINDED probe: receives only C(.) and (D, r) [+ base points from the input dist] ----
def blinded_probe(C, D, r, base_points, rng, n_probe=N_PROBE, h=H_FD):
    M = np.zeros((D, D), dtype=np.float64)
    for x0 in base_points:
        U = rng.standard_normal((n_probe, D)).astype(np.float32)
        U /= (np.linalg.norm(U, axis=1, keepdims=True) + 1e-8)
        dC = (C(x0[None, :] + h * U) - C(x0[None, :] - h * U)) / (2 * h)   # (n_probe, m)
        Jt = np.linalg.pinv(U) @ dC                                        # (D, m), J^T
        M += (Jt @ Jt.T).astype(np.float64)
    w, V = np.linalg.eigh(M)
    return V[:, -r:].astype(np.float32)                                    # top-r eigvecs (D, r)


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


def _inject(x, eps, Vsub, seed_off, seed):
    rng = np.random.default_rng(seed_off + seed)
    u = rng.standard_normal((N, Vsub.shape[0])).astype(np.float32)
    u /= (np.linalg.norm(u, axis=1, keepdims=True) + 1e-8)
    s = u @ Vsub
    g = rng.standard_normal((N, D)).astype(np.float32)
    g -= (g @ Vsub.T) @ Vsub
    g /= (np.linalg.norm(g, axis=1, keepdims=True) + 1e-8)
    delta = (np.sqrt(1 - ETA) * s + np.sqrt(ETA) * g) * eps[:, None]
    return (x + delta).astype(np.float32)


def _overlap(U, Vt):  # both (D,r) orthonormal; mean squared principal-angle cosine in [0,1]
    return float(((U.T @ Vt) ** 2).sum() / U.shape[1])


def _proj_var(delta, x, S):  # S: (D,r) orthonormal read subspace
    dd = delta - delta.mean(0, keepdims=True)
    xx = x - x.mean(0, keepdims=True)
    return float((dd @ S * (dd @ S)).sum() / ((xx @ S * (xx @ S)).sum() + 1e-12))


def _spearman4(a, b):
    ra, rb = np.argsort(np.argsort(a)).astype(float), np.argsort(np.argsort(b)).astype(float)
    return 1.0 - 6.0 * float(((ra - rb) ** 2).sum()) / (4 * 15)


def _dO(C, x, xhat):
    c0, cr = C(x), C(xhat)
    return float(np.linalg.norm(cr - c0, axis=1).mean() / (np.linalg.norm(c0, axis=1).mean() + 1e-12))


def main():
    rec = {"overlap": [], "overlap_rand": [], "recon_gap": []}
    per = {C: {"adv_dO": [], "adv_projhat": [], "loser": [], "floor": [],
               "sp_recon": [], "sp_projhat": [], "sp_projtrue": []} for C in CONSUMERS}

    for seed in range(SEEDS):
        x = _rep(seed)
        V = np.linalg.qr(np.random.default_rng(6000 + seed).standard_normal((D, D)))[0].astype(np.float32)
        WA, WB = V[:R].copy(), V[R:2 * R].copy()          # (r,D) orthonormal rows = read directions
        Strue = {"C_A": WA.T, "C_B": WB.T}                # (D,r) read subspaces
        Cfun = {"C_A": (lambda X, W=WA: np.tanh(X @ W.T)),
                "C_B": (lambda X, W=WB: np.tanh(X @ W.T))}
        base = x[np.random.default_rng(7000 + seed).choice(N, N_BASE, replace=False)]

        # ---- BLIND: probe each consumer with only its handle; recover Shat ----
        Shat = {}
        for C in CONSUMERS:
            Shat[C] = blinded_probe(Cfun[C], D, R, base, np.random.default_rng(8000 + seed))
        rec["overlap"].append(min(_overlap(Shat["C_A"], Strue["C_A"]), _overlap(Shat["C_B"], Strue["C_B"])))
        Srand = np.linalg.qr(np.random.default_rng(8888 + seed).standard_normal((D, R)))[0].astype(np.float32)
        rec["overlap_rand"].append(_overlap(Srand, Strue["C_A"]))

        d_real = _uniform_asym(x, axis=0)
        eps = np.linalg.norm(d_real - x, axis=1)
        krs = {"a_err_in_A": _inject(x, eps, WA, 100, seed), "b_err_in_B": _inject(x, eps, WB, 200, seed),
               "c_polar_antiprobe": _polar_antiprobe(x), "d_percoord_uniform4": d_real}
        recon = {a: float((np.linalg.norm(krs[a] - x, axis=1) / (np.linalg.norm(x, axis=1) + 1e-8)).mean()) for a in ARMS}
        rec["recon_gap"].append(abs(recon["a_err_in_A"] - recon["b_err_in_B"]) / recon["a_err_in_A"])

        for C in CONSUMERS:
            dO = {a: _dO(Cfun[C], x, krs[a]) for a in ARMS}
            pvh = {a: _proj_var(krs[a] - x, x, Shat[C]) for a in ARMS}       # BLIND projection
            pvt = {a: _proj_var(krs[a] - x, x, Strue[C]) for a in ARMS}      # true (diagnostic)
            a_, b_ = "a_err_in_A", "b_err_in_B"
            per[C]["adv_dO"].append(np.log(dO[b_] / dO[a_]))
            per[C]["adv_projhat"].append(np.log((pvh[b_] + 1e-12) / (pvh[a_] + 1e-12)))
            per[C]["loser"].append(max(dO[a_], dO[b_]))
            per[C]["floor"].append(_dO(Cfun[C], x, x.astype(np.float16).astype(np.float32)))
            arms_dO = [dO[a] for a in ARMS]
            per[C]["sp_recon"].append(_spearman4([recon[a] for a in ARMS], arms_dO))
            per[C]["sp_projhat"].append(_spearman4([pvh[a] for a in ARMS], arms_dO))
            per[C]["sp_projtrue"].append(_spearman4([pvt[a] for a in ARMS], arms_dO))

    def md(v):
        return float(np.median(v))

    out = {"claim": "GO-1 blinded-probe identifiability", "prereg": "GO-P-2026-011",
           "n_seeds": SEEDS, "arms": ARMS,
           "median_min_overlap": md(rec["overlap"]), "median_overlap_random_baseline": md(rec["overlap_rand"]),
           "recon_gap_a_vs_b": md(rec["recon_gap"]), "consumers": {}}
    for C in CONSUMERS:
        p = per[C]
        signagree = int(sum(1 for i in range(SEEDS) if np.sign(p["adv_projhat"][i]) == np.sign(p["adv_dO"][i])))
        out["consumers"][C] = {
            "median_adv_dO_logbovera": md(p["adv_dO"]), "median_adv_projhat_logbovera": md(p["adv_projhat"]),
            "blind_sign_agree_seeds": signagree, "median_loser_dO": md(p["loser"]), "median_floor_dO": md(p["floor"]),
            "median_spearman_recon_dO": md(p["sp_recon"]), "median_spearman_projhat_dO": md(p["sp_projhat"]),
            "median_spearman_projtrue_dO": md(p["sp_projtrue"]),
        }
    A, B = out["consumers"]["C_A"], out["consumers"]["C_B"]
    min_sp_rc = min(A["median_spearman_recon_dO"], B["median_spearman_recon_dO"])
    min_sp_ph = min(A["median_spearman_projhat_dO"], B["median_spearman_projhat_dO"])
    min_loser = min(A["median_loser_dO"], B["median_loser_dO"])
    max_floor = max(A["median_floor_dO"], B["median_floor_dO"])
    verdict = {
        "subspace_recovery": bool(out["median_min_overlap"] >= 0.90),
        "blind_predicts_flip": bool(
            A["blind_sign_agree_seeds"] >= 11 and B["blind_sign_agree_seeds"] >= 11
            and A["median_adv_dO_logbovera"] <= -np.log(1.3) and B["median_adv_dO_logbovera"] >= np.log(1.3)),
        "recon_fails": bool(min_sp_rc < min_sp_ph),
        "matched_distortion": bool(out["recon_gap_a_vs_b"] <= 0.02),
        "snr_loser": bool(min_loser >= 10 * max_floor),
    }
    out["verdict"] = verdict
    out["GO1_supported"] = all(verdict.values())
    print("===GO1-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
