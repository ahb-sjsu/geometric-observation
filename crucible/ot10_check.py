"""OT-10: the noisy cliff, per OT10-THEOREM.md and
PREREG-OT10-APPENDIX.md.

    .venv/Scripts/python crucible/ot10_check.py
"""

from __future__ import annotations

import json
import os

import numpy as np

SEED = 20260815
D = 32
LAM = 1.0
SIGMAS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
KS = [D - 2, D - 1, D]
TRIALS = 50
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "OT10-noisy-cliff.json")


def sym_noise(rng, k, sigma):
    e = rng.normal(scale=sigma, size=(k, k))
    return (e + e.T) / np.sqrt(2)


def trial(rng, k, sigma):
    u = rng.normal(size=D)
    u /= np.linalg.norm(u)
    p = LAM * np.outer(u, u)
    v = np.linalg.qr(rng.normal(size=(D, D)))[0][:, :k]
    b = v.T @ p @ v + sym_noise(rng, k, sigma)
    emb = v @ b @ v.T
    u_hat = np.linalg.eigh(emb)[1][:, -1]
    aff = float((u @ u_hat) ** 2)
    hidden = 1.0 - float(np.linalg.norm(v.T @ u) ** 2)
    return aff, hidden


def main():
    rng = np.random.default_rng(SEED)
    cells = {}
    for sigma in SIGMAS:
        for k in KS:
            res = [trial(rng, k, sigma) for _ in range(TRIALS)]
            aff = np.array([r[0] for r in res])
            hid = np.array([r[1] for r in res])
            cells[f"s{sigma}_k{k}"] = {
                "sigma": sigma, "k": k,
                "median_affinity": float(np.median(aff)),
                "median_err": float(np.median(1 - aff)),
                "hidden_exact": int(((aff >= 0.999)
                                     & (hid >= 1e-3)).sum())}
    pred = {s: s * s * (D - 1) / LAM ** 2 for s in SIGMAS}
    n1 = all(0.5 * pred[s] <= cells[f"s{s}_k{D}"]["median_err"]
             <= 2.0 * pred[s] for s in SIGMAS)
    errs = np.log([cells[f"s{s}_k{D}"]["median_err"] for s in SIGMAS])
    slope = float(np.polyfit(np.log(SIGMAS), errs, 1)[0])
    n2 = 1.8 <= slope <= 2.2
    n3 = all(cells[f"s{s}_k{k}"]["hidden_exact"] == 0
             for s in SIGMAS for k in (D - 2, D - 1)) and \
        all(cells[f"s{s}_k{D}"]["median_affinity"]
            - cells[f"s{s}_k{D - 1}"]["median_affinity"] >= 0.5
            for s in SIGMAS)
    for s in SIGMAS:
        c = cells[f"s{s}_k{D}"]
        print(f"sigma={s:g}: err@k=d {c['median_err']:.3e} "
              f"(pred {pred[s]:.3e})  aff@d-1 "
              f"{cells[f's{s}_k{D - 1}']['median_affinity']:.3f}")
    print(f"\nN1 floor within 2x: {'PASS' if n1 else 'FAIL'}")
    print(f"N2 slope {slope:.2f} in [1.8,2.2]: {'PASS' if n2 else 'FAIL'}")
    print(f"N3 location fixed: {'PASS' if n3 else 'FAIL'}")
    ok = n1 and n2 and n3
    json.dump({"claim": "OT-10", "seed": SEED, "cells": cells,
               "pred_floor": {str(k): v for k, v in pred.items()},
               "slope": slope, "N1": bool(n1), "N2": bool(n2),
               "N3": bool(n3), "verdict": "PASS" if ok else "FAIL"},
              open(OUT, "w"), indent=1)
    print(f"\nOT-10: {'PASS' if ok else 'FAIL'} -> "
          f"{os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
