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
two-corner separation (Cor 2). Open, in order: (1) higher-rank reads;
(2) m≥2 (pair sufficiency generalizes verbatim — two rank-one consumers
collapse to ≤3 coordinates; the moment method's determinant identities
are the candidate mechanism); (3) interior-α uniqueness (S2) as a lemma.
House rules: manuscript-grade until a sealed C3 harness registration
(PROTOCOL §5.1) — not yet ledger-bearing.

## Query coverage

~60 distinct WebSearch queries + ~20 page-level fetches across four sweeps
(IB/privacy-utility; secrecy/equivocation with page-level verification of
Villard–Piantanida, Sankar et al., Günlü et al.; SI placements + in-repo
Paper V delineation; targeted CR pass with page-level reads of
Lapidoth–Malär–Wigger). Full per-sweep query lists in the session transcript
and reproduced in each agent report.
