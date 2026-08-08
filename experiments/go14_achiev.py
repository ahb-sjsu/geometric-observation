#!/usr/bin/env python
"""GO-14 ACHIEVABILITY harness (tex v0.9, Section "Achievability: Lemma W, the
FIR-density residual, and the unconditional brackets").  Registration 084
pending -- NOTHING HERE IS SEALED.

Model: V AR(1) a = 0.8 unit variance; Y = 0.7 V + N, Var(Y) = 1; S = V + U,
tau2 = 0.4; D = 0.3; T = (V, Y) = W; family F0 (records jointly Gaussian with
(V, Y) and INDEPENDENT of U, i.e. A_u = 0).  se(t) = min(t + Delta, n).

WHAT THIS HARNESS IS FOR.  084 is the first registration on the ACHIEVABILITY
side.  082 certified the value Psi two-sided; 083 discharged the convexity step
of the LOWER-bound chain; 084 nets an explicit family of D-FEASIBLE F0 records
and the window transfer (LEMMA W) that turns them into statements about
L^inf.  It nets NO equality between L^inf and Psi -- no such statement exists
in the tex and none may be printed -- and no margin against any sealed
causal-spectral bar.

LEMMA W, AS STATED IN v0.9 (with the R-IND-5 restatements W1-W4 built into the
statement, NOT appended as afterthoughts):

  For a depth-L FIR stationary record x of F0 with a spectral floor, and for
  every n >= n0(L) (FEASIBILITY THRESHOLD -- W2, an explicit hypothesis), the
  repaired window record x^(n) is a D-feasible F0 record on the window and

      phi_n(Delta) <= L_a(x^(n)) <= rate(x) + C(L, n)/n,

  where C(L, n) is MONOTONE DECREASING in n with sup_{n >= n0(L)} C(L, n) <
  infinity, and only C(L, n) = o(n) is ever used.  NO CLAIM THAT C DOES NOT
  DEPEND ON n IS MADE ANYWHERE (W1: the object that does not move with n is the
  EDGE CHARGE sum delta_t, not the constant).  W3: the THREE builds are kept
  apart -- ZERO-EDGE (what steps (1)-(2) prove), TRUNCATED-TAPS (what every
  quoted constant and every bracket endpoint comes from) and REPAIRED (what
  feasibility requires); steps (1)-(2) do NOT apply to the truncated-taps
  build.  W4: the RATE COST of the repair is a SEPARATE estimate, not covered
  by steps (1)-(5); step (5) discharges FEASIBILITY only.

DESIGN RULE (the 079 lesson, restated by 080/081/082/083).  NO GATE MAY RACE AN
OPTIMIZER STOPPING POINT AND NO GATE MAY GATE A CERTIFICATE WIDTH.  This file
CONTAINS NO OPTIMIZER, NO FIXED POINT AND NO ROOT FIND.  The stationary K1-K3
kernels are PINNED DATA (provenance: the grid fixed point at Nf = 4096,
P = 180, the same reference W8 names) -- and the provenance of a record is
irrelevant to whether it is a valid feasible upper-bound certificate: what
makes an upper bound valid is F0 membership, exact D-feasibility and correct
evaluation, all three of which are GATED here.  The only linear algebra is
Cholesky / slogdet / a pinned-size normal-equation solve; every gate is
  (a) an exact identity with a tolerance orders above f64 noise,
  (b) a structural / set fact (sign, count, monotonicity),
  (c) an analytic inequality with a measured margin, or
  (d) a MUST-FAIL control, gated on the side of failure.
NO BRACKET WIDTH IS GATED.  The three bracket widths are REPORTED (and their
positivity is reported, never gated), and the recorded endpoints are used only
for reproduction gates on the RECORD VALUE V(10, 2048), never on a width.

SECTIONS.

s1 THE ORIENTATION GATE -- MANDATORY, AND FIRST.  The prover's first window
   build had a LAG-ORIENTATION DEFECT in a_v (the class of the R27 np.roll
   defect) that produced a spurious constant sigma_t offset MASQUERADING AS A
   NON-VANISHING EDGE CHARGE.  Gates: (a) two independent evaluators (raw CMI
   definition vs the Collapse/Cholesky route) agree; (b) the canonical build's
   deep-interior sigma_t reproduces the stationary pivot; (c) MUST-FAIL --
   the reversed-a_v build sits >= 1e-2 above the stationary pivot AT EVERY
   INTERIOR CELL, and converts the n-independent edge charge into an O(n) one;
   (d) W5 NEGATIVE CONTROL -- the per-cell DISTORTION has ZERO power against
   this defect (it is invariant under kernel reversal, exactly: reversal
   conjugates the symbol on |z| = 1); (e) a_y is real zero-phase by (K1), so
   its kernel is symmetric and carries NO orientation -- reversing a_y alone
   leaves the rate unchanged.  ANY SUCCESSOR BUILDING WINDOW RECORDS FROM
   SPECTRAL KERNELS MUST RUN THIS GATE.

s2 STEP (1) -- EDGE CELLS CONTRIBUTE EXACTLY ZERO.  For the ZERO-EDGE build the
   2L edge cells have sigma_t = eps exactly, numerator == denominator, per-cell
   CMI exactly 0; and Nc is BLOCK DIAGONAL, so the 2L ln eps they put into
   lndet Nc cancels identically.

s3 STEP (2) -- THE SUBSET CONDITIONING ARGUMENT.  The window conditioning set at
   an interior cell is a genuine SUBSET of the stationary one, so delta_t =
   ln(sigma_t/sigma_stat) >= 0.  This is the MIRROR of step (A) of the bypass,
   RUN THE OTHER WAY.  Swept over Delta in {0,1,2,3,5,9,20} INCLUDING past
   saturation (Delta >= n, where the coordinate becomes the block program):
   zero negative cells.

s4 STEP (3) -- THE EDGE CHARGE IS EXACTLY n-INDEPENDENT.  sum_t delta_t is
   identical to nine decimals over n in {128,256,512} at L in {4,10} and
   Delta in {0,1,2}, and the L = 10 triple reproduces the recorded
   0.043994832 / 0.051454447 / 0.052333440.  (The analytic input is the
   standard rational-spectral-factorization/Riccati fact, applied to the FIR
   RECORD, whose spectrum is rational by construction -- so it does not assume
   the density it is meant to isolate.  Non-circularity is a wording fact, not
   a gate.)

s5 STEP (4) -- THE SZEGO NOISE LEG HELPS.  lndet T_m - m <ln n(w)> >= 0, flat
   in m, plus the min-phase identity <ln n(w)> = 2 ln q0.

s6 STEP (5) -- THE REPAIR, AND THE FEASIBILITY THRESHOLD.  The window
   distortion is EXACTLY AFFINE in the scalar noise rescale and lands at
   dist = D in closed form.  W2 MUST-FAIL CONTROL: the ZERO-EDGE build at
   n = 64, L = 10 is INFEASIBLE (the repairing rescale c <= 0), while at
   n = 128 it is feasible -- so n0(L) is real and L-dependent.

s7 W1 -- C(L, n) IS MONOTONE DECREASING IN n.  THIS SECTION GATES MONOTONICITY
   AND NEVER n-INDEPENDENCE.  Pinned (mode, Delta, L, n) grid; the zero-edge
   L = 6, Delta = 0 row is the recorded refutation witness (71.76 -> 12.65, a
   factor 5.7 over n = 64..1024) and its decrease is gated as a fact with
   power.

s8 THE UNCONDITIONAL BRACKETS -- the headline.  Reproduce V(10, 2048) at three
   Delta; gate EXACT feasibility; gate the 8/8 anchor cross-check (every
   V(10, n) strictly ABOVE the sealed/certified phi_n upper end at
   n = 16/24/32, as a suboptimal D-feasible record must be); check the recorded
   upper ends are OUTWARD-rounded on the safe side; and W11 -- the safe side is
   NON-INCREASING IN P BY CONSTRUCTION and FLAT to 3.3e-16 over P = 20..400 and
   Nf = 1024..8192 (never "monotone decreasing", which tests f64 ties).

s9 DOES IT PROVE TOO MUCH?  NO.  The block program (se == n) and the
   Delta-ladder of a fixed record both stay strictly ABOVE the independently
   known block_inf = 0.5299499808119 and approach from above without crossing.

Sentinel ===GO14AC-JSON=== with ===END===; flag GO14AC_supported.
Pilot seed 20261170 / governed seed 20261171.  SEED STAMPS ONLY: the seed is
recorded in the output and feeds NO computation -- the one random draw (the s1
evaluator calibration) uses an internally pinned generator, so pilot and
governed produce a bit-identical payload.

Evaluator lineage.  Every conditional variance is read off a joint covariance
built by pushing the INDEPENDENT PRIMITIVES (V, N, U, Z) through an explicit
linear map.  Two routes are carried: la_cmi (the raw CMI definition, O(n^4),
small n only) and la_fast (ONE Cholesky of the interleaved (S, Yhat)
covariance plus lndet Nc, via Collapse).  la_fast's use of the Collapse
denominator identity is CHECKED against la_cmi in s1 and again on the
certificate records themselves in s8 -- it is never assumed.

PILOT RECORD (seed 20261170, 2026-08-07).
 Every bar was fixed BEFORE the pilot from the R-IND-5 verifier's committed
 artifacts (scratchpad r5W/: g0_orient, g1_out.json, g2_out.json, g3_out.json,
 g4_out.json, g6_extra) and from a pre-pilot calibration run of the pinned
 kernels.  NO BAR WAS EVER MOVED AGAINST A MEASUREMENT, in either direction.
 iter 1 -- ALL PASS 31/31, 47.2 s.  No gate failed and no bar was touched:
   every bar had been fixed before the run from the artifacts above, and the
   pilot exercised them as written.  A governed re-run (seed 20261171, 53.6 s)
   reproduced the JSON payload BIT-IDENTICALLY apart from the seed stamp and
   the pilot flag, confirming the seed-stamp-only discipline.  There was no
   iteration 2: nothing needed changing, and changing a bar after a passing
   measurement is exactly what the discipline forbids.
 MEASURED vs BAR (the ratio is the margin):
   s1 CMI route vs Collapse route 1.55e-15 / 1e-11 (6.5e3x) over 6 records;
      canonical deep-interior sigma offset 4.44e-16 / 1e-12 (2252x) over 480
      cells; MUST-FAIL reversed-a_v control: min over ALL interior cells
      +1.256e-2 / 1e-2 (1.26x -- a CLAIM REPRODUCTION, see DISCLOSURES (c))
      with the fat-margin form of the SAME control at 16.497 / 10.0 (1.65x)
      and slope +3.2891e-2 / 1e-2 (3.29x) per cell against a canonical slope
      of -1.18e-16 / 1e-12 (8.5e3x); W5 NEGATIVE CONTROL: per-cell distortion
      identical under reversal 2.22e-16 / 1e-15 (4.5x); reversing a_y alone
      moves the rate by 0.00e+00 and a_y's symmetry defect is 1.39e-17 / 1e-15
      (72x)
   s2 per-cell CMI on the 2L edge cells 0.00e+00 / 1e-15 (EXACTLY zero);
      |sigma_t - eps| 0.00e+00 / 1e-15; block-diagonality lndet residual
      1.71e-13 / 1e-9 (5848x); routes agree 1.8e-15
   s3 min delta_t -7.77e-16 / -1e-13 (129x) and 0 negative cells over
      Delta in {0,1,2,3,5,9,20} at n = 48 (so the last two are past
      saturation)
   s4 spread over n in {128,256,512} 1.93e-13 / 1e-9 (5181x) over 6 (L, Delta)
      rows; the recorded L=10 triple 0.043994832 / 0.051454447 / 0.052333440
      reproduced to 3.31e-10 / 1e-8 (30x)
   s5 leg +8.6219e-3 / +1.0793e-2 / +1.0756e-2 at L=10, min over the grid
      8.622e-3 / 1e-3 (8.6x); flatness over m in {16..512} 1.07e-11 / 1e-9
      (93x); min-phase <ln n(w)> = 2 ln q0 to 0.00e+00 / 1e-12
   s6 affine residual 1.67e-16 / 1e-15 (6.0x); |dist - D| 1.67e-16 / 1e-15
      (6.0x); W2 MUST-FAIL: zero-edge rescale at (n=64, L=10) =
      -0.832 / -0.922 / -0.948, worst -0.832 / -0.10 (8.3x); the same build at
      n = 128 has c >= +0.206 / 0.05 (4.1x)
   s7 18/18 pinned (mode, Delta, L) rows strictly decreasing in n with the row
      maximum at the first FEASIBLE n; the W1 refutation witness (ZERO-EDGE,
      L=6, Delta=0) falls 71.76 -> 20.38 -> 15.16 -> 13.39 -> 12.65 over
      n = 64..1024, factor 5.67 / 4.0 (1.42x).  NO GATE IN THIS SECTION
      ASSERTS n-INDEPENDENCE OF C
   s8 V(10,2048) = 0.562765641106 / 0.536445811112 / 0.531099487172,
      reproducing the recorded values to 0.00e+00 / 1e-9 (bit-exact -- see
      DISCLOSURES (g)); exact feasibility 1.67e-16 / 1e-15 (6.0x); anchor
      cross-check 8/8 with min margin +4.97e-4 / 1e-4 (5.0x); recorded upper
      ends outward-rounded on the safe side 3/3; la_cmi vs la_fast ON THE
      CERTIFICATE RECORDS 1.11e-15 / 1e-11 (9.0e3x); W11 safe side flat
      4.4e-16 / 1e-14 (22x) over 16 (Nf, P) pairs per Delta, and the direction
      has power, P=1 minus P=8 = 2.40e-2 / 1e-2 (2.4x)
   s9 block-schedule records 0.539958900 -> 0.538561102 over n = 64..1024,
      monotone decreasing 5/5, min excess over block_inf +8.611e-3 / 1e-4
      (86x); the Delta-ladder at n = 256 is monotone 10/10 with min excess
      +8.890e-3 / 1e-4 (89x); the recorded 082 Psi ladder is monotone with min
      excess +1.19e-9 (bookkeeping on pinned literals -- see DISCLOSURES (d))
 DISCLOSURES.
 (a) NO OPTIMIZER, no fixed point and no root find appears anywhere in this
   file, so no gate can race a stopping point.  The stationary kernels are
   PINNED DATA; nothing in this file re-derives them, and nothing needs to.
 (b) NO BRACKET WIDTH IS GATED.  The widths (3.914e-5 / 4.443e-5 / 4.947e-5)
   are reported, and their positivity is reported, never gated.
 (c) ONE gate is a CLAIM REPRODUCTION rather than a fat-margin measurement and
   is labelled as such: s1's "reversed control >= 1e-2 at every interior cell"
   (1.26x).  The recorded constant +1.256e-2 is a deterministic property of a
   pinned kernel, not an estimate, and the SAME control is gated a second time
   in a form with a fat margin (the O(n) growth of the edge charge).  The
   control is loudest at Delta = 0; at Delta = 1, 2 the same defect shows
   +1.96e-3 / +2.98e-4, which is why the 1e-2 form is gated at Delta = 0 only
   and the other two are REPORTED.
 (d) s9's "block-schedule window records converge like ~0.105/n" is an R-IND-5
   RECORDED datum about BLOCK-OPTIMAL window records; the records this harness
   builds are not block-optimal, so their excess over block_inf tends to a
   positive constant (+8.6e-3).  What is gated here is the DIRECTION (never
   below block_inf) and the monotonicity, which is what "does not prove too
   much" asserts.  Likewise the recorded "+1.70e-12 at Delta = 12" on the
   certified Psi ladder is carried as a literal and NOT re-derived; the
   min excess this file reports for the recorded ladder, +1.19e-9, is a
   property of the NINE-DECIMAL ROUNDING at which that ladder is printed in
   the tex, not a re-measurement -- it is a bookkeeping check on literals and
   is labelled as one.
 (e) This harness nets NO novelty claim: THE NOVELTY SWEEP ON LEMMA W'S
   COMBINATION (Collapse + subset-conditioning monotonicity + Toeplitz
   innovation monotonicity, assembled as a SIGNED two-leg boundary argument) IS
   OWED, and no novelty language for it appears in the tex or here.
 (e2) NO GATE ANYWHERE reads or asserts an equality between L^inf and Psi, and
   none may be added: the two inequalities of the tex's bracket come from
   structurally INDEPENDENT arguments and together give a BRACKET, never an
   equality.
 (f) The residual R of the tex's Remark on the density is NOT gated here: it is
   a RESIDUAL, its reference is the grid fixed point (W8), and the L >= 11
   entries of the U(L) list are f64 noise going negative -- they are neither
   gated nor cited.
 (g) s8's reproduction of V(10, 2048) is BIT-EXACT (0.00e+00), because this
   file evaluates the SAME pinned kernels by the same construction as the
   R-IND-5 verifier did.  That gate is therefore a REGRESSION gate, not an
   independent confirmation, and is labelled as one.  The independent content
   of s8 is elsewhere and is gated separately: the raw-CMI route against the
   Collapse route ON THE CERTIFICATE RECORDS THEMSELVES (1.11e-15), the exact
   D-feasibility (1.67e-16), and the 8/8 anchor cross-check against sealed
   values this file did not produce.
"""
import argparse
import json
import sys
import time

import numpy as np

t0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--pilot", action="store_true")
ap.add_argument("--seed", type=int, default=None)
a_ = ap.parse_args()
SEED = a_.seed if a_.seed is not None else (20261170 if a_.pilot
                                            else 20261171)
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

# ------------------------------------------------------------------ model
A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
D_TGT = 0.3
LN2 = np.log(2.0)
NF, PLAG = 4096, 240
LMAX = 26

# ------------------------------------------------------- recorded literals
# R-IND-5 / 082 record.  These are REFERENCE VALUES for reproduction gates
# and for bookkeeping; no bar is set from a measurement made in this file.
REC_EDGE_CHARGE = {0: 0.043994832, 1: 0.051454447, 2: 0.052333440}
REC_V2048 = {0: 0.5627656411063473, 1: 0.5364458111116368,
             2: 0.5310994871716196}
REC_UPPER_ROUNDED = {0: 0.5627656412, 1: 0.5364458112, 2: 0.5310994872}
REC_PSI_LB = {0: 0.5627264963, 1: 0.5364013784, 2: 0.5310500198}
# certified / sealed phi_n UPPER ends (tex Sections "Certified two-sided
# anchors" and "The Delta=2 finite-window cross-check, certified")
REC_ANCHOR = {0: {16: 0.5667581350, 24: 0.5654138570, 32: 0.5647418676},
              1: {16: 0.5408064658, 24: 0.5393377781},
              2: {16: 0.5358939352, 24: 0.5342788038, 32: 0.533471490973}}
BLOCK_INF = 0.5299499808119
# the certified Psi ladder of the tex ("Does it prove too much?"), Delta=0..9
REC_PSI_LADDER = [0.562726496, 0.536401378, 0.531050020, 0.530117530,
                  0.529973408, 0.529953058, 0.529950369, 0.529950029,
                  0.529949987, 0.529949982]

# ------------------------------------------------------------------- bars
BAR_S1_ROUTES = 1e-11
BAR_S1_CANON = 1e-12
BAR_S1_REV_CELL = 1e-2          # claim reproduction (see DISCLOSURES (c))
BAR_S1_REV_SUM = 10.0
BAR_S1_REV_SLOPE = 1e-2
BAR_S1_CANON_SLOPE = 1e-12
BAR_S1_DIST_ZEROPOWER = 1e-15
BAR_S1_AY_SYM = 1e-15
BAR_S2_CMI = 1e-15
BAR_S2_SIGEPS = 1e-15
BAR_S2_BLOCKDIAG = 1e-9
BAR_S3_MINDELTA = -1e-13
BAR_S4_SPREAD = 1e-9
BAR_S4_RECORDED = 1e-8
BAR_S5_LEG_MIN = 1e-3
BAR_S5_FLAT = 1e-9
BAR_S5_MINPHASE = 1e-12
BAR_S6_AFFINE = 1e-15
BAR_S6_DIST = 1e-15
BAR_S6_INFEAS = -0.10
BAR_S6_FEAS = 0.05
BAR_S7_WITNESS_FACTOR = 4.0
BAR_S8_V2048 = 1e-9
BAR_S8_FEAS = 1e-15
BAR_S8_ANCHOR_MARGIN = 1e-4
BAR_S8_ROUTES = 1e-11
BAR_S8_SAFE_FLAT = 1e-14
BAR_S8_SAFE_POWER = 1e-2
BAR_S9_ABOVE = 1e-4


def jsafe(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


# ============================================================== primitives
def cov_V(n):
    k = np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
    return A_ ** k


def sched(n, Delta):
    """se(t), t = 1..n, as PREFIX LENGTHS."""
    return np.minimum(np.arange(1, n + 1) + Delta, n)


def joint4(n, Av, Ay, Nc):
    """Cov of (V^n, Y^n, S^n, Yhat^n) from the INDEPENDENT primitives."""
    SV = cov_V(n)
    I = np.eye(n)
    O = np.zeros((n, n))
    G = Av + RHO * Ay
    M = np.block([[I, O, O, O],
                  [RHO * I, I, O, O],
                  [I, O, I, O],
                  [G, Ay, O, I]])
    CP = np.zeros((4 * n, 4 * n))
    for i, B in enumerate([SV, SN2 * I, TAU2 * I, Nc]):
        CP[i * n:(i + 1) * n, i * n:(i + 1) * n] = B
    return M @ CP @ M.T


def _cvar(C, t, cond):
    if len(cond) == 0:
        return float(C[t, t])
    b = C[np.ix_(cond, [t])].ravel()
    return float(C[t, t] - b @ np.linalg.solve(C[np.ix_(cond, cond)], b))


def la_cmi(n, Av, Ay, Nc, Delta=None, se=None, parts=False):
    """L_a straight from the CMI definition.  O(n^4); small n only."""
    C = joint4(n, Av, Ay, Nc)
    iV = np.arange(0, n)
    iY = np.arange(n, 2 * n)
    iS = np.arange(2 * n, 3 * n)
    iR = np.arange(3 * n, 4 * n)
    if se is None:
        se = sched(n, Delta)
    num = np.zeros(n)
    den = np.zeros(n)
    for t in range(n):
        cS = list(iS[:se[t]])
        cR = list(iR[:t])
        num[t] = _cvar(C, int(iR[t]), cS + cR)
        den[t] = _cvar(C, int(iR[t]), list(iV) + list(iY) + cS + cR)
    val = float(np.sum(np.log(num / den)) / (2 * LN2) / n)
    return (val, num, den) if parts else val


def moments(n, Av, Ay, Nc):
    SV = cov_V(n)
    G = Av + RHO * Ay
    CSS = SV + TAU2 * np.eye(n)
    CSR = SV @ G.T
    CRR = G @ SV @ G.T + SN2 * (Ay @ Ay.T) + Nc
    CRR = 0.5 * (CRR + CRR.T)
    CYR = (RHO * SV) @ G.T + SN2 * Ay.T
    return CSS, CSR, CRR, CYR


def _order(n, se):
    kind = np.empty(2 * n, np.int8)
    idx = np.empty(2 * n, np.int64)
    posR = np.empty(n, np.int64)
    p = j = 0
    for t in range(n):
        while j < se[t]:
            kind[p] = 0
            idx[p] = j
            p += 1
            j += 1
        posR[t] = p
        kind[p] = 1
        idx[p] = t
        p += 1
    while j < n:
        kind[p] = 0
        idx[p] = j
        p += 1
        j += 1
    return kind, idx, posR


def la_fast(n, Av, Ay, Nc, Delta=None, se=None, blocks=None):
    """L_a via ONE Cholesky of the interleaved (S, Yhat) covariance plus
    lndet Nc (Collapse).  The denominator identity is CHECKED against
    la_cmi in s1 and again on the certificate records in s8."""
    if se is None:
        se = sched(n, Delta)
    CSS, CSR, CRR, CYR = moments(n, Av, Ay, Nc) if blocks is None else blocks
    kind, idx, posR = _order(n, se)
    iS = np.where(kind == 0)[0]
    iR = np.where(kind == 1)[0]
    aS = idx[iS]
    aR = idx[iR]
    C = np.empty((2 * n, 2 * n))
    C[np.ix_(iS, iS)] = CSS[np.ix_(aS, aS)]
    C[np.ix_(iR, iR)] = CRR[np.ix_(aR, aR)]
    C[np.ix_(iS, iR)] = CSR[np.ix_(aS, aR)]
    C[np.ix_(iR, iS)] = CSR[np.ix_(aS, aR)].T
    Lc = np.linalg.cholesky(C)
    sig = np.diag(Lc)[posR] ** 2
    _, ldN = np.linalg.slogdet(Nc)
    return float(np.sum(np.log(sig)) - ldN) / (2 * LN2) / n, sig


def dist_of(n, Av, Ay, Nc, blocks=None):
    CSS, CSR, CRR, CYR = moments(n, Av, Ay, Nc) if blocks is None else blocks
    return float(np.mean(1.0 - 2 * np.diag(CYR) + np.diag(CRR)))


def percell_dist(n, Av, Ay, Nc, blocks=None):
    CSS, CSR, CRR, CYR = moments(n, Av, Ay, Nc) if blocks is None else blocks
    return 1.0 - 2 * np.diag(CYR) + np.diag(CRR)


# ------------------------------------------------------- the three builds
def build_window(n, av, ay, q, mode="zero", eps=1e-6):
    """mode='zero'  : the ZERO-EDGE build -- interior [L, n-L) carries the full
                      taps, the 2L edge cells are PURE independent noise of
                      variance eps, Nc BLOCK DIAGONAL.
       mode='trunc' : the TRUNCATED-TAPS build -- every cell keeps whatever
                      taps fall inside the window, MA Toeplitz over the whole
                      window.  Steps (1)-(2) do NOT apply to this build."""
    L = (len(av) - 1) // 2
    Lq = len(q) - 1
    Av = np.zeros((n, n))
    Ay = np.zeros((n, n))
    rows = range(L, n - L) if mode == "zero" else range(n)
    for t in rows:
        for k in range(-L, L + 1):
            s = t - k
            if 0 <= s < n:
                Av[t, s] += av[L + k]
                Ay[t, s] += ay[L + k]
    cz = np.array([float(np.dot(q[:len(q) - m], q[m:])) for m in range(Lq + 1)])
    k = np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
    T = np.where(k <= Lq, cz[np.minimum(k, Lq)], 0.0)
    if mode == "zero":
        Nc = eps * np.eye(n)
        ii = np.arange(L, n - L)
        Nc[np.ix_(ii, ii)] = T[np.ix_(ii, ii)]
    else:
        Nc = T
    return Av, Ay, Nc


def rescale_window(n, av, ay, q, D=D_TGT, mode="trunc", eps=1e-6):
    """the REPAIRED build: scale Nc by the unique c landing at dist == D."""
    Av, Ay, Nc = build_window(n, av, ay, q, mode=mode, eps=eps)
    d1 = dist_of(n, Av, Ay, Nc)
    c = 1.0 - (d1 - D) * n / np.trace(Nc)
    return Av, Ay, c * Nc, float(c), d1


# ------------------------------------------------- stationary FIR evaluator
def symbol2(c, Nf):
    L = (len(c) - 1) // 2
    w = 2 * np.pi * np.arange(Nf) / Nf
    out = np.zeros(Nf, complex)
    for k in range(-L, L + 1):
        out += c[L + k] * np.exp(-1j * w * k)
    return out


def symbol1(q, Nf):
    w = 2 * np.pi * np.arange(Nf) / Nf
    out = np.zeros(Nf, complex)
    for k in range(len(q)):
        out += q[k] * np.exp(-1j * w * k)
    return out


def stat_spectra(Nf, Delta, av, ay, q):
    w = 2 * np.pi * np.arange(Nf) / Nf
    z = np.exp(-1j * w)
    fV = (1 - A_ ** 2) / np.abs(1 - A_ * z) ** 2
    g = symbol2(av, Nf) + RHO * symbol2(ay, Nf)
    AY = symbol2(ay, Nf)
    nw = np.abs(symbol1(q, Nf)) ** 2
    return dict(fS=fV + TAU2, nw=nw,
                Phi_R=np.abs(g) ** 2 * fV + SN2 * np.abs(AY) ** 2 + nw,
                Phi_RS=z ** (Delta + 1) * g * fV,
                dist=float(np.mean(np.abs(g - RHO) ** 2 * fV
                                   + np.abs(AY - 1.0) ** 2 * SN2 + nw)))


def rate_stat(Nf, P, Delta, av, ay, q):
    """sigma = Var(R_u | R^{u-1}, S^{u-1}) by a P-lag normal-equation solve.
    A finite P OVERSTATES sigma (fewer regressors) and therefore the rate --
    THE CONSERVATIVE DIRECTION FOR AN UPPER BOUND (W11)."""
    sp = stat_spectra(Nf, Delta, av, ay, q)
    cRR = np.real(np.fft.ifft(sp["Phi_R"]))
    cRS = np.real(np.fft.ifft(sp["Phi_RS"]))
    cSS = np.real(np.fft.ifft(sp["fS"]))
    i = np.arange(1, P + 1)
    J, I = np.meshgrid(i, i)
    K_ = np.block([[cRR[np.abs(J - I)], cRS[(J - I) % Nf]],
                   [cRS[(J - I) % Nf].T, cSS[np.abs(J - I)]]])
    rhs = np.concatenate([cRR[i], cRS[i % Nf]])
    sigma = float(cRR[0] - rhs @ np.linalg.solve(K_, rhs))
    lnn = float(np.mean(np.log(sp["nw"])))
    return dict(rate=float((np.log(sigma) - lnn) / (2 * LN2)),
                dist=sp["dist"], sigma=sigma, nw=sp["nw"], lnn=lnn)


def rescale_stat(Nf, P, Delta, av, ay, q, D=D_TGT):
    """the STATIONARY repair: a scalar rescale of the MA factor landing at
    dist == D exactly (closed form; no root find)."""
    e = rate_stat(Nf, P, Delta, av, ay, q)
    c = 1.0 - (e["dist"] - D) / float(np.mean(e["nw"]))
    q2 = q * np.sqrt(c)
    return q2, float(c), rate_stat(Nf, P, Delta, av, ay, q2)


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


def kern(Delta, L):
    """depth-L truncation of the pinned kernels."""
    av = np.asarray(KERN[Delta]["av"], float)[LMAX - L:LMAX + L + 1].copy()
    ay = np.asarray(KERN[Delta]["ay"], float)[LMAX - L:LMAX + L + 1].copy()
    q = np.asarray(KERN[Delta]["q"], float)[:L + 1].copy()
    return av, ay, q


def toeplitz_noise(q, m):
    Lq = len(q) - 1
    cz = np.array([float(np.dot(q[:len(q) - i], q[i:])) for i in range(Lq + 1)])
    k = np.abs(np.subtract.outer(np.arange(m), np.arange(m)))
    return np.where(k <= Lq, cz[np.minimum(k, Lq)], 0.0)


# =========================================================== s1 ORIENTATION
print("s1 THE ORIENTATION GATE (mandatory, first) -- the lag-orientation "
      "defect masquerades as a non-vanishing edge charge", flush=True)
rng1 = np.random.default_rng(20260807)           # internally pinned
worst_routes = 0.0
for _ in range(6):
    n = int(rng1.integers(6, 12))
    Dl = int(rng1.integers(0, 3))
    Av = 0.35 * rng1.standard_normal((n, n))
    Ay = 0.35 * rng1.standard_normal((n, n))
    B = rng1.standard_normal((n, n))
    Nc = 0.15 * (B @ B.T) / n + 0.10 * np.eye(n)
    v1 = la_cmi(n, Av, Ay, Nc, Delta=Dl)
    v2, _ = la_fast(n, Av, Ay, Nc, Delta=Dl)
    worst_routes = max(worst_routes, abs(v1 - v2))

worst_canon = 0.0
canon_cells = 0
for Dl in (0, 1, 2):
    for L in (6, 10):
        av, ay, q = kern(Dl, L)
        st = rate_stat(NF, PLAG, Dl, av, ay, q)
        n = 128
        Av, Ay, Nc = build_window(n, av, ay, q, mode="zero", eps=1e-6)
        _, sig = la_fast(n, Av, Ay, Nc, Delta=Dl)
        deep = sig[L + 16:n - L - 16] - st["sigma"]
        worst_canon = max(worst_canon, float(np.max(np.abs(deep))))
        canon_cells += len(deep)

rev_min = {}
for Dl in (0, 1, 2):
    L, n = 6, 128
    av, ay, q = kern(Dl, L)
    st = rate_stat(NF, PLAG, Dl, av, ay, q)
    Av, Ay, Nc = build_window(n, av[::-1], ay, q, mode="zero", eps=1e-6)
    _, sig = la_fast(n, Av, Ay, Nc, Delta=Dl)
    rev_min[Dl] = float(np.min(sig[L:n - L] - st["sigma"]))

L, Dl = 6, 0
av, ay, q = kern(Dl, L)
st0 = rate_stat(NF, PLAG, Dl, av, ay, q)
growth = {}
for tag, avu in (("canonical", av), ("reversed", av[::-1])):
    s = []
    for n in (64, 128, 256, 512):
        Av, Ay, Nc = build_window(n, avu, ay, q, mode="zero", eps=1e-6)
        _, sig = la_fast(n, Av, Ay, Nc, Delta=Dl)
        s.append(float(np.sum(np.log(sig[L:n - L] / st0["sigma"]))))
    growth[tag] = dict(sums=s, slope=(s[-1] - s[-2]) / 256.0)

n = 128
Ac, Yc, Nc_c = build_window(n, av, ay, q, mode="zero", eps=1e-6)
Ar, Yr, Nc_r = build_window(n, av[::-1], ay, q, mode="zero", eps=1e-6)
Ab, Yb, Nc_b = build_window(n, av[::-1], ay[::-1], q, mode="zero", eps=1e-6)
pc_c = percell_dist(n, Ac, Yc, Nc_c)
pc_r = percell_dist(n, Ar, Yr, Nc_r)
pc_b = percell_dist(n, Ab, Yb, Nc_b)
dist_zero_power = max(float(np.max(np.abs(pc_c - pc_r))),
                      float(np.max(np.abs(pc_c - pc_b))))
Aay, Yay, Nc_ay = build_window(n, av, ay[::-1], q, mode="zero", eps=1e-6)
v_can, _ = la_fast(n, Ac, Yc, Nc_c, Delta=Dl)
v_ay, _ = la_fast(n, Aay, Yay, Nc_ay, Delta=Dl)
ay_rate_move = abs(v_ay - v_can)
ay_sym = max(float(np.max(np.abs(np.asarray(KERN[d]["ay"], float)
                                 - np.asarray(KERN[d]["ay"], float)[::-1])))
             for d in (0, 1, 2))

vals["s1"] = {"routes_worst": worst_routes, "canon_deep_worst": worst_canon,
              "canon_deep_cells": canon_cells,
              "reversed_min_interior": rev_min, "growth": growth,
              "dist_zero_power": dist_zero_power,
              "ay_reversal_rate_move": ay_rate_move, "ay_symmetry": ay_sym,
              "bars": {"routes": BAR_S1_ROUTES, "canon": BAR_S1_CANON,
                       "rev_cell": BAR_S1_REV_CELL, "rev_sum": BAR_S1_REV_SUM,
                       "rev_slope": BAR_S1_REV_SLOPE,
                       "canon_slope": BAR_S1_CANON_SLOPE,
                       "dist": BAR_S1_DIST_ZEROPOWER, "ay": BAR_S1_AY_SYM}}
verdicts["s1_two_evaluator_routes_agree"] = worst_routes <= BAR_S1_ROUTES
verdicts["s1_canonical_build_reproduces_stationary_sigma"] = \
    worst_canon <= BAR_S1_CANON
verdicts["s1_MUSTFAIL_reversed_kernel_at_every_interior_cell"] = \
    rev_min[0] >= BAR_S1_REV_CELL
verdicts["s1_MUSTFAIL_reversed_kernel_makes_edge_charge_O_of_n"] = (
    growth["reversed"]["sums"][-1] >= BAR_S1_REV_SUM
    and growth["reversed"]["slope"] >= BAR_S1_REV_SLOPE
    and abs(growth["canonical"]["slope"]) <= BAR_S1_CANON_SLOPE)
verdicts["s1_W5_distortion_gate_has_ZERO_power"] = \
    dist_zero_power < BAR_S1_DIST_ZEROPOWER
verdicts["s1_W5_ay_is_symmetric_and_carries_no_orientation"] = (
    ay_rate_move < BAR_S1_AY_SYM and ay_sym < BAR_S1_AY_SYM)
print(f"  two evaluator routes (raw CMI vs Collapse) {worst_routes:.2e} <= "
      f"{BAR_S1_ROUTES:.0e}; canonical deep-interior sigma offset "
      f"{worst_canon:.2e} <= {BAR_S1_CANON:.0e} over {canon_cells} cells")
print(f"  MUST-FAIL reversed-a_v control: min over ALL interior cells "
      f"{rev_min[0]:+.3e} >= {BAR_S1_REV_CELL:.0e} at Delta=0 (reported at "
      f"Delta=1,2: {rev_min[1]:+.2e} / {rev_min[2]:+.2e}); sum delta_t "
      + " -> ".join(f"{x:.3f}" for x in growth["reversed"]["sums"])
      + f" (slope {growth['reversed']['slope']:+.4e}/cell) against a "
        f"canonical slope of {growth['canonical']['slope']:+.2e}")
print(f"  W5 NEGATIVE CONTROL -- the per-cell DISTORTION has ZERO power: "
      f"{dist_zero_power:.2e} < {BAR_S1_DIST_ZEROPOWER:.0e}; reversing a_y "
      f"alone moves the rate by {ay_rate_move:.2e} (K1: a_y is real "
      f"zero-phase, symmetry defect {ay_sym:.2e}) [{time.time()-t0:.0f}s]",
      flush=True)

# ================================================= s2 EDGE CELLS ARE ZERO
print("\ns2 STEP (1) -- the edge cells of the ZERO-EDGE build contribute "
      "EXACTLY zero", flush=True)
w_cmi = w_sig = w_bd = 0.0
w_route2 = 0.0
for Dl in (0, 1, 2):
    for L in (6, 10):
        n, eps = 48, 1e-6
        av, ay, q = kern(Dl, L)
        Av, Ay, Nc = build_window(n, av, ay, q, mode="zero", eps=eps)
        vf, sig = la_fast(n, Av, Ay, Nc, Delta=Dl)
        vc, num, den = la_cmi(n, Av, Ay, Nc, Delta=Dl, parts=True)
        edge = np.r_[np.arange(L), np.arange(n - L, n)]
        inter = np.arange(L, n - L)
        contrib = np.log(num / den) / (2 * LN2)
        _, ldall = np.linalg.slogdet(Nc)
        _, ldint = np.linalg.slogdet(Nc[np.ix_(inter, inter)])
        w_cmi = max(w_cmi, float(np.max(np.abs(contrib[edge]))))
        w_sig = max(w_sig, float(np.max(np.abs(sig[edge] - eps))))
        w_bd = max(w_bd, abs(ldall - (2 * L * np.log(eps) + ldint)))
        w_route2 = max(w_route2, abs(vc - vf))
vals["s2"] = {"edge_percell_cmi": w_cmi, "edge_sigma_minus_eps": w_sig,
              "blockdiag_lndet_residual": w_bd, "routes": w_route2,
              "bars": {"cmi": BAR_S2_CMI, "sigeps": BAR_S2_SIGEPS,
                       "blockdiag": BAR_S2_BLOCKDIAG}}
verdicts["s2_edge_cells_contribute_exactly_zero"] = w_cmi < BAR_S2_CMI
verdicts["s2_edge_sigma_is_exactly_eps"] = w_sig < BAR_S2_SIGEPS
verdicts["s2_Nc_is_block_diagonal"] = w_bd < BAR_S2_BLOCKDIAG
print(f"  per-cell CMI on the 2L edge cells {w_cmi:.2e} < {BAR_S2_CMI:.0e}; "
      f"|sigma_t - eps| {w_sig:.2e} < {BAR_S2_SIGEPS:.0e}; block-diagonality "
      f"lndet Nc - [2L ln eps + lndet T_int] {w_bd:.2e} < "
      f"{BAR_S2_BLOCKDIAG:.0e} (routes agree {w_route2:.1e}) "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ================================================ s3 THE SUBSET ARGUMENT
print("\ns3 STEP (2) -- the SUBSET conditioning argument (the mirror of the "
      "bypass's superset step), verified PAST saturation", flush=True)
s3_rows = []
min_delta = 0.0
neg_total = 0
for Dl in (0, 1, 2, 3, 5, 9, 20):
    L, n = 6, 48
    av, ay, q = kern(0, L)
    stl = rate_stat(NF, PLAG, Dl, av, ay, q)
    Av, Ay, Nc = build_window(n, av, ay, q, mode="zero", eps=1e-6)
    _, sig = la_fast(n, Av, Ay, Nc, Delta=Dl)
    d = np.log(sig[L:n - L] / stl["sigma"])
    neg = int((d < BAR_S3_MINDELTA).sum())
    neg_total += neg
    min_delta = min(min_delta, float(d.min()))
    s3_rows.append({"Delta": Dl, "min": float(d.min()), "sum": float(d.sum()),
                    "neg": neg, "saturated": bool(Dl >= n)})
vals["s3"] = {"rows": s3_rows, "min_delta": min_delta, "neg_total": neg_total,
              "bar": BAR_S3_MINDELTA}
verdicts["s3_no_negative_delta_t_anywhere"] = (min_delta >= BAR_S3_MINDELTA
                                               and neg_total == 0)
print(f"  Delta in {{0,1,2,3,5,9,20}} (n=48, so Delta=20 is deep into the "
      f"saturated regime): min delta_t {min_delta:+.2e} >= "
      f"{BAR_S3_MINDELTA:.0e}, {neg_total} negative cells in total "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ======================================= s4 THE EDGE CHARGE IS n-INDEPENDENT
print("\ns4 STEP (3) -- sum_t delta_t is EXACTLY n-independent (this is the "
      "object that does not move with n -- NOT the constant C)", flush=True)
s4_rows = []
worst_spread = 0.0
worst_rec = 0.0
for Dl in (0, 1, 2):
    for L in (4, 10):
        av, ay, q = kern(Dl, L)
        st = rate_stat(NF, PLAG, Dl, av, ay, q)
        s = []
        for n in (128, 256, 512):
            Av, Ay, Nc = build_window(n, av, ay, q, mode="zero", eps=1e-6)
            _, sig = la_fast(n, Av, Ay, Nc, Delta=Dl)
            s.append(float(np.sum(np.log(sig[L:n - L] / st["sigma"]))))
        spread = max(s) - min(s)
        worst_spread = max(worst_spread, spread)
        row = {"Delta": Dl, "L": L, "sums": s, "spread": spread}
        if L == 10:
            row["recorded"] = REC_EDGE_CHARGE[Dl]
            row["dev"] = abs(s[0] - REC_EDGE_CHARGE[Dl])
            worst_rec = max(worst_rec, row["dev"])
        s4_rows.append(row)
vals["s4"] = {"rows": s4_rows, "worst_spread": worst_spread,
              "worst_recorded_dev": worst_rec,
              "bars": {"spread": BAR_S4_SPREAD, "recorded": BAR_S4_RECORDED}}
verdicts["s4_sum_delta_t_is_n_independent"] = worst_spread < BAR_S4_SPREAD
verdicts["s4_reproduces_the_recorded_L10_triple"] = worst_rec < BAR_S4_RECORDED
print(f"  spread over n in {{128,256,512}} at L in {{4,10}} x Delta in "
      f"{{0,1,2}}: {worst_spread:.2e} < {BAR_S4_SPREAD:.0e}")
print("  L=10 triple: "
      + " / ".join(f"{r['sums'][0]:.9f}" for r in s4_rows if r["L"] == 10)
      + f"  vs recorded 0.043994832 / 0.051454447 / 0.052333440, worst "
        f"deviation {worst_rec:.2e} < {BAR_S4_RECORDED:.0e} "
        f"[{time.time()-t0:.0f}s]", flush=True)

# ================================================== s5 THE SZEGO NOISE LEG
print("\ns5 STEP (4) -- the Szego noise leg is >= 0 (it HELPS), flat in m, "
      "and min-phase", flush=True)
leg_min = 1e9
leg_flat = 0.0
minphase = 0.0
legs = {}
for Dl in (0, 1, 2):
    for L in (6, 10):
        av, ay, q = kern(Dl, L)
        q2, _, e2 = rescale_stat(NF, PLAG, Dl, av, ay, q)
        vv = []
        for m in (16, 32, 64, 128, 256, 512):
            _, ld = np.linalg.slogdet(toeplitz_noise(q2, m))
            vv.append(ld - m * e2["lnn"])
        leg_min = min(leg_min, min(vv))
        leg_flat = max(leg_flat, max(vv) - min(vv))
        minphase = max(minphase, abs(e2["lnn"] - 2 * np.log(q2[0])))
        if L == 10:
            legs[Dl] = float(vv[3])
vals["s5"] = {"legs_L10": legs, "leg_min": leg_min, "flat": leg_flat,
              "minphase": minphase,
              "bars": {"min": BAR_S5_LEG_MIN, "flat": BAR_S5_FLAT,
                       "minphase": BAR_S5_MINPHASE}}
verdicts["s5_noise_leg_enters_with_the_helping_sign"] = leg_min >= BAR_S5_LEG_MIN
verdicts["s5_noise_leg_is_n_independent"] = leg_flat < BAR_S5_FLAT
verdicts["s5_min_phase_identity"] = minphase < BAR_S5_MINPHASE
print(f"  lndet T_m - m<ln n(w)> at L=10: "
      + " / ".join(f"{legs[d]:+.4e}" for d in (0, 1, 2))
      + f"; min over the grid {leg_min:+.3e} >= {BAR_S5_LEG_MIN:.0e}, "
        f"flatness over m in {{16..512}} {leg_flat:.2e} < {BAR_S5_FLAT:.0e}, "
        f"<ln n(w)> = 2 ln q0 to {minphase:.2e} [{time.time()-t0:.0f}s]",
      flush=True)

# ================================== s6 THE REPAIR AND FEASIBILITY THRESHOLD
print("\ns6 STEP (5) -- the repair is exactly affine and lands at dist = D; "
      "and W2, the FEASIBILITY THRESHOLD n >= n0(L)", flush=True)
w_affine = w_dist = 0.0
for Dl in (0, 1, 2):
    L = 10
    av, ay, q = kern(Dl, L)
    q2, _, _ = rescale_stat(NF, PLAG, Dl, av, ay, q)
    for n in (64, 256):
        Av, Ay, Nc0 = build_window(n, av, ay, q2, mode="trunc")
        d1 = dist_of(n, Av, Ay, Nc0)
        tr = np.trace(Nc0)
        cs = np.array([0.5, 0.8, 1.3])
        ds = np.array([dist_of(n, Av, Ay, c * Nc0) for c in cs])
        w_affine = max(w_affine,
                       float(np.max(np.abs(ds - (d1 + (cs - 1) * tr / n)))))
        c = 1.0 - (d1 - D_TGT) * n / tr
        w_dist = max(w_dist, abs(dist_of(n, Av, Ay, c * Nc0) - D_TGT))
thr = {}
for Dl in (0, 1, 2):
    av, ay, q = kern(Dl, 10)
    q2, _, _ = rescale_stat(NF, PLAG, Dl, av, ay, q)
    thr[Dl] = {}
    for n in (64, 128):
        _, _, _, c, _ = rescale_window(n, av, ay, q2, mode="zero")
        thr[Dl][n] = c
worst_infeas = max(thr[d][64] for d in (0, 1, 2))
worst_feas = min(thr[d][128] for d in (0, 1, 2))
vals["s6"] = {"affine_residual": w_affine, "dist_minus_D": w_dist,
              "zero_edge_rescale": thr,
              "bars": {"affine": BAR_S6_AFFINE, "dist": BAR_S6_DIST,
                       "infeas": BAR_S6_INFEAS, "feas": BAR_S6_FEAS}}
verdicts["s6_window_distortion_is_exactly_affine"] = w_affine < BAR_S6_AFFINE
verdicts["s6_repair_lands_at_dist_equals_D"] = w_dist < BAR_S6_DIST
verdicts["s6_MUSTFAIL_zero_edge_build_is_INFEASIBLE_at_n64_L10"] = \
    worst_infeas <= BAR_S6_INFEAS
verdicts["s6_the_same_build_is_feasible_at_n128"] = worst_feas >= BAR_S6_FEAS
print(f"  affine residual {w_affine:.2e} < {BAR_S6_AFFINE:.0e}; |dist - D| "
      f"{w_dist:.2e} < {BAR_S6_DIST:.0e}")
print(f"  W2 MUST-FAIL: the ZERO-EDGE build at n=64, L=10 has rescale c = "
      + " / ".join(f"{thr[d][64]:+.3f}" for d in (0, 1, 2))
      + f" (worst {worst_infeas:+.3f} <= {BAR_S6_INFEAS}), i.e. INFEASIBLE; "
        f"at n=128 the same build has c >= {worst_feas:+.3f} >= "
        f"{BAR_S6_FEAS} -- n0(L) is real and L-dependent "
        f"[{time.time()-t0:.0f}s]", flush=True)

# ================================================ s7 C(L, n) IS MONOTONE
print("\ns7 W1 -- C(L, n) is MONOTONE DECREASING in n.  THIS SECTION GATES "
      "MONOTONICITY AND NEVER n-INDEPENDENCE", flush=True)
s7_rows = []
bad_rows = 0
witness = None
for mode in ("trunc", "zero"):
    for Dl in (0, 1, 2):
        for L in (4, 6, 10):
            av, ay, q = kern(Dl, L)
            q2, _, e2 = rescale_stat(NF, PLAG, Dl, av, ay, q)
            pts = []
            for n in (64, 128, 256, 512, 1024):
                Av, Ay, Nc, c, _ = rescale_window(n, av, ay, q2, mode=mode)
                if c <= 0:
                    pts.append((n, None))
                    continue
                v, _ = la_fast(n, Av, Ay, Nc, Delta=Dl)
                pts.append((n, n * (v - e2["rate"])))
            good = [(n, x) for n, x in pts if x is not None]
            dec = all(good[i][1] > good[i + 1][1] for i in range(len(good) - 1))
            top = good[0][1] == max(x for _, x in good)
            ok = bool(dec and top)
            bad_rows += 0 if ok else 1
            row = {"mode": mode, "Delta": Dl, "L": L,
                   "pts": [(n, x) for n, x in pts], "decreasing": dec,
                   "max_at_first_feasible": top,
                   "factor": good[0][1] / good[-1][1]}
            s7_rows.append(row)
            if mode == "zero" and Dl == 0 and L == 6:
                witness = row
vals["s7"] = {"rows": s7_rows, "non_monotone_rows": bad_rows,
              "witness_factor": witness["factor"],
              "bar_witness_factor": BAR_S7_WITNESS_FACTOR,
              "note": "no gate in this section asserts that C does not "
                      "depend on n; only C(L,n) = o(n) is ever used"}
verdicts["s7_C_is_monotone_decreasing_in_n_every_row"] = bad_rows == 0
verdicts["s7_W1_refutation_witness_has_power"] = \
    witness["factor"] >= BAR_S7_WITNESS_FACTOR
print(f"  {len(s7_rows) - bad_rows}/{len(s7_rows)} pinned (mode, Delta, L) "
      f"rows strictly decreasing in n with the maximum at the first FEASIBLE "
      f"n")
print(f"  W1 witness (ZERO-EDGE, L=6, Delta=0): C = "
      + " -> ".join("%.2f" % x for _, x in witness["pts"] if x is not None)
      + f" over n = 64..1024, a factor {witness['factor']:.2f} >= "
        f"{BAR_S7_WITNESS_FACTOR} -- the constant DOES move with n; what does "
        f"not is the edge charge of s4 [{time.time()-t0:.0f}s]", flush=True)

# ============================================ s8 THE UNCONDITIONAL BRACKETS
print("\ns8 THE UNCONDITIONAL BRACKETS -- they depend on NO LEMMA: only F0 "
      "membership, exact feasibility and correct evaluation", flush=True)
s8_rows = []
w_v2048 = w_feas = w_routes8 = 0.0
anchors_ok = 0
anchors_tot = 0
anchor_min = 1e9
outward_ok = 0
widths = {}
for Dl in (0, 1, 2):
    av, ay, q = kern(Dl, 10)
    q2, _, e2 = rescale_stat(NF, PLAG, Dl, av, ay, q)
    row = {"Delta": Dl, "U10": e2["rate"], "V": {}}
    for n in (16, 24, 32, 48, 2048):
        Av, Ay, Nc, c, _ = rescale_window(n, av, ay, q2, mode="trunc")
        b = moments(n, Av, Ay, Nc)
        v, _ = la_fast(n, Av, Ay, Nc, Delta=Dl, blocks=b)
        dd = dist_of(n, Av, Ay, Nc, blocks=b)
        w_feas = max(w_feas, abs(dd - D_TGT))
        row["V"][n] = v
        if n <= 32:
            w_routes8 = max(w_routes8, abs(la_cmi(n, Av, Ay, Nc, Delta=Dl) - v))
            a = REC_ANCHOR[Dl].get(n)
            if a is not None:
                anchors_tot += 1
                anchors_ok += int(v > a)
                anchor_min = min(anchor_min, v - a)
        if n == 2048:
            w_v2048 = max(w_v2048, abs(v - REC_V2048[Dl]))
            outward_ok += int(REC_UPPER_ROUNDED[Dl] >= v)
            widths[Dl] = REC_UPPER_ROUNDED[Dl] - REC_PSI_LB[Dl]
            row["beats_UB32_from_n48"] = bool(row["V"][48] < REC_ANCHOR[0][32]
                                              ) if Dl == 0 else None
    s8_rows.append(row)

safe_grid = []
for Dl in (0, 1, 2):
    av, ay, q = kern(Dl, 10)
    q2, _, _ = rescale_stat(NF, PLAG, Dl, av, ay, q)
    g = [rate_stat(nf, P, Dl, av, ay, q2)["rate"]
         for nf in (1024, 2048, 4096, 8192) for P in (20, 60, 140, 400)]
    p1 = rate_stat(NF, 1, Dl, av, ay, q2)["rate"]
    p8 = rate_stat(NF, 8, Dl, av, ay, q2)["rate"]
    safe_grid.append({"Delta": Dl, "flat": max(g) - min(g), "P1": p1,
                      "P8": p8, "power": p1 - p8})
safe_flat = max(x["flat"] for x in safe_grid)
safe_power = min(x["power"] for x in safe_grid)

vals["s8"] = {"rows": s8_rows, "V2048_dev": w_v2048, "feas": w_feas,
              "routes": w_routes8, "anchors_ok": anchors_ok,
              "anchors_tot": anchors_tot, "anchor_min_margin": anchor_min,
              "outward_rounded_ok": outward_ok, "widths_REPORTED": widths,
              "safe_side": safe_grid,
              "brackets_REPORTED": {d: [REC_PSI_LB[d], REC_UPPER_ROUNDED[d]]
                                    for d in (0, 1, 2)},
              "bars": {"V2048": BAR_S8_V2048, "feas": BAR_S8_FEAS,
                       "anchor": BAR_S8_ANCHOR_MARGIN, "routes": BAR_S8_ROUTES,
                       "safe_flat": BAR_S8_SAFE_FLAT,
                       "safe_power": BAR_S8_SAFE_POWER},
              "note": "NO WIDTH IS GATED -- the widths and their positivity "
                      "are reported only"}
verdicts["s8_reproduces_V10_2048_at_three_Delta"] = w_v2048 < BAR_S8_V2048
verdicts["s8_certificate_records_are_exactly_D_feasible"] = w_feas < BAR_S8_FEAS
verdicts["s8_anchor_cross_check_is_8_of_8"] = (anchors_ok == anchors_tot == 8
                                               and anchor_min
                                               > BAR_S8_ANCHOR_MARGIN)
verdicts["s8_recorded_upper_ends_are_outward_rounded"] = outward_ok == 3
verdicts["s8_both_routes_agree_on_the_certificate_records"] = \
    w_routes8 < BAR_S8_ROUTES
verdicts["s8_W11_safe_side_is_flat_from_P20"] = safe_flat < BAR_S8_SAFE_FLAT
verdicts["s8_W11_safe_side_control_has_power"] = safe_power > BAR_S8_SAFE_POWER
print("  V(10,2048) = "
      + " / ".join(f"{r['V'][2048]:.12f}" for r in s8_rows)
      + f"  (recorded to {w_v2048:.2e} < {BAR_S8_V2048:.0e})")
print(f"  exact feasibility |dist - D| {w_feas:.2e} < {BAR_S8_FEAS:.0e}; "
      f"la_cmi vs la_fast on the certificate records {w_routes8:.2e}; "
      f"anchor cross-check {anchors_ok}/{anchors_tot} with min margin "
      f"{anchor_min:+.2e} > {BAR_S8_ANCHOR_MARGIN:.0e}")
print("  brackets (REPORTED, never gated): "
      + " / ".join(f"[{REC_PSI_LB[d]:.10f}, {REC_UPPER_ROUNDED[d]:.10f}] "
                   f"w={widths[d]:.3e}" for d in (0, 1, 2)))
print(f"  W11 safe side: NON-INCREASING IN P BY CONSTRUCTION; flat to "
      f"{safe_flat:.1e} < {BAR_S8_SAFE_FLAT:.0e} over Nf in {{1024..8192}} x "
      f"P in {{20..400}}, and the direction has power (P=1 minus P=8 = "
      f"{safe_power:.2e} > {BAR_S8_SAFE_POWER:.0e}) [{time.time()-t0:.0f}s]",
      flush=True)

# ============================================ s9 DOES IT PROVE TOO MUCH?
print("\ns9 DOES IT PROVE TOO MUCH?  No -- the machinery never produces a "
      "bound below the independently known block infimum", flush=True)
av, ay, q = kern(0, 10)
q2, _, _ = rescale_stat(NF, PLAG, 0, av, ay, q)
blk = []
for n in (64, 128, 256, 512, 1024):
    Av, Ay, Nc, c, _ = rescale_window(n, av, ay, q2, mode="trunc")
    v, _ = la_fast(n, Av, Ay, Nc, se=np.full(n, n))
    blk.append((n, v))
blk_min_excess = min(v - BLOCK_INF for _, v in blk)
blk_dec = all(blk[i][1] > blk[i + 1][1] for i in range(len(blk) - 1))

n = 256
Av, Ay, Nc, c, _ = rescale_window(n, av, ay, q2, mode="trunc")
b = moments(n, Av, Ay, Nc)
ladder = []
for Dl in (0, 1, 2, 3, 4, 6, 8, 12, 20, 32):
    v, _ = la_fast(n, Av, Ay, Nc, Delta=Dl, blocks=b)
    ladder.append((Dl, v))
lad_mono = all(ladder[i][1] >= ladder[i + 1][1] - 1e-14
               for i in range(len(ladder) - 1))
lad_min_excess = min(v - BLOCK_INF for _, v in ladder)
rec_mono = all(REC_PSI_LADDER[i] >= REC_PSI_LADDER[i + 1]
               for i in range(len(REC_PSI_LADDER) - 1))
rec_above = min(x - BLOCK_INF for x in REC_PSI_LADDER)

vals["s9"] = {"block_schedule": blk, "block_min_excess": blk_min_excess,
              "block_decreasing": blk_dec, "ladder": ladder,
              "ladder_monotone": lad_mono, "ladder_min_excess":
              lad_min_excess, "recorded_psi_ladder_monotone": rec_mono,
              "recorded_psi_ladder_min_excess": rec_above,
              "bar": BAR_S9_ABOVE,
              "note": "the recorded ~0.105/n convergence and the recorded "
                      "+1.70e-12 at Delta=12 are R-IND-5 data about "
                      "BLOCK-OPTIMAL / certified-Psi ladders and are NOT "
                      "re-derived here"}
verdicts["s9_block_program_never_falls_below_block_inf"] = (
    blk_min_excess > BAR_S9_ABOVE and blk_dec)
verdicts["s9_Delta_ladder_approaches_from_above_without_crossing"] = (
    lad_mono and lad_min_excess > BAR_S9_ABOVE)
verdicts["s9_recorded_Psi_ladder_is_monotone_and_above_block_inf"] = (
    rec_mono and rec_above >= 0.0)
print(f"  block schedule (se == n): "
      + " -> ".join(f"{v:.9f}" for _, v in blk)
      + f", monotone decreasing {blk_dec}, min excess over block_inf "
        f"{blk_min_excess:+.3e} > {BAR_S9_ABOVE:.0e}")
print(f"  Delta-ladder of a fixed record at n=256: "
      + " ".join(f"{v:.6f}" for _, v in ladder[:5]) + " ... "
      + f"{ladder[-1][1]:.6f}, monotone {lad_mono}, min excess "
        f"{lad_min_excess:+.3e}")
print(f"  bookkeeping on the recorded 082 Psi ladder (pinned literals, not "
      f"re-derived): monotone {rec_mono}, min excess over block_inf "
      f"{rec_above:+.2e} [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ report
vals["scope"] = {
    "lemma_W": "stated with W1-W4 IN the statement: C(L,n) MONOTONE "
               "DECREASING in n, sup_{n>=n0(L)} C(L,n) < infinity, only "
               "C(L,n) = o(n) used; feasibility threshold n >= n0(L) an "
               "explicit hypothesis; the three builds kept apart, steps "
               "(1)-(2) asserted only of the zero-edge build; the repair "
               "leg a SEPARATE estimate",
    "residual": "ONE residual: FIR-kernel stationary records dense in value. "
                "R's reference is the GRID FIXED POINT (Nf=4096, P=180); "
                "against the 082 certified LB endpoints the gap is "
                "+4.0e-11/+7.2e-11/+5.3e-11; L >= 11 entries are f64 noise "
                "going NEGATIVE at Delta=0 and are not cited",
    "brackets": "the two inequalities depend on NO LEMMA of the document -- "
                "only F0 membership, exact feasibility and correct "
                "evaluation.  'Unconditional' attaches to those inequalities "
                "and to the chain, NEVER to the value Psi",
    "no_equality": "NO statement that L^inf coincides with Psi is netted, "
                   "printed or implied; the chain is one-directional in each "
                   "direction SEPARATELY, and together they give a BRACKET",
    "novelty_sweep": "OWED on Lemma W's combination (Collapse + "
                     "subset-conditioning monotonicity + Toeplitz innovation "
                     "monotonicity as a SIGNED two-leg boundary argument); NO "
                     "novelty language is used for it anywhere",
    "optimizers": "none -- no optimizer, no fixed point and no root find, so "
                  "no gate can race a stopping point; the stationary kernels "
                  "are pinned data",
    "widths": "no bracket width is gated; the three widths and their "
              "positivity are reported only"}
verdicts = {k: bool(v) for k, v in verdicts.items()}
allpass = all(verdicts.values())
print()
for k, v in verdicts.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print(f"VERDICT: {'ALL PASS' if allpass else 'FAIL'} "
      f"{sum(verdicts.values())}/{len(verdicts)}")

out = {"verdict": verdicts, "GO14AC_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14AC-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
