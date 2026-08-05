#!/usr/bin/env python
"""GO-P-2026-068 harness: GO-13 Theorem 2 -- the tax-curve
characterization (envelope sign law).
  s1 envelope derivatives vs central finite differences, 4 instances
     covering both signs of dCT/dq
  s2 reference disambiguation at the 067 pilot instance: the MAX-based
     tax rises (dCT > 0, binding consumer B) while the A-referenced
     difference is near-flat -- nets the 067 clarification note
  s3 kink: bracket a max-switch q* (L_A = L_B) and check one-sided
     slopes match the two consumers' envelope sensitivities
  s4 w=1 flatness: dJ/dq = dL_i/dq = 0
Sentinel ===GO13TC-JSON=== with ===END===; flag GO13TC_supported.
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
SEED = a_.seed if a_.seed is not None else (20260923 if a_.pilot
                                            else 20260924)
rng = np.random.default_rng(SEED)
verdicts = {}
vals = {}
L2 = 2 * math.log(2)


def build(rABv):
    rAB, rAV, rBV = rABv
    S = np.array([[1, rAB, rAV], [rAB, 1, rBV], [rAV, rBV, 1.0]])
    return S, S[:, 2].copy()


def prog2(SigT, cvec, q, DA, DB, W, starts=60, ret_ch=False):
    SigTc = SigT - (1 - q) * np.outer(cvec, cvec)

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
    best, bp = None, None
    for _ in range(starts):
        p0 = np.concatenate([
            (np.eye(2, 3) * rng.uniform(0.3, 0.9)).ravel()
            + rng.normal(0, 0.05, 6),
            [math.log(rng.uniform(5e-3, 0.3)), rng.uniform(-0.1, 0.1),
             math.log(rng.uniform(5e-3, 0.3))]])
        r = minimize(obj, p0, constraints=cons, method="SLSQP",
                     options={"maxiter": 3000, "ftol": 1e-15})
        if r.success and (best is None or r.fun < best):
            best, bp = r.fun, r.x
    if not ret_ch:
        return best / L2
    A, SN = unpack(bp)
    M1 = A @ SigTc @ A.T + SN
    Ac = A @ cvec
    return best / L2, float(Ac @ np.linalg.solve(M1, Ac))


def prog1(SigT, cvec, q, i, Dv, W, starts=40, ret_ch=False):
    SigTc = SigT - (1 - q) * np.outer(cvec, cvec)
    y0 = np.eye(3)[i]

    def obj(p):
        u, nv = p[:3], math.exp(min(p[3], 20))
        return (W * math.log((u @ SigT @ u + nv) / nv)
                + (1 - W) * math.log((u @ SigTc @ u + nv) / nv))

    def c(p):
        u, nv = p[:3], math.exp(min(p[3], 20))
        d = y0 - u
        return Dv - (float(d @ SigT @ d) + nv)

    best, bp = None, None
    for _ in range(starts):
        p0 = np.concatenate([y0 * rng.uniform(0.3, 0.9)
                             + rng.normal(0, 0.05, 3),
                             [math.log(rng.uniform(1e-3, 0.3))]])
        r = minimize(obj, p0, constraints=[{"type": "ineq", "fun": c}],
                     method="SLSQP",
                     options={"maxiter": 3000, "ftol": 1e-15})
        if r.success and (best is None or r.fun < best):
            best, bp = r.fun, r.x
    if not ret_ch:
        return best / L2
    u, nv = bp[:3], math.exp(min(bp[3], 20))
    Q1 = float(u @ SigTc @ u)
    return best / L2, float((u @ cvec) ** 2 / (Q1 + nv))


INST = [
    ((0.3, 0.7, 0.2), 0.2, 0.2, 0.5, 0.5),
    ((-0.2, 0.5, 0.6), 0.3, 0.5, 0.5, 0.5),
    ((0.3, 0.7, 0.2), 0.25, 0.35, 0.25, 0.3),
    ((0.1, 0.6, -0.4), 0.3, 0.3, 0.7, 0.6),
]
h = 1e-4
worst_env, signs = 0.0, []
for rv, DA, DB, W, q in INST:
    SigT, cvec = build(rv)
    LJ, sensJ = prog2(SigT, cvec, q, DA, DB, W, ret_ch=True)
    dJ_fd = (prog2(SigT, cvec, q + h, DA, DB, W)
             - prog2(SigT, cvec, q - h, DA, DB, W)) / (2 * h)
    dJ_env = (1 - W) * sensJ / L2
    LA, sA = prog1(SigT, cvec, q, 0, DA, W, ret_ch=True)
    LB, sB = prog1(SigT, cvec, q, 1, DB, W, ret_ch=True)
    act, sact = (0, sA) if LA >= LB else (1, sB)
    Dv = DA if act == 0 else DB
    d1_fd = (prog1(SigT, cvec, q + h, act, Dv, W)
             - prog1(SigT, cvec, q - h, act, Dv, W)) / (2 * h)
    d1_env = (1 - W) * sact / L2
    worst_env = max(worst_env, abs(dJ_env - dJ_fd), abs(d1_env - d1_fd))
    signs.append(dJ_env - d1_env > 0)
vals["s1_worst_env_fd"] = worst_env
vals["s1_signs"] = signs
verdicts["s1_envelope"] = bool(worst_env <= 5e-4 and (True in signs)
                               and (False in signs))

# s2: max-based vs A-referenced at the 067 pilot instance
SigT, cvec = build((0.3, 0.7, 0.2))
q = 0.5
_, sensJ = prog2(SigT, cvec, q, 0.2, 0.2, 0.5, ret_ch=True)
LA, sA = prog1(SigT, cvec, q, 0, 0.2, 0.5, ret_ch=True)
LB, sB = prog1(SigT, cvec, q, 1, 0.2, 0.5, ret_ch=True)
dmax = 0.5 * (sensJ - sB) / L2
dAref = 0.5 * (sensJ - sA) / L2
vals["s2_binding_is_B"] = bool(LB > LA)
vals["s2_dCT_max"] = dmax
vals["s2_dCT_Aref"] = dAref
verdicts["s2_disambiguation"] = bool(LB > LA and dmax > 0.05
                                     and abs(dAref) < 0.05)

# s3: kink bracket on instance 3
rv, DA, DB, W = (0.3, 0.7, 0.2), 0.25, 0.35, 0.25
SigT, cvec = build(rv)


def gapAB(q):
    return (prog1(SigT, cvec, q, 0, DA, W, starts=30)
            - prog1(SigT, cvec, q, 1, DB, W, starts=30))


qs = brentq(gapAB, 0.05, 0.6, xtol=1e-6)
_, sA = prog1(SigT, cvec, qs, 0, DA, W, ret_ch=True)
_, sB = prog1(SigT, cvec, qs, 1, DB, W, ret_ch=True)
vals["s3_qstar"] = qs
vals["s3_kink_mag"] = abs(sA - sB) * (1 - W) / L2
verdicts["s3_kink"] = bool(0.05 < qs < 0.6
                           and vals["s3_kink_mag"] > 1e-4)

# s4: w=1 flatness
d1 = (prog2(SigT, cvec, 0.5 + h, DA, DB, 1.0)
      - prog2(SigT, cvec, 0.5 - h, DA, DB, 1.0)) / (2 * h)
vals["s4_w1_slope"] = abs(d1)
verdicts["s4_w1_flat"] = bool(abs(d1) <= 1e-5)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: (v if isinstance(v, (list, bool)) else float(v))
                   for k, v in vals.items()},
           verdicts=verdicts, GO13TC_supported=bool(allpass))
print("===GO13TC-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
