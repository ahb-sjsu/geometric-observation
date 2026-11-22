# VI-51: confirming pass on VI-50's dispositions (2026-11-21)

**Target.** The Lean files after VI-50's fixes, read against
`paper/consumer-relative-landauer.tex`, the same version as in VI-50 (sha256 `ad5ed7e8…`):

| File | sha256 prefix | What changed |
|---|---|---|
| `lean/ObservationTheory/ConsumerLandauerBlocks.lean` | `f92fd89e` | the header; `pathLaw`, `future_mass`, `pathLaw_zero`, `pathLaw_succ_tail`, `pathLaw_marginal`, `stale_monotone_path` (new); `cor3m_coordinated_attained` (new); docstrings |
| `lean/ObservationTheory/ConsumerLandauerIdentities.lean` | `2ce899ef` | the `cor3_joint_lower` docstring |
| `lean/ObservationTheory/FiniteEntropy.lean` | `e471f448` | the header contents list |
| `lean/ObservationTheory/BlockLLN.lean` | `026967ae` | new: independence, second moment, Chebyshev |

The question was faithfulness, not proofs: Lean checks the proofs.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It ran read-only git
commands and no compile. `Covering.lean` was outside its target and has had no faithfulness
reading.

**Verdict: the dispositions have converged.** There are no (A) or (B) findings.

- **`pathLaw` is the law of `(M, X₀, …, X_T)` under Prop 6's hypothesis.**
  - The indexing is right: X₀ is coordinate 0, and the product runs over the steps
    s = 0, …, T − 1.
  - The kernel's direction agrees with `ageStep`.
  - `pathLaw_marginal` and `stale_monotone_path` together state "L_t = H(M | X_t) is
    nondecreasing in t" for that process.
  - Nothing is vacuous.
- **Dispositions 1–8 are present and correct.** Disposition 10 was partial.
- **`cor3m_coordinated_attained`'s memory type is the code `Mⱼ = Uⱼⁿ`.**
- **BlockLLN's statements are the standard facts.** None of their hypotheses is degenerate.
- **The one-point instantiation was checked:** `condH` reduces to `H(M)`, and `condMI` to
  `I(Xᵢ; X̂ᵢ)`.

## Findings (all D) and dispositions

| # | Finding | Disposition |
|---|---|---|
| 1 | The hypothesis enters as the factorization. Its equivalence with the conditional-independence phrasing, and "stationary ⇒ homogeneous on the support", are not proved | Stated in the header and the `pathLaw` docstring |
| 2 | "For an inhomogeneous chain apply `stale_step` step by step" reads as covered | Reworded: an inhomogeneous chain is not formalized; `stale_step` is its one-step form |
| 3 | The `pathLaw` and `stale_monotone_path` docstrings omit "time-homogeneous" | Added |
| 4 | The header does not name `stale_monotone` | Named |
| 5 | `content_le_log_card` is the first link of the rate chain only with a one-point side-information type | Reworded: it is `L_n ≤ R_n`, and it is that link with a one-point type |
| 6 | The one-point instantiation gives only the outer ends of the rate chain | Reworded: "the outer ends of the rate chain, `log |ℳ| ≥ H(M) ≥ ∑ᵢ I(Xᵢ; X̂ᵢ)`" |
| 7 | The FiniteEntropy contents list still omits five helpers; its line 5 is stale | Helpers listed; line 5 reworded |
| 8 | The `cor3m_*` docstrings say "exactly" without "at every source sequence" | Qualified |
| 9 | "A weak law of large numbers": only Chebyshev's bound at finite n is proved | Reworded: "Chebyshev's bound, the quantitative weak law (the limit is not stated)" |
| 10 | VI-50's P1 suggested that the paper's monotonicity needs time homogeneity; it does not | VI-50's record corrected before P1 goes to the author |

**After these fixes.**
- **Build:** all seven modules, `Covering.lean` included, compile from scratch with zero
  `sorry`.
- **Axioms:** all 49 audited theorems depend only on `propext`, `Classical.choice` and
  `Quot.sound`.
- **Build record:** `paper/consumer-relative-landauer-lean-blocks-2026-11-21.txt`.
- **No further pass:** none is owed on these wording changes, since they add no mathematics.
  `Covering.lean` needs its own faithfulness reading before it backs any claim.
