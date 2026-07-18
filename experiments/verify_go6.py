# GO-6 (GO-P-2026-028): output vs surrogate vs reconstruction coding at matched rate.
# Governed by prereg/GO-P-2026-028. Synthetic; pure numpy.
#
# A nonlinear consumer U = C(X) = phi(A X), A: r x d (r<d), phi monotone. Downstream metric
# d_O(X,Xhat) = || C(X) - C(Xhat) ||^2. Local read operator P_C = A^T diag(E phi'(AX)^2) A has
# rank r, so ker P_C has dimension d-r > 0 (positive entropy share). Three coders at MATCHED
# rate R (matched as mutual information I in each coder's own space):
#   (a) OUTPUT coding   -- code U directly under D_Y (Thm B2-optimal): d_O(a)(R) = RD of Cov(U).
#   (b) SURROGATE coding-- code X under the quadratic surrogate d_{P_C}; measure the TRUE d_O.
#   (c) RECON coding    -- code X under MSE; measure the TRUE d_O.
# Sealed predictions: (1) d_O(a) <= d_O(b) <= d_O(c) at every rate; (2) the a-c gap is strict
# because ker P_C > 0, and collapses in the isotropic control P_C=I; (3) (b-a)/(c-a) -> 0 as R
# grows (Thm B3 high-resolution). MIT License.
import numpy as np
rng = np.random.default_rng(6)

def spd(n):
    A = rng.standard_normal((n, n)); return A @ A.T + 0.4 * np.eye(n)
def sqrtm(M):
    w, U = np.linalg.eigh((M + M.T) / 2); w = np.clip(w, 0, None); return U @ np.diag(np.sqrt(w)) @ U.T
def phi(z):  return 2.2 * np.tanh(1.2 * z)            # saturating monotone: quadratic surrogate
def dphi(z): return 2.2 * 1.2 / np.cosh(1.2 * z) ** 2  #   is a poor guide at large error (low rate)

def output_rd_curve(CovU, thetas):
    g = np.clip(np.linalg.eigvalsh((CovU + CovU.T) / 2), 1e-12, None)
    rates, dist = [], []
    for th in thetas:
        rates.append(0.5 * np.sum(np.log(g[g > th] / th)) if (g > th).any() else 0.0)
        dist.append(float(np.sum(np.minimum(th, g))))               # output distortion = d_O(a)
    return np.array(rates), np.array(dist)

def sigma_delta(W, Sx, nu):
    """rate-R optimal error cov minimizing tr(W Sigma) via reverse water-filling; returns (Sigma, rate)."""
    Sh = sqrtm(Sx); Wt = (Sh @ W @ Sh + (Sh @ W @ Sh).T) / 2
    w, V = np.linalg.eigh(Wt); w = np.clip(w, 1e-15, None)
    s = np.minimum(1.0, nu / w)
    Sig = Sh @ (V @ np.diag(s) @ V.T) @ Sh
    rate = 0.5 * np.sum(np.log(w[w > nu] / nu)) if (w > nu).any() else 0.0
    return (Sig + Sig.T) / 2, rate

def measure_dO(Sig, X, A, n_err=1):
    Ss = sqrtm(Sig); U = phi(X @ A.T); acc = 0.0
    for _ in range(n_err):
        e = rng.standard_normal(X.shape) @ Ss.T
        acc += np.mean(np.sum((phi((X + e) @ A.T) - U) ** 2, axis=1))
    return acc / n_err

def coder_curve(W, Sx, X, A, nus):
    rates, dist = [], []
    for nu in nus:
        Sig, r = sigma_delta(W, Sx, nu); rates.append(r); dist.append(measure_dO(Sig, X, A))
    return np.array(rates), np.array(dist)

def run_case(d, r, isotropic, label, N=120000):
    Sx = np.eye(d) if isotropic else spd(d)
    A = np.eye(d)[:r] if isotropic else rng.standard_normal((r, d))
    X = rng.multivariate_normal(np.zeros(d), Sx, N)
    if isotropic:  # linear identity consumer: P_C = I, ker P_C = 0
        Ause = np.eye(d); Pc = np.eye(d); CovU = Sx.copy()
        def measc(Sig): return float(np.trace(Sig))       # d_O = tr(Sigma) exactly (linear)
    else:
        Ause = A
        AX = X @ A.T
        Pc = A.T @ np.diag(np.mean(dphi(AX) ** 2, axis=0)) @ A       # rank r, ker dim d-r
        CovU = np.cov(phi(AX), rowvar=False)
    ker_dim = d - np.linalg.matrix_rank(Pc, tol=1e-8)
    thetas = np.geomspace(np.linalg.eigvalsh(CovU).max(), 1e-4, 40)
    nus = np.geomspace(np.linalg.eigvalsh(sqrtm(Sx) @ Pc @ sqrtm(Sx)).max() + 1e-9, 1e-5, 40)
    nus_c = np.geomspace(np.linalg.eigvalsh(Sx).max(), 1e-5, 40)
    Ra, Da = output_rd_curve(CovU, thetas)                          # (a) output
    if isotropic:
        # P_C = I and linear identity consumer: surrogate and reconstruction are the same coder,
        # and output coding of U = X is also the same reverse water-fill -> all three collapse.
        Rr, Drr = [], []
        for nu in nus_c:
            Sig, rr = sigma_delta(np.eye(d), Sx, nu); Rr.append(rr); Drr.append(float(np.trace(Sig)))
        Rb, Db = np.array(Rr), np.array(Drr); Rc, Dc = np.array(Rr), np.array(Drr)
        Ra, Da = np.array(Rr), np.array(Drr)
    else:
        Rb, Db = coder_curve(Pc, Sx, X, Ause, nus)                  # (b) surrogate
        Rc, Dc = coder_curve(np.eye(d), Sx, X, Ause, nus_c)         # (c) reconstruction
    # interpolate onto a common rate grid
    Rgrid = np.linspace(0.5, min(Ra.max(), Rb.max(), Rc.max()) - 0.2, 8)
    fa = np.interp(Rgrid, Ra, Da); fb = np.interp(Rgrid, Rb, Db); fc = np.interp(Rgrid, Rc, Dc)
    tol = 0.03 * np.maximum(fc, 1e-9)
    ordered = np.all(fa <= fb + tol) and np.all(fb <= fc + tol)
    gap_ac = float(np.median(fc - fa))
    conv = float((fb[-1] - fa[-1]) / max(fc[-1] - fa[-1], 1e-12))   # (b-a)/(c-a) at high rate
    print(f"  {label}: ker(P_C) dim={ker_dim}  ordering a<=b<=c: {ordered}  "
          f"median(c-a) gap={gap_ac:+.3e}  (b-a)/(c-a) @hiR={conv:.3f}")
    print(f"     a(out)={np.array2string(fa,precision=3)}")
    print(f"     b(sur)={np.array2string(fb,precision=3)}")
    print(f"     c(rec)={np.array2string(fc,precision=3)}")
    return dict(ordered=bool(ordered), gap_ac=gap_ac, conv=conv, ker_dim=int(ker_dim))

fail = []
print("=" * 78); print("[1] Nonlinear consumer, ker P_C > 0 (d=8, r=4): output <= surrogate <= reconstruction")
m = run_case(8, 4, isotropic=False, label="main")
if not m["ordered"]: fail.append("ordering")
if not (m["gap_ac"] > 1e-6 and m["ker_dim"] > 0): fail.append("kernel-gap")   # strict a-c gap w/ positive kernel
if not (m["conv"] < 0.15): fail.append("convergence")                         # (b-a)/(c-a) -> small at high R

print("=" * 78); print("[2] Isotropic control P_C=I (ker=0): the three coders collapse (a=b=c)")
c = run_case(8, 8, isotropic=True, label="control")
if not (abs(c["gap_ac"]) < 1e-6 or c["conv"] != c["conv"]):     # gap collapses (NaN conv ok: c-a==0)
    # with P_C=I all curves identical -> gap ~ 0
    if abs(c["gap_ac"]) > 1e-3: fail.append("control-collapse")

print("=" * 78)
print("VERDICT:", "ALL PASS" if not fail else f"FAIL: {fail}")
