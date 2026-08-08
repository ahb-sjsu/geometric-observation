#!/usr/bin/env python
"""GO-14 FIR-DENSITY harness (tex v1.0, Section "FIR density, and the scoped
equality L^inf = Psi at Delta = 0,1,2").  Registration 085 pending -- NOTHING
HERE IS SEALED.

Model: V AR(1) a = 0.8 unit variance; Y = 0.7 V + N, Var(Y) = 1; S = V + U,
tau2 = 0.4; D = 0.3; T = (V, Y) = W; family F0 (records jointly Gaussian with
(V, Y) and INDEPENDENT of U, i.e. A_u = 0).

WHAT THIS HARNESS IS FOR.  085 is the TERMINAL registration on this face.  082
certified the value Psi two-sided; 083 discharged the convexity step of the
LOWER-bound chain; 084 netted an explicit family of D-feasible F0 records and
the window transfer (Lemma W).  085 nets the FIR-DENSITY objects -- Lemma A'
(pivot upper semicontinuity), Lemma C' (the white-noise floor), Theorem D (FIR
density), Lemma M (the distortion-margin decomposition) -- and, with them, the
SCOPED equality L^inf(Delta) = Psi(D;Delta) at Delta = 0,1,2.

WHAT THE EQUALITY IS AND IS NOT.  It is a SCOPED theorem: it carries, beyond
Corollary cor:onedir's scope items (a)-(d), five further items -- (i) Lemma W
step (3)'s classical rational-spectral-factorization / Riccati citation with
its verified hypotheses, (ii) Fejer-Riesz and Fejer convergence, (iii) the
model hypothesis f_V in [0.1111, 9.0000], (iv) continuity of D -> Psi(D) at
D = 0.3 from convexity, (v) a window threshold n >= n0(L).  "UNCONDITIONAL"
DOES NOT ATTACH TO THIS EQUALITY -- it attaches only to cor:onedir's chain.
Psi remains a two-sided CERTIFIED BRACKET; the equality IDENTIFIES TWO
OBJECTS, it is NOT a licence to quote a value as exact, and cor:brackets
CONTINUES TO GOVERN the quotable numeric statement.  NO GATE IN THIS FILE
READS, ASSERTS OR GATES THAT EQUALITY, and none may be added: what is gated
here are the ingredient facts and their must-fail controls.

LEMMA A', AS RESTATED (F1, F2, F3, F14).
  (1) sigma(x) = dist^2(R_u, M) with M the CLOSED span of the admissible
      lags, so FINITE combinations are dense in M BY DEFINITION and the
      infimum over FINITELY SUPPORTED admissible filters equals sigma
      exactly.  Hypotheses: Phi_R, f_S in L1 and NOTHING ELSE.  The infimum
      is NOT ATTAINED by any finite filter; only eps-optimality is used.
  (2) for a filter fixed FIRST and within eps of sigma(x),
      sigma(x') <= sigma(x) + eps + C_V ||Phi' - Phi||_{L1}.
  F2: A''s admissibility -- V monic causal in R, V_S strictly causal in S --
  is the MIRROR of Definition def:adm's (C_0 monic causal in S, B_0 causal
  including lag 0 in R) and attaches to a DIFFERENT pivot (sigma, not s).
  The two are defined side by side in the tex and are never conflated.
  F3: the prover's FIRST pass at the peeking controls had NO POWER (S-peek
  +0.252, R-peek +0.031 -- POSITIVE) from a lag-sign defect in its helper;
  the R-IND-5 verifier independently hit and fixed the same defect.
  scratchpad firdens/t5b.py is the RUN OF RECORD; firdens/t5_ctl2.py STILL
  CARRIES THE DEFECT and must not be cited.  This file rebuilds all six
  controls from primitives and gates them on the side of failure.
  F14: the K-lag ladder of s1 is instantiated on the L = 10 DIRICHLET
  truncation at Delta = 0.  Instantiated on the optimum itself the ladder
  takes DIFFERENT values (the prover's +2.81e-2/+2.50e-3/+1.78e-5/+2.64e-10
  at K = 1/2/4/8 against this record's +1.27e-2/+1.09e-3/+7.96e-6/+1.30e-10);
  BOTH ARE VALID -- they are two instantiations of the same lemma.

THEOREM D (FIR DENSITY), HYPOTHESES PRINTED (F4).
  (a) f_V bounded above and below -- f_V in [0.1111, 9.0000] -- which is what
      turns FEASIBILITY into L2 kernel bounds;
  (b) continuity of D -> Psi(D) at D = 0.3, from convexity;
  (c) Lemma C' (the white-noise floor), which is LOAD-BEARING;
  (d) Lemma B' (the spectral cap) is DELETED FROM THE PROOF -- it is
      DISPENSABLE, because feasibility ALONE gives ||g||_2 <= 2.343168 and
      ||a_y||_2 <= 1.766965.  B' survives only as a recorded a-priori fact.
  F12: the Fejer build converges at Theta(L^-2); positivity holds at every
  rung; realisability is certified by a ROOT-FREE (cepstral) route, with the
  explicit warning that POLYNOMIAL ROOT-FINDING IS NOT FIT FOR PURPOSE beyond
  L ~ 96; and the Fejer mean preserves <n> EXACTLY.

LEMMA M, AS RESTATED (F5-F8, F9) -- THESE ARE NOT OPTIONAL.
  WITHDRAWN: "every constant n-independent" (measured C(6,n) =
  72.444/20.434/15.194/13.426/12.676 over n = 64..1024 -- the SAME factor-5.7
  decrease W1 refuted).  WITHDRAWN: "~18.7 at L = 6" as an upper bound
  (exceeded at n = 64 and n = 128; the asymptote is ~12.0).  WITHDRAWN: "no
  feasibility threshold" (at L = 10, n = 64 the shifted target D - eta_n is
  -0.01864 < 0 -- the SAME threshold at the SAME (n, L) that W2 recorded).
  THE CAUSE (F7): D -> U(L;D) is CONVEX, so mu*eta is a LOWER bound on the
  repair cost, not an upper one; the multiplier must be taken at the SHIFTED
  point.  LEMMA M THEREFORE DOES NOT DISCHARGE W1 OR W4; W1 AND W2 STAND.
  What Lemma M does deliver (F9) is the EXACT THREE-LEG DECOMPOSITION
      C(L,n) = -2L*rate(x_n) + [sum_t delta_t - Szego]/(2 ln 2)
               + n[U(L; D - eta_n) - U(L; D)],
      eta_n = 2L(1 + eps - D)/(n - 2L)   EXACTLY (not /n),
  each leg separately bounded, giving sup_{n >= n0(L)} C(L,n) < infinity.
  ONLY C(L,n) = o(n) IS USED DOWNSTREAM, so the conclusion is untouched.

F10 -- THE Psi CLASS, WRITTEN DOWN ONCE.  Psi(D;Delta) is the infimum of the
stationary rate over FEASIBLE STATIONARY RECORDS OF F0 with n(w) > 0 a.e.,
Phi_R in L1, and per-symbol distortion <= D.  That same class is used
verbatim in cor:onedir, thm:cert and Theorem D.

F11 -- THE LADDER IS U_tr(L), the TRUNCATION-AND-REPAIR value, NOT the
depth-L optimum: direct minimisation over depth-L FIR records gives strictly
SMALLER values at every rung, all still ABOVE Psi^LB.  s7 gates both.

F13 -- Lemma W's steps enter as "steps (1)-(4), with (3) carrying the
classical citation, and (5) superseded by Lemma M".  Step (3) IS
load-bearing.  The prover's "floored at n >= 0.1288" is UNREPRODUCED: the
record floors are 0.1495/0.1378/0.1404 and the Fejer ladder minimum is
0.1331.

DESIGN RULE (the 079 lesson, restated by 080/081/082/083/084).  NO GATE MAY
RACE AN OPTIMIZER STOPPING POINT AND NO GATE MAY GATE A CERTIFICATE WIDTH.
The stationary K1-K3 kernels are PINNED DATA (provenance: the grid fixed
point at Nf = 4096, P = 180, the same reference W8 names, and the same
literals the 084 harness carries) -- nothing here re-derives them.  The only
search anywhere in this file is s7's DIRECT MINIMISATION over depth-L FIR
records, and its gate is deliberately NOT on the search's stopping point: the
gate is that EVERY FEASIBLE RECORD EVALUATED DURING A PINNED, FIXED-BUDGET
SEARCH sits strictly above Psi^LB.  That is a statement about a SET OF
RECORDS, each of which is an independently valid feasible object; running the
search longer adds records to the set and cannot convert a pass into a fail
by "stopping earlier or later".  No bracket, width or certificate endpoint is
gated anywhere; the recorded 082 lower endpoints are used only as fixed
comparison literals on the safe side.

SECTIONS.

s1 LEMMA A'(1) AND THE SIX MUST-FAIL CONTROLS.  The K-lag admissible ladder
   (V monic causal in R, V_S strictly causal in S) decreases to sigma FROM
   ABOVE and hits it exactly.  Then SIX controls, each FULLY OPTIMISED over
   its enlarged index set so that it has power, must all BREAK the minorant:
   S-peek (uses S_u), R-peek (uses R_{u+1}), the two two-step variants,
   non-monic V(0) = 0.3 with the rest optimal, and non-monic with EVERYTHING
   re-optimised.  F3's disclosure travels with this section.

s2 LEMMA A'(2).  Zero violations of BOTH inequalities over >= 20 adversarial
   record pairs, including 12 random FIR records FAR from the optimum.

s3 THE FEJER BUILD.  Positivity at every rung to L = 200; ROOT-FREE
   (cepstral) realisability; Theta(L^-2) convergence; the Fejer mean
   preserving <n> exactly; and the ROOT-FINDING CONTROL, which must DEGRADE
   at L = 128 -- F12's warning, gated.

s4 THE CAP IS DISPENSABLE, THE FLOOR IS LOAD-BEARING.  f_V in [1/9, 9] turns
   feasibility alone into ||g||_2 <= 2.343168, ||a_y||_2 <= 1.766965 (gated).
   And the floor has power: at nu ~ 3e-6 the Fejer error in <ln n> does NOT
   vanish (gated).

s5 LEMMA M.  The window distortion identity EXACT, rebuilt cell by cell from
   the primitives, with the edge cell equal to 1 + eps exactly; D-feasible
   with NO rescale; and the THREE MUST-FAIL CONTROLS FOR F5-F8: C(6,n)
   DECREASES by a factor > 4 over n = 64..1024 (so n-independence is FALSE),
   the 18.7 figure is EXCEEDED at n = 64, and the shifted target at
   L = 10, n = 64 is NEGATIVE.  Plus F7's cause: D -> U(L;D) is convex and
   the secant slope over eta exceeds the tangent mu by a factor > 2.

s6 THE THREE-LEG DECOMPOSITION.  Residual < 1e-11 at every row, and
   eta_n = 2L(1 + eps - D)/(n - 2L) exactly.

s7 DOES IT PROVE TOO MUCH?  NO.  Every U_tr rung above the 082 certified
   lower endpoints; the Delta-ladder above block_inf; and the DIRECT
   minimisation records also above Psi^LB, with U_tr(L) strictly above the
   direct optimum at every rung (F11).

s8 THE THEOREM-D MODULUS.  Valid at every one of 28 rungs, zero violations,
   though LOOSE (first order against a truth that is second order).

Sentinel ===GO14FD-JSON=== with ===END===; flag GO14FD_supported.
Pilot seed 20261180 / governed seed 20261181.  SEED STAMPS ONLY: the seed is
recorded in the output and feeds NO computation.  The two random draws (s2's
adversarial FIR records, s7's search restarts) use INTERNALLY PINNED
generators, so pilot and governed produce a bit-identical payload.

Evaluator lineage.  Own evaluator, built from the MODEL PRIMITIVES ONLY, in
the TIME DOMAIN: exact analytic autocovariances; sigma as a Cholesky pivot of
the interleaved (R, S) covariance; <ln n> by Jensen-on-the-roots of the noise
Laurent polynomial.  NO FFT grid and NO Toeplitz normal equations enter any
rate number.  This is the R-IND-5 verifier's lineage, not the prover's; the
pinned kernels are used ONLY as data (a record is data, not a claim).

PILOT RECORD (seed 20261180, 2026-08-08).
 Every bar was fixed from the R-IND-5 verifier's committed artifacts
 (scratchpad rind5FIR/: m3.log, m4_out.json, m5_out.json, m6_out.json,
 m7_out.json, m8b.log; scratchpad firdens/: controls_out.json, ctl2b_out.json)
 and from a pre-pilot calibration of the pinned kernels through this file's
 own evaluator.  NO BAR WAS EVER MOVED AGAINST A MEASUREMENT.
 iter 1 -- 22/23, 19.8 s.  ONE gate failed, and it failed because a BAR WAS
   MIS-SPECIFIED, not because a measurement moved: s4 compared the
   feasibility constants against the SIX-DECIMAL literals 2.343168 /
   1.766965 at a bar of 1e-9, which is four orders BELOW those literals' own
   precision.  The bar could not have been met by any correct computation.
 iter 2 -- ALL PASS 23/23, 19.8 s.  s4's single bar is REPLACED by two
   correctly specified ones: the computed bounds against their CLOSED FORMS
   (rho + sqrt(D/min f_V), 1 + sqrt(D/sn2)) at 1e-12, and against the printed
   six-decimal literals at that literals' own precision, 5e-7.  THE
   MEASUREMENT DID NOT MOVE (0.0e+00 and 3.27e-7 respectively) and no other
   bar anywhere in the file was touched, in either direction.  A governed
   re-run (seed 20261181) reproduced the JSON payload BIT-IDENTICALLY apart
   from the seed stamp and the pilot flag, confirming the seed-stamp-only
   discipline.
 MEASURED vs BAR (the ratio is the margin):
   s1 K-lag ladder decreases from above, excess +1.27180e-2 / +1.08999e-3 /
      +7.9614e-6 / +1.3020e-10 at K = 1/2/4/8 and |excess| 1.67e-16 / 1e-15
      (6.0x) at K = 60, min excess over the ladder -1.67e-16 / -1e-12
      (6.0e3x); SIX MUST-FAIL controls -0.010659 / -0.021585 / -0.023042 /
      -0.012182 / -0.182975 / -0.341884, worst-case (least negative)
      -1.0659e-2 / -5e-3 (2.13x)
   s2 22 pairs / 20 (1.10x), max ||dPhi||_1 14.189 / 5.0 (2.84x); min slack
      sigma(x') <= q(x') +2.826e-11 / -1e-12 (no violations); min slack
      q(x') <= q(x) + C_V||dPhi||_1 +1.834e-5 / 1e-6 (18.3x)
   s3 42 rungs to L = 200 x 3 Delta: min n^(L) 0.133099 / 0.10 (1.33x, and
      it reproduces the recorded ladder minimum 0.1331); root-free
      || |q|^2 - n^(L) ||_inf 4.16e-16 / 1e-14 (24x); MA tail beyond lag L
      4.85e-17 / 1e-15 (20.6x); fitted log-log slope -1.94007/-1.94006/
      -1.94009 in [-2.2, -1.8] (last local slopes -1.98906/-1.98902/
      -1.98902); gaps at L = 200 2.177e-6 / 2.591e-6 / 3.279e-6; <n_L> - <n>
      0.00e+00 / 1e-16 (EXACT); ROOT-FINDING CONTROL residual
      3.86e-16 (L=32) -> 1.13e-13 (64) -> 4.64e-7 (96) -> 1.88e-1 (128),
      gated 1.88e-1 / 1e-3 (188x) against the ROOT-FREE 3.33e-16 at the same
      rung
   s4 f_V range [0.111111, 9.000000], max |endpoint - closed form|
      1.78e-15 / 1e-9 (5.6e5x); feasibility constants ||g||_2 <= 2.3431677
      and ||a_y||_2 <= 1.7669650 against their CLOSED FORMS 0.00e+00 / 1e-12
      and against the printed six-decimal literals 3.27e-7 / 5e-7 (1.53x --
      a rounding check, see iter 2); the record's own norms 0.503553 /
      0.540463 sit under the bounds (4.65x / 3.27x);
      FLOOR CONTROL: at nu = 3.100e-6 the Fejer <ln n> error is 0.3709 / 0.10
      (3.71x) and does NOT vanish, against 9.9e-4 at nu = 0.151
   s5 distortion identity, rebuilt cell by cell from the primitives:
      max |built - formula| 2.22e-16 / 1e-15 (4.5x) over 18 rows, edge cell
      minus (1 + eps) 0.00e+00 / 1e-16 (EXACT), interior cell minus D_stat
      1.67e-16 / 1e-15 (6.0x); D-feasible with NO rescale, |dist - D|
      2.78e-16 / 1e-14 (36x); MUST-FAIL F5: C(6,n) = 72.444 / 20.434 /
      15.194 / 13.426 / 12.676, decrease factor 5.715 / 4.0 (1.43x) --
      n-INDEPENDENCE IS FALSE; MUST-FAIL F6: C(6,64) 72.444 / 18.7 (3.87x);
      MUST-FAIL F8: shifted target at (L=10, n=64) -1.86364e-2 / -1e-3
      (18.6x) with lambda -0.83506; F7: secant slope over eta = 0.161769 is
      9.40818 against tangent mu = 2.2261061, ratio 4.226 / 2.0 (2.11x), and
      the D-ladder second differences are all positive, min +2.140e-3 / 0
      (convexity)
   s6 three-leg residual max 1.85e-13 / 1e-11 (54x) over 14 rows;
      eta_n against 2L(1+eps-D)/(n-2L) max 2.78e-17 / 1e-15 (36x)
   s7 U_tr ladder min margin over Psi^LB +3.9965e-11 / +7.2132e-11 /
      +5.2670e-11, worst 3.9965e-11 / 1e-11 (4.00x) over 30 rungs;
      Delta-ladder margin over block_inf +2.8224e-4 / 1e-4 (2.82x), monotone
      15/15 at three L; DIRECT minimisation 9/9 above Psi^LB, min margin
      +1.1226e-5 / 1e-6 (11.2x) taken over EVERY feasible record evaluated,
      and U_tr(L) - direct >= +9.1608e-6 / 1e-6 (9.2x) at every rung, both
      minima taken over that same set
   s8 28 rungs, 0 violations, min (bound - gap) 1.898e-8 / 1e-9 (19.0x);
      the modulus is LOOSE, gap/bound 3.30e-2 at L=1 down to the f64 floor at
      the deepest Dirichlet rungs
 DISCLOSURES.
 (a) THE ONLY SEARCH in this file is s7's direct minimisation, and BOTH of its
   gates read the MINIMUM OVER EVERY FEASIBLE RECORD THE PINNED, FIXED-BUDGET
   SEARCH EVALUATED, never where the search stops.  Both gates are
   MONOTONE-IMPROVING in search effort -- a longer search adds records to the
   set, lowers that minimum, and can only make "above Psi^LB" and "below
   U_tr" easier -- so neither can race a stopping point in either direction.
   Everything else is exact
   linear algebra on pinned data: Cholesky, slogdet, one polynomial root
   find for <ln n>, and FFTs on fixed grids.  No fixed point is solved
   anywhere and no bracket, width or certificate endpoint is gated.
 (b) THE EQUALITY IS NOT GATED.  L^inf = Psi is a SCOPED THEOREM of the tex;
   this file gates its ingredients and their controls.  No gate reads,
   asserts or implies the equality, and no gate compares a measured value to
   Psi as if Psi were exact -- Psi enters only as the 082 CERTIFIED LOWER
   ENDPOINT, on the safe side, in s3 and s7.
 (c) s3's root-finding control is a NUMERICAL control, not a mathematical
   one: the failure at L = 128 is an artefact of degree-2L root-finding on a
   polynomial whose coefficients span sixteen orders, NOT a failure of
   Fejer-Riesz.  The polynomial is presented with its numerically exact tail
   (an Nf = 4096 symbol round trip) precisely so that the artefact is
   reproduced; the root-FREE route certifies the same rung at 3.33e-16.
 (d) s1's ladder is instantiated on the L = 10 Dirichlet record (F14).  The
   prover instantiated the same lemma on the OPTIMUM and got different
   numbers; both are valid, and this file reports its own.
 (e) F3 is a disclosure, not a gate: this file rebuilds the six controls from
   primitives and never imports firdens/t5_ctl2.py, which still carries the
   lag-sign defect.  The +0.252 / +0.031 no-power values are carried as
   RECORDED LITERALS for the record and are not re-derived.
 (f) NO NOVELTY LANGUAGE is used anywhere for Lemma A''s packaging, Lemma W's
   combination or Theorem D: BOTH SWEEPS ARE OWED.  The window-side la_cmi
   cross-check is also OWED (084's validation was stationary-side only) and
   is not claimed here.
 (g) s5's "18.7" and s7's "0.564769/0.536414/0.531061" are RECORDED
   LITERALS from the prover and from the R-IND-5 addendum's full-strength
   run (8000 evals x 4 restarts).  This file's own search is deliberately
   smaller (900 evals x 2 restarts, pinned) and lands slightly higher in the
   6th-7th decimal; the GATE is against Psi^LB, never against those
   literals.
"""
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
SEED = a_.seed if a_.seed is not None else (20261180 if a_.pilot
                                            else 20261181)
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

# ------------------------------------------------------------------ model
A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
D_TGT = 0.3
LN2 = np.log(2.0)
ALPHA = 1.0 / (2.0 * LN2)
LMAX = 26
EPS_EDGE = 1e-3

# ------------------------------------------------------- recorded literals
# 082 certified LOWER endpoints (tex, "The certified brackets and the
# plateau").  Used ONLY as fixed comparison literals on the safe side.
REC_PSI_LB = {0: 0.5627264963, 1: 0.5364013784, 2: 0.5310500198}
# the anchor-free block infimum (tex R20)
BLOCK_INF = 0.5299499808119
# the multiplier of the stationary program at Delta = 0 (tex, same section)
REC_THETA0 = 3.086038362097
MU = REC_THETA0 / (2.0 * LN2)          # W12's 2.2261061
# F3: the prover's FIRST, DEFECTIVE pass -- carried as a disclosure literal
REC_NOPOWER = {"S_peek": +0.2521530854768266, "R_peek": +0.031249708862140957}
# F6: the withdrawn "~18.7 at L = 6" figure, carried so it can be EXCEEDED
REC_187 = 18.7
# F13: the record noise floors and the Fejer ladder minimum
REC_FLOORS = [0.1495, 0.1378, 0.1404]
REC_LADDER_MIN = 0.1331
# the R-IND-5 addendum's full-strength direct optima (literals; see (g))
REC_DIRECT_L3 = {0: 0.562747377388, 1: 0.536414037072, 2: 0.531061238971}

# ------------------------------------------------------------------- bars
BAR_S1_EXACT = 1e-15            # |K=60 excess| -- A'(1) hits sigma exactly
BAR_S1_ABOVE = -1e-12           # the ladder approaches FROM ABOVE
BAR_S1_CTL = -5e-3              # every must-fail control breaks by this much
BAR_S2_PAIRS = 20
BAR_S2_L1 = 5.0                 # pairs genuinely far from the optimum
BAR_S2_SLACK1 = -1e-12          # zero violations of sigma(x') <= q(x')
BAR_S2_SLACK2 = 1e-6            # zero violations of the L1 modulus
BAR_S3_NMIN = 0.10
BAR_S3_FR = 1e-14
BAR_S3_TAIL = 1e-15
BAR_S3_SLOPE = (-2.2, -1.8)
BAR_S3_MEANN = 1e-16
BAR_S3_ROOTFAIL = 1e-3          # the root-finding control must DEGRADE
BAR_S4_FV = 1e-9
BAR_S4_L2 = 1e-12               # grid vs CLOSED FORM
BAR_S4_ROUND = 5e-7             # agreement with the 6-decimal printed literal
BAR_S4_FLOOR = 0.10             # the <ln n> error must NOT vanish
BAR_S4_NU = 1e-5
BAR_S5_IDENT = 1e-15
BAR_S5_EDGE = 1e-16
BAR_S5_FEAS = 1e-14
BAR_S5_DECREASE = 4.0           # MUST-FAIL: n-independence is FALSE
BAR_S5_SHIFT = -1e-3            # MUST-FAIL: the shifted target is NEGATIVE
BAR_S5_SLOPE = 2.0              # secant / tangent
BAR_S6_RESID = 1e-11
BAR_S6_ETA = 1e-15
BAR_S7_LADDER = 1e-11
BAR_S7_BLOCK = 1e-4
BAR_S7_DIRECT = 1e-6
BAR_S7_UTR = 1e-6               # F11: U_tr strictly above the depth-L optimum
BAR_S8_SLACK = 1e-9


def jsafe(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


# =================================================== PINNED STATIONARY DATA
# Provenance: the stationary K1-K3 grid fixed point at Nf = 4096, P = 180 --
# the same reference W8 names for "R measured <= 1.5e-12".  These are DATA:
# nothing in this file re-derives them, and a record's provenance is
# irrelevant to whether it is a valid feasible upper-bound certificate.
# av, ay are indexed lag -26..+26; q is causal, lags 0..26.
KERN = {
  0: {
    'av': [
      -6.450476633265181e-17, -7.850230023405609e-16, -4.047634011754356e-15,
      -1.610115760411079e-14, -5.442640831886505e-14, -1.5870998588150898e-13,
      -3.835802503983175e-13, -6.352332889473213e-13, 2.570486450556091e-13,
      8.49621102463829e-12, 4.963839785056905e-11, 2.1388260882178258e-10,
      7.786886140307344e-10, 2.464038962356977e-09, 6.619419405289784e-09,
      1.3308896038783364e-08, 6.037699092410926e-09, -1.2812470102075103e-07,
      -9.53070351124991e-07, -4.916875840219957e-06, -2.1795788713239614e-05,
      -8.84765303713428e-05, -0.0003386647727450866, -0.0012443596647975419,
      -0.004452747730056737, -0.01576320613362213, 0.12251085848119367,
      0.05174645218839918, 0.019907268361402324, 0.007177609153696611,
      0.0024553598615864158, 0.0008011284145082431, 0.0002496220649664188,
      7.413429490420905e-05, 2.0869932078211925e-05, 5.5086361928474066e-06,
      1.334403893650497e-06, 2.8291828040577606e-07, 4.5585691163129406e-08,
      1.6040453706191008e-09, -2.9140004954087086e-09, -1.7310915130879086e-09,
      -7.027143221987443e-10, -2.379786947359042e-10, -7.024957326187747e-11,
      -1.7952077552999288e-11, -3.711952663762414e-12, -4.4698816493153623e-13,
      9.134172788219551e-14, 9.412416559499711e-14, 4.5285456262703416e-14,
      1.7062839963627175e-14, 5.492515446206947e-15,
    ],
    'ay': [
      3.0103900159443875e-16, 2.6613680426418585e-15, 1.291144616778956e-14,
      4.967595732078632e-14, 1.6355270373806785e-13, 4.634002006277626e-13,
      1.0708278657998133e-12, 1.5549041000086855e-12, -2.059414512447372e-12,
      -2.961478163295363e-11, -1.6036715447412378e-10, -6.674175698116029e-10,
      -2.369873831702699e-09, -7.3146293035254154e-09, -1.897588973372186e-08,
      -3.5133966802779365e-08, 2.7502602168304223e-09, 4.647712889411191e-07,
      3.1435394687394505e-06, 1.568823832019341e-05, 6.829065495463264e-05,
      0.0002738932339369776, 0.0010392723124324989, 0.0037941384245676222,
      0.013518393494197511, 0.047772802495335775, 0.5358535534854905,
      0.04777280249533576, 0.01351839349419751, 0.0037941384245676222,
      0.0010392723124324986, 0.0002738932339369775, 6.829065495463283e-05,
      1.5688238320192952e-05, 3.1435394687394505e-06, 4.647712889411348e-07,
      2.7502602169816756e-09, -3.513396680276093e-08, -1.8975889733705893e-08,
      -7.314629303536798e-09, -2.369873831847191e-09, -6.674175698543344e-10,
      -1.6036715447412378e-10, -2.961478217797606e-11, -2.059414326590214e-12,
      1.5549041145030188e-12, 1.070827883672598e-12, 4.634001503114447e-13,
      1.6355284273384994e-13, 4.9676055096752685e-14, 1.291144616778956e-14,
      2.661496799788611e-15, 3.0125692773004865e-16,
    ],
    'q': [
      0.41497427253297814, 0.03632666125625934, 0.010282097410146046,
      0.002887835837456342, 0.0007918573563038654, 0.00020898831805633898,
      5.221037023122024e-05, 1.2029356611857272e-05, 2.422981163611472e-06,
      3.632587521610369e-07, 4.822765206472205e-09, -2.6033689368368253e-08,
      -1.4284193836269507e-08, -5.540415965504797e-09, -1.802715460218402e-09,
      -5.098024067316767e-10, -1.2317817042071556e-10, -2.300821138772537e-11,
      -1.7299981434003236e-12, 1.1343405746171203e-12, 8.021775421157255e-13,
      3.4997355753479956e-13, 1.2413704107022216e-13, 3.7868796106782695e-14,
      9.902444167210423e-15, 2.059302072617107e-15, 2.4137545172699477e-16,
    ],
  },
  1: {
    'av': [
      -2.621440736575892e-16, -5.629910213074388e-16, -6.798274214020109e-16,
      2.0281402410553474e-15, 2.1007504959377732e-14, 1.1349867366202117e-13,
      4.97758618590895e-13, 1.9368062057059366e-12, 6.883799379754836e-12,
      2.248640668739226e-11, 6.672986799363724e-11, 1.7255641380897777e-10,
      3.374725697103669e-10, 1.1746839116688867e-10, -3.5737294600718587e-09,
      -2.6709859050337286e-08, -1.4200390804351983e-07, -6.56682747565353e-07,
      -2.806573016418086e-06, -1.139655300962899e-05, -4.469223480834616e-05,
      -0.00017136695552862936, -0.000651368612637499, -0.002500803141617285,
      -0.010580167120112074, 0.04990934574044738, 0.10744067280981731,
      0.04304183836155183, 0.015720661597509254, 0.00547697595687285,
      0.0018417515492132456, 0.0006011109610308124, 0.0001909361004940159,
      5.909376565757479e-05, 1.782208331351868e-05, 5.233258436589694e-06,
      1.4933942792457362e-06, 4.1284698274546566e-07, 1.1000223514449116e-07,
      2.8015708527027143e-08, 6.7227730492058815e-09, 1.4784257758432003e-09,
      2.7917924749571207e-10, 3.588519042182925e-11, -2.491806070598398e-12,
      -4.207979246605495e-12, -2.0980271539085464e-12, -8.085239803420256e-13,
      -2.728286665633568e-13, -8.371610565073172e-14, -2.3584108262709968e-14,
      -6.05737146616517e-15, -1.3756168639426355e-15,
    ],
    'ay': [
      4.204979032989391e-16, 9.9653340922182e-16, 1.8385433838344504e-15,
      4.481974232672217e-16, -1.811264378938374e-14, -1.2315762075400949e-13,
      -5.938349818503051e-13, -2.452260869427801e-12, -9.141728168361391e-12,
      -3.129214985592604e-11, -9.821179510360848e-11, -2.7655408768045793e-10,
      -6.526346203403298e-10, -9.685716258921532e-10, 1.6991210704057212e-09,
      2.4552619814972736e-08, 1.5089050376929647e-07, 7.459743600621338e-07,
      3.3156960271308043e-06, 1.3813270696311901e-05, 5.509846671209834e-05,
      0.0002133675735234937, 0.0008116231252382095, 0.003078793665513188,
      0.01189633356282469, 0.05282686336071028, 0.5180588002130597,
      0.052826863360710276, 0.01189633356282469, 0.0030787936655131878,
      0.0008116231252382095, 0.00021336757352349368, 5.509846671209845e-05,
      1.3813270696311193e-05, 3.3156960271308043e-06, 7.459743600624482e-07,
      1.5089050376942842e-07, 2.4552619814976703e-08, 1.6991210704190772e-09,
      -9.68571625861773e-10, -6.526346204595894e-10, -2.765540876165875e-10,
      -9.821179510360848e-11, -3.129215069824848e-11, -9.141728103939113e-12,
      -2.452260878408952e-12, -5.938349672591434e-13, -1.231576573332064e-13,
      -1.8112506494944378e-14, 4.481353079262268e-16, 1.8385433838344504e-15,
      9.968212118819855e-16, 4.207289565947864e-16,
    ],
    'q': [
      0.4046745380737573, 0.040728453556788155, 0.009138846443904142,
      0.0023639405610546447, 0.0006232351344876685, 0.00016392844618515992,
      4.2367330237172267e-05, 1.0634169428313701e-05, 2.556860059409257e-06,
      5.766952937167683e-07, 1.1715883586545043e-07, 1.9259510178800103e-08,
      1.4253327324061903e-09, -7.098975920007632e-10, -4.922389979912314e-10,
      -2.102039014480291e-10, -7.495488514932834e-11, -2.395278298647475e-11,
      -7.0162526192989755e-12, -1.887571269489434e-12, -4.588548750895738e-13,
      -9.579779659237518e-14, -1.435687143852756e-14, 1.9655742566823037e-16,
      1.3694162973883698e-15, 7.524837992601442e-16, 3.190881173633522e-16,
    ],
  },
  2: {
    'av': [
      2.0800884218028134e-16, 8.858577174930809e-16, 3.237350285868632e-15,
      1.0445975057020953e-14, 3.5413236496575377e-14, 1.2188674252051586e-13,
      3.394799748964242e-13, 7.317557504830825e-13, 1.5782905705555501e-12,
      1.9192401202986405e-12, -2.012222773627993e-11, -1.6901950306606524e-10,
      -7.730830001463328e-10, -3.4990684976409404e-09, -1.7631038664765684e-08,
      -7.671013318167903e-08, -2.8209751221649494e-07, -1.1231027502383675e-06,
      -5.013711821209665e-06, -1.931065641966363e-05, -6.34181652939232e-05,
      -0.0002690302496636622, -0.0014818292816295127, -0.0058337266080475975,
      0.01841218992517986, 0.04275722323152771, 0.10310451979316956,
      0.040918574663944926, 0.014610862755045634, 0.00482680422022977,
      0.0015583803509355385, 0.0005030076501133864, 0.00016014838514473735,
      4.987243110329256e-05, 1.5322285653582683e-05, 4.67171643806105e-06,
      1.4070409691331414e-06, 4.1740737104191746e-07, 1.2243637217907303e-07,
      3.5577605483695596e-08, 1.0207518006227899e-08, 2.8871991190187433e-09,
      8.069768388930916e-10, 2.2291156424563982e-10, 6.06461568950813e-11,
      1.6228195865053168e-11, 4.2768034498851205e-12, 1.1082612948122034e-12,
      2.8096314126957357e-13, 6.951305907154198e-14, 1.6773058098842194e-14,
      3.919913746018788e-15, 8.738404345459304e-16,
    ],
    'ay': [
      -1.2223862290701677e-16, -4.524156324875108e-16, -1.9933042849854987e-15,
      -8.563754951947085e-15, -2.7206499092114964e-14, -7.890422952079215e-14,
      -2.9837282134652664e-13, -1.0338592496731382e-12, -2.132125698239063e-12,
      -2.937817465101474e-12, -9.256093781843314e-12, 4.346749634668246e-12,
      3.7225398358387517e-10, 2.0536462765750932e-09, 7.144304220913067e-09,
      3.4542670730489116e-08, 1.8929853240550056e-07, 7.32028382908184e-07,
      2.349841251212604e-06, 1.050099043832809e-05, 5.0755755957334895e-05,
      0.0001692271226609545, 0.00047923451999641294, 0.0027000016913993926,
      0.016804313257691578, 0.05050022169181999, 0.5146864256304877,
      0.05050022169181999, 0.016804313257691578, 0.002700001691399392,
      0.00047923451999641283, 0.00016922712266095446, 5.075575595733515e-05,
      1.0500990438327579e-05, 2.349841251212604e-06, 7.320283829084367e-07,
      1.8929853240559882e-07, 3.4542670730481135e-08, 7.144304220922011e-09,
      2.0536462765775855e-09, 3.722539833167682e-10, 4.346749325075728e-12,
      -9.256093781843314e-12, -2.937817843672225e-12, -2.132125319331303e-12,
      -1.033859256686339e-12, -2.983728163778946e-13, -7.89042622936554e-14,
      -2.7206321474855255e-14, -8.563995986151273e-15, -1.9933042849854987e-15,
      -4.521513373366794e-16, -1.219342925207293e-16,
    ],
    'q': [
      0.4020725579022354, 0.03853519224181817, 0.013049294490584444,
      0.002091545117189671, 0.00036449049608152804, 0.00012952577432331444,
      3.922011321590537e-05, 8.096430744997191e-06, 1.7956991247609615e-06,
      5.627795111355358e-07, 1.466544205539454e-07, 2.6683685497995844e-08,
      5.476249167079794e-09, 1.592539236025878e-09, 2.936305740090724e-10,
      4.184153370717625e-12, -7.043906298235963e-12, -2.138374182087169e-12,
      -1.5990504332330159e-12, -7.919283711752335e-13, -2.290136116064051e-13,
      -6.005927404761882e-14, -2.078636790233742e-14, -6.6010500960414205e-15,
      -1.5348046163870963e-15, -3.4731217831394823e-16, -9.140238502366124e-17,
    ],
  },
}


def kern(Delta):
    """taps of the pinned stationary record at lags -LMAX..LMAX (g, a_y) and
    the noise autocovariance at lags 0..LMAX."""
    d = KERN[Delta]
    av = np.asarray(d["av"], float)
    ay = np.asarray(d["ay"], float)
    q = np.asarray(d["q"], float)
    g = av + RHO * ay
    cz = np.array([float(np.dot(q[:len(q) - m], q[m:])) for m in range(len(q))])
    return g, ay, cz


def window(L, kind):
    k = np.arange(-LMAX, LMAX + 1)
    if kind == "dir":
        return (np.abs(k) <= L).astype(float)
    return np.maximum(0.0, 1.0 - np.abs(k) / (L + 1.0))


# ============================================== grid-free record evaluator
class Rec:
    """a stationary record of F0 on Z: Yhat = g*V + a_y*N + Z, finite taps,
    Z an independent stationary noise with autocovariance cz[0..Lz].
    R_u := Yhat_{u-Delta-1} (the shifted frame of the tex)."""

    def __init__(self, g, gof, by, byof, cz, Delta):
        self.g = np.asarray(g, float)
        self.gof = int(gof)
        self.by = np.asarray(by, float)
        self.byof = int(byof)
        self.cz = np.asarray(cz, float)
        self.Delta = int(Delta)

    def covR_vec(self, kmax):
        k = np.arange(0, kmax + 1)
        acg = np.convolve(self.g, self.g[::-1])
        dv = np.arange(-(len(self.g) - 1), len(self.g))
        t1 = acg @ (A_ ** np.abs(k[None, :] - dv[:, None]))
        acb = np.convolve(self.by, self.by[::-1])
        t2 = np.zeros(kmax + 1)
        s = k <= len(self.by) - 1
        t2[s] = SN2 * acb[k[s] + len(self.by) - 1]
        t3 = np.zeros(kmax + 1)
        s2 = k < len(self.cz)
        t3[s2] = self.cz[k[s2]]
        return t1 + t2 + t3

    def covRS_vec(self, kmin, kmax):
        """E[R_{u+k} S_u], k = kmin..kmax."""
        k = np.arange(kmin, kmax + 1)
        jg = np.arange(self.gof, self.gof + len(self.g))
        kk = k - self.Delta - 1
        return (A_ ** np.abs(kk[:, None] - jg[None, :])) @ self.g

    def sigma(self, m=200):
        """Var(R_u | R^{u-1}, S^{u-1}): a Cholesky pivot of the interleaved
        (R, S) covariance in the order R_1, S_1, ..., R_m, S_m."""
        cR = self.covR_vec(m)
        i = np.arange(m)
        d = i[:, None] - i[None, :]
        cRS = self.covRS_vec(-(m - 1), m - 1)
        M = np.zeros((2 * m, 2 * m))
        M[0::2, 0::2] = cR[np.abs(d)]
        M[1::2, 1::2] = A_ ** np.abs(d) + TAU2 * (d == 0)
        M[0::2, 1::2] = cRS[d + (m - 1)]
        M[1::2, 0::2] = cRS[d + (m - 1)].T
        Lc = np.linalg.cholesky(M)
        return float(Lc[2 * (m - 1), 2 * (m - 1)] ** 2)

    def mean_log_n(self):
        return mean_log_laurent(self.cz)

    def dist(self):
        gm = self.g.copy()
        jg = np.arange(self.gof, self.gof + len(gm))
        gm = gm - RHO * (jg == 0)
        t1 = float(gm @ (A_ ** np.abs(jg[:, None] - jg[None, :])) @ gm)
        bm = self.by.copy()
        ja = np.arange(self.byof, self.byof + len(bm))
        bm = bm - (ja == 0)
        return t1 + SN2 * float(bm @ bm) + float(self.cz[0])

    def rate(self, m=200):
        return (np.log(self.sigma(m)) - self.mean_log_n()) * ALPHA


def mean_log_laurent(c):
    """<ln P> for P(e^{iw}) = sum_{|k|<=L} c[|k|] e^{ikw} > 0, by Jensen on
    the roots.  No FFT grid."""
    c = np.asarray(c, float)
    L = len(c) - 1
    while L > 0 and abs(c[L]) < 1e-300:
        L -= 1
    if L == 0:
        return float(np.log(c[0]))
    poly = np.array([c[abs(k)] for k in range(-L, L + 1)])
    r = np.roots(poly[::-1])
    return float(np.log(abs(poly[-1]))
                 + np.sum(np.log(np.abs(r[np.abs(r) > 1.0]))))


def trunc_record(Delta, L, kind="dir", Dt=D_TGT):
    """the depth-L FIR stationary record: window the pinned kernels, then the
    EXACT scalar noise rescale landing at distortion Dt (closed form; no root
    find).  kind = 'dir' (Dirichlet) or 'fej' (Fejer mean)."""
    g, ay, cz = kern(Delta)
    win = window(L, kind)
    gL, ayL = g * win, ay * win
    czL = cz * win[LMAX:]
    r0 = Rec(gL, -LMAX, ayL, -LMAX, np.zeros(len(czL)), Delta)
    lam = (Dt - r0.dist()) / czL[0]
    return Rec(gL, -LMAX, ayL, -LMAX, lam * czL, Delta), float(lam)


# ------------------------------------------------- covariance helpers (lag)
def cRRv(rec, d):
    return rec.covR_vec(int(np.abs(d).max()))[np.abs(d)]


def cSSv(d):
    return A_ ** np.abs(d) + TAU2 * (d == 0)


def cRSv(rec, d):
    lo, hi = int(d.min()), int(d.max())
    return rec.covRS_vec(lo, hi)[d - lo]


def pivot_general(rec, iR, iS):
    """Var(R_u - proj onto span{R_{u-i}: i in iR} u {S_{u-j}: j in iS}).
    iR/iS carrying NEGATIVE entries is exactly a PEEKING filter."""
    iR, iS = np.asarray(iR), np.asarray(iS)
    Krs = cRSv(rec, iS[None, :] - iR[:, None])
    K = np.block([[cRRv(rec, iR[:, None] - iR[None, :]), Krs],
                  [Krs.T, cSSv(iS[:, None] - iS[None, :])]])
    rhs = np.concatenate([cRRv(rec, iR), cRSv(rec, iS)])
    return float(cRRv(rec, np.array([0]))[0]
                 - rhs @ np.linalg.solve(K, rhs))


def opt_filter(rec, iR, iS):
    iR, iS = np.asarray(iR), np.asarray(iS)
    Krs = cRSv(rec, iS[None, :] - iR[:, None])
    K = np.block([[cRRv(rec, iR[:, None] - iR[None, :]), Krs],
                  [Krs.T, cSSv(iS[:, None] - iS[None, :])]])
    return np.linalg.solve(K, np.concatenate([cRRv(rec, iR), cRSv(rec, iS)]))


def qform(rec, v, vs):
    """Var(sum_i v_i R_{u-i} + sum_j vs_j S_{u-j}), taps at lags 0.. ."""
    iv = np.arange(len(v))
    js = np.arange(len(vs))
    return float(v @ cRRv(rec, iv[None, :] - iv[:, None]) @ v
                 + vs @ cSSv(js[None, :] - js[:, None]) @ vs
                 + 2 * v @ cRSv(rec, js[None, :] - iv[:, None]) @ vs)


# ------------------------------------------------------- spectra (L1 side)
NWS = 1 << 14
WS = 2 * np.pi * np.arange(NWS) / NWS
ZS = np.exp(-1j * WS)
FV = (1 - A_ ** 2) / np.abs(1 - A_ * ZS) ** 2
FS = FV + TAU2


def symb(taps, off):
    k = np.arange(off, off + len(taps))
    return (np.asarray(taps)[:, None] * ZS[None, :] ** k[:, None]).sum(0)


def spec(rec):
    g = symb(rec.g, rec.gof)
    by = symb(rec.by, rec.byof)
    nz = np.real(symb(np.concatenate([rec.cz[::-1][:-1], rec.cz]),
                      -(len(rec.cz) - 1)))
    gR = ZS ** (rec.Delta + 1) * g
    return (np.abs(gR) ** 2 * FV + SN2 * np.abs(by) ** 2 + nz, gR * FV, nz)


# -------------------------------------------------- the zero-edge build (Z)
def zero_edge(rec, L, n, eps=EPS_EDGE):
    """the ZERO-EDGE window build: interior rows [L, n-L) carry the full
    depth-L taps; the 2L edge cells are PURE independent noise of variance
    eps; N_cov is BLOCK DIAGONAL."""
    Delta = rec.Delta
    t = np.arange(n)
    inter = (t >= L) & (t < n - L)
    d = t[:, None] - t[None, :]
    CY = np.zeros((n, n))
    II = np.outer(inter, inter)
    CY[II] = cRRv(rec, d)[II]
    e = np.where(~inter)[0]
    CY[e, e] = eps
    CYS = np.zeros((n, n))
    CYS[inter, :] = cRSv(rec, d + Delta + 1)[inter, :]
    CSS = cSSv(d)
    m0 = n - 2 * L
    czf = np.zeros(max(m0, len(rec.cz)))
    czf[:len(rec.cz)] = rec.cz
    T = czf[np.abs(np.arange(m0)[:, None] - np.arange(m0)[None, :])]
    lndetN = 2 * L * np.log(eps) + float(np.linalg.slogdet(T)[1])
    kind, idx = [], []
    snext = 0
    for tt in range(n):
        while snext <= min(tt + Delta, n - 1):
            kind.append(0)
            idx.append(snext)
            snext += 1
        kind.append(1)
        idx.append(tt)
    kind, idx = np.array(kind), np.array(idx)
    iS, iR = np.where(kind == 0)[0], np.where(kind == 1)[0]
    aS, aR = idx[iS], idx[iR]
    K = np.empty((len(kind), len(kind)))
    K[np.ix_(iS, iS)] = CSS[np.ix_(aS, aS)]
    K[np.ix_(iR, iR)] = CY[np.ix_(aR, aR)]
    K[np.ix_(iR, iS)] = CYS[np.ix_(aR, aS)]
    K[np.ix_(iS, iR)] = CYS[np.ix_(aR, aS)].T
    sig = np.diag(np.linalg.cholesky(K)) ** 2
    sig = sig[iR]
    La = float((np.sum(np.log(sig)) - lndetN) / (2 * LN2 * n))
    Dstat = rec.dist()
    return dict(La=La, sig=sig, Dstat=float(Dstat), T=T, lndetN=lndetN,
                dist_formula=float(Dstat + 2 * L * (1.0 + eps - Dstat) / n))


def cell_distortion(rec, L, n, eps=EPS_EDGE):
    """per-cell E[(Yhat_t - Y_t)^2] REBUILT FROM THE PRIMITIVES: interior
    cells from the record's own second moments, edge cells from the fact that
    they are pure independent noise of variance eps."""
    jg = np.arange(rec.gof, rec.gof + len(rec.g))
    ja = np.arange(rec.byof, rec.byof + len(rec.by))
    varYh = float(rec.g @ (A_ ** np.abs(jg[:, None] - jg[None, :])) @ rec.g) \
        + SN2 * float(rec.by @ rec.by) + float(rec.cz[0])
    cov = RHO * float(rec.g @ (A_ ** np.abs(jg))) \
        + SN2 * float(rec.by[ja == 0].sum())
    d_int = varYh - 2 * cov + 1.0
    d_edge = eps + 1.0
    t = np.arange(n)
    inter = (t >= L) & (t < n - L)
    per = np.where(inter, d_int, d_edge)
    return float(per.mean()), float(d_int), float(d_edge)


# ============================================================= s1 LEMMA A'(1)
print("s1 LEMMA A'(1) -- sigma is the inf over FINITELY SUPPORTED admissible "
      "filters, and the SIX must-fail controls", flush=True)
recA, _ = trunc_record(0, 10, "dir")        # F14: the L=10 DIRICHLET record
sigA = recA.sigma(m=200)
ladder = []
for K in (1, 2, 4, 8, 16, 32, 60):
    p = pivot_general(recA, np.arange(1, K + 1), np.arange(1, K + 1))
    ladder.append((K, p, p - sigA))
lad_dec = all(ladder[i][1] >= ladder[i + 1][1] - 1e-15
              for i in range(len(ladder) - 1))
lad_min = min(x[2] for x in ladder)
lad_exact = abs(ladder[-1][2])
P = 60
base = pivot_general(recA, np.arange(1, P + 1), np.arange(1, P + 1))
ctl = {}
ctl["S-peek (uses S_u), fully optimised"] = pivot_general(
    recA, np.arange(1, P + 1), np.arange(0, P + 1)) - base
ctl["R-peek (uses R_{u+1}), fully optimised"] = pivot_general(
    recA, np.concatenate([[-1], np.arange(1, P + 1)]),
    np.arange(1, P + 1)) - base
ctl["R-peek two-step (R_{u+1}, R_{u+2})"] = pivot_general(
    recA, np.concatenate([[-2, -1], np.arange(1, P + 1)]),
    np.arange(1, P + 1)) - base
ctl["S-peek two-step (S_u, S_{u+1})"] = pivot_general(
    recA, np.arange(1, P + 1), np.arange(-1, P + 1)) - base
cbest = opt_filter(recA, np.arange(1, P + 1), np.arange(1, P + 1))
ctl["non-monic V(0)=0.3, rest optimal"] = qform(
    recA, np.concatenate([[0.3], -cbest[:P]]),
    np.concatenate([[0.0], -cbest[P:]])) - base
iR_, iS_ = np.arange(1, P + 1), np.arange(1, P + 1)
Krs_ = cRSv(recA, iS_[None, :] - iR_[:, None])
K_ = np.block([[cRRv(recA, iR_[:, None] - iR_[None, :]), Krs_],
               [Krs_.T, cSSv(iS_[:, None] - iS_[None, :])]])
rhs_ = np.concatenate([cRRv(recA, iR_), cRSv(recA, iS_)])
c03 = np.linalg.solve(K_, 0.3 * rhs_)
ctl["non-monic V(0)=0.3, fully re-optimised"] = (
    0.09 * cRRv(recA, np.array([0]))[0] - 0.3 * rhs_ @ c03) - base
ctl_worst = max(ctl.values())
vals["s1"] = {"record": "L=10 Dirichlet truncation at Delta=0 (F14)",
              "sigma": sigA, "ladder": ladder, "decreasing": lad_dec,
              "min_excess": lad_min, "exact_at_K60": lad_exact,
              "controls": ctl, "worst_control": ctl_worst,
              "bar_exact": BAR_S1_EXACT, "bar_above": BAR_S1_ABOVE,
              "bar_ctl": BAR_S1_CTL,
              "F3_prover_first_pass_no_power": REC_NOPOWER,
              "F3_run_of_record": "scratchpad firdens/t5b.py; t5_ctl2.py is "
                                  "DEFECTIVE (lag-sign) and is not cited",
              "note": "the infimum is NOT ATTAINED by any finite filter; only "
                      "eps-optimality is used.  Hypotheses: Phi_R, f_S in L1 "
                      "and nothing else"}
verdicts["s1_K_lag_ladder_decreases_to_sigma_from_above_and_is_exact"] = (
    lad_dec and lad_min >= BAR_S1_ABOVE and lad_exact < BAR_S1_EXACT)
verdicts["s1_all_six_admissibility_controls_BREAK"] = (
    len(ctl) == 6 and ctl_worst < BAR_S1_CTL)
for K, p, ex in ladder:
    print(f"  K={K:3d} admissible finite filter {p:.15f}  excess {ex:+.3e}")
print(f"  decreasing {lad_dec}, min excess {lad_min:+.3e} >= "
      f"{BAR_S1_ABOVE:.0e}, |excess| at K=60 {lad_exact:.2e} < "
      f"{BAR_S1_EXACT:.0e}")
for k, v in ctl.items():
    print(f"  MUST-FAIL {k:<42s} {v:+.6f}  "
          f"{'BREAKS' if v < BAR_S1_CTL else 'NO POWER'}")
print(f"  worst (least negative) control {ctl_worst:+.6f} < "
      f"{BAR_S1_CTL:+.0e}; F3 -- the prover's FIRST pass had NO POWER "
      f"(S-peek {REC_NOPOWER['S_peek']:+.3f}, R-peek "
      f"{REC_NOPOWER['R_peek']:+.3f}) [{time.time()-t0:.0f}s]", flush=True)

# ============================================================= s2 LEMMA A'(2)
print("s2 LEMMA A'(2) -- both inequalities on adversarial record pairs, "
      "including records far from the optimum", flush=True)
rng2 = np.random.default_rng(20260808)      # internally pinned
Kf = 20
cb2 = opt_filter(recA, np.arange(1, Kf + 1), np.arange(1, Kf + 1))
vK = np.concatenate([[1.0], -cb2[:Kf]])
vsK = np.concatenate([[0.0], -cb2[Kf:]])
C_V = float(np.max(np.abs(symb(vK, 0)) ** 2 + np.abs(symb(vsK, 0)) ** 2))
PR0, PRS0, _ = spec(recA)
q_x = qform(recA, vK, vsK)
cases = []
for L in (1, 2, 3, 5, 8):
    cases.append((f"dirichlet L={L}", trunc_record(0, L, "dir")[0]))
    cases.append((f"fejer L={L}", trunc_record(0, L, "fej")[0]))
for tt in range(12):
    Lr = int(rng2.integers(1, 7))
    dec = 0.6 ** np.abs(np.arange(-Lr, Lr + 1))
    cg = rng2.normal(size=2 * Lr + 1) * dec
    cay = rng2.normal(size=2 * Lr + 1) * dec
    qz = rng2.normal(size=Lr + 1)
    qz[0] = abs(qz[0]) + 0.4
    czr = np.array([float(np.dot(qz[:len(qz) - m], qz[m:]))
                    for m in range(len(qz))])
    cases.append((f"random FIR #{tt}", Rec(cg, -Lr, cay, -Lr, czr, 0)))
sl1, sl2, l1s = [], [], []
for name, rp in cases:
    PR1, PRS1, _ = spec(rp)
    l1 = float(np.mean(np.abs(PR1 - PR0) + np.abs(PRS1 - PRS0)))
    q_xp = qform(rp, vK, vsK)
    sl1.append(q_xp - rp.sigma(m=140))
    sl2.append((q_x + C_V * l1) - q_xp)
    l1s.append(l1)
vals["s2"] = {"pairs": len(cases), "C_V": C_V, "max_L1": max(l1s),
              "min_slack_sigma_le_q": min(sl1),
              "min_slack_q_le_q_plus_CV_L1": min(sl2),
              "violations": int(sum(1 for x in sl1 if x < BAR_S2_SLACK1)
                                + sum(1 for x in sl2 if x <= 0.0)),
              "bars": [BAR_S2_PAIRS, BAR_S2_L1, BAR_S2_SLACK1,
                       BAR_S2_SLACK2]}
verdicts["s2_zero_violations_of_both_A_prime_inequalities"] = (
    len(cases) >= BAR_S2_PAIRS and max(l1s) > BAR_S2_L1
    and min(sl1) >= BAR_S2_SLACK1 and min(sl2) > BAR_S2_SLACK2)
print(f"  {len(cases)} pairs (>= {BAR_S2_PAIRS}), C_V = {C_V:.6f}, max "
      f"||dPhi||_1 = {max(l1s):.3f} > {BAR_S2_L1}")
print(f"  min slack sigma(x') <= q(x')             {min(sl1):+.3e} "
      f">= {BAR_S2_SLACK1:.0e}")
print(f"  min slack q(x') <= q(x) + C_V ||dPhi||_1 {min(sl2):+.3e} "
      f"> {BAR_S2_SLACK2:.0e} [{time.time()-t0:.0f}s]", flush=True)

# ================================================================== s3 FEJER
print("s3 THE FEJER BUILD -- positivity, ROOT-FREE realisability, "
      "Theta(L^-2), and the root-finding control that must degrade",
      flush=True)
NWC = 1 << 15
WC = 2 * np.pi * np.arange(NWC) / NWC


def noise_spec(cz):
    P = np.zeros(NWC)
    for k in range(-(len(cz) - 1), len(cz)):
        P += cz[abs(k)] * np.cos(k * WC)
    return P


def cepstral(cz):
    """min-phase MA factor by the ROOT-FREE (cepstral / Kolmogorov) route."""
    L = len(cz) - 1
    P = noise_spec(cz)
    if P.min() <= 0:
        return None, float(P.min()), np.nan, np.nan
    c = np.fft.ifft(np.log(P))
    h = c.copy()
    h[1:NWC // 2] *= 2
    h[NWC // 2:] = 0
    Q = np.exp(np.fft.fft(0.5 * h))
    qt = np.real(np.fft.ifft(Q))
    return (qt[:L + 1], float(P.min()),
            float(np.max(np.abs(np.abs(Q) ** 2 - P))),
            float(np.max(np.abs(qt[L + 1:NWC // 2]))))


def tail_presentation(cz, L):
    """the SAME nonnegative trig polynomial, carried through an Nf = 4096
    symbol round trip so that its numerically exact tail is present, then
    Fejer-windowed to lag L.  This is the degree-2L presentation the
    root-finding route has to face."""
    nf = 4096
    Lz = len(cz) - 1
    c = np.zeros(nf)
    c[:Lz + 1] = cz
    c[-Lz:] = cz[1:][::-1]
    t = np.real(np.fft.ifft(np.real(np.fft.fft(c))))
    k = np.arange(L + 1)
    return t[:L + 1] * np.maximum(0.0, 1.0 - k / (L + 1.0))


def fejer_riesz_roots(c):
    """the ROOT-FINDING route -- kept ONLY as a control."""
    c = np.asarray(c, float)
    L = len(c) - 1
    poly = np.array([c[abs(k)] for k in range(-L, L + 1)])
    r = np.roots(poly[::-1])
    sel = list(r[np.abs(r) < 1.0])
    q = np.poly(sel)[::-1] if len(sel) else np.array([1.0])
    qq = np.asarray(q, complex)
    cc = np.convolve(qq, np.conj(qq[::-1]))
    k0 = len(qq) - 1
    qq = qq * np.sqrt(c[0] / np.real(cc[k0]))
    cc = np.convolve(qq, np.conj(qq[::-1]))
    return float(np.max(np.abs(np.real(cc[k0:k0 + L + 1]) - c)))


LS3 = [1, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160, 200]
LS3_FIT = [L for L in LS3 if L >= 8]
fej = {}
nmins, frs, tails, dn0s = [], [], [], []
for Delta in (0, 1, 2):
    rows = []
    for L in LS3:
        r, lam = trunc_record(Delta, L, "fej")
        _, cz0 = kern(Delta)[2][0], kern(Delta)[2]
        qt, pmin, fr, tail = cepstral(r.cz)
        gap = r.rate(m=max(160, 2 * L + 80)) - REC_PSI_LB[Delta]
        # the Fejer mean preserves <n> EXACTLY (lag-0 tap untouched)
        dn0 = abs((cz0 * window(L, "fej")[LMAX:])[0] - cz0[0])
        rows.append(dict(L=L, rate=gap + REC_PSI_LB[Delta], gap=gap,
                         nmin=pmin, fr=fr, tail=tail, lam=lam, dn0=dn0))
        nmins.append(pmin)
        frs.append(fr)
        tails.append(tail)
        dn0s.append(dn0)
    g = np.array([x["gap"] for x in rows if x["L"] in LS3_FIT])
    Lv = np.array(LS3_FIT, float)
    slope = float(np.polyfit(np.log(Lv), np.log(g), 1)[0])
    loc = float((np.log(g[-1]) - np.log(g[-2]))
                / (np.log(Lv[-1]) - np.log(Lv[-2])))
    fej[Delta] = dict(rows=rows, slope=slope, local_slope=loc,
                      gap200=rows[-1]["gap"])
    print(f"  Delta={Delta}: gap at L=200 {rows[-1]['gap']:.3e}, fitted "
          f"log-log slope {slope:+.4f} in [{BAR_S3_SLOPE[0]},"
          f"{BAR_S3_SLOPE[1]}], last local slope {loc:+.4f}")
root_ctl = {}
for L in (32, 64, 96, 128, 160, 200):
    r, lam = trunc_record(0, L, "fej")
    root_ctl[L] = fejer_riesz_roots(tail_presentation(kern(0)[2], L) * lam)
rootfree_128 = [x["fr"] for x in fej[0]["rows"] if x["L"] == 128][0]
slopes_ok = all(BAR_S3_SLOPE[0] <= fej[d]["slope"] <= BAR_S3_SLOPE[1]
                for d in (0, 1, 2))
vals["s3"] = {"rungs": len(nmins), "min_nmin": min(nmins),
              "max_rootfree_residual": max(frs), "max_MA_tail": max(tails),
              "max_dmean_n": max(dn0s),
              "slopes": {d: fej[d]["slope"] for d in (0, 1, 2)},
              "local_slopes": {d: fej[d]["local_slope"] for d in (0, 1, 2)},
              "gap_at_200": {d: fej[d]["gap200"] for d in (0, 1, 2)},
              "root_finding_control": root_ctl,
              "rootfree_at_128": rootfree_128,
              "ladder_min_recorded": REC_LADDER_MIN,
              "bars": [BAR_S3_NMIN, BAR_S3_FR, BAR_S3_TAIL, BAR_S3_SLOPE,
                       BAR_S3_MEANN, BAR_S3_ROOTFAIL],
              "note": "F12 -- realisability is certified ROOT-FREE; "
                      "polynomial root-finding is NOT FIT FOR PURPOSE beyond "
                      "L ~ 96 and is carried only as a control"}
verdicts["s3_Fejer_positive_at_every_rung"] = min(nmins) > BAR_S3_NMIN
verdicts["s3_root_free_Fejer_Riesz_realisability_at_every_rung"] = (
    max(frs) < BAR_S3_FR and max(tails) < BAR_S3_TAIL)
verdicts["s3_Theta_L_minus_2_convergence"] = slopes_ok
verdicts["s3_Fejer_mean_preserves_mean_n_exactly"] = max(dn0s) < BAR_S3_MEANN
verdicts["s3_MUSTFAIL_root_finding_route_degrades_at_L128"] = (
    root_ctl[128] > BAR_S3_ROOTFAIL and rootfree_128 < BAR_S3_FR)
print(f"  {len(nmins)} rungs: min n^(L) {min(nmins):.6f} > {BAR_S3_NMIN} "
      f"(recorded ladder minimum {REC_LADDER_MIN}); root-free "
      f"|| |q|^2 - n^(L) ||_inf {max(frs):.2e} < {BAR_S3_FR:.0e}; MA tail "
      f"beyond lag L {max(tails):.2e} < {BAR_S3_TAIL:.0e}")
print(f"  Fejer mean preserves <n>: max |<n_L> - <n>| = {max(dn0s):.2e}")
print("  MUST-FAIL root-finding control: "
      + " ".join(f"L={L}:{v:.2e}" for L, v in root_ctl.items())
      + f" -- at L=128 {root_ctl[128]:.2e} > {BAR_S3_ROOTFAIL:.0e} against "
        f"the root-free {rootfree_128:.2e} [{time.time()-t0:.0f}s]",
      flush=True)

# ============================================ s4 CAP DISPENSABLE, FLOOR REAL
print("s4 THE CAP IS DISPENSABLE (F4d) AND THE FLOOR IS LOAD-BEARING (F4c)",
      flush=True)
fv_lo, fv_hi = float(FV.min()), float(FV.max())
bnd_g = RHO + np.sqrt(D_TGT / fv_lo)
bnd_ay = 1.0 + np.sqrt(D_TGT / SN2)
gsym = np.real(symb(kern(0)[0], -LMAX))
aysym = np.real(symb(kern(0)[1], -LMAX))
n2_g = float(np.sqrt(np.mean(gsym ** 2)))
n2_ay = float(np.sqrt(np.mean(aysym ** 2)))
fv_err = max(abs(fv_lo - 1.0 / 9.0), abs(fv_hi - 9.0))
# the CLOSED FORMS: min f_V = (1-a^2)/(1+a)^2, max f_V = (1-a^2)/(1-a)^2
fv_lo_cf = (1 - A_ ** 2) / (1 + A_) ** 2
bnd_g_cf = RHO + np.sqrt(D_TGT / fv_lo_cf)
bnd_ay_cf = 1.0 + np.sqrt(D_TGT / SN2)
l2_err = max(abs(bnd_g - bnd_g_cf), abs(bnd_ay - bnd_ay_cf))
# and the agreement with the 6-decimal literals PRINTED in the tex, at the
# precision those literals carry
round_err = max(abs(bnd_g - 2.343168), abs(bnd_ay - 1.766965))
_, ay0, cz0 = kern(0)
g0 = kern(0)[0]
nz0 = np.real(symb(np.concatenate([cz0[::-1][:-1], cz0]), -(len(cz0) - 1)))
dsig = float(np.mean(np.abs(np.real(symb(g0, -LMAX)) - RHO) ** 2 * FV
                     + np.abs(np.real(symb(ay0, -LMAX)) - 1.0) ** 2 * SN2))


def fejer_grid(x, L):
    c = np.fft.ifft(x)
    k = np.arange(NWS)
    kk = np.minimum(k, NWS - k)
    return np.real(np.fft.fft(c * np.maximum(0.0, 1.0 - kk / (L + 1.0))))


floor_rows = []
for p in (0.0, 0.9, 0.99, 0.999, 0.99999):
    nv = nz0 * (1.0 - p * np.cos(WS) ** 2)
    nv = nv * (D_TGT - dsig) / float(np.mean(nv))
    mln = float(np.mean(np.log(nv)))
    nL = fejer_grid(nv, 16)
    mlnL = float(np.mean(np.log(np.maximum(nL, 1e-300))))
    floor_rows.append(dict(p=p, nu=float(nv.min()), err=abs(mlnL - mln),
                           L1=float(np.mean(np.abs(nL - nv)))))
    print(f"  floor control p={p:<8} nu={nv.min():.3e}  |<ln n_L> - <ln n>| "
          f"= {abs(mlnL - mln):.4f}   L1 = {np.mean(np.abs(nL - nv)):.2e}")
worst_floor = floor_rows[-1]
vals["s4"] = {"fV_range": [fv_lo, fv_hi], "fV_err": fv_err,
              "bound_g2": bnd_g, "bound_ay2": bnd_ay, "l2_err": l2_err,
              "closed_form_bounds": [bnd_g_cf, bnd_ay_cf],
              "rounding_err_vs_printed_literals": round_err,
              "record_g2": n2_g, "record_ay2": n2_ay,
              "floor": floor_rows,
              "bars": [BAR_S4_FV, BAR_S4_L2, BAR_S4_ROUND, BAR_S4_FLOOR,
                       BAR_S4_NU],
              "note": "Lemma B' (the cap) is DELETED FROM THE PROOF and kept "
                      "only as a recorded a-priori fact (<Gamma> <= 3.449116, "
                      "R-IND-5 record); feasibility ALONE gives the L2 bounds"}
verdicts["s4_feasibility_alone_gives_the_L2_kernel_bounds"] = (
    fv_err < BAR_S4_FV and l2_err < BAR_S4_L2 and round_err < BAR_S4_ROUND
    and n2_g < bnd_g and n2_ay < bnd_ay)
verdicts["s4_MUSTFAIL_the_floor_is_load_bearing"] = (
    worst_floor["nu"] < BAR_S4_NU and worst_floor["err"] > BAR_S4_FLOOR)
print(f"  f_V in [{fv_lo:.6f}, {fv_hi:.6f}], |err| {fv_err:.1e} < "
      f"{BAR_S4_FV:.0e}; feasibility alone gives ||g||_2 <= {bnd_g:.6f} and "
      f"||a_y||_2 <= {bnd_ay:.6f} (against the closed forms {l2_err:.1e} < "
      f"{BAR_S4_L2:.0e}; against the 6-decimal printed literals "
      f"{round_err:.1e} < {BAR_S4_ROUND:.0e})")
print(f"  the record's own norms {n2_g:.6f} / {n2_ay:.6f} sit under them; "
      f"at nu = {worst_floor['nu']:.3e} the <ln n> error is "
      f"{worst_floor['err']:.4f} > {BAR_S4_FLOOR} and does NOT vanish "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ============================================================== s5 LEMMA M
print("s5 LEMMA M -- the exact identity, and the THREE must-fail controls "
      "for F5-F8 (NOT OPTIONAL)", flush=True)
ident, edges, interiors = [], [], []
for Delta in (0, 1, 2):
    for L in (4, 6):
        rec, _ = trunc_record(Delta, L, "dir")
        for n in (64, 128, 256):
            wr = zero_edge(rec, L, n)
            dm, di, de = cell_distortion(rec, L, n)
            ident.append(abs(dm - wr["dist_formula"]))
            edges.append(abs(de - (1.0 + EPS_EDGE)))
            interiors.append(abs(di - wr["Dstat"]))
feas = []
CLn = {}
for L in (4, 6, 10):
    recD, _ = trunc_record(0, L, "dir")
    UL = recD.rate(m=200)
    rows = []
    for n in (64, 128, 256, 512, 1024):
        Dp = (n * D_TGT - 2 * L * (1.0 + EPS_EDGE)) / (n - 2 * L)
        rec, lam = trunc_record(0, L, "dir", Dt=Dp)
        if lam <= 0:
            rows.append(dict(n=n, infeasible=True, shifted_target=Dp,
                             lam=lam))
            continue
        wr = zero_edge(rec, L, n)
        dm, _, _ = cell_distortion(rec, L, n)
        feas.append(abs(dm - D_TGT))
        rows.append(dict(n=n, infeasible=False, shifted_target=Dp,
                         lam=lam, La=wr["La"], C=n * (wr["La"] - UL)))
    CLn[L] = dict(UL=UL, rows=rows)
c6 = [r["C"] for r in CLn[6]["rows"] if not r["infeasible"]]
dec_factor = c6[0] / c6[-1]
shift10 = [r for r in CLn[10]["rows"] if r["n"] == 64][0]
# F7: the CAUSE -- D -> U(L;D) is convex, so mu*eta UNDERSTATES the repair
L7, n7 = 6, 64
UL7 = CLn[6]["UL"]
Dp7 = (n7 * D_TGT - 2 * L7 * (1.0 + EPS_EDGE)) / (n7 - 2 * L7)
eta7 = D_TGT - Dp7
rec7, _ = trunc_record(0, L7, "dir", Dt=Dp7)
secant = (rec7.rate(m=200) - UL7) / eta7
Ds = np.linspace(0.20, 0.30, 11)
Us = np.array([trunc_record(0, L7, "dir", Dt=float(v))[0].rate(m=200)
               for v in Ds])
sec2 = Us[:-2] - 2 * Us[1:-1] + Us[2:]
vals["s5"] = {"identity_max_err": max(ident), "edge_max_err": max(edges),
              "interior_max_err": max(interiors), "rows": len(ident),
              "feasible_max_err": max(feas), "C": CLn,
              "C6": c6, "decrease_factor": dec_factor,
              "C6_at_64": c6[0], "withdrawn_18_7": REC_187,
              "shifted_target_L10_n64": shift10["shifted_target"],
              "lambda_L10_n64": shift10["lam"],
              "mu": MU, "secant_slope": secant, "eta": eta7,
              "secant_over_tangent": secant / MU,
              "min_second_difference": float(sec2.min()),
              "bars": [BAR_S5_IDENT, BAR_S5_EDGE, BAR_S5_FEAS,
                       BAR_S5_DECREASE, BAR_S5_SHIFT, BAR_S5_SLOPE],
              "note": "LEMMA M DOES NOT DISCHARGE W1 OR W4 -- W1 AND W2 "
                      "STAND.  Only C(L,n) = o(n) is used downstream, so the "
                      "conclusion is untouched"}
verdicts["s5_window_distortion_identity_is_EXACT"] = (
    max(ident) < BAR_S5_IDENT and max(edges) < BAR_S5_EDGE
    and max(interiors) < BAR_S5_IDENT)
verdicts["s5_D_feasible_with_no_rescale"] = max(feas) < BAR_S5_FEAS
verdicts["s5_MUSTFAIL_C6n_DECREASES_so_n_independence_is_FALSE"] = (
    dec_factor > BAR_S5_DECREASE
    and all(c6[i] > c6[i + 1] for i in range(len(c6) - 1)))
verdicts["s5_MUSTFAIL_the_18_7_figure_is_EXCEEDED_at_n64"] = c6[0] > REC_187
verdicts["s5_MUSTFAIL_shifted_target_at_L10_n64_is_NEGATIVE"] = (
    shift10["shifted_target"] < BAR_S5_SHIFT and shift10["lam"] < 0.0)
verdicts["s5_F7_convexity_makes_mu_eta_a_LOWER_bound"] = (
    float(sec2.min()) > 0.0 and secant / MU > BAR_S5_SLOPE)
print(f"  distortion identity rebuilt from primitives over {len(ident)} rows:"
      f" max |built - formula| {max(ident):.2e} < {BAR_S5_IDENT:.0e}; edge "
      f"cell - (1+eps) {max(edges):.2e}; interior cell - D_stat "
      f"{max(interiors):.2e}")
print(f"  D-feasible with NO rescale: max |dist - D| {max(feas):.2e} < "
      f"{BAR_S5_FEAS:.0e}")
print("  MUST-FAIL F5: C(6,n) = "
      + " / ".join(f"{v:.3f}" for v in c6)
      + f" -- decrease factor {dec_factor:.3f} > {BAR_S5_DECREASE}: "
        f"n-INDEPENDENCE IS FALSE")
print(f"  MUST-FAIL F6: C(6,64) = {c6[0]:.3f} EXCEEDS the withdrawn "
      f"{REC_187}")
print(f"  MUST-FAIL F8: at L=10, n=64 the shifted target is "
      f"{shift10['shifted_target']:+.5f} < {BAR_S5_SHIFT:.0e} "
      f"(lambda {shift10['lam']:+.3f}) -- the SAME threshold W2 recorded")
print(f"  F7 cause: secant slope over eta={eta7:.4f} is {secant:.4f} against "
      f"the tangent mu={MU:.7f}, ratio {secant/MU:.3f} > {BAR_S5_SLOPE}; "
      f"D-ladder second differences min {sec2.min():+.3e} > 0 "
      f"[{time.time()-t0:.0f}s]", flush=True)

# =================================================== s6 THREE-LEG (LEMMA M)
print("s6 THE EXACT THREE-LEG DECOMPOSITION (F9)", flush=True)
legs_rows = []
for L in (4, 6, 10):
    UL = CLn[L]["UL"]
    for n in (64, 128, 256, 512, 1024):
        Dp = (n * D_TGT - 2 * L * (1.0 + EPS_EDGE)) / (n - 2 * L)
        eta = D_TGT - Dp
        rec, lam = trunc_record(0, L, "dir", Dt=Dp)
        if lam <= 0:
            continue
        wr = zero_edge(rec, L, n)
        Cln = n * (wr["La"] - UL)
        rx = rec.rate(m=200)
        sstat = rec.sigma(m=200)
        dsum = float(np.sum(np.log(wr["sig"][L:n - L] / sstat)))
        m0 = n - 2 * L
        szeg = float(np.linalg.slogdet(wr["T"])[1]) - m0 * rec.mean_log_n()
        tot = -2 * L * rx + (dsum - szeg) / (2 * LN2) + n * (rx - UL)
        legs_rows.append(dict(L=L, n=n, eta=eta,
                              eta_err=abs(eta - 2 * L * (1 + EPS_EDGE - D_TGT)
                                          / (n - 2 * L)),
                              C=Cln, resid=tot - Cln))
resid = max(abs(r["resid"]) for r in legs_rows)
eta_err = max(r["eta_err"] for r in legs_rows)
vals["s6"] = {"rows": legs_rows, "max_residual": resid,
              "max_eta_error": eta_err,
              "bars": [BAR_S6_RESID, BAR_S6_ETA],
              "note": "C(L,n) = -2L*rate(x_n) + [sum delta_t - Szego]/(2 ln 2)"
                      " + n[U(L;D-eta_n) - U(L;D)], eta_n = "
                      "2L(1+eps-D)/(n-2L) EXACTLY (not /n)"}
verdicts["s6_three_leg_decomposition_residual_at_every_row"] = (
    resid < BAR_S6_RESID and len(legs_rows) >= 14)
verdicts["s6_eta_n_is_2L_times_1_plus_eps_minus_D_over_n_minus_2L"] = (
    eta_err < BAR_S6_ETA)
print(f"  {len(legs_rows)} rows, max |residual| {resid:.2e} < "
      f"{BAR_S6_RESID:.0e}; max |eta_n - 2L(1+eps-D)/(n-2L)| {eta_err:.1e} < "
      f"{BAR_S6_ETA:.0e} [{time.time()-t0:.0f}s]", flush=True)

# ================================================= s7 DOES IT PROVE TOO MUCH
print("s7 DOES IT PROVE TOO MUCH?  NO -- the U_tr ladder, the Delta-ladder, "
      "and the DIRECT minimisation (F11)", flush=True)
lad_margin = {}
for Delta in (0, 1, 2):
    mm = []
    for L in range(1, 11):
        r, _ = trunc_record(Delta, L, "dir")
        mm.append(r.rate(m=200) - REC_PSI_LB[Delta])
    lad_margin[Delta] = dict(margins=mm, min=min(mm))
worst_ladder = min(lad_margin[d]["min"] for d in (0, 1, 2))
dl_rows = []
for L in (4, 6, 10):
    r2, _ = trunc_record(2, L, "dir")
    vv = [Rec(r2.g, r2.gof, r2.by, r2.byof, r2.cz, Dl).rate(m=200)
          for Dl in range(15)]
    dl_rows.append(dict(L=L, monotone=bool(all(vv[i + 1] <= vv[i] + 1e-14
                                               for i in range(14))),
                        margin=vv[-1] - BLOCK_INF))
dl_min = min(r["margin"] for r in dl_rows)
dl_mono = all(r["monotone"] for r in dl_rows)


def laur_from_q(q):
    return np.array([float(np.dot(q[:len(q) - m], q[m:]))
                     for m in range(len(q))])


SEEN = {}


def obj(p, L, Delta, m=45):
    """the rate of the depth-L FIR record encoded by p, repaired to exactly
    D.  EVERY finite evaluation is a genuine feasible record, and every one
    is recorded in SEEN -- the gate is on that SET, not on where the search
    stops."""
    nn = 2 * L + 1
    g, by, q = p[:nn], p[nn:2 * nn], p[2 * nn:]
    cz = laur_from_q(q)
    if cz[0] <= 1e-9:
        return 10.0
    r0 = Rec(g, -L, by, -L, np.zeros(len(cz)), Delta)
    d0 = r0.dist()
    if d0 >= D_TGT:
        return 10.0 + d0
    try:
        v = Rec(g, -L, by, -L, (D_TGT - d0) / cz[0] * cz, Delta).rate(m=m)
    except Exception:
        return 10.0
    if np.isfinite(v):
        SEEN[(L, Delta)] = min(SEEN.get((L, Delta), 1e9), v)
    return v


rng7 = np.random.default_rng(11)            # internally pinned
direct = []
for Delta in (0, 1, 2):
    for L in (1, 2, 3):
        g, ay, cz = kern(Delta)
        win = window(L, "dir")
        gL = (g * win)[LMAX - L:LMAX + L + 1]
        ayL = (ay * win)[LMAX - L:LMAX + L + 1]
        czL = (cz * win[LMAX:])[:L + 1]
        q0, _, _, _ = cepstral(czL)
        p0 = np.concatenate([gL, ayL, np.real(q0)])
        utr = obj(p0, L, Delta)
        best, bp = utr, p0
        for t in range(2):
            pp = bp if t == 0 else bp + 0.02 * rng7.normal(size=len(bp))
            r = minimize(obj, pp, args=(L, Delta), method="Nelder-Mead",
                         options=dict(maxfev=900, xatol=1e-10, fatol=1e-12))
            if r.fun < best:
                best, bp = r.fun, r.x
        direct.append(dict(Delta=Delta, L=L, U_tr=utr, direct=best,
                           seen_min=SEEN[(L, Delta)],
                           margin=SEEN[(L, Delta)] - REC_PSI_LB[Delta],
                           utr_gap=utr - SEEN[(L, Delta)]))
d_min = min(r["margin"] for r in direct)
utr_gap = min(r["utr_gap"] for r in direct)
vals["s7"] = {"U_tr_ladder": lad_margin, "worst_ladder_margin": worst_ladder,
              "Delta_ladder": dl_rows, "Delta_ladder_min_margin": dl_min,
              "direct": direct, "direct_min_margin": d_min,
              "min_U_tr_minus_direct": utr_gap,
              "recorded_full_strength_L3": REC_DIRECT_L3,
              "bars": [BAR_S7_LADDER, BAR_S7_BLOCK, BAR_S7_DIRECT,
                       BAR_S7_UTR],
              "note": "F11 -- the tabulated ladder is U_tr(L), the "
                      "TRUNCATION-AND-REPAIR value, NOT the depth-L optimum.  "
                      "The direct gate is on the SET of feasible records the "
                      "pinned fixed-budget search evaluates, never on a "
                      "stopping point"}
verdicts["s7_every_U_tr_rung_above_the_082_certified_lower_endpoints"] = (
    worst_ladder > BAR_S7_LADDER)
verdicts["s7_Delta_ladder_stays_above_block_inf"] = (
    dl_mono and dl_min > BAR_S7_BLOCK)
verdicts["s7_every_directly_minimised_record_above_Psi_LB"] = (
    d_min > BAR_S7_DIRECT and len(direct) == 9)
verdicts["s7_F11_U_tr_is_strictly_above_the_depth_L_optimum"] = (
    utr_gap > BAR_S7_UTR)
print(f"  U_tr ladder (10 rungs x 3 Delta): min margins "
      + " / ".join(f"{lad_margin[d]['min']:+.4e}" for d in (0, 1, 2))
      + f", worst {worst_ladder:+.4e} > {BAR_S7_LADDER:.0e}")
print(f"  Delta-ladder monotone {dl_mono} at three L, min margin over "
      f"block_inf {dl_min:+.3e} > {BAR_S7_BLOCK:.0e}")
for r in direct:
    print(f"  direct Delta={r['Delta']} L={r['L']}: U_tr {r['U_tr']:.12f} > "
          f"direct {r['direct']:.12f}, margin over Psi^LB "
          f"{r['margin']:+.4e}")
print(f"  {len(direct)}/9 above Psi^LB, min margin {d_min:+.4e} > "
      f"{BAR_S7_DIRECT:.0e}; min U_tr - direct {utr_gap:+.4e} > "
      f"{BAR_S7_UTR:.0e} [{time.time()-t0:.0f}s]", flush=True)

# ============================================================== s8 MODULUS
print("s8 THE THEOREM-D MODULUS -- valid at every rung, though loose",
      flush=True)
xref, _ = trunc_record(0, LMAX, "dir")
sref = xref.sigma(m=260)
rref = xref.rate(m=260)
PRr, PRSr, nzr = spec(xref)
nu_ref = float(nzr.min())
K8 = 20
cb8 = opt_filter(xref, np.arange(1, K8 + 1), np.arange(1, K8 + 1))
v8 = np.concatenate([[1.0], -cb8[:K8]])
vs8 = np.concatenate([[0.0], -cb8[K8:]])
Cv8 = float(np.max(np.abs(symb(v8, 0)) ** 2 + np.abs(symb(vs8, 0)) ** 2))
epsK = qform(xref, v8, vs8) - sref
mod_rows = []
for L in range(1, 15):
    for kind in ("dir", "fej"):
        xl, _ = trunc_record(0, L, kind)
        PR1, PRS1, n1 = spec(xl)
        l1P = float(np.mean(np.abs(PR1 - PRr) + np.abs(PRS1 - PRSr)))
        l1n = float(np.mean(np.abs(n1 - nzr)))
        gap = xl.rate(m=200) - rref
        bound = ALPHA * ((epsK + Cv8 * l1P) / sref + l1n / nu_ref)
        mod_rows.append(dict(L=L, kind=kind, gap=gap, bound=bound,
                             slack=bound - gap,
                             ratio=gap / bound if bound > 0 else 0.0))
viol = sum(1 for r in mod_rows if r["slack"] < 0.0)
min_slack = min(r["slack"] for r in mod_rows)
vals["s8"] = {"rungs": len(mod_rows), "violations": viol,
              "min_slack": min_slack,
              "ratio_range": [min(r["ratio"] for r in mod_rows),
                              max(r["ratio"] for r in mod_rows)],
              "nu_reference": nu_ref, "C_V": Cv8, "eps_K": epsK,
              "bar": BAR_S8_SLACK,
              "note": "the modulus is FIRST ORDER in the kernel error while "
                      "the truth is SECOND ORDER (W7's squaring law), so it "
                      "is VALID everywhere and LOOSE everywhere; density "
                      "needs only -> 0"}
verdicts["s8_modulus_valid_at_every_rung"] = (
    viol == 0 and len(mod_rows) == 28 and min_slack > BAR_S8_SLACK)
print(f"  {len(mod_rows)} rungs, {viol} violations, min (bound - gap) "
      f"{min_slack:.3e} > {BAR_S8_SLACK:.0e}; the modulus is LOOSE -- "
      f"gap/bound runs {vals['s8']['ratio_range'][1]:.2e} down to "
      f"{vals['s8']['ratio_range'][0]:.2e} [{time.time()-t0:.0f}s]",
      flush=True)

# ------------------------------------------------------------------ report
vals["scope"] = {
    "lemma_A_prime": "A HILBERT-SPACE FACT: sigma = dist^2(R_u, M) with M the "
                     "CLOSED span, so finite combinations are dense BY "
                     "DEFINITION and the infima agree.  Hypotheses: Phi_R, "
                     "f_S in L1 and NOTHING ELSE.  The infimum is NOT "
                     "ATTAINED by any finite filter; only eps-optimality is "
                     "used.  Its admissibility (V monic causal in R, V_S "
                     "strictly causal in S) is the MIRROR of def:adm's and "
                     "attaches to a DIFFERENT pivot -- never conflated (F2)",
    "theorem_D": "hypotheses PRINTED: (a) f_V in [0.1111, 9.0000]; (b) "
                 "continuity of D -> Psi(D) at D = 0.3 from convexity; (c) "
                 "Lemma C' the floor, LOAD-BEARING; (d) Lemma B' the cap "
                 "DELETED FROM THE PROOF -- DISPENSABLE, kept only as a "
                 "recorded a-priori fact",
    "lemma_M": "the exact three-leg decomposition with eta_n = "
               "2L(1+eps-D)/(n-2L) EXACTLY.  WITHDRAWN: 'every constant "
               "n-independent', '~18.7 at L=6' as an upper bound, and 'no "
               "feasibility threshold'.  LEMMA M DOES NOT DISCHARGE W1 OR W4 "
               "-- W1 AND W2 STAND.  Only C(L,n) = o(n) is used downstream, "
               "so the conclusion is untouched",
    "psi_class": "Psi(D;Delta) = inf of the stationary rate over FEASIBLE "
                 "STATIONARY RECORDS OF F0 with n(w) > 0 a.e., Phi_R in L1, "
                 "per-symbol distortion <= D -- the SAME class in "
                 "cor:onedir, thm:cert and Theorem D (F10)",
    "ladder": "U_tr(L), the TRUNCATION-AND-REPAIR value, NOT the depth-L "
              "optimum (F11)",
    "lemma_W_steps": "steps (1)-(4), with (3) carrying the classical "
                     "citation, and (5) superseded by Lemma M.  Step (3) IS "
                     "load-bearing.  'Floored at n >= 0.1288' is "
                     "UNREPRODUCED: the floors are 0.1495/0.1378/0.1404 and "
                     "the ladder minimum is 0.1331 (F13)",
    "the_equality": "L^inf(Delta) = Psi(D;Delta) at Delta = 0,1,2 is a "
                    "SCOPED THEOREM of the tex, carrying five named scope "
                    "items beyond cor:onedir's.  'UNCONDITIONAL' DOES NOT "
                    "ATTACH TO IT.  Psi remains a two-sided CERTIFIED "
                    "BRACKET; the equality IDENTIFIES TWO OBJECTS and is NOT "
                    "a licence to quote a value as exact; cor:brackets "
                    "CONTINUES TO GOVERN the quotable numeric statement.  NO "
                    "GATE HERE READS OR ASSERTS IT",
    "optimizers": "the only search is s7's direct minimisation, gated on the "
                  "SET of feasible records a pinned fixed-budget search "
                  "evaluates -- never on a stopping point.  No fixed point "
                  "is solved anywhere",
    "widths": "no bracket, width or certificate endpoint is gated; the 082 "
              "lower endpoints enter only as fixed comparison literals on "
              "the safe side",
    "owed": "novelty sweeps on Lemma A''s packaging and on Lemma W's "
            "combination, and the window-side la_cmi cross-check.  NO "
            "NOVELTY LANGUAGE is used for A', W or Theorem D anywhere"}
verdicts = {k: bool(v) for k, v in verdicts.items()}
allpass = all(verdicts.values())
print()
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print(f"VERDICT: {'ALL PASS' if allpass else 'FAIL'} "
      f"{sum(verdicts.values())}/{len(verdicts)}")

out = {"verdict": verdicts, "GO14FD_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14FD-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
