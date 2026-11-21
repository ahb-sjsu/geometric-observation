# VI-35: confirming pass on the GO-16 corrections (2026-11-21)

**Target.** The fixes applied for the findings of VI-33 (`claims/audits/VI-33-GO16-corrections.md`)
in commit 36604a1: `paper/go16-adversarial-observer.tex` (Theorems 3–6, the corollaries,
the title block, abstract and status text), the net `experiments/verify_go16_diagonal.py`
and its JSON `results/GO16-diagonal.json`.

**Verifier.** A fresh-context general-purpose agent, working from local files only, with no
browser, connector or network tools and no access to the assistant's verdict. It re-derived
the corrected Theorem 3 by hand, and wrote its own check: a k-subset epigraph LP (a different
formulation from the harness's), plus a reader-side LP giving each attention's full range over
the optimal face. It ran this on 803 instances, 507 of them flat stretches of J, 150 of those
with J′(0+) = 0, built on purpose.

**Verdict.** The corrected Theorem 3 core holds, with **0 violations** of the value, the
blackout iff, the optimal face (= the segment {ρ(t)}), the uniqueness clause, the tie and
its value, or any attention range. A first run at a looser slack showed 13 deviations of at
most 3e-5, which vanished at slack 1e-12 (tolerance artefacts). The paper's witness, its
θ_j = 0 example and its integral example reproduce. Counts: 1 error (minor), 1 gap,
3 overclaims, 6 exposition items.

## Findings and dispositions (all applied, 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | ERROR (minor) | Theorem 3 (blackout paragraph) and Corollary 2 said "every saddle W* has a fractional *entry*", then "the reader must mix". A projection can have fractional entries (vvᵀ with v = (e₁+e₂)/√2), so the implication fails as written; the argument proves a fractional *eigenvalue*. The trace claim tr W*_SS = k−\|C\| also silently needs W*_CC = I, which forces W*_CS = 0. | Both now say no saddle W* is a projection. The blackout paragraph gives the block step: the diagonal is 1 on C, a row of 0 ⪯ W ⪯ I with a unit diagonal entry has no other entry, so W* = I_C ⊕ W*_SS, whose S-block is ≻ 0 with trace k−\|C\| < \|S\| and so has an eigenvalue in (0,1). |
| 2 | GAP | The net did not cover the clauses VI-33 corrected: a text putting back VI-33's E1 (non-uniqueness) or E2 (θ_j ∈ (0,1)) would still pass 6/6; nothing checked uniqueness, θ_j at the ends of a stretch, or the tie at an interior t*. VI-33's 3000-instance run is not committed. The docstring's premise was wrong: 32 of the 601 random instances are flat stretches (every positive-level optimum with nothing contested is one), none with contested coordinates. The paper's "nets Theorem 3 as corrected" overstated. | The harness gains d7 (the whole optimal face against the segment {ρ(t)}, by the k-subset LP, and the uniqueness clause), d8 (the tie and its value at both ends and the midpoint of the minimizer interval) and d9 (every coordinate's attention range from the reader-side LP, including the stretch ends and the blackout range), ported from this pass's check, on their own random stream with the three fixed cases and constructed flat stretches; coverage floors written before the first run. First run: 603 cases, 317 flat stretches, 0 violations, 9/9 PASS; d1–d6 reproduce field for field. Mutations on copies: E1 put back fails d7; θ_j = J′(μ_j−)/λ fails d9; "tie iff contested" inside the interval fails d8. The docstring's premise is withdrawn in place, and the paper describes d1–d9. |
| 3 | OVERCLAIM | The title block still led with "Statement v0.5 … R-IND-5-verified for Theorems 1–3 … and GOVERNED". | It now leads with v0.6: Theorem 3 refuted as sealed and corrected; checked, re-checked and confirmed (VI-30, VI-31, VI-33, VI-35); netted, ungoverned. |
| 4 | OVERCLAIM | The abstract offered "numerical harness ALL PASS 9/9" as verification; that harness passed the refuted statement (its V6 is circular), and the abstract did not mention the new net. | The abstract says so and cites `verify_go16_diagonal.py` (9/9, in CI). |
| 5 | OVERCLAIM | Theorem 5 (`thm:commuting`) said "the governed face is 090's V9"; 090 governs a refuted statement, V9 is one positive-level instance, and the blackout regime has no rotated face. | Scoped to exactly that. |
| 6 | exposition | The verification paragraph said the new net checks "not the attention bookkeeping" (d5 now does), and the net paragraph left out d5 and d6. | Both aligned with the harness (d1–d9); the full program's KKT conditions remain standard-cited. |
| 7 | exposition | The poker remark and the abstract: "the reader also mixes on a level coordinate" (θ_j is 0 or the cap at the ends of a stretch, as always in the integral regime); blacked-out θ "not pinned" (it is pinned when J′(0+) = 0); "each side's mixture is pinned" (the encoder's contested ρ_i = t*/μ_i is not unique on a contested flat stretch; in the E2 instance ρ₁ ranges over [¼, ½] and ρ₂ over [½, 1]). | "can mix", "pinned only when J′(0+) = 0", and "pinned given t*", with the non-uniqueness stated. |
| 8 | exposition | `frontier_attained` "proves the 'if' half for ε ≤ ½": ε is undefined there; the correct scope is the u = 1 branch. | Fixed. |
| 9 | exposition (harness) | d2's blackout sub-checks follow algebraically from slope0 ≥ 0 and k < n, so they cannot fail on their own; d2's iff compares the theorem's J with its own slope formula, not with the LP. | Stated in the harness docstring; the LP-side blackout coverage is now d7–d9's. |
| 10 | exposition | 0 was called a "breakpoint" of J; it is the end of the domain. | Fixed. |
| 11 | exposition (record) | VI-33's record said "X1–X8" over ten bullets. | The record's heading corrected, with a note. |

Outside the scope given, the verifier noted that the LEDGER GO-16 row still showed
`[predicted] ✅ (theorems netted)` while the paper says the theory gate is not cleared. The
row's status cell is corrected: `[predicted]` stands for what 090 and 091 still support,
Theorem 3 as sealed is refuted, and the corrected Theorem 3 is netted, ungoverned.

**Mutation runs on the old net (d1–d6), by the verifier.** d1 caught minimizing J over the
μ_j only (the sealed statement), a ×1.0001 conceded term, a wrong C, ρ = min(1, t/μ)², and
conceded ρ ≠ 1. d2's iff caught a slope without its −λ\|C\| term. d3 caught the sealed "tie
iff contested" and "tie always". d4 is a power check. d5 caught contested θ = s²/μ (λ dropped)
and a reversed blackout bound. d6 caught ρ = min(1, t/μ)² and conceded ρ ≠ 1. Nothing caught
the E1 or E2 reversions, θ_j = J′(μ_j−)/λ, or a wrong tie value; d7–d9 now do.

**Not checked by this pass:** the LaTeX compile, Lean, a non-diagonal SDP (no cvxpy on the
verifier's machine), and Theorems 4–6 beyond the VI-33 items.

## Owed

- Custody for the corrected Theorem 3, once the diagonalization step is either netted or
  recorded as a proved-not-netted gap.
- A rotated (non-diagonal) face for the blackout regime, which neither the governed record nor
  the net has.
