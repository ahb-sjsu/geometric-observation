"""Checks for the price of a fixed projection direction (sharpened bound) (Proposition fixedread, Theorem forced), 2026-10-01.

Notation as in the paper: A(Delta) = S Q S - Delta S (S = Sigma_T), K = (S^-1 + J)^-1, a one-dimensional
description Z = b^T T + N reproduced by E[Y | Z] at the active noise level.

F1 leakage of the description reading b equals 1/2 log(1 + Delta/mu_b), mu_b = b^T A b / b^T K b, computed
   directly from conditional covariances (distortion checked equal to D).
F2 mu_max - mu_b >= (mu_1 - mu_2) sin^2 theta_K(b, b(Delta)) on random b, and the excess-leakage bound.
F3 two budgets: min over b of the larger excess >= the minimax bound with sin^2(theta_12 / 2), brute force
   over directions (p = 3), random instances.
F4 the coupled instance: excess of the rate read b_R at D = 1.1, 1.2, 1.3, 1.38 with the bound; minimax over
   fixed reads for the pair (1.38, 1.1) with the bound.
"""
import numpy as np, math
from scipy.linalg import eigh
LN2 = math.log(2); rng = np.random.default_rng(7)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)

def pencil(S, Q, J, Delta):
    K = np.linalg.inv(np.linalg.inv(S) + J); A = S @ Q @ S - Delta * S
    w, V = eigh(A, K)                       # V^T K V = I, ascending
    return K, A, w[::-1], V[:, ::-1]

def ell_b(b, S, Q, J, Delta):
    K, A, _, _ = pencil(S, Q, J, Delta); mub = (b @ A @ b) / (b @ K @ b)
    return 0.5 * math.log2(1 + Delta / mub) if mub > 0 else math.inf, mub

def direct(b, S, Q, J, Delta, F, W):
    # noise at the active constraint, then leakage from conditional covariances
    s2 = (b @ S @ Q @ S @ b) / Delta - b @ S @ b
    Cz = S - np.outer(S @ b, S @ b) / (b @ S @ b + s2)            # Cov(T | Z)
    D = np.trace(Q @ S) - (b @ S @ Q @ S @ b) / (b @ S @ b + s2)
    K = np.linalg.inv(np.linalg.inv(S) + J)
    Kz = np.linalg.inv(np.linalg.inv(Cz) + J)                    # Cov(T | Z, S)
    return 0.5 * (np.linalg.slogdet(K)[1] - np.linalg.slogdet(Kz)[1]) / LN2, D

def sharp(Delta, mu1, a):
    # excess >= 1/2 log(1 + Delta a / ((mu1 - a)(mu1 + Delta))), a = (mu1 - mu2) sin^2 psi < mu1
    if a >= mu1:
        return math.inf          # every direction at this angle has mu_b <= 0: infinite leakage
    return 0.5 * math.log2(1 + Delta * a / ((mu1 - a) * (mu1 + Delta)))

def sin2K(b, v, K):
    c = (b @ K @ v) ** 2 / ((b @ K @ b) * (v @ K @ v)); return max(0.0, 1 - c)

def instance(p, m):
    G = rng.normal(size=(p, p)); S = G @ G.T / p + 0.3 * np.eye(p)
    F = np.zeros((m, p)); F[:, :m] = np.eye(m); Wm = rng.normal(size=(m, m)); W = Wm @ Wm.T / m + 0.2 * np.eye(m)
    H = rng.normal(size=(1 + rng.integers(0, p), p)); J = H.T @ H * rng.uniform(0.5, 3)
    return S, F, W, F.T @ W @ F, J

# F1, F2
ok1 = ok2 = True; worst1 = 0
for _ in range(200):
    p = int(rng.integers(3, 6)); m = int(rng.integers(2, p)); S, F, W, Q, J = instance(p, m)
    lam = np.linalg.eigvalsh(np.linalg.cholesky(S).T @ Q @ np.linalg.cholesky(S))[-1]
    Delta = rng.uniform(0.05, 0.95) * lam
    K, A, mu, V = pencil(S, Q, J, Delta)
    if mu[0] <= 0: continue
    for _ in range(10):
        b = rng.normal(size=p); lb, mub = ell_b(b, S, Q, J, Delta)
        if mub <= 0: continue
        ld, D = direct(b, S, Q, J, Delta, F, W)
        worst1 = max(worst1, abs(ld - lb), abs(D - (np.trace(Q @ S) - Delta)))
        gap = mu[0] - mub; bound = (mu[0] - mu[1]) * sin2K(b, V[:, 0], K)
        Lmin = 0.5 * math.log2(1 + Delta / mu[0])
        exc_bound = sharp(Delta, mu[0], bound)
        ok2 = ok2 and gap >= bound - 1e-10 and (lb - Lmin) >= exc_bound - 1e-10
ok1 = worst1 < 1e-9
check("F1 leakage of the read b: closed form == conditional-covariance computation, distortion == D", ok1, f"max err {worst1:.1e}")
check("F2 mu_max - mu_b >= (mu_1-mu_2) sin^2_K and the sharpened excess-leakage bound (random reads)", ok2)

# F3 two-budget minimax, p = 3, brute force over the sphere
def minimax(S, Q, J, D1, D2, n=200000):
    Dm = np.trace(Q @ S); B = rng.normal(size=(n, S.shape[0]))
    worst = np.full(n, -np.inf)
    for Dd in (D1, D2):
        Delta = Dm - Dd; K, A, mu, V = pencil(S, Q, J, Delta)
        mub = np.einsum('ij,jk,ik->i', B, A, B) / np.einsum('ij,jk,ik->i', B, K, B)
        with np.errstate(divide='ignore', invalid='ignore'):
            ex = np.where(mub > 0, 0.5 * np.log2(1 + Delta / mub), np.inf) - 0.5 * math.log2(1 + Delta / mu[0])
        worst = np.maximum(worst, ex)
    return worst.min()

def minimax_bound(S, Q, J, D1, D2):
    Dm = np.trace(Q @ S); vs, vals = [], []
    for Dd in (D1, D2):
        Delta = Dm - Dd; K, A, mu, V = pencil(S, Q, J, Delta); vs.append(V[:, 0]); vals.append((Delta, mu))
    th = math.acos(min(1.0, math.sqrt(1 - sin2K(vs[0], vs[1], K))))
    s2 = math.sin(th / 2) ** 2
    return min(sharp(De, mu[0], (mu[0] - mu[1]) * s2) for De, mu in vals), math.degrees(th)

ok3 = True; n3 = 0
while n3 < 25:
    S, F, W, Q, J = instance(3, 2)
    Dm = np.trace(Q @ S); lam = np.linalg.eigvalsh(np.linalg.cholesky(S).T @ Q @ np.linalg.cholesky(S))[-1]
    D1, D2 = Dm - 0.15 * lam, Dm - 0.6 * lam
    if min(pencil(S, Q, J, Dm - D1)[2][0], pencil(S, Q, J, Dm - D2)[2][0]) <= 0: continue
    mm = minimax(S, Q, J, D1, D2); bd, th = minimax_bound(S, Q, J, D1, D2)
    ok3 = ok3 and mm >= bd - 1e-9; n3 += 1
check("F3 two-budget minimax excess (brute force) >= bound with sin^2(theta_12/2), 25 instances", ok3)

# F4 coupled instance
u = np.array([math.cos(math.radians(50)), math.sin(math.radians(50))])
S = np.zeros((3, 3)); S[:2, :2] = np.diag([1.0, 0.4]); S[:2, 2] = S[2, :2] = 0.6 * u; S[2, 2] = 1.0
F = np.zeros((2, 3)); F[:, :2] = np.eye(2); Q = F.T @ F; J = np.zeros((3, 3)); J[2, 2] = 1 / 0.05
Dm = np.trace(Q @ S)
wR, VR = eigh(S @ Q @ S, S); bR = VR[:, -1]
print("F4 coupled instance (D, excess leakage of the rate read b_R, its bound, K-angle to b(D))")
for Dd in (1.1, 1.2, 1.3, 1.38):
    Delta = Dm - Dd; K, A, mu, V = pencil(S, Q, J, Delta)
    lb, mub = ell_b(bR, S, Q, J, Delta); Lmin = 0.5 * math.log2(1 + Delta / mu[0])
    s2 = sin2K(bR, V[:, 0], K)
    bd = sharp(Delta, mu[0], (mu[0] - mu[1]) * s2)
    print(f"   D={Dd}: L={Lmin:.4f}  excess={lb - Lmin:.4f}  bound={bd:.4f}  angle={math.degrees(math.asin(math.sqrt(s2))):.2f} deg")
mm = minimax(S, Q, J, 1.38, 1.1, n=400000); bd, th = minimax_bound(S, Q, J, 1.38, 1.1)
print(f"   pair (1.38, 1.1): K-angle between optimal reads {th:.2f} deg; best fixed read pays {mm:.4f} bits at one budget; bound {bd:.4f}")
check("F4 coupled minimax >= bound", mm >= bd - 1e-9)

# F5 scalar sources (every budget is one-dimensional, so L = L_1d): two budgets, brute force over the circle
print("F5 scalar sources (rho^2, tau^2, D1, D2): K-angle, best fixed read's larger excess, bound, L at both budgets")
ok5 = True
for rho2, tau2, D1, D2 in [(0.75, 0.05, 0.1, 0.7), (0.5, 1e-3, 0.2, 0.8)]:
    rho = math.sqrt(rho2); S = np.array([[1, rho], [rho, 1]]); Q = np.diag([1.0, 0]); J = np.diag([0, 1 / tau2])
    th = np.linspace(0, math.pi, 400001); B = np.stack([np.cos(th), np.sin(th)], 1)
    worst = np.full(len(th), -np.inf); Ls = []
    for Dd in (D1, D2):
        Delta = 1 - Dd; K, A, mu, V = pencil(S, Q, J, Delta); Lmin = 0.5 * math.log2(1 + Delta / mu[0]); Ls.append(Lmin)
        mub = np.einsum('ij,jk,ik->i', B, A, B) / np.einsum('ij,jk,ik->i', B, K, B)
        with np.errstate(divide='ignore', invalid='ignore'):
            ex = np.where(mub > 0, 0.5 * np.log2(1 + Delta / mub), np.inf) - Lmin
        worst = np.maximum(worst, ex)
    bd, thd = minimax_bound(S, Q, J, D1, D2)
    ok5 = ok5 and worst.min() >= bd - 1e-9
    print(f"   ({rho2}, {tau2}, {D1}, {D2}): angle {thd:.1f} deg, best fixed read pays {worst.min():.4f} bits, bound {bd:.4f}, L = {Ls[0]:.4f}, {Ls[1]:.4f}")
check("F5 scalar minimax >= bound", ok5)
print("FAILS:", fails)
