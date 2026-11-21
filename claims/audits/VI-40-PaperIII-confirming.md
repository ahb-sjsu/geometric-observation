# VI-40: confirming pass on the VI-39 dispositions (2026-11-21)

**Target.** Commit 1c155b1 against 287f349: the assistant's dispositions of VI-39's 18
findings (`claims/audits/VI-39-PaperIII-confirming.md`), plus a last sweep of Paper III,
`chapters/`, README.md and OBSERVATION.md for unconditional multi-observer claims and for
classes above Appendix B's.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It compiled the
committed tex and its parent's in scratch directories, and compared the scratch build with
the committed PDF.

**Verdict.** All 18 VI-39 dispositions are present. B4's new sentence is true, and is
exactly `thm:multiobs`. Its note on the kernel-overhead example is correct, worked by hand.
The pass found 1 error, 2 gaps, 3 overclaims and 5 exposition items, plus a rendering
defect in two ledger rows. The error is old text with the same defect as VI-39 #1.

## Findings and dispositions (applied 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | ERROR (old text) | Chapter 7 defined refinability without the corner rates ("whether a single scalable code can serve the coarse observer with a prefix …"). Appendix B now calls exactly that form false. "Served by adding bits" fits the kernel-overhead example too. | "serve both observers at their single-stage optimal rates R₁(D₁) and R₂(D₂)", with a note that without them two independent codes always serve both; "adding bits at no rate loss". |
| 2 | GAP (class qualifier) | GO-6 appeared as plain `[demonstrated]` in Appendix D, Chapter 14, the README and the LEDGER's GO-6 row. The verifier said the ledger's GO-6 claim row is not marked disputed. | Appendix D, Chapter 14 and the README now say "disputed (VI-32, VI-34; re-run owed)". **Not applied to the LEDGER row, where the finding is wrong.** The GO-6 row already carries "**Disputed (VI-32, VI-34), class left to the author**" in a later cell. Only its class cell is plain, and that cell is the author's to set. The VI-39 record's sentence that the ledger marks it disputed therefore stands. |
| 3 | OVERCLAIM (minor) | Appendix D's 022 row ("confirmed") gave no current disposition. | Now notes: 022's checks pass with VI-4's bug re-inserted (VI-32); the corner identity is `[predicted]`-grade through 023 [3]; the coding statements are `[exploratory]`. |
| 4 | GAP (record) | The LEDGER VI-5 note did not say that "the abstract k ≥ 3 region is Kostina–Tuncel 2019" is wrong. Kostina–Tuncel is two-stage throughout (checked in the PDF). | The note now says so. |
| 5 | OVERCLAIM (minor, old text) | Chapter 15 counted VI-5's "mis-attributed citation" among "six catches", but VI-5's replacement readings are themselves unchecked or wrong. | VI-5 is counted for the non-iterating construction alone. The citation is described as flagged, with replacement readings that proved unchecked or wrong; "Five catches". |
| 6 | OVERCLAIM (minor, old text) | Chapter 17: "the mismatch tax and omission floor are proved". | "derived (`[predicted]`-grade, the floor measured `[demonstrated]`)". |
| 7 | exposition (introduced) | Appendix B cited "Paper III's Example (iii)"; Paper III has no such example. | "§multiobs, consequence (iii)". |
| 8 | exposition (record) | VI-39 was missing from B4's and B5's incident columns, and VI-32 from B3's. | Added in Appendices B and F. |
| 9 | exposition (introduced) | In Paper III's related work, "(to which Assumption SR is attributed)" attached to the wrong noun. | Moved next to Effros. |
| 10 | exposition (record) | FRONTIER G11 and the VI-39 record's header said "all applied", but the IEEE package (#11) was not edited. | Both say the author's IEEE package is the exception. |
| 11 | exposition (old text) | Chapter 7: "equality on the right exactly when every read mode is active". A mode at the water level, γ_k = θ, is inactive by r_D's definition but contributes fully. | "exactly when no read mode lies below it", noting the mode at the level. |
| — | rendering (old text) | LEDGER rows VI-24 ("\|excess\|") and VI-28 ("Σ_{Y\|S}") had bare pipes inside a cell, so they rendered as 8 and 7 cells under a 6-cell header. | Escaped. |

**Confirmed right by the verifier:**
- **Compilation:** no errors, undefined references or multiply defined labels. The largest
  overfull box is 13.66 pt; the parent's 53 pt and 40 pt boxes are gone. The committed PDF's
  text is identical to a scratch build.
- **Edited tables:** every touched row has its header's cell count.
- **Classes:** B1 and B4 to B7 agree across Appendices B, D and F and Chapter 7.
- **Ledger and FRONTIER:** the VI-5 note agrees with FRONTIER G12b.
- **The sweep:** apart from #1 to #6 and #11, every multi-observer achievability, "iff" or
  "equivalent" claim in Paper III, the book, the README and OBSERVATION.md carries
  Assumption SR. OBSERVATION.md's "true-divergence reduction (the tilt is C)" correctly
  summarizes `thm:B2`, so it is not the withdrawn claim.

**Not checked:** Effros, Rimoldi and Equitz–Cover at the source; the net's solver; the
commit's lint, seals and CI.

## Owed

- A confirming pass on these dispositions, since #1 was an error.
