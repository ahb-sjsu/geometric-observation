"""GO-P-2026-088 (DRAFT) -- the consumer-relative flip in sensing (OT-EC Campaign 2).

Two planted rank-3 linear consumers with mutually orthogonal read subspaces;
two sensor schedules, each greedily aligned to one consumer's read operator,
trace-matched on time-average covariance. Predicted: the full two-consumer
verdict inversion (F1) at matched reconstruction, ordering predicted by
tr(P_i Sigma_bar) (F2), with a magnitude floor (F3). Planted consumers, no
recovery, no probe charge -- the planted-consumer complement to GO-087.

Machinery imported from the sealed blind_scheduling.py (NOT modified).

  --calibrate       internal calibration; prints candidate floors.
  --governed SEED   single governed run; writes results/GO88-consumer-flip.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from blind_scheduling import (D, M_POOL, K_BUDGET, T_STEPS, N_TEST,
                              make_system, steady_prior, greedy_weighted,
                              make_noise_bundles)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_SYS_CAL = 8
N_SYS_GOV = 20

# --------------------------------- SEALED GATES (frozen 2026-08-19 from the
# two disclosed calibration pilots; must match the prereg YAML)
FROZEN_TRACE_TOL = 0.10   # entry condition: rel. trace gap between aligned arms
FROZEN_Q_FLIP = 0.80      # F1 gate (cal: 1.000 on 4 matched systems)
FROZEN_Q_PRED = 0.85      # F2 gate (cal: 1.000)
FROZEN_DELTA_FLIP = 0.10  # F3 gate (cal: 0.303)
FROZEN_ISO_FRAC = 0.25    # control: iso may beat the aligned policy in <= this
FROZEN_MIN_MATCHED = 6    # integrity: governed run needs >= this many matched systems


class OrthoConsumer:
    """Linear consumer z = Lx with L supplied (rank 3)."""

    def __init__(self, L):
        self.L = L

    def loss(self, xhat, x):
        d = self.L @ (xhat - x)
        return float(d @ d)

    def pc(self):
        return self.L.T @ self.L


def make_consumer_pair(rng):
    """Two rank-3 linear consumers on mutually orthogonal row spaces."""
    Qb, _ = np.linalg.qr(rng.standard_normal((D, D)))
    w1 = rng.uniform(0.5, 1.5, size=3)[:, None]
    w2 = rng.uniform(0.5, 1.5, size=3)[:, None]
    return OrthoConsumer(w1 * Qb[:, 0:3].T), OrthoConsumer(w2 * Qb[:, 3:6].T)


def rollout2(A, Q, H, r, c1, c2, select_fn, noise):
    """One rollout scoring BOTH consumers on the same trajectory; also
    accumulates the time-average covariance matrix (deterministic given the
    selection rule, but accumulated here for transparency)."""
    S0 = steady_prior(A, Q)
    L0 = np.linalg.cholesky(S0 + 1e-9 * np.eye(D))
    x = L0 @ noise["x0"]
    xhat = np.zeros(D)
    S = S0.copy()
    Lq = np.linalg.cholesky(Q + 1e-12 * np.eye(D))
    l1 = l2 = 0.0
    Sbar = np.zeros((D, D))
    for t in range(T_STEPS):
        x = A @ x + Lq @ noise["w"][t]
        xhat = A @ xhat
        S = A @ S @ A.T + Q
        S = 0.5 * (S + S.T)
        for i in select_fn(S):
            h = H[i]
            y = h @ x + np.sqrt(r[i]) * noise["v"][t, i]
            Sh = S @ h
            kal = Sh / (h @ Sh + r[i])
            xhat = xhat + kal * (y - h @ xhat)
            S = S - np.outer(kal, Sh)
            S = 0.5 * (S + S.T)
        l1 += c1.loss(xhat, x)
        l2 += c2.loss(xhat, x)
        Sbar += S
    return l1 / T_STEPS, l2 / T_STEPS, Sbar / T_STEPS


def run(n_sys, seed):
    rng = np.random.default_rng(seed)
    per_sys = []
    for _ in range(n_sys):
        A, Q, H, r = make_system(rng)
        c1, c2 = make_consumer_pair(rng)
        P1, P2 = c1.pc(), c2.pc()
        noise = make_noise_bundles(rng, N_TEST)
        rand_rng = np.random.default_rng(rng.integers(2**31))
        rand_picks = [list(rand_rng.integers(0, M_POOL, size=K_BUDGET))
                      for _ in range(T_STEPS)]
        policies = {
            "align-1": lambda S: greedy_weighted(P1, S, H, r, K_BUDGET),
            "align-2": lambda S: greedy_weighted(P2, S, H, r, K_BUDGET),
            "iso-trace": lambda S: greedy_weighted(np.eye(D), S, H, r, K_BUDGET),
            "random": (lambda S, _c=iter(rand_picks * (N_TEST + 1)): next(_c)),
        }
        row = {}
        for name, fn in policies.items():
            L1s, L2s, Sb = [], [], None
            for nb in noise:
                a, b, Sbar = rollout2(A, Q, H, r, c1, c2, fn, nb)
                L1s.append(a)
                L2s.append(b)
                Sb = Sbar  # deterministic across rollouts
            row[name] = {"loss1": float(np.mean(L1s)), "loss2": float(np.mean(L2s)),
                         "tr": float(np.trace(Sb)),
                         "u1": float(np.trace(P1 @ Sb)), "u2": float(np.trace(P2 @ Sb))}
        per_sys.append(row)
    return per_sys


def gates_from(per_sys):
    matched = [s for s in per_sys
               if abs(s["align-1"]["tr"] - s["align-2"]["tr"])
               / max(s["align-1"]["tr"], s["align-2"]["tr"]) <= FROZEN_TRACE_TOL]
    n_excl = len(per_sys) - len(matched)
    flips = [ (s["align-1"]["loss1"] < s["align-2"]["loss1"]) and
              (s["align-2"]["loss2"] < s["align-1"]["loss2"]) for s in matched]
    f1 = float(np.mean(flips)) if matched else float("nan")
    # F2: does sign of u_i(align-1) - u_i(align-2) predict the loss ordering?
    checked = correct = 0
    for s in matched:
        for i in ("1", "2"):
            du = s["align-1"]["u" + i] - s["align-2"]["u" + i]
            dl = s["align-1"]["loss" + i] - s["align-2"]["loss" + i]
            checked += 1
            correct += int(du * dl > 0)
    f2 = correct / checked if checked else float("nan")
    # F3: relative gap on each consumer between anti-aligned and aligned policy
    gaps = []
    for s in matched:
        gaps.append((s["align-2"]["loss1"] - s["align-1"]["loss1"]) / s["align-2"]["loss1"])
        gaps.append((s["align-1"]["loss2"] - s["align-2"]["loss2"]) / s["align-1"]["loss2"])
    f3 = float(np.mean(gaps)) if gaps else float("nan")
    # controls
    iso_beats = []
    for s in matched:
        iso_beats.append(s["iso-trace"]["loss1"] < s["align-1"]["loss1"])
        iso_beats.append(s["iso-trace"]["loss2"] < s["align-2"]["loss2"])
    iso_frac = float(np.mean(iso_beats)) if iso_beats else float("nan")
    # random must be worse than each aligned policy ON ITS OWN consumer,
    # pooled over matched systems. (Per-cell all-comers is wrong by design:
    # the anti-aligned policy can legitimately serve the other consumer worse
    # than broad random sensing does.)
    rnd_worst = bool(matched) and (
        np.mean([s["random"]["loss1"] for s in matched])
        > np.mean([s["align-1"]["loss1"] for s in matched])
    ) and (
        np.mean([s["random"]["loss2"] for s in matched])
        > np.mean([s["align-2"]["loss2"] for s in matched])
    )
    return f1, f2, f3, iso_frac, rnd_worst, len(matched), n_excl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--governed", type=int, metavar="SEED")
    args = ap.parse_args()
    if args.calibrate:
        seed, n_sys, tag = 20260819, N_SYS_CAL, "CALIBRATION"
    elif args.governed is not None:
        seed, n_sys, tag = args.governed, N_SYS_GOV, "GOVERNED"
    else:
        ap.error("choose --calibrate or --governed SEED")

    print(f"[{tag}] seed={seed} n_sys={n_sys} D={D} pool={M_POOL} k={K_BUDGET} "
          f"T={T_STEPS} n_test={N_TEST}")
    per_sys = run(n_sys, seed)
    f1, f2, f3, iso_frac, rnd_worst, n_match, n_excl = gates_from(per_sys)
    print(f"trace-matched systems: {n_match}/{n_match + n_excl} "
          f"(band {FROZEN_TRACE_TOL:.2f}; excluded reported, never dropped silently)")
    print(f"F1 full two-consumer inversion: {f1:.3f}  (gate >= {FROZEN_Q_FLIP:.2f})")
    print(f"F2 composition-predicted ordering: {f2:.3f}  (gate >= {FROZEN_Q_PRED:.2f})")
    print(f"F3 mean relative consumer gap: {f3:.3f}  (gate >= {FROZEN_DELTA_FLIP:.2f})")
    print(f"controls: iso-beats-aligned fraction {iso_frac:.3f} "
          f"(gate <= {FROZEN_ISO_FRAC:.2f}); random worst: {rnd_worst}")

    if args.calibrate:
        print("\n[CALIBRATION] freeze conservative floors in the prereg, then seal.")
        return

    gates = {
        "F1_flip": f1 >= FROZEN_Q_FLIP,
        "F2_prediction": f2 >= FROZEN_Q_PRED,
        "F3_magnitude": f3 >= FROZEN_DELTA_FLIP,
        "I_min_matched": n_match >= FROZEN_MIN_MATCHED,
        "C_iso_bounded": iso_frac <= FROZEN_ISO_FRAC,
        "C_random_worst": rnd_worst,
    }
    verdict = "ALL PASS" if all(gates.values()) else "FAIL"
    out = {
        "id": "GO-P-2026-088", "seed": seed, "n_sys": n_sys,
        "config": {"D": D, "M_POOL": M_POOL, "K_BUDGET": K_BUDGET,
                   "T_STEPS": T_STEPS, "N_TEST": N_TEST,
                   "trace_tol": FROZEN_TRACE_TOL, "q_flip": FROZEN_Q_FLIP,
                   "q_pred": FROZEN_Q_PRED, "delta_flip": FROZEN_DELTA_FLIP,
                   "iso_frac": FROZEN_ISO_FRAC},
        "per_system": per_sys,
        "metrics": {"F1": f1, "F2": f2, "F3": f3, "iso_frac": iso_frac,
                    "random_worst": rnd_worst, "n_matched": n_match,
                    "n_excluded": n_excl},
        "gates": gates, "verdict": verdict,
    }
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "GO88-consumer-flip.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n[GOVERNED] verdict: {verdict}  gates: {gates}\nwrote {path}")


if __name__ == "__main__":
    main()
