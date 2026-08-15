"""OT-3 numerical half: the side-information cliff, constants per
PREREG-OT3-APPENDIX-V2.md (theorem-faithful bars: no *hidden* recovery;
chance-alignment rate promoted to a prediction). The theorem is OT3-THEOREM.md; this checks that
the instrument's confined-transcript estimator behaves exactly as T2
prices it: cliff at k = d - k0, never earlier, ramp bounded by
confinement mass.

    .venv/Scripts/python crucible/ot3_check_v2.py
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
OUT = os.path.join(HERE, "..", "results", "OT3-cliff-v2.json")


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
    hidden = 1.0 - float(np.linalg.norm(v.T @ u) ** 2) / r
    return affinity(u, u_hat), hidden


def main():
    rng = np.random.default_rng(SEED)
    cells = {}
    ok = True
    for r in RANKS:
        for k0 in K0S:
            m = D - k0
            for k in range(m - 6, m + 1):
                res = [trial(rng, r, k0, k) for _ in range(TRIALS)]
                a = np.array([x[0] for x in res])
                hid = np.array([x[1] for x in res])
                exact = a >= EXACT
                cells[f"r{r}_k0{k0}_k{k}"] = {
                    "m": m, "r": r, "exact_share": float(exact.mean()),
                    "hidden_exact_share":
                        float((exact & (hid >= 1e-3)).mean()),
                    "median_affinity": float(np.median(a)),
                    "mass_bound": k / m + 0.10}
    # bars per appendix v2
    import math
    def p_chance(m):
        return (2 * math.sqrt(1e-3) * math.gamma(m / 2)
                / (math.sqrt(math.pi) * math.gamma((m - 1) / 2)))
    bars = {"cliff_top": True, "no_hidden_recovery": True,
            "chance_rate": True, "ramp": True}
    for key, c in cells.items():
        k = int(key.split("_k")[-1])
        m, r = c["m"], c["r"]
        if k == m and c["exact_share"] != 1.0:
            bars["cliff_top"] = False
        if k < m and c["hidden_exact_share"] != 0.0:
            bars["no_hidden_recovery"] = False
        if k == m - 1 and r == 1:
            p = p_chance(m)
            tol = 3 * math.sqrt(p * (1 - p) / TRIALS)
            if abs(c["exact_share"] - p) > tol:
                bars["chance_rate"] = False
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
    json.dump({"claim": "OT-3-numerics-v2", "seed": SEED, "cells": cells,
               "bars": bars, "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-3 numerics: {verdict}  -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
