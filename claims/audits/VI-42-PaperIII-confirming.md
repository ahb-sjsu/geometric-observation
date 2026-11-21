# VI-42: confirming pass on the VI-40 dispositions (2026-11-21)

**Target.** Commit ed3ef84 against 1c155b1: the assistant's dispositions of VI-40's findings
(`claims/audits/VI-40-PaperIII-confirming.md`), including one finding the assistant had
declined (#2, the LEDGER's GO-6 row).

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It compiled ed3ef84's
tex in a scratch directory and compared it with the committed PDF. It counted cells in every
table of the touched files, treating `\|` as an escaped pipe. It ran pe_lint L2 on fresh
local clones of 44a5039 and ed3ef84.

**Verdict.** All VI-40 dispositions are present. Chapter 7's new definition of refinability
(the corner rates R₁(D₁), R₂(D₂)) agrees with Paper III's definition, `thm:multiobs` and
Appendix B's B4. Its parenthetical, that two independent codes always serve both observers
at a higher total rate, is true without Assumption SR. "Five catches" is the right count.
**0 errors**, 2 gaps, 1 overclaim, 5 exposition items, and one old rendering defect. With no
error, the confirming rule asks for no further pass on this text round.

## Findings and dispositions (applied 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | OVERCLAIM (minor, introduced) | Chapter 7: nesting means "it can be served by adding bits at no rate loss". That is the sufficiency of nesting, which holds only under Assumption SR. | "(under Assumption SR)". |
| 2 | GAP (consistency) | Chapter 15 no longer counts VI-5's citation as a catch, but Appendix B ("Two errors were caught"), Appendix D's 023 row, Appendix F and CHARTER.md still do. | Appendices B, D and F now count VI-5's construction only, and say that its citation correction proved unchecked or wrong (VI-36 to VI-40). **CHARTER.md is a governing document and is the author's: reported, not edited.** |
| 3 | GAP (class qualifier) | Chapter 17 cited GO-6 as measured evidence, with no qualifier. | "disputed: VI-32, VI-34, re-run owed". |
| 4 | exposition (record) | The VI-40 record called finding #2 "wrong", but half of it was right: the GO-6 class cell was plain. "The author's to set" does not separate that cell from others: the README's class column already carries the qualifier, and the LEDGER marks caveated classes in the class cell with ⚠ (GO-8, GO-9, OT-3, OT-7). pe_lint reads the first class token, so a marker changes nothing it parses. | The GO-6 class cell now reads `[demonstrated]` ⚠. The class is unchanged and remains the author's. The VI-40 record is reworded. |
| 5 | exposition (record) | VI-40 was missing from B4's and B5's incident columns. | Added in Appendices B and F. |
| 6 | exposition (record) | FRONTIER G11 said VI-40's findings were "applied", but one was declined. | G11 now says one finding was declined, then settled by VI-42. |
| 7 | exposition (introduced) | Appendix B wrote "§multiobs", a LaTeX label, as if it were a section name. | `sec:multiobs`, in code font as elsewhere. |
| 8 | exposition (old text) | Chapter 15 now says VI-5's replacement readings proved wrong, but not that VI-7's replacement ("effective dimension r_D") was itself refuted (NEG-18). | Said. |
| 9 | rendering (old text) | Bare pipes broke four tables: Appendix D's header `P(≥k \| null)` (the table would not render); README's GO-9 row ("U_m \| S") and GO-16 row (a fourth cell under a three-cell header); FRONTIER's F16.0 (nine cells under eight). | Pipes escaped; the README's and FRONTIER's extra cells merged into their neighbours. |

**Confirmed right by the verifier:**
- **Appendix D's 022 row and Chapter 17's classes:** agree with Appendix B.
- **The VI-5 note:** agrees with Paper III's Assumption SR paragraph.
- **The VI-40 LEDGER row's counts:** match the record.
- **The compile:** clean, 24 pages, with a largest overfull box of 13.66 pt; the
  committed PDF is identical to the scratch build.
- **pe_lint L2:** CONFORMING before and after, with only the claim count changing.

**Not checked:** Effros, Rimoldi and Kostina–Tuncel at the source; L3, verify_seals,
check_custody and CI.

## Owed

- To the author:
  - CHARTER.md still counts VI-5's citation among R-IND's catches;
  - the IEEE package (VI-38 #9, VI-39 #11);
  - GO-6's class;
  - the Effros PDF (G12b).
- For the net: version 4, then CI wiring and custody (G11).
