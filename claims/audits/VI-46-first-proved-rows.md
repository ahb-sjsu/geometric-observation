# VI-46: the first `[proved]` rows, their custody files, and Corollary 4's new proof (2026-11-21)

**Target.** An uncommitted change against 1e8c5fb that created the ledger's first `[proved]`
rows:
- **custody files** `claims/custody/PAPER-III.a.md`, `PAPER-V.a.md` and `PAPER-V.b.md`;
- **a new LEDGER section** with rows PAPER-III.a, PAPER-V.a and PAPER-V.b (`[proved]`) and
  PAPER-V.c and PAPER-V.d (`[exploratory]`);
- **consequential edits** to FRONTIER, the README, the VI-41 record, and the book's Appendices
  B and F and Chapter 7.

It also covered **Corollary 4's single-letter proof** in `paper/consumer-relative-landauer.tex`
(added in 1e8c5fb), which no fresh context had yet read.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser, connector
or network tools and no access to the assistant's verdict. Its checks:
- **re-derived** Lemma 1, Prop 1's KKT step, Prop 2, Cor 2, Prop 3, Prop 4 (the quadratic, the
  uniqueness of μ, the box argument), Prop 5 and Prop 6 of Paper V;
- **re-ran** `verify_consumer_landauer.py`, which matched the committed control log except one
  Cor 4 identity residual (6.9e-15 → 7.1e-15);
- **recomputed** every measured value against its log or JSON, checked the mutant indices and the
  hashes, and diffed the papers against the commits the custody files name;
- **checked Corollary 4's proof numerically** on 500 random singular cases (worst residual
  2.5e-8, the pseudo-inverse tolerance).

**Verdict.**
- **No false mathematics.** Corollary 4's new proof is correct.
- **PAPER-III.a should not stand as written:**
  - the paper asserted the max-det closed form without deriving it;
  - its kernel-uniqueness clause rests on `lem:maxdet`'s rate identity, which the row excluded;
  - no green CI run including the net was cited.
- **PAPER-V.a and PAPER-V.b** are sound, subject to the gaps below.
- **Counts:** 2 errors (both wording in the new ledger rows), 6 gaps, 2 overclaims and
  several exposition items.

## Findings and dispositions (applied 2026-11-21)

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | GAP | Paper III states the max-det closed form (consequence (ii)) and Σ° ("i.e.") but never derives them. `lem:maxdet` proves only the program and its uniqueness (as VI-36 X2 had noted). The proof of `thm:multiobs-loss` gave only the "if" half of "L = 0 iff nesting". | **Paper III amended.** `lem:maxdet` now states the closed form for any cap C ≻ 0, and its proof derives it (whitening by the cap, Hadamard's inequality, the scalar KKT conditions, and uniqueness for any positive definite cap). The proof of `thm:multiobs-loss` now gives the "only if" half by uniqueness. To be read by the next fresh-context pass. |
| 2 | OVERCLAIM / GAP | Kernel uniqueness, and with it the dispersion formula, rests on `lem:maxdet`'s rate identity, which no net covers. The bounds r_D ≤ 2V ≤ r are arithmetic consequences. | The dispersion formula leaves PAPER-III.a and becomes row **PAPER-III.b, `[exploratory]`**. It is promoted once the rate identity has a net or a source-checked citation. The book's B7 returns to `[exploratory]`. |
| 3 | GAP | No green CI run that includes the net was cited. | **Cited.** GitHub Actions run 44928434935 (1e8c5fb), job 136919564164 (shard 1/3), re-ran `verify_paper3_nets.py` in 13.8 s and reproduced the verdict and the flag. |
| 4 | GAP (the author's words) | PAPER-V.a read the author's acceptance of the split as settling VI-41 #10 (whether VI-41 counts as the re-reading), which was never asked. | **Reworded.** The custody file says #10 was not put to the author separately. The row rests on this pass instead, which re-derived all six results at the current text. |
| 5 | GAP | Prop 4's proof uses Appendix A's chain-rule step. That step belongs to PAPER-V.c, which is `[exploratory]`. | The component inequalities are now part of PAPER-V.b's claim, as Appendix A's step applied within one letter. They are netted only in part by GS[6] (one two-mode source, α ∈ {0, 1}, 5e-3), and the custody file says so. |
| 6 | ERROR (wording) | LEDGER PAPER-V.b: "a work discount that decreases in D to I(X;S)" is wrong. The discount tends to I(X;S) as D → 0. | "decreases in D and tends to I(X;S) as D → 0". |
| 7 | ERROR | LEDGER PAPER-V.d dropped Cor 3's restriction that consumer j decodes U_j^n from M_j alone. Without it the independent-reset clause is false (VI-43 #4). | Restriction restored. |
| 8 | OVERCLAIM / exposition | Prop 1's self-consistency residual is an identity of the iteration. Prop 5's and Prop 4's merged rows mix identities with checks that can fail. GS's single-curve check tests the remark after Prop 3, not (44). The separability value sits 4e-4 below its stated bound and passes only through the grid and its tolerance. | All applied in the custody files: the identity is marked, the rows are split, the remark is cited, and the slack is stated. |
| 9 | exposition | Coverage was described loosely. VI-42 confirmed only ed3ef84 against 1c155b1; Paper III's results last changed in 1c155b1 (confirmed by VI-40), and their derivation-grade readings were VI-32, VI-37 and VI-38. VI-41 checked Cor 2 through its net only; Cor 2's derivation-grade reading is VI-8. | Applied. |
| 10 | GAP | Text nearby still called the k = 2 max-det corner identity `[predicted]`-grade: Appendix B's B5 status and table row, Appendix F's B5 row, and Appendix D's 022 and 023 rows. B4's status listed VI-4 only, and FRONTIER said the B-theorems had no ledger rows. | All updated. |
| 11 | exposition (the author's words) | FRONTIER G11 said the row is `[proved]` "as the author agreed"; the author agreed to a row, and the class comes from T-CUST-1. V.d and the VI-41 note set "proceed as you recommend" beside a recommendation not in the question. The citation question went unanswered in the records. | Reworded. The records now say the recommendation was written after the author's reply. The citation question was answered later the same day: the author allowed the download ("yes, download the Polyanskiy–Wu chapters"). |
| 12 | exposition | PAPER-V.c overstated: Appendix A gives (R_n, L_n) ∈ U(D_n), and the closed-graph property is proved only for the Gaussian regions. | Reworded. |
| 13 | exposition | Say which of Cor 3's clauses the proposed search covers, and why Thm 2 differs. | Applied in PAPER-V.d. The search's power lies in the independent-reset clause; the joint and coordinated clauses reduce to H(g(M) given S) ≤ H(M given S) and the chain rule. Cor 3 quantifies over codes, and Thm 2 does not. |
| 14 | exposition (Cor 4) | The proof should name the auxiliary S′ that Prop 4 needs, and state that X̂ and Ẑ determine each other. | Applied in the paper. |

**Confirmed right by the verifier:**
- **Text unchanged.** Paper V's six row-(a) statements and proofs are unchanged since 44a5039,
  and Paper III since ed3ef84.
- **Re-derivations:** the eight Paper V results listed above.
- **Values and hashes:** every measured value, the mutant indices and probe ladders, the stale
  numbering map, and the sha256 values.
- **The CI wiring** of [1c], [2/3] and [0b].
- **The exclusions** of Assumption SR, Kostina–Verdú's Theorem 12, Landauer's bound and
  Theorem 1's operational reading.
- **No stale "no row is `[proved]`" statement** in a tracked document.

**Not checked:**
- GitHub CI status (the assistant checked it; see #3);
- re-runs of `verify_gaussian_sideinfo.py` and of the fire test;
- the full VI-8 and VI-9 records;
- Kostina–Verdú and Effros at the source;
- the slacks 5.6e-10 and 0.26%;
- compiling either paper.

## Also in this round

The author allowed the download of Polyanskiy and Wu's MIT 6.441 notes, chapters 23 and 24
(2026-11-21). The assistant read Theorem 24.2 and Definition 23.1 at the source. They cover a
memoryless source on general alphabets, with a non-negative separable distortion, D > D₀,
D_max < ∞, and fixed-length codes at average distortion. On that basis Paper V's Corollary 4 now
cites the theorem for its operational equality. The PDFs are kept outside the repository. An
independent reading of the citation is owed in the next pass.
