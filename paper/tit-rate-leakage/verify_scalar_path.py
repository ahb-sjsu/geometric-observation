"""Checks for the scalar described variable (any context, any holder) and the augmented-target corollary, 2026-10-01.

Scalar described variable Y = f^T T, weight w, q = sqrt(w) f, Delta = D_max - D, K = Sigma_{T|S}.
Claim P: every frontier point (weight alpha) is the one-dimensional description along
    b(lam) = M(lam)^-1 S q,  M(lam) = (1 - lam) S + lam K,   lam in [0, 1 - alpha],
normalized q^T S b = 1, with u = b^T S b, v = b^T (S - K) b, R = -1/2 log(1 - Delta u), L = R + 1/2 log(1 - Delta v),
and lam a root of lam (1 - Delta v(lam)) = (1 - alpha)(1 - Delta u(lam)) (the root of least weighted cost).
Claim S (alpha = 0): L(D) = 1/2 log(1 + Delta/mu*), mu* the unique positive root of q^T S (Delta S + mu K)^-1 S q = 1.
Claim A: the frontier description equals the weighted rate-distortion optimum for the weight
    Q' = Q + kappa H^T (H Se0 H^T + Sigma_U)^-1 H,  kappa = (1 - alpha)/(2 nu), at budget tr(Q' Se0).

P1 closed form vs the independent weighted determinant program (cvxpy), random p = 2..6, holder rank 1..p, alpha in [0,1).
P2 secular equation vs the determinant program at alpha = 0; the pencil relation lam = mu/(Delta + mu).
P3 p = 2 scalar context: secular root reproduces g* of the scalar corollary.
P4 limits at alpha = 0: as D -> D_max the direction tends to q + J S q (lam -> 1); as D -> 0 it tends to q (lam -> 0).
A1 augmented-target corollary on random instances (any m, any holder rank): reverse water-filling for Q' at
   budget tr(Q' Se0) reproduces Se0.
"""
import numpy as np, math
from scipy.optimize import brentq, minimize_scalar
import cvxpy as cp
LN2 = math.log(2); rng = np.random.default_rng(31)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)
ld = lambda M: np.linalg.slogdet(M)[1] / LN2

def msqrt(M, inv=False):
    w, U = np.linalg.eigh(M); w = np.clip(w, 1e-300 if inv else 0, None)
    return U @ np.diag(w ** (-0.5 if inv else 0.5)) @ U.T

def costs(S, J, Se0):
    K = np.linalg.inv(np.linalg.inv(S) + J); Se = np.linalg.inv(np.linalg.inv(Se0) + J)
    return 0.5 * (ld(S) - ld(Se0)), 0.5 * (ld(K) - ld(Se))

def weighted(S, Q, J, D, alpha):
    p = S.shape[0]; B = msqrt(J)
    X0 = cp.Variable((p, p), symmetric=True); E = cp.Variable((p, p), symmetric=True)
    blk = cp.bmat([[X0 - E, X0 @ B.T], [B @ X0, np.eye(p) + B @ X0 @ B.T]])
    obj = alpha * cp.log_det(X0) + (1 - alpha) * cp.log_det(E)
    cp.Problem(cp.Maximize(obj), [0.5 * (blk + blk.T) >> 0, S - X0 >> 0, cp.trace(Q @ X0) <= D]).solve(solver=cp.CLARABEL)
    X = 0.5 * (X0.value + X0.value.T); r, l = costs(S, J, X)
    return X, alpha * r + (1 - alpha) * l, r, l

def path_point(S, K, q, lam):
    M = (1 - lam) * S + lam * K; b = np.linalg.solve(M, S @ q); b = b / (q @ S @ b)
    return b, b @ S @ b, b @ (S - K) @ b

def scalar_frontier(S, J, q, D, alpha, grid=4001):
    K = np.linalg.inv(np.linalg.inv(S) + J); Delta = q @ S @ q - D
    def cost(lam):
        b, u, v = path_point(S, K, q, lam)
        if 1 - Delta * u <= 0: return math.inf, None
        R = -0.5 * math.log2(1 - Delta * u); L = R + 0.5 * math.log2(1 - Delta * v)
        return alpha * R + (1 - alpha) * L, (R, L, b, u, v)
    def g(lam):
        b, u, v = path_point(S, K, q, lam); return lam * (1 - Delta * v) - (1 - alpha) * (1 - Delta * u)
    lams = np.linspace(0, 1 - alpha, grid); gs = [g(l) for l in lams]
    roots = [0.0] if alpha == 1 else []
    for i in range(len(lams) - 1):
        if gs[i] == 0: roots.append(lams[i])
        elif gs[i] * gs[i + 1] < 0: roots.append(brentq(g, lams[i], lams[i + 1], xtol=1e-15))
    best = min((cost(l)[0], l) for l in roots)
    return best[0], best[1], cost(best[1])[1], len(roots)

def instance(p, r):
    G = rng.normal(size=(p, p)); S = G @ G.T / p + 0.3 * np.eye(p)
    f = np.zeros(p); f[0] = 1.0; w = rng.uniform(0.5, 2.0); q = math.sqrt(w) * f
    H = rng.normal(size=(r, p)); SU = np.diag(rng.uniform(0.05, 1.0, r))
    return S, q, np.outer(q, q), H, SU, H.T @ np.linalg.inv(SU) @ H

# P1
ok1 = True; worst = 0; nroots = []
for t in range(40):
    p = int(rng.integers(2, 7)); r = int(rng.integers(1, p + 1)); S, q, Q, H, SU, J = instance(p, r)
    D = rng.uniform(0.05, 0.9) * (q @ S @ q); alpha = 0.0 if t % 3 == 0 else float(rng.uniform(0, 0.95))
    fc, lam, info, nr = scalar_frontier(S, J, q, D, alpha); nroots.append(nr)
    _, fb, _, _ = weighted(S, Q, J, D, alpha)
    worst = max(worst, abs(fc - fb)); ok1 = ok1 and abs(fc - fb) < 2e-5 and 0 <= lam <= 1 - alpha + 1e-12
check("P1 scalar described variable: path b(lam) + one scalar equation == determinant program (40 instances, p<=6, holder rank<=p)",
      ok1, f"max |d cost| {worst:.1e}; roots per instance {sorted(set(nroots))}")

# P2 secular equation and pencil relation
ok2 = True; worst2 = 0
for t in range(30):
    p = int(rng.integers(2, 7)); r = int(rng.integers(1, p + 1)); S, q, Q, H, SU, J = instance(p, r)
    D = rng.uniform(0.05, 0.9) * (q @ S @ q); Delta = q @ S @ q - D; K = np.linalg.inv(np.linalg.inv(S) + J)
    phi = lambda mu: q @ S @ np.linalg.solve(Delta * S + mu * K, S @ q) - 1
    mu = brentq(phi, 1e-12, 1e8, xtol=1e-14)
    Lsec = 0.5 * math.log2(1 + Delta / mu)
    _, _, _, lm = weighted(S, Q, J, D, 0.0)
    _, lam, info, _ = scalar_frontier(S, J, q, D, 0.0)
    worst2 = max(worst2, abs(Lsec - lm)); ok2 = ok2 and abs(Lsec - lm) < 2e-5 and abs(lam - mu / (Delta + mu)) < 1e-6
check("P2 secular equation q^T S (Delta S + mu K)^-1 S q = 1 gives L(D); lam = mu/(Delta+mu) (30 instances)", ok2, f"max |dL| {worst2:.1e}")

# P3 scalar corollary
ok3 = True
for rho2, tau2, D in [(0.75, 0.5, 0.3), (0.5, 1e-3, 0.5), (0.6, 0.2, 0.1), (0.75, 0.5, 0.1)]:
    rho = math.sqrt(rho2); S = np.array([[1, rho], [rho, 1]]); q = np.array([1.0, 0]); J = np.diag([0, 1 / tau2])
    s_ = 1 + tau2; Delta = 1 - D; K = np.linalg.inv(np.linalg.inv(S) + J)
    mu = brentq(lambda m: q @ S @ np.linalg.solve(Delta * S + m * K, S @ q) - 1, 1e-12, 1e8, xtol=1e-15)
    a = D * s_; bq = -(D + s_ - rho2); cq = 1 - rho2
    gstar = (-bq + math.sqrt(bq * bq - 4 * a * cq)) / (2 * a)
    ok3 = ok3 and abs((1 + Delta / mu) - gstar) < 1e-9
check("P3 p = 2: secular root reproduces g* of Corollary scalar", ok3)

# P4 high-rate limit
S, q, Q, H, SU, J = instance(4, 2); K = np.linalg.inv(np.linalg.inv(S) + J)
Dm = q @ S @ q
_, lam_lo, info_lo, _ = scalar_frontier(S, J, q, (1 - 1e-5) * Dm, 0.0)      # low rate: D -> D_max
_, lam_hi, info_hi, _ = scalar_frontier(S, J, q, 1e-6 * Dm, 0.0)            # high rate: D -> 0
def c1(b, t): return 1 - abs(b @ t) / (np.linalg.norm(b) * np.linalg.norm(t))
e_lo = c1(info_lo[2], q + J @ S @ q); e_hi = c1(info_hi[2], q)
check("P4 alpha = 0: D -> D_max direction -> q + J S q (lam -> 1); D -> 0 direction -> q (lam -> 0)",
      e_lo < 1e-6 and e_hi < 1e-4, f"lam_lo={lam_lo:.6f} 1-cos={e_lo:.1e}; lam_hi={lam_hi:.2e} 1-cos={e_hi:.1e}")

# A1 augmented-target corollary
def Phi(A):
    w, E = np.linalg.eigh(0.5 * (A + A.T)); return E @ np.diag([1.0 if l <= 1 else 1.0 / l for l in w]) @ E.T
def rd_weighted(S, Qp, Dp):
    Sh = msqrt(S); Qt = Sh @ Qp @ Sh
    f = lambda lnu: np.trace(Qt @ Phi(2 * math.exp(lnu) * Qt)) - Dp
    nu = math.exp(brentq(f, -40, 40, xtol=1e-14)); return Sh @ Phi(2 * nu * Qt) @ Sh
okA = True; worstA = 0
for t in range(25):
    p = int(rng.integers(2, 5)); m = int(rng.integers(1, p + 1)); r = int(rng.integers(1, p + 1))
    G = rng.normal(size=(p, p)); S = G @ G.T / p + 0.3 * np.eye(p)
    F = np.zeros((m, p)); F[:, :m] = np.eye(m); Wm = rng.normal(size=(m, m)); Q = F.T @ (Wm @ Wm.T / m + 0.2 * np.eye(m)) @ F
    H = rng.normal(size=(r, p)); SU = np.diag(rng.uniform(0.05, 1.0, r)); J = H.T @ np.linalg.inv(SU) @ H
    D = rng.uniform(0.1, 0.85) * np.trace(Q @ S); alpha = float(rng.uniform(0, 0.95))
    Se0, _, _, _ = weighted(S, Q, J, D, alpha)
    Sh = msqrt(S); Shi = np.linalg.inv(Sh); X = Shi @ Se0 @ Shi; Qt = Sh @ Q @ Sh; Ht = H @ Sh
    T = (1 - alpha) * Ht.T @ np.linalg.inv(Ht @ X @ Ht.T + SU) @ Ht
    nus = np.logspace(-6, 6, 3000)
    errs = [np.linalg.norm(Phi(2 * nu * Qt + T) - X) for nu in nus]; nu = nus[int(np.argmin(errs))]
    nu = minimize_scalar(lambda z: np.linalg.norm(Phi(2 * z * Qt + T) - X), bounds=(nu / 1.01, nu * 1.01), method='bounded',
                         options={'xatol': 1e-14}).x
    kappa = (1 - alpha) / (2 * nu)
    Qp = Q + kappa * H.T @ np.linalg.inv(H @ Se0 @ H.T + SU) @ H
    Se_rd = rd_weighted(S, Qp, np.trace(Qp @ Se0))
    e = np.linalg.norm(Se_rd - Se0) / np.linalg.norm(Se0); worstA = max(worstA, e); okA = okA and e < 2e-3
check("A1 frontier description == weighted rate-distortion optimum for Q + kappa H^T Sigma_{S|Z}^-1 H (25 instances)", okA, f"max rel. err {worstA:.1e}")
print("FAILS:", fails)
