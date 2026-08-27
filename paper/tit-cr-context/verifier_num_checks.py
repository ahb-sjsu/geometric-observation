# Fresh-context numeric verification of tit-cr-context.tex Secs IV, V, VII.
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(20260826)
log2 = np.log2
fails = []
def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), name, detail)
    if not ok: fails.append((name, detail))

# ---------- closed form of thm:function ----------
def gstar(rho2, tau2, D):
    s = 1+tau2
    Bc = D+s-rho2
    disc = Bc*Bc - 4*D*s*(1-rho2)
    return (Bc + np.sqrt(disc))/(2*D*s)

def channel(rho2, tau2, D):
    s = 1+tau2; g = gstar(rho2, tau2, D)
    rho = np.sqrt(rho2); k = g*s-1
    mu = rho*(g-1)/k
    a = 1-1/g; b = mu/g
    Q0 = a*a+b*b+2*a*b*rho
    Q1 = Q0 - (a*rho+b)**2/s
    n = Q1/(g-1)
    return g, a, b, n, Q0, Q1, mu

def B1(rho2, tau2, D, a, b):
    s = 1+tau2; rho = np.sqrt(rho2)
    h = (1-a)**2 - 2*(1-a)*b*rho + b*b
    n = D-h
    if n <= 1e-14: return 1e9
    Q1 = a*a+b*b+2*a*b*rho - (a*rho+b)**2/s
    return 0.5*log2((Q1+n)/n)

def B0(rho2, tau2, D, a, b):
    rho = np.sqrt(rho2)
    h = (1-a)**2 - 2*(1-a)*b*rho + b*b
    n = D-h
    if n <= 1e-14: return 1e9
    Q0 = a*a+b*b+2*a*b*rho
    return 0.5*log2((Q0+n)/n)

def brute_min(f, multistart=40, dim=2, scale=1.0, center=None):
    best = None
    for i in range(multistart):
        x0 = rng.normal(0, scale, dim) if center is None else np.asarray(center) + rng.normal(0, scale*(0.02 + i/multistart), dim)
        r = minimize(f, x0, method='Nelder-Mead',
                     options=dict(xatol=1e-13, fatol=1e-14, maxiter=20000, maxfev=20000))
        if r.fun >= 1e8: continue
        if best is None or r.fun < best.fun: best = r
    return best

# A. thm:function vs brute force, plus direct Gaussian-MI evaluation from the joint covariance
def gauss_cmi(K, iT, iY, iS):
    # I(T;Y|S) for jointly Gaussian with covariance K, index lists
    def cdet(idx, cond):
        idx = list(idx); cond = list(cond)
        A = K[np.ix_(idx, idx)]
        if cond:
            B = K[np.ix_(idx, cond)]; C = K[np.ix_(cond, cond)]
            A = A - B @ np.linalg.solve(C, B.T)
        return np.linalg.det(A)
    return 0.5*log2(cdet(iT, iS)*cdet(iY, iS)/cdet(list(iT)+list(iY), iS))

maxerr_val = 0; maxerr_mom = 0; maxerr_D = 0; maxerr_mi = 0
for trial in range(60):
    rho2 = rng.uniform(0.02, 0.97); tau2 = rng.uniform(0.02, 4.0); D = rng.uniform(0.03, 0.95)
    g, a, b, n, Q0, Q1, mu = channel(rho2, tau2, D)
    L = 0.5*log2(g)
    r = brute_min(lambda x: B1(rho2, tau2, D, x[0], x[1]), center=(1-D, 0.0))
    maxerr_val = max(maxerr_val, abs(r.fun - L))
    maxerr_mom = max(maxerr_mom, np.hypot(r.x[0]-a, r.x[1]-b))
    rho = np.sqrt(rho2); s = 1+tau2
    h = (1-a)**2 - 2*(1-a)*b*rho + b*b
    maxerr_D = max(maxerr_D, abs(h+n-D))
    # direct MI from joint covariance of (Y,V,Yhat,S)
    K = np.array([
      [1,       rho,     a+b*rho,      rho],
      [rho,     1,       a*rho+b,      1],
      [a+b*rho, a*rho+b, Q0+n,         a*rho+b],
      [rho,     1,       a*rho+b,      s]])
    mi = gauss_cmi(K, [0,1], [2], [3])
    maxerr_mi = max(maxerr_mi, abs(mi - L))
check("thm:function value = brute-force min over (a,b), 60 random instances",
      maxerr_val < 5e-9, f"max val err {maxerr_val:.2e}")
check("thm:function optimizer = (a*,b*) of eq:channel",
      maxerr_mom < 5e-6, f"max moment err {maxerr_mom:.2e}")
check("achieving channel meets distortion with equality (h+n=D)",
      maxerr_D < 1e-12, f"max err {maxerr_D:.2e}")
check("I(T;Yhat|S) from joint covariance entropies = (1/2)log2 g*",
      maxerr_mi < 1e-10, f"max err {maxerr_mi:.2e}")

# B. anchors, numerically
D = 0.2
check("anchor rho=0: g*=1/D", abs(gstar(0.0, 0.7, D) - 1/D) < 1e-12)
for rho2 in (0.3, 0.85, 0.95):   # avoid the exact double-root boundary (1-rho2)/D=1
    lim = gstar(rho2, 1e-12, D)
    check(f"anchor tau->0 rho2={rho2}: g*->max(1,(1-rho2)/D)",
          abs(lim - max(1.0, (1-rho2)/D)) < 1e-6, f"{lim:.8f}")
# boundary case (1-rho2)/D = 1: convergence is O(tau), still to the right limit
for t2 in (1e-4, 1e-6, 1e-8):
    pass
check("anchor tau->0 at double-root boundary rho2=0.8,D=0.2 (O(tau) rate)",
      abs(gstar(0.8, 1e-8, D) - 1.0) < 1e-3 and abs(gstar(0.8, 1e-12, D) - 1.0) < 1e-5)
tau2 = 0.5
lim = gstar(1-1e-12, tau2, D)
check("anchor rho2->1: g*->(D+tau2)/(D s)",
      abs(lim - (D+tau2)/(D*(1+tau2))) < 1e-6, f"{lim:.8f}")

# C. cor:notmarginal numbers
v1 = 0.5*log2(5); v2 = 0.5*log2(5/3)
g1 = (17+np.sqrt(229))/6; g2 = (21+np.sqrt(261))/18
check("notmarginal: g* surd (D=0.1) matches quadratic root",
      abs(g1 - gstar(0.75, 0.5, 0.1)) < 1e-12, f"{g1:.6f}")
check("notmarginal: g* surd (D=0.3) matches quadratic root",
      abs(g2 - gstar(0.75, 0.5, 0.3)) < 1e-12, f"{g2:.6f}")
print(f"   values: L(inst1,D=.1)={v1:.6f}  L(inst2,D=.1)={0.5*log2(g1):.6f}  Steinberg={0.5*log2(5.5):.6f}")
print(f"   values: L(inst1,D=.3)={0.5*log2(5/3):.6f}  L(inst2,D=.3)={0.5*log2(g2):.6f}  Steinberg={0.5*log2(13/6):.6f}")
check("notmarginal quoted decimals (1.1610, 1.2105, 1.2297)",
      abs(v1-1.1610)<5e-5 and abs(0.5*log2(g1)-1.2105)<5e-5 and abs(0.5*log2(5.5)-1.2297)<5e-5)
check("notmarginal quoted decimals (0.3685, 0.5228, 0.5577)",
      abs(v2-0.3685)<5e-5 and abs(0.5*log2(g2)-0.5228)<5e-5 and abs(0.5*log2(13/6)-0.5577)<5e-5)
check("ordering: both L strictly below Steinberg margin",
      v1 < 0.5*log2(5.5) and 0.5*log2(g1) < 0.5*log2(5.5)
      and v2 < 0.5*log2(13/6) and 0.5*log2(g2) < 0.5*log2(13/6))
check("same (Y,S) margin: rho2/s equal for both instances",
      abs(0.5/1.0 - 0.75/1.5) < 1e-15)

# D. cor:misalign numbers at (rho2,tau2,D)=(0.75,0.5,0.3)
rho2, tau2, D = 0.75, 0.5, 0.3
g, a, b, n, Q0, Q1, mu = channel(rho2, tau2, D)
R0 = 0.5*log2((Q0+n)/n); Rmin = 0.5*log2(1/D)
s = 1+tau2
L1 = 0.5*log2(((1-D)*(1-rho2/s)+D)/D); LD = 0.5*log2(g)
print(f"   misalign: R(0)-Rmin={R0-Rmin:.6f}   L(1)-L(D)={L1-LD:.6f}")
check("misalign quoted 0.0400", abs((R0-Rmin)-0.0400) < 5e-5, f"{R0-Rmin:.6f}")
check("misalign quoted 0.0349", abs((L1-LD)-0.0349) < 5e-5, f"{L1-LD:.6f}")
# cross-check L(1) is B1 at the rate-optimal moments (1-D, 0, D(1-D))
check("L(1) equals B1 at (1-D,0,D(1-D))",
      abs(B1(rho2,tau2,D,1-D,0.0) - L1) < 1e-12)
# rate-minimizer via brute force is (1-D, 0)
r = brute_min(lambda x: B0(rho2, tau2, D, x[0], x[1]))
check("rate program brute min = (1-D,0), value (1/2)log2(1/D)",
      abs(r.fun-Rmin) < 1e-9 and np.hypot(r.x[0]-(1-D), r.x[1]) < 1e-5,
      f"x={r.x}, f={r.fun:.9f}")

# E. thm:region: scipy minimizer of weighted objective satisfies the two-level system
def phi_alpha(al, rho2, tau2, D, a, b):
    rho = np.sqrt(rho2); s = 1+tau2
    h = (1-a)**2-2*(1-a)*b*rho+b*b
    n = D-h
    if n <= 1e-14: return 1e9
    Q0 = a*a+b*b+2*a*b*rho; Q1 = Q0-(a*rho+b)**2/s
    return al*0.5*log2((Q0+n)/n)+(1-al)*0.5*log2((Q1+n)/n)

frontier = []
worst_sys = 0
for al in (0.0, 0.25, 0.5, 0.75, 1.0):
    r = brute_min(lambda x: phi_alpha(al, rho2, tau2, D, x[0], x[1]))
    a_, b_ = r.x
    rho = np.sqrt(rho2)
    h = (1-a_)**2-2*(1-a_)*b_*rho+b_*b_; n_ = D-h
    Q0_ = a_*a_+b_*b_+2*a_*b_*rho; Q1_ = Q0_-(a_*rho+b_)**2/s
    g0 = n_/(Q0_+n_); g1_ = n_/(Q1_+n_)
    mu_ = (a_*rho+b_)/s
    # residuals of eq:twolevel-1
    r1 = a_ - (1 - al*g0 - (1-al)*g1_)
    r2 = mu_ - a_*rho/(s-(1-al)*g1_)
    r3 = b_ - (1-al)*g1_*mu_
    res = max(abs(r1), abs(r2), abs(r3))
    worst_sys = max(worst_sys, res)
    frontier.append((al, 0.5*log2(1/g0), 0.5*log2(1/g1_)))
check("two-water-level system holds at brute minimizers, alpha grid",
      worst_sys < 1e-6, f"worst residual {worst_sys:.2e}")
R_list = [f[1] for f in frontier]; L_list = [f[2] for f in frontier]
check("frontier monotone: R increasing, L decreasing as alpha->0",
      all(np.diff(R_list[::-1]) >= -1e-9) and all(np.diff(L_list[::-1]) <= 1e-9),
      str([(round(f[0],2), round(f[1],4), round(f[2],4)) for f in frontier]))
check("alpha=0 endpoint matches thm:function (gamma1=1/g*)",
      abs(frontier[0][2]-LD) < 1e-6 and abs(frontier[0][1]-R0) < 1e-6,
      f"dL={frontier[0][2]-LD:.2e} dR={frontier[0][1]-R0:.2e}")
check("alpha=1 endpoint: (R,L)=(Rmin, L(1))",
      abs(frontier[-1][1]-Rmin) < 1e-6 and abs(frontier[-1][2]-L1) < 1e-6,
      f"dR={frontier[-1][1]-Rmin:.2e} dL={frontier[-1][2]-L1:.2e}")

# uniqueness spot check: multistart returns single optimizer at alpha=0.5
xs = []
for _ in range(30):
    x0 = rng.normal(0, 1.5, 2)
    r = minimize(lambda x: phi_alpha(0.5, rho2, tau2, D, x[0], x[1]), x0,
                 method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-13, maxiter=20000, maxfev=20000))
    if r.fun < 1e8: xs.append(r.x)
xs = np.array(xs)
check("prop:uniq spot: all multistarts converge to one point (alpha=0.5)",
      xs.std(axis=0).max() < 1e-5, f"spread {xs.std(axis=0).max():.2e}")

# F. lem:gauss general determinant identity, random matrices (p=3, r=2, m=2)
maxerr = 0
for _ in range(200):
    p, rr, m = 3, 2, 2
    G = rng.normal(0, 1, (p+rr, p+rr)); C = G @ G.T + 0.1*np.eye(p+rr)
    SigT = C[:p,:p]; SigS = C[p:,p:]; SigTS = C[:p,p:]
    SigTcS = SigT - SigTS @ np.linalg.solve(SigS, SigTS.T)
    A = rng.normal(0, 1, (m, p))
    Gn = rng.normal(0, 1, (m, m)); SigN = Gn @ Gn.T + 0.05*np.eye(m)
    # joint covariance of (T,S,Yhat), Yhat = A T + N
    SigYh = A @ SigT @ A.T + SigN
    SigYhT = A @ SigT; SigYhS = A @ SigTS
    K = np.block([[SigT, SigTS, SigYhT.T],
                  [SigTS.T, SigS, SigYhS.T],
                  [SigYhT, SigYhS, SigYh]])
    M = np.block([[SigYh, SigYhS],[SigYhS.T, SigS]])
    J = np.block([SigYhT.T, SigTS])
    Sig_e = SigT - J @ np.linalg.solve(M, J.T)
    lhs = np.linalg.det(Sig_e)
    rhs = np.linalg.det(SigTcS)*np.linalg.det(SigN)/np.linalg.det(A@SigTcS@A.T + SigN)
    maxerr = max(maxerr, abs(lhs-rhs)/abs(rhs))
    # det K three-factor identity
    e2 = abs(np.linalg.det(K) - np.linalg.det(SigS)*np.linalg.det(SigTcS)*np.linalg.det(SigN))/abs(np.linalg.det(K))
    maxerr = max(maxerr, e2)
check("lem:gauss determinant identity, 200 random (p=3,r=2,m=2) instances",
      maxerr < 1e-9, f"max rel err {maxerr:.2e}")

# G. lem:mxconvex spot checks: F(z)=a(z)a(z)^T/sigma(z), a affine, sigma concave
mineig = np.inf
for _ in range(300):
    q, p = 4, 3
    Fm = rng.normal(0,1,(p,q)); f0 = rng.normal(0,1,p)
    cq = rng.normal(0,1,(q,q)); Qm = cq@cq.T*0.1   # sigma = s0 + w.z - z^T Qm z concave
    w = rng.normal(0,1,q); s0 = 25.0
    z0 = rng.normal(0,1,q); z1 = rng.normal(0,1,q); t = rng.uniform(0,1)
    zt = (1-t)*z0+t*z1
    def sig(z): return s0 + w@z - z@Qm@z
    def F(z):
        az = Fm@z+f0
        return np.outer(az,az)/sig(z)
    if min(sig(z0), sig(z1), sig(zt)) <= 0.5: continue
    Mx = (1-t)*F(z0)+t*F(z1)-F(zt)
    mineig = min(mineig, np.linalg.eigvalsh(Mx).min())
check("lem:mxconvex: (1-t)F0+tF1-F(zt) PSD over 300 random trials",
      mineig > -1e-10, f"min eig {mineig:.2e}")

# H. prop:uniq convexity spot check: B_alpha convex along random segments (p=3)
p = 3
Lam = np.diag(rng.uniform(0.05, 1.0, p))
y0v = rng.normal(0,1,p); y0v /= np.linalg.norm(y0v)
Dv = 0.4
def Bal(al, c, v):
    nl = v - c@c
    if nl <= 1e-13: return None
    sg = v - c@((np.eye(p)-Lam)@c)
    return al*0.5*log2(v/nl) + (1-al)*0.5*log2(sg/nl)
worst = np.inf; count = 0
while count < 300:
    c0 = y0v + rng.normal(0, 0.2, p); c1 = y0v + rng.normal(0, 0.2, p)
    v0 = c0@c0 + rng.uniform(0.01, 0.2); v1 = c1@c1 + rng.uniform(0.01, 0.2)
    # keep inside distortion set
    if 1-2*y0v@c0+v0 > Dv or 1-2*y0v@c1+v1 > Dv: continue
    al = rng.uniform(0,1)
    f0_ = Bal(al, c0, v0); f1_ = Bal(al, c1, v1)
    fm = Bal(al, 0.5*(c0+c1), 0.5*(v0+v1))
    if None in (f0_, f1_, fm): continue
    worst = min(worst, 0.5*f0_+0.5*f1_-fm)
    count += 1
check("prop:uniq: midpoint convexity of B_alpha on domain D, 300 trials",
      worst > -1e-11, f"min gap {worst:.2e}")

# I. thm:vector, r=2 (p=3): brute min over c vs the alpha=0 scalar root of eq:vecfoc
def vec_obj(al, c, Lam, y0v, Dv):
    h = (y0v-c)@(y0v-c); nl = Dv-h
    if nl <= 1e-13: return 1e9
    Q0v = c@c; Q1v = c@(Lam@c)
    return al*0.5*log2((Q0v+nl)/nl) + (1-al)*0.5*log2((Q1v+nl)/nl)

for trial in range(5):
    Lam = np.diag(rng.uniform(0.05, 1.0, p))
    y0v = rng.normal(0,1,p); y0v /= np.linalg.norm(y0v)
    Dv = rng.uniform(0.1, 0.8)
    r = brute_min(lambda c: vec_obj(0.0, c, Lam, y0v, Dv), dim=p, scale=0.7)
    # scalar root problem in gamma1 from eq:vecfoc at alpha=0
    def resid(g1v):
        cc = (1-g1v)*np.linalg.solve((1-g1v)*np.eye(p)+g1v*Lam, y0v)
        nl = Dv - (y0v-cc)@(y0v-cc)
        if nl <= 0: return None
        return g1v*(cc@(Lam@cc)+nl) - nl
    lo, hi = 1e-9, 1-1e-9
    grid = np.linspace(lo, hi, 40001)
    vals = np.array([resid(x) if resid(x) is not None else np.nan for x in grid])
    sgn = np.sign(vals)
    idx = np.where(np.diff(sgn[~np.isnan(vals)]) != 0)[0]
    gr = grid[~np.isnan(vals)]
    roots = []
    for i in idx:
        aL, bL = gr[i], gr[i+1]
        for _ in range(80):
            mid = 0.5*(aL+bL)
            if resid(aL)*resid(mid) <= 0: bL = mid
            else: aL = mid
        roots.append(0.5*(aL+bL))
    Lroots = [0.5*log2(1/rt) for rt in roots]
    ok = any(abs(Lr - r.fun) < 1e-7 for Lr in Lroots)
    check(f"thm:vector r=2 trial {trial}: alpha=0 scalar-root value = brute min",
          ok, f"brute {r.fun:.8f}, roots {[round(x,8) for x in Lroots]}")

# vector FOC at generic alpha: check eq:vecfoc holds at brute minimizer
Lam = np.diag(rng.uniform(0.05, 1.0, p))
y0v = rng.normal(0,1,p); y0v /= np.linalg.norm(y0v)
Dv = 0.35; al = 0.4
r = brute_min(lambda c: vec_obj(al, c, Lam, y0v, Dv), dim=p, scale=0.7)
c_ = r.x; h_ = (y0v-c_)@(y0v-c_); n_ = Dv-h_
g0 = n_/(c_@c_+n_); g1v = n_/(c_@(Lam@c_)+n_)
lhs = ((1-(1-al)*g1v)*np.eye(p)+(1-al)*g1v*Lam) @ c_
rhs = (1-al*g0-(1-al)*g1v)*y0v
check("thm:vector eq:vecfoc holds at brute minimizer (alpha=0.4, r=2)",
      np.abs(lhs-rhs).max() < 1e-6, f"max residual {np.abs(lhs-rhs).max():.2e}")

# J. thm:vector at r=1 == thm:function (whitening included)
rho2, tau2, D = 0.75, 0.5, 0.3
rho = np.sqrt(rho2); s = 1+tau2
SigT = np.array([[1, rho],[rho, 1]])
SigTS = np.array([[rho],[1.0]])
SigTcS = SigT - SigTS@SigTS.T/s
Lch = np.linalg.cholesky(SigT)
Mw = np.linalg.solve(Lch, np.linalg.solve(Lch, SigTcS).T).T  # L^{-1} SigTcS L^{-T}
lam, O = np.linalg.eigh(Mw)
W = O.T @ np.linalg.inv(Lch)
check("whitening: W SigT W^T = I", np.abs(W@SigT@W.T-np.eye(2)).max() < 1e-12)
check("whitening: W SigTcS W^T = Lambda diag", np.abs(W@SigTcS@W.T-np.diag(lam)).max() < 1e-12)
eY = np.array([1.0, 0.0])
y0w = np.linalg.solve(W.T, eY)
check("whitening: |y0| = 1", abs(np.linalg.norm(y0w)-1) < 1e-12)
Lam2 = np.diag(lam)
r = brute_min(lambda c: vec_obj(0.0, c, Lam2, y0w, D), dim=2, scale=0.7)
g, a, b, n, Q0, Q1, mu = channel(rho2, tau2, D)
check("thm:vector r=1 alpha=0 value = thm:function value",
      abs(r.fun - 0.5*log2(g)) < 1e-8, f"{r.fun:.9f} vs {0.5*log2(g):.9f}")
c_from_ab = np.linalg.solve(W.T, np.array([a,b]))
check("r=1 minimizer maps via c=W^{-T}(a,b)", np.abs(r.x - c_from_ab).max() < 1e-5,
      f"{r.x} vs {c_from_ab}")
# also full frontier match at alpha=0.5
r_vec = brute_min(lambda c: vec_obj(0.5, c, Lam2, y0w, D), dim=2, scale=0.7)
r_ab  = brute_min(lambda x: phi_alpha(0.5, rho2, tau2, D, x[0], x[1]))
check("r=1 alpha=0.5 weighted values agree (vector vs scalar coords)",
      abs(r_vec.fun-r_ab.fun) < 1e-8, f"{r_vec.fun:.9f} vs {r_ab.fun:.9f}")

# K. prop:marg channel checks (instance 1 of cor:notmarginal)
for Dv in (0.1, 0.3):
    # X=(X1,X2) iid N(0,1), Y=X1, S=X1+X2, channel Yhat=(1-Dv)X1+Dv X2+N, VarN=Dv(1-2Dv)
    a1, b1, vN = 1-Dv, Dv, Dv*(1-2*Dv)
    K = np.array([
      [1, 0, 1, a1],
      [0, 1, 1, b1],
      [1, 1, 2, a1+b1],
      [a1, b1, a1+b1, a1*a1+b1*b1+vN]])
    dist = 1 - 2*a1 + a1*a1+b1*b1+vN
    # S is X-measurable, so use I(X;Yhat|S) = h(Yhat|S) - h(Yhat|X,S) = h(Yhat|S)-h(Yhat|X)
    varYh = a1*a1+b1*b1+vN
    varYh_S = varYh - (a1+b1)**2/2.0
    mi = 0.5*log2(varYh_S/vN)
    check(f"prop:marg channel D={Dv}: distortion=D and I(X;Yhat|S)=0.5log2(1/(2D))",
          abs(dist-Dv) < 1e-12 and abs(mi-0.5*log2(1/(2*Dv))) < 1e-10,
          f"dist {dist:.6f}, MI {mi:.6f}")

print()
print("FAILURES:", fails if fails else "none")
