"""Rank-one regime boundary and frame non-determination, 2026-10-01."""
import numpy as np, math
from scipy.optimize import minimize
LN2 = math.log(2); rng = np.random.default_rng(5)

def model(sig2, ang, c, tau2):
    u = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
    ST = np.zeros((3, 3)); ST[:2, :2] = np.diag(sig2); ST[:2, 2] = ST[2, :2] = c * u; ST[2, 2] = 1.0
    assert np.linalg.eigvalsh(ST).min() > 0
    J = np.zeros((3, 3)); J[2, 2] = 1 / tau2; K = np.linalg.inv(np.linalg.inv(ST) + J)
    return ST, J, K

E = np.zeros((2, 3)); E[:, :2] = np.eye(2)
def rank1(ST, K, D):
    w, U = np.linalg.eigh(ST); Sh = U @ np.diag(w ** 0.5) @ U.T; Shi = np.linalg.inv(Sh)
    M = Shi @ K @ Shi; A = Sh @ E.T @ E @ Sh; Delta = np.trace(ST[:2, :2]) - D
    w2, U2 = np.linalg.eigh(M); Mih = U2 @ np.diag(w2 ** -0.5) @ U2.T
    cw, cV = np.linalg.eigh(Mih @ (A - Delta * np.eye(3)) @ Mih)
    if cw[-1] <= 0: return None
    x = Mih @ cV[:, -1]; x /= np.linalg.norm(x)
    a = x @ A @ x; q = Delta / (a - Delta)          # whitened: x unit, q from active distortion
    b = Shi @ x                                    # description direction in T (W = b^T T + noise), Q = q b b^T
    Q = q * np.outer(b, b)
    P = np.linalg.inv(np.linalg.inv(ST) + Q)
    L = 0.5 * math.log2(1 + Delta / cw[-1])
    return L, b, Q, P, Delta

def kkt(ST, J, K, D):
    r = rank1(ST, K, D)
    if r is None: return None
    L, b, Q, P, Delta = r
    PS = np.linalg.inv(np.linalg.inv(P) + J); G = P @ E.T @ E @ P
    mu = 0.5 * (b @ PS @ b) / (b @ G @ b)
    Gam = 0.5 * PS - mu * G
    return L, np.linalg.eigvalsh(Gam).min(), np.linalg.norm(Gam @ b) / np.linalg.norm(b), b

def content(P, K, J): return 0.5 * (np.linalg.slogdet(K)[1] + np.linalg.slogdet(np.linalg.inv(P) + J)[1]) / LN2
def full_opt(ST, J, K, D, starts=12):
    best = np.inf; Pb = None
    Pf = lambda g: np.linalg.inv(np.linalg.inv(ST) + g.reshape(3, 3).T @ g.reshape(3, 3))
    for _ in range(starts):
        r = minimize(lambda g: content(Pf(g), K, J), rng.normal(0, 1.5, 9), method='SLSQP',
                     constraints=[{'type': 'ineq', 'fun': lambda g: D - np.trace(Pf(g)[:2, :2])}],
                     options={'maxiter': 3000, 'ftol': 1e-13})
        if r.success and np.trace(Pf(r.x)[:2, :2]) <= D + 1e-8 and r.fun < best: best, Pb = r.fun, Pf(r.x)
    Qv = np.sort(np.linalg.eigvalsh(np.linalg.inv(Pb) - np.linalg.inv(ST)))[::-1]
    return best, int(np.sum(Qv > 1e-5 * Qv[0]))

print("(A) KKT certificate for the rank-one candidate vs optimizer rank")
agree = True
for ang, c, t2 in [(50, 0.6, 0.05), (50, 0.6, 0.3), (30, 0.6, 1.0), (70, 0.55, 0.1)]:
    ST, J, K = model([1.0, 0.4], ang, c, t2)
    trY = 1.4; Ds = np.linspace(trY - 0.02, 0.45, 24)
    cross = None
    for D in Ds:
        k = kkt(ST, J, K, D)
        cert = (k is not None) and k[1] > -1e-9 and k[2] < 1e-7
        fv, rk = full_opt(ST, J, K, D)
        if cert and abs(k[0] - fv) > 1e-6: agree = False
        if (rk == 1) != cert: agree = False; print(f"   mismatch at D={D:.3f}: cert={cert} rank={rk}")
        if not cert and cross is None: cross = D
    print(f"  ang={ang} c={c} tau2={t2}: certificate fails first at D~{cross:.3f}")
print("PASS" if agree else "FAIL", "(A) certificate <=> optimizer rank one, values equal")

print("(B) read direction vs D (degrees in Y-plane); rate-optimal is 0 for Sigma_Y = diag(1,0.4)")
ST, J, K = model([1.0, 0.4], 50, 0.6, 0.05)
for D in [1.38, 1.3, 1.2, 1.1, 1.0]:
    k = kkt(ST, J, K, D)
    if k is None: continue
    d = ST[:2, :] @ k[3]; print(f"  D={D}: read angle {math.degrees(math.atan2(d[1], d[0])) % 180:6.2f}  L={k[0]:.5f}  cert={k[1] > -1e-9}")

print("(C) same (Y,S) law, different (c,tau2): c^2/(1+tau2) fixed = 0.3")
for c2, t2 in [(0.30, 1e-6), (0.33, 0.1), (0.36, 0.2)]:
    ST, J, K = model([1.0, 0.4], 50, math.sqrt(c2), t2)
    SYS = ST[:2, :2] - np.outer(ST[:2, 2], ST[:2, 2]) / (1 + t2)
    for D in [1.3, 1.15]:
        k = kkt(ST, J, K, D); d = ST[:2, :] @ k[3]
        print(f"  c2={c2} tau2={t2} D={D}: L={k[0]:.5f} read angle {math.degrees(math.atan2(d[1], d[0])) % 180:6.2f} cert={k[1] > -1e-9}  Cov(Y,S) law fixed: {np.round(ST[:2,2]/math.sqrt(1+t2),4)}")
