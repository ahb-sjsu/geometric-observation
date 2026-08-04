#!/usr/bin/env python
"""GO-P-2026-064 harness: numerical falsification net for GO-11 v0.10/v0.11
closing results:

  T9  (Thm. 9, the m=2 frontier system): matrix water levels -- FOC-N
      Sigma_N^{-1} = w M0^{-1} + (1-w) M1^{-1} + diag(mu) including the
      off-diagonal, per-mode 2x2 resolvents
      a_j = [Sigma_N^{-1} + (1-w)(lambda_j-1) M1^{-1}]^{-1} diag(mu) y_j,
      and the strengthened w=1 anchor (read-span record, mu_i = 1/D_i,
      error covariance diag(D)).
  T10 (Thm. 10, binary conditional CR function): the symmetric (d0,d1)
      family with the tilt equation ell(d0)-ell(d1) = 2(1-2q) ell(u),
      closed form L = h2(u) - (1-p)h2(d0) - p h2(d1), Fact-1 face
      R - L = 1 - h2(u), Gray and marginal anchors, and unconditional
      Lagrangian certificates against reproduction alphabets 2/4/6.
  X   (cross-net): Thm 10 retro-derives the 062 noisy-face discount
      (sealed artifact value 0.34324) as 1 - h2(1/6) = 0.34998 within
      the instrument-bias envelope measured on 062's explained face.

Single governed run. Sentinel ===GO11MB-JSON===; flag GO11MB_supported.
"""
import argparse
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import minimize, minimize_scalar

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a = ap.parse_args()
SEED = a.seed if a.seed is not None else (20260909 if a.pilot else 20260910)
rng = np.random.default_rng(SEED)

verdicts = {}
vals = {}


def h2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -(x * math.log2(x) + (1 - x) * math.log2(1 - x))


def ell(x):
    return math.log((1 - x) / x)


def conv(x, q):
    return x * (1 - q) + (1 - x) * q


# ----------------------------------------------------------------- T9 --
def whiten_m2(SigT, SigTcS):
    C = np.linalg.cholesky(SigT)
    Mi = np.linalg.inv(C)
    W = Mi @ SigTcS @ Mi.T
    lam, Q = np.linalg.eigh(W)
    Ytil = np.stack([Q.T @ C.T[:, 0], Q.T @ C.T[:, 1]])
    return np.clip(lam, 1e-12, 1.0), Ytil


def m2_opt(w, DA, DB, lam, Ytil, starts):
    dT = Ytil.shape[1]

    def unpack(p):
        A = p[:2 * dT].reshape(2, dT)
        Lc = np.array([[math.exp(min(p[2 * dT], 20)), 0],
                       [p[2 * dT + 1], math.exp(min(p[2 * dT + 2], 20))]])
        return A, Lc @ Lc.T

    def obj(p):
        A, SN = unpack(p)
        M0 = A @ A.T + SN
        M1 = A @ (lam[None, :] * A).T + SN
        dn, d0, d1 = (np.linalg.det(SN), np.linalg.det(M0),
                      np.linalg.det(M1))
        if dn <= 1e-280 or d0 <= 1e-280 or d1 <= 1e-280:
            return 90.0
        return w * math.log(d0 / dn) + (1 - w) * math.log(d1 / dn)

    cons = [
        {"type": "ineq", "fun": lambda p: DA - (
            float((Ytil[0] - unpack(p)[0][0]) @ (Ytil[0] - unpack(p)[0][0]))
            + unpack(p)[1][0, 0])},
        {"type": "ineq", "fun": lambda p: DB - (
            float((Ytil[1] - unpack(p)[0][1]) @ (Ytil[1] - unpack(p)[0][1]))
            + unpack(p)[1][1, 1])}]
    best, bp = None, None
    for _ in range(starts):
        p0 = np.concatenate([
            (Ytil * rng.uniform(0.3, 0.9)).ravel()
            + rng.normal(0, 0.06, 2 * dT),
            [math.log(rng.uniform(5e-3, 0.3)), rng.uniform(-0.1, 0.1),
             math.log(rng.uniform(5e-3, 0.3))]])
        r = minimize(obj, p0, constraints=cons, method="SLSQP",
                     options={"maxiter": 3000, "ftol": 1e-15})
        if r.success and (best is None or r.fun < best):
            best, bp = r.fun, r.x
    if bp is None:
        return None
    return unpack(bp)


def t9_checks(w, A, SN, lam, Ytil):
    M0 = A @ A.T + SN
    M1 = A @ (lam[None, :] * A).T + SN
    SNi, M0i, M1i = (np.linalg.inv(SN), np.linalg.inv(M0),
                     np.linalg.inv(M1))
    K = SNi - w * M0i - (1 - w) * M1i
    mu = np.diag(K).copy()
    off = abs(K[0, 1])
    col = 0.0
    for j in range(Ytil.shape[1]):
        Rj = np.linalg.inv(SNi + (1 - w) * (lam[j] - 1) * M1i)
        col = max(col, float(np.max(np.abs(
            A[:, j] - Rj @ (mu * Ytil[:, j])))))
    return off, col, mu


T9_INST = [(0.3, 0.7, 0.2, 0.4, 0.2, 0.2),
           (0.45, 0.55, -0.25, 0.8, 0.12, 0.30)]
worst_off, worst_col, miss = 0.0, 0.0, 0
for rAB, rAV, rBV, t, DA, DB in T9_INST:
    SigT = np.array([[1, rAB, rAV], [rAB, 1, rBV], [rAV, rBV, 1.0]])
    cts = SigT[:, 2:3]
    SigTcS = SigT - cts @ cts.T / (1 + t)
    lam, Ytil = whiten_m2(SigT, SigTcS)
    for w in (0.0, 0.5, 1.0):
        out = m2_opt(w, DA, DB, lam, Ytil, starts=50)
        if out is None:
            miss += 1
            continue
        off, col, mu = t9_checks(w, *out, lam, Ytil)
        worst_off, worst_col = max(worst_off, off), max(worst_col, col)
# r=2 vector-context instance
SigT = np.eye(4)
SigT[0, 1] = SigT[1, 0] = 0.25
SigT[0, 2] = SigT[2, 0] = 0.6
SigT[1, 3] = SigT[3, 1] = 0.5
SigT[0, 3] = SigT[3, 0] = 0.15
G = np.zeros((4, 2))
G[2, 0] = G[3, 1] = 1.0
x = SigT @ G
SigTcS = SigT - x @ np.linalg.solve(G.T @ SigT @ G + np.diag([0.4, 0.7]),
                                    x.T)
lam4, Ytil4 = whiten_m2(SigT, SigTcS)
for w in (0.0, 0.5):
    out = m2_opt(w, 0.25, 0.25, lam4, Ytil4, starts=60)
    if out is None:
        miss += 1
        continue
    off, col, mu = t9_checks(w, *out, lam4, Ytil4)
    worst_off, worst_col = max(worst_off, off), max(worst_col, col)

vals["s1_focn_offdiag"] = worst_off
vals["s1_permode_col"] = worst_col
vals["s1_solver_misses"] = miss
verdicts["s1_m2sys"] = bool(worst_off <= 5e-4 and worst_col <= 5e-4
                            and miss == 0)

# w=1 strengthened anchor, ASYMMETRIC distortions
SigT = np.array([[1, 0.3, 0.7], [0.3, 1, 0.2], [0.7, 0.2, 1.0]])
cts = SigT[:, 2:3]
lam, Ytil = whiten_m2(SigT, SigT - cts @ cts.T / 1.4)
DA, DB = 0.15, 0.35
A, SN = m2_opt(1.0, DA, DB, lam, Ytil, starts=50)
M0 = A @ A.T + SN
mu = np.diag(np.linalg.inv(SN) - np.linalg.inv(M0))
E = Ytil - A
EC = E @ E.T + SN
vals["s2_readspan"] = float(np.max(np.abs(A - SN @ np.diag(mu) @ Ytil)))
vals["s2_muD"] = float(max(abs(mu[0] * DA - 1), abs(mu[1] * DB - 1)))
vals["s2_errcov_offdiag"] = abs(float(EC[0, 1]))
vals["s2_errcov_diag"] = float(max(abs(EC[0, 0] - DA), abs(EC[1, 1] - DB)))
verdicts["s2_w1_anchor"] = bool(
    vals["s2_readspan"] <= 5e-4 and vals["s2_muD"] <= 2e-3
    and vals["s2_errcov_offdiag"] <= 2e-3 and vals["s2_errcov_diag"] <= 2e-3)


# ---------------------------------------------------------------- T10 --
def joint_L(C, p, q):
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    Pyv = np.array([(1 - p) / 2 if y == v else p / 2 for y, v in states])
    K = C.shape[1]
    dec = np.arange(K) % 2
    Ps_v = {0: {0: 1 - q, 1: q}, 1: {0: q, 1: 1 - q}}
    HYh_YV = 0.0
    for i in range(4):
        HYh_YV += Pyv[i] * sum(-C[i, k] * math.log2(C[i, k])
                               for k in range(K) if C[i, k] > 1e-300)
    Psy = np.zeros((2, K))
    for i, (y, v) in enumerate(states):
        for s in (0, 1):
            Psy[s] += Pyv[i] * Ps_v[v][s] * C[i]
    Ps = Psy.sum(axis=1)
    HYh_S = sum(-Psy[s, k] * math.log2(Psy[s, k] / Ps[s])
                for s in (0, 1) for k in range(K) if Psy[s, k] > 1e-300)
    Pyh = Psy.sum(axis=0)
    HYh = sum(-x * math.log2(x) for x in Pyh if x > 1e-300)
    dist = sum(Pyv[i] * sum(C[i, k] for k in range(K)
                            if dec[k] != states[i][0]) for i in range(4))
    return HYh_S - HYh_YV, HYh - HYh_YV, dist


def fam_L(d0, p, q, D):
    d1 = (D - (1 - p) * d0) / p
    a = (1 - p) * d0 + p * (1 - d1)
    u = conv(a, q)
    return h2(u) - (1 - p) * h2(d0) - p * h2(d1), d1, u


def opt_family(p, q, D):
    lo = max(0.0, (D - p) / (1 - p)) + 1e-12
    hi = min(1.0, D / (1 - p)) - 1e-12
    r = minimize_scalar(lambda d0: fam_L(d0, p, q, D)[0], bounds=(lo, hi),
                        method="bounded", options={"xatol": 1e-13})
    L, d1, u = fam_L(r.x, p, q, D)
    return L, r.x, d1, u


def lagr_cert(p, q, D, Lfam, K, starts):
    eps = 1e-5
    beta = -(opt_family(p, q, D + eps)[0]
             - opt_family(p, q, D - eps)[0]) / (2 * eps)

    def unpack(x):
        Z = x.reshape(4, K)
        Ez = np.exp(Z - Z.max(axis=1, keepdims=True))
        return Ez / Ez.sum(axis=1, keepdims=True)

    def F(x):
        L, _, d = joint_L(unpack(x), p, q)
        return L + beta * d

    Fmin = None
    for _ in range(starts):
        r = minimize(F, rng.normal(0, 2.0, 4 * K), method="BFGS",
                     options={"maxiter": 2000, "gtol": 1e-12})
        if Fmin is None or r.fun < Fmin:
            Fmin = r.fun
    return Fmin - (Lfam + beta * D)


T10_INST = [(0.15, 0.1, 0.05), (0.25, 0.2, 0.1), (0.3, 0.05, 0.12),
            (0.2, 0.35, 0.08)]
worst_tilt, worst_f1, worst_cf = 0.0, 0.0, 0.0
for p, q, D in T10_INST:
    Lf, d0, d1, u = opt_family(p, q, D)
    worst_tilt = max(worst_tilt,
                     abs(ell(d0) - ell(d1) - 2 * (1 - 2 * q) * ell(u)))
    C = np.array([[1 - d0, d0], [1 - d1, d1], [d1, 1 - d1],
                  [d0, 1 - d0]])
    Lc, Rc, dc = joint_L(C, p, q)
    worst_f1 = max(worst_f1, abs((Rc - Lc) - (1 - h2(u))))
    worst_cf = max(worst_cf, abs(Lc - Lf), abs(dc - D))
vals["s3_tilt"] = worst_tilt
vals["s3_fact1"] = worst_f1
vals["s3_closedform"] = worst_cf
verdicts["s3_bin_family"] = bool(worst_tilt <= 2e-5 and worst_f1 <= 1e-10
                                 and worst_cf <= 1e-9)

# certificates: K=2,4 at all four instances; K=6 at one
worst_cert = 0.0
for p, q, D in T10_INST:
    Lf = opt_family(p, q, D)[0]
    worst_cert = max(worst_cert, abs(lagr_cert(p, q, D, Lf, K=2, starts=40)),
                     abs(lagr_cert(p, q, D, Lf, K=4, starts=50)))
worst_cert6 = abs(lagr_cert(0.25, 0.2, 0.1, opt_family(0.25, 0.2, 0.1)[0],
                            K=6, starts=80))
vals["s4_cert24"] = worst_cert
vals["s4_cert6"] = worst_cert6
verdicts["s4_bin_cert"] = bool(worst_cert <= 1e-6 and worst_cert6 <= 1e-6)

# anchors + monotonicity
p, D = 0.25, 0.1
Lg = opt_family(p, 0.0, D)[0]
Lh, _, d1h, _ = opt_family(p, 0.5, D)
d0h = opt_family(p, 0.5, D)[1]
Ls = [opt_family(p, qq, D)[0] for qq in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)]
vals["s5_gray"] = abs(Lg - (h2(p) - h2(D)))
vals["s5_marg"] = abs(Lh - (1 - h2(D)))
vals["s5_dd"] = float(max(abs(d0h - D), abs(d1h - D)))
mono = all(Ls[i] <= Ls[i + 1] + 1e-12 for i in range(5))
verdicts["s5_bin_anchors"] = bool(vals["s5_gray"] <= 1e-8
                                  and vals["s5_marg"] <= 1e-8
                                  and vals["s5_dd"] <= 1e-5 and mono)

# cross-net: 062 noisy face retro-derivation
derived_noisy = 1 - h2(conv(1.0 / 12.0, 0.1))
derived_clean = 1 - h2(1.0 / 12.0)
MEAS_NOISY, MEAS_CLEAN = 0.34323891625615766, 0.5781779406464015
bias_clean = MEAS_CLEAN - derived_clean
bias_noisy = MEAS_NOISY - derived_noisy
vals["s6_derived_noisy"] = derived_noisy
vals["s6_bias_noisy"] = bias_noisy
vals["s6_bias_clean"] = bias_clean
verdicts["s6_062_crossnet"] = bool(
    abs(bias_noisy) <= 0.015 and abs(bias_noisy - bias_clean) <= 0.008)

# ------------------------------------------------------------- verdict --
allpass = all(verdicts.values())
out = dict(seed=SEED, pilot=bool(a.pilot),
           runtime_s=round(time.time() - t0, 1),
           values={k: (float(v) if isinstance(v, (int, float, np.floating))
                       else v) for k, v in vals.items()},
           verdicts=verdicts, GO11MB_supported=bool(allpass))
print("===GO11MB-JSON===")
print(json.dumps(out, indent=1))
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")
sys.exit(0 if allpass else 1)
