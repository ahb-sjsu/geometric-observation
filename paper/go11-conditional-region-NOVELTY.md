# Novelty-sweep record — `go11-conditional-region.tex` (problem statement)

**Date:** 2026-08-04 · **Method:** four independent fresh-context web-search
agents (one interrupted by a spend limit and resumed/relaunched; full reports
in the session transcript; this file is the durable record). **Standing
caveat:** every "no prior found" is relative to the recorded queries, not a
proof of absence. **Disposition:** all findings folded into problem-statement
v0.2 (Fact 1 re-attributed; "what is known" tightened to Paper V's true
extent; conjectures reframed as expected-by-analogy; convexity warning added;
Question 1's first decidable step recorded).

## Headline findings

1. **Fact 1 is folklore, not a contribution.** The identity
   I(X;X̂) − I(X;X̂|S) = I(X̂;S) appears verbatim inside Paper V's own
   achievability proof (binning step) and is working folklore throughout the
   rate–distortion–equivocation lineage. v0.2 attributes it and claims only
   the reframing (single curve of corners → distortion-constrained IB /
   max-leakage Yamamoto member).
2. **Paper V solves the one-constraint pair-region completely** (general
   alphabets; Pareto-channel fixed point = the β′-scalarization with
   β′ = 1−α; scalar corner + mode-aligned reset water-filling as the solved
   Gaussian instances). GO-11's open content is exactly: general non-aligned
   Gaussian S (Paper V's own declared "general Gaussian coupling" gap) and
   everything two-consumer beyond thm:multi's structural union.
3. **The scalar single-distortion instance of the frontier is prior art**:
   - Wang–Wu–Ma–Zhang, "Task-Oriented Lossy Compression with Data,
     Perception, and Classification Constraints" (IEEE JSAC 2024/25,
     arXiv:2405.04144): min I(X;X̂) under MSE cap + H(S|X̂) ≤ C (an I(X̂;S)
     floor), same Markov chain, closed scalar/bivariate-Gaussian form,
     one-constraint-active-at-a-time structure. The RDC line is fast-moving
     (universal-representations follow-up arXiv:2504.09932) — live risk of a
     vector paper appearing.
   - Günlü–Schaefer–Boche–Poor (TIFS 18:3803–3816, 2023, arXiv:2205.05068):
     the conditional-leakage coordinate I(X;W|S) itself, exact closed
     scalar-Gaussian region via conditional EPI, **under a degradedness
     ordering** — contains the scalar single-consumer corner.
4. **Orientation correction (secrecy sweep):** the Yamamoto lineage is the
   *same* optimization family, not a sign-flipped cousin — maximizing
   equivocation at an S-holder = minimizing L up to H(X|S). All exact
   Gaussian regions found there are scalar, one distortion:
   Villard–Piantanida 2013 (exact only for eavesdropper-without-SI; the
   **non-degraded scalar Gaussian converse explicitly left open**);
   Schieler–Cuff/Satpathy–Cuff (Gaussian solved only with no adversary SI);
   Ekrem–Ulukus (only vector-Gaussian equivocation result; tight only with
   the rate constraint removed); Tandon–Sankar–Poor (only exact
   two-distortion+equivocation region; discrete, privatizes S itself).
5. **Question 1's endpoint (vector-Gaussian common reconstruction) is open —
   emphatically.** Scalar CR: Steinberg 2009; Lapidoth–Malär–Wigger 2014
   (arbitrary scalar Gaussian S via ξ-reduction). The full CR follow-up line
   (HB-with-CR, cascade, SR — finite alphabets verified, interactive,
   action-dependent, 2026 channel variant): **no vector Gaussian case
   anywhere**; no "CR water-filling" exists in print, not even the
   mode-aligned case Paper V solved. The strongest general-coupling vector
   machinery (Stylianou–Gkagkos–Charalambous indirect/WZ RDFs) is
   structurally disqualified: its water-filling comes from the estimator
   *using* S, which the CR Markov constraint forbids.
6. **Machinery map for the conjectures:** Liu–Shao–Zhang–Poor semantic RD
   (T-COM 2022, arXiv:2201.12477) — two simultaneous quadratic constraints,
   error-covariance convex program + reverse water-filling (second
   coordinate is state-MSE, not information); sign-flipped scalar closed
   forms since Rebollo-Monedero et al. 2010 + Sankar et al. 2013;
   special-case vector water-filling tilting toward least-leaking modes
   (Tripathy–Wang–Ishwar Prop 2) — the mirror of Conjecture 2's allocation;
   linear-policy optimality for mixed-quadratic Gaussian objectives
   (Kazıklı–Gezici–Yüksel). Cautionary: the 2026 rate–distortion–deception
   paper hit the same three-non-commuting-matrices wall and found no closed
   form → Conjecture 2 flagged "possibly optimistic".
7. **Technical warning recorded (Remark in v0.2):** the β′-scalarization is
   convex only on β′ ∈ [0,1] (convex combination of the coordinates);
   I(X̂;S) is convex in the channel, so β′ > 1 leaves the convex regime.
8. **First decidable step recorded (Question 1):** the rank-one
   marginalization dichotomy — does marginalizing the channel onto w'X (and
   driving Steinberg's scalar formula with E[w'X|S]) lose optimality? Either
   collapse to the scalar corner or the first genuinely vector obstruction.

## Residual risks (to refresh at claim time)

- IEEE-only venues without arXiv copies (no web sweep can exclude).
- The RDC line producing a vector-Gaussian paper (fast-moving, 2024–2026).
- Maximal-correlation / common-information-under-distortion had the weakest
  coverage of the four sweeps.
- The Zaidi–Estella Aguerri–Shamai IB survey was verified at abstract level,
  not by reading all 51 pages.

## VERIFICATION ADDENDUM — Proposition 1 (marginalization dichotomy), 2026-08-04

The dichotomy recorded as Question 1's first decidable step in v0.2 was
**settled the same day** (v0.3, Proposition 1): marginalization is strictly
suboptimal. Canonical instance X ~ N(0,I₂), Y = X₁, S = X₁+X₂:
L_marg(D) = ½log₂((1+D)/(2D)) (scalar corner) vs
L_vec(D) = ½log₂⁺(1/(2D)) = Gray's R_{Y|S}(D) exactly (converse via Gray;
achievability by Ŷ = (1−D)X₁ + DX₂ + N, and Ŷ = S/2 for D ≥ ½). Strict gap
½log₂(1+D) at every D ∈ (0,½]. Mechanism: an X-measurable S is implicitly
known to the encoder, so the CR Markov constraint costs nothing beyond
conditional RD — "writing the record in ink the eraser can read."

**Pre-assertion numerics (author-side, logged):** closed forms reproduced by
40-start SLSQP over linear channels (2e-4) and unrestricted discretized
conditional-BA (grid error; 0.372 vs 0.368 at D=0.3, 0.005 vs 0 at D=0.5).

**R-IND-5 fresh-context pass: CONFIRMED, 0 errors, 2 wording sharpenings**
(verifier seed 91724; own parametrizations): (a) 2M-sample MC of the named
channel at four D values; (b) exhaustive 1251×1001 linear grid — argmin
exactly (1−D, D); (c) 35k-parameter Adam over unrestricted p(ŷ|y,s) at four
multipliers — never below the Gray floor; (d) marginalized-class BA never
below the corner. Sharpenings folded into v0.3: (iii)'s "widening" → "equal
to the full marginalized value" (the absolute gap decreases on [½,1)); and
Conjecture 3's "when S is informative" corrected to "when S has an
X-independent component (τ²>0)" — forced by Prop 1 itself, which exhibits a
maximally informative X-measurable S attaining the single-consumer
conditional floor at every D ≤ ½. Verifier also confirmed no contradiction
with the tax note's floors (different instance: two-consumer product floor
vs single-consumer, non-X-measurable vs X-measurable S).

**New operational prediction recorded (Remark):** optimal joint records
should tilt *toward* the reset context's X-measurable directions — the
encoder-side complement of the eraser-side allocation tilt measured in
GO-P-2026-058/059. A future GO-11 operational face can gate on this.

## VERIFICATION ADDENDUM 2 — Theorems 1–2, Corollary 1 (refined question settled), 2026-08-05

The refined question was settled in v0.4/v0.5 (Sec. 7): **Theorem 1** (pair
sufficiency — the d-dimensional rank-one-read problem collapses to
T = (w'X, γ'X) for every d, by channel resampling); **Theorem 2** (exact
single-consumer CR function: L(D) = ½log₂ g*, g* the larger root of
P(g) = Dsg² − (D+s−ρ²)g + (1−ρ²), s = 1+τ², in closed form; uniqueness via
P(1) = (D−1)τ² < 0; achievability by the explicit linear channel; converse
by the Paper-V second-moment method); **Corollary 1** (Kaspi verdict:
structurally yes — only (ρ,τ²) matter; formula-wise no — instances with
identical (Y,S) margins give different L: 1.1610 vs 1.2105 bits at D=0.1).

**Pre-assertion numerics (author-side, seed 20260805, logged):** cubic =
60-start SLSQP direct optimum with exact coefficients (a,b) = ((g−1)/g,
(g−1)ρ/(gk)); moment-converse bound = cubic to 1e-6 at 12 instances;
unrestricted conditional-BA never below (grid error only); anchor algebra
(classical/Gray/Steinberg) exact; margin-pair distinguisher confirmed.

**R-IND-5 fresh-context pass (verifier seed 20260804): CONFIRMED with the
assigned step PROVED, one sharpening, one error — all folded into v0.5:**
- **Task-3 obligation DISCHARGED**: the converse's final minimization was
  proved analytically. Key: the determinant identity
  det Σ_{T|S}/det Σ_e = (Var(aY+bV|S)+n)/n (the S-column of the moment
  matrix = V-column + τ²e_S), so the moment program IS the linear-channel
  program; B → ∞ on the PSD and distortion boundaries; FOCs linear in
  (a,b); P(1) < 0 pins the unique stationary g* > 1. Converse closed.
- **Sharpening S1**: the drafted cubic factors as k × quadratic — the k
  factor is spurious (root 1/(1+τ²) < 1, never feasible). v0.5 states the
  quadratic closed form and the uniqueness proof (upgrading the drafted
  "unique on every tested instance" hedge to a theorem).
- **ERROR E1 (overclaim, corrected)**: the drafted Scope remark said
  Theorem 2 "settles Conjectures 1–2 for m=1 rank-one". False: it settles
  the WORK-ONLY ENDPOINT. The verifier exhibited strict rate excess in the
  L-optimal channel (0.0400 bits at (ρ²,τ²,D)=(0.75,0.5,0.3); 0.0204 at
  (0.75,0.5,0.1)) — so the m=1 (R,L) frontier is a genuinely nontrivial
  curve, no single channel attains both corners, UNLIKE Paper V's scalar
  corner. Recorded in v0.5 as a finding in its own right; the weighted-
  objective extension of the moment method is the named next step.
- **E2 (typo)**: "Fact~\ref{thm:pair}" collided with Fact 1; fixed to
  Theorem refs. Setup sharpened to state MUTUAL independence (the S-kernel
  argument needs the joint form, not pairwise).
- **Verifier numerics**: 8 fresh instances (incl. ρ²=0.95, τ²=5, D∈{0.05,
  0.9}) — quadratic = direct = raw 3-variable moment program to ≤3e-9
  bits; 25,500-point feasible-root-uniqueness sweep: exactly one root
  everywhere (497 float64 flags at τ²=1e-6 resolved by 50-digit mpmath);
  Gray-floor/Steinberg-margin sandwich: 0 violations.

**Standing after v0.5**: Question 1's endpoint SOLVED for rank-one reads
(first vector-Gaussian CR-type function; the CR sweep found no prior).

## VERIFICATION ADDENDUM 3 — Theorem 3 + Corollary 2 (the m=1 frontier), 2026-08-05

**The m=1 frontier settled in v0.6**: Theorem 3 — the exact rate–work
region for rank-one reads, Pareto frontier traced by the two-water-level
stationarity system (a = 1 − αγ₀ − (1−α)γ₁; m = aρ/(s−(1−α)γ₁);
b = (1−α)γ₁m; γᵢ = n/(Qᵢ+n); frontier point (½log₂1/γ₀, ½log₂1/γ₁)).
Converse by the same moment method with a second determinant identity
det Σ_T/det Σ_e0 = (Q₀+n)/n; endpoints = classical reverse channel (α=1)
and Theorem 2 (α=0). Corollary 2 — **misalignment always opens a strict
tradeoff**: for ρ²∈(0,1), τ²>0 the L-optimal moments have b≠0, the
R-optimal moments have b=0 (both provably unique), so no channel attains
both corners; excesses 0.0400/0.0349 bits at (0.75,0.5,0.3). Single-corner
collapses are exactly ρ²→1 (Paper V's scalar corner) and ρ=0 (+ the
τ²→∞ limit). Settles Conjecture 1 for m=1 rank-one.

**Pre-assertion numerics (author, seed 20260806):** stationarity system
holds at the multi-start optimum and weighted moment program agrees to
1e-6 bits at 20 (ρ²,τ²,D,α) combos; anchors exact; E1's 0.0400
reproduced; α-sweep monotone. Known artifact: discretized BA at α=0.75
read 0.0015 BELOW the linear value — grid bias (discrete source easier
to describe); the rigorous check is the exact moment program.

**R-IND-5 pass (verifier seed 771177): CONFIRMED, 0 errors, 2 sharpenings
(folded into v0.6):**
- S1: Corollary 2's R-minimizer uniqueness was asserted, not proved —
  verifier supplied the two-line proof (elimination b(1−ρ²)=0 at α=1,
  then (a,n) forced) and the moment-route strictness inference (any
  L_min-attaining channel carries the b≠0 moments → its rate ≥ B₀ there
  > R_min). Both now in the corollary text.
- S2: "traces the full Pareto boundary" weakened to
  uniqueness-conditional (interior-α minimizer uniqueness is
  numerics-supported — 625-initialization probes, exactly one root every
  time — not proved; endpoint uniqueness IS proved).
- Micro-notes folded: m defined; ρ=0 degeneracy phrased as
  corner-collapse; D<½ scope on the τ²=0 formula; τ²→∞ limit noted.
- Verifier numerics: 2 fresh instances × 5+41 α-points, three independent
  routes (system roots / raw-log-det channel optimization / raw moment
  program) agree to ≤5e-9 bits; strict monotonicity of R(α), L(α); both
  quoted excesses confirmed (0.040046, 0.034949); ρ²→1 collapse probed.

**Standing after v0.6**: the single-consumer (m=1, rank-one) problem is
now FULLY solved — endpoint (Thm 2) + entire frontier (Thm 3) + strict
two-corner separation (Cor 2).

## VERIFICATION ADDENDUM 4 — the m=2 region (Theorems 4–5, Cor. 3), 2026-08-05

**The m=2 region settled in v0.7 as a matrix program**: Theorem 4
((m+1)-sufficiency — m consumers + context collapse to m+1 coordinates,
resampling verbatim); Theorem 5 (the exact region = closure of quadrant
union over a 9-parameter Gaussian family (A ∈ R^{2×3}, Σ_N ⪰ 0) — Gaussian
sufficiency for m=2 rank-one, settling Conjecture 1 there; determinant
identities generalize by the same Schur double-count; Markov moment
identity Cov(S,Ŷ)=Cov(V,Ŷ) row-wise). **Conjecture 2 WITHDRAWN as
stated** (no water-filling closed form emerged; three non-commuting forms;
the program is the honest endpoint — the caution written into v0.2 was
correct). Corollary: the GO-10 worked instance decomposes exactly, deriving
the tax-gap formula ½log₂(1/(s²+(1−s²)D)) from the region itself.
Conjecture 3: floor strictly loose at D>0, gap → 0 as D→0 (0.0664→0.0035
across D=0.3→0.02) — predicted shape, iff still open, now a checkable
statement about the program's optimizer.

**Pre-assertion numerics (author, seed 20260807):** GO-10 anchor exact to
4 decimals (region, corner degeneracy, tax gap); α=1 rate = Xiao–Luo to
1e-5; floors hold; frontier monotone and nondegenerate at the misaligned
instance (misalignment tradeoff persists at m=2); coarse unrestricted BA
(9³ grid) below by 0.033 — grid bias, disclosed (the rigorous converse is
the moment method).

**R-IND-5 pass (verifier seed 20260808): CONFIRMED, 0 errors, 2
sharpenings (both folded into v0.7):**
- S1: Theorem 5 implicitly required Σ_T ≻ 0 and the flagship corollary
  instance (V=Y_A) violates it — hypothesis added + degenerate-reduction
  clause; verifier confirmed both routes land on the same value
  (2.190412 vs 2.190411 at ρ_AV = 1−1e-6).
- S2: the corollary's single-corner sum needed an unstated super-additivity
  converse — verifier supplied the 4-line proof ((Y_A,S) ⊥ Y_B; chain rule;
  the induced marginal channels ARE Markov, but only by the instance's
  double orthogonality — exactly the Prop-1 coupling subtlety); now a
  written proof in the corollary.
- Verifier numerics: fresh instance (0.45, 0.55, −0.25, 0.8) with D_A≠D_B —
  Xiao–Luo anchor to 7e-13, floors strict (+0.0881), frontier monotone;
  cor:go10 at (τ²=0.6, D=0.15) all four closed forms to 1e-6;
  exhaustiveness probe with 10 genuinely non-Gaussian noisy-quantizer
  channels: worst domination margin +0.073 ≥ 0; determinant identities to
  1e-10; rem:c3's 0.0293 gap reproduced independently.

## VERIFICATION ADDENDUM 5 — Theorem 6 (work-floor exactness iff), 2026-08-05

**Conjecture 3 SETTLED WITH A CORRECTION in v0.8 (Theorem 6):** the work
floor ½log₂(det Σ_{Y|S}/det Δ) is attained iff (a) τ²=0 and Δ ⪯ Σ_{Y|V},
or (b) β=0 and Δ ⪯ Σ_Y; strict in every other case, with the explicit
deficit sandwich 0 < L_min − floor ≤ ½log₂[det(I−Σ_{Y|S}⁻¹Δ)/
det(I−Σ_{Y|V}⁻¹Δ)] → 0 as Δ→0 on the misaligned branch. **The correction:**
the conjectured condition used Σ_{Y|S}; the attainable branch requires the
encoder-accessible Σ_{Y|V} — the same S-vs-V substitution Prop 1/Thm 2
forced everywhere. Necessity mechanism: floor tightness pins the error
moments (Cov Z = Δ, Z ⊥ (Ŷ,S) ⟹ Z ⊥ V), and the no-V-leakage step
evaluates to [Δ 0]M⁻¹[β; Var V] = 0 ⟺ β=0 or τ²=0. m=1 corollary: on the
active-floor regime D ≤ Var(Y|V), attained iff ρτ=0 (P(g_f) = −ρ²τ²/s).

**Pre-assertion numerics (author, seed 20260809):** iff verified on
inside/outside/boundary probes in both branches (incl. a barely-inside
instance det margin 0.002 — attained, as predicted); sandwich holds at 8
strict points; inconsistency functional zero exactly on the (a)/(b)
branches (|q| = 4.6e-2 vs ≤2e-17).

**R-IND-5 pass (verifier seed 271828): CONFIRMED, 0 errors, 2 sharpenings
(folded into v0.8):**
- Key step re-derived exactly (partial covariance = [Δ 0]M⁻¹[β;1] to
  1e-12; no accidental cancellation possible — Δ diagonal ≻ 0 acts
  componentwise; M ≻ 0 inside scope).
- S1: the m=1 corollary glossed the clamp sliver (τ=0, D > 1−ρ²: g_f
  becomes the SMALLER root; floor negative, L=0) — fixed by scoping to the
  active-floor regime D ≤ Var(Y|V), the m=1 shadow of condition (a).
- S2: "Otherwise (τ²>0 and β≠0)" mislabeled the complement (which also
  contains the SDC-violating cases, both verified strict: gaps 0.0059 /
  0.0019) — restated; plus two rigor one-liners folded (boundary 0/0 via
  Δ_t↑Δ limit; strictness needs L_min attained — compactness + LSC).
- Verifier numerics: 11 fresh configurations incl. exact-boundary
  attainment, small-τ² continuity (gap 0.000471 vs sandwich 0.000473 —
  nearly tight!), large-β near-singular Σ_{Y|V}; doc's 0.0293 gap
  reproduced independently.

**Standing after v0.8**: Conjectures 1 (m≤2 rank-one), 2 (withdrawn/
replaced), and 3 (Theorem 6) are all resolved. Remaining open in the
manuscript: interior-α uniqueness lemma; higher-rank reads; vector S;
operational faces.

**Standing after v0.7**: GO-11's original problem is now settled at every
level the tools reach — one-constraint region (Paper V, attributed), m=1
fully solved (Thms 2–3, Cor 2), m=2 exactly characterized as a
finite matrix program (Thm 5) with the alignment degeneracies in closed
form (Cor 3) and the GO-10 tax formula derived from the region. Open
residue: Conjecture 3's iff; interior-α uniqueness lemma; higher-rank
reads; vector S. House rules: all manuscript-grade until a sealed C3
harness registration (PROTOCOL §5.1) — not yet ledger-bearing.

## VERIFICATION ADDENDUM 6 — the last theory rungs (v0.9), 2026-08-05

**All three remaining rungs settled in v0.9:**
- **Theorem 7 (vector S, m=1 rank-one: SOLVED).** (1+r)-sufficiency
  (resampling verbatim); whitening by the pair (Σ_T, Σ_{T|S}) → the
  generalized two-water-level system with per-mode closed form
  u = (1−αγ₀−(1−α)γ₁)·[(1−(1−α)γ₁)I + (1−α)γ₁Λ]⁻¹y₀; Theorem 3 = r=1
  case; converse dimension-free.
- **Theorem 8 (higher-rank reads).** (k+r)-sufficiency + the k×(k+r)
  matrix program; EXACT decomposition under simultaneous block-diagonality
  (superadditivity proof supplied by the verifier); misalignment strictly
  helps (numerical exhibit 0.0057 bits).
- **Proposition (interior-α uniqueness): the S2 debt DISCHARGED.** The
  verifier PROVED the assigned lemma: aa'/s is matrix-convex (Schur-
  certificate averaging), so the weighted objective is convex in moment
  coordinates on the active slice; every eq:vecfoc solution is the unique
  global minimizer, at every α ∈ (0,1]. Theorem 3's uniqueness hedge and
  the trace-completeness caveat are retired unconditionally.

**Pre-assertion numerics (author, seed 20260904):** FOC holds at r∈{1,2,3}
fully general couplings (after correcting the author's first drafted FOC —
caught by the author's own sanity run: values matched Thm 3 exactly while
the drafted formula failed, forcing the re-derivation with the y₀-collapse);
moment program to 5e-7; BA never below; aligned decomposition to 8e-4;
misaligned strict.

**R-IND-5 pass (verifier seed 314159): CONFIRMED + assigned lemma PROVED;
4 sharpenings folded:** Σ_T≻0 hypothesis + scalar-record cross-reference
(thm:vecS); the ill-typed Markov identity Γ'E[TŶ] corrected to
Γ'E[XŶ] (V-block); thm:rankk's alignment condition restated as
simultaneous block-diagonality with the decomposition proof attached
(was numerics-only in a theorem environment — fair adversarial objection).
Verifier numerics: FOC to 3.9e-9 at 5 fresh instances incl. r=4 and
λ_min=0.02 at D=0.92; r=1 ↔ Thm 3 algebraic + numeric match; vector det
identity to 1.1e-11; 2160-run uniqueness hunt: single optimum everywhere
(dispersion ≤3e-8); 400 Hessian probes: min eigenvalue +0.36.

**Standing after v0.9**: the m=1 theory is CLOSED — endpoint, frontier,
floor-iff, vector S, uniqueness — with higher-rank reads exactly
characterized (program + alignment decomposition) and m=2 as the matrix
program. Every named open item from v0.1 is now settled, withdrawn-with-
reason, or reduced to a computable program. Remaining GO-11 work is
operational/editorial: further tilt families if ever wanted; paperization
(Syed). Manuscript-grade beyond the 060/061/062-netted content: the v0.9
theorems (7, 8, uniqueness) are not yet under a sealed harness — a future
registration (or an 060 successor) could net eq:vecfoc and the
decomposition the way 060 netted Thms 1–5.

## Query coverage

~60 distinct WebSearch queries + ~20 page-level fetches across four sweeps
(IB/privacy-utility; secrecy/equivocation with page-level verification of
Villard–Piantanida, Sankar et al., Günlü et al.; SI placements + in-repo
Paper V delineation; targeted CR pass with page-level reads of
Lapidoth–Malär–Wigger). Full per-sweep query lists in the session transcript
and reproduced in each agent report.

## Verification addendum 7 — Theorem 9 (the m=2 frontier system), v0.10

2026-08-04. Pre-assertion numerics (seed 20260907, `sanity_m2sys.py`): the
FOC-N off-diagonal identity and the per-mode resolvent formula hold at the
80-start m=2 program optimum to ≤2e-7 at two scalar-context instances and
one vector-context instance (r=2, d_T=4), all three weights w ∈ {0, ½, 1};
w=1 read-span anchor to 1.4e-8.

**R-IND-5 pass: PASS — no mathematical errors; 7 sharpenings folded.**
Independent verifier re-derived both gradients (FD-checked to ≤1.1e-9),
Newton-polished the raw KKT system (non-circular: the polish never uses
the theorem's identities) and confirmed (i)–(v) to ≤3.3e-16. Sharpenings
folded into v0.10: (1) "traces the frontier" → containment language
(frontier ⊆ solution set; every solution achievable; compare by objective);
(2) bracket-invertibility lemma (= wM₀⁻¹+(1−w)λⱼM₁⁻¹+diag(μ) ≻ 0);
(3) LICQ automatic — disjoint constraint supports; (4) symmetric-
differentiation convention note (constraints diagonal-only, factor 2
cancels); (5) constraints active WLOG but strict complementarity NOT
assumed — verifier exhibited a slack instance with an exactly flat
minimizer ray (J constant to 8 decimals over a +44 bump in (Σ_N)₂₂), so
μᵢ=0 degeneracy gives non-isolated solutions; (6) eleven-scalar count
demoted to bookkeeping; (7) w=1 anchor STRENGTHENED: μᵢ = 1/Dᵢ and
EEᵀ+Σ_N = diag(D) hold without symmetry (verifier: exact to 4.4e-16 in
generic asymmetric instances; folded with the Hadamard/backward-channel
and envelope-theorem arguments on the Xiao–Luo regime).

**Standing after v0.10**: the two-water-level structure SURVIVES m=2 —
water levels promoted to 2×2 matrices (M₀, M₁), with per-mode 2×2
resolvent formula in any context dimension; the frontier conjecture
(withdrawn as scalar water-filling at v0.7) partially rehabilitated as
matrix-resolvent water-filling. Open at m=2:
uniqueness of the system solution.
