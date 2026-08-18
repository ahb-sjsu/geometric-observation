"""SC-2 graded runner — the transport bars B1/B2/B3 per PREREG-SC2.md.
Reuses fam_sc2_shakedown; runs on seeds DISJOINT from the shakedown's
{0,1,2}. Refuses to grade unless the appendix is SEALED, and enforces
the one-day cooling-off in code.

    .venv/Scripts/python crucible/sc2_check.py

Built 2026-08-18 (unsealed); grades only on/after the 2026-08-19 seal.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fam_sc2_shakedown as fam  # noqa: E402

APPENDIX = os.path.join(HERE, "PREREG-SC2.md")
OUT = os.path.join(HERE, "..", "results", "SC2-graded.json")
FAMILY_CONSTRUCTED = date(2026, 8, 18)

GRADED_SEEDS = [20260819, 20260820, 20260821]     # disjoint from {0,1,2}
RHO_GRID = [0.05, 0.10, 0.20, 0.30]
D_GRID = [2, 20, 100, 500, 2000]
c = fam.C_RATE
lam = fam.C_AUTOCORR
FLOOR = 2 * c * (1 - c)
KAPPA = 1 - 2 * c                                  # SpaceComms.lean


def require_seal():
    t = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-SC2.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: PREREG-SC2.md seal carries no parseable date.")
    seal_date = date(int(m[1]), int(m[2]), int(m[3]))
    if (seal_date - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {seal_date} not >=1 day "
                 f"after family construction {FAMILY_CONSTRUCTED}.")
    return seal_date


def r2(y, pred):
    y = np.asarray(y, float)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0


def main():
    seal_date = require_seal()
    print(f"SC-2 graded — sealed {seal_date}, seeds {GRADED_SEEDS} "
          f"(disjoint from {{0,1,2}})")
    print(f"derived: floor 2c(1-c)={FLOOR:.3f}, kappa=1-2c={KAPPA:.3f}\n")

    per_seed = {}
    for seed in GRADED_SEEDS:
        # Arm B: aware_err(D) and excess(D) at rho=0.15
        h = fam.handover_series(0.15)
        cser = fam.congestion_series(np.random.default_rng(seed * 2711 + 7))
        aware, excess = [], []
        for D in D_GRID:
            ne, ae = fam.errors(cser, h, D)
            aware.append(ae)
            excess.append(ne - ae)
        pred_aware = [FLOOR * (1 - lam ** D) for D in D_GRID]
        b1_r2 = r2(aware, np.array(pred_aware))
        b1_floor = aware[-1] >= 0.9 * FLOOR
        b1 = b1_r2 >= 0.95 and b1_floor
        b2 = (max(excess) - min(excess)) <= 0.01

        # Arm B3: excess = kappa*rho, at small D
        cserA = fam.congestion_series(np.random.default_rng(seed * 2711 + 1))
        exc_rho = []
        for rho in RHO_GRID:
            ne, ae = fam.errors(cserA, fam.handover_series(rho), 2)
            exc_rho.append(ne - ae)
        slope = float(np.polyfit(RHO_GRID, exc_rho, 1)[0])
        b3_r2 = r2(exc_rho, slope * np.array(RHO_GRID)
                   + np.polyfit(RHO_GRID, exc_rho, 1)[1])
        b3 = b3_r2 >= 0.98 and abs(slope - KAPPA) <= 0.05

        per_seed[seed] = {
            "aware_err": [round(a, 4) for a in aware],
            "excess_D": [round(e, 4) for e in excess],
            "b1_r2": round(b1_r2, 4), "b1_floor": bool(b1_floor),
            "b2_spread": round(max(excess) - min(excess), 4),
            "b3_slope": round(slope, 4), "b3_r2": round(b3_r2, 4),
            "B1": bool(b1), "B2": bool(b2), "B3": bool(b3)}
        print(f"seed {seed}: B1(delay law) r2={b1_r2:.3f} floor={b1_floor} "
              f"-> {'ok' if b1 else 'FAIL'}")
        print(f"           B2(D-invariance) spread={max(excess)-min(excess):.4f} "
              f"-> {'ok' if b2 else 'FAIL'}")
        print(f"           B3(kappa) slope={slope:.3f} r2={b3_r2:.3f} "
              f"-> {'ok' if b3 else 'FAIL'}")

    B1 = all(per_seed[s]["B1"] for s in GRADED_SEEDS)
    B2 = all(per_seed[s]["B2"] for s in GRADED_SEEDS)
    B3 = all(per_seed[s]["B3"] for s in GRADED_SEEDS)
    verdict = "PASS" if (B1 and B2 and B3) else "FAIL"
    print(f"\nB1 delay-decorrelation law: {'PASS' if B1 else 'FAIL'}")
    print(f"B2 schedule D-invariance:   {'PASS' if B2 else 'FAIL'}")
    print(f"B3 duty floor kappa=1-2c:   {'PASS' if B3 else 'FAIL'}")
    print(f"\nSC-2: {verdict}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"campaign": "SC-2", "sealed": str(seal_date),
               "seeds": GRADED_SEEDS, "floor": round(FLOOR, 4),
               "kappa": round(KAPPA, 4),
               "per_seed": {str(k): v for k, v in per_seed.items()},
               "B1": B1, "B2": B2, "B3": B3, "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
