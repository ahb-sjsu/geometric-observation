#!/usr/bin/env python
"""GO-14 process-limit harness (numerics for Conjecture v0.2, the
process-limit face of the causal-erasure coordinate; prereg 078
pending -- nothing sealed here, this harness nets the faces).

s1 evaluator cross-check: the fast interleaved-Cholesky L_a evaluator
   (route B, R-IND-5 lineage) vs the sealed 076 harness terms()
   (route A, copied verbatim from experiments/go14_causal_erasure.py)
   at the sealed anchors (block_16 = 0.5349675, diag UB(0) =
   0.5722547) + 2 random records; chain-rule identity residual
   < 1e-9 at every tested U-INDEPENDENT record;
s2 U-scoping faces (Hypothesis 1 of the tex is load-bearing):
   (a) random U-coupled records break the chain rule (|resid| > 0.01);
   (b) Delta-lag-causal U-coupling extends the identity exactly
       (resid < 1e-9);
   (c) the trivial Delta-causal U-record Yh_t = 0.54 Y_t + 0.23 S_t
       + N(0, 0.1625) is D-feasible (per-cell noise shave if the
       literal 0.1625 overshoots D by rounding -- disclosed in vals)
       and achieves L_a(0) < 0.55, beating the family min;
s3 family anchor: full-space min L_a(0) at n=16 from 2 warm starts
   reproduces <= 0.5668 and beats the 076-recorded 0.567353;
s4 mechanism: at the s3 winner Ay is transpose-symmetric (rel
   residual < 1e-3); the Av interior-row kernel changes sign exactly
   at lag Delta for Delta in {0,1,2} (Delta=1,2 winners recomputed
   warm-started from the Delta=0 winner);
s5 diag ladder + rate: La(n, Delta) at {24,32,48}x{4,5,6} reproduces
   the R-IND-5-confirmed raw values to 1e-6; per-lag extrapolated
   excess ratios (two-point 32/48) rise monotonically and stay
   < lambda_s^-2 + 0.15;
s6 reference construction: the causal-spectral allocation at
   Delta=0/1/2 reproduces {0.547945, 0.532344, 0.530253} to 1e-4;
   full-space plateau gaps (n=16/24 two-point limits minus the
   allocation) exceed 3x the block-face-calibrated two-point error.
Sentinel ===GO14PL-JSON=== with ===END===; flag GO14PL_supported.
Pilot seed 20261110 / governed seed 20261111. SEED STAMPS ONLY: the
seed is recorded in the output and feeds NO computation -- the fixed
record draws use an internally pinned generator (20260805) so pilot
and governed verify identical numbers; all optimizers are
deterministic warm-started (the 070 lesson)."""
import argparse
import json
import sys
import time

import numpy as np
from scipy.optimize import minimize

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261110 if a_.pilot
                                            else 20261111)
rngi = np.random.default_rng(20260805)   # pinned: draws identical
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
LN2 = np.log(2.0)
D_TGT = 0.3
NF = 1e-8            # noise parameterization floor (R-IND-5 lineage)
ZFLOOR = 1e-7        # 076 harness floor (route-A record vectors)

# sealed / verifier-confirmed reference values (bars, never recomputed
# from these -- every gated quantity below is recomputed from scratch)
BLOCK16_SEALED = 0.5349675144698425      # 076 seal (s3 block16)
DIAG0_SEALED = 0.5722546593              # 076 seal (diag UB(0))
FS16_BEAT = 0.567353                     # 076-recorded non-diag beat
HARD_LA = {(24, 4): 0.5333164330178152, (24, 5): 0.5332971559430583,
           (24, 6): 0.5332947270100958, (32, 4): 0.5324812757915258,
           (32, 5): 0.5324610143191735, (32, 6): 0.5324584245311400,
           (48, 4): 0.5316462526061340, (48, 5): 0.5316250208213668,
           (48, 6): 0.5316222729803203}  # R-IND-5 diag ladder (raw)
HARD_CAND = {0: 0.547945, 1: 0.532344, 2: 0.530253}  # causal-spectral
BLOCKINF_REF = 0.529950                  # erratum-corrected value


# ===================== route A: 076 harness, verbatim ====================
def ld(M):
    n = M.shape[0]
    j = 1e-11 * max(1.0, float(np.trace(M)) / n)
    return float(np.linalg.slogdet(M + j * np.eye(n))[1])


def cmi_bits(S, ia, ib, ic):
    ii = list(ia) + list(ib)
    if len(ic) > 0:
        S22 = S[np.ix_(ic, ic)]
        S12 = S[np.ix_(ii, ic)]
        Sc = S[np.ix_(ii, ii)] - S12 @ np.linalg.solve(
            S22 + 1e-12 * np.eye(len(ic)), S12.T)
    else:
        Sc = S[np.ix_(ii, ii)].copy()
    Sc = 0.5 * (Sc + Sc.T)
    na = len(ia)
    return 0.5 * (ld(Sc[:na, :na]) + ld(Sc[na:, na:]) - ld(Sc)) / LN2


class PA:
    """076 window model (route A); diag-class record only."""

    def __init__(self, n):
        self.n = n
        idx = np.arange(n)
        self.Cv = A_ ** np.abs(idx[:, None] - idx[None, :])
        self.mu, self.U = np.linalg.eigh(self.Cv)
        self.Cy = RHO ** 2 * self.Cv + SN2 * np.eye(n)
        self.lam = RHO ** 2 * self.mu + SN2
        n3 = 3 * n
        St = np.zeros((n3, n3))
        St[0:n, 0:n] = self.Cv
        St[n:2 * n, n:2 * n] = self.Cy
        St[2 * n:, 2 * n:] = self.Cv + TAU2 * np.eye(n)
        St[0:n, n:2 * n] = RHO * self.Cv
        St[n:2 * n, 0:n] = RHO * self.Cv
        St[0:n, 2 * n:] = self.Cv
        St[2 * n:, 0:n] = self.Cv
        St[n:2 * n, 2 * n:] = RHO * self.Cv
        St[2 * n:, n:2 * n] = RHO * self.Cv
        self.static = St

    def blk(self, d):
        return (self.U * d) @ self.U.T

    def sigma_diagclass(self, g, h, z):
        n = self.n
        Ay = self.blk(g)
        Av = self.blk(h)
        Cvh = RHO * self.Cv @ Ay.T + self.Cv @ Av.T
        Cyh = self.Cy @ Ay.T + RHO * self.Cv @ Av.T
        Chh = (Ay @ self.Cy @ Ay.T + Av @ self.Cv @ Av.T
               + Ay @ (RHO * self.Cv) @ Av.T
               + Av @ (RHO * self.Cv) @ Ay.T + self.blk(z))
        S = np.zeros((4 * n, 4 * n))
        S[:3 * n, :3 * n] = self.static
        S[0:n, 3 * n:] = Cvh
        S[3 * n:, 0:n] = Cvh.T
        S[n:2 * n, 3 * n:] = Cyh
        S[3 * n:, n:2 * n] = Cyh.T
        S[2 * n:3 * n, 3 * n:] = Cvh
        S[3 * n:, 2 * n:3 * n] = Cvh.T
        S[3 * n:, 3 * n:] = Chh
        return S


def terms_A(Pm, S, Delta):
    """076 terms(): per-cell L_a, leak; block per-symbol (verbatim)."""
    n = Pm.n
    ia = list(range(2 * n))
    Sb, Hb = 2 * n, 3 * n
    La, leak = [], []
    for t in range(n):
        se = min(t + Delta + 1, n)
        icS = list(range(Sb, Sb + se))
        icH = list(range(Hb, Hb + t))
        La.append(cmi_bits(S, ia, [Hb + t], icS + icH))
        if se < n:
            iaf = list(range(Sb + se, Sb + n))
            leak.append(cmi_bits(S, iaf, [Hb + t], icS + icH))
        else:
            leak.append(0.0)
    Iblk = cmi_bits(S, ia, list(range(Hb, Hb + n)),
                    list(range(Sb, Sb + n))) / n
    return np.array(La), np.array(leak), Iblk


# ============= route B: interleaved-Cholesky evaluator (R-IND-5) =========
class Mod:
    def __init__(self, n):
        self.n = n
        i = np.arange(n)
        self.Cv = A_ ** np.abs(i[:, None] - i[None, :])
        self.Cy = RHO ** 2 * self.Cv + SN2 * np.eye(n)
        self.Cs = self.Cv + TAU2 * np.eye(n)
        self.ev, self.Uv = np.linalg.eigh(self.Cv)
        self.lam = RHO ** 2 * self.ev + SN2

    def bl(self, d):
        return (self.Uv * d) @ self.Uv.T


def blocks_B(M, Ay, Av, Ncov, Au=None):
    Cvh = M.Cv @ (RHO * Ay.T + Av.T)
    Cyh = M.Cy @ Ay.T + RHO * M.Cv @ Av.T
    Csh = Cvh.copy()
    X = RHO * (Ay @ M.Cv @ Av.T)
    Chh = Ay @ M.Cy @ Ay.T + Av @ M.Cv @ Av.T + X + X.T + Ncov
    if Au is not None:
        Csh = Csh + TAU2 * Au.T
        Chh = Chh + TAU2 * Au @ Au.T
    return Cvh, Cyh, Csh, Chh


def distortion(M, Ay, Av, Ncov, Au=None):
    _, Cyh, _, Chh = blocks_B(M, Ay, Av, Ncov, Au)
    return float(np.mean(np.diag(M.Cy) - 2 * np.diag(Cyh)
                         + np.diag(Chh)))


def il_order(n, Delta):
    order, pos, prev = [], np.zeros(n, int), 0
    for t in range(n):
        se = min(t + Delta + 1, n)
        order += list(range(prev, se))
        pos[t] = len(order)
        order.append(n + t)
        prev = se
    return np.array(order), pos


def _chol_diag(C, order, pos):
    Cp = C[np.ix_(order, order)]
    j = 1e-11 * max(1.0, float(np.trace(Cp)) / Cp.shape[0])
    L = np.linalg.cholesky(Cp + j * np.eye(Cp.shape[0]))
    return np.diag(L)[pos] ** 2


def _CR(M, Ay, Av, Ncov, Au):
    n = M.n
    _, _, Csh, Chh = blocks_B(M, Ay, Av, Ncov, Au)
    C = np.zeros((2 * n, 2 * n))
    C[:n, :n] = M.Cs
    C[:n, n:] = Csh
    C[n:, :n] = Csh.T
    C[n:, n:] = Chh
    R = np.zeros((2 * n, 2 * n))
    R[:n, :n] = TAU2 * np.eye(n)
    if Au is not None:
        R[:n, n:] = TAU2 * Au.T
        R[n:, :n] = TAU2 * Au
        R[n:, n:] = TAU2 * Au @ Au.T + Ncov
    else:
        R[n:, n:] = Ncov
    return C, R


def la_chol(M, Ay, Av, Ncov, Delta, Au=None, op=None):
    """(La, leak, Iblk); identity resid = |mean La - Iblk - mean leak|."""
    n = M.n
    C, R = _CR(M, Ay, Av, Ncov, Au)
    order, pos = op if op is not None else il_order(n, Delta)
    vnum = _chol_diag(C, order, pos)
    vden = _chol_diag(R, order, pos)
    o2 = np.concatenate([np.arange(n), n + np.arange(n)])
    p2 = n + np.arange(n)
    vS = _chol_diag(C, o2, p2)
    vSden = _chol_diag(R, o2, p2)
    La = 0.5 * np.log2(vnum / vden)
    leak = 0.5 * np.log2(vnum / vS)
    Iblk = float(np.mean(0.5 * np.log2(vS / vSden)))
    return La, leak, Iblk


def la_val(M, Ay, Av, Ncov, Delta, Au=None, op=None):
    n = M.n
    C, R = _CR(M, Ay, Av, Ncov, Au)
    order, pos = op if op is not None else il_order(n, Delta)
    try:
        vnum = _chol_diag(C, order, pos)
        vden = _chol_diag(R, order, pos)
    except np.linalg.LinAlgError:
        return 60.0
    return float(np.mean(0.5 * np.log2(vnum / vden)))


def resid_of(M, Ay, Av, Ncov, Delta, Au=None):
    La, leak, Iblk = la_chol(M, Ay, Av, Ncov, Delta, Au=Au)
    return abs(float(np.mean(La)) - (Iblk + float(np.mean(leak))))


def kalman_pole():
    Mv = 1.0
    for _ in range(2000):
        K = Mv / (Mv + TAU2)
        Mv = A_ ** 2 * (1 - K) * Mv + (1 - A_ ** 2)
    K = Mv / (Mv + TAU2)
    return A_ * (1 - K)


# ===================== diagonal-class optimizer ==========================
def diag_dist(M, g, h, z):
    lam, mu = M.lam, M.ev
    return float(np.mean((1 - g) ** 2 * lam + h ** 2 * mu
                         - 2 * (1 - g) * h * RHO * mu + z))


def diag_opt(M, Delta, starts, maxiter=200, ftol=1e-11):
    n = M.n
    op = il_order(n, Delta)

    def f(x):
        g, h, u = x[:n], x[n:2 * n], x[2 * n:]
        return la_val(M, M.bl(g), M.bl(h), M.bl(u ** 2 + NF), Delta,
                      op=op)

    def dc(x):
        return D_TGT - diag_dist(M, x[:n], x[n:2 * n],
                                 x[2 * n:] ** 2 + NF)
    cons = [{'type': 'ineq', 'fun': dc}]
    best = None
    for x0 in starts:
        r = minimize(f, x0, method='SLSQP', constraints=cons,
                     bounds=[(-2, 2)] * (2 * n) + [(0, 2)] * n,
                     options={'maxiter': maxiter, 'ftol': ftol})
        v = float(f(r.x))
        d = D_TGT - dc(r.x)
        if d <= D_TGT + 1e-7 and (best is None or v < best[0]):
            best = (v, r.x.copy(), d)
    return best


def start_scalar(M):
    n = M.n
    return np.concatenate([np.full(n, 1 - D_TGT), np.zeros(n),
                           np.full(n, np.sqrt(D_TGT * (1 - D_TGT)))])


def start_rwf(M):
    lam = M.lam
    lo, hi = 1e-9, float(lam.max())
    for _ in range(200):
        th = 0.5 * (lo + hi)
        if np.minimum(th, lam).mean() > D_TGT:
            hi = th
        else:
            lo = th
    Di = np.minimum(th, lam)
    g = 1 - Di / lam
    u = np.sqrt(np.maximum(Di * g - NF, 0.0))
    return np.concatenate([g, np.zeros(M.n), u])


def interp_x(M_prev, x_prev, M_new):
    """Cross-n warm start: interpolate (g,h,u) over the mode
    eigenvalue (eigh -> ascending in both)."""
    npv = M_prev.n
    g = np.interp(M_new.ev, M_prev.ev, x_prev[:npv])
    h = np.interp(M_new.ev, M_prev.ev, x_prev[npv:2 * npv])
    u = np.interp(M_new.ev, M_prev.ev, x_prev[2 * npv:])
    return np.concatenate([g, h, u])


# ===================== full-space optimizer ==============================
def fs_make(M, Delta):
    n = M.n
    it = np.tril_indices(n)
    op = il_order(n, Delta)
    nA = n * n
    nB = len(it[0])

    def parts(x):
        Ay = x[:nA].reshape(n, n)
        Av = x[nA:2 * nA].reshape(n, n)
        B = np.zeros((n, n))
        B[it] = x[2 * nA:2 * nA + nB]
        Ncov = B @ B.T + NF * np.eye(n)
        return Ay, Av, Ncov, B

    def f(x):
        Ay, Av, Ncov, _ = parts(x)
        return la_val(M, Ay, Av, Ncov, Delta, op=op)

    def dist(x):
        Ay, Av, Ncov, _ = parts(x)
        return distortion(M, Ay, Av, Ncov)

    def dist_jac(x):
        Ay, Av, _, B = parts(x)
        gAy = (2.0 / n) * (Ay @ M.Cy + RHO * Av @ M.Cv - M.Cy)
        gAv = (2.0 / n) * (Av @ M.Cv + RHO * Ay @ M.Cv - RHO * M.Cv)
        gB = (2.0 / n) * B
        return np.concatenate([gAy.ravel(), gAv.ravel(), gB[it]])

    return f, dist, dist_jac, parts, it


def fs_pack(Ay, Av, B, it):
    return np.concatenate([Ay.ravel(), Av.ravel(), B[it]])


def fs_opt(M, Delta, starts, maxiter=200, ftol=1e-10):
    f, dist, dist_jac, parts, it = fs_make(M, Delta)
    cons = [{'type': 'ineq', 'fun': lambda x: D_TGT - dist(x),
             'jac': lambda x: -dist_jac(x)}]
    best = None
    log = []
    for name, x0 in starts:
        v0 = float(f(x0))
        r = minimize(f, x0, method='SLSQP', constraints=cons,
                     options={'maxiter': maxiter, 'ftol': ftol})
        v = float(f(r.x))
        d = dist(r.x)
        ok = d <= D_TGT + 1e-6
        log.append((name, v0, v, d, int(r.nit), int(r.status), ok))
        if ok and (best is None or v < best[0]):
            best = (v, r.x.copy())
    return best, log, parts


def B_of(Ncov, n):
    w, Q = np.linalg.eigh(0.5 * (Ncov + Ncov.T) - NF * np.eye(n))
    return np.linalg.cholesky((Q * np.maximum(w, 1e-12)) @ Q.T
                              + 1e-12 * np.eye(n))


def diag_embed(M, xd):
    n = M.n
    g, h, u = xd[:n], xd[n:2 * n], xd[2 * n:]
    Ay, Av = M.bl(g), M.bl(h)
    Ncov = M.bl(u ** 2 + NF)
    return Ay, Av, B_of(Ncov, n)


def toe_ext(Amat, n2):
    n1 = Amat.shape[0]
    t0_ = n1 // 2
    O = np.zeros((n2, n2))
    for t in range(n2):
        for k in range(-t0_, n1 - t0_):
            j = t + k
            if 0 <= j < n2:
                O[t, j] = Amat[t0_, t0_ + k]
    return O


# ===================== exact per-mode block solver =======================
def mode_val(x, mu, lam):
    g, h, sz = x
    z = sz ** 2 + 1e-13
    csh = g * RHO * mu + h * mu
    css = mu + TAU2
    chh = g ** 2 * lam + h ** 2 * mu + 2 * g * h * RHO * mu + z
    vg = chh - csh ** 2 / css
    v = 0.5 * np.log2(max(vg, 1e-300) / z)
    d = (1 - g) ** 2 * lam + h ** 2 * mu - 2 * (1 - g) * h * RHO * mu + z
    return v, d


def block_exact(M, D=D_TGT, iters=42):
    n = M.n
    X = np.zeros((n, 3))
    X[:, 0] = 1 - D / M.lam
    X[:, 2] = np.sqrt(0.5 * D)
    lo, hi = 0.02, 30.0

    def pas(slp, X0):
        V = np.zeros(n)
        Dd = np.zeros(n)
        Xn = np.zeros((n, 3))
        for i in range(n):
            r = minimize(lambda x: (mode_val(x, M.ev[i], M.lam[i])[0]
                                    + slp * mode_val(x, M.ev[i],
                                                     M.lam[i])[1]),
                         X0[i], method='Nelder-Mead',
                         options={'xatol': 1e-11, 'fatol': 1e-14,
                                  'maxiter': 800})
            V[i], Dd[i] = mode_val(r.x, M.ev[i], M.lam[i])
            Xn[i] = r.x
        return V, Dd, Xn
    for _ in range(iters):
        slp = 0.5 * (lo + hi)
        V, Dd, X = pas(slp, X)
        if Dd.mean() < D:
            hi = slp
        else:
            lo = slp
    V, Dd, X = pas(hi, X)
    return float(V.mean()), float(Dd.mean()), X


# ===================== causal-spectral allocation ========================
def sl_cond(x, Se, Sv, Sy):
    al, be, sz = x
    z = sz ** 2 + 1e-13
    SyC = RHO ** 2 * Se + SN2
    vh = al ** 2 * SyC + be ** 2 * Se + 2 * al * be * RHO * Se + z
    v = 0.5 * np.log2(max(vh, 1e-300) / z)
    d = (1 - al) ** 2 * Sy + be ** 2 * Sv - 2 * (1 - al) * be * RHO * Sv \
        + z
    return v, d


def alloc(Se_grid, Sv_grid, Sy_grid, D=D_TGT, iters=40, X0=None):
    NW = len(Se_grid)
    X = X0 if X0 is not None else np.c_[
        1 - D / Sy_grid, np.zeros(NW), np.full(NW, np.sqrt(0.4 * D))]
    lo, hi = 0.02, 30.0

    def pas(slp, X0_):
        V = np.zeros(NW)
        Dd = np.zeros(NW)
        Xn = np.zeros((NW, 3))
        for i in range(NW):
            r = minimize(lambda x: (sl_cond(x, Se_grid[i], Sv_grid[i],
                                            Sy_grid[i])[0]
                                    + slp * sl_cond(x, Se_grid[i],
                                                    Sv_grid[i],
                                                    Sy_grid[i])[1]),
                         X0_[i], method='Nelder-Mead',
                         options={'xatol': 1e-11, 'fatol': 1e-14,
                                  'maxiter': 800})
            V[i], Dd[i] = sl_cond(r.x, Se_grid[i], Sv_grid[i],
                                  Sy_grid[i])
            Xn[i] = r.x
        return V, Dd, Xn
    for _ in range(iters):
        slp = 0.5 * (lo + hi)
        V, Dd, X = pas(slp, X)
        if Dd.mean() < D:
            hi = slp
        else:
            lo = slp
    V, Dd, X = pas(hi, X)
    return float(V.mean()), float(Dd.mean()), X


def gamma_e(Delta, m=400, kmax=70):
    """Autocov of e_t = V_t - E[V_t | S_{t-m..t+Delta}] (time domain)."""
    j = np.arange(-m, Delta + 1)
    G = A_ ** np.abs(j[:, None] - j[None, :]) + TAU2 * np.eye(len(j))
    c0 = A_ ** np.abs(j)
    w = np.linalg.solve(G, c0)
    gam = np.zeros(kmax + 1)
    for k in range(kmax + 1):
        cv_k = A_ ** np.abs(j - k)
        cv_0k = A_ ** np.abs(j + k)
        Gk = A_ ** np.abs(j[:, None] - (j[None, :] + k))
        Gk = Gk + TAU2 * (j[:, None] == (j[None, :] + k))
        gam[k] = (A_ ** k - w @ cv_k - w @ cv_0k + w @ Gk @ w)
    return gam


def Se_from_gamma(gam, wg):
    k = np.arange(1, len(gam))
    return gam[0] + 2 * np.sum(gam[1:, None]
                               * np.cos(k[:, None] * wg[None, :]),
                               axis=0)


LAM_S = kalman_pole()
vals["lambda_s"] = LAM_S
vals["lambda_s_m2"] = LAM_S ** -2

# ------------------------------------------------------------ s1 evaluators
print("[s1] evaluator cross-check (route A = 076 verbatim vs route B "
      "= interleaved Cholesky) at the sealed anchors ...", flush=True)
n16 = 16
MA = PA(n16)
MB = Mod(n16)
b16, b16d, Xb = block_exact(MB)
vals["s1_block16"] = b16
vals["s1_block16_err"] = abs(b16 - BLOCK16_SEALED)
verdicts["s1_block16_anchor"] = vals["s1_block16_err"] < 1e-7
xblk = np.concatenate([Xb[:, 0], Xb[:, 1],
                       np.sqrt(np.maximum(Xb[:, 2] ** 2 + 1e-13 - NF,
                                          0.0))])
rd0 = diag_opt(MB, 0, [start_rwf(MB), start_scalar(MB)], maxiter=250,
               ftol=1e-12)
xd0 = rd0[1]
vals["s1_diagUB0"] = rd0[0]
vals["s1_diagUB0_err"] = abs(rd0[0] - DIAG0_SEALED)
verdicts["s1_diagUB0_anchor"] = vals["s1_diagUB0_err"] < 5e-6
recs = {"rwf": start_rwf(MB), "scalar": start_scalar(MB),
        "blockopt": xblk, "diagUB0": xd0}
for k in (1, 2):
    xr = rngi.normal(0, 0.3, 3 * n16)
    xr[2 * n16:] = np.abs(xr[2 * n16:]) + 0.2
    recs[f"rand{k}"] = xr
xmax, imax = 0.0, 0.0
for nm, x in recs.items():
    g, h, u = x[:n16], x[n16:2 * n16], x[2 * n16:]
    z = u ** 2 + NF
    SA = MA.sigma_diagclass(g, h, z)
    Ay, Av, Nc = MB.bl(g), MB.bl(h), MB.bl(z)
    for Delta in (0, 2, 5):
        LaA, lkA, IbA = terms_A(MA, SA, Delta)
        LaB, lkB, IbB = la_chol(MB, Ay, Av, Nc, Delta)
        xmax = max(xmax, float(np.max(np.abs(LaA - LaB))),
                   float(np.max(np.abs(lkA - lkB))), abs(IbA - IbB))
        imax = max(imax, abs(float(np.mean(LaB)) - (IbB
                                                    + float(np.mean(lkB)))))
vals["s1_xcheck_max"] = xmax
vals["s1_identity_max"] = imax
verdicts["s1_xcheck"] = xmax < 1e-9
verdicts["s1_identity"] = imax < 1e-9
print(f"  block16 {b16:.10f} (sealed {BLOCK16_SEALED:.10f}, err "
      f"{vals['s1_block16_err']:.1e}); diag UB(0) {rd0[0]:.10f} "
      f"(sealed {DIAG0_SEALED}, err {vals['s1_diagUB0_err']:.1e})",
      flush=True)
print(f"  route A vs B max diff {xmax:.2e} over 6 records x 3 Deltas; "
      f"identity resid max {imax:.2e} (U-independent) "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------ s2 U-scoping
print("[s2] U-scoping faces (Hypothesis 1 load-bearing) ...", flush=True)
gsc = np.full(n16, 1 - D_TGT)
Ay_s = np.eye(n16) * (1 - D_TGT)
Av_s = np.zeros((n16, n16))
Nc_s = np.eye(n16) * (D_TGT * (1 - D_TGT))
# (a) random dense U-couplings break the chain rule
res_a = []
for k in range(2):
    Au = 0.08 * rngi.normal(0, 1, (n16, n16))
    res_a.append(resid_of(MB, Ay_s, Av_s, Nc_s, 0, Au=Au))
Au_up = 0.15 * np.triu(rngi.normal(0, 1, (n16, n16)), 1)  # anticausal
res_a.append(resid_of(MB, Ay_s, Av_s, Nc_s, 0, Au=Au_up))
vals["s2a_resids"] = res_a
verdicts["s2a_random_break"] = min(res_a) > 0.01
print(f"  (a) random U-coupled residuals {['%.4f' % r for r in res_a]}"
      f" (all > 0.01)", flush=True)
# (b) Delta-lag-causal U-coupling: identity extends exactly
res_b = []
tt, ss = np.meshgrid(np.arange(n16), np.arange(n16), indexing='ij')
Au_c0 = 0.08 * rngi.normal(0, 1, (n16, n16)) * (ss <= tt)
res_b.append(resid_of(MB, Ay_s, Av_s, Nc_s, 0, Au=Au_c0))
Au_c2 = 0.08 * rngi.normal(0, 1, (n16, n16)) * (ss <= tt + 2)
res_b.append(resid_of(MB, Ay_s, Av_s, Nc_s, 2, Au=Au_c2))
vals["s2b_resids"] = res_b
verdicts["s2b_causal_exact"] = max(res_b) < 1e-9
print(f"  (b) Delta-lag-causal residuals {['%.2e' % r for r in res_b]}"
      f" (< 1e-9: exact extension)", flush=True)
# (c) the trivial Delta-causal U-record
Ay_t = 0.54 * np.eye(n16)
Av_t = 0.23 * np.eye(n16)
Au_t = 0.23 * np.eye(n16)
z_t = 0.1625
d_t = distortion(MB, Ay_t, Av_t, z_t * np.eye(n16), Au=Au_t)
vals["s2c_dist_raw"] = d_t
if d_t > D_TGT:                      # literal 0.1625 overshoots D by
    z_t = z_t - (d_t - D_TGT) - 1e-12   # rounding: per-cell noise shave
d_t = distortion(MB, Ay_t, Av_t, z_t * np.eye(n16), Au=Au_t)
La_t, lk_t, Ib_t = la_chol(MB, Ay_t, Av_t, z_t * np.eye(n16), 0,
                           Au=Au_t)
v_t = float(np.mean(La_t))
r_t = abs(v_t - (Ib_t + float(np.mean(lk_t))))
vals["s2c_z_used"] = z_t
vals["s2c_dist"] = d_t
vals["s2c_La0"] = v_t
vals["s2c_resid"] = r_t
verdicts["s2c_feasible"] = d_t <= D_TGT + 1e-9
verdicts["s2c_below_055"] = v_t < 0.55
print(f"  (c) trivial U-record: z={z_t:.7f} (raw dist "
      f"{vals['s2c_dist_raw']:.7f} -> shaved), dist={d_t:.9f}, "
      f"L_a(0)={v_t:.6f} < 0.55, chain resid {r_t:.1e} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------- s3 family anchor
print("[s3] full-space min L_a(0) at n=16, 2 warm starts ...",
      flush=True)
f16, dist16, dj16, parts16, it16 = fs_make(MB, 0)
Ay0, Av0, B0 = diag_embed(MB, xd0)
sh = np.zeros((n16, n16))
sh[np.arange(n16 - 1), np.arange(1, n16)] = 1.0
starts3 = [("diag-embed", fs_pack(Ay0, Av0, B0, it16)),
           ("asym-shift", fs_pack(Ay0 + 0.08 * sh - 0.02 * sh.T,
                                  Av0 - 0.06 * sh + 0.02 * sh.T, B0,
                                  it16))]
best16, log3, _ = fs_opt(MB, 0, starts3, maxiter=200)
for nm, v0, v, d, nit, st, ok in log3:
    print(f"  {nm}: {v0:.6f} -> {v:.7f} d={d:.8f} nit={nit} st={st} "
          f"ok={ok}", flush=True)
v16_0 = best16[0]
Ayw0, Avw0, Ncw0, _ = parts16(best16[1])
vals["s3_fs16_D0"] = v16_0
vals["s3_start_vals"] = {nm: v for nm, _, v, _, _, _, _ in log3}
vals["s3_resid"] = resid_of(MB, Ayw0, Avw0, Ncw0, 0)
verdicts["s3_family_min"] = v16_0 <= 0.5668
verdicts["s3_beats_076"] = v16_0 < FS16_BEAT
verdicts["s2c_beats_family_min"] = vals["s2c_La0"] < v16_0
print(f"  family min L_a(0) = {v16_0:.7f} <= 0.5668, beats "
      f"{FS16_BEAT}; trivial U-record {vals['s2c_La0']:.6f} beats it "
      f"(scoping load-bearing) [{time.time()-t0:.0f}s]", flush=True)

# ----------------------------------------------------------- s4 mechanism
print("[s4] mechanism: transpose symmetry + sign boundary at lag "
      "Delta ...", flush=True)


def symres(Amat):
    return float(np.max(np.abs(Amat - Amat.T))
                 / max(np.max(np.abs(Amat)), 1e-12))


def boundary_lags(Av, n):
    out = []
    for t in (n // 2 - 1, n // 2, n // 2 + 1):
        k = Av[t]
        s0 = np.sign(k[t])
        jb = 0
        for j in range(0, n - t):
            if np.sign(k[t + j]) == s0:
                jb = j
            else:
                break
        out.append(int(jb))
    return out


vals["s4_Ay_symres_D0"] = symres(Ayw0)
verdicts["s4_Ay_transpose_sym"] = vals["s4_Ay_symres_D0"] < 1e-3
bl_ok = True
bls = {0: boundary_lags(Avw0, n16)}
winners = {0: (Ayw0, Avw0, Ncw0)}
xd_prev = xd0
prev_pack = best16[1]
for Delta in (1, 2):
    rdd = diag_opt(MB, Delta, [xd_prev], maxiter=200, ftol=1e-12)
    xd_prev = rdd[1]
    AyD, AvD, BD = diag_embed(MB, rdd[1])
    fD, _, _, partsD, itD = fs_make(MB, Delta)
    stD = [("prevD", prev_pack),
           ("diag-embed", fs_pack(AyD, AvD, BD, itD))]
    bD, logD, _ = fs_opt(MB, Delta, stD, maxiter=150)
    for nm, v0, v, d, nit, st, ok in logD:
        print(f"  D={Delta} {nm}: {v0:.6f} -> {v:.7f} nit={nit} "
              f"st={st} ok={ok}", flush=True)
    AyW, AvW, NcW, _ = partsD(bD[1])
    winners[Delta] = (AyW, AvW, NcW)
    bls[Delta] = boundary_lags(AvW, n16)
    vals[f"s4_fs16_D{Delta}"] = bD[0]
    vals[f"s4_Ay_symres_D{Delta}"] = symres(AyW)
    prev_pack = bD[1]
for Delta in (0, 1, 2):
    if any(b != Delta for b in bls[Delta]):
        bl_ok = False
vals["s4_boundary_lags"] = {str(d): bls[d] for d in bls}
verdicts["s4_sign_boundary_at_Delta"] = bl_ok
print(f"  Ay sym-resid(D=0) {vals['s4_Ay_symres_D0']:.2e} < 1e-3; "
      f"interior-row Av boundary lags {vals['s4_boundary_lags']} "
      f"(== Delta) [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------ s5 ladder + rate
print("[s5] diag ladder (24,32,48)x(4,5,6) + closure-rate face ...",
      flush=True)
ladder = {}
blocks_n = {16: b16}
Mprev, xprev_by_D = MB, {}
la_err_max = 0.0
for n in (24, 32, 48):
    Mn = Mod(n)
    bl_n, _, _ = block_exact(Mn)
    blocks_n[n] = bl_n
    ladder[n] = {"block": bl_n}
    xchain = None
    for Delta in (4, 5, 6):
        if Delta == 4:
            if n == 24:
                starts = [start_rwf(Mn), start_scalar(Mn)]
            else:
                starts = [interp_x(Mprev, xprev_by_D[4], Mn),
                          start_rwf(Mn)]
        else:
            starts = [xchain]
        r = diag_opt(Mn, Delta, starts, maxiter=300, ftol=1e-13)
        r2 = diag_opt(Mn, Delta, [r[1]], maxiter=300, ftol=1e-14)
        if r2 and r2[0] < r[0]:
            r = r2
        xchain = r[1]
        xprev_by_D[Delta] = r[1]
        err = abs(r[0] - HARD_LA[(n, Delta)])
        la_err_max = max(la_err_max, err)
        ladder[n][Delta] = {"La": r[0], "excess": r[0] - bl_n,
                            "hard_err": err}
        print(f"  n={n} D={Delta}: La={r[0]:.10f} (hard "
              f"{HARD_LA[(n, Delta)]:.10f}, err {err:.1e}) "
              f"excess={r[0]-bl_n:.4e}", flush=True)
    Mprev = Mn
vals["s5_ladder"] = {str(n): {str(k): v for k, v in ladder[n].items()}
                     for n in ladder}
vals["s5_la_err_max"] = la_err_max
verdicts["s5_ladder_reproduced"] = la_err_max < 1e-6
E = {D: 3 * ladder[48][D]["excess"] - 2 * ladder[32][D]["excess"]
     for D in (4, 5, 6)}
r45 = E[4] / E[5]
r56 = E[5] / E[6]
vals["s5_Einf_3248"] = {str(k): v for k, v in E.items()}
vals["s5_ratio_45"] = r45
vals["s5_ratio_56"] = r56
bound = LAM_S ** -2 + 0.15
verdicts["s5_ratios_rise"] = r45 < r56
verdicts["s5_ratios_below_pole"] = (r45 < bound) and (r56 < bound)
print(f"  E_inf(32/48 two-point) ratios: 4->5 {r45:.3f} < 5->6 "
      f"{r56:.3f} < {bound:.3f} (= lam_s^-2 + 0.15) "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ---------------------------------------- s6 reference-construction gaps
print("[s6] causal-spectral allocation + full-space plateau gaps ...",
      flush=True)
NW = 256
wg = (np.arange(NW) + 0.5) * np.pi / NW
Svw = (1 - A_ ** 2) / (1 + A_ ** 2 - 2 * A_ * np.cos(wg))
Syw = RHO ** 2 * Svw + SN2
Se_ts = Svw * TAU2 / (Svw + TAU2)
binf, dinf, Xw = alloc(Se_ts, Svw, Syw)
vals["s6_block_inf"] = binf
verdicts["s6_blockinf_anchor"] = abs(binf - BLOCKINF_REF) < 1e-5
cand = {}
for Delta in (2, 1, 0):
    gam = gamma_e(Delta)
    Se = Se_from_gamma(gam, wg)
    v, d, Xw = alloc(Se, Svw, Syw, X0=Xw)
    cand[Delta] = v
    print(f"  cand(D={Delta}) = {v:.7f} (hard {HARD_CAND[Delta]}, "
          f"err {abs(v - HARD_CAND[Delta]):.1e})", flush=True)
vals["s6_cand"] = {str(k): v for k, v in cand.items()}
cerr = max(abs(cand[D] - HARD_CAND[D]) for D in (0, 1, 2))
vals["s6_cand_err_max"] = cerr
verdicts["s6_alloc_reproduced"] = cerr < 1e-4
# full-space n=24 winners (Toeplitz-extended warm starts) -> two-point
M24 = Mod(24)
v16_by_D = {0: v16_0, 1: vals["s4_fs16_D1"], 2: vals["s4_fs16_D2"]}
v24_by_D = {}
for Delta in (0, 1, 2):
    AyW, AvW, NcW = winners[Delta]
    eAy, eAv = toe_ext(AyW, 24), toe_ext(AvW, 24)
    eN = toe_ext(NcW, 24)
    eN = 0.5 * (eN + eN.T)
    fD, _, _, partsD, itD = fs_make(M24, Delta)
    st = [("toe16", fs_pack(eAy, eAv,
                            B_of(eN + 1e-6 * np.eye(24), 24), itD))]
    b24, log6, _ = fs_opt(M24, Delta, st, maxiter=100)
    nm, v0, v, d, nit, stt, ok = log6[0]
    print(f"  n=24 D={Delta} toe16: {v0:.6f} -> {v:.7f} nit={nit} "
          f"st={stt} ok={ok}", flush=True)
    v24_by_D[Delta] = b24[0]
vals["s6_fs24"] = {str(k): v for k, v in v24_by_D.items()}
err_cal = abs(3 * blocks_n[24] - 2 * blocks_n[16] - binf)
vals["s6_err_cal"] = err_cal
gaps = {}
gap_ok = True
for Delta in (0, 1, 2):
    twopt = 3 * v24_by_D[Delta] - 2 * v16_by_D[Delta]
    gaps[Delta] = twopt - cand[Delta]
    if not (gaps[Delta] > 3 * err_cal):
        gap_ok = False
    print(f"  D={Delta}: twopt(16,24)={twopt:.7f}, plateau gap "
          f"{gaps[Delta]:+.6f} > 3 x err_cal {3*err_cal:.1e} "
          f"({gaps[Delta]/max(err_cal,1e-12):.0f}x)", flush=True)
vals["s6_gaps"] = {str(k): v for k, v in gaps.items()}
verdicts["s6_plateau_gaps"] = gap_ok
print(f"  block_inf={binf:.7f} (ref {BLOCKINF_REF}); err_cal "
      f"{err_cal:.2e} [{time.time()-t0:.0f}s]", flush=True)

# -------------------------------------------------------------------- report
verdicts = {k: bool(v) for k, v in verdicts.items()}
allpass = all(verdicts.values())
print()
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")


def jsafe(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(o)


out = {"verdict": verdicts, "GO14PL_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14PL-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
