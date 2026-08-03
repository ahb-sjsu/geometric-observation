# Numerical falsification harness for the GAUSSIAN-WITH-SIDE-INFORMATION
# extension of the consumer-relative Landauer paper (GO-P-2026-044): the
# scalar Gaussian rate-work region is a single-corner quadrant
#   R >= 1/2 log2(sigma^2/D),
#   L >= 1/2 log2((sigma^2(1-rho^2) + rho^2 D)/D),
# both attained simultaneously by the classical reverse channel (no scalar
# rate-work tradeoff), and the vector region with independent read modes has
# a nontrivial frontier traced by a generalized water-filling whose alpha=1
# endpoint is classical reverse water-filling and whose alpha=0 endpoint
# tilts distortion toward side-information-opaque modes -- the Gaussian
# analogue of Prop 2.  numpy only; deterministic; Tier A (CI, < 3 min).
#
# Sections:
#  [1] moment-level converse: LMMSE algebra e_lin = (1-r2)(v-c^2)/(v-r2 c^2)
#      exact vs direct 2x2 solve; min of l(c,v) over the admissible moment
#      set equals the closed form, minimizer at (c,v) = (1-D, 1-D).
#  [2] Gaussian channel family: exact L = 1/2 log2((v-r2c^2)/(v-c^2)) and the
#      single-curve identity L = 1/2 log2(1+(1-r2)(2^{2R}-1)) (no scalar
#      allocation freedom).
#  [3] quantizer net (non-Gaussian channels): K-level quantizers of X never
#      beat either scalar bound at their own distortion (erf-exact R, L, D).
#  [4] discrete-optimizer net: finely quantized joint (X,S) + the eq.-(20)
#      fixed point reproduces the analytic corner within discretization
#      tolerance, INCLUDING the degeneracy (alpha=1 and alpha=0 channels give
#      near-identical (R,L)).
#  [5] vector allocation program: per-mode quadratic + mu-bisection satisfies
#      KKT and feasibility; 20k random feasible allocations never beat any
#      alpha-weighted value (globality net for the convexity of the weighted
#      objective); alpha=1 reduces to classical reverse water-filling;
#      omitted modes cost zero in both coordinates.
#  [6] strict vector frontier + full-channel net: registered example
#      sigma=(1,1), rho=(0.95,0), p=(1,1), D=0.5 has L-gap and R-gap >= 0.05
#      bits between the two endpoint allocations; a full-channel discrete
#      optimizer on the 2-mode product source brackets the analytic frontier.
#  [7] side-information discount: monotone in D, -> I(X;S) as D -> 0.
# MIT License.
import math

import numpy as np

rng = np.random.default_rng(20260803)
LOG2 = np.log(2.0)

# ----------------------------------------------------------------- helpers
def Hb(p):
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 1e-300]
    return float(-(p * np.log2(p)).sum())

def mi(J):
    return Hb(J.sum(1)) + Hb(J.sum(0)) - Hb(J)

def coords(pXS, q):
    pX = pXS.sum(1)
    R = mi(pX[:, None] * q)
    L = 0.0
    for s in range(pXS.shape[1]):
        ps = pXS[:, s].sum()
        if ps > 1e-15:
            pxg = pXS[:, s] / ps
            L += ps * mi(pxg[:, None] * q)
    return R, float(L)

def fixed_point(pXS, d, alpha, beta, iters=4000, tol=1e-12):
    nx, ns = pXS.shape
    nxh = d.shape[1]
    pX = pXS.sum(1)
    pS = pXS.sum(0)
    psx = pXS / np.maximum(pX, 1e-300)[:, None]
    pxg = pXS / np.maximum(pS, 1e-300)[None, :]
    q = np.full((nx, nxh), 1.0 / nxh)
    for _ in range(iters):
        qm = pX @ q
        qs = pxg.T @ q
        lq = alpha * np.log(np.maximum(qm, 1e-300))[None, :] \
            + (1 - alpha) * (psx @ np.log(np.maximum(qs, 1e-300))) \
            - beta * LOG2 * d
        lq -= lq.max(axis=1, keepdims=True)
        qn = np.exp(lq)
        qn /= qn.sum(axis=1, keepdims=True)
        delta = float(np.abs(qn - q).max())
        q = qn
        if delta < tol:
            break
    return q

def solve_at_D(pXS, d, alpha, Dt, bisect=60, iters=4000, tol=1e-12):
    lo, hi = 0.0, 800.0
    pX = pXS.sum(1)
    q = None
    for _ in range(bisect):
        beta = 0.5 * (lo + hi)
        q = fixed_point(pXS, d, alpha, beta, iters=iters, tol=tol)
        Dd = float((pX[:, None] * q * d).sum())
        if Dd > Dt:
            lo = beta
        else:
            hi = beta
    return q

PHI = lambda z: 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
phi = lambda z: math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)

def gauss_grid(N, span=4.2):
    """Uniform grid on [-span, span] with exact standard-normal cell masses,
    per-cell conditional means and second moments (erf/phi closed forms)."""
    e = np.linspace(-span, span, N + 1)
    e[0], e[-1] = -40.0, 40.0
    p = np.array([PHI(e[j + 1]) - PHI(e[j]) for j in range(N)])
    m1 = np.array([phi(e[j]) - phi(e[j + 1]) for j in range(N)])          # int x phi
    m2 = np.array([p[j] + e[j] * phi(e[j]) - e[j + 1] * phi(e[j + 1])
                   if abs(e[j]) < 39 else p[j] for j in range(N)])        # int x^2 phi
    x = np.where(p > 1e-300, m1 / np.maximum(p, 1e-300), 0.5 * (e[:-1] + e[1:]))
    return e, p, x, m1, m2

def joint_xs_pmf(Nx, Ns, rho, sub=8):
    """Exact-enough joint pmf of gridded (X,S), X,S ~ N(0,1) corr rho, via
    per-cell midpoint quadrature of the conditional Gaussian."""
    ex, px, xx, _, _ = gauss_grid(Nx)
    es, _, xs_, _, _ = gauss_grid(Ns)
    sr = math.sqrt(max(1.0 - rho * rho, 1e-12))
    J = np.zeros((Nx, Ns))
    for j in range(Nx):
        a, b = max(ex[j], -6.0), min(ex[j + 1], 6.0)
        if b <= a:
            J[j, :] = px[j] / Ns  # negligible tail mass, spread it
            continue
        ts = a + (np.arange(sub) + 0.5) * (b - a) / sub
        w = np.array([phi(t) for t in ts]) * (b - a) / sub
        w *= px[j] / max(w.sum(), 1e-300)                 # renormalize to cell mass
        for k in range(Ns):
            lo = np.array([PHI((max(es[k], -40.0) - rho * t) / sr) for t in ts])
            hi = np.array([PHI((min(es[k + 1], 40.0) - rho * t) / sr) for t in ts])
            J[j, k] = float((w * (hi - lo)).sum())
    J /= J.sum()
    return J, xx, xs_

# --------------------------------------------------- scalar closed forms
Rmin = lambda D: 0.5 * np.log2(1.0 / D)
Lmin = lambda D, rho: 0.5 * np.log2(((1 - rho * rho) + rho * rho * D) / D)
ell = lambda c, v, rho: 0.5 * np.log2((v - rho * rho * c * c) / (v - c * c))

fail = []
# =====================================================================================
print("=" * 78)
print("[1] scalar moment-level converse: LMMSE algebra + min of l(c,v) = closed form")
worst_alg = 0.0
for _ in range(2000):
    rho = rng.uniform(-0.98, 0.98)
    c = rng.uniform(-1.5, 1.5)
    v = c * c + 10 ** rng.uniform(-4, 1)
    K = np.array([[v, rho * c], [rho * c, 1.0]])
    cross = np.array([c, rho])
    e_direct = 1.0 - cross @ np.linalg.solve(K, cross)
    e_formula = (1 - rho * rho) * (v - c * c) / (v - rho * rho * c * c)
    worst_alg = max(worst_alg, abs(e_direct - e_formula))
print(f"  LMMSE algebra: 2000 random (rho,c,v), worst |direct - formula| = {worst_alg:.1e}")
if worst_alg > 1e-10:
    fail.append("lmmse-algebra")

worst_min = 0.0
for rho in (0.15, 0.5, 0.8, 0.95):
    for D in (0.05, 0.25, 0.6, 0.9):
        best = np.inf
        bc = bv = None
        for c in np.linspace(1 - math.sqrt(D) + 1e-6, 1 + math.sqrt(D) - 1e-6, 4001):
            v = D - 1 + 2 * c                       # budget binding (l dec. in v)
            if v > c * c + 1e-12:
                val = ell(c, v, rho)
                if val < best:
                    best, bc, bv = val, c, v
        worst_min = max(worst_min, abs(best - Lmin(D, rho)),
                        abs(bc - (1 - D)), abs(bv - (1 - D)))
print(f"  min over admissible moments vs closed form + minimizer (1-D,1-D): "
      f"worst dev = {worst_min:.1e}")
if worst_min > 5e-4:                                 # grid resolution bound
    fail.append("moment-minimum")

# =====================================================================================
print("=" * 78)
print("[2] Gaussian channels: exact L and the single-curve identity (no scalar tradeoff)")
worst2 = 0.0
for _ in range(3000):
    rho = rng.uniform(-0.98, 0.98)
    b = rng.uniform(-2, 2)
    w = 10 ** rng.uniform(-3, 1)
    c, v = b, b * b + w
    R = 0.5 * np.log2(v / (v - c * c))
    L = ell(c, v, rho)
    worst2 = max(worst2, abs(L - 0.5 * np.log2(1 + (1 - rho * rho) * (2 ** (2 * R) - 1))))
print(f"  3000 random Gaussian channels: |L - curve(R)| worst = {worst2:.1e}")
if worst2 > 1e-10:
    fail.append("single-curve")

# =====================================================================================
print("=" * 78)
print("[3] quantizer net: non-Gaussian channels never beat either scalar bound")
viol3 = 0
tested3 = 0
for trial in range(400):
    rho = rng.uniform(0.1, 0.95)
    K = int(rng.integers(2, 9))
    edges = np.sort(rng.uniform(-2.5, 2.5, size=K - 1))
    e = np.concatenate([[-40.0], edges, [40.0]])
    p = np.array([PHI(e[j + 1]) - PHI(e[j]) for j in range(K)])
    if p.min() < 1e-6:
        continue
    m1 = np.array([phi(e[j]) - phi(e[j + 1]) for j in range(K)])
    m2 = np.array([p[j] + (e[j] * phi(e[j]) if abs(e[j]) < 39 else 0.0)
                   - (e[j + 1] * phi(e[j + 1]) if abs(e[j + 1]) < 39 else 0.0)
                   for j in range(K)])
    xhat = m1 / p                                     # centroid reproduction
    Dq = float((m2 - 2 * xhat * m1 + xhat ** 2 * p).sum())
    if not (1e-4 < Dq < 0.999):
        continue
    tested3 += 1
    R = Hb(p)                                         # deterministic quantizer
    # H(Xh|S) by quadrature over s (vectorized erf over the s-grid x edges)
    sgrid = np.linspace(-5, 5, 601)
    ws = np.exp(-0.5 * sgrid ** 2)
    ws /= ws.sum()
    sr = math.sqrt(1 - rho * rho)
    Z = (np.clip(e[None, :], -40, 40) - rho * sgrid[:, None]) / sr   # (601, K+1)
    E = np.vectorize(math.erf)(Z / math.sqrt(2.0))
    PK = 0.5 * np.diff(E, axis=1)                       # (601, K)
    PK = np.maximum(PK, 1e-300)
    PK /= PK.sum(axis=1, keepdims=True)
    L = float((ws * (-(PK * np.log2(PK)).sum(axis=1))).sum())
    if R < Rmin(Dq) - 1e-9 or L < Lmin(Dq, rho) - 1e-9:
        viol3 += 1
print(f"  quantizer channels tested = {tested3}; bound violations = {viol3}")
if viol3:
    fail.append(f"quantizer-violations={viol3}")

# =====================================================================================
print("=" * 78)
print("[4] discrete-optimizer net: quantized (X,S) reproduces the analytic corner")
worst4 = 0.0
degen = 0.0
for rho in (0.5, 0.9):
    D = 0.25
    J, xx, _ = joint_xs_pmf(41, 21, rho)
    d = (xx[:, None] - xx[None, :]) ** 2
    qR = solve_at_D(J, d, 1.0, D)
    qL = solve_at_D(J, d, 0.0, D)
    Rr, Lr = coords(J, qR)
    Rl, Ll = coords(J, qL)
    worst4 = max(worst4, abs(Rr - Rmin(D)), abs(Ll - Lmin(D, rho)))
    degen = max(degen, abs(Lr - Ll), abs(Rl - Rr))
    print(f"  rho={rho}: R(a=1)={Rr:.4f} (analytic {Rmin(D):.4f})  "
          f"L(a=0)={Ll:.4f} (analytic {Lmin(D, rho):.4f})  "
          f"corner degeneracy |dR|,|dL| <= {degen:.4f}")
if worst4 > 0.06 or degen > 0.03:
    fail.append(f"discrete-corner worst={worst4:.3f} degen={degen:.3f}")

# =====================================================================================
print("=" * 78)
print("[5] vector allocation: quadratic+bisection = KKT; random allocations never beat")

def alloc(alpha, sig2, rho2, p, D):
    """Generalized water-filling: per-mode positive root, clipped, mu-bisected."""
    c = sig2 * (1 - rho2)

    def d_of_mu(mu):
        d = np.empty_like(sig2)
        for i in range(len(sig2)):
            if rho2[i] < 1e-14:
                d[i] = (alpha if alpha > 0 else 1.0) / (2 * mu * p[i]) \
                    if alpha > 0 else 1.0 / (2 * mu * p[i])
                d[i] = 1.0 / (2 * mu * p[i])          # alpha cancels at rho=0
            else:
                A = 2 * mu * p[i] * rho2[i]
                Bq = 2 * mu * p[i] * c[i] - alpha * rho2[i]
                Cq = -c[i]
                d[i] = (-Bq + math.sqrt(Bq * Bq - 4 * A * Cq)) / (2 * A)
            d[i] = min(d[i], sig2[i])
        return d

    lo, hi = 1e-9, 1e9
    for _ in range(200):
        mu = math.sqrt(lo * hi)
        if float((p * d_of_mu(mu)).sum()) > D:
            lo = mu
        else:
            hi = mu
    mu = math.sqrt(lo * hi)
    d = d_of_mu(mu)
    R = float((0.5 * np.log2(sig2 / d)).sum())
    c_ = c
    L = float((0.5 * np.log2((c_ + rho2 * d) / d)).sum())
    return d, R, L, mu

worst5 = 0.0
viol5 = 0
for trial in range(30):
    r = int(rng.integers(2, 9))
    sig2 = rng.uniform(0.3, 3.0, r)
    rho2 = rng.uniform(0.0, 0.97, r) ** 1.0
    p = rng.uniform(0.3, 2.0, r)
    D = rng.uniform(0.15, 0.8) * float((p * sig2).sum())
    for alpha in (0.0, 0.3, 0.7, 1.0):
        d, R, L, mu = alloc(alpha, sig2, rho2, p, D)
        worst5 = max(worst5, abs(float((p * d).sum()) - D))
        c = sig2 * (1 - rho2)
        act = d < sig2 - 1e-9
        if act.any():                                  # KKT residual, scale-free
            marg = alpha / (2 * d[act]) + (1 - alpha) * c[act] / (
                2 * d[act] * (c[act] + rho2[act] * d[act]))
            worst5 = max(worst5, float(np.abs(marg / (mu * p[act]) - 1).max()))
        Jstar = alpha * R + (1 - alpha) * L
        cnt = att = 0
        while cnt < 5000 and att < 200000:              # batched rejection
            W = rng.dirichlet(np.ones(r), size=10000) * D / p
            att += 10000
            ok = (W <= sig2 + 1e-12).all(axis=1) & (W > 1e-12).all(axis=1)
            W = W[ok][: 5000 - cnt]
            if W.size == 0:
                continue
            cnt += W.shape[0]
            Rw = (0.5 * np.log2(sig2 / W)).sum(axis=1)
            Lw = (0.5 * np.log2((c + rho2 * W) / W)).sum(axis=1)
            if float((alpha * Rw + (1 - alpha) * Lw).min()) < Jstar - 1e-9:
                viol5 += 1
                break
    # omitted-mode identity
    dfull = sig2.copy()
    worst5 = max(worst5, float(np.abs(0.5 * np.log2((c + rho2 * dfull) / dfull)).max()))
# alpha=1 classical reverse water-filling cross-check
sig2 = np.array([2.0, 1.0, 0.5])
p = np.array([1.0, 1.0, 1.0])
d1, R1, _, _ = alloc(1.0, sig2, np.array([0.5, 0.5, 0.5]), p, 0.9)
th = 0.3                                              # equal-split water level
worst5 = max(worst5, float(np.abs(d1 - np.minimum(sig2, th)).max()))
print(f"  30 random (r,sig,rho,p,D) x 4 alpha: feasibility+KKT+omitted+classical "
      f"worst = {worst5:.2e}; random-allocation beats = {viol5}")
if worst5 > 1e-5 or viol5:
    fail.append(f"vector-allocation worst={worst5:.1e} viol={viol5}")

# =====================================================================================
print("=" * 78)
print("[6] strict vector frontier + 2-mode full-channel net")
sig2 = np.array([1.0, 1.0])
rho2 = np.array([0.95 ** 2, 0.0])
p2 = np.array([1.0, 1.0])
Dv = 0.5
dR_, Rr, Lr, _ = alloc(1.0, sig2, rho2, p2, Dv)
dL_, Rl, Ll, _ = alloc(0.0, sig2, rho2, p2, Dv)
gapL = Lr - Ll
gapR = Rl - Rr
print(f"  registered example rho=(0.95,0), D=0.5: alloc(a=1)={np.round(dR_,3)} "
      f"alloc(a=0)={np.round(dL_,3)}  L-gap={gapL:.4f}  R-gap={gapR:.4f}")
if not (gapL >= 0.05 and gapR >= 0.05):
    fail.append(f"strictness gapL={gapL:.3f} gapR={gapR:.3f}")

# full-channel separability net on the 2-mode product source.  The vector
# converse rests on I(X;Xh) >= sum_i I(X_i;Xh_i) and I(X;Xh|S) >= sum_i
# I(X_i;Xh_i|S_i) for independent pairs -- inequalities that hold for ANY
# independent-pair source, quantized included.  So the exact-to-exact net is:
# the full-channel optimum on the quantized product source must never beat the
# per-mode discrete envelope (min over budget splits of the per-mode optima)
# computed on the SAME grids.  Grid coarseness cannot produce a false failure;
# a joint channel beating the envelope would refute the separability step.
J1, x1, _ = joint_xs_pmf(13, 7, 0.95)
J2, x2, _ = joint_xs_pmf(13, 7, 0.0)
Jv = np.einsum("ab,cd->acbd", J1, J2).reshape(13 * 13, 7 * 7)
xv1 = np.repeat(x1, 13)
xv2 = np.tile(x2, 13)
dv = (xv1[:, None] - xv1[None, :]) ** 2 + (xv2[:, None] - xv2[None, :]) ** 2
d1m = (x1[:, None] - x1[None, :]) ** 2
splits = np.linspace(0.04, Dv - 0.04, 13)

def permode_env(alpha):
    """min over budget splits of the summed per-mode discrete optima."""
    best = np.inf
    for d1 in splits:
        v = 0.0
        for Jm, dm, dt in ((J1, d1m, d1), (J2, d1m, Dv - d1)):
            qm_ = solve_at_D(Jm, dm, alpha, dt, bisect=36, iters=2500, tol=1e-11)
            Rm, Lm = coords(Jm, qm_)
            v += alpha * Rm + (1 - alpha) * Lm
        best = min(best, v)
    return best

ok6 = True
for alpha in (1.0, 0.0):
    env = permode_env(alpha)
    qf = solve_at_D(Jv, dv, alpha, Dv, bisect=28, iters=1500, tol=1e-10)
    Rf, Lf = coords(Jv, qf)
    Jfull = alpha * Rf + (1 - alpha) * Lf
    sep_ok = Jfull >= env - 5e-3                       # solver tolerance only
    ok6 &= sep_ok
    print(f"  full-channel a={alpha:.0f}: weighted objective {Jfull:.4f} vs "
          f"per-mode envelope {env:.4f}  (R,L)=({Rf:.4f},{Lf:.4f})  "
          f"separability holds={sep_ok}")
if not ok6:
    fail.append("full-channel-separability")

# =====================================================================================
print("=" * 78)
print("[7] side-information discount: monotone in D, -> I(X;S) as D -> 0")
ok7 = True
for rho in (0.3, 0.7, 0.95):
    Ds = np.linspace(1e-4, 0.999, 400)
    disc = Rmin(Ds) - Lmin(Ds, rho)
    ok7 &= bool((np.diff(disc) < 1e-12).all())
    ok7 &= abs(disc[0] - 0.5 * np.log2(1 / (1 - rho * rho))) < 2e-3
print(f"  discount decreasing in D and -> I(X;S) at D->0: {ok7}")
if not ok7:
    fail.append("discount")

print("=" * 78)
print("VERDICT:", "ALL PASS" if not fail else f"FAIL: {fail}")
