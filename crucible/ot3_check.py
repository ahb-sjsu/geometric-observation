"""OT-3 numerical half: the side-information cliff, constants per
PREREG-OT3-APPENDIX.md. The theorem is OT3-THEOREM.md; this checks that
the instrument's confined-transcript estimator behaves exactly as T2
prices it: cliff at k = d - k0, never earlier, ramp bounded by
confinement mass.

    .venv/Scripts/python crucible/ot3_check.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEED = 20260815
D = 32
RANKS = (1, 4)
K0S = (0, 8, 16)
TRIALS = 50
EXACT = 0.999
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT3-cliff.json")


def affinity(u_true, u_hat):
    return float(np.linalg.norm(u_true.T @ u_hat) ** 2 / u_true.shape[1])


def trial(rng, r, k0, k):
    m = D - k0
    basis = np.linalg.qr(rng.normal(size=(D, D)))[0]
    w = basis[:, :m]                       # promise subspace
    frame = np.linalg.qr(rng.normal(size=(m, m)))[0]
    u_w = frame[:, :r]                     # operator frame inside W
    lam = np.sort(10 ** rng.uniform(-1, 0, r))[::-1]
    u = w @ u_w
    p = u @ np.diag(lam) @ u.T
    v = w @ np.linalg.qr(rng.normal(size=(m, m)))[0][:, :k]
    block = v.T @ p @ v
    emb = v @ block @ v.T
    vals, vecs = np.linalg.eigh(emb)
    u_hat = vecs[:, -r:]
    return affinity(u, u_hat)


def main():
    rng = np.random.default_rng(SEED)
    cells = {}
    ok = True
    for r in RANKS:
        for k0 in K0S:
            m = D - k0
            for k in range(m - 6, m + 1):
                a = np.array([trial(rng, r, k0, k) for _ in range(TRIALS)])
                cells[f"r{r}_k0{k0}_k{k}"] = {
                    "m": m, "exact_share": float((a >= EXACT).mean()),
                    "median_affinity": float(np.median(a)),
                    "mass_bound": k / m + 0.10}
    # bars
    bars = {"cliff_top": True, "cliff_bottom": True,
            "no_smoothing": True, "ramp": True}
    for key, c in cells.items():
        k = int(key.split("_k")[-1])
        m = c["m"]
        if k == m and c["exact_share"] != 1.0:
            bars["cliff_top"] = False
        if k == m - 1 and c["exact_share"] != 0.0:
            bars["cliff_bottom"] = False
        if k in (m - 1, m - 3) and c["exact_share"] != 0.0:
            bars["no_smoothing"] = False
        if k <= m - 1 and c["median_affinity"] > c["mass_bound"]:
            bars["ramp"] = False
    ok = all(bars.values())

    for r in RANKS:
        for k0 in K0S:
            m = D - k0
            row = [f"k={k}:{cells[f'r{r}_k0{k0}_k{k}']['exact_share']:.2f}"
                   f"/{cells[f'r{r}_k0{k0}_k{k}']['median_affinity']:.3f}"
                   for k in range(m - 3, m + 1)]
            print(f"r={r} k0={k0:>2} (cliff at {m}):  " + "  ".join(row))
    print("bars:", bars)
    verdict = "PASS" if ok else "FAIL"
    json.dump({"claim": "OT-3-numerics", "seed": SEED, "cells": cells,
               "bars": bars, "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-3 numerics: {verdict}  -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
