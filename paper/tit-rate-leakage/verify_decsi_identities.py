"""verify_decsi_identities.py: numerical checks of the identities in the decoder side-information section (2026-10-02).

N1 Lemma mmsecomp: fixed-gain identity (I-LB)M(I-LB)' + LL' = (M^-1 + B'B)^-1, random M > 0, B of any rank.
N2 Lemma mmsecomp: Monte Carlo of the affine estimate on a NON-Gaussian description (T Gaussian, V = sign quantizer of
   a projection, C' a Gaussian observation): the affine estimate's error covariance equals (M_C^-1 + J_+)^-1, and the
   average over cells of (V, C') of the per-cell best affine error, which bounds the MMSE from above, lies below it.
   Cells of C' are 200 quantile bins, so conditional moments are estimated, to Monte Carlo accuracy.
N3 Degradedness with singular J_C: A = J_S J_C^+ gives A J_C = J_S and J_S - A J_C A' >= 0; the constructed statistic
   A c + extra noise has exactly the joint second moments with T of J_S T + nu_S.
N4 Theorem decsi(b): (Sigma_{T|C}^-1 + J_S - J_C)^-1 = Sigma_{T|S}.
N5 Carry-over: det(H X H' + Sigma_U) = det(Sigma_U) det(I + J X), with H rank-deficient.
N6 Carry-over: for V = a'T + N, Cov(T | V, C) = (Sigma_{T|C}^-1 + a a'/sigma^2)^-1 by direct Gaussian conditioning.
N7 Finite-alphabet leakage identity: H(X|E) - H(X|V,C) - I(X;C|V0) + I(X;E|V0) = I(X;V|C) + I(V0;C) - I(V0;E)
   for random pmfs with V0 a function of V and V-X-(C,E).
"""
import numpy as np
from scipy.stats import norm
from scipy.linalg import sqrtm

rng = np.random.default_rng(20261002)
fails = 0
def check(name, ok, detail):
    global fails
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}"); fails += (not ok)

def rand_pd(p, r=None):
    G = rng.normal(size=(p, p if r is None else r)); return G @ G.T + (0.3 * np.eye(p) if r is None else 0)

# N1
err = 0.0
for _ in range(500):
    p = rng.integers(2, 6); k = rng.integers(1, p + 2); M = rand_pd(p); B = rng.normal(size=(k, p))
    L = M @ B.T @ np.linalg.inv(B @ M @ B.T + np.eye(k))
    lhs = (np.eye(p) - L @ B) @ M @ (np.eye(p) - L @ B).T + L @ L.T
    err = max(err, np.abs(lhs - np.linalg.inv(np.linalg.inv(M) + B.T @ B)).max())
check("N1 fixed-gain identity", err < 1e-9, f"max abs error {err:.2e} over 500 random cases")

# N2: T ~ N(0, Sigma) in R^2, C' = h'T + N_C, V = sign(g'T), O = B T + n, Monte Carlo with 400000 draws.
Sigma = np.array([[1.0, 0.4], [0.4, 0.7]]); h = np.array([0.8, -0.3]); sc = 0.5; g = np.array([1.0, 0.6])
Bm = np.array([[0.9, 0.2]]); n = 400000
T = rng.multivariate_normal(np.zeros(2), Sigma, size=n); V = np.sign(T @ g)
Cp = T @ h + np.sqrt(sc) * rng.normal(size=n); O = T @ Bm.T + rng.normal(size=(n, 1))
# E[T | V, C'] by binning C' finely within each V class (nonparametric, consistent)
bins = np.quantile(Cp, np.linspace(0, 1, 201)); cb = np.clip(np.searchsorted(bins, Cp) - 1, 0, 199)
cell = (V > 0).astype(int) * 200 + cb
mean_w = np.zeros((400, 2)); cov_w = np.zeros((400, 2, 2)); cnt = np.bincount(cell, minlength=400)
for c in np.unique(cell):
    Tc = T[cell == c]; mean_w[c] = Tc.mean(0); cov_w[c] = np.cov(Tc.T, bias=True)
MC = np.einsum('c,cij->ij', cnt / n, cov_w)
L = MC @ Bm.T @ np.linalg.inv(Bm @ MC @ Bm.T + np.eye(1))
est = mean_w[cell] + (O - mean_w[cell] @ Bm.T) @ L.T
err_cov = np.cov((T - est).T, bias=True); target = np.linalg.inv(np.linalg.inv(MC) + Bm.T @ Bm)
dev = np.abs(err_cov - target).max()
# per-cell best affine estimate from O (error (C_w^-1 + J_+)^-1); it bounds the MMSE given (V, C', O) from above
mmse = np.einsum('c,cij->ij', cnt / n, np.array([np.linalg.inv(np.linalg.inv(cw + 1e-12 * np.eye(2)) + Bm.T @ Bm) for cw in cov_w]))
gap = np.linalg.eigvalsh(target - mmse).min()
check("N2 affine estimate on a non-Gaussian description", dev < 5e-3 and gap > -5e-3,
      f"|error cov - (M_C^-1+J_+)^-1| {dev:.1e}; min eig of bound - per-cell affine error {gap:+.1e} (>= 0 up to Monte Carlo)")

# N3
worst_a, worst_psd, worst_mom = 0.0, np.inf, 0.0
for _ in range(300):
    p = rng.integers(2, 6); r = rng.integers(1, p); Gm = rng.normal(size=(p, r))
    Jc = Gm @ Gm.T                                         # singular, rank r
    K = rng.normal(size=(r, r)); K = K @ K.T; K = K / (np.linalg.eigvalsh(K).max() * rng.uniform(1.0, 3.0))
    Js = Gm @ K @ Gm.T                                     # 0 <= Js <= Jc, same range
    A = Js @ np.linalg.pinv(Jc)
    worst_a = max(worst_a, np.abs(A @ Jc - Js).max())
    extra = Js - A @ Jc @ A.T; worst_psd = min(worst_psd, np.linalg.eigvalsh(0.5 * (extra + extra.T)).min())
    Sg = rand_pd(p)                                        # moments of (T, A c + extra noise) vs (T, Js T + nu_S)
    cross = A @ Jc @ Sg; var = A @ (Jc @ Sg @ Jc + Jc) @ A.T + extra
    worst_mom = max(worst_mom, np.abs(cross - Js @ Sg).max(), np.abs(var - (Js @ Sg @ Js + Js)).max())
check("N3 degradedness with singular J_C", worst_a < 1e-8 and worst_psd > -1e-9 and worst_mom < 1e-8,
      f"max|A J_C - J_S| {worst_a:.1e}; min eig of J_S - A J_C A' {worst_psd:+.1e}; moment mismatch {worst_mom:.1e}")

# N4
err = 0.0
for _ in range(300):
    p = rng.integers(2, 6); Sg = rand_pd(p); Jc = rand_pd(p, rng.integers(1, p + 1)); Js = Jc + rand_pd(p, rng.integers(1, p + 1))
    StC = np.linalg.inv(np.linalg.inv(Sg) + Jc)
    err = max(err, np.abs(np.linalg.inv(np.linalg.inv(StC) + Js - Jc) - np.linalg.inv(np.linalg.inv(Sg) + Js)).max())
check("N4 reduction identity", err < 1e-8, f"max abs error {err:.2e}")

# N5
err = 0.0
for _ in range(300):
    p = rng.integers(2, 6); r = rng.integers(1, 6); H = rng.normal(size=(r, p))
    if rng.uniform() < 0.5: H[-1] = H[0]                  # rank-deficient
    SU = np.diag(rng.uniform(0.2, 2.0, r)); X = rand_pd(p); J = H.T @ np.linalg.inv(SU) @ H
    l, rr = np.linalg.slogdet(H @ X @ H.T + SU)[1], np.linalg.slogdet(SU)[1] + np.linalg.slogdet(np.eye(p) + J @ X)[1]
    err = max(err, abs(l - rr))
check("N5 determinant identity", err < 1e-9, f"max |log det difference| {err:.2e}")

# N6
err = 0.0
for _ in range(300):
    p = rng.integers(2, 6); Sg = rand_pd(p); a = rng.normal(size=p); s2 = rng.uniform(0.1, 2.0)
    Hc = rng.normal(size=(rng.integers(1, 4), p)); SNc = np.diag(rng.uniform(0.2, 1.5, len(Hc)))
    G = np.vstack([a, Hc]); Cobs = G @ Sg @ G.T + np.diag(np.r_[s2, np.diag(SNc)])
    post = Sg - Sg @ G.T @ np.linalg.inv(Cobs) @ G @ Sg
    StC = np.linalg.inv(np.linalg.inv(Sg) + Hc.T @ np.linalg.inv(SNc) @ Hc)
    err = max(err, np.abs(post - np.linalg.inv(np.linalg.inv(StC) + np.outer(a, a) / s2)).max())
check("N6 rank-one carry-over", err < 1e-9, f"max abs error {err:.2e}")

# N7
def Hm(p): p = p[p > 0]; return float(-(p * np.log2(p)).sum())
err = 0.0
for _ in range(300):
    nx, nc, ne, nv = rng.integers(2, 5, 4); nv0 = rng.integers(1, nv + 1)
    pxce = rng.dirichlet(np.ones(nx * nc * ne)).reshape(nx, nc, ne)
    pvx = rng.dirichlet(np.ones(nv), size=nx)              # p(v | x)
    f = rng.integers(0, nv0, nv)                           # v0 = f(v)
    P = np.einsum('xce,xv->xcev', pxce, pvx)               # joint p(x, c, e, v), with V - X - (C, E)
    P0 = np.zeros((nx, nc, ne, nv0))
    for v in range(nv): P0[..., f[v]] += P[..., v]
    def H_(*keep, J=P):                                    # entropy of the marginal on axes 'keep'
        drop = tuple(i for i in range(J.ndim) if i not in keep); return Hm(J.sum(axis=drop).ravel())
    X, C, E, Vv = 0, 1, 2, 3
    HXgE = H_(X, E) - H_(E); HXgVC = H_(X, C, Vv) - H_(C, Vv)
    IXCgV0 = H_(X, Vv, J=P0) + H_(C, Vv, J=P0) - H_(X, C, Vv, J=P0) - H_(Vv, J=P0)
    IXEgV0 = H_(X, Vv, J=P0) + H_(E, Vv, J=P0) - H_(X, E, Vv, J=P0) - H_(Vv, J=P0)
    IXVgC = H_(X, C) + H_(C, Vv) - H_(X, C, Vv) - H_(C)
    IV0C = H_(Vv, J=P0) + H_(C, J=P0) - H_(C, Vv, J=P0); IV0E = H_(Vv, J=P0) + H_(E, J=P0) - H_(E, Vv, J=P0)
    err = max(err, abs((HXgE - HXgVC - IXCgV0 + IXEgV0) - (IXVgC + IV0C - IV0E)))
check("N7 finite-alphabet leakage identity", err < 1e-10, f"max abs error {err:.2e} bits over 300 random pmfs")
print(f"FAILS: {fails}")
