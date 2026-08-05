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