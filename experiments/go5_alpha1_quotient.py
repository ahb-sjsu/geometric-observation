# Geometric Observation — GO-5: the alpha=1 density/hubness quotient restores
# invariant fidelity in a NON-SPECTRAL domain (locally-scaled NN retrieval).
# Governed by prereg/GO-P-2026-016 (sealed 3906cac4; registered commit 7b221fc).
# PROSPECTIVE. The diffusion-map density-cancellation exponent alpha=1, applied
# directly to retrieval ranking (no eigenvectors), recovers the latent-neighbor
# invariant that sampling-density hubness corrupts. MIT License.
"""GO-5: does s_ij = W_ij/(q_i q_j)^alpha at alpha=1 restore true-neighbor recall?"""

from __future__ import annotations

import json

import numpy as np
from sklearn.neighbors import NearestNeighbors

N, D, DLAT, Q, KREC = 8000, 128, 8, 1000, 10
ALPHAS = [0.0, 0.5, 1.0, 1.5]


def _latent(seed, uniform=False):
    rng = np.random.default_rng(seed)
    if uniform:
        z = rng.standard_normal((N, DLAT)) * 3.0           # single Gaussian ~ uniform density
    else:
        M = 30
        centers = rng.standard_normal((M, DLAT)) * 3.0
        w = rng.dirichlet(np.ones(M) * 0.3)                # sparse -> few dense clusters (hubs)
        comp = rng.choice(M, N, p=w)
        z = centers[comp] + 0.15 * rng.standard_normal((N, DLAT))
    A = rng.standard_normal((D, DLAT)).astype(np.float32)
    x = (z @ A.T + 0.02 * rng.standard_normal((N, D))).astype(np.float32)
    return z.astype(np.float32), x


def _sqdist(X):
    g = X @ X.T
    d2 = np.diag(g)[:, None] + np.diag(g)[None, :] - 2 * g
    return np.maximum(d2, 0.0)


def _skew(v):
    v = np.asarray(v, float)
    m = v.mean(); s = v.std()
    return float(((v - m) ** 3).mean() / (s ** 3 + 1e-12))


def _run(seed, uniform=False):
    z, x = _latent(seed, uniform)
    # true latent neighbors (the invariant) for Q queries
    qi = np.random.default_rng(9000 + seed).choice(N, Q, replace=False)
    nn_z = NearestNeighbors(n_neighbors=KREC + 1).fit(z)
    true = nn_z.kneighbors(z[qi], return_distance=False)[:, 1:]   # (Q, KREC)

    Dx = _sqdist(x)                                               # (N,N) sq euclidean in x
    np.fill_diagonal(Dx, np.inf)
    sig = np.sqrt(np.sort(Dx, axis=1)[:, 6])                      # 7th-NN distance (self excluded)
    W = np.exp(-Dx / (sig[:, None] * sig[None, :] + 1e-12)).astype(np.float32)
    np.fill_diagonal(W, 0.0)
    q = W.sum(1) + 1e-12                                          # density

    out = {}
    for a in ALPHAS:
        qinv = q ** (-a)
        s_q = W[qi] * qinv[None, :]                               # rank rows only need /q_j^alpha
        top = np.argpartition(-s_q, KREC, axis=1)[:, :KREC]
        rec = np.mean([len(set(top[i]) & set(true[i])) / KREC for i in range(Q)])
        # hubness: k-occurrence over ALL points, skew
        s_all = W * qinv[None, :]
        topk_all = np.argpartition(-s_all, KREC, axis=1)[:, :KREC]
        occ = np.bincount(topk_all.ravel(), minlength=N)
        out[a] = {"recall": float(rec), "hub_skew": _skew(occ)}
    return out


def main():
    seeds = [0, 1, 2]
    res = {s: _run(s) for s in seeds}
    ctrl = _run(0, uniform=True)

    def rec(s, a):
        return res[s][a]["recall"]

    gains = [rec(s, 1.0) - rec(s, 0.0) for s in seeds]
    argmax_is_1 = []
    for s in seeds:
        best = max(res[s][a]["recall"] for a in ALPHAS)
        argmax_is_1.append((res[s][1.0]["recall"] >= best - 0.01) and (rec(s, 1.0) > rec(s, 0.0)))
    hub_down = [res[s][1.0]["hub_skew"] < res[s][0.0]["hub_skew"] for s in seeds]

    verdict = {
        "restoration": bool(float(np.median(gains)) >= 0.05 and all(g > 0 for g in gains)),
        "alpha1_optimal": bool(sum(argmax_is_1) >= 2),
        "hubness_reduced": bool(all(hub_down)),
    }
    out = {
        "claim": "GO-5 alpha=1 density quotient (non-spectral)", "prereg": "GO-P-2026-016",
        "alphas": ALPHAS, "n_seeds": len(seeds),
        "per_seed": {str(s): {"recall": {str(a): res[s][a]["recall"] for a in ALPHAS},
                              "hub_skew": {str(a): res[s][a]["hub_skew"] for a in ALPHAS},
                              "gain_1_minus_0": rec(s, 1.0) - rec(s, 0.0),
                              "alpha1_optimal": argmax_is_1[i]} for i, s in enumerate(seeds)},
        "median_gain": float(np.median(gains)),
        "specificity_control_uniform": {"recall": {str(a): ctrl[a]["recall"] for a in ALPHAS},
                                        "gain_1_minus_0": ctrl[1.0]["recall"] - ctrl[0.0]["recall"]},
        "verdict": verdict,
    }
    out["GO5_supported"] = all(verdict.values())
    print("===GO5-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
