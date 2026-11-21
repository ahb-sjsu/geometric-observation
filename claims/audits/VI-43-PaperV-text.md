# VI-43: Paper V's text fixes for VI-41 (2026-11-21)

**Target.** The uncommitted change to `paper/consumer-relative-landauer.tex` against
1629c82. It answers VI-41's findings #8 (Corollary 3 had no written proof), #9 (the Gaussian
results used Theorem 1, which is proved only for finite alphabets and bounded distortion),
#12 (Proposition 4's hypotheses) and #13 (Theorem 1's converse lacked its limit step). The
change:
- restated Corollary 3 for exact block recovery and gave it a finite-blocklength proof;
- added the limit step from the codes' distortions D_n to D in Theorem 1's converse;
- scoped Corollary 4 and Propositions 3 and 4 to a single-letter region U(D), with a
  one-sided relation to the operational region, and added a general-alphabet
  single-letterization to Appendix A;
- stated Proposition 4's hypotheses, and proved the existence and uniqueness of its level μ;
- adjusted the abstract, the introduction and the Limits section.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. Its checks:
- re-derived every new step;
- re-derived Proposition 3's moment algebra, and Proposition 4's KKT condition, clipping
  and worked example (ΔL = 0.1106 and ΔR = 0.1306 bits, as stated);
- compiled the changed tex in a scratch directory: 14 pages, clean;
- swept the repository's other prose about Paper V.

**Verdict.** **No false mathematical step.** The pass found 0 errors, 3 gaps, 2 overclaims
and 10 exposition items in the paper, and 6 items in other files.

The main finding is #1. Corollary 3's statement left out a hypothesis that its proof uses:
consumer j decodes from M_j alone. Without it, the independent-reset clause is false.

## Findings in the paper, and dispositions (applied 2026-11-21)

| # | Severity | Finding | Applied |
|---|---|---|---|
| 1 | GAP (the clause is false without it) | Cor 3's independent-reset minimum Σ_j H(U_j\|S) needs consumer j to decode from M_j alone, and that restriction was only in the proof. Counterexample: U_1 = U_2 = U, M_1 = U^n, M_2 empty, both consumers reading M_1. "Full cross-memory coordination" was also defined only in the proof. | The statement now names the separate memories and the restriction, and defines coordination (each reset may condition on S^n and on the memories not yet reset). A sentence after the proof gives the counterexample. |
| 2 | exposition | Cor 3 was missing "per source symbol" and did not name its code. "Exact at every blocklength" could be read as a claim about work. | "Per source symbol"; the code M_j = U_j^n is named. The proof is now "exact for the Landauer content", and the work reading rests on the asymptotic tightness of the Landauer bound. The corollary keeps its name and number, which other files cite. |
| 3 | GAP (minor) | The scope paragraph needs a closed-graph property, and closedness of U(D). Prop 4's proof gave only right-continuity at a fixed pair. Cor 4's region was not covered. | The scope paragraph states the property: U(D) is closed, and (R+1/k, L+1/k) ∈ U(D+1/k) for all k implies (R, L) ∈ U(D). Prop 4's proof proves both (a box with R+1, at D+1/k and at fixed D), and covers Prop 3 and Cor 4 (quadrants with continuous corners). |
| 4 | GAP (citation) | "Achievability is the classical Gaussian rate–distortion coding theorem" had no citation, and the bib's only coding theorem (Shannon 1959) is for discrete sources. | **Not cited.** The assistant could not check a source for the continuous-alphabet theorem. The text now says that without side information the equality reduces to the achievability half of the rate–distortion theorem for the Gaussian source P_C^{1/2}X under squared error, "a classical result that is likewise not reproved here". **Cor 4's operational equality is therefore not claimed as proved in this paper.** A checked citation is the author's to add. |
| 5 | OVERCLAIM (minor) | "the scalar Gaussian problem has no rate–work tradeoff" | "the scalar single-letter region". |
| 6 | OVERCLAIM | The abstract's "complete achievable region" was unscoped, and its vector clause and the introduction's were operational. | The abstract's region is "for finite alphabets", the Gaussian clauses say "single-letter" and "a lower bound on every code", and the introduction's vector clause is single-letter. |
| 7 | exposition | "test channels on R^r": r is defined later, and Cor 4's source is not r-dimensional. | "test channels from the source space to any reproduction alphabet". |
| 8 | exposition | "The converse holds for general alphabets": only the per-code converse does. | "The per-code converse". The paragraph says the finite-alphabet limit step used compactness, and is replaced here. |
| 9 | exposition | "The results of this section are about U(D)" did not fit Cor 4 or Prop 5. | Names Cor 4 and Props 3–4. Prop 5 is "an optimization inside a stated memory model". |
| 10 | exposition | RW(D) was undefined; the defined symbol is RW_C(D). | RW_C(D), defined as before; its definition does not depend on the alphabet. |
| 11 | exposition | The Limits item said the extension "would make its closed forms the operational region", including Cor 4's. | Restricted to Props 3–4, the closed forms with reset side information. |
| 12 | exposition | "so is every point of the closure" | "every point of the closure of the achievable set lies in it too". |
| 13 | exposition (older text) | Prop 3's proof presumed a conditional density of X given (X̂, S). | Added: without one on a set of positive probability, the conditional law is not absolutely continuous with respect to the Gaussian law of X given S, so I(X; X̂ \| S) = ∞. |
| 14 | exposition | (a) The component Markov chain needs both X̂ − X − S and S_i ⊥ X_{≠i} \| X_i. (b) "Dominated by the allocation program" should be by a feasible allocation's point. (c) "exactly when c_i > 0" was redundant. | (a) The factorization p(x̂_i, s_i \| x_i) = p(s_i \| x_i) p(x̂_i \| x_i) is given. (b) Reworded: every pair lies above some allocation's point, and the program traces the lower boundary. (c) "since c_i > 0". |

## Other files (applied 2026-11-21)

| # | Finding | Applied |
|---|---|---|
| R1 | README.md, Paper V's entry: "the full achievable region" and "the Gaussian region with reset side information" were unscoped. "Two R-IND-5 passes (0 errors)" left out VI-41 and VI-43. | "for finite alphabets"; "the single-letter Gaussian region …, a lower bound on every code; achievability for continuous alphabets not proved". The verification line names VI-41 and VI-43, and says no check in the nets can fail on Thms 1 and 3 or Cor 1. |
| R2 | `paper/go11-conditional-region.tex` (two places) and its NOVELTY note said Paper V's region theorem holds for "general alphabets". The tex also called the mode-aligned case "solved". | "Finite alphabets", with the Gaussian results single-letter and the converse proved; the mode-aligned case is "solved in Paper V at the single-letter level". |
| R3 | LEDGER VI-9 row: the scalar-corner and vector-tradeoff headline was operational. | A dated note. The original text stays. |
| R4 | README GO-9 row: "the operational face of TC(U₁; …; U_m \| S)". GO-9's records are lossy, so GO-9 measures the total correlation of the stored records. Cor 3's chain rule gives that for any separate memories; Cor 3 itself prices exact outputs. | Reworded in the README. The LEDGER GO-9 row does not use the phrase. |
| R5 | FRONTIER G14, the LEDGER VI-41 row and the VI-41 record still listed Cor 3's proof, Prop 4's hypotheses and the continuous-alphabet extension as owed. VI-41's "Props 2–4 describe the operational region" is now false for Props 3–4. Achievability with side information on continuous alphabets is a new open item. | G14 updated. The VI-41 row and record each carry a dated note. The open item is added to FRONTIER's list of other papers' open items. |
| R6 | REGISTRY-ACCOUNTING, prereg 044's title. | A dated note. The sealed prereg is not touched. |

Confirmed consistent by the verifier: OBSERVATION.md:15, chapters/ch07_cost.md:209,
notebooks/README.md:5, README.md:107, tit-cr-context-r2.tex:363–366 and
complementarity-tax.tex:689–690.

**Checked and found right by the verifier:**
- **Corollary 3's proof**, given #1's hypothesis. Each step holds: the joint bound, the
  sequential reset and the chain rule, and the independent bound. M_j = U_j^n meets all three
  with equality at every n, and TC ≥ 0 follows by subadditivity.
- **Theorem 1's limit step**, and U_C(D)'s closedness.
- **Appendix A's general-alphabet single-letterization.** Every term is finite and the
  chain rule holds on standard Borel spaces. It needs neither identical distributions nor
  the Markov chain, so it transfers across Prop 4's components.
- **"Every code has (R_n, L_n) ∈ U(D_n)"** on general alphabets.
- **Proposition 4:** its KKT condition and the existence and uniqueness of μ.
- **The compile.**

**Not checked:**
- Props 1, 2, 5 and 6 and Thms 2–3, beyond spot checks;
- the nets and the fire test;
- the bibliography against its sources;
- a source for the continuous-alphabet Gaussian coding theorem (#4);
- the imported thermodynamics: whether a sequential conditional reset costs
  Σ_j H(M_j \| …) in the physical ideal model.

## Owed

- **A confirming pass** on these dispositions. #1 and #3 change a statement and a proof,
  although the pass found no error.
- **To the author:** a checked citation for the continuous-alphabet Gaussian rate–distortion
  coding theorem, if Cor 4's operational equality is to be claimed. Also the earlier Paper V
  decisions: the row split, and the class of (d).
- **Open:** achievability of the Gaussian region with reset side information, on continuous
  alphabets with unbounded squared error.
