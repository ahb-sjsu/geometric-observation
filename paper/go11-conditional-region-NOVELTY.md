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

## Query coverage

~60 distinct WebSearch queries + ~20 page-level fetches across four sweeps
(IB/privacy-utility; secrecy/equivocation with page-level verification of
Villard–Piantanida, Sankar et al., Günlü et al.; SI placements + in-repo
Paper V delineation; targeted CR pass with page-level reads of
Lapidoth–Malär–Wigger). Full per-sweep query lists in the session transcript
and reproduced in each agent report.
