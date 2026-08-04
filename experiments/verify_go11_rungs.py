# Numerical falsification harness for GO-11 v0.9's closing theorems
# (GO-P-2026-063; paper/go11-conditional-region.tex v0.9). Claims netted:
#   T7 (Thm 7, vector S solved): whitened two-water-level system with
#       per-mode closed form
#         u = (1 - a*g0 - (1-a)*g1) [(1-(1-a)g1) I + (1-a) g1 Lambda]^{-1} y0,
#       g0 = n/(|u|^2+n), g1 = n/(u'Lambda u+n); Thm 3 = r=1 case;
#       converse via the dimension-free moment identities.
#   T8 (Thm 8, higher-rank reads): k x (k+r) matrix program; EXACT
#       per-mode decomposition under simultaneous block-diagonality;
#       misalignment strictly better than forced decomposition.
#   U  (Proposition, interior-alpha uniqueness): the weighted objective is
#       convex on the active slice (netted: Hessian positivity probes;
#       (g0,g1) fixed-point root hunts find exactly one root; multi-start
#       dispersion nil).
# Sections [1]-[6] implement prereg GO-P-2026-063 s1-s6 with sealed bars.
# numpy + scipy; Tier A (single run, ~4 min).
#   python verify_go11_rungs.py           -> GOVERNED seed 20260906
#   python verify_go11_rungs.py --pilot   -> logged pilot seed 20260905
# SLSQP non-convergence is a logged instrumentation miss per the sealed
# design note, not evidence against the theory.  MIT License.
import argparse
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import minimize

LOG2 = math.log(2.0)
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
A_ = ap.parse_args()
SEED = 20260905 if A_.pilot else 20260906
rng = np.random.default_rng(SEED)
fail = []
res = {"prereg": "GO-P-2026-063", "seed": SEED, "pilot": bool(A_.pilot),
       "sections": {}}
print(f"GO-P-2026-063 harness -- {'PILOT' if A_.pilot else 'GOVERNED'} run, "
      f"seed {SEED}")
t0 = time.time()


def whiten(SigT, SigTS):
    C = np.linalg.cholesky(SigT)
    Mi = np.linalg.inv(C)
    W = Mi @ SigTS @ Mi.T
    lam, Q = np.linalg.eigh(W)
    y0 = Q.T @ C.T[:, 0]
    return np.clip(lam, 1e-12, 1.0), y0


def rand_instance(r):
    dT = 1 + r
    A = rng.standard_normal((dT, dT))
    SigT = A @ A.T / dT + 0.5 * np.eye(dT)
    Dg = np.diag(1 / np.sqrt(np.diag(SigT)))
    SigT = Dg @ SigT @ Dg
    G = rng.standard_normal((dT, r)) * 0.5
    SU = np.diag(rng.uniform(0.2, 1.0, r))
    SigS = G.T @ SigT @ G + SU
    x = SigT @ G
    SigTcS = SigT - x @ np.linalg.solve(SigS, x.T)
    return SigT, SigTcS, G, SigS, x


def direct_opt(al, D, lam, y0, starts=50):
    d = len(y0)

    def obj(p):
        u = p[:d]
        if abs(p[d]) > 40:
            return 80.0
        n = math.exp(p[d])
        Q0 = float(u @ u)
        Q1 = float(u @ (lam * u))
        return (al * math.log((Q0 + n) / n)
                + (1 - al) * math.log((Q1 + n) / n))

    cons = [{"type": "ineq", "fun": lambda p: D - (
        float((y0 - p[:d]) @ (y0 - p[:d])) + math.exp(min(p[d], 40)))}]
    best, bp = None, None
    for _ in range(starts):
        p0 = np.concatenate([y0 * rng.uniform(0.2, 1.0)
                             + rng.normal(0, 0.15, d),
                             [math.log(rng.uniform(1e-3, D))]])
        rr = minimize(obj, p0, constraints=cons, method="SLSQP",
                      options={"maxiter": 1500, "ftol": 1e-15})
        if rr.success and (best is None or rr.fun < best):
            best, bp = rr.fun, rr.x
    if bp is None:
        return None
    u = bp[:d]
    n = math.exp(bp[d])
    Q0, Q1 = float(u @ u), float(u @ (lam * u))
    return dict(R=0.5 * math.log2((Q0 + n) / n),
                L=0.5 * math.log2((Q1 + n) / n), u=u, n=n, J=best)


def foc_resid(al, u, n, lam, y0):
    Q0, Q1 = float(u @ u), float(u @ (lam * u))
    g0, g1 = n / (Q0 + n), n / (Q1 + n)
    scale = 1 - al * g0 - (1 - al) * g1
    u_pred = scale * y0 / ((1 - (1 - al) * g1) + (1 - al) * g1 * lam)
    return float(np.max(np.abs(u - u_pred)))


# =============================================================== [1] s1
print("=" * 78)
print("[1] s1 eq:vecfoc at the optimum, r in {1,2,3,4} + extreme instance")
ok1 = True
miss1 = False
worst1 = 0.0
for r in (1, 2, 3, 4):
    SigT, SigTcS, *_ = rand_instance(r)
    lam, y0 = whiten(SigT, SigTcS)
    D = float(rng.uniform(0.15, 0.6))
    for al in (0.0, 0.5, 1.0):
        sol = direct_opt(al, D, lam, y0)
        if sol is None:
            miss1 = True
            continue
        worst1 = max(worst1, foc_resid(al, sol["u"], sol["n"], lam, y0))
# extreme: lambda_min = 0.02, y0 tilted onto the low mode, D = 0.92
lam_e = np.array([0.02, 0.6, 1.0])
y0_e = np.array([0.7, 0.5, math.sqrt(1 - 0.49 - 0.25)])
for al in (0.25, 0.75):
    sol = direct_opt(al, 0.92, lam_e, y0_e, starts=60)
    if sol is None:
        miss1 = True
        continue
    worst1 = max(worst1, foc_resid(al, sol["u"], sol["n"], lam_e, y0_e))
ok1 = worst1 <= 5e-4
print(f"  worst FOC residual = {worst1:.2e} (bar 5e-4)")
res["sections"]["s1"] = {"worst_foc": worst1, "pass": bool(ok1)}
if miss1:
    fail.append("s1-INSTRUMENTATION-MISS")
elif not ok1:
    fail.append("s1-vecfoc")

# =============================================================== [2] s2
print("=" * 78)
print("[2] s2 r=1 consistency with Theorem 3's known frontier")
ok2 = True
rho, t = math.sqrt(0.75), 0.5
SigT = np.array([[1, rho], [rho, 1.0]])
sts = SigT[:, 1:2]
SigTcS = SigT - sts @ sts.T / (1 + t)
lam1, y01 = whiten(SigT, SigTcS)
known = {0.0: (0.9085, 0.5228), 0.5: (0.8772, 0.5328), 1.0: (0.8685, 0.5577)}
for al, (Rk, Lk) in known.items():
    sol = direct_opt(al, 0.3, lam1, y01, starts=60)
    if sol is None:
        fail.append("s2-INSTRUMENTATION-MISS")
        ok2 = False
        break
    ok2 &= abs(sol["R"] - Rk) < 2e-3 and abs(sol["L"] - Lk) < 2e-3
print(f"  Thm-3 values reproduced: {ok2}")
res["sections"]["s2"] = {"pass": bool(ok2)}
if not ok2 and "s2-INSTRUMENTATION-MISS" not in fail:
    fail.append("s2-thm3-consistency")

# =============================================================== [3] s3
print("=" * 78)
print("[3] s3 moment-program converse (r=2, general coupling)")
ok3 = True
SigT, SigTcS, G, SigS, x = rand_instance(2)
lam, y0 = whiten(SigT, SigTcS)
dT = 3
D = 0.3
ldT = np.linalg.slogdet(SigT)[1]
ldTcS = np.linalg.slogdet(SigTcS)[1]
worst3 = 0.0
for al in (0.0, 0.5, 1.0):
    sol = direct_opt(al, D, lam, y0, starts=60)
    if sol is None:
        fail.append("s3-INSTRUMENTATION-MISS")
        ok3 = False
        break
    Jsys = al * sol["R"] + (1 - al) * sol["L"]

    def f(p, al=al):
        cvec = p[:dT]
        if abs(p[dT]) > 40:
            return 80.0
        v = math.exp(p[dT])
        Se0 = SigT - np.outer(cvec, cvec) / v
        d0 = np.linalg.det(Se0)
        Ov = np.block([[np.array([[v]]), (G.T @ cvec).reshape(1, 2)],
                       [(G.T @ cvec).reshape(2, 1), SigS]])
        Cts = np.hstack([cvec.reshape(dT, 1), x])
        try:
            Se1 = SigT - Cts @ np.linalg.solve(Ov, Cts.T)
        except np.linalg.LinAlgError:
            return 80.0
        d1 = np.linalg.det(Se1)
        if d0 <= 1e-280 or d1 <= 1e-280:
            return 80.0
        return al * (ldT - math.log(d0)) + (1 - al) * (ldTcS - math.log(d1))

    cons = [{"type": "ineq", "fun": lambda p: D - (
        1 - 2 * p[0] + math.exp(min(p[dT], 40)))},
        {"type": "ineq", "fun": lambda p: np.linalg.eigvalsh(np.block(
            [[SigT, p[:dT].reshape(dT, 1)],
             [p[:dT].reshape(1, dT),
              np.array([[math.exp(min(p[dT], 40))]])]]))[0]}]
    best = None
    for _ in range(60):
        p0 = np.concatenate([SigT[:, 0] * rng.uniform(0.2, 0.9)
                             + rng.normal(0, 0.1, dT),
                             [math.log(rng.uniform(1e-3, 1.0))]])
        rr = minimize(f, p0, constraints=cons, method="SLSQP",
                      options={"maxiter": 1500, "ftol": 1e-15})
        if rr.success and (best is None or rr.fun < best):
            best = rr.fun
    if best is None:
        fail.append("s3-INSTRUMENTATION-MISS")
        ok3 = False
        break
    worst3 = max(worst3, abs(0.5 * best / LOG2 - Jsys))
ok3 = ok3 and worst3 <= 5e-4
print(f"  worst |moment - system| = {worst3:.2e} (bar 5e-4)")
res["sections"]["s3"] = {"worst_dev": worst3, "pass": bool(ok3)}
if not ok3 and "s3-INSTRUMENTATION-MISS" not in fail:
    fail.append("s3-moment-converse")

# =============================================================== [4] s4
print("=" * 78)
print("[4] s4 unrestricted conditional-BA never below (r=2 instance)")
SigT = np.eye(3)
SigT[0, 1] = SigT[1, 0] = 0.6
SigT[0, 2] = SigT[2, 0] = 0.4
tau = np.array([0.4, 0.8])
G4 = np.zeros((3, 2))
G4[1, 0] = 1.0
G4[2, 1] = 1.0
SigS4 = G4.T @ SigT @ G4 + np.diag(tau)
x4 = SigT @ G4
SigTcS = SigT - x4 @ np.linalg.solve(SigS4, x4.T)
lam, y0 = whiten(SigT, SigTcS)
D = 0.35
L_sys = direct_opt(0.0, D, lam, y0, starts=60)["L"]


def Hb(p):
    p = np.asarray(p, float).ravel()
    p = p[p > 1e-300]
    return float(-(p * np.log2(p)).sum())


def mi_j(J):
    return Hb(J.sum(1)) + Hb(J.sum(0)) - Hb(J)


from math import erf, sqrt


def gbins(mu, sd, edges):
    cd = [0.5 * (1 + erf((e - mu) / (sd * sqrt(2)))) for e in edges]
    return np.maximum(np.diff([0.0] + cd + [1.0]), 0)


n1 = 11
g1d = np.linspace(-2.8, 2.8, n1)
pts = np.stack(np.meshgrid(g1d, g1d, g1d, indexing="ij"), -1).reshape(-1, 3)
Sti = np.linalg.inv(SigT)
w = np.exp(-0.5 * np.einsum("ni,ij,nj->n", pts, Sti, pts))
pT = w / w.sum()
nbins4 = 5
edges = list(np.linspace(-2.5, 2.5, nbins4 - 1))
pXS = np.zeros((len(pT), nbins4 * nbins4))
for i in range(len(pT)):
    b1 = gbins(pts[i, 1], math.sqrt(tau[0]), edges)
    b2 = gbins(pts[i, 2], math.sqrt(tau[1]), edges)
    pXS[i] = pT[i] * np.outer(b1, b2).ravel()
yh = np.linspace(-2.4, 2.4, 11)
dmat = (pts[:, 0:1] - yh[None, :]) ** 2


def ba(beta, iters=1500, tol=1e-10):
    nx, ny = dmat.shape
    pX = pXS.sum(1)
    psx = pXS / np.maximum(pX, 1e-300)[:, None]
    pS = pXS.sum(0)
    pxg = pXS / np.maximum(pS, 1e-300)[None, :]
    q = np.full((nx, ny), 1.0 / ny)
    for _ in range(iters):
        r1 = pxg.T @ q
        lq = psx @ np.log(np.maximum(r1, 1e-300)) - beta * LOG2 * dmat
        lq -= lq.max(1, keepdims=True)
        qn = np.exp(lq)
        qn /= qn.sum(1, keepdims=True)
        if np.abs(qn - q).max() < tol:
            q = qn
            break
        q = qn
    return q


blo, bhi = 0.05, 3000.0
pX = pXS.sum(1)
for _ in range(40):
    bm = math.sqrt(blo * bhi)
    q = ba(bm)
    dd = float((pX[:, None] * q * dmat).sum())
    if dd > D:
        blo = bm
    else:
        bhi = bm
q = ba(bhi)
Lb = 0.0
for si in range(pXS.shape[1]):
    ps = pXS[:, si].sum()
    if ps > 1e-14:
        pxg = pXS[:, si] / ps
        Lb += ps * mi_j(pxg[:, None] * q)
ok4 = L_sys - 0.03 <= Lb <= L_sys + 0.15
print(f"  BA L = {Lb:.4f} vs system {L_sys:.4f} (window [-0.03, +0.15]) "
      f"ok={ok4}")
res["sections"]["s4"] = {"ba": Lb, "sys": L_sys, "pass": bool(ok4)}
if not ok4:
    fail.append("s4-ba-net")

# =============================================================== [5] s5
print("=" * 78)
print("[5] s5 Thm 8: aligned decomposition exact; misaligned strict")


def matrix_prog(al, D, SigT, SigTcS, k, starts=60):
    dT = SigT.shape[0]
    npar = k * dT + k * (k + 1) // 2

    def unpack(p):
        Am = p[:k * dT].reshape(k, dT)
        Lc = np.zeros((k, k))
        idx = k * dT
        for i in range(k):
            for j in range(i + 1):
                Lc[i, j] = math.exp(min(p[idx], 20)) if i == j else p[idx]
                idx += 1
        return Am, Lc @ Lc.T

    def obj(p):
        Am, SN = unpack(p)
        d0 = np.linalg.det(Am @ SigT @ Am.T + SN)
        d1 = np.linalg.det(Am @ SigTcS @ Am.T + SN)
        dn = np.linalg.det(SN)
        if dn <= 1e-280 or d0 <= 1e-280 or d1 <= 1e-280:
            return 80.0
        return al * math.log(d0 / dn) + (1 - al) * math.log(d1 / dn)

    E = np.zeros((k, dT))
    for i in range(k):
        E[i, i] = 1.0

    cons = [{"type": "ineq", "fun": lambda p: D - (
        np.trace((E - unpack(p)[0]) @ SigT @ (E - unpack(p)[0]).T)
        + np.trace(unpack(p)[1]))}]
    best = None
    for _ in range(starts):
        p0 = np.concatenate([
            (E * rng.uniform(0.3, 0.9)).ravel()
            + rng.normal(0, 0.08, k * dT),
            rng.normal(-1.5, 0.5, k * (k + 1) // 2)])
        rr = minimize(obj, p0, constraints=cons, method="SLSQP",
                      options={"maxiter": 2500, "ftol": 1e-14})
        if rr.success and (best is None or rr.fun < best):
            best = rr.fun
    return None if best is None else 0.5 * best / LOG2


ok5 = True
miss5 = False
tA = 0.5
SigT4 = np.eye(3)
SigT4[0, 2] = SigT4[2, 0] = 0.7
sts = SigT4[:, 2:3]
SigTcS4 = SigT4 - sts @ sts.T / (1 + tA)
D4 = 0.5
Jfull = matrix_prog(0.0, D4, SigT4, SigTcS4, 2)
best_dec = None
SigTm = np.array([[1, 0.7], [0.7, 1.0]])
stsm = SigTm[:, 1:2]
SigTcm = SigTm - stsm @ stsm.T / (1 + tA)
lm, y0m = whiten(SigTm, SigTcm)
for d1 in np.linspace(0.08, D4 - 0.05, 12):
    s1v = direct_opt(0.0, d1, lm, y0m, starts=25)
    if s1v is None:
        miss5 = True
        continue
    d2 = D4 - d1
    L2 = max(0.0, 0.5 * math.log2(1 / d2)) if d2 < 1 else 0.0
    val = s1v["L"] + L2
    if best_dec is None or val < best_dec:
        best_dec = val
if Jfull is None or best_dec is None:
    miss5 = True
else:
    ok5 &= abs(Jfull - best_dec) <= 8e-3
    print(f"  aligned: program={Jfull:.4f} decomposition={best_dec:.4f} "
          f"|diff|={abs(Jfull-best_dec):.4f} (bar 8e-3)")
# misaligned strictness
SigT5 = np.eye(3)
SigT5[0, 2] = SigT5[2, 0] = 0.55
SigT5[1, 2] = SigT5[2, 1] = 0.45
SigT5[0, 1] = SigT5[1, 0] = 0.2
sts = SigT5[:, 2:3]
SigTcS5 = SigT5 - sts @ sts.T / (1 + tA)
Jfull5 = matrix_prog(0.0, D4, SigT5, SigTcS5, 2)
best_dec5 = None
SigTm1 = np.array([[1, 0.55], [0.55, 1.0]])
s1m = SigTm1[:, 1:2]
SigTc1 = SigTm1 - s1m @ s1m.T / (1 + tA)
lm1, y01m = whiten(SigTm1, SigTc1)
SigTm2 = np.array([[1, 0.45], [0.45, 1.0]])
s2m = SigTm2[:, 1:2]
SigTc2 = SigTm2 - s2m @ s2m.T / (1 + tA)
lm2, y02m = whiten(SigTm2, SigTc2)
for d1 in np.linspace(0.08, D4 - 0.05, 12):
    a1 = direct_opt(0.0, d1, lm1, y01m, starts=25)
    a2 = direct_opt(0.0, D4 - d1, lm2, y02m, starts=25)
    if a1 is None or a2 is None:
        miss5 = True
        continue
    val = a1["L"] + a2["L"]
    if best_dec5 is None or val < best_dec5:
        best_dec5 = val
if Jfull5 is None or best_dec5 is None:
    miss5 = True
else:
    gap5 = best_dec5 - Jfull5
    ok5 &= gap5 >= 2e-3
    print(f"  misaligned: program={Jfull5:.4f} forced-decomp="
          f"{best_dec5:.4f} strict gap={gap5:.4f} (bar >= 2e-3)")
res["sections"]["s5"] = {"pass": bool(ok5 and not miss5)}
if miss5:
    fail.append("s5-INSTRUMENTATION-MISS")
elif not ok5:
    fail.append("s5-thm8")

# =============================================================== [6] s6
print("=" * 78)
print("[6] s6 uniqueness nets: dispersion, fixed-point roots, Hessian")
ok6 = True
disp_max = 0.0
root_max = 0.0
hess_min = np.inf
for r in (1, 2, 3):
    SigT, SigTcS, *_ = rand_instance(r)
    lam, y0 = whiten(SigT, SigTcS)
    D = float(rng.uniform(0.2, 0.5))
    for al in (0.3, 0.7):
        # dispersion over independent multi-starts
        vals = []
        for _ in range(12):
            s = direct_opt(al, D, lam, y0, starts=5)
            if s is not None:
                vals.append(s["J"])
        if len(vals) >= 8:
            disp_max = max(disp_max, max(vals) - min(vals))
        # fixed-point root hunt on (g0, g1)
        roots = []
        for g0i in np.linspace(0.05, 0.95, 6):
            for g1i in np.linspace(0.05, 0.95, 6):
                g0, g1 = g0i, g1i
                for _ in range(600):
                    scale = 1 - al * g0 - (1 - al) * g1
                    u = scale * y0 / ((1 - (1 - al) * g1)
                                      + (1 - al) * g1 * lam)
                    n = D - float((y0 - u) @ (y0 - u))
                    if n <= 1e-9:
                        break
                    Q0, Q1 = float(u @ u), float(u @ (lam * u))
                    g0n, g1n = n / (Q0 + n), n / (Q1 + n)
                    if abs(g0n - g0) < 1e-12 and abs(g1n - g1) < 1e-12:
                        break
                    g0 = 0.5 * g0 + 0.5 * g0n
                    g1 = 0.5 * g1 + 0.5 * g1n
                else:
                    continue
                if n > 1e-9:
                    roots.append((g0, g1))
        if len(roots) >= 2:
            rr = np.array(roots)
            root_max = max(root_max, float(np.max(
                np.abs(rr - rr.mean(0)))))
        # Hessian probe of F(u) on the active slice at 5 random points
        sol = direct_opt(al, D, lam, y0, starts=10)
        if sol is None:
            continue
        d = len(y0)
        for _ in range(5):
            u0 = sol["u"] + rng.normal(0, 0.05, d)
            n0 = D - float((y0 - u0) @ (y0 - u0))
            if n0 <= 1e-3:
                continue

            def F(u):
                nn = D - float((y0 - u) @ (y0 - u))
                if nn <= 1e-9:
                    return 80.0
                return (al * math.log((float(u @ u) + nn) / nn)
                        + (1 - al) * math.log(
                            (float(u @ (lam * u)) + nn) / nn))

            eps = 1e-4
            H = np.zeros((d, d))
            F0 = F(u0)
            for i in range(d):
                for j in range(i, d):
                    ei = np.zeros(d)
                    ej = np.zeros(d)
                    ei[i] = eps
                    ej[j] = eps
                    H[i, j] = H[j, i] = (
                        F(u0 + ei + ej) - F(u0 + ei) - F(u0 + ej) + F0
                    ) / eps ** 2
            hess_min = min(hess_min, float(np.linalg.eigvalsh(H)[0]))
ok6 = disp_max <= 1e-5 and root_max <= 1e-6 and hess_min >= 0.02
print(f"  dispersion={disp_max:.2e} (bar 1e-5)  root spread="
      f"{root_max:.2e} (bar 1e-6)  min Hessian eig={hess_min:.3f} "
      f"(bar >= 0.02)")
res["sections"]["s6"] = {"dispersion": disp_max, "root_spread": root_max,
                         "hess_min": hess_min, "pass": bool(ok6)}
if not ok6:
    fail.append("s6-uniqueness")

# =====================================================================
print("=" * 78)
verdict = "ALL PASS" if not fail else f"FAIL: {fail}"
res["verdict"] = {f"s{i}": (f"s{i}" not in
                            [f.split("-")[0] for f in fail])
                  for i in range(1, 7)}
res["GO11R_supported"] = not fail
res["seconds_total"] = round(time.time() - t0, 1)
print("VERDICT:", verdict)
print("===GO11R-JSON===")
print(json.dumps(res, indent=1, default=float))
print("===END===")
