#!/usr/bin/env python
"""GO-14 (H*)-REPAIR harness (tex v0.6: the lemma chain L1-L4, the
cross-block read X, the split-causal sub-family F0^sc, the Pi-retraction,
the repaired T*(ii) feasibility step, and the recomputed plateau
arithmetic).  Registration 081 pending -- NOTHING HERE IS SEALED.

Model: V AR(1) a = 0.8 unit variance; Y = 0.7 V + N, Var(Y) = 1;
S = V + U, tau2 = 0.4; D = 0.3; T = (V, Y) = W; family F0 (records
jointly Gaussian with (V, Y) and INDEPENDENT of U); phi_n(Delta) =
min L_a over F0 on the n-window; kappa = (1/2) log2(1/(1-a^2)) =
0.736966 bits.  Split of the n-window at m: b1 = cells 1..m,
b2 = cells m+1..n; E = (S^{b1}, Yh^{b1}); the CROSS-BLOCK READ is

        X := I(Yh^{b1}; W^{b2} | W^{b1}) .

DESIGN RULE (the 079 lesson, restated by 080): NO GATE MAY RACE AN
OPTIMIZER STOPPING POINT.  Every gate below is one of
  (a) an exact identity with a tolerance many orders above f64 noise,
  (b) an analytic inequality with a fat, measured margin,
  (c) a set/structural identity, or
  (d) reproduction of a committed value inside a band that is orders
      above the observed endpoint spread.
No certificate width and no bracket is gated anywhere.  Sections
s1-s5 and s7 contain NO OPTIMIZER AT ALL (the H-repair chain is
deterministic, analytic and optimizer-free -- that is the point of the
repair).  s6 and s8 are the only sections that read optimizer
endpoints; the disclosure for them is in the pilot record below.

s1 L1 -- KAPPA IS AN IDENTITY, NOT A BOUND.  I(T^{b1};T^{b2}) = kappa
   exactly at every split, m in {3,4,6,8,12,16} (AR(1) Markov: both
   data-processing steps are equalities).  Gate: max |I - kappa| <
   1e-12 AND m-INDEPENDENCE (spread over m < 1e-12) -- the proof
   predicts a constant, so a drift in m would refute the mechanism.

s2 L2 -- THE CROSS-READ BOUND.  I(E;T^{b2}) <= kappa + X and (for
   Delta > 0) I(E';E) <= kappa + X, E' = S^{b2,1..Delta}, on a pinned
   battery: 3 generic F0 styles x Delta in {0,1,2}, their split-causal
   Pi-projections, and the two ADVERSARIAL copy-row classes that refute
   the universal lemma.  Gate: zero violations, AND TIGHTNESS at the
   adversarial witness (min slack < 1e-5) -- the inequality is sharp
   exactly where the universal claim dies.

s3 L3 + L4 + THE H-REPAIR INEQUALITY.  L3: the exact identity
   D2 = I(E;T^{b2}) - I(E;T^{b2}|S',Yh') - sum_j I(E;S'_j|pfx_j)
   (residual gate 1e-9), the chain-rule collapse
   sum_{j<=Delta+1} = I(E;S'^{1..Delta+1}) (gate 1e-9) and
   I(E;S'^{1..Delta+1}) >= I_m, hence D2 <= I(E;T^{b2}) - I_m.
   L4: D1 <= I(E';E), and D1 = 0 at Delta = 0.  Hence
   D1 + D2 <= c(Delta;m) + (2 - 1{Delta=0}) X.  Gate: zero violations
   over the whole battery INCLUDING both refuting counterexamples, with
   min slack > 0.1.

s4 SPLIT-CAUSAL SUB-FAMILY F0^sc(m) = {H[b1,idx2] = H[b1,idx1]
   Sig11^-1 Sig12}.  Gate: X = 0 to 1e-12 on projected records;
   (H*) HOLDS there with the tex's own constants c(Delta;m) (min slack
   > 0.5); and the section is LINEAR -- moment midpoints of
   split-causal records stay split-causal (residual and X both < 1e-12),
   which is what makes Theorem C certify phi^sc two-sided.

s5 THE Pi-RETRACTION IDENTITIES.  Pi replaces the block-1 rows by their
   W^{b1}-conditional means plus matching independent noise.  Gate:
   distortion preserved < 1e-14, the entire block-1 joint law preserved
   < 1e-14, X killed < 1e-12, and Pi STRICTLY IMPROVES generic records
   (n*(L_a(Pi R) - L_a(R)) < -0.05 on the pinned generic battery).

s6 THE T*(ii) HYGIENE REPAIR.  The restriction step of Theorem T*(ii)
   needs each block distortion <= D; the 2m-optimizer's blocks
   STRADDLE D.  Gate: d1 < D < d2 at n in {16,24,32} with |d_i - D| >
   1e-4 (measured 2.6e-4..5.1e-4), the recorded values reproduced within
   1e-5, and the mean exactly D; PLUS the repair itself -- convexity of
   the value function D -> phi_8(D) on the pinned grid D in
   {0.26,0.28,0.30,0.32,0.34}: at each interior node the certified UB
   sits below the chord of the two certified LBs, slack > 5e-4
   (measured ~1.5e-3).  This is the gate that the naive route was wrong.

sK THEOREM K (KKT structure; unconditional, F0, any Delta).  Two exact
   structural facts drive it: K = Sig_WS' Sig_W^-1 = [I, 0] (because
   E[S|W] = V and V is a coordinate block of W) so the Q-factor terms
   live only on the V-columns; and Sig_W^-1 Sig_WY = [0; I] so the
   distortion gradient lives only on the Y-columns.  The supports are
   DISJOINT, so stationarity splits by column block:
     (K1) Ay = theta N,  theta = 2 mu ln2;
     (K2) N^-1 = theta I + V Sig_s^-1 V';
     (K3) Av = -N V Sig_s^-1 V_S',
   where V Sig_s^-1 V' and -V Sig_s^-1 V_S' are the (Yh,Yh) and
   (Yh,S) blocks of the RECORD-pivot Gram of the interleaved order
   (see pivot_gram; the reference-pivot reading of (K2) is FALSE at the
   47% level and is not what the theorem says).  Gates: the two
   structural facts < 1e-12; the Cholesky split G_S + G_Yh = J^-1 <
   1e-12; the three identities < 1e-6 at six certified optimizers
   ((16/24/32/48, Delta=0) and (16, Delta=1), (16, Delta=2));
   Ay transpose-symmetry < 1e-6 -- which turns the 078-era EMPIRICAL
   mechanism finding into a COROLLARY; and the m-uniform regularity
   0 < N <= I/theta, 0 < Ay <= I with theta >= 1.119.
   DISCLOSURE: the three identity residuals track the POLISH ACCURACY
   of the optimizer (observed ~1e-8), not the identities, which are
   exact; the bar is set 26x above the observed value for that reason.

s7 CONSTANTS + COROLLARY ARITHMETIC (exact, no optimizer except the
   single scalar X(m=8) carried in from s8's shared endpoint):
   c(0) + X = 0.4266326 to 1e-6; the recomputed plateau
   LB(32,0) - (c(0)+X)/32 = 0.5514005 > 0.5479448 with ratio to the
   tex-v0.4 bracket width in [200,210]; the base-24 negative control
   FAILS by > 1e-4; and the sealed 079 LB(32,0) read from
   results/GO14-convexity.json matches the hard-coded value exactly.
   Also the ALTERNATIVE arithmetic under the decay prover's (D)+(F)
   route, c(0) + Xbar = 0.485324: the plateau still clears (margin
   1.62e-3, gate 1e-3) and the base-24 control still fails (2.76e-3).

s8 THE MONOTONE m-TABLE (the prover's cheap-hardening item), retiring
   the "m in {8,16} only" caveat: D1+D2, I(E;T^{b2}) and X at Delta = 0
   for m in {8,12,16,24} (n = 2m).  Gate: all three STRICTLY DECREASING
   in m, each step >= 1e-6 (smallest measured step 5.3e-6), and every
   entry reproducing the committed prover value within 1e-5.
   DISCLOSURE: s6 and s8 are the only sections reading optimizer
   endpoints.  The optimizer is a deterministic COLD START (no warm
   start, no random restart), and its endpoints reproduce the prover's
   independently produced committed values BIT-IDENTICALLY here
   (measured spread 0.0e0, gated at 1e-5); the monotone bar 1e-6 per
   step therefore sits ~5x under the smallest true step and orders
   above any endpoint spread.  Neither gate is a width or a bracket.

s9 THE SPLIT-CAUSAL TRANSFER STEP AND (H***).  Concatenating two
   independent m-optimal records is split-causal, so
   phi^sc_{2m} <= phi_m UNCONDITIONALLY.  Gate: the CERTIFIED form
   UB(phi^sc_{2m}) < LB(phi_m) at (2m,m) = (16,8)/(24,12)/(32,16),
   slack > 5e-4 (measured ~1.9e-3-3.8e-3).  The resulting hypothesis
   (H***) constrains the split-causality VALUE GAP
   p_n = n (phi^sc_n - phi_n) -- a gap between two CONVEX programs,
   hence two-sided certifiable by Theorem C, unlike X which is only
   measurable at a computed optimizer.  Gate: p_n reproduces the
   committed certified values within 1e-5 and stays inside the
   admissible pbar = 32(LB(32,0) - 0.5479448) - c(0) = 0.1169299.

Sentinel ===GO14HR-JSON=== with ===END===; flag GO14HR_supported.
Pilot seed 20261140 / governed seed 20261141.  SEED STAMPS ONLY: the
seed is recorded in the output and feeds NO computation -- every random
draw uses an internally pinned generator (20260806) and every optimizer
is a deterministic cold start, so pilot and governed verify identical
numbers.

Evaluator lineage: every mutual information / conditional variance goes
through an INDEPENDENT slogdet route on explicit 4n joint covariances
(the R-IND-5 transfer verifier's evaluator), never through the
optimizer's cho_solve pivot route; the certify machinery
(experiments/go14_convexity.py lineage) is used ONLY to produce points,
and every reported endpoint is re-valued independently.

All floating-point certificates: no interval arithmetic.

PILOT RECORD (seed 20261140, 2026-08-07).
 iter 1 -- ALL PASS 24/24, 162 s (sections s1-s8 as first written).
   Every bar had been fixed BEFORE the run from the (H*)-repair
   prover's committed artifacts; no bar was moved, in either
   direction.  Re-run of the identical command reproduced the whole
   JSON payload BIT-IDENTICALLY (verified by whole-payload compare),
   confirming the seed-stamp-only discipline.
 iter 2 -- ALL PASS 29/29, 223 s, after the decay prover's material
   was added (sK, s9, and the (D)+(F) arithmetic in s7).  No bar of
   iter 1 was touched; the five new verdicts carry bars set from the
   decay prover's committed values.
 MEASURED vs BAR (the ratio is the margin):
   s1 3.8e-14 / 1e-12 (26x); m-spread 4.1e-14
   s2 tightness 5.67e-7 / 1e-5 (18x); adversarial X repro 0.0 / 1e-6
   s3 identity 9.3e-11 / 1e-9 (11x); H-repair min slack 0.768 / 0.1 (7.7x)
   s4 X 1.0e-14 / 1e-12 (97x); (H*) slack 0.768 / 0.5 (1.5x);
      linearity 1.1e-16 / 1e-12
   s5 dist 1.1e-16 and law 6.7e-16 / 1e-14 (15-90x); X 2.1e-14 / 1e-12;
      worst gain -0.308 / -0.05 (6.2x)
   sK identities max 8.3e-8 / 1e-6 (12x); symmetry 2.1e-8 / 1e-6 (48x);
      structural 2.4e-15 / 1e-12; theta 3.078 / 1.119 (2.8x)
   s6 straddle 2.56e-4 / 1e-4 (2.6x); repro 0.0 / 1e-5;
      convexity slack 1.47e-3 / 5e-4 (2.9x)
   s7 c+X err 1.7e-8 / 1e-6 (59x); margin 3.456e-3 / 2.5e-3 (1.4x);
      ratio 203.3 in [200,210]; shortfall24 3.11e-4 / 1e-4 (3.1x);
      (D)+(F) margin 1.62e-3 / 1e-3 (1.6x), shortfall 2.76e-3 (2.8x)
   s8 min step 4.96e-6 / 1e-6 (5.0x); repro 0.0 / 1e-5
   s9 min slack 1.88e-3 / 5e-4 (3.8x); p repro 0.0 / 1e-5; p_max
      0.004382, 26.7x inside the admissible 0.116930
 DISCLOSURES.  (a) The prover's report attributes the tightness of L2
   to the three-Y-copy counterexample; the artifact and this harness
   both put it at the TWO-V-copy witness (slack 5.67e-7 there against
   0.144 at the three-Y-copy record).  The value 5.67e-7 is correct;
   the attribution is not, and the tex prints the corrected one.
 (b) The prover's report quotes L_a = 1.73 / 2.25 for the refuting
   records; the harness's pinned witnesses measure 4.2187 / 4.7397.
   Those numbers are not reproducible from any artifact in the
   scratchpad, so the tex prints the harness's own.
 (c) The prover's report quotes the feasible cold-start m=16 charge as
   0.0769152; the artifact and this harness both give 0.07691493
   (difference 3e-7, immaterial at the 5e-3 band).  The tex prints
   0.0769149.
 (d) The coordinator's transmitted form of (K2)/(K3) uses "V Sig_s^-1
   V'"; that object must be the RECORD-pivot Gram.  With the
   reference-pivot Gram (K2) fails at 47% and (K3) at 120%.  Verified,
   disclosed, and stated correctly in the tex.
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
SEED = a_.seed if a_.seed is not None else (20261140 if a_.pilot
                                            else 20261141)
verdicts = {}
vals = {"seed": SEED, "pilot": bool(a_.pilot)}

A_ = 0.8
RHO = 0.7
TAU2 = 0.4
SN2 = 1.0 - RHO ** 2
D_TGT = 0.3
LN2 = np.log(2.0)
KAPPA = 0.5 * np.log2(1.0 / (1.0 - A_ ** 2))     # 0.7369655941662063

HERE = os.path.dirname(os.path.abspath(__file__))
CXJSON = os.path.join(HERE, os.pardir, "results", "GO14-convexity.json")
SEALED_LB32 = 0.5647327868912777     # 079 governed s5_32_0 LB
SEALED_LB24 = 0.5654101216393774     # 079 governed s5_24_0 LB
SEALED_W32 = 9.180762755356398e-06   # 079 governed s5_32_0 width
TEXW32 = 1.7e-5                      # tex v0.4 anchor-table width (32,0)
SPEC0 = 0.5479448                    # causal-spectral allocation, Delta=0
# committed prover values ((H*) repair prover, 2026-08-07, hstar/)
REC_TABLE = {8:  {"DD": 0.07697093254679632, "IET": 0.5430687170240702,
                  "X": 0.006346781587488671, "price": 0.00505196675266717,
                  "phi": 0.5667581621669033},
             12: {"DD": 0.07693357621089636, "IET": 0.543058722599273,
                  "X": 0.006336043148090764, "price": 0.005043503671239513,
                  "phi": 0.5654138766074547},
             16: {"DD": 0.07691493424586315, "IET": 0.5430537329034071,
                  "X": 0.006330685986242935, "price": 0.005039283762428681,
                  "phi": 0.5647419676540331},
             24: {"DD": 0.07689635964790742, "IET": 0.5430487767580624,
                  "X": 0.006325355205529827, "price": 0.0050350790668680645,
                  "phi": 0.5640699776859408}}
REC_BLOCKD = {16: (0.2994861556653743, 0.3005138198402818, 2.2206487637049577),
              24: (0.2996579783437916, 0.3003420038472895, 2.2224707305467746),
              32: (0.29974364837320827, 0.30025626149149687,
                   2.223381035033526)}
REC_ADV_X = {"two_V_copies": 18.457642670850465,
             "three_Y_copies": 29.273693634497832}
REC_CPLUSX = 0.4266326               # c(0) + X(m=8), tex v0.6
REC_PLATEAU = 0.5514005              # recomputed Delta=0 plateau
# decay prover (2026-08-07): the (D)+(F) conversion constant, and the
# certified split-causality value gaps p_n = n (phi^sc_n - phi_n)
XBAR_DF = 0.065038                   # Xbar under (D) + (F)
REC_P = {16: 0.004164598246669371, 24: 0.004206979225707563,
         32: 0.004382478407720214}
REC_PHISC = {16: 0.5670144752858837, 24: 0.5655854048245753,
             32: 0.5648697384970781}
THETA_FLOOR = 1.119                  # 2 ln2 phi_n(D)/(1-D) bound


# ===================== model + independent evaluator =====================
def cov_model(n):
    i = np.arange(n)
    Cv = A_ ** np.abs(i[:, None] - i[None, :])
    Cy = RHO ** 2 * Cv + SN2 * np.eye(n)
    Cvy = RHO * Cv
    Cs = Cv + TAU2 * np.eye(n)
    return Cv, Cy, Cvy, Cs


def joint_cov(n, Av, Ay, Nc):
    """4n x 4n covariance, order V(0:n) Y(n:2n) S(2n:3n) Yh(3n:4n)."""
    Cv, Cy, Cvy, Cs = cov_model(n)
    CyhV = Av @ Cv + Ay @ Cvy
    CyhY = Av @ Cvy + Ay @ Cy
    CyhS = Av @ Cv + Ay @ Cvy
    CyhYh = (Av @ Cv @ Av.T + Ay @ Cy @ Ay.T + Av @ Cvy @ Ay.T
             + Ay @ Cvy @ Av.T + Nc)
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


def prefC(n, t, Delta):
    """big-window staircase conditioning set of cell t (4n indices)."""
    se = min(t + Delta + 1, n)
    return list(range(2 * n, 2 * n + se)) + list(range(3 * n, 3 * n + t))


def blocks_idx(n, m):
    b1 = list(range(0, m)) + list(range(n, n + m))
    b2 = list(range(m, n)) + list(range(n + m, 2 * n))
    E = list(range(2 * n, 2 * n + m)) + list(range(3 * n, 3 * n + m))
    return b1, b2, E


def dist_of(n, Av, Ay, Nc):
    Cv, Cy, Cvy, Cs = cov_model(n)
    CyhY = Av @ Cvy + Ay @ Cy
    CyhYh = (Av @ Cv @ Av.T + Ay @ Cy @ Ay.T + Av @ Cvy @ Ay.T
             + Ay @ Cvy @ Av.T + Nc)
    per = np.diag(Cy) - 2 * np.diag(CyhY) + np.diag(CyhYh)
    return float(per.mean()), per


def la_bits(n, Av, Ay, Nc, Delta):
    S4 = joint_cov(n, Av, Ay, Nc)
    T = list(range(2 * n))
    return float(sum(cmi_bits(S4, T, [3 * n + t], prefC(n, t, Delta))
                     for t in range(n)) / n)


def deficits(S4, n, m, Delta):
    """per-side boundary charges D1, D2 at the split n = m + (n-m)."""
    m2 = n - m
    b1, b2, _ = blocks_idx(n, m)
    D2 = 0.0
    for t2 in range(m2):
        t = m + t2
        se = min(t2 + Delta + 1, m2)
        ownC = (list(range(2 * n + m, 2 * n + m + se))
                + list(range(3 * n + m, 3 * n + m + t2)))
        D2 += (cmi_bits(S4, b2, [3 * n + t], ownC)
               - cmi_bits(S4, b2, [3 * n + t], prefC(n, t, Delta)))
    D1 = 0.0
    for t in range(m):
        se1 = min(t + Delta + 1, m)
        ownC = (list(range(2 * n, 2 * n + se1))
                + list(range(3 * n, 3 * n + t)))
        D1 += (cmi_bits(S4, b1, [3 * n + t], ownC)
               - cmi_bits(S4, b1, [3 * n + t], prefC(n, t, Delta)))
    return D1, D2


def sum_j_terms(S4, n, m, Delta, first_only=False):
    """sum_j I(E; S'_j | pfx_j); first_only -> j <= Delta+1 only."""
    m2 = n - m
    _, _, E = blocks_idx(n, m)
    hi = min(Delta + 1, m2) if first_only else m2
    tot = 0.0
    for j in range(1, hi + 1):
        kj = sum(1 for u in range(m2) if min(u + Delta + 1, m2) < j)
        pfx = (list(range(2 * n + m, 2 * n + m + j - 1))
               + list(range(3 * n + m, 3 * n + m + kj)))
        tot += cmi_bits(S4, E, [2 * n + m + j - 1], pfx)
    return tot


def imi_SS(m, Delta):
    """exact I(S_{1..m}; S_{m+1..m+Delta+1}) in bits, stationary window."""
    n = m + Delta + 1
    _, _, _, Cs = cov_model(n)
    return cmi_bits(Cs, range(m), range(m, n), [])


def cross_read(S4, n, m):
    """X = I(Yh^{b1}; W^{b2} | W^{b1}) -- the cross-block read."""
    b1, b2, _ = blocks_idx(n, m)
    return cmi_bits(S4, list(range(3 * n, 3 * n + m)), b2, b1)


def const_c(m, Delta):
    return (2.0 - (1.0 if Delta == 0 else 0.0)) * KAPPA - imi_SS(m, Delta)


def sigW(n):
    Cv, Cy, Cvy, _ = cov_model(n)
    return np.block([[Cv, Cvy], [Cvy, Cy]])


def sc_map(n, m):
    """Sig11^-1 Sig12 -- the split-causal linear map."""
    SW = sigW(n)
    idx1 = list(range(0, m)) + list(range(n, n + m))
    idx2 = list(range(m, n)) + list(range(n + m, 2 * n))
    return (np.linalg.solve(SW[np.ix_(idx1, idx1)], SW[np.ix_(idx1, idx2)]),
            idx1, idx2)


def split_project(n, m, Av, Ay, Nc):
    """Pi: the retraction onto the split-causal sub-family F0^sc(m).

    Yh^{b1} <- E[Yh^{b1} | W^{b1}] + independent compensating noise.
    Preserves EXACTLY the joint law of (W^{b1}, S^{b1}, Yh^{b1}) and the
    per-cell distortion of every cell; kills the cross-read X.
    """
    A = np.hstack([Av, Ay])
    Mmap, idx1, idx2 = sc_map(n, m)
    SW = sigW(n)
    S11 = SW[np.ix_(idx1, idx1)]
    S12 = SW[np.ix_(idx1, idx2)]
    S22 = SW[np.ix_(idx2, idx2)]
    S2g1 = S22 - S12.T @ np.linalg.solve(S11, S12)
    A1 = A[np.ix_(range(m), idx1)]
    A2 = A[np.ix_(range(m), idx2)]
    An = A.copy()
    An[np.ix_(range(m), idx1)] = A1 + A2 @ Mmap.T
    An[np.ix_(range(m), idx2)] = 0.0
    Nn = Nc.copy()
    Nn[:m, :m] = Nn[:m, :m] + A2 @ S2g1 @ A2.T
    return An[:, :n], An[:, n:], 0.5 * (Nn + Nn.T)


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
    ks = kcounts(n, np.minimum(np.arange(n) + Delta + 1, n))
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


def pivot_gram(M, H, Gam, Delta, side):
    """The Gram of the interleaved-order pivots of J = Cov(S^n, Yh^n).

    side='Y' -> the RECORD pivots (v_t, v_t^S, sigma_t): cell t is
    predicted from S^{se(t)}, Yh^{t-1}.  side='S' -> the reference
    pivots.  The two Grams sum to J^{-1} (Cholesky decomposition of the
    inverse along the interleaved total order) -- gated in sK.
    Theorem K reads V Sig_s^{-1} V'   = pivot_gram(...,'Y')[n:, n:]
    and              V Sig_s^{-1} V_S' = -pivot_gram(...,'Y')[n:, :n].
    """
    n = M.n
    J = np.block([[M.Cs, M.K @ H.T], [(M.K @ H.T).T, Gam]])
    se = np.minimum(np.arange(n) + Delta + 1, n)
    ks = kcounts(n, se)
    Gm = np.zeros((2 * n, 2 * n))
    for i in range(n):
        if side == "S":
            j = i
            cond = list(range(j)) + [n + k for k in range(ks[j])]
        else:
            j = n + i
            cond = list(range(se[i])) + [n + k for k in range(i)]
        cf = cho_factor(J[np.ix_(cond, cond)], lower=True,
                        check_finite=False)
        b = J[cond, j]
        w = cho_solve(cf, b, check_finite=False)
        s = float(J[j, j] - b @ w)
        u = np.zeros(2 * n)
        u[j] = 1.0
        u[cond] = -w
        Gm += np.outer(u, u) / s
    return Gm, J


def certify(n, Delta, Dt=D_TGT, maxit1=1500, maxit2=300, nbis=40,
            sec=None):
    """full-space cold-start Lagrangian polish + moment-box tangent LB.
    Deterministic: no warm start, no random restart, no seed.

    sec = None      -> the full family F0
    sec = ('sc', m) -> the SPLIT-CAUSAL linear section F0^sc(m)
                       (Definition: H[b1rows, idx2] = H[b1rows, idx1] Mmap),
                       a convex linear section, so the same machinery
                       certifies phi^sc two-sided."""
    M = Model(n)
    gDH, gDG = grad_dist(M)
    iu = np.triu_indices(n)
    symw = np.where(iu[0] == iu[1], 1.0, 2.0)
    proj = gproj = None
    if sec is not None:
        msec = sec[1]
        Mmap, i1, i2 = sc_map(n, msec)

        def proj(H):
            H = H.copy()
            H[np.ix_(range(msec), i2)] = H[np.ix_(range(msec), i1)] @ Mmap
            return H

        def gproj(gH):
            gH = gH.copy()
            g2 = gH[np.ix_(range(msec), i2)]
            gH[np.ix_(range(msec), i1)] += g2 @ Mmap.T
            gH[np.ix_(range(msec), i2)] = 0.0
            return gH

    def unpack(x):
        H = x[:2 * n * n].reshape(n, 2 * n)
        if proj is not None:
            H = proj(H)
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
            gh = gh + mu * gDH
            if gproj is not None:
                gh = gproj(gh)
            return (v + mu * (dist_HG(M, H, G) - Dt),
                    np.concatenate([gh.ravel(),
                                    ((gg + mu * gDG))[iu] * symw]))
        res = minimize(lagr, x0, jac=True, method="L-BFGS-B",
                       options={"maxiter": maxiter, "ftol": 1e-18,
                                "gtol": 1e-14, "maxcor": 40})
        H_, G_ = unpack(res.x)
        out = f_and_grad(M, H_, G_, Delta)
        if out is None:                      # blend back into the cone
            xr = res.x
            for _ in range(60):
                xr = 0.5 * (xr + x0ref)
                H_, G_ = unpack(xr)
                out = f_and_grad(M, H_, G_, Delta)
                if out is not None:
                    break
            if out is None:
                raise np.linalg.LinAlgError("outside the cone")
            res.x = xr
        v_, gh_, gg_ = out
        return res.x, v_, dist_HG(M, H_, G_), gh_, gg_

    H0, G0 = moments(M, 0.7 * np.eye(n), np.zeros((n, n)),
                     0.21 * np.eye(n))
    x0ref = np.concatenate([H0.ravel(), G0[iu]])
    x = x0ref.copy()
    lo, hi = 0.0, 4.0
    x, v_, d_, gh_, gg_ = solve(hi, x, maxit1)
    while d_ > Dt:
        hi *= 2.0
        x, v_, d_, gh_, gg_ = solve(hi, x, maxit2)
    mu = hi
    for _ in range(nbis):
        mu = 0.5 * (lo + hi)
        x, v_, d_, gh_, gg_ = solve(mu, x, maxit2)
        if d_ > Dt:
            lo = mu
        else:
            hi = mu
        if abs(d_ - Dt) < 1e-11:
            break
    x, v_, d_, gh_, gg_ = solve(mu, x, maxit1)
    ghL = gh_ + mu * gDH
    if gproj is not None:
        ghL = gproj(ghL)
    rn = float(np.sqrt(np.sum(ghL ** 2) + np.sum((gg_ + mu * gDG) ** 2)))
    H_, G_ = unpack(x)
    bG = (1.0 + np.sqrt(n * Dt)) ** 2
    Rbox = float(np.sqrt(np.sum((np.sqrt(bG) + np.abs(H_)) ** 2)
                         + np.sum((bG + np.abs(G_)) ** 2)))
    LB = (v_ + mu * (d_ - Dt)) - rn * Rbox
    if d_ > Dt:                          # feasible projection of the UB
        Hid, Gid = moments(M, np.eye(n), np.zeros((n, n)),
                           1e-6 * np.eye(n))
        if proj is not None:
            Hid = proj(Hid)
        d0 = dist_HG(M, Hid, Gid)
        tt = (Dt - d0) / (d_ - d0)
        H_, G_ = Hid + tt * (H_ - Hid), Gid + tt * (G_ - Gid)
        UB = f_and_grad(M, H_, G_, Delta)[0]
        d_ = dist_HG(M, H_, G_)
    else:
        UB = v_
    return {"LB": LB, "UB": UB, "width": UB - LB, "rnorm": rn, "mu": mu,
            "dist_minus_D": d_ - Dt, "H": H_, "G": G_, "M": M}


# ===================== pinned record battery ============================
rngi = np.random.default_rng(20260806)   # pinned: draws are identical


def rand_rec(n, style):
    """pinned generic F0 record styles (the prover's battery)."""
    if style == 0:
        Ay = 0.7 * np.eye(n) + 0.15 * rngi.normal(size=(n, n)) / np.sqrt(n)
        Av = 0.15 * rngi.normal(size=(n, n)) / np.sqrt(n)
        B = 0.3 * rngi.normal(size=(n, n)) / np.sqrt(n)
        Nc = B @ B.T + 0.10 * np.eye(n)
    elif style == 1:
        Ay = 0.5 * np.eye(n) + 0.35 * rngi.normal(size=(n, n)) / np.sqrt(n)
        Av = 0.35 * rngi.normal(size=(n, n)) / np.sqrt(n)
        B = 0.5 * rngi.normal(size=(n, n)) / np.sqrt(n)
        Nc = B @ B.T + 0.05 * np.eye(n)
    else:
        Ay = 0.85 * np.eye(n) + 0.05 * rngi.normal(size=(n, n)) / np.sqrt(n)
        Av = 0.20 * rngi.normal(size=(n, n)) / np.sqrt(n)
        B = 0.15 * rngi.normal(size=(n, n)) / np.sqrt(n)
        Nc = B @ B.T + 0.02 * np.eye(n)
    return Av, Ay, Nc


def adv_record(n, m, bcoef, varz, eps1, copies, kind):
    """PINNED, analytic, D-feasible F0 counterexample (the 080 s4 class):
    block-1 rows spent on (near-)exact copies of block-2 cells."""
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
    return Av, Ay, Nc


N16, M8 = 16, 8
GEN = [rand_rec(N16, s) for s in (0, 1, 2)]              # generic F0
SCR = [split_project(N16, M8, *R) for R in GEN]          # split-causal
ADV = {"two_V_copies": adv_record(N16, M8, 0.50, 0.02, 0.001,
                                  [(6, 9), (7, 8)], "V"),
       "three_Y_copies": adv_record(N16, M8, 0.0, 0.001, 0.001,
                                    [(5, 10), (6, 9), (7, 8)], "Y")}
BATTERY = ([(f"generic{s}", D, GEN[s]) for s in range(3)
            for D in (0, 1, 2)]
           + [(f"splitcausal{s}", D, SCR[s]) for s in range(3)
              for D in (0, 1, 2)]
           + [(k, D, ADV[k]) for k in ADV for D in (0, 2)])


def diag_of(n, m, Delta, Av, Ay, Nc):
    """every quantity of the lemma chain, independent slogdet route."""
    S4 = joint_cov(n, Av, Ay, Nc)
    b1, b2, E = blocks_idx(n, m)
    D1, D2 = deficits(S4, n, m, Delta)
    X = cross_read(S4, n, m)
    IET = cmi_bits(S4, E, b2, [])
    SY = list(range(2 * n + m, 3 * n)) + list(range(3 * n + m, 4 * n))
    IETc = cmi_bits(S4, E, b2, SY)
    sj_all = sum_j_terms(S4, n, m, Delta)
    sj_first = sum_j_terms(S4, n, m, Delta, first_only=True)
    m2 = n - m
    joint1 = cmi_bits(S4, E, list(range(2 * n + m,
                                        2 * n + m + min(Delta + 1, m2))),
                      [])
    Ep = list(range(2 * n + m, 2 * n + m + Delta))
    IEpE = cmi_bits(S4, Ep, E, []) if Delta > 0 else 0.0
    Im = imi_SS(m, Delta)
    cc = const_c(m, Delta)
    fac = 2.0 - (1.0 if Delta == 0 else 0.0)
    return {"D1": D1, "D2": D2, "X": X, "I_E_Tb2": IET, "I_Ep_E": IEpE,
            "I_m": Im, "c": cc, "dist": dist_of(n, Av, Ay, Nc)[0],
            "L2_slack": KAPPA + X - IET,
            "L2b_slack": (KAPPA + X - IEpE) if Delta > 0 else float("inf"),
            "L3_identity_res": D2 - (IET - IETc - sj_all),
            "L3_collapse_res": sj_first - joint1,
            "L3_joint_minus_Im": joint1 - Im,
            "L3_slack": (IET - Im) - D2,
            "L4_slack": (IEpE - D1) if Delta > 0 else -D1,
            "H_slack": cc + fac * X - (D1 + D2)}


# ------------------------------------------------------------------ s1
print("[s1] L1: I(T^b1;T^b2) = kappa exactly, m-independent ...",
      flush=True)
BAR_S1 = 1e-12
s1 = {}
for m in (3, 4, 6, 8, 12, 16):
    n = 2 * m
    S = joint_cov(n, np.zeros((n, n)), np.zeros((n, n)), np.eye(n))
    b1, b2, _ = blocks_idx(n, m)
    s1[str(m)] = cmi_bits(S, b1, b2, [])
res1 = max(abs(v - KAPPA) for v in s1.values())
spread1 = max(s1.values()) - min(s1.values())
vals["s1"] = {"I_by_m": s1, "kappa": KAPPA, "max_dev": res1,
              "m_spread": spread1, "bar": BAR_S1}
verdicts["s1_L1_identity"] = res1 < BAR_S1
verdicts["s1_L1_m_independent"] = spread1 < BAR_S1
print(f"  kappa = {KAPPA:.13f}; max |I(T^b1;T^b2) - kappa| over "
      f"m in {{3,4,6,8,12,16}} = {res1:.2e} < {BAR_S1:.0e}; spread over m "
      f"= {spread1:.2e} [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s2/s3
print("[s2/s3] L2 (cross-read bound + tightness), L3, L4 and the "
      "H-repair inequality on the pinned battery ...", flush=True)
BAR_ZERO = -1e-9          # "zero violations" tolerance on the slacks
BAR_TIGHT = 1e-5          # tightness of L2 at the adversarial witness
BAR_L3ID = 1e-9           # L3 identity residual
BAR_HSLACK = 0.1          # min slack of the H-repair inequality
DG = {}
for (tag, Delta, R) in BATTERY:
    DG[(tag, Delta)] = diag_of(N16, M8, Delta, *R)
rows = [dict(tag=k[0], Delta=k[1], **{q: v[q] for q in
             ("D1", "D2", "X", "I_E_Tb2", "I_Ep_E", "c", "dist",
              "L2_slack", "L2b_slack", "L3_identity_res",
              "L3_collapse_res", "L3_joint_minus_Im", "L3_slack",
              "L4_slack", "H_slack")})
        for k, v in DG.items()]
min_L2 = min(r["L2_slack"] for r in rows)
min_L2b = min(r["L2b_slack"] for r in rows if np.isfinite(r["L2b_slack"]))
adv_slacks = {k: DG[(k, 0)]["L2_slack"] for k in ADV}
tight_witness = min(adv_slacks, key=adv_slacks.get)
tight_slack = adv_slacks[tight_witness]
max_L3id = max(abs(r["L3_identity_res"]) for r in rows)
max_L3col = max(abs(r["L3_collapse_res"]) for r in rows)
min_L3joint = min(r["L3_joint_minus_Im"] for r in rows)
min_L3 = min(r["L3_slack"] for r in rows)
min_L4 = min(r["L4_slack"] for r in rows)
max_D1_D0 = max(abs(r["D1"]) for r in rows if r["Delta"] == 0)
min_H = min(r["H_slack"] for r in rows)
advX_err = {k: abs(DG[(k, 0)]["X"] - REC_ADV_X[k]) for k in ADV}
advD2 = {k: DG[(k, 0)]["D2"] for k in ADV}
advLa = {k: la_bits(N16, *ADV[k], 0) for k in ADV}
advD = {k: DG[(k, 0)]["dist"] for k in ADV}
vals["s2"] = {"cells": len(rows), "min_L2_slack": min_L2,
              "min_L2b_slack": min_L2b, "adv_L2_slacks": adv_slacks,
              "tight_witness": tight_witness, "tight_slack": tight_slack,
              "adv_X": {k: DG[(k, 0)]["X"] for k in ADV},
              "adv_X_repro_err": advX_err, "adv_D2": advD2,
              "adv_La": advLa, "adv_dist": advD,
              "bars": {"zero_violation": BAR_ZERO, "tight": BAR_TIGHT}}
vals["s3"] = {"max_L3_identity_res": max_L3id,
              "max_L3_collapse_res": max_L3col,
              "min_L3_joint_minus_Im": min_L3joint,
              "min_L3_slack": min_L3, "min_L4_slack": min_L4,
              "max_D1_at_Delta0": max_D1_D0, "min_H_slack": min_H,
              "bars": {"identity": BAR_L3ID, "H_slack": BAR_HSLACK}}
vals["battery_rows"] = rows
verdicts["s2_L2_no_violation"] = (min_L2 > BAR_ZERO
                                  and min_L2b > BAR_ZERO)
verdicts["s2_L2_tight_at_witness"] = (BAR_ZERO < tight_slack < BAR_TIGHT)
verdicts["s2_adv_X_reproduced"] = all(v < 1e-6 for v in advX_err.values())
verdicts["s3_L3_identity"] = (max_L3id < BAR_L3ID
                              and max_L3col < BAR_L3ID)
verdicts["s3_L3_bound"] = (min_L3joint > -1e-12 and min_L3 > BAR_ZERO)
verdicts["s3_L4_bound"] = (min_L4 > BAR_ZERO and max_D1_D0 < 1e-12)
verdicts["s3_H_repair_inequality"] = (min_H > BAR_HSLACK)
print(f"  {len(rows)} battery cells (3 generic x 3 Delta, 3 split-causal "
      f"x 3 Delta, 2 adversarial x 2 Delta)", flush=True)
print(f"  L2  min slack (kappa + X - I(E;T^b2)) = {min_L2:+.3e} "
      f"(>= 0); second leg I(E';E): {min_L2b:+.3e}", flush=True)
print(f"  L2  TIGHT at the {tight_witness} witness (X = "
      f"{DG[(tight_witness,0)]['X']:.4f} bits): slack {tight_slack:.3e} "
      f"< {BAR_TIGHT:.0e} -- sharp exactly where the universal claim "
      f"dies", flush=True)
for k in ADV:
    print(f"      {k}: dist {advD[k]:.4f} (feasible), D2 {advD2[k]:.4f}, "
          f"X {DG[(k,0)]['X']:.4f} (repro err {advX_err[k]:.1e}), "
          f"L_a {advLa[k]:.4f}", flush=True)
print(f"  L3  max identity residual {max_L3id:.2e} < {BAR_L3ID:.0e}; "
      f"chain-rule collapse {max_L3col:.2e}; min (joint - I_m) "
      f"{min_L3joint:+.3e}; min slack of D2 <= I(E;T^b2) - I_m "
      f"{min_L3:+.3e}", flush=True)
print(f"  L4  min slack of D1 <= I(E';E) {min_L4:+.3e}; max |D1| at "
      f"Delta=0 {max_D1_D0:.2e}", flush=True)
print(f"  H   D1 + D2 <= c(Delta;m) + (2 - 1{{Delta=0}}) X: zero "
      f"violations, min slack {min_H:.4f} > {BAR_HSLACK} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s4
print("[s4] the split-causal sub-family F0^sc(m): X = 0, (H*) as a "
      "theorem, and linearity of the section ...", flush=True)
BAR_SCX = 1e-12
BAR_SCH = 0.5
BAR_LIN = 1e-12
sc_rows = [r for r in rows if r["tag"].startswith("splitcausal")]
max_scX = max(abs(r["X"]) for r in sc_rows)
min_scH = min(r["c"] - (r["D1"] + r["D2"]) for r in sc_rows)
Mmap, idx1, idx2 = sc_map(N16, M8)
Msc = Model(N16)
HGs = [moments(Msc, R[1], R[0], R[2]) for R in SCR]
lin_res = []
mid_X = []
for i in range(len(HGs)):
    for j in range(i + 1, len(HGs)):
        Hm = 0.5 * (HGs[i][0] + HGs[j][0])
        Gm = 0.5 * (HGs[i][1] + HGs[j][1])
        r = np.max(np.abs(Hm[np.ix_(range(M8), idx2)]
                          - Hm[np.ix_(range(M8), idx1)] @ Mmap))
        lin_res.append(float(r))
        Ay, Av, Nc = rec_of(Msc, Hm, Gm)
        mid_X.append(abs(cross_read(joint_cov(N16, Av, Ay, Nc), N16, M8)))
vals["s4"] = {"max_abs_X": max_scX, "min_Hstar_slack": min_scH,
              "max_midpoint_linear_residual": max(lin_res),
              "max_midpoint_X": max(mid_X), "pairs": len(lin_res),
              "bars": {"X": BAR_SCX, "Hstar_slack": BAR_SCH,
                       "linear": BAR_LIN}}
verdicts["s4_X_vanishes"] = max_scX < BAR_SCX
verdicts["s4_Hstar_is_a_theorem"] = min_scH > BAR_SCH
verdicts["s4_section_is_linear"] = (max(lin_res) < BAR_LIN
                                    and max(mid_X) < BAR_SCX)
print(f"  X on projected records: max |X| = {max_scX:.2e} < "
      f"{BAR_SCX:.0e}; (H*) with the tex's own constants c(Delta;m): "
      f"min slack {min_scH:.4f} > {BAR_SCH}", flush=True)
print(f"  linearity: {len(lin_res)} moment midpoints stay split-causal, "
      f"max residual {max(lin_res):.2e}, max |X| {max(mid_X):.2e} "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s5
print("[s5] the Pi-retraction identities ...", flush=True)
BAR_PI_ID = 1e-14
BAR_PI_X = 1e-12
BAR_PI_GAIN = -0.05
pi_dist, pi_law, pi_X, pi_price = 0.0, 0.0, 0.0, []
for style in (0, 1, 2):
    for n in (12, 16, 20):
        m = n // 2
        Av, Ay, Nc = rand_rec(n, style)
        Avp, Ayp, Ncp = split_project(n, m, Av, Ay, Nc)
        pi_dist = max(pi_dist, abs(dist_of(n, Av, Ay, Nc)[0]
                                   - dist_of(n, Avp, Ayp, Ncp)[0]))
        Sa, Sb = joint_cov(n, Av, Ay, Nc), joint_cov(n, Avp, Ayp, Ncp)
        ib = (list(range(0, m)) + list(range(n, n + m))
              + list(range(2 * n, 2 * n + m))
              + list(range(3 * n, 3 * n + m)))
        pi_law = max(pi_law, float(np.max(np.abs(Sa[np.ix_(ib, ib)]
                                                 - Sb[np.ix_(ib, ib)]))))
        pi_X = max(pi_X, abs(cross_read(Sb, n, m)))
        for Delta in (0, 2):
            pi_price.append(n * (la_bits(n, Avp, Ayp, Ncp, Delta)
                                 - la_bits(n, Av, Ay, Nc, Delta)))
vals["s5"] = {"max_dist_dev": pi_dist, "max_block1_law_dev": pi_law,
              "max_abs_X": pi_X, "price_min": min(pi_price),
              "price_max": max(pi_price), "records": len(pi_price),
              "bars": {"identity": BAR_PI_ID, "X": BAR_PI_X,
                       "gain": BAR_PI_GAIN}}
verdicts["s5_pi_preserves_distortion"] = pi_dist < BAR_PI_ID
verdicts["s5_pi_preserves_block1_law"] = pi_law < BAR_PI_ID
verdicts["s5_pi_kills_X"] = pi_X < BAR_PI_X
verdicts["s5_pi_improves_generic"] = max(pi_price) < BAR_PI_GAIN
print(f"  distortion preserved to {pi_dist:.2e}, block-1 joint law to "
      f"{pi_law:.2e} (bar {BAR_PI_ID:.0e}); |X(Pi R)| <= {pi_X:.2e}",
      flush=True)
print(f"  n*(L_a(Pi R) - L_a(R)) over {len(pi_price)} generic cells: "
      f"[{min(pi_price):+.4f}, {max(pi_price):+.4f}] bits -- Pi STRICTLY "
      f"IMPROVES every generic record [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s6/s8
print("[s6/s8] shared cold-start optimizers at Delta = 0, "
      "n in {16,24,32,48} ...", flush=True)
OPT = {}
OPTREC = {}
OPTC = {}
for n in (16, 24, 32, 48):
    c = certify(n, 0)
    OPTC[(n, 0)] = c
    Ay, Av, Nc = rec_of(c["M"], c["H"], c["G"])
    OPTREC[n] = (Av, Ay, Nc)
    d = diag_of(n, n // 2, 0, Av, Ay, Nc)
    _, per = dist_of(n, Av, Ay, Nc)
    Avp, Ayp, Ncp = split_project(n, n // 2, Av, Ay, Nc)
    price = n * (la_bits(n, Avp, Ayp, Ncp, 0) - la_bits(n, Av, Ay, Nc, 0))
    OPT[n] = {"UB": c["UB"], "LB": c["LB"], "width": c["width"],
              "mu": c["mu"], "dist_minus_D": c["dist_minus_D"],
              "d1": float(per[:n // 2].mean()),
              "d2": float(per[n // 2:].mean()),
              "dmean": float(per.mean()), "price": price,
              "La": la_bits(n, Av, Ay, Nc, 0), **d}
    print(f"  n={n} (m={n//2}): phi_UB {c['UB']:.10f} (recorded "
          f"{REC_TABLE[n//2]['phi']:.10f}, err "
          f"{abs(c['UB']-REC_TABLE[n//2]['phi']):.1e}); D1+D2 "
          f"{d['D1']+d['D2']:.7f}; I(E;T^b2) {d['I_E_Tb2']:.7f}; X "
          f"{d['X']:.7e} [{time.time()-t0:.0f}s]", flush=True)
# cross-block kernel norms at the (16,0) optimizer (reported, ungated)
Av16, Ay16, _ = OPTREC[N16]
A16 = np.hstack([Av16, Ay16])
a11 = float(np.linalg.norm(A16[np.ix_(range(M8), idx1)]))
a12 = float(np.linalg.norm(A16[np.ix_(range(M8), idx2)]))
vals["A12_over_A11"] = a12 / a11
vals["A12_fro"] = a12
vals["A11_fro"] = a11

# ------------------------------------------------------------------ sK
print("[sK] Theorem K: the KKT system splits by column block "
      "(K1 Ay = theta N; K2 N^-1 = theta I + V Sig_s^-1 V'; "
      "K3 Av = -N V Sig_s^-1 V_S') ...", flush=True)
BAR_K = 1e-6           # generous vs the observed ~3e-8 polish residual
BAR_KSTRUCT = 1e-12    # the two exact structural facts
BAR_KSYM = 1e-6
for (n, Dl) in ((16, 1), (16, 2)):
    OPTC[(n, Dl)] = certify(n, Dl)
kres = {}
k_ok = True
struct = 0.0
for key in sorted(OPTC, key=lambda kk: (kk[1], kk[0])):
    n, Dl = key
    c = OPTC[key]
    Mk, H, G, mu = c["M"], c["H"], c["G"], c["mu"]
    th = 2.0 * mu * LN2
    A = H @ Mk.SigWinv
    Av_, Ay_ = A[:, :n], A[:, n:]
    N = G - H @ Mk.P @ H.T
    N = 0.5 * (N + N.T)
    Ni = np.linalg.inv(N)
    GY, J = pivot_gram(Mk, H, G, Dl, "Y")
    GS, _ = pivot_gram(Mk, H, G, Dl, "S")
    Ji = np.linalg.inv(J)
    struct = max(struct,
                 float(np.abs(Mk.K - np.hstack([np.eye(n),
                                                np.zeros((n, n))])).max()),
                 float(np.abs(Mk.SigWinv @ Mk.CovWY
                              - np.vstack([np.zeros((n, n)),
                                           np.eye(n)])).max()))
    chol = float(np.linalg.norm(GS + GY - Ji) / np.linalg.norm(Ji))
    r1 = float(np.linalg.norm(Ay_ - th * N) / np.linalg.norm(Ay_))
    r2 = float(np.linalg.norm(Ni - (th * np.eye(n) + GY[n:, n:]))
               / np.linalg.norm(Ni))
    r3 = float(np.linalg.norm(Av_ + N @ GY[n:, :n])
               / np.linalg.norm(Av_))
    sym = float(np.linalg.norm(Ay_ - Ay_.T) / np.linalg.norm(Ay_))
    eN = np.linalg.eigvalsh(N)
    eA = np.linalg.eigvalsh(Ay_)
    ok = (r1 < BAR_K and r2 < BAR_K and r3 < BAR_K and sym < BAR_KSYM
          and chol < BAR_KSTRUCT and eN[0] > 0.0
          and eN[-1] <= 1.0 / th + 1e-9 and eA[0] > 0.0
          and eA[-1] <= 1.0 + 1e-9 and th >= THETA_FLOOR)
    k_ok = k_ok and ok
    kres[f"{n}_{Dl}"] = {"theta": th, "K1": r1, "K2": r2, "K3": r3,
                         "Ay_sym": sym, "chol_split": chol,
                         "lmin_N": float(eN[0]), "lmax_N": float(eN[-1]),
                         "inv_theta": 1.0 / th, "lmin_Ay": float(eA[0]),
                         "lmax_Ay": float(eA[-1]), "ok": bool(ok)}
    print(f"  (n={n},D={Dl}): theta {th:.6f} >= {THETA_FLOOR}; K1 "
          f"{r1:.2e} K2 {r2:.2e} K3 {r3:.2e} (bar {BAR_K:.0e}); Ay "
          f"transpose-symmetry {sym:.2e}; 0 < lmin(N) {eN[0]:.6f}, "
          f"lmax(N) {eN[-1]:.6f} <= 1/theta {1/th:.6f}; Ay in "
          f"({eA[0]:.4f}, {eA[-1]:.4f}] <= I [{time.time()-t0:.0f}s]",
          flush=True)
vals["sK"] = {"cells": kres, "struct_max_dev": struct,
              "lmin_N_min": min(v["lmin_N"] for v in kres.values()),
              "bars": {"identity": BAR_K, "structural": BAR_KSTRUCT,
                       "symmetry": BAR_KSYM, "theta_floor": THETA_FLOOR}}
verdicts["sK_structural_facts"] = struct < BAR_KSTRUCT
verdicts["sK_identities"] = bool(k_ok)
print(f"  structural facts K = [I,0] and SigW^-1 SigWY = [0;I] to "
      f"{struct:.2e}; min lmin(N) over the six optimizers "
      f"{min(v['lmin_N'] for v in kres.values()):.6f} (the (F) quantity, "
      f"reported not gated) [{time.time()-t0:.0f}s]", flush=True)

print("[s6] T*(ii) hygiene: block distortions straddle D, and the "
      "value function D -> phi_8(D) is convex ...", flush=True)
BAR_STRADDLE = 1e-4
BAR_D_REPRO = 1e-5
BAR_CVX = 5e-4
str_ok = True
str_rows = {}
for n in (16, 24, 32):
    d1, d2, dm = OPT[n]["d1"], OPT[n]["d2"], OPT[n]["dmean"]
    r1, r2, mu = REC_BLOCKD[n]
    ok = (d1 < D_TGT - BAR_STRADDLE and d2 > D_TGT + BAR_STRADDLE
          and abs(dm - D_TGT) < 1e-6 and abs(d1 - r1) < BAR_D_REPRO
          and abs(d2 - r2) < BAR_D_REPRO)
    str_ok = str_ok and ok
    str_rows[str(n)] = {"d1": d1, "d2": d2, "mean": dm, "mu": OPT[n]["mu"],
                        "D_minus_d1": D_TGT - d1, "d2_minus_D": d2 - D_TGT,
                        "repro_err": max(abs(d1 - r1), abs(d2 - r2)),
                        "recorded": [r1, r2, mu], "ok": bool(ok)}
    print(f"  n={n}: d1 = {d1:.9f} < D = 0.3 < d2 = {d2:.9f} (mean "
          f"{dm:.9f}); straddle {min(D_TGT-d1, d2-D_TGT):.2e} > "
          f"{BAR_STRADDLE:.0e}; repro err "
          f"{max(abs(d1-r1), abs(d2-r2)):.1e}; mu = {OPT[n]['mu']:.4f}",
          flush=True)
DGRID = [0.26, 0.28, 0.30, 0.32, 0.34]
phiD = {}
for Dv in DGRID:
    c = certify(8, 0, Dt=Dv)
    phiD[f"{Dv:.2f}"] = {"LB": c["LB"], "UB": c["UB"],
                         "width": c["width"]}
    print(f"  phi_8(D={Dv:.2f}) in [{c['LB']:.9f}, {c['UB']:.9f}] "
          f"[{time.time()-t0:.0f}s]", flush=True)
cvx_slack = []
for i in range(1, len(DGRID) - 1):
    lo, mid, hi = (f"{DGRID[i-1]:.2f}", f"{DGRID[i]:.2f}",
                   f"{DGRID[i+1]:.2f}")
    chord = 0.5 * (phiD[lo]["LB"] + phiD[hi]["LB"])
    cvx_slack.append(chord - phiD[mid]["UB"])
    print(f"  convexity at D={mid}: chord of certified LBs {chord:.9f} "
          f">= certified UB {phiD[mid]['UB']:.9f}, slack "
          f"{chord - phiD[mid]['UB']:+.3e}", flush=True)
mu16 = OPT[16]["mu"]
cost_ignored = 8.0 * mu16 * (OPT[16]["d2"] - D_TGT)
vals["s6"] = {"straddle": str_rows, "phi8_of_D": phiD,
              "convexity_slack": cvx_slack,
              "cost_of_ignoring_bits": cost_ignored,
              "bars": {"straddle": BAR_STRADDLE, "repro": BAR_D_REPRO,
                       "convexity": BAR_CVX}}
verdicts["s6_blocks_straddle_D"] = bool(str_ok)
verdicts["s6_value_function_convex"] = all(s > BAR_CVX for s in cvx_slack)
print(f"  min convexity slack {min(cvx_slack):.3e} > {BAR_CVX:.0e}; "
      f"ignoring the straddle would have cost m mu (d2 - D) = "
      f"{cost_ignored:.4f} bits [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s7
print("[s7] constants + the recomputed corollary arithmetic ...",
      flush=True)
BAR_CONST = 1e-6
BAR_MARGIN = 2.5e-3
BAR_SHORT24 = 1e-4
c0 = const_c(8, 0)
Xb = OPT[16]["X"]                    # X at the m = 8 (base) optimizer
cX = c0 + Xb
plateau = SEALED_LB32 - cX / 32.0
margin = plateau - SPEC0
ratio_tex = margin / TEXW32
ratio_sealed = margin / SEALED_W32
base24 = SEALED_LB24 - cX / 24.0
short24 = SPEC0 - base24
cDF = c0 + XBAR_DF                   # the (D) + (F) constant
plateauDF = SEALED_LB32 - cDF / 32.0
marginDF = plateauDF - SPEC0
short24DF = SPEC0 - (SEALED_LB24 - cDF / 24.0)
file_lb32 = None
if os.path.exists(CXJSON):
    with open(CXJSON) as fh:
        file_lb32 = json.load(fh)["vals"]["s5_32_0"]["LB"]
vals["s7"] = {"c0": c0, "X_base": Xb, "c_plus_X": cX,
              "c_plus_X_err": abs(cX - REC_CPLUSX),
              "plateau": plateau, "plateau_err": abs(plateau - REC_PLATEAU),
              "spec0": SPEC0, "margin": margin, "ratio_texwidth": ratio_tex,
              "ratio_sealedwidth": ratio_sealed, "base24": base24,
              "shortfall24": short24, "sealed_LB32_file": file_lb32,
              "sealed_LB32_const": SEALED_LB32,
              "Xbar_DF": XBAR_DF, "c_plus_Xbar_DF": cDF,
              "plateau_DF": plateauDF, "margin_DF": marginDF,
              "ratio_texwidth_DF": marginDF / TEXW32,
              "shortfall24_DF": short24DF,
              "bars": {"const": BAR_CONST, "margin": BAR_MARGIN,
                       "ratio": [200.0, 210.0], "short24": BAR_SHORT24,
                       "margin_DF": 1.0e-3, "short24_DF": 1.0e-3}}
verdicts["s7_c_plus_X"] = abs(cX - REC_CPLUSX) < BAR_CONST
verdicts["s7_plateau_under_DF"] = (plateauDF > SPEC0
                                   and marginDF > 1.0e-3
                                   and short24DF > 1.0e-3)
verdicts["s7_plateau"] = (abs(plateau - REC_PLATEAU) < BAR_CONST
                          and plateau > SPEC0 and margin > BAR_MARGIN
                          and 200.0 <= ratio_tex <= 210.0)
verdicts["s7_base24_fails"] = (base24 < SPEC0 and short24 > BAR_SHORT24)
verdicts["s7_sealed_LB32_matches"] = (
    file_lb32 is not None and abs(file_lb32 - SEALED_LB32) < 1e-15)
print(f"  c(0) = {c0:.10f}; X(m=8) = {Xb:.10f}; c(0) + X = {cX:.10f} "
      f"(= {REC_CPLUSX} to {abs(cX-REC_CPLUSX):.1e})", flush=True)
print(f"  L^inf(0) >= {SEALED_LB32:.10f} - {cX:.7f}/32 = {plateau:.7f} > "
      f"{SPEC0}: margin {margin:+.4e} = {ratio_tex:.0f}x the tex-v0.4 "
      f"width, {ratio_sealed:.0f}x the sealed width", flush=True)
print(f"  base-24 negative control: {base24:.7f} < {SPEC0} -- FAILS by "
      f"{short24:.2e} (> {BAR_SHORT24:.0e}); sealed LB(32,0) from "
      f"results/GO14-convexity.json {file_lb32} matches exactly",
      flush=True)
print(f"  under (D)+(F) instead of (H**): c(0) + Xbar = {cDF:.6f} -> "
      f"L^inf(0) >= {plateauDF:.7f} > {SPEC0}, margin {marginDF:+.4e} "
      f"({marginDF/TEXW32:.0f}x the tex-v0.4 width); base-24 control "
      f"fails by {short24DF:.3e} [{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s8
print("[s8] the monotone m-table at Delta = 0, m in {8,12,16,24} ...",
      flush=True)
BAR_STEP = 1e-6
BAR_TAB_REPRO = 1e-5
MS = [8, 12, 16, 24]
tab = {}
for m in MS:
    o = OPT[2 * m]
    tab[str(m)] = {"DD": o["D1"] + o["D2"], "IET": o["I_E_Tb2"],
                   "X": o["X"], "price": o["price"], "phi": o["UB"]}
repro = max(abs(tab[str(m)][q] - REC_TABLE[m][q])
            for m in MS for q in ("DD", "IET", "X", "price", "phi"))
steps = {}
mono_ok = True
for q in ("DD", "IET", "X"):
    st = [tab[str(MS[i])][q] - tab[str(MS[i + 1])][q]
          for i in range(len(MS) - 1)]
    steps[q] = st
    mono_ok = mono_ok and all(s >= BAR_STEP for s in st)
lim = {}
for q in ("DD", "IET", "X", "price"):
    v1, v2 = tab[str(MS[0])][q], tab[str(MS[-1])][q]
    lim[q] = (MS[-1] * v2 - MS[0] * v1) / (MS[-1] - MS[0])
vals["s8"] = {"table": tab, "steps": steps, "repro_max_err": repro,
              "limits_1_over_m": lim, "min_step": min(min(v) for v
                                                      in steps.values()),
              "bars": {"step": BAR_STEP, "repro": BAR_TAB_REPRO}}
verdicts["s8_table_reproduced"] = repro < BAR_TAB_REPRO
verdicts["s8_monotone_decreasing"] = bool(mono_ok)
print(f"    m   D1+D2      I(E;T^b2)   X            Pi-price", flush=True)
for m in MS:
    r = tab[str(m)]
    print(f"  {m:3d}  {r['DD']:.7f}  {r['IET']:.7f}  {r['X']:.7e}  "
          f"{r['price']:.7f}", flush=True)
print(f"  every quantity strictly decreasing in m (min step "
      f"{min(min(v) for v in steps.values()):.2e} >= {BAR_STEP:.0e}); "
      f"max reproduction error vs the committed prover values "
      f"{repro:.2e} < {BAR_TAB_REPRO:.0e}", flush=True)
print(f"  two-point 1/m limits: X_inf ~ {lim['X']:.4e}, (D1+D2)_inf ~ "
      f"{lim['DD']:.6f}, I(E;T^b2)_inf ~ {lim['IET']:.5f}; "
      f"||A12||_F/||A11||_F = {100*vals['A12_over_A11']:.2f}% "
      f"[{time.time()-t0:.0f}s]", flush=True)

# ------------------------------------------------------------------ s9
print("[s9] phi^sc_{2m} <= phi_m (unconditional) and the (H***) "
      "split-causality value gap p_n = n (phi^sc_n - phi_n) ...",
      flush=True)
BAR_SC_SLACK = 5e-4
BAR_P_REPRO = 1e-5
PBAR_ADMISSIBLE = 32.0 * (SEALED_LB32 - SPEC0) - c0     # = 0.1169299
PHI_HALF = {8: {"LB": phiD["0.30"]["LB"], "UB": phiD["0.30"]["UB"]}}
c12 = certify(12, 0)
PHI_HALF[12] = {"LB": c12["LB"], "UB": c12["UB"]}
PHI_HALF[16] = {"LB": OPT[16]["LB"], "UB": OPT[16]["UB"]}
s9 = {}
s9_ok = True
p_ok = True
for n in (16, 24, 32):
    m = n // 2
    cs = certify(n, 0, sec=("sc", m))
    slack = PHI_HALF[m]["LB"] - cs["UB"]
    p_cert = n * (cs["UB"] - OPT[n]["LB"])
    p_ub = n * (cs["UB"] - OPT[n]["UB"])
    err = abs(p_cert - REC_P[n])
    ok = (slack > BAR_SC_SLACK and err < BAR_P_REPRO
          and p_cert < PBAR_ADMISSIBLE)
    s9_ok = s9_ok and (slack > BAR_SC_SLACK)
    p_ok = p_ok and (err < BAR_P_REPRO and p_cert < PBAR_ADMISSIBLE)
    s9[str(n)] = {"phi_sc_LB": cs["LB"], "phi_sc_UB": cs["UB"],
                  "phi_half_LB": PHI_HALF[m]["LB"],
                  "slack_phisc_le_phihalf": slack,
                  "p_certified": p_cert, "p_point": p_ub,
                  "p_recorded": REC_P[n], "p_err": err,
                  "phi_sc_repro_err": abs(cs["UB"] - REC_PHISC[n]),
                  "headroom_x": PBAR_ADMISSIBLE / p_cert, "ok": bool(ok)}
    print(f"  n={n} (m={m}): phi^sc_{n} <= {cs['UB']:.10f} < "
          f"phi_{m} >= {PHI_HALF[m]['LB']:.10f} (certified slack "
          f"{slack:+.3e} > {BAR_SC_SLACK:.0e}); p_{n} = {p_cert:.7f} "
          f"(recorded {REC_P[n]:.7f}, err {err:.1e}), {PBAR_ADMISSIBLE/p_cert:.1f}x "
          f"inside the admissible {PBAR_ADMISSIBLE:.6f} "
          f"[{time.time()-t0:.0f}s]", flush=True)
vals["s9"] = {"rows": s9, "pbar_admissible": PBAR_ADMISSIBLE,
              "p_max": max(v["p_certified"] for v in s9.values()),
              "bars": {"slack": BAR_SC_SLACK, "p_repro": BAR_P_REPRO}}
verdicts["s9_phisc_2m_le_phi_m"] = bool(s9_ok)
verdicts["s9_p_values"] = bool(p_ok)
p_flat = "/".join("%.6f" % s9[str(n)]["p_certified"] for n in (16, 24, 32))
p_max = max(v["p_certified"] for v in s9.values())
print(f"  the split-causality value gap is FLAT in n ({p_flat}) and "
      f"stays {PBAR_ADMISSIBLE/p_max:.0f}x inside the (H***) bar "
      f"pbar < {PBAR_ADMISSIBLE:.6f} [{time.time()-t0:.0f}s]", flush=True)

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


out = {"verdict": verdicts, "GO14HR_supported": allpass, "vals": vals,
       "runtime_s": round(time.time() - t0, 1)}
print("===GO14HR-JSON===")
print(json.dumps(out, indent=1, default=jsafe))
print("===END===")
sys.exit(0 if allpass else 1)
