"""OP3-B graded runner — the CORRECTED front-law bars per PREREG-OP3B.md,
after the 2026-08-19 seal FAILed on bar-calibration defects
(OP3-SEAL-NOTES.md). A new sealed act; edits nothing in the failed
op3_graded.py. Reuses op3_graded's measurement functions
(per_mode_cos2, population_operator) verbatim; only the BARS change.

Corrected bars (calibrated on the shakedown seeds {0,1,2} + the
derivation, NOT the failed disjoint seeds):

  B1' collapse exponent (primary): continuous best-fit p of the collapse
      cos^2 = s/(s+A), s = m*w^(p*i), lies in [3.5, 5.5] with RMS <= 0.20
      on each seed. (Derived p=4; shakedown 4.0-4.5, RMS 0.14-0.17.)
  B2' recovery matches the predicted level: the affine-operator overlap
      at m=1000 lies in [0.50, 0.70] on each seed -- incomplete AS the
      front law predicts, NOT >=0.9 (the failed bar contradicted the law;
      shakedown mean cos^2 0.57-0.61).
  B3' the front advances (weak): the recovered-mode count (cos^2>=0.5) at
      m=1000 exceeds that at m=4 by >=1 on the seed mean (the front moves
      with budget; per-seed noise allowed -- the count is non-monotonic).

Refuses to grade unless the appendix is SEALED, and enforces the
one-day cooling-off in code.

    .venv/Scripts/python crucible/op3b_check.py

Built 2026-08-19 (unsealed); grades only on/after the 2026-08-20 seal.
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
sys.path.insert(0, r"C:\source\readscope\calibration")
sys.path.insert(0, r"C:\source\readscope")
import op3_graded as g  # the measurement functions (unchanged sealed runner)

APPENDIX = os.path.join(HERE, "PREREG-OP3B.md")
OUT = os.path.join(HERE, "..", "results", "OP3B-graded.json")
FAMILY_CONSTRUCTED = date(2026, 8, 19)

GRADED_SEEDS = [20260901, 20260902, 20260903]   # fresh; disjoint from 0/1/2 and 08-19..21
W = g.op3.SPECTRUM_DECAY
P_GRID = np.arange(2.0, 6.01, 0.25)


def require_seal():
    t = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-OP3B.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: PREREG-OP3B.md seal carries no parseable date.")
    seal_date = date(int(m[1]), int(m[2]), int(m[3]))
    if (seal_date - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {seal_date} not >=1 day "
                 f"after family construction {FAMILY_CONSTRUCTED}.")
    return seal_date


def best_p_continuous(points):
    """Continuous best-fit collapse exponent and its RMS."""
    best = None
    for p in P_GRID:
        s = np.array([q["m"] * (W ** (p * q["i"])) for q in points])
        y = np.array([q["cos2"] for q in points])
        br = None
        for logA in np.linspace(-11, 8, 500):
            pred = s / (s + np.exp(logA))
            rms = float(np.sqrt(np.mean((pred - y) ** 2)))
            if br is None or rms < br:
                br = rms
        if best is None or br < best[1]:
            best = (float(p), br)
    return best


def main():
    seal_date = require_seal()
    print(f"OP3-B graded — sealed {seal_date}, seeds {GRADED_SEEDS}\n")
    per_seed, counts_min, counts_max = {}, [], []
    for seed in GRADED_SEEDS:
        points, cos2_by_m = [], {}
        read_big = None
        for m in g.M_GRID:
            c2, A_big = g.per_mode_cos2(seed, g.BASE_N * m)
            cos2_by_m[m] = c2
            for i, v in enumerate(c2):
                points.append({"i": i, "m": m, "cos2": v})
            if m == g.M_GRID[-1]:
                read_big = A_big
        bp, rms = best_p_continuous(points)
        _, topM = g.population_operator(seed)
        overlap = float(g.subspace_overlap(read_big, topM).overlap)
        cnt_min = sum(1 for v in cos2_by_m[g.M_GRID[0]] if v >= 0.5)
        cnt_max = sum(1 for v in cos2_by_m[g.M_GRID[-1]] if v >= 0.5)
        counts_min.append(cnt_min); counts_max.append(cnt_max)
        b1 = 3.5 <= bp <= 5.5 and rms <= 0.20
        b2 = 0.50 <= overlap <= 0.70
        per_seed[seed] = {"best_p": round(bp, 3), "rms": round(rms, 4),
                          "overlap": round(overlap, 4),
                          "count_min": cnt_min, "count_max": cnt_max,
                          "B1": bool(b1), "B2": bool(b2)}
        print(f"seed {seed}: best_p={bp:.2f} rms={rms:.3f} -> B1 "
              f"{'ok' if b1 else 'FAIL'};  overlap={overlap:.3f} -> B2 "
              f"{'ok' if b2 else 'FAIL'};  count {cnt_min}->{cnt_max}")

    B1 = all(per_seed[s]["B1"] for s in GRADED_SEEDS)
    B2 = all(per_seed[s]["B2"] for s in GRADED_SEEDS)
    B3 = (float(np.mean(counts_max)) - float(np.mean(counts_min))) >= 1.0
    verdict = "PASS" if (B1 and B2 and B3) else "FAIL"
    print(f"\nB1' collapse exponent in [3.5,5.5], RMS<=0.20: "
          f"{'PASS' if B1 else 'FAIL'}")
    print(f"B2' recovery in [0.50,0.70] (as predicted): "
          f"{'PASS' if B2 else 'FAIL'}")
    print(f"B3' front advances (mean count {np.mean(counts_min):.1f}->"
          f"{np.mean(counts_max):.1f}, >=+1): {'PASS' if B3 else 'FAIL'}")
    print(f"\nOP3-B corrected front law: {verdict}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"claim": "OP3B-frontlaw", "sealed": str(seal_date),
               "seeds": GRADED_SEEDS,
               "per_seed": {str(k): v for k, v in per_seed.items()},
               "mean_count_advance":
                   round(float(np.mean(counts_max) - np.mean(counts_min)), 3),
               "B1": B1, "B2": B2, "B3": B3, "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
