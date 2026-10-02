"""Checks for the tilted water-filling iteration (majorization-minimization), 2026-10-01.

Whitened coordinates as in Theorem tilted. Objective f(X) = -1/2 ln det X + (1-alpha)/2 ln det(Ht X Ht^T + SU),
feasible set {0 < X <= I, tr(Qt X) <= D}. Iteration:
    B_t = (1-alpha) (Ht X_t Ht^T + SU)^-1,   X_{t+1} = Phi(2 nu_t Qt + Ht^T B_t Ht),  nu_t set by tr(Qt X_{t+1}) = D.
Claim: f(X_{t+1}) <= f(X_t) for t >= 1 (majorization of the concave term by its tangent), and X_t -> the frontier point.
M1 monotone decrease on every instance (m > 1 and holder rank r > 1, non-commuting, partial and full Q).
M2 limit equals the independent weighted determinant program (cost and X).
M3 iterations to reach 1e-9 relative change in cost; the worst case is reported.
"""
import numpy as np, math
from scipy.optimize import brentq
import cvxpy as cp
LN2 = math.log(2); rng = np.random.default_rng(41)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)

def msqrt(M, inv=False):
    w, U = np.linalg.eigh(M); w = np.clip(w, 1e-300 if inv else 0, None)
    return U @ np.diag(w ** (-0.5 if inv else 0.5)) @ U.T

def Phi(A):
    w, E = np.linalg.eigh(0.5 * (A + A.T)); return E @ np.diag([1.0 if l <= 1 else 1.0 / l for l in w]) @ E.T

def weighted(S, Q, J, D, alpha):
    p = S.shape[0]; B = msqrt(J)
    X0 = cp.Variable((p, p), symmetric=True); E = cp.Variable((p, p), symmetric=True)
    blk = cp.bmat([[X0 - E, X0 @ B.T], [B @ X0, np.eye(p) + B @ X0 @ B.T]])
    obj = alpha * cp.log_det(X0) + (1 - alpha) * cp.log_det(E)
    cp.Problem(cp.Maximize(obj), [0.5 * (blk + blk.T) >> 0, S - X0 >> 0, cp.trace(Q @ X0) <= D]).solve(solver=cp.CLARABEL)
    return 0.5 * (X0.value + X0.value.T)

def instance(p, m, r):
    G = rng.normal(size=(p, p)); S = G @ G.T / p + 0.3 * np.eye(p)
    F = np.zeros((m, p)); F[:, :m] = np.eye(m); Wm = rng.normal(size=(m, m)); Q = F.T @ (Wm @ Wm.T / m + 0.2 * np.eye(m)) @ F
    H = rng.normal(size=(r, p)); SU = np.diag(rng.uniform(0.05, 1.0, r))
    return S, Q, H, SU, H.T @ np.linalg.inv(SU) @ H

def mm(S, Q, H, SU, D, alpha, tol=1e-12, itmax=5000):
    Sh = msqrt(S); Qt = Sh @ Q @ Sh; Ht = H @ Sh
    f = lambda X: -0.5 * np.linalg.slogdet(X)[1] + 0.5 * (1 - alpha) * np.linalg.slogdet(Ht @ X @ Ht.T + SU)[1]
    X = np.eye(S.shape[0]); hist = []
    for t in range(itmax):
        T = (1 - alpha) * Ht.T @ np.linalg.inv(Ht @ X @ Ht.T + SU) @ Ht
        g = lambda lnu: np.trace(Qt @ Phi(2 * math.exp(lnu) * Qt + T)) - D
        nu = math.exp(brentq(g, -40, 40, xtol=1e-15))
        Xn = Phi(2 * nu * Qt + T); hist.append(f(Xn))
        if np.linalg.norm(Xn - X) < tol: X = Xn; break
        X = Xn
    return Sh @ X @ Sh, hist

ok1 = ok2 = True; worst_inc = 0; worst_gap = 0; its = []
n = 0
while n < 40:
    p = int(rng.integers(3, 7)); m = int(rng.integers(2, p + 1)); r = int(rng.integers(2, p + 1))
    S, Q, H, SU, J = instance(p, m, r)
    if np.linalg.norm(Q @ S @ J - J @ S @ Q) < 1e-3: continue
    D = rng.uniform(0.1, 0.85) * np.trace(Q @ S); alpha = float(rng.uniform(0, 0.95))
    Se_mm, hist = mm(S, Q, H, SU, D, alpha)
    inc = max([hist[i + 1] - hist[i] for i in range(len(hist) - 1)] + [0.0]); worst_inc = max(worst_inc, inc)
    ok1 = ok1 and inc < 1e-12
    Se_ref = weighted(S, Q, J, D, alpha)
    Sh = msqrt(S); Shi = np.linalg.inv(Sh); Ht = H @ Sh
    fobj = lambda Se: -0.5 * np.linalg.slogdet(Shi @ Se @ Shi)[1] + 0.5 * (1 - alpha) * np.linalg.slogdet(Ht @ (Shi @ Se @ Shi) @ Ht.T + SU)[1]
    gap = fobj(Se_mm) - fobj(Se_ref); worst_gap = max(worst_gap, abs(gap))
    ok2 = ok2 and abs(gap) < 1e-6 and np.linalg.norm(Se_mm - Se_ref) / np.linalg.norm(Se_ref) < 1e-3
    rel = [abs(hist[i + 1] - hist[i]) / max(1.0, abs(hist[i])) for i in range(len(hist) - 1)]
    k = next((i + 1 for i, x in enumerate(rel) if x < 1e-9), len(hist)); its.append(k)
    n += 1
check("M1 cost nonincreasing along the iteration (40 instances, m>1, holder rank r>1, non-commuting)", ok1, f"max increase {worst_inc:.1e}")
check("M2 limit == weighted determinant program", ok2, f"max |d cost| {worst_gap:.1e}")
check("M3 iterations to 1e-9 relative change", True, f"median {int(np.median(its))}, max {max(its)}")
print("FAILS:", fails)
