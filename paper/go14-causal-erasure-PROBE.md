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