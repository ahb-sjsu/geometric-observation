# VI-53: confirming pass on VI-52's dispositions (2026-11-21)

**Target.** The state at commit 4f55b41:
- the note `paper/t1-moving-kernel/t1-moving-kernel.tex`;
- the net `experiments/verify_ft7_moving_kernel.py` and its output;
- the CI wiring in `ci/reproduce.py`;
- the VI-52 record, its ledger row, and the FT.7 and FT.9 rows of `claims/FRONTIER.md`.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It re-derived every
proof step and constant by hand. It also:
- re-ran the net: output identical apart from the timing field;
- re-ran the fire test: 6 of 6;
- cross-checked the search for the least rate with its own independent optimizer, which
  agreed to 10⁻⁵ at all four values of D;
- ran the search on a fixed-kernel loss at 37°, off the script's angle grid.

It did not check the prior-art sources or the GitHub run.

One hygiene note from the verifier: importing the net module wrote a gitignored bytecode file
under `experiments/`, which it deleted.

**Verdict.**
- **No error in the mathematics or the net code.** All 14 of VI-52's dispositions were
  present. The constants of Theorem A(d), the empty-set clause, the new definition of the
  restricted output rate, and Corollary C's constants are correct.
- **Not yet converged at 4f55b41:** three overclaims remained in the note's prose, and one
  numeral was misrounded.

## Findings and dispositions

| # | Sev. | Finding | Disposition |
|---|---|---|---|
| 1 | O | The abstract called T1's weight "the right object" for a fixed kernel; the note's own remark says it proves nothing there | Reworded: T1 bounds the price when the kernel is fixed and its sandwich assumption holds |
| 2 | O | The abstract's list of hypotheses omitted the measurable right inverse | Added |
| 3 | O | The closing sentence gave two conditions and the pointwise rank; what is proved is Corollary C | Restated as Corollary C with k < p and the (p − k)/2 coefficient |
| 4 | X | The fourth Theorem A(c) value was printed 9.544; the JSON rounds to 9.543. The values used a Monte Carlo λ | The net now computes the bound from the exact λ_min(Q) = 0.13993; the note prints 2.639, 4.941, 7.244, 9.546 |
| 5 | X | "Where it is tight": Theorem A(a) is not tight there; the ratio tends to 1/2 | Reworded |
| 6 | X/G | "Stays above the bound of Theorem A(c)" at D = 10⁻², outside the proved range D < D₀ | Said so; and that the gap is a constant 1.85 nats, so the slope is the sensitive check |
| 7 | X | "Decoder" language after the section says no coding theorem is invoked | The note says "decoder" is informal; the net's docstring says "section map" |
| 8 | X | "Minimizes over all covariances" is a numerical search, not a certified minimum | Reworded in the note and the docstring |
| 9 | X | The prior-art sentences stated a half-read paper's content flatly | Prefixed "according to that summary"; the comparison with Proposition B is "as far as we read" |
| 10 | X | A method docstring still said "optimal by symmetry" | Corrected |
| 11 | G | Check c5 was one-sided and compared two different samples | The family is now also evaluated on the search's own sample; the check is two-sided at 10⁻³ (observed 10⁻⁴) |
| 12 | G | Mutants m5 and m6 passed on "slope is not 1", which garbage would also satisfy; both ignored a direction on the angle grid | Both must now return slope 1/2 within tolerance; m6's ignored direction is at 37° |
| 13 | X | Check c3 for the main instance is correct but nearly trivial | Left as is; recorded |
| 14 | G | CI wall-time risk under the 1,800 s limit | Read from the GitHub log of run 44981387791: the net took 113.1 s on the runner. No change |
| 15 | X | The note was not compiled in CI | Added to the paper job, with the undefined-reference check |
| 16 | X | FRONTIER's FT.7 row led with a stale "not yet in CI" sentence | Marked superseded |

**After these fixes.** The net passes 22 of 22 checks at seed 20261131 and its fire test
catches 6 of 6; the two instrument mutants both return slope 0.5000. The note compiles to 5
pages with no undefined references.

**Whether a further pass is owed.** The changes after this pass are wording, one
recomputed bound, and tighter checks; they add no new mathematics. No further pass is run
on them. The author has not read the proofs, and the prior art (Linder–Zamir,
Linder–Zamir–Zeger) remains unread.
