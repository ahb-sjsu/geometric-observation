# VI-52: the T1 addendum on moving read kernels, and its net (2026-11-21)

**Target.**
- The note `paper/t1-moving-kernel/t1-moving-kernel.tex`, v0.1, then uncommitted: Lemma 1
  (the kernel of Q), Theorem A (fixed-covariance Gaussian test channels), Proposition B (a
  section turns the consumer's rate into an output rate), Corollary C (the rate gap), and
  the example g_a(x) = x₁ + a sin x₂.
- The net `experiments/verify_ft7_moving_kernel.py` and its output
  `results/FT7-moving-kernel-net.json`, as committed in ec4367b.
- The cited parts of the frozen T1 note, for the constants the addendum takes from it.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It read every proof
line and re-derived each constant by hand. It also:
- re-ran the net: verdict and numbers identical apart from the timing field;
- ran its own grid over all 2×2 covariances for g₁;
- ran its own adversarial cases for Theorem A(a);
- checked the entropy and variance of U by independent quadrature.

**Verdict.**
- **No mathematical error in any numbered statement.** Lemma 1, Theorem A (a)–(d),
  Proposition B (a)–(c), Corollary C and every stated quantity of the example are correct
  as stated. The constant K matches T1's proof.
- **Two overclaims in the prose.**
- **A real weakness in the net.** Its slope checks ran on hand-picked achievable families,
  so they could not fail if the lower bound, Theorem A(c), were false.

## Findings and dispositions

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | O | The closing sentence said "the codes T1 serves pay a growing price", a claim about codes, against the note's own scope | Reworded to the fixed-covariance Gaussian test channels behind those codes |
| 2 | O | The abstract stated the excess for any moving kernel, with coefficient (q − r)/2; what is proved is (p − k)/2 under Q ≻ 0, a closed convex image and a regular output law | The abstract now states those conditions, and that the statements are about test channels and information rates |
| 3 | G | The net's slope checks (c2) could not fail if Theorem A(c) were false; "optimal by symmetry" was unproved | New check c5 minimizes the rate over all 2×2 Δ for g₁ and tests its slope, its distance from the family, and Theorem A(c)'s bound. The docstring and the note now say c2 tests the upper bound only |
| 4 | G | Check c1 never sampled the tight direction | Adversarial Δ along the least eigenvector of Q added; K and s₀ recorded for g₁ |
| 5 | G | Fire mutants m2–m4 only compared measured slopes with other numbers | Two instrument mutants added (m5, m6): the full minimization on a fixed-kernel consumer and on a corrupted loss must fail the slope check |
| 6 | E | Check c3 for g₁ never called g, so it was vacuous | It now evaluates the consumer on the section's output |
| 7 | G | R_U^A was not defined as an informational infimum; measurability unaddressed; "coding" and "decoder" language with no coding theorem | Definition stated; the image is σ-compact, hence Borel; the section is retitled, and it says no coding theorem is invoked and what one would need |
| 8 | X | The constants c and D₁ of Theorem A(d) were not displayed | Displayed |
| 9 | X | A measurable section probably always exists (the verifier's recollection of a uniformization theorem, unchecked) | Not asserted. The note now says the substance of the hypothesis is that the decoder holds a section |
| 10 | G | "U has a density, so J_g has rank k on a set of positive probability" was asserted without proof | The claim is dropped. The corollary is stated with k, and identifies k with r only when J_g has rank k almost everywhere |
| 11 | X | "Its proof gives ρ_b"; the Cover–Thomas citation for the vector Gaussian bound is imprecise; the Misra entry incomplete | Reworded; the Cover–Thomas flag stays in the source; the Misra–Goyal–Varshney entry completed from a search |
| 12 | X | Theorem A(b) when the set is empty | One clause added |
| 13 | X | The script's docstring used names that the PDF does not, and a stale check list | The docstring now refers to labels and lists what each check can fail on |
| 14 | X | The note was untracked while the script citing it was committed | Committed with these fixes |

**After the fixes.** The net passes 22 of 22 checks at seed 20261131, and its fire test
catches 6 of 6 mutants. For g₁ the least rate over all covariances has slope 1.0009 in
ln(1/D), sits within 0.004 nats of the family tQ⁻¹, and stays above Theorem A(c)'s bound.

**Prior art.**
- Linder–Zamir and Linder–Zamir–Zeger could not be obtained and are unread.
- Misra–Goyal–Varshney was read in part: the first half of its arXiv version, through an
  automated summary. It states that an encoder which knows the function can do no better
  than compute it and encode the result, which is Proposition B's idea.
- The note credits that remark and makes no claim of priority.

**Owed.** A confirming pass on these dispositions, chiefly the new check c5 and the two
instrument mutants. The author has not read the proofs.
