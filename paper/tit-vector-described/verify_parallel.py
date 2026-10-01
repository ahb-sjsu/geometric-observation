"""Checks for Section III (parallel described variables) of tit-vector.tex, 2026-10-01.
Run on Atlas: PYTHONPATH with sympy; numpy, scipy.

Per coordinate j: Var Y_j = sig2_j, Var V_j = 1, corr rho_j, S_j = V_j + U_j, U_j ~ N(0, tau2_j).
Scalar function (normalized delta = D_j / sig2_j): ell(delta) = 0.5 log2 g*, P(g) = d s g^2 - (d+s-rho^2) g + (1-rho^2).
Claims checked:
 C1 slope formula  ell'(d) = - g k / (2 ln2 (d s g^2 - 1 + rho^2)),  k = g s - 1
 C2 endpoint slope ell'(1-) = - tau2 / (2 ln2 (tau2 + rho^2))
 C3 ell convex (and strictly) on (0,1): sign of ell'' on a dense grid + random params; symbolic attempt
 C4 allocation by equal slopes == brute-force grid minimum (m=2,3)
 C5 no jointly Gaussian vector channel (correlated across coordinates) beats the allocation value (m=2)
 C6 the activation-order inversion example
"""
import numpy as np, math, sys
from scipy.optimize import brentq, minimize
import sympy as sp

LN2 = math.log(2)
rng = np.random.default_rng(20261001)

def gstar(d, rho2, s):
    B = d + s - rho2
    return (B + math.sqrt(B * B - 4 * d * s * (1 - rho2))) / (2 * d * s)

def ell(d, rho2, tau2):
    if d >= 1: return 0.0
    return 0.5 * math.log2(gstar(d, rho2, 1 + tau2))

def ellp(d, rho2, tau2):
    s = 1 + tau2; g = gstar(d, rho2, s); k = g * s - 1
    return -g * k / (2 * LN2 * (d * s * g * g - 1 + rho2))

def rate_content_channel(d, rho2, tau2):
    if d >= 1: return 0.0
    s = 1 + tau2; g = gstar(d, rho2, s); k = g * s - 1; r = math.sqrt(rho2)
    a = (g - 1) / g; b = (g - 1) * r / (g * k)
    Q0 = a * a + b * b + 2 * a * b * r; Q1 = Q0 - (a * r + b) ** 2 / s; nu = Q1 / (g - 1)
    return 0.5 * math.log2((Q0 + nu) / nu)

fails = 0
def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("  " + info if info else ""))
    if not ok: fails += 1

# C1
worst = 0
for _ in range(2000):
    rho2 = rng.uniform(0, 0.99); tau2 = 10 ** rng.uniform(-3, 1); d = rng.uniform(0.01, 0.99)
    h = 1e-6 * d
    fd = (ell(d + h, rho2, tau2) - ell(d - h, rho2, tau2)) / (2 * h)
    worst = max(worst, abs(fd - ellp(d, rho2, tau2)) / abs(fd))
check("C1 slope formula vs central difference (2000 random points)", worst < 1e-5, f"max rel err {worst:.2e}")

# C2
worst = 0
for _ in range(500):
    rho2 = rng.uniform(0, 0.99); tau2 = 10 ** rng.uniform(-3, 1)
    lim = -tau2 / (2 * LN2 * (tau2 + rho2))
    worst = max(worst, abs(ellp(1 - 1e-9, rho2, tau2) - lim) / abs(lim))
check("C2 endpoint slope at delta -> 1", worst < 1e-6, f"max rel err {worst:.2e}")

# C3 convexity: second difference
minsec = np.inf
for _ in range(400):
    rho2 = rng.uniform(0, 0.999); tau2 = 10 ** rng.uniform(-4, 2)
    ds = np.linspace(1e-3, 1 - 1e-3, 400)
    sl = np.array([ellp(d, rho2, tau2) for d in ds])
    minsec = min(minsec, np.min(np.diff(sl)))
check("C3 slope increasing on (0,1) (ell convex), 400 random (rho2,tau2)", minsec > 0, f"min slope increment {minsec:.3e}")

# C3 symbolic: ell'' sign via implicit differentiation
g, d, s, r2 = sp.symbols('g d s r2', positive=True)
P = d * s * g**2 - (d + s - r2) * g + (1 - r2)
gp = -sp.diff(P, d) / sp.diff(P, g)
gpp = sp.simplify((sp.diff(gp, d) + sp.diff(gp, g) * gp))
lnpp = sp.simplify(gpp / g - gp**2 / g**2)      # (ln g)'' ; ell'' = lnpp / (2 ln 2)
num, den = sp.fraction(sp.together(lnpp))
print("C3 symbolic (ln g)'' numerator:", sp.factor(num))
print("C3 symbolic (ln g)'' denominator:", sp.factor(den))
# also the slope identity symbolically, using P(g)=0 to eliminate (d+s-r2)
lp_formula = -g * (g * s - 1) / (d * s * g**2 - 1 + r2)
diffexpr = sp.simplify((gp / g).subs(d, sp.solve(P, d)[0]) - lp_formula.subs(d, sp.solve(P, d)[0]))
check("C1 symbolic slope identity on P(g)=0", diffexpr == 0, str(diffexpr))

# allocation
def alloc(params, D):
    """params: list of (sig2, rho2, tau2). Equal-slope allocation; returns (Ds, total L)."""
    tot = sum(p[0] for p in params)
    if D >= tot: return [p[0] for p in params], 0.0
    kap = [p[2] / (2 * LN2 * p[0] * (p[2] + p[1])) for p in params]
    def Dj(theta, p, kj):
        if theta <= kj: return p[0]
        f = lambda x: ellp(x, p[1], p[2]) / p[0] + theta
        lo, hi = 1e-14, 1 - 1e-12
        if f(lo) > 0: return lo * p[0]
        return brentq(f, lo, hi, xtol=1e-15) * p[0]
    def total(theta): return sum(Dj(theta, p, k) for p, k in zip(params, kap))
    lo, hi = min(kap) * (1 - 1e-12), 1.0
    while total(hi) > D: hi *= 2
    th = brentq(lambda t: total(t) - D, lo, hi, xtol=1e-15, rtol=1e-14)
    Ds = [Dj(th, p, k) for p, k in zip(params, kap)]
    return Ds, sum(ell(x / p[0], p[1], p[2]) for x, p in zip(Ds, params))

worst = 0
for _ in range(200):
    params = [(rng.uniform(0.2, 2), rng.uniform(0, 0.95), 10 ** rng.uniform(-2, 0.5)) for _ in range(2)]
    D = rng.uniform(0.05, 0.95) * sum(p[0] for p in params)
    Ds, val = alloc(params, D)
    grid = np.linspace(max(0, D - params[1][0]) + 1e-9, min(D, params[0][0]) - 1e-9, 20001)
    bf = min(ell(x / params[0][0], params[0][1], params[0][2]) + ell((D - x) / params[1][0], params[1][1], params[1][2]) for x in grid) if len(grid) else val
    worst = max(worst, val - bf)
check("C4 equal-slope allocation <= brute-force grid min + 1e-7 (m=2, 200 cases)", worst < 1e-7, f"max excess {worst:.2e}")

# C5 vector Gaussian channels with cross-coordinate correlation cannot beat the allocation
def joint_cov(params):
    m = len(params); p = 2 * m
    ST = np.zeros((p, p)); STS = np.zeros((p, m)); SS = np.zeros((m, m)); STY = np.zeros((p, m))
    for j, (sig2, rho2, tau2) in enumerate(params):
        r = math.sqrt(rho2); sg = math.sqrt(sig2)
        iy, iv = 2 * j, 2 * j + 1
        ST[iy, iy] = sig2; ST[iv, iv] = 1; ST[iy, iv] = ST[iv, iy] = r * sg
        STS[iy, j] = r * sg; STS[iv, j] = 1; SS[j, j] = 1 + tau2
        STY[iy, j] = sig2; STY[iv, j] = r * sg
    STgS = ST - STS @ np.linalg.inv(SS) @ STS.T
    return ST, STgS, STY

def vec_obj(x, m, ST, STgS):
    A = x[:2 * m * m].reshape(m, 2 * m)
    Lc = np.zeros((m, m)); Lc[np.tril_indices(m)] = x[2 * m * m:]
    SN = Lc @ Lc.T + 1e-12 * np.eye(m)
    num = np.linalg.slogdet(A @ STgS @ A.T + SN)[1]; den = np.linalg.slogdet(SN)[1]
    return 0.5 * (num - den) / LN2

def vec_dist(x, m, ST, STY, trY):
    A = x[:2 * m * m].reshape(m, 2 * m)
    Lc = np.zeros((m, m)); Lc[np.tril_indices(m)] = x[2 * m * m:]
    SN = Lc @ Lc.T
    return trY - 2 * np.trace(A @ STY) + np.trace(A @ ST @ A.T) + np.trace(SN)

worst_gain = -np.inf; ncase = 0
for _ in range(25):
    m = 2
    params = [(rng.uniform(0.3, 1.5), rng.uniform(0.1, 0.9), 10 ** rng.uniform(-1.5, 0)) for _ in range(m)]
    trY = sum(p[0] for p in params); D = rng.uniform(0.2, 0.8) * trY
    Ds, val = alloc(params, D)
    ST, STgS, STY = joint_cov(params)
    best = np.inf
    for _r in range(12):
        x0 = np.concatenate([rng.normal(0, 0.5, 2 * m * m), rng.uniform(0.2, 0.6, m * (m + 1) // 2)])
        res = minimize(vec_obj, x0, args=(m, ST, STgS), method='SLSQP',
                       constraints=[{'type': 'ineq', 'fun': lambda x: D - vec_dist(x, m, ST, STY, trY)}],
                       options={'maxiter': 2000, 'ftol': 1e-12})
        if res.success and vec_dist(res.x, m, ST, STY, trY) <= D + 1e-7:
            best = min(best, res.fun)
    ncase += 1
    worst_gain = max(worst_gain, val - best)   # positive => a joint channel beat the allocation
    print(f"  C5 case {ncase}: allocation {val:.6f}  best joint channel {best:.6f}  diff {best - val:+.2e}")
check("C5 no correlated vector Gaussian channel beats the allocation (m=2, 25 cases)", worst_gain < 1e-5, f"max gain {worst_gain:.2e}")

# C6 the inversion example
P1 = (1.0, 0.0, 1.0)      # context useless
P2 = (0.6, 0.9, 0.05)     # smaller variance, informative clean-ish context
kap = lambda p: p[2] / (2 * LN2 * p[0] * (p[2] + p[1]))
print(f"C6 content thresholds: coord1 {kap(P1):.4f}  coord2 {kap(P2):.4f}  (smaller is activated first)")
print(f"C6 rate thresholds   : coord1 {1/(2*LN2*P1[0]):.4f}  coord2 {1/(2*LN2*P2[0]):.4f}")
for D in [1.5, 1.4, 1.2, 1.0, 0.8]:
    Ds, val = alloc([P1, P2], D)
    th = None
    # reverse water-filling for rate
    lev = brentq(lambda t: min(t, P1[0]) + min(t, P2[0]) - D, 1e-12, 2)
    Dr = [min(lev, P1[0]), min(lev, P2[0])]
    Rr = sum(0.5 * math.log2(p[0] / x) for p, x in zip([P1, P2], Dr))
    Lr = sum(ell(x / p[0], p[1], p[2]) for p, x in zip([P1, P2], Dr))
    Rc = sum(rate_content_channel(x / p[0], p[1], p[2]) for p, x in zip([P1, P2], Ds))
    print(f"  D={D}: content-opt alloc ({Ds[0]:.4f},{Ds[1]:.4f}) L={val:.4f} R={Rc:.4f} | rate-opt alloc ({Dr[0]:.4f},{Dr[1]:.4f}) R={Rr:.4f} L={Lr:.4f}")

print("FAILS:", fails)

# C7 exact curvature: (ln g)'' = N / (g Delta^3), N = (1-r2) k^3 + r2 tau2 g^2 (tau2^2 g + tau2 (2g+1) + g + 1)
g, s, r2, d = sp.symbols('g s r2 d', positive=True)
P = d * s * g**2 - (d + s - r2) * g + (1 - r2)
gp = -sp.diff(P, d) / sp.diff(P, g)
lnpp = sp.diff(gp, d) / g + sp.diff(gp, g) * gp / g - gp**2 / g**2
dsol = ((s - r2) * g - (1 - r2)) / (g * (g * s - 1))
Delta = 2 * d * s * g - (d + s - r2)
tau2 = s - 1; k = g * s - 1
N = (1 - r2) * k**3 + r2 * tau2 * g**2 * (tau2**2 * g + tau2 * (2 * g + 1) + g + 1)
ident = sp.simplify((lnpp - N / (g * Delta**3)).subs(d, dsol))
check("C7 symbolic curvature identity (ln g)'' = N/(g Delta^3) on P(g)=0", ident == 0, str(ident))
slope_ident = sp.simplify((gp / g + k / Delta).subs(d, dsol))
check("C7 symbolic slope identity (ln g)' = -k/Delta on P(g)=0", slope_ident == 0, str(slope_ident))
worst = 0
for _ in range(500):
    rho2 = rng.uniform(0, 0.99); t2 = 10 ** rng.uniform(-3, 1); dd = rng.uniform(0.02, 0.98)
    hh = 1e-4 * dd
    fd2 = (ell(dd + hh, rho2, t2) - 2 * ell(dd, rho2, t2) + ell(dd - hh, rho2, t2)) / hh**2
    ss = 1 + t2; gg = gstar(dd, rho2, ss); kk = gg * ss - 1
    De = math.sqrt((dd + ss - rho2)**2 - 4 * dd * ss * (1 - rho2))
    NN = (1 - rho2) * kk**3 + rho2 * t2 * gg**2 * (t2**2 * gg + t2 * (2 * gg + 1) + gg + 1)
    worst = max(worst, abs(fd2 - NN / (2 * LN2 * gg * De**3)) / abs(fd2))
check("C7 numeric curvature formula vs second difference (500 points)", worst < 1e-4, f"max rel err {worst:.2e}")

# C8 disjoint-support interval for the example
th = kap(P1)
D2 = brentq(lambda x: ellp(x, P2[1], P2[2]) / P2[0] + th, 1e-12, 1 - 1e-12) * P2[0]
lo_c = P1[0] + D2; lo_r = 2 * P2[0]; hi = P1[0] + P2[0]
print(f"C8 content-opt describes coord 2 alone on [{lo_c:.4f}, {hi}); rate-opt describes coord 1 alone on [{lo_r}, {hi})")
print(f"C8 disjoint supports on [{max(lo_c, lo_r):.4f}, {hi})")
Ds, val = alloc([P1, P2], 1.4)
Rc = sum(rate_content_channel(x / p[0], p[1], p[2]) for p, x in zip([P1, P2], Ds))
print(f"C8 D=1.4: content-opt L={val:.4f} R={Rc:.4f}; rate-opt R={0.5*math.log2(1/0.8):.4f} L={0.5*math.log2(1/0.8):.4f}; ratios {0.5*math.log2(1/0.8)/val:.2f}, {Rc/(0.5*math.log2(1/0.8)):.2f}")
print("FAILS (final):", fails)
