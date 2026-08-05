#!/usr/bin/env python
"""GO-P-2026-071 harness: the WEIGHTED spectral theorem (GO-12
Conjecture 1 closed): per-mode decomposition at w in {0.5, 0.75},
convexity + equal slopes of the per-mode weighted value, classical-RWF
anchor at w~1 and work-endpoint closed-form anchor at w~0.
Sentinel ===GO12WS-JSON=== with ===END===; flag GO12WS_supported.
Pilot seed 20261003 / governed seed 20261004."""
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
SEED = a_.seed if a_.seed is not None else (20261003 if a_.pilot
                                            else 20261004)
verdicts = {}
vals = {}
rng = np.random.default_rng(SEED)
a, rho, tau2 = 0.8, 0.7, 0.4
def mode_params(n):
    k = np.arange(n)
    SV = np.real(np.fft.ifft(
        1.0 / np.abs(1 - a * np.exp(-2j * np.pi * k / n)) ** 2))
    SV = SV / SV[0]
    lamV = np.clip(np.real(np.fft.fft(SV)), 1e-9, None)
    SY = rho * rho * lamV + (1 - rho * rho)
    return lamV, SY


def mode_covs(n):
    lamV, SY = mode_params(n)
    SigZ = np.zeros((2 * n, 2 * n))
    for k in range(n):
        SigZ[k, k] = SY[k]
        SigZ[n + k, n + k] = lamV[k]
        SigZ[k, n + k] = SigZ[n + k, k] = rho * lamV[k]
    SigS = np.diag(lamV + tau2)
    CzS = np.zeros((2 * n, n))
    for k in range(n):
        CzS[k, k] = rho * lamV[k]
        CzS[n + k, k] = lamV[k]
    SigZcS = SigZ - CzS @ np.linalg.solve(SigS, CzS.T)
    return SigZ, SigZcS


def Jw_mode(SigZ, SigZcS, n, k, Dk, w, starts=6):
    """Per-mode weighted value: min w*rate + (1-w)*cond over scalar
    channels aY_k + bV_k + noise, dist <= Dk (nats/2ln2 -> bits)."""
    i, j = k, n + k

    def val(p):
        av, bv, nv = p[0], p[1], math.exp(min(p[2], 15))
        q0 = (av * av * SigZ[i, i] + 2 * av * bv * SigZ[i, j]
              + bv * bv * SigZ[j, j])
        q1 = (av * av * SigZcS[i, i] + 2 * av * bv * SigZcS[i, j]
              + bv * bv * SigZcS[j, j])
        if q0 + nv <= 0 or q1 + nv <= 0:
            return 90.0
        return (w * math.log((q0 + nv) / nv)
                + (1 - w) * math.log((max(q1, 0.0) + nv) / nv))

    def dk(p):
        av, bv, nv = p[0], p[1], math.exp(min(p[2], 15))
        e0, e1 = 1 - av, -bv
        return (e0 * e0 * SigZ[i, i] + 2 * e0 * e1 * SigZ[i, j]
                + e1 * e1 * SigZ[j, j] + nv)

    best = None
    for a0 in np.linspace(0.15, 0.9, starts):
        r = minimize(val, np.array([a0, 0.1, -2.0]),
                     constraints=[{"type": "ineq",
                                   "fun": lambda p: Dk - dk(p)}],
                     method="SLSQP",
                     options={"maxiter": 2000, "ftol": 1e-14})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    return best / (2 * math.log(2))


def alloc_w(n, D, w, starts=3):
    SigZ, SigZcS = mode_covs(n)
    lamV, SY = mode_params(n)

    def tot(dv):
        return sum(Jw_mode(SigZ, SigZcS, n, k, dv[k], w)
                   for k in range(n))

    best = None
    for _ in range(starts):
        d0 = np.full(n, D) + rng.uniform(-0.02, 0.02, n)
        d0 = np.clip(d0, 1e-3, None)
        d0 *= D * n / d0.sum()
        r = minimize(tot, d0, constraints=[
            {"type": "eq", "fun": lambda dv: dv.mean() - D}],
            bounds=[(1e-4, float(SY[k]) * 3) for k in range(n)],
            method="SLSQP", options={"maxiter": 400, "ftol": 1e-12})
        if r.success and (best is None or r.fun < best[0]):
            best = (r.fun, r.x)
    return best[0] / n, best[1]


def full_w(n, D, w, warm_dv, starts=8):
    SigZ, SigZcS = mode_covs(n)
    tril = np.tril_indices(n)

    def unpack(p):
        A = p[:2 * n * n].reshape(n, 2 * n)
        L = np.zeros((n, n))
        L[tril] = p[2 * n * n:]
        for i in range(n):
            L[i, i] = math.exp(min(L[i, i], 15))
        return A, L @ L.T

    def obj(p):
        A, SN = unpack(p)
        M0 = A @ SigZ @ A.T + SN
        M1 = A @ SigZcS @ A.T + SN
        s0, l0 = np.linalg.slogdet(M0)
        s1, l1 = np.linalg.slogdet(M1)
        s2, ln = np.linalg.slogdet(SN)
        if s0 <= 0 or s1 <= 0 or s2 <= 0:
            return 90.0
        return (w * (l0 - ln) + (1 - w) * (l1 - ln)) / (2 * math.log(2) * n)

    def dist(p):
        A, SN = unpack(p)
        E = np.hstack([np.eye(n), np.zeros((n, n))]) - A
        return (np.trace(E @ SigZ @ E.T) + np.trace(SN)) / n

    # warm start from per-mode channels at warm_dv
    warmA = np.zeros((n, 2 * n))
    warm_sn = np.full(n, -2.0)
    for k in range(n):
        i, j = k, n + k

        def val(p, i=i, j=j):
            av, bv, nv = p[0], p[1], math.exp(min(p[2], 15))
            q0 = (av * av * SigZ[i, i] + 2 * av * bv * SigZ[i, j]
                  + bv * bv * SigZ[j, j])
            q1 = (av * av * SigZcS[i, i] + 2 * av * bv * SigZcS[i, j]
                  + bv * bv * SigZcS[j, j])
            if q0 + nv <= 0 or max(q1, 0) + nv <= 0:
                return 90.0
            return (w * math.log((q0 + nv) / nv)
                    + (1 - w) * math.log((max(q1, 0.0) + nv) / nv))

        def dkf(p, i=i, j=j):
            av, bv, nv = p[0], p[1], math.exp(min(p[2], 15))
            e0, e1 = 1 - av, -bv
            return (e0 * e0 * SigZ[i, i] + 2 * e0 * e1 * SigZ[i, j]
                    + e1 * e1 * SigZ[j, j] + nv)

        bk = None
        for a0 in (0.3, 0.6, 0.85):
            r = minimize(val, np.array([a0, 0.1, -2.0]),
                         constraints=[{"type": "ineq", "fun":
                                       lambda p: warm_dv[k] - dkf(p)}],
                         method="SLSQP",
                         options={"maxiter": 1500, "ftol": 1e-14})
            if r.success and (bk is None or r.fun < bk[0]):
                bk = (r.fun, r.x)
        if bk is not None:
            warmA[k, k], warmA[k, n + k] = bk[1][0], bk[1][1]
            warm_sn[k] = min(bk[1][2], 15)
    tri_diag = np.cumsum(np.arange(1, n + 1)) - 1
    warm_p = np.concatenate([warmA.ravel(), np.zeros(n * (n + 1) // 2)])
    warm_p[2 * n * n + tri_diag] = warm_sn

    best = None
    for i2 in range(starts + 1):
        if i2 == 0:
            p0 = warm_p
        else:
            A0 = np.hstack([np.diag(rng.uniform(0.3, 0.9, n)),
                            np.zeros((n, n))])
            p0 = np.concatenate([
                (A0 + rng.normal(0, 0.03, (n, 2 * n))).ravel(),
                rng.normal(-2.0, 0.3, n * (n + 1) // 2)])
        r = minimize(obj, p0, constraints=[
            {"type": "ineq", "fun": lambda p: D - dist(p)}],
            method="SLSQP", options={"maxiter": 4000, "ftol": 1e-13})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    return best


ok = True
n, D = 5, 0.3
allocs = {}
worst_gap = 0.0
for w in (0.5, 0.75):
    La, dv = alloc_w(n, D, w)
    Lf = full_w(n, D, w, dv)
    allocs[w] = (La, dv)
    worst_gap = max(worst_gap, abs(Lf - La))
vals["s1_worst_gap"] = worst_gap
verdicts["s1_decomposition"] = bool(worst_gap <= 2e-3)

SigZ, SigZcS = mode_covs(n)
lamV, SY = mode_params(n)
cvx = True
for k in (0, 2, 4):
    ds = np.linspace(0.05, min(2.5, 3 * SY[k]), 25)
    vs = [Jw_mode(SigZ, SigZcS, n, k, d, 0.5) for d in ds]
    cvx &= bool((np.diff(vs, 2) >= -1e-6).all())
La, dv = allocs[0.5]
h = 1e-4
slopes = [(Jw_mode(SigZ, SigZcS, n, k, dv[k] + h, 0.5)
           - Jw_mode(SigZ, SigZcS, n, k, dv[k] - h, 0.5)) / (2 * h)
          for k in range(n)]
vals["s2_spread"] = max(slopes) - min(slopes)
verdicts["s2_convex_slopes"] = bool(cvx and vals["s2_spread"] <= 5e-3)

La1, _ = alloc_w(n, D, 0.9999)
th_lo, th_hi = 1e-6, float(SY.max())
for _ in range(200):
    th = 0.5 * (th_lo + th_hi)
    if np.minimum(th, SY).mean() > D:
        th_hi = th
    else:
        th_lo = th
Lrwf = float(np.mean(0.5 * np.log2(np.maximum(SY / np.minimum(th, SY),
                                              1.0))))
vals["s3_rwf_dev"] = abs(La1 - Lrwf)


def gstar(r2, sv, Dv):
    A_, B_, C_ = Dv * sv, -(Dv + sv - r2), (1 - r2)
    return max((-B_ + math.sqrt(max(B_ * B_ - 4 * A_ * C_, 0)))
               / (2 * A_), 1.0)


La0, dv0 = alloc_w(n, D, 1e-6)
rho2m = rho * rho * lamV / SY
sm = 1 + tau2 / lamV
L070 = float(np.mean([0.5 * math.log2(
    gstar(rho2m[k], sm[k], min(dv0[k] / SY[k], 1.0)))
    for k in range(n)]))
vals["s3_w0_dev"] = abs(La0 - L070)
verdicts["s3_anchors"] = bool(vals["s3_rwf_dev"] <= 5e-3
                              and vals["s3_w0_dev"] <= 5e-3)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: float(v) for k, v in vals.items()},
           verdicts=verdicts, GO12WS_supported=bool(allpass))
print("===GO12WS-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
