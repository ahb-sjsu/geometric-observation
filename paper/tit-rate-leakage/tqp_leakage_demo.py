"""Operational demo with practical scalar codebooks (turboquant-pro tables), 2026-10-01.

Source (the paper's coupled instance): T = (Y1, Y2, V) Gaussian, Sigma_Y = diag(1, 0.4), Var V = 1,
Cov(Y, V) = 0.6 u with u at 50 degrees; holder S = V + U, Var U = 0.05; decoder distortion E||Y - Yhat||^2.

A one-dimensional practical description: Z = b^T T / sd, quantized by a scalar codebook (cells = midpoints
between centroids, as turboquant-pro does), index M. Decoder reconstructs Yhat = E[Y | M] = c_YZ E[Z | cell].
All costs are exact Gaussian integrals. Revised 2026-10-02 after review: the aware direction is the exact maximizer
of |rho_ZS| subject to the budget (a one-parameter generalized eigenproblem; dense sampling is kept as a cross-check),
and the leakage integral is evaluated by adaptive quadrature with breakpoints at the cell edges (reference) and by
Gauss-Hermite at 80-1280 nodes (convergence table T2). Quoted values use the adaptive reference.
  rate H(M) (the same for every direction b, so comparisons are at matched rate),
  distortion D(b) = tr Sigma_Y - |c_YZ|^2 sum_i p_i m_i^2,
  leakage L(b) = H(M | S) bits (deterministic quantizer, so I(T;M|S) = H(M|S)).
T0  turboquant-pro's shipped Lloyd-Max tables vs exact Lloyd-Max for N(0,1): MSE on N(0,1) and on rotated unit
    vectors at d=128 (Monte Carlo for the latter).
T1  for each codebook and distortion budget D0: leakage of the conventional principal-axis quantizer vs the best
    direction meeting D0 (same codebook, same rate); its Y-plane angle vs the theory's pencil direction; the
    information-theoretic floor L_1d(D0).
T1a H(M|S) is strictly decreasing in |rho_ZS| for every codebook, which justifies maximizing |rho_ZS| in T1.
T2  convergence of the leakage values of T1 in the quadrature order.
"""
import numpy as np, math
from scipy.stats import norm
from scipy.optimize import minimize
LN2 = math.log(2); rng = np.random.default_rng(2026)

# turboquant-pro tables (turboquant_pro/core.py:74-96, identical in pgvector.py:108)
TQP = {2: np.array([-1.510, -0.453, 0.453, 1.510]),
       3: np.array([-1.748, -1.050, -0.500, -0.069, 0.069, 0.500, 1.050, 1.748]),
       4: np.array([-2.401, -1.844, -1.437, -1.099, -0.800, -0.524, -0.262, -0.066,
                    0.066, 0.262, 0.524, 0.800, 1.099, 1.437, 1.844, 2.401])}

def lloyd_max(K, iters=2000):
    c = norm.ppf((np.arange(K) + 0.5) / K)
    for _ in range(iters):
        a = np.concatenate([[-np.inf], (c[:-1] + c[1:]) / 2, [np.inf]])
        p = norm.cdf(a[1:]) - norm.cdf(a[:-1])
        c = (norm.pdf(a[:-1]) - norm.pdf(a[1:])) / p
    return c

def cells(c):
    a = np.concatenate([[-np.inf], (c[:-1] + c[1:]) / 2, [np.inf]])
    p = norm.cdf(a[1:]) - norm.cdf(a[:-1])
    m = (norm.pdf(a[:-1]) - norm.pdf(a[1:])) / p          # exact conditional means E[Z | cell]
    return a, p, m

def mse_reconstruct(c, recon):
    a, p, m = cells(c)
    # E (Z - recon_i)^2 over cells = sum p_i (Var(Z|cell) + (m_i - recon_i)^2); Var(Z|cell) = E[Z^2|cell] - m_i^2
    lo = np.where(np.isfinite(a[:-1]), a[:-1], 0.0); hi = np.where(np.isfinite(a[1:]), a[1:], 0.0)
    ez2 = (lo * norm.pdf(lo) * np.isfinite(a[:-1]) - hi * norm.pdf(hi) * np.isfinite(a[1:])) / p + 1
    return float(np.sum(p * (ez2 - m**2 + (m - recon)**2)))

print("T0  codebook check (N(0,1) MSE)")
for k in (2, 3, 4):
    lm = lloyd_max(2**k)
    print(f"   {k}-bit: tqp table MSE = {mse_reconstruct(TQP[k], TQP[k]):.5f}   exact Lloyd-Max MSE = {mse_reconstruct(lm, lm):.5f}"
          f"   (tqp cells with exact centroids: {mse_reconstruct(TQP[k], cells(TQP[k])[2]):.5f})   Lloyd-Max levels {np.round(lm[len(lm)//2:], 4)}")
# rotated unit vectors at d = 128, coordinates scaled by sqrt(d), as turboquant-pro applies the table
d = 128; X = rng.normal(size=(20000, d)); X /= np.linalg.norm(X, axis=1, keepdims=True); Zc = (X * math.sqrt(d)).ravel()
for k in (2, 3, 4):
    lm = lloyd_max(2**k)
    def emp(c):
        a = (c[:-1] + c[1:]) / 2; idx = np.searchsorted(a, Zc); return float(np.mean((Zc - c[idx])**2))
    print(f"   {k}-bit on rotated unit vectors (d=128): tqp table MSE = {emp(TQP[k]):.5f}   exact Lloyd-Max MSE = {emp(lm):.5f}")

# the coupled instance
SY = np.diag([1.0, 0.4]); u = np.array([math.cos(math.radians(50)), math.sin(math.radians(50))])
Sig = np.zeros((3, 3)); Sig[:2, :2] = SY; Sig[:2, 2] = Sig[2, :2] = 0.6 * u; Sig[2, 2] = 1.0
tau2 = 0.05; F = np.zeros((2, 3)); F[:, :2] = np.eye(2); trSY = np.trace(SY)
hS = np.array([0.0, 0.0, 1.0]); varS = Sig[2, 2] + tau2
from scipy.integrate import quad
from scipy.linalg import eigh
from scipy.special import roots_hermitenorm               # numpy's hermegauss returns nan nodes above ~600
GH = {n: roots_hermitenorm(n) for n in (80, 160, 320, 640, 1280)}   # probabilists' Hermite, weight exp(-x^2/2)

def leak_gh(rho, c, n):
    a, p, m = cells(c); sz = math.sqrt(max(1 - rho**2, 1e-15)); H = 0.0
    for x, w in zip(*GH[n]):
        if w < 1e-300: continue                             # far nodes of high-order rules carry zero weight
        q = np.clip(norm.cdf((a[1:] - rho * x) / sz) - norm.cdf((a[:-1] - rho * x) / sz), 0.0, None); q = q[q > 1e-300]
        H += w * float(-np.sum(q * np.log2(q)))
    return H / math.sqrt(2 * math.pi)

def leak_ref(rho, c):
    """H(M|S) by adaptive quadrature over the standardized S, split at the points where S crosses a cell edge."""
    a, p, m = cells(c); sz = math.sqrt(max(1 - rho**2, 1e-15)); r = abs(rho)
    def f(x):
        q = norm.cdf((a[1:] - rho * x) / sz) - norm.cdf((a[:-1] - rho * x) / sz); q = q[q > 1e-300]
        return float(-np.sum(q * np.log2(q))) * norm.pdf(x)
    edges = sorted(e / rho for e in a[1:-1]) if r > 1e-12 else []
    pts = [-12.0] + [e for e in edges if -12 < e < 12] + [12.0]
    return sum(quad(f, lo, hi, epsabs=1e-13, epsrel=1e-12, limit=500)[0] for lo, hi in zip(pts[:-1], pts[1:]))

def stats(b, c):
    b = b / math.sqrt(b @ Sig @ b)                          # Var Z = 1
    a, p, m = cells(c)
    cYZ = F @ Sig @ b
    D = trSY - (cYZ @ cYZ) * float(np.sum(p * m**2))
    HM = float(-np.sum(p * np.log2(p)))
    covZS = b @ Sig @ hS; rho = covZS / math.sqrt(varS)
    HMS = leak_ref(rho, c)
    ang = math.degrees(math.atan2(cYZ[1], cYZ[0])) % 180
    return D, HM, HMS, ang, rho

# theory: one-dimensional Gaussian-test-channel optimum (pencil) at budget D0
K = np.linalg.inv(np.linalg.inv(Sig) + np.outer(hS, hS) / tau2)
def theory(D0):
    Delta = trSY - D0; A = Sig @ F.T @ F @ Sig - Delta * Sig
    w, U = np.linalg.eigh(K); Kih = U @ np.diag(w ** -0.5) @ U.T
    cw, cV = np.linalg.eigh(Kih @ A @ Kih); b = Kih @ cV[:, -1]
    cYZ = F @ Sig @ b; ang = math.degrees(math.atan2(cYZ[1], cYZ[0])) % 180
    return 0.5 * math.log2(1 + Delta / cw[-1]), ang

def sph(t):  # angles -> unit vector
    return np.array([math.sin(t[0]) * math.cos(t[1]), math.sin(t[0]) * math.sin(t[1]), math.cos(t[0])])

def leak_of_rho(rho, c):
    return leak_ref(rho, c)

AS = np.outer(Sig @ hS, Sig @ hS) / varS                     # b'AS b / b'Sig b = rho_ZS^2
BY = Sig @ F.T @ F @ Sig                                     # b'BY b / b'Sig b = |c_YZ|^2
def rq(M, b): return float(b @ M @ b) / float(b @ Sig @ b)
def top(M): w, V = eigh(0.5 * (M + M.T), Sig); return V[:, -1]
def exact_aware(need):
    """Maximize rho^2 = b'AS b/b'Sig b subject to |c_YZ|^2 = b'BY b/b'Sig b >= need (one-parameter eigenproblem)."""
    b0 = top(AS)
    if rq(BY, b0) >= need: return b0
    lo, hi = 0.0, 1.0
    while rq(BY, top(AS + hi * BY)) < need: hi *= 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if rq(BY, top(AS + mid * BY)) < need: lo = mid
        else: hi = mid
    return top(AS + hi * BY)

mono = True
for k in (2, 3, 4):
    for cb in (TQP[k], lloyd_max(2**k)):
        Ls = [leak_of_rho(r, cb) for r in np.linspace(0, 0.995, 200)]
        mono = mono and all(Ls[i + 1] < Ls[i] + 1e-12 for i in range(len(Ls) - 1))
print(f"\nT1a leakage H(M|S) strictly decreasing in |rho_ZS| for every codebook (200 points each): {'PASS' if mono else 'FAIL'}")

print("\nT1  matched-rate comparison on the coupled instance (exact costs; exact aware direction, sampling as cross-check)")
bR = np.array([1.0, 0, 0])                                  # principal axis of Sigma_Y (rate-optimal read)
CASES = []
for label, books in (("tqp table", TQP), ("exact Lloyd-Max", {k: lloyd_max(2**k) for k in (2, 3, 4)})):
    print(f"  codebooks: {label}")
    for k in (2, 3, 4):
        c = books[k]
        DR, HM, LR, angR, rhoR = stats(bR, c)
        print(f"   {k}-bit: rate H(M) = {HM:.4f} bits; principal-axis quantizer D = {DR:.4f}, leakage = {LR:.4f} bits")
        for frac in (0.15, 0.4, 0.7):
            D0 = DR + frac * (trSY - DR)
            # Exact reduction: at fixed rate, D(b) <= D0 iff |c_YZ|^2 >= (trSY - D0)/(1 - D_q), the same set for every
            # codebook, and the leakage depends on b only through rho_ZS. Maximize |rho_ZS| over feasible directions by
            # dense sampling (2e6 directions), then evaluate the exact leakage there.
            _, p_, m_ = cells(c); gain = float(np.sum(p_ * m_**2))
            need = (trSY - D0) / gain
            Bdir = rng.normal(size=(2000000, 3))                       # cross-check only
            sd = np.sqrt(np.einsum('ij,jk,ik->i', Bdir, Sig, Bdir))
            cYZ = (Bdir @ Sig @ F.T) / sd[:, None]
            rho = (Bdir @ Sig @ hS) / sd / math.sqrt(varS)
            feas = np.einsum('ij,ij->i', cYZ, cYZ) >= need
            rho_samp = float(np.max(np.where(feas, np.abs(rho), -1)))
            bvec = exact_aware(need)
            Db, _, Lb, angb, rhob = stats(bvec, c)
            Lth, angth = theory(D0)
            CASES.append((label, k, frac, rhoR, rhob, c))
            print(f"      f={frac:.2f} D0={D0:.4f}: aware leakage {Lb:.4f} vs principal {LR:.4f} "
                  f"({100*(LR-Lb)/LR:.1f}% less) | angle {angb:6.2f} deg (pencil {angth:6.2f}) | floor L_1d(D0) = {Lth:.4f}"
                  f" | |rho| exact {abs(rhob):.6f}, sampled {rho_samp:.6f}, D(b) {Db:.4f}")

print()
print("T2  quadrature convergence of the leakage values (Lloyd-Max codebooks; principal and aware)")
print("    k    f   code       GH80      GH160     GH320     GH640     GH1280    adaptive")
for label, k, frac, rhoR, rhob, c in CASES:
    if label != "exact Lloyd-Max": continue
    for nm, r in (("princ", rhoR), ("aware", rhob)):
        vals = [leak_gh(r, c, n) for n in (80, 160, 320, 640, 1280)]
        print(f"    {k}  {frac:.2f} {nm}  " + "  ".join(f"{v:.6f}" for v in vals) + f"  {leak_ref(r, c):.6f}")
