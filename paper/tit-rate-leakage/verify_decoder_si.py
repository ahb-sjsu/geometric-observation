"""Checks for the decoder-side-information (degraded) theorem, 2026-10-01.
D1 key inequality for a NON-Gaussian description: scalar T ~ N(0,1), V = sign(T + w) with w ~ N(0, s_w^2),
   C = T + N(0, s_c^2), S = T + N(0, s_s^2), s_s < s_c (holder dominates, J_S >= J_C).
   M_C = E Var(T|V,C), M_S = E Var(T|V,S) by numerical integration;
   check M_S <= 1/(1/M_C + J_S - J_C)  and  leakage bound I(T;V|S) >= 1/2 log(Var(T|S)/M_S).
D2 reduction algebra (Gaussian descriptions, vector): with P = Cov(T|V), M_C = (P^-1 + J_C)^-1, M_S = (P^-1 + J_S)^-1,
   the triple (I(T;V|C), I(T;V|S), tr(Q M_C)) equals the no-side-information triple (r', l', tr(Q P'))
   of the conditional source Sigma' = Sigma_{T|C}, holder information J' = J_S - J_C, at P' = M_C.
D3 minimum leakage with decoder side information (Gaussian V, brute force over G) equals the reduced
   no-side-information optimum computed by the max-det program on (Sigma', J').
"""
import numpy as np, math
from scipy import integrate
from scipy.stats import norm
from scipy.optimize import minimize
import cvxpy as cp
LN2 = math.log(2); rng = np.random.default_rng(101)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)

# D1: posterior of T given (V=v, Y=y) where Y = T + N(0, s^2): density ~ phi(t) * Phi(v*t/s_w) * phi((y-t)/s)
def post_moments(v, y, s, s_w):
    f = lambda t: norm.pdf(t) * norm.cdf(v * t / s_w) * norm.pdf((y - t) / s)
    lo, hi = min(-8, y - 8 * s), max(8, y + 8 * s)
    z = integrate.quad(f, lo, hi, limit=200)[0]
    m1 = integrate.quad(lambda t: t * f(t), lo, hi, limit=200)[0] / z
    m2 = integrate.quad(lambda t: t * t * f(t), lo, hi, limit=200)[0] / z
    return m2 - m1 * m1, z

def expected_post_var(s, s_w, ngrid=161):
    # E over (V, Y) of Var(T | V, Y); joint density of (V=v, Y=y) is the normalizer z / s (Y density) ...
    tot = 0.0
    ys = np.linspace(-7 * math.sqrt(1 + s * s), 7 * math.sqrt(1 + s * s), ngrid); dy = ys[1] - ys[0]
    for v in (-1, 1):
        for y in ys:
            var, z = post_moments(v, y, s, s_w)
            tot += var * (z / s) * dy      # p(v, y) = int phi(t) Phi(v t/s_w) phi((y-t)/s)/s dt
    return tot

def mutual_info_TV_given_Y(s, s_w, ngrid=121):
    # I(T;V|Y) = H(V|Y) - H(V|T)
    ys = np.linspace(-7 * math.sqrt(1 + s * s), 7 * math.sqrt(1 + s * s), ngrid); dy = ys[1] - ys[0]
    HVgY = 0.0
    for y in ys:
        ps = []
        for v in (-1, 1):
            f = lambda t: norm.pdf(t) * norm.cdf(v * t / s_w) * norm.pdf((y - t) / s) / s
            ps.append(integrate.quad(f, -10, 10, limit=200)[0])
        py = sum(ps)
        for pv in ps:
            if pv > 0: HVgY -= pv * math.log2(pv / py) * dy
    HVgT = integrate.quad(lambda t: norm.pdf(t) * (lambda q: -(q * math.log2(q) + (1 - q) * math.log2(1 - q)) if 0 < q < 1 else 0.0)(norm.cdf(t / s_w)), -10, 10, limit=200)[0]
    return HVgY - HVgT

ok = True
for s_w, s_c, s_s in [(0.5, 1.0, 0.5), (0.3, 2.0, 0.7), (1.0, 1.5, 0.4)]:
    MC = expected_post_var(s_c, s_w); MS = expected_post_var(s_s, s_w)
    JC, JS = 1 / s_c**2, 1 / s_s**2
    bound = 1 / (1 / MC + JS - JC)
    lhs_ok = MS <= bound + 1e-6
    I = mutual_info_TV_given_Y(s_s, s_w); lb = 0.5 * math.log2((1 / (1 + JS)) / MS)
    ok = ok and lhs_ok and (I >= lb - 1e-4)
    print(f"   s_w={s_w} s_c={s_c} s_s={s_s}: M_C={MC:.5f} M_S={MS:.5f} bound={bound:.5f}  I(T;V|S)={I:.5f} >= {lb:.5f}")
check("D1 non-Gaussian description: M_S <= (M_C^-1 + J_S - J_C)^-1 and the leakage lower bound", ok)

# D2, D3: vector reduction
def instance(p):
    A = rng.normal(size=(p, p)); Sig = A @ A.T / p + 0.3 * np.eye(p)
    B = rng.normal(size=(p, p)); JC = B @ B.T / p * 0.6
    Ex = rng.normal(size=(p, p)); JS = JC + Ex @ Ex.T / p * 0.8     # holder dominates
    Wm = rng.normal(size=(p, p)); Q = Wm @ Wm.T / p * 0.5 + np.diag([1.0] + [0.0] * (p - 1))
    return Sig, JC, JS, Q
ld = lambda M: np.linalg.slogdet(M)[1] / LN2
ok2 = True; ok3 = True; worst3 = 0
for _ in range(10):
    p = 3; Sig, JC, JS, Q = instance(p)
    KC = np.linalg.inv(np.linalg.inv(Sig) + JC); KS = np.linalg.inv(np.linalg.inv(Sig) + JS)
    # D2 on random Gaussian descriptions
    for _ in range(20):
        G = rng.normal(size=(p, p)); P = np.linalg.inv(np.linalg.inv(Sig) + G.T @ G)
        MC = np.linalg.inv(np.linalg.inv(P) + JC); MS = np.linalg.inv(np.linalg.inv(P) + JS)
        R, L, Dd = 0.5 * (ld(KC) - ld(MC)), 0.5 * (ld(KS) - ld(MS)), np.trace(Q @ MC)
        Sp, Jp = KC, JS - JC; Kp = np.linalg.inv(np.linalg.inv(Sp) + Jp)
        Pp = MC
        r2 = 0.5 * (ld(Sp) - ld(Pp)); l2 = 0.5 * (ld(Kp) - ld(np.linalg.inv(np.linalg.inv(Pp) + Jp))); D2 = np.trace(Q @ Pp)
        ok2 = ok2 and abs(R - r2) < 1e-10 and abs(L - l2) < 1e-10 and abs(Dd - D2) < 1e-10 and np.linalg.norm(Kp - KS) < 1e-10
    # D3 min leakage: brute force over Gaussian G vs reduced max-det
    D = 0.5 * np.trace(Q @ KC)
    def Lval(g):
        G = g.reshape(p, p); P = np.linalg.inv(np.linalg.inv(Sig) + G.T @ G)
        MS = np.linalg.inv(np.linalg.inv(P) + JS); return 0.5 * (ld(KS) - ld(MS))
    def Dval(g):
        G = g.reshape(p, p); P = np.linalg.inv(np.linalg.inv(Sig) + G.T @ G)
        return np.trace(Q @ np.linalg.inv(np.linalg.inv(P) + JC))
    best = np.inf
    for _ in range(14):
        res = minimize(Lval, rng.normal(0, 1.5, p * p), method='SLSQP', constraints=[{'type': 'ineq', 'fun': lambda g: D - Dval(g)}],
                       options={'maxiter': 4000, 'ftol': 1e-14})
        if res.success and Dval(res.x) <= D + 1e-8: best = min(best, res.fun)
    Sp, Jp = KC, JS - JC; Kp = KS
    w, U = np.linalg.eigh(Jp); Jh = U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T
    X = cp.Variable((p, p), symmetric=True); Z = cp.Variable((p, p), symmetric=True)
    blk = cp.bmat([[Z - X, X @ Jh], [Jh @ X, np.eye(p) - Jh @ X @ Jh]])
    prob = cp.Problem(cp.Maximize(cp.log_det(X)), [0.5 * (blk + blk.T) >> 0, cp.trace(Q @ Z) <= D, Kp - X >> 0])
    prob.solve(solver=cp.CLARABEL)
    md = 0.5 * (ld(Kp) - np.linalg.slogdet(X.value)[1] / LN2)
    worst3 = max(worst3, abs(md - best)); ok3 = ok3 and abs(md - best) < 1e-5
check("D2 reduction algebra: decoder-SI triple == no-SI triple of (Sigma_{T|C}, J_S - J_C) (200 descriptions)", ok2)
check("D3 min leakage with decoder SI (Gaussian brute force) == reduced max-det (10 cases)", ok3, f"max |diff| {worst3:.2e}")
print("FAILS:", fails)
