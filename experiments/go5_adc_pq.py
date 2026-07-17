# Geometric Observation — GO-5 v3: the alpha=1 density quotient restores exact-NN
# recall in locally-scaled ADC / product-quantization retrieval (non-spectral).
# Governed by prereg/GO-P-2026-018 (sealed 50a18fcb; registered commit 5ec52c5).
# PROSPECTIVE. Substrate: real 768-d Atlas book embeddings. PQ-induced hubness is a
# density nuisance orthogonal to the exact full-precision NN invariant; ADC is
# density-biased, so the alpha=1 quotient has something real to correct. MIT License.
"""GO-5 v3 (ADC/PQ): does s_qj = W_qj/q_j^alpha at alpha=1 restore exact-NN recall?"""

from __future__ import annotations

import json
import os

import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors

SCRATCH = os.environ.get("GO4_DATA", os.path.dirname(__file__))
NDB, Q, R, D = 10000, 1000, 1000, 768
M_SUB, KC, KREC = 16, 256, 10
DSUB = D // M_SUB
ALPHAS = [0.0, 0.5, 1.0, 1.5]


def _unit(X):
    return (X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)).astype(np.float32)


def _skew(v):
    v = np.asarray(v, float); m = v.mean(); s = v.std()
    return float(((v - m) ** 3).mean() / (s ** 3 + 1e-12))


def _train_pq(db, seed):
    cents = np.zeros((M_SUB, KC, DSUB), dtype=np.float32)
    codes = np.zeros((NDB, M_SUB), dtype=np.int32)
    for s in range(M_SUB):
        sub = db[:, s * DSUB:(s + 1) * DSUB]
        km = MiniBatchKMeans(n_clusters=KC, n_init=3, max_iter=50, batch_size=2048,
                             random_state=seed * 100 + s).fit(sub)
        cents[s] = km.cluster_centers_
        codes[:, s] = km.labels_
    return cents, codes


def _adc(queries, cents, codes):
    """ADC squared-distance (n_q, NDB): query full-precision, db PQ-coded."""
    out = np.zeros((queries.shape[0], NDB), dtype=np.float32)
    for s in range(M_SUB):
        qsub = queries[:, s * DSUB:(s + 1) * DSUB]                 # (n_q, DSUB)
        d2 = ((qsub[:, None, :] - cents[s][None, :, :]) ** 2).sum(-1)  # (n_q, KC)
        out += d2[:, codes[:, s]]                                  # gather per db code
    return out


def _run(seed):
    X = _unit(np.load(os.path.join(SCRATCH, f"go4_seed{seed}.npy")).astype(np.float32))
    db, queries, ref = X[:NDB], X[NDB:NDB + Q], X[NDB + Q:NDB + Q + R]
    # invariant: exact full-precision 10-NN
    true = NearestNeighbors(n_neighbors=KREC).fit(db).kneighbors(queries, return_distance=False)

    cents, codes = _train_pq(db, seed)
    adc_q = _adc(queries, cents, codes)                            # (Q, NDB) squared ADC
    adc_r = _adc(ref, cents, codes)                               # (R, NDB)
    eps = float(np.median(adc_q)) + 1e-12
    Wq = np.exp(-adc_q / eps)
    Wr = np.exp(-adc_r / eps)
    q_dens = Wr.sum(0) + 1e-12                                     # db density from held-out ref bank

    out = {}
    for a in ALPHAS:
        s = Wq / (q_dens[None, :] ** a)
        top = np.argpartition(-s, KREC, axis=1)[:, :KREC]
        rec = np.mean([len(set(top[i]) & set(true[i])) / KREC for i in range(Q)])
        occ = np.bincount(top.ravel(), minlength=NDB)             # k-occurrence over queries
        out[a] = {"recall": float(rec), "hub_skew": _skew(occ)}
    # diagnostics: exact recall ceiling is 1.0 by construction; report raw-ADC recall = out[0]
    return out


def main():
    seeds = [0, 1, 2]
    res = {s: _run(s) for s in seeds}

    def rec(s, a):
        return res[s][a]["recall"]

    gains = [rec(s, 1.0) - rec(s, 0.0) for s in seeds]
    a1opt = []
    for s in seeds:
        best = max(res[s][a]["recall"] for a in ALPHAS)
        a1opt.append((rec(s, 1.0) >= best - 0.005) and (rec(s, 1.0) > rec(s, 0.0)))
    hub_down = [res[s][1.0]["hub_skew"] < res[s][0.0]["hub_skew"] for s in seeds]
    base_hub = [res[s][0.0]["hub_skew"] >= 0.5 for s in seeds]

    verdict = {
        "baseline_hubness": bool(sum(base_hub) >= 2),
        "restoration": bool(float(np.median(gains)) >= 0.02 and all(g > 0 for g in gains)),
        "alpha1_optimal": bool(sum(a1opt) >= 2),
        "hubness_reduced": bool(all(hub_down)),
    }
    out = {
        "claim": "GO-5 alpha=1 quotient (ADC/PQ, non-spectral)", "prereg": "GO-P-2026-018",
        "alphas": ALPHAS, "n_seeds": len(seeds),
        "per_seed": {str(s): {"recall": {str(a): rec(s, a) for a in ALPHAS},
                              "hub_skew": {str(a): res[s][a]["hub_skew"] for a in ALPHAS},
                              "gain_1_minus_0": rec(s, 1.0) - rec(s, 0.0),
                              "alpha1_optimal": a1opt[i]} for i, s in enumerate(seeds)},
        "median_gain": float(np.median(gains)),
        "verdict": verdict,
    }
    out["GO5_supported"] = all(verdict.values())
    print("===GO5-JSON===")
    print(json.dumps(out, indent=2))
    print("===END===")


if __name__ == "__main__":
    main()
