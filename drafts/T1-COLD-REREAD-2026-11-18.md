# Cold reread of the T1 worked-result registration draft (2026-11-18)

**What this is.** This is the cold reread that the programme's ledger procedure requires before
`drafts/T1-WORKED-RESULT-REGISTRATION-DRAFT.md` may be sealed. That draft registers a
governed run of the T1 "learn then serve" chain: probe a consumer by queries, estimate its
read operator Q, design a rate-leakage-distortion (RLD) code for the estimate, and check
the design against the bounds of the T1 note.

**Who and how.** Claude (Opus 5.5) did the reread on 2026-11-18, the day after the draft was
written, at the request of the session that wrote it. I worked in a fresh context: I had the
files listed below and the task brief, but not the drafting session's conversation or
reasoning.

**What I did not do.**
- I edited, staged and committed nothing that is tracked.
- I did not run `scripts/seal.py` and ran no instrument with `--governed`.
- I contacted no remote machine.

**Bottom line.** The draft is **not ready to seal**. Its numbers are right and every bar can
pass. Four problems remain:
1. **The bars cannot fail.** Every gating bar follows from a proved result with a structural
   margin, so a correct instrument cannot miss any of them. The prose says otherwise, and one
   outcome it describes cannot occur.
2. **Prior computation is undisclosed.** The note's own committed checks already simulated
   H1's statistic and computed H2's reference loss on the registered instance. The draft says
   no pilot and no data exist.
3. **H4's pass count is unsupported.** Its rule (18 of 20 seeds) is not supported by the
   bound its power note cites.
4. **The integrity machinery is incomplete:**
   - the instrument hashes are not recorded;
   - the guard accepts an instrument edited and committed after the seal;
   - there is no admissibility block;
   - there is no `retrospective` field.

Section 2 has 27 findings: 8 blocking, 8 rewrite, 7 wording, 4 owner. All can be fixed in the
text plus a small change to the instrument.

---

## 1. What was read and what was run

**Commit.** `163b178` (master, 2026-11-18 00:34 −08:00). The draft and instruments last
changed at `6dd5ada`, `32f26d3` and `a4395c8`, all on 2026-11-17. The note last changed at
`163b178`.

**Read in full:**
- `drafts/T1-WORKED-RESULT-REGISTRATION-DRAFT.md` (393 lines), including both "For the cold
  reread" sections;
- `experiments/t1_worked_result.py` (v1.0);
- `experiments/t1_arm_r_llama.py` (v1.0), both stages; the analysis code was read, the capture
  was not run;
- `paper/t1-learn-then-serve/t1-learn-then-serve.tex`, version 4.1;
- `paper/t1-learn-then-serve/AUDIT-VI-23.md` and `AUDIT-VI-24.md`;
- `paper/t1-learn-then-serve/verify_t1_v4.py`, checks C1 to C7, and the committed outputs
  `verify_t1_v3.json` and `verify_t1_v4.json`;
- `drafts/t1-design/design.py` and `drafts/t1-design/h4robust.py`;
- `prereg/TEMPLATE.md`, `prereg/GO-P-2026-091-go16-discrete-twin.md`, `scripts/seal.py`;
- the `| T1 |`, `VI-22` and `RLD-III.3` rows of `claims/LEDGER.md`;
- PE-CLS-1.0, sections 3 to 5, 7.5, 9.1 and 10;
- the owner's standing ledger procedure, item 1b (cold reread);
- for arm R's provenance: `experiments/gateB_llama_asymptotic_floor.py` (GO-027), the GO-027
  prereg, and `results/t1-arm-r-smoke-2026-11-17.json`.

**Run.** Everything ran locally, on CPU.
- `python experiments/t1_worked_result.py --smoke`: ALL PASS in 2.2 s. This is the smoke
  instance (p = 3), not the registered one.
- Scratch scripts and their outputs are in the session scratchpad. That folder is not
  durable, so every number this record relies on is quoted below. The folder is a
  `reread\` folder in the session's temporary scratchpad, outside the repository (its local
  path is omitted here), and its contents are:
  - `bars.py` and `bars.out.txt`: constants, H1 spread, the H2 and H3 ranges over the
    Lemma-1 event, solver noise, the H4 worst case and failure radius, Proposition 2,
    Theorem 5's remainder;
  - `h3pm.py`: the same quantities under ε±;
  - `cor8.py`: whether Corollary 8 applies, arm B's certificate constants, binomial tails;
  - `guardrepo/`: a throwaway git repository for the guard test, run on a copy of the guard
    function, not the instrument.

**Disclosure of what this reread computed on the registered instance.**
- Closed forms: ν±, ε_m, ε±, the exact roots t±, τ, the H4 closed form, Theorem 5's ρ_b, and
  Corollary 8's ρ̄.
- The instrument's coding functions (`Coder.design`, `Coder.wf_rate`) evaluated at Q itself
  and at adversarially chosen Q̂ on the boundary of the Lemma-1 event. This used no random
  draw.
- The solver's noise at Q(I + E), with ‖E‖ = 1e-11, for arm L (`default_rng(12345)`).
- Arm B's Q from the instrument's own constructor, which uses the instrument's fixed seed.
  This reproduces the eigenvalues already disclosed, 1.97e-4 and 0.0689.
- The variance of the read metric, in closed form.

**What this reread did not do on the registered instance.**
- No probe set was drawn from π.
- No consumer loss was simulated.
- No governed seed array was used.
- No bar was changed in response to a measurement.

---

## 2. Findings

Class key:
- **blocking**: the registration must not be sealed as is;
- **rewrite**: a bar, gate or claim should change;
- **wording**: the text is wrong or unclear but no bar changes;
- **owner**: a choice only the owner can make.

Line numbers refer to the draft at `163b178`. Where a proposed text is long, the table points
to an appendix.

| # | Where in the draft | Class | Finding and evidence | Proposed change |
|---|---|---|---|---|
| B1 | Version-3 note, line 18–19; version-4 note, line 63–64; YAML `pilot:` (232–233); `governs:` comment (171–174) | blocking | **Prior computation on the registered instance is not disclosed, and two sentences deny it.**<br><br>**C2** (in `verify_t1_v3.py` and `verify_t1_v4.py`, `default_rng([20261117, 2])`, 4000 repetitions per cell) drew probe sets from π on exactly this instance and computed H1's statistic. The instance is Σ = diag(2, 0.5), G = diag(4, 1), β ∈ {0.05, 0.2}, m ∈ {8, 32, 128, 512}. Coverage of the ε± event was 1.0 in all eight arm-S cells (`verify_t1_v4.json`).<br><br>**C5** computed, by quadrature, the consumer loss of the true-Q design at the registered D, for both arms S and every α. It found loss / tr(QΔ) = 0.99986 at β = 0.05 and 0.99813 at β = 0.2. That is the instrument's `full_design_loss` reference, and it is close to the quantity H2 bounds.<br><br>**C6** drew one probe set at m = 128 and one at m = 512 per arm S on this instance (`[20261117, 6]`).<br><br>**C4 and C8** use this instance's Σ, G and holder.<br><br>**Audit VI-23**'s `audit_remarks.py` and `audit_v2_0301.py` also use the registered Σ, G and H.<br><br>**What the draft says instead:**<br>– "NO pilot was run … no simulated data" (232–233);<br>– "Nothing below has been run on the registered instance" (version-3 note). That sentence was committed in `d05ea85`, the same commit that added C2;<br>– "nothing has been run on the registered instance" (version-4 note).<br><br>None of these computations used a governed seed array, so no governed number has been seen. But H1's sampling distribution and H2's reference value have been. | Replace `pilot:` with the itemized disclosure in Appendix B. Delete the two denials. Add this reread's own computations, listed in section 1. |
| B2 | YAML: the field is missing | blocking | **No `retrospective:` field.** The template requires one. Given B1, this is a known instance: H1's sampling distribution and H2's reference value were seen before the claim is fixed, and sealing is what fixes it. Under PE-CLS §4.3 the claim is therefore retrospective. It cannot be classed `predicted`. The governed draws, which no one has seen, can serve as the registered replication, so the result can hold at most `demonstrated`. | Add `retrospective: true` with its reason (Appendix B). The owner's alternative is in O3(a). |
| B3 | YAML `H4_benefit` (209–213) and `power: H4` (227–231) | blocking | **H4's pass rule (18 of 20 seeds) is not supported by the bound its power note relies on.**<br><br>The power note shows that every Q̂ inside the Lemma-1 event clears the floor. That part is correct: on the ball of relative error 0.3 my grid gives a worst reduction of 16.14%, 15.16% and 12.75% for L, S(0.05) and S(0.2), against the draft's random-search 16.2, 15.2 and 12.8.<br><br>But Lemma 1 guarantees the event only with probability ≥ 0.9 per seed. Under that guarantee alone:<br>– P(fewer than 18 of 20 seeds pass) = **0.323 per cell**, against 0.0024 for H1's 14-of-20 rule;<br>– across the six H4 cells that involve sampling, the family-wise false-fail rate can reach **0.90**.<br><br>In fact H4 will pass almost surely, but for a different reason. A seed misses only at a relative estimation error of about 0.42 or more (0.46 for L, 0.45 for S(0.05)). The closed-form standard deviation of the error is at most 0.038 for every m ≥ 32, so such an error is over 10 standard deviations out. That is a normal-approximation argument, not the bound the note cites, and C2 has already observed the coverage.<br><br>This is the defect class the first cold reread in this programme found: a gate set inconsistent with the count its own bound requires. | Choose one of two options:<br><br>**(a), recommended.** Set H4 at 14 of 20. Lemma 1 together with the deterministic robustness calculation supports this exactly. State that H4 then holds on every seed inside the H1 event. This keeps every bar a consequence of a theorem.<br><br>**(b)** Keep 18 of 20, and replace the power note by the closed-form spread argument, labelled as a normal approximation and as informed by C2. |
| B4 | "What a miss would mean", H4 bullet (383–384) | blocking | **The draft describes a miss that cannot occur.** It reads: "H4 misses with H1–H3 holding: at this instance the consumer's anisotropy buys less than half its closed-form value; a boundary of the flip, not of T1."<br><br>Three reasons this cannot be what a miss means:<br>– the anisotropy's value at this instance is a closed form (20.0%, 19.1%, 16.8%), which the run does not measure;<br>– H4's statistic is a deterministic function of Q̂, and it stays above the floor for every Q̂ within relative error about 0.42 of Q;<br>– so a miss means only that at least 3 seeds (at least 7 under option (a) of B3) had estimation errors of 0.42 or more, far outside Lemma 1's event (ε ≤ 0.29 in every H4 cell), or that the instrument is wrong.<br><br>This is the first reread's other defect class: a branch that is unreachable by construction, described as if it were a finding about the world. | Replace the bullet with the text in Appendix A. |
| B5 | "What a miss would mean", H1 and H2/H3 bullets (377–382); "The instrument", item 8 (372–373) | blocking | **Physics gates and instrument gates are not separated in advance.** PE-CLS §3.2 requires this ("MUST"). The draft's "Either is a finding against Lemma 1 or against the harness, and the instrument is checked first" invites exactly the after-the-fact re-description that §3.2 forbids.<br><br>Separately, an H1 miss on arm L cannot be a failure of the matrix Bernstein bound: ν = 0 there and the consumer is linear. It can only be a finite-difference or code error. | Declare the gates before the run (Appendix A):<br>– **Instrument gates** (a miss voids the run): SC1–SC3; arm L in full, meaning exact recovery, H2, H3 and H4 on arm L; the shuffled control; the seal guard.<br>– **Physics gates** (a miss refutes): H1–H4 on S(0.05) and S(0.2).<br>– One governed run. A rerun only after a void under an instrument gate, and only under a dated amendment. |
| B6 | YAML `governs:` (170); the seal guard described in "The instrument" (273–285); arm R's analysis guard (308–313) | blocking | **The instruments' content hashes are not recorded, and the guard does less than the text implies.** PE-CLS §3.3 requires the hashes ("MUST").<br><br>`check_governed` checks that each script is tracked by git and equal to HEAD. It does not check that the script is equal to what was sealed, and it never looks at `paper/tit-stationary/spectral_core.py`, the solver the instrument imports.<br><br>I tested a copy of the guard in a throwaway repository:<br>1. A sealed, committed prereg: **accepted**.<br>2. An uncommitted edit to the instrument: refused.<br>3. The same edit, committed: **accepted**.<br>4. An uncommitted edit to `spectral_core.py`: **accepted**.<br><br>Arm R's analysis compares the capture's script hash with the working copy, which the guard only ties to HEAD, so it has the same gap. | **Record the hashes.** Write the sha256 of each file's text, with line endings normalized (as `text_sha256` in `t1_arm_r_llama.py` already computes it), into the sealed document, for:<br>– `experiments/t1_worked_result.py`;<br>– `experiments/t1_arm_r_llama.py`;<br>– `paper/tit-stationary/spectral_core.py`.<br><br>**Enforce them.** Make both guards compare against those recorded values, and write the solver's hash into the result JSON.<br><br>**Name the keys safely.** No key may end in `hash` followed by `sha256:`. `seal.py` blanks every such match, and `check_governed` reads the first one. |
| B7 | YAML (the fields are missing); "What it would show" | blocking | **No admissibility block, no reasoned exemption, and no stated claim or target class.**<br><br>PE-CLS §7.5 has been in force since 2026-10-17, and no prereg in this repository carries an admissibility block yet, so this would be the first registration sealed under it. Without the block or an exemption, the result cannot license any promotion. | **Add a claim.** Add `claim:` (one sentence) and the target: a new ledger row for the worked result, at most `demonstrated` given B2.<br><br>**Add one of:**<br>– the reasoned exemption (recommended);<br>– the A1–A4 block.<br>Both texts are in Appendix B.<br><br>**Use the witnesses that already exist.** The shuffled control is a guaranteed H4 miss: reductions of −70.0%, −66.2% and −57.1% against floors of 10.0%, 9.5% and 8.4%. |
| B8 | The two "For the cold reread" sections (14–96) | blocking | **The reread must be recorded in the sealed document, and the current sections are not that record.** Item 1b of the owner's standing ledger procedure says to record the reread inside the sealed document. The two sections are notes addressed to the reread. Parts of them are now false (B1) and parts are stale, such as the numbering maps. | Replace both sections with a short record of this reread:<br>– who did it, when, and whether in a fresh context;<br>– each finding and how it was disposed of;<br>– a pointer to this file. |
| R1 | YAML `H1_estimation` (195–198); `jacobians` (187–189); `m_probes` comment (235); the instrument's `eps_m`, `rel_err`, D̂ and τ | rewrite | **H1 tests version 2's constant ε_m, which the note no longer states.** Version 4.1's Lemma 1 has one-sided constants ε±, and Proposition 2 adds a deterministic finite-difference error ε_h. This resolves choice C1. | **H1.** Require −(ε₋ + ε_h) ≤ λmin(M) − 1 and λmax(M) − 1 ≤ ε₊ + ε_h, where M = Q^{−1/2} Q̂ Q^{−1/2}.<br><br>**ε_h** (Proposition 2):<br>– 9.2e-10 at β = 0.05;<br>– 3.4e-9 at β = 0.2;<br>– zero for arm L, whose tolerance stays 1e-6.<br><br>**Budget and price:**<br>– D̂ = D(1 − ε₋ − ε_h)/(1 + ν₊);<br>– τ computed with ε± + ε_h.<br><br>**Instrument.** Return and record both one-sided errors.<br><br>**Comments.** For `jacobians`, cite Proposition 2's ε_h in place of "O(h²) ~ 1e-8". For `m_probes`, write "ε₋ spans 0.147 to 0.013 at β = 0.05".<br><br>The new values are in Appendix C. |
| R2 | YAML `H2_loss`; "What it would show" | rewrite | **On arms S, H2 cannot fail with a correct instrument.**<br><br>On the H1 event, tr(QΔ̂) ≤ D̂/(1 − ε) = D/(1 + ν₊) exactly. My adversarial search attains this bound on the event boundary: 0.9416 D at β = 0.05 and 0.8108 D at β = 0.2.<br><br>At every sample, the consumer loss is at most (1 + ν₊) times the quadratic form, by the mean value theorem; this is the same argument that gives ν₊. So the Monte Carlo loss can exceed D(1.005) + 4 SE only through an excursion of about 5–6 standard errors in the Monte Carlo mean of the quadratic form. And C5 shows the loss is 0.998–0.9999 of tr(QΔ̂).<br><br>Only arm L exercises H2. Its expected loss is exactly D (tr(QΔ̂)/D = 1 − 2e-12). The 0.5% margin is 1.9 SE, so the false-fail rate per test is 1.8e-9. The draft's "about 3e-5" is a valid but conservative bound. | Keep H2, and describe it as above.<br><br>Record, per seed and per α:<br>– tr(QΔ̂);<br>– tr(Q̂Δ̂);<br>– loss / tr(QΔ̂).<br>The last is Theorem 5's quantity, which the instrument does not record now. |
| R3 | YAML `H3_price` (203–208) | rewrite | **H3 is deterministic given Q̂ and has a guaranteed slack on arms S.** At the worst Q̂ on the event boundary, taken over all α, the cost sits below the bound by at least:<br>– 0.153 bits (β = 0.05) and 0.588 bits (β = 0.2) under ε_m;<br>– 0.145 bits and 0.571 bits under ε±.<br><br>So H3 can fail only through a solver error.<br><br>On arm L, H3 checks that the solver is deterministic. cost(Q̂) − cost(Q) is at most 7.7e-12 bits at perturbations of 1e-11, against the 1e-6 tolerance, which is sound.<br><br>The draft's own parenthesis, "(a theorem consequence; any violation is an error in the theorem or the instrument)", is right. The section on misses contradicts it. | Keep H3, and state the slack. |
| R4 | "What it would show" (98–107); the *[decided]* item "Three arms gate the verdict" (126–130) | rewrite | **The prose overstates what the run tests.**<br><br>Every gating bar is a consequence of a proved result with the margins given in R2, R3 and B3. The results are Lemma 1, Theorem 11(b) at the level of test channels, and a closed form. The arms were chosen so that every constant is known in advance. That *[decided]* reason is correct, and it is exactly what makes the test one-directional in practice.<br><br>Also, the centre of version 4.1, **Corollary 8** (the certificate without a lower sandwich), is not exercised. Its hypothesis ρ̄(D) < D fails at D = 0.3 tr(QΣ):<br>– ρ̄/D = 1.06 at β = 0.05, and Corollary 8 needs D below about 0.28 tr(QΣ);<br>– ρ̄/D = 4.38 at β = 0.2, and it needs D below about 0.076 tr(QΣ). | Use the replacement paragraph in Appendix A. |
| R5 | YAML `serving_horizon` (246); version-4 note, item 4 (87–89); the instrument's `probe_overhead_per_symbol` | rewrite | **The probing overhead per symbol is under-counted.** The version-4 note says the instrument implements shared calibration, assumption (A3-i). Under (A3-i) in version 4.1, the decoder's own queries "are counted with the learner's". So the one-time cost is 4pm/K queries per symbol, not 2pm/K. The note's "nothing is communicated or counted" contradicts (A3-i). | Use 4pm/K: 2pm queries at the learner plus 2pm at the decoder. Or report both figures. |
| R6 | Arm B bullet (140–143) | rewrite | **The text says arm B's read metric has a kernel. It does not.** The draft reads "(c) fails (its read metric is not bounded below and has a kernel)".<br><br>The registered W leaves the all-ones vector outside its range (check C7). So the read metric is nonsingular at every point and Q ≻ 0, with eigenvalues 1.97e-4 and 0.0689.<br><br>Arm B fails (A1a) for a different reason: the loss saturates, so no lower constant ν₋ < 1 exists. The read metric is nonsingular everywhere, but it tends to zero at saturated points. | Rewrite the bullet: "(A1a) fails: the loss saturates, so no lower constant below one exists. The read metric is nonsingular at every point (check C7), but it tends to zero at saturated points."<br><br>Add that Corollary 8 would be vacuous here:<br>– M₁ ≤ 1/2 gives ν₊ = M₁²/λmin(Q) − 1 ≈ 1270;<br>– ε₋ < 1 would then need m > 9,400.<br>So arm B stays report-only (choice C4). |
| R7 | "What a miss would mean", last bullet (385–386) | rewrite | **"The sketch makes no prediction for them" is wrong for version 4.1.**<br><br>For arm B: Theorem 5 applies, because the consumer has three bounded derivatives, and it predicts loss ≈ tr(QΔ) within ρ. No M₁–M₃ are computed, so there is no bar.<br><br>For arm R:<br>– the scores are linear in exact arithmetic, so Lemma 1 predicts exact recovery at m = 1;<br>– Remark 17 predicts that floating-point noise biases the plain estimator upward by a term that does not shrink with m, and that the paired estimator removes it. This prediction is qualitative, and the smoke run already showed it (trace bias +0.36% plain, −0.03% paired), so it would not be prospective;<br>– the softmax divergence reads across keys, which the note does not cover (Remark 16). | Use the replacement text in Appendix A. |
| R8 | YAML `design`, `controls` | rewrite | **No result path and no run rule.** PE-CLS §3.4 requires the result to be committed. The sealed example 091 states "single governed run … no silent reruns". | Name the two result files, for example `results/GO-P-2026-NNN-t1-worked-result.json` and `…-arm-r.json`, to be committed with the run. State one governed run per instrument. |
| W1 | `power: H1` (220–223) | wording | **The power note cites a coverage figure no audit measured on this instance.** It says "The audit's Monte Carlo found Lemma 1's coverage near 0.999." VI-22 says "Monte Carlo coverage conservative" without naming an instance. VI-23's figures (0.9993–1.0) are for other laws.<br><br>The relevant numbers are:<br>– C2's coverage of 1.0 at ε± on this instance, which is prior data (B1);<br>– the closed form: the statistic's relative standard deviation per coordinate is 0.001–0.076, so the bar sits at least 4.7 standard deviations out under ε± and at least 6.9 under ε_m.<br><br>The note should also say what H1 can detect: if the true coverage were 0.7, a cell would fail with probability 0.39. | Replace the sentence with these numbers. |
| W2 | Version-3 note, item 2, τ figures (33–35) | wording | **The version-3 τ figures were computed from ν rounded to three digits.** At full precision they are:<br>– S(0.05): 0.734 / 0.511 / 0.422 / 0.382 bits (the draft has 0.733 / … / 0.421 / …);<br>– S(0.2): 2.848 / 1.949 / 1.632 / 1.494 bits (the draft has 2.846 / 1.948 / 1.631 / 1.493). | Use the full-precision values, or say the figures are rounded. |
| W3 | Throughout the body; the instrument's docstring | wording | **Version-2 names survive in the body:** "the sketch", "the sketch's Theorem 2", "(c)", "proof sketch". In the instrument's docstring: "(Lemma 1, Theorem 2)" and "outer bound of Thm 2(a)". | Rename, against version 4.1:<br>– Theorem 2 → Theorem 11;<br>– (c) → (A1a) and (A1b);<br>– "the sketch" → "the note (v4.1)";<br>– finite differences → Proposition 2;<br>– output noise → Remark 17;<br>– the softmax kernel → Remark 15;<br>– the knowledge model → Proposition 12;<br>– "a bi-Lipschitz consumer" → "a bi-Lipschitz G^{1/2}C" (Remark 13).<br><br>Fix the docstring before the hashes are recorded (B6), because the edit changes the file's hash. |
| W4 | Arm R bullets and disclosure (144–153, 316–355) | wording | **Several statements about arm R need correcting:**<br>(a) The disclosure's "Softmax KL against the reconstruction design: about 0.28 / 0.26" gives ratios of each design's divergence to the reconstruction design's, not divergences. The reconstruction design's median divergence is 0.21 at R = 64 and 0.076 at R = 128.<br>(b) The divergence uses a full, non-causal softmax of the 768 row-0 queries over the 256 row-0 keys.<br>(c) ν = 0 holds for the consumer in exact arithmetic only. The bfloat16 black box is a noisy consumer in the sense of Remark 17.<br>(d) Probe sets are nested across m: each seed uses prefixes of one draw of 128 points, unlike the synthetic arms.<br>(e) "the computed rate and leakage are upper bounds there": RLD-III.3 (an `[exploratory]` ledger row) makes the Gaussian region achievable for a memoryless source that is not Gaussian. The reported leakage is the Gaussian formula, not the leakage of the forward channel the instrument actually applies to the keys. | Reword each point as stated. |
| W5 | `controls` (247–249) | wording | **The shuffled control is described as permuting the consumer; the instrument permutes the estimate.** The draft says "shuffled-consumer (Q̂ from a consumer with permuted coordinates)". The instrument computes P Q̂ Pᵀ. The two differ because the source is anisotropic. The control's miss is deterministic: reductions of −70.0%, −66.2% and −57.1%. | Say "Q̂ with its coordinates reversed: a guaranteed H4 miss, serving as the A1 witness for H4's grading code." |
| W6 | Header (3–12) | wording | **The procedure citation and the header are wrong for a sealed document.** "PE-CLS-1.0 (procedure 1b)": PE-CLS has no numbered procedure 1b. Item 1b belongs to this programme's ledger procedure. The header still reads "DRAFT, NOT SEALED". | Cite "the programme's ledger procedure, item 1b (cold reread)". Update the header at sealing. |
| W7 | YAML against the template | wording | **Template fields are absent:** `q_family`, `invariant`, `nuisance`, `predicted_failure_class`, `arm_ordering`, `n`. The recent sealed entries 090 and 091 omit them too. | Mark them "n/a" with a reason, or map them: `arm_ordering` is H4; `n` is 20 seeds per cell. |
| O1 | Every *[decided]* item | owner | **No *[decided]* item has been read by the owner.** Claude filled them all on 2026-11-17 "at the owner's instruction". My assessment is in section 3, under C6: all are sound except the serving horizon (R5), H4's pass rule (B3) and the description of the effect floor (B4). | The owner signs or overrides each item before sealing. |
| O2 | Arm R is "optional" (144; YAML `consumer`) | owner | **An optional arm lets the decision to run it be made after the seal.** | Decide now:<br>– run arm R once after sealing (the draft records the go-ahead as given on 2026-11-17; I did not verify that); or<br>– drop it from `governs:`.<br>If it is kept and never run, record it as not run, with the reason (PE-CLS §5). |
| O3 | The design as a whole | owner | **After the rewrites the registration is honest, but it still cannot fail with a correct instrument.** It is a governed numerical verification. If the owner wants something at risk, there are two options:<br><br>**(a) A fresh synthetic instance** that no check has touched. This restores `retrospective: false` for the synthetic arms. It does not make the bars any more able to fail.<br><br>**(b) A prediction outside the proved results**, for example the sign and size of Remark 6's formal second-order term c₂, on a consumer where the sign is not obvious (for p ≥ 3 it can be positive). It would need a control-variate estimator of loss minus quadratic form on common samples. At n_mc = 2e5 the per-seed relative standard error (2.6e-3) exceeds the effect |c₂|/tr(QΔ̂) (at most 1.4e-3) on this instance, and C5 has already computed the effect here. | The owner's choice. Neither option is needed to seal an honest verification. |
| O4 | The guard and amendments | owner | **The guard would block a pre-run amendment.** It refuses any prereg whose hash no longer verifies. The ledger procedure says a dated amendment supersedes the hash. So an amendment made after sealing but before the run would block the governed run. | Decide one of:<br>– amendments before the run require a new ID; or<br>– the guard accepts an amendment block when the original hash is recorded in it. |

Totals: 8 blocking, 8 rewrite, 7 wording, 4 owner.

---

## 3. Choices left to the reread

**C1. State H1 at ε± or at ε_m? Resolved: ε±, plus Proposition 2's ε_h (R1).**
1. **It tests the note as it stands.** Version 4.1 states Lemma 1 with ε±. ε_m now appears only as "the constant of version 2".
2. **It is stronger at no extra risk.** ε± gives the stronger statement and so the more falsifiable bar, at no cost in false-fail rate. Each tail still has probability at most δ/2. So the failure bound per seed stays at δ = 0.1, and the 14-of-20 rule with its 0.0024 is unchanged.
3. **The instrument must change anyway** (B6, R2, R5). "No change to the instrument" therefore no longer favours ε_m.
4. **H4's robustness requirement still holds with margin.** It needs ε ≤ 0.3, and the largest ε± in any H4 cell is 0.208. The worst reduction on the ε± event is 15.1% or more, against floors of 9.5% and 8.4% (Appendix C).

*Disclosure.* C2 had already computed coverage at ε± on this instance (1.0). The choice follows the note's change of lemma, not that coverage; coverage at ε_m, which is larger, was necessarily also 1.0.

*Not chosen:* the exact roots t± of the proof (0.177 and 0.189 at β = 0.2, m = 32), which the note says "may be used". They are tighter still. But D̂ and τ are stated with ε±, and mixing the two adds complexity without changing reachability: the statistic sits more than 4.5 standard deviations inside either. The owner may prefer t±.

**C2. Candidate H5, Theorem 5's bound |loss − tr(QΔ̂)| ≤ ρ(Δ̂) + 4 SE? Resolved: report only, not a bar.**
- On the H2 designs, ρ_b is 16–17% of tr(QΔ̂) at β = 0.05 and 44–76% at β = 0.2. ρ_f is larger: 3.6 and 7.6 at D, where ρ_b is 0.46 and 2.43 (C5).
- The actual excess is about −1e-4 to −1.4e-3 of tr(QΔ̂): the formal c₂ here, and C5's exact −1.4e-4 and −1.9e-3 at D.
- Such a bar fails only if the Monte Carlo loss is off by a sixth to three quarters of its value.

Instead, record the quantity itself (R2).

**C3. The sharper c₂ test of Remark 6? Resolved: not in this registration.**
- It is formal, not proved.
- It is below the Monte Carlo resolution per seed.
- C5 has already computed it on this instance, so it would not be prospective.

See O3(b) for how it could be added.

**C4. A bar for arm B? Resolved: none, as drafted.**
- Theorem 5 needs M₁–M₃ for softmax(Wx), and no one has computed them.
- Corollary 8 needs ε₋ < 1, which here requires m > 9,400 (ν₊ ≈ 1270).

**C5. Cite Proposition 2 instead of treating the differences as exact? Resolved: yes (R1).**
- ε_h is 9.2e-10 at β = 0.05 and 3.4e-9 at β = 0.2 at h = 1e-4. That confirms the version-4 note's "a few times 1e-9".
- Rounding error for arm L is about 1e-12; the smoke run measured 3e-13.

**C6. The *[decided]* items (for O1).**

| Item | Assessment |
|---|---|
| Synthetic arms L, S(0.05) and S(0.2) gate the verdict; arm R is real and report-only | Sound as a design. It makes the test one-directional (R4), which is inherent in testing a proved result where every constant is known. |
| Holder S = (1, 0.5)T + U, all three α | Sound. |
| Σ = diag(2, 0.5) | Sound. H4's reduction exists because of the anisotropy. At R = 1 the two designs coincide: both give Δ = diag(0.5, 0.5), checked by hand. |
| π = the source law | Sound, and now required by Theorem 5. |
| D = 0.3 tr(QΣ) | Sound for Theorem 11. It rules out Corollary 8 (R4); say so. |
| h = 1e-4, noiseless | Sound (Proposition 2). |
| Bars from closed forms | The numbers are sound. The descriptions are fixed by B3–B5 and R2–R4. |
| Effect floor at half the closed-form reduction (20.0 / 19.1 / 16.8% → 10.0 / 9.5 / 8.4%) | The numbers reproduce exactly. A miss is unreachable for errors below about 0.42 (B4). |
| Power | The H1 and H2 arithmetic is correct and conservative. The H4 argument is wrong (B3). |
| m ∈ {8, 32, 128, 512}; 20 seeds; base seed; cluster = seed; fixed n | Sound. |
| Codes are Gaussian test channels; no practical quantizer | Sound. Theorem 7 now makes them operational in RLD I. |
| Bits matched through the closed-form rate | Sound. |
| Serving horizon K = 1e6 at 2pm/K | Wrong under (A3-i) (R5). |

**C7. The instrument details that "the text above does not state" (items 1–8 of "The instrument"). Resolved: adopt them into the YAML.**
- Adopt as they stand: item 1 (held-out pairs), item 2 (arm B), item 4 (seed scheme), item 6 (H2 and H3 only on seeds inside the event, nulls elsewhere) and item 7 (SC1–SC3 as instrument gates).
- Adopt as revised: item 8 (the verdict), per B5.
- Adopt with corrected wording: item 5 (the shuffled control), per W5; item 3 (arm R), per W4.
- Make the instrument changes of R1, R2, R5 and B6 before the hashes are recorded.

**C8. The draft asks the reread to weigh that arm R will probably repeat the smoke pattern on layers 6 and 24. Weighed; no change beyond W4 and O2.** The smoke run cannot have tuned anything:
- the smoke capture was made by the committed script: the recorded `script_sha256 caaba47b…` equals the committed file's text hash;
- it ran on layer 12, with its own text and seeds;
- no harness has captured layers 6 or 24 on GO-027's corpus: `gateB_llama_keys`, `_rematch` and `_weighted_floor` capture {8, 16}, and `_asymptotic_floor` captures {4, 20};
- the governed corpus is byte-identical to GO-027's;
- arm R has no bars, so there was nothing to tune.

A repeat would make arm R a held-out replication of a report-only observation, reported at `[exploratory]`.

**C9. The `retrospective` flag. Resolved: `true` (B2).** O3(a) is the owner's alternative.

---

## 4. What I checked and found sound

**Parameters.** Every number in the YAML matches the code (`GOVERNED`, and `INSTANCES["governed"]` for arm R):
- p, Σ, G, the β values, H and U, the α values;
- the D fraction and δ;
- the m lists, 20 seeds, the 14 and 18 thresholds;
- n_mc, 0.5%, 4 SE, the 1e-6 tolerances;
- R = 2, h, 10⁴ held-out pairs, 10⁶ draws for arm B's Q;
- the seeds, k = 3, K;
- for arm R: layers {6, 24}, 8 rows of 256 tokens, 5 seeds, m ∈ {1, 8, 32, 128}, the rates, 4 divergence draws, the holder's seed and rows.

**Arm S's closed forms.**
- q(s²) = 1 + 2βe^{−s²/2} + (β²/2)(1 + e^{−2s²}).
- Q = G·diag(q).
- ν± follow from the mean value theorem and are tight, since cos x = ±1 is attained.
- The loss sandwich (A1a) holds with the same constants.

**The design table** reproduces exactly:
- ν±;
- the looseness parts, 0.345 and 1.368 bits;
- τ at all four m;
- the H4 reductions, 20.0%, 19.1% and 16.8%.

ε± and t± match the note's 0.186 / 0.208 and 0.177 / 0.189, and ε_m ≥ ε± in every cell.

**The H4 robustness claim** is confirmed by a grid (worst 16.14%, 15.16%, 12.75%), and the shuffled control misses by construction.

**The power arithmetic** holds:
- P(at least 7 failures of 20 | 0.1) = 0.00239;
- 12 × 0.0024 ≤ 0.03;
- 720 × 3e-5 ≤ 0.03, conservatively.

**Instrument logic** matches the prose:
- H1 uses the spectral norm in the whitened metric; arm L uses 1e-6;
- H2 compares with D(1.005) + 4 SE, using D, not D̂;
- H3 compares with V_Q(α, D/(1 − ν₋)) + τ + 1e-6, and D/(1 − ν₋) stays below D_max (0.628 D_max at β = 0.2);
- H4 uses the closed-form water-filling at 2 bits, with the true Q in the comparison;
- seeds outside the event are recorded as nulls;
- the verdict and the INSTRUMENT ERROR route are composed as described;
- seed arrays are distinct for each purpose and independent across m;
- arm B's W comes from `default_rng(20261117)`, as registered.

**Numerical health:**
- arm L recovers Q with error about 3e-13 (smoke), against a tolerance of 1e-6;
- tr(QΔ)/D for arm L's designs is 1 − 2e-12;
- the solver's noise in H3 is at most 7.7e-12 bits, against 1e-6;
- ε_h is at most 3.4e-9.

**Smoke run.** ALL PASS was reproduced, in 2.2 s.

**Seal guard:**
- it uses the same hash rule as `seal.py`;
- its `status:` and `governs:` patterns read the draft's YAML layout correctly;
- it refuses uncommitted changes.

**Arm R:**
- the Jacobian is reconstructed correctly: Σ_j (J v_j) v_jᵀ = J;
- P = QᵀQ/n with G = (d/n)I, the same P as GO-027's;
- the query count is 2d (plain) and 4d (paired) per point;
- the forward test channel has error covariance Δ for any source with covariance Σ;
- the disclosed smoke figures match the result file, for example a condition number of 1713 and an effective rank of 5.0 for head 0.

**ID and repository safety:**
- GO-P-2026-092 is free here and in `observation-theory-campaigns`, which holds 087–089;
- the rebase guard is installed (`.githooks/pre-rebase`, `core.hooksPath = .githooks`).

---

## 5. What I did not check

- **The note's proofs.** They were audited in VI-22 to VI-24. Nor did I check the RLD series' theorems or Tropp's Theorem 1.4. I re-derived only what bars depend on: the event algebra behind Theorem 11(b) and the mean-value sandwich.
- **The governed path end to end** (four arms, 20 seeds, n_mc = 2e5). The hard limits forbid running it, so only the smoke path ran. The governed runtime is unknown.
- **The solver.** I did not check that `spectral_core.solve` is correct beyond SC1 and my precision probe, in particular at α = 0.
- **Arm R's capture code**, which I read but did not run. Nor did I check:
  - whether bfloat16 rounding errors are independent across the two random bases, which is the paired estimator's premise;
  - Atlas's thermal and GPU rules;
  - the owner's recorded go-ahead.
- **Other harnesses' layers.** Whether harnesses on other corpora captured layers 6 or 24 of this model. This does not affect the held-out claim for arm R's corpus, and I did not search.
- **Remark 6's derivation of c₂.** I used it only for orders of magnitude, and it agrees with C5.
- **The exact distribution of H1's statistic.** I used a normal approximation, which is rough at m = 8. I deliberately ran no Monte Carlo of H1 on fresh seeds, because C2 already exists.
- **PE-CLS conformance of the ledger as a whole.**

---

## 6. Verdict

**Not ready to seal.** It will be ready after the eight blocking findings and the eight rewrites
are applied and the owner has settled O1–O4.

The bars themselves need only R1, plus option (a) or (b) of B3. Their numbers are correct, and
each bar passes with a large, computable margin.

The blocking problems are of three kinds:
1. **Honesty about what the run can show.** The section on misses describes an outcome that
   cannot occur, and it lets an instrument be blamed after the fact (B4, B5).
2. **Disclosure.** Prior computation on the instance is undisclosed, and the `retrospective`
   field is missing (B1, B2).
3. **Integrity machinery:**
   - H4's pass rule is unsupported by the bound it cites (B3);
   - the instrument hashes are missing and the guard has a gap (B6);
   - the admissibility block is missing (B7);
   - the reread record is missing (B8).

After the rewrites, the registration is an honest governed numerical verification of Lemma 1
and Theorem 11(b) on a synthetic instance. It adds measured looseness and two report-only
arms. With a correct instrument it cannot fail, and the text will say so.

---

## Appendix A. Proposed replacement text

**"What it would show"** (replaces lines 98–107):

> A governed, end-to-end run of the T1 chain on a synthetic instance where every constant is
> known in advance. The run probes a consumer by queries: central differences, 2p queries per
> probe point, and 4pm per session once the decoder's own probing under (A3-i) is counted.
> It estimates the consumer's read operator, designs the RLD I frontier point for the
> estimate, and measures the design's consumer loss, rate and leakage. It compares these with
> the bounds of Lemma 1 and Theorem 11(b) of the note (v4.1), at the level of Gaussian test
> channels, which Theorem 7 makes operational in RLD I.
>
> Every gating bar follows from a proved result, with the margins stated in the prediction
> block. With a correct instrument none of them can fail. A pass is therefore a numerical
> verification and a demonstration of the chain, not a test that could have refuted it.
>
> What the run adds beyond the proofs is measurement:
> - how loose τ is at this instance (its looseness part is an upper bound, not a price shown
>   to be paid; Theorem 5);
> - the realized estimation error against Lemma 1's constants;
> - the probing cost;
> - two report-only arms: a softmax read-out that fails (A1a) (arm B), and a real
>   attention-score consumer of Llama-3.2-3B in bfloat16 (arm R).
>
> The run does not test Corollary 8, because its hypothesis ρ̄(D) < D fails at the
> registered D.

**"What a miss would mean"** (replaces lines 375–386):

> These gates are fixed here, before the run.
>
> - **Instrument gates** void the run. A void is recorded as `void: <gate>`, and a rerun
>   needs a dated amendment. The instrument gates are:
>   - SC1–SC3;
>   - arm L in full: exact recovery to 1e-6, and H2, H3 and H4 on arm L;
>   - the shuffled control, which must miss H4 in every cell;
>   - the seal guard.
> - **Physics gates** are H1–H4 on arms S(0.05) and S(0.2). Each follows from a proved result:
>   Lemma 1 with Proposition 2's ε_h; Theorem 11(b) together with the mean value theorem; and
>   the deterministic H4 calculation. Their margins are stated in the prediction block.
>
>   A miss on a physics gate, with every instrument gate passing, contradicts a proved result
>   at this instance. It is logged as a verification incident against the result named below,
>   and it stays in the record whatever a later examination of the code finds.
>   - **H1 misses:** Lemma 1, with ε_h, failed on a consumer that meets its hypotheses.
>   - **H2 or H3 misses, with H1 holding:** for a Gaussian test channel, either Theorem 11(b)
>     failed or arm S's mean-value sandwich did. For H3 this is equivalent to the series'
>     solver violating (P1)–(P3).
>   - **H4 misses, with H1 holding:** at least 7 seeds (3, if the 18-of-20 rule is kept) had
>     a relative estimation error of about 0.42 or more, far outside Lemma 1's event. That is a
>     failure of Lemma 1 on seeds that H1's rule tolerates. It is not a statement about the
>     consumer's anisotropy, whose value at this instance is a closed form.
> - **Arms B and R carry no bars.**
>   - Theorem 5 applies to arm B, but its derivative bounds are not computed.
>   - Arm R's scores are linear only in exact arithmetic. Its bfloat16 noise has no constants
>     (Remark 17), and its softmax divergence reads across keys, which the note does not cover
>     (Remark 16).
>
>   Results for both arms are reported at `[exploratory]`.

## Appendix B. Proposed YAML additions

The blocks below are indented by four spaces only within this record. **Do not paste any line
that begins with `status:` or `governs:` from this file into the prereg.** The guard reads the
first match of each pattern anywhere in the file, so a stray line could satisfy it falsely.

    retrospective: true
        # the instance's H1 statistic (note check C2: 4000 probe sets per cell, coverage 1.0 at
        # eps+-) and H2's reference loss (check C5: loss / tr(Q Delta) = 0.99986 and 0.99813)
        # were computed before sealing; no governed seed array was used. Class at most
        # demonstrated; the governed draws are the registered replication.
    claim: "On the synthetic instance p = 2, Sigma = diag(2, 0.5), G = diag(4, 1), holder
        S = (1, 0.5) T + U, the learn-then-serve chain of the T1 note v4.1, with Jacobians from
        2p consumer queries per probe point, meets Lemma 1's one-sided bounds and Theorem
        11(b)'s loss and cost bounds at the level of Gaussian test channels for the consumers
        x and x + beta sin x (beta = 0.05, 0.2), and the learned design keeps at least half the
        closed-form consumer benefit at 2 bits."
    target: a new ledger row for the worked result, at most [demonstrated]; this run does not
        change the class of the T1 row
    instruments_sha256:      # sha256 of the line-ending-normalized text, filled in at sealing,
                             # checked by both guards (B6). Do not rename these keys to end in "hash".
      experiments/t1_worked_result.py: <64 hex>
      experiments/t1_arm_r_llama.py: <64 hex>
      paper/tit-stationary/spectral_core.py: <64 hex>
    gates:
      instrument: [SC1, SC2, SC3, arm L (H1 exact, H2, H3, H4), shuffled control, seal guard]
      physics: [H1, H2, H3, H4 on arms S(0.05) and S(0.2)]
    runs: one governed run per instrument; results committed as named in design; no reruns
        except after an instrument-gate void, under a dated amendment
    pilot: |
      No governed seed array has been used. Computations on this instance before sealing:
      - design calculation, 2026-11-17 (drafts/t1-design/design.py, h4robust.py): closed forms
        and 20 000 random perturbations of Q; no probe draws.
      - note check C2 (verify_t1_v3.py, verify_t1_v4.py; default_rng([20261117, 2])): 4000 probe
        sets per cell, arms S, all four m; coverage of the eps+- event 1.0 in all eight cells.
      - note check C5: exact consumer loss of the true-Q design at D = 0.3 tr(Q Sigma), arms S,
        all alpha: loss / tr(Q Delta) = 0.99986 (beta 0.05) and 0.99813 (beta 0.2).
      - note check C6: one probe set at m = 128 and 512 per arm S (default_rng([20261117, 6])),
        at D = 0.002 and 0.0005 tr(Q Sigma).
      - note checks C4, C8, and audit VI-23 (audit_remarks.py, audit_v2_0301.py): this Sigma,
        G and holder.
      - audit VI-23 and the cold reread: arm B's Q, eigenvalues (1.97e-4, 0.0689).
      - the cold reread (drafts/T1-COLD-REREAD-2026-11-18.md): closed forms and adversarial
        Q_hat on the Lemma-1 event boundary; no probe draw; no Monte Carlo of the loss.
      - smoke runs: t1_worked_result.py --smoke (a different instance); arm R on layer 12
        (results/t1-arm-r-smoke-2026-11-17.json).
      No bar was set or moved in response to any of these. H1 moved from eps_m to eps+-
      because the note's Lemma 1 changed. H4's count moved because of the cited bound.
    admissibility:
      exempt: "numerical verification of proved results (Lemma 1, Proposition 2 and Theorem
        11(b) of the T1 note v4.1) on a synthetic instance; with a correct instrument no gating
        bar can fail (margins in the prediction block). Witnesses that the grading code can
        return a miss: the shuffled control (a guaranteed H4 miss in every cell) and
        constructed records (Q_hat = 1.5 Q for H1; a loss of 1.1 D for H2)."

If the owner prefers a full block to the exemption:

    admissibility:
      A1: {status: pass, artifact: "witness records scored as misses by the registered grading
           code: the shuffled control (H4 reductions -70.0 / -66.2 / -57.1% against floors
           10.0 / 9.5 / 8.4%); Q_hat = 1.5 Q (H1); loss 1.1 D (H2). Free components fit after
           the seal: none."}
      A2: {status: pass, artifact: "Q_hat is fit on probe draws (purpose 1), independent of the
           H2 Monte Carlo draws (purpose 2) and of the held-out pairs (purpose 4); Q is closed
           form for arms L and S; identification: lambda_min(Q) = 1.000 / 1.080 / 1.339."}
      A3: {status: na, reason: "no manipulation; consequences of proved results tested on a
           fixed synthetic instance"}
      A4: {status: pass, artifact: "estimands as stated; H2 and H3 are graded on the seeds
           inside the H1 event, and the count of seeds outside it is reported per cell;
           multiplicity: family-wise false-fail <= 0.03 for H1 and for H2, as in power."}

A caution on the full block: with a correct instrument, nothing the instrument could actually
produce on this instance withholds the pass. The block's A1 therefore meets the letter of the
check but not its purpose. The exemption is the honest form.

## Appendix C. Values under ε± (R1), with the guaranteed margins

The ε± columns include ε_h, which changes nothing at four decimals. The two right-hand columns
give the worst case over the event boundary, taken over all α.

| Arm | m | ε₊ | ε₋ | D̂/D | τ (bits) | Minimum H3 slack (bits) | Maximum tr(QΔ̂)/D |
|---|---|---|---|---|---|---|---|
| S(0.05) | 8 | 0.1160 | 0.1473 | 0.8028 | 0.734 | 0.262 | 0.9416 |
| S(0.05) | 32 | 0.0532 | 0.0611 | 0.8841 | 0.511 | 0.190 | 0.9416 |
| S(0.05) | 128 | 0.0254 | 0.0274 | 0.9158 | 0.422 | 0.159 | 0.9416 |
| S(0.05) | 512 | 0.0124 | 0.0129 | 0.9294 | 0.382 | 0.145 | 0.9416 |
| S(0.2) | 8 | 0.4069 | 0.4956 | 0.4089 | 2.848 | 0.696 | 0.8108 |
| S(0.2) | 32 | 0.1855 | 0.2077 | 0.6424 | 1.949 | 0.673 | 0.8108 |
| S(0.2) | 128 | 0.0883 | 0.0938 | 0.7347 | 1.632 | 0.608 | 0.8108 |
| S(0.2) | 512 | 0.0430 | 0.0444 | 0.7748 | 1.494 | 0.571 | 0.8108 |

**H4: worst reduction on the ε± event.**

| m | S(0.05) (floor 9.53%) | S(0.2) (floor 8.39%) |
|---|---|---|
| 32 | 18.93% | 15.08% |
| 128 | 19.03% | 16.42% |
| 512 | 19.06% | 16.69% |

**The same margins under ε_m, for comparison.**

| Margin | S(0.05) | S(0.2) |
|---|---|---|
| Minimum H3 slack at m = 8 / 32 / 128 / 512 (bits) | 0.323 / 0.223 / 0.175 / 0.153 | 0.696 / 0.696 / 0.638 / 0.588 |
| Maximum tr(QΔ̂)/D | 0.9416 | 0.8108 |

**Relative estimation error at which H4 can first fail** (grid search), with the shuffled
control's reduction at Q̂ = Q:

| Arm | Failure radius | Shuffled reduction |
|---|---|---|
| L | 0.458 | −70.0% |
| S(0.05) | 0.447 | −66.2% |
| S(0.2) | 0.418 | −57.1% |
