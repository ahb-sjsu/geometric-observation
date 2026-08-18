"""SC-2 — LEO / interplanetary transport under predictable nonstationarity
(shakedown). Second campaign of the space-comms crucible.

Motivation: Starlink handovers on a fixed ~15 s cadence cause bursty loss
that standard TCP/QUIC misread as congestion; the proposed LEO-aware
transports (StarTCP, Leotp, Cloudflare's CC) fix it by knowing the
handover schedule. SpaceX's proposed Marslink pushes this to the limit —
a Starlink-architecture relay at up to 1.5 AU, where the ~25-minute
round-trip makes closed-loop congestion control physically impossible,
so the controller MUST predict the channel from its structure.

Observation Theory reading (P4 + P5, distinct from SC-1's allocation
law): the congestion controller is a *consumer* whose read operator
"loss -> congestion" is mismatched to a predictably nonstationary
channel. The observed loss is `L = H OR C`: a deterministic, known
handover indicator `H` (duty cycle ρ) ORed with the true congestion
state `C` (a Markov process, stationary rate c, lag-1 autocorrelation
λ). Feedback is delayed by `D` (propagation). Two read operators:

  naive  Ĉ(t) = L(t-D)                 (reacts to any loss)
  aware  Ĉ(t) = L(t-D) AND NOT H(t-D)  (masks the known schedule)

Two a-priori claims this shakedown looks at:

  Arm A (P5, the metric-consequence floor): masking the *predictable*
    disruption removes a false-congestion error equal to the handover
    duty cycle — `excess = naive_err - aware_err ≈ ρ(1-c)`, and this is
    invariant to the delay `D` (the schedule is known at any lag).

  Arm B (P4, nonstationarity vs delay): the feedback-tracking error
    grows with `D` as the congestion state decorrelates
    (`~ 2c(1-c)(1 - λ^D)`), toward the fully-decorrelated floor. Past a
    derivable crossover `D*` the delay error dominates the duty cycle:
    reactive feedback is useless and only the deterministic schedule is
    recoverable. Marslink (`D` ~ 25 min) is deep in that regime — the
    theory predicts *which* structure survives interplanetary delay: the
    predictable handover schedule, not the reactive congestion feedback.

No evidential weight; bars live in PREREG-SC2.md and seal on a fresh day.

    python crucible/fam_sc2_shakedown.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "SC2-shakedown.json")

T = 200_000                 # time steps
T_H = 100                   # handover period (steps)
C_RATE = 0.15               # stationary congestion probability
C_AUTOCORR = 0.90           # lag-1 autocorrelation of the congestion state
SEEDS = [0, 1, 2]
RHO_GRID = [0.05, 0.10, 0.20, 0.30]        # Arm A: handover duty cycle
D_GRID = [2, 20, 100, 500, 2000]           # Arm B: feedback delay (steps)


def congestion_series(rng):
    """2-state Markov chain with stationary rate C_RATE and lag-1
    autocorrelation C_AUTOCORR."""
    lam = C_AUTOCORR
    q0 = 1.0 - C_RATE * (1.0 - lam)        # P(0->0)
    q1 = lam + C_RATE * (1.0 - lam)        # P(1->1)
    c = np.empty(T, dtype=bool)
    c[0] = rng.random() < C_RATE
    u = rng.random(T)
    for t in range(1, T):
        if c[t - 1]:
            c[t] = u[t] < q1
        else:
            c[t] = u[t] >= q0            # flip 0->1 with prob 1-q0
    return c


def handover_series(rho):
    """Deterministic periodic handover: H=1 for the first ρ·T_H steps of
    each period. Known schedule (no randomness)."""
    delta = int(round(rho * T_H))
    h = np.zeros(T, dtype=bool)
    phase = np.arange(T) % T_H
    h[phase < delta] = True
    return h


def errors(c, h, D):
    """Naive and handover-aware read-operator error rates at delay D."""
    L = h | c
    obs_L = L[:-D] if D > 0 else L
    obs_H = h[:-D] if D > 0 else h
    tgt_C = c[D:] if D > 0 else c
    naive = obs_L
    aware = obs_L & ~obs_H
    naive_err = float(np.mean(naive != tgt_C))
    aware_err = float(np.mean(aware != tgt_C))
    return naive_err, aware_err


def main():
    print(f"SC-2 transport shakedown — T={T} T_H={T_H} c={C_RATE} "
          f"λ={C_AUTOCORR} seeds={SEEDS}")
    print("Arm A: excess=naive-aware vs duty ρ (predict ≈ ρ(1-c))")
    print("Arm B: aware_err vs delay D (predict rises ~2c(1-c)(1-λ^D))\n")

    rows = []
    # Arm A: sweep duty at small delay.
    print("Arm A (D=2):")
    armA = {r: [] for r in RHO_GRID}
    for seed in SEEDS:
        c = congestion_series(np.random.default_rng(seed * 2711 + 1))
        for rho in RHO_GRID:
            h = handover_series(rho)
            ne, ae = errors(c, h, 2)
            excess = ne - ae
            armA[rho].append(excess)
            rows.append({"arm": "A", "seed": seed, "rho": rho, "D": 2,
                         "naive_err": ne, "aware_err": ae, "excess": excess})
    for rho in RHO_GRID:
        pred = rho * (1 - 2 * C_RATE)   # derived kappa = 1-2c (SpaceComms.lean)
        print(f"  ρ={rho:.2f}: excess={np.mean(armA[rho]):.4f} "
              f"(predict ρ(1-2c)={pred:.4f})")
    # slope of excess vs rho (seed-mean)
    xs = np.array(RHO_GRID)
    ys = np.array([np.mean(armA[r]) for r in RHO_GRID])
    slope = float(np.polyfit(xs, ys, 1)[0])
    print(f"  excess-vs-ρ slope={slope:.3f} "
          f"(derived κ=1-2c={1-2*C_RATE:.3f})\n")

    # Arm B: sweep delay at fixed duty.
    print("Arm B (ρ=0.15):")
    h = handover_series(0.15)
    armB = {D: {"naive": [], "aware": [], "excess": []} for D in D_GRID}
    for seed in SEEDS:
        c = congestion_series(np.random.default_rng(seed * 2711 + 7))
        for D in D_GRID:
            ne, ae = errors(c, h, D)
            armB[D]["naive"].append(ne)
            armB[D]["aware"].append(ae)
            armB[D]["excess"].append(ne - ae)
            rows.append({"arm": "B", "seed": seed, "rho": 0.15, "D": D,
                         "naive_err": ne, "aware_err": ae,
                         "excess": ne - ae})
    floor = 2 * C_RATE * (1 - C_RATE)
    for D in D_GRID:
        ae = np.mean(armB[D]["aware"])
        ex = np.mean(armB[D]["excess"])
        pred_ae = floor * (1 - C_AUTOCORR ** D)
        print(f"  D={D:>4}: aware_err={ae:.4f} (predict {pred_ae:.4f}, "
              f"floor {floor:.4f})  excess={ex:.4f}")
    print(f"  decorrelation floor 2c(1-c)={floor:.4f}; "
          f"excess stays ≈ ρ(1-c)={0.15 * (1 - C_RATE):.4f} (D-invariant)")

    record = {
        "campaign": "SC-2", "sealed": False, "shakedown": True,
        "note": "no evidential weight; bars in crucible/PREREG-SC2.md",
        "generated": datetime.now(timezone.utc).isoformat(),
        "constants": {"T": T, "T_H": T_H, "c_rate": C_RATE,
                      "c_autocorr": C_AUTOCORR, "rho_grid": RHO_GRID,
                      "d_grid": D_GRID, "seeds": SEEDS},
        "armA_slope": round(slope, 4),
        "decorrelation_floor": round(floor, 4),
        "rows": rows,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(record, open(OUT, "w"), indent=1)
    print(f"\nwrote {os.path.relpath(OUT, HERE)}")


if __name__ == "__main__":
    main()
