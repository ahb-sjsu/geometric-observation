"""OT-12: the two floor curves, constants per PREREG-OT12-APPENDIX-V2.md:
grid derived from the measured rms output change; interior-coverage
manipulation check added (a curve claim needs a curve).

    .venv/Scripts/python crucible/ot12_check_v2.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, r"C:\source\readscope")
from readscope.probe import blind_probe          # noqa: E402
from readscope.regimes import applicability      # noqa: E402

SEED = 20260815
D = 64
K = 16
TEMP = 1.0
N_PTS = 24
N_DF_PTS = 200
N_PAIRS = 30
N_DRAWS = 2000
TRACE = 0.01
SKETCH = 80
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT12-floor-curves-v2.json")
M_GRID = [30, 10, 3, 1, 0.3, 0.1, 0.03]


def make_consumer(w, g):
    def c(x):
        s = w @ np.asarray(x, float) / TEMP
        s = s - s.max()
        e = np.exp(s)
        v = float(e[0] / e.sum())
        return v if g is None else round(v * g) / g
    return c


def batch_consumer(w, g, xs):
    s = xs @ w.T / TEMP
    s = s - s.max(axis=1, keepdims=True)
    e = np.exp(s)
    v = e[:, 0] / e.sum(axis=1)
    return v if g is None else np.round(v * g) / g


def main():
    rng = np.random.default_rng(SEED)
    w = rng.normal(size=(K, D))
    w /= np.linalg.norm(w, axis=1, keepdims=True)
    pts = rng.normal(size=(N_PTS, D))
    df_pts = rng.normal(size=(N_DF_PTS, D))
    sigmas, chols = [], []
    for _ in range(N_PAIRS):
        pair = []
        for _ in range(2):
            gm = rng.normal(size=(D, 4))
            m = gm @ gm.T
            pair.append(m * (TRACE / np.trace(m)))
        sigmas.append(pair)
        chols.append([np.linalg.cholesky(m + 1e-15 * np.eye(D))
                      for m in pair])
    draws = rng.normal(size=(N_DRAWS, D))

    # calibration: median RMS output change of the unquantized consumer
    rms_all = []
    for pair, chol in zip(sigmas, chols):
        for cl in chol:
            deltas = draws[:200] @ cl.T
            d0 = batch_consumer(w, None, pts)
            for x0, v0 in zip(pts[:8], d0[:8]):
                vv = batch_consumer(w, None, x0[None, :] + deltas)
                rms_all.append(float(np.sqrt(np.mean((vv - v0) ** 2))))
    rms = float(np.median(rms_all))
    grid = [None] + [max(2, int(round(1.0 / (m * rms)))) for m in M_GRID]
    print(f"calibrated rms={rms:.3e}; derived g grid: {grid}")

    cells = []
    for g in grid:
        c = make_consumer(w, g)
        ap = applicability(c, df_pts, eps=1e-3,
                           rng=np.random.default_rng(SEED))
        df = 1.0 - ap.evidence["zero_response_fraction"]
        res = blind_probe(c, pts, mode="lstsq", sketch_dim=SKETCH,
                          eps=1e-3, rng=np.random.default_rng(SEED),
                          check_regime=False)
        p_hat = res.S
        hits = informative = 0
        for pair, chol in zip(sigmas, chols):
            pred = np.sign(np.trace(p_hat @ (pair[0] - pair[1])))
            dmg = []
            for cl in chol:
                deltas = draws @ cl.T
                d0 = batch_consumer(w, g, pts)
                tot = 0.0
                for x0, v0 in zip(pts, d0):
                    vv = batch_consumer(w, g, x0[None, :] + deltas)
                    tot += float(np.mean((vv - v0) ** 2))
                dmg.append(tot / N_PTS)
            meas = np.sign(dmg[0] - dmg[1])
            if pred != 0 and meas != 0:
                informative += 1
                hits += int(pred == meas)
        acc = hits / informative if informative else float("nan")
        cells.append({"g": "inf" if g is None else g,
                      "DF": round(df, 4),
                      "informative_frac": round(informative / N_PAIRS, 4),
                      "informative": informative,
                      "accuracy": None if not informative
                      else round(acc, 4)})
        print(f"g={'inf' if g is None else g:>4}: DF={df:.3f}  "
              f"informative={informative}/30  "
              f"acc={'--' if not informative else f'{acc:.3f}'}")

    fr = [c["informative_frac"] for c in cells]
    interior = sum(0.10 < f < 0.90 for f in fr)
    window = fr[0] >= 0.9 and fr[-1] <= 0.5 and interior >= 3
    f1 = all(fr[i + 1] <= fr[i] + 0.05 for i in range(len(fr) - 1))
    graded = [c for c in cells if c["informative"] >= 10]
    f2 = all(c["accuracy"] >= 0.85 for c in graded)
    f3 = not any(c["accuracy"] <= 0.60 for c in graded)
    ok = window and f1 and f2 and f3
    verdict = "VOID" if not window else ("PASS" if ok else "FAIL")
    print(f"\nwindow: {'ok' if window else 'VOID'}")
    print(f"F1 fraction non-increasing (tol 0.05/step): "
          f"{'PASS' if f1 else 'FAIL'}")
    print(f"F2 ceiling >=0.85 on {len(graded)} graded cells: "
          f"{'PASS' if f2 else 'FAIL'}")
    print(f"F3 no informative-and-wrong cell: {'PASS' if f3 else 'FAIL'}")
    json.dump({"claim": "OT-12-v2", "seed": SEED, "rms": rms,
               "cells": cells,
               "window": bool(window), "F1": bool(f1), "F2": bool(f2),
               "F3": bool(f3), "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-12: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
