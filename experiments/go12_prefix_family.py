#!/usr/bin/env python
"""GO-P-2026-066 harness: the conditional-variance reduction and the
access-class interpolation (GO-12 Theorem 1).

  s1  REDUCTION: L_G(D) = 1/2 log2 g*(rho^2, 1/(1-q_G), D) for ANY
      Gaussian context sigma-algebra G -- gated against direct channel
      optimization on SIX access classes including asymmetric and
      gapped subsets.
  s2  SLICE CONSISTENCY: q_slice = 1 - a^{2D}/(1+tau2) reproduces the
      065 (B) substitution s_eff = (1+tau2)/a^{2Delta} exactly.
  s3  CLOSED FORMS: prefix = steady-state Kalman fixed-lag variance
      (Riccati + geometric improvement) vs windowed covariance; path =
      noncausal Wiener MMSE integral vs windowed covariance.
  s4  STRICT INTERPOLATION: L_slice > L_prefix > L_path over a lag
      grid, two instances, plus pole edges a in {0.05, 0.99}.

Single governed run. Sentinel ===GO12PF-JSON=== with ===END===;
summary flag GO12PF_supported.
"""
import argparse
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import minimize

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20260917 if a_.pilot
                                            else 20260918)
rng = np.random.default_rng(SEED)
verdicts = {}
vals = {}


def gstar(rho2, s, D):
    A, B, C = D * s, -(D + s - rho2), (1 - rho2)
    return (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)


def build_cov(a, rho, tau2, idx_S):
    n = len(idx_S)
    C = np.zeros((2 + n, 2 + n))
    C[0, 0] = C[1, 1] = 1.0
    C[0, 1] = C[1, 0] = rho
    for i, si in enumerate(idx_S):
        C[0, 2 + i] = C[2 + i, 0] = rho * a ** abs(si)
        C[1, 2 + i] = C[2 + i, 1] = a ** abs(si)
        for j, sj in enumerate(idx_S):
            C[2 + i, 2 + j] = a ** abs(si - sj) + (tau2 if i == j else 0)
    return C


def qG(a, rho, tau2, idx_S):
    C = build_cov(a, rho, tau2, idx_S)
    cv = C[1, 2:]
    return 1.0 - cv @ np.linalg.solve(C[2:, 2:], cv)


def direct_L(a, rho, tau2, idx_S, D, starts=40):
    C = build_cov(a, rho, tau2, idx_S)
    CSi = np.linalg.inv(C[2:, 2:])

    def L_of(al, be, nv):
        w = np.array([al, be])
        var_h = w @ C[:2, :2] @ w + nv
        cross = w @ C[:2, 2:]
        return 0.5 * math.log2((var_h - cross @ CSi @ cross) / nv)

    def dist(al, be, nv):
        w = np.array([al, be])
        return 1.0 - 2 * (w @ C[0, :2]) + (w @ C[:2, :2] @ w + nv)

    best = None
    for _ in range(starts):
        p0 = np.array([rng.uniform(0.2, 1.0), rng.uniform(-0.3, 0.6),
                       math.log(rng.uniform(1e-3, 0.5))])
        r = minimize(
            lambda p: L_of(p[0], p[1], math.exp(min(p[2], 20))), p0,
            constraints=[{"type": "ineq", "fun":
                          lambda p: D - dist(p[0], p[1],
                                             math.exp(min(p[2], 20)))}],
            method="SLSQP", options={"maxiter": 2000, "ftol": 1e-14})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    return best


def kalman_fixed_lag(a, tau2, lag, iters=400):
    p = 1.0
    for _ in range(iters):
        pm = a * a * p + (1 - a * a)
        p = pm * tau2 / (pm + tau2)
    q, c, pk = p, p, p
    for _ in range(lag):
        pm = a * a * pk + (1 - a * a)
        cm = a * c
        gain = pm / (pm + tau2)
        pk = pm * tau2 / (pm + tau2)
        q = q - cm * cm / (pm + tau2)
        c = cm * (1 - gain)
    return q


def wiener_path(a, tau2, ngrid=200000):
    w = (np.arange(ngrid) + 0.5) * (2 * np.pi / ngrid) - np.pi
    SV = (1 - a * a) / np.abs(1 - a * np.exp(-1j * w)) ** 2
    return float(np.mean(SV * tau2 / (SV + tau2)))


# s1: reduction vs direct, six access classes
a, rho, tau2, D = 0.8, 0.7, 0.4, 0.3
Delta, K = 3, 80
classes = {
    "slice": [Delta], "twosample": [Delta, Delta - 1],
    "straddle": [-2, Delta], "gapped": [-5, 2, 7],
    "prefix": list(range(-K, Delta + 1)),
    "path": list(range(-K, K + 1)),
}
worst_red, qs = 0.0, {}
for name, idx in classes.items():
    q = qG(a, rho, tau2, idx)
    qs[name] = q
    Lred = 0.5 * math.log2(gstar(rho * rho, 1 / (1 - q), D))
    Ldir = direct_L(a, rho, tau2, idx, D)
    worst_red = max(worst_red, abs(Lred - Ldir)
                    if Ldir is not None else 1.0)
vals["s1_worst_gap"] = worst_red
verdicts["s1_reduction"] = bool(worst_red <= 1e-6)

# s2: slice consistency with 065 (B)
q_form = 1 - a ** (2 * Delta) / (1 + tau2)
vals["s2_qdev"] = abs(qs["slice"] - q_form)
vals["s2_sdev"] = abs(1 / (1 - qs["slice"]) - (1 + tau2) / a ** (2 * Delta))
verdicts["s2_slice_065"] = bool(vals["s2_qdev"] <= 1e-12
                                and vals["s2_sdev"] <= 1e-8)

# s3: closed forms vs windowed covariances
vals["s3_kalman_dev"] = abs(kalman_fixed_lag(a, tau2, Delta)
                            - qs["prefix"])
vals["s3_wiener_dev"] = abs(wiener_path(a, tau2) - qs["path"])
verdicts["s3_closed_forms"] = bool(vals["s3_kalman_dev"] <= 1e-6
                                   and vals["s3_wiener_dev"] <= 1e-4)

# s4: strict interpolation, lag grid, two instances + pole edges
strict_ok, min_gap_sp, min_gap_pf = True, 1.0, 1.0
for (ai, ti) in [(0.8, 0.4), (0.55, 1.1)]:
    q_f = wiener_path(ai, ti)
    for lag in (0, 1, 3, 6):
        q_s = 1 - ai ** (2 * lag) / (1 + ti)
        q_p = kalman_fixed_lag(ai, ti, lag)
        strict_ok &= q_s > q_p > q_f
        min_gap_sp = min(min_gap_sp, q_s - q_p)
        min_gap_pf = min(min_gap_pf, q_p - q_f)
for ai in (0.05, 0.99):
    q_f = wiener_path(ai, 0.4)
    for lag in (0, 2):
        q_s = 1 - ai ** (2 * lag) / 1.4
        q_p = kalman_fixed_lag(ai, 0.4, lag)
        strict_ok &= q_s >= q_p >= q_f - 1e-12
vals["s4_min_gap_slice_prefix"] = min_gap_sp
vals["s4_min_gap_prefix_path"] = min_gap_pf
verdicts["s4_interpolation"] = bool(strict_ok and min_gap_sp > 1e-9
                                    and min_gap_pf > 1e-12)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: float(v) for k, v in vals.items()},
           verdicts=verdicts, GO12PF_supported=bool(allpass))
print("===GO12PF-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
