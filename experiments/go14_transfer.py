#!/usr/bin/env python
"""GO-14 n-transfer harness (Theorem T, Hypothesis (H*), the executed
within-class ladder upgrade; registration 080 pending -- nothing here is
sealed).

Model: V AR(1) a = 0.8 unit variance; Y = 0.7 V + N, Var(Y) = 1;
S = V + U, tau2 = 0.4; D = 0.3; T = (V, Y); family F0 (records jointly
Gaussian with (V, Y) and INDEPENDENT of U); phi_n(Delta) = min L_a over
F0 on the n-window; kappa = (1/2) log2(1/(1-a^2)) = 0.736966 bits.

s1 SUBADDITIVITY (Theorem T(i), the unconditional leg).  Block
   concatenation of independent sub-window records: at EVERY cell the
   big-window per-cell term is <= the own-window term (numerators shrink
   under the extra conditioning; denominators are EQUAL because the
   concatenated noise is block-diagonal), hence f(n1+n2) <= f(n1)+f(n2).
   Grid (n1,n2) in {(8,8), (8,4)} x Delta in {0,2}, pinned F0 records.
   Gated: zero per-term violations, block-local denominator equality
   < 1e-12, and the totals inequality.  NOTE the per-term inequality is
   RECORD-UNIVERSAL (it holds for every F0 record, not only optimizers),
   which is exactly why pinned records suffice here and no optimizer
   enters this section; the optimizer-level Fekete inequality is netted
   separately in s7 from certified anchors, with a 1e-2-scale slack.

s2 SET IDENTITY (the interleaved-prefix match): bigC_t = ownC_t UNION E
   with E = (S^{b1}, Yh^{b1}) as a FORMAL set difference at every
   block-2 cell, plus the block-1 extension set and the single
   interleaved total order realizing both ownC_t and pfx_j with
   k(j) = #{t: se(t) < j}.  m in {3,5,8} x Delta in {0,1,2,m-1,m};
   gate zero failures.

s3 ZERO-CLAIM + F0-CONDITIONALITY.  I(E; S'_j | pfx_j, T^{b2}) = 0 for
   pinned F0 records (gate < 1e-12), AND the pinned U-coupled
   counterexamples break it: block-1 rows coupled to U^{b2} give 0.2223
   bits, block-2-ONLY coupling gives 0.0950 bits (the violation is
   induced purely through the conditioning).  The zero-claim and the
   marginalization step are F0-ONLY -- this is the family-conditionality
   gate.

s4 THE (H*) REFUTATION, netted as a fact (the 076 s2a precedent -- a
   harness netting a refutation).  Deterministic, D-feasible, F0
   records: (a) two V-copy rows in block 1 give D2 > c(0) = 0.4202858,
   refuting the SHARPENED per-side constant; (b) three Y-copy rows give
   D2 > 10 bits, i.e. ~26 kappa, refuting "<= kappa per side" outright.
   No universal constant exists; any proof must use optimizer structure.
   Both records are built analytically (no optimizer anywhere in s4).

s5 OPTIMIZER VERIFICATIONS at m in {8,16} (and at those two m ONLY):
   the per-side boundary charge D2 and I(E; T^{b2}) at the (16,0) and
   (32,0) family optimizers.  DISCLOSURE: these two quantities are
   evaluated at an OPTIMIZER endpoint, so the tight reproduction figures
   (recorded 0.076971/0.076926 and 0.5431) are REPORTED but the GATES
   are (i) the (H*) inequalities D2 < c(0) and I(E;T^{b2}) < kappa with
   their measured 5.5x / 0.19-bit margins and (ii) reproduction bands
   5e-3 / 2e-2 wide, i.e. five-to-six orders above the solver-endpoint
   spread.  No gate here is set at certificate-width scale.

s6 CONSTANTS + THE PLATEAU ARITHMETIC (exact, no optimizer):
   I_n = I(S^{b1}; S'^{1..Delta+1}) monotone increasing in n and
   converged to I_32 by n = 16; c(Delta;n) = (2 - 1{Delta=0}) kappa
   - I_n; c(0) = 0.4202858, c(1) = 1.1257294 (the recorded 1.1257 is
   FALSE in the 5th decimal -- gated), c(2) = 1.1218626; the corollary
   arithmetic LB(32,0) - c(0)/32 > causal-spectral, AND the n=24 base
   FAILING.  LB(32,0) is the SEALED 079 value, reproduced from
   results/GO14-convexity.json.

s7 ANCHORS + LADDER REPRODUCTION (not re-certification).  Full-space
   phi_4/phi_8/phi_12 reproduce the recorded anchors; the Fekete
   inequality 12 phi_12 <= 8 phi_8 + 4 phi_4 (slack ~6e-2); the
   strict-decrease chain phi_8 > phi_16 > phi_24 > phi_32 (EXACT
   superadditivity refuted); and the 9 diag-class ladder cells
   (24/32/48 x 4/5/6) + 3 block cells reproduce the recorded raw class
   values.  ROUTE TAKEN (disclosed): the winner parameters are NOT in
   the repo, so the ladder is RECOMPUTED with the bounded section
   optimizer and gated at 1e-5 -- ~10x the observed prover-vs-verifier
   endpoint spread (1.1e-6 at the loosest cell, (48,6)), not at
   certificate-width scale.

Sentinel ===GO14TR-JSON=== with ===END===; flag GO14TR_supported.
Pilot seed 20261130 / governed seed 20261131.  SEED STAMPS ONLY: the
seed is recorded in the output and feeds NO computation -- every random
draw uses an internally pinned generator (20260806) and every optimizer
is a deterministic cold start, so pilot and governed verify identical
numbers.

Evaluator lineage: all mutual informations / conditional variances go
through an INDEPENDENT slogdet route on explicit 4n joint covariances
(the R-IND-5 transfer verifier's evaluator), never through the
optimizer's cho_solve pivot route; the prover's f_and_grad/certify
machinery (experiments/go14_convexity.py lineage) is used ONLY to
produce points, and every reported endpoint is re-valued independently.

All floating-point certificates: no interval arithmetic.

PILOT RECORD (seed 20261130, two iterations, both disclosed):
 iter 1 -- 21/23.  Two FAILs, both in the harness, neither a bar
   change: (a) rec_of() halved the recovered noise covariance twice, so
   the s5 optimizer record was not the certified winner (its L_a read
   0.8767 against the certified 0.5667582); fixed, after which the
   record-space evaluator agrees with the moment-form optimum to
   3e-15.  (b) The first s4 counterexamples (scalar base + copy rows)
   were too weak to carry the refutation -- D2 = 0.3651 against the
   sharpened constant 0.4202858, and 6.62 bits against the 10-bit bar.
   The BARS WERE NOT MOVED: the constructions were strengthened
   (block-2 rows made informative, which is what the deficit measures)
   until the refutation carried at the constants that were already
   written down.
 iter 2 -- ALL PASS 23/23, runtime 347 s.  Reproduced bit-identically
   on a third run (D2 at m=8 agrees to the last digit), confirming the
   seed-stamp-only discipline.
"""
import argparse
import json
import os
import sys
import time

import numpy as np
from numpy.linalg import slogdet
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261130 if a_.pilot
                                            else 20261131)
rngi = np.random.default_rng(20260806)   # pinned: draws identical
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
D_TGT = 0.3
LN2 = np.log(2.0)
KAPPA = 0.5 * np.log2(1.0 / (1.0 - A_ ** 2))     # 0.7369655941662063

# ---- committed / sealed reference values (every one is reproduced) ----
HERE = os.path.dirname(os.path.abspath(__file__))
CXJSON = os.path.join(HERE, os.pardir, "results", "GO14-convexity.json")
SEALED_LB32 = 0.5647327868912777     # 079 governed s5_32_0 LB
SEALED_UB32 = 0.5647419676540331     # 079 governed s5_32_0 UB
SEALED_W32 = 9.180762755356398e-06   # 079 governed s5_32_0 width
SEALED_LB24 = 0.5654101216393774     # 079 governed s5_24_0 LB
TEXW32 = 1.7e-5                      # tex v0.4 anchor-table width (32,0)
SPEC0 = 0.5479448                    # causal-spectral allocation, Delta=0
PHI = {8: 0.5707933841926708, 12: 0.5681028133859690,   # transfer anchors
       4: 0.5788743565395545}
PHI_SEALED = {16: 0.5667581350, 24: 0.5654138570, 32: 0.5647418676}
# R-IND-5-confirmed raw diag-class ladder values (078 lineage)
RECORDED_LADDER = {(24, 4): 0.5333164330178152, (24, 5): 0.5332971559430583,
                   (24, 6): 0.5332947270100958, (32, 4): 0.5324812757915258,
                   (32, 5): 0.5324610143191735, (32, 6): 0.5324584245311400,
                   (48, 4): 0.5316462526061340, (48, 5): 0.5316250208213668,
                   (48, 6): 0.5316222729803203}
RECORDED_BLOCK = {24: 0.5332943959711205, 32: 0.5324580707712684,
                  48: 0.5316218852854745}
# R-IND-5 transfer-verifier recorded values (s3/s4/s5 reproduction bars)
REC_UCOUNTER = {"b1rows": 0.22226321262695733, "b2rows": 0.09497890251221086}
REC_D2 = {8: 0.076971, 16: 0.076926}
REC_IET = {8: 0.543069, 16: 0.543057}


# ===================== model + independent evaluator =====================
def cov_model(n):
    i = np.arange(n)
    Cv = A_ ** np.abs(i[:, None] - i[None, :])
    Cy = RHO ** 2 * Cv + SN2 * np.eye(n)
    Cvy = RHO * Cv
    Cs = Cv + TAU2 * np.eye(n)
    return Cv, Cy, Cvy, Cs


def joint_cov(n, Av, Ay, Nc, Au=None):
    """4n x 4n covariance, order V(0:n) Y(n:2n) S(2n:3n) Yh(3n:4n).
    Yh = Av V + Ay Y + Au U + Z, S = V + U, Cov(Z) = Nc, Z indep."""
    Cv, Cy, Cvy, Cs = cov_model(n)
    if Au is None:
        Au = np.zeros((n, n))
    CyhV = Av @ Cv + Ay @ Cvy
    CyhY = Av @ Cvy + Ay @ Cy
    CyhS = Av @ Cv + Ay @ Cvy + TAU2 * Au
    CyhYh = (Av @ Cv @ Av.T + Ay @ Cy @ Ay.T + Av @ Cvy @ Ay.T
             + Ay @ Cvy @ Av.T + TAU2 * Au @ Au.T + Nc)
    Z = np.zeros((4 * n, 4 * n))
    for (i, j), B in {(0, 0): Cv, (0, 1): Cvy, (0, 2): Cv, (0, 3): CyhV.T,
                      (1, 1): Cy, (1, 2): Cvy, (1, 3): CyhY.T,
                      (2, 2): Cs, (2, 3): CyhS.T, (3, 3): CyhYh}.items():
        Z[i * n:(i + 1) * n, j * n:(j + 1) * n] = B
    Z = np.triu(Z)
    return Z + Z.T - np.diag(np.diag(Z))


def ld(S, idx):
    idx = list(idx)
    if not idx:
        return 0.0
    s, v = slogdet(S[np.ix_(idx, idx)])
    if s <= 0:
        raise np.linalg.LinAlgError("nonpositive determinant")
    return v


def cmi_bits(S, A, B, C):
    """I(A;B|C) in bits, independent slogdet route."""
    A, B, C = list(A), list(B), list(C)
    return 0.5 * (ld(S, A + C) + ld(S, B + C) - ld(S, C)
                  - ld(S, A + B + C)) / LN2


def cvar_ld(S, i, cond):
    """Var(x_i | x_cond) via slogdet ratio (independent route)."""
    cond = list(cond)
    return float(np.exp(ld(S, cond + [i]) - ld(S, cond)))


def sched_prefix(n, Delta):
    return np.minimum(np.arange(n) + Delta + 1, n)


def prefC(n, t, Delta):
    """big-window staircase conditioning set of cell t (4n indices)."""
    se = min(t + Delta + 1, n)
    return list(range(2 * n, 2 * n + se)) + list(range(3 * n, 3 * n + t))


def blocks_idx(n, m):
    b1 = list(range(0, m)) + list(range(n, n + m))
    b2 = list(range(m, n)) + list(range(n + m, 2 * n))
    E = list(range(2 * n, 2 * n + m)) + list(range(3 * n, 3 * n + m))
    return b1, b2, E


def dist_of(n, Av, Ay, Nc, Au=None):
    Cv, Cy, Cvy, Cs = cov_model(n)
    CyhY = Av @ Cvy + Ay @ Cy
    CyhYh = (Av @ Cv @ Av.T + Ay @ Cy @ Ay.T + Av @ Cvy @ Ay.T
             + Ay @ Cvy @ Av.T + Nc)
    if Au is not None:
        CyhYh = CyhYh + TAU2 * Au @ Au.T
    per = np.diag(Cy) - 2 * np.diag(CyhY) + np.diag(CyhYh)
    return float(per.mean()), per


def la_bits(n, Av, Ay, Nc, Delta, Au=None):
    S4 = joint_cov(n, Av, Ay, Nc, Au)
    T = list(range(2 * n))
    return float(sum(cmi_bits(S4, T, [3 * n + t], prefC(n, t, Delta))
                     for t in range(n)) / n)


def deficits(S4, n, m, Delta):
    """per-side boundary charges D1, D2 at the split n = m + (n-m)."""
    m2 = n - m
    b1, b2, E = blocks_idx(n, m)
    T = list(range(2 * n))
    D2 = 0.0
    mid_le_big = True
    for t2 in range(m2):
        t = m + t2
        se = min(t2 + Delta + 1, m2)
        ownC = (list(range(2 * n + m, 2 * n + m + se))
                + list(range(3 * n + m, 3 * n + m + t2)))
        bigC = prefC(n, t, Delta)
        own = cmi_bits(S4, b2, [3 * n + t], ownC)
        mid = cmi_bits(S4, b2, [3 * n + t], bigC)
        big = cmi_bits(S4, T, [3 * n + t], bigC)
        D2 += own - mid
        if big < mid - 1e-11:
            mid_le_big = False
    D1 = 0.0
    for t in range(m):
        se1 = min(t + Delta + 1, m)
        ownC = (list(range(2 * n, 2 * n + se1))
                + list(range(3 * n, 3 * n + t)))
        D1 += (cmi_bits(S4, b1, [3 * n + t], ownC)
               - cmi_bits(S4, b1, [3 * n + t], prefC(n, t, Delta)))
    return D1, D2, mid_le_big


def zero_claim(S4, n, m, Delta):
    """max_j |I(E; S'_j | pfx_j, T^{b2})| -- F0-only."""
    m2 = n - m
    _, b2, E = blocks_idx(n, m)
    worst = 0.0
    for j in range(1, m2 + 1):
        kj = sum(1 for u in range(m2) if min(u + Delta + 1, m2) < j)
        pfx = (list(range(2 * n + m, 2 * n + m + j - 1))
               + list(range(3 * n + m, 3 * n + m + kj)))
        worst = max(worst, abs(cmi_bits(S4, E, [2 * n + m + j - 1],
                                        pfx + b2)))
    return worst


def imi_SS(m, Delta):
    """exact I(S_{1..m}; S_{m+1..m+Delta+1}) in bits, stationary window."""
    n = m + Delta + 1
    _, _, _, Cs = cov_model(n)
    return cmi_bits(Cs, range(m), range(m, n), [])


# ===================== optimizer machinery (points only) =================
class Model:
    def __init__(self, n):
        self.n = n
        Cv, Cy, Cvy, Cs = cov_model(n)
        self.Cv, self.Cy, self.Cs = Cv, Cy, Cs
        self.SigW = np.block([[Cv, Cvy], [Cvy, Cy]])
        self.SigWinv = np.linalg.inv(self.SigW)
        self.CovWS = np.vstack([Cv, Cvy])
        self.CovWY = np.vstack([Cvy, Cy])
        self.P = self.SigWinv
        self.Q = (self.SigWinv @ self.CovWS
                  @ np.linalg.solve(Cs, self.CovWS.T) @ self.SigWinv)
        self.K = self.CovWS.T @ self.SigWinv
        self.GY = self.SigWinv @ self.CovWY
        self.trCy = float(np.trace(Cy))
        self.lnpivS = 2.0 * np.log(np.diag(np.linalg.cholesky(Cs)))
        self.ev, self.Uv = np.linalg.eigh(Cv)
        self.lam = RHO ** 2 * self.ev + SN2
        self.emax = float(self.ev.max())
        self.lmax = float(self.lam.max())


def kcounts(n, se0):
    return np.array([int(np.sum(se0 <= j)) for j in range(n)])


def moments(M, Ay, Av, Ncov):
    Ablk = np.hstack([Av, Ay])
    H = Ablk @ M.SigW
    Gam = Ablk @ M.SigW @ Ablk.T + Ncov
    return H, 0.5 * (Gam + Gam.T)


def rec_of(M, H, G):
    """(H, Gamma) -> (Ay, Av, Ncov), PSD-clipped noise."""
    n = M.n
    Ablk = H @ M.SigWinv
    Av, Ay = Ablk[:, :n], Ablk[:, n:]
    Nc = G - H @ M.P @ H.T
    w, Qe = np.linalg.eigh(0.5 * (Nc + Nc.T))
    return Ay, Av, (Qe * np.maximum(w, 1e-12)) @ Qe.T


def dist_HG(M, H, Gam):
    return (M.trCy - 2.0 * float(np.sum(H * M.GY.T))
            + float(np.trace(Gam))) / M.n


def grad_dist(M):
    return -(2.0 / M.n) * M.GY.T, np.eye(M.n) / M.n


def f_and_grad(M, H, Gam, Delta):
    """per-symbol value (bits) + analytic gradient (prover derivation,
    experiments/go14_convexity.py lineage) -- used to PRODUCE points."""
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
    J = np.block([[M.Cs, M.K @ H.T], [(M.K @ H.T).T, Gam]])
    GJ = np.zeros((2 * n, 2 * n))
    for j in range(n):
        cond = list(range(j)) + [n + i for i in range(ks[j])]
        try:
            if cond:
                cf = cho_factor(J[np.ix_(cond, cond)], lower=True,
                                check_finite=False)
                b = J[cond, j]
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


def certify(n, Delta, maxit1=1500, maxit2=300, nbis=40):
    """full-space point + (ungated) two-sided bracket, cold start."""
    M = Model(n)
    gDH, gDG = grad_dist(M)
    iu = np.triu_indices(n)
    symw = np.where(iu[0] == iu[1], 1.0, 2.0)

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
    x = np.concatenate([H0.ravel(), G0[iu]])
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
    H_, G_ = unpack(x)
    bG = (1.0 + np.sqrt(n * D_TGT)) ** 2
    Rbox = float(np.sqrt(np.sum((np.sqrt(bG) + np.abs(H_)) ** 2)
                         + np.sum((bG + np.abs(G_)) ** 2)))
    LB = (v_ + mu * (d_ - D_TGT)) - rn * Rbox
    if d_ > D_TGT:                       # feasible projection of the UB
        Hid, Gid = moments(M, np.eye(n), np.zeros((n, n)),
                           1e-6 * np.eye(n))
        d0 = dist_HG(M, Hid, Gid)
        tt = (D_TGT - d0) / (d_ - d0)
        H_, G_ = Hid + tt * (H_ - Hid), Gid + tt * (G_ - Gid)
        UB = f_and_grad(M, H_, G_, Delta)[0]
    else:
        UB = v_
    return {"LB": LB, "UB": UB, "width": UB - LB, "rnorm": rn, "mu": mu,
            "dist_minus_D": d_ - D_TGT, "H": H_, "G": G_, "M": M}


def sec_to_HG(M, x):
    n = M.n
    al, be, ga = x[:n], x[n:2 * n], x[2 * n:]
    Hv = (M.Uv * al) @ M.Uv.T
    Hy = (M.Uv * be) @ M.Uv.T
    G = (M.Uv * ga) @ M.Uv.T
    return np.hstack([Hv, Hy]), 0.5 * (G + G.T)


def proj_sec(M, gH, gG):
    n = M.n
    return np.concatenate([
        np.einsum('ti,ts,si->i', M.Uv, gH[:, :n], M.Uv),
        np.einsum('ti,ts,si->i', M.Uv, gH[:, n:], M.Uv),
        np.einsum('ti,ts,si->i', M.Uv, gG, M.Uv)])


def certify_sec(n, Delta, maxit1=1500, maxit2=300, nbis=40):
    """diag-class (stationary-symmetric) SECTION point + bracket.
    The section is a convex LINEAR section of (H, Gamma) (R-IND-5
    restatement 3), so the same Lagrangian machinery applies inside it;
    here only the VALUE is used (ladder reproduction, s7)."""
    M = Model(n)
    gDH, gDG = grad_dist(M)
    gD_sec = proj_sec(M, gDH, gDG)

    def fval(x):
        H, G = sec_to_HG(M, x)
        return f_and_grad(M, H, G, Delta)

    def solve(mu, x0, maxiter):
        def lagr(x):
            out = fval(x)
            if out is None:
                return 1e3, np.zeros_like(x)
            v, gh, gg = out
            H, G = sec_to_HG(M, x)
            return (v + mu * (dist_HG(M, H, G) - D_TGT),
                    proj_sec(M, gh, gg) + mu * gD_sec)
        res = minimize(lagr, x0, jac=True, method="L-BFGS-B",
                       options={"maxiter": maxiter, "ftol": 1e-18,
                                "gtol": 1e-15, "maxcor": 60})
        x = res.x
        v, gh, gg = fval(x)
        H, G = sec_to_HG(M, x)
        return (x, v, dist_HG(M, H, G),
                proj_sec(M, gh, gg) + mu * gD_sec)

    g0 = 1.0 - D_TGT
    z0 = D_TGT * (1.0 - D_TGT)
    x = np.concatenate([RHO * g0 * M.ev, g0 * M.lam,
                        g0 ** 2 * M.lam + z0])
    lo, hi = 0.0, 4.0
    x, v_, d_, gr_ = solve(hi, x, maxit1)
    while d_ > D_TGT:
        hi *= 2.0
        x, v_, d_, gr_ = solve(hi, x, maxit2)
    mu = hi
    for _ in range(nbis):
        mu = 0.5 * (lo + hi)
        x, v_, d_, gr_ = solve(mu, x, maxit2)
        if d_ > D_TGT:
            lo = mu
        else:
            hi = mu
        if abs(d_ - D_TGT) < 1e-12:
            break
    x, v_, d_, gr_ = solve(mu, x, maxit1)
    rn = float(np.linalg.norm(gr_))
    Gcap = n * (1.0 + np.sqrt(D_TGT)) ** 2
    Rbox = float(np.sqrt((M.emax + M.lmax) * Gcap + Gcap ** 2)
                 + np.linalg.norm(x))
    LB = (v_ + mu * (d_ - D_TGT)) - rn * Rbox
    if d_ > D_TGT:
        xid = np.concatenate([RHO * M.ev, M.lam, M.lam + 1e-6])
        Hi, Gi = sec_to_HG(M, xid)
        d0 = dist_HG(M, Hi, Gi)
        tt = (D_TGT - d0) / (d_ - d0)
        x = xid + tt * (x - xid)
        UB = fval(x)[0]
        d_ = dist_HG(M, *sec_to_HG(M, x))
    else:
        UB = v_
    return {"LB": LB, "UB": UB, "width": UB - LB, "rnorm": rn, "mu": mu,
            "dist_minus_D": d_ - D_TGT}


# ===================== pinned record samplers ===========================
def rand_rec(n, rng, style):
    if style == 0:
        Ay = 0.7 * np.eye(n) + 0.15 * rng.normal(size=(n, n)) / np.sqrt(n)
        Av = 0.15 * rng.normal(size=(n, n)) / np.sqrt(n)
        B = 0.3 * rng.normal(size=(n, n)) / np.sqrt(n)
        Nc = B @ B.T + 0.10 * np.eye(n)
    elif style == 1:
        Ay = 0.5 * np.eye(n) + 0.35 * rng.normal(size=(n, n)) / np.sqrt(n)
        Av = 0.35 * rng.normal(size=(n, n)) / np.sqrt(n)
        B = 0.5 * rng.normal(size=(n, n)) / np.sqrt(n)
        Nc = B @ B.T + 0.05 * np.eye(n)
    else:
        Ay = 0.85 * np.eye(n) + 0.05 * rng.normal(size=(n, n)) / np.sqrt(n)
        Av = 0.20 * rng.normal(size=(n, n)) / np.sqrt(n)
        B = 0.15 * rng.normal(size=(n, n)) / np.sqrt(n)
        Nc = B @ B.T + 0.02 * np.eye(n)
    return Ay, Av, Nc


def blkdiag(A, B):
    n1, n2 = A.shape[0], B.shape[0]
    O = np.zeros((n1 + n2, n1 + n2))
    O[:n1, :n1] = A
    O[n1:, n1:] = B
    return O


# ------------------------------------------------------ s1 subadditivity
print("[s1] Theorem T(i): block-concatenation subadditivity, per-term "
      "+ block-local denominators ...", flush=True)
BAR_S1_PT = 1e-12          # per-term violation tolerance
BAR_S1_DEN = 1e-12         # block-local denominator relative deviation
s1_cells = 0
s1_viol = 0
s1_worst_pt = -1e9         # max (big - own)
s1_den = 0.0
s1_tot_ok = True
s1_min_slack = 1e9
s1_rows = []
for (n1, n2) in ((8, 8), (8, 4)):
    n = n1 + n2
    for style in (0, 1, 2):
        R1 = rand_rec(n1, rngi, style)
        R2 = rand_rec(n2, rngi, (style + 1) % 3)
        AyC = blkdiag(R1[0], R2[0])
        AvC = blkdiag(R1[1], R2[1])
        NcC = blkdiag(R1[2], R2[2])
        S4 = joint_cov(n, AvC, AyC, NcC)
        S1 = joint_cov(n1, R1[1], R1[0], R1[2])
        S2 = joint_cov(n2, R2[1], R2[0], R2[2])
        for Delta in (0, 2):
            big, own = [], []
            for t in range(n):
                big.append(cmi_bits(S4, range(2 * n), [3 * n + t],
                                    prefC(n, t, Delta)))
            for t in range(n1):
                own.append(cmi_bits(S1, range(2 * n1), [3 * n1 + t],
                                    prefC(n1, t, Delta)))
            for t in range(n2):
                own.append(cmi_bits(S2, range(2 * n2), [3 * n2 + t],
                                    prefC(n2, t, Delta)))
            big = np.array(big)
            own = np.array(own)
            d = big - own
            s1_worst_pt = max(s1_worst_pt, float(d.max()))
            s1_viol += int(np.sum(d > BAR_S1_PT))
            s1_cells += n
            slack = float(own.sum() - big.sum())
            s1_min_slack = min(s1_min_slack, slack)
            s1_tot_ok = s1_tot_ok and (big.sum() <= own.sum() + 1e-12)
            # block-local denominators: Var(Yh_t | T^n, cond)
            #                         = Var(Yh_t | T^{b(t)}, cond)
            for t in range(n):
                cond = prefC(n, t, Delta)
                vfull = cvar_ld(S4, 3 * n + t, list(range(2 * n)) + cond)
                blk = (list(range(0, n1)) + list(range(n, n + n1))
                       if t < n1 else
                       list(range(n1, n)) + list(range(n + n1, 2 * n)))
                vblk = cvar_ld(S4, 3 * n + t, blk + cond)
                s1_den = max(s1_den, abs(vfull - vblk) / vfull)
            s1_rows.append({"n1": n1, "n2": n2, "style": style,
                            "Delta": Delta, "tot_big": float(big.sum()),
                            "tot_own": float(own.sum()), "slack": slack})
vals["s1_cells"] = s1_cells
vals["s1_violations"] = s1_viol
vals["s1_worst_big_minus_own"] = s1_worst_pt
vals["s1_denom_rel_dev"] = s1_den
vals["s1_min_total_slack"] = s1_min_slack
vals["s1_bars"] = {"per_term": BAR_S1_PT, "denom": BAR_S1_DEN}
vals["s1_rows"] = s1_rows
verdicts["s1_subadd_per_term"] = (s1_viol == 0)
verdicts["s1_denom_block_local"] = (s1_den < BAR_S1_DEN)
verdicts["s1_subadd_totals"] = bool(s1_tot_ok)
print(f"  {s1_cells} cells over (8,8)/(8,4) x Delta in {{0,2}} x 3 pinned "
      f"record pairs: violations {s1_viol}, worst (big - own) "
      f"{s1_worst_pt:+.2e} <= {BAR_S1_PT:.0e}", flush=True)
print(f"  block-local denominator max rel dev {s1_den:.2e} < "
      f"{BAR_S1_DEN:.0e}; min total slack (sum own - sum big) "
      f"{s1_min_slack:+.3e} > 0 [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------- s2 set identity
print("[s2] interleaved-prefix set identity bigC_t = ownC_t U E + the "
      "total-order realization ...", flush=True)
set_fails = []
order_fails = []
s2_cells = 0
for m in (3, 5, 8):
    n = 2 * m
    for Delta in (0, 1, 2, m - 1, m):
        _, _, E = blocks_idx(n, m)
        Eset = set(E)
        for t2 in range(m):
            t = m + t2
            se_own = min(t2 + Delta + 1, m)
            own = (set(range(2 * n + m, 2 * n + m + se_own))
                   | set(range(3 * n + m, 3 * n + m + t2)))
            if set(prefC(n, t, Delta)) != own | Eset:
                set_fails.append(("b2", m, Delta, t2))
            s2_cells += 1
        for t in range(m):
            big = set(prefC(n, t, Delta))
            se_own = min(t + Delta + 1, m)
            own = (set(range(2 * n, 2 * n + se_own))
                   | set(range(3 * n, 3 * n + t)))
            se_big = min(t + Delta + 1, n)
            want = (set(range(2 * n + m, 2 * n + se_big))
                    if se_big > m else set())
            if (big - own) != want:
                set_fails.append(("b1", m, Delta, t))
            if Delta == 0 and (big - own):
                set_fails.append(("b1-Delta0-nonempty", m, Delta, t))
            s2_cells += 1
        # one linear order realizing ownC_t AND pfx_j with k(j)
        items = [(j, 0, j) for j in range(1, m + 1)]
        items += [(min(t2 + Delta + 1, m), 1, t2) for t2 in range(m)]
        order = sorted(items)
        pos = {(("S" if it[1] == 0 else "Y"), it[2]): k
               for k, it in enumerate(order)}
        for t2 in range(m):
            se = min(t2 + Delta + 1, m)
            pred = {k for k in pos if pos[k] < pos[("Y", t2)]}
            want = ({("S", j) for j in range(1, se + 1)}
                    | {("Y", u) for u in range(t2)})
            if pred != want:
                order_fails.append(("Y", m, Delta, t2))
        for j in range(1, m + 1):
            kj = sum(1 for t2 in range(m) if min(t2 + Delta + 1, m) < j)
            pred = {k for k in pos if pos[k] < pos[("S", j)]}
            want = ({("S", i) for i in range(1, j)}
                    | {("Y", u) for u in range(kj)})
            if pred != want:
                order_fails.append(("S", m, Delta, j))
            if kj != max(0, min(j - Delta - 1, m - Delta - 1)):
                order_fails.append(("kcount", m, Delta, j))
vals["s2_cells"] = s2_cells
vals["s2_set_failures"] = len(set_fails)
vals["s2_order_failures"] = len(order_fails)
verdicts["s2_set_identity"] = (len(set_fails) == 0)
verdicts["s2_interleaved_order"] = (len(order_fails) == 0)
print(f"  {s2_cells} cells, m in {{3,5,8}} x Delta in {{0,1,2,m-1,m}}: "
      f"set-difference failures {len(set_fails)}, order/k(j) failures "
      f"{len(order_fails)} [{time.time()-t0:.0f}s]", flush=True)

# --------------------------------------- s3 zero-claim + F0-conditionality
print("[s3] zero-claim I(E;S'_j|pfx_j,T^b2) = 0 (F0-ONLY) + the "
      "U-coupled counter-values ...", flush=True)
BAR_ZC = 1e-12
BAR_UCOUNTER = 0.05
BAR_UREPRO = 1e-6
n16, m8 = 16, 8


def r1_rec(scale, seed):
    """pinned F0 record family of the transfer verifier (n = 16)."""
    r = np.random.default_rng(seed)
    Av = scale * r.standard_normal((n16, n16)) / np.sqrt(n16)
    Ay = (0.7 * np.eye(n16)
          + scale * r.standard_normal((n16, n16)) / np.sqrt(n16))
    R = r.standard_normal((n16, n16)) / np.sqrt(n16)
    return Av, Ay, 0.15 * (R @ R.T) + 0.05 * np.eye(n16)


zc_worst = 0.0
for s in range(12):
    Av, Ay, Nc = r1_rec(0.6 if s % 2 else 0.2, 100 + s)
    S4 = joint_cov(n16, Av, Ay, Nc)
    for Delta in (0, 2):
        zc_worst = max(zc_worst, zero_claim(S4, n16, m8, Delta))
vals["s3_zeroclaim_F0_max"] = zc_worst
vals["s3_records"] = 12
verdicts["s3_zeroclaim_F0"] = zc_worst < BAR_ZC
# U-coupled counterexamples (pinned draws, verifier-identical order)
rngU = np.random.default_rng(20260806)
ucnt = {}
for tag, rows in (("b1rows", range(0, m8)), ("b2rows", range(m8, n16))):
    Av, Ay, Nc = r1_rec(0.3, 55)
    Au = np.zeros((n16, n16))
    for t in rows:
        Au[t, m8:] = 0.5 * rngU.standard_normal(m8) / np.sqrt(m8)
    S4 = joint_cov(n16, Av, Ay, Nc, Au)
    ucnt[tag] = {str(d): zero_claim(S4, n16, m8, d) for d in (0, 2)}
vals["s3_ucoupled"] = ucnt
u_b1 = ucnt["b1rows"]["0"]
u_b2 = ucnt["b2rows"]["0"]
vals["s3_urepro_err"] = {"b1rows": abs(u_b1 - REC_UCOUNTER["b1rows"]),
                         "b2rows": abs(u_b2 - REC_UCOUNTER["b2rows"])}
vals["s3_bars"] = {"zeroclaim": BAR_ZC, "ucounter": BAR_UCOUNTER,
                   "urepro": BAR_UREPRO}
verdicts["s3_family_conditionality"] = (u_b1 > BAR_UCOUNTER
                                        and u_b2 > BAR_UCOUNTER)
verdicts["s3_ucounter_reproduction"] = (
    abs(u_b1 - REC_UCOUNTER["b1rows"]) < BAR_UREPRO
    and abs(u_b2 - REC_UCOUNTER["b2rows"]) < BAR_UREPRO)
print(f"  12 pinned F0 records x Delta in {{0,2}} x all j: max "
      f"|I(E;S'_j|pfx_j,T^b2)| = {zc_worst:.2e} < {BAR_ZC:.0e}",
      flush=True)
print(f"  U-coupled: block-1 rows -> U^b2 gives {u_b1:.4f} bits "
      f"(recorded 0.2223), block-2-ONLY coupling gives {u_b2:.4f} bits "
      f"(recorded 0.0950) -- both > {BAR_UCOUNTER}: the zero-claim and "
      f"the marginalization step are F0-ONLY [{time.time()-t0:.0f}s]",
      flush=True)

# ---------------------------------------------------- s4 (H*) refutation
print("[s4] the (H*) REFUTATION netted: 'D_i <= kappa per side' is FALSE "
      "as an F0 lemma ...", flush=True)
I8 = imi_SS(m8, 0)
C0_SHARP = KAPPA - I8            # sharpened per-side constant at m = 8


def adv_record(n, m, bcoef, varz, eps1, copies, kind):
    """PINNED, analytic, D-feasible F0 counterexample.  No optimizer
    anywhere: block-2 rows are Yh_t = Y_t + bcoef V_t + Z_t (distortion
    bcoef^2 + varz per cell), block-1 non-copy rows are near-exact
    own-cell records (distortion eps1), and the listed block-1 rows are
    replaced by (near-)exact copies of block-2 V- or Y-cells.
    DISCLOSED: the R-IND-5 transfer verifier's own counterexample
    records are not in the repository; these are independent
    re-derivations of the same counterexample CLASS (block-1 rows spent
    on copies of block-2 cells), and the measured charges are reported
    against the recorded ones rather than asserted equal to them."""
    Ay = np.zeros((n, n))
    Av = np.zeros((n, n))
    Nc = np.zeros((n, n))
    for t in range(n):
        if t < m:
            Ay[t, t] = 1.0 - eps1
            Nc[t, t] = eps1 * (1.0 - eps1)
        else:
            Ay[t, t] = 1.0
            Av[t, t] = bcoef
            Nc[t, t] = varz
    for t, src in copies:
        Ay[t, :] = 0.0
        Av[t, :] = 0.0
        if kind == "V":
            Av[t, src] = 1.0
        else:
            Ay[t, src] = 1.0
        Nc[t, :] = 0.0
        Nc[:, t] = 0.0
        Nc[t, t] = 1e-6
    return Ay, Av, Nc


s4 = {}
# (a) two V-copy rows -- refutes the SHARPENED constant c(0) = kappa - I
AyA, AvA, NcA = adv_record(n16, m8, 0.50, 0.02, 0.001,
                           [(6, 9), (7, 8)], "V")
dA, _ = dist_of(n16, AvA, AyA, NcA)
S4A = joint_cov(n16, AvA, AyA, NcA)
D1A, D2A, _ = deficits(S4A, n16, m8, 0)
_, b2A, EA = blocks_idx(n16, m8)
iA = cmi_bits(S4A, EA, b2A, [])
s4["two_V_copies"] = {"dist": dA, "D1": D1A, "D2": D2A, "I_E_Tb2": iA,
                      "La": la_bits(n16, AvA, AyA, NcA, 0)}
# (b) three Y-copy rows -- refutes kappa itself (Theta(m) worst case)
AyB, AvB, NcB = adv_record(n16, m8, 0.0, 0.001, 0.001,
                           [(5, 10), (6, 9), (7, 8)], "Y")
dB, _ = dist_of(n16, AvB, AyB, NcB)
S4B = joint_cov(n16, AvB, AyB, NcB)
D1B, D2B, _ = deficits(S4B, n16, m8, 0)
iB = cmi_bits(S4B, EA, b2A, [])
s4["three_Y_copies"] = {"dist": dB, "D1": D1B, "D2": D2B, "I_E_Tb2": iB,
                        "La": la_bits(n16, AvB, AyB, NcB, 0)}
BAR_S4A = C0_SHARP
BAR_S4B = 10.0
vals["s4"] = s4
vals["s4_c0_sharp"] = C0_SHARP
vals["s4_recorded_reference"] = {"two_V_copies_D2": 0.4563,
                                 "three_Y_copies_D2": 18.93,
                                 "three_Y_copies_dist": 0.2986,
                                 "note": "R-IND-5 transfer-verifier "
                                         "records; not in-repo, so the "
                                         "harness re-derives the class"}
vals["s4_bars"] = {"two_V_copies_D2_gt": BAR_S4A,
                   "three_Y_copies_D2_gt": BAR_S4B,
                   "feasible_D": D_TGT + 1e-9}
verdicts["s4_counterexamples_feasible"] = (dA <= D_TGT + 1e-9
                                           and dB <= D_TGT + 1e-9)
verdicts["s4_sharp_constant_refuted"] = D2A > BAR_S4A
verdicts["s4_kappa_per_side_refuted"] = D2B > BAR_S4B
print(f"  kappa = {KAPPA:.6f}; I_8 = {I8:.6f}; sharpened c(0) = "
      f"kappa - I_8 = {C0_SHARP:.7f}", flush=True)
print(f"  (a) two V-copy rows: dist {dA:.6f} (FEASIBLE), D2 = {D2A:.4f} "
      f"> {C0_SHARP:.4f} -- the sharpened per-side constant is EXCEEDED "
      f"(I(E;T^b2) = {iA:.2f})", flush=True)
print(f"  (b) three Y-copy rows: dist {dB:.6f} (FEASIBLE), D2 = "
      f"{D2B:.2f} bits ~ {D2B/KAPPA:.0f} kappa > {BAR_S4B} -- "
      f"'<= kappa per side' is FALSE as an F0 lemma; worst case grows "
      f"with m, so NO universal constant exists [{time.time()-t0:.0f}s]",
      flush=True)

# ------------------------------------------- s5 optimizer verifications
print("[s5] (H*) verified AT OPTIMIZERS, m in {8,16} only ...",
      flush=True)
BAR_D2_BAND = 5e-3
BAR_IET_BAND = 2e-2
BAR_IET_HEAD = 0.10          # required headroom under kappa
s5 = {}
opt_ok = True
for (nn, mm) in ((16, 8), (32, 16)):
    c = certify(nn, 0)
    Ay, Av, Nc = rec_of(c["M"], c["H"], c["G"])
    la = la_bits(nn, Av, Ay, Nc, 0)
    S4 = joint_cov(nn, Av, Ay, Nc)
    D1, D2, mid_le_big = deficits(S4, nn, mm, 0)
    _, b2, E = blocks_idx(nn, mm)
    iET = cmi_bits(S4, E, b2, [])
    zc = zero_claim(S4, nn, mm, 0)
    d_, _ = dist_of(nn, Av, Ay, Nc)
    s5[f"m{mm}"] = {"n": nn, "La": la, "UB": c["UB"], "LB": c["LB"],
                    "rnorm": c["rnorm"], "dist": d_, "D1": D1, "D2": D2,
                    "I_E_Tb2": iET, "zero_claim": zc,
                    "mid_le_big": bool(mid_le_big),
                    "D2_err_vs_recorded": abs(D2 - REC_D2[mm]),
                    "I_err_vs_recorded": abs(iET - REC_IET[mm]),
                    "evaluator_gap_La_minus_UB": la - c["UB"]}
    ok = (D2 < C0_SHARP and iET < KAPPA - BAR_IET_HEAD
          and abs(D2 - REC_D2[mm]) < BAR_D2_BAND
          and abs(iET - REC_IET[mm]) < BAR_IET_BAND
          and mid_le_big and zc < 1e-11
          and abs(la - c["UB"]) < 1e-9)
    opt_ok = opt_ok and ok
    print(f"  m={mm} (n={nn} optimizer, La {la:.7f}): D1 = {D1:.6f}, "
          f"D2 = {D2:.6f} (recorded {REC_D2[mm]}, err "
          f"{abs(D2-REC_D2[mm]):.1e}) < c(0) = {C0_SHARP:.4f} "
          f"[{C0_SHARP/D2:.1f}x]", flush=True)
    print(f"        I(E;T^b2) = {iET:.6f} (recorded {REC_IET[mm]}, err "
          f"{abs(iET-REC_IET[mm]):.1e}), {KAPPA-iET:.3f} bits under "
          f"kappa; zero-claim {zc:.1e}; mid<=big {mid_le_big} "
          f"[{time.time()-t0:.0f}s]", flush=True)
vals["s5"] = s5
vals["s5_bars"] = {"D2_lt": C0_SHARP, "IET_lt": KAPPA - BAR_IET_HEAD,
                   "D2_band": BAR_D2_BAND, "IET_band": BAR_IET_BAND}
verdicts["s5_optimizer_Hstar"] = bool(opt_ok)

# ------------------------------------------------ s6 constants + plateau
print("[s6] constants c(Delta;n) = (2 - 1{Delta=0}) kappa - I_n and the "
      "plateau arithmetic ...", flush=True)
BAR_MONO = 1e-12
BAR_CONV = 1e-12
BAR_CONST = 1e-6
NS = (8, 12, 16, 24, 32)
Itab = {}
mono_ok = True
conv_ok = True
for Delta in (0, 1, 2):
    row = [imi_SS(nn, Delta) for nn in NS]
    Itab[str(Delta)] = row
    for i in range(len(row) - 1):
        if row[i + 1] < row[i] - BAR_MONO:
            mono_ok = False
    for i, nn in enumerate(NS):
        if nn >= 16 and abs(row[i] - row[-1]) > BAR_CONV:
            conv_ok = False
CS = {0: 0.4202858, 1: 1.1257294, 2: 1.1218626}
QUOTED = {0: 0.42029, 1: 1.1258, 2: 1.1219}
cvals = {}
const_ok = True
for Delta in (0, 1, 2):
    I32 = Itab[str(Delta)][-1]
    c = (2.0 - (1.0 if Delta == 0 else 0.0)) * KAPPA - I32
    cvals[str(Delta)] = c
    const_ok = const_ok and abs(c - CS[Delta]) < BAR_CONST
    const_ok = const_ok and c <= QUOTED[Delta]
# the 5th-decimal erratum: c(1) > 1.1257 (the recorded value was FALSE)
c1_erratum = cvals["1"] > 1.1257
vals["s6_I_table"] = {"n": list(NS), "I": Itab}
vals["s6_c"] = cvals
vals["s6_bars"] = {"mono": BAR_MONO, "converged": BAR_CONV,
                   "const": BAR_CONST}
verdicts["s6_In_monotone"] = bool(mono_ok)
verdicts["s6_In_converged_by16"] = bool(conv_ok)
verdicts["s6_constants"] = bool(const_ok and c1_erratum)
print("  I_n(Delta=0): " + " ".join(f"{v:.10f}" for v in Itab["0"])
      + f"  monotone-increasing (tol {BAR_MONO:.0e}): {mono_ok}",
      flush=True)
print(f"  c(0) = {cvals['0']:.7f} <= 0.42029; c(1) = {cvals['1']:.7f} "
      f"<= 1.1258 (and > 1.1257 -- the recorded 1.1257 is FALSE in the "
      f"5th decimal: {c1_erratum}); c(2) = {cvals['2']:.7f} <= 1.1219",
      flush=True)
# sealed LB(32,0) reproduction from the committed 079 result
file_lb32 = None
if os.path.exists(CXJSON):
    with open(CXJSON) as fh:
        file_lb32 = json.load(fh)["vals"]["s5_32_0"]["LB"]
vals["s6_sealed_LB32_file"] = file_lb32
verdicts["s6_sealed_LB32_reproduced"] = (
    file_lb32 is not None and abs(file_lb32 - SEALED_LB32) < 1e-12)
c0 = cvals["0"]
plateau32 = SEALED_LB32 - c0 / 32.0
plateau24 = SEALED_LB24 - c0 / 24.0
margin = plateau32 - SPEC0
short24 = SPEC0 - plateau24
vals["s6_plateau"] = {"LB32": SEALED_LB32, "c0": c0, "value": plateau32,
                      "spec": SPEC0, "margin": margin,
                      "x_texwidth": margin / TEXW32,
                      "x_sealedwidth": margin / SEALED_W32,
                      "UB32": SEALED_UB32}
vals["s6_base24"] = {"LB24": SEALED_LB24, "value": plateau24,
                     "shortfall": short24}
verdicts["s6_plateau_arithmetic"] = (
    abs(plateau32 - 0.5515989) < 1e-6 and margin > 3.0e-3
    and 210.0 < margin / TEXW32 < 220.0)
verdicts["s6_base24_fails"] = (plateau24 < SPEC0 and short24 > 1e-5)
print(f"  L^inf(0) >= LB(32,0) - c(0)/32 = {SEALED_LB32:.10f} - "
      f"{c0:.7f}/32 = {plateau32:.7f} > {SPEC0} (causal-spectral), "
      f"margin {margin:+.4e} = {margin/TEXW32:.0f}x the tex-v0.4 "
      f"bracket width ({margin/SEALED_W32:.0f}x the sealed width)",
      flush=True)
print(f"  base n=24: {SEALED_LB24:.10f} - {c0:.7f}/24 = {plateau24:.7f} "
      f"< {SPEC0} -- FAILS by {short24:.2e}: there is no constant slack "
      f"and (H*) is genuinely load-bearing [{time.time()-t0:.0f}s]",
      flush=True)

# ------------------------------------------- s7 anchors + ladder repro
print("[s7] anchors + within-class ladder REPRODUCTION ...", flush=True)
BAR_ANCHOR = 1e-5
BAR_LADDER = 1e-5
anch = {}
anch_ok = True
for nn in (4, 8, 12):
    c = certify(nn, 0)
    anch[str(nn)] = {"UB": c["UB"], "LB": c["LB"], "width": c["width"],
                     "recorded": PHI[nn], "err": abs(c["UB"] - PHI[nn])}
    anch_ok = anch_ok and abs(c["UB"] - PHI[nn]) < BAR_ANCHOR
    print(f"  phi_{nn}(0) = {c['UB']:.10f} (recorded {PHI[nn]:.10f}, err "
          f"{c['UB']-PHI[nn]:+.1e}) [{time.time()-t0:.0f}s]", flush=True)
p4, p8, p12 = (anch["4"]["UB"], anch["8"]["UB"], anch["12"]["UB"])
fekete = 8.0 * p8 + 4.0 * p4 - 12.0 * p12
chain = [p8, PHI_SEALED[16], PHI_SEALED[24], PHI_SEALED[32]]
gaps = [chain[i] - chain[i + 1] for i in range(3)]
vals["s7_anchors"] = anch
vals["s7_fekete_slack"] = fekete
vals["s7_chain"] = {"values": chain, "gaps": gaps}
vals["s7_bars"] = {"anchor": BAR_ANCHOR, "ladder": BAR_LADDER,
                   "fekete_slack_min": 1e-2, "chain_gap_min": 1e-4}
verdicts["s7_anchor_reproduction"] = bool(anch_ok)
verdicts["s7_fekete_subadditivity"] = fekete > 1e-2
verdicts["s7_strict_decrease"] = all(g > 1e-4 for g in gaps)
print(f"  Fekete check: 8 phi_8 + 4 phi_4 - 12 phi_12 = {fekete:+.4e} "
      f"> 1e-2 (subadditive at the certified anchors)", flush=True)
print(f"  strict-decrease chain phi_8 > phi_16 > phi_24 > phi_32: gaps "
      f"{gaps[0]:.2e}/{gaps[1]:.2e}/{gaps[2]:.2e} -- EXACT "
      f"superadditivity is REFUTED", flush=True)
lad = {}
lad_ok = True
for (nn, Delta) in [(24, 4), (24, 5), (24, 6), (32, 4), (32, 5), (32, 6),
                    (48, 4), (48, 5), (48, 6)]:
    c = certify_sec(nn, Delta)
    ref = RECORDED_LADDER[(nn, Delta)]
    lad[f"{nn}_{Delta}"] = {"value": c["UB"], "LB": c["LB"],
                            "width": c["width"], "recorded": ref,
                            "err": abs(c["UB"] - ref)}
    lad_ok = lad_ok and abs(c["UB"] - ref) < BAR_LADDER
    print(f"  diag-class ({nn},{Delta}): {c['UB']:.10f} (recorded "
          f"{ref:.10f}, err {c['UB']-ref:+.1e}) [{time.time()-t0:.0f}s]",
          flush=True)
blk = {}
blk_ok = True
for nn in (24, 32, 48):
    c = certify_sec(nn, nn)
    ref = RECORDED_BLOCK[nn]
    blk[str(nn)] = {"value": c["UB"], "LB": c["LB"], "recorded": ref,
                    "err": abs(c["UB"] - ref)}
    blk_ok = blk_ok and abs(c["UB"] - ref) < BAR_LADDER
    print(f"  block_{nn} (Delta = n): {c['UB']:.10f} (recorded "
          f"{ref:.10f}, err {c['UB']-ref:+.1e}) [{time.time()-t0:.0f}s]",
          flush=True)
vals["s7_ladder"] = lad
vals["s7_block"] = blk
verdicts["s7_ladder_reproduction"] = bool(lad_ok)
verdicts["s7_block_reproduction"] = bool(blk_ok)

# ---------------------------------------------------------------- report
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


out = {"verdict": verdicts, "GO14TR_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14TR-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
