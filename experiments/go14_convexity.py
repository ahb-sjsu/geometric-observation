#!/usr/bin/env python
"""GO-14 convexity-theorem harness (Theorems R + C of the causal-erasure
coordinate; prereg 079 pending -- nothing sealed here, this harness nets
the moment-coordinate representation, the joint-convexity certificates,
and the certified two-sided anchor brackets).

s1 representation identity (Theorem R): the moment-coordinate evaluator
   2 ln2 n L_a = [lndet(Gam - HQH') - lndet(Gam - HPH')]
                 + sum_j [ln Var(S_j|S^{j-1}) - ln Var(S_j|S^{j-1},
                   Yh^{k(j)})]
   vs a DEFINITIONAL per-cell CMI evaluator (4n joint covariance), over
   a fixed grid of (record, n, Delta) cells including the edges
   Delta in {0, n-2, n-1, n}, AND two non-staircase nondecreasing
   schedules with the schedule-general k(j) = #{t: se(t) < j}
   (R-IND-5 restatement 1: the staircase form k(j) = max(0, j-Delta-1)
   is prefix-schedule-specific); gate max residual < 1e-9;
s2 certificates (Theorem C legs): eigmin(Q) > -1e-12; P - Q equals the
   closed form SigW^-1 Sig_{W|S} SigW^-1 to < 1e-12; eigmin(P-Q) at
   n in {8,16,24,32} matches the quoted per-n values within 1e-6
   (restatement 5: decreasing in n, >= 3.9e-3 for n <= 32); Sylvester
   det identity det(I-Z) = det(M_P)/det(M_Q) on fixed records;
s3 Jensen midpoints in (H, Gamma): pinned-seed sweep, >= 4,000 pairs
   across n in {8,12,16} x Delta in {0,1,2,5}, gate ZERO violations
   (threshold 1e-9); per-piece block/leak midpoints zero violations
   (per-cell convexity stays OPEN -- restatement 4 -- only the
   regrouped pieces are gated);
s4 tangent-plane at the (16,0) winner: >= 300 pinned points, zero
   violations of f(x) >= f(w) + <grad f(w), x - w>;
s5 anchor brackets: recompute the Lagrangian-polish certified LB at
   (16,0), (16,1), (24,0), (32,0) by mu-bisection on dist(x(mu)) = D
   (self-contained cold starts -- convexity makes every KKT point
   global, so no stored winners are needed); gate LB <= winner value
   AND width < 2x the R-IND-5 verifier's quoted width; block_16
   bracket at Delta = n; gate the sandwich-margin interval
   min L_a(0) - block_16 within [0.0317, 0.0318]; winner upper ends
   are feasible-projected (restatement 6: raw polish endpoints sit
   ~1e-8..1e-11 outside D-feasibility; correction ~1e-10..1e-8,
   recorded);
s6 U-legs (restatement 2): U-independence is ONE premise, load-bearing
   in TWO legs of Theorem R -- a fixed dense-U-coupled record shows
   moment-form residual > 0.1 with only-one-leg corrections and
   < 1e-9 with both legs corrected; a Delta-causal U-record shows
   record-space chain rule residual < 1e-9 but moment-form residual
   > 0.5 (the non-conflation gate: the record-space chain-rule
   extension does NOT rescue moment-form Theorem R).

Sentinel ===GO14CX-JSON=== with ===END===; flag GO14CX_supported.
Pilot seed 20261120 / governed seed 20261121. SEED STAMPS ONLY: the
seed is recorded in the output and feeds NO computation -- all random
draws use an internally pinned generator (20260806) so pilot and
governed verify identical numbers; all optimizers are deterministic
warm-started (the 070 lesson). Evaluator lineage: R-IND-5 verifier
vlib (jitter-free cho_solve conditional variances) + prover
f_and_grad (envelope gradient of the leak pivots), both adapted and
re-validated against the sealed anchors block_16 = 0.5349675145 and
family min L_a(0) = 0.5667581350 at n=16.

All floating-point certificates (restatement 7): no interval
arithmetic; certified widths exceed f64 error by ~7 orders.
"""
import argparse
import json
import sys
import time

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261120 if a_.pilot
                                            else 20261121)
rngi = np.random.default_rng(20260806)   # pinned: draws identical
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
D_TGT = 0.3
LN2 = np.log(2.0)

# sealed / R-IND-5-confirmed reference values (bars; every gated
# quantity below is recomputed from scratch)
BLOCK16_SEALED = 0.5349675144698425      # 076 seal (s3 block16)
VSTAR = {(16, 0): 0.5667581350,          # 078-lineage family anchors
         (16, 1): 0.5408064658,          # (R-IND-5 winner evaluations)
         (24, 0): 0.5654138570,
         (32, 0): 0.5647418676}
# R-IND-5 verifier / prover certified widths of record (tighter of the
# two per anchor); gate = 2x these
WIDTH_REF = {(16, 0): 3.45e-6, (16, 1): 3.6e-6, (24, 0): 4.3e-6,
             (32, 0): 1.7e-5}
# eigmin(P-Q), pinned (restatement 5: decreasing in n; quote per-n or
# ">= 3.9e-3 for n <= 32")
EIGPQ_REF = {8: 1.0382003788e-2, 16: 5.5944061668e-3,
             24: 4.4308928741e-3, 32: 3.9528701408e-3}
MARGIN_LO, MARGIN_HI = 0.0317, 0.0318    # sandwich-margin gate window


# ===================== model + moment coordinates ========================
class Model:
    def __init__(self, n):
        self.n = n
        i = np.arange(n)
        self.Cv = A_ ** np.abs(i[:, None] - i[None, :])
        self.Cy = RHO ** 2 * self.Cv + SN2 * np.eye(n)
        self.Cs = self.Cv + TAU2 * np.eye(n)
        self.SigW = np.block([[self.Cv, RHO * self.Cv],
                              [RHO * self.Cv, self.Cy]])
        self.SigWinv = np.linalg.inv(self.SigW)
        self.CovWS = np.vstack([self.Cv, RHO * self.Cv])
        self.CovWY = np.vstack([RHO * self.Cv, self.Cy])
        self.P = self.SigWinv
        self.Q = (self.SigWinv @ self.CovWS
                  @ np.linalg.solve(self.Cs, self.CovWS.T)
                  @ self.SigWinv)
        self.K = self.CovWS.T @ self.SigWinv        # Csh = K H'
        self.GY = self.SigWinv @ self.CovWY
        self.trCy = float(np.trace(self.Cy))
        Lc = np.linalg.cholesky(self.Cs)
        self.lnpivS = 2.0 * np.log(np.diag(Lc))


def cvar(S, i, cond):
    """Var(x_i | x_cond), jitter-free."""
    if len(cond) == 0:
        return float(S[i, i])
    C = S[np.ix_(cond, cond)]
    b = S[cond, i]
    cf = cho_factor(C, lower=True, check_finite=False)
    return float(S[i, i] - b @ cho_solve(cf, b, check_finite=False))


def joint4(M, Ay, Av, Ncov, Au=None):
    """Cov of (V^n, Y^n, S^n, Yh^n), built directly from definitions."""
    n = M.n
    Cv, Cy = M.Cv, M.Cy
    CvY = RHO * Cv
    CvH = Cv @ Av.T + CvY @ Ay.T
    CyH = CvY.T @ Av.T + Cy @ Ay.T
    CsH = CvH.copy()
    ChH = (Av @ Cv @ Av.T + Ay @ Cy @ Ay.T
           + Av @ CvY @ Ay.T + Ay @ CvY.T @ Av.T + Ncov)
    if Au is not None:
        CsH = CsH + TAU2 * Au.T
        ChH = ChH + TAU2 * Au @ Au.T
    Z = np.zeros((4 * n, 4 * n))
    Z[0:n, 0:n] = Cv
    Z[n:2 * n, n:2 * n] = Cy
    Z[2 * n:3 * n, 2 * n:3 * n] = M.Cs
    Z[3 * n:, 3 * n:] = ChH

    def put(i, j, B):
        Z[i * n:(i + 1) * n, j * n:(j + 1) * n] = B
        Z[j * n:(j + 1) * n, i * n:(i + 1) * n] = B.T
    put(0, 1, CvY)
    put(0, 2, Cv)
    put(1, 2, CvY.T)
    put(0, 3, CvH)
    put(1, 3, CyH)
    put(2, 3, CsH)
    return 0.5 * (Z + Z.T)


def sched_prefix(n, Delta):
    """se0(t) = 0-based count of S cells visible to the eraser of cell
    t: min(t + Delta + 1, n)."""
    return np.minimum(np.arange(n) + Delta + 1, n)


def nla_def(M, Ay, Av, Ncov, Delta=None, Au=None, se0=None):
    """n * L_a in bits BY DEFINITION: per-cell CMI on the 4n joint."""
    n = M.n
    if se0 is None:
        se0 = sched_prefix(n, Delta)
    S4 = joint4(M, Ay, Av, Ncov, Au)
    iT = list(range(2 * n))
    Sb, Hb = 2 * n, 3 * n
    tot = 0.0
    for t in range(n):
        cond = list(range(Sb, Sb + se0[t])) + list(range(Hb, Hb + t))
        vnum = cvar(S4, Hb + t, cond)
        vden = cvar(S4, Hb + t, iT + cond)
        tot += 0.5 * np.log2(vnum / vden)
    return tot


def moments(M, Ay, Av, Ncov):
    """F0 record -> (H, Gamma) moment coordinates (W = (V; Y))."""
    Ablk = np.hstack([Av, Ay])
    H = Ablk @ M.SigW
    Gam = Ablk @ M.SigW @ Ablk.T + Ncov
    return H, 0.5 * (Gam + Gam.T)


def kcounts(n, se0):
    """Schedule-general k(j), 0-based: #{t: se0(t) <= j} = number of
    Yh cells preceding S_{j+1} in the interleaved order."""
    return np.array([int(np.sum(se0 <= j)) for j in range(n)])


def repr_bits(M, H, Gam, Delta=None, se0=None, ret_parts=False):
    """Theorem R RHS in TOTAL bits (n L_a): block bracket + leak sum.
    Returns None outside int D."""
    n = M.n
    if se0 is None:
        se0 = sched_prefix(n, Delta)
    MQ = Gam - H @ M.Q @ H.T
    MP = Gam - H @ M.P @ H.T
    sQ, lQ = np.linalg.slogdet(MQ)
    sP, lP = np.linalg.slogdet(MP)
    if sQ <= 0 or sP <= 0:
        return None
    ks = kcounts(n, se0)
    Csh = M.K @ H.T
    J = np.block([[M.Cs, Csh], [Csh.T, Gam]])
    lk = 0.0
    for j in range(n):
        cond = list(range(j)) + [n + i for i in range(ks[j])]
        try:
            s = cvar(J, j, cond)
        except np.linalg.LinAlgError:
            return None
        if s <= 0:
            return None
        lk += M.lnpivS[j] - np.log(s)
    if ret_parts:
        return ((lQ - lP) / (2 * LN2), lk / (2 * LN2))
    return (lQ - lP + lk) / (2 * LN2)


def dist_HG(M, H, Gam):
    """Mean per-cell distortion, AFFINE in (H, Gamma)."""
    return (M.trCy - 2.0 * float(np.sum(H * M.GY.T))
            + float(np.trace(Gam))) / M.n


def grad_dist(M):
    return -(2.0 / M.n) * M.GY.T, np.eye(M.n) / M.n


def f_and_grad(M, H, Gam, Delta):
    """Per-symbol value (bits) + analytic gradients in full-matrix
    Frobenius coordinates (prover derivation, FD-validated on the
    R-IND-5 record; envelope gradient -u_j u_j'/s_j per leak pivot)."""
    n = M.n
    MQ = Gam - H @ M.Q @ H.T
    MP = Gam - H @ M.P @ H.T
    try:
        LQ = np.linalg.cholesky(MQ)
        LP = np.linalg.cholesky(MP)
    except np.linalg.LinAlgError:
        return None
    val = 2.0 * (float(np.sum(np.log(np.diag(LQ))))
                 - float(np.sum(np.log(np.diag(LP)))))
    ks = kcounts(n, sched_prefix(n, Delta))
    Csh = M.K @ H.T
    J = np.block([[M.Cs, Csh], [Csh.T, Gam]])
    GJ = np.zeros((2 * n, 2 * n))
    for j in range(n):
        cond = list(range(j)) + [n + i for i in range(ks[j])]
        try:
            if cond:
                C = J[np.ix_(cond, cond)]
                b = J[cond, j]
                cf = cho_factor(C, lower=True, check_finite=False)
                w = cho_solve(cf, b, check_finite=False)
                s = float(J[j, j] - b @ w)
            else:
                w = np.zeros(0)
                s = float(J[j, j])
            if s <= 0:
                return None
        except np.linalg.LinAlgError:
            return None
        val += M.lnpivS[j] - np.log(s)
        u = np.zeros(2 * n)
        u[j] = 1.0
        u[cond] = -w
        GJ -= np.outer(u, u) / s
    SC = 1.0 / (2.0 * n * LN2)
    MQi = np.linalg.inv(MQ)
    MPi = np.linalg.inv(MP)
    gG = SC * (MQi - MPi + GJ[n:, n:])
    gH = SC * (-2.0 * MQi @ H @ M.Q + 2.0 * MPi @ H @ M.P
               + 2.0 * GJ[n:, :n] @ M.K)
    return SC * val, gH, 0.5 * (gG + gG.T)


# ===================== samplers (internally pinned) ======================
def rand_rec(M, rng, style):
    n = M.n
    if style == 0:
        Ay = 0.7 * np.eye(n) + 0.15 * rng.normal(size=(n, n))
        Av = 0.15 * rng.normal(size=(n, n))
        B = 0.3 * rng.normal(size=(n, n))
        N = B @ B.T / n + 0.05 * np.eye(n)
    elif style == 1:
        Ay = 0.4 * rng.normal(size=(n, n))
        Av = 0.4 * rng.normal(size=(n, n))
        B = 0.5 * rng.normal(size=(n, n))
        N = B @ B.T / np.sqrt(n) + 0.02 * np.eye(n)
    else:
        Ay = 0.7 * np.eye(n) + 0.05 * rng.normal(size=(n, n))
        Av = 0.05 * rng.normal(size=(n, n))
        B = 0.1 * rng.normal(size=(n, n))
        N = B @ B.T / n + 2e-4 * np.eye(n)
    return Ay, Av, N


def sample_HG(M, rng, style):
    """Point of int D directly: H free, Gam = H P H' + Ncov."""
    n = M.n
    if style == 0:
        Ay = 0.6 * np.eye(n) + 0.2 * rng.normal(size=(n, n))
        Av = 0.2 * rng.normal(size=(n, n))
        B = 0.35 * rng.normal(size=(n, n))
        Ncov = B @ B.T / n + 0.03 * np.eye(n)
        return moments(M, Ay, Av, Ncov)
    if style == 1:
        H = rng.normal(scale=rng.uniform(0.1, 0.9), size=(n, 2 * n))
        B = rng.normal(scale=0.5, size=(n, n))
        Ncov = B @ B.T / np.sqrt(n) + 0.01 * np.eye(n)
    elif style == 2:
        H = rng.normal(scale=0.4, size=(n, 2 * n))
        B = rng.normal(scale=0.15, size=(n, n + 2))
        Ncov = B @ B.T / n + 1e-6 * np.eye(n)
    else:
        H = rng.normal(scale=1.2, size=(n, 2 * n))
        B = rng.normal(scale=1.0, size=(n, n))
        Ncov = B @ B.T + 0.1 * np.eye(n)
    Gam = H @ M.P @ H.T + Ncov
    return H, 0.5 * (Gam + Gam.T)


# ===================== record-space route (U-coupled, s6) ================
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
    L = np.linalg.cholesky(Cp)
    return np.diag(L)[pos] ** 2


def la_record(M, Ay, Av, Ncov, Delta, Au=None):
    """(La, leak, Iblk) per-cell bits, record space, exact-with-Au
    interleaved-Cholesky route (076/R-IND-5 lineage)."""
    n = M.n
    Cvh = M.Cv @ (RHO * Ay.T + Av.T)
    Csh = Cvh.copy()
    X = RHO * (Ay @ M.Cv @ Av.T)
    Chh = Ay @ M.Cy @ Ay.T + Av @ M.Cv @ Av.T + X + X.T + Ncov
    if Au is not None:
        Csh = Csh + TAU2 * Au.T
        Chh = Chh + TAU2 * Au @ Au.T
    C = np.block([[M.Cs, Csh], [Csh.T, Chh]])
    R = np.zeros((2 * n, 2 * n))
    R[:n, :n] = TAU2 * np.eye(n)
    if Au is not None:
        R[:n, n:] = TAU2 * Au.T
        R[n:, :n] = TAU2 * Au
        R[n:, n:] = TAU2 * Au @ Au.T + Ncov
    else:
        R[n:, n:] = Ncov
    order, pos = il_order(n, Delta)
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


def legs(M, Ay, Av, Nc, Au, Delta):
    """Theorem R RHS with 0/1/2 legs corrected for Au (verifier v1
    lineage). Returns (truth, as-stated, num-fixed, den-fixed,
    both-fixed), total bits."""
    n = M.n
    truth = nla_def(M, Ay, Av, Nc, Delta, Au=Au)
    H, G = moments(M, Ay, Av, Nc)
    G = G + TAU2 * Au @ Au.T            # true Gamma includes Au U
    se0 = sched_prefix(n, Delta)
    ks = kcounts(n, se0)
    CshF = M.K @ H.T                    # family form (WRONG under Au)
    CshT = CshF + TAU2 * Au.T           # true moments
    ldPF = np.linalg.slogdet(G - H @ M.P @ H.T)[1]
    R = np.zeros((2 * n, 2 * n))
    R[:n, :n] = TAU2 * np.eye(n)
    R[:n, n:] = TAU2 * Au.T
    R[n:, :n] = TAU2 * Au
    R[n:, n:] = TAU2 * Au @ Au.T + Nc
    ldPT = 0.0
    for t in range(n):
        cond = list(range(se0[t])) + [n + i for i in range(t)]
        ldPT += np.log(cvar(R, n + t, cond))

    def rhs(Csh, ldP):
        MQ = G - Csh.T @ np.linalg.solve(M.Cs, Csh)
        lQ = np.linalg.slogdet(MQ)[1]
        J = np.block([[M.Cs, Csh], [Csh.T, G]])
        lk = 0.0
        for j in range(n):
            cond = list(range(j)) + [n + i for i in range(ks[j])]
            lk += M.lnpivS[j] - np.log(cvar(J, j, cond))
        return (lQ - ldP + lk) / (2 * LN2)

    return (truth, rhs(CshF, ldPF), rhs(CshT, ldPF), rhs(CshF, ldPT),
            rhs(CshT, ldPT))


# ===================== certified-bracket machinery (s4/s5) ===============
def certify(n, Delta, maxit1=1200, maxit2=300, nbis=36):
    """Self-contained certified two-sided bracket at (n, Delta):
    mu-bisection on dist(x(mu)) = D over Lagrangian polishes (L-BFGS,
    analytic gradient) from a cold scalar-record start; LB by weak
    duality + moment-box tangent bound; UB by feasible projection
    (blend toward the near-copy record). Returns a dict."""
    M = Model(n)
    gDH, gDG = grad_dist(M)
    iu = np.triu_indices(n)
    symw = np.where(iu[0] == iu[1], 1.0, 2.0)

    def pack(H, G):
        return np.concatenate([H.ravel(), G[iu]])

    def unpack(x):
        H = x[:2 * n * n].reshape(n, 2 * n)
        G = np.zeros((n, n))
        G[iu] = x[2 * n * n:]
        return H, G + G.T - np.diag(np.diag(G))

    def solve(mu, x0, maxiter):
        def lagr(x):
            H, G = unpack(x)
            out = f_and_grad(M, H, G, Delta)
            if out is None:
                return 1e3, np.zeros_like(x)
            v, gh, gg = out
            return (v + mu * (dist_HG(M, H, G) - D_TGT),
                    np.concatenate([(gh + mu * gDH).ravel(),
                                    ((gg + mu * gDG))[iu] * symw]))
        res = minimize(lagr, x0, jac=True, method="L-BFGS-B",
                       options={"maxiter": maxiter, "ftol": 1e-18,
                                "gtol": 1e-14, "maxcor": 40})
        H_, G_ = unpack(res.x)
        v_, gh_, gg_ = f_and_grad(M, H_, G_, Delta)
        return res.x, v_, dist_HG(M, H_, G_), gh_, gg_

    H0, G0 = moments(M, 0.7 * np.eye(n), np.zeros((n, n)),
                     0.21 * np.eye(n))
    x = pack(H0, G0)
    lo, hi = 0.0, 4.0
    x, v_, d_, gh_, gg_ = solve(hi, x, maxit1)
    while d_ > D_TGT:
        hi *= 2.0
        x, v_, d_, gh_, gg_ = solve(hi, x, maxit2)
    mu = hi
    for _ in range(nbis):
        mu = 0.5 * (lo + hi)
        x, v_, d_, gh_, gg_ = solve(mu, x, maxit2)
        if d_ > D_TGT:
            lo = mu
        else:
            hi = mu
        if abs(d_ - D_TGT) < 1e-11:
            break
    x, v_, d_, gh_, gg_ = solve(mu, x, maxit1)
    rn = float(np.sqrt(np.sum((gh_ + mu * gDH) ** 2)
                       + np.sum((gg_ + mu * gDG) ** 2)))
    lag = v_ + mu * (d_ - D_TGT)
    H_, G_ = unpack(x)
    bG = (1.0 + np.sqrt(n * D_TGT)) ** 2
    Rbox = float(np.sqrt(np.sum((np.sqrt(bG) + np.abs(H_)) ** 2)
                         + np.sum((bG + np.abs(G_)) ** 2)))
    LB = lag - rn * Rbox
    # feasible projection for the UB end (restatement 6)
    proj = 0.0
    if d_ > D_TGT:
        Hid, Gid = moments(M, np.eye(n), np.zeros((n, n)),
                           1e-6 * np.eye(n))
        d0 = dist_HG(M, Hid, Gid)
        tt = (D_TGT - d0) / (d_ - d0)
        Hf, Gf = Hid + tt * (H_ - Hid), Gid + tt * (G_ - Gid)
        UB = repr_bits(M, Hf, Gf, Delta) / n
        proj = UB - v_
    else:
        UB = v_
    return {"mu": mu, "dist_minus_D": d_ - D_TGT, "rnorm": rn,
            "Rbox": Rbox, "LB": LB, "UB": UB, "width": UB - LB,
            "proj_corr": proj, "H": H_, "G": G_, "vraw": v_, "M": M}


# ------------------------------------------------------------ s1 identity
print("[s1] Theorem R representation identity: moment-coordinate "
      "evaluator vs definitional per-cell CMI ...", flush=True)
BAR_S1 = 1e-9
worst_s1 = 0.0
cells = 0
for n in (8, 12, 16):
    M = Model(n)
    for style in (0, 1, 2):
        for rep in (0, 1):
            Ay, Av, Nc = rand_rec(M, rngi, style)
            H, G = moments(M, Ay, Av, Nc)
            for Delta in sorted({0, 2, n - 2, n - 1, n}):
                truth = nla_def(M, Ay, Av, Nc, Delta)
                r = repr_bits(M, H, G, Delta)
                worst_s1 = max(worst_s1, abs(r - truth))
                cells += 1
vals["s1_cells_staircase"] = cells
vals["s1_resid_staircase"] = worst_s1
# two non-staircase nondecreasing schedules, schedule-general k(j)
worst_ns = 0.0
ns = 0
for n, seeds in ((8, 2), (12, 2)):
    M = Model(n)
    for rep in range(seeds):
        inc = rngi.integers(0, 3, size=n)
        se0 = np.minimum(np.cumsum(inc), n)
        Ay, Av, Nc = rand_rec(M, rngi, rep % 2)
        H, G = moments(M, Ay, Av, Nc)
        truth = nla_def(M, Ay, Av, Nc, se0=se0)
        r = repr_bits(M, H, G, se0=se0)
        worst_ns = max(worst_ns, abs(r - truth))
        ns += 1
vals["s1_cells_nonstaircase"] = ns
vals["s1_resid_nonstaircase"] = worst_ns
vals["s1_bar"] = BAR_S1
verdicts["s1_repr_identity"] = worst_s1 < BAR_S1
verdicts["s1_general_schedule"] = worst_ns < BAR_S1
print(f"  staircase grid: {cells} cells (edges Delta in "
      f"{{0, n-2, n-1, n}}), max |repr - def| = {worst_s1:.2e} < "
      f"{BAR_S1:.0e}", flush=True)
print(f"  non-staircase schedules (general k(j) = #{{t: se(t) < j}}): "
      f"{ns} cells, max resid = {worst_ns:.2e} [{time.time()-t0:.0f}s]",
      flush=True)

# --------------------------------------------------------- s2 certificates
print("[s2] Theorem C certificates: PSD legs, closed form, "
      "eigmin(P-Q) table, Sylvester ...", flush=True)
BAR_EIGQ = -1e-12
BAR_CF = 1e-12
BAR_EIGPQ = 1e-6
BAR_SYL = 1e-9
eq_min = 0.0
cf_max = 0.0
epq_err = 0.0
epq_tab = {}
for n in (8, 16, 24, 32):
    M = Model(n)
    eq_min = min(eq_min, float(np.linalg.eigvalsh(M.Q).min()))
    Rm = M.P - M.Q
    epq = float(np.linalg.eigvalsh(Rm).min())
    epq_tab[n] = epq
    epq_err = max(epq_err, abs(epq - EIGPQ_REF[n]))
    SigWS = M.SigW - M.CovWS @ np.linalg.solve(M.Cs, M.CovWS.T)
    cf_max = max(cf_max, float(np.max(np.abs(
        Rm - M.SigWinv @ SigWS @ M.SigWinv))))
vals["s2_eigminQ"] = eq_min
vals["s2_closedform_max"] = cf_max
vals["s2_eigminPQ"] = {str(k): v for k, v in epq_tab.items()}
vals["s2_eigminPQ_err_max"] = epq_err
verdicts["s2_Q_psd"] = eq_min > BAR_EIGQ
verdicts["s2_closed_form"] = cf_max < BAR_CF
verdicts["s2_eigminPQ_pinned"] = epq_err < BAR_EIGPQ
# Sylvester det identity det(I - Z) = det(M_P)/det(M_Q) on fixed records
n = 12
M = Model(n)
w, U = np.linalg.eigh(M.P - M.Q)
Rh = U @ np.diag(np.sqrt(np.clip(w, 0, None))) @ U.T
syl_max = 0.0
zin = True
tested = 0
while tested < 6:
    H, G = sample_HG(M, rngi, tested % 4)
    MQ = G - H @ M.Q @ H.T
    MP = G - H @ M.P @ H.T
    if np.linalg.slogdet(MP)[0] <= 0 or np.linalg.slogdet(MQ)[0] <= 0:
        continue
    Z = Rh @ H.T @ np.linalg.solve(MQ, H) @ Rh
    if float(np.linalg.eigvalsh(Z).max()) >= 1.0:
        zin = False
    lhs = np.linalg.slogdet(np.eye(2 * n) - Z)[1]
    rhs_ = np.linalg.slogdet(MP)[1] - np.linalg.slogdet(MQ)[1]
    syl_max = max(syl_max, abs(lhs - rhs_))
    tested += 1
vals["s2_sylvester_max"] = syl_max
vals["s2_bars"] = {"eigQ": BAR_EIGQ, "cf": BAR_CF, "eigPQ": BAR_EIGPQ,
                   "syl": BAR_SYL}
verdicts["s2_sylvester"] = syl_max < BAR_SYL and zin
print(f"  eigmin(Q) = {eq_min:+.2e} > -1e-12; |P-Q - closed form| = "
      f"{cf_max:.2e} < 1e-12", flush=True)
print(f"  eigmin(P-Q): " + ", ".join(
    f"n={k}: {v:.6e}" for k, v in epq_tab.items())
    + f" (max err vs pinned {epq_err:.1e})", flush=True)
print(f"  Sylvester det(I-Z)=det(MP)/det(MQ): {tested} records, max "
      f"resid {syl_max:.2e}, Z < I on int D: {zin} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------- s3 Jensen
print("[s3] Jensen midpoints in (H, Gamma): total + per-piece ...",
      flush=True)
BAR_JEN = 1e-9
PAIRS = {8: 550, 12: 300, 16: 200}
tot = viol = skip = 0
worst_j = -1e9
for n in (8, 12, 16):
    M = Model(n)
    for Delta in (0, 1, 2, 5):
        for _ in range(PAIRS[n]):
            H1, G1 = sample_HG(M, rngi, int(rngi.integers(4)))
            H2, G2 = sample_HG(M, rngi, int(rngi.integers(4)))
            f1 = repr_bits(M, H1, G1, Delta)
            f2 = repr_bits(M, H2, G2, Delta)
            fm = repr_bits(M, 0.5 * (H1 + H2), 0.5 * (G1 + G2), Delta)
            if None in (f1, f2, fm):
                skip += 1
                continue
            gap = fm - 0.5 * (f1 + f2)
            worst_j = max(worst_j, gap)
            viol += gap > BAR_JEN
            tot += 1
vals["s3_pairs"] = tot
vals["s3_skipped"] = skip
vals["s3_worst_gap"] = worst_j
vals["s3_violations"] = viol
vals["s3_bar"] = BAR_JEN
verdicts["s3_jensen_total"] = (viol == 0) and (tot >= 4000)
print(f"  total: {tot} pairs ({skip} skipped outside int D), "
      f"violations {viol}, worst gap {worst_j:+.2e} "
      f"[{time.time()-t0:.0f}s]", flush=True)
vb = vl = 0
wb = wl = -1e9
np_pairs = 0
for n in (8, 12):
    M = Model(n)
    for Delta in (0, 2):
        for _ in range(60):
            H1, G1 = sample_HG(M, rngi, int(rngi.integers(4)))
            H2, G2 = sample_HG(M, rngi, int(rngi.integers(4)))
            p1 = repr_bits(M, H1, G1, Delta, ret_parts=True)
            p2 = repr_bits(M, H2, G2, Delta, ret_parts=True)
            pm = repr_bits(M, 0.5 * (H1 + H2), 0.5 * (G1 + G2), Delta,
                           ret_parts=True)
            if None in (p1, p2, pm):
                continue
            gb = pm[0] - 0.5 * (p1[0] + p2[0])
            gl = pm[1] - 0.5 * (p1[1] + p2[1])
            wb, wl = max(wb, gb), max(wl, gl)
            vb += gb > BAR_JEN
            vl += gl > BAR_JEN
            np_pairs += 1
vals["s3_piece_pairs"] = np_pairs
vals["s3_piece_worst"] = {"block": wb, "leak": wl}
verdicts["s3_jensen_pieces"] = (vb == 0) and (vl == 0)
print(f"  per-piece ({np_pairs} pairs): block viol {vb} worst "
      f"{wb:+.2e}; leak viol {vl} worst {wl:+.2e} (per-CELL convexity "
      f"stays OPEN -- not gated) [{time.time()-t0:.0f}s]", flush=True)

# -------------------------------------------- (16,0) certificate (for s4)
print("[s4] tangent plane at the (16,0) winner ...", flush=True)
c160 = certify(16, 0)
M16 = c160["M"]
Hw, Gw = c160["H"], c160["G"]
vw, gHw, gGw = f_and_grad(M16, Hw, Gw, 0)
BAR_TAN = -1e-9
minsl = 1e9
tviol = ttested = 0
while ttested < 320:
    Hx, Gx = sample_HG(M16, rngi, int(rngi.integers(4)))
    fx = repr_bits(M16, Hx, Gx, 0)
    if fx is None:
        continue
    fx /= 16
    lin = vw + float(np.sum(gHw * (Hx - Hw)) + np.sum(gGw * (Gx - Gw)))
    sl = fx - lin
    minsl = min(minsl, sl)
    tviol += sl < BAR_TAN
    ttested += 1
vals["s4_points"] = ttested
vals["s4_min_slack"] = minsl
vals["s4_violations"] = tviol
vals["s4_bar"] = BAR_TAN
verdicts["s4_tangent_plane"] = (tviol == 0) and (ttested >= 300)
print(f"  {ttested} pinned points, violations {tviol}, min slack "
      f"{minsl:+.3e} [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------- s5 anchor brackets
print("[s5] certified anchor brackets (mu-bisection Lagrangian polish, "
      "cold starts) ...", flush=True)
bracket = {(16, 0): c160}
for (n, Delta) in ((16, 1), (24, 0), (32, 0)):
    bracket[(n, Delta)] = certify(n, Delta)
brk_ok = True
for (n, Delta), c in bracket.items():
    wbar = 2.0 * WIDTH_REF[(n, Delta)]
    ok = (c["LB"] <= VSTAR[(n, Delta)] + 1e-9 and c["LB"] <= c["UB"]
          and c["width"] < wbar
          and abs(c["UB"] - VSTAR[(n, Delta)]) < 5e-7)
    brk_ok = brk_ok and ok
    vals[f"s5_{n}_{Delta}"] = {
        "LB": c["LB"], "UB": c["UB"], "width": c["width"],
        "width_bar": wbar, "vstar_ref": VSTAR[(n, Delta)],
        "mu": c["mu"], "rnorm": c["rnorm"], "Rbox": c["Rbox"],
        "proj_corr": c["proj_corr"], "dist_minus_D": c["dist_minus_D"]}
    print(f"  ({n},{Delta}): [{c['LB']:.9f}, {c['UB']:.10f}] width "
          f"{c['width']:.2e} < {wbar:.1e}; ref v* "
          f"{VSTAR[(n, Delta)]:.10f} (UB err "
          f"{c['UB']-VSTAR[(n, Delta)]:+.1e}, proj corr "
          f"{c['proj_corr']:+.1e}) [{time.time()-t0:.0f}s]", flush=True)
verdicts["s5_anchor_brackets"] = brk_ok
# block_16 bracket at Delta = n (full-S schedule: leak = 0 identically)
cblk = certify(16, 16)
vals["s5_block16"] = {"LB": cblk["LB"], "UB": cblk["UB"],
                      "width": cblk["width"], "sealed": BLOCK16_SEALED}
verdicts["s5_block16_anchor"] = (
    cblk["LB"] <= BLOCK16_SEALED + 1e-9
    and abs(cblk["UB"] - BLOCK16_SEALED) < 5e-7)
mlo = c160["LB"] - cblk["UB"]
mhi = c160["UB"] - cblk["LB"]
vals["s5_margin"] = {"lo": mlo, "hi": mhi,
                     "window": [MARGIN_LO, MARGIN_HI]}
verdicts["s5_sandwich_margin"] = (MARGIN_LO <= mlo <= mhi <= MARGIN_HI)
print(f"  block_16 in [{cblk['LB']:.9f}, {cblk['UB']:.10f}] width "
      f"{cblk['width']:.2e} (sealed {BLOCK16_SEALED:.10f})", flush=True)
print(f"  sandwich margin minL_a(0) - block_16 in [{mlo:.7f}, "
      f"{mhi:.7f}] within [{MARGIN_LO}, {MARGIN_HI}] "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------- s6 U-legs
print("[s6] U-independence: one premise, two legs + the non-conflation "
      "gate ...", flush=True)
BAR_LEG_HI = 0.1
BAR_LEG_LO = 1e-9
BAR_NONCONF = 0.5
n = 12
M = Model(n)
Ay6, Av6, Nc6 = rand_rec(M, rngi, 0)
Au_dense = 0.15 * rngi.normal(size=(n, n)) + 0.25 * np.eye(n)
truth, r00, rN, rD, rND = legs(M, Ay6, Av6, Nc6, Au_dense, 0)
vals["s6_dense"] = {"as_stated": abs(r00 - truth),
                    "num_fixed": abs(rN - truth),
                    "den_fixed": abs(rD - truth),
                    "both_fixed": abs(rND - truth)}
verdicts["s6_two_legs"] = (
    abs(r00 - truth) > BAR_LEG_HI and abs(rN - truth) > BAR_LEG_HI
    and abs(rD - truth) > BAR_LEG_HI and abs(rND - truth) < BAR_LEG_LO)
print(f"  dense Au: as-stated {abs(r00-truth):.3f}, num-only "
      f"{abs(rN-truth):.3f}, den-only {abs(rD-truth):.3f} (all > 0.1); "
      f"both-fixed {abs(rND-truth):.1e} < 1e-9", flush=True)
# Delta-causal U-record: record-space chain rule exact, moment form NOT
Delta6 = 2
tt_, ss_ = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
Au_c = 0.15 * rngi.normal(size=(n, n)) * (ss_ <= tt_ + Delta6)
La6, lk6, Ib6 = la_record(M, Ay6, Av6, Nc6, Delta6, Au=Au_c)
chain_res = abs(float(np.mean(La6)) - (Ib6 + float(np.mean(lk6))))
tr2, rc2, _, _, _ = legs(M, Ay6, Av6, Nc6, Au_c, Delta6)
mom_res = abs(rc2 - tr2)
vals["s6_causal"] = {"chain_resid": chain_res, "moment_resid": mom_res}
vals["s6_bars"] = {"leg_hi": BAR_LEG_HI, "leg_lo": BAR_LEG_LO,
                   "nonconf": BAR_NONCONF}
verdicts["s6_nonconflation"] = (chain_res < BAR_LEG_LO
                                and mom_res > BAR_NONCONF)
print(f"  Delta-causal Au (Delta={Delta6}): record-space chain resid "
      f"{chain_res:.1e} < 1e-9 BUT moment-form resid {mom_res:.3f} > "
      f"0.5 -- the two extensions must not be conflated "
      f"[{time.time()-t0:.0f}s]", flush=True)

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


for c in bracket.values():
    c.pop("H", None), c.pop("G", None), c.pop("M", None)
out = {"verdict": verdicts, "GO14CX_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14CX-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
