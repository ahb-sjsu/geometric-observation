"""Checks for the commuting-geometry and block-decoupling theorems, 2026-10-01.
Whitened coordinates (Sigma_T = I without loss): Q, J PSD; X = Sigma_e0, 0 < X <= I, tr(Q X) <= D.
  rate r(X) = -1/2 log2 det X ; leakage l(X) = 1/2 log2 det(X^{-1} + J) - 1/2 log2 det(I + J)  (zero at X = I)
C1 commuting Q, J: minimum leakage equals the leakage water-filling formula
   x_i = min{1, (sqrt(1 + 4 j_i/(theta q_i)) - 1)/(2 j_i)}  (x_i = min{1, 1/(theta q_i)} when j_i = 0; x_i = 1 when q_i = 0)
C2 commuting: the brute-force optimum is diagonal in the common eigenbasis
C3 commuting: the weighted frontier point (alpha) equals the closed form root of
   theta q j x^2 + (theta q - alpha j) x - 1 = 0, capped at 1
C4 block-diagonal (non-commuting inside blocks): optimum is block-diagonal
C5 activation order: x_i < 1 iff theta > 1/(q_i (1 + j_i))
"""
import numpy as np, math
from scipy.optimize import minimize, brentq
LN2 = math.log(2); rng = np.random.default_rng(77)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)

def rate(X): return -0.5 * np.linalg.slogdet(X)[1] / LN2
def leak(X, J): return 0.5 * (np.linalg.slogdet(np.linalg.inv(X) + J)[1] - np.linalg.slogdet(np.eye(len(J)) + J)[1]) / LN2

def Xof(g):
    p = int(round(math.sqrt(len(g)))); G = g.reshape(p, p); return np.linalg.inv(np.eye(p) + G.T @ G)

def brute(Q, J, D, alpha=0.0, starts=14):
    p = Q.shape[0]; best = np.inf; Xb = None
    obj = lambda g: alpha * rate(Xof(g)) + (1 - alpha) * leak(Xof(g), J)
    for _ in range(starts):
        res = minimize(obj, rng.normal(0, 1.5, p * p), method='SLSQP',
                       constraints=[{'type': 'ineq', 'fun': lambda g: D - np.trace(Q @ Xof(g))}],
                       options={'maxiter': 5000, 'ftol': 1e-14})
        if res.success and np.trace(Q @ Xof(res.x)) <= D + 1e-8 and res.fun < best:
            best, Xb = res.fun, Xof(res.x)
    return best, Xb

def x_of(theta, q, j, alpha=0.0):
    if q <= 0: return 1.0
    if j <= 0:
        x = (1.0) / (theta * q) if alpha == 0.0 else 1.0 / (theta * q)
        return min(1.0, x)
    a = theta * q * j; b = theta * q - alpha * j; c = -1.0
    x = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    return min(1.0, x)

def closed_form(q, j, D, alpha=0.0):
    tot = lambda th: sum(qi * x_of(th, qi, ji, alpha) for qi, ji in zip(q, j)) - D
    lo, hi = 1e-12, 1.0
    while tot(hi) > 0: hi *= 2
    th = brentq(tot, lo, hi, xtol=1e-15, rtol=1e-14)
    x = np.array([x_of(th, qi, ji, alpha) for qi, ji in zip(q, j)])
    R = sum(-0.5 * math.log2(xi) for xi in x)
    L = sum(0.5 * math.log2((1 + ji * xi) / (xi * (1 + ji))) for xi, ji in zip(x, j))
    return th, x, R, L

def rand_orth(p):
    Qm, _ = np.linalg.qr(rng.normal(size=(p, p))); return Qm

# C1, C2, C5
ok1 = ok2 = ok5 = True; w1 = 0; w2 = 0
for _ in range(16):
    p = int(rng.integers(2, 5)); U = rand_orth(p)
    q = rng.uniform(0, 2, p); q[rng.integers(0, p)] *= rng.integers(0, 2)  # sometimes a direction the decoder ignores
    j = rng.uniform(0, 3, p) * (rng.uniform(size=p) > 0.2)
    Q = U @ np.diag(q) @ U.T; J = U @ np.diag(j) @ U.T
    D = rng.uniform(0.15, 0.85) * q.sum()
    th, x, R, L = closed_form(q, j, D)
    bv, Xb = brute(Q, J, D)
    w1 = max(w1, abs(L - bv)); ok1 = ok1 and abs(L - bv) < 1e-6
    Xd = U.T @ Xb @ U; off = np.abs(Xd - np.diag(np.diag(Xd))).max()
    w2 = max(w2, off); ok2 = ok2 and off < 1e-4
    for qi, ji, xi in zip(q, j, x):
        if qi > 0:
            act = th > 1.0 / (qi * (1 + ji))
            ok5 = ok5 and (act == (xi < 1 - 1e-12))
check("C1 commuting: leakage water-filling formula == brute-force minimum (16 cases)", ok1, f"max |diff| {w1:.2e}")
check("C2 commuting: brute-force optimum diagonal in the common eigenbasis", ok2, f"max off-diagonal {w2:.1e}")
check("C5 activation iff theta > 1/(q(1+j))", ok5)

# C3 weighted frontier
ok3 = True; w3 = 0
for _ in range(10):
    p = 3; U = rand_orth(p); q = rng.uniform(0.2, 2, p); j = rng.uniform(0, 3, p)
    Q = U @ np.diag(q) @ U.T; J = U @ np.diag(j) @ U.T
    D = rng.uniform(0.2, 0.8) * q.sum(); alpha = rng.uniform(0.1, 0.9)
    th, x, R, L = closed_form(q, j, D, alpha)
    bv, Xb = brute(Q, J, D, alpha=alpha)
    val = alpha * R + (1 - alpha) * L
    w3 = max(w3, abs(val - bv)); ok3 = ok3 and abs(val - bv) < 1e-6
check("C3 commuting: weighted frontier closed form == brute force (10 cases)", ok3, f"max |diff| {w3:.2e}")

# C4 block-diagonal, non-commuting inside blocks
ok4 = True; w4 = 0
for _ in range(8):
    U = rand_orth(4)
    def blk():
        A = rng.normal(size=(2, 2)); return A @ A.T / 2 + 0.1 * np.eye(2)
    Qb = np.zeros((4, 4)); Jb = np.zeros((4, 4))
    Qb[:2, :2] = blk(); Qb[2:, 2:] = blk(); Jb[:2, :2] = blk(); Jb[2:, 2:] = blk()
    Q = U @ Qb @ U.T; J = U @ Jb @ U.T
    D = 0.5 * np.trace(Q)
    bv, Xb = brute(Q, J, D)
    Xd = U.T @ Xb @ U; off = np.abs(Xd[:2, 2:]).max()
    w4 = max(w4, off); ok4 = ok4 and off < 1e-4
check("C4 block-diagonal geometry: optimum block-diagonal (8 cases)", ok4, f"max cross-block entry {w4:.1e}")
print("FAILS:", fails)
