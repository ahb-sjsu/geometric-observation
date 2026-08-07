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