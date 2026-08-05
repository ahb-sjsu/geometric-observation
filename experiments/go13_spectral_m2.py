#!/usr/bin/env python
"""GO-P-2026-073 harness: the spectral m=2 theorem (GO-13 Thm 4).
s1 full cross-mode program (n=3, 2n-row records) vs the two-price
per-mode Theorem-9 allocation; s2 two common prices (per-consumer
equal slopes across modes); s3 n=1 static anchor.
Sentinel ===GO13SM-JSON=== with ===END===; flag GO13SM_supported.
Pilot seed 20261009 / governed seed 20261010."""
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
SEED = a_.seed if a_.seed is not None else (20261009 if a_.pilot
                                            else 20261010)
verdicts = {}
vals = {}
import math
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(SEED)
aP, rAB, rAV, rBV, tau2, W = 0.8, 0.3, 0.7, 0.2, 0.4, 0.5
DA, DB = 0.25, 0.25


def lam_modes(n):
    k = np.arange(n)
    SV = np.real(np.fft.ifft(
        1.0 / np.abs(1 - aP * np.exp(-2j * np.pi * k / n)) ** 2))
    SV = SV / SV[0]
    return np.clip(np.real(np.fft.fft(SV)), 1e-9, None)


def mode_cov(lam):
    SA = rAV * rAV * lam + (1 - rAV * rAV)
    SB = rBV * rBV * lam + (1 - rBV * rBV)
    cAB = (rAB - rAV * rBV) + rAV * rBV * lam
    SigT = np.array([[SA, cAB, rAV * lam],
                     [cAB, SB, rBV * lam],
                     [rAV * lam, rBV * lam, lam]])
    ck = SigT[:, 2]
    SigTc = SigT - np.outer(ck, ck) / (lam + tau2)
    return SigT, SigTc


def m2_mode(SigT, SigTc, dA, dB, starts=25):
    """Thm-9 weighted program at one mode (record 2x3 + SN 2x2)."""
    def unpack(p):
        A = p[:6].reshape(2, 3)
        Lc = np.array([[math.exp(min(p[6], 15)), 0],
                       [p[7], math.exp(min(p[8], 15))]])
        return A, Lc @ Lc.T

    def obj(p):
        A, SN = unpack(p)
        M0 = A @ SigT @ A.T + SN
        M1 = A @ SigTc @ A.T + SN
        s0, l0 = np.linalg.slogdet(M0)
        s1, l1 = np.linalg.slogdet(M1)
        s2, ln = np.linalg.slogdet(SN)
        if s0 <= 0 or s1 <= 0 or s2 <= 0:
            return 90.0
        return W * (l0 - ln) + (1 - W) * (l1 - ln)

    cons = []
    for i, Dv in ((0, dA), (1, dB)):
        def c(p, i=i, Dv=Dv):
            A, SN = unpack(p)
            e = np.eye(3)[i] - A[i]
            return Dv - (float(e @ SigT @ e) + SN[i, i])
        cons.append({"type": "ineq", "fun": c})
    best, bp = None, None
    for _ in range(starts):
        p0 = np.concatenate([
            (np.eye(2, 3) * rng.uniform(0.3, 0.9)).ravel()
            + rng.normal(0, 0.05, 6),
            [math.log(rng.uniform(5e-3, 0.3)), rng.uniform(-0.1, 0.1),
             math.log(rng.uniform(5e-3, 0.3))]])
        r = minimize(obj, p0, constraints=cons, method="SLSQP",
                     options={"maxiter": 3000, "ftol": 1e-14})
        if r.success and (best is None or r.fun < best):
            best, bp = r.fun, r.x
    return best / (2 * math.log(2)), bp


def alloc(n, starts=3):
    lam = lam_modes(n)
    covs = [mode_cov(lam[k]) for k in range(n)]

    def tot(dv):
        return sum(m2_mode(covs[k][0], covs[k][1], dv[k], dv[n + k],
                           starts=12)[0] for k in range(n))

    best = None
    for _ in range(starts):
        d0 = np.concatenate([np.full(n, DA), np.full(n, DB)])
        d0 += rng.uniform(-0.02, 0.02, 2 * n)
        d0[:n] *= DA * n / d0[:n].sum()
        d0[n:] *= DB * n / d0[n:].sum()
        r = minimize(tot, d0, constraints=[
            {"type": "eq", "fun": lambda dv: dv[:n].mean() - DA},
            {"type": "eq", "fun": lambda dv: dv[n:].mean() - DB}],
            bounds=[(5e-3, 3.0)] * (2 * n),
            method="SLSQP", options={"maxiter": 200, "ftol": 1e-11})
        if r.success and (best is None or r.fun < best[0]):
            best = (r.fun, r.x)
    return best[0] / n, best[1]


def full(n, warm_dv, starts=8):
    lam = lam_modes(n)
    covs = [mode_cov(lam[k]) for k in range(n)]
    ZT = np.zeros((3 * n, 3 * n))
    ZTc = np.zeros((3 * n, 3 * n))
    for k in range(n):
        idx = [k, n + k, 2 * n + k]
        for i2 in range(3):
            for j2 in range(3):
                ZT[idx[i2], idx[j2]] = covs[k][0][i2, j2]
                ZTc[idx[i2], idx[j2]] = covs[k][1][i2, j2]
    m = 2 * n
    tril = np.tril_indices(m)

    def unpack(p):
        A = p[:m * 3 * n].reshape(m, 3 * n)
        L = np.zeros((m, m))
        L[tril] = p[m * 3 * n:]
        for i2 in range(m):
            L[i2, i2] = math.exp(min(L[i2, i2], 15))
        return A, L @ L.T

    def obj(p):
        A, SN = unpack(p)
        M0 = A @ ZT @ A.T + SN
        M1 = A @ ZTc @ A.T + SN
        s0, l0 = np.linalg.slogdet(M0)
        s1, l1 = np.linalg.slogdet(M1)
        s2, ln = np.linalg.slogdet(SN)
        if s0 <= 0 or s1 <= 0 or s2 <= 0:
            return 90.0
        return (W * (l0 - ln) + (1 - W) * (l1 - ln)) / (2 * math.log(2) * n)

    def dA_(p):
        A, SN = unpack(p)
        tot = 0.0
        for k in range(n):
            e = np.zeros(3 * n)
            e[k] = 1.0
            e -= A[k]
            tot += float(e @ ZT @ e) + SN[k, k]
        return tot / n

    def dB_(p):
        A, SN = unpack(p)
        tot = 0.0
        for k in range(n):
            e = np.zeros(3 * n)
            e[n + k] = 1.0
            e -= A[n + k]
            tot += float(e @ ZT @ e) + SN[n + k, n + k]
        return tot / n

    # warm start from per-mode optima at warm_dv
    warmA = np.zeros((m, 3 * n))
    warm_sn = np.full(m, -2.0)
    for k in range(n):
        _, bp = m2_mode(covs[k][0], covs[k][1], warm_dv[k],
                        warm_dv[n + k], starts=25)
        Ak = bp[:6].reshape(2, 3)
        for i2 in range(2):
            row = k if i2 == 0 else n + k
            warmA[row, k] = Ak[i2, 0]
            warmA[row, n + k] = Ak[i2, 1]
            warmA[row, 2 * n + k] = Ak[i2, 2]
        warm_sn[k] = bp[6]
        warm_sn[n + k] = bp[8]
    tri_diag = np.cumsum(np.arange(1, m + 1)) - 1
    warm_p = np.concatenate([warmA.ravel(),
                             np.zeros(m * (m + 1) // 2)])
    warm_p[m * 3 * n + tri_diag] = warm_sn

    best = None
    for i3 in range(starts + 1):
        if i3 == 0:
            p0 = warm_p
        else:
            p0 = np.concatenate([
                (warmA + rng.normal(0, 0.03, warmA.shape)).ravel(),
                rng.normal(-2.0, 0.3, m * (m + 1) // 2)])
        r = minimize(obj, p0, constraints=[
            {"type": "ineq", "fun": lambda p: DA - dA_(p)},
            {"type": "ineq", "fun": lambda p: DB - dB_(p)}],
            method="SLSQP", options={"maxiter": 5000, "ftol": 1e-13})
        if r.success and (best is None or r.fun < best):
            best = r.fun
    return best


ok = True
n = 3
La, dv = alloc(n)
Lf = full(n, dv)
vals["s1_gap"] = abs(Lf - La)
verdicts["s1_decomposition"] = bool(vals["s1_gap"] <= 3e-3)

lam = lam_modes(n)
covs = [mode_cov(lam[k]) for k in range(n)]
h = 2e-4
muA, muB = [], []
for k in range(n):
    vp = m2_mode(covs[k][0], covs[k][1], dv[k] + h, dv[n + k],
                 starts=15)[0]
    vm = m2_mode(covs[k][0], covs[k][1], dv[k] - h, dv[n + k],
                 starts=15)[0]
    muA.append((vp - vm) / (2 * h))
    vp = m2_mode(covs[k][0], covs[k][1], dv[k], dv[n + k] + h,
                 starts=15)[0]
    vm = m2_mode(covs[k][0], covs[k][1], dv[k], dv[n + k] - h,
                 starts=15)[0]
    muB.append((vp - vm) / (2 * h))
vals["s2_spreadA"] = max(muA) - min(muA)
vals["s2_spreadB"] = max(muB) - min(muB)
vals["s2_muA"] = float(np.mean(muA))
vals["s2_muB"] = float(np.mean(muB))
vals["s2_price_gap"] = abs(vals["s2_muA"] - vals["s2_muB"])
verdicts["s2_two_prices"] = bool(vals["s2_spreadA"] <= 2e-2
                                 and vals["s2_spreadB"] <= 2e-2
                                 and vals["s2_price_gap"] >= 0.02)

La1, _ = alloc(1)
SigT1, SigTc1 = mode_cov(lam_modes(1)[0])
Ls, _ = m2_mode(SigT1, SigTc1, DA, DB, starts=40)
vals["s3_anchor_dev"] = abs(La1 - Ls)
verdicts["s3_anchor"] = bool(vals["s3_anchor_dev"] <= 1e-6)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: float(v) for k, v in vals.items()},
           verdicts=verdicts, GO13SM_supported=bool(allpass))
print("===GO13SM-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
