"""verify_converses.py -- independent checks for the M2 converse closures of
tit-cr-context.tex (Secs. IV, V, VII).

Symbolic (sympy, exact):
  S1  conditional determinant identity  det Sig_{T|S}/det Sig_e = (Q1+n)/n
  S2  rate determinant identity         det Sig_T/det Sig_e0    = (Q0+n)/n
  S3  four gradient identities of the weighted objective
  S4  stationarity system linear in (a,b) at fixed g; closed-form solution
  S5  active-distortion constraint reduces to (g-1)/(g k) * P(g)
  S6  P(g_f) = -rho^2 tau^2 / s at the floor value g_f = (s-rho^2)/(Ds)
  S7  weighted FOC reduces linearly to the two-water-level relations

Numeric (numpy/scipy):
  N1  closed form L(D) vs direct minimization, 6 random instances (<=1e-7 bits)
  N2  frontier at alpha in {0, 0.5, 1} vs direct weighted minimization,
      2 instances (<=1e-7 bits per coordinate)
  N3  cor:notmarginal arithmetic (1.1610/1.2105/1.2297; 0.3685/0.5228/0.5577)
  N4  cor:misalign endpoint excesses 0.0400 / 0.0349 at (0.75, 0.5, 0.3)
  N5  vector-context FOC (eq:vecfoc) at r = 2, one instance, alpha in
      {0, 0.5, 1} (residual <= 1e-7)
  N6  rem:cleanboundary displays at tau = 0: L_min and reverse-channel
      content vs direct computation at 3 instances; strict gap
  N7  binary tilt residual: exactly one sign change on the feasible
      segment over a (p, q, D) grid (lem:tiltroot)
  N8  clean-context branch of thm:floor (lem:cleanctx): conditional-space
      program vs determinant bound at a tau = 0 instance, inside and
      outside the semidefinite condition
  N9  quantization convergence of Appendix app:gaussian: I(Yhat; S_Delta)
      increases to I(Yhat; S) under refining quantizers
"""

import numpy as np
import sympy as sp
from scipy.optimize import minimize

RESULTS = []


def report(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


# ----------------------------------------------------------------------------
# Symbolic checks
# ----------------------------------------------------------------------------
a, b, n, rho, tau, D, g, alpha, g0, g1 = sp.symbols(
    "a b n rho tau D g alpha gamma0 gamma1", positive=True
)
s = 1 + tau**2

# moment-level covariance of (Y, V, S, Yhat) with Yhat = a Y + b V + N', Var N' = n
SigT = sp.Matrix([[1, rho], [rho, 1]])
Q0 = a**2 + b**2 + 2 * a * b * rho
mu = (a * rho + b) / s
Q1 = sp.expand(Q0 - s * mu**2)
h = (1 - a) ** 2 - 2 * (1 - a) * b * rho + b**2

K4 = sp.Matrix(
    [
        [1, rho, rho, a + b * rho],
        [rho, 1, 1, a * rho + b],
        [rho, 1, s, a * rho + b],  # E[S Yhat] = E[V Yhat] (Markov moment identity)
        [a + b * rho, a * rho + b, a * rho + b, Q0 + n],
    ]
)  # order (Y, V, S, Yhat)

SigTS_full = K4[:3, :3]
SigT_S = SigT - sp.Matrix([[rho], [1]]) * sp.Matrix([[rho, 1]]) / s  # Sigma_{T|S}

# S1: det Sig_e = det K4 / det M ; ratio identity
M = sp.Matrix([[Q0 + n, a * rho + b], [a * rho + b, s]])  # Cov((Yhat, S))
det_Sig_e = sp.simplify(K4.det() / M.det())
lhs = sp.simplify(SigT_S.det() / det_Sig_e)
ok = sp.simplify(lhs - (Q1 + n) / n) == 0
report("S1 conditional determinant identity det Sig_{T|S}/det Sig_e = (Q1+n)/n", ok)

# S2: rate identity with S deleted
K3 = sp.Matrix(
    [[1, rho, a + b * rho], [rho, 1, a * rho + b], [a + b * rho, a * rho + b, Q0 + n]]
)
det_Sig_e0 = sp.simplify(K3.det() / (Q0 + n))
ok = sp.simplify(SigT.det() / det_Sig_e0 - (Q0 + n) / n) == 0
report("S2 rate determinant identity det Sig_T/det Sig_e0 = (Q0+n)/n", ok)

# S3: four gradient identities (symbolic differentiation of the weighted
# objective's building blocks; mu treated as its definition (a rho + b)/s)
ids = [
    (sp.diff(Q0 - h, a), 2),
    (sp.diff(Q0 - h, b), 2 * rho),
    (sp.diff(Q1 - h, a), 2 * (1 - rho * mu)),
    (sp.diff(Q1 - h, b), 2 * (rho - mu)),
]
ok = all(sp.simplify(l - r) == 0 for l, r in ids)
report("S3 four gradient identities d(Q0-h), d(Q1-h) w.r.t. (a,b)", ok)

# S4: the alpha=0 stationarity system, linear in (a,b) at fixed g, and its
# closed-form solution a = (g-1)/g, b = (g-1) rho/(g k)
k = g * s - 1
Ea = sp.expand((a + b * rho) - (1 - (1 - rho * mu) / g))  # first FOC relation
Eb = sp.expand((a * rho + b) - (rho - (rho - mu) / g))  # second FOC relation
lin = all(sp.degree(sp.Poly(E, a, b), gen=v) <= 1 for E in (Ea, Eb) for v in (a, b))
sol = sp.solve([Ea, Eb], [a, b], dict=True)
ok = (
    lin
    and len(sol) == 1
    and sp.simplify(sol[0][a] - (g - 1) / g) == 0
    and sp.simplify(sol[0][b] - (g - 1) * rho / (g * k)) == 0
)
report("S4 stationarity system linear in (a,b) at fixed g; solution matches eq:ab", ok)

# S5: constraint (g-1)(D-h) = Q1 at the stationary (a,b) reduces to P(g)=0
# with cofactor (g-1)/(g k)
P = D * s * g**2 - (D + s - rho**2) * g + (1 - rho**2)
a_g = (g - 1) / g
b_g = (g - 1) * rho / (g * k)
expr = ((g - 1) * (D - h) - Q1).subs([(a, a_g), (b, b_g)])
ok = sp.simplify(sp.together(expr) - P * (g - 1) / (g * k)) == 0
report("S5 (g-1)(D-h) - Q1 = P(g) (g-1)/(g k) at the stationary point", ok)

# S6: floor value
g_f = (s - rho**2) / (D * s)
ok = sp.simplify(P.subs(g, g_f) - (-(rho**2) * tau**2 / s)) == 0
report("S6 P(g_f) = -rho^2 tau^2/s at g_f = (s-rho^2)/(Ds)", ok)

# S7: weighted FOC reduces linearly to the displayed two-water-level relations
Fa = alpha * g0 + (1 - alpha) * g1 * (1 - rho * mu) + (a + b * rho - 1)
Fb = alpha * g0 * rho + (1 - alpha) * g1 * (rho - mu) + (a * rho + b - rho)
solw = sp.solve([sp.expand(Fa), sp.expand(Fb)], [a, b], dict=True)
a_w = sp.simplify(solw[0][a])
b_w = sp.simplify(solw[0][b])
a_pred = 1 - alpha * g0 - (1 - alpha) * g1
mu_pred = a_pred * rho / (s - (1 - alpha) * g1)
ok = (
    len(solw) == 1
    and sp.simplify(a_w - a_pred) == 0
    and sp.simplify(b_w - (1 - alpha) * g1 * mu_pred) == 0
)
report("S7 weighted FOC solves to a = 1-a g0-(1-a)g1, b = (1-a) g1 mu_c", ok)

# ----------------------------------------------------------------------------
# Numeric checks
# ----------------------------------------------------------------------------
rng = np.random.default_rng(20260826)


def quads(av, bv, r2, t2):
    r = np.sqrt(r2)
    sv = 1 + t2
    q0 = av**2 + bv**2 + 2 * av * bv * r
    q1 = q0 - (av * r + bv) ** 2 / sv
    hv = (1 - av) ** 2 - 2 * (1 - av) * bv * r + bv**2
    return q0, q1, hv


def gstar(r2, t2, Dv):
    sv = 1 + t2
    disc = (Dv + sv - r2) ** 2 - 4 * Dv * sv * (1 - r2)
    return ((Dv + sv - r2) + np.sqrt(disc)) / (2 * Dv * sv)


def L_closed(r2, t2, Dv):
    return 0.5 * np.log2(gstar(r2, t2, Dv))


def direct_min(r2, t2, Dv, alpha_w=0.0, nstarts=60):
    """Multi-start minimization of the weighted moment objective over (a,b)."""

    def f(x):
        av, bv = x
        q0, q1, hv = quads(av, bv, r2, t2)
        nv = Dv - hv
        if nv <= 1e-14 or q1 <= 0:
            return 1e6
        return alpha_w * 0.5 * np.log2((q0 + nv) / nv) + (1 - alpha_w) * 0.5 * np.log2(
            (q1 + nv) / nv
        )

    best, best_x = np.inf, None
    starts = [(1 - Dv, 0.0)] + [tuple(rng.uniform(-1, 1.5, 2)) for _ in range(nstarts)]
    for x0 in starts:
        res = minimize(f, x0, method="Nelder-Mead",
                       options=dict(xatol=1e-13, fatol=1e-14, maxiter=20000,
                                    maxfev=20000))
        if res.fun < best:
            best, best_x = res.fun, res.x
    return best, best_x


# N1: closed form vs direct minimization at 6 random instances
worst = 0.0
for _ in range(6):
    r2 = rng.uniform(0.05, 0.95)
    t2 = rng.uniform(0.05, 5.0)
    Dv = rng.uniform(0.05, 0.95)
    Ld, _ = direct_min(r2, t2, Dv, alpha_w=0.0)
    worst = max(worst, abs(Ld - L_closed(r2, t2, Dv)))
ok = worst <= 1e-7
report("N1 closed form L(D) vs direct (a,b,n) minimization, 6 instances", ok,
       f"max dev {worst:.2e} bits")


def solve_system(r2, t2, Dv, alpha_w):
    """Solve the two-water-level system by damped fixed-point iteration on
    (a, b), then return (R, L)."""
    r = np.sqrt(r2)
    sv = 1 + t2
    av, bv = 1 - Dv, 0.0
    for _ in range(20000):
        q0, q1, hv = quads(av, bv, r2, t2)
        nv = Dv - hv
        if nv <= 0:
            nv = 1e-12
        G0 = nv / (q0 + nv)
        G1 = nv / (q1 + nv)
        a_new = 1 - alpha_w * G0 - (1 - alpha_w) * G1
        mu_new = a_new * r / (sv - (1 - alpha_w) * G1)
        b_new = (1 - alpha_w) * G1 * mu_new
        step = 0.5
        av += step * (a_new - av)
        bv += step * (b_new - bv)
    q0, q1, hv = quads(av, bv, r2, t2)
    nv = Dv - hv
    return 0.5 * np.log2((q0 + nv) / nv), 0.5 * np.log2((q1 + nv) / nv), av, bv


# N2: frontier points at alpha in {0, 0.5, 1} vs direct weighted minimization
worst = 0.0
for (r2, t2, Dv) in [(0.75, 0.5, 0.3), (0.3, 1.5, 0.15)]:
    for aw in (0.0, 0.5, 1.0):
        Rs, Ls, _, _ = solve_system(r2, t2, Dv, aw)
        _, x = direct_min(r2, t2, Dv, alpha_w=aw)
        q0, q1, hv = quads(x[0], x[1], r2, t2)
        nv = Dv - hv
        Rd = 0.5 * np.log2((q0 + nv) / nv)
        Ld = 0.5 * np.log2((q1 + nv) / nv)
        worst = max(worst, abs(Rs - Rd), abs(Ls - Ld))
ok = worst <= 1e-7
report("N2 frontier at alpha in {0,0.5,1} vs direct weighted min, 2 instances",
       ok, f"max dev {worst:.2e} bits")

# N3: cor:notmarginal arithmetic
vals = {
    "L1(0.1)": (0.5 * np.log2(1 / 0.2), 1.1610),
    "L2(0.1)": (L_closed(0.75, 0.5, 0.1), 1.2105),
    "St(0.1)": (0.5 * np.log2(1.1 / 0.2), 1.2297),
    "L1(0.3)": (0.5 * np.log2(1 / 0.6), 0.3685),
    "L2(0.3)": (L_closed(0.75, 0.5, 0.3), 0.5228),
    "St(0.3)": (0.5 * np.log2(1.3 / 0.6), 0.5577),
}
ok = all(abs(round(v, 4) - target) < 5e-5 for v, target in vals.values())
strict = (
    vals["L1(0.1)"][0] < vals["St(0.1)"][0]
    and vals["L2(0.1)"][0] < vals["St(0.1)"][0]
    and vals["L1(0.3)"][0] < vals["St(0.3)"][0]
    and vals["L2(0.3)"][0] < vals["St(0.3)"][0]
)
gstar_exact = abs(gstar(0.75, 0.5, 0.1) - (17 + np.sqrt(229)) / 6) < 1e-12 and abs(
    gstar(0.75, 0.5, 0.3) - (21 + np.sqrt(261)) / 18
) < 1e-12
report("N3 cor:notmarginal arithmetic to 4 decimals + strict margin ordering",
       ok and strict and gstar_exact,
       ", ".join(f"{k}={v:.4f}" for k, (v, _) in vals.items()))

# N4: cor:misalign endpoint excesses at (0.75, 0.5, 0.3)
r2, t2, Dv = 0.75, 0.5, 0.3
sv = 1 + t2
gs = gstar(r2, t2, Dv)
kk = gs * sv - 1
av, bv = (gs - 1) / gs, (gs - 1) * np.sqrt(r2) / (gs * kk)
q0, q1, hv = quads(av, bv, r2, t2)
nv = Dv - hv
R0 = 0.5 * np.log2((q0 + nv) / nv)
Rmin = 0.5 * np.log2(1 / Dv)
L1v = 0.5 * np.log2(((1 - Dv) * (1 - r2 / sv) + Dv) / Dv)
Lmin = 0.5 * np.log2(gs)
ok = abs(round(R0 - Rmin, 4) - 0.0400) < 5e-5 and abs(round(L1v - Lmin, 4) - 0.0349) < 5e-5
report("N4 cor:misalign endpoint excesses 0.0400 / 0.0349 at (0.75,0.5,0.3)",
       ok, f"R(0)-Rmin={R0-Rmin:.4f}, L(1)-Lmin={L1v-Lmin:.4f}")

# N5: vector-context FOC at r = 2 (eq:vecfoc), one instance, three weights
r = 2
B = rng.normal(size=(3, 3))
SigT_v = B @ B.T
d = np.sqrt(np.diag(SigT_v))
SigT_v = SigT_v / np.outer(d, d)  # correlation form; Var Y = 1
Bu = rng.normal(size=(r, r))
SigU = Bu @ Bu.T + 0.3 * np.eye(r)
SigV = SigT_v[1:, 1:]
SigTS = SigT_v[:, 1:]
SigS = SigV + SigU
SigT_S_v = SigT_v - SigTS @ np.linalg.solve(SigS, SigTS.T)

Lc = np.linalg.cholesky(SigT_v)
F = np.linalg.solve(Lc, np.linalg.solve(Lc, SigT_S_v).T).T
lam, O = np.linalg.eigh((F + F.T) / 2)
Wm = O.T @ np.linalg.inv(Lc)
y0 = np.linalg.solve(Wm.T, np.eye(3)[:, 0])
assert abs(y0 @ y0 - 1) < 1e-10, "whitening: |y0| != 1"
Dv = 0.2

def fvec(c, aw):
    hv = np.sum((y0 - c) ** 2)
    nv = Dv - hv
    q0 = c @ c
    q1 = c @ (lam * c)
    if nv <= 1e-14 or q1 <= 0:
        return 1e6
    return aw * 0.5 * np.log2((q0 + nv) / nv) + (1 - aw) * 0.5 * np.log2((q1 + nv) / nv)

worst = 0.0
for aw in (0.0, 0.5, 1.0):
    best, best_c = np.inf, None
    for _ in range(40):
        c0 = y0 * rng.uniform(0.3, 0.95) + 0.1 * rng.normal(size=3)
        res = minimize(fvec, c0, args=(aw,), method="Nelder-Mead",
                       options=dict(xatol=1e-13, fatol=1e-14, maxiter=40000,
                                    maxfev=40000))
        if res.fun < best:
            best, best_c = res.fun, res.x
    c = best_c
    hv = np.sum((y0 - c) ** 2)
    nv = Dv - hv
    G0 = nv / (c @ c + nv)
    G1 = nv / (c @ (lam * c) + nv)
    bracket = (1 - (1 - aw) * G1) * np.eye(3) + (1 - aw) * G1 * np.diag(lam)
    c_pred = (1 - aw * G0 - (1 - aw) * G1) * np.linalg.solve(bracket, y0)
    worst = max(worst, np.max(np.abs(c - c_pred)))
ok = worst <= 1e-7
report("N5 vector-context FOC eq:vecfoc at r=2, alpha in {0,0.5,1}", ok,
       f"max residual {worst:.2e}")

# N6: rem:cleanboundary at tau = 0, three instances
def L_direct_tau0(r2, Dv, nstarts=60):
    """Direct minimization of the conditional content over linear channels
    at tau = 0 (Q1 = Var(aY+bV|V) = a^2(1-r2))."""

    def f(x):
        av, bv = x
        r = np.sqrt(r2)
        q1 = av**2 * (1 - r2)
        hv = (1 - av) ** 2 - 2 * (1 - av) * bv * r + bv**2
        nv = Dv - hv
        if nv <= 1e-14:
            return 1e6
        return 0.5 * np.log2((q1 + nv) / nv) if q1 > 0 else 0.0

    best = np.inf
    for x0 in [(1 - Dv, 0.0)] + [tuple(rng.uniform(-1, 1.5, 2)) for _ in range(nstarts)]:
        res = minimize(f, x0, method="Nelder-Mead",
                       options=dict(xatol=1e-13, fatol=1e-14, maxiter=20000,
                                    maxfev=20000))
        best = min(best, res.fun)
    return best


ok = True
detail = []
for (r2, Dv) in [(0.5, 0.2), (0.75, 0.1), (0.3, 0.8)]:
    Lmin_disp = max(0.0, 0.5 * np.log2((1 - r2) / Dv))
    Lmin_dir = L_direct_tau0(r2, Dv)
    # reverse channel Yhat = (1-D)Y + W, Var W = D(1-D): content display
    varYS = (1 - Dv) ** 2 * (1 - r2) + Dv * (1 - Dv)
    LR_disp = 0.5 * np.log2(((1 - Dv) * (1 - r2) + Dv) / Dv)
    LR_alg = 0.5 * np.log2(varYS / (Dv * (1 - Dv)))
    ok &= abs(Lmin_disp - Lmin_dir) <= 1e-7
    ok &= abs(LR_disp - LR_alg) <= 1e-12
    ok &= LR_disp > Lmin_disp + 1e-6  # strict tradeoff at every instance
    detail.append(f"({r2},{Dv}): Lmin={Lmin_disp:.4f}, LR={LR_disp:.4f}")
report("N6 rem:cleanboundary tau=0 displays and strict gap, 3 instances", ok,
       "; ".join(detail))


# N7: binary tilt residual sign-change scan
def ell(x):
    return np.log((1 - x) / x)


ok = True
worst_cfg = None
for p in np.linspace(0.05, 0.45, 9):
    for q in list(np.linspace(0.02, 0.5, 9)):
        for Dv in np.linspace(0.05, 0.45, 9):
            lo = max(0.0, (Dv - p) / (1 - p))
            hi = Dv / (1 - p)
            d0 = np.linspace(lo + 1e-9 + 1e-7 * (hi - lo), hi - 1e-9 - 1e-7 * (hi - lo), 4001)
            d1 = (Dv - (1 - p) * d0) / p
            m = (d1 > 1e-12) & (d1 < 1 - 1e-12)
            d0, d1 = d0[m], d1[m]
            aa = 2 * (1 - p) * d0 + p - Dv
            u = aa * (1 - 2 * q) + q
            psi = ell(d0) - ell(d1) - 2 * (1 - 2 * q) * ell(u)
            signs = np.sign(psi)
            changes = int(np.sum(signs[:-1] * signs[1:] < 0))
            if changes != 1:
                ok = False
                worst_cfg = (p, q, Dv, changes)
report("N7 binary tilt residual: exactly one sign change on segment (grid)",
       ok, "729 (p,q,D) cells" if ok else f"failed at {worst_cfg}")

# N8: clean-context branch of thm:floor (lem:cleanctx) at tau = 0
SigY = np.array([[1.0, 0.35], [0.35, 1.0]])
beta_v = np.array([0.6, 0.25])
Sig_c = SigY - np.outer(beta_v, beta_v)  # Sigma_{Y|V}


def cond_program(Sig_c, DA, DB, nstarts=50):
    """Minimize (1/2)log2 det(A Sig_c A' + Sig_N)/det Sig_N over the
    conditional-space Gaussian channels with individual distortions."""

    def unpack(x):
        A = x[:4].reshape(2, 2)
        Ln = np.array([[abs(x[4]) + 1e-9, 0.0], [x[5], abs(x[6]) + 1e-9]])
        return A, Ln @ Ln.T

    def f(x):
        A, SN = unpack(x)
        E = np.eye(2) - A
        c1 = E[0] @ Sig_c @ E[0] + SN[0, 0]
        c2 = E[1] @ Sig_c @ E[1] + SN[1, 1]
        pen = 1e4 * (max(0, c1 - DA) + max(0, c2 - DB))
        s1 = np.linalg.slogdet(A @ Sig_c @ A.T + SN)[1]
        s0 = np.linalg.slogdet(SN)[1]
        return 0.5 * (s1 - s0) / np.log(2) + pen

    # seed the reverse channel (the known optimum inside the SDC) plus
    # random starts; NM polishes from there cheaply
    starts = []
    Delta = np.diag([DA, DB])
    if np.all(np.linalg.eigvalsh(Sig_c - Delta) >= 0):
        A_rev = (Sig_c - Delta) @ np.linalg.inv(Sig_c)
        SN_rev = (Sig_c - Delta) @ np.linalg.inv(Sig_c) @ Delta
        SN_rev = (SN_rev + SN_rev.T) / 2
        Lc0 = np.linalg.cholesky(SN_rev + 1e-12 * np.eye(2))
        starts.append(np.concatenate([A_rev.ravel(),
                                      [Lc0[0, 0], Lc0[1, 0], Lc0[1, 1]]]))
    for _ in range(nstarts):
        starts.append(np.concatenate(
            [(np.eye(2) + 0.2 * rng.normal(size=(2, 2))).ravel(),
             rng.uniform(0.05, 0.5, 3)]))
    best = np.inf
    for x0 in starts:
        res = minimize(f, x0, method="Nelder-Mead",
                       options=dict(xatol=1e-11, fatol=1e-12, maxiter=12000,
                                    maxfev=12000))
        best = min(best, res.fun)
    return best


# inside the condition: Delta < Sig_c
DA, DB = 0.15, 0.10
inside = np.all(np.linalg.eigvalsh(Sig_c - np.diag([DA, DB])) > 0)
floor_in = 0.5 * np.log2(np.linalg.det(Sig_c) / (DA * DB))
val_in = cond_program(Sig_c, DA, DB)
# outside the condition: Delta not <= Sig_c (but B_det still positive)
DA2, DB2 = 0.62, 0.05
outside = not np.all(np.linalg.eigvalsh(Sig_c - np.diag([DA2, DB2])) >= 0)
floor_out = 0.5 * np.log2(np.linalg.det(Sig_c) / (DA2 * DB2))
val_out = cond_program(Sig_c, DA2, DB2)
ok = (inside and outside
      and abs(val_in - floor_in) <= 1e-6
      and val_out > floor_out + 1e-4)
report("N8 lem:cleanctx: conditional program = B_det iff Delta <= Sigma_{Y|V}",
       ok, f"inside: {val_in:.6f} vs {floor_in:.6f}; "
           f"outside: {val_out:.6f} > {floor_out:.6f}")

# N9: quantization convergence I(Yhat; S_Delta) -> I(Yhat; S)
from scipy.stats import norm
from numpy.polynomial.hermite_e import hermegauss

r_ys = 0.7  # correlation of the jointly Gaussian (Yhat, S), standardized
I_closed = -0.5 * np.log2(1 - r_ys**2)
nodes, weights = hermegauss(160)
weights = weights / np.sqrt(2 * np.pi)


def I_quant(K):
    """I(Yhat; q(S)) for a uniform K-bin quantizer of S on [-8, 8] with
    unbounded outer cells (edges nest as K doubles)."""
    edges = np.concatenate([[-np.inf], np.linspace(-8, 8, K - 1), [np.inf]])
    sd = np.sqrt(1 - r_ys**2)
    # P(bin | yhat) at Gauss-Hermite nodes; S | Yhat=y ~ N(r y, 1-r^2)
    up = norm.cdf((edges[None, 1:] - r_ys * nodes[:, None]) / sd)
    lo = norm.cdf((edges[None, :-1] - r_ys * nodes[:, None]) / sd)
    pcond = np.clip(up - lo, 1e-300, 1.0)
    pmarg = weights @ pcond
    HS = -np.sum(pmarg * np.log2(pmarg))
    HScond = -weights @ np.sum(pcond * np.log2(pcond), axis=1)
    return HS - HScond


Ks = [4, 8, 16, 32, 64, 128]
vals = [I_quant(K) for K in Ks]
increasing = all(vals[i + 1] > vals[i] - 1e-12 for i in range(len(vals) - 1))
below = all(v <= I_closed + 1e-9 for v in vals)
close = I_closed - vals[-1] <= 1e-3
report("N9 I(Yhat;S_Delta) increases to I(Yhat;S) under refinement",
       increasing and below and close,
       f"I_Delta: {', '.join(f'{v:.5f}' for v in vals)} -> {I_closed:.5f}")

# ----------------------------------------------------------------------------
print()
if all(RESULTS):
    print(f"ALL {len(RESULTS)} CHECKS PASS")
else:
    print(f"{RESULTS.count(False)} of {len(RESULTS)} CHECKS FAIL")
    raise SystemExit(1)
