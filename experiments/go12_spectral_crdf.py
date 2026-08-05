#!/usr/bin/env python
"""GO-P-2026-070 harness: the spectral conditional RDF (GO-12
Theorem 2-spectral, work endpoint, circulant embedding).

  s1  cross-mode decomposition: the FULL matrix program over all
      modes (n=6, record matrix 6x12 + full Sigma_N) equals the
      per-mode equal-slope allocation program
  s2  equal slopes at interior modes + per-mode convexity probe
  s3  n-sweep convergence (16/64/256) toward the frequency integral
  s4  anchors: tau2->inf = classical reverse water-filling of S_Y;
      n=1 = static Theorem 2

Sentinel ===GO12SP-JSON=== with ===END===; flag GO12SP_supported.
Pilot seed 20260930 / governed seed 20261001.
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
SEED = a_.seed if a_.seed is not None else (20260930 if a_.pilot
                                            else 20261001)
FAST, N_S1 = False, 6
verdicts = {}
vals = {}

rng = np.random.default_rng(SEED)
a, rho, tau2 = 0.8, 0.7, 0.4


def mode_params(n):
    """Real-DFT mode variances for circulant AR(1) V, plus derived
    static params per mode: (SY_k, rho_k^2, s_k)."""
    k = np.arange(n)
    SV = np.real(np.fft.ifft(
        1.0 / np.abs(1 - a * np.exp(-2j * np.pi * k / n)) ** 2))
    SV = SV / SV[0]                      # normalize Var V_t = 1
    lamV = np.real(np.fft.fft(SV))       # mode variances of V
    lamV = np.clip(lamV, 1e-9, None)
    SY = rho * rho * lamV + (1 - rho * rho)
    rho2 = rho * rho * lamV / SY         # corr^2(Ymode, Vmode)
    s = 1 + tau2 / lamV                  # context SNR per mode
    return lamV, SY, rho2, s


def gstar(rho2, s, D):
    A_, B_, C_ = D * s, -(D + s - rho2), (1 - rho2)
    disc = max(B_ * B_ - 4 * A_ * C_, 0.0)
    return max((-B_ + math.sqrt(disc)) / (2 * A_), 1.0)


def phi(rho2, s, SY, Dk):
    return 0.5 * math.log2(gstar(rho2, s, min(Dk / SY, 1.0)))


def gstar_vec(rho2, s, D):
    A_ = D * s
    B_ = -(D + s - rho2)
    C_ = 1 - rho2
    disc = np.maximum(B_ * B_ - 4 * A_ * C_, 0.0)
    return np.maximum((-B_ + np.sqrt(disc)) / (2 * A_), 1.0)


def phi_vec(rho2, s, SY, Dk):
    return 0.5 * np.log2(gstar_vec(rho2, s, np.minimum(Dk / SY, 1.0)))


def alloc_value(n, D):
    """Vectorized equal-slope allocation: per-mode slope inversion by
    array bisection, water level by outer bisection."""
    lamV, SY, rho2, s = mode_params(n)
    h = 1e-7

    def dphi_vec(d):
        return (phi_vec(rho2, s, SY, d + h)
                - phi_vec(rho2, s, SY, d - h)) / (2 * h)

    def Dk_of_slope(lam):
        lo = np.full(n, 1e-5) * SY
        hi = SY * (1 - 1e-9)
        sat_hi = dphi_vec(hi) + lam <= 0     # objective still falling
        sat_lo = dphi_vec(lo) + lam >= 0     # objective already rising
        a_, b_ = lo.copy(), hi.copy()
        for _ in range(80):
            m = 0.5 * (a_ + b_)
            g = dphi_vec(m) + lam
            a_ = np.where(g < 0, m, a_)
            b_ = np.where(g >= 0, m, b_)
        Dks = 0.5 * (a_ + b_)
        Dks[sat_hi] = SY[sat_hi]
        Dks[sat_lo] = lo[sat_lo]
        return Dks

    lo_l, hi_l = 1e-6, 50.0
    while Dk_of_slope(hi_l).mean() > D:
        hi_l *= 2
    for _ in range(90):
        mid = 0.5 * (lo_l + hi_l)
        if Dk_of_slope(mid).mean() > D:
            lo_l = mid
        else:
            hi_l = mid
    Dks = Dk_of_slope(0.5 * (lo_l + hi_l))
    # exact mean-D repair on interior modes (uniform shift, tiny)
    interior = (Dks > 1.1e-5 * SY) & (Dks < SY * (1 - 1e-6))
    if interior.any():
        Dks[interior] += (D - Dks.mean()) * n / interior.sum()
    val = float(phi_vec(rho2, s, SY, Dks).sum()) / n
    return val, Dks


def full_program(n, D, starts=10):
    """Full matrix program in mode coordinates WITHOUT assuming
    diagonality: record Yh = A z + noise, z = all 2n mode variables
    (Y-modes, V-modes), A n x 2n, Sigma_N n x n (Cholesky), minimize
    (1/n) I(T; Yh | S-modes)."""
    lamV, SY, rho2, s = mode_params(n)
    # covariance of z = (Ymodes, Vmodes): independent across k
    dY, dV = SY, lamV
    cYV = rho * lamV
    SigZ = np.zeros((2 * n, 2 * n))
    for k in range(n):
        SigZ[k, k] = dY[k]
        SigZ[n + k, n + k] = dV[k]
        SigZ[k, n + k] = SigZ[n + k, k] = cYV[k]
    # S-modes: SV-mode + tau2 (white in modes)
    SigS = np.diag(lamV + tau2)
    CzS = np.zeros((2 * n, n))
    for k in range(n):
        CzS[k, n - n + k] = rho * lamV[k]     # Cov(Ymode, Smode)
        CzS[n + k, k] = lamV[k]
    SigZcS = SigZ - CzS @ np.linalg.solve(SigS, CzS.T)
    npar = n * 2 * n + n * (n + 1) // 2
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
        M1 = A @ SigZcS @ A.T + SN
        sn, ld1 = np.linalg.slogdet(M1)
        if sn <= 0:
            return 90.0
        s2_, ldn = np.linalg.slogdet(SN)
        if s2_ <= 0:
            return 90.0
        return (ld1 - ldn) / (2 * math.log(2) * n)

    def dist(p):
        A, SN = unpack(p)
        # E|Ymodes - Yh|^2 / n ; Yh = A z + noise
        E = np.hstack([np.eye(n), np.zeros((n, n))]) - A
        return (np.trace(E @ SigZ @ E.T) + np.trace(SN)) / n

    best = None
    for _ in range(starts):
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
n, D = N_S1, 0.3
Lalloc, dv = alloc_value(n, D)
Lfull = full_program(n, D)
vals["s1_gap"] = abs(Lfull - Lalloc)
verdicts["s1_decomposition"] = bool(vals["s1_gap"] <= 2e-3)

lamV, SY, rho2, s_ = mode_params(n)
h = 1e-5
slopes = []
for k in range(n):
    if 1.1e-5 * SY[k] < dv[k] < SY[k] * (1 - 1e-6):
        sl = (phi(rho2[k], s_[k], SY[k], dv[k] + h)
              - phi(rho2[k], s_[k], SY[k], dv[k] - h)) / (2 * h)
        slopes.append(sl)
vals["s2_n_interior"] = len(slopes)
vals["s2_spread"] = (max(slopes) - min(slopes)) if len(slopes) > 1 else 0.0
cvx = True
for k in (0, n // 2, n - 1):
    ds = np.linspace(0.02 * SY[k], 0.98 * SY[k], 60)
    vs = [phi(rho2[k], s_[k], SY[k], d) for d in ds]
    cvx &= bool((np.diff(vs, 2) >= -1e-9).all())
verdicts["s2_slopes_convexity"] = bool(vals["s2_spread"] <= 1e-6 and cvx
                                       and len(slopes) >= 3)

v16, _ = alloc_value(16, D)
v64, _ = alloc_value(64, D)
v256, _ = alloc_value(256, D)
vals["s3_v"] = [v16, v64, v256]
vals["s3_c1"] = abs(v64 - v256)
verdicts["s3_convergence"] = bool(vals["s3_c1"] < abs(v16 - v64)
                                  and vals["s3_c1"] <= 1e-4)

tau2 = 1e9
Lbig, _ = alloc_value(64, D)
lamV, SY, _, _ = mode_params(64)
th_lo, th_hi = 1e-6, float(SY.max())
for _ in range(200):
    th = 0.5 * (th_lo + th_hi)
    if np.minimum(th, SY).mean() > D:
        th_hi = th
    else:
        th_lo = th
Lrwf = float(np.mean(0.5 * np.log2(np.maximum(SY / np.minimum(th, SY),
                                              1.0))))
vals["s4_rwf_dev"] = abs(Lbig - Lrwf)
tau2 = 0.4
L1, _ = alloc_value(1, D)
Lstat = 0.5 * math.log2(gstar(rho * rho, 1 + tau2, D))
vals["s4_static_dev"] = abs(L1 - Lstat)
verdicts["s4_anchors"] = bool(vals["s4_rwf_dev"] <= 1e-3
                              and vals["s4_static_dev"] <= 1e-9)

allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a_.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: (v if isinstance(v, list) else float(v))
                   for k, v in vals.items()},
           verdicts=verdicts, GO12SP_supported=bool(allpass))
print("===GO12SP-JSON===")
print(json.dumps(out, indent=1))
print("===END===")
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
