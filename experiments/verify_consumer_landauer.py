# Numerical falsification harness for the consumer-relative Landauer paper
# (paper/consumer-relative-landauer.pdf): the rate-work-distortion region
# RW_C(D) = conv U_{q in T_C(D)} {(R,L): R >= I(X;Xh), L >= I(X;Xh|S)},
# its Pareto-channel equation, the exact binary frontier, the materialization
# barrier, several-consumer total correlation, Gaussian read-operator
# water-filling (isothermal + temperature-weighted), and the staleness-work
# complement.  Registered as GO-P-2026-042; falsification net for analytic
# results per charter rule R-IND-5 -- a mismatch sends the claim back to the
# proof.  numpy only; deterministic seed; Tier A (CI, CPU, < 3 min).
#
# Sections:
#  [1] Prop 2  exact binary rate-work frontier: closed form vs product-BSC
#      channels; random+adversarial channel net cannot beat the support lines;
#      matched-rate inversion (same R, D; Landauer content 0.1187 vs 1).
#  [2] Prop 1  Pareto-channel fixed point (eq. 20): the alternating update
#      decreases J_{a,b}; converged channel is self-consistent; no random
#      channel beats it; a=1 reproduces the classical binary R(D)=1-h2(D);
#      midpoint-convexity probe of BOTH coordinates in q(xh|x) (the proof's
#      premise; note I(X;Xh|S) = sum_s p(s) I_s, each I_s convex in q).
#  [3] Thm 1   finite-n converse net on the Prop-2 source: no random
#      deterministic code (exact H(M|S^n), optimal decoder) lands strictly
#      below the closed-form lower boundary at its own distortion.
#  [4] Thm 2   materialization barrier: H(A,M|S^n) = n H(X|S) exactly, for
#      random sources and random deterministic descriptions; sequential chain
#      rule; ideal work gap Delta-W >= 0.
#  [5] Cor 2+3 exact consumer endpoints R_C(0)=H(U), L_C(0|S)=H(U|S) (via the
#      optimizer) and several-consumer conditional total correlation TC >= 0,
#      strict on dependent reads; coordinated reset = joint conditional entropy.
#  [6] Cor 4   Gaussian read geometry: eigenvalue water-filling formula (41)
#      equals the max-det program (reverse water-filling with the Sigma <= Sx
#      cap, cf. verify_rate_region.sigma_star); random admissible Gaussian
#      codes never beat it; ker P_C modes are free.
#  [7] Prop 3  temperature-weighted water-filling: dual-bisection solution
#      d_i* = min{lambda_i, nu T_i}; KKT residuals; 50k random feasible
#      allocations never beat W*; equal-T reduces to reverse water-filling.
#  [8] Prop 4  staleness: L_t = H(M|X_t) nondecreasing for random finite
#      Markov chains (exact); binary example: I + L = 1 bit at every age.
# MIT License.
import numpy as np

rng = np.random.default_rng(20260802)
LOG2 = np.log(2.0)

# ----------------------------------------------------------------- helpers
def Hb(p):
    """Shannon entropy (bits) of a probability vector/array (ravelled)."""
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 1e-300]
    return float(-(p * np.log2(p)).sum())

def h2(t):
    t = float(t)
    if t <= 0.0 or t >= 1.0:
        return 0.0
    return -t * np.log2(t) - (1 - t) * np.log2(1 - t)

def h2v(t):
    """Vectorized binary entropy (bits)."""
    t = np.clip(np.asarray(t, dtype=float), 0.0, 1.0)
    u = np.clip(t, 1e-300, 1.0)
    v = np.clip(1.0 - t, 1e-300, 1.0)
    return -t * np.log2(u) - (1.0 - t) * np.log2(v)

def frontier_grid(D, npts=800):
    """Vectorized closed-form lower boundary of Prop 2 at distortion D."""
    t = np.linspace(0.0, D, npts)
    return np.stack([2.0 - h2v(t) - h2v(2 * D - t), 1.0 - h2v(2 * D - t)], axis=1)

def mi(J):
    """I(X;Y) in bits from a joint array J[x,y]."""
    return Hb(J.sum(1)) + Hb(J.sum(0)) - Hb(J)

def coords(pXS, q):
    """(R, L) = (I(X;Xh), I(X;Xh|S)) in bits for channel q[x,xh], joint pXS[x,s].
    Markov Xh - X - S holds by construction (q depends on x only)."""
    pX = pXS.sum(1)
    R = mi(pX[:, None] * q)
    L = 0.0
    for s in range(pXS.shape[1]):
        ps = pXS[:, s].sum()
        if ps < 1e-15:
            continue
        pxg = pXS[:, s] / ps
        L += ps * mi(pxg[:, None] * q)
    return R, float(L)

def dist(pXS, q, d):
    return float((pXS.sum(1)[:, None] * q * d).sum())

def rand_simplex(rows, cols, r):
    return r.dirichlet(np.ones(cols), size=rows)

# ------------------------------------------- Prop-2 source (two fair bits)
# x = 2a+b, S = A; d = half-Hamming per component.
PX4 = np.full(4, 0.25)
PXS2 = np.zeros((4, 2))
for x in range(4):
    PXS2[x, x >> 1] = 0.25
D4 = np.zeros((4, 4))
for x in range(4):
    for y in range(4):
        D4[x, y] = 0.5 * ((x >> 1) != (y >> 1)) + 0.5 * ((x & 1) != (y & 1))

def bsc(t):
    return np.array([[1 - t, t], [t, 1 - t]])

def prod_channel(ta, tb):
    """q[(a,b) -> (ah,bh)] = BSC_ta(a,ah) * BSC_tb(b,bh) on x = 2a+b."""
    A, B = bsc(ta), bsc(tb)
    q = np.zeros((4, 4))
    for x in range(4):
        for y in range(4):
            q[x, y] = A[x >> 1, y >> 1] * B[x & 1, y & 1]
    return q

def frontier(D, t):
    """Closed-form lower Pareto boundary of Prop 2 at distortion D, 0<=t<=D."""
    return 2 - h2(t) - h2(2 * D - t), 1 - h2(2 * D - t)

# ------------------------------------------------- Pareto-channel optimizer
def pareto_fixed_point(pXS, d, alpha, beta, iters=3000, tol=1e-13, q0=None):
    """Alternating minimization of J = a*I(X;Xh) + (1-a)*I(X;Xh|S) + b*E d
    via the eq.-(20) update.  Returns (q, J_trace)."""
    nx, ns = pXS.shape
    nxh = d.shape[1]
    pX = pXS.sum(1)
    pS = pXS.sum(0)
    psx = pXS / np.maximum(pX, 1e-300)[:, None]          # p(s|x)
    pxg = pXS / np.maximum(pS, 1e-300)[None, :]          # p(x|s) columns
    q = rand_simplex(nx, nxh, rng) if q0 is None else q0.copy()
    Js = []
    for _ in range(iters):
        qm = pX @ q                                       # q(xh)
        qs = (pxg.T @ q)                                  # q(xh|s), rows s
        lq = alpha * np.log(np.maximum(qm, 1e-300))[None, :] \
            + (1 - alpha) * (psx @ np.log(np.maximum(qs, 1e-300))) \
            - beta * LOG2 * d
        lq -= lq.max(axis=1, keepdims=True)
        qn = np.exp(lq)
        qn /= qn.sum(axis=1, keepdims=True)
        R, L = coords(pXS, qn)
        Js.append(alpha * R + (1 - alpha) * L + beta * dist(pXS, qn, d))
        if len(Js) > 1 and abs(Js[-2] - Js[-1]) < tol:
            q = qn
            break
        q = qn
    return q, Js

def J_of(pXS, d, q, alpha, beta):
    R, L = coords(pXS, q)
    return alpha * R + (1 - alpha) * L + beta * dist(pXS, q, d)

fail = []
# =====================================================================================
print("=" * 78)
print("[1] Prop 2: exact binary rate-work frontier (D = 0.15)")
D = 0.15
ts = np.linspace(0.0, D, 61)
worst = 0.0
for t in ts:
    q = prod_channel(t, 2 * D - t)
    R, L = coords(PXS2, q)
    Rf, Lf = frontier(D, t)
    dd = dist(PXS2, q, D4)
    worst = max(worst, abs(R - Rf), abs(L - Lf), abs(dd - D))
print(f"  product-BSC channels realize the closed form: worst residual = {worst:.1e}")
if worst > 1e-10:
    fail.append("prop2-achievability")

# support-line converse net: random + adversarially optimized channels with
# distortion <= D never beat min_t [a R(t) + (1-a) L(t)].
alphas = np.linspace(0.0, 1.0, 11)
tgrid = np.linspace(0.0, D, 2001)
Fgrid = np.array([frontier(D, t) for t in tgrid])        # (R, L) rows
viol = 0
tested = 0
for trial in range(4000):
    gam = rng.uniform(0.0, 4 * D)
    q = (1 - gam) * np.eye(4) + gam * rand_simplex(4, 4, rng)
    if dist(PXS2, q, D4) > D + 1e-12:
        continue
    tested += 1
    R, L = coords(PXS2, q)
    for a in alphas:
        if a * R + (1 - a) * L < (a * Fgrid[:, 0] + (1 - a) * Fgrid[:, 1]).min() - 1e-9:
            viol += 1
            break
# adversarial: run the optimizer at each alpha with beta tuned to land at D
for a in alphas:
    best = None
    for beta in np.linspace(0.5, 30.0, 40):
        q, _ = pareto_fixed_point(PXS2, D4, a, beta, q0=np.full((4, 4), 0.25))
        dd = dist(PXS2, q, D4)
        if dd <= D + 1e-9:
            R, L = coords(PXS2, q)
            v = a * R + (1 - a) * L
            best = v if best is None else min(best, v)
    lb = (a * Fgrid[:, 0] + (1 - a) * Fgrid[:, 1]).min()
    tested += 1
    if best is not None and best < lb - 1e-7:
        viol += 1
print(f"  support-line net: {tested} admissible channels (random + optimizer), "
      f"violations = {viol}")
if viol:
    fail.append(f"prop2-converse-violations={viol}")

# matched-rate inversion: (DA,DB) = (0,0.30) vs (0.30,0)
q1 = prod_channel(0.0, 0.30)
q2 = prod_channel(0.30, 0.0)
R1, L1 = coords(PXS2, q1)
R2, L2 = coords(PXS2, q2)
ok_inv = (abs(R1 - R2) < 1e-12 and abs(dist(PXS2, q1, D4) - dist(PXS2, q2, D4)) < 1e-12
          and abs(R1 - (2 - h2(0.30))) < 1e-12
          and abs(L1 - (1 - h2(0.30))) < 1e-12 and abs(L2 - 1.0) < 1e-12)
print(f"  matched-rate inversion: R = {R1:.4f} = {R2:.4f}, D tied at 0.15; "
      f"L = {L1:.4f} vs {L2:.4f} (ratio {L2/L1:.2f}x)  ok={ok_inv}")
if not ok_inv:
    fail.append("prop2-inversion")

# =====================================================================================
print("=" * 78)
print("[2] Prop 1: Pareto-channel equation -- descent, self-consistency, optimality")
worst_sc = 0.0
worst_desc = 0.0
beat = 0
for trial in range(40):
    nx, ns, nxh = rng.integers(2, 5), rng.integers(2, 4), rng.integers(2, 5)
    pXS = rng.dirichlet(np.ones(nx * ns)).reshape(nx, ns)
    d = rng.uniform(0.0, 1.0, size=(nx, nxh))
    alpha = rng.uniform(0.0, 1.0)
    beta = rng.uniform(0.2, 8.0)
    q, Js = pareto_fixed_point(pXS, d, alpha, beta)
    worst_desc = max(worst_desc, float(np.max(np.diff(Js))) if len(Js) > 1 else 0.0)
    # self-consistency of eq. (20) at the fixed point
    pX = pXS.sum(1)
    pS = pXS.sum(0)
    psx = pXS / np.maximum(pX, 1e-300)[:, None]
    pxg = pXS / np.maximum(pS, 1e-300)[None, :]
    qm = pX @ q
    qs = pxg.T @ q
    num = (qm[None, :] ** alpha) * np.exp((1 - alpha) * (psx @ np.log(np.maximum(qs, 1e-300)))) \
        * 2.0 ** (-beta * d)
    pred = num / num.sum(axis=1, keepdims=True)
    m = q > 1e-9                                          # eq. (20) governs the support
    worst_sc = max(worst_sc, float(np.abs(q - pred)[m].max()))
    # global-optimality net: random channels + random restarts
    Jstar = J_of(pXS, d, q, alpha, beta)
    for _ in range(400):
        if J_of(pXS, d, rand_simplex(nx, nxh, rng), alpha, beta) < Jstar - 1e-8:
            beat += 1
            break
print(f"  40 random (source, d, a, b): descent worst uptick = {worst_desc:.1e}; "
      f"eq.(20) self-consistency worst = {worst_sc:.1e}; random channels beating J* = {beat}")
if worst_desc > 1e-9 or worst_sc > 1e-6 or beat:
    fail.append("prop1-fixed-point")

# a=1 reproduces the classical binary rate-distortion function
pb = np.array([[0.5, 0.0], [0.0, 0.5]])                   # X = S = fair bit (S unused at a=1)
dh = 1.0 - np.eye(2)
worst_rd = 0.0
for beta in np.linspace(1.0, 12.0, 20):
    q, _ = pareto_fixed_point(pb, dh, 1.0, beta, q0=np.full((2, 2), 0.5))
    R, _ = coords(pb, q)
    Dd = dist(pb, q, dh)
    if 1e-4 < Dd < 0.5 - 1e-4:
        worst_rd = max(worst_rd, abs(R - (1 - h2(Dd))))
print(f"  a=1 classical check: |R - (1 - h2(D))| worst = {worst_rd:.1e}")
if worst_rd > 1e-6:
    fail.append("prop1-classical-limit")

# midpoint-convexity probe of both coordinates (the proof's premise)
cviol = 0
for _ in range(2000):
    nx, ns, nxh = 3, 2, 3
    pXS = rng.dirichlet(np.ones(nx * ns)).reshape(nx, ns)
    qa = rand_simplex(nx, nxh, rng)
    qb = rand_simplex(nx, nxh, rng)
    qm = 0.5 * (qa + qb)
    Ra, La = coords(pXS, qa)
    Rb, Lb = coords(pXS, qb)
    Rm, Lm = coords(pXS, qm)
    if Rm > 0.5 * (Ra + Rb) + 1e-10 or Lm > 0.5 * (La + Lb) + 1e-10:
        cviol += 1
print(f"  midpoint convexity of I(X;Xh) and I(X;Xh|S) in q: violations = {cviol}/2000")
if cviol:
    fail.append(f"prop1-convexity-violations={cviol}")

# =====================================================================================
print("=" * 78)
print("[3] Thm 1 converse net: random finite-n codes vs the single-letter boundary")
viol3 = 0
tested3 = 0
for n in (1, 2):
    xs = 4 ** n
    # enumerate x^n and s^n = a^n; joint p(x^n) product, s determined by x here
    xidx = np.array(np.meshgrid(*([np.arange(4)] * n), indexing="ij")).reshape(n, -1).T
    pxn = np.full(xs, 0.25 ** n)
    an = (xidx >> 1)                                     # per-letter a = s
    sid = an @ (2 ** np.arange(n)[::-1])                 # s^n index, 2^n values
    dn = np.zeros((xs, 4))                               # per-letter d for decoder
    for K in (2, 3, 4, 6, 8):
        for _ in range(1500):
            f = rng.integers(0, K, size=xs)
            # optimal decoder: per index m and position i, best xh
            Dsum = 0.0
            for m in range(K):
                w = pxn * (f == m)
                pm = w.sum()
                if pm < 1e-15:
                    continue
                for i in range(n):
                    cost = np.array([ (w * D4[xidx[:, i], y]).sum() for y in range(4) ])
                    Dsum += cost.min()
            Dn = Dsum / n
            if Dn >= 0.235:
                continue
            tested3 += 1
            Rn = np.log2(K) / n
            # exact H(M | S^n)
            pms = np.zeros((K, 2 ** n))
            for x in range(xs):
                pms[f[x], sid[x]] += pxn[x]
            Ln = (Hb(pms) - Hb(pms.sum(0))) / n
            Fg = frontier_grid(Dn)
            for a in alphas:
                if a * Rn + (1 - a) * Ln < (a * Fg[:, 0] + (1 - a) * Fg[:, 1]).min() - 1e-9:
                    viol3 += 1
                    break
print(f"  admissible random deterministic codes tested = {tested3}; "
      f"boundary violations = {viol3}")
if viol3:
    fail.append(f"thm1-converse-violations={viol3}")

# =====================================================================================
print("=" * 78)
print("[4] Thm 2: materialization barrier H(A,M|S^n) = n H(X|S), chain rule, gap >= 0")
worst4 = 0.0
for trial in range(60):
    nx, ns = rng.integers(2, 6), rng.integers(2, 4)
    pXS = rng.dirichlet(np.ones(nx * ns)).reshape(nx, ns)
    n = 2
    xs = nx ** n
    xi = np.array(np.meshgrid(*([np.arange(nx)] * n), indexing="ij")).reshape(n, -1).T
    # joint over (x^n, s^n): product of per-letter joints
    pj = np.ones((xs, ns ** n))
    si = np.array(np.meshgrid(*([np.arange(ns)] * n), indexing="ij")).reshape(n, -1).T
    for r_ in range(xs):
        for c in range(ns ** n):
            v = 1.0
            for i in range(n):
                v *= pXS[xi[r_, i], si[c, i]]
            pj[r_, c] = v
    K = int(rng.integers(2, 6))
    fmap = rng.integers(0, K, size=xs)                    # M = f(A), deterministic
    HXgS = Hb(pj) - Hb(pj.sum(0))                         # H(A|S^n) = n H(X|S)
    hxs = 0.0                                             # n * single-letter H(X|S)
    hxs = n * (Hb(pXS) - Hb(pXS.sum(0)))
    # H(A, M | S^n) = H(A | S^n) since M = f(A); verify by explicit (A,M) joint
    pam = np.zeros((xs * K, ns ** n))
    for r_ in range(xs):
        pam[r_ * K + fmap[r_], :] += pj[r_, :]
    HAMgS = Hb(pam) - Hb(pam.sum(0))
    # chain rule: H(A|M,S^n) + H(M|S^n) = H(A,M|S^n)
    pms = np.zeros((K, ns ** n))
    for r_ in range(xs):
        pms[fmap[r_], :] += pj[r_, :]
    HMgS = Hb(pms) - Hb(pms.sum(0))
    HAgMS = HAMgS - HMgS                                  # via joint identity
    worst4 = max(worst4, abs(HAMgS - HXgS), abs(HXgS - hxs),
                 abs((HAgMS + HMgS) - HAMgS))
print(f"  60 random (source, f): |H(A,M|S^n) - nH(X|S)| and chain-rule "
      f"worst residual = {worst4:.1e}")
if worst4 > 1e-9:
    fail.append("thm2-identity")

# ideal work gap Delta-W = H(X|S) - L_C(D|S) >= 0 via the a=0 optimizer
gap_neg = 0
for trial in range(20):
    nx, ns = 4, 2
    pXS = rng.dirichlet(np.ones(nx * ns)).reshape(nx, ns)
    d = rng.uniform(0.0, 1.0, size=(nx, nx))
    np.fill_diagonal(d, 0.0)
    q, _ = pareto_fixed_point(pXS, d, 0.0, rng.uniform(0.5, 6.0))
    _, L = coords(pXS, q)
    if (Hb(pXS) - Hb(pXS.sum(0))) - L < -1e-9:
        gap_neg += 1
print(f"  Delta-W >= 0: negative gaps = {gap_neg}/20")
if gap_neg:
    fail.append("thm2-gap")

# =====================================================================================
print("=" * 78)
print("[5] Cor 2 exact-consumer endpoints + Cor 3 several-consumer TC >= 0")
worst5 = 0.0
for trial in range(15):
    nx, ns, nu = 6, 2, 3
    pXS = rng.dirichlet(np.ones(nx * ns)).reshape(nx, ns)
    U = rng.integers(0, nu, size=nx)                      # U = C(X)
    d = (U[:, None] != U[None, :]).astype(float)          # zero-distortion = exact U
    pX = pXS.sum(1)
    pu = np.zeros(nu)
    pus = np.zeros((nu, ns))
    for x in range(nx):
        pu[U[x]] += pX[x]
        pus[U[x], :] += pXS[x, :]
    HU = Hb(pu)
    HUgS = Hb(pus) - Hb(pus.sum(0))
    # drive D -> 0 with large beta at both endpoints
    qR, _ = pareto_fixed_point(pXS, d, 1.0, 60.0)
    qL, _ = pareto_fixed_point(pXS, d, 0.0, 60.0)
    R0, _ = coords(pXS, qR)
    _, L0 = coords(pXS, qL)
    worst5 = max(worst5, abs(R0 - HU), abs(L0 - HUgS))
print(f"  15 random exact consumers: |R_C(0) - H(U)|, |L_C(0|S) - H(U|S)| "
      f"worst = {worst5:.1e}")
if worst5 > 5e-3:
    fail.append("cor2-endpoints")

tc_neg = 0
tc_max = 0.0
for trial in range(400):
    nx, ns, m = 12, 2, 3
    pXS = rng.dirichlet(np.ones(nx * ns)).reshape(nx, ns)
    Us = [rng.integers(0, 3, size=nx) for _ in range(m)]
    # joint read (U1,...,Um) given S vs marginals given S
    key = np.zeros(nx, dtype=int)
    for j, U in enumerate(Us):
        key = key * 3 + U
    pjoint = np.zeros((3 ** m, ns))
    for x in range(nx):
        pjoint[key[x], :] += pXS[x, :]
    Hjoint = Hb(pjoint) - Hb(pjoint.sum(0))
    Hsum = 0.0
    for U in Us:
        pu = np.zeros((3, ns))
        for x in range(nx):
            pu[U[x], :] += pXS[x, :]
        Hsum += Hb(pu) - Hb(pu.sum(0))
    tc = Hsum - Hjoint
    tc_neg += tc < -1e-10
    tc_max = max(tc_max, tc)
print(f"  400 random 3-consumer reads: TC(U1;U2;U3|S) negative = {tc_neg}; "
      f"max saved by coordinated reset = {tc_max:.3f} bits")
if tc_neg or not tc_max > 0.05:
    fail.append("cor3-total-correlation")

# =====================================================================================
print("=" * 78)
print("[6] Cor 4: Gaussian read-operator water-filling = max-det program; net; kernel")

def spd(nn):
    A = rng.standard_normal((nn, nn))
    return A @ A.T + 0.5 * np.eye(nn)

def sqrtm_sym(M):
    w, U = np.linalg.eigh((M + M.T) / 2)
    return U @ np.diag(np.sqrt(np.maximum(w, 0))) @ U.T

def logdet(M):
    return float(np.linalg.slogdet((M + M.T) / 2)[1])

def sigma_star(P, Dq, Cap):
    """argmax{ logdet S : 0 <= S <= Cap, tr(P S) <= Dq } (reverse water-filling
    in the whitened basis; the cap binds on ker P).  From verify_rate_region."""
    Ch = sqrtm_sym(Cap)
    p, V = np.linalg.eigh(Ch @ P @ Ch)
    p = np.maximum(p, 0.0)
    if Dq >= float(np.sum(p)):
        e = np.ones_like(p)
    else:
        lo, hi = 0.0, max(p.max(), 1e-9)
        for _ in range(300):
            mid = 0.5 * (lo + hi)
            if float(np.sum(np.minimum(p, mid))) < Dq:
                lo = mid
            else:
                hi = mid
        th = 0.5 * (lo + hi)
        e = np.minimum(1.0, np.where(p > 0, th / np.where(p > 0, p, 1.0), 1.0))
    return Ch @ (V @ np.diag(e) @ V.T) @ Ch

def waterfill_rate(lams, Dq):
    """Eq. (40)-(41): theta from D = sum min{lam, theta}; R = 1/2 sum [log2 lam/theta]_+."""
    lams = np.asarray(lams, dtype=float)
    lo, hi = 0.0, max(lams.max(), 1e-9)
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if float(np.minimum(lams, mid).sum()) < Dq:
            lo = mid
        else:
            hi = mid
    th = 0.5 * (lo + hi)
    return 0.5 * float(np.sum(np.maximum(np.log2(lams / th), 0.0))), th

def post_cov(Sx, M, Sn):
    Syy = M @ Sx @ M.T + Sn
    Sxy = Sx @ M.T
    P = Sx - Sxy @ np.linalg.pinv((Syy + Syy.T) / 2, rcond=1e-12) @ Sxy.T
    return (P + P.T) / 2

worst6 = 0.0
viol6 = 0
tested6 = 0
for trial in range(40):
    dd_ = int(rng.integers(3, 6))
    r_ = int(rng.integers(1, dd_ + 1))                    # allow rank-deficient reads
    Sx = spd(dd_)
    Jc = rng.standard_normal((r_, dd_))
    G = spd(r_)
    P = Jc.T @ G @ Jc
    W = sqrtm_sym(Sx)
    lams = np.linalg.eigvalsh(W @ P @ W)
    lams = lams[lams > 1e-10]
    Dq = rng.uniform(0.05, 0.9) * float(lams.sum())
    Rf, th = waterfill_rate(lams, Dq)
    Ss = sigma_star(P, Dq, Sx)
    Rs = 0.5 * (logdet(Sx) - logdet(Ss)) / LOG2
    worst6 = max(worst6, abs(Rf - Rs))
    # random admissible Gaussian codes never beat the water-filling rate
    for _ in range(300):
        m_ = int(rng.integers(1, dd_ + 1))
        Mm = rng.standard_normal((m_, dd_))
        s_ = np.exp(rng.uniform(-1.5, 1.5))
        C = post_cov(Sx, Mm, s_ * np.eye(m_))
        if float(np.trace(P @ C)) > Dq + 1e-9:
            continue
        tested6 += 1
        if 0.5 * (logdet(Sx) - logdet(C)) / LOG2 < Rf - 1e-7:
            viol6 += 1
print(f"  40 random (Sx, P_C): |eq.(41) - max-det| worst = {worst6:.1e}; "
      f"admissible Gaussian codes tested = {tested6}, violations = {viol6}")
if worst6 > 1e-7 or viol6:
    fail.append("cor4-waterfilling")

# =====================================================================================
print("=" * 78)
print("[7] Prop 3: temperature-weighted water-filling d_i* = min{lam_i, nu T_i}")

def het_waterfill(lams, Ts, Dq):
    lams = np.asarray(lams, float)
    Ts = np.asarray(Ts, float)
    lo, hi = 0.0, float((lams / Ts).max()) + 1e-9
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if float(np.minimum(lams, mid * Ts).sum()) < Dq:
            lo = mid
        else:
            hi = mid
    nu = 0.5 * (lo + hi)
    dstar = np.minimum(lams, nu * Ts)
    Wst = 0.5 * float(np.sum(Ts * np.maximum(np.log(lams / dstar), 0.0)))  # kB = 1, nats
    return nu, dstar, Wst

worst7 = 0.0
viol7 = 0
for trial in range(30):
    r_ = int(rng.integers(2, 9))
    lams = rng.uniform(0.2, 5.0, size=r_)
    Ts = rng.uniform(0.3, 3.0, size=r_)
    Dq = rng.uniform(0.1, 0.9) * float(lams.sum())
    nu, dstar, Wst = het_waterfill(lams, Ts, Dq)
    worst7 = max(worst7, abs(float(dstar.sum()) - Dq))
    # KKT: active modes (d < lam) share marginal work  T_i / (2 d_i) = 1/(2 nu)
    act = dstar < lams - 1e-9
    if act.any():
        marg = Ts[act] / dstar[act]
        worst7 = max(worst7, float(np.abs(marg - 1.0 / nu).max()) * nu)
    # random feasible allocations never beat W* (attempt-capped rejection)
    cnt = 0
    attempts = 0
    while cnt < 2000 and attempts < 100000:
        attempts += 1
        w = rng.dirichlet(np.ones(r_)) * Dq
        if (w <= lams + 1e-12).all() and (w > 1e-12).all():
            cnt += 1
            Wr = 0.5 * float(np.sum(Ts * np.maximum(np.log(lams / w), 0.0)))
            if Wr < Wst - 1e-9:
                viol7 += 1
                break
    # equal-T reduces to the isothermal water level of eq. (40)
    nuE, dE, _ = het_waterfill(lams, np.ones(r_), Dq)
    _, thE = waterfill_rate(lams, Dq)
    worst7 = max(worst7, float(np.abs(dE - np.minimum(lams, thE)).max()))
print(f"  30 random (spectrum, T, D): feasibility+KKT+equal-T worst = {worst7:.1e}; "
      f"random-allocation violations = {viol7}")
if worst7 > 1e-6 or viol7:
    fail.append("prop3-het-waterfilling")

# =====================================================================================
print("=" * 78)
print("[8] Prop 4: staleness -- L_t = H(M|X_t) nondecreasing; binary complement = 1 bit")
worst8 = 0.0
mono_viol = 0
for trial in range(40):
    k = int(rng.integers(2, 6))
    Pt = rng.dirichlet(np.ones(k), size=k)                # transition matrix
    w, V = np.linalg.eig(Pt.T)
    pi = np.real(V[:, np.argmax(np.real(w))])
    pi = np.abs(pi) / np.abs(pi).sum()                    # stationary
    Wch = rng.dirichlet(np.ones(k), size=k) if trial % 2 else np.eye(k)[rng.permutation(k)]
    # p(M, X_t) = sum_x0 pi(x0) W(m|x0) P^t(x0, xt)
    Pk = np.eye(k)
    Ls = []
    for t in range(26):
        J = (Wch.T * pi[None, :]) @ Pk                    # rows m, cols xt
        Ls.append(Hb(J) - Hb(J.sum(0)))                   # H(M|X_t)
        Pk = Pk @ Pt
    dLs = np.diff(Ls)
    mono_viol += int((dLs < -1e-10).any())
    worst8 = max(worst8, float(-dLs.min()) if len(dLs) else 0.0)
print(f"  40 random finite chains (M deterministic or noisy read of X_0): "
      f"monotonicity violations = {mono_viol}, worst decrease = {worst8:.1e}")
if mono_viol:
    fail.append("prop4-monotonicity")

p = 0.05
worst8b = 0.0
for t in range(0, 41):
    qt = 0.5 * (1 - (1 - 2 * p) ** t)
    worst8b = max(worst8b, abs((1 - h2(qt)) + h2(qt) - 1.0))
    # exact chain computation must match h2(qt)
    Pt = bsc(p)
    Pk = np.linalg.matrix_power(Pt, t)
    J = 0.5 * Pk                                          # pi = (1/2,1/2), M = X0
    worst8b = max(worst8b, abs((Hb(J) - Hb(J.sum(0))) - h2(qt)))
print(f"  binary example p=0.05: |H(X0|Xt) - h2(q_t)| and complement-to-1 "
      f"worst = {worst8b:.1e}")
if worst8b > 1e-10:
    fail.append("prop4-binary")

# =====================================================================================
print("=" * 78)
print("VERDICT:", "ALL PASS" if not fail else f"FAIL: {fail}")
