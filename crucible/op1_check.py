"""OP1 graded runner — the cross-consumer transfer bars B1/B2/B3 per
PREREG-OP1.md. Reuses fam_op1_shakedown; runs on seeds DISJOINT from the
shakedown's {0,1,2}. Refuses to grade unless the appendix is SEALED, and
enforces the one-day cooling-off in code.

    .venv/Scripts/python crucible/op1_check.py

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
import fam_op1_shakedown as fam  # noqa: E402
from readscope import water_fill  # noqa: E402

APPENDIX = os.path.join(HERE, "PREREG-OP1.md")
OUT = os.path.join(HERE, "..", "results", "OP1-graded.json")
FAMILY_CONSTRUCTED = date(2026, 8, 18)

GRADED_SEEDS = [20260819, 20260820, 20260821]     # disjoint from {0,1,2}


def require_seal():
    t = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-OP1.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: PREREG-OP1.md seal carries no parseable date.")
    seal_date = date(int(m[1]), int(m[2]), int(m[3]))
    if (seal_date - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {seal_date} not >=1 day "
                 f"after family construction {FAMILY_CONSTRUCTED}.")
    return seal_date


def pairs(seed):
    """Overlaps tr(P_A P_B) and B-damage tr(P_B Σ_δ^A). The A-optimal codec
    (Σ_δ^A) is built from A alone; B's damage is used ONLY to grade — never
    fed into the prediction (the no-probe-of-B guarantee, B3)."""
    rng = np.random.default_rng(seed * 5237 + 11)
    overlaps, damages = [], []
    for _ in range(fam.N_PAIRS):
        V_A, s_A = fam.soft_operator(rng)
        mix = rng.uniform(0.0, 1.0)
        V_B, s_B = fam.soft_operator(rng, mix=mix, V_ref=V_A)
        P_A = fam.op_from(V_A, s_A)
        P_B = fam.op_from(V_B, s_B)
        overlap = float(np.trace(P_A @ P_B))
        alloc = water_fill(sensitivity=s_A, variance=np.ones(fam.D),
                           budget=fam.BUDGET)         # A-optimal codec, A only
        var = np.power(2.0, -2.0 * alloc.bits)
        Sigma_A = (V_A * var) @ V_A.T
        damage = float(np.trace(P_B @ Sigma_A))
        overlaps.append(overlap)
        damages.append(damage)
    return np.array(overlaps), np.array(damages)


def r2_of(y, pred):
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0


def main():
    seal_date = require_seal()
    print(f"OP1 graded — sealed {seal_date}, seeds {GRADED_SEEDS} "
          f"(disjoint from {{0,1,2}})")
    print("prediction: damage from tr(P_A P_B) alone; no probe of B\n")

    per_seed = {}
    for seed in GRADED_SEEDS:
        ov, dm = pairs(seed)
        rho = float(stats.spearmanr(ov, dm).statistic)                 # B1
        b, a = np.polyfit(ov, dm, 1)
        r2 = r2_of(dm, a + b * ov)                                     # B2
        # B3: fit the affine law on half, predict the HELD-OUT half's damage
        # from overlap ALONE (never from B's response), grade the prediction.
        n = len(ov); h = n // 2
        idx = np.argsort(ov)                      # split across the range
        tr, te = idx[0::2], idx[1::2]
        bb, aa = np.polyfit(ov[tr], dm[tr], 1)
        pred = aa + bb * ov[te]
        oos_rho = float(stats.spearmanr(pred, dm[te]).statistic)
        oos_r2 = r2_of(dm[te], pred)                                   # B3
        b1 = rho <= -0.6
        b2 = r2 >= 0.9 and b < 0
        b3 = oos_rho >= 0.6 and oos_r2 >= 0.8
        per_seed[seed] = {"spearman": round(rho, 4), "slope": round(float(b), 5),
                          "r2": round(r2, 4), "oos_rho": round(oos_rho, 4),
                          "oos_r2": round(oos_r2, 4),
                          "overlap_range": [round(float(ov.min()), 3),
                                            round(float(ov.max()), 3)],
                          "B1": bool(b1), "B2": bool(b2), "B3": bool(b3)}
        print(f"seed {seed}: B1 Spearman={rho:+.3f} -> {'ok' if b1 else 'FAIL'}")
        print(f"           B2 R²={r2:.3f} slope={b:+.4f} -> {'ok' if b2 else 'FAIL'}")
        print(f"           B3 held-out ρ={oos_rho:+.3f} R²={oos_r2:.3f} "
              f"-> {'ok' if b3 else 'FAIL'}")

    B1 = all(per_seed[s]["B1"] for s in GRADED_SEEDS)
    B2 = all(per_seed[s]["B2"] for s in GRADED_SEEDS)
    B3 = all(per_seed[s]["B3"] for s in GRADED_SEEDS)
    verdict = "PASS" if (B1 and B2 and B3) else "FAIL"
    print(f"\nB1 transfer correlation (≤ −0.6):  {'PASS' if B1 else 'FAIL'}")
    print(f"B2 overlap a sufficient predictor: {'PASS' if B2 else 'FAIL'}")
    print(f"B3 blind held-out prediction:      {'PASS' if B3 else 'FAIL'}")
    print(f"\nOP1: {verdict}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"campaign": "OP1", "sealed": str(seal_date),
               "seeds": GRADED_SEEDS,
               "per_seed": {str(k): v for k, v in per_seed.items()},
               "B1": B1, "B2": B2, "B3": B3, "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
