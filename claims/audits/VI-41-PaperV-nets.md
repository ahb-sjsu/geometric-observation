# VI-41: Paper V's nets and the fire test (2026-11-21)

**Target.** Paper V's two sealed C3 nets:
- `experiments/verify_consumer_landauer.py` ("CL", prereg 042);
- `experiments/verify_gaussian_sideinfo.py` ("GS", prereg 044).

Also under review:
- the assistant's new fire test, `experiments/fire_paper5_nets.py` (commit 44a5039), and its
  outputs `results/PAPER5-fire.json` (attempt 2), `results/PAPER5-fire-attempt1.json` and
  the two control logs;
- whether the proofs on record (VI-8, VI-9) cover the current text of
  `paper/consumer-relative-landauer.tex`.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. Its checks:
- re-ran CL unmutated on Windows (numpy 2.5.2): identical to the committed log apart from
  one residual in the 15th digit;
- re-ran GS's random sections; identical;
- loaded the fire test's definitions without running it, and re-ran several mutants with
  diagnostics;
- re-derived Lemma 1, Theorem 1 (converse and achievability), Propositions 2 and 3, and
  checked the steps of Propositions 1 and 4 to 6, Corollary 4 and the exact-tax equation.

**Verdict.**
- **No false step in the mathematics.**
- **The fire test is mechanically sound:** every gate fires for the stated reason, no gate is
  trivial, the non-firing probes act as null controls, the attempt history matches the
  JSONs, and the guard is correct.
- **Its account of the nets overclaimed.**
- **Counts:** 2 errors (a docstring statement; a vacuous harness check), 4 gaps,
  5 overclaims and 5 exposition items.

## What the nets can and cannot catch (the verifier's coverage table, condensed)

| Result | Can a check fail if it is false? | Resolution / note |
|---|---|---|
| Lemma 1 (convexity) | yes (CL5, a negated claim) | sign at 1e-10 |
| Theorem 1 (the region) | **no** | CL6a's corner is an identity; every other tested code sits ≥ 0.311 bits above the boundary; achievability, closedness and the limit step have no net |
| Corollary 1 (work endpoint) | **no** | ΔW ≥ 0 cannot fail |
| Proposition 1 (Pareto channel) | yes (CL4, CL4b) | random channels come within 0.26% of J⋆ |
| Corollary 2 (exact consumer) | yes (CL8) | bar 5e-3, measured 1.7e-13 |
| Proposition 2 (binary frontier) | yes (CL1–CL3) | 0.0074 to 0.13 bits by direction; D = 0.15 only; shape errors below 0.015 bits pass |
| Theorem 2 (materialization) | **no** | identities; its "chain rule" check is arithmetic on itself |
| Theorem 3 (several consumers) | **no** | no check |
| Corollary 3 (coordinated reset) | **no** | TC ≥ 0 is subadditivity; **no written proof in the paper** |
| Corollary 4 (Gaussian work law) | converse side only, by random codes | 6% to 20%; the formula check computes one closed form twice (VI-4 pattern) |
| Proposition 3 (scalar corner) | yes (GS1, GS2, GS4, GS9; probes GS3, GS5) | quantizers within 0.019 bits; corner 0.1 bits |
| Proposition 4 (vector frontier) | yes (GS6, GS7; probe GS8) | random net 0 at r = 2 up to 0.14 bits at r = 8; separability 5e-3 to 1e-2 |
| Proposition 5 (thermal) | yes (CL12) | 5.6e-10 relative |
| Proposition 6 (staleness) | yes (CL13, CL14) | 1e-10 |

## Findings and dispositions (2026-11-21)

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | ERROR (docstring) | The fire test said every number other than the harness's "Prop 3/4" matched the paper. The equation numbers are stale: the nets' eq. (20) is the paper's (21), and their (40)–(41) are its (41)–(42), because Lemma 1's eq. (10) was inserted in 7ef2eb8. "Prop 1's convexity premise" is now Lemma 1. | **Applied** in the fire test's docstring. The sealed nets and prereg 042 keep their old numbers; the custody table will carry the map. |
| 2 | ERROR (harness) | CL's "sequential chain rule" check computes HAgMS = HAMgS − HMgS, then checks (HAgMS + HMgS) − HAMgS: arithmetic on itself. CL's header and prereg 042 claim a chain-rule check. | The net is sealed and is not edited. Section [4] is recorded as identities only, here and in the custody table. |
| 3 | OVERCLAIM | CL6a should carry ~, as a check that cannot fail for a mathematical reason. Its 1163 catches are injective maps at D = 0 with L_n = H(X\|S) exactly. Thm 1's converse is not netted. | **Applied** (marked ~, with the measurement). |
| 4 | OVERCLAIM | CL11 should carry ~: CL's "eq.(41) = max-det" computes one reverse water-filling twice, with no solver. Only the random-code net can fail on Cor 4, and it comes no closer than 6.1% above the optimum. | **Applied** (marked ~). Cor 4 needs a non-circular net: an independent solver or dual certificate, and a feasibility check. |
| 5 | OVERCLAIM | CL9 should carry ~: TC ≥ 0 is subadditivity. Cor 3's content is not checked. | **Applied** (marked ~). |
| 6 | OVERCLAIM | "Catches a boundary raised by 1e-2" holds only for a uniform raise in the best direction. The optimizer's β grid lands below D. Slack ranges from 0.0074 to 0.13 bits by α, and a 0.015 raise for t < 0.9 D was not caught. | **Applied** in the docstring; the custody table carries the range and the D = 0.15 scope. |
| 7 | OVERCLAIM | REGISTRY-ACCOUNTING (042) and LEDGER VI-8 say the net passes "at machine precision". Only the identity residuals do; the nets pass with slack from 0.0074 to 0.31 bits, or 6%. | Each carries a dated note; the original text stays. |
| 8 | GAP | No net for Thm 1's achievability, closedness or limit step, nor for Cor 1 or Thm 3. **Cor 3 has no written proof.** GO-7 (`[replicated]`, Tier B, not in CI) is the only operational evidence for binning. | **Owed:** write Cor 3's proof; nets for the converse steps and for binning. Listed in FRONTIER G14. |
| 9 | GAP | Thm 1 is proved for discrete sources with bounded distortion. Props 3–4 and Cor 4 state the operational region for Gaussian sources under MSE, and the extension is never stated. | **Owed:** state the extension (the converse with differential entropies; achievability by discretization), or restate Props 3–4 as single-letter statements. |
| 10 | GAP | VI-8 reviewed an earlier draft, and the text folded in afterwards was never re-read by a fresh context. That text covers: Lemma 1's proof, the mixture-channel converse, closedness, Thm 3's remark, Prop 6's hypothesis, and VI-9's five folds. | This pass re-read the folded text and found no false step. Whether to accept it as that reread is the author's call. |
| 11 | GAP (custody) | The fire test was committed only after both attempts, and its JSONs lack the edit texts and the hashes of the script and the mutants. | Disclosed in its docstring. A future run records all three and is committed before it runs. |
| 12 | exposition | Prop 4 does not state its range of D, \|ρ_i\| < 1, or the mutual independence of the pairs. | **Owed** (paper text). |
| 13 | exposition | Thm 1's converse needs right-continuity of the union in D, which holds by compactness but is not said. | **Owed** (paper text). |
| 14 | exposition | GS7 mutates the input, not the claim. Its 0.05 bar is looser than the paper's stated gaps of about 0.11 and 0.13. | **Applied** in the docstring; the custody table will quote 0.1105 and 0.1306. |
| 15 | exposition | Other checks that cannot fail and have no gate: self-consistency, the complement-to-1 identity, ΔW ≥ 0, the omitted-mode identity, and GS[4]'s degeneracy and α = 1 checks. | To the custody table. |
| 16 | exposition | The mutate() guard is heuristic (any "#"), but adequate. | No change. |

## Recommendation (the verifier's), and where it stands

No result is `[proved]` yet: T-CUST-1 also needs a custody table. A single Paper V row would
be dishonest. The verifier suggests four:
- **(a)** Lemma 1, Prop 1, Cor 2, Prop 2, Prop 5 and Prop 6: `[proved]` once a custody
  table exists.
- **(b)** Props 3–4 as single-letter statements: `[proved]` after a custody table and the
  fix of #12. Cor 4 joins them once it has a net that is not circular.
- **(c)** Thm 1, Thm 3 and Cor 1, the coding theorems: their proofs are verified, but no net
  can fail, so `[exploratory]` by the VI-32 precedent until a converse-step net and a binning
  net exist. GO-7 is their operational evidence.
- **(d)** Thm 2 and Cor 3, accounting identities whose physics is imported: Cor 3 needs a
  written proof. The charter does not say how an identity with no net that can fail reaches
  `[proved]`. That is the author's decision.

Props 2–4 describe the operational region RW(D), so their operational reading takes Thm 1's
grade. (Dated note, 2026-11-21, VI-43: no longer true for Props 3–4. They are now
statements about the single-letter region U(D); their operational reading is a converse only.
Cor 3's proof and Thm 1's limit step are written, Prop 4's hypotheses are stated, and the continuous-alphabet
extension is replaced by that rescoping: `claims/audits/VI-43-PaperV-text.md`.)

No ledger row for Paper V's theorems is created in this commit. The split and (d) go to the
author first.
