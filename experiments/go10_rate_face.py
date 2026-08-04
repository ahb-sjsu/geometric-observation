# GO-10 rate face -- EXPLORATORY, UNREGISTERED (decision 2026-08-04): the
# theta-geometry of the complementarity tax's RATE coordinate, measured as
# operational codebook rates at matched distortion.  Not sealed, not
# ledger-bearing, class at most [exploratory]: the predictions are the
# ATTRIBUTED rate theory (Gray 1973 / Xiao-Luo 2005 after the read-plane
# reduction; see paper/complementarity-tax-NOVELTY.md), and the C3 harness
# GO-P-2026-055 already verified the geometry exactly at the information
# level (SDP = closed form to <1e-7 bits across the sweep).  What this adds
# is instrument physics only: whether finite-n random-codebook covering
# losses cancel in rate DIFFERENCES, so the measured tax tracks sin^2(theta).
# GO-10's class ([replicated], via the work side on two families) does not
# ride on this file.
#
# Two consumers read a 2-D white Gaussian source through unit vectors u = e1
# and v = (cos t, sin t).  For each angle t, nested random codebooks measure:
#   R_single_op : minimal rate for a scalar codebook on the projection to
#                 reach mean-squared distortion D  (theta-independent),
#   R_joint_op(t): minimal rate for a 2-D codebook, codewords drawn from the
#                 max-det program's optimal reproduction N(0, I - Sigma0(t,D)),
#                 encoder = min over codewords of max(d_A, d_B), to reach
#                 max(mean d_A, mean d_B) <= D,
#   CT_op(t)    = R_joint_op(t) - R_single_op.
# Reference values:
#   on-regime (D <= 1 - cos t):  CT_pred(t) = 1/2 log2(sin^2 t / D)
#   off-regime (t = 30 deg here): CT_pred = R_AB(SDP) - 1/2 log2(1/D)
#   aligned control (t = 0, v = u exactly): CT_pred = 0.
# Finite-n covering loss is an additive offset shared across t, so the
# informative comparison is INCREMENTS between angles (offsets cancel); the
# collapse control and the monotone chain carry the absolute content.
#
# Nested-prefix instrument: one top-size codebook per (t); per block, the
# running min of the encode objective over codeword prefixes 2^k gives the
# exact distortion-vs-rate curve for nested codebooks at every k in one pass.
# Rate resolution = 1/n bits/symbol (0.125 at n = 8).
#
# Usage: python go10_rate_face.py [--pilot]   (seeds 20260823 / 20260824)
# Output: sentinel JSON ===GO10RF-JSON===.  CPU; numpy + scipy (SDP).  MIT.
import argparse
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import minimize

DT = 0.25
N_BLK = 8
T_PILOT, T_GOV = 200, 400
THETAS = [0, 30, 45, 60, 75, 90]        # 0 = aligned collapse control (v = u)
ONREG = [45, 60, 75, 90]                # D <= 1 - cos t holds
K_SINGLE = (4, 14)                      # prefix exponents: rates 0.5 .. 1.75
K_JOINT = (6, 22)                       # rates 0.75 .. 2.75


def sigma0(theta_deg, D, rng, restarts=12):
    """Optimal error covariance of the joint program (max det Sigma s.t.
    Sigma <= I, u'Su <= D, v'Sv <= D); None on solver non-convergence."""
    th = math.radians(theta_deg)
    u = np.array([1.0, 0.0])
    v = np.array([math.cos(th), math.sin(th)])

    def mat(p):
        return np.array([[p[0], p[2]], [p[2], p[1]]])

    def negobj(p):
        sign, ld = np.linalg.slogdet(mat(p))
        return 1e6 if sign <= 0 else -ld

    cons = [
        {"type": "ineq", "fun": lambda p: np.linalg.eigvalsh(mat(p))[0]},
        {"type": "ineq", "fun": lambda p: np.linalg.eigvalsh(np.eye(2) - mat(p))[0]},
        {"type": "ineq", "fun": lambda p: D - u @ mat(p) @ u},
        {"type": "ineq", "fun": lambda p: D - v @ mat(p) @ v},
    ]
    best, bp = None, None
    for _ in range(restarts):
        x0 = np.array([rng.uniform(0.01, 0.5), rng.uniform(0.01, 0.5),
                       rng.uniform(-0.1, 0.1)])
        r = minimize(negobj, x0, constraints=cons, method="SLSQP",
                     options={"maxiter": 600, "ftol": 1e-12})
        if r.success and (best is None or r.fun < best):
            best, bp = r.fun, r.x
    if bp is None:
        return None, None
    S0 = np.array([[bp[0], bp[2]], [bp[2], bp[1]]])
    return S0, -0.5 * math.log2(np.linalg.det(S0))


def rate_at_D(klo, khi, n, dcurve, D):
    """Interpolated rate (bits/symbol) where the distortion curve crosses D.
    dcurve[i] = distortion of the prefix codebook 2^(klo+i); decreasing."""
    rates = [(k) / n for k in range(klo, khi + 1)]
    for i, d in enumerate(dcurve):
        if d <= D:
            if i == 0:
                return rates[0]
            d0, d1 = dcurve[i - 1], d
            if d0 <= d1:
                return rates[i]
            f = (d0 - D) / (d0 - d1)
            return rates[i - 1] + f * (rates[i] - rates[i - 1])
    return float("nan")


def single_rate(rng, n, T, kmax, klo, D):
    """Scalar-source operational rate: nested codebook on Y ~ N(0,1)."""
    Y = rng.normal(0, 1, size=(T, n)).astype(np.float32)
    C = rng.normal(0, math.sqrt(1 - D), size=(1 << kmax, n)).astype(np.float32)
    csq = (C * C).sum(1)
    curve = np.zeros(kmax - klo + 1)
    for t in range(T):
        d = (csq - 2.0 * (C @ Y[t]) + float(Y[t] @ Y[t])) / n
        run = np.minimum.accumulate(d)
        curve += run[(1 << np.arange(klo, kmax + 1)) - 1]
    curve /= T
    return rate_at_D(klo, kmax, n, curve, D), curve


def joint_rate(rng, n, T, kmax, klo, D, theta_deg, S0):
    """2-D joint operational rate at angle theta; encoder min max(dA,dB)."""
    th = math.radians(theta_deg)
    u = np.array([1.0, 0.0], dtype=np.float32)
    v = np.array([math.cos(th), math.sin(th)], dtype=np.float32)
    X = rng.normal(0, 1, size=(T, n, 2)).astype(np.float32)
    Crep = np.eye(2) - S0                        # optimal reproduction cov
    L = np.linalg.cholesky(Crep + 1e-12 * np.eye(2)).astype(np.float32)
    C = rng.normal(0, 1, size=(1 << kmax, n, 2)).astype(np.float32) @ L.T
    Cu = C @ u                                   # (Ncw, n) projections
    Cv = C @ v
    cusq = (Cu * Cu).sum(1)
    cvsq = (Cv * Cv).sum(1)
    ks = (1 << np.arange(klo, kmax + 1)) - 1
    curveA = np.zeros(kmax - klo + 1)
    curveB = np.zeros(kmax - klo + 1)
    for t in range(T):
        yu = X[t] @ u
        yv = X[t] @ v
        dA = (cusq - 2.0 * (Cu @ yu) + float(yu @ yu)) / n
        dB = (cvsq - 2.0 * (Cv @ yv) + float(yv @ yv)) / n
        obj = np.maximum(dA, dB)
        # running min of the objective over nested prefixes, and the index of
        # a codeword achieving it (last achiever; distortion-equivalent to
        # the first under float scores, and deterministic)
        best = np.minimum.accumulate(obj)
        newmin = obj <= best
        run_idx = np.maximum.accumulate(np.where(newmin, np.arange(obj.size), -1))
        sel = run_idx[ks]
        curveA += dA[sel]
        curveB += dB[sel]
    curveA /= T
    curveB /= T
    rate = rate_at_D(klo, kmax, n, np.maximum(curveA, curveB), D)
    return rate, curveA, curveB


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    a = ap.parse_args()
    SEED = 20260823 if a.pilot else 20260824
    rng = np.random.default_rng(SEED)
    n, T = N_BLK, (T_PILOT if a.pilot else T_GOV)
    print(f"GO-10 rate face -- EXPLORATORY run (unregistered)")
    print(f"seed={SEED} n={n} T={T} D={DT} thetas={THETAS} "
          f"grid step={1/n:.3f} b/sym", flush=True)
    t0 = time.time()

    Rs, _ = single_rate(rng, n, T, K_SINGLE[1], K_SINGLE[0], DT)
    Rs2, _ = single_rate(rng, n, T, K_SINGLE[1], K_SINGLE[0], DT)
    print(f"  singles: R_A_op={Rs:.4f}  R_B_op={Rs2:.4f}  "
          f"(Shannon 1.0000)  ({time.time()-t0:.0f}s)", flush=True)

    out = dict(seed=SEED, pilot=bool(a.pilot), exploratory=True, n=n,
               trials=T, D=DT, R_single_op=[Rs, Rs2], thetas={})
    miss = False
    CT = {}
    for th in THETAS:
        if th == 0:
            # aligned control (v = u): the joint program degenerates to the
            # scalar one; optimal error covariance is diag(D, 1)
            S0 = np.array([[DT, 0.0], [0.0, 1.0]])
            Rab_pred = 0.5 * math.log2(1 / DT)
        else:
            S0, Rab_pred = sigma0(th, DT, rng)
            if S0 is None:
                miss = True
                continue
        Rj, cA, cB = joint_rate(rng, n, T, K_JOINT[1], K_JOINT[0], DT, th, S0)
        CT[th] = Rj - max(Rs, Rs2)
        ct_pred = Rab_pred - 0.5 * math.log2(1 / DT)
        out["thetas"][str(th)] = dict(
            R_joint_op=Rj, CT_op=CT[th], CT_pred=ct_pred,
            R_ab_pred=Rab_pred)
        print(f"  theta={th:3d}: R_joint_op={Rj:.4f}  CT_op={CT[th]:.4f}  "
              f"CT_pred={ct_pred:.4f}  ({time.time()-t0:.0f}s)", flush=True)

    # descriptive checks (NOT sealed gates -- exploratory)
    checks = {}
    if not miss and all(th in CT for th in THETAS):
        g = out["thetas"]
        exc = max(Rs, Rs2) - 1.0
        checks["singles_agree"] = bool(abs(Rs - Rs2) <= 0.10)
        checks["covering_excess"] = float(exc)
        incs = {th: (CT[th] - CT[45])
                - (g[str(th)]["CT_pred"] - g["45"]["CT_pred"])
                for th in (30, 60, 75, 90)}
        checks["increment_residuals_vs_45"] = {str(k): float(v)
                                               for k, v in incs.items()}
        checks["aligned_collapse_CT0"] = float(CT[0])
        checks["monotone"] = bool(
            CT[0] < CT[30] < CT[45] < CT[60] < CT[75] < CT[90])
    out["checks"] = checks
    out["instrumentation_miss"] = bool(miss)
    out["seconds_total"] = round(time.time() - t0, 1)
    print(f"\nCT_op: " + "  ".join(f"{th}:{CT.get(th, float('nan')):.3f}"
                                   for th in THETAS))
    print(f"checks: {checks}")
    print("===GO10RF-JSON===")
    print(json.dumps(out, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
