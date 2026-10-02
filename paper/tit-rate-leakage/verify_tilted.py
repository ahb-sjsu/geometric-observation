"""Checks for the tilted water-filling characterization, 2026-10-01.

Whitened coordinates: X = S^-1/2 Sigma_e0 S^-1/2 (S = Sigma_T), Qt = S^1/2 Q S^1/2, Ht = H S^1/2.
Claim: the frontier point of weight alpha is the unique X with
    X = Phi(At),  At = 2 nu Qt + (1 - alpha) Ht^T (Ht X Ht^T + Sigma_U)^-1 Ht,  tr(Qt X) = D,
where Phi(A) = sum_i min(1, 1/lambda_i) e_i e_i^T is reverse water-filling at level 1 on the spectrum of A.

W1 KKT form at the true optimum: take the optimum X* from an independent solver (cvxpy max-det for
   alpha = 0; the weighted determinant program for alpha in (0,1)), form At(X*), find nu by a 1-D search, and check
   Phi(At) = X*. Random instances: partial and full Q, holders of rank 1..p, non-commuting.
W2 scalar-holder solver: two scalars (nu, beta), At = 2 nu Qt + beta g g^T, beta = (1-alpha)/(g^T X g + s_U^2),
   solved by nested root finding WITHOUT any convex solver; compare its cost to the independent optimum.
W3 reductions: alpha = 1 is reverse water-filling on Qt; commuting geometry matches the commuting closed form.
W4 coupled instance (partial Q, scalar holder): tilted water-filling vs max-det at D = 0.3, 0.6, 0.9, 1.2,
   with the error direction in the plane of Y and the rank of the description.
"""
import numpy as np, math
from scipy.optimize import brentq, minimize, minimize_scalar
import cvxpy as cp
LN2 = math.log(2); rng = np.random.default_rng(23)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)
ld = lambda M: np.linalg.slogdet(M)[1] / LN2

def msqrt(M, inv=False):
    w, U = np.linalg.eigh(M); w = np.clip(w, 1e-300 if inv else 0, None)
    return U @ np.diag(w ** (-0.5 if inv else 0.5)) @ U.T

def Phi(A):
    w, E = np.linalg.eigh(0.5 * (A + A.T))
    return E @ np.diag([1.0 if l <= 1 else 1.0 / l for l in w]) @ E.T

def costs(S, J, Se0):
    K = np.linalg.inv(np.linalg.inv(S) + J); Se = np.linalg.inv(np.linalg.inv(Se0) + J)
    return 0.5 * (ld(S) - ld(Se0)), 0.5 * (ld(K) - ld(Se))

def maxdet(S, Q, J, D):
    p = S.shape[0]; K = np.linalg.inv(np.linalg.inv(S) + J); Jh = msqrt(J)
    X = cp.Variable((p, p), symmetric=True); Z = cp.Variable((p, p), symmetric=True)
    blk = cp.bmat([[Z - X, X @ Jh], [Jh @ X, np.eye(p) - Jh @ X @ Jh]])
    cp.Problem(cp.Maximize(cp.log_det(X)), [0.5 * (blk + blk.T) >> 0, cp.trace(Q @ Z) <= D, K - X >> 0]).solve(solver=cp.CLARABEL)
    return np.linalg.inv(np.linalg.inv(X.value) - J)

def weighted(S, Q, J, D, alpha, starts=None):
    """Independent reference: the weighted program as a determinant maximization.
    max alpha logdet X0 + (1-alpha) logdet E  s.t.  E <= (X0^-1 + J)^-1 (an LMI by Woodbury/Schur),
    0 < X0 <= S, tr(Q X0) <= D. At the optimum E = (X0^-1 + J)^-1."""
    p = S.shape[0]; B = msqrt(J)
    X0 = cp.Variable((p, p), symmetric=True); E = cp.Variable((p, p), symmetric=True)
    blk = cp.bmat([[X0 - E, X0 @ B.T], [B @ X0, np.eye(p) + B @ X0 @ B.T]])
    obj = alpha * cp.log_det(X0) + (1 - alpha) * cp.log_det(E)
    pr = cp.Problem(cp.Maximize(obj), [0.5 * (blk + blk.T) >> 0, S - X0 >> 0, cp.trace(Q @ X0) <= D])
    pr.solve(solver=cp.CLARABEL)
    if X0.value is None: return None, None
    X = 0.5 * (X0.value + X0.value.T); r, l = costs(S, J, X)
    return X, alpha * r + (1 - alpha) * l

def whiten(S, Q, H):
    Sh = msqrt(S); return Sh, Sh @ Q @ Sh, H @ Sh

def tilt(Qt, Ht, SU, X, nu, alpha):
    return 2 * nu * Qt + (1 - alpha) * Ht.T @ np.linalg.inv(Ht @ X @ Ht.T + SU) @ Ht

def instance(p, partial, r):
    G = rng.normal(size=(p, p)); S = G @ G.T / p + 0.3 * np.eye(p)
    if partial:
        m = int(rng.integers(1, p)); F = np.zeros((m, p)); F[:, :m] = np.eye(m)
        Wm = rng.normal(size=(m, m)); Q = F.T @ (Wm @ Wm.T / m + 0.2 * np.eye(m)) @ F
    else:
        Wm = rng.normal(size=(p, p)); Q = Wm @ Wm.T / p + 0.3 * np.eye(p)
    H = rng.normal(size=(r, p)); SU = np.diag(rng.uniform(0.05, 1.0, r))
    return S, Q, H, SU, H.T @ np.linalg.inv(SU) @ H

def kkt_residual(S, Q, H, SU, Se0, alpha):
    Sh, Qt, Ht = whiten(S, Q, H); Shi = np.linalg.inv(Sh); X = Shi @ Se0 @ Shi
    res = minimize_scalar(lambda nu: np.linalg.norm(Phi(tilt(Qt, Ht, SU, X, nu, alpha)) - X),
                          bounds=(1e-8, 1e6), method='bounded', options={'xatol': 1e-12})
    nus = np.logspace(-6, 6, 4000)
    errs = [np.linalg.norm(Phi(tilt(Qt, Ht, SU, X, nu, alpha)) - X) for nu in nus]
    i = int(np.argmin(errs))
    res2 = minimize_scalar(lambda nu: np.linalg.norm(Phi(tilt(Qt, Ht, SU, X, nu, alpha)) - X),
                           bounds=(nus[max(i - 1, 0)], nus[min(i + 1, len(nus) - 1)]), method='bounded', options={'xatol': 1e-14})
    return min(res.fun, res2.fun) / np.linalg.norm(X)

# W1
worst = 0; ok1 = True; n = 0
while n < 40:
    p = int(rng.integers(2, 5)); partial = bool(rng.integers(0, 2)); r = int(rng.integers(1, p + 1))
    S, Q, H, SU, J = instance(p, partial, r)
    if np.linalg.norm(Q @ S @ J - J @ S @ Q) < 1e-3: continue
    D = rng.uniform(0.1, 0.85) * np.trace(Q @ S)
    alpha = 0.0 if n % 2 == 0 else float(rng.uniform(0.1, 0.9))
    Se0 = maxdet(S, Q, J, D) if alpha == 0 else weighted(S, Q, J, D, alpha)[0]
    if Se0 is None: continue
    e = kkt_residual(S, Q, H, SU, Se0, alpha); worst = max(worst, e); ok1 = ok1 and e < 2e-3; n += 1
check("W1 independent optimum == water-filling on the tilted weight (40 non-commuting instances, partial/full Q, holder rank 1..p)", ok1, f"max rel. residual {worst:.1e}")

# W2 scalar-holder solver with no convex solver
def solve_scalar_holder(S, Q, h, sU2, D, alpha):
    Sh, Qt, _ = whiten(S, Q, h[None, :]); g = Sh @ h
    def X_of(nu, beta): return Phi(2 * nu * Qt + beta * np.outer(g, g))
    def nu_of(beta):
        f = lambda lnu: np.trace(Qt @ X_of(math.exp(lnu), beta)) - D
        if f(-40) <= 0:          # the tilt alone already meets the budget: no nu > 0 at this beta
            return math.exp(-40)
        return math.exp(brentq(f, -40, 40, xtol=1e-14))
    if alpha == 1:
        nu = nu_of(0.0); return Sh @ X_of(nu, 0.0) @ Sh
    def gap(beta):
        X = X_of(nu_of(beta), beta); return beta * (g @ X @ g + sU2) - (1 - alpha)
    beta = brentq(gap, 0.0, (1 - alpha) / sU2, xtol=1e-15)
    X = X_of(nu_of(beta), beta); return Sh @ X @ Sh

ok2 = True; worst2 = 0; n = 0
while n < 25:
    p = int(rng.integers(2, 5)); partial = bool(rng.integers(0, 2))
    S, Q, H, SU, J = instance(p, partial, 1)
    D = rng.uniform(0.1, 0.85) * np.trace(Q @ S); alpha = 0.0 if n % 2 == 0 else float(rng.uniform(0.1, 0.9))
    Se0 = solve_scalar_holder(S, Q, H[0], SU[0, 0], D, alpha)
    r_, l_ = costs(S, J, Se0); fc = alpha * r_ + (1 - alpha) * l_
    if alpha == 0:
        r2, l2 = costs(S, J, maxdet(S, Q, J, D)); fb = l2
    else:
        fb = weighted(S, Q, J, D, alpha)[1]
        if fb is None: continue
    feas = np.trace(Q @ Se0) <= D + 1e-9 and np.linalg.eigvalsh(S - Se0)[0] > -1e-9
    worst2 = max(worst2, abs(fc - fb)); ok2 = ok2 and feas and abs(fc - fb) < 1e-5; n += 1
check("W2 scalar-holder two-scalar solver (no convex solver) == independent optimum (25 instances)", ok2, f"max |d cost| {worst2:.1e}")

# W3 reductions
S, Q, H, SU, J = instance(3, False, 2); D = 0.4 * np.trace(Q @ S)
Sh, Qt, Ht = whiten(S, Q, H); w, E = np.linalg.eigh(Qt)
th = brentq(lambda t: sum(min(1.0, t / q) * q for q in w) - D, 1e-9, 1e3)
X_rwf = E @ np.diag([min(1.0, th / q) for q in w]) @ E.T
Shi = np.linalg.inv(Sh); X_w, _ = weighted(S, Q, J, D, 1.0); X_w = Shi @ X_w @ Shi
check("W3a alpha = 1: optimum is reverse water-filling on the eigenvalues of Qt", np.linalg.norm(X_w - X_rwf) < 1e-4)
# commuting: S = I, Q, J diagonal -> per-direction formula of the commuting theorem
q = np.array([1.0, 0.7, 0.3]); j = np.array([0.5, 4.0, 1.5]); alpha = 0.4; D = 0.9
def x_comm(th):
    out = []
    for qi, ji in zip(q, j):
        a, b = th * qi * ji, th * qi - alpha * ji
        out.append(min(1.0, (-b + math.sqrt(b * b + 4 * a)) / (2 * a)))
    return np.array(out)
thc = brentq(lambda t: (q * x_comm(t)).sum() - D, 1e-6, 1e6)
Xc = np.diag(x_comm(thc))
X_t, _ = weighted(np.eye(3), np.diag(q), np.diag(j), D, alpha)
check("W3b commuting geometry: optimum equals the commuting closed form", np.linalg.norm(X_t - Xc) < 1e-4)
e = kkt_residual(np.eye(3), np.diag(q), np.diag(np.sqrt(j)), np.eye(3), Xc, alpha)
check("W3c commuting closed form satisfies the tilted water-filling condition", e < 1e-6, f"rel. residual {e:.1e}")

# W4 coupled instance
u = np.array([math.cos(math.radians(50)), math.sin(math.radians(50))])
S = np.zeros((3, 3)); S[:2, :2] = np.diag([1.0, 0.4]); S[:2, 2] = S[2, :2] = 0.6 * u; S[2, 2] = 1.0
Q = np.diag([1.0, 1.0, 0.0]); h = np.array([0.0, 0.0, 1.0]); sU2 = 0.05; J = np.outer(h, h) / sU2
print("W4 coupled instance: D, L (tilted water-filling), L (max-det), rank of the description")
ok4 = True
for Dd in (0.3, 0.6, 0.9, 1.2):
    Se0 = solve_scalar_holder(S, Q, h, sU2, Dd, 0.0); _, lt = costs(S, J, Se0)
    _, lm = costs(S, J, maxdet(S, Q, J, Dd))
    Li = np.linalg.cholesky(np.linalg.inv(S)); rk = int(np.sum(np.linalg.eigvalsh(Li.T @ (S - Se0) @ Li) > 1e-7))
    ok4 = ok4 and abs(lt - lm) < 1e-5
    print(f"   D={Dd}: L={lt:.5f}  max-det {lm:.5f}  rank {rk}")
check("W4 coupled instance: tilted water-filling == max-det at four budgets", ok4)
print("FAILS:", fails)
