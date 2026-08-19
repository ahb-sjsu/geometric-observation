"""GO-P-2026-089 (DRAFT) -- operational event triggering (OT-EC Campaign 4).

Smart-sensor remote estimation: a sensor node sees the state; a remote
estimator (which the consumer reads) coasts on x_hat = A x_hat between
transmissions and receives the exact state on transmission. The trigger is
SIGNAL-AWARE: transmit when the realized gap e = x - x_hat satisfies
e' W e > tau. Pilot 1 (disclosed) established the null that motivates this:
with covariance-only (signal-agnostic) statistics, every threshold trigger
collapses to a quasi-periodic schedule and T1 is ~0 -- direction only matters
to WHEN if the trigger sees the realized error. Thresholds are calibrated
per (system, policy) on CALIBRATION noise bundles to hit the matched mean
transmission budget, then frozen and evaluated on held-out bundles (common
random numbers across policies), exactly as the draft prereg registered.

Triggers: ot-true e'P_C e | ot-blind e'P_hat e (query-only recovery as
GO-087, probe cost charged in transmission-equivalents) | iso e'e |
periodic (evenly spaced) | shuffled / anti controls.

Machinery imported from the sealed blind_scheduling.py (NOT modified).

  --calibrate       internal calibration; prints candidate floors.
  --governed SEED   single governed run; writes results/GO89-operational-trigger.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from blind_scheduling import (D, M_POOL, T_STEPS, N_TEST, LAMBDA_P,
                              make_system, steady_prior,
                              make_noise_bundles, probe_read_operator,
                              anti_operator, LinearConsumer, MLPConsumer,
                              ThresholdConsumer)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_SYS_CAL = 8
N_SYS_GOV = 20
B_UPDATES = 15        # update budget per rollout
K_PER_UPDATE = 3      # sensors per update (consumer-agnostic greedy, all arms)

# --------------------------------- SEALED GATES (frozen 2026-08-19 from the
# three disclosed calibration pilots; must match the prereg YAML)
FROZEN_DELTA_T = 0.10     # T1 gate (cal: armP 0.259, armN 0.348; raised from 0.05 draft)
FROZEN_EPS_T = 0.25       # T2 gate: blind capture >= 0.75 (cal 0.876)
FROZEN_BUDGET_BAND = 0.10 # T3: realized mean updates within +-band of target


def system_factors(A, Q):
    """Precompute per-system factors once (steady_prior is a 400-step
    recursion; recomputing it per rollout was the pilot-2 timeout)."""
    S0 = steady_prior(A, Q)
    L0 = np.linalg.cholesky(S0 + 1e-9 * np.eye(D))
    Lq = np.linalg.cholesky(Q + 1e-12 * np.eye(D))
    return L0, Lq


def error_paths(A, L0, Lq, noise_list):
    """Precompute, per bundle, the free-running error increments: with resets,
    e after a fire restarts from 0 and evolves e_{t+1} = A e_t + w_t, so the
    whole trigger process is a function of (x0_free, w) only."""
    return [(L0 @ nb["x0"], np.array([Lq @ nb["w"][t] for t in range(T_STEPS)]))
            for nb in noise_list]


def count_fires(A, W, tau, path):
    """Fires-only fast path (no consumer, no loss)."""
    e0, wseq = path
    e = e0.copy()
    fires = 0
    for t in range(T_STEPS):
        e = A @ e + wseq[t]
        if e @ (W @ e) > tau:
            e = np.zeros(D)
            fires += 1
    return fires


def trigger_rollout(A, L0, Lq, consumer, W, tau, noise, periodic_fires=None):
    """One rollout of smart-sensor remote estimation. Signal-aware trigger:
    transmit (reset e to 0) when e' W e > tau; or a fixed periodic schedule
    when `periodic_fires` is given. Returns (mean consumer loss, n_fires)."""
    x = L0 @ noise["x0"]
    xhat = np.zeros(D)
    loss_sum, fires = 0.0, 0
    for t in range(T_STEPS):
        x = A @ x + Lq @ noise["w"][t]
        xhat = A @ xhat
        e = x - xhat
        fire = (t in periodic_fires) if periodic_fires is not None \
            else (e @ (W @ e) > tau)
        if fire:
            xhat = x.copy()
            fires += 1
        loss_sum += consumer.loss(xhat, x)
    return loss_sum / T_STEPS, fires


def calibrate_tau(A, W, paths, budget):
    """Bisect tau so the MEAN transmission count over the calibration error
    paths hits `budget`."""
    lo, hi = 0.0, 1.0
    def mean_fires(tau):
        return float(np.mean([count_fires(A, W, tau, p) for p in paths]))
    while mean_fires(hi) > budget and hi < 1e9:
        hi *= 4
    best_tau, best_gap = hi, float("inf")
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        n = mean_fires(mid)
        gap = abs(n - budget)
        if gap < best_gap:
            best_gap, best_tau = gap, mid
        if n >= budget:
            lo = mid
        else:
            hi = mid
    return best_tau


def run_arm(arm, n_sys, seed):
    rng = np.random.default_rng(seed)
    per_sys = []
    for s_idx in range(n_sys):
        A, Q, H, r = make_system(rng)
        S_probe = steady_prior(A, Q)
        if arm == "P":
            consumer = LinearConsumer(rng)
            true_pc = consumer.true_pc()
        else:
            consumer = MLPConsumer(rng) if s_idx % 2 == 0 else ThresholdConsumer(rng)
            true_pc, _ = probe_read_operator(consumer, S_probe, rng, n_probe=320)
        probed_pc, n_q = probe_read_operator(consumer, S_probe, rng)
        perm = rng.permutation(D)
        shuf_pc, n_qs = probe_read_operator(consumer, S_probe, rng, perm=perm)
        charge_upd = int(np.ceil(LAMBDA_P * n_q / K_PER_UPDATE))
        P_anti = anti_operator(probed_pc)

        # normalize trigger metrics to unit trace so tau scales are comparable
        def unit(P):
            return P / max(np.trace(P), 1e-12)

        specs = {
            "ot-true":  (unit(true_pc), B_UPDATES),
            "ot-blind": (unit(probed_pc), B_UPDATES - charge_upd),
            "iso":      (np.eye(D) / D, B_UPDATES),
            "shuffled": (unit(shuf_pc), B_UPDATES - charge_upd),
            "anti":     (unit(P_anti), B_UPDATES - charge_upd),
        }
        L0, Lq = system_factors(A, Q)
        cal_noise = make_noise_bundles(rng, N_TEST)      # threshold calibration
        eval_noise = make_noise_bundles(rng, N_TEST)     # held-out, CRN across arms
        cal_paths = error_paths(A, L0, Lq, cal_noise)
        periodic_fires = set(np.linspace(0, T_STEPS - 1, B_UPDATES).astype(int))
        row = {}
        for name, (W, budget) in specs.items():
            tau = calibrate_tau(A, W, cal_paths, budget)
            out = [trigger_rollout(A, L0, Lq, consumer, W, tau, nb) for nb in eval_noise]
            row[name] = {"loss": float(np.mean([o[0] for o in out])),
                         "loss_se": float(np.std([o[0] for o in out]) / np.sqrt(N_TEST)),
                         "updates": float(np.mean([o[1] for o in out]))}
        out = [trigger_rollout(A, L0, Lq, consumer, None, 0.0, nb, periodic_fires)
               for nb in eval_noise]
        row["periodic"] = {"loss": float(np.mean([o[0] for o in out])),
                           "loss_se": float(np.std([o[0] for o in out]) / np.sqrt(N_TEST)),
                           "updates": float(np.mean([o[1] for o in out]))}
        row["_meta"] = {"n_queries": n_q, "charge_updates": charge_upd}
        per_sys.append(row)
    return per_sys


def metrics_from(armP, armN):
    def rel_impr(per_sys):
        vals = []
        for s in per_sys:
            base = min(s["periodic"]["loss"], s["iso"]["loss"])
            vals.append((base - s["ot-true"]["loss"]) / base)
        return float(np.mean(vals))
    t1P, t1N = rel_impr(armP), rel_impr(armN)
    g_bl = sum(s["periodic"]["loss"] - s["ot-blind"]["loss"] for s in armP)
    g_tr = sum(s["periodic"]["loss"] - s["ot-true"]["loss"] for s in armP)
    t2 = float(g_bl / max(g_tr, 1e-12))
    # T3: verdict arms within band of their own targets
    ok = []
    for s in armP + armN:
        ok.append(abs(s["ot-true"]["updates"] - B_UPDATES) <= FROZEN_BUDGET_BAND * B_UPDATES)
        tgt = B_UPDATES - s["_meta"]["charge_updates"]
        ok.append(abs(s["ot-blind"]["updates"] - tgt) <= FROZEN_BUDGET_BAND * B_UPDATES)
        ok.append(abs(s["iso"]["updates"] - B_UPDATES) <= FROZEN_BUDGET_BAND * B_UPDATES)
    t3 = all(ok)
    shuf_gap = float(np.mean([s["shuffled"]["loss"] - s["iso"]["loss"] for s in armP + armN]))
    def pooled(per_sys, k):
        return float(np.mean([s[k]["loss"] for s in per_sys]))
    anti_worst = all(
        pooled(a, "anti") >= max(pooled(a, "iso"), pooled(a, "ot-true"),
                                 pooled(a, "ot-blind")) - 1e-12
        for a in (armP, armN))
    return t1P, t1N, t2, t3, shuf_gap, anti_worst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--governed", type=int, metavar="SEED")
    args = ap.parse_args()
    if args.calibrate:
        seed, n_sys, tag = 20260820, N_SYS_CAL, "CALIBRATION"
    elif args.governed is not None:
        seed, n_sys, tag = args.governed, N_SYS_GOV, "GOVERNED"
    else:
        ap.error("choose --calibrate or --governed SEED")

    print(f"[{tag}] seed={seed} n_sys={n_sys} B={B_UPDATES} k/upd={K_PER_UPDATE} "
          f"T={T_STEPS} n_test={N_TEST} lambda_p={LAMBDA_P}")
    armP = run_arm("P", n_sys, seed)
    armN = run_arm("N", n_sys, seed + 1)
    t1P, t1N, t2, t3, shuf_gap, anti_worst = metrics_from(armP, armN)
    print(f"T1 rel improvement of ot-true over best({{periodic,iso}}): "
          f"armP {t1P:.3f}, armN {t1N:.3f}  (gate both >= {FROZEN_DELTA_T:.2f})")
    print(f"T2 blind capture of ot-true's advantage over periodic (armP, pooled, "
          f"probe-charged): {t2:.3f}  (gate >= {1 - FROZEN_EPS_T:.2f})")
    print(f"T3 budgets within band: {t3}")
    print(f"controls: shuffled-vs-iso gap {shuf_gap:+.4f} (want ~>= 0); "
          f"anti worst pooled per arm: {anti_worst}")

    if args.calibrate:
        print("\n[CALIBRATION] freeze conservative floors in the prereg, then seal.")
        return

    gates = {
        "T1_armP": t1P >= FROZEN_DELTA_T,
        "T1_armN": t1N >= FROZEN_DELTA_T,
        "T2_blind_match": t2 >= 1 - FROZEN_EPS_T,
        "T3_budget_band": t3,
        "C_shuffled_no_free_lunch": shuf_gap >= -0.02,
        "C_anti_worst": anti_worst,
    }
    verdict = "ALL PASS" if all(gates.values()) else "FAIL"
    out = {
        "id": "GO-P-2026-089", "seed": seed, "n_sys": n_sys,
        "config": {"D": D, "M_POOL": M_POOL, "B_UPDATES": B_UPDATES,
                   "K_PER_UPDATE": K_PER_UPDATE, "T_STEPS": T_STEPS,
                   "N_TEST": N_TEST, "LAMBDA_P": LAMBDA_P,
                   "delta_T": FROZEN_DELTA_T, "eps_T": FROZEN_EPS_T,
                   "budget_band": FROZEN_BUDGET_BAND},
        "armP": armP, "armN": armN,
        "metrics": {"T1_armP": t1P, "T1_armN": t1N, "T2": t2, "T3": t3,
                    "shuffled_gap": shuf_gap, "anti_worst": anti_worst},
        "gates": gates, "verdict": verdict,
    }
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "GO89-operational-trigger.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n[GOVERNED] verdict: {verdict}  gates: {gates}\nwrote {path}")


if __name__ == "__main__":
    main()
