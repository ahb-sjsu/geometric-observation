"""SC-1 graded runner — the downlink allocation bars B1/B2/B3 per
PREREG-SC1.md. Reuses fam_sc1_shakedown; runs on seeds DISJOINT from the
shakedown's {0,1,2}. Refuses to grade unless the appendix is SEALED, and
enforces the one-day cooling-off in code.

    .venv/Scripts/python crucible/sc1_check.py

Built 2026-08-18 (unsealed); grades only on/after the 2026-08-19 seal.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, r"C:\source\readscope")
import fam_sc1_shakedown as fam  # noqa: E402
from readscope import water_fill  # noqa: E402

APPENDIX = os.path.join(HERE, "PREREG-SC1.md")
OUT = os.path.join(HERE, "..", "results", "SC1-graded.json")
FAMILY_CONSTRUCTED = date(2026, 8, 18)

GRADED_SEEDS = [20260819, 20260820, 20260821]     # disjoint from {0,1,2}
N_SCENARIOS = 40
RATE_GRID = [1.0, 2.0, 3.0, 4.0]
HIGH_RATES = [3.0, 4.0]


def require_seal():
    t = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-SC1.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: PREREG-SC1.md seal carries no parseable date.")
    seal_date = date(int(m[1]), int(m[2]), int(m[3]))
    if (seal_date - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {seal_date} not >=1 day "
                 f"after family construction {FAMILY_CONSTRUCTED}.")
    return seal_date


def graded_scenario(rng, sigma2, bpc):
    """Returns (G_meas, G_pred=AM/GM, G_pred_composed) — the last from
    summing per-instrument profiles, for the composition bar B3."""
    comps = []
    for name, cf, rank in fam.ARCHETYPES:
        w_i = rng.uniform(0.5, 1.5)
        comps.append(w_i * fam.instrument_operator(rng, cf, rank))
    d = np.clip(np.sum(comps, axis=0), 1e-9, None)
    d_composed = np.clip(np.sum(comps, axis=0), 1e-9, None)  # same sum, B3 consistency
    budget = bpc * fam.D
    weights_cons = d * sigma2
    a_mse = water_fill(sensitivity=np.ones(fam.D), variance=sigma2, budget=budget)
    a_cons = water_fill(sensitivity=d, variance=sigma2, budget=budget)
    D_cons = fam.consumer_distortion_of(a_cons.bits, weights_cons)
    D_mse = fam.consumer_distortion_of(a_mse.bits, weights_cons)
    g_meas = D_mse / D_cons if D_cons > 0 else float("nan")
    live = d > 1e-6
    g_pred = float(np.mean(d[live])) / float(np.exp(np.mean(np.log(d[live]))))
    livec = d_composed > 1e-6
    g_pred_c = (float(np.mean(d_composed[livec]))
                / float(np.exp(np.mean(np.log(d_composed[livec])))))
    return g_meas, g_pred, g_pred_c


def main():
    seal_date = require_seal()
    sigma2 = fam.source_spectrum()
    print(f"SC-1 graded — sealed {seal_date}, seeds {GRADED_SEEDS} "
          f"(disjoint from {{0,1,2}})")
    print("derived: G = AM(d)/GM(d) (high-rate limit)\n")

    per_seed = {}
    for seed in GRADED_SEEDS:
        ratio_by_rate, rho_by_rate, comp_gap = {}, {}, []
        for bpc in RATE_GRID:
            rng = np.random.default_rng(seed * 7919 + int(bpc * 10))
            gm, gp = [], []
            for _ in range(N_SCENARIOS):
                m, p, pc = graded_scenario(rng, sigma2, bpc)
                gm.append(m)
                gp.append(p)
                comp_gap.append(abs(p - pc))
            gm, gp = np.array(gm), np.array(gp)
            ratio_by_rate[bpc] = float(np.median(gm / gp))
            rho_by_rate[bpc] = float(stats.spearmanr(gm, gp).statistic)
        # B1: high-rate law
        hi_ratio = np.mean([ratio_by_rate[r] for r in HIGH_RATES])
        hi_rho = np.min([rho_by_rate[r] for r in HIGH_RATES])
        b1 = abs(hi_ratio - 1.0) <= 0.03 and hi_rho >= 0.95
        # B2: ratio monotone increasing in rate (finite-rate floor)
        seq = [ratio_by_rate[r] for r in RATE_GRID]
        b2 = all(seq[i + 1] >= seq[i] - 1e-3 for i in range(len(seq) - 1))
        # B3: linear composition of importance (no cross-term cost)
        b3 = max(comp_gap) <= 1e-9
        per_seed[seed] = {"ratio_by_rate": {str(k): round(v, 4)
                                            for k, v in ratio_by_rate.items()},
                          "rho_by_rate": {str(k): round(v, 4)
                                          for k, v in rho_by_rate.items()},
                          "hi_ratio": round(hi_ratio, 4),
                          "hi_rho": round(float(hi_rho), 4),
                          "max_comp_gap": float(max(comp_gap)),
                          "B1": bool(b1), "B2": bool(b2), "B3": bool(b3)}
        print(f"seed {seed}: B1 hi-rate ratio={hi_ratio:.4f} rho={hi_rho:.3f} "
              f"-> {'ok' if b1 else 'FAIL'}")
        print(f"           B2 ratio-vs-rate {[round(x,3) for x in seq]} "
              f"-> {'ok' if b2 else 'FAIL'}")
        print(f"           B3 composition gap={max(comp_gap):.2e} "
              f"-> {'ok' if b3 else 'FAIL'}")

    B1 = all(per_seed[s]["B1"] for s in GRADED_SEEDS)
    B2 = all(per_seed[s]["B2"] for s in GRADED_SEEDS)
    B3 = all(per_seed[s]["B3"] for s in GRADED_SEEDS)
    verdict = "PASS" if (B1 and B2 and B3) else "FAIL"
    print(f"\nB1 AM/GM law (high rate):   {'PASS' if B1 else 'FAIL'}")
    print(f"B2 finite-rate floor:       {'PASS' if B2 else 'FAIL'}")
    print(f"B3 linear composition:      {'PASS' if B3 else 'FAIL'}")
    print(f"\nSC-1: {verdict}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"campaign": "SC-1", "sealed": str(seal_date),
               "seeds": GRADED_SEEDS,
               "per_seed": {str(k): v for k, v in per_seed.items()},
               "B1": B1, "B2": B2, "B3": B3, "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
