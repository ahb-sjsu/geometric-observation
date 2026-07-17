# Geometric Observation — GO-4: fixed-budget verdict inverts under budget-matched
# observation, on REAL book-paragraph embeddings from Atlas /archive.
# Governed by prereg/GO-P-2026-015 (sealed 8b0482f1; registered commit ccd7123).
# PROSPECTIVE. Substrate beyond Paper I S5.10 (PREREG_RUNG4): the wavelength
# mechanism on a real 768-d embedding manifold. MIT License.
"""GO-4: does refinement's geometry verdict flip between a fixed and a spectral-gap-matched mode budget?"""

from __future__ import annotations

import glob
import json
import os

import numpy as np
import pyamg
from scipy.sparse import csr_matrix, eye
from scipy.sparse.linalg import lobpcg
from scipy.sparse.csgraph import dijkstra
from sklearn.neighbors import NearestNeighbors

SCRATCH = os.environ.get("GO4_DATA", os.path.dirname(__file__))
N_LEVELS = [2000, 4000, 8000, 16000, 32000]
KNN, M_FIXED, A_ANCHORS, T_TARGETS = 15, 10, 200, 150


def _knn_graph(X, k=KNN):
    nn = NearestNeighbors(n_neighbors=k + 1, metric="cosine", algorithm="brute").fit(X)
    dist, idx = nn.kneighbors(X)                     # includes self at col 0
    n = X.shape[0]
    rows = np.repeat(np.arange(n), k)
    cols = idx[:, 1:].ravel()
    d = dist[:, 1:].ravel()                          # cosine distance in [0,2]
    W = csr_matrix((d, (rows, cols)), shape=(n, n))
    W = W.maximum(W.T)                               # symmetric (union), edge=cosine dist
    sim = W.copy(); sim.data = np.exp(-(W.data ** 2) / (np.median(W.data) ** 2 + 1e-12))
    return W, sim                                    # W: distance graph (geodesics); sim: affinity


def _laplacian_eigs(sim, K):
    deg = np.asarray(sim.sum(1)).ravel()
    dinv = 1.0 / np.sqrt(np.maximum(deg, 1e-12))
    n = sim.shape[0]
    Dinv = csr_matrix((dinv, (np.arange(n), np.arange(n))), shape=(n, n))
    L = eye(n, format="csr") - Dinv @ sim @ Dinv
    L = ((L + L.T) * 0.5).tocsr()
    # Bottom-K eigenpairs via AMG-preconditioned LOBPCG. Result-identical to
    # shift-invert eigsh(sigma=1e-6) -- validated max|dlambda|=3e-15 at N=4000 --
    # but ~5x faster at N=32k (eigsh's sparse-LU fill-in blows up). angle_rho uses
    # row-normalized eigenvector distances, invariant to sign / degenerate-subspace
    # rotation, so identical.
    ml = pyamg.smoothed_aggregation_solver(L, B=np.ones((n, 1)))
    M = ml.aspreconditioner()
    X0 = np.random.default_rng(12345).standard_normal((n, K))
    vals, vecs = lobpcg(L, X0, M=M, tol=1e-7, largest=False, maxiter=800)
    order = np.argsort(vals)
    return vals[order], vecs[:, order]


def _angle_rho(vecs_m, geo, anchors, targets_per_anchor, rng):
    U = vecs_m / (np.linalg.norm(vecs_m, axis=1, keepdims=True) + 1e-12)  # NJW row-normalize
    g_all, a_all = [], []
    n = U.shape[0]
    for ai, a in enumerate(anchors):
        tgt = rng.choice(n, targets_per_anchor, replace=False)
        gd = geo[ai, tgt]
        finite = np.isfinite(gd)
        tgt, gd = tgt[finite], gd[finite]
        ad = np.linalg.norm(U[a][None, :] - U[tgt], axis=1)
        g_all.append(gd); a_all.append(ad)
    g = np.concatenate(g_all); a = np.concatenate(a_all)
    rg = np.argsort(np.argsort(g)).astype(float); ra = np.argsort(np.argsort(a)).astype(float)
    rg -= rg.mean(); ra -= ra.mean()
    return float((rg * ra).sum() / (np.sqrt((rg * rg).sum() * (ra * ra).sum()) + 1e-12))


def _spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx = np.argsort(np.argsort(x)).astype(float); ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx * ry).sum() / (np.sqrt((rx * rx).sum() * (ry * ry).sum()) + 1e-12))


def _process_seed(seed):
    X = np.load(os.path.join(SCRATCH, f"go4_seed{seed}.npy")).astype(np.float32)
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    per_N = {}
    for N in N_LEVELS:
        Xn = X[:N]
        K = min(250, max(30, int(12 * N / 2000) + 24))
        W, sim = _knn_graph(Xn)
        vals, vecs = _laplacian_eigs(sim, K)
        rng = np.random.default_rng(70000 + seed)
        anchors = rng.choice(N, A_ANCHORS, replace=False)
        geo = dijkstra(W, directed=False, indices=anchors)     # (A, N) geodesic distances
        per_N[N] = {"vals": vals, "vecs": vecs, "geo": geo, "anchors": anchors}
        print(f"  seed{seed} N={N} K={K} lambda[10]={vals[10]:.4f} done", flush=True)

    tau = float(per_N[2000]["vals"][10])                       # resolved scale from N_min
    rows = []
    for N in N_LEVELS:
        d = per_N[N]
        rng = np.random.default_rng(80000 + seed + N)
        m_matched = int(np.sum(d["vals"][1:] <= tau))          # # nontrivial modes below tau
        m_matched = max(m_matched, 1)
        ar_fixed = _angle_rho(d["vecs"][:, 1:1 + M_FIXED], d["geo"], d["anchors"], T_TARGETS, rng)
        ar_matched = _angle_rho(d["vecs"][:, 1:1 + m_matched], d["geo"], d["anchors"], T_TARGETS, rng)
        rows.append({"N": N, "m_fixed": M_FIXED, "m_matched": m_matched,
                     "angle_rho_fixed": ar_fixed, "angle_rho_matched": ar_matched})
        print(f"  seed{seed} N={N} m_matched={m_matched} rho_fixed={ar_fixed:.3f} rho_matched={ar_matched:.3f}", flush=True)

    Ns = [r["N"] for r in rows]
    trend_fixed = _spearman(Ns, [r["angle_rho_fixed"] for r in rows])
    trend_matched = _spearman(Ns, [r["angle_rho_matched"] for r in rows])
    m_seq = [r["m_matched"] for r in rows]
    return {"seed": seed, "tau": tau, "rows": rows,
            "trend_fixed": trend_fixed, "trend_matched": trend_matched,
            "m_grows": all(m_seq[i] < m_seq[i + 1] for i in range(len(m_seq) - 1)) or (m_seq[-1] > m_seq[0]),
            "converge_gap_Nmin": abs(rows[0]["angle_rho_fixed"] - rows[0]["angle_rho_matched"])}


def main():
    seeds = [_process_seed(s) for s in range(3)]

    def inv(s):
        return (s["trend_fixed"] - s["trend_matched"] >= 1.0) and (s["trend_matched"] < 0) and (s["trend_fixed"] > 0)

    n_inv = sum(inv(s) for s in seeds)
    n_conv = sum(s["converge_gap_Nmin"] <= 0.05 for s in seeds)
    verdict = {
        "inversion": bool(n_inv >= 2),
        "convergence": bool(n_conv >= 2),
        "mechanism_m_grows": bool(all(s["m_grows"] for s in seeds)),
    }
    out = {"claim": "GO-4 budget inversion (Atlas book embeddings)", "prereg": "GO-P-2026-015",
           "substrate": "Atlas /archive/results_aesthetics/book_translation_cache (768-d book-paragraph embeddings)",
           "n_seeds": 3, "N_levels": N_LEVELS,
           "seeds": [{"seed": s["seed"], "tau": s["tau"], "trend_fixed": s["trend_fixed"],
                      "trend_matched": s["trend_matched"], "inversion": inv(s),
                      "converge_gap_Nmin": s["converge_gap_Nmin"], "m_matched_seq": [r["m_matched"] for r in s["rows"]],
                      "rows": s["rows"]} for s in seeds],
           "n_inversion": n_inv, "n_convergence": n_conv, "verdict": verdict}
    out["GO4_supported"] = all(verdict.values())
    print("===GO4-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
