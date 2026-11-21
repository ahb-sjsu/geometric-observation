# VI-39: confirming pass on the VI-38 dispositions (2026-11-21)

**Target.** Commit 287f349 against 9f69677: the assistant's dispositions of VI-38's 18
findings, recorded in `claims/audits/VI-38-PaperIII-confirming.md`, across Paper III,
Appendices A, B, D and F, Chapter 7, the preface, the front matter, OBSERVATION.md,
BOOK_PLAN.md, the README, the net's docstring and the ledger records.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It read the
Kostina–Verdú and Kostina–Tuncel PDFs itself, rendering Kostina–Verdú's pages 7 and 8 and
reading page 2. It compiled a scratch copy of the tex.

**Verdict.** 1 error, 4 gaps, 6 overclaims, 7 exposition items. All 18 VI-38 dispositions
are present. The verifier confirmed the source quotations against the PDFs:
- restriction (iv), E[d⁹(X, Y⋆)] < ∞;
- (iii) with 0 < ε < 1;
- (a)–(c), including "finite-valued";
- Remark 9's ε-dependent max/min;
- Rimoldi as Kostina–Tuncel quote it, for two stages;
- Effros cited for the two-stage region on continuous alphabets.

It re-read the uniqueness argument step by step, and confirmed Example (iii) by hand. Most
findings are older text that the earlier passes missed. Five were introduced by 287f349:
#1, #4, #12, #13 and #14.

## Findings and dispositions (applied 2026-11-21, except #11, whose files are the author's)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | ERROR (wording; introduced by 287f349) | Appendix B's rewritten B4: "If a single scalable code serves the coarse observer with a prefix …, then the optima nest" drops the corner rates, and as written is false. Paper III's Example (iii) is served by two independent codes at a higher total rate. | "serves both observers at their single-stage optimal rates R₁(D₁), R₂(D₂) (the corner) …", with a note on why the corner matters. |
| 2 | OVERCLAIM | Paper III's discussion: "the Gaussian weighted-quadratic region is settled in §multiobs". | "§multiobs proves the converse and gives equality under Assumption SR". |
| 3 | OVERCLAIM | Appendix F's B4 label: "refinability iff Σ₂⋆ ⪯ Σ₁⋆". | "refinability ⇒ Σ₂⋆ ⪯ Σ₁⋆ (⇔ under Assumption SR)". |
| 4 | OVERCLAIM (minor; introduced by 287f349) | The front matter and BOOK_PLAN called nesting "the refinability criterion", which reads as an iff. | "refinability requires nested optimal error covariances (sufficient under an achievability assumption)". |
| 5 | OVERCLAIM (old text) | Chapter 7 and the front matter: "the 'true-divergence reduction' … *is* that tilt". Appendix B withdrew this as matching no statement (VI-32). | Withdrawn in Chapter 7, with a note. The front matter now says only that R_C's water-filling tilts toward P_C. |
| 6 | OVERCLAIM (minor) | Chapter 7: "a **standard** successive-refinement achievability assumption" (it is unchecked); "a rate loss, which the theory **computes**". | "standard" is dropped; "which the theory bounds below (exactly, under the assumption)". |
| 7 | OVERCLAIM (old text) | Appendix D's registry rows for 023 ("Complete rate region … confirmed") and 025 ("confirmed w/ sharpenings"). | Each now keeps the registered title and adds the current disposition (023: corner identity `[predicted]`-grade, region `[exploratory]`; 025: the sharpened constant `[refuted]`, checks cannot fail). |
| 8 | GAP | `cor:kobs` and Appendix B's VI-5 note still called Rimoldi's the "L-stage" theorem, which is unchecked, while the Assumption SR paragraph was cut back to two stages. | Both hedged the same way: Kostina–Tuncel quote Rimoldi for two stages; the L-stage form (VI-5's reading) is not checked at the source. |
| 9 | GAP (record) | LEDGER row VI-5 says "the abstract k ≥ 3 region is Kostina–Tuncel 2019 (Effros gives bounds, not the tight region)", uncorrected. That reading contradicts attributing Assumption SR to Effros. | A dated correction on the VI-5 row. FRONTIER G12b lists VI-5's contrary reading as something to settle at the source. |
| 10 | GAP (class qualifier) | Chapter 7, Appendix F's GO-6 row and BOOK_PLAN gave GO-6 (B2, B3) plain `[demonstrated]`, and Chapter 7 said GO-6 "confirms Thm B3". The ledger and Appendix B mark it disputed. | "disputed (VI-32, VI-34; re-run owed)" in all three; "confirms" became "supports". |
| 11 | GAP (report to the author) | The author's IEEE package has more than the IEEE tex: the cover letter ("the complete two-stage rate region … characterized by a single Loewner condition"), `observation-theory-ieee-docx.tex` ("abstract-source successive-refinement coding theorem", "the complete rate region"), and SUBMISSION.md, which says the repository version's "content is identical". The IEEE tex also has "exactly when" (78), "refinable iff" (922) and "settles completely" (1396). | **Not edited**: these are the author's. All of them are named in the report to the author. |
| 12 | exposition (introduced) | "the single V below" (V is displayed above); "the third this sentence first gave" (the d³ was in the previous sentence). | "above"; "this paragraph". |
| 13 | exposition (introduced) | A 40 pt overfull box in consequence (ii); the whitening formula ran into the margin. | The formula is displayed. The assistant also displayed the rate tuple in the Assumption SR paragraph, which removed a 53 pt overfull box the verifier had not counted. The largest remaining box is 14 pt, from older text. |
| 14 | exposition (introduced) | The net's docstring says the named pair's gaps "vanish to about 1e-11"; the JSON has 1.9e-11 to 2.7e-10. | "below 3e-10 in magnitude". |
| 15 | exposition | Appendix B attributed "line by line" to VI-38; it is VI-37's wording. | Corrected: VI-37 checked it line by line, and VI-38 found it right. |
| 16 | exposition | The custody summary header was dated 2026-11-20. The B1 and B6 incident columns omitted VI-32 and VI-38. | Re-dated; the columns are completed in Appendices B and F. |
| 17 | exposition | FRONTIER G11 named one of VI-38's two gaps. | Both named. |
| 18 | exposition | Paper III's related work called Effros "the source of Assumption SR", stronger than "attributed to". | "to which Assumption SR is attributed". |

**Not checked by the verifier:** Effros 1999, Rimoldi 1994 and Equitz–Cover 1991 (not
available locally; "the scalar P = I case being Equitz–Cover's theorem" stays an unchecked
attribution in a remark that no proof uses); Kostina–Verdú's IEEE numbering; the net's
solver parts; the commit's lint and seal checks.

## Owed

- A confirming pass on these dispositions. A round that finds an error gets another pass,
  and #1 was an error.
- Net version 4, then CI wiring and custody. Effros at the source (G12b).
