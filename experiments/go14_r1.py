#!/usr/bin/env python
"""GO-14 (R1) harness (tex v0.8: (R1) promoted from a LEMMA to THEOREM R1 --
joint convexity of the process-rate functional on the cyclostationary class
K_n(eps, M), proved in four steps, with the Scoping Lemma).  Registration 083
pending -- NOTHING HERE IS SEALED.

Model: V AR(1) a = 0.8 unit variance; Y = 0.7 V + N, Var(Y) = 1; S = V + U,
tau2 = 0.4; D = 0.3; T = (V, Y) = W; family F0 (records jointly Gaussian with
(V, Y) and INDEPENDENT of U, i.e. A_u = 0).

WHAT THIS HARNESS IS FOR.  083 is registered SEPARATELY from the Psi
certificate (082): the two objects are structurally independent.  This file
nets the FOUR STEPS of Theorem R1 and its Scoping Lemma, plus the R21-R29
restatements of the R-IND-5 pass on (R1).  It nets NO value of Psi, NO margin
against any sealed bar, and NO identification of L^inf: the chain remains
ONE-DIRECTIONAL, L^inf(Delta) >= Psi(D; Delta), and "unconditional" attaches
to the CHAIN, never to the Psi value (which stays a two-sided certified
bracket under the floating-point house convention).

THEOREM R1 (what the sections below net).  Fix a period n, a lag Delta (indeed
any n-periodic nondecreasing schedule) and constants eps > 0, M < infinity.  On
the convex set K_n(eps, M) = {(h, Gamma) in L_n : Gamma <= M I,
n(w) = Gamma - h P h* >= eps I a.e.} the process-rate functional is finite and
JOINTLY CONVEX -- and K_n carries NO WINDOW LENGTH ANYWHERE.  Steps:
 (0) Collapse + shifted frame: Delta enters as a UNIMODULAR PHASE on h, a
     linear invertible change of coordinates;
 (1) BLOCKING by n makes (R_b, S_b) a stationary 2n-variate process, and the
     Cholesky of its one-step block innovation reproduces the process pivots;
 (2) MATRIX SZEGO (Wiener-Masani) -- the ONLY analytic input:
     2 ln2 n rate = [<lndet M_Q> - <lndet n>] + <lndet Phi_S> - sum_i ln s_i;
 (3a) the block leg is convex (matrix quadratic-over-linear composed with
     -lndet(I - .), using Q >= 0 to make M_Q Loewner-concave);
 (3b) the leak leg is convex because each s_i is an INF OF AFFINE functions of
     (H, Gamma) -- the load-bearing new step.
SCOPING LEMMA: step (B) is only ever applied to step-(A) periodizations with
independent noise copies, whose blocked noise spectrum is CONSTANT in w; the
shifts conjugate it by a block cyclic shift that is UNITARY on |z| = 1, so one
(eps, M) serves the whole orbit and its convex hull.  N > 0 is w.l.o.g.
(convex program + Slater).

DESIGN RULE (the 079 lesson, restated by 080/081/082).  NO GATE MAY RACE AN
OPTIMIZER STOPPING POINT AND NO GATE MAY GATE A CERTIFICATE WIDTH.  This file
is the easiest case in the campaign to satisfy: IT CONTAINS NO OPTIMIZER AT
ALL.  There is no L-BFGS-B, no Nelder-Mead, no fixed-point iteration and no
root find anywhere in it; every number is produced by a direct factorization
(Cholesky / LU / eigh) or by a spectrally accurate quadrature of an analytic
periodic integrand.  No bracket, no width and no certificate endpoint is read
or gated.  Every gate is one of
  (a) an exact identity with a tolerance many orders above f64 noise,
  (b) a structural / set fact (in-cone, out-of-cone, count of violations),
  (c) an analytic inequality with a fat measured margin, or
  (d) a MUST-FAIL control, gated on the side of failure.
The adversarial SEARCHES that the (R1) prover and the R-IND-5 verifier ran
(Nelder-Mead maximisation of the Jensen gap: prover best -2.39e-2 over 6 runs
x 3 restarts, verifier best -1.62e-6 over 24 runs x <=2500 evals, NEITHER ever
crossing) are recorded here as CONTEXT and are deliberately NOT reproduced:
a gate on a search's best value would race a stopping point.

s1 COLLAPSE + THE FRAME/ORDER PAIR (R21).  The Collapse identity is re-checked
   against the definitional CMI, and the moment-coordinate route against the
   record route.  Then the block-innovation sequence is read in BOTH frames
   WITH THEIR MATCHING ORDERS:
     FRAME-R (this document's): R_u := Yhat_{u-Delta-1}, order
              R_1, S_1, ..., R_n, S_n  -- this is the frame that produces the
              phase z^{Delta+1} and Lemma S's s = Var(S_u | S^{u-1}, R^u);
     FRAME-S (equally valid):  R_u := Yhat_{u-Delta},   order
              S_1, R_1, ..., S_n, R_n.
   Each is internally correct.  MIXING THEM IS THE ONE PLACE A SILENT WRONG
   THEOREM IS AVAILABLE, and the mixed pairing is gated as a MUST-FAIL
   control: it returns the lag-(Delta+1) rate EXACTLY (< 1e-12) and therefore
   differs from the lag-Delta rate by up to 7.6e-2 bits.  FRAME AND ORDER MUST
   BE PRINTED AS A PAIR.

s2 THE BLOCK-INNOVATION CHOLESKY (step 1).  With Lambda the one-step block
   innovation covariance of the blocked stationary 2n-variate process,
   sum_i ln sigma_i = lndet Lambda - sum_i ln s_i, in both frames, at
   n in {2,3,4,6} x Delta in {0,1,2}.  Gate: both legs to < 1e-11.

s3 THE MATRIX SZEGO STEP (step 2) -- THE ONLY ANALYTIC INPUT.  The blocked
   spectra are built by the EXACT ALIASING formula
   Phi(theta)[j,k] = (1/n) sum_{m<n} f((theta + 2 pi m)/n) e^{i(theta+2pi m)(j-k)/n}
   and the blocked transfer function of a tiled period-n record is read off
   EXACTLY (finite block support), so there is ZERO block-lag truncation and
   the only error is the theta-quadrature.  Gate the full decomposition to
   < 1e-12 at n in {1,2,3,4,6} x Delta in {0,1,2}.  R22 CONTROL: the eps floor
   is NOT a hypothesis of the Szego step -- on the extremal family
   f = |1 - c e^{-iw}|^2 the identity holds up to and INCLUDING c = 1, where
   the spectrum VANISHES at a frequency.  Also: the earlier n=2 anomaly is
   settled as BLOCK-LAG TRUNCATION of the chord evaluator, not a failure of
   the identity -- the DMAX sweep decays geometrically to 1.6e-13.

s4 INF OF AFFINE (step 3b, the load-bearing new step).  Per instance, three
   SEPARATE links: (L1) shat_w is exactly AFFINE in (H, Gamma) for a frozen
   causal predictor w (this is where A_u = 0 enters); (L2a) shat_w(mid) =
   s(mid) when w is the midpoint's own optimum; (L2b) shat_w >= s at both
   endpoints.  Hence s is an inf of affine, hence concave, hence -ln s convex.
   R23: (i) an inf of affine over ANY index set is concave -- no density, no
   continuity, no topology; (ii) the closure argument is needed ONLY to
   identify that inf with s, and truncating the family gives a DIFFERENT
   function that is still concave.  Both are gated separately.
   CONTROL: a predictor PEEKING two slots ahead is inadmissible and must
   BREAK the minorant -- gated on the side of failure.

s5 CONVEXITY (the conclusion), AND WHAT IT NEEDS.  Pinned Jensen chords in the
   moment coordinates over adversarial spectra (near-cone-boundary, deep
   notch, sign-alternating, near-deterministic, large-gain), n = 1..8,
   Delta = 0,1,2, plus second differences along lines: zero violations.
   TWO CONTROLS, both gated on the side of failure:
   (i) THE MOMENT CHART IS LOAD-BEARING -- in the RECORD-parameter chart
       (A_v, A_y, N) the same functional is NON-convex (negative second
       differences);
   (ii) THE LEMMA ALONE PROVES NOTHING -- the same inf-of-affine argument
       applies verbatim to sigma_t and to nu_t, so BOTH legs are concave; the
       rate is nevertheless NOT concave.  THE REGROUPING IS THE PROOF.

s6 THE SCOPING LEMMA.  (d1) a step-(A) periodization has blocked noise
   spectrum CONSTANT in w; (d2) its k-shift conjugates that spectrum by the
   block cyclic shift U_k, unitary on |z| = 1, so the eigenvalues are the same
   at every frequency and every k; (d3) one (eps, M) therefore serves the whole
   orbit AND its convex hull; (d4) N > 0 is w.l.o.g.
   R26 -- THE CONJUGATION HAS A SIDE AND A SIGN.  The correct statement is
   Phi^(k)(theta) = U_k(theta)* N U_k(theta) with the wrapped entries carrying
   e^{+i theta}.  Gate the correct combination exact AND at least one of the
   other three sign/side combinations failing by O(1).

s7 R24 AND R25.  R24: over a pinned battery of >= 22,000 chords across FOUR
   non-psd-Q families with R = P - Q psd there are ZERO Lemma-C-stat
   violations, while the R-breaking control (Q' = 1.3 P) violates.  So R >= 0
   is DEMONSTRATED NECESSARY; Q >= 0 is a hypothesis of the PROOF ROUTE (it is
   what makes M_Q Loewner-concave), not of the statement.
   R25: outside F0 the moment coordinates are not even WELL-POSED -- two
   records with IDENTICAL (H, Gamma) have rates differing by AT LEAST 0.136
   bits.  The entry point is the leak leg Cov(R, S) = H Sig_W^-1 Sig_WS.

s8 R29 -- THE STRENGTHENING.  At the BLOCKED SPECTRAL level
   lambda_min(R(w)) = 3.172e-3 UNIFORMLY in w and in n = 1..8, and
   Q(w) = blockdiag(Phi_S(w)^-1, 0) EXACTLY at every block size, with
   max eig Z < 1 strictly on the class interior.  This supplies the n-uniform
   floor the tex previously declined to claim, and explains the recorded
   finite-window decrease of eigmin(P - Q) as CONVERGENCE TO IT FROM ABOVE.

s9 SHIFT-INVARIANCE, AND THE np.roll BUG (R27).  With GENUINE shifts of the
   bi-infinite period-n record the rate is shift-invariant to machine
   precision.  CONTROL: np.roll of the window matrices is NOT a shift (Sigma_V
   is Toeplitz, not circulant); gated as a MOMENT-COORDINATE bug -- rolled
   (H, Gamma) pairs LEAVE THE CONE, while in RECORD coordinates the roll is
   wrong by only <= 1e-7, so pre-fix record-space numerics are neither over-
   nor under-condemned.

Sentinel ===GO14R1-JSON=== with ===END===; flag GO14R1_supported.
Pilot seed 20261160 / governed seed 20261161.  SEED STAMPS ONLY: the seed is
recorded in the output and feeds NO computation -- every random draw uses an
internally pinned generator, so pilot and governed verify identical numbers.

Evaluator lineage.  Every conditional variance is read off a joint covariance
built by pushing the INDEPENDENT PRIMITIVES (V, N, U, Z) through an explicit
linear map, so no identity under test is assumed anywhere.  The spectral
sections build their own blocked spectra by exact aliasing and their own
blocked transfer functions by exact finite-support reads.

PILOT RECORD (seed 20261160, 2026-08-07).
 iter 1 -- 43/44, 31 s.  ONE control was UNDER-SAMPLED, not failing: the R24
   R-breaking control (Q' = 1.3 P) was run at 700 draws, of which only 73
   survived the psd screen (with R negative definite most draws leave the
   cone), giving 19 violations against a bar of 50.  The BAR WAS NOT MOVED;
   the control's draw count was raised to 6,000 -- the size the R-IND-5
   verifier used -- which keeps 673 and gives 198 violations.
 iter 2 -- 43/44, 33 s.  The R25 witness was FRAGILE, and this is the one
   substantive design change of the pilot.  The random A_u battery's worst
   spread sits at 0.12-0.15 bits depending on the draw, i.e. it straddles the
   0.136 the restatement asks to be printed; gating a claim on which side of
   0.136 a random draw lands would have been a seed lottery, and shopping for
   a seed that clears it would have been worse.  Replaced by a PINNED
   DETERMINISTIC LADDER with no randomness at all (A_v, A_y fixed analytic
   kernels; A_u = s I for s = 0, 0.2, ..., 1.2; Cov(Z) = 0.6 I - tau2 A_u A_u'
   so that (H, Gamma) is held EXACTLY fixed), which moves the rate by 1.635
   bits.  The random battery is still run and REPORTED, but the gates read the
   pinned ladder.  No bar was loosened: the 0.136 gate is unchanged and now
   clears by 12x instead of by a coin flip.
 iter 3 -- ALL PASS 44/44, 31.2 s (re-runs 37.0 / 38.8 s and, governed,
   33.4 s -- the payload is identical, only wall-clock moves).  A governed
   re-run (seed 20261161) reproduced the JSON payload BIT-IDENTICALLY,
   confirming the
   seed-stamp-only discipline.  Every bar was fixed BEFORE the run from the
   (R1) prover's and the R-IND-5 verifier's committed artifacts (scratchpad
   r1/ and rind5D/); no bar was moved against a measurement at any point, in
   either direction.
 MEASURED vs BAR (the ratio is the margin):
   s1 collapse vs the definitional CMI 8.88e-16 / 1e-12 (1126x) over 18 cells;
      record route vs moment route 8.88e-16 / 1e-12; both frames read in THEIR
      OWN order 1.75e-15 / 1e-12 (572x) over 24 (n, Delta, frame) cells;
      R21 MUST-FAIL control: the mixed pairing returns the lag-(Delta+1) rate
      to 3.33e-16 / 1e-12 and is therefore wrong by 7.640e-2 / 5e-2 (1.5x)
   s2 sum of block log-pivots = lndet Lambda 1.78e-15 / 1e-11 (5628x);
      sum ln sigma = lndet Lambda - sum ln s 1.33e-15 / 1e-11 (7506x)
   s3 full Szego decomposition 3.55e-15 / 1e-12 (282x) over 15 (n, Delta)
      cells at Nf = 4096 (Nf = 256 gives 7.99e-15); legs 1.78e-15 / 3.55e-15;
      R22 extremal family incl. c = 1 (min f = 0.0 EXACTLY, the spectrum
      VANISHES) 2.71e-14 / 1e-12 (37x); the n=2 anomaly is truncation --
      DMAX 2 -> 28 takes 1.76e-3 -> 1.61e-13 / 1e-9 (6213x)
   s4 900 per-instance certificates: (L1) affine 4.44e-16 / 1e-11 (22518x),
      0 violations; (L2a) shat(mid) = s(mid) 4.44e-16 / 1e-11, 0 violations;
      (L2b) shat >= s at both ends min slack +9.90e-6, 0 violations;
      concavity margin +1.909e-5 / 1e-6 (19x); min s 0.421289 > tau2 = 0.4
      (1.05x, and the floor is analytic, not measured); R23(ii) truncated
      family still concave 0/180, worst +7.92e-4; CONTROL peeking 2 slots
      ahead breaks 240/240 (100%, bar 95%), worst -0.2930 / -5e-2 (5.9x)
   s5 Jensen 0/1944 chords, smallest slack +9.639e-3; curvature 0/2160 second
      differences, smallest +1.392e-3; CONTROL (i) the RECORD chart is
      non-convex 1206/3960 = 30.5% / 5% (6.1x) negative second differences,
      most negative -1.255 / -1e-2 (125x); CONTROL (ii) both legs concave
      (0/135 and 0/135, margins +1.18e-1 and +3.76e-1) while the rate is NOT
      concave, best chord -5.172e-2 / -1e-2 (5.2x)
   s6 blocked noise spectrum constant in w 0.0e+00; U_k unitary 2.26e-16 /
      1e-12; eigenvalues invariant over the orbit AND over w 5.55e-16 / 1e-12;
      R26 correct side/sign (U_k* N U_k, e^{+i theta}) 1.19e-16 / 1e-12
      (8407x) and the three wrong combinations 4.117e-1 / 2.591e-1 / 4.117e-1
      against the 1e-1 O(1) bar (4.1x); hull floor slack +0.0913 / 2e-2
      (4.6x) with the Gamma cap respected; the rate rises 0.383 -> 11.224 as
      lambda_min(N) goes 1e-1 -> 1e-8, blow-up 10.84 / 5.0 (2.2x)
   s7 R24: 0 violations over 22,000 chords across FOUR non-psd-Q families with
      R psd (worst chord -4.98e-8, i.e. every single chord on the convex
      side), while the R-breaking control gives 198/673 / 50 (4.0x), worst
      +2.139; the theorem's own hypotheses give 0/5500.
      R25: (H, Gamma) held identical to 2.22e-16 (pinned) / 8.88e-16 (random)
      against 1e-13; the pinned deterministic A_u-ladder moves the rate by
      1.6350 bits / 0.136 (12.0x) and / 0.10 (16.3x); the random battery
      reports 0.1228 bits and is NOT gated
   s8 R29: lambda_min(R(w)) = 3.1715534e-3 / 3.0e-3 (1.06x) uniform in w and
      in n = 1..8, with spread over n 3.61e-15 / 1e-12 (277x); Q(w) =
      blockdiag(Phi_S(w)^-1, 0) to 1.40e-14 / 1e-13 (7.1x); max eig Z
      0.915440, gap to 1 of 0.0846 / 1e-2 (8.5x); the finite-window
      eigmin(P-Q) 1.038e-2/5.594e-3/4.431e-3/3.953e-3 at n = 8/16/24/32 is
      monotone decreasing and stays 7.81e-4 / 5e-4 (1.6x) ABOVE the blocked
      floor -- convergence FROM ABOVE
   s9 genuine-shift invariance 5.55e-16 / 1e-12 (1802x) over 27 shifted cells;
      R27 CONTROL: 27/27 rolled (H, Gamma) pairs leave the cone (bar 90%),
      while in RECORD coordinates the same roll is wrong by only 2.82e-9 /
      1e-7 (35x)
 DISCLOSURES.
 (a) NO OPTIMIZER, no fixed point and no root find appears anywhere in this
   file, so no gate can race a stopping point; and no bracket, width or
   certificate endpoint is read or gated.  The adversarial Nelder-Mead
   searches on record (prover -2.39e-2 over 6 runs x 3 restarts; verifier
   -1.62e-6 over 24 runs x <=2500 evals, four orders closer to zero and still
   never crossing) are carried in the JSON as RECORDED CONTEXT and are
   deliberately not reproduced or gated.
 (b) Two gates are CLAIM REPRODUCTIONS rather than fat-margin measurements and
   are labelled as such: s4's "min s > tau^2" (1.05x -- but tau^2 = 0.4 is an
   analytic floor, not an estimate) and s8's "floor >= 3.0e-3" (1.06x -- the
   floor 3.1715534e-3 is a deterministic eigenvalue of an exactly aliased
   spectrum, reproducible to 3.6e-15 across n).  Neither races anything.
 (c) The s1 R21 control is gated on the WORST cell (7.64e-2); the smallest
   cell error is 1.5e-3, so the mixed pairing is not uniformly loud -- which
   is exactly why frame and order must be printed as a pair rather than left
   to the reader.
 (d) s7's random A_u battery is REPORTED, never gated (see iter 2).
 (e) This harness nets NO value of Psi, NO margin against any sealed bar, and
   NO novelty claim: the novelty sweep on the (R1) combination is OWED.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261160 if a_.pilot
                                            else 20261161)
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
D_TGT = 0.3
LN2 = np.log(2.0)
TWOLN2 = 2.0 * LN2


def jsafe(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(o)


# ======================================================================
#  CORE: everything from the independent primitives (V, N, U, Z)
# ======================================================================
def sigV(M):
    k = np.abs(np.subtract.outer(np.arange(M), np.arange(M)))
    return A_ ** k


class Win:
    _c = {}

    def __init__(self, M):
        self.M = M
        self.SV = sigV(M)
        self.I = np.eye(M)
        self.SS = self.SV + TAU2 * self.I                     # Cov(S)
        self.SW = np.block([[self.SV, RHO * self.SV],
                            [RHO * self.SV,
                             RHO ** 2 * self.SV + SN2 * self.I]])
        self.SWS = np.vstack([self.SV, RHO * self.SV])        # Cov(W, S)
        self.SWi = np.linalg.inv(self.SW)
        self.PS = np.linalg.solve(self.SW, self.SWS)          # Sig_W^-1 Sig_WS

    @classmethod
    def get(cls, M):
        if M not in cls._c:
            cls._c[M] = Win(M)
        return cls._c[M]


def joint4(win, Av, Ay, Nc, Au=None):
    """Cov of the stacked (V, Y, S, Yhat), 4M x 4M, from the primitives."""
    M = win.M
    I, Z0 = win.I, np.zeros((M, M))
    if Au is None:
        Au = Z0
    covP = [win.SV, SN2 * I, TAU2 * I, Nc]                    # V, N, U, Z
    Mp = np.block([
        [I, Z0, Z0, Z0],                                      # V
        [RHO * I, I, Z0, Z0],                                 # Y
        [I, Z0, I, Z0],                                       # S
        [Av + RHO * Ay, Ay, Au, I],                           # Yhat
    ])
    CP = np.zeros((4 * M, 4 * M))
    for i in range(4):
        CP[i * M:(i + 1) * M, i * M:(i + 1) * M] = covP[i]
    return Mp @ CP @ Mp.T


def IX(M):
    return (np.arange(0, M), np.arange(M, 2 * M),
            np.arange(2 * M, 3 * M), np.arange(3 * M, 4 * M))


def cvar(C, tgt, cond):
    if len(cond) == 0:
        return float(C[tgt, tgt])
    b = C[np.ix_(cond, [tgt])].ravel()
    return float(C[tgt, tgt] - b @ np.linalg.solve(C[np.ix_(cond, cond)], b))


def la_definition(win, Av, Ay, Nc, Delta, t0_, per, Au=None):
    """L_a in bits STRAIGHT FROM THE CMI DEFINITION (no collapse used)."""
    M = win.M
    C = joint4(win, Av, Ay, Nc, Au)
    iV, iY, iS, iR = IX(M)
    tot = 0.0
    for t in range(t0_, t0_ + per):
        se = min(t + 1 + Delta, M)
        cS = list(iS[:se]); cR = list(iR[:t]); tgt = int(iR[t])
        num = cvar(C, tgt, cS + cR)
        den = cvar(C, tgt, list(iV) + list(iY) + cS + cR)
        tot += np.log(num / den)
    return tot / (TWOLN2 * per)


def order_SR(M, Delta):
    """Interleaved order of (S^M, Yhat^M): S_j before Yhat_t iff
    j < se(t) = min(t+1+Delta, M)."""
    order, posR, posS = [], [], []
    j = 0
    for t in range(M):
        se = min(t + 1 + Delta, M)
        while j < se:
            posS.append(len(order)); order.append(j); j += 1
        posR.append(len(order)); order.append(M + t)
    while j < M:
        posS.append(len(order)); order.append(j); j += 1
    return np.array(order), np.array(posR), np.array(posS)


_O = {}


def get_order(M, Delta):
    k = (M, Delta)
    if k not in _O:
        _O[k] = order_SR(M, Delta)
    return _O[k]


def jointSR(win, Av, Ay, Nc, Au=None):
    M = win.M
    C = joint4(win, Av, Ay, Nc, Au)
    ix = np.concatenate([np.arange(2 * M, 3 * M), np.arange(3 * M, 4 * M)])
    return C[np.ix_(ix, ix)]


def pivots(win, Av, Ay, Nc, Delta, Au=None):
    """sigma_t, s_j (interleaved Cholesky) and nu_t (Cholesky of Nc)."""
    M = win.M
    J = jointSR(win, Av, Ay, Nc, Au)
    order, posR, posS = get_order(M, Delta)
    d2 = np.diag(np.linalg.cholesky(J[np.ix_(order, order)])) ** 2
    return d2[posR], d2[posS], np.diag(np.linalg.cholesky(Nc)) ** 2


def rate_collapse(win, Av, Ay, Nc, Delta, t0_, per, Au=None):
    sg, s, nu = pivots(win, Av, Ay, Nc, Delta, Au)
    return float((np.log(sg[t0_:t0_ + per]).sum()
                  - np.log(nu[t0_:t0_ + per]).sum()) / (TWOLN2 * per))


def H_of(win, Av, Ay):
    """H = Cov(Yhat, W), M x 2M (A_u is invisible to H -- this is R25)."""
    g = Av + RHO * Ay
    CRV = g @ win.SV
    CRY = RHO * (g @ win.SV) + SN2 * Ay
    return np.hstack([CRV, CRY])


def Gam_of(win, Av, Ay, Nc, Au=None):
    g = Av + RHO * Ay
    G = g @ win.SV @ g.T + SN2 * (Ay @ Ay.T) + Nc
    if Au is not None:
        G = G + TAU2 * (Au @ Au.T)
    return 0.5 * (G + G.T)


def to_moments(win, Av, Ay, Nc, Au=None):
    return H_of(win, Av, Ay), Gam_of(win, Av, Ay, Nc, Au)


def noise_from_moments(win, H, Gam):
    N = Gam - H @ win.SWi @ H.T
    return 0.5 * (N + N.T)


def mix_moments(xs, wts):
    """Convex combination in the MOMENT coordinates (H, Gamma)."""
    H = sum(w * x[0] for x, w in zip(xs, wts))
    G = sum(w * x[1] for x, w in zip(xs, wts))
    return H, 0.5 * (G + G.T)


def AvAy_from_H(win, H):
    A = np.linalg.solve(win.SW, H.T).T
    M = win.M
    return A[:, :M], A[:, M:]


def fast_rate(win, H, Gam, Delta, t0_, per, ret=False):
    """Rate from the MOMENT pair alone (F0 route).  J is AFFINE in (H,Gam):
    Cov(Yhat, S) = H Sig_W^-1 Sig_WS is the leak leg."""
    M = win.M
    CRS = H @ win.PS
    N = Gam - H @ win.SWi @ H.T
    N = 0.5 * (N + N.T)
    J = np.empty((2 * M, 2 * M))
    J[:M, :M] = win.SS; J[:M, M:] = CRS.T
    J[M:, :M] = CRS;    J[M:, M:] = Gam
    J = 0.5 * (J + J.T)
    order, posR, posS = get_order(M, Delta)
    d2 = np.diag(np.linalg.cholesky(J[np.ix_(order, order)])) ** 2
    nu = np.diag(np.linalg.cholesky(N)) ** 2
    sg = d2[posR]; s = d2[posS]
    r = float((np.log(sg[t0_:t0_ + per]).sum()
               - np.log(nu[t0_:t0_ + per]).sum()) / (TWOLN2 * per))
    if ret:
        return r, sg, s, nu, N
    return r


def rand_block(n, rng, scale=0.30, nfloor=0.10, nscale=0.15):
    Av = scale * rng.standard_normal((n, n))
    Ay = scale * rng.standard_normal((n, n))
    B = rng.standard_normal((n, n))
    Nc = nscale * (B @ B.T) / n + nfloor * np.eye(n)
    return Av, Ay, Nc


def tile_shift(n, Av, Ay, Nc, M, k):
    """GENUINE shift-by-k of the bi-infinite period-n record: block boundaries
    at ..., k-n, k, k+n, ...  read on the window [0, M)."""
    AvT = np.zeros((M, M)); AyT = np.zeros((M, M)); NT = np.zeros((M, M))
    b = -2
    while b * n + k < M:
        r0 = b * n + k
        lo, hi = max(0, r0), min(M, r0 + n)
        if hi > lo:
            sl = slice(lo, hi); bl = slice(lo - r0, hi - r0)
            AvT[sl, sl] = Av[bl, bl]; AyT[sl, sl] = Ay[bl, bl]
            NT[sl, sl] = Nc[bl, bl]
        b += 1
    return AvT, AyT, NT


def roll_shift(Mat, k):
    """The BUGGY 'shift' (R27): np.roll of the window matrices."""
    return np.roll(np.roll(Mat, k, 0), k, 1)


def adversarial(kind, n, rng):
    """Adversarial record families used by s4/s5."""
    if kind == "dense":
        return rand_block(n, rng, scale=0.30)
    if kind == "big":
        return rand_block(n, rng, scale=0.90, nfloor=0.30, nscale=0.40)
    if kind == "tight":                        # ~1e-6 from the cone boundary
        Av, Ay, _ = rand_block(n, rng, scale=0.30)
        return Av, Ay, 1e-6 * np.eye(n) + 1e-7 * np.ones((n, n))
    if kind == "notch":                        # deep narrow spectral notch
        Av, Ay, _ = rand_block(n, rng, scale=0.30)
        F = np.fft.fft(np.eye(n), axis=0) / np.sqrt(n)
        ev = 0.5 + 0.5 * rng.random(n)
        ev[rng.integers(0, n)] = 1e-3
        ev = 0.5 * (ev + ev[(-np.arange(n)) % n])
        C = np.real(F.conj().T @ np.diag(ev) @ F)
        return Av, Ay, 0.5 * (C + C.T)
    if kind == "alt":                          # sign-alternating kernels
        s = np.array([(-1.0) ** (i + j) for i in range(n)
                      for j in range(n)]).reshape(n, n)
        Av, Ay, Nc = rand_block(n, rng, scale=0.55)
        return Av * s, Ay * s, Nc
    if kind == "neardet":                      # near-deterministic
        Av, Ay, Nc = rand_block(n, rng, scale=0.30, nfloor=0.0, nscale=0.004)
        return Av, Ay, Nc + 3e-4 * np.eye(n)
    if kind == "banded":
        Av, Ay, Nc = rand_block(n, rng, scale=0.35)
        k = np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
        return Av * (k <= 1), Ay * (k <= 1), Nc
    raise ValueError(kind)


# ======================================================================
#  BLOCKED SPECTRA (s3, s6, s8): exact aliasing + exact finite-support reads
# ======================================================================
def fV(w):
    return (1 - A_ ** 2) / np.abs(1 - A_ * np.exp(-1j * w)) ** 2


def blocked_scalar(f, n, nf):
    """EXACT blocked n x n spectral density of a scalar stationary process."""
    th = 2 * np.pi * np.arange(nf) / nf
    P = np.zeros((nf, n, n), complex)
    jk = np.subtract.outer(np.arange(n), np.arange(n))
    for m in range(n):
        w = (th + 2 * np.pi * m) / n
        P += (f(w)[:, None, None] / n) * np.exp(1j * np.multiply.outer(w, jk))
    return P


def blocked_transfer(Mat, n, t0_, dmax, nf):
    """A(theta) = sum_d A_d e^{-i d theta}, A_d[j,k] = Mat[t0+j, t0-dn+k]."""
    th = 2 * np.pi * np.arange(nf) / nf
    A = np.zeros((nf, n, n), complex)
    for d in range(-dmax, dmax + 1):
        Ad = Mat[np.ix_(t0_ + np.arange(n), t0_ - d * n + np.arange(n))]
        A = A + np.exp(-1j * d * th)[:, None, None] * Ad
    return A


def ct(X):
    return np.conj(np.swapaxes(X, 1, 2))


def model_blocked(n, nf):
    PhiV = blocked_scalar(fV, n, nf)
    I = np.eye(n)[None, :, :] + 0j
    PhiW = np.zeros((nf, 2 * n, 2 * n), complex)
    PhiW[:, :n, :n] = PhiV
    PhiW[:, :n, n:] = RHO * PhiV
    PhiW[:, n:, :n] = RHO * PhiV
    PhiW[:, n:, n:] = RHO ** 2 * PhiV + SN2 * I
    PhiS = PhiV + TAU2 * I
    PhiWS = np.concatenate([PhiV, RHO * PhiV], axis=1)
    return PhiW, PhiS, PhiWS


def avg_ld(P):
    return float(np.mean(np.linalg.slogdet(P)[1]))


def spectral_legs(n, nf, Av, Ay, Nw, t0_, dmax):
    PhiW, PhiS, PhiWS = model_blocked(n, nf)
    Az = np.concatenate([blocked_transfer(Av, n, t0_, dmax, nf),
                         blocked_transfer(Ay, n, t0_, dmax, nf)], axis=2)
    PhiZ = blocked_transfer(Nw, n, t0_, dmax, nf)
    h = Az @ PhiW
    Gam = h @ ct(Az) + PhiZ
    P = np.linalg.inv(PhiW)
    Q = P @ PhiWS @ np.linalg.inv(PhiS) @ ct(PhiWS) @ P
    MQ = Gam - h @ Q @ ct(h)
    nsp = Gam - h @ P @ ct(h)
    return dict(MQ=MQ, nsp=nsp, PhiS=PhiS, PhiZ=PhiZ)


print("=" * 78)
print("GO-14 (R1) HARNESS -- Theorem R1, the Scoping Lemma, and R21-R29")
print(f"  seed stamp {SEED} ({'pilot' if a_.pilot else 'governed'});"
      " NO OPTIMIZER ANYWHERE IN THIS FILE")
print("=" * 78)

# ==================================================================== s1
print("[s1] Collapse + the FRAME/ORDER PAIR (R21) ...", flush=True)
BAR_S1_CMI = 1e-12
BAR_S1_MOM = 1e-12
BAR_S1_FRAME = 1e-12
BAR_S1_MIXEQ = 1e-12
BAR_S1_MIXWRONG = 5e-2

rng = np.random.default_rng(90210)
w_cmi = 0.0
n_cmi = 0
for n in (3, 4):
    M = n * 10; tt = 4 * n
    win = Win.get(M)
    for Delta in (0, 1, 2):
        for rep in range(3):
            blk = rand_block(n, rng)
            Av, Ay, Nc = tile_shift(n, *blk, M, 0)
            a = la_definition(win, Av, Ay, Nc, Delta, tt, n)
            b = rate_collapse(win, Av, Ay, Nc, Delta, tt, n)
            w_cmi = max(w_cmi, abs(a - b)); n_cmi += 1
w_mom = 0.0
for n in (3, 4):
    M = n * 10; tt = 4 * n
    win = Win.get(M)
    for Delta in (0, 1, 2):
        blk = rand_block(n, rng)
        Av, Ay, Nc = tile_shift(n, *blk, M, 0)
        H, G = to_moments(win, Av, Ay, Nc)
        w_mom = max(w_mom, abs(rate_collapse(win, Av, Ay, Nc, Delta, tt, n)
                               - fast_rate(win, H, G, Delta, tt, n)))
print(f"  CMI definition vs COLLAPSE, {n_cmi} cells: worst {w_cmi:.2e} < "
      f"{BAR_S1_CMI:.0e}; record route vs MOMENT route {w_mom:.2e}", flush=True)


def seq_indices(M, Delta, frame):
    """Interleaved scalar sequence of the blocked process, in the frame's
    OWN within-block order.  FRAME-R: R_u = Yhat_{u-Delta-1}, order R,S.
    FRAME-S: R_u = Yhat_{u-Delta}, order S,R."""
    idx, tag = [], []
    if frame == "S":
        for u in range(Delta, M):
            idx.append(u);                 tag.append(("S", u))
            idx.append(M + u - Delta);     tag.append(("R", u))
    else:
        for u in range(Delta + 1, M):
            idx.append(M + u - Delta - 1); tag.append(("R", u))
            idx.append(u);                 tag.append(("S", u))
    return np.array(idx), tag


rng2 = np.random.default_rng(4242)
w_frame = 0.0
w_lam = 0.0
w_id = 0.0
n_frame = 0
mix_rows = []
for n in (2, 3, 4, 6):
    B = max(10, 120 // n); M = n * B
    win = Win.get(M)
    for Delta in (0, 1, 2):
        blk = rand_block(n, rng2)
        Av, Ay, Nc = tile_shift(n, *blk, M, 0)
        J = jointSR(win, Av, Ay, Nc)
        sg, s, nu = pivots(win, Av, Ay, Nc, Delta)
        for frame in ("S", "R"):
            idx, tag = seq_indices(M, Delta, frame)
            C = J[np.ix_(idx, idx)]
            d2 = np.diag(np.linalg.cholesky(C)) ** 2
            e = 0.0
            for p, (kind, u) in enumerate(tag):
                if u < max(3 * n, 40) or u > M - max(3 * n, 40):
                    continue
                if kind == "R":
                    t = u - (Delta if frame == "S" else Delta + 1)
                    e = max(e, abs(d2[p] - sg[t]) / sg[t])
                else:
                    e = max(e, abs(d2[p] - s[u]) / s[u])
            w_frame = max(w_frame, e); n_frame += 1
            # ---- step (1): the one-step BLOCK INNOVATION covariance Lambda
            b0 = (len(idx) // (4 * n)) * 2 * n
            past = np.arange(0, b0); blki = np.arange(b0, b0 + 2 * n)
            Cb = C[np.ix_(blki, blki)]; Cp = C[np.ix_(past, past)]
            Cbp = C[np.ix_(blki, past)]
            Lam = Cb - Cbp @ np.linalg.solve(Cp, Cbp.T)
            Lam = 0.5 * (Lam + Lam.T)
            sld = np.linalg.slogdet(Lam)[1]
            w_lam = max(w_lam, abs(sld - np.log(d2[blki]).sum()))
            dl = np.diag(np.linalg.cholesky(Lam)) ** 2
            if frame == "S":
                ls = np.log(dl[0::2]).sum(); lsig = np.log(dl[1::2]).sum()
            else:
                lsig = np.log(dl[0::2]).sum(); ls = np.log(dl[1::2]).sum()
            w_id = max(w_id, abs(lsig - (sld - ls)))
        # ---- R21 MUST-FAIL CONTROL: this document's FRAME read in the OTHER
        # ---- frame's within-block ORDER
        idx = []
        for u in range(Delta + 1, M):
            idx.append(u); idx.append(M + u - Delta - 1)
        idx = np.array(idx)
        d2 = np.diag(np.linalg.cholesky(J[np.ix_(idx, idx)])) ** 2
        lo = (M // 2 // n) * n
        sl = slice(2 * (lo - Delta - 1) + 1, 2 * (lo - Delta - 1) + 1 + 2 * n, 2)
        r_mix = float((np.log(d2[sl]).sum() - np.log(nu[lo:lo + n]).sum())
                      / (TWOLN2 * n))
        r_true = rate_collapse(win, Av, Ay, Nc, Delta, lo, n)
        r_next = rate_collapse(win, Av, Ay, Nc, Delta + 1, lo, n)
        mix_rows.append(dict(n=n, Delta=Delta, r_true=r_true, r_mix=r_mix,
                             r_next=r_next, err=r_mix - r_true,
                             eq_next=abs(r_mix - r_next)))
mix_eq = max(r["eq_next"] for r in mix_rows)
mix_wrong = max(abs(r["err"]) for r in mix_rows)
vals["s1"] = {"cmi_vs_collapse": w_cmi, "record_vs_moment": w_mom,
              "n_cmi_cells": n_cmi, "frame_pivots_worst": w_frame,
              "n_frame_cells": n_frame, "mixed": mix_rows,
              "mixed_equals_lag_Dp1": mix_eq, "mixed_error_vs_true": mix_wrong,
              "bars": {"cmi": BAR_S1_CMI, "moment": BAR_S1_MOM,
                       "frame": BAR_S1_FRAME, "mix_eq": BAR_S1_MIXEQ,
                       "mix_wrong": BAR_S1_MIXWRONG}}
verdicts["s1_collapse_matches_CMI_definition"] = w_cmi < BAR_S1_CMI
verdicts["s1_record_route_matches_moment_route"] = w_mom < BAR_S1_MOM
verdicts["s1_both_frames_exact_with_matching_orders"] = w_frame < BAR_S1_FRAME
verdicts["s1_R21_mixed_pairing_returns_lag_Delta_plus_1"] = mix_eq < BAR_S1_MIXEQ
verdicts["s1_R21_mixed_pairing_is_WRONG"] = mix_wrong > BAR_S1_MIXWRONG
print(f"  both frames read in THEIR OWN order: worst relative pivot error "
      f"{w_frame:.2e} < {BAR_S1_FRAME:.0e} over {n_frame} (n,Delta,frame) "
      f"cells", flush=True)
print(f"  R21 CONTROL -- this document's frame R_u = Yhat_(u-Delta-1) read in "
      f"the OTHER order (S first) returns the lag-(Delta+1) rate to "
      f"{mix_eq:.1e} and is therefore WRONG by up to {mix_wrong:.2e} bits > "
      f"{BAR_S1_MIXWRONG:.0e}: FRAME AND ORDER MUST BE PRINTED AS A PAIR "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ==================================================================== s2
print("[s2] step (1): the block-innovation Cholesky ...", flush=True)
BAR_S2_LAM = 1e-11
BAR_S2_ID = 1e-11
vals["s2"] = {"lndet_Lambda_worst": w_lam, "identity_worst": w_id,
              "cells": n_frame,
              "bars": {"lam": BAR_S2_LAM, "identity": BAR_S2_ID}}
verdicts["s2_block_log_pivots_equal_lndet_Lambda"] = w_lam < BAR_S2_LAM
verdicts["s2_block_innovation_identity"] = w_id < BAR_S2_ID
print(f"  sum of block log-pivots == lndet Lambda: worst {w_lam:.2e} < "
      f"{BAR_S2_LAM:.0e}", flush=True)
print(f"  sum_i ln sigma_i == lndet Lambda - sum_i ln s_i: worst {w_id:.2e} < "
      f"{BAR_S2_ID:.0e}, over {n_frame} (n, Delta, frame) cells "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ==================================================================== s3
print("[s3] step (2): the MATRIX SZEGO identity (the only analytic input) ...",
      flush=True)
BAR_S3_ID = 1e-12
BAR_S3_LEG = 1e-12
BAR_S3_EXTREMAL = 1e-12
BAR_S3_TRUNC = 1e-9
rng3 = np.random.default_rng(1618)
rows3 = []
for n in (1, 2, 3, 4, 6):
    B = max(24, 400 // n); M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    blk = rand_block(n, rng3)
    Av, Ay, Nc = tile_shift(n, *blk, M, 0)
    for Delta in (0, 1, 2):
        sg, s, nu = pivots(win, Av, Ay, Nc, Delta)
        lnu = np.log(nu[tt:tt + n]).sum()
        ls = np.log(s[tt:tt + n]).sum()
        lsig = np.log(sg[tt:tt + n]).sum()
        r = rate_collapse(win, Av, Ay, Nc, Delta, tt, n)
        for nf in (256, 4096):
            L = spectral_legs(n, nf, Av, Ay, Nc, tt, 3)
            S1 = abs(avg_ld(L['PhiZ']) - lnu)
            S2 = abs(avg_ld(L['PhiS']) + avg_ld(L['MQ']) - (ls + lsig))
            ID = abs(avg_ld(L['MQ']) - avg_ld(L['nsp']) + avg_ld(L['PhiS'])
                     - ls - TWOLN2 * n * r)
            rows3.append(dict(n=n, Delta=Delta, nf=nf, S1=S1, S2=S2, ID=ID))
w3 = {k: max(r[k] for r in rows3 if r['nf'] == 4096) for k in ("S1", "S2", "ID")}
w3_256 = {k: max(r[k] for r in rows3 if r['nf'] == 256)
          for k in ("S1", "S2", "ID")}
print(f"  full decomposition 2ln2 n rate = <lndet M_Q> - <lndet n> + "
      f"<lndet Phi_S> - sum ln s, 15 (n, Delta) cells at Nf=4096: worst "
      f"{w3['ID']:.2e} < {BAR_S3_ID:.0e}  (legs {w3['S1']:.2e}/{w3['S2']:.2e}; "
      f"Nf=256 gives {w3_256['ID']:.2e})", flush=True)

# R22: the extremal family, INCLUDING the vanishing-spectrum case
notch = []
Mn = 400
for c in (0.5, 0.9, 0.99, 0.999, 1.0):
    L = np.eye(Mn) - c * np.eye(Mn, k=-1)
    Nc = L @ L.T
    nu = np.diag(np.linalg.cholesky(Nc)) ** 2
    mid = float(np.log(nu[200:220]).mean())
    notch.append(dict(c=c, min_f=(1 - c) ** 2, resid=abs(mid)))
extremal = max(r["resid"] for r in notch)
min_f_at_1 = [r["min_f"] for r in notch if r["c"] == 1.0][0]

# the n=2 anomaly is BLOCK-LAG TRUNCATION of the chord evaluator, not the
# identity: sweep DMAX on a chord (whose derived noise is NOT block banded)
sweep = []
for n in (2, 3):
    B = 60; M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    x1 = to_moments(win, *tile_shift(n, *rand_block(n, rng3), M, 0))
    x2 = to_moments(win, *tile_shift(n, *rand_block(n, rng3), M, 1))
    H, G = mix_moments([x1, x2], [0.5, 0.5])
    Av, Ay = AvAy_from_H(win, H)
    Nw = noise_from_moments(win, H, G)
    Delta = 0
    r = fast_rate(win, H, G, Delta, tt, n)
    sg, s, nu = pivots(win, Av, Ay, Nw, Delta)
    ls = np.log(s[tt:tt + n]).sum()
    for dmax in (2, 12, 20, 28):
        if dmax * n > tt or dmax * n > M - tt - n:
            continue
        L = spectral_legs(n, 4096, Av, Ay, Nw, tt, dmax)
        ID = abs(avg_ld(L['MQ']) - avg_ld(L['nsp']) + avg_ld(L['PhiS'])
                 - ls - TWOLN2 * n * r)
        sweep.append(dict(n=n, dmax=dmax, ID=ID))
trunc_deep = max(r["ID"] for r in sweep if r["dmax"] == 28)
trunc_shallow = min(r["ID"] for r in sweep if r["dmax"] == 2)
vals["s3"] = {"nf4096": w3, "nf256": w3_256, "cells": rows3,
              "extremal": notch, "extremal_worst": extremal,
              "min_f_at_c1": min_f_at_1, "dmax_sweep": sweep,
              "trunc_dmax28": trunc_deep, "trunc_dmax2": trunc_shallow,
              "bars": {"identity": BAR_S3_ID, "leg": BAR_S3_LEG,
                       "extremal": BAR_S3_EXTREMAL, "trunc": BAR_S3_TRUNC}}
verdicts["s3_szego_full_identity"] = w3["ID"] < BAR_S3_ID
verdicts["s3_szego_legs"] = max(w3["S1"], w3["S2"]) < BAR_S3_LEG
verdicts["s3_R22_extremal_family_incl_vanishing_spectrum"] = \
    (extremal < BAR_S3_EXTREMAL) and (min_f_at_1 == 0.0)
verdicts["s3_n2_anomaly_is_block_lag_truncation"] = \
    (trunc_deep < BAR_S3_TRUNC) and (trunc_shallow > 1e-4)
print(f"  R22 -- the eps floor is NOT a hypothesis of the Szego step: on the "
      f"extremal family f = |1 - c e^(-iw)|^2 the identity holds up to and "
      f"INCLUDING c = 1 (min f = {min_f_at_1:.1f}, the spectrum VANISHES), "
      f"worst residual {extremal:.2e} < {BAR_S3_EXTREMAL:.0e}", flush=True)
print(f"  the n=2 anomaly is BLOCK-LAG TRUNCATION of the chord evaluator, not "
      f"the identity: DMAX 2 -> 28 takes the residual {trunc_shallow:.1e} -> "
      f"{trunc_deep:.1e} < {BAR_S3_TRUNC:.0e} [{time.time()-t0:.0f}s]",
      flush=True)

# ==================================================================== s4
print("[s4] step (3b): s_i is an INF OF AFFINE -- the three links, and the "
      "peeking control ...", flush=True)
BAR_S4_AFFINE = 1e-11
BAR_S4_MID = 1e-11
BAR_S4_ENDS = -1e-11
BAR_S4_MARGIN = 1e-6
BAR_S4_TAU2 = TAU2
BAR_S4_TRUNC_CONC = -1e-12
BAR_S4_CTRL_FRAC = 0.95
BAR_S4_CTRL_DEPTH = -5e-2
rng4 = np.random.default_rng(271828)
_JC = {}


def J_of(win, H, G):
    """Cov(S^M, Yhat^M) from the MOMENT pair -- AFFINE in (H, Gamma).
    Cov(Yhat, S) = H Sig_W^-1 Sig_WS is the F0 leak leg (R25's entry point)."""
    key = (id(H), id(G))
    hit = _JC.get(key)
    if hit is not None and hit[0] is H and hit[1] is G:
        return hit[2]
    CRS = H @ win.PS
    J = np.block([[win.SS, CRS.T], [CRS, G]])
    if len(_JC) > 32:
        _JC.clear()
    _JC[key] = (H, G, J)
    return J


def s_exact(win, H, G, Delta, jpos, extra=None, depth=None):
    """Leak pivot at S-slot jpos, plus the optimal frozen predictor.
    `depth` truncates the predictor; `extra` adds LATER slots (inadmissible)."""
    M = win.M
    J = J_of(win, H, G)
    order, posR, posS = get_order(M, Delta)
    p = posS[jpos]
    tgt = int(order[p])
    prev = list(order[:p]) if depth is None else list(order[max(0, p - depth):p])
    if extra:
        prev = prev + [int(order[q]) for q in extra]
    if not prev:
        return float(J[tgt, tgt]), np.zeros(0), [], tgt
    K = J[np.ix_(prev, prev)]
    b = J[np.ix_(prev, [tgt])].ravel()
    w = np.linalg.solve(K, b)
    return float(J[tgt, tgt] - b @ w), w, prev, tgt


def shat(win, H, G, w, prev, tgt):
    """The FROZEN-predictor minorant: exactly AFFINE in (H, Gamma)."""
    J = J_of(win, H, G)
    return float(J[tgt, tgt] - 2 * w @ J[np.ix_(prev, [tgt])].ravel()
                 + w @ J[np.ix_(prev, prev)] @ w)


c1 = c2 = c3 = 0
n_t = 0
w1 = w2 = 0.0
w3v = 9.9
marg = 9.9
smin = 9.9
ctrl_break = ctrl_tot = 0
ctrl_worst = 0.0
for n in (2, 3, 4, 6):
    B = max(8, 132 // n); M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    for Delta in (0, 1, 2):
        for kind in ("dense", "banded", "notch", "neardet"):
            for rep in range(5):
                a = adversarial(kind, n, rng4); b = adversarial(kind, n, rng4)
                k = int(rng4.integers(0, n))
                xa = to_moments(win, *tile_shift(n, *a, M, 0))
                xb = to_moments(win, *tile_shift(n, *b, M, k))
                lam = float(rng4.uniform(0.2, 0.8))
                xm = mix_moments([xa, xb], [1 - lam, lam])
                if np.linalg.eigvalsh(noise_from_moments(win, *xm)).min() <= 0:
                    continue
                for jj in range(tt, tt + n):
                    try:
                        sm, w, prev, tgt = s_exact(win, *xm, Delta, jj)
                        sa = s_exact(win, *xa, Delta, jj)[0]
                        sb = s_exact(win, *xb, Delta, jj)[0]
                    except np.linalg.LinAlgError:
                        continue
                    ha = shat(win, *xa, w, prev, tgt)
                    hb = shat(win, *xb, w, prev, tgt)
                    hm = shat(win, *xm, w, prev, tgt)
                    n_t += 1
                    e1 = abs(hm - ((1 - lam) * ha + lam * hb))   # (L1) affine
                    e2 = abs(hm - sm)                            # (L2a) tight
                    e3 = min(ha - sa, hb - sb)                   # (L2b) >= s
                    w1 = max(w1, e1); w2 = max(w2, e2); w3v = min(w3v, e3)
                    c1 += e1 > 1e-11; c2 += e2 > 1e-11; c3 += e3 < -1e-11
                    marg = min(marg, sm - ((1 - lam) * sa + lam * sb))
                    smin = min(smin, sa, sb, sm)
                try:                    # CONTROL: peek 2 slots ahead
                    order, posR, posS = get_order(M, Delta)
                    p = posS[tt]
                    sm, w, prev, tgt = s_exact(win, *xm, Delta, tt,
                                               extra=[p + 1, p + 2])
                    sa = s_exact(win, *xa, Delta, tt)[0]
                    ha = shat(win, *xa, w, prev, tgt)
                    ctrl_tot += 1
                    ctrl_break += (ha - sa < -1e-9)
                    ctrl_worst = min(ctrl_worst, ha - sa)
                except np.linalg.LinAlgError:
                    pass

# R23(ii): truncating the family gives a DIFFERENT function, still concave
tb = tt2 = 0
tworst = 9.9
depth_rows = []
for n in (3, 4):
    B = 30; M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    for Delta in (0, 1):
        for rep in range(15):
            xa = to_moments(win, *tile_shift(n, *rand_block(n, rng4), M, 0))
            xb = to_moments(win, *tile_shift(n, *rand_block(n, rng4), M, 1))
            xm = mix_moments([xa, xb], [0.5, 0.5])
            if np.linalg.eigvalsh(noise_from_moments(win, *xm)).min() <= 0:
                continue
            for d in (4, 12, None):
                sa = s_exact(win, *xa, Delta, tt, depth=d)[0]
                sb = s_exact(win, *xb, Delta, tt, depth=d)[0]
                sm = s_exact(win, *xm, Delta, tt, depth=d)[0]
                g = sm - 0.5 * (sa + sb)
                tt2 += 1; tb += g < BAR_S4_TRUNC_CONC
                tworst = min(tworst, g)
# R23(ii) closure: the finite-support causal predictors are dense
n = 4; B = 40; M = n * B; tt = (B // 2) * n
win = Win.get(M)
x = to_moments(win, *tile_shift(n, *rand_block(n, rng4), M, 0))
s_full = s_exact(win, *x, 0, tt)[0]
clos = []
mono = True
prev_gap = None
for depth in (1, 2, 4, 8, 16, 32, 64):
    gap = s_exact(win, *x, 0, tt, depth=depth)[0] - s_full
    if prev_gap is not None and gap > prev_gap + 1e-14:
        mono = False
    prev_gap = gap
    clos.append(dict(depth=depth, gap=gap))
vals["s4"] = {"instances": n_t, "L1_viol": c1, "L1_worst": w1,
              "L2a_viol": c2, "L2a_worst": w2, "L2b_viol": c3,
              "L2b_min_slack": w3v, "concavity_margin_min": marg,
              "s_min": smin, "tau2": TAU2,
              "peek_break": ctrl_break, "peek_tot": ctrl_tot,
              "peek_worst": ctrl_worst,
              "trunc_conc_viol": tb, "trunc_conc_tot": tt2,
              "trunc_conc_worst": tworst,
              "closure": clos, "closure_monotone": mono,
              "bars": {"affine": BAR_S4_AFFINE, "mid": BAR_S4_MID,
                       "ends": BAR_S4_ENDS, "margin": BAR_S4_MARGIN,
                       "tau2": BAR_S4_TAU2, "trunc": BAR_S4_TRUNC_CONC,
                       "ctrl_frac": BAR_S4_CTRL_FRAC,
                       "ctrl_depth": BAR_S4_CTRL_DEPTH}}
verdicts["s4_L1_shat_is_affine"] = (c1 == 0) and (w1 < BAR_S4_AFFINE)
verdicts["s4_L2a_shat_equals_s_at_midpoint"] = (c2 == 0) and (w2 < BAR_S4_MID)
verdicts["s4_L2b_shat_ge_s_at_endpoints"] = (c3 == 0) and (w3v >= BAR_S4_ENDS)
verdicts["s4_concavity_margin_positive"] = marg > BAR_S4_MARGIN
verdicts["s4_s_bounded_below_by_tau2"] = smin > BAR_S4_TAU2
verdicts["s4_R23_truncated_family_still_concave"] = tb == 0
verdicts["s4_peeking_predictor_control_BREAKS"] = \
    (ctrl_break >= BAR_S4_CTRL_FRAC * ctrl_tot) and \
    (ctrl_worst < BAR_S4_CTRL_DEPTH)
print(f"  {n_t} per-instance concavity certificates, three links SEPARATE: "
      f"(L1) affine {c1} viol / worst {w1:.1e}; (L2a) shat(mid) = s(mid) {c2} "
      f"viol / worst {w2:.1e}; (L2b) shat >= s at both ends {c3} viol / min "
      f"slack {w3v:+.2e}", flush=True)
print(f"  concavity margin min {marg:+.3e} > {BAR_S4_MARGIN:.0e}; min s "
      f"{smin:.6f} > tau2 = {TAU2}", flush=True)
print(f"  R23(i) an inf of affine over ANY index set is concave -- no topology; "
      f"R23(ii) the closure argument only IDENTIFIES that inf with s: "
      f"truncating gives a different, still-concave function ({tb}/{tt2} "
      f"violations, worst {tworst:+.2e}), and the truncations converge "
      f"monotonically to s ({mono})", flush=True)
print(f"  CONTROL -- a predictor peeking 2 slots ahead is inadmissible and "
      f"BREAKS the minorant: {ctrl_break}/{ctrl_tot}, worst {ctrl_worst:+.4f} "
      f"< {BAR_S4_CTRL_DEPTH:.0e} [{time.time()-t0:.0f}s]", flush=True)

# ==================================================================== s5
print("[s5] the conclusion: convexity, and the two controls that show what "
      "it needs ...", flush=True)
BAR_S5_CHORD = -1e-11
BAR_S5_CURV = -1e-11
BAR_S5_CHART_FRAC = 0.05
BAR_S5_CHART_DEPTH = -1e-2
BAR_S5_LEG = -1e-11
BAR_S5_NOTCONC = -1e-2
rng5 = np.random.default_rng(101)
KINDS = ["dense", "big", "tight", "notch", "alt", "neardet"]
nv = nt = 0
worst5 = 9.9
worst_at = None
for n in (1, 2, 3, 4, 6, 8):
    B = max(8, 64 // n); M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    for Delta in (0, 1, 2):
        for ka in KINDS:
            for kb in KINDS:
                for rep in range(3):
                    a = adversarial(ka, n, rng5); b = adversarial(kb, n, rng5)
                    xa = to_moments(win, *tile_shift(n, *a, M, 0))
                    xb = to_moments(win, *tile_shift(
                        n, *b, M, int(rng5.integers(0, n))))
                    lam = float(rng5.uniform(0.1, 0.9))
                    xm = mix_moments([xa, xb], [1 - lam, lam])
                    try:
                        ra = fast_rate(win, *xa, Delta, tt, n)
                        rb = fast_rate(win, *xb, Delta, tt, n)
                        rm = fast_rate(win, *xm, Delta, tt, n)
                    except np.linalg.LinAlgError:
                        continue
                    g = (1 - lam) * ra + lam * rb - rm
                    nt += 1
                    nv += g < BAR_S5_CHORD
                    if g < worst5:
                        worst5 = g; worst_at = (n, Delta, ka, kb, round(lam, 4))
nv2 = nt2 = 0
worst5b = 9.9
for n in (2, 3, 4, 6):
    B = max(8, 64 // n); M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    for Delta in (0, 1, 2):
        for rep in range(20):
            a = adversarial(KINDS[rng5.integers(len(KINDS))], n, rng5)
            b = adversarial(KINDS[rng5.integers(len(KINDS))], n, rng5)
            xa = to_moments(win, *tile_shift(n, *a, M, 0))
            xb = to_moments(win, *tile_shift(n, *b, M, 1))
            v = []
            ok = True
            for t in np.linspace(0.05, 0.95, 11):
                xm = mix_moments([xa, xb], [1 - t, t])
                try:
                    v.append(fast_rate(win, *xm, Delta, tt, n))
                except np.linalg.LinAlgError:
                    ok = False; break
            if not ok:
                continue
            v = np.array(v)
            d2 = v[:-2] - 2 * v[1:-1] + v[2:]
            nt2 += len(d2); nv2 += int((d2 < BAR_S5_CURV).sum())
            worst5b = min(worst5b, float(d2.min()))

# CONTROL (i): the RECORD-parameter chart is NOT convex -- the moment chart
# is load-bearing.  Line scans with second differences.
rng5b = np.random.default_rng(24680)
cv = ct_ = 0
cworst = 9.9
cwit = None
for n in (1, 2, 3):
    B = max(10, 48 // n); M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    for Delta in (0, 1):
        for rep in range(60):
            sc = float(10 ** rng5b.uniform(-0.5, 0.6))
            a = rand_block(n, rng5b, scale=sc, nfloor=0.05, nscale=0.05)
            b = rand_block(n, rng5b, scale=sc, nfloor=0.05, nscale=0.05)
            if rep % 3 == 0:
                b = (-a[0], -a[1], b[2])
            if rep % 3 == 1:
                b = (a[0], a[1], b[2])
            v = []
            ok = True
            for t in np.linspace(0.02, 0.98, 13):
                p = tuple((1 - t) * u + t * vv for u, vv in zip(a, b))
                if np.linalg.eigvalsh(0.5 * (p[2] + p[2].T)).min() <= 1e-10:
                    ok = False; break
                try:
                    v.append(fast_rate(win, *to_moments(
                        win, *tile_shift(n, *p, M, 0)), Delta, tt, n))
                except np.linalg.LinAlgError:
                    ok = False; break
            if not ok:
                continue
            v = np.array(v)
            d2 = v[:-2] - 2 * v[1:-1] + v[2:]
            ct_ += len(d2); cv += int((d2 < -1e-11).sum())
            if d2.min() < cworst:
                cworst = float(d2.min()); cwit = (n, Delta, round(sc, 4), rep % 3)

# CONTROL (ii): the lemma ALONE proves nothing -- both legs are concave and
# the rate is NOT concave.  THE REGROUPING IS THE PROOF.
rng5c = np.random.default_rng(777)
vs = vn = 0
tt3 = 0
ws = wn = 9.9
wr = -9.9
for n in (2, 3, 4):
    B = max(8, 64 // n); M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    for Delta in (0, 1, 2):
        for rep in range(15):
            xa = to_moments(win, *tile_shift(n, *rand_block(n, rng5c), M, 0))
            xb = to_moments(win, *tile_shift(n, *rand_block(n, rng5c), M, 1))
            xm = mix_moments([xa, xb], [0.5, 0.5])
            try:
                ra, sga, sa, nua, _ = fast_rate(win, *xa, Delta, tt, n, ret=1)
                rb, sgb, sb, nub, _ = fast_rate(win, *xb, Delta, tt, n, ret=1)
                rm, sgm, sm, num, _ = fast_rate(win, *xm, Delta, tt, n, ret=1)
            except np.linalg.LinAlgError:
                continue
            tt3 += 1
            LS = lambda v_: float(np.log(v_[tt:tt + n]).sum())
            g = LS(sgm) - 0.5 * (LS(sga) + LS(sgb))
            vs += g < BAR_S5_LEG; ws = min(ws, g)
            g2 = LS(num) - 0.5 * (LS(nua) + LS(nub))
            vn += g2 < BAR_S5_LEG; wn = min(wn, g2)
            wr = max(wr, rm - 0.5 * (ra + rb))
vals["s5"] = {"chord_viol": nv, "chord_tot": nt, "chord_worst_slack": worst5,
              "chord_worst_at": worst_at, "curv_viol": nv2, "curv_tot": nt2,
              "curv_worst": worst5b,
              "chart_viol": cv, "chart_tot": ct_, "chart_worst": cworst,
              "chart_witness": cwit,
              "sigma_leg_viol": vs, "sigma_leg_margin": ws,
              "nu_leg_viol": vn, "nu_leg_margin": wn,
              "rate_concavity_best": wr, "leg_tot": tt3,
              "recorded_searches": {
                  "prover_nelder_mead_best_gap": -2.39e-2,
                  "verifier_nelder_mead_best_gap": -1.62e-6,
                  "note": "RECORDED CONTEXT ONLY -- not reproduced and not "
                          "gated: a gate on a search's best value would race "
                          "an optimizer stopping point"},
              "bars": {"chord": BAR_S5_CHORD, "curv": BAR_S5_CURV,
                       "chart_frac": BAR_S5_CHART_FRAC,
                       "chart_depth": BAR_S5_CHART_DEPTH,
                       "leg": BAR_S5_LEG, "not_concave": BAR_S5_NOTCONC}}
verdicts["s5_moment_chart_chords_zero_violations"] = (nv == 0) and (worst5 > 0)
verdicts["s5_moment_chart_curvature_zero_violations"] = \
    (nv2 == 0) and (worst5b > 0)
verdicts["s5_record_chart_control_is_NONCONVEX"] = \
    (cv > BAR_S5_CHART_FRAC * ct_) and (cworst < BAR_S5_CHART_DEPTH)
verdicts["s5_both_legs_concave"] = (vs == 0) and (vn == 0)
verdicts["s5_rate_is_NOT_concave"] = wr < BAR_S5_NOTCONC
print(f"  {nv}/{nt} Jensen violations in the MOMENT chart (n = 1..8, Delta = "
      f"0,1,2, six adversarial families incl. lambda_min(N) ~ 1e-6, a 1e-3 "
      f"notch, sign-alternating and near-deterministic); smallest slack "
      f"{worst5:+.3e} at {worst_at}", flush=True)
print(f"  {nv2}/{nt2} negative second differences along lines; smallest "
      f"{worst5b:+.3e}", flush=True)
print(f"  CONTROL (i) THE MOMENT CHART IS LOAD-BEARING: in the RECORD-parameter "
      f"chart the same functional is NON-convex -- {cv}/{ct_} negative second "
      f"differences (> {BAR_S5_CHART_FRAC:.0%}), most negative {cworst:+.3e} < "
      f"{BAR_S5_CHART_DEPTH:.0e}, witness {cwit}", flush=True)
print(f"  CONTROL (ii) THE LEMMA ALONE PROVES NOTHING: sum ln sigma concave "
      f"({vs}/{tt3} viol, margin {ws:+.2e}) AND sum ln nu concave ({vn}/{tt3}, "
      f"{wn:+.2e}), yet the rate is NOT concave (best chord {wr:+.3e} < "
      f"{BAR_S5_NOTCONC:.0e}).  THE REGROUPING IS THE PROOF "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ==================================================================== s6
print("[s6] the SCOPING LEMMA: unitarity, eigenvalue invariance, R26's side "
      "and sign, the hull floor ...", flush=True)
BAR_S6_UNIT = 1e-12
BAR_S6_EIG = 1e-12
BAR_S6_CONJ = 1e-12
BAR_S6_WRONG = 1e-1
BAR_S6_HULL = 2e-2
BAR_S6_BLOWUP = 5.0


def Uk(n, k, th, sign=+1):
    """Block cyclic shift X'_b[j] = X_{bn+k+j}; wrapped entries e^{sign i th}."""
    nf = len(th)
    U = np.zeros((nf, n, n), complex)
    for j in range(n):
        l = j + k
        if l < n:
            U[:, j, l] = 1.0
        else:
            U[:, j, l - n] = np.exp(sign * 1j * th)
    return U


rng6 = np.random.default_rng(13579)
NF6 = 64
th6 = 2 * np.pi * np.arange(NF6) / NF6
w_unit = w_eig = 0.0
w_conj = 0.0
w_wrong = 0.0
const_w = 0.0
combos = {"U N U* , e^{+i th}": 0.0, "U* N U , e^{-i th}": 0.0,
          "U N U* , e^{-i th}": 0.0}
for n in (2, 3, 4, 6):
    B = 24; M = n * B; tt = (B // 2) * n
    blk = rand_block(n, rng6)
    Nc = blk[2]
    evN = np.sort(np.linalg.eigvalsh(Nc))
    for k in range(n):
        Av, Ay, Nk = tile_shift(n, *blk, M, k)
        Pk = blocked_transfer(Nk, n, tt, 2, NF6)
        if k == 0:      # (d1) the blocked noise spectrum is CONSTANT in w
            const_w = max(const_w, float(np.abs(Pk - Pk[0][None]).max()))
        U = Uk(n, k, th6, +1)
        w_unit = max(w_unit, float(np.abs(U @ ct(U) - np.eye(n)).max()))
        # R26: the CORRECT statement is Phi^(k) = U_k* N U_k, e^{+i theta}
        w_conj = max(w_conj, float(np.abs(Pk - ct(U) @ Nc @ U).max()))
        Um = Uk(n, k, th6, -1)
        combos["U N U* , e^{+i th}"] = max(
            combos["U N U* , e^{+i th}"], float(np.abs(Pk - U @ Nc @ ct(U)).max()))
        combos["U* N U , e^{-i th}"] = max(
            combos["U* N U , e^{-i th}"], float(np.abs(Pk - ct(Um) @ Nc @ Um).max()))
        combos["U N U* , e^{-i th}"] = max(
            combos["U N U* , e^{-i th}"], float(np.abs(Pk - Um @ Nc @ ct(Um)).max()))
        ev = np.sort(np.linalg.eigvalsh(0.5 * (Pk + ct(Pk))), axis=1)
        w_eig = max(w_eig, float(np.abs(ev - evN[None, :]).max()))
w_wrong = max(combos.values())
hull = []
for n in (2, 3, 4, 6, 8):
    B = 24; M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    blk = rand_block(n, rng6)
    epsN = float(np.linalg.eigvalsh(blk[2]).min())
    xs = [to_moments(win, *tile_shift(n, *blk, M, k)) for k in range(n)]
    xbar = mix_moments(xs, [1.0 / n] * n)
    Nbar = noise_from_moments(win, *xbar)
    lo = float(np.linalg.eigvalsh(Nbar[tt:tt + 4 * n, tt:tt + 4 * n]).min())
    Gmax = max(float(np.linalg.eigvalsh(
        x[1][tt:tt + 4 * n, tt:tt + 4 * n]).max()) for x in xs)
    Gbar = float(np.linalg.eigvalsh(xbar[1][tt:tt + 4 * n,
                                            tt:tt + 4 * n]).max())
    hull.append(dict(n=n, eps=epsN, hull_lo=lo, slack=lo - epsN,
                     Gamma_cap=Gmax, Gamma_hull=Gbar))
hull_slack = min(r["slack"] for r in hull)
hull_cap_ok = all(r["Gamma_hull"] <= r["Gamma_cap"] + 1e-12 for r in hull)
# (d4) N > 0 w.l.o.g.: the rate BLOWS UP at the cone boundary
n = 3; B = 24; M = n * B; tt = (B // 2) * n
win = Win.get(M)
Av0, Ay0, _ = rand_block(n, rng6)
brows = []
for e in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8):
    Av, Ay, Nt = tile_shift(n, Av0, Ay0, e * np.eye(n), M, 0)
    brows.append(dict(eps=e, rate=rate_collapse(win, Av, Ay, Nt, 0, tt, n)))
blow = brows[-1]["rate"] - brows[0]["rate"]
vals["s6"] = {"blocked_noise_constant_in_w": const_w, "U_unitary": w_unit,
              "eigenvalue_invariance": w_eig,
              "R26_correct_Ustar_N_U_plus": w_conj,
              "R26_wrong_combinations": combos, "R26_wrong_worst": w_wrong,
              "hull": hull, "hull_min_slack": hull_slack,
              "hull_cap_ok": hull_cap_ok, "boundary": brows,
              "boundary_blowup": blow,
              "bars": {"unit": BAR_S6_UNIT, "eig": BAR_S6_EIG,
                       "conj": BAR_S6_CONJ, "wrong": BAR_S6_WRONG,
                       "hull": BAR_S6_HULL, "blowup": BAR_S6_BLOWUP}}
verdicts["s6_blocked_noise_spectrum_constant_in_w"] = const_w < 1e-12
verdicts["s6_shift_operator_is_unitary"] = w_unit < BAR_S6_UNIT
verdicts["s6_eigenvalues_invariant_over_orbit_and_w"] = w_eig < BAR_S6_EIG
verdicts["s6_R26_conjugation_correct_side_and_sign"] = w_conj < BAR_S6_CONJ
verdicts["s6_R26_wrong_combination_FAILS_by_O1"] = w_wrong > BAR_S6_WRONG
verdicts["s6_hull_floor_and_cap_survive"] = \
    (hull_slack > BAR_S6_HULL) and hull_cap_ok
verdicts["s6_rate_blows_up_at_cone_boundary"] = blow > BAR_S6_BLOWUP
print(f"  blocked noise spectrum CONSTANT in w to {const_w:.1e}; U_k unitary "
      f"to {w_unit:.1e}; eigenvalues identical at every w and every k to "
      f"{w_eig:.1e}", flush=True)
print(f"  R26 -- SIDE AND SIGN: Phi^(k)(theta) = U_k(theta)* N U_k(theta) with "
      f"wrapped entries e^(+i theta) holds to {w_conj:.1e} < "
      f"{BAR_S6_CONJ:.0e}; the other three combinations are FALSE BY O(1) "
      f"(worst {w_wrong:.3e} > {BAR_S6_WRONG:.0e}): " +
      ", ".join(f"{k} {v:.2e}" for k, v in combos.items()), flush=True)
print(f"  one (eps, M) serves the orbit AND its convex hull: min hull floor "
      f"slack {hull_slack:+.4f} > {BAR_S6_HULL:.0e}, cap respected "
      f"{hull_cap_ok}; and N > 0 is w.l.o.g. -- the rate rises "
      f"{brows[0]['rate']:.3f} -> {brows[-1]['rate']:.3f} as lambda_min(N) "
      f"goes 1e-1 -> 1e-8, so the boundary is never active on a minimisation "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ==================================================================== s7
print("[s7] R24 (which psd hypothesis is DEMONSTRATED necessary) and R25 "
      "(F0 as a well-posedness condition) ...", flush=True)
BAR_S7_QPSD_VIOL = 0
BAR_S7_RBREAK = 50
BAR_S7_MOMENTS = 1e-13
BAR_S7_F0 = 0.10
BAR_S7_F0_CLAIM = 0.136
rng7 = np.random.default_rng(31337)


def cstat(h, G, P, Q):
    s1 = np.linalg.slogdet(G - h @ Q @ h.T)
    s2 = np.linalg.slogdet(G - h @ P @ h.T)
    if s1[0] <= 0 or s2[0] <= 0:
        return None
    return s1[1] - s2[1]


def battery(mkQ, trials):
    v = t_ = 0
    worst = -9.9
    for _ in range(trials):
        k = int(rng7.integers(1, 4)); m = int(rng7.integers(1, 4))
        Bp = rng7.standard_normal((k, k)); P = Bp @ Bp.T + 0.2 * np.eye(k)
        Q = mkQ(P, k)
        ha = 0.8 * rng7.standard_normal((m, k))
        hb = 0.8 * rng7.standard_normal((m, k))
        sl = float(10 ** rng7.uniform(-9, 0))
        Ga = ha @ P @ ha.T + sl * np.eye(m)
        Gb = hb @ P @ hb.T + sl * np.eye(m)
        hm = 0.5 * (ha + hb); Gm = 0.5 * (Ga + Gb)
        va, vb, vm = (cstat(ha, Ga, P, Q), cstat(hb, Gb, P, Q),
                      cstat(hm, Gm, P, Q))
        if va is None or vb is None or vm is None:
            continue
        t_ += 1
        g = vm - 0.5 * (va + vb)
        v += g > 1e-9
        worst = max(worst, g)
    return dict(viol=int(v), tot=int(t_), worst=float(worst))


def _indef(P, k):
    ev, U = np.linalg.eigh(P)
    return U @ np.diag(ev * np.where(np.arange(k) % 2 == 0, 0.9, -1.5)) @ U.T


fams = {
    "theorem (Q psd, R psd)": lambda P, k: P @ np.linalg.inv(P + np.eye(k)) @ P,
    "Q'' = -0.2 I   (Q NOT psd, R psd)": lambda P, k: -0.2 * np.eye(k),
    "Q''' = -2 P    (Q NOT psd, R psd)": lambda P, k: -2.0 * P,
    "Q indefinite (+0.9/-1.5 on eig P), R psd": _indef,
    "Q'''' = -(P + I) (Q NOT psd, R psd)": lambda P, k: -(P + np.eye(k)),
}
bat = {}
for tag, f in fams.items():
    bat[tag] = battery(f, 5500)
    print(f"    {tag:<42} {bat[tag]['viol']:>4}/{bat[tag]['tot']:<5} viol, "
          f"worst {bat[tag]['worst']:+.4g}", flush=True)
rbreak = battery(lambda P, k: 1.3 * P, 6000)
print(f"    {'Q_ = 1.3 P  (Q psd, R NOT psd)':<42} {rbreak['viol']:>4}/"
      f"{rbreak['tot']:<5} viol, worst {rbreak['worst']:+.4g}   <-- MUST BREAK",
      flush=True)
q_tot = sum(b["tot"] for t_, b in bat.items() if not t_.startswith("theorem"))
q_viol = sum(b["viol"] for t_, b in bat.items() if not t_.startswith("theorem"))
thm_viol = bat["theorem (Q psd, R psd)"]["viol"]

# R25: outside F0 the moment coordinates are ILL-POSED.  A record
# Yhat = Av V + Ay Y + Au U + Z with Au != 0 leaves A_u INVISIBLE to
# H = Cov(Yhat, W), and tau2 Au Au' can be absorbed into Cov(Z), so (H, Gamma)
# is held EXACTLY fixed while the rate moves.  Two witnesses: a PINNED
# DETERMINISTIC ladder (no randomness at all) and a random battery.
Mf = 24; ttf = 9; perf = 6
winf = Win.get(Mf)
_i = np.arange(Mf); _d = np.subtract.outer(_i, _i)
DET_AV = 0.25 * np.tril(np.cos(_d))
DET_AY = 0.20 * np.tril(np.sin(1.0 + _d))
DET_NF = 0.60
det_rows = []
for sc in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
    Au = sc * np.eye(Mf)
    Ncp = DET_NF * np.eye(Mf) - TAU2 * (Au @ Au.T)
    Hd = H_of(winf, DET_AV, DET_AY)
    Gd = Gam_of(winf, DET_AV, DET_AY, Ncp, Au)
    det_rows.append(dict(
        Au_scale=sc,
        rate=la_definition(winf, DET_AV, DET_AY, Ncp, 0, ttf, perf, Au=Au),
        H_defect=float(np.abs(Hd - H_of(winf, DET_AV, DET_AY)).max()),
        Gamma_defect=float(np.abs(
            Gd - Gam_of(winf, DET_AV, DET_AY,
                        DET_NF * np.eye(Mf))).max())))
det_gap = max(r["rate"] for r in det_rows) - min(r["rate"] for r in det_rows)
det_moments = max(max(r["H_defect"], r["Gamma_defect"]) for r in det_rows)
rng7b = np.random.default_rng(31338)
f0rows = []
worstgap = 0.0
worst_moments = 0.0
for trial in range(12):
    Av0, Ay0, Nc0 = rand_block(Mf, rng7b, scale=0.25, nfloor=0.60, nscale=0.20)
    H = H_of(winf, Av0, Ay0)
    G = Gam_of(winf, Av0, Ay0, Nc0)
    vv = []
    for scale in (0.0, 0.15, 0.30, 0.45, 0.60):
        Au = scale * np.tril(rng7b.standard_normal((Mf, Mf)))
        # hold (H, Gamma) EXACTLY fixed by absorbing tau2 Au Au' into Nc
        Ncp = Nc0 - TAU2 * (Au @ Au.T)
        if np.linalg.eigvalsh(0.5 * (Ncp + Ncp.T)).min() <= 1e-6:
            continue
        Hc = H_of(winf, Av0, Ay0)                 # A_u is invisible to H
        Gc = Gam_of(winf, Av0, Ay0, Ncp, Au)
        eH = float(np.abs(Hc - H).max()); eG = float(np.abs(Gc - G).max())
        r = la_definition(winf, Av0, Ay0, Ncp, 0, ttf, perf, Au=Au)
        vv.append((scale, r, eH, eG))
    if len(vv) < 2:
        continue
    rs = [v_[1] for v_ in vv]
    gap = max(rs) - min(rs)
    worstgap = max(worstgap, gap)
    worst_moments = max(worst_moments, max(max(v_[2], v_[3]) for v_ in vv))
    f0rows.append(dict(gap=gap, rates=rs,
                       moment_defect=max(max(v_[2], v_[3]) for v_ in vv)))
vals["s7"] = {"battery": bat, "R_breaking_control": rbreak,
              "nonpsdQ_chords": q_tot, "nonpsdQ_violations": q_viol,
              "theorem_violations": thm_viol,
              "F0_pinned_ladder": det_rows, "F0_pinned_gap_bits": det_gap,
              "F0_pinned_moment_defect": det_moments,
              "F0_random_worst_gap_bits": worstgap,
              "F0_random_moment_defect": worst_moments, "F0_random_rows": f0rows,
              "bars": {"qpsd": BAR_S7_QPSD_VIOL, "rbreak": BAR_S7_RBREAK,
                       "moments": BAR_S7_MOMENTS, "f0": BAR_S7_F0,
                       "f0_claim": BAR_S7_F0_CLAIM}}
verdicts["s7_R24_R_breaking_control_VIOLATES"] = rbreak["viol"] > BAR_S7_RBREAK
verdicts["s7_R24_Q_breaking_families_do_not_violate"] = \
    (q_viol == BAR_S7_QPSD_VIOL) and (q_tot >= 22000)
verdicts["s7_R24_theorem_hypotheses_zero_violations"] = thm_viol == 0
verdicts["s7_R25_moment_pair_held_identical"] =     max(worst_moments, det_moments) < BAR_S7_MOMENTS
verdicts["s7_R25_F0_is_a_wellposedness_condition"] = det_gap > BAR_S7_F0
verdicts["s7_R25_spread_is_at_least_0136_bits"] = det_gap >= BAR_S7_F0_CLAIM
print(f"  R24: {q_viol} violations over {q_tot} chords across FOUR non-psd-Q "
      f"families with R = P - Q psd, while the R-breaking control gives "
      f"{rbreak['viol']}/{rbreak['tot']} (worst {rbreak['worst']:+.3f}).  "
      f"R = P - Q >= 0 is DEMONSTRATED NECESSARY; Q >= 0 is a hypothesis of "
      f"the PROOF ROUTE (it makes M_Q Loewner-concave), not of the statement",
      flush=True)
print(f"  R25: at (H, Gamma) held identical to "
      f"{max(worst_moments, det_moments):.1e}, the PINNED deterministic "
      f"A_u-ladder moves the rate by {det_gap:.4f} bits and the random "
      f"battery by {worstgap:.4f} bits.  So outside F0 two records with the "
      f"SAME (H, Gamma) differ by AT LEAST 0.136 bits -- printed as a lower "
      f"bound, NEVER as a maximum.  The entry point is the leak leg "
      f"Cov(R,S) = H Sig_W^-1 Sig_WS [{time.time()-t0:.0f}s]", flush=True)

# ==================================================================== s8
print("[s8] R29: the n-UNIFORM blocked spectral floor ...", flush=True)
BAR_S8_FLOOR = 3.0e-3
BAR_S8_SPREAD = 1e-12
BAR_S8_QEXACT = 1e-13
BAR_S8_ZGAP = 1e-2
BAR_S8_WINGAP = 5e-4
rng8 = np.random.default_rng(2024)
NF8 = 512
rows8 = []
for n in (1, 2, 3, 4, 5, 6, 7, 8):
    PhiW, PhiS, PhiWS = model_blocked(n, NF8)
    P = np.linalg.inv(PhiW)
    Q = P @ PhiWS @ np.linalg.inv(PhiS) @ ct(PhiWS) @ P
    R = P - Q
    eQ = float(np.linalg.eigvalsh(0.5 * (Q + ct(Q))).min())
    eR = float(np.linalg.eigvalsh(0.5 * (R + ct(R))).min())
    Qref = np.zeros_like(Q)
    Qref[:, :n, :n] = np.linalg.inv(PhiS)
    dQ = float(np.abs(Q - Qref).max())
    blk = rand_block(n, rng8)
    A = np.concatenate([np.repeat(blk[0][None], NF8, 0),
                        np.repeat(blk[1][None], NF8, 0)], axis=2)
    h = A @ PhiW
    Gam = h @ ct(A) + np.repeat(blk[2][None], NF8, 0)
    MQ = Gam - h @ Q @ ct(h)
    ev, U = np.linalg.eigh(0.5 * (R + ct(R)))
    Rh = U @ (np.sqrt(np.maximum(ev, 0))[:, :, None] * ct(U))
    Z = Rh @ ct(h) @ np.linalg.inv(MQ) @ h @ Rh
    mz = float(np.linalg.eigvalsh(0.5 * (Z + ct(Z))).max())
    rows8.append(dict(n=n, eigmin_Q=eQ, eigmin_R=eR, Q_blockdiag_defect=dQ,
                      max_eig_Z=mz))
floor = min(r["eigmin_R"] for r in rows8)
spread = max(r["eigmin_R"] for r in rows8) - floor
dQmax = max(r["Q_blockdiag_defect"] for r in rows8)
zmax = max(r["max_eig_Z"] for r in rows8)
# the recorded FINITE-WINDOW eigmin(P-Q) decrease is convergence FROM ABOVE
winrows = []
for n in (8, 16, 24, 32):
    win = Win.get(n)
    Pn = win.SWi
    Qn = win.SWi @ win.SWS @ np.linalg.solve(win.SS, win.SWS.T) @ win.SWi
    winrows.append(dict(n=n, eigmin=float(
        np.linalg.eigvalsh(0.5 * (Pn - Qn + (Pn - Qn).T)).min())))
wmono = all(winrows[i]["eigmin"] > winrows[i + 1]["eigmin"]
            for i in range(len(winrows) - 1))
wgap = min(r["eigmin"] for r in winrows) - floor
vals["s8"] = {"blocked": rows8, "floor": floor, "floor_spread_over_n": spread,
              "Q_blockdiag_worst": dQmax, "max_eig_Z": zmax,
              "finite_window": winrows, "window_monotone_decreasing": wmono,
              "window_gap_above_floor": wgap,
              "bars": {"floor": BAR_S8_FLOOR, "spread": BAR_S8_SPREAD,
                       "qexact": BAR_S8_QEXACT, "zgap": BAR_S8_ZGAP,
                       "wingap": BAR_S8_WINGAP}}
verdicts["s8_R29_blocked_floor_uniform_in_w_and_n"] = floor >= BAR_S8_FLOOR
verdicts["s8_R29_floor_is_n_uniform"] = spread < BAR_S8_SPREAD
verdicts["s8_R29_Q_equals_blockdiag_PhiSinv_0"] = dQmax < BAR_S8_QEXACT
verdicts["s8_R29_Z_strictly_below_I"] = (1.0 - zmax) > BAR_S8_ZGAP
verdicts["s8_R29_finite_window_converges_from_above"] = wmono and \
    (wgap > BAR_S8_WINGAP)
print(f"  lambda_min(R(w)) = {floor:.6e} UNIFORMLY in w and in n = 1..8 "
      f"(spread over n {spread:.1e} < {BAR_S8_SPREAD:.0e}), >= "
      f"{BAR_S8_FLOOR:.1e}", flush=True)
print(f"  Q(w) = blockdiag(Phi_S(w)^-1, 0) EXACTLY at every block size: worst "
      f"{dQmax:.2e} < {BAR_S8_QEXACT:.0e}; max eig Z = {zmax:.6f} < 1 "
      f"strictly (gap {1-zmax:.4f} > {BAR_S8_ZGAP:.0e})", flush=True)
print(f"  the recorded finite-window eigmin(P-Q) = " +
      "/".join(f"{r['eigmin']:.3e}" for r in winrows) +
      f" at n = 8/16/24/32 is monotone decreasing ({wmono}) and stays "
      f"{wgap:.2e} ABOVE the blocked floor: CONVERGENCE FROM ABOVE "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ==================================================================== s9
print("[s9] shift-invariance with GENUINE shifts, and the np.roll control "
      "(R27) ...", flush=True)
BAR_S9_SHIFT = 1e-12
BAR_S9_CONE_FRAC = 0.90
BAR_S9_ROLL_REC = 1e-7
rng9 = np.random.default_rng(90210)
worst_fix = 0.0
n_shift = 0
roll_bad = roll_tot = 0
worst_roll = 0.0
roll_cone = roll_cone_tot = 0
for n in (3, 4, 5):
    B = max(10, 90 // n); M = n * B; tt = (B // 2) * n
    win = Win.get(M)
    for Delta in (0, 1, 2):
        blk = rand_block(n, rng9)
        base = None
        for k in range(n):
            Av, Ay, Nc = tile_shift(n, *blk, M, k)
            r = rate_collapse(win, Av, Ay, Nc, Delta, tt, n)
            if base is None:
                base = r
            else:
                worst_fix = max(worst_fix, abs(r - base)); n_shift += 1
        Av0, Ay0, Nc0 = tile_shift(n, *blk, M, 0)
        for k in range(1, n):
            rr = rate_collapse(win, roll_shift(Av0, k), roll_shift(Ay0, k),
                               roll_shift(Nc0, k), Delta, tt, n)
            roll_tot += 1
            roll_bad += abs(rr - base) > 1e-9
            worst_roll = max(worst_roll, abs(rr - base))
        H0, G0 = to_moments(win, Av0, Ay0, Nc0)
        for k in range(1, n):
            Hr = np.hstack([roll_shift(H0[:, :M], k), roll_shift(H0[:, M:], k)])
            Gr = roll_shift(G0, k)
            roll_cone_tot += 1
            if float(np.linalg.eigvalsh(
                    noise_from_moments(win, Hr, Gr)).min()) <= 0:
                roll_cone += 1
vals["s9"] = {"genuine_shift_worst": worst_fix, "shift_cells": n_shift,
              "roll_record_worst": worst_roll, "roll_record_mismatches":
              roll_bad, "roll_record_tot": roll_tot,
              "roll_left_cone": roll_cone, "roll_cone_tot": roll_cone_tot,
              "bars": {"shift": BAR_S9_SHIFT, "cone_frac": BAR_S9_CONE_FRAC,
                       "roll_record": BAR_S9_ROLL_REC}}
verdicts["s9_genuine_shift_invariance"] = worst_fix <= BAR_S9_SHIFT
verdicts["s9_R27_roll_control_leaves_the_cone"] = \
    roll_cone >= BAR_S9_CONE_FRAC * roll_cone_tot
verdicts["s9_R27_roll_is_small_in_RECORD_coordinates"] = \
    worst_roll < BAR_S9_ROLL_REC
print(f"  GENUINE shifts of the bi-infinite period-n record: rate "
      f"shift-invariance worst {worst_fix:.2e} <= {BAR_S9_SHIFT:.0e} over "
      f"{n_shift} shifted cells", flush=True)
print(f"  R27 CONTROL -- np.roll is NOT a shift (Sigma_V is Toeplitz, not "
      f"circulant): {roll_cone}/{roll_cone_tot} rolled (H, Gamma) pairs LEAVE "
      f"THE CONE, so it is a MOMENT-COORDINATE bug; in RECORD coordinates the "
      f"same roll is wrong by only {worst_roll:.2e} < {BAR_S9_ROLL_REC:.0e} "
      f"({roll_bad}/{roll_tot} detectable mismatches), so pre-fix record-space "
      f"numerics are neither over- nor under-condemned [{time.time()-t0:.0f}s]",
      flush=True)

# ---------------------------------------------------------------- report
vals["scope"] = {
    "novelty_sweep": "OWED on the (R1) combination (blocked cyclostationary "
                     "Szego + inf-of-affine leak + matrix "
                     "quadratic-over-linear); NO novelty language is used "
                     "anywhere for this combination",
    "chain": "ONE-DIRECTIONAL: L^inf(Delta) >= Psi(D; Delta).  "
             "'Unconditional' attaches to the CHAIN, never to the Psi value",
    "optimizers": "none -- this file contains no optimizer, no fixed point "
                  "and no root find, so no gate can race a stopping point",
    "widths": "no bracket, width or certificate endpoint is read or gated"}
verdicts = {k: bool(v) for k, v in verdicts.items()}
allpass = all(verdicts.values())
print()
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print(f"VERDICT: {'ALL PASS' if allpass else 'FAIL'} "
      f"{sum(verdicts.values())}/{len(verdicts)}")

out = {"verdict": verdicts, "GO14R1_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14R1-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
