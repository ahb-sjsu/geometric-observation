#!/usr/bin/env python
"""GO-P-2026-067 harness: GO-13 Theorem 1 -- the matrix-q reduction,
access-class universality of the dynamic tax, coordinate monotonicity,
and the q->1 endpoint CT_W -> CT_R. Gates:
  s1 reduction vs direct conditioning on actual S-sets (three classes)
  s2 equal-q universality (slice vs prefix tuned to identical q)
  s3 coordinate monotonicity in q + q->1 endpoint = marginal program
  s4 tax-curve report: |CT_W(q_hi) - CT_R| small; full curve REPORTED
     (Conjecture 2's monotone clause is exploratory, not gated)
Sentinel ===GO13MQ-JSON=== with ===END===; flag GO13MQ_supported.
"""
import argparse
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import minimize, brentq

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20260920 if a_.pilot
                                            else 20260921)
rng = np.random.default_rng(SEED)
verdicts = {}
vals = {}
rAB, rAV, rBV, aP = 0.3, 0.7, 0.2, 0.8
SigT = np.array([[1, rAB, rAV], [rAB, 1, rBV], [rAV, rBV, 1.0]])
cvec = SigT[:, 2].copy()
DA, DB, W = 0.2, 0.2, 0.5


def qG(tau2, idx):
    n = len(idx)
    CS = np.array([[aP ** abs(i - j) + (tau2 if i == j else 0)
                    for j in idx] for i in idx])
    cv = np.array([aP ** abs(i) for i in idx])
    return 1.0 - cv @ np.linalg.solve(CS, cv)


def prog(SigTc, m=1, starts=50):
    """Thm-9 weighted program value at (SigT, SigTc); m=1 uses read A."""
    if m == 1:
        y0 = np.array([1.0, 0, 0])

        def obj(p):
            u, nv = p[:3], math.exp(min(p[3], 20))
            Q0 = float(u @ SigT @ u)
            Q1 = float(u @ SigTc @ u)
            return (W * math.log((Q0 + nv) / nv)
                    + (1 - W) * math.log((Q1 + nv) / nv))

        def con(p):
            u, nv = p[:3], math.exp(min(p[3], 20))
            d = y0 - u
            return DA - (float(d @ SigT @ d) + nv)

        best = None
        for _ in range(starts):
            p0 = np.concatenate([y0 * rng.uniform(0.3, 0.9)
                                 + rng.normal(0, 0.05, 3),
                                 [math.log(rng.uniform(1e-3, 0.3))]])
            r = minimize(obj, p0,
                         constraints=[{"type": "ineq", "fun": con}],
                         method="SLSQP",
                         options={"maxiter": 3000, "ftol": 1e-15})
            if r.success and (best is None or r.fun < best):
                best = r.fun
        return best / (2 * math.log(2))

    def unpack(p):
        A = p[:6].reshape(2, 3)
        Lc = np.array([[math.exp(min(p[6], 20)), 0],
                       [p[7], math.exp(min(p[8], 20))]])
        return A, Lc @ Lc.T

    def obj(p):
        A, SN = unpack(p)
        M0 = A @ SigT @ A.T + SN
        M1 = A @ SigTc @ A.T + SN
        dn = np.linalg.det(SN)
        d0_, d1_ = np.linalg.det(M0), np.linalg.det(M1)
        if dn <= 1e-280 or d0_ <= 1e-280 or d1_ <= 1e-280:
            return 90.0
        return (W * math.log(d0_ / dn)
                + (1 - W) * math.log(d1_ / dn))

    cons = []
    for i, Dv in ((0, DA), (1, DB)):
        def c(p, i=i, Dv=Dv):
            A, SN = unpack(p)
            d = np.eye(3)[i] - A[i]
            return Dv - (float(d @ SigT @ d) + SN[i, i])
        cons.append({"type": "ineq", "fun": c})
    best = None
    for _ in range(starts):
        p0 = np.concatenate([
            (np.eye(2, 3) * rng.uniform(0.3, 0.9)).ravel()
            + rng.normal(0, 0.05, 6),
            [math.log(rng.uniform(5e-3, 0.3)), rng.uniform(-0.1, 0.1),
             math.log(rng.uniform(5e-3, 0.3))]])
        r = minimize(obj, p0, constraints=cons, method="SLSQP",
                     options={"maxiter": 3000, "ftol": 1e-15})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    return best / (2 * math.log(2))


def direct(tau2, idx, starts=50):
    """Direct m=2: minimize w*rate + (1-w)*I(T;Yh|S-set)."""
    n = len(idx)
    CS = np.array([[aP ** abs(i - j) + (tau2 if i == j else 0)
                    for j in idx] for i in idx])
    cv = np.array([aP ** abs(i) for i in idx])   # Cov(V_t, S)
    CTS = np.outer(cvec, cv)                     # Cov(T, S) rank-one
    CSi = np.linalg.inv(CS)

    def unpack(p):
        A = p[:6].reshape(2, 3)
        Lc = np.array([[math.exp(min(p[6], 20)), 0],
                       [p[7], math.exp(min(p[8], 20))]])
        return A, Lc @ Lc.T

    def obj(p):
        A, SN = unpack(p)
        M0 = A @ SigT @ A.T + SN
        CYS = A @ CTS
        M1 = M0 - CYS @ CSi @ CYS.T
        dn = np.linalg.det(SN)
        d0_, d1_ = np.linalg.det(M0), np.linalg.det(M1)
        if dn <= 1e-280 or d0_ <= 1e-280 or d1_ <= 1e-280:
            return 90.0
        return (W * math.log(d0_ / dn)
                + (1 - W) * math.log(d1_ / dn))

    cons = []
    for i, Dv in ((0, DA), (1, DB)):
        def c(p, i=i, Dv=Dv):
            A, SN = unpack(p)
            d = np.eye(3)[i] - A[i]
            return Dv - (float(d @ SigT @ d) + SN[i, i])
        cons.append({"type": "ineq", "fun": c})
    best = None
    for _ in range(starts):
        p0 = np.concatenate([
            (np.eye(2, 3) * rng.uniform(0.3, 0.9)).ravel()
            + rng.normal(0, 0.05, 6),
            [math.log(rng.uniform(5e-3, 0.3)), rng.uniform(-0.1, 0.1),
             math.log(rng.uniform(5e-3, 0.3))]])
        r = minimize(obj, p0, constraints=cons, method="SLSQP",
                     options={"maxiter": 3000, "ftol": 1e-15})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    return best / (2 * math.log(2))


worst_s1 = 0.0
for tau2, idx in [(0.4, [2]), (0.4, list(range(-25, 3))),
                  (1.1, [-1, 3])]:
    q = qG(tau2, idx)
    SigTc = SigT - (1 - q) * np.outer(cvec, cvec)
    worst_s1 = max(worst_s1, abs(prog(SigTc, m=2) - direct(tau2, idx)))
vals["s1_worst_gap"] = worst_s1
verdicts["s1_reduction"] = bool(worst_s1 <= 1e-6)

q_target = qG(0.4, [2])
t2m = brentq(lambda t: qG(t, list(range(-25, 1))) - q_target, 1e-3, 50)
vals["s2_univ_gap"] = abs(direct(0.4, [2])
                          - direct(t2m, list(range(-25, 1))))
verdicts["s2_universality"] = bool(vals["s2_univ_gap"] <= 1e-6)

prev, mono, curve = -1.0, True, []
for q in (0.2, 0.6, 0.95, 0.999999):
    SigTc = SigT - (1 - q) * np.outer(cvec, cvec)
    Lab = prog(SigTc, m=2)
    mono &= Lab > prev - 1e-9
    prev = Lab
    curve.append([q, Lab, Lab - prog(SigTc, m=1)])
Lab1 = prog(SigT, m=2)
CT_R = Lab1 - prog(SigT, m=1)
vals["s3_endpoint_dev"] = abs(prev - Lab1)
vals["s3_monotone"] = bool(mono)
verdicts["s3_mono_endpoint"] = bool(mono
                                    and vals["s3_endpoint_dev"] <= 1e-4)

vals["s4_tax_curve"] = curve
vals["s4_CT_R"] = CT_R
vals["s4_tax_endpoint_dev"] = abs(curve[-1][2] - CT_R)
verdicts["s4_tax_endpoint"] = bool(vals["s4_tax_endpoint_dev"] <= 1e-3)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: (v if isinstance(v, (list, bool))
                       else float(v)) for k, v in vals.items()},
           verdicts=verdicts, GO13MQ_supported=bool(allpass))
print("===GO13MQ-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
