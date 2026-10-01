"""Rank-one (pencil) characterization checks, 2026-10-01.
Claim: when the content-optimal description is one-dimensional, its direction x (whitened, x = Sigma^{1/2} b)
minimizes x^T M x / x^T (A - Delta I) x with M = Sigma^{-1/2} K Sigma^{-1/2}, A = Sigma^{1/2} E^T E Sigma^{1/2},
Delta = tr Sigma_Y - D, and L = 1/2 log2(1 + Delta * lambda_min).
"""
import numpy as np, math
from scipy.linalg import eigh, sqrtm
from scipy.optimize import minimize
LN2 = math.log(2); rng = np.random.default_rng(11)

def gstar(d, r2, s):
    B = d + s - r2; return (B + math.sqrt(B * B - 4 * d * s * (1 - r2))) / (2 * d * s)

def pencil_value(ST, K, m, D):
    p = ST.shape[0]; E = np.zeros((m, p)); E[:, :m] = np.eye(m)
    Sh = np.real(sqrtm(ST)); Shi = np.linalg.inv(Sh)
    M = Shi @ K @ Shi; A = Sh @ E.T @ E @ Sh
    Delta = np.trace(ST[:m, :m]) - D
    B = A - Delta * np.eye(p)
    w, U = np.linalg.eigh(M); Mih = U @ np.diag(w ** -0.5) @ U.T
    cw, cV = np.linalg.eigh(Mih @ B @ Mih)
    if cw[-1] <= 1e-12:
        return float('nan'), float('nan'), None, Delta     # rank-one description cannot meet the budget
    lam = 1.0 / cw[-1]; x = Mih @ cV[:, -1]
    return 0.5 * math.log2(1 + Delta * lam), lam, Sh @ x, Delta   # Sh@x = Sigma b direction in T-space

fails = 0
def check(n, ok, info=""):
    global fails; print(("PASS " if ok else "FAIL ") + n + "  " + info); fails += (not ok)

# (a) scalar: pencil value equals the closed form
worst = 0
for _ in range(500):
    r2 = rng.uniform(0, 0.95); t2 = 10 ** rng.uniform(-2, 1); D = rng.uniform(0.05, 0.95); r = math.sqrt(r2)
    ST = np.array([[1, r], [r, 1.0]]); J = np.diag([0, 1 / t2]); K = np.linalg.inv(np.linalg.inv(ST) + J)
    v, lam, _, Dl = pencil_value(ST, K, 1, D)
    worst = max(worst, abs(v - 0.5 * math.log2(gstar(D, r2, 1 + t2))))
check("(a) scalar: 1/2 log2(1 + Delta lambda_min) == closed form (500 random)", worst < 1e-9, f"max abs err {worst:.2e}")

# (b) coupled m=2, scalar V: pencil value vs full optimizer over all descriptions, high D
def model(sig2, ang, c, tau2):
    u = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
    ST = np.zeros((3, 3)); ST[:2, :2] = np.diag(sig2); ST[:2, 2] = ST[2, :2] = c * u; ST[2, 2] = 1.0
    J = np.zeros((3, 3)); J[2, 2] = 1 / tau2; K = np.linalg.inv(np.linalg.inv(ST) + J)
    return ST, J, K
def content(P, K, J): return 0.5 * (np.linalg.slogdet(K)[1] + np.linalg.slogdet(np.linalg.inv(P) + J)[1]) / LN2
def full_opt(ST, J, K, D, starts=16):
    best = np.inf; Pb = None
    for _ in range(starts):
        g0 = rng.normal(0, 1.5, 9)
        Pf = lambda g: np.linalg.inv(np.linalg.inv(ST) + g.reshape(3, 3).T @ g.reshape(3, 3))
        r = minimize(lambda g: content(Pf(g), K, J), g0, method='SLSQP',
                     constraints=[{'type': 'ineq', 'fun': lambda g: D - np.trace(Pf(g)[:2, :2])}],
                     options={'maxiter': 3000, 'ftol': 1e-13})
        if r.success and np.trace(Pf(r.x)[:2, :2]) <= D + 1e-8 and r.fun < best:
            best = r.fun; Pb = Pf(r.x)
    return best, Pb
rows = []
for ang, c, t2 in [(50, 0.6, 0.05), (50, 0.6, 0.3), (30, 0.6, 1.0), (70, 0.55, 0.1)]:
    ST, J, K = model([1.0, 0.4], ang, c, t2)
    assert np.linalg.eigvalsh(ST).min() > 0, 'Sigma_T not PD'
    for D in [1.3, 1.1, 0.9, 0.7, 0.5, 0.3]:
        pv, lam, dirT, Dl = pencil_value(ST, K, 2, D)
        fv, P = full_opt(ST, J, K, D)
        Q = np.linalg.inv(P) - np.linalg.inv(ST); ev = np.sort(np.linalg.eigvalsh(Q))[::-1]
        rank = int(np.sum(ev > 1e-6 * max(ev[0], 1e-12)))
        a = float('nan') if dirT is None else math.degrees(math.atan2(dirT[1], dirT[0])) % 180
        rows.append((ang, c, t2, D, pv, fv, rank, a))
        print(f"  ang={ang} c={c} tau2={t2} D={D}: pencil {pv:.6f}  full {fv:.6f}  diff {pv-fv:+.2e}  rank(Q)={rank}  read angle in Y {a:6.2f}")
ok = all((r[6] == 1 and abs(r[4] - r[5]) < 1e-5) or (r[6] > 1 and (math.isnan(r[4]) or r[4] >= r[5] - 1e-6)) for r in rows)
check("(b) pencil == full optimum whenever optimum is rank one; pencil >= optimum otherwise", ok)
print("FAILS:", fails)
