# VI-44: confirming pass on the VI-43 dispositions (2026-11-21)

**Target.** Commit 431bad7 against 57bccec: Paper V's text fixes and the dispositions of
VI-43's findings (`claims/audits/VI-43-PaperV-text.md`), in
`paper/consumer-relative-landauer.tex` and the record files the commit touched.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It re-derived every new
step and compiled the tex in a scratch directory: 14 pages, clean, with the same byte size as
the committed PDF.

**Verdict.** All 14 paper dispositions and all 6 record dispositions are present and
correct. **No false mathematical step, 0 errors.** It also found 1 gap (the missing citation,
already owed to the author), 3 minor overclaims and 11 exposition items. With no error, the
confirming rule asks for no further pass: **the text round on Paper V has converged.**

## Findings and dispositions (applied 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | exposition | "Without the restriction … the independent-reset minimum is smaller" is too general. Without the restriction the minimum is H(U_1,…,U_m\|S), so it is smaller only when TC > 0. | "can be strictly smaller": one memory can then hold every output and the others be empty, so the minimum falls to H(U_1,…,U_m\|S); for example U_1 = U_2 with H(U_1\|S) > 0. |
| 2 | OVERCLAIM (minor) | Cor 1 defines W⋆_C operationally, and Cor 4 states its closed form. The scope paragraph re-read R_C and L_C as single-letter minima, but not W⋆_C. | The scope paragraph now reads W⋆_C = k_B T ln2 · L_C the same way: the single-letter work, a lower bound on every code's ideal reset work. |
| 3 | exposition (older text) | "rate and Landauer content coincide" fails code by code (L_n ≤ R_n). | "the minima of rate and Landauer content coincide". |
| 4 | exposition | The conclusion's Gaussian residue was stated operationally. | "at the single-letter level and as a bound on every code". |
| 5 | GAP (citation, already owed) | Cor 4's operational equality reduces to an uncited classical theorem; the record already says so. Separately, Cor 4's own single-letter proof leaned on uncited vector reverse water-filling. | The citation stays owed to the author. **Cor 4's single-letter proof is now self-contained.** It uses the change of variables Z = Vᵀ P_C^{1/2} X, Prop 4 at ρ_i = 0 with unit weights for the bound, and the pull-back X̂ = (P_C^{1/2})⁺ V Ẑ for attainment. (This new proof has not had a fresh-context reading.) |
| 6 | exposition | "a finite set of channels" | "the set of channels between finite alphabets". |
| 7 | exposition | The phrase gave the distortion to the alphabet. U_C(D) and U(D) were not related. | "on which d_C is defined, with distortion at most D", and U(D) is U_C(D) for this source. |
| 8 | exposition | RW_C(D) ⊆ U(D) was left implicit. | Stated. |
| 9 | exposition | "a lower bound on every code" is wrong for a region. | "which contains every code's rate–work pair", in the abstract, the introduction and the README. |
| 10 | OVERCLAIM (minor) | README: VI-41's two errors and the owed nets were not mentioned. The results no check can fail on were incomplete. | Now: "no false step in the mathematics; VI-41 found two errors in the nets' accounting; text gaps fixed …; nets and custody still owed". No check can fail on Thms 1–3 or Cors 1 and 3, and Cor 4 is netted on its converse side only. |
| 11 | OVERCLAIM (minor) | GO-11's tex: "solved, in general" contradicted "finite alphabets". The scalar corner and water-filling lacked "single-letter". | "solved."; "and, single-letter, the scalar corner and mode-aligned reset water-filling". |
| 12 | exposition (record) | The dated notes on the VI-41 row and record did not mention Thm 1's limit step, and "since this record" could be read as causal. | Both mention the limit step; the record now says "no longer true". |
| 13 | exposition (record) | VI-43 was recorded with "10 exposition", but its table has 9 exposition rows. | The VI-43 record and LEDGER row say 9 rows, noting that the verifier counted 10. The 431bad7 commit message keeps "10". |
| 14 | exposition (record) | FRONTIER G14 kept VI-41's "Cor 3 has no written proof" ahead of VI-43's fix, and said "3 gaps, all applied" although #4 was rescoped, not cited. | The earlier clause is marked "(at VI-41)". The cell says #4 was rescoped and its citation is owed. |
| 15 | exposition (commit message) | 431bad7's message said the GO-11 tex compiles with "0 overfull boxes". It has 5, none of them new. | Recorded here. Commit messages are not amended. |

**Confirmed right by the verifier:**
- **Cor 3:** its restated statement is exactly what its proof proves.
- **Thm 1:** its limit step, and the closedness of U_C(D).
- **The Gaussian scope paragraph:** it claims what is proved. The reduction of Cor 4's
  equality is correct.
- **The end of Prop 4's proof:** both inclusions of the allocation characterization of U(D),
  the box argument, and closedness.
- **Prop 3:** the no-density clause. The moment algebra was re-derived.
- **Prop 4's component factorization.**
- **The worked example:** recomputed as ΔL = 0.1105 and ΔR = 0.1306.
- **The record files:** cell counts.

**Not checked:**
- Thm 1's achievability beyond reading;
- the unchanged results;
- the nets;
- the bibliography;
- a source for the continuous-alphabet theorem;
- the imported thermodynamics.

## Owed

- **To the author:** a checked citation for the continuous-alphabet Gaussian rate–distortion
  coding theorem, if Cor 4's operational equality is to be claimed. Also the earlier Paper V
  decisions: the row split, and the class of (d).
- **A fresh-context reading of Cor 4's new single-letter proof (#5).** That is a short check;
  it can ride with the next Paper V pass.
- **Paper V's nets and custody (VI-41).**
