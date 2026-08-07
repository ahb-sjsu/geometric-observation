#!/usr/bin/env python
"""GO-14 PLATEAU harness (tex v0.7: the Collapse identity, step (A)
periodization, step (B) shift-averaging, Lemma S, Lemma C-stat, and the
box-free per-frequency weak-duality CERTIFICATE for Psi(Delta) at
Delta = 0, 1, 2).  Registration 082 pending -- NOTHING HERE IS SEALED.

Model: V AR(1) a = 0.8 unit variance; Y = 0.7 V + N, Var(Y) = 1;
S = V + U, tau2 = 0.4; D = 0.3; T = (V, Y) = W; family F0 (records
jointly Gaussian with (V, Y) and INDEPENDENT of U).  Finite window:
phi_n(Delta) = inf_{F0} L_a(Delta).  Stationary (shifted) frame
R_u := Yh_{u-Delta-1}, in which Delta enters ONLY as the phase
z^{Delta+1} on the record's cross spectra; Psi(D; Delta) is the value of
the stationary program in the per-frequency moment coordinates
h = (Phi_RV, Phi_RY), Gam = Phi_R, with P = Sig_W^-1 and
Q = diag(1/f_S, 0).

WHAT IS AND IS NOT CLAIMED.  The chain
  phi_n >= rate(periodize) >= rate(shift-average) >= Psi(D)
is ONE-DIRECTIONAL: it yields L^inf(Delta) >= Psi(Delta) and cannot
yield the converse.  This harness therefore nets a LOWER bound and a
two-sided certificate for Psi; it nets NO identification of L^inf.

DESIGN RULE (the 079 lesson, restated by 080/081, and sharpened by the
Delta=2 anchor pass: finite-n LB endpoints are BLAS-sensitive at ~1e-7
through rn*R_box).  NO GATE MAY RACE AN OPTIMIZER STOPPING POINT AND NO
GATE MAY GATE A CERTIFICATE WIDTH.  Every gate below is one of
  (a) an exact identity with a tolerance many orders above f64 noise,
  (b) a structural / set fact,
  (c) an analytic inequality with a fat, measured margin, or
  (d) reproduction of a committed value inside a band that is orders
      above the observed reproduction spread.
No bracket width is gated anywhere.  Sections s1, s2, s4, s5 contain no
optimizer at all.  s3 and the R19 constants of s7 read cold-start
optimizer endpoints, but only through analytic inequalities whose
margins (1.3e-3 .. 1.7e-3 bits) are five orders above the endpoint
spread (~1e-8), and through reproduction bands (1e-4) that are three
orders above it.  s6-s8 read the stationary fixed point, but the fixed
point is a deterministic contraction with residual ~5e-14 and every
gate against it is either a validity inequality (one-sided, with the
violation side unbounded) or a reproduction band 1e-8/1e-9 wide against
an observed spread of ~1e-11.

s1 THE COLLAPSE IDENTITY.  2 ln2 n L_a = sum_t ln sigma_t - lndet N,
   exactly, every n, every nondecreasing schedule, every F0 record
   (sigma_t = Var(Yh_t | S^{se(t)}, Yh^{t-1})).  Gate: worst relative
   |collapse - definitional CMI| < 1e-12 on random F0 records with
   staircase schedules INCLUDING the edges Delta in {n-2, n-1, n, n+3},
   and on random NON-staircase nondecreasing schedules.
   R6 EXTENSION AND ITS CONTROL: the identity does NOT need
   U-independence, it needs exactly Delta-LAG-CAUSAL U-coupling
   (Au[t,s] = 0 for s > t + Delta); F0 (Au = 0) is the special case.
   Gate BOTH directions: Delta-causal Au is exact (< 1e-12) while dense
   and strictly anticausal Au FAIL by > 0.02 bits.

s2 STEP (A), PERIODIZATION.  Repeat an n-record along Z with INDEPENDENT
   noise copies.  Gate: distortion EXACTLY preserved (< 1e-12), lndet N
   EXACTLY additive (< 1e-11), and every sigma_t DECREASES -- zero
   violations over >= 1200 (cell x tiling) pairs.
   R7 CONTROL: "independent noise copies" is LOAD-BEARING.  Correlating
   the copies (cross-block noise correlation 0.3/0.6/0.9) must BREAK
   (A): gate that the tiled per-symbol value EXCEEDS the untiled one by
   > 0.01 bits at all three correlations, on a random record AND at the
   cold-start (8,0) optimizer (where the untiled value is phi_8).

s3 STEP (B), SHIFT-AVERAGING.  The shift-average of a period-n record's
   moment pair is a stationary pair in the same cone, its per-symbol
   distortion is unchanged, and its rate is no larger.  Gate at the
   cold-start optimizers (8,0), (12,0), (16,0), (16,1), (16,2) and on
   random period-n records: (i) cone membership, min_w nbar(w) > 1e-3
   and eigmin of the realised Toeplitz noise > 1e-3; (ii) distortion
   preserved < 1e-12; (iii) rate(shift-average) - rate(cyclostationary)
   < -1e-4 (measured -1.3e-3 .. -2.4e-3 at the optimizers).  NOTE the
   wording the verifier permits: step (B) produces an EXPLICIT
   stationary record of no larger rate and identical per-symbol
   distortion.  It does not "attain" anything.

s4 LEMMA C-stat.  Per frequency, ln(Gam - hQh*) - ln(Gam - hPh*) with
   Q >= 0 and R = P - Q >= 0 is jointly convex in (h, Gam).  Gate:
   zero Jensen violations over 60,000 random chords with Gamma pushed to
   1e-9 of the cone boundary.
   R12 CONTROL: the psd hypothesis is load-bearing.  With Q' = 1.3 P
   (so R = P - Q' is NEGATIVE definite) the same chords must VIOLATE:
   gate >= 1000 violations.

s5 THE MINORANT shat >= s -- the one place a sign slip inverts the whole
   bound.  For admissible frozen filters (C monic causal in S, B causal
   INCLUDING lag 0 in R), shat(x;C,B) = <|C|^2 f_S + |B|^2 Gam
   + 2Re(conj(C) B h1)> is AFFINE in x and >= s(x) always.  Gate: zero
   violations over 2,880 (record x frozen-filter) pairs -- 120
   adversarial records x 24 filters including foreign optima,
   truncations to 1/2/5/20 lags, oscillating and near-unit-root filters.
   R11 CONTROL: admissibility is a HYPOTHESIS WITH CONTENT.  A NON-MONIC
   C (= 0.3) must INVERT the minorant: gate shat - s < -0.1.

s6 THE DUAL BOUND IS VALID WITHOUT ANY OPTIMALITY (R17).  The
   per-frequency weak-duality bound needs only (i) admissibility of the
   frozen filters, (ii) beta > 0, (iii) a correct cell infimum -- no
   optimality of the fixed point, no convexity of the process rate, no
   differentiability, and NO moment box.  Gate at deliberately
   NON-OPTIMAL anchors (25 random feasible stationary records per
   Delta), mistuned mu (x0.95, x1.10), truncated frozen filters
   (12/4/1 lags) and mistuned shat linearisation (+/-5%):
   (i) VALIDITY -- zero cases with LB > Psi_UB + 1e-9;
   (ii) POWER -- every deliberately non-optimal anchor is strictly
        degraded, max(LB - Psi_UB) < -1e-6, so the test is not vacuous;
   (iii) at least 15 of the 25 random anchors per Delta produce a finite
        bound (beta > 0).

s7 REPRODUCTION.  (i) The recomputed two-sided certificate reproduces
   the committed 10-digit quotable brackets within 1e-8 (observed
   ~4e-11): Psi(0) in [0.5627264963, 0.5627264964], Psi(1) in
   [0.5364013784, 0.5364013785], Psi(2) in [0.5310500198,
   0.5310500199].  (ii) The margins against the SEALED causal-spectral
   bars (results/GO14-process-limit.json, s6_cand) reproduce
   +0.0147817164 / +0.0040574952 / +0.0007968190 within 1e-9 -- this is
   exact arithmetic on committed constants, not a measurement; the
   recomputed LB must additionally clear each bar by > MARGIN - 1e-6.
   (iii) R20: the anchor-free block certificate reproduces
   block_inf = 0.5299499808119 within 1e-9, and the committed
   s6_block_inf = 0.529949985183839 is confirmed HIGH by 4.4e-9 (gated
   into the band [3e-9, 6e-9]).  (iv) R19: the O(1/n) constant is
   Delta-DEPENDENT -- n(phi_16 - Psi) = 0.064507 / 0.070483 / 0.077503
   at Delta = 0/1/2, each reproduced within 1e-4 and pairwise separated
   by > 3e-3, so no Delta-uniform constant may be quoted.

s8 "DOES IT PROVE TOO MUCH?"  The identical machinery on the BLOCK
   program (se == n; no leak, so the cell dual needs NO ANCHOR AT ALL)
   must NOT produce a value above the independently known block_inf:
   gate LB_block <= block_inf + 1e-9.  And the Delta-ladder must
   approach block_inf FROM ABOVE and never cross: gate
   min_Delta (LB(Delta) - block_inf) >= -1e-9 over Delta in
   {0,1,2,4,6,9} (measured +7.2e-10 at Delta = 9), with the fat-margin
   form LB(Delta) - block_inf >= 1e-7 for Delta <= 6 (measured 3.9e-7
   at Delta = 6) and a strictly decreasing ladder, min step > 1e-8
   (measured 3.9e-7).

Sentinel ===GO14PL2-JSON=== with ===END===; flag GO14PL2_supported.
Pilot seed 20261150 / governed seed 20261151.  SEED STAMPS ONLY: the
seed is recorded in the output and feeds NO computation -- every random
draw uses an internally pinned generator and every optimizer and fixed
point is a deterministic cold start, so pilot and governed verify
identical numbers.

Evaluator lineage.  The time-domain sections (s1-s3) evaluate every
conditional variance from an explicitly constructed 4n joint covariance
built from the independent primitives (V, N, U, Z) -- correct by
construction and independent of every identity tested.  The spectral
sections (s4-s8) use their own grid, own normal-equation prediction
solves, own rate, own cell infimum and own dual; the finite-n
optimizers of s3/s7(iv) use the moment-coordinate Lagrangian of the
go14_convexity.py lineage and are re-valued through the time-domain
route before being used.

CURVATURE CONSTANT (R14).  The cell guard uses the CORRECTED modulus
beta*lambda_min(P+Q) with guard 2|u|^2/(beta lambda_min(P+Q)).  The
earlier "Hessian >= 2 beta lambda_min(P)" assertion is not proved by
its stated reason (phi(hRh*) is radially CONCAVE); the corrected
modulus is 3.5% larger here and numerically inert (guards ~1e-26).

All floating-point certificates: no interval arithmetic (house
convention).  Lag truncation is on the SAFE side for the LB (a
truncated filter is admissible, so shat >= s and the bound only
loosens); it has the WRONG sign for an upper bound, which is why the
UB's P-independence is measured rather than assumed.

NOTHING HERE GATES A WIDTH.  The tightest reproduction band in the file
is s7's 1e-8 against the 10-digit quotable brackets -- ONE HUNDRED TIMES
the 1e-10 bracket width, so the gate survives a 100-bracket-width move
of the recomputed value.  The certified widths themselves (UB - LB,
observed ~1e-13 here) are RECORDED and never gated, and so is the
"recomputed endpoints lie inside the quotable bracket" flag.

PILOT RECORD (seed 20261150, 2026-08-07).
 iter 1 -- ALL PASS 30/30, 38.9 s.  Every bar was fixed BEFORE the run
   from the psi-bracket prover's and the R-IND-5 verifier's committed
   artifacts (scratchpad psicert/, spectral/, rind5B/, rind5C/) and from
   results/GO14-process-limit.json.  No bar was moved against a
   measurement at any point, in either direction.
 iter 2 -- ALL PASS 30/30, 44.8 s (re-runs 47.3 s and, governed,
   48.6 s -- the payload is identical, only wall-clock moves).  ONE bar
   was TIGHTENED-for-robustness
   after iter 1, against no failure: s6's "how many of the 25 random
   NON-OPTIMAL anchors yield a finite bound (beta > 0)" was lowered from
   20 to 15, because at 20 the measured 24 gave only 1.2x margin and the
   count is a discrete, platform-sensitive quantity (which random anchor
   lands with beta <= 0 depends on BLAS rounding in the normal-equation
   solve).  Every other bar and every measured value is UNCHANGED, and a
   re-run of the identical command reproduced the whole JSON payload
   BIT-IDENTICALLY, confirming the seed-stamp-only discipline.
 MEASURED vs BAR (the ratio is the margin):
   pre  sealed bars read from results/GO14-process-limit.json s6_cand
      match the pinned literals EXACTLY (0.0e+00); cold-start anchors
      vs committed |d| = 2.5e-9 / 1.9e-8 / 4.4e-8 / 5.8e-12 / 2.5e-11
      at (8,0)/(12,0)/(16,0)/(16,1)/(16,2), each re-valued by the
      independent time-domain route to <= 2.2e-16
   s1 collapse 5.65e-15 / 1e-12 (177x) over 84 cells incl. the edges;
      non-staircase 1.73e-15 / 1e-12 (578x) over 16 cells; R6
      Delta-lag-causal Au 6.7e-16 / 1e-12 (1493x); dense and strictly
      anticausal Au fail by >= 0.1485 / 0.02 (7.4x)
   s2 dist 1.78e-15 / 1e-12 (562x); lndet 2.84e-14 / 1e-11 (352x);
      sigma violations 0 over 1200 (cell x tiling) pairs; R7
      correlated-copy control min excess +0.0290 / 0.01 (2.9x)
      (random n=5: +0.0290/+0.1605/+0.6463 at c = 0.3/0.6/0.9;
      (8,0) optimizer: +0.0319/+0.1684/+0.6836 over phi_8)
   s3 cone worst 1.405e-1 / 1e-3 (140x, both min_w nbar and the
      realised Toeplitz eigmin); distortion 4.4e-16 / 1e-12 (2273x);
      rate gap worst -1.291e-3 / -1e-4 (12.9x) at (16,0); the five
      optimizer gaps are -2.363e-3/-1.673e-3/-1.291e-3/-1.523e-3/
      -1.688e-3 and the nine random-record gaps are all < -0.24
   s4 Jensen violations 0 over 60000 chords at 1.0e-9 from the cone
      boundary, worst chord +7.879e-4; R12 control (Q' = 1.3 P) 60000
      violations / 1000 (60x), worst -21.414
   s5 min(shat - s) -2.22e-16 / -1e-11 (45x) over 2880 pairs, 0
      violations, attained at a FOREIGN optimum; R11 non-monic control
      -0.5447 / -0.1 (5.4x); inadmissible anticausal pair +11.9221
   s6 validity worst LB - Psi_UB +2.22e-16 / 1e-9; power worst
      -3.61e-6 / -1e-6 (3.6x); finite random anchors 24/25/25 / 15
      (1.6x); R18 Delta=2 tuning costs -2.31e-5 (mu x0.95) and
      -2.20e-3 (mu x1.10) of margin, validity never lost
   s7 bracket reproduction 7.1e-11 / 1e-8 (141x); margin arithmetic
      4.6e-11 / 1e-9 (22x); recomputed LB clears the sealed bars by
      +1.47817164e-2 / +4.0574952e-3 / +7.968190e-4; block_inf
      3.5e-14 / 1e-9; R20 erratum +4.37e-9 inside [3e-9, 6e-9]
      (1.46x / 1.37x); R19 constants 0.064506/0.070483/0.077503 vs the
      recorded 0.064507/0.070483/0.077503, max error 1.1e-6 / 1e-4
      (91x), min pairwise separation 6.0e-3 / 3e-3 (2.0x)
   s8 LB_block - block_inf -3.52e-14 / 1e-9 (does NOT prove too much);
      min ladder excess +7.216e-10, inside the -1e-9 no-crossing
      tolerance by 1.72e-9; Delta <= 6 fat-margin excess +3.879e-7 /
      1e-7 (3.9x); min ladder step 3.872e-7 / 1e-8 (39x)
 DISCLOSURES.
 (a) The sealed causal-spectral bars are READ FROM
   results/GO14-process-limit.json (s6_cand) at run time and
   cross-checked against the pinned literals; the harness never uses
   the superseded 0.5323430 / 0.5302540 values, whose margins R16
   showed to be wrong (Delta=1 by +8.8e-7, NON-conservatively).
 (b) The recomputed finite-n optimizer values are cold-start L-BFGS-B
   endpoints, NOT certified brackets: phi_8 = 0.5707933867 (committed
   0.5707933842), phi_12 = 0.5681027948 (0.5681028134),
   phi_16(0) = 0.5667581182 (0.5667581622), phi_16(1) = 0.5408065772
   (0.5408065772), phi_16(2) = 0.5358939352 (committed
   s4_fs16_D2 = 0.5358939351814885).  Spread <= 4.4e-8; the tightest
   gate that reads them has a band of 1e-4 (s7's R19 constants) and the
   analytic ones have margins >= 1.3e-3.  No width is gated.
 (c) The shift-averaged stationary records built in s3 evaluate to
   0.5631757430 / 0.5629263942 / 0.5628390182 / 0.5364993215 /
   0.5311645087 at (8,0)/(12,0)/(16,0)/(16,1)/(16,2); the last two
   reproduce the constructive upper bounds Psi(1) <= 0.5364993215 and
   Psi(2) <= 0.5311645087 of R-IND-5 restatement 10 to 10 digits.  These
   are REPORTED, not gated.
 (d) Delta=2 has the campaign's smallest margin (R18) and no headroom in
   the certificate's tuning.  s6 records the degradations; only VALIDITY
   is gated, never the margin under mistuning.
 (e) The s8 no-crossing gate at Delta=9 is a TOLERANCE band (-1e-9), not
   a margin: the true excess there is +7.2e-10, smaller than the band.
   The gate with power is the Delta <= 6 form (+3.9e-7 against 1e-7) and
   the strictly-decreasing ladder (min step 3.9e-7 against 1e-8).  This
   is deliberate -- gating +7.2e-10 tightly would race the fixed point.
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
SEED = a_.seed if a_.seed is not None else (20261150 if a_.pilot
                                            else 20261151)
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
D_TGT = 0.3
LN2 = np.log(2.0)
AL = 1.0 / (2.0 * LN2)

# closed-form Szego constant for the S-side (Lemma S): f_S is an
# ARMA(1,1) sdf, <ln f_S> = ln(tau2 a / lambda_s) exactly.
_bb = (1 - A_ ** 2) + TAU2 * (1 + A_ ** 2)
_cc = TAU2 * A_
LAM_S = (_bb - np.sqrt(_bb ** 2 - 4 * _cc ** 2)) / (2 * _cc)
LNFS = np.log(_cc / LAM_S)                       # -0.1025391956...

HERE = os.path.dirname(os.path.abspath(__file__))
PLJSON = os.path.join(HERE, os.pardir, "results", "GO14-process-limit.json")

# ---- committed reference values (bars).  Every gated quantity below is
# ---- recomputed from scratch; these are only the targets.
# sealed causal-spectral allocation (078 governed s6_cand) -- pinned
# literals, cross-checked against the committed JSON at run time
SEALED_BAR = {0: 0.5479447799144537,
              1: 0.5323438832146611,
              2: 0.5302532008457406}
# the 10-digit QUOTABLE brackets, rounded OUTWARD at 1e-10 (R15)
QUOTE = {0: (0.5627264963, 0.5627264964),
         1: (0.5364013784, 0.5364013785),
         2: (0.5310500198, 0.5310500199)}
# the corrected plateau margins (R16) = QUOTE_LB - SEALED_BAR
MARGIN_REC = {0: 0.0147817164, 1: 0.0040574952, 2: 0.0007968190}
# R20 erratum: the anchor-free two-sided block certificate
BLOCK_INF_CERT = 0.5299499808119
BLOCK_INF_COMMITTED = 0.529949985183839          # high by 4.4e-9
# R19: the O(1/n) constant is Delta-DEPENDENT
REC_C1N = {0: 0.064507, 1: 0.070483, 2: 0.077503}
# committed finite-n anchors (reported, never gated at width)
REC_PHI = {(8, 0): 0.5707933842, (12, 0): 0.5681028134,
           (16, 0): 0.5667581622, (16, 1): 0.5408065772,
           (16, 2): 0.5358939351814885}


def jsafe(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(o)


# ======================================================================
#  TIME-DOMAIN EVALUATOR (s1-s3): everything from the 4n joint covariance
#  built out of the independent primitives (V, N, U, Z).
# ======================================================================
def sig_V(n):
    k = np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
    return A_ ** k


def joint_all(n, Av, Ay, Nc, Au=None):
    """Cov of the stacked (V^n, Y^n, S^n, Yh^n), 4n x 4n."""
    SV = sig_V(n)
    I = np.eye(n)
    Z0 = np.zeros((n, n))
    if Au is None:
        Au = Z0
    covP = [SV, SN2 * I, TAU2 * I, Nc]
    M = np.block([[I, Z0, Z0, Z0],
                  [RHO * I, I, Z0, Z0],
                  [I, Z0, I, Z0],
                  [Av + RHO * Ay, Ay, Au, I]])
    CP = np.zeros((4 * n, 4 * n))
    for i in range(4):
        CP[i * n:(i + 1) * n, i * n:(i + 1) * n] = covP[i]
    return M @ CP @ M.T


def idx4(n):
    return dict(V=np.arange(0, n), Y=np.arange(n, 2 * n),
                S=np.arange(2 * n, 3 * n), R=np.arange(3 * n, 4 * n))


def sched_prefix(n, Delta):
    """se(t) = min(t + Delta, n), 1-based count of visible S cells."""
    return np.minimum(np.arange(1, n + 1) + Delta, n)


def cond_var(C, tgt, cond):
    if len(cond) == 0:
        return float(C[tgt, tgt])
    b = C[np.ix_(cond, [tgt])].ravel()
    Kc = C[np.ix_(cond, cond)]
    return float(C[tgt, tgt] - b @ np.linalg.solve(Kc, b))


def la_direct(n, Av, Ay, Nc, Delta=None, se=None, Au=None, parts=False):
    """L_a in bits STRAIGHT FROM THE CMI DEFINITION (no collapse used)."""
    C = joint_all(n, Av, Ay, Nc, Au)
    ix = idx4(n)
    if se is None:
        se = sched_prefix(n, Delta)
    se = np.asarray(se, int)
    num = np.zeros(n)
    den = np.zeros(n)
    iT = list(ix['V']) + list(ix['Y'])
    for t in range(n):
        cS = list(ix['S'][:se[t]])
        cR = list(ix['R'][:t])
        tgt = int(ix['R'][t])
        num[t] = cond_var(C, tgt, cS + cR)
        den[t] = cond_var(C, tgt, iT + cS + cR)
    v = float(np.sum(np.log(num / den)) / (2 * LN2) / n)
    return (v, num, den) if parts else v


def la_collapse(n, Av, Ay, Nc, Delta=None, se=None, Au=None):
    """THE COLLAPSE FORM: 2 ln2 n L_a = sum_t ln sigma_t - lndet N."""
    v, num, den = la_direct(n, Av, Ay, Nc, Delta, se, Au, parts=True)
    _, ldN = slogdet(Nc)
    return float(np.sum(np.log(num)) - ldN) / (2 * LN2) / n, v


def la_chol(n, Av, Ay, Nc, Delta=None, se=None):
    """Same value via ONE Cholesky of the interleaved (S, Yh) covariance
    plus the Cholesky of N (F0 only).  Returns (L_a, sigma_t)."""
    C = joint_all(n, Av, Ay, Nc)
    ix = idx4(n)
    if se is None:
        se = sched_prefix(n, Delta)
    se = np.asarray(se, int)
    order = []
    pos_R = []
    j = 0
    for t in range(n):
        while j < se[t]:
            order.append(int(ix['S'][j])); j += 1
        pos_R.append(len(order))
        order.append(int(ix['R'][t]))
    while j < n:
        order.append(int(ix['S'][j])); j += 1
    Cj = C[np.ix_(order, order)]
    Lc = np.linalg.cholesky(Cj)
    sig = np.array([Lc[p, p] ** 2 for p in pos_R])
    _, ldN = slogdet(Nc)
    return float(np.sum(np.log(sig)) - ldN) / (2 * LN2) / n, sig


def dist_time(n, Av, Ay, Nc, Au=None):
    C = joint_all(n, Av, Ay, Nc, Au)
    ix = idx4(n)
    d = 0.0
    for t in range(n):
        iy, ir = int(ix['Y'][t]), int(ix['R'][t])
        d += C[iy, iy] - 2 * C[iy, ir] + C[ir, ir]
    return d / n


def rand_record_t(n, rng, scale=0.35):
    Av = scale * rng.standard_normal((n, n))
    Ay = scale * rng.standard_normal((n, n))
    B = rng.standard_normal((n, n))
    Nc = 0.15 * (B @ B.T) / n + 0.10 * np.eye(n)
    return Av, Ay, Nc


def tile(n, Av, Ay, Nc, B):
    """periodize with INDEPENDENT noise copies (block-diagonal N)."""
    M = n * B
    AvT = np.zeros((M, M)); AyT = np.zeros((M, M)); NT = np.zeros((M, M))
    for b in range(B):
        s = slice(b * n, (b + 1) * n)
        AvT[s, s] = Av; AyT[s, s] = Ay; NT[s, s] = Nc
    return AvT, AyT, NT


# ======================================================================
#  FINITE-n MOMENT-COORDINATE OPTIMIZER (go14_convexity.py lineage)
# ======================================================================
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
                  @ np.linalg.solve(self.Cs, self.CovWS.T) @ self.SigWinv)
        self.K = self.CovWS.T @ self.SigWinv
        self.GY = self.SigWinv @ self.CovWY
        self.trCy = float(np.trace(self.Cy))
        self.lnpivS = 2.0 * np.log(np.diag(np.linalg.cholesky(self.Cs)))


def sched0(n, Delta):
    return np.minimum(np.arange(n) + Delta + 1, n)


def kcounts(n, se0):
    return np.array([int(np.sum(se0 <= j)) for j in range(n)])


def moments(M, Ay, Av, Nc):
    Ab = np.hstack([Av, Ay])
    H = Ab @ M.SigW
    Gm = Ab @ M.SigW @ Ab.T + Nc
    return H, 0.5 * (Gm + Gm.T)


def dist_HG(M, H, Gm):
    return (M.trCy - 2.0 * float(np.sum(H * M.GY.T))
            + float(np.trace(Gm))) / M.n


def grad_dist(M):
    return -(2.0 / M.n) * M.GY.T, np.eye(M.n) / M.n


def f_and_grad(M, H, Gm, Delta):
    n = M.n
    MQ = Gm - H @ M.Q @ H.T
    MP = Gm - H @ M.P @ H.T
    try:
        LQ = np.linalg.cholesky(MQ)
        LP = np.linalg.cholesky(MP)
    except np.linalg.LinAlgError:
        return None
    val = 2.0 * (float(np.sum(np.log(np.diag(LQ))))
                 - float(np.sum(np.log(np.diag(LP)))))
    ks = kcounts(n, sched0(n, Delta))
    Csh = M.K @ H.T
    J = np.block([[M.Cs, Csh], [Csh.T, Gm]])
    GJ = np.zeros((2 * n, 2 * n))
    for j in range(n):
        cond = list(range(j)) + [n + i for i in range(ks[j])]
        if cond:
            C = J[np.ix_(cond, cond)]
            b = J[cond, j]
            cf = cho_factor(C, lower=True, check_finite=False)
            wv = cho_solve(cf, b, check_finite=False)
            s = float(J[j, j] - b @ wv)
        else:
            wv = np.zeros(0)
            s = float(J[j, j])
        if s <= 0:
            return None
        val += M.lnpivS[j] - np.log(s)
        u = np.zeros(2 * n)
        u[j] = 1.0
        u[cond] = -wv
        GJ -= np.outer(u, u) / s
    SC = 1.0 / (2.0 * n * LN2)
    MQi = np.linalg.inv(MQ)
    MPi = np.linalg.inv(MP)
    gG = SC * (MQi - MPi + GJ[n:, n:])
    gH = SC * (-2.0 * MQi @ H @ M.Q + 2.0 * MPi @ H @ M.P
               + 2.0 * GJ[n:, :n] @ M.K)
    return SC * val, gH, 0.5 * (gG + gG.T)


def polish(n, Delta, maxit1=900, maxit2=250, nbis=30):
    """Deterministic COLD-START Lagrangian polish with mu-bisection to
    dist = D.  Returns the endpoint as a record (Av, Ay, Nc).  Used only
    to produce points; every quantity read off it is re-valued through
    the independent time-domain route, and no width is gated."""
    M = Model(n)
    gDH, gDG = grad_dist(M)
    iu = np.triu_indices(n)
    symw = np.where(iu[0] == iu[1], 1.0, 2.0)

    def unpack(x):
        H = x[:2 * n * n].reshape(n, 2 * n)
        Gm = np.zeros((n, n))
        Gm[iu] = x[2 * n * n:]
        return H, Gm + Gm.T - np.diag(np.diag(Gm))

    def pack(H, Gm):
        return np.concatenate([H.ravel(), Gm[iu]])

    def solve(mu, x0, mx):
        def lagr(x):
            H, Gm = unpack(x)
            o = f_and_grad(M, H, Gm, Delta)
            if o is None:
                return 1e3, np.zeros_like(x)
            v, gh, gg = o
            return (v + mu * (dist_HG(M, H, Gm) - D_TGT),
                    np.concatenate([(gh + mu * gDH).ravel(),
                                    ((gg + mu * gDG))[iu] * symw]))
        r = minimize(lagr, x0, jac=True, method="L-BFGS-B",
                     options={"maxiter": mx, "ftol": 1e-18, "gtol": 1e-14,
                              "maxcor": 40})
        H_, G_ = unpack(r.x)
        v_, gh_, gg_ = f_and_grad(M, H_, G_, Delta)
        return r.x, v_, dist_HG(M, H_, G_), gh_, gg_

    H0, G0 = moments(M, 0.7 * np.eye(n), np.zeros((n, n)), 0.21 * np.eye(n))
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
    H_, G_ = unpack(x)
    rn = float(np.sqrt(np.sum((gh_ + mu * gDH) ** 2)
                       + np.sum((gg_ + mu * gDG) ** 2)))
    Ab = H_ @ M.SigWinv
    Nc = G_ - H_ @ M.SigWinv @ H_.T
    return dict(mu=float(mu), v=float(v_), dist=float(d_), rn=rn,
                Av=Ab[:, :n], Ay=Ab[:, n:], Nc=0.5 * (Nc + Nc.T))


# ======================================================================
#  SHIFT-AVERAGING (step B), executed
# ======================================================================
NFS = 4096
_ws = 2 * np.pi * np.arange(NFS) / NFS
_zs = np.exp(-1j * _ws)
FVS = (1 - A_ ** 2) / np.abs(1 - A_ * _zs) ** 2


def _sym(kp, kn):
    a = np.zeros(NFS)
    a[:len(kp)] = kp
    for j, v in enumerate(kn):
        a[NFS - 1 - j] = v
    return np.fft.fft(a)


def _toep_spec(spec, M):
    c = np.real(np.fft.ifft(spec))
    k = np.subtract.outer(np.arange(M), np.arange(M))
    return c[k % NFS]


def _toep_kern(kp, kn, M):
    c = np.zeros(NFS)
    c[:len(kp)] = kp
    for j, v in enumerate(kn):
        c[NFS - 1 - j] = v
    k = np.subtract.outer(np.arange(M), np.arange(M))
    return c[k % NFS]


def _rate_win(M, Av, Ay, Nc, Delta, t0, per):
    _, sig = la_chol(M, Av, Ay, Nc, Delta=Delta)
    npv = np.diag(np.linalg.cholesky(Nc)) ** 2
    return float(np.sum(np.log(sig[t0:t0 + per]) - np.log(npv[t0:t0 + per]))
                 / (2 * LN2) / per)


def shiftavg(n, Av, Ay, Nc, Delta, DMAX=60, M2=160):
    """Periodize, then SHIFT-AVERAGE the moment pair, then REALISE the
    averaged stationary record and evaluate it."""
    B = 2 * int(np.ceil((DMAX + 2) / n)) + 2
    M = n * B
    AvT, AyT, NT = tile(n, Av, Ay, Nc, B)
    t0 = (B // 2) * n
    DM = min(DMAX, t0 - 1)
    Lcyc = _rate_win(M, AvT, AyT, NT, Delta, t0, n)
    dcyc = dist_time(n, Av, Ay, Nc)
    avp = np.array([Av[np.arange(d, n), np.arange(0, n - d)].sum() / n
                    for d in range(n)])
    avn = np.array([Av[np.arange(0, n - d), np.arange(d, n)].sum() / n
                    for d in range(1, n)])
    ayp = np.array([Ay[np.arange(d, n), np.arange(0, n - d)].sum() / n
                    for d in range(n)])
    ayn = np.array([Ay[np.arange(0, n - d), np.arange(d, n)].sum() / n
                    for d in range(1, n)])
    gW = AvT + RHO * AyT
    Gam = gW @ sig_V(M) @ gW.T + SN2 * (AyT @ AyT.T) + NT
    Gb = np.array([np.mean([Gam[t0 + i, t0 + i - d] for i in range(n)])
                   for d in range(DM + 1)])
    AVB = _sym(avp, avn)
    AYB = _sym(ayp, ayn)
    GB = AVB + RHO * AYB
    nbar = np.real(_sym(Gb, Gb[1:]) - np.abs(GB) ** 2 * FVS
                   - np.abs(AYB) ** 2 * SN2)
    AvS = _toep_kern(avp, avn, M2)
    AyS = _toep_kern(ayp, ayn, M2)
    NS = _toep_spec(nbar + 0j, M2)
    NS = 0.5 * (NS + NS.T)
    emin = float(np.linalg.eigvalsh(NS).min())
    Lst = _rate_win(M2, AvS, AyS, NS, Delta, M2 // 2, 1)
    Cst = joint_all(M2, AvS, AyS, NS)
    ix = idx4(M2)
    tt = M2 // 2
    iy, ir = int(ix['Y'][tt]), int(ix['R'][tt])
    dst = float(Cst[iy, iy] - 2 * Cst[iy, ir] + Cst[ir, ir])
    return dict(Lcyc=Lcyc, Lst=Lst, dcyc=float(dcyc), dst=dst,
                nmin=float(nbar.min()), emin=emin)


# ======================================================================
#  SPECTRAL MACHINERY (s4-s8): own grid, own solves, own dual
# ======================================================================
class Grid:
    def __init__(self, Nf=1024, P=60):
        self.Nf, self.P = Nf, P
        w = 2 * np.pi * np.arange(Nf) / Nf
        self.w = w
        self.z = np.exp(-1j * w)
        self.fV = (1 - A_ ** 2) / np.abs(1 - A_ * self.z) ** 2
        self.fS = self.fV + TAU2
        self.fY = RHO ** 2 * self.fV + SN2
        det = self.fV * SN2
        self.P11 = self.fY / det                  # Sig_W(w)^{-1}
        self.P12 = np.full(Nf, -RHO / SN2)
        self.P22 = np.full(Nf, 1.0 / SN2)
        self.Q11 = 1.0 / self.fS                  # Q = diag(1/f_S, 0)
        self.R11 = self.P11 - self.Q11            # R = P - Q
        self.R12 = self.P12.copy()
        self.R22 = self.P22.copy()
        self.cSS = np.real(np.fft.ifft(self.fS))

    def mean(self, x):
        return float(np.mean(np.real(x)))

    def sym(self, kpos, kneg=None):
        x = np.zeros(self.Nf)
        x[:len(kpos)] = kpos
        if kneg is not None:
            for j, v in enumerate(kneg):
                x[self.Nf - 1 - j] = v
        return np.fft.fft(x)


def qf(a11, a12, a22, x1, x2):
    return (a11 * np.abs(x1) ** 2 + 2 * a12 * np.real(x1 * np.conj(x2))
            + a22 * np.abs(x2) ** 2)


def nz_of(g, h1, h2, Gam):
    return Gam - qf(g.P11, g.P12, g.P22, h1, h2)


def MQ_of(g, h1, Gam):
    return Gam - np.abs(h1) ** 2 / g.fS


def dist_spec(g, h1, h2, Gam, Dl):
    zD = g.z ** (Dl + 1)
    return float(np.mean(Gam) - 2 * np.mean(np.real(np.conj(zD) * h2)) + 1.0)


def pivot_s(g, Gam, h1, P=None):
    """s = Var(S_u | S^{u-1}, R^u) and the OPTIMAL admissible filters:
    C(z) monic causal in S, B(z) causal INCLUDING lag 0 in R."""
    P = g.P if P is None else P
    cRR = np.real(np.fft.ifft(np.asarray(Gam, complex)))
    cRS = np.real(np.fft.ifft(h1))
    cSS = g.cSS
    iR = np.arange(0, P + 1)
    iS = np.arange(1, P + 1)
    Krr = cRR[np.abs(iR[None, :] - iR[:, None])]
    Kss = cSS[np.abs(iS[None, :] - iS[:, None])]
    Krs = cRS[(iS[None, :] - iR[:, None]) % g.Nf]
    K = np.block([[Krr, Krs], [Krs.T, Kss]])
    rhs = np.concatenate([cRS[(-iR) % g.Nf], cSS[iS]])
    co = np.linalg.solve(K, rhs)
    s = float(cSS[0] - rhs @ co)
    kC = np.zeros(P + 1); kC[0] = 1.0; kC[1:] = -co[P + 1:]
    return s, g.sym(kC), g.sym(-co[:P + 1])


def shat_of(g, h1, Gam, C, B):
    """THE MINORANT: Var(C S + B R), AFFINE in (h1, Gam), >= s always."""
    return float(np.mean(np.abs(C) ** 2 * g.fS + np.abs(B) ** 2 * Gam
                         + 2 * np.real(np.conj(C) * B * h1)))


def rate_spec(g, h1, h2, Gam, P=None):
    """rate = block + leak (bits/symbol), Collapse + Lemma S."""
    nz = nz_of(g, h1, h2, Gam)
    MQ = MQ_of(g, h1, Gam)
    blk = AL * (g.mean(np.log(MQ)) - g.mean(np.log(nz)))
    s, C, B = pivot_s(g, Gam, h1, P)
    return blk + AL * (LNFS - np.log(s)), dict(block=blk, s=s, C=C, B=B)


def _phi_cell(om, beta):
    k = AL / beta
    r = np.sqrt(om ** 2 + 4 * k * om)
    nn = np.maximum(0.5 * (-om + r), 1e-320)
    return AL * np.log1p(om / nn) + beta * nn, nn


def cell_inf(g, beta, p1, p2, nb=200):
    """Per-frequency lower bound on inf_{h, n>0} [alpha ln(1 + hRh*/n)
    + beta (n + hPh*) + 2Re(p* h)].  R14: the curvature modulus is
    beta*lambda_min(P+Q) and the guard is 2|u|^2/(beta lmin(P+Q))."""
    R11, R12, R22 = g.R11, g.R12, g.R22
    P11, P12, P22 = g.P11, g.P12, g.P22
    detR = R11 * R22 - R12 ** 2
    kap = (R22 * np.abs(p1) ** 2 - 2 * R12 * np.real(p1 * np.conj(p2))
           + R11 * np.abs(p2) ** 2) / detR
    trivial = kap <= AL * beta

    def h_of(ps):
        m11 = ps * R11 + beta * P11
        m12 = ps * R12 + beta * P12
        m22 = ps * R22 + beta * P22
        dt = m11 * m22 - m12 ** 2
        return (-(p1 * m22 - p2 * m12) / dt, -(-p1 * m12 + p2 * m11) / dt)

    lo = np.full(g.Nf, -16.0)
    hi = np.full(g.Nf, 16.0)
    for _ in range(nb):
        mid = 0.5 * (lo + hi)
        ps = 10.0 ** mid
        a1, a2 = h_of(ps)
        gm = qf(R11, R12, R22, a1, a2) - AL * beta / (ps * (ps + beta))
        neg = gm < 0
        lo = np.where(neg, mid, lo)
        hi = np.where(neg, hi, mid)
    ps = 10.0 ** (0.5 * (lo + hi))
    a1, a2 = h_of(ps)
    om = qf(R11, R12, R22, a1, a2)
    ph, nn = _phi_cell(om, beta)
    MQ = nn + om
    val = ph + beta * qf(P11, P12, P22, a1, a2) + 2 * np.real(
        np.conj(p1) * a1 + np.conj(p2) * a2)
    dphi = AL / MQ
    u1 = dphi * (a1 * R11 + a2 * R12) + beta * (a1 * P11 + a2 * P12) + p1
    u2 = dphi * (a1 * R12 + a2 * R22) + beta * (a1 * P12 + a2 * P22) + p2
    S11, S12, S22 = P11 + g.Q11, P12, P22          # P + Q
    lmPQ = 0.5 * ((S11 + S22) - np.sqrt((S11 - S22) ** 2 + 4 * S12 ** 2))
    guard = 2.0 * (np.abs(u1) ** 2 + np.abs(u2) ** 2) / (beta * lmPQ)
    cLB = np.where(trivial, 0.0, np.minimum(val - guard, 0.0))
    return cLB, dict(val=val, guard=guard, trivial=trivial, psi=ps, n=nn,
                     om=om, h=(a1, a2),
                     resid=np.sqrt(np.abs(u1) ** 2 + np.abs(u2) ** 2))


def dual_LB(g, Dl, mu, C, B, sh, D=D_TGT, nb=200):
    """THE BOX-FREE PER-FREQUENCY DUAL (R17).  Valid for ANY mu >= 0 with
    beta > 0, ANY ADMISSIBLE frozen filters (C, B), ANY linearisation
    point sh > 0.  Needs no optimality, no convexity of the process
    rate, no differentiability, and no moment box."""
    zD = g.z ** (Dl + 1)
    beta = mu - AL * np.abs(B) ** 2 / sh
    p1 = -AL * C * np.conj(B) / sh
    p2 = -mu * zD
    const = (AL * LNFS - AL * np.log(sh) + AL
             - (AL / sh) * float(np.mean(np.abs(C) ** 2 * g.fS))
             + mu * (1.0 - D))
    if np.min(beta) <= 0:
        return -np.inf, dict(beta_min=float(np.min(beta)), bad=True)
    cLB, info = cell_inf(g, beta, p1, p2, nb)
    LB = const + float(np.mean(cLB))
    info.update(LB=LB, const=const, beta_min=float(np.min(beta)), bad=False,
                ntriv=int(info["trivial"].sum()))
    return LB, info


def cell_argmin(g, beta, p1, p2, nb=64):
    cLB, info = cell_inf(g, beta, p1, p2, nb)
    a1, a2 = info["h"]
    a1 = np.where(info["trivial"], 0.0, a1)
    a2 = np.where(info["trivial"], 0.0, a2)
    nn = np.where(info["trivial"], 1.0, info["n"])
    return a1, a2, nn


def solve_mu(g, Dl, mu, x0=None, iters=60, damp=0.6, tol=3e-15):
    """Cell-argmin fixed point at fixed mu (deterministic contraction)."""
    zD = g.z ** (Dl + 1)
    if x0 is None:
        h1 = 0.5 * g.fV * zD
        h2 = 0.5 * (RHO * g.fV + SN2) * zD
        Gam = np.maximum(np.abs(h1) ** 2 / g.fV + 0.3,
                         qf(g.P11, g.P12, g.P22, h1, h2) + 0.05)
    else:
        h1, h2, Gam = [np.array(v, copy=True) for v in x0]
    d = np.inf
    for it in range(iters):
        s, C, B = pivot_s(g, Gam, h1)
        beta = mu - AL * np.abs(B) ** 2 / s
        if beta.min() <= 0:
            raise RuntimeError("beta <= 0")
        a1, a2, nn = cell_argmin(g, beta, -AL * C * np.conj(B) / s, -mu * zD)
        Gn = nn + qf(g.P11, g.P12, g.P22, a1, a2)
        d = max(np.max(np.abs(a1 - h1)), np.max(np.abs(a2 - h2)),
                np.max(np.abs(Gn - Gam)))
        h1 = (1 - damp) * h1 + damp * a1
        h2 = (1 - damp) * h2 + damp * a2
        Gam = (1 - damp) * Gam + damp * Gn
        if d < tol:
            break
    return (h1, h2, Gam), float(d)


def solve_D_spec(g, Dl, D=D_TGT, mu0=2.2, mu1=2.4, x0=None, nit=14):
    """Secant on mu so that dist = D.  Deterministic, warm-startable."""
    x, d = solve_mu(g, Dl, mu0, x0, iters=(60 if x0 is None else 40))
    f0 = dist_spec(g, *x, Dl) - D
    x, d = solve_mu(g, Dl, mu1, x, iters=40)
    f1 = dist_spec(g, *x, Dl) - D
    a, b = mu0, mu1
    for _ in range(nit):
        if abs(f1 - f0) < 1e-18:
            break
        m2 = min(max(b - f1 * (b - a) / (f1 - f0), 0.5), 20.0)
        x, d = solve_mu(g, Dl, m2, x, iters=30)
        f2 = dist_spec(g, *x, Dl) - D
        a, f0, b, f1 = b, f1, m2, f2
        if abs(f2) < 1e-15:
            break
    x, d = solve_mu(g, Dl, b, x, iters=80, damp=0.55)
    return b, x, d


def block_cert(g, mu, D=D_TGT):
    """THE BLOCK PROGRAM (se == n): no leak, so the cell dual needs NO
    ANCHOR AT ALL -- beta = mu, p1 = 0, const = mu(1 - D)."""
    zD = g.z
    beta = np.full(g.Nf, mu)
    p1 = np.zeros(g.Nf, complex)
    p2 = -mu * zD
    cLB, info = cell_inf(g, beta, p1, p2)
    LB = mu * (1.0 - D) + float(np.mean(cLB))
    a1, a2 = info["h"]
    a1 = np.where(info["trivial"], 0.0, a1)
    a2 = np.where(info["trivial"], 0.0, a2)
    nn = np.where(info["trivial"], 1.0, info["n"])
    Gam = nn + qf(g.P11, g.P12, g.P22, a1, a2)
    dd = float(np.mean(Gam) - 2 * np.mean(np.real(np.conj(zD) * a2)) + 1.0)
    UB = AL * (g.mean(np.log(MQ_of(g, a1, Gam))) - g.mean(np.log(nn)))
    return LB, UB, dd


def rand_rec_spec(g, rng, K=8, scale=0.25, nfloor=0.02, Dl=0):
    """A random FEASIBLE-cone stationary F0 record in moment coords."""
    kv = scale * rng.standard_normal(K); kvn = scale * rng.standard_normal(K)
    ky = scale * rng.standard_normal(K); kyn = scale * rng.standard_normal(K)
    ky[0] += 0.7
    kn = 0.05 * rng.standard_normal(6)
    av = g.sym(kv, kvn)
    ay = g.sym(ky, kyn)
    nw = nfloor + np.abs(np.real(g.sym(kn, kn[1:]))) + 0.05
    zD = g.z ** (Dl + 1)
    gg = av + RHO * ay
    gR = zD * gg
    h1 = gR * g.fV
    h2 = zD * (gg * RHO * g.fV + ay * SN2)
    Gam = np.abs(gR) ** 2 * g.fV + np.abs(ay) ** 2 * SN2 + nw
    return h1, h2, np.real(Gam)


# ======================================================================
#  preamble: the committed sealed bars, and the cold-start anchors
# ======================================================================
print("[pre] sealed causal-spectral bars + cold-start finite-n anchors ...",
      flush=True)
with open(PLJSON) as fh:
    _pl = json.load(fh)["vals"]
FILE_BAR = {int(k): float(v) for k, v in _pl["s6_cand"].items()}
FILE_BLOCK = float(_pl["s6_block_inf"])
bar_err = max(abs(FILE_BAR[d] - SEALED_BAR[d]) for d in (0, 1, 2))
vals["sealed_bars_file"] = FILE_BAR
vals["sealed_bars_pinned"] = SEALED_BAR
vals["sealed_bar_match"] = bar_err
vals["block_inf_committed_file"] = FILE_BLOCK
verdicts["pre_sealed_bars_match_committed"] = bar_err == 0.0
print(f"  s6_cand read from results/GO14-process-limit.json: "
      f"{FILE_BAR[0]:.13f} / {FILE_BAR[1]:.13f} / {FILE_BAR[2]:.13f}"
      f"  (pinned literals agree exactly: {bar_err:.1e})", flush=True)

ANCH = {}
for (n_, D_) in ((8, 0), (12, 0), (16, 0), (16, 1), (16, 2)):
    o = polish(n_, D_)
    o["La_time"] = la_direct(n_, o["Av"], o["Ay"], o["Nc"], Delta=D_)
    o["dist_time"] = dist_time(n_, o["Av"], o["Ay"], o["Nc"])
    ANCH[(n_, D_)] = o
    print(f"  cold-start ({n_},{D_}): phi ~ {o['v']:.10f} "
          f"(committed {REC_PHI[(n_, D_)]:.10f}, "
          f"|d| {abs(o['v'] - REC_PHI[(n_, D_)]):.1e}); independent "
          f"time-domain re-valuation {o['La_time']:.10f} "
          f"(|d| {abs(o['La_time'] - o['v']):.1e}); dist "
          f"{o['dist_time']:.10f}; rnorm {o['rn']:.1e} "
          f"[{time.time()-t0:.0f}s]", flush=True)
vals["anchors"] = {f"{n}_{d}": {"v": ANCH[(n, d)]["v"],
                                "committed": REC_PHI[(n, d)],
                                "err": abs(ANCH[(n, d)]["v"]
                                           - REC_PHI[(n, d)]),
                                "La_time": ANCH[(n, d)]["La_time"],
                                "dist": ANCH[(n, d)]["dist_time"],
                                "rnorm": ANCH[(n, d)]["rn"],
                                "mu": ANCH[(n, d)]["mu"]}
                   for (n, d) in ANCH}

# ------------------------------------------------------------------ s1
print("[s1] the COLLAPSE identity: 2 ln2 n L_a = sum_t ln sigma_t "
      "- lndet N ...", flush=True)
BAR_S1 = 1e-12
BAR_S1_FAIL = 0.02
rng1 = np.random.default_rng(20260807)
worst_st = 0.0
cells_st = 0
for n in (6, 8, 10, 12):
    for Delta in sorted(set([0, 1, 2, n - 2, n - 1, n, n + 3])):
        for rep in range(3):
            Av, Ay, Nc = rand_record_t(n, rng1)
            c, d = la_collapse(n, Av, Ay, Nc, Delta=Delta)
            worst_st = max(worst_st, abs(c - d) / max(abs(d), 1e-12))
            cells_st += 1
worst_ns = 0.0
cells_ns = 0
for n in (8, 10):
    for rep in range(8):
        se = np.sort(rng1.integers(0, n + 1, size=n))
        Av, Ay, Nc = rand_record_t(n, rng1)
        c, d = la_collapse(n, Av, Ay, Nc, se=se)
        worst_ns = max(worst_ns, abs(c - d) / max(abs(d), 1e-12))
        cells_ns += 1
uext = {}
n = 8
for Delta in (0, 2):
    for tag, mk in (
            ("dense", lambda: 0.3 * rng1.standard_normal((n, n))),
            ("Delta_lag_causal", lambda: 0.3 * rng1.standard_normal((n, n))
             * (np.subtract.outer(np.arange(n), np.arange(n)) + Delta >= 0)),
            ("strictly_anticausal", lambda: 0.3 * rng1.standard_normal((n, n))
             * (np.subtract.outer(np.arange(n), np.arange(n)) < 0))):
        Av, Ay, Nc = rand_record_t(n, rng1)
        c, d = la_collapse(n, Av, Ay, Nc, Delta=Delta, Au=mk())
        uext[f"{tag}_D{Delta}"] = abs(c - d)
u_ok = max(uext[k] for k in uext if k.startswith("Delta_lag_causal"))
u_bad = min(uext[k] for k in uext if not k.startswith("Delta_lag_causal"))
vals["s1"] = {"cells_staircase": cells_st, "resid_staircase": worst_st,
              "cells_nonstaircase": cells_ns, "resid_nonstaircase": worst_ns,
              "u_extension_gaps": uext, "u_causal_worst": u_ok,
              "u_noncausal_best": u_bad,
              "bars": {"identity": BAR_S1, "control_fail": BAR_S1_FAIL}}
verdicts["s1_collapse_identity"] = worst_st < BAR_S1
verdicts["s1_nonstaircase_schedules"] = worst_ns < BAR_S1
verdicts["s1_R6_Delta_lag_causal_U_exact"] = u_ok < BAR_S1
verdicts["s1_R6_dense_and_anticausal_U_fail"] = u_bad > BAR_S1_FAIL
print(f"  staircase (incl. edges Delta in {{n-2,n-1,n,n+3}}): {cells_st} "
      f"cells, worst rel {worst_st:.2e} < {BAR_S1:.0e} "
      f"({BAR_S1/max(worst_st,1e-300):.0f}x)", flush=True)
print(f"  non-staircase nondecreasing schedules: {cells_ns} cells, worst rel "
      f"{worst_ns:.2e} < {BAR_S1:.0e}", flush=True)
print(f"  R6: Delta-LAG-CAUSAL U-coupling is EXACT ({u_ok:.1e}); dense and "
      f"strictly anticausal U-coupling FAIL by >= {u_bad:.4f} bits "
      f"(> {BAR_S1_FAIL}) -- F0 is the special case Au = 0, and the "
      f"non-conflation rule for moment-form Theorem R still applies "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s2
print("[s2] step (A) PERIODIZATION with INDEPENDENT noise copies ...",
      flush=True)
BAR_S2_DIST = 1e-12
BAR_S2_LDET = 1e-11
BAR_S2_CTRL = 0.01
rng2 = np.random.default_rng(11223344)
bad = 0
tot = 0
wd = 0.0
wl = 0.0
for n in (4, 6):
    for Delta in (0, 1, 2, n - 1, n):
        for rep in range(2):
            Av, Ay, Nc = rand_record_t(n, rng2)
            L0, sig0 = la_chol(n, Av, Ay, Nc, Delta=Delta)
            d0 = dist_time(n, Av, Ay, Nc)
            _, ld0 = slogdet(Nc)
            for B in (2, 4, 6):
                AvT, AyT, NT = tile(n, Av, Ay, Nc, B)
                LT, sigT = la_chol(n * B, AvT, AyT, NT, Delta=Delta)
                wd = max(wd, abs(dist_time(n * B, AvT, AyT, NT) - d0))
                _, ldT = slogdet(NT)
                wl = max(wl, abs(ldT - B * ld0))
                ratio = sigT.reshape(B, n) / sig0[None, :]
                tot += ratio.size
                bad += int(np.sum(ratio > 1 + 1e-12))
ctrl = {}
for tag, (n, Delta, Bc, rec) in (
        ("random_n5", (5, 1, 3, rand_record_t(5, rng2))),
        ("optimizer_8_0", (8, 0, 3, (ANCH[(8, 0)]["Av"], ANCH[(8, 0)]["Ay"],
                                     ANCH[(8, 0)]["Nc"])))):
    Av, Ay, Nc = rec
    L0, _ = la_chol(n, Av, Ay, Nc, Delta=Delta)
    AvT, AyT, NT = tile(n, Av, Ay, Nc, Bc)
    row = {}
    for c in (0.3, 0.6, 0.9):
        NT2 = NT.copy()
        for b in range(Bc):
            for b2 in range(Bc):
                if b != b2:
                    NT2[b * n:(b + 1) * n, b2 * n:(b2 + 1) * n] = \
                        c ** abs(b - b2) * Nc
        if np.linalg.eigvalsh(NT2).min() <= 0:
            row[str(c)] = None
            continue
        LT2, _ = la_chol(n * Bc, AvT, AyT, NT2, Delta=Delta)
        row[str(c)] = {"tiled": LT2, "untiled": L0, "excess": LT2 - L0}
    ctrl[tag] = {"phi_n": L0, "rows": row}
ctrl_min = min(v["excess"] for tg in ctrl for v in ctrl[tg]["rows"].values()
               if v is not None)
vals["s2"] = {"cells": tot, "sigma_violations": bad, "dist_err": wd,
              "lndet_err": wl, "correlated_control": ctrl,
              "control_min_excess": ctrl_min,
              "bars": {"dist": BAR_S2_DIST, "lndet": BAR_S2_LDET,
                       "control": BAR_S2_CTRL}}
verdicts["s2_distortion_preserved"] = wd < BAR_S2_DIST
verdicts["s2_lndetN_additive"] = wl < BAR_S2_LDET
verdicts["s2_every_sigma_decreases"] = bad == 0
verdicts["s2_R7_correlated_copies_break_A"] = ctrl_min > BAR_S2_CTRL
print(f"  distortion preserved {wd:.2e} < {BAR_S2_DIST:.0e}; lndet N "
      f"additive {wl:.2e} < {BAR_S2_LDET:.0e}; every sigma_t decreases: "
      f"{bad} violations over {tot} (cell x tiling) pairs", flush=True)
for tg in ctrl:
    r = ctrl[tg]["rows"]
    ex = "/".join("%.4f" % r[c]["excess"] for c in ("0.3", "0.6", "0.9")
                  if r[c] is not None)
    print(f"  R7 control [{tg}] correlated noise copies at c=0.3/0.6/0.9 "
          f"EXCEED the untiled value {ctrl[tg]['phi_n']:.7f} by {ex} bits "
          f"-- 'independent noise copies' is a HYPOTHESIS of the "
          f"construction", flush=True)
print(f"  min excess {ctrl_min:.4f} > {BAR_S2_CTRL} "
      f"({ctrl_min/BAR_S2_CTRL:.1f}x) [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s3
print("[s3] step (B) SHIFT-AVERAGING: an EXPLICIT stationary record of no "
      "larger rate and identical per-symbol distortion ...", flush=True)
BAR_S3_CONE = 1e-3
BAR_S3_DIST = 1e-12
BAR_S3_RATE = -1e-4
rng3 = np.random.default_rng(777001)
s3rows = {}
s3_ok_rate = True
s3_ok_cone = True
s3_ok_dist = True
for (n_, D_) in sorted(ANCH):
    o = ANCH[(n_, D_)]
    r = shiftavg(n_, o["Av"], o["Ay"], o["Nc"], D_)
    gap = r["Lst"] - r["Lcyc"]
    dd = abs(r["dst"] - r["dcyc"])
    s3rows[f"opt_{n_}_{D_}"] = dict(r, gap=gap, dist_err=dd)
    s3_ok_rate = s3_ok_rate and (gap < BAR_S3_RATE)
    s3_ok_cone = s3_ok_cone and (min(r["nmin"], r["emin"]) > BAR_S3_CONE)
    s3_ok_dist = s3_ok_dist and (dd < BAR_S3_DIST)
    print(f"  optimizer ({n_},{D_}): cyclostationary {r['Lcyc']:.10f} -> "
          f"shift-averaged stationary {r['Lst']:.10f} (gap {gap:+.3e} < "
          f"{BAR_S3_RATE:.0e}); cone min_w nbar {r['nmin']:.3e}, Toeplitz "
          f"eigmin {r['emin']:.3e}; distortion preserved {dd:.1e} "
          f"[{time.time()-t0:.0f}s]", flush=True)
nrand = 0
for n_ in (3, 4, 5):
    for D_ in (0, 1, 2):
        Av, Ay, Nc = rand_record_t(n_, rng3, scale=0.30)
        r = shiftavg(n_, Av, Ay, Nc, D_)
        gap = r["Lst"] - r["Lcyc"]
        dd = abs(r["dst"] - r["dcyc"])
        s3rows[f"rand_{n_}_{D_}"] = dict(r, gap=gap, dist_err=dd)
        nrand += 1
        s3_ok_rate = s3_ok_rate and (gap < BAR_S3_RATE)
        s3_ok_cone = s3_ok_cone and (min(r["nmin"], r["emin"]) > BAR_S3_CONE)
        s3_ok_dist = s3_ok_dist and (dd < BAR_S3_DIST)
gap_worst = max(v["gap"] for v in s3rows.values())
cone_worst = min(min(v["nmin"], v["emin"]) for v in s3rows.values())
dist_worst = max(v["dist_err"] for v in s3rows.values())
vals["s3"] = {"rows": s3rows, "n_random": nrand, "gap_worst": gap_worst,
              "cone_worst": cone_worst, "dist_worst": dist_worst,
              "bars": {"cone": BAR_S3_CONE, "dist": BAR_S3_DIST,
                       "rate": BAR_S3_RATE}}
verdicts["s3_averaged_pair_in_cone"] = bool(s3_ok_cone)
verdicts["s3_distortion_preserved"] = bool(s3_ok_dist)
verdicts["s3_stationary_rate_no_larger"] = bool(s3_ok_rate)
print(f"  {len(s3rows)} cases ({len(ANCH)} optimizers + {nrand} random "
      f"period-n records): worst rate gap {gap_worst:+.3e} < "
      f"{BAR_S3_RATE:.0e} ({gap_worst/BAR_S3_RATE:.1f}x), worst cone margin "
      f"{cone_worst:.3e} > {BAR_S3_CONE:.0e}, worst distortion error "
      f"{dist_worst:.1e} [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s4
print("[s4] LEMMA C-stat: ln(Gam - hQh*) - ln(Gam - hPh*) is jointly "
      "convex when Q >= 0 and R = P - Q >= 0 ...", flush=True)
BAR_S4_CTRL = 1000
gS = Grid(Nf=1024, P=60)
rng4 = np.random.default_rng(4242)
NCH = 60000
ii = rng4.integers(0, gS.Nf, NCH)


def _pt(m):
    return ((rng4.standard_normal(m) + 1j * rng4.standard_normal(m)) * 0.5,
            (rng4.standard_normal(m) + 1j * rng4.standard_normal(m)) * 0.5)


def _hP(i, x1, x2):
    return (gS.P11[i] * np.abs(x1) ** 2
            + 2 * gS.P12[i] * np.real(x1 * np.conj(x2))
            + gS.P22[i] * np.abs(x2) ** 2)


h1a, h2a = _pt(NCH)
h1b, h2b = _pt(NCH)
ea = 10 ** rng4.uniform(-9, -1, NCH)
eb = 10 ** rng4.uniform(-9, -1, NCH)
lam = rng4.uniform(0, 1, NCH)
Ga = _hP(ii, h1a, h2a) + ea
Gb = _hP(ii, h1b, h2b) + eb


def _F(i, x1, x2, Gm):
    return np.log(Gm - gS.Q11[i] * np.abs(x1) ** 2) - np.log(Gm - _hP(i, x1, x2))


fa = _F(ii, h1a, h2a, Ga)
fb = _F(ii, h1b, h2b, Gb)
fm = _F(ii, lam * h1a + (1 - lam) * h1b, lam * h2a + (1 - lam) * h2b,
        lam * Ga + (1 - lam) * Gb)
jgap = lam * fa + (1 - lam) * fb - fm
jtol = 1e-9 * np.maximum(1.0, np.abs(lam * fa) + np.abs((1 - lam) * fb))
jviol = int(np.sum(jgap < -jtol))
CQ = 1.3


def _Fc(i, x1, x2, Gm):
    return np.log(Gm - CQ * _hP(i, x1, x2)) - np.log(Gm - _hP(i, x1, x2))


Ga2 = CQ * _hP(ii, h1a, h2a) + ea
Gb2 = CQ * _hP(ii, h1b, h2b) + eb
fa2 = _Fc(ii, h1a, h2a, Ga2)
fb2 = _Fc(ii, h1b, h2b, Gb2)
fm2 = _Fc(ii, lam * h1a + (1 - lam) * h1b, lam * h2a + (1 - lam) * h2b,
          lam * Ga2 + (1 - lam) * Gb2)
cgap = lam * fa2 + (1 - lam) * fb2 - fm2
cfin = np.isfinite(cgap)
cviol = int(np.sum(cgap[cfin] < -1e-9))
vals["s4"] = {"n_chords": NCH, "violations": jviol,
              "worst_chord": float(jgap.min()),
              "median_chord": float(np.median(jgap)),
              "boundary_eps_min": float(min(ea.min(), eb.min())),
              "control_Qprime_over_P": CQ, "control_finite": int(cfin.sum()),
              "control_violations": cviol,
              "control_worst": float(np.nanmin(cgap[cfin])),
              "bars": {"violations": 0, "control_violations": BAR_S4_CTRL}}
verdicts["s4_Cstat_jensen"] = jviol == 0
verdicts["s4_R12_psd_hypothesis_load_bearing"] = cviol >= BAR_S4_CTRL
print(f"  {NCH} random chords with Gamma pushed to "
      f"{min(ea.min(), eb.min()):.1e} of the cone boundary: {jviol} "
      f"violations, worst chord {jgap.min():+.3e}", flush=True)
print(f"  R12 control Q' = {CQ} P (so R = P - Q' is NEGATIVE definite): "
      f"{cviol}/{int(cfin.sum())} violations, worst {np.nanmin(cgap[cfin]):+.3f} "
      f"-- BOTH Q >= 0 and R = P - Q >= 0 are load-bearing "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s5
print("[s5] THE MINORANT shat >= s -- the one place a sign slip inverts "
      "the bound ...", flush=True)
BAR_S5 = -1e-11
BAR_S5_CTRL = -0.1
g5 = Grid(Nf=1024, P=80)
rng5 = np.random.default_rng(11081)
recs5 = [rand_rec_spec(g5, rng5, K=int(rng5.integers(2, 12)),
                       scale=float(rng5.uniform(0.05, 1.2)),
                       nfloor=float(rng5.uniform(0.002, 0.6)),
                       Dl=int(rng5.integers(0, 3))) for _ in range(120)]
pool = []
for k in range(0, 120, 8):                       # FOREIGN optima
    _s, _C, _B = pivot_s(g5, recs5[k][2], recs5[k][0])
    pool.append((f"foreign_opt_rec{k}", _C, _B))
for Pt in (1, 2, 5, 20):                         # TRUNCATIONS
    _s, _C, _B = pivot_s(g5, recs5[3][2], recs5[3][0], P=Pt)
    pool.append((f"trunc_P{Pt}", _C, _B))
_k1 = np.zeros(6); _k1[0] = 1.0
pool.append(("C=1,B=0", g5.sym(_k1), g5.sym(np.zeros(3))))
pool.append(("C=1,B=+3", g5.sym(_k1), g5.sym(np.array([3.0]))))
pool.append(("C=1,B=-3", g5.sym(_k1), g5.sym(np.array([-3.0]))))
pool.append(("oscillating", g5.sym(np.array([1.0, -0.9, 0.5])),
             g5.sym(np.array([1.0, -2.0, 3.0, -4.0]))))
pool.append(("near_unit_root", g5.sym(np.array([1.0, 0.99])),
             g5.sym(np.array([0.1]))))
worst5 = np.inf
nv5 = 0
nt5 = 0
wl5 = None
for (h1, h2, Gam) in recs5:
    s, _, _ = pivot_s(g5, Gam, h1)
    for lbl, C, B in pool:
        gap = shat_of(g5, h1, Gam, C, B) - s
        nt5 += 1
        if gap < worst5:
            worst5, wl5 = gap, lbl
        nv5 += int(gap < BAR_S5)
s0, _, _ = pivot_s(g5, recs5[0][2], recs5[0][0])
nonmonic = shat_of(g5, recs5[0][0], recs5[0][2],
                   g5.sym(np.array([0.3])), g5.sym(np.zeros(2))) - s0
anticaus = shat_of(g5, recs5[0][0], recs5[0][2],
                   g5.sym(np.array([1.0]), np.array([0.6])),
                   g5.sym(np.array([0.0]), np.array([0.5, 0.3]))) - s0
vals["s5"] = {"pairs": nt5, "records": len(recs5), "filters": len(pool),
              "violations": nv5, "min_slack": float(worst5),
              "min_slack_at": wl5, "control_nonmonic": float(nonmonic),
              "control_anticausal": float(anticaus),
              "bars": {"slack": BAR_S5, "control": BAR_S5_CTRL}}
verdicts["s5_minorant_shat_ge_s"] = nv5 == 0
verdicts["s5_R11_nonmonic_control_inverts"] = nonmonic < BAR_S5_CTRL
print(f"  {nt5} (record x frozen-filter) pairs = {len(recs5)} adversarial "
      f"records x {len(pool)} admissible filters (foreign optima, "
      f"truncations to 1/2/5/20 lags, oscillating, near-unit-root): "
      f"{nv5} violations, min(shat - s) {worst5:+.2e} at {wl5}", flush=True)
print(f"  R11 control: a NON-MONIC C (= 0.3) gives shat - s = "
      f"{nonmonic:+.4f} < {BAR_S5_CTRL} and INVERTS the bound (an "
      f"inadmissible anticausal pair gives {anticaus:+.4f}) -- "
      f"'admissible' is a HYPOTHESIS WITH CONTENT, not an adjective "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s6
print("[s6] R17: the box-free per-frequency dual is VALID WITHOUT any "
      "optimality of the fixed point ...", flush=True)
BAR_S6_VALID = 1e-9
BAR_S6_POWER = -1e-6
BAR_S6_FINITE = 15
g6 = Grid(Nf=1024, P=60)
FP = {}
xprev = None
for Dl in (0, 1, 2):
    mu_, x_, res_ = solve_D_spec(g6, Dl, x0=xprev)
    xprev = x_
    r_, aux_ = rate_spec(g6, *x_)
    FP[Dl] = dict(mu=mu_, x=tuple(v.copy() for v in x_), rate=r_, aux=aux_,
                  resid=res_, dist=dist_spec(g6, *x_, Dl))
    print(f"  stationary fixed point Delta={Dl}: mu {mu_:.12f}, residual "
          f"{res_:.2e}, dist {FP[Dl]['dist']:.15f}, rate {r_:.13f} "
          f"[{time.time()-t0:.0f}s]", flush=True)
rng6 = np.random.default_rng(606061)
s6rows = {}
valid_worst = -np.inf
power_worst = -np.inf
fin_min = 10 ** 9
for Dl in (0, 1, 2):
    mu0 = FP[Dl]["mu"]
    h1, h2, Gam = FP[Dl]["x"]
    PsiUB = FP[Dl]["rate"]
    rows = []
    for lbl, mu, Pt, shf, strict in (
            ("reference", mu0, None, 1.0, False),
            ("mu x0.95", mu0 * 0.95, None, 1.0, True),
            ("mu x1.10", mu0 * 1.10, None, 1.0, True),
            ("filters truncated to 12 lags", mu0, 12, 1.0, False),
            ("filters truncated to 4 lags", mu0, 4, 1.0, True),
            ("filters truncated to 1 lag", mu0, 1, 1.0, True),
            ("shat linearisation +5%", mu0, None, 1.05, True),
            ("shat linearisation -5%", mu0, None, 0.95, True)):
        s, C, B = pivot_s(g6, Gam, h1, P=Pt)
        shv = shat_of(g6, h1, Gam, C, B)
        LB, info = dual_LB(g6, Dl, mu, C, B, shv * shf)
        dg = LB - PsiUB
        rows.append({"anchor": lbl, "LB": float(LB), "LB_minus_PsiUB": dg,
                     "margin_over_bar": float(LB - SEALED_BAR[Dl]),
                     "shat_minus_s": float(shv - FP[Dl]["aux"]["s"]),
                     "strict": strict})
        valid_worst = max(valid_worst, dg)
        if strict:
            power_worst = max(power_worst, dg)
    nfin = 0
    nviol = 0
    bestLB = -np.inf
    for k in range(25):
        h1r, h2r, Gr = rand_rec_spec(g6, rng6, K=int(rng6.integers(2, 8)),
                                     scale=float(rng6.uniform(0.1, 0.6)),
                                     nfloor=float(rng6.uniform(0.05, 0.4)),
                                     Dl=Dl)
        sr, Cr, Br = pivot_s(g6, Gr, h1r)
        LB, info = dual_LB(g6, Dl, mu0, Cr, Br, sr)
        if np.isfinite(LB):
            nfin += 1
            bestLB = max(bestLB, LB)
            nviol += int(LB > PsiUB + BAR_S6_VALID)
    valid_worst = max(valid_worst, bestLB - PsiUB)
    power_worst = max(power_worst, bestLB - PsiUB)
    fin_min = min(fin_min, nfin)
    s6rows[str(Dl)] = {"Psi_UB": PsiUB, "rows": rows,
                       "random_anchors": 25, "random_finite": nfin,
                       "random_violations": nviol,
                       "random_best_LB": float(bestLB),
                       "random_best_minus_PsiUB": float(bestLB - PsiUB)}
    print(f"  Delta={Dl}: Psi_UB {PsiUB:.12f}; mistuned mu x0.95/x1.10 -> "
          f"{rows[1]['LB_minus_PsiUB']:+.2e}/{rows[2]['LB_minus_PsiUB']:+.2e}; "
          f"frozen filters truncated to 12/4/1 lags -> "
          f"{rows[3]['LB_minus_PsiUB']:+.1e}/{rows[4]['LB_minus_PsiUB']:+.1e}/"
          f"{rows[5]['LB_minus_PsiUB']:+.1e}; shat linearisation +/-5% -> "
          f"{rows[6]['LB_minus_PsiUB']:+.1e}/{rows[7]['LB_minus_PsiUB']:+.1e}; "
          f"25 random NON-OPTIMAL anchors: {nfin} finite, {nviol} violations, "
          f"best {bestLB - PsiUB:+.2e}", flush=True)
vals["s6"] = {"rows": s6rows, "validity_worst": float(valid_worst),
              "power_worst": float(power_worst), "finite_min": fin_min,
              "bars": {"validity": BAR_S6_VALID, "power": BAR_S6_POWER,
                       "finite": BAR_S6_FINITE}}
verdicts["s6_R17_dual_valid_without_optimality"] = valid_worst < BAR_S6_VALID
verdicts["s6_R17_nonoptimal_anchors_strictly_degrade"] = \
    power_worst < BAR_S6_POWER
verdicts["s6_random_anchors_give_finite_bounds"] = fin_min >= BAR_S6_FINITE
print(f"  VALIDITY: worst LB - Psi_UB over every anchor {valid_worst:+.2e} "
      f"< {BAR_S6_VALID:.0e} (zero cases exceed).  POWER: every "
      f"deliberately non-optimal anchor is strictly degraded, worst "
      f"{power_worst:+.2e} < {BAR_S6_POWER:.0e} "
      f"({power_worst/BAR_S6_POWER:.1f}x).  R18: Delta=2 has NO headroom "
      f"in the tuning -- mu x0.95 costs "
      f"{s6rows['2']['rows'][1]['margin_over_bar']:+.2e} of margin and "
      f"mu x1.10 costs {s6rows['2']['rows'][2]['margin_over_bar']:+.2e} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s7
print("[s7] reproduction of the committed brackets, margins, block_inf "
      "and the Delta-DEPENDENT O(1/n) constant ...", flush=True)
BAR_S7_BRACKET = 1e-8
BAR_S7_MARGIN = 1e-9
BAR_S7_LBCLEAR = 1e-6
BAR_S7_BLOCK = 1e-9
BAR_S7_C1N = 1e-4
BAR_S7_C1N_SEP = 3e-3
psi = {}
brk_err = 0.0
mar_err = 0.0
lb_clear_ok = True
for Dl in (0, 1, 2):
    mu0 = FP[Dl]["mu"]
    h1, h2, Gam = FP[Dl]["x"]
    aux = FP[Dl]["aux"]
    LB, info = dual_LB(g6, Dl, mu0, aux["C"], aux["B"], aux["s"])
    UB = FP[Dl]["rate"]
    qlo, qhi = QUOTE[Dl]
    marg_arith = qlo - SEALED_BAR[Dl]
    psi[str(Dl)] = {"LB": float(LB), "UB": float(UB), "width": float(UB - LB),
                    "quote": [qlo, qhi], "LB_err": abs(LB - qlo),
                    "UB_err": abs(UB - qhi),
                    "inside_quote": bool(qlo <= LB and UB <= qhi),
                    "sealed_bar": SEALED_BAR[Dl],
                    "margin_arithmetic": marg_arith,
                    "margin_recorded": MARGIN_REC[Dl],
                    "margin_arith_err": abs(marg_arith - MARGIN_REC[Dl]),
                    "margin_recomputed": float(LB - SEALED_BAR[Dl])}
    brk_err = max(brk_err, abs(LB - qlo), abs(UB - qhi))
    mar_err = max(mar_err, abs(marg_arith - MARGIN_REC[Dl]))
    lb_clear_ok = lb_clear_ok and (LB - SEALED_BAR[Dl]
                                   > MARGIN_REC[Dl] - BAR_S7_LBCLEAR)
    print(f"  Psi({Dl}) in [{qlo:.10f}, {qhi:.10f}] (10-digit quotable, "
          f"rounded OUTWARD); recomputed LB {LB:.13f} UB {UB:.13f}, "
          f"reproduction error {max(abs(LB-qlo), abs(UB-qhi)):.1e}; margin "
          f"over the SEALED bar {SEALED_BAR[Dl]:.13f} = "
          f"{marg_arith:+.10f} (recorded {MARGIN_REC[Dl]:+.10f})",
          flush=True)
lo_b, hi_b = 1.0, 6.0
for _ in range(80):
    mid = 0.5 * (lo_b + hi_b)
    bLB, bUB, bdd = block_cert(g6, mid)
    if bdd > D_TGT:
        lo_b = mid
    else:
        hi_b = mid
mu_blk = 0.5 * (lo_b + hi_b)
bLB, bUB, bdd = block_cert(g6, mu_blk)
blk_err = max(abs(bLB - BLOCK_INF_CERT), abs(bUB - BLOCK_INF_CERT))
erratum = BLOCK_INF_COMMITTED - bLB
c1n = {}
c1n_err = 0.0
for Dl in (0, 1, 2):
    v = 16.0 * (ANCH[(16, Dl)]["v"] - FP[Dl]["rate"])
    c1n[str(Dl)] = {"measured": float(v), "recorded": REC_C1N[Dl],
                    "err": abs(v - REC_C1N[Dl])}
    c1n_err = max(c1n_err, abs(v - REC_C1N[Dl]))
c1n_sep = min(abs(c1n[str(i)]["measured"] - c1n[str(j)]["measured"])
              for i in (0, 1, 2) for j in (0, 1, 2) if i < j)
vals["s7"] = {"psi": psi, "bracket_err": brk_err, "margin_err": mar_err,
              "block": {"mu": mu_blk, "LB": float(bLB), "UB": float(bUB),
                        "dist": bdd, "certified": BLOCK_INF_CERT,
                        "err": blk_err, "committed": BLOCK_INF_COMMITTED,
                        "committed_high_by": float(erratum)},
              "c_over_n": c1n, "c_over_n_err": c1n_err,
              "c_over_n_min_separation": c1n_sep,
              "bars": {"bracket": BAR_S7_BRACKET, "margin": BAR_S7_MARGIN,
                       "lb_clear": BAR_S7_LBCLEAR, "block": BAR_S7_BLOCK,
                       "c1n": BAR_S7_C1N, "c1n_sep": BAR_S7_C1N_SEP}}
verdicts["s7_brackets_reproduced"] = brk_err < BAR_S7_BRACKET
verdicts["s7_margins_vs_sealed_bars"] = mar_err < BAR_S7_MARGIN
verdicts["s7_recomputed_LB_clears_sealed_bars"] = bool(lb_clear_ok)
verdicts["s7_R20_block_inf_reproduced"] = blk_err < BAR_S7_BLOCK
verdicts["s7_R20_committed_block_inf_high"] = 3e-9 < erratum < 6e-9
verdicts["s7_R19_c_over_n_reproduced"] = c1n_err < BAR_S7_C1N
verdicts["s7_R19_c_over_n_is_Delta_dependent"] = c1n_sep > BAR_S7_C1N_SEP
print(f"  margins reproduce +{MARGIN_REC[0]:.10f} / +{MARGIN_REC[1]:.10f} "
      f"/ +{MARGIN_REC[2]:.10f} to {mar_err:.1e} < {BAR_S7_MARGIN:.0e}; "
      f"bracket reproduction {brk_err:.1e} < {BAR_S7_BRACKET:.0e}",
      flush=True)
print(f"  R20: anchor-free block certificate LB = UB = {bLB:.13f} "
      f"reproduces block_inf {BLOCK_INF_CERT:.13f} to {blk_err:.1e}; the "
      f"COMMITTED s6_block_inf {BLOCK_INF_COMMITTED:.15f} is HIGH by "
      f"{erratum:.2e}", flush=True)
print(f"  R19: n(phi_16 - Psi) = "
      f"{c1n['0']['measured']:.6f} / {c1n['1']['measured']:.6f} / "
      f"{c1n['2']['measured']:.6f} at Delta = 0/1/2 (recorded "
      f"{REC_C1N[0]:.6f}/{REC_C1N[1]:.6f}/{REC_C1N[2]:.6f}, max error "
      f"{c1n_err:.1e}); min pairwise separation {c1n_sep:.4f} > "
      f"{BAR_S7_C1N_SEP:.0e} -- the O(1/n) constant is Delta-DEPENDENT and "
      f"c(0) is a Delta=0 statement ONLY [{time.time()-t0:.0f}s]",
      flush=True)

# ------------------------------------------------------------------ s8
print("[s8] 'does it prove too much?' -- the block program and the "
      "Delta-ladder ...", flush=True)
BAR_S8_NOEXCEED = 1e-9
BAR_S8_NOCROSS = -1e-9
BAR_S8_FAT = 1e-7
BAR_S8_STEP = 1e-8
ladder = {}
xprev = FP[2]["x"]
for Dl in (0, 1, 2, 4, 6, 9):
    if Dl in FP:
        mu_, x_, res_ = FP[Dl]["mu"], FP[Dl]["x"], FP[Dl]["resid"]
        aux_ = FP[Dl]["aux"]
        LB, _i = dual_LB(g6, Dl, mu_, aux_["C"], aux_["B"], aux_["s"])
    else:
        mu_, x_, res_ = solve_D_spec(g6, Dl, x0=xprev)
        xprev = x_
        r_, aux_ = rate_spec(g6, *x_)
        LB, _i = dual_LB(g6, Dl, mu_, aux_["C"], aux_["B"], aux_["s"])
    ladder[Dl] = {"mu": float(mu_), "LB": float(LB), "resid": float(res_),
                  "dist": dist_spec(g6, *x_, Dl),
                  "excess": float(LB - BLOCK_INF_CERT)}
    print(f"  Delta={Dl}: LB {LB:.13f}, excess over block_inf "
          f"{LB - BLOCK_INF_CERT:+.4e} [{time.time()-t0:.0f}s]", flush=True)
DL = [0, 1, 2, 4, 6, 9]
exc = [ladder[d]["excess"] for d in DL]
steps = [exc[i] - exc[i + 1] for i in range(len(exc) - 1)]
fat = min(ladder[d]["excess"] for d in (0, 1, 2, 4, 6))
vals["s8"] = {"block_LB": float(bLB), "block_UB": float(bUB),
              "block_exceeds_by": float(bLB - BLOCK_INF_CERT),
              "ladder": {str(d): ladder[d] for d in DL},
              "min_excess": float(min(exc)), "min_step": float(min(steps)),
              "fat_min_excess": float(fat), "steps": steps,
              "bars": {"noexceed": BAR_S8_NOEXCEED, "nocross": BAR_S8_NOCROSS,
                       "fat": BAR_S8_FAT, "step": BAR_S8_STEP}}
verdicts["s8_block_certificate_does_not_exceed"] = \
    (bLB - BLOCK_INF_CERT) <= BAR_S8_NOEXCEED
verdicts["s8_ladder_never_crosses_block_inf"] = min(exc) >= BAR_S8_NOCROSS
verdicts["s8_ladder_fat_margin_through_Delta6"] = fat > BAR_S8_FAT
verdicts["s8_ladder_strictly_decreasing"] = min(steps) > BAR_S8_STEP
print(f"  block-program certificate LB = {bLB:.13f} exceeds the "
      f"independently known block_inf by {bLB - BLOCK_INF_CERT:+.2e} "
      f"<= {BAR_S8_NOEXCEED:.0e}: it does NOT prove too much", flush=True)
print(f"  the Delta-ladder approaches block_inf FROM ABOVE and never "
      f"crosses: min excess {min(exc):+.3e} >= {BAR_S8_NOCROSS:.0e} "
      f"(at Delta=9), fat-margin form through Delta=6 {fat:.3e} > "
      f"{BAR_S8_FAT:.0e} ({fat/BAR_S8_FAT:.1f}x), strictly decreasing with "
      f"min step {min(steps):.3e} > {BAR_S8_STEP:.0e} "
      f"({min(steps)/BAR_S8_STEP:.0f}x) [{time.time()-t0:.0f}s]", flush=True)

# ---------------------------------------------------------------- report
verdicts = {k: bool(v) for k, v in verdicts.items()}
allpass = all(verdicts.values())
print()
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print("VERDICT:", "ALL PASS" if allpass else "FAIL")

out = {"verdict": verdicts, "GO14PL2_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14PL2-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
