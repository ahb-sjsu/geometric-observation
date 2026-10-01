"""Checks for the full-description low-distortion closed form and the rank bound, 2026-10-01.

L1 (alpha = 0) Q > 0, J arbitrary (non-commuting): the closed form
   Sigma_e0 = Q^-1/2 Z Q^-1/2, Z = sum z_i w_i w_i^T over the eigenpairs (p_i, w_i) of P = Q^-1/2 J Q^-1/2,
   z_i the positive root of theta p z^2 + (theta - alpha p) z - 1 = 0, theta set by sum z_i = D,
   equals the minimum-leakage optimum of the max-det program (cvxpy), whenever Sigma_e0 <= Sigma_T.
L2 (alpha in (0,1)) same closed form vs multi-start SLSQP on the weighted program.
L3 the closed-form rate and leakage formulas.
L4 rank bound: for singular Q (partial description), the optimal Sigma_T - Sigma_e0 has rank <= rank Q
   (min leakage via cvxpy; weighted via SLSQP), random instances and the coupled instance.
"""
import numpy as np, math
from scipy.optimize import brentq, minimize
import cvxpy as cp
LN2 = math.log(2); rng = np.random.default_rng(11)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)
ld = lambda M: np.linalg.slogdet(M)[1] / LN2

def msqrt(M, inv=False):
    w, U = np.linalg.eigh(M); w = np.clip(w, 0, None)
    return U @ np.diag(w ** (-0.5 if inv else 0.5)) @ U.T

def closed_form(S, Q, J, D, alpha):
    Qih = msqrt(Q, inv=True); p, Wv = np.linalg.eigh(Qih @ J @ Qih); p = np.clip(p, 0, None)
    def zs(th):
        out = []
        for pi in p:
            if pi < 1e-14: out.append(1 / th)
            else:
                a, b = th * pi, th - alpha * pi
                out.append((-b + math.sqrt(b * b + 4 * a)) / (2 * a))
        return np.array(out)
    th = brentq(lambda t: zs(t).sum() - D, 1e-9, 1e9)
    z = zs(th); Z = Wv @ np.diag(z) @ Wv.T
    Se0 = Qih @ Z @ Qih
    K = np.linalg.inv(np.linalg.inv(S) + J)
    r = 0.5 * (ld(S @ Q)) - 0.5 * np.sum(np.log2(z))
    l = 0.5 * ld(K @ Q) + 0.5 * np.sum(np.log2((1 + p * z) / z))
    return Se0, r, l

def costs(S, J, Se0):
    K = np.linalg.inv(np.linalg.inv(S) + J); Se = np.linalg.inv(np.linalg.inv(Se0) + J)
    return 0.5 * (ld(S) - ld(Se0)), 0.5 * (ld(K) - ld(Se))

def maxdet(S, Q, J, D):
    p = S.shape[0]; K = np.linalg.inv(np.linalg.inv(S) + J); Jh = msqrt(J)
    X = cp.Variable((p, p), symmetric=True); Zv = cp.Variable((p, p), symmetric=True)
    blk = cp.bmat([[Zv - X, X @ Jh], [Jh @ X, np.eye(p) - Jh @ X @ Jh]])
    pr = cp.Problem(cp.Maximize(cp.log_det(X)), [0.5 * (blk + blk.T) >> 0, cp.trace(Q @ Zv) <= D, K - X >> 0])
    pr.solve(solver=cp.CLARABEL)
    Se = X.value; Se0 = np.linalg.inv(np.linalg.inv(Se) - J)
    return Se0

def weighted(S, Q, J, D, alpha, starts=12):
    p = S.shape[0]; iu = np.tril_indices(p)
    def unpack(x):
        L = np.zeros((p, p)); L[iu] = x; return L @ L.T + 1e-12 * np.eye(p)
    def f(x):
        r, l = costs(S, J, unpack(x)); return alpha * r + (1 - alpha) * l
    cons = [{'type': 'ineq', 'fun': lambda x: D - np.trace(Q @ unpack(x))},
            {'type': 'ineq', 'fun': lambda x: np.linalg.eigvalsh(S - unpack(x))[0]}]
    best = None
    for _ in range(starts):
        L0 = np.linalg.cholesky(S * rng.uniform(0.05, 0.5)) @ np.linalg.qr(rng.normal(size=(p, p)))[0]
        L0 = np.linalg.cholesky(L0 @ L0.T)
        res = minimize(f, L0[iu], method='SLSQP', constraints=cons, options={'maxiter': 3000, 'ftol': 1e-13})
        if res.success and (best is None or res.fun < best.fun): best = res
    return unpack(best.x), best.fun

def instance(p, rankJ, Qfull=True, m=None):
    G = rng.normal(size=(p, p)); S = G @ G.T / p + 0.3 * np.eye(p)
    if Qfull:
        Wm = rng.normal(size=(p, p)); Q = Wm @ Wm.T / p + 0.3 * np.eye(p)
    else:
        F = np.zeros((m, p)); F[:, :m] = np.eye(m); Wm = rng.normal(size=(m, m)); Q = F.T @ (Wm @ Wm.T / m + 0.2 * np.eye(m)) @ F
    H = rng.normal(size=(rankJ, p)); J = H.T @ H * rng.uniform(0.5, 3)
    return S, Q, J

# L1, L3
ok1 = ok3 = True; n1 = 0; worst = 0
while n1 < 30:
    p = int(rng.integers(2, 5)); S, Q, J = instance(p, int(rng.integers(1, p + 1)))
    noncomm = np.linalg.norm(Q @ S @ J - J @ S @ Q)
    D = rng.uniform(0.02, 0.4) * np.trace(Q @ S)
    Se0, r, l = closed_form(S, Q, J, D, 0.0)
    if np.linalg.eigvalsh(S - Se0)[0] < 1e-9: continue           # outside the regime
    Sm = maxdet(S, Q, J, D); rm, lm = costs(S, J, Sm)
    rc, lc = costs(S, J, Se0)
    worst = max(worst, abs(lm - l)); ok1 = ok1 and abs(lm - l) < 1e-5 and noncomm > 1e-3
    ok3 = ok3 and abs(rc - r) < 1e-9 and abs(lc - l) < 1e-9 and abs(np.trace(Q @ Se0) - D) < 1e-9
    n1 += 1
check("L1 min-leakage closed form == max-det optimum (30 non-commuting instances in the regime)", ok1, f"max |dL| {worst:.1e}")
check("L3 closed-form rate/leakage formulas and active distortion", ok3)

# L2 weighted
ok2 = True; n2 = 0; worst2 = 0
while n2 < 12:
    p = int(rng.integers(2, 4)); S, Q, J = instance(p, int(rng.integers(1, p + 1)))
    D = rng.uniform(0.02, 0.3) * np.trace(Q @ S); alpha = rng.uniform(0.1, 0.9)
    Se0, r, l = closed_form(S, Q, J, D, alpha)
    if np.linalg.eigvalsh(S - Se0)[0] < 1e-9: continue
    _, fbest = weighted(S, Q, J, D, alpha)
    fc = alpha * r + (1 - alpha) * l
    worst2 = max(worst2, fc - fbest); ok2 = ok2 and fc <= fbest + 1e-6
    n2 += 1
check("L2 weighted closed form <= best of multi-start SLSQP (12 instances)", ok2, f"max excess {worst2:.1e}")

# L4 rank bound, partial description
ok4 = True; ranks = []
for _ in range(15):
    p = int(rng.integers(3, 5)); m = int(rng.integers(1, p)); S, Q, J = instance(p, int(rng.integers(1, p + 1)), Qfull=False, m=m)
    D = rng.uniform(0.2, 0.8) * np.trace(Q @ S)
    Sm = maxdet(S, Q, J, D); ev = np.sort(np.linalg.eigvalsh(np.linalg.cholesky(np.linalg.inv(S)) .T @ (S - Sm) @ np.linalg.cholesky(np.linalg.inv(S))))
    rk = int(np.sum(ev > 1e-6)); ranks.append((p, m, rk)); ok4 = ok4 and rk <= m
u = np.array([math.cos(math.radians(50)), math.sin(math.radians(50))])
S = np.zeros((3, 3)); S[:2, :2] = np.diag([1.0, 0.4]); S[:2, 2] = S[2, :2] = 0.6 * u; S[2, 2] = 1.0
Q = np.diag([1.0, 1.0, 0.0]); J = np.zeros((3, 3)); J[2, 2] = 20.0
for Dd in (0.3, 0.6, 0.9, 1.2):
    Sm = maxdet(S, Q, J, Dd); Li = np.linalg.cholesky(np.linalg.inv(S))
    ev = np.sort(np.linalg.eigvalsh(Li.T @ (S - Sm) @ Li)); rk = int(np.sum(ev > 1e-6)); ranks.append(("coupled", Dd, rk)); ok4 = ok4 and rk <= 2
check("L4 rank(Sigma_T - Sigma_e0) <= rank Q at the min-leakage optimum (15 random + coupled)", ok4, str(ranks[-4:]))
print("FAILS:", fails)
