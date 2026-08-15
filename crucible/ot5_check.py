"""OT-5: the regime boundary, constants per PREREG-OT5-APPENDIX.md.

    .venv/Scripts/python crucible/ot5_check.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import blind_probe          # noqa: E402
from readscope.regimes import applicability      # noqa: E402

SEED = 20260815
D = 64
K = 16
TEMPS = [3.0, 1.0, 0.3, 0.1, 0.03, 0.01]
N_PTS = 24
N_DF_PTS = 200
N_PAIRS = 30
N_DRAWS = 2000
TRACE = 0.01
SKETCH = 80                                       # 1.25 * d
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT5-regime-boundary.json")


def make_consumer(w, temp):
    def c(x):
        s = w @ np.asarray(x, float) / temp
        s = s - s.max()
        e = np.exp(s)
        return float(e[0] / e.sum())
    return c


def batch_consumer(w, temp, xs):
    s = xs @ w.T / temp
    s = s - s.max(axis=1, keepdims=True)
    e = np.exp(s)
    return e[:, 0] / e.sum(axis=1)


def main():
    rng = np.random.default_rng(SEED)
    w = rng.normal(size=(K, D))
    w /= np.linalg.norm(w, axis=1, keepdims=True)
    pts = rng.normal(size=(N_PTS, D))
    df_pts = rng.normal(size=(N_DF_PTS, D))
    sigmas = []
    for _ in range(N_PAIRS):
        pair = []
        for _ in range(2):
            g = rng.normal(size=(D, 4))
            m = g @ g.T
            pair.append(m * (TRACE / np.trace(m)))
        sigmas.append(pair)
    chols = [[np.linalg.cholesky(m + 1e-15 * np.eye(D)) for m in pair]
             for pair in sigmas]
    draws = rng.normal(size=(N_DRAWS, D))

    cells = []
    for temp in TEMPS:
        c = make_consumer(w, temp)
        ap = applicability(c, df_pts, eps=1e-3,
                           rng=np.random.default_rng(SEED))
        df = 1.0 - ap.evidence["zero_response_fraction"]
        res = blind_probe(c, pts, mode="lstsq", sketch_dim=SKETCH,
                          eps=1e-3, rng=np.random.default_rng(SEED),
                          check_regime=False)
        p_hat = res.S
        hits = 0
        for pair, chol in zip(sigmas, chols):
            pred = np.sign(np.trace(p_hat @ (pair[0] - pair[1])))
            dmg = []
            for cl in chol:
                deltas = draws @ cl.T
                d0 = batch_consumer(w, temp, pts)
                tot = 0.0
                for x0, v0 in zip(pts, d0):
                    vv = batch_consumer(w, temp, x0[None, :] + deltas)
                    tot += float(np.mean((vv - v0) ** 2))
                dmg.append(tot / N_PTS)
            meas = np.sign(dmg[0] - dmg[1])
            hits += int(pred == meas)
        acc = hits / N_PAIRS
        cells.append({"T": temp, "DF": round(df, 4),
                      "accuracy": round(acc, 4)})
        print(f"T={temp:>5}: DF={df:.3f}  accuracy={acc:.3f}")

    dfs = np.array([c["DF"] for c in cells])
    accs = np.array([c["accuracy"] for c in cells])
    manip = dfs.max() >= 0.9 and dfs.min() <= 0.3
    v1 = all(a >= 0.90 for d_, a in zip(dfs, accs) if d_ >= 0.9)
    v2 = accs[-1] <= 0.70
    rho = float(stats.spearmanr(accs, dfs).statistic)
    v3 = rho >= 0.80
    v4 = not any(d_ >= 0.8 and a <= 0.6 for d_, a in zip(dfs, accs))
    ok = manip and v1 and v2 and v3 and v4
    print(f"\nmanipulation check (DF spans): {'ok' if manip else 'VOID'}")
    print(f"V1 smooth-end acc>=0.90: {'PASS' if v1 else 'FAIL'}")
    print(f"V2 sharpest acc<=0.70: {accs[-1]:.3f} -> "
          f"{'PASS' if v2 else 'FAIL'}")
    print(f"V3 spearman(acc, DF)={rho:.3f} (>=0.80) -> "
          f"{'PASS' if v3 else 'FAIL'}")
    print(f"V4 no high-DF failure: {'PASS' if v4 else 'FAIL'}")
    json.dump({"claim": "OT-5", "seed": SEED, "cells": cells,
               "manipulation_ok": bool(manip), "V1": bool(v1),
               "V2": bool(v2), "V3": bool(v3), "spearman": rho,
               "V4": bool(v4),
               "verdict": "PASS" if ok else "FAIL"},
              open(OUT, "w"), indent=1)
    print(f"\nOT-5: {'PASS' if ok else 'FAIL'} -> "
          f"{os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
