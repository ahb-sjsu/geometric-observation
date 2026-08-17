"""OT-16: the noisy cliff, graded per PREREG-OT16-APPENDIX.md on a
fresh seed. Arms imported unchanged from the family module.

    .venv/Scripts/python crucible/ot16_check.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fam_p3n_shakedown import (SPECTRA, X_GRID, cell_confined,  # noqa: E402
                               cell_full, cell_sideinfo, sin_theta)

SEED = 20260818
DIMS = [16, 32, 64]
K0S = [8, 16]
TRIALS = 20
BAND = [x for x in X_GRID if x <= 0.3]
OUT = os.path.join(HERE, "..", "results", "OT16-noisy-cliff.json")
APPENDIX = os.path.join(HERE, "PREREG-OT16-APPENDIX.md")

_ = sin_theta  # re-exported for auditability of the import surface


def require_seal():
    t = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: DRAFT-UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-OT16-APPENDIX.md is not SEALED.")


def main():
    require_seal()
    rng = np.random.default_rng(SEED)
    main_cells, n4_cells = [], []

    for d in DIMS:
        for name, lam in SPECTRA.items():
            gamma = lam[-1]
            for x in X_GRID:
                sigma = x * gamma / np.sqrt(d)
                full = [cell_full(rng, d, lam, sigma)
                        for _ in range(TRIALS)]
                conf = [cell_confined(rng, d, lam, sigma)
                        for _ in range(TRIALS)]
                main_cells.append({
                    "d": d, "spectrum": name, "x": x,
                    "full": round(float(np.median(full)), 4),
                    "full_iqr": round(float(np.subtract(
                        *np.percentile(full, [75, 25]))), 4),
                    "conf": round(float(np.median(conf)), 4),
                    "conf_iqr": round(float(np.subtract(
                        *np.percentile(conf, [75, 25]))), 4)})
    d = 32
    for k0 in K0S:
        for name, lam in SPECTRA.items():
            gamma = lam[-1]
            for x in X_GRID:
                sigma = x * gamma / np.sqrt(d - k0)
                full = [cell_sideinfo(rng, d, k0, lam, sigma, False)
                        for _ in range(TRIALS)]
                conf = [cell_sideinfo(rng, d, k0, lam, sigma, True)
                        for _ in range(TRIALS)]
                n4_cells.append({
                    "k0": k0, "spectrum": name, "x": x,
                    "full": round(float(np.median(full)), 4),
                    "conf": round(float(np.median(conf)), 4)})

    def cells_of(dd, name):
        return sorted((c for c in main_cells
                       if c["d"] == dd and c["spectrum"] == name),
                      key=lambda c: c["x"])

    mc1 = True
    b1 = b2 = b3 = True
    kill_conf = kill_lin = False
    slopes = []
    for dd in DIMS:
        for name in SPECTRA:
            cs = cells_of(dd, name)
            band = [c for c in cs if c["x"] in BAND]
            interior = sum(0.05 < c["full"] < 0.7 for c in cs)
            sep = min(c["conf"] - c["full"] for c in band)
            iqr_ok = all(max(c["full_iqr"], c["conf_iqr"]) <= sep / 3
                         for c in band)
            mc1 &= interior >= 2 and iqr_ok
            r1 = band[1]["full"] / max(band[0]["full"], 1e-9) / (0.1 / 0.03)
            r2 = band[2]["full"] / max(band[1]["full"], 1e-9) / (0.3 / 0.1)
            b1 &= 0.8 <= r1 <= 1.25 and 0.8 <= r2 <= 1.25
            kill_lin |= not (0.5 <= r1 <= 2 and 0.5 <= r2 <= 2)
            slopes.append(np.mean([c["full"] / c["x"] for c in band]))
            confs = [c["conf"] for c in band]
            b2 &= (all(0.65 <= v <= 0.78 for v in confs)
                   and (max(confs) - min(confs)) / max(confs) <= 0.10)
            kill_conf |= any(v < 0.5 for v in confs)
            b3 &= band[0]["conf"] / max(band[0]["full"], 1e-9) >= 10
            print(f"d={dd:>3} {name}: interior {interior}, ratios "
                  f"{r1:.2f}/{r2:.2f}, slope {slopes[-1]:.3f}, "
                  f"conf band {min(confs):.3f}-{max(confs):.3f}, "
                  f"step ratio {band[0]['conf'] / max(band[0]['full'], 1e-9):.0f}x")
    collapse = max(slopes) / min(slopes)
    b1 &= collapse <= 1.5
    print(f"slope collapse max/min: {collapse:.3f} (bar 1.5)")

    b4 = True
    for k0 in K0S:
        for name in SPECTRA:
            cs = sorted((c for c in n4_cells
                         if c["k0"] == k0 and c["spectrum"] == name),
                        key=lambda c: c["x"])
            band = [c for c in cs if c["x"] in BAND]
            x01 = next(c for c in cs if c["x"] == 0.1)
            ok = (0.05 <= x01["full"] <= 0.2
                  and all(0.65 <= c["conf"] <= 0.78 for c in band))
            b4 &= ok
            print(f"N4 k0={k0} {name}: W-full@0.1 {x01['full']:.3f}, "
                  f"W-minus-one band "
                  f"{min(c['conf'] for c in band):.3f}-"
                  f"{max(c['conf'] for c in band):.3f} "
                  f"{'ok' if ok else 'BAR FAIL'}")

    void = not mc1
    verdict = "VOID" if void else (
        "PASS" if (b1 and b2 and b3 and b4
                   and not kill_conf and not kill_lin) else "FAIL")
    print(f"\nMC1 interior/IQR on fresh seed: {'ok' if mc1 else 'VOID'}")
    print(f"B1 linearity + collapse: {'PASS' if b1 else 'FAIL'}")
    print(f"B2 confined face at 1/sqrt2: {'PASS' if b2 else 'FAIL'}")
    print(f"B3 step ratio >=10 at x=0.03: {'PASS' if b3 else 'FAIL'}")
    print(f"B4 N4 shift: {'PASS' if b4 else 'FAIL'}")
    if kill_conf:
        print("KILL: confinement leaked (in-band confined < 0.5)")
    if kill_lin:
        print("KILL: linear-floor model refuted (ratio outside [0.5,2])")
    json.dump({"claim": "OT-16", "seed": SEED,
               "main_cells": main_cells, "n4_cells": n4_cells,
               "slope_collapse": round(float(collapse), 4),
               "MC1": bool(mc1), "B1": bool(b1), "B2": bool(b2),
               "B3": bool(b3), "B4": bool(b4),
               "kill_confinement": bool(kill_conf),
               "kill_linearity": bool(kill_lin),
               "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"\nOT-16: {verdict} -> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
