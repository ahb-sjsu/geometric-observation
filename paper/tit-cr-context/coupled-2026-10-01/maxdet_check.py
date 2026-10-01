"""General coupled case as a max-det program in the holder's posterior covariance X, 2026-10-01.
  minimize  -1/2 log det X
  s.t.      [[Z - E X E^T, E X Jh], [Jh X E^T, I - Jh X Jh]] >= 0,  tr Z <= D,  X <= K
content = 1/2 log2 det K / det X.  Compared with brute force over Gaussian descriptions W = G T + N(0, I).
"""
import numpy as np, math, sys
from scipy.optimize import minimize
import cvxpy as cp
LN2 = math.log(2); rng = np.random.default_rng(2026)

def instance(m, r):
    p = m + r
    while True:
        A = rng.normal(size=(p, p)); ST = A @ A.T / p + 0.15 * np.eye(p)
        d = np.sqrt(np.diag(ST)); ST = ST / np.outer(d, d)          # unit variances
        if np.linalg.eigvalsh(ST).min() > 0.05: break
    tauU = 10 ** rng.uniform(-1.3, 0.3, r)
    J = np.zeros((p, p)); J[m:, m:] = np.diag(1 / tauU)
    K = np.linalg.inv(np.linalg.inv(ST) + J)
    return ST, J, K

def maxdet(ST, J, K, m, D):
    p = ST.shape[0]; E = np.zeros((m, p)); E[:, :m] = np.eye(m)
    w, U = np.linalg.eigh(J); Jh = U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T
    X = cp.Variable((p, p), symmetric=True); Z = cp.Variable((m, m), symmetric=True)
    blk = cp.bmat([[Z - E @ X @ E.T, E @ X @ Jh], [Jh @ X @ E.T, np.eye(p) - Jh @ X @ Jh]])
    cons = [0.5 * (blk + blk.T) >> 0, cp.trace(Z) <= D, K - X >> 0, X >> 1e-9 * np.eye(p)]
    prob = cp.Problem(cp.Maximize(cp.log_det(X)), cons)
    prob.solve(solver=cp.SCS, eps=1e-9, max_iters=200000) if 'CLARABEL' not in cp.installed_solvers() else prob.solve(solver=cp.CLARABEL)
    Xv = X.value
    return 0.5 * (np.linalg.slogdet(K)[1] - np.linalg.slogdet(Xv)[1]) / LN2, Xv

def brute(ST, J, K, m, D, starts=16):
    p = ST.shape[0]; best = np.inf
    Pf = lambda g: np.linalg.inv(np.linalg.inv(ST) + g.reshape(p, p).T @ g.reshape(p, p))
    f = lambda g: 0.5 * (np.linalg.slogdet(K)[1] + np.linalg.slogdet(np.linalg.inv(Pf(g)) + J)[1]) / LN2
    for _ in range(starts):
        r = minimize(f, rng.normal(0, 1.5, p * p), method='SLSQP',
                     constraints=[{'type': 'ineq', 'fun': lambda g: D - np.trace(Pf(g)[:m, :m])}],
                     options={'maxiter': 4000, 'ftol': 1e-13})
        if r.success and np.trace(Pf(r.x)[:m, :m]) <= D + 1e-8: best = min(best, r.fun)
    return best

print("solvers:", cp.installed_solvers())
worst = 0; n = 0
for m, r in [(2, 1), (2, 2), (3, 1), (3, 2)]:
    for _ in range(5):
        ST, J, K = instance(m, r); D = rng.uniform(0.15, 0.85) * m
        v, Xv = maxdet(ST, J, K, m, D); b = brute(ST, J, K, m, D)
        # recover P from X and check feasibility
        P = np.linalg.inv(np.linalg.inv(Xv) - J)
        feas = np.trace(P[:m, :m]) - D
        n += 1; worst = max(worst, abs(v - b))
        print(f"  m={m} r={r} D={D:.3f}: maxdet {v:.6f}  brute {b:.6f}  diff {v-b:+.2e}  dist slack {feas:+.1e}  minEig(Sigma_T - P) {np.linalg.eigvalsh(ST-P).min():+.1e}")
print(("PASS" if worst < 1e-4 else "FAIL") + f" max-det program == brute-force optimum over Gaussian descriptions ({n} instances), max |diff| {worst:.2e}")
