# VI-54: the D₀ bound and the gap paragraph of the T1 addendum, v0.2 (2026-11-22)

**Target.** The changes to `paper/t1-moving-kernel/t1-moving-kernel.tex` between commits
23d76a9 and a4ed9bb (v0.2):
- in the scope remark after Theorem A, a new upper bound D₀ ≤ λs₀ + Ks₀² = 3λ²/(4K), with
  its argument;
- in the example, the statement that D₀ ≤ 0.0021 for g₁, and what follows for the tested D;
- the reworded paragraph on the gap numbers.

The author asked for this pass on 2026-11-22: "run a fresh pass on the D₀ bound".

**Verifier.** A fresh-context general-purpose agent, local files only, read-only, with no
browser, connector or network tools and no access to the assistant's verdict. It:
- checked the D₀ argument line by line: admissibility of the test matrix, the direction of
  each inequality, the limit for an infimum, and the algebra;
- recomputed λ, K, s₀ and 3λ²/(4K) for g₁ independently of the JSON;
- reproduced every new number from `results/FT7-moving-kernel-net.json`;
- derived its own closed form for the loss of g₁ and checked it against one Monte Carlo
  point (4 million samples, about 1.2 standard errors) and one limit.

It did not re-run the net or the fire test, recompile the note, re-read the proofs of
Theorem A(b), Proposition B or Corollary C beyond what the new text uses, or check T1's
imported remainder.

**Verdict.** No mathematical error in the changed passages. The D₀ bound is correct and
correctly used, and every new number reproduces from the JSON.

## Findings and dispositions

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | O | The gap figures 5.4672, 5.4676 and 5.4635 are quoted to four decimals, but the family rates behind them carry sampling error of about 0.003, more than the 0.0004 between the two bounds on R_U. 5.4635 and 5.4672 come from different samples, so their difference is noise | The note now says the two bounds on R_U are 0.0004 apart, that the family's rate differs by 0.004 between the samples, and quotes "about 5.46 to 5.47" |
| 2 | E | The script's docstring still said D₀ "is not explicit", implying the smaller D are inside the proved range, and listed `prop:B` and `cor:C` under "Claims checked" | Docstring corrected. No code changed; the net was not re-run |
| 3 | X | "Has no numerical check" omitted check c3, which tests the identity g(s(u)) = u, trivially for g₁ | Said so |
| 4 | G | The comparison with ½log(1/D) + c₋ was not caveated where it is made; that side needs D < D₀ | Caveat added |
| 5 | G | The upper side's comparison value was never stated | "Against ½log(1/D) + c₊ = 6.158" added. The custody file now says this side needs only D < D₁ |
| 6 | X | The hypothesis s₀ < λ_min(Σ) is sufficient, not necessary | Said so |
| 7 | X | "Part (c) can only cover D below 3λ²/(4K)" could be read as saying the inequality fails above it | Reworded: the bound limits the proof's range, not the inequality |
| 8 | G | "No lower bound for D₀" is true of the note but improvable for the example (see below) | Not applied; recorded as a lead |
| 9 | X | The remark's title, "What the theorem does not cover", now holds a positive result | Retitled "Scope of the theorem" |

**A lead, not relied on.** With its closed form for the loss, the verifier estimated
D₀ ≈ 0.0014 for g₁, the infimum being approached at the remark's own test matrix. If that
holds, D = 10⁻³, 10⁻⁴ and 10⁻⁵ are inside Theorem A(c)'s proved range and 10⁻² is outside.
No second context has checked the formula, and the minimization is a grid with a simplex
polish, not certified. The verifier also noted that the committed JSON already implies
D₀ ≲ 0.0014 from one of check c1's adversarial cases, which confirms independently that
D = 10⁻² is outside the range.

**After the fixes.** The note is v0.3 and compiles to 5 pages with no undefined references.

**Whether a further pass is owed.** The v0.3 changes are wording and one docstring. No
further pass is run on them. No pass has read the net's code since 45cbc15. The author has
not said he has read the proofs, and the prior art remains unread.
