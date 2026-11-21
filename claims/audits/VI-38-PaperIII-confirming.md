# VI-38: confirming pass on the Paper III round (2026-11-21)

**Target.** Commits 5375b7b and 9f69677 against ff8916d:
- the VI-37 dispositions, including the dated correction to its row 1;
- the source checks against Kostina–Verdú (arXiv:1102.3944) and Kostina–Tuncel
  (arXiv:1707.09567v2);
- net version 3 and its result;
- the classes in Appendices B and F.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It was given the two
arXiv PDFs saved during the source check and read them itself. It rendered Kostina–Verdú's
page 7 to an image to read restriction (iv). Without cvxpy, it re-ran every non-solver part
of the net from its file and seed.

**Verdict.** 3 errors, 2 gaps, 6 overclaims, 7 exposition items.

**The main finding is against the assistant.** VI-37's verifier recalled Kostina–Verdú's
moment restriction (iv) as a higher power than 3. The assistant overruled it, writing that
restriction (iv) "was read on the page" as a third moment. **The page reads
E[d⁹(X, Y⋆)] < ∞.** The assistant re-read it after this report, in the text extraction and
on the rendered page: the verifier was right, and the assistant had misread the page. Paper
III's conclusion is unaffected, since the Gaussian letter has all moments. But the
misquote shipped in three places and closed FRONTIER G12 on a false reading.

## Findings and dispositions (all applied, 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | ERROR | Restriction (iv) is E[d⁹] < ∞, not E[d³] (Paper III `cor:dispersion`; VI-37 row 10; LEDGER row VI-37). | `cor:dispersion` now says d⁹ and gives (iii) with 0 < ε < 1 in full. VI-37 row 10 and the LEDGER row carry dated corrections saying the verifier was right. Appendices A and B, and FRONTIER G12, name this correction. |
| 2 | ERROR | The refinability criterion that VI-32 refuted ("Loewner nesting of read metrics") survives in Appendix A, in Chapter 7's rewritten chain paragraph, and in the preface, the front matter, OBSERVATION.md and BOOK_PLAN.md. VI-37 row 2's sweep looked for `[proved]` tags, not for the phrase. | All six rewritten to "nested optimal error covariances". The phrase sweep was repeated: none remain. |
| 3 | ERROR (older text) | Chapter 7's commission tax still confused ranks with Loewner constants (VI-32 #3) and was tagged `[proved]`. | Restated as in Appendix B, B6 (m P̂ ⪯ P ⪯ M P̂, at most (r/2) log(M/m), the r/2 sharp), tagged `[predicted]`-grade, with a dated note. |
| 4 | OVERCLAIM | Appendix B's B4 Statement was unconditional ("is", "iff", "exact"), and B5's heading said "Complete rate region". | B4: contained in the region, equal to it under Assumption SR; nesting necessary, and sufficient under SR; the rate loss at least the bound, and exact under SR. The heading is now "Rate region". |
| 5 | OVERCLAIM | Paper III's related work still claimed "the complete rate region". | "the rate region's converse, with equality under Assumption SR"; the corner condition is necessary, and sufficient under SR; the rate loss is a bound; the k-observer extension is the converse. |
| 6 | OVERCLAIM (minor) | Paper III's "three consequences" (i) and (ii) stated refinability without SR. | (i) nesting, hence refinability under SR; (ii) refinable under SR, with the scalar P = I case being Equitz–Cover's theorem. |
| 7 | OVERCLAIM | Chapter 7 still tagged B1 and B6 `[proved]`. Appendices B and F say no COST-face theorem is. | Retagged: B1 `[exploratory]`; B6 `[predicted]`-grade, its floor measurement `[demonstrated]`. Each carries a dated note. |
| 8 | OVERCLAIM (minor) | B5's status gave `[predicted]`-grade to "the corner"; only the max-det corner identity has it. | "the max-det corner identity"; refinability as a coding statement is `[exploratory]`, as in B4. |
| 9 | OVERCLAIM | The README described Paper III's region unconditionally and linked the stale v0.1 draft `paper/two-observer-theorem.tex`. The IEEE copy `paper/ieee/observation-theory-ieee.tex` still calls Kostina–Tuncel the coding theorem. | README rescoped; the draft is named as superseded and is no longer linked as the source. **The IEEE copy is the author's and is not edited**: reported to the author. |
| 10 | GAP | Version 3 doubled m4's tolerance (5e-6 + 0.005 L to 1e-5 + 0.01 L), undisclosed. On pairs with L ≈ 1, a corner error up to about 0.01 nats passes. m4 tests nothing on the nested pairs, nor on the named pair VI32_not_refinable_though_P1<=P2. | Disclosed in the net's docstring history. No reason for the doubling was recorded, and none survives in the session record. A version 4 with an absolute tolerance, on a fresh seed, is owed before the net joins CI (FRONTIER G11). Nothing's class rests on m4, which is a consistency check. |
| 11 | GAP (custody) | The source checks were the assistant's own reading, which produced #1 and overruled a fresh-context finding (C-AI-1, C-AI-2). | Paper III, Appendix B and FRONTIER G12 now say who checked: the assistant, then independently VI-38. With the correction applied, the Kostina–Verdú check has an independent reading. Kostina–Tuncel too: VI-38 confirmed the row-1 correction against the source. |
| 12 | exposition | `thm:multiobs`: "under Assumption SR the converse holds" means the reverse implication. | "the reverse implication holds". |
| 13 | exposition | The corollary titled "Exact rate loss" states a bound. The introduction equated refinability with nesting. | Retitled "Rate loss"; the introduction and section opening rescoped. |
| 14 | exposition | B5's heading "Achievability for k ≥ 3" also covers k = 2. "L-resolution coding theorem" is a second-hand description. Kostina–Tuncel cite Effros only for the two-stage region, so SR for k ≥ 3 rests on Effros's title. | Heading "Achievability, for every k". Paper III and Appendix B now say what Kostina–Tuncel cite Effros for, and that the k ≥ 3 reading rests on its title ("multiresolution"). Rimoldi is given as Kostina–Tuncel quote it, for two stages. |
| 15 | exposition | The abstract shipped "not yet checked at the source" (T-CUST-3). | The abstract states a successive-refinement achievability assumption. The body's SR paragraph gives its status. |
| 16 | exposition | Example (iii)'s minimal total rate needs no SR: two independent single-stage codes attain it. | Said so in the text. |
| 17 | exposition | The net's docstring described m1's trace check as two-sided; the code checks only the overshoot. | Docstring corrected (a slack trace would show in the logdet comparison). |
| 18 | exposition | Condition (c) also requires a finite-valued distortion. Remark 9 says Theorem 12 survives non-uniqueness. Restriction (iii) includes 0 < ε < 1. The incident columns of Appendices B and F differed. Appendix B's status header was dated 2026-11-20. | `cor:dispersion` names all three conditions. Without uniqueness, V is an ε-dependent extremum (Remark 9), so the uniqueness argument is what gives a single V. The incident columns are aligned, and the header is dated 2026-11-21. |

**Confirmed right, as the verifier checked it:**
- **VI-37's other dispositions:** present and correct.
- **The row-1 correction:** correct against arXiv:1707.09567v2.
- **Kostina–Verdú, apart from (iv):** Theorem 12 (abstract alphabets, footnote 9), Definition 6, Property 2, eq. (94), (a)–(c), and (i)–(iii) with d_max = Σγ_k.
- **The dispersion formula:** re-derived by hand, and matched to the net's terms to 7e-15 over 200 configurations.
- **The kernel-uniqueness argument and the separation boundary:** right.
- **The converses:** none uses achievability.
- **The net's non-solver parts:** reproduce from file and seed. These include the disclosed version 2 history: 8 of 20 draws below the floor, r31's ratio, and the stream re-synchronizing at r46.
- **LaTeX:** compiles with no undefined references.

**Not checked by the verifier:** the solver parts of the net; Effros (unavailable); IEEE
numbering; that version 3's criteria predate its run.

## Owed

- A confirming pass on this round's changes (the assistant's dispositions above).
- Net version 4 (m4 with an absolute tolerance, fresh seed), then CI wiring and custody.
- Effros 1999 at the source (FRONTIER G12b), held for the author's permission.
