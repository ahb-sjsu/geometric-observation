# VI-48: the rate-identity net, the CI file mode, and the proposed promotion of PAPER-III.b (2026-11-21)

**Target.**
- **The net** `experiments/verify_paper3_rate_identity.py`:
  - version 1 (3073453), attempt 1 crashed;
  - the fix b54ecab; version 1, attempt 2 FAILED r3;
  - version 2 (69c4359) passed.
- **Its outputs** `results/PAPER3-rate-identity-v1.json` and `results/PAPER3-rate-identity.json`,
  and the run account `results/PAPER3-rate-identity-RUNS.md`.
- **The proof** of `lem:maxdet`'s rate identity in `paper/observation-theory.tex`.
- **The CI change** in `ci/reproduce.py`: the new entry, and the file mode for a `None` sentinel.
- **Uncommitted drafts:** the rate identity joining PAPER-III.a, and PAPER-III.b moving to
  `[proved]`, with their custody files, ledger rows, FRONTIER, README and book edits.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. Its checks:
- **re-ran version 2** in a scratch copy: 17.6 s, ALL PASS, every JSON field identical apart from
  the timestamp, git fields and hash;
- **checked the recorded hashes** of both versions against their commits;
- **re-derived** the proof and every quantity the net computes;
- **regenerated the channels** from the seed;
- **ran its own mutants**, replacing `sigma_star` and `rate_formula` together.

**Verdict.**
- **The net's computations are right.** It is built to fail on the water-filling part.
- **The proof of the rate identity is right,** including the case of singular P.
- **The CI file mode is safe.**
- **The rate identity can join PAPER-III.a** once this pass is logged, the files are committed
  and a green CI run is cited.
- **The net's own power gates do not show its power:**
  - all five are passed by the formula's own optimum channel, and two cannot fail at all;
  - the reviewer showed the power with self-consistent mutants instead;
  - the `lem:info` test is weak in relative terms;
  - r3 and r4's deterministic checks are identities of the code.
- **PAPER-III.b should not become `[proved]` as written.** It claimed two clauses that no check
  can fail on and that rest on rows not `[proved]`.
- **Counts:** 0 errors, 4 overclaims, 4 gaps and several exposition items.

## Findings and dispositions (2026-11-21)

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | OVERCLAIM | PAPER-III.b claimed that, with Kostina–Verdú's Theorem 12, V_Y is the dispersion of the consumer coding problem. That rests on `prop:dispersion`, the finite-n reduction, which Appendix B keeps `[exploratory]` because 025's checks cannot fail. It breaks FRONTIER's bottom-up rule. | PAPER-III.b is scoped to the per-mode terms of the tilted information and its variance V_Y. Both dispersion readings move to "Not claimed", with what each rests on: the tilted letter's needs kernel uniqueness; the consumer problem's also needs `prop:dispersion`. |
| 2 | OVERCLAIM | Kernel uniqueness was claimed at `[proved]` with no check that can fail on it. The r1 and r3 bars pass a gap of exactly zero, and the positive near-optimal gaps are forced by the boundary geometry (115 of 120 instances have inactive modes). | Scoped out of PAPER-III.b. It is listed as proved (VI-37, VI-38, re-derived here) but not netted. |
| 3 | GAP | The r5 gates are passed by the formula's own optimum. (a) and (e) cannot fail. Formula-independent informative channels catch (c) on 5 instances and (d) on 2. The 6 product catches of (a) are all trivial. The custody file's "67 of 160" counts catches by the optimum. | The run account and the custody files now say so. The power evidence is attributed to this pass's own mutants: every self-consistent VI-4 or rotated-basis mutant failed r2 and r3, down to a median excess of 1.4e-7 nats. Version 3 (owed) builds that power into its gates. |
| 4 | OVERCLAIM | "A formula too high by more than 6e-8 is caught" was circular: the near-optimal channels perturb the formula's own Λ⋆. | Reworded as a one-sided first-order descent test in PSD directions, backed by this pass's mutants, not by the net's gates. |
| 5 | GAP | r3's optimum check and r4's feasibility, trace and Monte Carlo checks are identities of the code, yet they were cited as headline custody values. | Labelled as identities in the run account and the custody files. The custody files now cite the formula-independent families: skew gap 0.0435, random-Gaussian gap 1.4e-7, `lem:info` skew slack 0.0164. |
| 6 | OVERCLAIM | The `lem:info` resolution was stated in absolute nats only. The smallest slack/I is 0.101 (product) and 0.207 (skew), so a `lem:info` strengthened by a factor of about 1.11 or 1.26 would pass. | Stated in relative terms too, in the run account and the custody file. |
| 7 | GAP (procedure) | No VI row covered the net or the new clause, yet custody drafts existed. PAPER-III.a's R-IND-5 did not name VI-32's reading of `lem:cm`, `lem:info` and `lem:maxdet`. No green CI run of the new net was cited. The JSON, run account and PAPER-III.b custody file were untracked. | The work is split in two. **Commit 1** adds the net to CI (the reproduce entry, the JSON, the run account and this record). **Commit 2** does the promotion, after a green CI run and a confirming pass, with this VI row in the ledger. The VI-32 reading is added to PAPER-III.a's R-IND-5. The custody files stayed uncommitted drafts until then. |
| 8 | GAP | The r3 clause was removed with no replacement. The stated reason is correct: the reviewer confirmed the first-order prediction ½·scale·Σ_k (1 − p̃_k/θ)₊ (VᵀΣx^{1/2}EΣx^{1/2}V)_kk to within 0.998–1.003 at eps = 1e-4 on both seeds. | Recorded in the run account. Version 3 makes the prediction its clause. |
| 9 | exposition | (a) Version 2's change of r3's docstring wording is not in its History. (b) A custody bar for the skew count was mislabelled. (c) A stray capital in the ledger. (d) The run's `IntegrationWarning`s are unrecorded. (e) "No source sufficed" overstates: only Polyanskiy–Wu ch. 25 was checked (Cover and Thomas, Thm 10.3.3, is a likely source and was not checked). (f) File mode, like sentinel mode, cannot reproduce a committed FAIL. | (a), (d) and (f) are recorded in the run account; (b), (c) and (e) are fixed in the drafts. |

**Confirmed right by the verifier:**
- **The hashes:** version 2's `05f0cc04…` equals the LF-normalized blob at 69c4359; version 1's
  matches b54ecab.
- **Each run** started 6 s after its commit.
- **The mathematics:**
  - the scalar truncated moments and the tail-stable difference;
  - the product channel, where I = H(cell) and the cell-to-output map is injective;
  - the skew quadrature;
  - the Gaussian channels;
  - the closed form and the water level;
  - both mutants.
- **Every number in the run account,** and the r5(b) split.
- **Version 1's figures,** and the history's disclosures.
- **The proof,** re-derived line by line:
  - `lem:cm` and `lem:info`, including the I = ∞ edge;
  - the converse;
  - achievability;
  - the KKT step with p̃_k = 0;
  - uniqueness;
  - `cor:dispersion`'s uniqueness chain.

  The converse and achievability text is unchanged since ab63c7c.
- **CI:**
  - a missing file fails;
  - a stale file cannot pass;
  - the `finally` always restores the committed file;
  - the net is in shard 2/3, and scipy is in the CI requirements.
- **Custody values:** every value matches its source.

**Not checked:**
- Kostina–Verdú, Effros and Cover and Thomas at the source;
- `verify_paper3_nets.py` itself;
- `pe_lint`, the LaTeX builds and a Linux CI run;
- the smoke-test values quoted in commit messages.
