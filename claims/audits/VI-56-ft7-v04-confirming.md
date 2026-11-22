# VI-56: confirming pass on the T1 addendum v0.4 after VI-55 (2026-11-22)

**Target.** Commit 5b9d1c8: the note `paper/t1-moving-kernel/t1-moving-kernel.tex` (v0.4),
the net `experiments/verify_ft7_exact.py` with `results/FT7-exact-net.json`, and the
records (the VI-55 audit file, the custody file `claims/custody/T1-MK.md`, the T1-MK and
VI-55 ledger rows, the FT.7 frontier row). The pass covered the material no fresh context
had read:
- `prop:gapex`, the gap constant of the example;
- the dispositions of VI-55;
- the text added after VI-55's reading (the support sentence in `thm:A`(b), the
  strict-inequality remark in `thm:reduce`(b), the paragraph on fibers, the method
  statement for h(U), the limits, the prior-work paragraph for internal consistency, the
  reordered numerical section);
- the net's check e5 and mutant m6.

The request for this pass, 2026-11-22: "yes, run the confirming pass".

**Verifier.** A fresh-context general-purpose agent, local files only, read-only, with no
browser, connector or network tools and no access to the assistant's verdict. It:
- re-derived `prop:gapex` step by step, with h(U) by its own quadrature (1.598216176507,
  error estimate 2·10⁻¹⁴) and the entropy step at a ∈ {0.3, 1, 3} and five values of D;
- re-ran the net (identical apart from the timing field) and its fire test (6 of 6);
- checked every number of the exact-loss paragraph against the JSON;
- compiled the note in a scratch directory (9 pages, no undefined references).

It did not check T1's imported remainder, the cited papers, the first net, or the proofs of
`thm:sharp`, `cor:C`, `cor:gapq` and `prop:exact` beyond their use.

**Verdict.** No mathematical error in the material added after VI-55. One example violated
the note's standing assumption, and one net check could not fail on the quantity its
docstring named.

## Findings and dispositions

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | E | "Output laws and images" used g(x) = (x₁, x₁²), whose derivative is unbounded, against the standing assumption of three bounded derivatives | Replaced by g(x) = (x₁, sin x₁): bounded derivatives, a sine curve for image, no density in R², a measurable right inverse |
| 2 | O | "Codes": "a code that adapts its error covariance … can do better; Proposition B is exactly such a comparison" is an operational claim; the proposition is about information rates | Reworded as a statement about test channels; "no statement about codes is made" |
| 3 | O | Prior work: "the pointwise read rank is constant" describes the example; the note assumes constant rank nowhere | "In the example here the pointwise read rank is one everywhere" |
| 4 | O | The custody file still said "transversal", which the note now disclaims | The note's wording used |
| 5 | G | Check e5's two "excess" comparisons are one identity in which h(U) and Var U cancel: both say the family's rate is within 10⁻⁴ of R₀(D). They test the constant of `thm:sharp`, not h(U) or c′₊ against c′₋. Mutant m6 was caught only by a guard written for it | Docstring and note say so. h(U) now has a second quadrature method in the verdict (agreement 3·10⁻¹³). Two mutants added: m7, the entropy step with the bound ½ log(1 + D/Var U); m8, h(U) shifted by 10⁻⁶ |
| 6 | G | K_f was defined as the value of `eq:K`, which is 0 for an affine consumer | "Any constant at least that value" |
| 7 | G | The ledger's VI-55 and T1-MK rows omitted `prop:gapex` and that VI-55 had passed over an unsupported claim | Both rows amended |
| 8 | G | `prop:gapex`'s proof gave no range for the two sides of the expansion | Both sides stated, with their ranges |
| 9 | X | "Theorem A needs q = p and says nothing about it": true only for r < p | Said so |
| 10 | X | "No stated range of D"; the range is stated, not explicit | "No explicit range" |
| 11 | X | The custody file gave K as the value of `eq:K`; the note's parenthesis was ambiguous | Both reworded |
| 12 | X | Custody rows: a four-decimal figure hid that the measured value is below the leading term by the O(D) term; "0.014 below, 0.0011 above" was the wrong way round | Six decimals; wording corrected |
| 13 | X | Statements about the author's acts that were not quotations: "the author supplied", "the author pointed out … and supplied the missing step", "the author did", "the author has not yet read the proofs". The verifier could not confirm from local files who wrote the `prop:gapex` argument | Reworded throughout to what is on record: the review of v0.2 and the later notes were passed on by the author in the working session of 2026-11-22; their writer is not stated. "No statement by the author of having read the proofs is on record" |
| 14 | X | The custody file dated the note's footnote 2026-11-21 | Corrected |
| 15 | X | The custody file's sentence about its own fresh-context read did not say that read covered the first version only | Said so |
| 16 | X | VI-55's disposition #9 (a forward reference to `cor:gapq`) was superseded by `prop:gapex` | Noted in the VI-55 file |
| 17 | X | FRONTIER read as if the fire test were in CI | Corrected |
| 18 | X | Notation collisions; H_a against H of `thm:reduce` invites a misreading | H_a renamed Θ_a in the note and the custody file. The others (B, f, s, W, r reused locally) are left and recorded here |

**After the fixes.** The note is v0.5, 9 pages, with no undefined references. The exact net
passes 5 of 5 checks at seed 20261122 and its fire test catches 8 of 8 mutants.

**Whether a further pass is owed.** The changes after this pass are a replaced example, the
two-line expansion in the proof of `prop:gapex` (which the verifier itself derived), a second
quadrature method and two mutants in the net, wording, and records. No further pass is run
on them. No fresh context has checked the assistant's reading of the three prior-work
papers, and no statement by the author of having read the proofs is on record.
