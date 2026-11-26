# Corrections of 2026-11-26: Geometric Observation (Volume 14)

This volume had no corrections file before this survey. The repairs below were made by the
assistant in the survey of the series of 2026-11-26, against `claims/LEDGER.md` (the
authority), `claims/REGISTRY-ACCOUNTING.md`, `PROTOCOL.md`, `CHARTER.md`, the registrations
in `prereg/`, the result files in `results/` and the papers in `paper/`. The author has not
read them. Nothing was committed. No figure line, no caption under a figure, no heading a
figure is placed before, no sealed registration and no file under `tools/`, `figures/` or
`.build/` was changed; `claims/LEDGER.md` and the registry were not changed. Lines were
added in several chapters, so line numbers below are those before the edit unless stated.

The untracked files `ledger/claims/*.json` (dated 2026-10-17) were not used as a source:
they predate rows NEG-17, NEG-18, GO-14 and PAPER-III/V, and differ from the ledger on GO-16
and the 077 row (Open, item 12).

## Repaired in the survey of 2026-11-26

### Conventions applied across the book

1. **Paper I's legibility results carried class tags with no ledger row.** The preface,
   Chapters 3, 5, 9, 11 and 17, Appendix A and Appendix F tagged results of Paper I
   (`the-angular-observer`) and Paper I.5 `[proved]` or `[demonstrated]`. No ledger row
   carries them; Appendix F itself said the tags were "the book's, not the ledger's", with
   custody unaudited (FRONTIER G11). Front matter: "a sentence may not wear a tag its ledger
   row has not earned". Each such tag now reads "(proved in Paper I; not yet a ledger row)"
   or "(measured in Paper I; not yet a ledger row)" (Paper I.5 for the Weyl ordering, as
   Chapter 11 sources it). Places: preface (polar decomposition), Ch. 3 L92, Ch. 5 L134,
   Ch. 9 L22, 40, 66, 72, 78, 83, 98, 112, Ch. 11 L45, Ch. 17 L149, Appendix A L69,
   Appendix F's legibility table, `BOOK_PLAN.md` (Ch. 9 entry).
2. **The definition of `[proved]` had three parts; the charter has four.** CHARTER
   T-CUST-1 and PROTOCOL §1 also require a constants/slack and known-gaps table, and the
   ledger keeps the RLD rows `[exploratory]` for want of one. Chapter 15 already gave four.
   The front matter, Chapter 14 and Appendix F now add the fourth.
3. **Gate B hits tagged `[demonstrated]`.** The ledger's class cell for every Gate B hit is
   "`[predicted]` target → hit" (GO-B-AV163, GO-B-PDAR, GO-B-whale, GO-B-legal,
   GO-B-Llama-rematch, GO-B-DOA, GO-B-LOCATA), and Chapter 14 already wrote them so. Chapters
   5, 8, 10, 12 and 13, the preface ("[refuted → demonstrated]" for the Llama rematch) and
   Appendix F's sweep table now read "[predicted, hit]". (Open, item 1.)
4. **"Twelve domains" read as twelve replications.** The sweep (Chapter 13,
   `DOMAIN-GENERALITY-SWEEP.md`) has twelve rows: six sealed flips (A1 031, A3 033, D2, D3,
   L 036/039, W 038), A2 (021, worse-arm discrimination on one consumer, not a flip: the
   ledger's A2 note), D1 partial, D4 an honest negative, and three (A2) verdicts (M, K, Mu).
   - Front matter, status paragraph: "replicated across twelve domains and three distinct
     branches of physics" → "put at risk in twelve domains and three distinct branches of
     physics, and confirmed as a sealed flip in six of them".
   - Front matter, Core Objects: "sealed across 12 domains + 3 physics" → "tested in 12
     domains + 3 physics, a sealed flip in 6".
   - Preface: "Twelve domains. Three distinct branches of physics — electromagnetic,
     acoustic, elastic." → "Twelve domains put at risk, six of them sealed flips. Three
     distinct branches of physics — acoustic and elastic, and, in part, electromagnetic."
     (D1, the radar row, is partial in the ledger.)
   - Ch. 1 L89–90, Appendix E L19–20, Ch. 8 L81–84, Ch. 13 L112–114 and Appendix E L89–90:
     the same correction in each chapter's words; the attention rematch (021) is named as
     worse-arm discrimination, not a flip, and the moral and genre rows as (A2) verdicts.
5. **The κ magnitude law is a loss the book reported as live.** `results/GO-kappa-law.json`
   ("EXPLORATORY / honest negative": flip magnitude is not monotone in κ; κ is "an ordinal
   coupling-null predictor with an EXACT null condition"; GO-P-2026-040 never sealed),
   Paper IV's remark on κ, and Appendix D (040 void).
   - Ch. 12 L67–81: the retrospective fit "across the twelve measured domains" and "one
     sealed prediction … [predicted]" replaced by what was measured: κ computed for two
     anchors (about 0.006 and 0.80), a synthetic sweep that found the magnitude peaked, the
     sharp null when read support equals signal support, 040 void; Ch. 12 L7–8 "a dial" →
     "an ordinal dial (an ordering, not a magnitude)".
   - Front matter, Core Objects row for κ; Ch. 1 L135; Ch. 5 L138 ("makes quantitative" →
     "turns into an ordinal test with an exact null condition"); Ch. 18 L62–64 (the regime
     map is also marked an exploratory diagnostic, not yet a ledger row: Chapter 12, item
     41 below); `BOOK_PLAN.md` Ch. 12 entry.
6. **Theorem numbers of the program's papers read as the book's.** The series checker found
   19 references to a Theorem, Corollary or Proposition the book does not define. Each meant
   a paper's statement and now names the paper in the abbreviated form the ledger uses:
   Appendix A L45 and Appendix B L277 "Kostina–Verdú's Thm 12"; Ch. 24 "Paper I's Thm 16(a)",
   "Thm 20", "Thm 16(b)", Paper II's "Thm 16 / 20 / 22 / 23", "Paper III's Cor. 6"; Ch. 25
   "Paper V's Cor. 2", "Cor. 4", "Prop. 3", "Prop. 4", "Prop. 5", "Prop. 6". Chapters 26, 27,
   28 and 29 now say, where their numbering starts, that theorem numbers are those of the
   GO-11 manuscript, the GO-12 and GO-13 statements, the GO-16 statement and the
   estimation-and-control paper. The one remaining flag is the caption of Figure 25.2 (see
   Figures).

### Front matter, preface, `BOOK_PLAN.md`

7. **Preface, Maya.** The running example presented Maya as a real person. Added "(Maya is a
   composite, and her story is illustrative.)", as Chapter 1 now says of its three
   engineers.
8. **Preface, "The book has seven parts".** The book's table of contents has nine (Parts
   I–IX). Now "nine parts", the last two named (Part VIII in time, Part IX beyond a single
   consumer).
9. **`BOOK_PLAN.md`.** "18 chapters + 6 appendices" → 29 chapters (20–23 stubs) and 7
   appendices; Ch. 16 entry "NEG-1…NEG-14" → NEG-1…NEG-18, the Crucible's losses and 077's
   P2; Ch. 12 entry's "[refuted-as-null]" (not a ledger class) → "an honest negative in the
   ledger", and the failed magnitude law and void 040 recorded; Appendix B entry "B1–B3" →
   B1–B7 with B4–B7 named.

### Part I to Part III (Chapters 1–9, Appendix B)

10. **Ch. 1 L15.** Added "(The three are composites, and their numbers are illustrative.)"
    No source holds the engineers' numbers.
11. **Ch. 1 L153.** "a specific ledger, sealed before it was measured" → "and, where the row
    is a registered test, sealed before it was measured": NEG-2, NEG-4 and theorem rows were
    never registrations.
12. **Ch. 2 L69, L72 (NEG-4).** "provably moves" → "measurably moves"; "over the range that
    matters" → "in this measurement". NEG-4 is one measurement, not a proof.
13. **Ch. 4 L109–110.** "three of the sweep's confirmations" → three rows of the sweep, the
    whale row a sealed flip and the moral and genre rows (A2) verdicts (the ledger's A2
    note; Chapter 13).
14. **Ch. 6 L116–117.** "the VI that the DOA prereg caught": no VI row exists. Now "the
    design pivot that the DOA prereg, GO-P-2026-031, logged after its first attempt returned
    zero error for every arm" (prereg 031).
15. **Ch. 7 L3–6.** "every numbered result resolves to a ledger row" → "to its entry [in
    Appendix B] and, where one exists, to a ledger row": B1 and B6 have no ledger row.
16. **Ch. 7 L45–46 (GO-6).** Added that the harness's isotropic control assigns the three
    curves the same array and cannot fail (VI-32; ledger GO-6), as Chapter 14 says.
17. **Ch. 7 L88 (VI-4).** "the prereg amended and re-sealed" → its prediction rewritten in
    place and re-sealed, a re-seal the charter no longer allows, disclosed since (ledger
    VI-25; Chapter 15).
18. **Ch. 7 L155–156 (omission floor).** The text gave the exploratory follow-up's
    "~10^5×" as the sealed 027 result. Now 027's ratio 800–5700× (median floor 0.10 nats),
    with the exploratory {8,16} figure named as such (`results/GateB-asymptotic-floor.json`,
    `results/mismatch-asymptotic-floor.json`; ledger NEG-13).
19. **Ch. 7, RLD-I and RLD-IV bullets, L180, L198, L208.** The turning direction narrowed as
    the RLD-I row was on 2026-11-20 (VI-27): the direction of the best one-dimensional
    description turns unless it is a common generalized eigenvector; "turn" → "can turn";
    the incommensurate-sampling clause scoped to a cyclostationary process with a
    correlation of finite range (RLD-IV.3, VI-26).
20. **Appendix B L313–317.** "three months later" → "four months later" (preregs 022–028
    dated 2026-07-17/18; VI-32 on 2026-11-20).
21. **Appendix B custody table, B4.** VI-47 added to the incidents, as the PAPER-III.a row
    lists it; Appendix F's B4 row likewise.
22. **Ch. 8 L12–19, L90–91 (arm labels reversed).** The text called the read-preserving arm
    O and the reconstruction-optimal arm R, against its own L73 and L78 and prereg 036. Now R
    = read-preserving, O = reconstruction-optimal throughout.
23. **Ch. 8 L95 (ZCA whale numbers).** "[demonstrated]" → "[exploratory — an `a2_probe`
    characterization, not a sealed test]": `results/whale-ketos-a2.json` has no ledger row,
    and sealed 038 used eigenbasis codes.
24. **Ch. 9.** Tags per item 1.

### Part IV and Part V (Chapters 10–14, Appendices A, C, E, G)

25. **Ch. 10 L49–55 (gradient Gate B).** "the blind projected variance … and the probe finds
    it": in prereg 010 the curvature H was planted, not probed. Now says so, and that
    recovering a curvature operator blind is not yet on the record.
26. **Ch. 10 L106.** "strong heads near 0.96" → "at 0.815 and 0.958" (ledger GO-B-Llama).
27. **Ch. 11, emergent-geometry application.** Added that no result of it is recorded in the
    repository or the ledger; the account is kept.
28. **Ch. 12 L23.** "[refuted → demonstrated]" → "[refuted → predicted, hit]" (item 3).
29. **Ch. 12 L29–31 (D4).** "cannot appear no matter how well you recover P_C" → "at the
    rate tested …", with Paper IV's statement that the null is a low-rate one (prop:kappa).
30. **Ch. 12 L40–42 (moral).** "the flip appears [refuted-as-stated; …]": not a ledger class,
    and moral is an (A2) verdict in Chapter 13. Now "the probe returns an (A2) verdict
    consistent with the flip … [exploratory — no ledger row …]".
31. **Ch. 12 L109–110.** "[demonstrated, for the two-axis diagnostic]" → the two-axis
    diagnostic rests on unsealed `a2_probe` characterizations and is not yet a ledger row;
    the shortcut stays `[refuted]`, NEG-14.
32. **Ch. 13 L7.** "one compressor" → "one compressor across the real-array rows" (the
    ledger: A3, D1, D2, D3 share `compress3`; L, W and A2 use other codes).
33. **Ch. 13 L53.** "the disjoint-recording set is 310 GB" → the full set about 800 GB, the
    indoor recordings 310 GB (ledger GO-B-RaDICaL; Appendix C).
34. **Ch. 13 L62.** "The strongest of the real-data domains" → "of the battery's real-data
    domains" (ledger GO-B-AV163).
35. **Ch. 14 L105–110.** "the LOCATA miss caught a GT-leakage artifact" → "an over-optimistic
    calibration selection". The leakage was in the earlier exploratory 8/8, caught by a
    reviewer; the 032 miss caught the calibration map's 74%
    (`experiments/locata_gateb-NOTES.md`; ledger GO-B-LOCATA).
36. **Ch. 14, after GO-6.** Added that the ledger's core continues: GO-7 to GO-14 and GO-16
    (there is no GO-15), in Chapters 25 to 28.
37. **Appendix A L45, L69.** Items 6 and 1.
38. **Appendix C L5, L40–43.** "re-run by CI" → "for the CPU harnesses, re-run by CI"
    (AGENTS.md §3); the KV-serving rows 056/077 added to the GPU rows.
39. **Appendix E L43.** "(NEG, Chapter 10)" with no number → "(a registered miss, Chapter 10)".
40. **Appendix E L60.** "for the flagship theorem, a proof assistant" → for GO-16's lemmas
    and Paper V's identity layer (ledger GO-16; VI-50, VI-51). No flagship theorem is
    machine-checked.
41. **Appendix E L74–77 (D4).** "D4 was predicted to be a coupling null *and was*": prereg
    034 registered D4 as a flip test, and its A4 records the coupling diagnosis after the
    run. Now says so.
42. **Appendix G L33–34, L88–89.** "a domain the GO-P sweep did not itself enter": the sweep
    has citation retrieval (row L); now scoped to hubness. Two adjacent code spans with no
    word between (checker: doubled word) now read as one phrase.

### Part VI and Part VII (Chapters 15–18, Appendices D and F)

43. **Ch. 16, carriage of every `[refuted]` row (PROTOCOL Rule 1.2).** OT-4 and OT-5
    (`[refuted]`), OT-9 and OT-10 (`[refuted]` as sealed) and prediction P2 of registration
    077 (`[refuted]` as sealed) were in no chapter of the Honest Negatives, and the Crucible
    rows in no chapter at all. Entries added after NEG-18, restating the ledger rows and their
    classes and adding nothing to them, with the void OT-11 and OT-12, the two campaign
    verdicts, and the ledger's note that v1.0 was declared on 2026-08-18. NEG-15 and NEG-16
    were added earlier the same day (commit 8e2bda0).
44. **Ch. 16, closing.** "placed a dozen sealed bets" → "dozens" (the registry runs to 092);
    "exercised, sixteen times" → "exercised once for every entry above" (the chapter now
    carries NEG-1 to NEG-18 and five further rows; a count would go stale again).
45. **Ch. 16 L7 and L86.** "(VI-3)" and "(VI-2)" are the charter's rules VI-3 and VI-2, not
    the ledger's verification incidents of those numbers (Chapter 15 cites the incidents).
    Now "(its rule VI-3)" and "(the charter's rule VI-2)".
46. **Ch. 17 L64–65.** "found errors in remarks and wording only" → no false mathematical
    step; their errors in remarks and wording, gaps and overstatements were all applied
    (ledger VI-22, VI-23, VI-24). "the author has read all its proofs (2026-11-18)" → "by the
    author's own statement of 2026-11-18" (the ledger's RLD section quotes the statement).
47. **Ch. 18 L3–5, the counting sentence.** "Seventeen chapters, seven theorems, twelve
    domains, and sixteen honest negatives" → "The seventeen chapters before this one, their
    theorems, the twelve domains of the sweep, and the honest negatives of Chapter 16".
    Recount: Chapter 18 has seventeen chapters before it and eleven after (29 in all);
    "seven theorems" counted Appendix B's B1–B7 and missed Paper I's legibility results in
    Chapter 9 and everything in Part IX, so the theorems cannot be counted cleanly; the
    sweep has twelve domains (item 4); Chapter 16 carried sixteen negatives when the count
    was written and now carries NEG-1 to NEG-18 and five more rows (item 43).
48. **Ch. 18, "this closing chapter" and "— end of the main text —".** Parts VIII and IX
    follow. Now "this chapter" and "— end of Part VII —"; "Every volume of this series ends
    by reducing" → "reduces". Where the principle belongs is left to the author (Open, 3).
49. **Appendix D.** It claimed to give "every GO-P-2026 ID" a disposition and stopped at 041;
    the sequence runs to 092. Added a block table for 042–092 from
    `claims/REGISTRY-ACCOUNTING.md` (the post-041 misses and their successors, 056, 057, 075
    burned, 077 split, 087–089 migrated, 090–091, 092 reserved), the completeness argument
    for the whole sequence, the extended supersession chains, and a paragraph on the
    content-hash audit VI-25 (13 of 84 hashes did not verify, 6 re-seals, ten of the thirteen
    disclosed nowhere; now in `prereg/SEAL-DISCLOSURES.json`, checked by
    `scripts/verify_seals.py`).
50. **Appendix F.**
    - "Standing negatives" stopped at NEG-14: NEG-15 to NEG-18 added with their classes
      (NEG-15 is `[demonstrated]` as a negative; NEG-16 refuted for the end task with a
      demonstrated co-primary), and the other `[refuted]` rows of item 43.
    - "Verification incidents" stopped at VI-7: a paragraph on VI-8 to VI-57, with the note
      that VI-30 and VI-32 found errors after a seal, so "caught pre-publication" does not
      hold for all.
    - Falsifiable-core table: Chapter 14 (and 12 for GO-5) added to the chapter columns, and
      a pointer to GO-7…GO-16 under "Beyond one consumer".
    - "Every claim above resolves to a row in `claims/LEDGER.md`": now excepts the
      legibility results and B1 and B6, which have no row.
    - The sweep table lists A2 (021) on its own line as worse-arm discrimination, not a flip.
51. **Ch. 14, front matter and Appendix F.** Item 2.

### Part VIII (Chapters 19–23)

52. **The refresh-floor "law" was tagged `[demonstrated]` and is refuted at its source.**
    Ch. 19 L68–70 and L120–123 and Ch. 21 stated φ ≈ 0.177·T_coh (R² ≈ 0.92)
    `[demonstrated]`. Its source, `observation-theory-campaigns/analysis/csi/CSI-refreshfloor.json`,
    says "Exploration, never sealed … REFUTED … do not cite" (the floors were measured at a
    0.15 BLER threshold against a 0.10 claim; the fresh baseline at BLER 0.113 never met the
    budget), as do `CSI-PREDICT-NOTES.md` and `experiments/RADIO-FRESHNESS-TRACK.md`. The
    sealed rerun XPROTO-CSI-SWEEP2 (2026-08-27, PASS) gives the longest compliant report
    period at the 0.10 budget: 4/6/4 TTI at 10 Hz, 2/2/3 at 25 Hz, 1 TTI at 50 Hz and above,
    with no proportionality law. Chapters 19 and 21 now say this; the predictor "wall" is
    tagged `[exploratory]` (its notes call it an exploration); "universality of the constant
    is [predicted]" → no constant survives. Ch. 21 notes that the campaign repository's "OT-14
    law" is not ledger row OT-14 (the Third Crucible's P4 test), and Ch. 23 L17 drops the
    label.
53. **Ch. 20 header.** "Every number resolves to a SEALS.md row (Appendix D/F)" → is to
    resolve there; neither appendix nor the ledger carries these rows yet.
54. **Ch. 21 L23.** "RTT $>$ $T_{coh}$" (two formulas run together; checker) → one formula.
55. **Ch. 22.** "linear recal" → "linear recalibration recovers only ~1.6×"
    (`analysis/sensor/EXPLORATION-SENSOR-DRIFT.md`); the scope correction of the AICSI cell
    (the dissociation did not survive real 3GPP CDL-C; the pre-registered kill fired on
    2026-08-25) added to the demonstrated wing as a kept negative.

### Part IX (Chapters 24–29)

56. **Ch. 24 L9.** "VI-16 to VI-22" → "VI-16 to VI-21": VI-22 audited the T1 note.
57. **Ch. 24, status of the papers.** Added that in this chapter Papers I–IV are the RLD
    series, not the program's Papers I–V of the other chapters (Paper I there is the angular
    observer, Paper III the paper of Chapter 7). "Paper III's Cor. 6" here and "Paper III" in
    Chapter 7 are different papers.
58. **Ch. 24 L225.** "tight as D→0 only when the whole source is reproduced" → "when": the
    paper proves sufficiency only, and the ledger row RLD-III.3 says "when".
59. **Ch. 25 L37–39.** "ledger rows PAPER-V.a and PAPER-V.b record the import" → PAPER-V.a and
    PAPER-V.d, the two rows that record the imported Landauer reading.
60. **Ch. 25, Prop. 4 example.** "equal weights" added; the endpoint gaps 0.1105 and 0.1306
    hold under it (the paper: "equal read weights"; recomputed).
61. **Ch. 25 L211–212.** "after the author accepted the four-row split" → the author's reply
    quoted as the ledger records it ("yes, I accept. Proceed as you recommend") to a question
    that carried no recommendation for row PAPER-V.d.
62. **Ch. 25, Gaussian sources.** PAPER-V.b's fresh-context passes (VI-9, VI-41, VI-43, VI-44,
    VI-46 to VI-49) named; VI-9 was cited nowhere in the book.
63. **Ch. 26 L9.** "every result below carries that class [`[replicated]`]": the replication
    is of the rows' operational faces (058/059, 061/062); the registry grades the theorems
    netted by 060, 063, 064 "citable at `[predicted]` grade". Now says both.
64. **Ch. 26 L259 (GO-11's Theorem 9).** The two hypotheses of `thm:m2sys` (an attained
    optimum with Σ_N ≻ 0; at w = 1, the regime where the two-consumer floor is exact) added.
65. **Ch. 27 L81 (GO-12's Theorem 1).** τ² > 0 added (`thm:qred` assumes it). **L97:** the
    prefix-to-path gap named as a gap in conditional variance, not in L.
66. **Ch. 27, seal disclosures (VI-25, `prereg/SEAL-DISCLOSURES.json`).** Added: 070 re-sealed
    with a dated amendment changing no bar; 067 and 068 re-sealed with amendments recording
    the prior hashes; 069's rerun amendment written into the sealed file and re-sealed; 079's
    harness changed four times after its governed run and moved out of the CI re-run tier;
    081 demoted one sealed sub-gate after its run.
67. **Ch. 27 L140–145 (GO-13).** The `[demonstrated]` grade is the operational face's (069);
    the registry grades the theorems of 067, 068, 072, 073 "citable at `[predicted]` grade".
68. **Ch. 27 L163.** Danskin's theorem "under the paper's attainment and constant-sensitivity
    hypotheses, and away from a switch of the binding consumer" (GO-13 statement, Thm 2).
69. **Ch. 27 L280.** "registration 056 was a miss" → "(ledger row NEG-16, Chapter 16)".
70. **Ch. 27 L314.** "a different and cheaper coordinate" → "a different coordinate, which an
    unregistered probe suggests is much cheaper" (`go15-reference-coupled.tex`: "Nothing here
    is a claim").
71. **Ch. 27 L228.** "$C_\Delta$ is …" after a display formula (checker: doubled word) →
    "Here $C_\Delta$ is …".
72. **Ch. 28 L170.** Added that 090's only hash field, like 091's, is the harness's hash, not
    a content hash of the registration, and that 090's harness was hardened for CI after the
    governed run; the sealed harness reproduces the verdict (VI-25).
73. **Ch. 29 L296.** Beside "VI-14 and VI-15 confirmed … with no error": VI-14 also found a
    DR-1 gate that could not fail and a DR-2 gate whose misreading would have failed the run,
    recorded by a clarifying amendment (ledger VI-14).

### Mechanical (series checker)

74. `python C:\source\erisml-lib\tools\series-build\series_check.py`: 19 hard defects before
    this survey (all dangling Theorem/Corollary/Proposition references), 1 after (the
    caption of Figure 25.2, which this survey may not edit). KaTeX: 0 failures. Doubled
    words repaired at Appendix G L88 and Ch. 27 L228 (above) and Ch. 21 L23; the remaining
    two flags (Ch. 25 L20, Ch. 26, Theorem 3's two display lines) are a display formula
    followed by a sentence that opens with a formula, and one six-equation system split over
    two display lines, and were left. Misspelling "recal" repaired (item 55); "gotcha" (Ch.
    11 L81) is intended. British and American spellings are mixed (Appendix G, Ch. 8, 12, 13,
    16) and were not standardized. The checker's `.build/reports` folder was removed.

## Open, for the author

1. **The class of Gate B hits.** The book now follows the ledger's class cells ("`[predicted]`
   target → hit") for every Gate B hit (Repaired, 3). If these rows are meant to be
   `[demonstrated]` (PROTOCOL §1 also asks for CI and Tier A/B reproduction, which the GPU
   and MATLAB rows lack), the ledger's cells must say so first. Needed: the class.
2. **Gate B misses and partials without a NEG row.** 032 (LOCATA), 035 (legal), 041 (20
   Newsgroups, PARTIAL), D1 (PARTIAL) and D4 (an "honest negative") have no NEG row, yet the
   book tags several "[refuted]" or "[refuted, as a flip]" (Ch. 4 L99, Ch. 8 L120, Ch. 10
   L70 and L122, Ch. 12 L36, Ch. 13 L104 and L106, Ch. 17 L137, Appendix F's D4 line;
   PROTOCOL §4: "A miss is a `[refuted]` row"). Needed: NEG rows for them (and Chapter 16
   then carries them, Rule 1.2), or a ruling that their tag is "missed" or "partial".
3. **The place of Chapter 18.** The principle chapter still sits at the end of Part VII,
   with Parts VIII and IX after it. Its wording no longer claims to end the book (Repaired,
   48). Needed: whether the principle moves to the end or the later parts are framed as
   extensions of it.
4. **Part structure.** The front matter's table of contents and the chapters' own prose use
   Parts I–IX (Ch. 13–14 Part V, Ch. 15–16 Part VI, Ch. 17–18 Part VII). The site build
   (`erisml-lib/tools/series-build/build.py`) groups the chapters as Parts A–G (Ch. 10–13
   "Instruments", Ch. 14–18 "Discipline", Ch. 19–23 "Ageing"). Needed: one structure; the
   build configuration is not in this repository.
5. **The front matter's epistemic-status paragraph is dated 2026-07-20.** It names the core
   as GO-1 … GO-6 and does not mention Parts VIII and IX. Its twelve-domain sentence was
   corrected (Repaired, 4). Needed: whether to re-date and extend it.
6. **What "three physics" means.** Ch. 13's section "The three physics" counts real media
   (electromagnetic D1, partial; acoustic; elastic); its verdict, Ch. 8,
   `DOMAIN-GENERALITY-SWEEP.md` and Appendix E count confirmed flips (synthetic, acoustic,
   seismic). Real media with a clean sealed flip are two. Needed: one definition.
7. **The Crucible and Observation Theory v1.0.** Rows OT-1, OT-2, OT-3, OT-6, OT-7 and OT-8
   (the passes) and the declaration of v1.0 (2026-08-18) appear in no chapter; only the
   losses are now in Chapter 16. OT-13 to OT-18 have no rows in the ledger's tables, only its
   status paragraph. Needed: where the campaigns belong (Chapter 14 is the natural place),
   and rows for OT-13 to OT-18 if the book is to cite them.
8. **Part VIII (Chapters 19–23) has no ledger rows.** Its classes rest on
   `observation-theory-campaigns` (track documents and `SEALS.md`). Needed: rows or a ledger
   pointer, and the classes, in particular: the ZooKeeper 99× gap is one cell (XPROTO-ZK) but
   tagged `[replicated]`; the sensor row is tagged `[refuted]` from an unsealed exploration
   and is not in Chapter 16, though Chapter 19 says it is kept "in the Ch. 16 tradition"; the
   refuted 0.177 fit (withdrawn or refuted, and a NEG row?). Also in Ch. 22: the cellular
   range "0.28–0.47 → 0.05–0.13" does not match the current track (CSI 0.34–0.37 → 0.10, BEAM
   0.31 → 0.02, AICSI 0.28 → 0.13, HO 0.31–0.44 → 0.09–0.12, PHY 0.27–0.42 → 0.055–0.13,
   URLLC ~0.11 → ~1e-5), which cells it covers is the author's choice; "two witness kinds
   (LSN/oplog/zxid)" lists three; "six independent data substrates" cannot be checked; the
   QOT and GRID tracks say unsealed while `SEALS.md` lists them sealed on 2026-08-25.
9. **The legibility results need ledger rows** after the custody audit in
   `the-angular-observer` (FRONTIER G11). Then the class tags removed in Repaired, 1 can be
   restored at their true class. Also unrecorded here: the a2_probe regime map (Ch. 12) and
   the moral precondition.
10. **Chapter 12, "Every honest negative … sorts into exactly one of four kinds".** Design and
    power failures fit none: 032's single-bin MUSIC and uniform baseline, NEG-12's
    unmatched quantizer pair, D1's resolution and data limit. Needed: a fifth kind, or the
    claim scoped to the flip negatives it covers.
11. **Smaller statements in Part I–V.** Appendix E L42 "caught in itself — twice" names only
    035 (the second is probably LOCATA 032); Ch. 8 L112–117 says D4 "cannot appear" without
    the rate qualifier Paper IV gives (Ch. 12 now has it); the commission tax's "sharp" r/2
    in Ch. 7 and B6 has no ledger row and was not checked at the source (Paper III
    `thm:commission`); Ch. 5 L80–84 states the bridge price under a pointwise read-metric
    sandwich, the T1 note proves it under the loss sandwich (A1a): which is meant; Ch. 11's
    emergent-geometry application has no record (Repaired, 27).
12. **Ledger text (not changed; the ledger is the author's record).**
    - GO-11: "one error caught in Prop 1's drafting", while addendum 1 of
      `paper/go11-conditional-region-NOVELTY.md` records 0 errors (Ch. 26's "two catches"
      agrees with the addenda).
    - 077: the vector-u successor is "candidate 078", but 078 is now GO-14's process-limit
      registration.
    - VI-10: the disposition still says the harness is "not yet registered or run", while
      GO-10 records 055 ALL PASS 7/7.
    - RLD-IV.1: "(all checks passed)", while the Paper IV README records one failed
      criterion (1.9e-6 against 1e-6).
    - GO-10, GO-11, GO-13: one class per row, earned by the operational faces, while the
      registry grades the theorems "citable at `[predicted]` grade"; whether to split the
      class cells as GO-16's is.
    - The untracked `ledger/claims/*.json` (2026-10-17) disagree with the ledger (GO-16 one
      class, the 077 file without P2, no GO-14, NEG-17, NEG-18 or PAPER rows), and AGENTS.md
      §3 says such untracked files switch `pe_lint`'s front end. Remove or regenerate.
13. **`BOOK-OUTLINE.md`** (outside this survey) still states "OT-14 law ≈ 0.177·T_coh …
    [demonstrated]" and the old cellular range (lines 70, 80, 88, 103).

## Figures and captions

Made stale by the repairs, or found stale (none was edited):

- **Figure 14.1** draws `[proved]` as "all three of" a proof, a harness and a re-derivation,
  and the caption says "[proved] needs three things together". T-CUST-1 has four: add the
  constants/slack and known-gaps table; "three" → "four" (Repaired, 2).
- **Figure 19.1** draws the refresh floor at 0.177 of the coherence time and its caption tags
  that slope `[demonstrated]`. The fit is refuted at its source (Repaired, 52): the figure
  should draw φ without a measured ratio, and the caption drop 0.177 and the tag.
- **Figure 10.2**: "[demonstrated, GO-P-2026-036, 4/4]" and "[demonstrated, GO-P-2026-039]"
  → "[predicted, hit …]" (Repaired, 3).
- **Figure 13.1**: "D2 and D3 are [demonstrated]" → "[predicted, hit]" (Repaired, 3).
- **Figure 12.1**: "which the chapter reports only as a retrospective [exploratory] fit and
  one sealed [predicted] point" is false: there is no sealed point (040 is void) and no
  retrospective fit across domains, only an exploratory sweep that came out negative
  (Repaired, 5).
- **Figure 25.2**: "(Proposition 6)" → "(Paper V's Prop. 6)" (Repaired, 6); this is the
  series checker's one remaining hard defect.
- **Figure 22.1** changes only if Open, 8 (the cellular range) is settled.

Checked and not stale: Figures 2.1, 5.1, 6.1, 7.1, 8.1, 16.1, 16.2, 17.1, 17.2 (C* =
−0.291379 in `paper/t1-moving-kernel`), 26.1, 27.1, 28.1 (J(0) = 5.3 recomputed), 29.1, B.1.

## Ledger rows no chapter carries

OT-1, OT-2, OT-3, OT-6, OT-7, OT-8 (the Crucible's passes; OT-1 to OT-3, OT-7 and OT-8 are
named only as a range or in passing in Chapter 16) and the v1.0 declaration (Open, 7). Every
other row of `claims/LEDGER.md` (the falsifiable core, the Gate B rows, NEG-1 to NEG-18, the
OT-EC rows, RLD, T1, T1-MK, PAPER-III and PAPER-V) is carried by at least one chapter. Of the verification incidents, only VI-1 (the
founding incident) is not cited by number or within a cited range.
