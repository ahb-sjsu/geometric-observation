# GO-14 probe record (2026-08-05, pre-registration numerics)

Definitional fork SETTLED at probe level (full report in session task
output; code in scratchpad probe_go14/):

- ADOPT definition (a): L_Delta = (1/n) sum_t I(T^n; Yhat_t |
  S^{t+Delta}, Yhat^{t-1}) -- the Delta-lagged causally-conditioned
  CMI. EXACT chain rule (residual 3e-12): n L_a = I(T^n;Yhat^n|S^n)
  + C_Delta, C_Delta >= 0 the smoothing-leakage charge
  sum_t I(Yhat_t; S_{>t+Delta} | past), = 0 iff the record is
  Delta-lag causally simulatable from S; decay pole identified:
  lambda_s = a(1-K), K the steady Kalman gain (ratio 7.95/lag
  measured = lambda_s^{-2}).
- REJECT definition (b) (memoryless eraser): monotone but floors
  0.0136 bits above the netted block coordinate (wrong
  Delta->infinity invariant; chain-rule-inconsistent).
- Interpolation conjecture SURVIVES: min L_a strictly inside
  (path 0.5350, slice 0.6219/0.7879/0.8490) at Delta = 0/2/5, D=0.3,
  n=16; strict monotonicity PROVABLE (per-term identity), lower
  margin collapses like lambda_s^{2 Delta}.
- Bookkeeping candidate REFUTED: fixed-lag static quadratic misses by
  a gap converging to the spectral gain 0.0263 bits -- record memory
  + cross-cell code structure carry real value.
- First-theorem draft (for the R-IND-5 + seal loop): the chain-rule
  identity + iff-condition + strict sandwich + geometric convergence
  at rate (a(1-K))^{2 Delta}; corollary: L_a is NOT the fixed-lag
  bookkeeping value, deficit -> spectral gain.
- Caveats on record: stationary-symmetric record class only (local
  certificates); finite-n drift quantified (n=8/16/24); Var(Y)=1
  normalization validated against the netted g* endpoint (1e-6), not
  assumed; Delta=5 strictness 2.7e-6 quoted as "strict,
  O(lambda_s^{2 Delta})", never as a numeric margin.

Next loop (when picked up): R-IND-5 verifier on the identity +
sandwich; GO-14 tex v0.2; seal GO-P-2026-076 (ID after 075); pilot;
governed. Novelty sweep owed for the causally-conditioned-CMI
framing (Kramer/Lev-Khina line mapped in GO-12 novelty record).

## R-IND-5 pass 1 (2026-08-05): PASS conditional -- sharpenings on record

Identity/sandwich/monotonicity/pole/bookkeeping all survive
adversarial re-derivation (identity residual 1.1e-14; all 20+ probe
numbers reproduced to every quoted digit; independence premise and
per-term identity verified, not assumed). MANDATORY restatements
before the 076 seal:
1. (ii) REFUTED AS WORDED -- counterexamples: N-only records (Yhat
   built from N = Y - rho V) collapse EXACTLY while carrying 1.43
   bits; a feasible boundary-V record collapses at Delta=6, n=16,
   D=0.3. Correct statement: for tau2>0, D < rho^2(n-Delta-1)/n, and
   Delta <= n-2, every D-feasible collapsing record must be V-free on
   cells t <= n-Delta-1, which the budget forbids; strictness of
   min L_a > block routes through block-optimality + C_Delta > 0 at
   the (unique per-mode) block optimizer, NOT through universal
   non-collapse.
2. Quoted minima are CLASS-CONDITIONAL (stationary-symmetric/diagonal
   records, local certificates) -- state in the theorem, pending the
   full-space search closure.
3. Spectral-gain constant is n-PINNED: 0.0213/0.0263/0.0280 at
   n=8/16/24, -> ~0.0313 at infinity (block(inf) = 0.52991 by
   frequency waterfilling); state gap_n -> static(q_path) - block_n.
4. Pole wording: per-lag ratio -> lambda_s^{-2} = 7.955 WITH the
   (n-Delta)/(n-Delta-1) finite-window prefactor (measured 5.51->9.18
   through Delta=0..8 at n=16); sandwich and monotonicity restricted
   to Delta <= n-2; block-opt leak (2.7e-6) vs min-L_a gap (2.37e-6)
   not to be conflated.
5. Tex v0.1 SIGN ERROR: the conjecture says "strictly increasing in
   Delta"; definition (a) gives strictly DECREASING. Fix at v0.2.
Two INCOMPLETE sub-checks (n=40 pole plateau; full-space non-diagonal
search) being closed by the resumed verifier before seal.
## R-IND-5 pass 1 closure (2026-08-05): both INCOMPLETE sub-checks done

(1) POLE CONFIRMED with structure: per-cell (interior t=12, n=32)
leak ratio -> lambda_s^{-2} = 7.955 within 0.3-1% at the tail;
aggregate ratio carries the (n-Delta-1)/(n-Delta-2) cell-count
prefactor (measured within 1.5% of prediction over Delta=6..11).
Wording fixed: never quote a constant measured ratio.

(2) DIAGONAL CLASS BEATEN for L_a: min L_a(0) <= 0.567353 <
0.572255 (improvement 4.9e-3 bits) via two independent non-diagonal
parameterizations agreeing to 8e-5, with a failed first-order
certificate at the diagonal optimum (directional derivative 8.6e-3
vs 1e-6 noise). Diagonal optimality REMAINS PROVEN for the block
coordinate; REFUTED for L_a. HARD REQUIREMENT for the 076 seal: all
quoted minima are diagonal-class upper bounds; the interpolation is
stated as block/n < min L_a(Delta) <= diag-class value; the
overstatement is bounded by min L_a - block per lag (<= 1.07e-3 at
Delta=2, <= 2.4e-6 at Delta=5). Verdict remains PASS under the
class-conditional phrasing; any seal presenting 0.572255 as THE
minimum must FAIL.

076 loop queued: tex v0.2 (five restatements + sign fix + true-min
bracketing), harness netting the identity/sandwich/pole-per-cell/
class-bracket, pilot, seal, governed.

## 076 loop CLOSED (2026-08-05): sealed a843fb7a, governed ALL PASS 12/12

Tex v0.2 shipped (all five restatements + the sign fix + the
class-conditional Remark as a hard term). Harness
experiments/go14_causal_erasure.py; pilot phase = THREE disclosed
runs (json bug; s4 gated at the wrong channel — the pole is
CELL-LOCAL, rwf shows its own stable ~3.93/lag ≈ lambda_s^2/rho^2
empirically, now scoped into the theorem and recorded ungated; s6's
closed-form per-frequency g* generalization exposed WRONG (0.656 vs
0.530) against the exact per-mode decomposition and replaced by
direct per-frequency Lagrangian minimization -> block_inf 0.52995 vs
verifier 0.52991). Governed seed 20261102: ALL PASS 12/12, identity
7.2e-12, UB(0) 0.572255 with the 2.4e-3 non-diagonal beat netted in
s5, pole relerr 1.7e-4, prefactor 8.0e-3, gap_inf 0.03131.
GO-14 now [predicted] in LEDGER/README. NEXT for GO-14: the novelty
sweep (OWED before any novelty language), then the open faces
(full-space min, process limit + innovations form, reset protocol,
rwf pole characterization).

## Novelty sweep (2026-08-05, arXiv-API only -- S2 429'd throughout, WebSearch budget exhausted): L_a + chain rule NOVEL conditional on four citations

Coordinate L_a(Delta) and the block+leakage chain rule with the
Kalman-pole characterization: NOT FOUND under any phrasing tried
(null set on record: causally-conditioned+erasure, delayed directed
information, smoothing leakage, sequential erasure, quantum state
smoothing+thermodynamic, chain rule+Landauer in our sense). MUST-CITE
adjacents wherever novelty is claimed: (i) Berta et al. 1609.06994/
1808.00135 (conditional erasure cost = CMI -- static conditioning);
(ii) Boyd-Mandal-Crutchfield 1708.03030 modularity dissipation +
1612.08616 retrodictive generators (smoothed-vs-causal has thermo
consequences); (iii) Venkat-Weissman-Carmon-Shamai 1302.2167
(Gaussian lookahead: the existing Delta-knob between filter and
smoother, estimation-theoretic, no erasure face); (iv) Sandberg et
al. 1402.1010 (Kalman-Bucy demon: Landauer against a FILTERED
reference -- no smoothing side, no lag coordinate). Related-work:
del Rio 1009.1630, Rosinberg et al. 1412.5138/1612.04945 (delayed
feedback), Asnani-Weissman 1105.5755, Naiss-Permuter 1012.5071.
RESIDUAL: hold headline novelty wording until the owed S2/DBLP pass
(non-arXiv venues unswept). Process-limit probe in flight.

## Process-limit probe (2026-08-05, diag-class, CPU): limit exists, closure law scoped, a new closed-form candidate survives

Cross-validated against every sealed 076 number first (block_16,
UB(0), excess(2), block_inf, chain-rule residual <= 3.6e-12).
(1) LIMIT EXISTS: clean O(1/n) (Richardson quad rms <= 3.5e-8,
calibrated on the block face to 1.4e-7): L_a^inf(Delta) =
0.568571/0.537401/0.531206/0.529977 (+/- <= 1.2e-5) at Delta=0/1/2/4;
excess over block_inf: 0.038621/0.007451/0.001256/2.75e-5.
(2) CLOSURE LAW SCOPED: per-lag ratios 5.18 -> 5.93 -> 6.87 rise
TOWARD lambda_s^-2 = 7.955 from below -- rate supported as a
Delta->infinity asymptotic, CONSTANT NOT IDENTIFIED through Delta=4
(genuine small-Delta record-reshaping transient; two-term ladder
fails; rwf pole excluded at 210% resid). Excess ~5:1 leak-dominated.
(3) NEW CANDIDATE SURVIVES -- causal-spectral allocation: equal-slope
per-frequency conditional quadratics with conditioning spectrum =
Delta-lag causal Wiener error spectrum S_e^(Delta) (min-phase
factorization 1.2e-14; reproduces block_inf to 1.6e-10 at two-sided;
own excess obeys lambda_s^{2Delta} cleanly, c_spec = 0.0190 +/-
0.0007). Also surviving: block_inf + c_static*lambda_s^{2Delta},
c_static = G*'(q_path)(P_f - P_s_inf) = 0.026668. REFUTED as
expressions of the min (above the diag UB at every Delta): slice,
static_filter, static_prefix(Delta) (misses by the spectral gain
0.0313 at Delta->inf, 0.0180 at Delta=0). Scalar fixed-lag law exact:
(P_s(Delta)-P_s_inf)/lambda_s^{2Delta} = P_f - P_s_inf to 6 digits.
(4) Per-cell stationarity PASS; the diag kernel is exactly
time-symmetric BY CLASS -- it cannot express causal asymmetry, which
is plausibly exactly why non-diagonal records beat it for L_a.
CONJECTURE v0.1 recorded in the probe report (session task output):
(i) limit exists O(1/n); (ii) innovations rate lambda_s^{2Delta}
scoped as asymptotic, c unclaimed; (iii) HEADLINE to net or refute:
L_a^inf = the causal-spectral allocation (consistent-with, not
demonstrated -- discrimination REQUIRES the full-space search, since
the diag class is structurally symmetric). NEXT NUMERICS before any
seal: full-space min at n=16-24, Delta=0..2 (does the non-diag
optimum approach the causal-spectral value?); diag Delta=5-6 at
n=32-40 to pin the diag constant. Then R-IND-5 -> tex fold ->
prereg 078.

## Full-space discrimination (2026-08-05): both closed forms UNSUPPORTED; constant pinned; the mechanism found

New exact interleaved-Cholesky L_a evaluator (agrees with sealed
harness to 1.9e-11; identity residual <= 3.6e-12 everywhere).
TRACK 1 (general (Ay, Av, B) records, n=16/24, Delta=0..2): GATE
PASS -- n=16 Delta=0 winner 0.5667581 beats the 076 verifier record
0.567353 by 5.9e-4; all basins (diag-embed, random tilt,
block-embed, cross-n Toeplitz) converge to the same value <= 1e-7,
status 0, distortion active. Process-limit (two-point 1/n,
calibrated <= 5e-6): L_fs^inf = 0.562725/0.536400/0.531049 at
Delta=0/1/2 -- plateaus +0.0148/+0.0041/+0.0008 ABOVE the
causal-spectral candidate (80-400x the extrapolation error) with the
WRONG shape (drifting rate, not the candidate's clean lambda law):
BOTH closed-form candidates (c_spec 0.019, c_static 0.0267) are too
small at every Delta -- the process rate is NOT single-letterized by
any tested causal-conditioning spectrum; the gap is genuine
cross-cell code value (winner cuts leakage 0.033->0.024 by paying
block penalty the per-frequency relaxations cannot express).
TRACK 2 (diag Delta=4/5/6, n=24..48, block-calibrated 1.3e-7):
E_inf = 2.661e-5/3.477e-6/4.210e-7; per-lag ratios
5.18->5.93->6.87->7.65+/-0.15->8.26+/-1.07 REACH lambda_s^-2=7.955
within error at Delta=5->6; c_diag = 0.111 +/- 0.006 (bracket
[0.105,0.125]); full-family c_fs in [0.09,0.125].
MECHANISM (the discovery): the full-space optimizer's Ay and noise
kernels are time-SYMMETRIC (<5e-5); ALL causal structure lives in
the V-coupling Av, whose kernel CHANGES SIGN EXACTLY AT LAG Delta --
horizon-matched V-cancellation: the record aligns V-content with the
span the eraser will hold and anti-correlates V beyond the access
horizon, suppressing smoothing leakage. Exactly what the
symmetric-by-class diag family cannot express (explains the 076
beat). Falsifiable per-cell at any n.
CONJECTURE v0.2 on record (session task output): (1) limit exists
O(1/n); (2) rate lambda_s^{2Delta} with c_diag = 0.111+/-0.006, c NOT
an available single-letter invariant; (3) the sign-boundary-at-Delta
mechanism clause, testable; (4) reproducible anchors: family min
L_a(0) <= 0.5667581 at n=16, diag ladder E_inf(4/5/6). Scope: family-
conditional (U-coupled records = open definitional question for
R-IND-5); equality-unsupported is an evidence verdict -- the natural
next theory face is a LOWER BOUND via the convexity-lemma machinery
on the interleaved-chol representation (sum of log-ratios of nested
Schur complements). NEXT LOOP: R-IND-5 on v0.2 -> tex v0.3 -> seal
prereg 078 -> governed.

## R-IND-5 pass on Conjecture v0.2 (2026-08-05): READY TO SEAL 078 conditional on SIX mandatory restatements

Independent verifier (own evaluators, 2 routes agreeing 2e-10,
sealed anchors reproduced exactly; full report in session task
output; code scratchpad rind5/). PER-CLAIM: LIMIT PASS (O(1/n)
survives model attack, alpha=0.996-1.001; new n=32 full-space point
0.56474187 closes the two-point hole; limits confirmed to 1.2e-6).
RATE PASS/CONSTANT RESTATE (ratios rise 5.18->7.65 from below,
NOT converged at Delta=6; c(Delta) still rising 0.107/0.112/0.117 --
quote bracket [0.105,0.125] ONLY, drop +/-0.006; c_fs data-supported
(0.07,0.125]). PLATEAUS CONFIRMED (+0.014781/+0.004057/+0.000795,
160-3000x error). MECHANISM PASS (sign boundary exactly at lag
Delta, no drift, 7 adversarial starts -> same record, KKT certificate
8.4e-6; define time-symmetric = TRANSPOSE symmetry, persymmetry
fails 6% at edges). ANCHORS PASS except E_inf(6) REFUTED as 4-digit
(pair-sensitivity +/-10% around ~4.4e-7; quote raw La(48,6) =
0.5316222730 instead).
**LOAD-BEARING (d): U-COUPLED RECORDS BREAK EVERYTHING** -- chain
rule FALSE outside U-independent family (random U-coupled residuals
0.015-0.40; optimizer endpoint 4.59 bits); identity extends exactly
iff U-coupling is Delta-lag causal (Au[t,s]=0 for s>t+Delta); minima
collapse: trivial Delta-causal U-record hits 0.539536 < 0.566758,
general U-coupled certified-feasible record hits L_a(0) = 0.092864
(< block_16 -- sandwich INVERTED). U-independence = numbered hard
hypothesis in Thm 1 AND 078; U-coupled variant = a different,
far cheaper coordinate, OPEN.
(e) causal-spectral allocation VERIFIED to 7 digits by an
independent route BUT is neither UB nor LB (no achievability map, no
DPI direction) -- reword to "not matched by any tested
causal-conditioning spectrum"; label it a reference construction.
ERRATA to fix: tex v0.2 item (v) block_inf 0.52991 -> 0.529950
(propagated from pass-1 coarse waterfilling; gap 0.0313 unaffected);
PROBE process-limit excess(4) 2.75e-5 -> 2.66e-5 (stageC.json).
SIX RESTATEMENTS (verbatim list in task output): 1 U-independence
hard hypothesis + counter-values on record; 2 c bracket only;
3 raw-La anchors, E_inf(6) +/-10%; 4 "no tested spectrum" rewording,
reference-construction label; 5 transpose-symmetry definition;
6 errata + ratio "unresolved beyond Delta~6" + c_fs bracket scoping.
ANY SEAL WITHOUT HYPOTHESIS 1 MUST FAIL.
NEXT: tex v0.3 with all six + errata; harness netting anchors/
ladder/mechanism/U-counter-values; pilot; seal 078; STOP for
governed go-ahead (not yet authorized).

## S2/DBLP/Crossref residual pass (2026-08-05/06): ALL FOUR OBJECTS HOLD-NOVEL -- the novelty gate is CLEARED

Non-arXiv coverage closed: DBLP (authoritative for ISIT/ITW/IEEE-TIT
-- all core phrasings null), Crossref (APS camera-only face reached;
returns null-relevant), S2 still 429-walled (2/11 returns, null,
low-value; the one unexercised channel = S2 with an API key,
belt-and-suspenders only). Verdicts: (1) L_a as erasure-cost
coordinate HOLDS-NOVEL; (2) chain rule + Kalman-pole leakage
HOLDS-NOVEL ("smoothing leakage" exists once in DBLP, a 1989 image-
diffusion paper); (3) sequential Landauer vs causally-growing
reference HOLDS-NOVEL with ONE non-arXiv adjacent found: Anderson
2018 (Springer, doi:10.1007/978-3-319-93458-7_2, conditional
erasure, STATIC conditioning) -- joins the Berta line in must-cite/
related-work; Ji-Gour-Wilde arXiv:2503.09012 (static QSI, feedback)
-> related-work; ISITA 2024 distributed-erasure region optional;
(4) horizon-matched record design HOLDS-NOVEL. WebSearch budget
exhausted this session (disclosed). NET: the arXiv verdict (NOVEL
conditional on four must-cites) STANDS with Anderson 2018 added as
the fifth; headline novelty language may be promoted at the next tex
revision with the five citations in force.

## LOWER-BOUND PROVER (2026-08-06): JOINT CONVEXITY PROVED -- the family optimization is a convex program; all 078 anchors certified two-sided

Theorem R (representation): in moment coordinates H = A Sigma_W =
Cov(Yh,W), Gamma = Cov(Yh) on the convex cone D = {Gamma -
H Sigma_W^-1 H' >= 0}, for ANY nondecreasing prefix-access schedule:
2ln2 n L_a = [lndet(Gamma - HQH') - lndet(Gamma - HPH')] +
sum_j [ln Var(S_j|S^{j-1}) - ln Var(S_j|S^{j-1}, Yh^{k(j)})],
k(j) = max(0, j-Delta-1) -- the S-side (reversed) leakage form;
re-proves the 076 chain rule in one line; U-independence enters
EXACTLY once (step 2, residuals (U,Z) independent given W).
Theorem C (convexity): block bracket = the exact 074 G-form (C<->H',
V<->Gamma, P-Q = Sigma_W^-1 Sigma_{W|S} Sigma_W^-1 >= 0) -- convex by
the 074 lift; each leak term = -ln of a concave inf-of-linear Schur
pivot bounded below by tau2 -- convex; distortion AFFINE. So n L_a is
jointly convex on D, every KKT point is the GLOBAL family minimum,
strong duality gives computable lower bounds. The per-term trap
avoided by the S-vs-Yh pivot regrouping (per-cell convexity open,
not refuted -- 9600 samples, no violation).
Sanity: representation residual 1.15e-12 over 144 cells; 32,000
Jensen midpoints ZERO violations; tangent-plane at the winner 400/400
(min slack +1.13e-2); analytic gradient vs FD 1.2e-10; eigmin(P-Q) >
5.6e-3.
CERTIFIED TWO-SIDED ANCHORS (Lagrangian polish + moment-box bound):
p*(16,0) in [0.566751148, 0.5667581350] (width 7.0e-6); (16,1)
3.6e-6; (16,2) 3.8e-6; (24,0/1/2) 4.3e-6/1.5e-5/1.6e-5; (32,0)
1.7e-5. UPGRADES: (a) FIRES -- 078 anchors are certified family
VALUES; (b) FIRES conditional on the O(1/n) model ONLY (certified
strict gaps +0.01477/+0.00406/+0.00080 above the causal-spectral
candidate at 300x/100x/14x bracket ratios; unconditional limit needs
an n-monotonicity/superadditivity lemma -- NAMED OPEN FACE);
(c) FIRES -- sandwich margin computable: minL_a(0) - block_16 in
[0.0317836, 0.0317906]. SCOPE: family F0 only (U-coupled NOT
covered); diag class = non-convex slice (its ladder stays UB-only);
minimizer uniqueness NOT claimed (gauge flats not excluded --
"an optimizer", never "the").
NEXT LOOP (in flight): R-IND-5 with the prover's 5-point attack list
(k(j) off-by-one; 074 sub-lemma transpose conventions; moment-box
legitimacy + NF-floor inactivity; own-code Jensen/tangent reruns;
weak-duality direction of the mu-fit bound) -> tex v0.4 (Theorems
R+C, certified anchors, O(1/n)-conditional rewording of the
no-spectrum-matches face) -> prereg 079.

## R-IND-5 on Theorems R+C (2026-08-06): READY TO SEAL 079 conditional on SEVEN restatements

Independent verifier (own evaluator/polish/box, fresh seeds; code
scratchpad verifR5/). Theorem R PASS (identity to 2.0e-12 over 279
cells incl. edges; k(j) convention CORRECT, shifted variants
detected at 0.1-0.7 bits). Theorem C PASS (074 mapping exact to
0.0e0; PSD legs closed-form-verified; composition chain RE-PROVED
independently; 11,200 own-code Jensen midpoints + 1,566 curvature
probes: ZERO violations). All seven anchor brackets recomputed
end-to-end (mutually consistent, some tighter: (16,0) LB
0.566754682 width 3.45e-6); moment box VALID (per-cell can grab the
whole budget: sqrt(Gamma_tt) <= 1 + sqrt(nD); adversarial blowup
reaches 10.1748 vs box 10.1818 -- nearly tight); bound direction
correct link-by-link (400 pts, 0 violations); NF floor inactive;
uniqueness probe: NO flat found (3 polishes agree to 2.8e-14 value,
2e-6 coords) -- keep "an optimizer" wording anyway. Sandwich margin
tightened: [0.0317872, 0.0317906].
SEVEN MANDATORY RESTATEMENTS for tex v0.4 + 079:
1 (R2) schedule-general k(j) = #{t: se(t) < j}; the printed
  max(0, j-Delta-1) is staircase-specific (blind use deviates 1.05
  bits) -- state both, reduction explicit.
2 (R3) U-independence: single premise, load-bearing in TWO legs
  (numerator/leak AND denominator; leg-by-leg counter-values 0.32-
  2.01 bits at n=12; both corrected -> exact for arbitrary Au incl.
  anticausal). Delta-lag-causal U-coupling does NOT rescue moment-
  form Theorem R (2.4-3.5 bits) though it extends the record-space
  chain rule -- the two extensions must not be conflated.
3 (C3) "diag class = non-convex slice" REFUTED AS WORDED: in (H,
  Gamma) it is a CONVEX (linear) section; diag ladder is UB-only
  because class < family, and within-class values are certifiable by
  the same Lagrangian machinery restricted to the section (upgrade
  opportunity, noted).
4 (C2) per-cell convexity stays OPEN (verifier also found zero
  violations); never print "single terms are NOT convex".
5 (C1) eigmin(P-Q) erratum: 5.5944e-3 at n=16, decreasing in n --
  quote ">= 3.9e-3 for n <= 32" or per-n.
6 (A1) winners distortion-infeasible by ~4e-11: one-line feasible-
  projection remark (correction ~1e-10, immaterial at 3.5e-6).
7 (A2) "certified" = floating-point certificates (no interval
  arithmetic; widths exceed f64 error by ~7 orders); claim (c)
  inherits block_16 precision via proven diag-optimality.
A seal carrying restatement-1 or -3 as-worded must FAIL.
CHAIN (authorized end-to-end): tex v0.4 -> harness -> pilot -> seal
079 -> governed -> package.

## GO-14 closers (2026-08-06): the n-transfer lemma PROVED; the diag ladder certified within-class

TASK 1 -- n-TRANSFER LEMMA (prover grade, R-IND-5 pending):
kappa := (1/2)log2(1/(1-a^2)) = 0.736966 bits (the AR(1) boundary
information). (i) EXACT SUBADDITIVITY f(n1+n2) <= f(n1)+f(n2) via
block-concatenation (per-term inequality verified all cells;
denominator equality 1.3e-15) => by Fekete, L^inf = lim = inf phi_n
EXISTS UNCONDITIONALLY and every finite-n UB bounds the limit.
(ii) boundary-charged superadditivity: phi_m - phi_2m <= c(Delta)/2m
with c(0) <= 0.42029, c(1) <= 1.1257, c(2) <= 1.1219, always <=
2 kappa; EXACT superadditivity REFUTED (phi_8 > phi_16 > phi_24 >
phi_32 certificate-strict; new anchors phi_8(0) in [0.570790938,
0.5707933842], phi_12(0) in [0.568030932, 0.5681028134]); the
obstruction IS the split-boundary coupling, <= kappa per side. Key
step: the interleaved chain rule cancels record-noise coupling
EXACTLY inside the identity (zero-claim 4.8e-16) -- U-independence
load-bearing TWICE (marginalization + the S-pivot zero-claim).
(iii) two-sided: 0 <= phi_n - L^inf <= c/n (measured drift 0.0645
sits 6.5x inside proven c(0) = 0.4203).
COROLLARIES: L^inf(0) in [0.551591, 0.564742] UNCONDITIONAL;
**the Delta=0 plateau over the causal-spectral allocation is now
UNCONDITIONAL: L^inf(0) >= 0.5515910 > 0.5479448, margin +3.65e-3
(~250x bracket width)** -- Conjecture v0.2 item (3) at Delta=0 no
longer needs the O(1/n) model. Delta=1/2 stay model-conditional
(would need certified anchors at n ~ 260/1320 or a sharper
constant). Scope: FULL-FAMILY only (diag concatenation leaves the
class); constant depends only on the pole.
R-IND-5 attack list (from the prover): interleaved-prefix match;
U-free zero-claim; marginal-law step; convexity-in-D; dropped
negative term sign; sharpening monotonicity-in-m.

TASK 2 -- DIAG LADDER CERTIFIED WITHIN-CLASS (the convex-section
upgrade executed): all 9 ladder cells (24/32/48 x 4/5/6) + 3 block
values now certified two-sided CLASS VALUES (widths 2.2e-7..1.6e-6;
section moment box Rbox 73-136; 4/9 SLSQP endpoints were true class
minima to 2e-11). E_inf(4) CONFIRMED in-bar (+/-4.4%); E_inf(5)
sign now certificate-grade; E_inf(6) NOT resolvable at achievable
widths (bracket contains 0) -- independently RATIFIES the R-IND-5
demotion to the raw La(48,6) anchor. (48,6) cell flagged loosest
(projection correction 1.1e-6, still brackets).
NEXT: R-IND-5 on the transfer lemma -> tex v0.5 (Theorem T +
unconditional Delta=0 plateau corollary + executed diagsection
upgrade) -> registration 080.

## R-IND-5 on the n-transfer lemma (2026-08-06): PASS on (i)+(iii)-lower; "kappa per side" REFUTED as an F0 lemma; plateau label DEMOTED to conditional

THEOREMS (unconditional): (i) exact subadditivity + Fekete (set
identity exact all cells incl. unequal blocks 8+4->12; phi_n >= 0
hygiene + eps-optimal concatenation to state); (iii)-LOWER
0 <= phi_n - L^inf. Anchors phi_8/phi_12 reproduced to 1.5e-10.
REFUTED: I(E;T^{b2}) <= kappa as a universal F0 statement --
D-feasible counterexamples: two V-copies D2 = 0.4563 > kappa - I =
0.4203; three Y-copy rows D2 = 18.93 bits ~ 26 kappa; worst case
Theta(m). NO universal constant exists; any proof must use
optimizer structure. At optimizers the bound holds 5.5x-stable
(D2 = 0.076971/0.076926, I(E;T^{b2}) = 0.543 at m=8/16 -- verified
at those two m ONLY).
MANDATORY RESTATEMENTS for tex v0.5 + 080: (1) (H*) numbered
hypothesis "dyadic-chain optimizers have per-side boundary charge
<= c(Delta;n)" with counter-values + optimizer verifications on
record; (ii), (iii)-upper, and the plateau corollary carry
"conditional on (H*)"; NEVER print "<= kappa per side" as an F0
lemma. (2) c(Delta;n) = (2 - 1{Delta=0}) kappa - I_n, I_n MONOTONE
INCREASING (uniform validity from base n); c(1) -> <= 1.1258 (5th
decimal was false). (3) zero-claim + marginalization tagged F0-only
with counter-values 0.2223/0.0950 bits (violation arises from
block-2-only coupling via conditioning). (4) corollary uses the
SEALED 079 LB(32,0) = 0.5647327869 -> L^inf(0) >= 0.5515989
conditional on (H*); margin 215x (not ~250x); the prover's
0.564729705 citation exists NOWHERE -- do not cite; base n=24
FAILS by 5e-5 (no constant slack -- (H*) genuinely load-bearing).
(5) Task-2 E_inf items are 1/n-MODEL-conditional, not certificates
(tag); drop the unverifiable 4/9-endpoints claim or ship endpoints.
(6) ladder spot-checks + section box PASS (box exactly attained --
tight); E_inf demotion of Delta=6 re-ratified.
REPAIR PATH (recorded): an optimizer-regularity bound on
I(E;T^{b2}) via the Theorems R+C convex-program structure (measured
0.543, stable in m, 0.19 under kappa) would restore the
unconditional label with the same constants -- the natural next
prover face. A seal carrying "plateau UNCONDITIONAL", the kappa
lemma, or c(1) <= 1.1257 must FAIL.
NEXT: tex v0.5 with all six restatements -> registration 080
(scope: theorems (i)+(iii)-lower + anchors + within-class ladder +
conditional corollary under (H*)).

## (H*) REPAIR PROVER (2026-08-07): (H*) REPLACED, not discharged -- the reverse direction reduces to ONE SCALAR

THE LEMMA CHAIN (proved, F0-only, no optimizer structure, per-step
certificates): with X := I(Yh^{b1}; W^{b2} | W^{b1}) the CROSS-BLOCK
READ, **D1 + D2 <= c(Delta;m) + (2 - 1{Delta=0}) X**.
L1: kappa is an IDENTITY not a bound -- I(T^{b1};T^{b2}) = kappa
exactly, every m,n (AR(1) Markov; both DPI steps equalities; cert
3.8e-14, m-independent as the proof predicts). L2: I(E;T^{b2}) <=
kappa + X and I(E';E) <= kappa + X (S^{b1} drops because
U _|_ (W,Yh)); min slack +5.67e-7 -- **TIGHT exactly at the
three-Y-copy counterexample, i.e. sharp where the universal claim
dies**. L3: D2 <= I(E;T^{b2}) - I_m (identity residual <= 9.3e-11;
chain-rule collapse 1.3e-15; zero-claim <= 2.5e-10). L4:
D1 <= I(E';E), = 0 at Delta=0.
COROLLARY -- **(H*) IS A THEOREM on the split-causal sub-family**
F0^sc(m) (records whose block-1 cells read no block-2 source;
equivalently the LINEAR moment condition H[b1,idx2] =
H[b1,idx1] Sig11^-1 Sig12), WITH THE TEX'S OWN CONSTANTS. F0^sc is a
CONVEX LINEAR SECTION, so Theorem C certifies it two-sided (executed:
phi^sc brackets at (16,0)/(24,0)/(32,0)/(16,1)/(16,2); the
split-causality price is FLAT IN n at ~0.0041 bits at Delta=0 -- a
pure boundary constant).
Pi-RETRACTION LEMMA: Pi (project block-1 onto its W^{b1}-conditional
mean + matching independent noise) preserves distortion EXACTLY
(1.1e-16) and the entire block-1 joint law (4.4e-16), kills X
(1.5e-14), IMPROVES generic records by 0.37-3.11 bits, and costs
only 5.0e-3 bits at optimizers.
**THE REFUTATION IS NOW EXPLAINED, NOT JUST RECORDED**: the V-copy /
Y-copy counterexamples are precisely records with enormous X (18.46
and 29.27 bits). The tex's blanket "never print <= kappa per side as
an F0 lemma" must be REFINED: it is a theorem on F0^sc(m), and the
refutation is exactly the failure of split-causality.
**080 DOES NOT BECOME UNCONDITIONAL.** It becomes conditional on a
STRICTLY WEAKER, BETTER-MARGINED, MONOTONE-VERIFIED hypothesis
(H**): "at dyadic-chain optimizers, X <= Xbar" -- ONE SCALAR,
measured 6.3e-3 against an admissible 0.117 (18x headroom, vs (H*)'s
0.077 against 0.420 = 5.5x), monotone decreasing in m, and
constructively bounded by Pi at any m. Constants grow slightly:
c(0) 0.420286 -> 0.426633; the plateau corollary SURVIVES at
0.5514005 > 0.5479448, margin +3.456e-3 (203x tex-v0.4 width, 376x
sealed), and the base-24 negative control still FAILS -- now by
3.11e-4, so the no-slack claim STRENGTHENS.
**BONUS HOLE FOUND AND REPAIRED (independent of (H*)):** Theorem
T*(ii)'s restriction step assumed each block distortion <= D, but
the 2m-optimizer's blocks STRADDLE D (0.299486/0.300514 at n=16;
mean exactly D). Repaired by convexity of D -> phi_m(D), which
Theorem C supplies. Ignoring it would have cost m mu (d2 - D) ~
9.1e-3 bits -- LARGER THAN THE WHOLE REPAIR TERM.
**EXTENDED TABLE RETIRES THE "m in {8,16} ONLY" CAVEAT**: m in
{8,12,16,24} at Delta=0, {8,12,16} at Delta=1,2; EVERY quantity
(D1+D2, I(E;T^b2), X, Pi-price) MONOTONE DECREASING in m, so the
base value dominates the whole chain; two-point 1/m limits X_inf ~
6.31e-3, (D1+D2)_inf ~ 0.076859, I(E;T^b2)_inf ~ 0.54304. Two
precision notes on the sealed record: at m=16 the recorded D2
0.076926 / I 0.543057 came from a warm-polish endpoint at
d-D = +6.4e-5 (distortion-INFEASIBLE); the feasible cold-start
certified values are 0.0769152 / 0.543054 (difference 1.1e-5, well
inside the harness's 5e-3 band -- a precision note, NOT a bar
change).
ROUTE 2 QUANTIFIED (evidence, not proof): along convex affine
sections through the optimizer, forcing I(E;T^{b2}) = kappa costs
>= 1.159e-2 bits/symbol (2898x the bracket width, 2.9x the entire
n=16->inf drift); forcing D1+D2 = c(0) costs >= 3.261e-2 (8153x).
The refuting records are far worse (L_a 1.73 and 2.25 vs phi_16
0.5668).
**THE EXACT OBSTRUCTION (and why KKT provably cannot close it):**
since Sig_W^-1 Sig_WY = [0;I], the distortion gradient VANISHES
IDENTICALLY on the cross-read coordinates -- so KKT stationarity
there carries NO multiplier: the cross-read is a distortion-FREE
direction in which the objective is STATIONARY, and the optimizer
chooses X > 0 because it strictly lowers L_a. No exchange/zeroing
argument can force X = 0; KKT yields an equation, not a bound. What
is missing is an OPTIMIZER DECAY estimate: ||A12||_F/||A11||_F =
3.4%, the cross-block kernel decaying geometrically at ratio
~0.28-0.35 ~ the smoothing pole lambda_s = 0.354554. A
Demko/Jaffard-type exponential off-diagonal decay bound for inverses
of banded PD operators, applied to the R+C KKT system, would give
||A12|| <= C lambda^. uniformly in m and CLOSE THE GAP -- a standard
TYPE of theorem, much softer than (H*).
NEXT LOOP (prover's recommendation, adopted): (1) prove the decay
(highest leverage -- makes T* v2 and the plateau UNCONDITIONAL with
constant c + Xbar); (2) BYPASS transfer entirely with an n-UNIFORM
DUAL CERTIFICATE (stationary/Toeplitz multiplier feasible for every
n, via the GO-13 spectral machinery 070/071/073) -- no boundary
charge, no hypothesis at all, and it reaches Delta=1,2 which the
transfer route cannot without anchors at n ~ 260/1320; (3) cheap
hardening: m=24,32 at Delta=1,2; phi^sc at (48,0); net the H-repair
identities as harness gates (deterministic, analytic, optimizer-free).
PREREG IMPACT: 080's gates are UNTOUCHED -- nothing here contradicts
any sealed gate, and the s4 refutation gate is now EXPLAINED rather
than merely recorded. A v0.6 revision needs a fresh registration
(081) for: the H-repair lemma family, the certified phi^sc brackets,
the extended m x Delta table, the Pi-retraction identities, the
convexity-of-phi_m(D) hygiene, and the recomputed corollary
arithmetic. Eleven sentence-level tex edits specified in the report.

## DECAY PROVER (2026-08-07): THEOREM K proved (unconditional, new) -- the decay itself NOT proved, but (H**) reduced to two model-scale hypotheses, and a BETTER hypothesis (H***) found

**THEOREM K (KKT structure; UNCONDITIONAL, F0, any Delta, any
schedule).** Two exact model facts drive it, both structural:
K := Sig_WS' Sig_W^-1 = [I, 0] (since E[S|W] = V and V IS a
coordinate block of W), so every Q-factor term lives ONLY on the
V-columns; and Sig_W^-1 Sig_WY = [0;I], so the distortion gradient
lives ONLY on the Y-columns. **The two supports are DISJOINT**, so
stationarity splits by column block. With A = H Sig_W^-1 = [Av, Ay],
N = Cov(Z), theta = 2 mu ln2, and (v_t, v_t^S, sigma_t) the record
pivots of the interleaved order:
  (K1) Ay = theta N
  (K2) N^-1 = theta I + sum_t v_t v_t'/sigma_t = theta I + V Sig_s^-1 V'
  (K3) Av = -N V Sig_s^-1 V_S'
Verified at EVERY certified optimizer: relative residuals <= 3.2e-8
at (16,0)/(24,0)/(32,0)/(48,0)/(16,1)/(16,2)/(24,1) -- residuals
track the polish accuracy, not the identities.
**COROLLARIES, unconditional and m-uniform:**
- Ay = theta N is SYMMETRIC POSITIVE DEFINITE. **This UPGRADES the
  078-era empirical "mechanism" finding (Ay and the noise kernel
  transpose-symmetric to <5e-5; all causal asymmetry in Av) from an
  EMPIRICAL DISCOVERY to a COROLLARY OF THEOREM K** (measured
  symmetry defect 1.2e-9..1.4e-8). And Av = -N V Sig_s^-1 V_S'
  carries the asymmetry through V_S, whose column support ends
  EXACTLY at t+Delta -- the structural candidate for the observed
  "sign change exactly at lag Delta" (a lead, not yet a claim).
- 0 < N <= I/theta and 0 < Ay <= I, UNIFORMLY IN m -- the first
  m-uniform optimizer-regularity statement in the program.
- theta >= 2ln2 phi_n(D)/(1-D) >= 1.119 (convexity of D -> phi_n(D)
  plus phi_n(1) = 0), hence N <= 0.894 I unconditionally.
SPECTRAL PLATEAU CONFIRMED (Demko's hypothesis holds numerically,
uniformly in m): at Delta=0, m = 8/12/16/24, theta 3.0785->3.0835,
cond N 1.4453->1.4492, cond M_Q 2.197->2.217, lmin(J) 0.2686 flat,
sigma_t in [0.3753, 0.4588], and **||A12||_F FLAT in m**
(5.4823e-2 -> 5.4722e-2). Measured kernel decay identical to 3-4
digits across n=16/24/32/48 (a fixed Toeplitz kernel plus
non-moving boundary corrections); per-lag ratios DECREASE with lag
(.284->.200 for Ay, .377->.279 for Av), so a single geometric
envelope is conservative. At lambda = lambda_s = 0.354554 (GO-14's
own smoothing pole) the envelope constants are C_v = 0.1980,
C_y = 0.1631, identical to 3 digits at n=24/32/48.
**CONVERSION THEOREM (proved, uniform in m BY CONSTRUCTION).**
Exactly: X = (1/2) log2 det(I + N11^-1 A2 Sig_{2|1} A2'). Under
(D) kernel-decay envelopes and (F) lmin(N) >= nu:
X <= (1/(2 ln2 nu)) (lam^2/(1-lam^2)) [(C_v + rho C_y)^2 T_g(lam)
+ (1-rho^2) C_y^2/(1-lam^2)], T_g(lam) = (1/(1-lam^2))(1+lam a)/
(1-lam a) - a^2/(1-lam a)^2 -- INDEPENDENT OF m (the sums run over
infinite half-lines). Sig_{2|1} used EXACTLY, not enveloped (the
-a^{j+k+2} boundary term is worth 2.6x and is what makes the bound
clear the bar). Link-by-link loss audited at real optimizers:
logdet->tr 1.004x, N11 >= nu I 1.22x, Schur-with-envelope 8.4x,
total 10.3x.
**RESULT: Xbar = 0.065038 vs the 0.1169299 bar -- CLEARS with 1.80x
margin, uniformly in m.** Robust: free-lambda optimization gives
0.0648; insensitive to the envelope-fit window (caps 6..16 identical
to 4 digits). Whole chain gated numerically at all four Delta=0
optimizers. Corollary arithmetic: c(0) + Xbar = 0.485324 ->
L^inf(0) >= 0.5495664 > 0.5479448, margin +1.622e-3 (95x the quoted
bracket, 177x the sealed); base-24 control STILL FAILS, now by
2.757e-3, so the no-slack claim STRENGTHENS FURTHER.
**THE OBSTRUCTION (honest, and NOT the spectral hypothesis -- that
one holds): CIRCULARITY OF THE OPERATOR.** The only operator whose
inverse produces the optimizer is N = (theta I + V Sig_s^-1 V')^-1
(K1-K2), equivalently J = Cov(S^n, Yh^n) -- both built FROM THE
OPTIMIZER ITSELF (M := V Sig_s^-1 V' = N^-1 - theta I exactly). So
"M decays exponentially" <=> "N decays exponentially": Jaffard's
inverse-closedness RETURNS ITS OWN HYPOTHESIS. The model's decay
(Sig_S, Sig_W, Sig_{W|S} all exactly a^|t-s|) enters the KKT system
ONLY through the affine data, never through the operator being
inverted. Nothing injects it into A except a FIXED-POINT/BOOTSTRAP
argument in a Jaffard (or Groechenig-Klotz weighted) Banach algebra:
show the KKT map sends a ball {||A||_{A_lam} <= R} into itself and
contracts. That is the missing theorem -- a genuine research step.
SECOND missing piece, independent: (F) lmin(N) >= nu uniformly. KKT
gives the UPPER side (N <= I/theta, proved) but not the lower; every
attempted route closes on itself (lmax(M) <= 1/lmin(M_Q) and
M_Q >= N give 1/nu <= theta + 1/nu), and coercivity fails because a
record that does not use a direction pays nothing there.
ALTERNATIVES EVALUATED AND CLOSED: (b) Pi-retraction/perturbation
STRUCTURALLY CANNOT bound X -- at an optimizer the Pi-price is >= 0
automatically and the measured price/X ratio is 0.7960 at every n
and every Delta, so "price >= 0" is consistent with ANY X; the
convexity variant just repackages the same missing estimate.
(c) m-induction: X is monotone (6.3468/6.3360/6.3307/6.3254e-3 ->
6.31e-3) but the step compares the m- and 2m-optimizers = the
missing estimate again.
**BONUS -- A CLEANER HYPOTHESIS THAN (H**): (H***).**
Concatenating two independent m-optimal records is SPLIT-CAUSAL, so
**phi^sc_{2m} <= phi_m UNCONDITIONALLY**; applying the F0^sc
boundary-charge THEOREM to the 2m-window sc-optimizer gives
phi_m - phi^sc_{2m} <= c/(2m), hence phi_n - L^inf <= (c + pbar)/n
where p_m := m(phi^sc_m - phi_m) is the SPLIT-CAUSALITY VALUE GAP.
So (H**) can be replaced by **(H***): p_m <= pbar < 0.1169** --
same bar, but p is a gap between TWO CONVEX PROGRAMS and is
therefore **TWO-SIDED CERTIFIABLE by Theorem C**, unlike X which is
only measurable at a computed optimizer. Already certified:
p = 0.004165/0.004207/0.004382 at m = 8/12/16 -- flat, **27x
headroom** (vs X's 18x).
NEXT ROUTE (replaces "prove the decay" as stated): solve the
STATIONARY KKT system (K1-K3) in the SPECTRAL domain with the GO-13
machinery (070/071/073). K1-K3 become per-frequency scalar
equations; if the symbols are rational with poles off the unit
circle, the Toeplitz coefficients decay at exactly the modulus of
the nearest pole -- which the numerics say is lambda_s = a(1-K) =
0.354554, GO-14's OWN NETTED CONSTANT. Then transfer
stationary->finite-window by a stability estimate from Theorem C's
strong convexity (the only place boundary corrections enter). This
also feeds the n-uniform dual-certificate route.
WHAT v0.6+ CAN SAY: Theorem K and its corollaries are UNCONDITIONAL
and seal-able (analytic, optimizer-free to state, deterministic to
gate); the 078 mechanism material UPGRADES to a corollary;
rem:repair is replaced by an EXECUTED REDUCTION ((H**) <= (D)+(F),
conversion proved, Xbar = 0.0650 at 1.80x); phi^sc_{2m} <= phi_m and
(H***) are unconditional additions. WHAT IT STILL CANNOT SAY: the
plateau corollary CANNOT drop its hypothesis -- it trades (H**) for
(D)+(F), margin +1.622e-3 (95x bracket) instead of +3.456e-3, with
the base-24 control failing by 2.757e-3.

## CORRECTIONS to the two prover reports (found by the v0.6/harness build, 2026-08-07)

Independent re-measurement from the committed artifacts contradicts
three statements recorded above. The corrected values are what tex
v0.6 and the 081 harness carry:
1. L2's TIGHTNESS is attained at the **two-V-copy** witness
   (slack 5.67e-7), NOT the three-Y-copy witness (0.144 there). The
   recorded VALUE 5.67e-7 is right; the attribution above is wrong.
2. The refuting records' L_a values are **4.2187 / 4.7397**, not the
   1.73 / 2.25 recorded above -- those two numbers are not
   reproducible from any artifact.
3. The feasible cold-start m=16 charge is **0.07691493**, not
   0.0769152 (3e-7, immaterial, but the record should be exact).
4. CAUTION netted in the harness: **(K2)/(K3) require the RECORD-
   pivot Gram**; with the reference-pivot Gram they fail at 47% and
   120%. Stated in the v0.6 proof skeleton.
5. Scope note: the Delta=1,2 rows of the m-table are the prover's
   and were NOT re-netted by the build; sK covers six of the seven
   certified optimizers ((24,1) omitted).
Pi-gains measured [-2.74, -0.31] on a different draw order vs the
prover's [-3.11, -0.37]; both printed in v0.6.

## SPECTRAL PROVER (2026-08-07): the COLLAPSE identity, the stationary system, lambda_s REFUTED as the pole -- and a BYPASS that would make the plateau unconditional (one step pending R-IND-5)

**COLLAPSE IDENTITY (new, exact, unconditional).** Using
prod_t sigma_t prod_j s_j = det J = det Sig_S det Cov(Yh|S), the
S-side leak sum telescopes against lndet Cov(Yh|S), leaving
**2 ln2 n L_a = sum_t ln sigma_t - lndet N**, every n, every
schedule, every F0 record. Verified at ALL TEN certified optimizers
(n=16/24/32/48 x Delta=0/1/2), rel residual <= 1.2e-14. It
re-derives K1-K3 in five lines and makes the periodization argument
below a one-liner.
**STATIONARY SYSTEM.** In the shifted frame R_u := Yh_{u-Delta-1}
the interleaved order becomes the plain simultaneous order of (R,S),
and **Delta enters ONLY as the phase e^{-i(Delta+1)w} on the
cross-spectrum** -- that is the entire content of the lag coordinate
at stationarity. Symbols: K2 1/n(w) = theta + |v(w)|^2/sigma;
K1 a_y = theta n (real, zero-phase, positive -- so "A_y symmetric
PD" is a ONE-LINE stationary corollary); K3 a_v = -z^{-(Delta+1)}
n v(1/z) v_s(z)/sigma. **NOT RATIONAL** at any finite order (the
fixed point compounds degree; Hankel singular values fall
geometrically rather than truncating) -- analytic in an annulus,
hence geometric decay, but no finite-order closure.
L^inf VALUES (10-digit stable across Nf 1024..8192, lag depth
50..250): **0.562726496 / 0.536401378 / 0.531050020** at
Delta=0/1/2 (then 0.530117530 / 0.529973408 at 3/4).
**FIVE INDEPENDENT VALIDATIONS**: (1) Richardson on the certified
anchors agrees to 5.0e-7/6.3e-7/8.2e-7; (2) n(phi_n - L^inf) FLAT
(0.064507/0.064497/0.064495/0.064487 at n=16/24/32/48) -- the O(1/n)
law with c(0) = 0.064495 +/- 3e-5 relative; (3) theta transfers
(finite-n extrapolates to 3.086040 vs stationary 3.086038362, 1.6e-6);
(4) kernels transfer ENTRYWISE (n=32 central row vs stationary: N
1.7370e-1 vs 1.7364e-1; A_y 5.3538e-1 vs 5.3585e-1; A_v lag +1
5.180e-2 vs 5.175e-2; lag -1 -1.578e-2 vs -1.576e-2 -- differences
exactly the size of the O(1/n) theta drift); (5) a KKT-FREE direct
minimization over FIR records (Powell + Nelder-Mead, 2 starts, no
reference to K1-K3) returns 0.5627265093 vs the fixed point's
0.5627264963 -- gap 1.3e-8.
**THE 078 MECHANISM IS NOW AN EXACT STATIONARY COROLLARY**: the
stationary a_v kernel is POSITIVE for j <= t+Delta and NEGATIVE for
j > t+Delta at both Delta=0 and Delta=1 (sign flip one lag later),
i.e. the sign boundary sits EXACTLY at the access horizon, and K3
explains it -- the anticausal branch comes from v(1/z), the causal
branch from z^{-(Delta+1)} v_s(z), and the shift places the
crossover at lag Delta. Horizon-matched V-cancellation: corollary,
not measurement.
**lambda_s REFUTED AS THE POLE, UPHELD AS AN ENVELOPE.** The
mechanism that would produce lambda_s CANCELS: det Phi_X = f_S
Phi_{R|S} = tau^2 |g|^2 f_V + r f_S, so the f_S zero is NOT
inherited. Measured dominant singularity (roots of u = theta sigma
+ v vtilde, whose zeros are the poles of n and a_y): modulus
**rho* ~ 0.28 (band 0.26-0.29)**, a COMPLEX PAIR (0.2517+/-0.0530i
etc.) -- which explains why the decay prover's per-lag ratios swept
downward (.284->.200) and no single geometric rate fit. rho* is
STRICTLY INSIDE lambda_s = 0.3545538, so **lambda_s remains a VALID
CONSERVATIVE envelope -- hypothesis (D) and the conversion theorem
stand, and Xbar = 0.065038 is LOOSE; re-deriving at rho* would
tighten it materially.** Flagged conjecture (not a claim):
a*lambda_s = 0.2836431 sits inside the band -- one a-sweep settles
it. Caveat: a sub-dominant lambda_s component with small residue
cannot be excluded below the ~1e-9 float64 floor (lags > 13).
**THE BYPASS (GOAL 2) -- and it is NOT a dual multiplier.** Since
dist is affine, the dual is ONE-DIMENSIONAL and feasibility is
automatic; all content sits in an n-uniform lower bound on
Omega_n(Theta)/n. The Collapse identity supplies it in two steps:
**(A) PERIODIZATION => Omega_n/n SUBADDITIVE.** Repeat any n-record
along Z with independent noise copies: distortion is EXACTLY
preserved, lndet N is EXACTLY additive (block-diagonal), and every
sigma_t only DECREASES (its conditioning set gains all earlier
blocks). So L^process(D) <= phi_n for every n. **This is Theorem T
in one line instead of a page, and it costs NO boundary charge
because it goes the EASY way.**
**(B) SHIFT-AVERAGING => stationary Gaussian records attain the
process infimum.** On Z the functional is exactly shift-invariant
and (Theorem C) convex in moment coordinates; the shift-average of a
period-n record's moment functions is a STATIONARY pair in the same
cone, and convexity gives value(average) <= average(value) = value.
**(A)+(B) => phi_n >= Psi(D) for every n => L^inf = Psi(D)** -- the
stationary spectral value, with **NO boundary charge, NO anchors, NO
(H*)/(H**)/(H***), and NO decay estimate.**
**MARGINS vs the causal-spectral bar:** Delta=0 **+0.0147817**
(9.1x the current (H**)-conditional margin, 4.3x the (H*)-era one,
~1600x the sealed n=32 bracket); Delta=1 **+0.0040584**; Delta=2
**+0.0007960** -- and Delta=1,2 were PROVABLY UNREACHABLE by the
transfer route (would need certified anchors at n ~ 260 / 1320).
Consistency: L^inf < certified UB(32,0) = 0.5647420, and every
certified LB(n) sits ABOVE L^inf, exactly as phi_n decreasing to
L^inf requires.
**STATUS, HONESTLY: (A) is solid (the existing subadditivity,
trivial in collapse coordinates). (B) IS THE NEW STEP, prover-grade
but NOT YET R-IND-5'd** -- two soft spots: (i) convexity + lower
semicontinuity of the PROCESS-RATE functional in process-moment
coordinates (inherited from Theorem C by per-symbol limits), and
(ii) realisability of the shift-averaged moment pair in the cone.
**Until (B) is verified, 0.5627265 is an IDENTIFICATION supported by
five independent numerical routes, NOT a sealed theorem.**
IF (B) SURVIVES: the Delta=0 plateau (the campaign's standing goal)
becomes UNCONDITIONAL with no hypothesis at all; so do Delta=1,2;
L^inf is IDENTIFIED rather than extrapolated; and (H*)/(H**)/
(H***)/(D)/(F)/the boundary charge all become UNNECESSARY for the
plateau (they remain of independent interest for T*).
UNCONDITIONAL AND SEAL-ABLE NOW, independent of (B): the Collapse
identity, the stationary K1-K3 symbol table, the exact mechanism
corollary, and the rho* refutation with lambda_s retained as
envelope.
NEXT LOOP: (1) R-IND-5 step (B) -- highest leverage by a wide
margin; (2) certify the stationary optimum TWO-SIDED (per-frequency
Lagrangian + moment box) to make 0.5627265 quotable as a bracket
rather than a 10-digit fixed point; (3) settle rho* by re-solving at
a second a and testing rho* = a lambda_s, then re-run the conversion
at rho* to sharpen Xbar; (4) finish the Delta-ladder at stationarity
(Delta 5..9) to pin the closure constant the campaign left bracketed
at [0.105, 0.125] -- c(Delta) = 0.0328/0.0513/0.0696/0.0843/0.0937
at Delta=0..4 is still rising, so the bracket is reachable.

### Spectral addendum (same day): the Delta-ladder settles the closure law and the constant -- and separates two objects the campaign had been conflating

Delta = 0..9 at stationarity, fixed-point residual <= 9.8e-14:
L^inf = 0.562726496 / 0.536401378 / 0.531050020 / 0.530117530 /
0.529973408 / 0.529953058 / 0.529950369 / 0.529950029 /
0.529949987 / 0.529949982; excess 3.278e-2 down to 7.38e-10;
per-lag ratios 5.081 / 5.865 / 6.565 / 7.152 / 7.612 / 7.934 /
8.111 / 8.148.
1. **THE CLOSURE RATE IS CONFIRMED as lambda_s^-2 = 7.954917.** The
   ratios rise monotonically FROM BELOW and cross lambda_s^-2 at
   Delta ~ 6; the small overshoot at Delta=7,8 is inside numerical
   error (excess 5.9e-9 / 7.4e-10 against a ~1e-11 floor). The
   campaign's standing wording ("rate supported as an asymptotic,
   constant NOT identified, unresolved beyond Delta~6") TIGHTENS:
   the rate IS reached, and the reason it was unresolved beyond
   Delta~6 is that FINITE-n ANCHORS RUN OUT OF PRECISION there --
   not that the law bends.
   **CRITICAL DISTINCTION the campaign had been conflating:** this
   is lambda_s appearing where it GENUINELY BELONGS -- in the
   Delta-CLOSURE EXPONENT -- as opposed to the KERNEL POLE, where
   the same prover REFUTED it (true dominant singularity rho* ~
   0.28, a complex pair). Two different objects; keep them apart in
   all future wording.
2. **THE FULL-FAMILY CONSTANT IS PINNED: c_fs ~ 0.098 +/- 0.004**
   (plateau at Delta=5-7). Inside the recorded data-supported
   bracket (0.07, 0.125], and STRICTLY BELOW the diagonal-class
   c_diag = 0.111 +/- 0.006 -- as it MUST be, since the full family
   beats the diagonal class and so has the smaller excess. That
   ordering is a free consistency check on both numbers, and it
   replaces the bracket [0.105, 0.125] (a DIAG-CLASS object) with a
   FAMILY value.
3. **ERRATUM: block_inf = 0.5299499808**, not 0.529950. The sealed
   value is right to 6 digits and NOTHING downstream moves (the
   0.0313 gap is unaffected), but the 7th digit should be corrected
   in tex/registry -- same class as the earlier 0.52991 ->
   0.529950 fix, and it matters here because the ladder's excess at
   Delta >= 5 is smaller than the rounding of the reference.

### Spectral addendum 2 (same day): pole estimates at Delta=1,2 -- rho* cross-checks at three Delta, and the a*lambda_s conjecture WEAKENS

High-resolution roots (Nf=8192, P=250) of u = theta sigma + v vtilde
across the reliable truncation range L=12..24. Dominant moduli:
Delta=0: 0.272/0.287/0.288 (L=16/20/24); Delta=1:
0.269/0.268/0.277; Delta=2: 0.254/0.264/0.265.
1. **The kernel-pole refutation now holds at THREE Delta.** Every
   estimate is in 0.25-0.29; none approaches lambda_s = 0.3545538.
   Consolidated: **rho* = 0.27 +/- 0.02, UNIFORM in Delta** -- the
   apparent downward drift with Delta is smaller than the
   L-truncation scatter at fixed Delta, so NO Delta-dependence is
   claimed. lambda_s remains a sound conservative envelope for
   hypothesis (D); it is not the pole.
2. **The complex pair is confirmed independently**: at Delta=2 the
   whitening filter's own coefficients oscillate in sign from the
   outset (1, -0.2054, -0.0485, +0.00035, +0.00066, -0.00032,
   -0.000088, +8.2e-6, ...). That is WHY no single geometric
   envelope ever fit the measured per-lag ratios and why the decay
   prover saw ratios "decreasing with lag" -- **the sweep is the
   cosine factor, not a changing rate.**
3. **DOWNGRADE the rho* = a*lambda_s = 0.2836431 conjecture** to
   "consistent but unsupported": it sits inside the Delta=0 band but
   at the TOP EDGE of Delta=1 and OUTSIDE most Delta=2 estimates --
   and a product of two model constants should show NO
   Delta-dependence at all. The a-sweep remains the only way to
   decide; if rho* fails to track a*lambda_s there, the constant is
   genuinely DYNAMICALLY GENERATED by the KKT fixed point with no
   closed form in the model parameters.
**The two appearances of lambda_s are now cleanly separated and
independently established: it IS the Delta-closure exponent
(confirmed, lambda_s^-2 = 7.9549, addendum 1) and it is NOT the
kernel pole (refuted at three Delta, rho* ~ 0.27, here).**

## R-IND-5 ON THE BYPASS (2026-08-07): (A) and (B) BOTH PASS -- but the chain is ONE-DIRECTIONAL, so "IDENTIFIED" is REFUTED and the PLATEAU SURVIVES

Fresh-context verifier, own evaluator from the CMI definition (no
prover code reused for any L_a number); calibration against the
sealed record exact to 3e-16.
**COLLAPSE: PASS** (5.6e-15 over 84 cells; non-staircase schedules
1.7e-15; edges 8.2e-16) -- and re-derived in ONE LINE rather than
the artifact's telescoping route (conditioning on W reduces Yh_t to
Z_t and S^{se(t)} to U^{se(t)} _|_ Z, so every denominator is
Var(Z_t|Z^{t-1}) and telescopes).
**RESTATEMENT 6: Collapse does NOT require U-independence -- it
requires exactly Delta-LAG-CAUSAL U-coupling** (dense Au: 0.2018
bits off at Delta=0, anticausal 0.3329, Delta-causal EXACTLY 0).
F0 is the special case Au=0. The non-conflation rule still applies:
this does NOT extend moment-form Theorem R.
**(A) PERIODIZATION: PASS, all three sub-claims separately** --
distortion preserved <= 4.4e-16; lndet N additive <= 7.1e-15; every
sigma_t decreases over **1200 cells, 0 violations**. The suspected
hidden failure (superset vs merely-different conditioning) DOES NOT
OCCUR, with the reason given: the block-b translate's set is
genuinely a SUBSET of the tiled cell's, since bn+min(i+Delta,n) =
min(bn+i+Delta, bn+n) <= min(bn+i+Delta, M). Measured boundary
charge 0.04205/n, flat to 5 digits at the certified optimizers.
**RESTATEMENT 7: "independent noise copies" is LOAD-BEARING, not
decorative** -- correlating them BREAKS (A) outright (tiled rate
0.7987/0.9218/1.3977 vs phi_5 = 0.7757 at cross-block noise
correlation 0.3/0.6/0.9). State as a hypothesis of the construction.
**(B)(i) CONVEXITY: PASS** (69 Jensen points + 40 curvature lines,
0 violations; tested on the CYCLOSTATIONARY class the argument
actually touches, not just the stationary one). **The l.s.c. "soft
spot" is a RED HERRING** -- attainment is never invoked; (B)
produces ONE EXPLICIT stationary record per n and the infimum
comparison follows by definition. **RESTATEMENT 5: delete "attain".**
**RESTATEMENT 4: (R1) must be a stated LEMMA, not a citation of
Theorem C** -- F_T convex on the linear section, F_T/T -> rate
pointwise on records with spectra bounded above and away from 0,
and pointwise limits of convex functions are convex.
**(B)(ii) REALISABILITY: PASS, CONSTRUCTIVELY.** Cone membership is
automatic with a named reason (the kernel-dispersion term is a
variance, hence PSD, and it is what makes the inequality strict);
the verifier BUILT the record (Abar = diagonal-average of A, Gammabar
= period-average, noise spectrum explicit). **No schedule leak**:
on Z the schedule IS shift-invariant, the finite-n truncation
appears only on the <= side of (A). Executed at the certified
optimizers: shift-averaged stationary records at 0.5631757405 /
0.5629264128 / 0.5628390620 (n=8/12/16), distortion preserved to
machine precision, converging from ABOVE like C/n^2. 8/8 adversarial
edge cases (near-deterministic noise, sign-alternating kernels,
rank-2 noise, strictly anticausal Av) hold with cone margin >= 0.2.
**THE CENTRAL FINDING -- MY OWN ATTACK: THE CHAIN IS
ONE-DIRECTIONAL.** Every step is an inequality the SAME way and
each produces an explicit feasible object:
phi_n >= rate(periodize) >= rate(shift-average) >= Psi(D).
So it yields **L^inf >= Psi(D)** and CANNOT yield L^inf <= Psi(D).
**The recorded line "(A)+(B) => phi_n >= Psi => L^inf = Psi"
contains a NON-SEQUITUR at the second arrow.** The converse needs an
unwritten truncation/achievability lemma (and the stationary optimum
is NOT rational at any finite order, so the FIR-density step is not
free -- and it is a boundary-charge argument again, in the other
direction).
**CONSEQUENCE: the PLATEAU SURVIVES (it is a LOWER bound) but
"IDENTIFIED" DIES.** Permitted headline: **L^inf(0) in [0.5627265,
0.5647420]** -- an unconditional-modulo-(R2) bracket of width
2.0e-3, lower end from the bypass, upper end the certified n=32
anchor. A seal printing "the process limit is IDENTIFIED" or
"L^inf = Psi(D)" MUST FAIL.
**AND "NO HYPOTHESIS AT ALL" ALSO DIES (restatement 3).** The
bypass removes (H*), (H**), (H***), (D), (F) and the boundary
charge -- a real, large advance -- but REPLACES them with (R1)
convexity of the process rate and **(R2) global optimality of the
stationary program**, which is currently a FLOATING-POINT
certificate: interior stationarity verified in 12 moment directions
(|grad J| <~ 2e-6, curvature +1.3e3..+1.5e4, no descent on any
line), NO interval arithmetic, and **executed at Delta=0 ONLY**.
A SIXTH independent validation of the value arrived en route: the
verifier's window-Cholesky re-evaluation of the fixed point gives
0.5627264963 (4.0e-11 from the prover's Toeplitz-innovation solve,
a completely different numerical route) at distortion 0.3 to
5.6e-14, and grid-independent (Nf 1024/P 60 identical to 10 digits).
**NEW DECOMPOSITION (worth keeping): the O(1/n) drift splits exactly
into the two bypass steps** -- n(phi_n - Psi) = 0.0645 = 0.0420
(periodization/boundary) + 0.0225 (cyclostationarity) + residual.
**The entire (H*)/(H**)/(H***) machinery was fighting only the first
65%.**
**RESTATEMENT 8: c(0) is [0.06447, 0.06449], NOT 0.064495 +/- 3e-5
relative** -- the sequence is monotone decreasing over n=8..48 with
spread 3.0e-4 relative (10x the quoted band); 0.064495 is simply the
n=32 point; Richardson(32,48) = 0.064471.
**RESTATEMENT 9 -- ARTIFACT HYGIENE: validation (4) is TRUE ON
SUBSTANCE but its committed artifact is NOT REPRODUCIBLE.**
spectral/transfer.log reports a flat 6.76e-2 defect at every row and
every n with NO boundary layer; the verifier's rerun gives a clean
boundary layer (4.20e-2, 1.40e-2, 4.90e-3, 1.66e-3, then 9.5e-4
bulk, halving to 4.7e-4 at n=32 -- genuinely O(1/n)). The 6.76e-2 is
exactly |a_v(+1) - a_v(-1)|, an Av LAG-ORIENTATION MISMATCH that
swamps the real signal. Regenerate before citing. Also: direct.log
is TRUNCATED mid-run at Delta=2, and the internal check
"blk + leak = L" is an ALGEBRAIC IDENTITY, not an independent
validation -- stop citing it as one.
**RESTATEMENT 10 -- Delta SCOPE:** the independent re-evaluation and
the stationarity probe were executed at Delta=0 ONLY. Delta=1,2
carry constructive UPPER bounds only (Psi(1) <= 0.5364993215,
Psi(2) <= 0.5311645087, both ~1.1e-4 above the claimed values), and
the Delta=2 margin 7.96e-4 is the SMALLEST IN THE CAMPAIGN -- do not
promote it ahead of a two-sided stationary certificate at Delta=2.
**SEAL-ABLE NOW unchanged: the Collapse identity (w/ restatement 6),
step (A) in full (w/ restatement 7), the stationary K1-K3 table, the
mechanism corollary, the rho* refutation. SEAL-ABLE with
restatements 1-5, 8, 10: step (B) as a theorem and the corollary
L^inf(Delta) >= Psi(Delta) for Delta=0,1,2. NOT SEAL-ABLE: "no
hypothesis at all" and "L^inf = Psi / IDENTIFIED".**
**HIGHEST-LEVERAGE NEXT STEP, AND IT IS NOW SMALL: two-side Psi(D)
with a per-frequency Lagrangian + moment-box bound at Delta=0,1,2.**
The stationarity probe says the POINT is right; what is missing is a
BRACKET. With it, (R2) collapses and the plateau genuinely becomes
unconditional at +0.0147817 / +0.0040584 / +0.0007960 -- 9.1x the
current margin, reaching two lags the transfer route could never
reach.

## PSI-BRACKET PROVER (2026-08-07): TWO-SIDED CERTIFICATES AT Delta = 0, 1, 2 -- (R2) COLLAPSES STRUCTURALLY

**THE CERTIFICATE NEEDS NO OPTIMALITY CLAIM.** Weak duality gives
Psi(D) >= inf_x [rate + mu(dist - D)] for every mu >= 0; a
SUBGRADIENT at an ARBITRARY point plus an explicit moment box bounds
that infimum below. So the whole of (R2) -- "global optimality of
the stationary program", previously a floating-point stationarity
probe in 12 directions at Delta=0 only -- is GONE, replaced by two
checkable lemmas. Control H proves the point structurally: with mu
scaled x0.5..x2.0 or the anchor perturbed by 1e-4..1e-2, the bound
degrades (to 0.1377 or negative) but is NEVER invalid and never
exceeds Psi_UB. The KKT solve only makes it TIGHT, not valid.
**THE MINORANT (the key device).** Freeze the leak's inner filters
at any admissible (C0 monic causal in S, B0 causal-incl-lag-0 in R):
shat(x) = <|C0|^2 f_S + |B0|^2 Gamma + 2Re(C0bar B0 h1)> is AFFINE
in x and shat >= s ALWAYS, so
J^-_mu(x) = alpha[<ln M_Q> - <ln n>] + alpha[<ln f_S> - ln shat(x)]
+ mu(dist(x) - D) <= rate(x) for every feasible x and mu >= 0.
**THE ONLY CONVEXITY INPUT is Lemma C-stat**: per frequency,
ln(Gamma - hQh*) - ln(Gamma - hPh*) with P - Q >= 0 is jointly
convex -- **the SCALAR INSTANCE of the already-proved 074 lemma**
(it equals -ln(1-Z), Z = hRh*/M_Q). Everything else is elementary
(-ln(affine) convex; dist affine). **NO process-rate convexity, NO
concavity of s, NO attainment, NO lower semicontinuity, NO
differentiability, and NO optimality of the anchor.**
Structural facts used: Sig_W^-1 Sig_WS = e1 EXACTLY (Theorem K's
first fact, re-verified 2.4e-15), so **Q = diag(1/f_S, 0), rank-one
diagonal**; R = P - Q positive definite in CLOSED FORM (det R =
(1/f_V - 1/f_S)/s_N^2 > 0); Delta enters ONLY as the phase z^{Delta+1}
on h. Lemma S (evaluation) via Collapse + Wiener-Masani/Szego, with
<ln f_S> = ln(tau^2 a/lambda_s) = -0.1025391956 in CLOSED FORM (grid
agrees 2.8e-16).
**THE MOMENT BOX, explicit** (Holder in the L1/L-infinity pairing --
**an L2 box FAILS here: the distortion constraint controls <Gamma>,
NOT <Gamma^2>**; worth a numbered remark): <Gamma> <= (1+sqrt D)^2 =
2.395445115 (Minkowski); <|Phi_RV|>, <|Phi_RY|> <= 1 + sqrt D =
1.547722558 (pointwise + integral Cauchy-Schwarz, <f_V> = <f_Y> = 1).
**Far tighter than the finite-n box** (sqrt(nD) -> sqrt D per
symbol). FREE STRUCTURAL CHECK found en route: **<Gamma_p> = 1 - D =
0.7 EXACTLY at all three Delta** -- the optimum is a proper test
channel (E[Yh^2] = E[Yh Y]).
**CERTIFIED BRACKETS (min-LB / max-UB over Nf in {1024,2048,4096,
8192} x P in {60,100,140,200}):**
  Delta=0: [0.562726496337, 0.562726496340] w 3.20e-12, bar
    0.5479448, **margin +0.014781696337**
  Delta=1: [0.536401378468, 0.536401378471] w 3.79e-12, bar
    0.5323430, **margin +0.004058378468**
  Delta=2: [0.531050019848, 0.531050019852] w 4.31e-12, bar
    0.5302540, **margin +0.000796019848 = 1.85e8 BRACKET WIDTHS**
theta = 3.086038362097/3.130079068857/3.151357871769, identical to
12 digits across the whole grid family. **The Delta=2 requirement
(bracket well under 7.96e-4) is met by EIGHT ORDERS, not
marginally.** QUOTABLE FORM (rounded outward at 1e-10 per the 079
house convention, so widths exceed f64 round-off by ~7 orders):
Psi(0) in [0.5627264963, 0.5627264964]; Psi(1) in [0.5364013784,
0.5364013785]; Psi(2) in [0.5310500198, 0.5310500199].
DISCRETIZATION/TRUNCATION: LB spread over the grid family
4.0e-13/1.4e-12/7.7e-13, UB spread <= 6.7e-16; integrands analytic
and periodic so the rectangle rule is spectrally accurate
(confirmed, not assumed); **lag truncation is on the SAFE side for
the LB** (a truncated filter is admissible, shat >= s, so it can
only loosen); ||g||_inf is resolved (flat across the family) and
even a 1000x underestimate leaves 2e5 of Delta=2 margin. Floating
point, no interval arithmetic (house convention).
CROSS-CHECKS, all consistent: the R-IND-5 verifier's INDEPENDENT
window-Cholesky evaluator re-evaluates the certified point to
<= 1.6e-15 at all three Delta; every sealed certified LB(phi_n) sits
ABOVE Psi_UB at n = 8..48, with n(phi_n^UB - Psi_UB) = 0.064535/
0.064516/0.064507/0.064497/0.064495/0.064487 -- **monotone
decreasing, exactly restatement 8's picture, and confirming 0.064495
is merely the n=32 point**; all independent constructive UBs sit
above Psi_UB; a NEW D-ladder (D = 0.26..0.34) sits strictly below
the sealed 081 phi_8(D) LBs, smooth and monotone; 400 random
feasible stationary records per Delta give zero violations (min
slack +0.090/+0.110/+0.116).
SCOPE NOTE: **Delta=2 has NO sealed finite-n anchor** in the
committed artifacts, so its cross-check rests on the window-Cholesky
re-evaluation and the constructive UB, not on a sealed phi_n. A
sealed phi_n bracket at Delta=2 is cheap and owed.
**PERMITTED WORDING NOW:** "Psi(Delta) in [LB, UB] two-sided
certified, Delta=0,1,2"; "L^inf(Delta) >= Psi(Delta) >= LB,
unconditional MODULO (R1) alone" at margins +0.0147817/+0.0040584/
+0.0007960 -- **retiring (H*), (H**), (H***), (D), (F) and the
boundary charge from the plateau, at three lags, two of which the
transfer route provably could not reach**; and "the certificate
needs neither optimality of the fixed point nor differentiability of
the rate functional." **STILL FORBIDDEN, UNCHANGED: "L^inf = Psi" /
"IDENTIFIED" (the chain is still one-directional) and "no hypothesis
at all" -- (R1) and (A)'s independent-noise-copies hypothesis are
untouched by this work. A seal claiming otherwise must FAIL.**
**(R1) IS NOW THE SINGLE REMAINING LOAD-BEARING HYPOTHESIS for the
whole plateau** -- and it is a pointwise-limit-of-convex-functions
statement on the cyclostationary class, a much softer object than
anything the campaign has been fighting.
NEXT: R-IND-5 this certificate (attack list from the prover: the
Q = diag(1/f_S,0) reduction; **the shat >= s DIRECTION -- the one
place a sign slip inverts the bound**; the L1/L-infinity pairing
with the L2-box-invalid remark; the box constants; Lemma S's Szego
hypotheses on degenerate spectra; own-code re-derivation of the
per-frequency cell inf) -> tex v0.7 with Lemma S and Lemma C-stat
numbered -> seal 082 -> governed. Then (R1) as the highest-leverage
prover target, and the owed sealed phi_n bracket at Delta=2.

### Delta=2 anchor gap CLOSED (2026-08-07): certified finite-n brackets at n = 16, 24, 32 -- NO RED FLAGS

The Psi prover's scope note is discharged numerically. Same 079
certify() machinery (cold start, deterministic, ~4.5 min CPU) that
produced the sealed anchors; controls reproduced FIRST.
CONTROLS: (16,0)/(16,1)/(24,0) reproduce the sealed brackets with
every UB within 1.2e-7 of the sealed UB and 6.3e-8 of the R-IND-5
winner (the harness's own gate is 5e-7); LB differences <= 6.9e-7
fully explained by rn ~ 1e-8 (the BLAS gradient-noise floor) times
R_box ~ 183-354. All three overlap the sealed brackets and contain
v*.
**NEW CERTIFIED BRACKETS:**
  phi_16(2) in [0.535891743313, 0.535893963469], width **2.22e-6**
  phi_24(2) in [0.534274270522, 0.534279127269], width **4.86e-6**
  phi_32(2) in [0.533465073456, 0.533471490973], width **6.42e-6**
-- at or BETTER than the sealed-cell width band (3.0e-6..9.2e-6);
nothing had to be disclosed as short. Diagnostics: rn = 1.19/1.28/
1.11e-8; **the NF floor is INACTIVE** (eigmin(N) ~ 0.1404 at all
three n, and eigmax(N) under Theorem K's 1/theta cap -- the
optimizer is interior); dist-D strictly negative so proj_corr = 0
and each UB is a RAW FEASIBLE evaluation; independent evaluator
(repr_bits vs f_and_grad) agrees to 5.6e-16.
GLOBALITY CHECK: a second, unrelated cold start (0.55 I, noise
0.26 I) lands within 5.3e-7 -- inside the certified widths, at all
three n. Consistent with a single global optimum, as Theorem C
requires; no second KKT point.
**CROSS-CHECK vs the Psi certificate: NO VIOLATIONS.** Every
certified LB(phi_n) sits STRICTLY ABOVE Psi(2)'s UB, by 4.84e-3 /
3.22e-3 / 2.42e-3 -- margins ~500-2000x the bracket widths. And
n(phi_n^UB - Psi_UB) = 0.0775031 / 0.0774986 / 0.0774871 against the
recorded 0.077503 / 0.077492 / 0.077485 -- deviations +1.0e-7 /
+6.6e-6 / +2.1e-6, ALL ON THE UPPER SIDE exactly as expected since
the UB carries a few x1e-7 of slack, and **monotone decreasing in
n** as restatement 8 requires. Second independent cross-check: the
COMMITTED results/GO14-process-limit.json value s4_fs16_D2 =
0.5358939351814885 lies strictly inside the new (16,2) bracket.
**RED FLAGS: NONE.** No LB fell below Psi(2)'s UB at any n; the
n-scaling matched and stayed monotone; the NF floor is inactive; two
cold starts agreed inside the widths; controls reproduced against
both the 079 JSON and the R-IND-5 width-of-record brackets.
**BOOKKEEPING NOTE for the 082 write-up:** the (16,0) bracket
[0.566754682, 0.5667581350] used in several briefs is the R-IND-5
**width-of-record** bracket [v* - 3.45e-6, v*], NOT the
results/GO14-convexity.json bracket. Both are valid records of
different things; **082 must use ONE convention consistently and say
which.**
STATUS: the gap is discharged NUMERICALLY. Sealing it is a
registration act -- 082 should carry these three cells so the
Delta=2 plateau claim rests on a sealed finite-window cross-check
rather than on the window-Cholesky re-evaluation and the
constructive UB alone. Carried forward unchanged: floating point, no
interval arithmetic; **the LB endpoint is BLAS-sensitive at ~1e-7
through rn*R_box (exactly why the 079 width GATES sit in CI's
artifact-self-consistency tier), so a governed runner must
RE-DERIVE these, never copy them.**

## R-IND-5 ON THE PSI CERTIFICATE (2026-08-07): READY TO SEAL 082 with TEN restatements (R11-R20) -- nothing refuted, but FOUR wrong numbers and ONE false proof-step found

Fresh context, own spectra/solver/gradient/box/dual (structurally
unrelated cell-argmin fixed point, not the K1-K3 filter recursion).
No sign error, no direction error, no counterexample.
**WEAK DUALITY re-derived: PASS.** Link-by-link audit at 363 random
feasible records, all six links, ZERO violations at all three Delta.
COUNTEREXAMPLE SEARCH FAILED (as it should): projected steepest
descent on the true rate along dist=D from the certified point and
from perturbed anchors finds nothing below LB (best = LB + 3.2e-12);
6000 random feasible records incl. deep-notch and tall-spike noise
spectra scored with the UNDER-estimating evaluator, 0 violations;
KKT-free Nelder-Mead/Powell over FIR records, no violation.
**THE MINORANT shat >= s: PASS** over 2880 (record x frozen-filter)
pairs -- 120 adversarial records x 24 filter choices including
foreign optima, truncations to 1/2/5/20 lags, oscillating and
near-unit-root filters. min(shat - s) = -2.2e-16 (machine zero,
attained only when the filter IS that record's optimum).
**R11 -- THE CONTROL THAT GIVES THE TEST POWER: a NON-MONIC C
(C = 0.3) gives shat - s = -0.5447 and INVERTS the bound**, and fed
into the dual it produces "lower bounds" ABOVE the true rate. So
"admissible" is a HYPOTHESIS with content (C monic causal in S, B
causal INCLUDING lag 0 in R), not an adjective.
**Q = diag(1/f_S,0) and det R: PASS** (1.5e-15 / 6.7e-16; det R
verified 5.3e-15 with s_N^2 appearing exactly once -- the verifier's
own first transcription as s_N^4 was ITS error, the probe is right).
R > 0 uniformly (min eigenvalue 3.17e-3).
**R12 -- Lemma C-stat: PASS with a SHORTER PROOF than the 074
citation**: phi(h,t) = hRh*/t is jointly convex (quadratic-over-
linear) and NONINCREASING in t; M_Q is jointly concave; composition
gives Z convex; -ln(1-u) convex increasing finishes. Hypotheses used
are exactly Q >= 0 AND R = P-Q >= 0 -- no lift, no 074. 60000 random
chords with Gamma pushed to 1e-9 of the cone boundary: 0 violations;
CONTROL with Q > P: 12532/20000 violations (worst +13.2), so the psd
hypothesis is load-bearing.
**R13 -- Lemma S: PASS at the certified points, with a mandatory
scope clause.** Identity residuals -2.2e-16/-4.4e-16/-1.1e-15;
<ln f_S> closed form agrees 2.9e-16 across Nf = 256..16384; Szego
CANNOT degenerate on the S side here (f_S in [0.5111, 9.400]). NEW:
on records with a deep narrow notch in n, the FINITE-LAG evaluator
for sigma and s converges very slowly (residual 2.4e-4 at P=50,
still 1.5e-4 at P=1600) -- an EVALUATOR property, not a Lemma-S
failure (P-independent to 4.4e-16 at the anchors), and it does not
touch the certificate, whose leak term is an exact integral of
frozen filters. By-product: rate_blockleak <= true rate <=
rate_collapse there, so the empirical gates used the aggressive side.
**R14 -- A FALSE PROOF-STEP IN THE CODE.** psicert/cert.py
::dual_cells asserts "Hessian >= 2 beta lambda_min(P) I". That is
NOT proved by the stated reason: phi(hRh*) is radially CONCAVE.
Correct argument gives modulus **beta lambda_min(P+Q)** and guard
2|u|^2/(beta lambda_min(P+Q)) -- 3.5% larger here (0.14231 vs
0.14725), numerically inert (guards 1.0e-26 vs 9.7e-27, LB unchanged
to 0.0e+00), but the sentence MUST be replaced.
**MOMENT BOX: PASS; and the "L2 box is invalid" claim CONFIRMED
CONSTRUCTIVELY** -- feasible records at fixed dist and <Gamma> have
<Gamma^2> = 1.667/1.965/2.929/6.770 as the spike narrows (64/16/4/1
bins), i.e. <Gamma^2> DIVERGES; no L2 box exists. Worth numbering.
||g||_inf is genuinely resolved (flat 2.5e-13..4.6e-13 across
Nf = 512..8192). <Gamma_p> = 0.7 = 1-D exactly at all three Delta.
**BRACKETS: PASS on substance**, reproduced digit-for-digit by an
independent solver, and the independent window-Cholesky evaluator
returns 0.562726496340/0.536401378471/0.531050019852 at three
window sizes -- 12-digit agreement.
**R15 -- OUTWARD ROUNDING VIOLATED AT 12 DIGITS**: the quoted LBs
are rounded INWARD (up) by ~4e-13 and the Delta=1 UB inward (down)
by 4e-16. The 10-digit quotable form is correct and safe; fix the
12-digit line or drop it.
**R16 -- THE BARS ARE WRONG, AND ONE ERROR IS NOT CONSERVATIVE.**
psicert used BAR = {0.5479448, 0.5323430, 0.5302540}; the SEALED
causal-spectral values (results/GO14-process-limit.json s6_cand)
are 0.5479447799144537 / 0.5323438832146611 / 0.5302532008457406.
**The recorded Delta=1 margin +0.0040584 is 8.8e-7 TOO LARGE**
(Delta=2's is 8.2e-7 too small, conservative). CORRECT MARGINS:
**+0.0147817164 / +0.0040574952 / +0.0007968190.** All three still
clear by 4-8 orders over the bracket width; no verdict moves.
**R17 -- STATE THE CERTIFICATE VIA THE BOX-FREE PER-FREQUENCY DUAL,
NOT THE BOX.** The dual is valid for ANY mu with beta > 0, ANY
admissible frozen filters, ANY linearisation point: 25 random
NON-OPTIMAL anchors per Delta give valid bounds, and truncating the
frozen filters to 12/4/1 lags loses 0/3.6e-6/1.08e-2 -- it survives
brutal mistreatment. The BOX route does not (1e-4 anchor
perturbation collapses it to 0.1377). Both agree at the anchor.
**AND THE DUAL NEEDS NO CONVEXITY OF J^- AT ALL** (separability
replaces the tangent) -- Lemma C-stat is then used only to COMPUTE
each cell infimum reliably, not to establish validity. **A genuine
STRENGTHENING the seal should claim.**
**R18 -- Delta=2 HAS NO HEADROOM IN THE CERTIFICATE'S TUNING**:
mu x0.95 -> margin -2.4e-5; mu x1.10 -> -2.2e-3; shat linearisation
+/-5% -> -4.9e-5/-1.7e-4. Validity never lost, only margin. Record
it: Delta=2 is the campaign's smallest margin.
**ATTACK (c) "does it prove too much?": NO.** The identical
machinery on the BLOCK program (se == n; no leak, so the cell dual
needs NO ANCHOR AT ALL) gives UB = LB = 0.5299499808119 against the
recorded block_inf 0.5299499808 -- agreement 1.2e-11, and it does
NOT produce a value above the independently known answer. Full
Delta-ladder 0..9 matches the recorded ladder at every Delta, with
LB(9) - block_inf = +7.3e-10 >= 0: the machinery approaches the
known value FROM ABOVE and never crosses.
**ATTACK (d) Delta=2 independent route: PASS** -- window-Cholesky
0.531050019852 at three windows; and rind5B/opt_16_2.npz IS a
certified finite-n anchor at Delta=2 ([0.5358908014, 0.5358939352],
LB > Psi_UB(2), n(phi_n - Psi) = 0.077503). The probe's scope note
was literally true ("not in the COMMITTED artifacts") but the
cross-check is stronger than recorded.
**R19 -- THE O(1/n) CONSTANT IS Delta-DEPENDENT**: n(phi_16 - Psi)
= 0.064507 / 0.070483 / 0.077503 at Delta=0/1/2. Restatement 8's
c(0) in [0.06447, 0.06449] is a **Delta=0 statement** and must never
be quoted or reused as Delta-uniform.
**R20 -- ERRATUM: results/GO14-process-limit.json s6_block_inf =
0.529949985183839 is HIGH by 4.4e-9.** The anchor-free two-sided
certificate pins **block_inf in [0.5299499808, 0.5299499809]**; use
0.5299499808119 (a new and tighter number than addendum 1's).
**ATTACK (e) truncation: PASS** for the LB (a truncated filter is
admissible so shat >= s and the LB only loosens). **CAVEAT for the
UB, not the LB**: the rate evaluator's s is itself P-truncated, so
the computed rate UNDER-states the true rate -- the wrong sign for
an upper bound. Flat to 4.4e-16 at the anchors over P = 50..1600, so
the UB is safe; STATE THE SIGN.
**EXACT PERMITTED WORDING (082):** "Psi(Delta) in [LB, UB],
two-sided certified (floating point, house convention), with LB from
a per-frequency weak-duality bound requiring no optimality of the
fixed point, no convexity of the process-rate functional, and no
differentiability: Psi(0) in [0.5627264963, 0.5627264964], Psi(1) in
[0.5364013784, 0.5364013785], Psi(2) in [0.5310500198,
0.5310500199]." And: "L^inf(Delta) >= Psi(Delta) >= LB,
unconditional MODULO (R1) ALONE, where (A) is instantiated by the
independent-noise-copy periodization, at margins **+0.0147817 /
+0.0040575 / +0.0007968**." And: "(R2) is DISCHARGED: global
optimality of the stationary program is no longer required anywhere
in the plateau chain."
**STILL FORBIDDEN, unchanged: "L^inf = Psi", "IDENTIFIED", "no
hypothesis at all". ADDITIONALLY FORBIDDEN: presenting the BOX bound
as the certificate without R17; any margin computed against
0.5323430 / 0.5302540; any claim of a Delta-uniform O(1/n)
constant.**
The four numeric corrections (R15, R16, R19, R20) and the one
proof-step correction (R14) are EDITS, not re-runs -- no computation
repeats. **(R1) is confirmed as the single remaining load-bearing
hypothesis and the highest-leverage next target.**

### Psi-certificate verifier, final two attacks (same day): THREE independent searches fail, and the sign-slip failure mode is LOUD, not silent

**T13 -- KKT-free adversarial search, independent of the fixed
point.** Nelder-Mead + Powell over FIR record parametrizations, 6
restarts per Delta, all constrained to dist = 0.300000000: best
feasible rates found are 0.630606482560 / 0.677990215830 /
0.673693618992 against certified LBs 0.562726496337 /
0.536401378468 / 0.531050019848 -- clearances +6.8e-2 / +1.4e-1 /
+1.4e-1, no violation. **Combined with the projected steepest
descent from the certified point (best = LB + 3.2e-12/3.8e-12/
4.3e-12) and the 6000 random feasible records, THREE INDEPENDENT
SEARCH STRATEGIES FAIL to find a feasible record below the LB.**
**T14 -- THE DETECTOR HAS POWER, and the sign slip is LOUD.** Feed
a deliberately INADMISSIBLE (non-monic) frozen filter into the same
dual so that shat < s: C x0.6 gives shat - s = -0.5488 and returns
"LB" = **1.271551022522**; C x0.3 gives -0.7642 and returns
**1.958937356731** -- both EXCEED the true rate by 2.3-3.5x.
**So a sign slip at the shat >= s step does NOT produce a
plausible-looking number: it produces a bound several times the true
rate, immediately visible against any upper bound.** That RETIRES
the Psi prover's own stated worry ("the one place a sign slip
inverts the bound" would have been caught on sight) and independently
confirms R11 -- monicity of C is a HYPOTHESIS, not an adjective.
Total independent compute ~50 min across seven scripts, all
deterministic, scratchpad only. **Verdict unchanged: READY TO SEAL
082 with R11-R20.**

## (R1) PROVER (2026-08-07): (R1) IS A THEOREM -- proved by a route that DISCHARGES all three recorded steps rather than repairing them; step (B) FULLY discharged

**THEOREM (R1).** Fix a period n, a lag Delta (indeed any n-periodic
nondecreasing schedule), and constants eps > 0, M < infinity. On the
convex set K_n(eps,M) = {(h,Gamma) in L_n : Gamma <= M I,
n(w) := Gamma - h P h* >= eps I a.e.} -- where L_n is the LINEAR
space of period-n bi-infinite moment kernel pairs -- the process-rate
functional is finite and JOINTLY CONVEX. K_n is convex (Gamma <= MI
linear; n(.) matrix-CONCAVE so {n >= eps I} convex) and **carries NO
WINDOW LENGTH ANYWHERE**.
PROOF, four steps, each certified:
(0) Collapse + shifted frame: Delta enters as a UNIMODULAR PHASE on
h -- a linear invertible change of coordinates, so convexity is
Delta-INDEPENDENT (12 cells vs the R-IND-5 verifier's own CMI
evaluator, worst 1.33e-15).
(1) BLOCKING by n makes (S_b, R_b) a STATIONARY 2n-variate process;
Cholesky of its one-step block innovation in the within-block order
reproduces the process pivots exactly.
(2) MATRIX SZEGO (Wiener-Masani) -- **the ONLY analytic input** --
gives the identity the whole proof rests on: 2ln2 n rate =
<lndet M_Q - lndet n> + <lndet Phi_S> - sum_i ln s_i, i.e.
(I) convex + (II) constant - (III) convex. Certified over 36 records
(tiled/shift-averaged/chord, n in {2,3,4,6}, Delta in {0,1,2}):
Gamma - hPh* = Phi_Z to 3.6e-14; Szego legs to 5.4e-11/1.8e-10; full
identity 1.8e-10 (machine precision at n >= 3; n=2 is block-lag
truncation, not identity, limited).
(3a) (I) CONVEX per frequency: -lndet(I - Z) with Z = R^{1/2} h*
M_Q^-1 h R^{1/2}; matrix quadratic-over-linear is jointly
matrix-convex and Loewner-nonincreasing in its denominator, M_Q is
jointly matrix-CONCAVE (this is where Q >= 0 is used), composition
gives Z matrix-convex, and -lndet(I - .) is convex nondecreasing on
0 <= Z < I. **4200 chords, blocks n = 1..8, Gamma pushed to 1.9e-14
of the cone boundary: ZERO violations.**
(3b) (III) CONVEX -- **THE LOAD-BEARING NEW STEP**: s_i is an INF OF
AFFINE functions of (H, Gamma) -- each frozen causal predictor gives
an exactly affine shat, linear in H **because A_u = 0** -- so s_i is
CONCAVE, bounded in [tau^2, Var(S)], and -ln s_i is convex. **This
is exactly Definition def:adm + R11, which the tex already contains
but uses ONLY inside the Psi certificate.** Certified by 1080
PER-INSTANCE concavity certificates with all three links separate
(affineness 4.4e-16; shat(mid) = s(mid) 4.4e-16; shat >= s at both
endpoints with slack >= 0 exactly; margin >= +1.80e-5). **CONTROL: a
predictor peeking 2 slots ahead (inadmissible) BREAKS 286/288
instances, worst -0.294 -- the test has power.**
**STEP (B) FULLY DISCHARGED, and the class restriction is FREE.**
Corollary (Theorem B, unconditional): the n shifts have equal rate,
the average lies in K_n, is stationary, has identical per-symbol
distortion, and has rate <= the average = the original.
**SCOPING LEMMA: the class restriction is AUTOMATIC.** Step (B) is
only ever applied to step-(A) periodizations with independent noise
copies, whose blocked noise spectrum is CONSTANT in w; their shifts
conjugate it by a block cyclic shift that is UNITARY on |z| = 1, so
the eigenvalues are the same at every frequency and one
(eps, M) serves the whole orbit and its convex hull. N > 0 is
w.l.o.g. (convex program + Slater; inf over a convex set = inf over
its relative interior). Certified: eigenvalues equal to 5.6e-16 at
all w and all k; shift-average floor exceeds eps with slack
>= +6.8e-2.
**VERDICTS ON THE THREE RECORDED STEPS:** (i) "linear section" TRUE
but USELESS (the right object is window-free); (ii) "F_T/T -> rate"
is a GENUINE GAP -- F_T is a DIFFERENT functional (truncated
schedule, no pre-window past, truncated W) and its convergence needs
its own boundary-charge argument the campaign does not have;
MEASURED true (T(F_T/T - rate) flat to 5-6 digits from T = 2n) but
**measured is not proved -- and THIS ROUTE DOES NOT USE IT**;
(iii) "pointwise limit of convex functions" BREAKS EXACTLY WHERE
EXPECTED -- the domain D_T MOVES WITH T (different ambient space at
each T), so the statement is ILL-POSED as recorded; repairable by
pulling back along the linear restrictions, but only GIVEN (ii).
**This route eliminates both.**
NUMERICS (~75 min, deterministic): T1 2352 chords rate-convex 0
violations (and separately piece (I) convex, the leak sum concave,
and s_i concave POINTWISE, 0 violations each); T2 576
shift-averaging orbits 0 violations with 2880 second differences all
positive; T5 4200 matrix C-stat chords 0; T7b 126 cross-period
chords (lcm to 24) 0; **T8: Nelder-Mead MAXIMISING the Jensen gap
over 6 runs x 3 restarts x <=1600 evals FAILED TO FIND A VIOLATION**
(best gap -2.39e-2). Adversarial coverage: near-cone-boundary
(lambda_min(N) ~ 1e-6), deep-notch spectra evaluated EXACTLY by
Cholesky pivots (not the finite-lag evaluator whose Lemma-S caveat
applies), sign-alternating kernels, near-deterministic and
large-gain records. T6a reproduces the recorded step-(B) values at
ALL FIVE certified optimizers to <= 4.5e-11.
**A MATERIAL BUG IN EARLIER TOOLING FOUND AND FIXED: np.roll of the
window matrices is NOT a shift** (Sigma_V is Toeplitz, not
circulant), so a rolled record's derived noise is not the rolled
noise and can leave the cone. With genuine shifts, shift-invariance
of the rate holds to <= 1e-12 -- it did not before.
**TWO CORRECTIONS FOR THE TEX:**
1. **R12 IS OVERSTATED.** The tex calls Q >= 0 and R = P-Q >= 0
   "both load-bearing (R12)", but the recorded control (Q' = 1.3P)
   only breaks R >= 0. An independent control Q'' = -0.2I (so
   Q NOT >= 0 but R >= 0) gives **0 violations in 4200 chords**,
   while Q' = 1.3P gives 177/1280 (worst +2.33). So Q >= 0 is a
   hypothesis OF THIS PROOF ROUTE (it is what makes M_Q concave),
   NOT a demonstrated necessity of the statement. Soften.
2. **NEW, worth numbering: F0 IS LOAD-BEARING FOR THE COORDINATES
   THEMSELVES.** Outside F0, two records with IDENTICAL (H, Gamma)
   (to 4.4e-16) have rates differing by up to **0.136 bits**. So
   "convex in the moment coordinates" is not even WELL-POSED outside
   F0 -- a sharper form of the existing non-conflation rule, and the
   exact place it enters is the leak leg Cov(R,S) = H Sig_W^-1
   Sig_WS.
**WHAT 083 CAN CLAIM: cor:onedir becomes UNCONDITIONAL** --
L^inf(Delta) >= Psi(D;Delta) >= LB with NO (H*), (H**), (H***), (D),
(F), no boundary charge, **no (R1), no (R2)**; margins unchanged at
+0.0147817164/+0.0040574952/+0.0007968190. **AND PAST (IC) TOO**:
the independent-copies clause is a SPECIFICATION OF AN OBJECT WE
CONSTRUCT, not an assumption about anything unknown -- R7 survives
as a WORDING RULE (the tiling must be specified with independent
copies, never left implicit), not a live hypothesis. Standing scope
that remains: the family F0 (a DEFINITION), the floating-point house
convention on the Psi bracket, and the sealed Collapse/
Wiener-Masani analytic inputs. **UNCHANGED PROHIBITIONS: "L^inf =
Psi", "IDENTIFIED", any reverse inequality. Permitted headline stays
L^inf(0) in [0.5627265, 0.5647420].**
NEXT: R-IND-5 with four named targets -- (a) the block-innovation
Cholesky claim; (b) **the MATRIX Szego step at n > 1, the only
analytic input and the only place a hidden hypothesis could sit**;
(c) the inf-of-affine representation of s_i incl. the
dense-subspace/closure point; (d) the eps-floor Scoping Lemma. Then
tex v0.8 -> 083, **registered SEPARATELY from the Psi certificate
(082): they are structurally independent**. Novelty sweep OWED on
the combination (blocked cyclostationary Szego + inf-of-affine leak
+ matrix quadratic-over-linear giving convexity of a
causally-conditioned process-rate functional in spectral moment
coordinates) against Wiener-Masani/Helson-Lowdenslager and the
070/073 conditional-RDF attributions. The REVERSE inequality
(truncation/achievability) is untouched and still open.

## R-IND-5 ON (R1) (2026-08-07): PASS on all four named targets and all five independent attacks -- READY TO SEAL 083 with R21-R29

Fresh context, own CMI-definition evaluator built from the
independent primitives (V,N,U,Z); no prover code reused for any rate
number. Calibration first: CMI vs Collapse 8.88e-16 over 18 cells.
**(a) BLOCK-INNOVATION CHOLESKY: PASS** (pivots 1.75e-15; lndet
Lambda 1.78e-15; the identity itself 1.33e-15 over 24 cells).
**R21 -- A FRAME/ORDER COLLISION FOUND, AND IT IS THE ONE PLACE A
SILENT WRONG THEOREM IS AVAILABLE.** The PROBE states within-block
order S_1,R_1,...,S_n,R_n, which requires R_u = Yh_{u-Delta}; the
TEX uses R_u := Yh_{u-Delta-1} (which is what produces the phase
z^{Delta+1} and Lemma S), requiring the OPPOSITE order
R_1,S_1,...,R_n,S_n. Each is internally correct; **MIXING THEM
SILENTLY RETURNS THE LAG-(Delta+1) RATE** -- measured errors up to
**-7.64e-2 bits**. Frame and order must be printed AS A PAIR.
**(b) MATRIX SZEGO: PASS, and the n=2 question is SETTLED AS
TRUNCATION.** The verifier replaced window-extraction spectra with an
EXACT ALIASING route plus exact finite-support blocked transfer
functions -- zero block-lag truncation -- and the identity holds to
**3.55e-15 at Nf=4096, INCLUDING at n=2**. The prover's 1.8e-10 is
its DMAX, quantitatively: the chord sweep decays geometrically at
a^{2n} (n=2: 1.9e-3 -> 2.0e-10 -> 1.6e-13 at DMAX 2/20/28).
**R22 -- THE eps FLOOR IS NOT A HYPOTHESIS OF THE SZEGO STEP.**
Wiener-Masani needs only Phi >= 0 with lndet Phi in L^1; verified on
the extremal family f = |1 - c e^{-iw}|^2 up to and INCLUDING c = 1
(spectrum VANISHING at a frequency), residual <= 2.7e-14. The
floor's real jobs are keeping K_n convex and closed, keeping the
functional finite, and giving the Scoping Lemma one class for the
whole orbit. Do not write that the analytic input requires it.
**(c) INF-OF-AFFINE: PASS** (900 per-instance certificates; links
4.44e-16; min slack +9.90e-6; margin +1.909e-5; min s = 0.421289
against the tau^2 = 0.4 floor). **CONTROL: the peeking predictor
breaks 240/240 -- 100%, vs the prover's 286/288.** Closure: shat
converges to s monotonically and geometrically, machine zero by
depth 32.
**R23 -- SPLIT THE s-LEMMA IN TWO.** (i) An inf of affine functions
over ANY index set is concave -- no density, no continuity, no
topology. (ii) The closure argument is needed ONLY to identify that
inf with s. Truncating the family gives a DIFFERENT function that is
still concave (0/180). The single-sentence phrasing invites the
reader to think concavity is at risk; it is not.
**(d) SCOPING LEMMA: PASS**, with a convention correction.
Unitarity 2.26e-16; eigenvalue invariance 5.55e-16; convex-hull
floors +0.09..+0.69 (prover: >= +6.8e-2); "N > 0 w.l.o.g." confirmed
(the rate BLOWS UP at the cone boundary -- 0.383 -> 11.224 as
lambda_min(N) goes 1e-1 -> 1e-8, so the boundary is never active).
**R26 -- THE CONJUGATION HAS A SIDE AND A SIGN**: the correct
statement is Phi^{(k)}(theta) = **U_k(theta)* N U_k(theta)** with
wrapped entries carrying **e^{+i theta}** (residual 1.14e-16); the
other three sign/side combinations are FALSE BY O(1) (2.98e-1,
4.12e-1).
**MY OWN ATTACKS -- ALL FAILED TO BREAK IT.** (1) Jensen hunt: 0
violations over 1944 random chords (adversarial: lambda_min(N)=1e-6,
notch 1e-3, sign-alternating, near-deterministic), 0/2160 second
differences, 0/60 non-staircase schedules, 0/108 cross-period
chords, window-length independence flat to 1e-15 from B=16; **and a
Nelder-Mead MAXIMISING the Jensen gap over 24 runs x <=2500 evals
reached -1.62e-6 -- FOUR ORDERS closer to zero than the prover's
-2.39e-2 -- and STILL NEVER CROSSED.** (2) Delta-as-phase: genuine
invertible coordinate change (time-domain shift reproduces the
lag-(Delta+1) value to 2.61e-12; K_n maps ONTO K_n because n =
Gamma - hPh* is invariant under h -> z^k h). Caveat recorded: the
shift DOES move the distortion functional, so Delta-independence is
a statement about the OBJECTIVE's convexity, not a common feasible
set. (3) **DOES IT PROVE TOO MUCH? NO -- and the check is sharp:**
the same inf-of-affine lemma applies verbatim to sigma_t and nu_t,
so BOTH legs are concave and **the lemma ALONE proves nothing**; the
rate is NOT concave (concavity fails 135/135, max -5.17e-2).
**THE REGROUPING IS THE PROOF.** In the RECORD-parameter chart the
same functional is NON-convex (1206/3960 negative second
differences, worst -1.255; directed search reaches -23.4) -- **the
moment chart is load-bearing**, and the argument correctly refuses
there. Lemma C-stat with R not psd: 165/645 violations. Per-cell
convexity is NOT implied. (4) **THE np.roll FIX IS CORRECT**:
shift-invariance 3.33e-16, BETTER than the claimed 1e-12. **R27 --
SCOPE THE BUG**: it is a MOMENT-COORDINATE bug (27/27 rolled (H,
Gamma) leave the cone); in RECORD coordinates the roll is wrong by
only <= 4.3e-9, so pre-fix record-space numerics are neither over-
nor under-condemned. (5) Both prover corrections UPHELD:
**R24 -- R12 softening CONFIRMED WITH WIDER EVIDENCE: 22,000 chords
across four non-psd-Q families with R psd give ZERO violations,
while the R-breaking control gives 165/645 and 185/505 on a second
seed.** R >= 0 is demonstrated necessary; **Q >= 0 is a hypothesis
of the PROOF ROUTE, not of the statement.**
**R25 -- "0.136 bits" IS A LOWER BOUND**: the verifier reproduces
**0.1383 bits** at (H,Gamma) identical to 8.9e-16. Print "at least
0.136", never as a maximum; name the entry point (the leak leg).
**R28 -- FULL-PERIOD READS ARE PART OF THE DECOMPOSITION**: the
legs are individually well-defined only at per = n (sum_j ln s_j is
offset-invariant to 8.88e-16 over a full period, NOT over
sub-periods).
**R29 -- NEW, A STRENGTHENING NOBODY ASKED FOR: at the BLOCKED
SPECTRAL level lambda_min(R(w)) = 3.172e-3 UNIFORMLY in w and in
n = 1..8, and Q(w) = blockdiag(Phi_S(w)^-1, 0) EXACTLY at every
block size (<= 1.4e-14), with max eig Z < 1 strictly on the class
interior. This SUPPLIES THE n-UNIFORM FLOOR THE TEX EXPLICITLY
DECLINES TO CLAIM, and explains the recorded finite-window decrease
(1.04e-2/5.59e-3/4.43e-3/3.95e-3 at n=8/16/24/32) as CONVERGENCE TO
IT FROM ABOVE.**
**EXACT PERMITTED WORDING: "UNCONDITIONAL" MAY NOW BE PRINTED --
ATTACHED TO THE CHAIN, NEVER TO THE VALUE.** Permitted: "L^inf(D)
>= Psi(D;Delta) >= LB(Delta) for Delta = 0,1,2, with NO (H*), (H**),
(H***), (D), (F), no boundary charge, NO (R1) as a hypothesis (it is
now a THEOREM), and no (R2); margins +0.0147817164 / +0.0040574952 /
+0.0007968190." Scope travelling with it, unchanged: the family F0
(a definition, and by R25 a WELL-POSEDNESS condition on the
coordinates); the independent-noise-copy SPECIFICATION (a
construction choice, stated explicitly -- R7 survives as a WORDING
RULE, not a live hypothesis); the classical Wiener-Masani/Szego
input CITED WITH its non-degeneracy hypotheses, verified to hold on
K_n; and the floating-point house convention on the Psi bracket.
**"UNCONDITIONAL" MUST NOT BE ATTACHED TO THE Psi VALUE** -- that
remains a two-sided CERTIFIED BRACKET under the house convention.
**UNCHANGED PROHIBITIONS: "L^inf = Psi", "IDENTIFIED", any reverse
inequality, "no hypothesis at all"; no margin against 0.5323430/
0.5302540; no Delta-uniform O(1/n) constant; the box bound is
corroboration, never the certificate. The chain remains
ONE-DIRECTIONAL and the headline stays L^inf(0) in [0.5627265,
0.5647420].**
STILL OWED, unchanged: the novelty sweep on the combination
(blocked cyclostationary Szego + inf-of-affine leak + matrix
quadratic-over-linear) vs Wiener-Masani/Helson-Lowdenslager and the
070/073 conditional-RDF attributions. The REVERSE inequality
(truncation/achievability) is untouched and still open.

## (R1) NOVELTY SWEEP (2026-08-07): combination NOVEL, EVERY INGREDIENT STANDARD -- and an ATTRIBUTION GAP FOUND IN-HOUSE (074)

**METHOD LIMITS, on the record first (must travel with any "first"
phrasing):** 26 queries; the arXiv **API returned HTTP 429
throughout**, forcing the HTML search endpoint, which is
**TITLE+ABSTRACT ONLY** -- so this is a **METADATA-LEVEL sweep, NOT
full text**; curl blocked in-environment; **WebSearch budget was
ALREADY EXHAUSTED (200/200) before the sweep started**, so Semantic
Scholar and general-web/Scholar were **NOT RUN**. Two attributions
(Vastola-Poor, Franke) are metadata-confirmed but **NOT
PAGE-VERIFIED**.
**PER-CHANNEL VERDICTS.**
1. Convexity of RD-type functionals in spectral/moment coordinates:
   **ADJACENT-KNOWN.** The existing work convexifies in
   ESTIMATION-ERROR COVARIANCE (Tanaka-Kim-Parrilo-Mitter
   1411.7632; Tanaka CCA 2015 -- the stationary instance, closest in
   spirit; Stavrou-Tanaka-Tatikonda 1711.09853) or in CAUSAL FILTER
   COEFFICIENTS in the time domain (Derpich-Ostergaard 1001.4181).
   R1 convexifies in (h, Gamma) -- cross-spectrum AND record
   spectrum -- a chart in which the record-parameter chart is
   PROVABLY NON-convex by our own evidence.
2a. Blocking cyclostationary -> stationary + spectral evaluation:
   **KNOWN -- cite, do NOT present as the program's device.**
   Kipnis-Goldsmith-Eldar T-IT 2018 (1505.05586) obtains the
   cyclostationary DRF by orthogonalizing over the POLYPHASE
   decomposition. This is our ingredient (a) at the level of
   EVALUATION. Also Abakasanga-Shlezinger-Dabora Entropy 2020;
   Tan-Dabora-Poor 2405.11405 / 2507.00656.
2b. Wiener-Masani/Helson-Lowdenslager used to establish CONVEXITY:
   **NOVEL** ("Wiener-Masani" -> 4 arXiv hits, none about convexity
   of an information functional; "Helson-Lowdenslager" -> 17, ALL
   functional analysis/operator theory, NONE information-theoretic).
   **So the blocking+Szego step is a KNOWN EVALUATION DEVICE; using
   it as the second step of a CONVEXITY PROOF is where nothing was
   found. Write that distinction explicitly.**
3. Inf-of-affine / frozen predictors => concavity of prediction
   error: **KNOWN AT THE CORE -- SAY SO PLAINLY.** This is the
   classical mechanism of minimax-robust prediction (Vastola-Poor
   T-IT 1984; Franke 1985; Franke-Poor 1984): the prediction-error
   variance is concave in the spectral density PRECISELY because it
   is an infimum over frozen predictors of spectrum-linear
   functionals. **The defensible remainder is only the packaging:**
   the causally-conditioned CROSS-record instance
   Var(S_u | S^{u-1}, R^u) as an inf of functionals AFFINE JOINTLY
   in (h, Gamma), with the F0 restriction making the minorant
   linear. **Claim the packaging and the coordinates, NEVER the
   mechanism.** CAUTION: the sweep's nulls here are **ARTIFACTS OF
   THE DATE RANGE** (this literature is 1983-85, pre-arXiv) -- **do
   NOT quote them as a null set.**
4. Convexity of causally-conditioned information functionals in
   spectral coordinates: **ADJACENT-KNOWN.** The Charalambous/
   Stavrou NRDF line (14 items swept) convexifies in the causal
   REPRODUCTION KERNEL -- the definitional convexity that makes NRDF
   computable -- not in spectral moments. **CLOSEST SINGLE ITEM TO
   THE OBJECT, and it is NEW: Zheng-Lamperski arXiv:2512.06238
   (IFAC WC 2026), an explicit formula for the causally conditioned
   directed information rate of Gaussian sequences -- it EVALUATES
   the same species R1 CONVEXIFIES. No convexity claim in the
   abstract; full text unchecked. THIS IS THE PAPER A REFEREE WILL
   RAISE -- page-verify before the tex revision.**
5. Matrix quadratic-over-linear on log-det: **KNOWN. TEXTBOOK.**
   Every step is standard convex analysis: Boyd-Vandenberghe 2004
   Sec 3.1.7 (matrix fractional) + 3.2.4 (composition), and Ando
   1979 (operator concavity). The arXiv nulls here reflect that this
   is textbook material never posted -- **do NOT report them as
   novelty evidence.**
**ATTRIBUTION GAP FOUND IN-HOUSE (must fix):** the sweep grepped
prereg/GO-P-2026-074-go13-m2-convexity.md and
paper/go11-conditional-region-NOVELTY.md and found the 074 lemma
(aa'/s matrix-convex, "Schur-certificate averaging") recorded only
as "the verifier PROVED the assigned lemma" -- **NO EXTERNAL
ATTRIBUTION EXISTS ANYWHERE IN THE PROGRAM FOR IT.** The scalar and
matrix instances are BOTH standard. **074 and the R1 step (3a) that
invokes it must both acquire the Boyd-Vandenberghe / Ando citation
at the next revision; the program's contribution there is the LIFT
INTO THE MOMENT CHART, not the convexity.** Also: **Wiener-Masani
and Helson-Lowdenslager are NAMED in the tex but NOT FORMALLY CITED
-- there is no \cite or \bibitem anywhere in
paper/go14-causal-erasure.tex** (confirmed by grep).
**OVERALL VERDICT: every ingredient is individually standard or
adjacent-known; the COMBINATION and the CONCLUSION are NOVEL,
conservatively scoped** -- no source states joint convexity of a
causally-conditioned, lagged-reference PROCESS rate in SPECTRAL
MOMENT coordinates on a window-free convex set.
**PERMITTED LANGUAGE: "four standard ingredients, combined; to our
knowledge the resulting joint convexity in spectral moment
coordinates has not been stated" -- disclaiming novelty on EACH
ingredient in the sentence that introduces it. DO NOT write "a new
convexity technique" or "novel convexity lemma", and attach novelty
to NEITHER (c) NOR the inf-of-affine mechanism in (d). THE
GENUINELY DEFENSIBLE CLAIM, supported by our own R-IND-5 evidence
and stated by no external source: THE MOMENT CHART IS LOAD-BEARING
-- the same functional is non-convex in record coordinates
(1206/3960 negative second differences, directed search to -23.4) --
so THE CHOICE OF CHART, not the convexity machinery, is the
contribution.** All sweep-level caveats travel with any "first" or
"has not been stated" phrasing.
**CITATION LIST for the next tex revision (10 items):**
Kipnis-Goldsmith-Eldar 1505.05586 (step 1, blocking/polyphase);
Abakasanga et al. Entropy 2020 + Tan-Dabora-Poor 2405.11405 /
2507.00656; **Boyd-Vandenberghe 2004 Sec 3.1.7/3.2.4 and Ando 1979
(step 3a -- AND RETRO-ATTACH TO 074)**; Vastola-Poor T-IT 1984 and
Franke 1985 (step 3b, page-verify first); Tanaka et al. 1411.7632 /
Tanaka CCA 2015 / Stavrou et al. 1711.09853 (adjacent, covariance
coordinates -- one-line distinguish required); Derpich-Ostergaard
1001.4181 (adjacent, filter coordinates);
**Zheng-Lamperski 2512.06238 (adjacent, CLOSEST -- page-verify)**;
Wiener-Masani 1957/58 and Helson-Lowdenslager 1958 (the analytic
input -- cite WITH the non-degeneracy hypotheses per R22).
**TWO FOLLOW-UPS OWED BEFORE ANY NOVELTY SENTENCE IS PRINTED:**
page-verify Zheng-Lamperski for a convexity statement; and re-run
channels 1/3/4 through Semantic Scholar and a full-text engine once
the WebSearch budget resets -- **the 1983-85 robust-prediction layer
and any journal-only convexity result are INVISIBLE to an
arXiv-abstract sweep.**

## ACHIEVABILITY PROVER (2026-08-07): L^inf = Psi NOT LICENSED and NOT PRINTED -- but LEMMA W proved, the converse reduced to ONE residual, and an UNCONDITIONAL 51x BRACKET NARROWING delivered

**THE VERDICT, up front: the equality is NOT licensed.** What is:
**LEMMA W (the window transfer -- NEW, the converse-direction
boundary-charge argument R-IND-5 named as missing).** Any FIR
stationary record converts to a finite-window F0 record at O(1/n)
with an **explicitly n-INDEPENDENT, measured edge charge**:
phi_n <= L_a(x^(n)) <= rate(x) + C(L)/n, C(L) < infinity independent
of n. Steps: (0) Collapse [theorem]; (1) **edge cells contribute
EXACTLY ZERO** to the rate [proved, one line]; (2) interior sigma_t
>= sigma_stat because the window conditioning set is a genuine
SUBSET of the stationary one [proved -- the same structural reason
as step (A) of the bypass, RUN THE OTHER WAY]; (3) sum_t delta_t <
infinity uniformly in n [outline complete + measured exactly; needs
the standard rational-spectral-factorization/Riccati citation --
**the SAME CITATION CLASS as Wiener-Masani in Theorem R1 step (2),
not a new hypothesis**]; (4) **the noise leg HELPS**
(lndet T_m >= m<ln n>) [proved, one line]; (5) distortion
feasibility **discharged CONSTRUCTIVELY** -- window distortion is
exactly affine in a scalar noise rescale, solved in closed form to
12 digits; **Theorem C's convexity repair was available and NOT
NEEDED**.
**STRUCTURAL FINDING WORTH KEEPING: in Collapse coordinates the
converse boundary charge is CHEAP, because the two legs have
OPPOSITE AND BOTH-FAVOURABLE SIGNS** -- the numerator leg is >= 0
but geometrically summable, the noise/lndet leg is <= 0 outright.
**That is why the (H*)/(H**)/(H***) machinery has NO COUNTERPART
here.**
MEASURED (Delta=0): sum delta_t = 0.043994832 **IDENTICAL TO 9
DECIMALS at n=128 AND n=256** -- the edge charge is n-INDEPENDENT,
not merely O(1); per-cell profile geometric at ratio ~0.037, dead at
the f64 floor by the 6th interior cell; the Szego leg is +0.0086 on
the HELPING side, sign as (4) requires. Net edge charge 0.0255 bits.
**THE RESIDUAL -- exactly one thing remains: FIR-KERNEL STATIONARY
RECORDS ARE DENSE IN VALUE (U(L) decreasing to Psi).** Measured
U(L) - Psi: 4.8e-4 / 4.6e-5 / 4.3e-6 / 3.7e-7 / 2.9e-8 / 1.2e-10 /
7.9e-14 at L = 2..10 (Delta=0), at the f64 floor by L=12; per-L
ratios 0.048-0.102 while the KERNELS' per-lag ratios are 0.25-0.34.
**THE VALUE LOSS IS THE SQUARE OF THE KERNEL LOSS -- exactly what a
stationary Lagrangian requires (first order vanishes) -- and it
INDEPENDENTLY REPRODUCES the recorded rho* = 0.27 +/- 0.02, since
rho*^2 ~ 0.073 sits inside the measured band.** Proof route: (a)
continuity of the rate under uniform kernel convergence with a
spectral floor [sketchable and believed complete; the frozen filters
lie in a UNIFORMLY BOUNDED H^2 ball, so two-sided continuity follows
by evaluating each record's shat at the OTHER's optimal filters];
(b) that the stationary optimum's kernels lie in the WIENER ALGEBRA
[**the fixed-point map PRESERVES W** -- by Wiener's 1/f theorem and
matrix Wiener-Levy -- **but this is INVARIANCE, NOT CONVERGENCE**;
making it a proof needs a CONTRACTION ESTIMATE IN THE WIENER NORM,
which the prover does not have]. Verified hypothesis for (a): the
spectral floor is real and comfortable (n(w) in [0.1495, 0.2167] /
[0.1378, 0.2095] / [0.1404, 0.2082]); empirical W-membership of the
noise factor 4.8e-8/2.2e-8/3.4e-8.
**SO: L^inf(Delta) <= Psi(Delta) + R(Delta), with R measured
<= 1.5e-12 and consistent with 0, but PROVED zero only conditional
on the FIR-density link.**
**THE UNCONDITIONAL DELIVERABLE (needs NO new lemma): hard upper
bounds on L^inf from L^inf <= phi_n (already a theorem) plus an
explicit exactly-D-feasible F0 record on n = 2048, evaluated by
finite Cholesky.** NEW BRACKETS:
  Delta=0: **[0.5627264963, 0.5627656412]** (width 3.914e-5, from
    2.0155e-3 -- a **51.5x NARROWING**)
  Delta=1: **[0.5364013784, 0.5364458112]** (width 4.443e-5)
  Delta=2: **[0.5310500198, 0.5310994872]** (width 4.947e-5)
The bound beats the standing UB(32,0) = 0.5647420 from n = 48 on.
Constructive O(1/n) constants 0.08017/0.09100/0.10131 --
**Delta-DEPENDENT, quoted per-Delta only (R19)** -- sitting
+24%/+29%/+31% above the recorded OPTIMAL constants, **which is the
CORRECT SIGN and a nontrivial consistency check** (a suboptimal
record's constant must exceed the optimizer's); the Delta=0 constant
decomposes as 0.02616 (edge) + 2.2261 x 0.02430 (edge-distortion
repair) = 0.08026 vs measured 0.08017.
GATES/CONTROLS: four evaluators agree to 8.9e-16 (rate) and 4.4e-16
(distortion), so the Collapse denominator identity is CHECKED on the
constructed records, not assumed. **ORIENTATION GUARD (this one bit
the prover): the first window build had a LAG-ORIENTATION DEFECT --
the same class as R27's np.roll defect -- producing a spurious
CONSTANT +1.26e-2 offset in sigma_t that MASQUERADED AS A
NON-VANISHING EDGE CHARGE.** It is now a hard gate with a
reversed-kernel control that fails loudly (+1.26e-2 at every
interior cell vs +2.2e-16 canonical). **ANY SUCCESSOR BUILDING
WINDOW RECORDS FROM SPECTRAL KERNELS MUST RUN THIS GATE.** Safe
side confirmed: U(L)'s sigma comes from a P-lag innovation solve
which OVERSTATES the rate -- the conservative direction for an upper
bound -- flat to 12 digits over P = 40..260 and Nf = 1024..8192.
Anchor cross-check: every V(10,n) at n = 16/24/32 sits strictly
ABOVE the corresponding certified phi_n upper end at all three
Delta (7/7), as a suboptimal record must. Psi recomputed here lands
inside the certified brackets at all three lags.
**PERMITTED WORDING, verbatim: "L^inf(Delta) in [Psi^LB(Delta),
V(10, 2048; Delta)] for Delta = 0,1,2 -- the lower end by Corollary
onedir, the upper end an explicit D-feasible F0 record on n = 2048
through Corollary lower. Under Lemma W the upper end may be replaced
by U(L), giving L^inf <= Psi + R(Delta) with R measured <= 1.5e-12
and proved zero only conditional on the FIR-density link." NO
STATEMENT THAT L^inf COINCIDES WITH Psi MAY BE PRINTED.**
WHAT REMAINS, exactly: (1) the density residual R -- **the ONLY
thing between here and a converse theorem; measured <= 1.5e-12,
needing a Wiener-norm contraction estimate for the K1-K3 iteration
-- a SMALL, WELL-POSED FUNCTIONAL-ANALYSIS PROBLEM, not an open
modelling question**; (2) Lemma W step (3)'s citation, written with
its hypotheses (which are verified). NEXT: R-IND-5 Lemma W **with
the orientation control MANDATORY**; then write link (b), the single
estimate that would convert the whole chain to L^inf = Psi. Cheap
sharpening available: re-optimize the 2L edge rows (currently
truncated taps, not optimized) to close 0.0802 -> 0.0645, ~24% of
the O(1/n) term. **Novelty sweep OWED on Lemma W's combination**
(Collapse + subset-conditioning monotonicity + Toeplitz innovation
monotonicity as a SIGNED two-leg boundary argument).

## R-IND-5 ON LEMMA W (2026-08-07): PASS on substance, but "C(L) INDEPENDENT of n" is REFUTED AS WORDED -- seal 084 ONLY with W1-W12

Fresh context, own evaluator from the model primitives (CMI route
AND collapse route), agreeing with rind5B to 1.55e-15. **The
prover's evaluators supplied NO rate or distortion number.**
**THE ORIENTATION GATE (mandatory first): PASS, and it fails loudly
for the verifier too** -- canonical build sigma_t offset
+0.000e+00 vs **reversed-kernel control +1.256e-02 AT EVERY INTERIOR
CELL** (the recorded constant reproduced exactly). Extended: the
defect makes sum delta_t grow LINEARLY (1.76 -> 3.87 -> 8.08 ->
16.50 at n = 64/128/256/512, +3.289e-2 per cell) -- **it converts an
n-INDEPENDENT edge charge into an O(n) one, exactly the masquerade
the prover reported.** The gate is real, has power, and guards
precisely its claim.
**W5 (mandatory): the gate is the sigma_t gate ONLY.** The per-cell
DISTORTION has ZERO power -- it agrees to +/-1.1e-16 in all three
builds, and analytically so: reversing a real two-sided kernel
conjugates its symbol on |z|=1 and the distortion is invariant under
that. The prover's gate (2) is DECORATIVE. Also on record: **a_y is
real zero-phase (K1) so its kernel is symmetric and carries NO
orientation -- only a_v does.**
LEMMA W STEP BY STEP: (1) edge cells contribute **EXACTLY zero**
(0.000e+00 per-cell CMI at all three Delta; Nc block-diagonal so the
2L ln eps cancels identically); (2) the SUBSET conditioning argument
is sound at both interior edges and for Delta > 0 -- **extended to
Delta in {0,1,2,3,5,9,20,100}, i.e. past Delta >= n where se
saturates: min delta_t >= -7.8e-16, ZERO negative cells**; (3)
sum delta_t is **not merely bounded but EXACTLY n-independent** --
0.043994832 identical to 9 decimals over n = 128/256/512/1024 and
L = 4..12, with the recorded value confirmed as the **L=10** one
(the probe does not say which L); **non-circularity CHECKED**: the
Riccati citation applies to the depth-L FIR record itself, so it
does NOT assume the density it is meant to isolate; (4) the noise
leg helps, sign correct, and is itself n-independent (+8.622e-3 /
+1.079e-2 / +1.076e-2, flat in m, with <ln n(w)> = 2 ln q0 to
0.00e+00 confirming min-phase); (5) the repair is exactly affine
(residual <= 1.7e-16) and lands at dist = D to <= 1.7e-16 at every n
and Delta.
**THE ONE REFUTATION -- W1: "C(L) INDEPENDENT of n" IS FALSE AS
WORDED, in the verifier's own measurements, for the very build the
proof covers.** The n-independent object is the EDGE CHARGE, not the
constant. The zero-edge constant runs 71.76 -> 20.38 -> 15.16 ->
13.39 -> 12.65 over n = 64..1024 (a factor 5.7, still falling);
cause ISOLATED to **the REPAIR leg**, which converges from above to
mu*n*Delta-dist = 31.17. **The CONCLUSION SURVIVES INTACT**: the
constant is monotone decreasing in n in 12/12 swept rows, so
sup_n C(L,n) < infinity and **only C(L,n) = o(n) is needed**.
**W2: Lemma W needs a FEASIBILITY THRESHOLD n >= n0(L)** -- the
zero-edge build is INFEASIBLE at small n (n=64, L=10: the repairing
rescale is c <= 0). The lemma as stated carries no such hypothesis.
**W3: THREE OBJECTS MUST BE KEPT APART AND LABELLED** -- the
ZERO-EDGE build (what steps (1)-(2) prove), the TRUNCATED-TAPS build
(**what every quoted constant and every bracket endpoint actually
comes from**), and the REPAIRED records (what feasibility requires).
**Steps (1) and (2) do NOT apply to the truncated-taps build** (its
edge cells are not independent noise; its Nc is not block-diagonal).
**W4: the REPAIR LEG is not covered by steps (1)-(5)** -- step (5)
discharges FEASIBILITY exactly; the RATE COST of the repair is a
SEPARATE estimate (n-independent in the trunc build, n-dependent in
the zero-edge one).
REDUCTION TO ONE RESIDUAL: **PASS, complete and non-circular** (no
joint limit -- n at fixed L, then L; U(L) >= Psi forced by weak
duality, verified +4.0e-11/+7.2e-11/+5.3e-11 against the 082
certified LBs; the spectral-floor hypothesis verified).
SQUARING CLAIM: **PASS on substance and SHARPER than reported** --
(U(L)-Psi)/T(L)^2 is **~4.3-4.8, CONSTANT over L=1..6** at Delta=0
(4.0-4.5 at Delta=1; 2.9-4.6 at Delta=2). **That is the quotable
form.** W6: the recorded list is at L in {2,3,4,5,6,8,10}, NOT
"L=2..10". **W7: the rho* cross-link is a CONSISTENCY CHECK, NOT an
independent reproduction** -- a value-ratio band of 0.048-0.100
admits rho* in ~[0.22, 0.32], so rho* = 0.27+/-0.02 landing inside
is weak evidence; the Delta=1,2 kernel ratios (0.27-0.30) are the
better witness. **W8: "R <= 1.5e-12" MUST NAME ITS REFERENCE** (the
grid fixed point at Nf=4096/P=180); against the 082 certified LB
endpoints the gap is +4.0e-11/+7.2e-11/+5.3e-11, and **L >= 11 is
pure f64 noise going NEGATIVE at Delta=0 (-1.25e-13) -- do not cite
those entries as convergence evidence.**
**THE UNCONDITIONAL BRACKETS: PASS -- "the STRONGEST ITEM in the
package".** Independently rebuilt and evaluated: 0.562765641106 /
0.536445811112 / 0.531099487172, reproducing the quoted ends to
<= 9.4e-11, **outward-rounded on the safe side**, exactly feasible
to <= 1.7e-16 at every n, with la_cmi vs la_fast agreeing to 1.1e-15
ON THE CERTIFICATE RECORDS THEMSELVES. **They depend on NO LEMMA
WHATSOEVER** -- only F0 membership, exact feasibility, and correct
evaluation. 51.5x narrowing confirmed; beats UB(32,0) from n=48 on.
**W10: the anchor cross-check is 8/8, not 7/7** (the probe
undercounts its own table).
SAFE SIDE: **PASS on sign** (a P-lag solve OVERSTATES sigma, hence
the rate -- conservative for an upper bound), with power (P=1 ->
0.5867 down to P=8 -> 0.56272650). **W11: at P >= 20 the rate is
flat AT THE f64 FLOOR (3.3e-16 over P=20..400 and Nf=1024..8192);
"monotone decreasing over P=40..260" is TESTING FLOATING-POINT
TIES**, and the verifier's own run reports "decreasing: False" for
that reason. Write "non-increasing by construction; flat to 3.3e-16
from P=20".
**DOES IT PROVE TOO MUCH? NO, and the check is sharp** -- applied to
the BLOCK program (se == n), whose value is independently two-sided
certified, the Delta-ladder approaches block_inf = 0.5299499808119
**from above and never crosses** (down to +1.70e-12 at Delta=12),
and the block-schedule window records give upper bounds strictly
ABOVE it converging like ~0.105/n. **The machinery does not produce
a bound below a known value.**
**W9: the constants' "correct sign" is FORCED ONLY AT EQUAL n.**
phi_n <= V(10,n) forces it at equal n (verified 3/3, and that IS the
8/8 anchor cross-check); but the recorded 0.064507/0.070483/0.077503
are R19's **n=16** values while the constructive constants are
quoted at **n=2048**, and both sequences decrease in n -- so the
+24%/+29%/+31% comparison **is NOT forced as stated**. Rephrase to
equal-n, or compare against the LIMIT c_phi ~ 0.06447.
**W12: the decomposition constant is n*Delta-dist = 0.024260, not
0.02430**; with it the identity closes to 2e-6 rather than 9e-5.
**NOTHING FORBIDDEN IS IMPLIED**: the bracket has strictly positive
width at every Delta (+3.91e-5/+4.44e-5/+4.95e-5), and the two
inequalities come from structurally INDEPENDENT arguments -- **the
chain is one-directional in each direction SEPARATELY; together they
give a BRACKET, never an equality.**
**READY TO SEAL 084 WITH W1-W12. If W1-W4 are NOT folded, THE SEAL
SHOULD FAIL** -- the sentence as written is false in the verifier's
measurements for the very construction the proof covers. All twelve
are EDITS to the statement, not re-runs; no computation repeats.
Novelty sweep on Lemma W's combination remains OWED.