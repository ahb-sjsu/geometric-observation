"""Core routines for "Rate, Leakage, and Distortion for Stationary Gaussian Sources".

Everything is in the whitened coordinate X of the companion paper [1, Sec. IV]:
a block b has data (Qt_b, Ht_b, SU_b) with Qt = Sigma^{1/2} Q Sigma^{1/2},
Ht = H Sigma^{1/2}, and costs (bits)

    r(X)   = -1/2 log2 det X
    I(X)   =  1/2 log2 det(Ht Ht^* + SU) - 1/2 log2 det(Ht X Ht^* + SU)
    l(X)   = r(X) - I(X)                       (leakage)
    d(X)   = tr(Qt X)                          (distortion)

over Hermitian 0 < X <= I.  A problem is a list of blocks with weights c_b:
minimise sum_b c_b [alpha r + (1-alpha) l](X_b) subject to sum_b c_b d(X_b) <= D.
The solver is the water-filling iteration of [1, Prop. 11] applied to the
penalised problem at a fixed level nu, with an outer bisection on nu.  It uses
no structure of the blocks, so the same code solves a full real pn-dimensional
window problem (one block) and the per-frequency Hermitian problems.

No convex-optimisation package is needed: numpy only.
"""
import numpy as np

LOG2 = np.log(2.0)


# ---------------------------------------------------------------- linear algebra
def herm(A):
    return (A + A.conj().T) / 2


def psd_sqrt(A):
    w, V = np.linalg.eigh(herm(A))
    return (V * np.sqrt(np.clip(w, 0, None))) @ V.conj().T


def logdet2(A):
    """log2 det of a Hermitian positive definite matrix."""
    s, ld = np.linalg.slogdet(herm(A))
    return float(ld) / LOG2


def Phi(A):
    """Reverse water-filling at level one on the spectrum of Hermitian A >= 0."""
    w, V = np.linalg.eigh(herm(A))
    x = np.where(w > 1.0, 1.0 / np.maximum(w, 1e-300), 1.0)
    return herm((V * x) @ V.conj().T)


# ---------------------------------------------------------------- costs
def rate(X):
    return -0.5 * logdet2(X)


def info_S(X, Ht, SU):
    return 0.5 * logdet2(Ht @ Ht.conj().T + SU) - 0.5 * logdet2(Ht @ X @ Ht.conj().T + SU)


def leak(X, Ht, SU):
    return rate(X) - info_S(X, Ht, SU)


def dist(X, Qt):
    return float(np.real(np.trace(Qt @ X)))


def tilt(X, Ht, SU, alpha):
    M = Ht @ X @ Ht.conj().T + SU
    return (1 - alpha) * herm(Ht.conj().T @ np.linalg.solve(M, Ht))


# ---------------------------------------------------------------- solver
def penalised_block(Qt, Ht, SU, alpha, nu, X0=None, tol=1e-13, itmax=2000):
    """Fixed point X = Phi(2 nu Qt + tilt(X)): the minimiser of
    alpha r + (1-alpha) l + (nu / ln 2) tr(Qt X) over 0 < X <= I  [1, Thm. 7]."""
    p = Qt.shape[0]
    X = np.eye(p, dtype=complex if np.iscomplexobj(Qt) or np.iscomplexobj(Ht) else float) if X0 is None else X0
    for _ in range(itmax):
        Xn = Phi(2 * nu * Qt + tilt(X, Ht, SU, alpha))
        if np.linalg.norm(Xn - X) < tol:
            X = Xn
            break
        X = Xn
    return X


def solve(blocks, weights, alpha, D, tol=1e-12, warm=None):
    """blocks: list of (Qt, Ht, SU); weights: c_b.  Returns dict with the common
    level nu, the per-block X, and the per-block rate / leakage / distortion."""
    weights = np.asarray(weights, float)
    Xs = [None] * len(blocks) if warm is None else list(warm)

    def total(nu):
        nonlocal Xs
        Xs = [penalised_block(Q, H, S, alpha, nu, X0=Xs[i]) for i, (Q, H, S) in enumerate(blocks)]
        return float(sum(c * dist(X, Q) for c, X, (Q, _, _) in zip(weights, Xs, blocks)))

    dmax = float(sum(c * np.real(np.trace(Q)) for c, (Q, _, _) in zip(weights, blocks)))
    if D >= dmax:
        Xs = [np.eye(Q.shape[0], dtype=Q.dtype) for (Q, _, _) in blocks]
        nu = 0.0
    else:
        lo, hi = 0.0, 1.0
        while total(hi) > D:
            lo, hi = hi, hi * 2
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if total(mid) > D:
                lo = mid
            else:
                hi = mid
            if hi - lo < tol * max(1.0, hi):
                break
        nu = hi
        total(nu)
    R = np.array([rate(X) for X in Xs])
    L = np.array([leak(X, H, S) for X, (_, H, S) in zip(Xs, blocks)])
    Dv = np.array([dist(X, Q) for X, (Q, _, _) in zip(Xs, blocks)])
    return dict(nu=nu, X=Xs, R=float(weights @ R), L=float(weights @ L), D=float(weights @ Dv),
                Rb=R, Lb=L, Db=Dv, cost=float(alpha * (weights @ R) + (1 - alpha) * (weights @ L)))


# ---------------------------------------------------------------- spectra
class Spectrum:
    """A real stationary vector source with spectral density matrix
    Sigma(w) = G(w) G(w)^* + B, G(w) = sum_k G_k e^{-iwk} (real taps), B > 0;
    holder S = h * T + U with real filter taps H_k and white noise SU > 0."""

    def __init__(self, G, B, Hk, SU, Q):
        self.G = [np.asarray(g, float) for g in G]
        self.B = np.asarray(B, float)
        self.Hk = [np.asarray(h, float) for h in Hk]
        self.SU = np.asarray(SU, float)
        self.Q = np.asarray(Q, float)
        self.p = self.B.shape[0]

    def Gw(self, w):
        return sum(g * np.exp(-1j * w * k) for k, g in enumerate(self.G))

    def Sigma(self, w):
        g = self.Gw(w)
        return herm(g @ g.conj().T + self.B)

    def H(self, w, delay=0):
        return np.exp(-1j * w * delay) * sum(h * np.exp(-1j * w * k) for k, h in enumerate(self.Hk))

    def block(self, w, delay=0):
        """Whitened per-frequency data (Qt(w), Ht(w), SU)."""
        R = psd_sqrt(self.Sigma(w))
        return herm(R @ self.Q @ R), self.H(w, delay) @ R, self.SU.astype(complex)

    def blocks(self, n, delay=0):
        return [self.block(2 * np.pi * k / n, delay) for k in range(n)]

    def autocov(self, tau):
        """E[T_{t+tau} T_t^T], exact for the moving-average form."""
        out = self.B.copy() if tau == 0 else np.zeros_like(self.B)
        K = len(self.G)
        for k in range(K):
            j = k - tau
            if 0 <= j < K:
                out = out + self.G[k] @ self.G[j].T
        return out


def circulant_problem(sp, n, delay=0):
    """The full real pn-dimensional n-periodic problem as ONE block.
    Returns (Qt, Ht, SU_n) with the per-symbol normalisation left to the weight 1/n."""
    p = sp.p
    r = sp.Hk[0].shape[0]
    w = 2 * np.pi * np.arange(n) / n
    Sig = np.zeros((n * p, n * p))
    Hn = np.zeros((n * r, n * p))
    Sw = [sp.Sigma(x) for x in w]
    Hw = [sp.H(x, delay) for x in w]
    for a in range(n):
        for b in range(n):
            ph = np.exp(1j * w * (a - b))
            Sig[a * p:(a + 1) * p, b * p:(b + 1) * p] = np.real(sum(f * S for f, S in zip(ph, Sw))) / n
            Hn[a * r:(a + 1) * r, b * p:(b + 1) * p] = np.real(sum(f * H for f, H in zip(ph, Hw))) / n
    Rt = np.real(psd_sqrt(Sig))
    Qn = np.kron(np.eye(n), sp.Q)
    return herm(Rt @ Qn @ Rt), Hn @ Rt, np.kron(np.eye(n), sp.SU), Sig


def toeplitz_problem(sp, n):
    """The window problem of the stationary source itself (block-Toeplitz covariance).
    Requires a memoryless holder map (one tap)."""
    assert len(sp.Hk) == 1
    p = sp.p
    Sig = np.zeros((n * p, n * p))
    for a in range(n):
        for b in range(n):
            Sig[a * p:(a + 1) * p, b * p:(b + 1) * p] = sp.autocov(a - b)
    Rt = np.real(psd_sqrt(Sig))
    Qn = np.kron(np.eye(n), sp.Q)
    Hn = np.kron(np.eye(n), sp.Hk[0])
    return herm(Rt @ Qn @ Rt), Hn @ Rt, np.kron(np.eye(n), sp.SU), Sig


def spectral_solve(sp, n, alpha, D, delay=0, half=False):
    """Per-frequency Hermitian programs with one common level, n grid points.
    half=True uses X(-w) = conj X(w): only 0 <= k <= n/2 is solved, with the
    weights doubled for the paired frequencies (n even).  The costs are the same."""
    if not half:
        return solve(sp.blocks(n, delay), np.full(n, 1.0 / n), alpha, D)
    assert n % 2 == 0
    ks = np.arange(n // 2 + 1)
    wts = np.full(len(ks), 2.0 / n)
    wts[0] = wts[-1] = 1.0 / n
    return solve([sp.block(2 * np.pi * k / n, delay) for k in ks], wts, alpha, D)


def assemble_circulant(sp, n, Xs):
    """Real pn x pn matrix U diag(X_k) U^* from per-frequency solutions."""
    p = sp.p
    w = 2 * np.pi * np.arange(n) / n
    X = np.zeros((n * p, n * p), dtype=complex)
    for a in range(n):
        for b in range(n):
            ph = np.exp(1j * w * (a - b))
            X[a * p:(a + 1) * p, b * p:(b + 1) * p] = sum(f * x for f, x in zip(ph, Xs)) / n
    return X


# ---------------------------------------------------------------- scalar closed form [1, Cor. 17]
def gstar(rho2, s, delta):
    """Larger root of delta s g^2 - (delta + s - rho2) g + (1 - rho2), 0 < delta < 1."""
    b = delta + s - rho2
    return (b + np.sqrt(b * b - 4 * delta * s * (1 - rho2))) / (2 * delta * s)


def ell_scalar(rho2, s, delta):
    """Minimum leakage (bits) of the scalar pair at normalised distortion delta."""
    delta = np.asarray(delta, float)
    return np.where(delta < 1, 0.5 * np.log2(gstar(rho2, s, np.minimum(delta, 1 - 1e-300))), 0.0)


def ell_slope(rho2, s, delta):
    """d ell / d delta in bits  [1, Lemma 26]."""
    g = gstar(rho2, s, delta)
    Dd = np.sqrt((delta + s - rho2) ** 2 - 4 * delta * s * (1 - rho2))
    return -(g * s - 1) / (2 * LOG2 * Dd)
