# VI-47: confirming pass on VI-46, Paper III's new derivation, and Paper V's citation (2026-11-21)

**Target.** The uncommitted round after VI-46, against 1e8c5fb:
- **Paper III's new mathematics:**
  - the closed-form clause of `lem:maxdet` for any cap C ≻ 0, and its proof;
  - the "only if" half of L = 0 iff Σ₂⋆ ⪯ Σ₁⋆ in the proof of `thm:multiobs-loss`;
  - the pointer in consequence (ii).
- **Paper V's citation of Polyanskiy and Wu**, MIT 6.441 notes (Spring 2016), Theorem 24.2, for
  Corollary 4's operational equality, together with the two exposition edits to Corollary 4's
  proof.
- **Every disposition of VI-46's 14 findings,** across:
  - the custody files;
  - the LEDGER rows PAPER-III.a, PAPER-III.b and PAPER-V.a to PAPER-V.d, and the VI-46 row;
  - FRONTIER, the README and the VI-41 note;
  - Appendices B, D and F and Chapter 7.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. Its checks:
- **re-derived** the closed form and the "only if" half by hand;
- **tested the closed form** with its own code on 2,342 random instances (singular P̃,
  repeated eigenvalues, d = 1 to 6): the worst dual gap was 4.6e-12, the dual matrix was always
  positive semidefinite, and no random feasible competitor beat it;
- **read Definition 23.1 and Theorems 23.2 to 23.5 and 24.1 to 24.4 at the source**, in the
  copies downloaded with the author's permission;
- **compiled both papers** in a scratch copy, with no undefined references or citations.

**Verdict.**
- **The new mathematics is correct, and the citation is sound.**
- **0 errors.**
- **PAPER-V.a and PAPER-V.b stand.**
- **PAPER-III.a stands once this pass is logged.** Until now no fresh-context reading covered the
  derivation its new clauses rest on.
- **Counts:** 1 gap (that timing) and 10 exposition items.
- **Convergence.** With no error, the confirming rule asks for no further pass, so this round
  has converged.

## Findings and dispositions (applied 2026-11-21)

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | GAP / OVERCLAIM | Every record listed VI-46 as covering PAPER-III.a, but VI-46 read the text before the derivation existed. The row was marked `[proved]` before T-CUST-1's second part held for the changed clauses. | **This pass is logged as the first reading of the derivation.** It is added to the R-IND-5 column, the custody file, FRONTIER and Appendix B. The custody file records that the draft was marked `[proved]` before this pass, and that nothing was committed until after it. |
| 2 | exposition | "Concave with linear constraints and a strictly feasible point, so its KKT conditions are sufficient" is a non sequitur: Slater gives necessity, while concavity with affine constraints gives sufficiency. The multipliers on w_k ≤ 1 were not exhibited, and the case w_k = 0 was not mentioned. The "if" direction in `thm:multiobs-loss` silently uses uniqueness. | The proof now says any KKT point is optimal and exhibits λ = 1/θ and μ_k = (1 − p̃_k/θ)₊. The case w_k = 0 is noted. The "if" direction names the uniqueness it uses. |
| 3 | exposition | The custody file said m1 and m2 test the cap Σx only. In fact they draw 150 random positive definite caps, which are generic caps. | Reworded. |
| 4 | exposition | The custody file said VI-40 confirmed 1c155b1, "the last change to these results". 1c155b1 touched neither result. `lem:maxdet` last changed in ab63c7c (2026-07-17) and `thm:multiobs-loss` in 287f349 (its title), which VI-39 read. | Corrected, and VI-39 added. |
| 5 | exposition | PAPER-III.a's claim sentence omitted P ⪰ 0 and D > 0. | Added. |
| 6 | exposition | The bib entry repeated the year, lowercased the title, gave no URL, chapter or page, and used a title that does not appear in the source files. | Rewritten: the course title in braces, "MIT OpenCourseWare", ch. 24, p. 247, the URL and an access date. |
| 7 | exposition | "A code with M messages has Landauer content at most log₂M": L_n is per symbol, so the bound is nL_n ≤ log₂M. "Approach L_C(D)" silently used the per-code converse and R_C = L_C. | Fixed in Paper V, with both steps named. |
| 8 | exposition | The limits paragraph's "the cited coding theorem" had no antecedent, and the note "checked against its source" did not say by whom. | The limits paragraph now cites Theorem 24.2. The note says the author's assistant checked it, and then a fresh-context reading. |
| 9 | exposition (the author's words) | FRONTIER G11 and the custody file said the author agreed that "these results" get a row; the question covered all of Paper III's netted results, and the split into III.a and III.b was not put to the author. VI-46's record said the author "asked for" the download. | Both say so now. The record says "allowed". |
| 10 | exposition | PAPER-V.b's custody file did not say the citation's independent reading was owed, and the README's Paper V entry omitted VI-46. | Both updated with this pass. |
| 11 | exposition | The docstring of `verify_paper3_nets.py` still says `lem:maxdet` states only the program and the uniqueness. Paper V's conclusion gave the Gaussian work law only "as a bound on every code". | The harness is hash-bound and left as it ran. Its stale docstring is noted in the custody file and in the run account's version 5 list. The conclusion now separates the case without side information, where codes approach the bound. |

**Confirmed right by the verifier:**
- **`lem:maxdet`:**
  - the whitening bijection;
  - the Hadamard step;
  - the form of KKT points;
  - infeasibility of λ = 0;
  - existence and uniqueness of θ;
  - attainment;
  - the edge cases p̃_k = 0, D ≥ tr(PC) and singular P;
  - uniqueness for any C ≻ 0.
- **`thm:multiobs-loss`:** both halves of the iff, and Σ₁⋆ ≻ 0.
- **Consequence (ii) and example (iii).**
- **The code:** `water_level` and `sigma_star` implement the stated θ and closed form, and the
  cited JSON values and the harness hash match.
- **Theorem 24.2** at the source, with its hypotheses checked for Paper V's source.
- **Paper V's reasoning:** the rate-to-content step and the "least rate and work" conclusion,
  under Paper V's definitions.
- **Corollary 4's two edits.**
- **All 14 VI-46 dispositions** are present.
- **Rule compliance:**
  - PAPER-III.b's class and reason are right;
  - PAPER-III.a rests on nothing outside the row;
  - no tracked text still calls B7 `[proved]`;
  - every quotation of the author is verbatim.

**Not checked:**
- the GitHub run;
- the text of the question the author answered;
- re-runs of the nets and of the fire test;
- `pe_lint`;
- Effros and Kostina–Verdú at the source.

## Also in this round

The author allowed the download of chapter 25 of the same notes (2026-11-21). The assistant read
it: it proves the scalar Gaussian case (§25.1.2) but states no vector or reverse water-filling
result. So it does not supply a checked source for `lem:maxdet`'s rate identity, and PAPER-III.b
stays `[exploratory]`. Its route to `[proved]` is a net, for example quantizer channels that must
never beat the closed form.
