# VI-37: confirming pass on the VI-36 dispositions for Paper III (2026-11-21)

**Target.** The fixes made for VI-36 (`claims/audits/VI-36-PaperIII-nets-and-confirm.md`),
uncommitted at the time:
- version 2 of `experiments/verify_paper3_nets.py` and its result;
- in `paper/observation-theory.tex`: the Kostina–Verdú paragraph and kernel-uniqueness
  argument of `cor:dispersion`, the separation boundary, and the successive-refinement
  attribution with its echoes;
- Appendices B and F (B4's split, B5, B7).

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools, no cvxpy, and no access to the assistant's verdict. It re-ran
every non-solver part of the net from its file and seed. The m3 counts, L and v for every
sample row, and all 15 dispersion rows reproduced the committed JSON bit for bit. It also
rebuilt the generator as it was before the change made after version 2's second attempt.

**Verdict.** 2 errors, 3 gaps, 3 overclaims, 5 exposition items.
- **Resolved by version 2:** A1–A4, O1, O2, X1 and X2; A5 only partly.
- **Correct:** the new mathematics. The kernel-uniqueness argument checks line by line, and
  the separation boundary is valid, with "vanishes" holding under the stated hypotheses.
- **Not yet honest everywhere:** the attribution text is honest where it sits, but the
  headline statements contradicted it.

## Findings and dispositions (all applied, 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | ERROR | `chapters/appendix_a_related_work.md`, edited in this round, still said "the k ≥ 3 region is attributed to Kostina–Tuncel", contradicting the source check. | Rewritten: Kostina–Tuncel prove no coding theorem; achievability for k = 2 and k ≥ 3 is Assumption SR (Effros, unchecked). |
| 2 | ERROR (older text) | `chapters/ch07_cost.md` had three stale passages: refinable iff P₁ ⪯ P₂, tagged `[proved]` (refuted by VI-32); "the tight region is Kostina–Tuncel's"; and "effective dimension r_D" (refuted by NEG-18). | All three rewritten to match Appendix B and Paper III, each with a dated note of what it used to say. The VI-4 paragraph also notes that the check added then cannot fail either. A sweep of the book and README found no other `[proved]` tag on these results. |
| 3 | GAP | m4's "binding" test (dual μ > 1e-7) does not detect binding. In nested pairs the true μ is 0, but the reported duals rise like 1/δ (interior-point residue), so every sample row was "binding", the fallback could not be reached, and "0 unresolved" was no evidence. The escape hatch was a loophole by design. | Version 3: m4 fits gap = a + c√δ on δ ∈ {1e-5, 3e-6, 1e-6} for every pair, with no binding test and no escape hatch, gated as \|a\| ≤ 1e-5 + 0.01 L. The duals are reported, not used. |
| 4 | GAP (disclosure) | The generator change after version 2's second attempt was larger than disclosed: 8 of the 20 first draws of the nested-distinct class fell below the new floor, which is about 2800 times the ratio of the pair that crashed, and the change replaced pairs r22–r45. Under the final rule, attempt 2 would have failed m4. The criteria omitted the redraw rule. The "docstring's history" did not exist (the file was untracked). | The docstring's history now states all of this. The redraw rule is in the criteria, as a scope limit of the net. Version 3 runs on a fresh seed (20261126), with criteria written before its first run. |
| 5 | GAP | None of the 14 recorded m4 rows tested anything (all had gap ≡ 0 by construction); the fits on the 39 informative pairs were not recorded. | Every pair is recorded: gaps, intercept, tolerance, solver statuses and duals. |
| 6 | OVERCLAIM | All achievability rests on Effros, unchecked, yet the abstract, the introduction, the section opening ("we answer completely"), the statements of `thm:region`, `thm:multiobs` and `thm:multiobs-loss`, `cor:kobs`'s k = 2 clause, related work and open problem (c) asserted it, and only k ≥ 3 was called "not proved here". The flag "to be checked at the source" shipped in four places. | A named **Assumption SR** (successive-refinement achievability for this Gaussian quadratic case, any number of stages) replaces the attribution paragraph. Every converse is stated unconditionally; every achievability claim is stated under SR, the same way for k = 2 and k ≥ 3: `thm:region` (renamed "Two-stage rate region": contained in, and under SR equal to), `thm:multiobs` (nesting necessary; sufficient under SR), `thm:multiobs-loss` (a lower bound, attained under SR), `cor:kobs`, the abstract, the introduction, the section opening, related work and open problem (c′), which now names SR itself as open. |
| 7 | OVERCLAIM | B4's split graded refinability and the rate loss `[predicted]` on 023's check [3], which only computes the closed-form corner and takes the region as given. Necessity uses the unnetted region converse; sufficiency and the attained minimum use SR. | Appendices B and F: the max-det corner identity is `[predicted]`-grade; the region, refinability and the rate loss as coding statements are `[exploratory]`; B5 states the SR dependence for k = 2 too. |
| 8 | OVERCLAIM (minor) | m7's false-corner clause is arithmetic (a_false = a − 0.05 L exactly). m4's target also follows from compactness, so m4 is a consistency check of resolution 5e-6 + 0.005 L, and a true instance can trip it if the active set changes inside the fitted range. | The clause is dropped. The docstring states m4's resolution and that it is a consistency check, with m3 the tighter check on Σ°. |
| 9 | exposition | m5(a) does no quadrature on inactive coordinates: with P* = δ₀ the definition is closed form. It is not circular (it pins the y² coefficient, and is the only check that rejects the κ family), but it takes P* as given. | The docstring says so. The VI-36 record's A1 wording ("by quadrature") is superseded by this row. |
| 10 | exposition | The verifier recalled Theorem 12's moment restriction as a much higher power than 3 (unverified) and asked for the basic conditions (a)–(c) to be named, and for the arXiv numbering to be distinguished from the cited IEEE version. | **Not changed on the moment:** restriction (iv) was read on the page during the source check, "E[d³(X, Y*)] < ∞ where averaging is with respect to P_X × P_Y*", so the exponent 3 stands and the verifier's recollection was wrong. The corollary now names (a)–(c) and says the numbering is that of arXiv:1102.3944. |
| 11 | exposition | The uniqueness argument used `lem:info`'s equality cases without stating them, and gave Y = Ŷ + Z before the step that yields it. | Rewritten in order: Σ(Ŷ) = Σ* by uniqueness; both inequalities in `lem:info`'s proof are then equalities (independence; Gaussianity); the binding trace and `lem:cm` give Ŷ = E[Y\|Ŷ]; then Y = Ŷ + Z and deconvolution. |
| 12 | exposition | "Effros … extends the region to stationary sources and any number of resolutions" is second-hand, and leaves out the property that matters. | Now "which Kostina–Tuncel cite for the extension to continuous alphabets and stationary sources". |
| 13 | exposition | `prop:separation`: why R_C vanishes was unsaid, and the boundary argument (an achievability) sat under "Converse". Appendix B said "a net with inactive modes is owed" under a bullet that cites one. The JSON's `run` field was added by hand. | R_C(D) = 0 for D ≥ E d_C(X, x̂₀), finite by the reference letter; the boundary argument is labelled "Boundary (achievability)"; Appendix B points to the net; the harness now records its environment itself, and the JSON is saved exactly as printed. |

**Correction to row 1 (2026-11-21, after commit 5375b7b).** Row 1's applied text, and the
same phrase in Paper III's Assumption SR paragraph, said Kostina–Tuncel "prove no coding
theorem". That overcorrects. arXiv:1707.09567v2 proves a nonasymptotic converse bound (its
Theorem 3: a necessary condition for a two-stage excess-distortion code to exist, given its
code sizes, distortion levels and per-stage failure probabilities), which
recovers known dispersion converses. What it does not prove is achievability: for the
region's operational meaning it quotes Rimoldi for discrete memoryless sources and points to
Effros "for a generalization to continuous alphabets and stationary sources". Both passages
now say this. VI-36's "not a coding theorem" (its B5 row) is to be read the same way: not
the achievability theorem Paper III had cited it as. The substance is unchanged: Paper III's
achievability still rests on Assumption SR. Found by the assistant on rereading the source
while briefing the next confirming pass, not by a fresh context; that pass checks it.

**Correction to row 10 (2026-11-21, VI-38).** Row 10 is wrong. Kostina–Verdú's restriction
(iv) reads "E[d⁹(X, Y⋆)] < ∞ where averaging is with respect to P_X × P_Y⋆" (arXiv:1102.3944,
p. 7), a ninth moment. The verifier's recollection of a higher power was right, and the
assistant misread the page and overruled it. Paper III's `cor:dispersion` now says d⁹; the
conclusion is unaffected, since the Gaussian letter has every moment. See
`claims/audits/VI-38-PaperIII-confirming.md`.

**Confirmed resolved or right:**
- **m2:** a valid weak-duality certificate. Levels 1.2θ and 0.8θ both fail 150/150.
- **A3 and A4:** resolved.
- **X1 and X2:** resolved.
- **The kernel-uniqueness argument:** right line by line.
- **Restrictions (i)–(iii):** right, with d_max = Σγ_k.
- **The separation boundary:** right.
- **B7's class:** consistent across Appendices B and F and with CHARTER.

## Version 3 of the net (seed 20261126, as executed)

7/7 PASS in 33 s (Atlas; Python 3.12.3, numpy 2.4.6, scipy 1.18.1, cvxpy 1.9.3 with
Clarabel).
- **m1/m2:** logdet agreement 1.1e-7, \|dual gap\| ≤ 2.8e-14. VI-4's bug loses on 95 of 150
  (52 have rank-one P). The 1.2θ level fails 150/150.
- **m3:** 41 nested pairs (20 with distinct non-commuting observers), 40 non-nested, 1 in the
  excluded band; 75 cap-binding.
- **m4:** 574 joint solves, 11 inaccurate, 0 failures. The worst \|a\| is 13% of its
  tolerance; among the 38 pairs with L ≥ 1e-2, the largest \|a\| is 3.6e-6. "Always
  refinable" is refuted on 40 pairs.
- **m5:** definition agreement 1.8e-15; the κ family passes Csiszár and fails the definition
  at 32/32 inactive modes.
- **m6, m7:** the old constant is refuted in 10/10 configurations.

## Owed

- Effros 1999 checked at the source (FRONTIER G12b): its PDF is a file download, held for the
  author's permission. Until then Assumption SR stands as an assumption.
- A confirming pass on this round's changes before any B-theorem is promoted; then CI wiring
  of the net and custody.
