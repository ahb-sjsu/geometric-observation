"""Checks for Proposition prop:pencil of tit-cr-context-r2.tex (Section VI), 2026-10-01.
Run on Atlas with numpy, scipy, sympy.
  P1 scalar: det(A_D - mu Sigma_{T|S}) at mu = (1-D)/(g-1) equals P(g) times a g-free factor over (g-1)^2
  P2 scalar: 1/2 log2(1 + (1-D)/mu_max) equals 1/2 log2 g* (random parameters)
  P3 vector context (r = 1, 2, 3): pencil value equals direct minimization over scalar Gaussian channels
"""
import numpy as np, math
import sympy as sp
from scipy.optimize import minimize
LN2 = math.log(2); rng = np.random.default_rng(20261002)
fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + ("  " + info if info else "")); fails += (not ok)

r, s, D, mu, g = sp.symbols('rho s D mu g', real=True)
ST = sp.Matrix([[1, r], [r, 1]]); J = sp.Matrix([[0, 0], [0, 1 / (s - 1)]])
K = sp.simplify((ST.inv() + J).inv())
A = ST * sp.Matrix([[1, 0], [0, 0]]) * ST - (1 - D) * ST
sub = sp.factor(sp.together((A - mu * K).det().subs(mu, (1 - D) / (g - 1))))
Pg = D * s * g**2 - (D + s - r**2) * g + (1 - r**2)
fac = sp.factor(sp.simplify(sub * (g - 1)**2 / Pg))
check("P1 scalar identity", not fac.has(g), f"factor = {fac}")

def pencil(STn, Kn, Dv):
    e = np.zeros(STn.shape[0]); e[0] = 1
    A = STn @ np.outer(e, e) @ STn - (1 - Dv) * STn
    w, U = np.linalg.eigh(Kn); Kih = U @ np.diag(w ** -0.5) @ U.T
    return 0.5 * math.log2(1 + (1 - Dv) / np.linalg.eigvalsh(Kih @ A @ Kih)[-1])

def gstar(d, r2, ss):
    Bq = d + ss - r2; return (Bq + math.sqrt(Bq * Bq - 4 * d * ss * (1 - r2))) / (2 * d * ss)
worst = 0
for _ in range(500):
    r2 = rng.uniform(0, 0.95); t2 = 10 ** rng.uniform(-2, 1); Dv = rng.uniform(0.02, 0.98); rr = math.sqrt(r2)
    STn = np.array([[1, rr], [rr, 1.0]]); Kn = np.linalg.inv(np.linalg.inv(STn) + np.diag([0, 1 / t2]))
    worst = max(worst, abs(pencil(STn, Kn, Dv) - 0.5 * math.log2(gstar(Dv, r2, 1 + t2))))
check("P2 scalar pencil value == closed form (500 random)", worst < 1e-10, f"max abs err {worst:.2e}")

worst = 0; n = 0
for rdim in [1, 2, 3]:
    for _ in range(6):
        p = 1 + rdim
        while True:
            Am = rng.normal(size=(p, p)); S_ = Am @ Am.T / p + 0.2 * np.eye(p); d = np.sqrt(np.diag(S_)); S_ = S_ / np.outer(d, d)
            if np.linalg.eigvalsh(S_).min() > 0.05: break
        SU = np.diag(10 ** rng.uniform(-1.3, 0.5, rdim))
        Jn = np.zeros((p, p)); Jn[1:, 1:] = np.linalg.inv(SU)
        Kn = np.linalg.inv(np.linalg.inv(S_) + Jn)
        Dv = rng.uniform(0.05, 0.95)
        pv = pencil(S_, Kn, Dv)
        def obj(x):
            b = x[:p]; s2 = math.exp(x[p]); return 0.5 * math.log2(1 + b @ Kn @ b / s2)
        def con(x):
            b = x[:p]; s2 = math.exp(x[p]); return Dv - (1 - (S_[0] @ b) ** 2 / (b @ S_ @ b + s2))
        best = np.inf
        for _r in range(20):
            res = minimize(obj, np.concatenate([rng.normal(size=p), [rng.normal()]]), method='SLSQP',
                           constraints=[{'type': 'ineq', 'fun': con}], options={'maxiter': 3000, 'ftol': 1e-14})
            if res.success and con(res.x) > -1e-9: best = min(best, res.fun)
        worst = max(worst, abs(pv - best)); n += 1
check(f"P3 vector context: pencil == direct minimization ({n} cases, r=1..3)", worst < 1e-6, f"max abs err {worst:.2e}")
print("FAILS:", fails)
