"""SC-1 — the space-comms downlink substrate (shakedown).

First campaign of a new cross-domain crucible: does Observation Theory
transfer to a bandwidth-starved deep-space downlink, where the
"consumers" are downstream instrument science processors, each with its
own read operator? The core claim (P1+P2) is that consumer-relative bit
allocation `tr(P·Σ)` beats consumer-blind MSE allocation by a margin
that is DERIVABLE, not merely observed.

Working the high-rate water-filling algebra through gives a clean
a-priori prediction. With source spectrum `σ_k²` and aggregate consumer
importance `d_k = Σ_i w_i (P_i)_kk` (in the coding basis, where the
quantization noise is diagonal), the optimal consumer distortion is the
weighted geometric mean, while MSE allocation applied to the consumer
weights gives the arithmetic mean — the signal variance cancels:

    G = D_mse / D_cons = AM(d) / GM(d)          (high-rate limit)

`G ≥ 1` always (AM ≥ GM), `= 1` iff the instruments read uniformly, and
grows with the spread of `d`. This is readscope's core (the gain of
consumer relativity) written for a downlink: the gain is the AM/GM gap
of the instrument-importance spectrum.

This shakedown builds a family of synthetic downlink scenarios — a
power-law source spectrum, K instruments reading random subspaces
(tracker/spectrometer/imager archetypes) — sweeps the bit budget, and
checks the interior across seeds: does `G_measured` track `AM(d)/GM(d)`,
converging at high rate and departing at finite rate (the interior)?
No evidential weight; bars live in PREREG-SC1.md and seal on a fresh
day.

    python crucible/fam_sc1_shakedown.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\source\readscope")
from readscope import water_fill  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "SC1-shakedown.json")

D = 64                       # coding coordinates per frame
SPECTRUM_ALPHA = 1.5         # source variance sigma_k^2 ~ (k+1)^-alpha
K_INSTRUMENTS = 3            # consumers per scenario
N_SCENARIOS = 40             # per seed
BITS_PER_COORD = [1.0, 2.0, 3.0, 4.0]   # budget sweep = rate arm
SEEDS = [0, 1, 2]
# instrument archetypes: (subspace centre as a fraction of the band, rank)
ARCHETYPES = [("tracker", 0.10, 6), ("imager", 0.45, 8),
              ("spectrometer", 0.80, 4)]


def source_spectrum():
    k = np.arange(D)
    s = (k + 1.0) ** (-SPECTRUM_ALPHA)
    return s / s.sum() * D           # mean variance 1


def instrument_operator(rng, centre_frac, rank):
    """A rank-`rank` projection whose subspace clusters near band position
    `centre_frac` (0=low coords/aligned with signal top, 1=high coords).
    Returns the coding-basis diagonal d^(i)_k = (P_i)_kk."""
    centre = centre_frac * (D - 1)
    # draw directions concentrated near the centre coordinate band
    cols = []
    for _ in range(rank):
        v = rng.normal(size=D) * np.exp(-0.5 * ((np.arange(D) - centre)
                                                / (0.12 * D)) ** 2)
        v += 0.05 * rng.normal(size=D)      # a little leakage everywhere
        cols.append(v / np.linalg.norm(v))
    V = np.linalg.qr(np.array(cols).T)[0]   # orthonormalise the frame
    P = V @ V.T
    return np.clip(np.diag(P), 0.0, None)


def consumer_distortion_of(bits, weights):
    return float(np.sum(weights * np.power(2.0, -2.0 * bits)))


def scenario(rng, sigma2, bits_per_coord):
    # aggregate instrument importance d_k = sum_i w_i (P_i)_kk
    d = np.zeros(D)
    for name, cf, rank in ARCHETYPES:
        w_i = rng.uniform(0.5, 1.5)
        d += w_i * instrument_operator(rng, cf, rank)
    d = np.clip(d, 1e-9, None)
    budget = bits_per_coord * D
    weights_cons = d * sigma2
    a_mse = water_fill(sensitivity=np.ones(D), variance=sigma2, budget=budget)
    a_cons = water_fill(sensitivity=d, variance=sigma2, budget=budget)
    D_cons = consumer_distortion_of(a_cons.bits, weights_cons)
    D_mse = consumer_distortion_of(a_mse.bits, weights_cons)
    g_meas = D_mse / D_cons if D_cons > 0 else float("nan")
    # high-rate prediction over coords that carry importance
    live = d > 1e-6
    am = float(np.mean(d[live]))
    gm = float(np.exp(np.mean(np.log(d[live]))))
    g_pred = am / gm
    cv2 = float(np.var(d[live]) / np.mean(d[live]) ** 2)
    return {"g_meas": g_meas, "g_pred": g_pred, "cv2": cv2,
            "n_dark_mse": int(np.sum(a_mse.bits <= 1e-9)),
            "n_dark_cons": int(np.sum(a_cons.bits <= 1e-9))}


def main():
    sigma2 = source_spectrum()
    print(f"SC-1 downlink shakedown — d={D} K={K_INSTRUMENTS} "
          f"scenarios={N_SCENARIOS} seeds={SEEDS}")
    print("prediction: G = D_mse/D_cons -> AM(d)/GM(d) at high rate\n")

    rows, by_seed_rate = [], {}
    for seed in SEEDS:
        for bpc in BITS_PER_COORD:
            rng = np.random.default_rng(seed * 7919 + int(bpc * 10))
            gm_meas, gm_pred = [], []
            for _ in range(N_SCENARIOS):
                r = scenario(rng, sigma2, bpc)
                rows.append({"seed": seed, "bits_per_coord": bpc, **r})
                gm_meas.append(r["g_meas"])
                gm_pred.append(r["g_pred"])
            gm_meas = np.array(gm_meas)
            gm_pred = np.array(gm_pred)
            rho = float(stats.spearmanr(gm_meas, gm_pred).statistic)
            ratio = float(np.median(gm_meas / gm_pred))
            by_seed_rate[(seed, bpc)] = (rho, ratio, gm_pred)
            print(f"  seed {seed} rate {bpc:.0f}b/coord: "
                  f"G_pred spread [{gm_pred.min():.2f},{gm_pred.max():.2f}]  "
                  f"Spearman(meas,pred)={rho:+.3f}  "
                  f"median meas/pred={ratio:.3f}")
        print()

    # interior summary: does the family span a range of G_pred (not all ~1),
    # does G_meas track G_pred, and does meas/pred -> 1 as rate grows?
    print("interior check (seed-pooled):")
    for bpc in BITS_PER_COORD:
        rhos = [by_seed_rate[(s, bpc)][0] for s in SEEDS]
        ratios = [by_seed_rate[(s, bpc)][1] for s in SEEDS]
        spreads = [by_seed_rate[(s, bpc)][2] for s in SEEDS]
        allpred = np.concatenate(spreads)
        print(f"  rate {bpc:.0f}b/coord: Spearman {np.mean(rhos):+.3f} "
              f"(min {min(rhos):+.3f})  meas/pred {np.mean(ratios):.3f}  "
              f"G_pred in [{allpred.min():.2f},{allpred.max():.2f}]")

    record = {
        "campaign": "SC-1", "sealed": False, "shakedown": True,
        "note": "no evidential weight; bars in crucible/PREREG-SC1.md",
        "generated": datetime.now(timezone.utc).isoformat(),
        "constants": {"d": D, "alpha": SPECTRUM_ALPHA,
                      "k_instruments": K_INSTRUMENTS,
                      "n_scenarios": N_SCENARIOS,
                      "bits_per_coord": BITS_PER_COORD, "seeds": SEEDS,
                      "archetypes": ARCHETYPES},
        "rows": rows,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(record, open(OUT, "w"), indent=1)
    print(f"\nwrote {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
