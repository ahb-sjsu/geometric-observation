# Geometric Observation — GO-5 v4: the alpha=1 density quotient restores geodesic
# recall in NON-SPECTRAL diffusion-distance retrieval (P^t by matrix powers, no
# eigendecomposition). Governed by prereg/GO-P-2026-019 (sealed 62af7093;
# registered commit 4b587cd). PROSPECTIVE. The domain where density lives in the
# retrieval base (the random walk) and is orthogonal to geometry. MIT License.
"""GO-5 v4: does alpha=1 (Laplace-Beltrami) diffusion distance restore geodesic-NN recall?"""

from __future__ import annotations

import json

import numpy as np
from sklearn.neighbors import NearestNeighbors

N, Q, DAMB, DLAT, KNN, KREC, T = 4000, 1000, 50, 2, 15, 10, 3
ALPHAS = [0.0, 0.5, 1.0, 1.5]


def _substrate(seed, uniform=False):
    rng = np.random.default_rng(seed)
    if uniform:
        u1 = rng.random(N)
    else:
        r = rng.random(N)
        u1 = np.log1p(r * (np.exp(3.0) - 1.0)) / 3.0             # density p(u1) ~ exp(3 u1)
    u = np.column_stack([u1, rng.random(N)]).astype(np.float32)  # latent geometry (uniform in u2)
    A = rng.standard_normal((DAMB, DLAT)).astype(np.float32)
    x = (u @ A.T + 0.01 * rng.standard_normal((N, DAMB))).astype(np.float32)
    return u, x


def _sqdist(X):
    g = X @ X.T
    d2 = np.diag(g)[:, None] + np.diag(g)[None, :] - 2 * g
    return np.maximum(d2, 0.0)


def _kernel(x):
    Dx = _sqdist(x)
    idx = np.argsort(Dx, axis=1)[:, 1:KNN + 1]                   # kNN (exclude self)
    eps = float(np.median(Dx[np.arange(N)[:, None], idx])) + 1e-12
    W = np.zeros((N, N), dtype=np.float64)
    for i in range(N):
        W[i, idx[i]] = np.exp(-Dx[i, idx[i]] / eps)
    W = np.maximum(W, W.T)                                        # symmetric kNN affinity
    return W


def _diffusion_recall(W, alpha, u_true_nn, qi):
    q = W.sum(1) + 1e-12                                          # density
    Wa = W / np.power(np.outer(q, q), alpha)                     # Coifman-Lafon alpha-normalization
    d = Wa.sum(1) + 1e-12
    P = Wa / d[:, None]                                          # row-stochastic transition
    Psi = np.linalg.matrix_power(P, T)                           # P^t by MATRIX POWERS (non-spectral)
    pi = d / d.sum()
    Phi = (Psi / np.sqrt(pi)[None, :]).astype(np.float64)        # pi-weighted diffusion coords
    # diffusion distance from Q queries to all N
    Phiq = Phi[qi]
    g = Phiq @ Phi.T
    sq = (Phiq * Phiq).sum(1)[:, None] + (Phi * Phi).sum(1)[None, :] - 2 * g
    np.put_along_axis(sq, qi[:, None], np.inf, axis=1)           # exclude self
    top = np.argpartition(sq, KREC, axis=1)[:, :KREC]
    rec = np.mean([len(set(top[i]) & set(u_true_nn[i])) / KREC for i in range(len(qi))])
    return float(rec), float(q.max() / q.min())


def _run(seed, uniform=False):
    u, x = _substrate(seed, uniform)
    qi = np.random.default_rng(500 + seed).choice(N, Q, replace=False)
    true_nn = NearestNeighbors(n_neighbors=KREC + 1).fit(u).kneighbors(u[qi], return_distance=False)[:, 1:]
    W = _kernel(x)
    out, dens_ratio = {}, None
    for a in ALPHAS:
        rec, dr = _diffusion_recall(W, a, true_nn, qi)
        out[a] = rec
        if a == 0.0:
            dens_ratio = dr
    return out, dens_ratio


def main():
    seeds = [0, 1, 2]
    res, ratios = {}, {}
    for s in seeds:
        res[s], ratios[s] = _run(s)
    ctrl, _ = _run(0, uniform=True)

    gains = [res[s][1.0] - res[s][0.0] for s in seeds]
    a1opt = []
    for s in seeds:
        best = max(res[s][a] for a in ALPHAS)
        a1opt.append((res[s][1.0] >= best - 0.005) and (res[s][1.0] > res[s][0.0]))
    dens_ok = [ratios[s] >= 5.0 for s in seeds]

    verdict = {
        "density_regime": bool(sum(dens_ok) >= 2),
        "restoration": bool(float(np.median(gains)) >= 0.03 and all(g > 0 for g in gains)),
        "alpha1_optimal": bool(sum(a1opt) >= 2),
    }
    out = {
        "claim": "GO-5 alpha=1 diffusion-distance (non-spectral)", "prereg": "GO-P-2026-019",
        "alphas": ALPHAS, "n_seeds": len(seeds),
        "per_seed": {str(s): {"recall": {str(a): res[s][a] for a in ALPHAS},
                              "density_ratio": ratios[s],
                              "gain_1_minus_0": res[s][1.0] - res[s][0.0],
                              "alpha1_optimal": a1opt[i]} for i, s in enumerate(seeds)},
        "median_gain": float(np.median(gains)),
        "specificity_control_uniform": {"recall": {str(a): ctrl[a] for a in ALPHAS},
                                        "gain_1_minus_0": ctrl[1.0] - ctrl[0.0]},
        "verdict": verdict,
    }
    out["GO5_supported"] = all(verdict.values())
    print("===GO5-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
