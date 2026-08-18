"""OP3 graded runner — the corrected front-law bars B1'/B2'/B3' per
PREREG-OP3.md. Reuses C-15's planted family (via op3_exponent); runs on
seeds DISJOINT from the shakedown's {0,1,2}. Refuses to grade unless the
appendix is SEALED, and enforces the one-day cooling-off in code.

    .venv/Scripts/python crucible/op3_graded.py

Built 2026-08-18 (unsealed); grades only on/after the 2026-08-19 seal.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date

import numpy as np

sys.path.insert(0, r"C:\source\readscope")
sys.path.insert(0, r"C:\source\readscope\calibration")
from readscope import blind_probe, subspace_overlap  # noqa: E402
import op3_exponent as op3  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
APPENDIX = os.path.join(HERE, "PREREG-OP3.md")
OUT = os.path.join(HERE, "..", "results", "OP3-frontlaw-graded.json")

# Cooling-off is a code guard, not a recollection: the barred quantity's
# interior (op3_frontlaw) was committed 2026-08-18, so a compliant seal
# is dated strictly later.
FAMILY_CONSTRUCTED = date(2026, 8, 18)

# Disjoint from the shakedown seeds {0,1,2}; date-stamped for the run day.
GRADED_SEEDS = [20260819, 20260820, 20260821]
W = op3.SPECTRUM_DECAY          # 0.75
K = op3.K                       # 8
RANK = op3.RANK                 # 16
DIM = op3.DIM                   # 32
BASE_N = op3.BASE_N             # 384
M_GRID = [4, 16, 64, 256, 1000]
P_CANDIDATES = [2.0, 3.0, 4.0, 5.0, 6.0]
DERIVED_P = 4
DERIVED_RATE = 1.0 / np.log(W ** (-4))   # 0.869
RATE_TOL = 0.10
N_POP = 200_000                 # population-operator Monte Carlo size


def require_seal():
    t = open(APPENDIX, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-OP3.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: PREREG-OP3.md seal carries no parseable date.")
    seal_date = date(int(m[1]), int(m[2]), int(m[3]))
    if (seal_date - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {seal_date} is not >=1 day "
                 f"after family construction {FAMILY_CONSTRUCTED}.")
    return seal_date


def population_operator(seed):
    """S = E[g g^T] for the analytic gradient of the planted consumer,
    then the affine target M = (1+1/k) S + tr(S)/k I. Eigenvectors of M
    are the estimator's population target (the mechanism B3' checks)."""
    basis, weights, _ = op3.setup(RANK, seed, 1)
    rng = np.random.default_rng(seed * 101 + 7)
    x = rng.standard_normal((N_POP, DIM)) * op3.INPUT_SCALE
    u = x @ basis                      # (N, RANK)
    jac = (weights * (1.0 - np.tanh(u) ** 2))    # dC/du per mode
    g = jac @ basis.T                  # (N, DIM) gradients
    S = (g.T @ g) / N_POP
    M = (1.0 + 1.0 / K) * S + (np.trace(S) / K) * np.eye(DIM)
    evals, evecs = np.linalg.eigh(M)
    topM = evecs[:, ::-1][:, :RANK]    # top-16 eigenspace of M
    return basis, topM


def per_mode_cos2(seed, n):
    basis, weights, pts = op3.setup(RANK, seed, n)
    cons = op3.scalar_consumer(basis, weights)
    res = blind_probe(cons, pts, mode="lstsq", sketch_dim=K, eps=1e-3,
                      rng=np.random.default_rng(seed * 31 + K),
                      check_regime=False)
    A = np.linalg.qr(res.read_subspace(RANK))[0]
    B = np.linalg.qr(basis[:, :RANK])[0]
    cc = np.linalg.svd(B.T @ A, compute_uv=False)
    return (cc ** 2).tolist(), A


def best_p(points):
    """p minimizing the collapse RMS of cos^2 = s/(s+A), s=m*w^(p*i)."""
    out = {}
    for p in P_CANDIDATES:
        s = np.array([pt["m"] * (W ** (p * pt["i"])) for pt in points])
        y = np.array([pt["cos2"] for pt in points])
        best = None
        for logA in np.linspace(-10, 8, 3601):
            pred = s / (s + np.exp(logA))
            rms = float(np.sqrt(np.mean((pred - y) ** 2)))
            if best is None or rms < best:
                best = rms
        out[p] = best
    return min(out, key=out.get), out


def front_slope(cos2_by_m):
    """i*(m) = interpolated mode where mean cos^2 crosses 0.5; slope vs ln m."""
    ms, istar = [], []
    for m in M_GRID:
        c = cos2_by_m[m]
        i_cross = None
        for i in range(len(c) - 1):
            if c[i] >= 0.5 > c[i + 1]:
                i_cross = i + (c[i] - 0.5) / (c[i] - c[i + 1])
                break
        if i_cross is not None:
            ms.append(np.log(m))
            istar.append(i_cross)
    if len(ms) < 2:
        return None, list(zip(M_GRID, [None] * len(M_GRID)))
    slope = float(np.polyfit(ms, istar, 1)[0])
    return slope, istar


def main():
    seal_date = require_seal()
    print(f"OP3 graded — sealed {seal_date}, seeds {GRADED_SEEDS} "
          f"(disjoint from shakedown 0/1/2)")
    print(f"derived: p={DERIVED_P}, front rate={DERIVED_RATE:.3f} "
          f"(bar +/-{RATE_TOL})\n")

    per_seed = {}
    b3_overlaps = []
    for seed in GRADED_SEEDS:
        points, cos2_by_m = [], {}
        for m in M_GRID:
            c2, A_big = per_mode_cos2(seed, BASE_N * m)
            cos2_by_m[m] = c2
            for i, v in enumerate(c2):
                points.append({"i": i, "m": m, "cos2": v})
            if m == M_GRID[-1]:
                read_big = A_big
        bp, rms_by_p = best_p(points)
        slope, istar = front_slope(cos2_by_m)
        # B3': estimator realizes the affine operator M (top-16 overlap).
        _, topM = population_operator(seed)
        ov = subspace_overlap(read_big, topM).overlap
        b3_overlaps.append(ov)
        per_seed[seed] = {"best_p": bp, "rms_by_p": rms_by_p,
                          "front_slope": slope, "istar": istar,
                          "affine_overlap": round(float(ov), 4)}
        print(f"seed {seed}: best_p={bp:.0f}  front_slope="
              f"{slope:.3f}  affine_overlap={ov:.3f}")

    # Bars.
    b1 = all(per_seed[s]["best_p"] == DERIVED_P for s in GRADED_SEEDS)
    slopes = [per_seed[s]["front_slope"] for s in GRADED_SEEDS]
    mean_slope = float(np.mean(slopes))
    b2 = (abs(mean_slope - DERIVED_RATE) <= RATE_TOL
          and all(sl > 0.5 for sl in slopes))
    mean_ov = float(np.mean(b3_overlaps))
    b3 = mean_ov >= 0.9
    verdict = "PASS" if (b1 and b2 and b3) else "FAIL"

    print(f"\nB1' exponent==4 on every seed: {'PASS' if b1 else 'FAIL'}")
    print(f"B2' front rate (mean {mean_slope:.3f}, bar "
          f"{DERIVED_RATE:.3f}+/-{RATE_TOL}, all seeds >0.5): "
          f"{'PASS' if b2 else 'FAIL'}")
    print(f"B3' affine-operator overlap (mean {mean_ov:.3f}, bar 0.9): "
          f"{'PASS' if b3 else 'FAIL'}")
    print(f"\nOP3 corrected front law: {verdict}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"claim": "OP3-frontlaw", "sealed": str(seal_date),
               "seeds": GRADED_SEEDS, "derived_p": DERIVED_P,
               "derived_rate": round(DERIVED_RATE, 4),
               "per_seed": {str(k): v for k, v in per_seed.items()},
               "mean_front_slope": round(mean_slope, 4),
               "mean_affine_overlap": round(mean_ov, 4),
               "B1": bool(b1), "B2": bool(b2), "B3": bool(b3),
               "verdict": verdict},
              open(OUT, "w"), indent=1)
    print(f"-> {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
