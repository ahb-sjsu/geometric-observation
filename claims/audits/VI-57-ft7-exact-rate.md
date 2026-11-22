# VI-57: the exact fixed-covariance rate of the sine example, and the "Main results" section (2026-11-22)

**Target.** The uncommitted v0.7 of `paper/t1-moving-kernel/t1-moving-kernel.tex`:
- the new Proposition `prop:rate`: for g₁ = x₁ + sin x₂, Σ = I and 0 < D ≤ 10⁻², R_fixed(D)
  is −½ log of the maximum of a strictly concave one-dimensional function, with an explicit
  minimizing covariance;
- the section "Main results", added in v0.6 (commit ed0468c) and never reviewed;
- check e6 and mutant m9 of `experiments/verify_ft7_exact.py`, with
  `results/FT7-exact-net.json`.

**Where the result came from.** The assistant derived `prop:rate` on 2026-11-22, after a
list of remaining limits, passed on by the author with no instruction, named the lack of a
certified minimum. The pass was started on the assistant's own initiative, under the rule
that a new proof gets a fresh-context pass before it is asserted.

**Verifier.** A fresh-context general-purpose agent, local files only, read-only, with no
browser, connector or network tools and no access to the assistant's verdict. It:
- checked the proof line by line, every numerical bound with 50-digit arithmetic;
- solved the one-dimensional problem with its own 50-digit root-finder at five values of D;
- ran its own constrained minimization over 2×2 covariances in a different parametrization
  (60 random starts; agreement to 10⁻¹⁴) and a polar grid of 721 × 481 rays (never below the
  proposition's value);
- derived the expansion R_fixed(D) = R₀(D) − c₁D + O(D²), c₁ = 0.676952;
- re-ran the net (identical apart from the timing field) and its fire test (9 of 9);
- compiled a scratch copy of the note (10 pages, no undefined references).

It did not check how far above D = 10⁻² the proposition holds, the case a ≠ 1, `prop:exact`
beyond the formula for F″ and F(1), the Monte Carlo script, or the record files.

**Verdict.** No mathematical error in `prop:rate`, its proof, or the "Main results" section.
Every numerical bound in the proof holds with slack.

## Findings and dispositions

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | O | The range 0 < D ≤ 10⁻² was dropped where the proposition is cited (three places), and "the value of a concave problem" should be −½ log of its maximum | Range and wording restored in all three |
| 2 | G | The proof used 0 < v ≤ 1 and F ≥ 0 without saying so | One sentence added at its start |
| 3 | X | "Not the minimizer, although within O(D)" can be said exactly: the minimizer is v\* times the matrix with diagonal (F′(v\*), 1) and off-diagonal −e^{−1/2}; Q⁻¹ has F′(0) there | Stated. The expansion with c₁ = 0.67695 is quoted as the verifier's derivation, not proved in the text |
| 4 | X | "Agrees to 10⁻¹³" and "known to floating-point accuracy" are observations of one run; the script requires 10⁻⁹ and there is no rounding bound | Said so |
| 5 | X | "The fire test has six mutants" was stale | Corrected to ten |
| 6 | X | Main results: "all of these are statements about fixed-covariance Gaussian test channels" is not true of R_C; the gap display lacked "(D → 0)" | Both corrected |
| 7 | X | Net: the loss check was an identity by construction and did not use the proposition's formula for d₁₁; the bracket condition is implied by the root-finder | d₁₁ is now computed from the proposition's own formula; the docstring says what each condition can catch |
| 8 | X | Mutant m9 fails by 0.52 nats and does not probe the 10⁻⁹ tolerance | Mutant m10 added (d₁₂ scaled by 0.99; fails by a few 10⁻⁶) |
| 9 | X | Docstring: `prop:rate` unlisted; "200,000 random" is 40,000 per value of D; the note on e3's search out of date | Corrected. The docstring also records the verifier's point that the loss is concave, not monotone, along a ray |
| 10 | X | Symbols reused: κ, φ, G | Renamed η, Φ_D, Ψ in the proposition; η = det Θ₁ noted |
| 11 | X | The footnote did not say where `prop:rate` comes from | Added |

**After the fixes.** The exact net passes 6 of 6 checks at seed 20261122 and its fire test
catches 10 of 10 mutants. The note is v0.7, 10 pages, with no undefined references.

**Whether a further pass is owed.** The changes after this pass are wording, renamed
symbols, one sentence of hypotheses in the proof, the quoted expansion (the verifier's own),
one mutant, and one net condition made stricter. No further pass is run on them.

**What stays open** (from the list of limits of 2026-11-22):
- an explicit lower bound on D₀ for a general consumer;
- images that are not closed and convex, and outputs with no density: the stratification
  by the rank of J_g is not done, and R_U restricted to the image is not evaluated there;
- a certified minimum for any consumer other than g₁, and for g₁ above D = 10⁻² or a ≠ 1;
- the query model for learning a selection of fiber representatives (frontier item FT.9).
