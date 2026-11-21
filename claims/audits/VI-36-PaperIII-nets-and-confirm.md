# VI-36: R-IND-5 on the Paper III nets, and a confirming pass on VI-34's fixes (2026-11-21)

**Target.**
- **Task A:** version 1 of the new net `experiments/verify_paper3_nets.py` (uncommitted then)
  and its result JSON. It nets the max-det closed form, `thm:multiobs-loss` and
  `cor:dispersion` of `paper/observation-theory.tex`.
- **Task B:** commit ff8916d, which applied the fixes for VI-34's findings to Paper III and to
  Appendices B and F, Chapter 16 and the ledger.

**Verifier.** A fresh-context general-purpose agent, working from local files only, with no
browser, connector or network tools, no cvxpy, and no access to the assistant's verdict. It
re-derived the per-mode terms from the definition and wrote its own barrier/Newton solver for
the region's joint program. That solver reproduced the net's gaps to 3–4 digits (pair r31:
9.17e-4, 9.17e-4, 4.97e-4, 1.78e-4, 5.83e-5, 1.86e-5 down to δ = 1e-7).

**Verdict.**
- **Task A:** 0 errors, 5 gaps, 2 overclaims, 3 exposition items. The closed forms, the
  water level, the dual certificate, the joint program, the per-mode terms and the Monte Carlo
  standard errors are right; the weak points are what some checks can catch.
- **Task B:** 0 errors, 2 gaps, 3 overclaims, 3 exposition items. Ten of VI-34's twelve
  findings are fully resolved; #2 and #12 were only partly resolved.

## Task A findings and dispositions (version 2 of the net, 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| A1 | GAP | m5's Csiszár check does not determine the inactive term, whose output support is {0}: every term (λ−κ)(y²−g) + ½log(1+2κg) − κg passes it, and at κ = 0.1 the variance moves from 0.18 to 0.115 while the mean moves by 0.0033, below m6's 5 SE. So a wrong slope, with V computed to match, passes m5 and m6. | m5 now also checks the stated terms against the definition, j_k(y) = −λ*D_k − log E exp(−λ*(y − Ŷ_k)²) under the optimal output law, by quadrature at 7 points per coordinate. Agreement is 1.8e-15. m7 now requires the κ-family to pass Csiszár and fail the definition (23/23). |
| A2 | GAP | m2's gap gate was one-sided and left feasibility out: a water level 1.2θ gives an infeasible matrix with a negative gap and passed m2 on 150/150. | m2 gates \|gap\| and includes feasibility; m7 requires the 1.2θ level to fail m2 (150/150). |
| A3 | GAP | m3 had no nested pair with distinct observers (all 40 independent pairs were non-nested), and 12 of the 40 had a slack cap, so Σ° = Σ₁* trivially. | 20 nested pairs with distinct, non-commuting observers (P₂ full rank, D₂ a fraction of the largest nesting D₂, found by bisection). The closed-form comparison counts only pairs whose cap binds (71). |
| A4 | GAP (tolerance) | L is second order in a nesting violation (1e-4 gives L ≈ 2e-8), so a fixed "L = 0" threshold can fail the iff spuriously. | Scale-consistent thresholds with an excluded band: v ≥ −1e-9 implies L ≤ 1e-9, and v ≤ −1e-4 implies L ≥ 1e-12. One pair fell in the band. |
| A5 | GAP | The m4 replacement has the same structural flaw two decades lower: the verifier built true instances (fresh seed) on which it fails. It was re-tuned on the same seed and pairs, and the failing first-run output was not kept. Its "gap ≥ 0" and "nonincreasing" clauses cannot fail. Its resolution is about 2% of L. Four solves returned "optimal_inaccurate" and were accepted silently. | m4 now reads the dual μ of the base-rate constraint and fits gap = a + c√δ (+ eδ) over the δ ≤ 1e-4 at which it binds, gating \|a\| ≤ 5e-6 + 0.005 L. Pairs with fewer than three binding δ are judged at δ = 1e-6 and counted (at most 3 unresolved; 0 occurred). At most 5% of solves may be inaccurate (15 of 574), and solver failures fail the check. m7 requires a false corner R2° − 0.05 L to fail the gate (39 pairs). The by-construction clauses are reported, not gated. The run uses a fresh seed (20261125), with criteria written before it. The lost first-run output is disclosed in the docstring and here. |
| O1 | OVERCLAIM | m4 takes thm:region's set as given and checks only the corner step of thm:multiobs-loss. The labels "Targets: thm:region" must not be used to lift B5's region converse out of `[exploratory]`. | Targets relabelled. The docstring and the paper say the net is not one for thm:region's converse or achievability. |
| O2 | OVERCLAIM (minor) | m6's bounds and strict-inequality clauses follow from the formula's arithmetic and from the variance clause. | Labelled as consequences, reported per configuration, not gated. |
| X1 | exposition | "Below 0.1θ the shift is < 1e-3" is wrong: the 1e-3 threshold is near γ/θ = 0.064. | Corrected. |
| X2 | exposition | lem:maxdet does not state the closed form, and m1 nets the closed form, not the lemma's rate identity. VI-4's bug equals the truth at rank P = 1 (47 of 150 instances then). | Said in the targets. The rank-one count is reported (51 of 150 now; the bug loses on 98). |
| X3 | exposition | T-CUST-1 is not met yet: the net is not in CI, and cvxpy is only in the uncommitted requirements. | Owed: CI wiring after this record's confirming pass. |

## Task B findings and dispositions (2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| B1 | OVERCLAIM | `cor:dispersion` asserted the expansion while saying Kostina–Verdú's hypotheses were "to be checked at the source", a flag that must not ship (T-CUST-3); the fix also dropped the "excess-distortion" qualifier, which the Q⁻¹(ε) expansion needs. | **Checked at the source** (arXiv:1102.3944): the expansion is their Theorem 12, which holds for abstract alphabets; its restrictions (i)–(iv) and basic conditions hold for the ℝ^r-valued letter; the scalar constant is their eq. (94). The corollary now says so, restores "excess-distortion", and proves the optimal kernel unique from Lemmas cm, info and maxdet. That argument is new and awaits a confirming pass. FRONTIER G12 closed. |
| B2 | OVERCLAIM | "We confirmed Theorem region and Corollaries multiobs–kobs numerically" contradicts Appendix B (no net can fail on the region converse); the k = 3 "chain" check is a covariance computation. | Rewritten: the only check that can fail is 023's [3], on the corner. The new net is described with its scope. |
| B3 | GAP | The open problems omitted Gaussian achievability for k ≥ 3 and the sufficiency of nesting. | Added as item (c′), with the Effros check below. |
| B4 | OVERCLAIM | Appendix B's B4 stated the region at `[predicted]`-grade while B5 marks the region converse `[exploratory]`, and B4 cites 022, which cannot fail. | B4 split in Appendices B and F: region `[exploratory]`; refinability and rate loss `[predicted]`-grade on 023 [3]. |
| B5 | GAP | k = 2 achievability cited Kostina–Tuncel unconditionally while k ≥ 3 was "to be checked". | **Checked at the source** (arXiv:1707.09567): Kostina–Tuncel is a two-stage parametric characterization of the region's boundary, not a coding theorem, and it cites Effros (IEEE T-IT 45(6), 1999) for the extension to continuous alphabets and stationary sources. Paper III called it "the abstract-source successive-refinement coding theorem". Every achievability claim now rests explicitly on the Effros attribution, whose hypotheses are not yet checked at the source (the paper's PDF is a file download, held for the author's permission). |
| X1 | exposition | "The converse direction of the refinability criterion" reads as the proved necessity; "refinable" was undefined for k stages. | "The sufficiency of nesting"; refinable defined as achievability of the corner of cumulative rates. |
| X2 | exposition | Appendix B's B7, the Appendix F row and the custody table gave the corrected V no class. | `[exploratory]` until the net is in CI with a custody table (Track P). |
| X3 | exposition (older text) | prop:separation's flat-segment caveat is vacuous: R_C is convex and nonincreasing, so it is strictly decreasing wherever it is positive. | The statement now says the boundary ρR_C(D) = C > 0 is transmissible, with the one-line reason in the proof. |

**Checked and right (Task B):**
- **The separation proof.** Both of the expurgation fixes hold: the per-letter average of squared seminorms is a squared seminorm on ℝ^{nd}, so d(x₀,c) ≤ 4S_n; the S_n are uniformly integrable; and E[S_n 1_E] ≤ E[S_n 1{S_n > K}] + Kλ_n → 0 covers an E on the joint space.
- **cor:kobs.** The rescoping holds, and the Blocks step carries over.
- **The dispersion terms and bounds.**
- **The other fixes.** VI-34's #1, #3, #6, #10, #11 and the rescoped passages are right.

**Checked and right (Task A):** the water level, `sigma_star`, the dual function and gap
(identically 0 for the closed form), the joint program's encoding of the region and of R1 =
R1(D1) + δ, Csiszár's identity as a necessary condition, the factorization per coordinate,
the support of the output law, λ* = 1/(2θ), and the standard-error formulas.

## Owed

- A confirming pass on version 2 of the net and on this round's new text: the kernel-uniqueness
  argument in `cor:dispersion`, the separation boundary, the attribution paragraph and B4's
  split. Then CI wiring of the net (it needs cvxpy) and custody.
- Effros 1999 checked at the source: does its L-resolution theorem cover a continuous source
  with unbounded quadratic distortion? Until then, thm:region's equality and the sufficiency
  of nesting rest on that attribution.
