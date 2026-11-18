"""Audit VI-24, Theorem 7 (From test channels to codes) of T1 note v4.

Independent checks of the three properties the proof claims for the surrogate
distortion d_k(t, xh) = E[ l_C(T, xh) | T_k = t], with part1's saturating dyadic
quantizer q_k (App. A: bounded cells [j 2^-k, (j+1) 2^-k), -4^k <= j < 4^k, left
endpoints, lower tail merged with the first bounded cell, upper tail -> 2^k).

 (Q) the partitions are nested; q_k(Y) -> Y in L^2 for Y Gaussian.
 (1) d_k is finite (bounded) on the finite alphabets, for each k.
 (2) a deterministic code that acts on T_k^n has consumer loss = surrogate distortion
     (exact surrogate vs Monte Carlo true loss).
 (3) the surrogate distortion of the channel, E d_k(T_k, That_k) under the true joint
     law of (T_k, That_k), converges to E l_C(T, That); it is NOT E l_C(T, That_k).
 (P) for the Gaussian test channel, I(T;That) = r(Delta) and I(T;That|S) = l(Delta)
     (the identification used in Cor. 8(b)), incl. singular Cov V.

Exact one-dimensional quadrature (Gauss-Legendre per quantizer cell); no Monte Carlo
except in (2). Does not import the author's verify script.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from numpy.polynomial.hermite_e import hermegauss
from scipy.special import ndtr

rng = np.random.default_rng(20261118)


def quantizer(k):
    h = 2.0 ** -k
    inner = np.arange(-4 ** k + 1, 4 ** k + 1) * h          # edges j h, j=-4^k+1..4^k
    edges = np.concatenate(([-np.inf], inner, [np.inf]))
    vals = np.concatenate(([-2.0 ** k], np.arange(-4 ** k + 1, 4 ** k) * h, [2.0 ** k]))
    assert len(vals) == len(edges) - 1 == 2 * 4 ** k + 1
    return edges, vals


def q(k, y):
    edges, vals = quantizer(k)
    return vals[np.searchsorted(edges, y, side="right") - 1]


# ---------------------------------------------------------------- consumers (weighted maps g)
CONS = {
    "x+0.2sin x": lambda x: np.stack([x + 0.2 * np.sin(x)], -1),
    "circle (cos,sin)": lambda x: np.stack([np.cos(x), np.sin(x)], -1),
    "(tanh 2x, 0.3x)": lambda x: np.stack([np.tanh(2 * x), 0.3 * x], -1),
    "|x| (Lipschitz, not C1)": lambda x: np.stack([np.abs(x)], -1),
}

out = []
P = out.append
P("=== (Q) nestedness of the dyadic partitions and L2 convergence of q_k ===")
for k in range(1, 7):
    e1, _ = quantizer(k)
    e2, _ = quantizer(k + 1)
    fin1 = e1[np.isfinite(e1)]
    fin2 = set(np.round(e2[np.isfinite(e2)] * 2 ** (k + 1)).astype(np.int64).tolist())
    nested = all(int(round(v * 2 ** (k + 1))) in fin2 for v in fin1)
    P(f"k={k}: level-k edges subset of level-(k+1) edges: {nested}")
ys = rng.normal(0, 2.0, 2_000_000)
for k in range(1, 7):
    P(f"k={k}: E|q_k(Y)-Y|^2 for Y~N(0,4) (MC 2e6) = {np.mean((q(k, ys) - ys) ** 2):.3e}")


def cell_nodes(k, sd, nper=24, ntail=400):
    """Gauss-Legendre nodes/weights (times the N(0,sd^2) density) per cell."""
    edges, vals = quantizer(k)
    lo_cut, hi_cut = -14 * sd, 14 * sd
    xg, wg = leggauss(nper)
    xt, wt = leggauss(ntail)
    T, W, A = [], [], []
    for a in range(len(vals)):
        lo, hi = edges[a], edges[a + 1]
        lo = max(lo, lo_cut) if np.isfinite(lo) else lo_cut
        hi = min(hi, hi_cut) if np.isfinite(hi) else hi_cut
        if hi <= lo:  # cell entirely beyond 14 sd: mass < 1e-40
            continue
        xx, ww = (xt, wt) if (not np.isfinite(edges[a]) or not np.isfinite(edges[a + 1])) else (xg, wg)
        t = 0.5 * (hi - lo) * xx + 0.5 * (hi + lo)
        w = 0.5 * (hi - lo) * ww * np.exp(-t ** 2 / (2 * sd ** 2)) / (sd * np.sqrt(2 * np.pi))
        T.append(t); W.append(w); A.append(np.full(len(t), a))
    return np.concatenate(T), np.concatenate(W), np.concatenate(A), edges, vals


def cond_mean_g_That(g, c, tau, t, nodes=160):
    """E[g(c t + tau V)], V ~ N(0,1), Gauss-Hermite (probabilists')."""
    z, w = hermegauss(nodes)
    w = w / w.sum()
    Y = c * t[:, None] + tau * z[None, :]
    G = g(Y)  # (nt, nz, dout)
    return np.einsum("j,ijd->id", w, G)


def cond_mean_abs(c, tau, t):
    mu = c * t
    return np.stack([tau * np.sqrt(2 / np.pi) * np.exp(-mu ** 2 / (2 * tau ** 2)) + mu * (1 - 2 * ndtr(-mu / tau))], -1)


P("")
P("=== (1)+(3) surrogate distortion of the 1-D Gaussian test channel ===")
P("That = (1-D/s2) T + V, V~N(0, D - D^2/s2).  SD_k = E d_k(T_k, That_k) under the true joint law;")
P("NAIVE_k = E l(T, That_k) (true loss of the quantized channel); TARGET = E l(T, That).")
for name, g in CONS.items():
    for s2, Dl in [(1.0, 0.1), (1.0, 0.5), (4.0, 0.3)]:
        sd = np.sqrt(s2)
        c = 1 - Dl / s2
        tau = np.sqrt(Dl - Dl ** 2 / s2)
        # exact target: E||g(T)||^2 - 2 E<g(T), E[g(That)|T]> + E||g(That)||^2
        tt, ww, _, _, _ = cell_nodes(3, sd)  # just a fine quadrature of the N(0,s2) law
        gT = g(tt)
        if name.startswith("|x|"):
            mT = cond_mean_abs(c, tau, tt)
        else:
            mT = cond_mean_g_That(g, c, tau, tt)
        Eg2 = np.sum(ww * np.sum(gT ** 2, -1))
        z, wz = hermegauss(200); wz = wz / wz.sum()
        sdh = np.sqrt(s2 - Dl)
        # E||g(That)||^2 by the same cellwise quadrature at That's own scale
        th, wh, _, _, _ = cell_nodes(3, sdh)
        EgH2 = np.sum(wh * np.sum(g(th) ** 2, -1))
        cross = np.sum(ww * np.sum(gT * mT, -1))
        target = Eg2 - 2 * cross + EgH2
        line = f"{name:24s} s2={s2:.0f} Delta={Dl:.1f}: TARGET={target:.8f}"
        P(line)
        for k in range(1, 6):
            t, w, a_idx, edges, vals = cell_nodes(k, sd)
            gt = g(t)
            ncell = len(vals)
            pa = np.bincount(a_idx, weights=w, minlength=ncell)
            ma = np.stack([np.bincount(a_idx, weights=w * gt[:, d], minlength=ncell) for d in range(gt.shape[1])], -1)
            ma = np.where(pa[:, None] > 0, ma / np.maximum(pa[:, None], 1e-300), 0)
            g2a = np.bincount(a_idx, weights=w * np.sum(gt ** 2, -1), minlength=ncell)
            g2a = np.where(pa > 0, g2a / np.maximum(pa, 1e-300), 0)
            gv = g(vals)  # g at reproduction letters (ncell, dout)
            # F(t) = E[g(That_k) | T=t] = sum_b g(v_b) P(That in b | T=t)
            F = np.zeros_like(gt)
            for i0 in range(0, len(t), 3000):
                tc = t[i0:i0 + 3000]
                cdf = ndtr((edges[None, :] - c * tc[:, None]) / tau)
                Pb = np.diff(cdf, axis=1)
                F[i0:i0 + 3000] = Pb @ gv
            # marginal of That_k
            pb = np.diff(ndtr(edges / sdh))
            EgHk2 = np.sum(pb * np.sum(gv ** 2, -1))
            SD = Eg2 - 2 * np.sum(w * np.sum(ma[a_idx] * F, -1)) + EgHk2
            NAIVE = Eg2 - 2 * np.sum(w * np.sum(gt * F, -1)) + EgHk2
            # (1): max of d_k over the finite alphabets (cells of positive probability)
            pos = pa > 1e-300
            dmax = np.max(g2a[pos][:, None] - 2 * ma[pos] @ gv.T + np.sum(gv ** 2, -1)[None, :])
            P(f"    k={k}: SD_k={SD:.8f} (SD-TARGET={SD - target:+.2e})  NAIVE_k-SD_k={NAIVE - SD:+.2e}  max d_k={dmax:.3g}  cells={ncell}")

P("")
P("=== (2) consumer loss of a code acting on T_k^n equals its surrogate distortion ===")
k, n = 2, 2
g = CONS["circle (cos,sin)"]
sd = 1.0
t, w, a_idx, edges, vals = cell_nodes(k, sd)
gt = g(t)
ncell = len(vals)
pa = np.bincount(a_idx, weights=w, minlength=ncell)
ma = np.stack([np.bincount(a_idx, weights=w * gt[:, d], minlength=ncell) for d in range(2)], -1) / np.maximum(pa[:, None], 1e-300)
g2a = np.bincount(a_idx, weights=w * np.sum(gt ** 2, -1), minlength=ncell) / np.maximum(pa, 1e-300)


def code(a1, a2):
    """A deterministic 'code' T_k^2 -> (xh1, xh2) in the reproduction alphabet (arbitrary, nonlinear)."""
    s = vals[a1] + 0.5 * vals[a2]
    b = np.clip(np.searchsorted(edges, np.round(s * 3) / 3, side="right") - 1, 0, ncell - 1)
    b2 = np.clip(np.searchsorted(edges, np.abs(vals[a1] - vals[a2]), side="right") - 1, 0, ncell - 1)
    return vals[b], vals[b2]


A1, A2 = np.meshgrid(np.arange(ncell), np.arange(ncell), indexing="ij")
X1, X2 = code(A1, A2)
dk = lambda a, xh: g2a[a] - 2 * np.sum(ma[a] * g(xh), -1) + np.sum(g(xh) ** 2, -1)
SD = np.sum(pa[A1] * pa[A2] * 0.5 * (dk(A1, X1) + dk(A2, X2)))
N = 4_000_000
T1, T2 = rng.normal(0, sd, N), rng.normal(0, sd, N)
a1 = np.searchsorted(edges, T1, side="right") - 1
a2 = np.searchsorted(edges, T2, side="right") - 1
x1, x2 = code(a1, a2)
L = 0.5 * (np.sum((g(T1) - g(x1)) ** 2, -1) + np.sum((g(T2) - g(x2)) ** 2, -1))
P(f"circle consumer, k=2, n=2: surrogate distortion (exact) = {SD:.6f}; true consumer loss (MC 4e6) = {L.mean():.6f} +- {L.std() / np.sqrt(N):.6f}")

P("")
P("=== (P) Gaussian test channel: I(T;That)=r(Delta), I(T;That|S)=l(Delta) ===")


def cond_cov(Cxx, Cxy, Cyy):
    return Cxx - Cxy @ np.linalg.pinv(Cyy, rcond=1e-12) @ Cxy.T


worst = 0.0
for trial in range(200):
    p = int(rng.integers(1, 5))
    r = int(rng.integers(1, 4))
    A = rng.normal(size=(p, p)); Sig = A @ A.T + 0.2 * np.eye(p)
    H = rng.normal(size=(r, p)); B = rng.normal(size=(r, r)); SU = B @ B.T + 0.1 * np.eye(r)
    # Delta <= Sigma; sometimes with an eigen-direction where Delta = Sigma (Cov V singular)
    Ls = np.linalg.cholesky(Sig)
    U, _ = np.linalg.qr(rng.normal(size=(p, p)))
    ev = rng.uniform(0.01, 1.0, p)
    if trial % 3 == 0:
        ev[0] = 1.0
    Dl = Ls @ U @ np.diag(ev) @ U.T @ Ls.T
    Si = np.linalg.inv(Sig)
    Ahat = np.eye(p) - Dl @ Si
    CV = Dl - Dl @ Si @ Dl
    # joint covariance of (T, That, S)
    CTT = Sig; CTH = Sig @ Ahat.T; CHH = Ahat @ Sig @ Ahat.T + CV
    CTS = Sig @ H.T; CHS = Ahat @ Sig @ H.T; CSS = H @ Sig @ H.T + SU
    I_TH = 0.5 * np.log2(np.linalg.det(Sig) / np.linalg.det(cond_cov(CTT, CTH, CHH)))
    CT_S = cond_cov(CTT, CTS, CSS)
    Cy = np.block([[CHH, CHS], [CHS.T, CSS]])
    CT_HS = cond_cov(CTT, np.hstack([CTH, CTS]), Cy)
    I_THgS = 0.5 * np.log2(np.linalg.det(CT_S) / np.linalg.det(CT_HS))
    J = H.T @ np.linalg.inv(SU) @ H
    K = np.linalg.inv(Si + J)
    Se = np.linalg.inv(np.linalg.inv(Dl) + J)
    rD = 0.5 * np.log2(np.linalg.det(Sig) / np.linalg.det(Dl))
    lD = 0.5 * np.log2(np.linalg.det(K) / np.linalg.det(Se))
    worst = max(worst, abs(I_TH - rD), abs(I_THgS - lD))
P(f"200 random (p<=4, r<=3) instances, 1/3 with singular Cov V: max |I - formula| = {worst:.2e} bits")

open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
