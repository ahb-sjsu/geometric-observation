"""Checks for Section VIII (coupled described variables) of tit-cr-context-r2.tex, 2026-10-01.
Run on Atlas with numpy, scipy, sympy, cvxpy (clarabel).
  C1 scalar: det(A(Delta) - mu K) = 0 at mu = Delta/(g-1) is proportional to P(g)  (symbolic)
  C2 max-det program == brute-force optimum over Gaussian descriptions (random coupled instances)
  C3 one-dimensional value == max-det optimum whenever the certificate holds, and not otherwise
  C4 turning example numbers;  C5 same (Y,S) law, different read directions
"""
import numpy as np, math
import sympy as sp
from scipy.optimize import minimize
import cvxpy as cp
LN2 = math.log(2); rng = np.random.default_rng(20261001)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)

# C1 symbolic
r, s, D, mu, g = sp.symbols('rho s D mu g', real=True)
ST = sp.Matrix([[1, r], [r, 1]]); J = sp.Matrix([[0, 0], [0, 1 / (s - 1)]])
K = sp.simplify((ST.inv() + J).inv()); Delta = 1 - D
A = ST * sp.Matrix([[1, 0], [0, 0]]) * ST - Delta * ST
char = sp.simplify((A - mu * K).det())
sub = sp.factor(sp.together(char.subs(mu, Delta / (g - 1))))
Pg = D * s * g**2 - (D + s - r**2) * g + (1 - r**2)
ratio = sp.factor(sp.simplify(sub * (g - 1)**2 / Pg))
check("C1 scalar: det(A - mu K) at mu = Delta/(g-1) equals P(g) times a g-free factor over (g-1)^2", not ratio.has(g), f"factor = {ratio}")

E2 = None
def setup(SY, CYV, SV, SU):
    m, rr = SY.shape[0], SV.shape[0]; p = m + rr
    STn = np.zeros((p, p)); STn[:m, :m] = SY; STn[:m, m:] = CYV; STn[m:, :m] = CYV.T; STn[m:, m:] = SV
    assert np.linalg.eigvalsh(STn).min() > 0
    Jn = np.zeros((p, p)); Jn[m:, m:] = np.linalg.inv(SU)
    Kn = np.linalg.inv(np.linalg.inv(STn) + Jn)
    En = np.zeros((m, p)); En[:, :m] = np.eye(m)
    return STn, Jn, Kn, En

def maxdet(STn, Jn, Kn, En, Dv):
    p = STn.shape[0]; m = En.shape[0]
    w, U = np.linalg.eigh(Jn); Jh = U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T
    X = cp.Variable((p, p), symmetric=True); Z = cp.Variable((m, m), symmetric=True)
    blk = cp.bmat([[Z - En @ X @ En.T, En @ X @ Jh], [Jh @ X @ En.T, np.eye(p) - Jh @ X @ Jh]])
    prob = cp.Problem(cp.Maximize(cp.log_det(X)), [0.5 * (blk + blk.T) >> 0, cp.trace(Z) <= Dv, Kn - X >> 0])
    prob.solve(solver=cp.CLARABEL)
    return 0.5 * (np.linalg.slogdet(Kn)[1] - np.linalg.slogdet(X.value)[1]) / LN2

def brute(STn, Jn, Kn, En, Dv, starts=16):
    p = STn.shape[0]; m = En.shape[0]; best = np.inf
    Pf = lambda gg: np.linalg.inv(np.linalg.inv(STn) + gg.reshape(p, p).T @ gg.reshape(p, p))
    f = lambda gg: 0.5 * (np.linalg.slogdet(Kn)[1] + np.linalg.slogdet(np.linalg.inv(Pf(gg)) + Jn)[1]) / LN2
    for _ in range(starts):
        res = minimize(f, rng.normal(0, 1.5, p * p), method='SLSQP',
                       constraints=[{'type': 'ineq', 'fun': lambda gg: Dv - np.trace(En @ Pf(gg) @ En.T)}],
                       options={'maxiter': 4000, 'ftol': 1e-13})
        if res.success and np.trace(En @ Pf(res.x) @ En.T) <= Dv + 1e-8: best = min(best, res.fun)
    return best

def one_dim(STn, Jn, Kn, En, Dv):
    Delta = np.trace(En @ STn @ En.T) - Dv
    A = STn @ En.T @ En @ STn - Delta * STn
    w, U = np.linalg.eigh(Kn); Kih = U @ np.diag(w ** -0.5) @ U.T
    cw, cV = np.linalg.eigh(Kih @ A @ Kih)
    if cw[-1] <= 0: return None
    b = Kih @ cV[:, -1]; mu_max = cw[-1]
    sig2 = (np.linalg.norm(En @ STn @ b) ** 2) / Delta - b @ STn @ b
    P = STn - np.outer(STn @ b, STn @ b) / (b @ STn @ b + sig2)
    X = np.linalg.inv(np.linalg.inv(P) + Jn)
    G = P @ En.T @ En @ P; mus = 0.5 * (b @ X @ b) / (b @ G @ b)
    Gam = 0.5 * X - mus * G
    cert = np.linalg.eigvalsh(Gam).min() > -1e-10 * np.abs(np.linalg.eigvalsh(Gam)).max()
    L1 = 0.5 * math.log2(1 + Delta / mu_max)
    ydir = En @ STn @ b
    return L1, cert, np.linalg.norm(Gam @ b) / np.linalg.norm(b), math.degrees(math.atan2(ydir[1], ydir[0])) % 180 if len(ydir) > 1 else None

# C2 + C3 random coupled instances
worst2 = 0; c3ok = True; n = 0
for m, rr in [(2, 1), (2, 2), (3, 1), (3, 2)]:
    for _ in range(4):
        p = m + rr
        while True:
            Am = rng.normal(size=(p, p)); S_ = Am @ Am.T / p + 0.15 * np.eye(p); d = np.sqrt(np.diag(S_)); S_ = S_ / np.outer(d, d)
            if np.linalg.eigvalsh(S_).min() > 0.05: break
        STn, Jn, Kn, En = setup(S_[:m, :m], S_[:m, m:], S_[m:, m:], np.diag(10 ** rng.uniform(-1.3, 0.3, rr)))
        for frac in [0.92, 0.6]:
            Dv = frac * m
            v = maxdet(STn, Jn, Kn, En, Dv); bv = brute(STn, Jn, Kn, En, Dv); worst2 = max(worst2, abs(v - bv)); n += 1
            od = one_dim(STn, Jn, Kn, En, Dv)
            if od is not None:
                if od[1] and abs(od[0] - v) > 1e-6: c3ok = False
                if (not od[1]) and od[0] < v - 1e-7: c3ok = False
                if od[1] and od[2] > 1e-6: c3ok = False
check(f"C2 max-det == brute force over Gaussian descriptions ({n} cases)", worst2 < 1e-5, f"max |diff| {worst2:.2e}")
check("C3 certificate => one-dimensional value equals the optimum (and Gamma b = 0); no certificate => one-dimensional value not below optimum", c3ok)

# C4 turning example
SY = np.diag([1.0, 0.4]); u = np.array([math.cos(math.radians(50)), math.sin(math.radians(50))])
STn, Jn, Kn, En = setup(SY, 0.6 * u.reshape(2, 1), np.eye(1), np.array([[0.05]]))
print("C4 turning example: Sigma_Y = diag(1,0.4), Cov(Y,V) = 0.6 u(50 deg), tau^2 = 0.05")
for Dv in [1.38, 1.3, 1.2, 1.1, 1.06, 1.05]:
    od = one_dim(STn, Jn, Kn, En, Dv); md = maxdet(STn, Jn, Kn, En, Dv)
    print(f"   D={Dv}: one-dim L={od[0]:.5f}  optimum L={md:.5f}  certificate={od[1]}  read angle (Y-plane) {od[3]:.2f} deg")
# certificate boundary by bisection
lo, hi = 0.9, 1.38
for _ in range(50):
    mid = 0.5 * (lo + hi)
    if one_dim(STn, Jn, Kn, En, mid)[1]: hi = mid
    else: lo = mid
print(f"   certificate boundary D_1 = {hi:.4f}")

# C5 same (Y,S) law, different split: Cov(Y,S) = c u, Var S = 1 + tau2; normalize S -> fixed c/sqrt(1+tau2) = sqrt(0.3)
print("C5 same (Y,S) law (Corr direction u at 50 deg, c^2/(1+tau^2) = 0.3), D = 1.3")
for c2, t2 in [(0.33, 0.1), (0.36, 0.2), (0.39, 0.3), (0.42, 0.4)]:
    STn, Jn, Kn, En = setup(SY, math.sqrt(c2) * u.reshape(2, 1), np.eye(1), np.array([[t2]]))
    od = one_dim(STn, Jn, Kn, En, 1.3); md = maxdet(STn, Jn, Kn, En, 1.3)
    print(f"   (c^2,tau^2)=({c2},{t2}): L={md:.5f} one-dim={od[0]:.5f} cert={od[1]} read angle {od[3]:.2f} deg")
print("FAILS:", fails)
