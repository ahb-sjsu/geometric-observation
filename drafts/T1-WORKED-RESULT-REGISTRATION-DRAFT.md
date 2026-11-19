# DRAFT — T1 worked result: learn a consumer's read operator, pay for the probing, serve it, and bound the downstream loss against the RLD frontier

**Status: DRAFT, NOT SEALED, NO REGISTRATION NUMBER.** Drafted 2026-11-17 by Claude
(Opus 5.5) at the owner's request, from version 2 of the T1 note (`paper/t1-learn-then-serve`,
then titled a proof sketch) and an outside reader's recommendation that the next synthesis
centre on one worked result. Rewritten 2026-11-18 by the same session after the cold reread
recorded below, against version 4.1 of the note. Sealing waits for the owner's read of this
text. At sealing it takes the next free `GO-P-2026-NNN` (092 at the time of writing), moves to
`prereg/`, has its status set to SEALED before `scripts/seal.py` runs, and has its instrument
hashes checked against the files as committed (`--verify-only`, right after the sealing
commit). No governed measurement may run before the sealing commit exists.

## The cold reread (2026-11-18)

**Who and how.** The programme's ledger procedure (item 1b) requires a cold reread before
sealing. The session that drafted this text also wrote the instruments and versions 3 to 4.1 of
the note, so it could not reread it cold. A fresh-context agent (Claude, Opus 5.5) did the reread
at commit `163b178`, with the files and a brief but without the drafting conversation. Its full
record, with evidence for every finding, is `drafts/T1-COLD-REREAD-2026-11-18.md`. It ran only
the smoke instance and closed-form calculations: no probe draw from the registered instance, no
Monte Carlo of its loss, no governed seed.

**Verdict: not ready to seal as written.** The numbers were right and every bar could pass. But:
- **No bar could fail.** With a correct instrument no gating bar could fail, though the text
  described misses as findings, and one described miss could not occur.
- **Prior computation was undisclosed.** The note's own checks had computed H1's statistic and
  H2's reference loss on the registered instance, while the text said nothing had run there.
- **H4's pass count was unsupported** by the bound its power note cited.
- **The integrity checks were incomplete:** no instrument hashes, a guard gap, no
  admissibility block and no `retrospective` field.

It made 27 findings: 8 blocking, 8 rewrite, 7 wording and 4 for the owner.

**The owner's decisions** (2026-11-18, "proceed as you recommend", on the recommendations
put to the owner that day):
- the registration is sealed as an honest governed verification of proved results, at most
  `[demonstrated]`, not redesigned to put something at risk (O3);
- H4 passes at 14 of 20 seeds (B3, option (a));
- an amendment before the run takes a new registration number, so the guard's refusal of an
  amended file stays (O4);
- arm R runs once after the seal, report-only (O2).

The items marked *[decided]* below were filled by Claude on 2026-11-17 at the owner's
instruction. They stand as revised here, and the owner reads this text before sealing (O1).

**How each finding was disposed of:**

| Finding | Disposition |
|---|---|
| B1 prior computation undisclosed | `pilot:` itemizes every computation on this instance; the denials are gone |
| B2 no `retrospective:` | `retrospective: true`, with its reason |
| B3 H4 at 18 of 20 unsupported | 14 of 20; on every seed inside H1's event H4 holds by the closed-form calculation |
| B4 an unreachable miss | "What a miss would mean" rewritten |
| B5 gates not fixed in advance | `gates:` block; the instrument returns VOID, ALL PASS or MISS by it |
| B6 hashes and guard gap | `instruments_sha256:` block. The guard (instrument v1.1) checks every listed file, including the solver, against it. Tested in a throwaway repository, ten cases |
| B7 no admissibility block | `claim:`, `target:` and a reasoned exemption |
| B8 reread not recorded | this section |
| R1 H1 at the old ε_m | H1 at ε± plus Proposition 2's ε_h; D̂ and τ follow; instrument v1.1 |
| R2 H2 cannot fail on arms S | stated in `margins:`; tr(QΔ̂), tr(Q̂Δ̂) and loss/tr(QΔ̂) recorded per seed |
| R3 H3 has guaranteed slack | stated in `margins:` |
| R4 "What it would show" overstated | rewritten; Corollary 8 is not tested at this D |
| R5 overhead 2pm/K | 4pm/K under (A3-i) |
| R6 arm B "has a kernel" | corrected: (A1a) fails because the loss saturates |
| R7 "no prediction" for arms B and R | what version 4.1 says about each is stated |
| R8 no result files, no run rule | `results:` and `runs:` |
| W1 H1 power cited an unmeasured coverage | rewritten with the closed-form spread, prior data named |
| W2 τ rounded from rounded ν | full precision throughout |
| W3 version-2 names | version-4.1 names in the text and in both docstrings |
| W4 arm R statements | corrected (divergence ratios, non-causal softmax, Remark 17, nested probes, leakage formula) |
| W5 shuffled control misdescribed | "the estimate with its coordinates reversed" |
| W6 procedure citation | "the programme's ledger procedure, item 1b" |
| W7 template fields | mapped or marked n/a in `template_fields:` |
| O1–O4 | as decided above |

The notes this draft carried for the reread (versions 3 and 4 of the note) are replaced by
this section and by the text below, which now cites version 4.1 directly.

## What it would show

A governed, end-to-end run of the T1 chain on a synthetic instance where every constant is
known in advance. The run probes a consumer by queries: central differences, 2p queries per
probe point, and 4pm per session once the decoder's own probing under shared calibration
(A3-i) is counted. It estimates the consumer's read operator, designs the RLD I frontier point
for the estimate, and measures the design's consumer loss, rate and leakage. It compares them
with the bounds of Lemma 1, Proposition 2 and Theorem 11(b) of the note (v4.1), at the level of
Gaussian test channels, which Theorem 7 makes operational in RLD I.

Every gating bar follows from a proved result, with the margins stated in `margins:` below.
With a correct instrument none of them can fail. A pass is therefore a numerical verification
and a demonstration of the chain, not a test that could have refuted it.

What the run adds beyond the proofs is measurement:
- how loose τ is at this instance (its looseness part τ_ν is an upper bound, not a price shown
  to be paid; Theorem 5);
- the realized estimation error, against Lemma 1's constants;
- the probing cost;
- two report-only arms: a softmax read-out that fails (A1a) (arm B), and a real
  attention-score consumer of Llama-3.2-3B in bfloat16 (arm R).

The run does not test Corollary 8, the note's certificate without a lower sandwich: its
hypothesis ρ̄(D) < D fails at the registered D (ρ̄/D = 1.06 at β = 0.05 and 4.38 at β = 0.2,
computed by the cold reread).

## The consumer — [decided]

The note's sandwich results cover a consumer that:
- (a) acts on each symbol separately;
- has a read metric of full rank on the symbols' space, or of lower rank with a kernel that does
  not move (then only in the settings of RLD I–III);
- satisfies (A1): (A1a) a loss between 1 − ν₋ and 1 + ν₊ times a quadratic form for all pairs of
  points, and (A1b) the same bounds on the read metric, with constants **known in advance**.

For a Gaussian source, (A1a) forces the weighted map g = G^{1/2}C to be bi-Lipschitz
(Remark 13), so the sandwich results speak only near linearity. Consumers the ledger already
instruments:

| Candidate | Existing instrument | (a) per symbol | full rank | (A1) |
|---|---|---|---|---|
| attention heads of a trained language model, keys as symbols | GO-P-2026-027 harness `experiments/gateB_llama_asymptotic_floor.py` (Llama-3.2-3B, Atlas GPU 1) | the softmax reads across tokens; the scores before it, for a fixed set of queries, are a per-key linear consumer with read operator P = QᵀQ/n, as that harness computes it | iff the queries span the key space | the scores: ν = 0 in exact arithmetic; the softmax: fails |
| MUSIC direction-of-arrival on radar snapshots | DOA rows 031/033/034 | not checked | not checked | not checked |
| a citation-ranking consumer | legal rows 035/036/039 | not checked | not checked | not checked |

*[decided]* **Three synthetic arms gate the verdict, on CPU. One real arm, report-only, runs
once after the seal.** Reason: the theorem can be tested only where (A1) holds with constants
known in advance. No trained consumer in the ledger is known to satisfy (A1) except through a
linear layer, where it holds with ν = 0 and the prediction is exact by construction. That
choice is also what makes every bar a consequence of a proved result (see "What it would
show").

- **Arm L, linear control.** C(x) = x, output metric G = diag(4, 1). Then ν₋ = ν₊ = 0, Q = G,
  and the prediction is exact.
- **Arm S, smooth monotone consumer, the theorem's regime.** C(x) = x + β sin x
  componentwise, G = diag(4, 1), β ∈ {0.05, 0.2}.
  - **The constants are known in advance exactly.** By the mean value theorem each
    coordinate's difference quotient lies in [1 − β, 1 + β]. With q(s²) = E(1 + β cos X)² for
    X ~ N(0, s²),
    - q(s²) = 1 + 2β e^{−s²/2} + (β²/2)(1 + e^{−2s²});
    - Q = G·diag(q(σ₁²), q(σ₂²));
    - 1 − ν₋ = minᵢ (1 − β)²/qᵢ and 1 + ν₊ = maxᵢ (1 + β)²/qᵢ.
  - **Derivative bounds of g = G^{1/2}C**, for Proposition 2: the maps are diagonal, so
    M₁ = 2(1 + β) and M₂ = M₃ = 2β.
- **Arm B, boundary, report-only.** A softmax read-out C(x) = softmax(Wx), W a fixed 3×2 matrix
  drawn with seed 20261117 and scaled to unit spectral norm, G = I₃.
  - **(A1a) fails** because the loss saturates, so no lower constant below one exists. The read
    metric is nonsingular at every point (the registered W leaves the all-ones vector outside
    its range; the note's check C7), but it tends to zero at saturated points.
  - **Theorem 5 applies**, because the consumer has three bounded derivatives. But M₁–M₃ for
    softmax(Wx) are not computed, so it gives no bar.
  - **Corollary 8 would be vacuous:** M₁ ≤ 1/2 gives ν₊ = M₁²/λmin(Q) − 1 ≈ 1270, and ε₋ < 1
    would then need m > 9,400.
  - So the run applies the same recipe and records the outcome.
- **Arm R, real consumer, report-only, run once after the seal.** The per-key attention-score
  consumer of the GO-P-2026-027 harness on held-out layers, keys as symbols, with the true
  operator P = QᵀQ/n from that harness. The owner gave the compute go-ahead for Atlas GPU 1 on
  2026-11-17, and decided on 2026-11-18 that the arm runs. Its instrument is
  `experiments/t1_arm_r_llama.py` (see "The instrument", item 3).
  - **Reported:**
    - the recovery error of P from black-box score queries in bfloat16, with the paired
      finite-difference estimator of Remark 17;
    - the probing count;
    - at matched rate, the softmax divergence of the learned design against the
      reconstruction design.
  - **The consumer is noisy.** The scores are linear, so ν = 0 holds only in exact
    arithmetic. The bfloat16 black box is a noisy consumer in the sense of Remark 17.
  - **The leakage is a formula, not a measurement.** The keys are not Gaussian. The reported
    leakage is the Gaussian formula for the design; RLD-III.3, an `[exploratory]` ledger row,
    makes that region achievable for a memoryless non-Gaussian source. It is not the leakage
    of the forward channel the instrument actually applies to the keys.

## The holder — [decided]

S = H T + U with H = (1, 0.5) and U ~ N(0, 1), as in the series' existing checks
(`verify_vector_ergodic.py`, `verify_ergodic_memory.py`), at all three weights α ∈ {0, 0.5, 1}.
Reason: the holder is what distinguishes the RLD frontier from a rate–distortion function, and
the slice α = 1, where it plays no part, comes free in the same run. Arm R uses a fixed random
8×d_head Gaussian H drawn with seed 20261117, with noise variance equal to the mean
per-coordinate key variance.

## Instance

```yaml
id: GO-P-2026-NNN            # assigned at sealing (092 is free at the time of writing)
date: YYYY-MM-DD             # the sealing date; must predate the first governed measurement
status: DRAFT                # set to "SEALED <date>" before seal.py, never after
governs: experiments/t1_worked_result.py, experiments/t1_arm_r_llama.py
    # both v1.1, 2026-11-18. Smoke-tested only: the synthetic arms on a different instance
    # (p = 3, Sigma = I, beta = 0.1); arm R (as v1.0) on layer 12 with its own text. See pilot.
    # No governed number has been seen.
instruments_sha256:          # text sha256 with line endings normalized. Recomputed and checked at
                             # sealing; both guards refuse unless every listed file matches.
                             # Do not rename these keys to end in "hash" (seal.py's pattern).
  experiments/t1_worked_result.py: efb97381cd6a27f50db8c4a981ec763f662b348879b19092083565ff511dfa32
  experiments/t1_arm_r_llama.py: 5586527eb6eba7c868380c6fc34df3327aeccd21f571dcbb93ca2d2476fb0576
  paper/tit-stationary/spectral_core.py: af1ef7d5ccf363a04660812f4bf2a1f06f3268bb5bc2719cf77fde54f8386272
retrospective: true
    # H1's sampling distribution (note check C2: 4000 probe sets per cell, coverage 1.0 at
    # eps+-) and H2's reference loss (check C5: loss / tr(Q Delta) = 0.99986 and 0.99813) were
    # computed on this instance before sealing; no governed seed array was used. Class at most
    # [demonstrated]; the governed draws are the registered replication.
claim: "On the synthetic instance p = 2, Sigma = diag(2, 0.5), G = diag(4, 1), holder
    S = (1, 0.5) T + U, the learn-then-serve chain of the T1 note v4.1, with Jacobians from
    2p consumer queries per probe point, meets Lemma 1's one-sided bounds (with Proposition 2's
    finite-difference term) and Theorem 11(b)'s loss and cost bounds at the level of Gaussian
    test channels for the consumers x and x + beta sin x (beta = 0.05, 0.2), and the learned
    design keeps at least half the closed-form consumer benefit at 2 bits."
target: a new ledger row for the worked result, at most [demonstrated]; this run does not
    change the class of the T1 row
instance:
  representation: T ~ N(0, Sigma), Sigma = diag(2, 0.5), p = 2      # [decided]
      # anisotropic, so that the consumer's weight and the source disagree in their
      # ordering of the two coordinates' value per bit at moderate rate
  consumer: arms L, S (beta in {0.05, 0.2}), B, and R, as above      # [decided]
      # loss: ||C(x_hat) - C(x)||_G^2, measured by Monte Carlo
  holder: S = H T + U, H = (1, 0.5), U ~ N(0, 1); alpha in {0, 0.5, 1}   # [decided]
  probe_distribution: pi = N(0, Sigma), the source law                    # [decided]
  distortion: D = 0.3 * tr(Q Sigma)                                        # [decided]
      # the series' check convention (0.3 D_max); Corollary 8 needs D below about
      # 0.28 (beta 0.05) and 0.076 (beta 0.2) of tr(Q Sigma), so it is not tested
probe_output:
  read_operator: Q_hat = mean of J(x_i)^T G J(x_i) over m probe points
  jacobians: central differences, step h = 1e-4, noiseless outputs (arms L, S, B)   # [decided]
      # Proposition 2: eps_h = (2 M1 sqrt(p) b + p b^2) / lambda_min(Q), b = M3 h^2 / 6;
      # eps_h = 9.2e-10 (beta 0.05), 3.4e-9 (beta 0.2), 0 (arm L).
      # arm R: the paired estimator of Remark 17, two independent difference Jacobians per point
  nu_bounds: arms L, S: the closed forms above, computed before the run and written into the
      sealed document; arm B: none ((A1a) fails). nu_hat is also measured on 10^4 held-out
      pairs and reported, never used for a bar.
  derivative_bounds: arm S: M1 = 2 (1 + beta), M2 = M3 = 2 beta; arm L: M1 = 2, M2 = M3 = 0
  queries: 2 p m consumer evaluations per probe set at the learner (4 m for p = 2), and as many
      again at the decoder under (A3-i): 4 p m per session
prediction:               # [decided] bars set from closed forms; see margins and power
  H1_estimation: per arm in {L, S(0.05), S(0.2)} and m in {8, 32, 128, 512}, with
      M = Q^{-1/2} Q_hat Q^{-1/2}: lambda_max(M) - 1 <= eps_+ + eps_h and
      1 - lambda_min(M) <= eps_- + eps_h, eps_pm = sqrt(2 nu+ nu- L/m) + 2 nu_pm L/(3m),
      L = ln(2p/delta) = ln 40, delta = 0.1 (Lemma 1 and Proposition 2), in at least 14 of 20
      seeds per cell (arm L: nu = 0 and eps_h = 0, so the bar is exact recovery to 1e-6)
  H2_loss: on the seeds where the H1 event holds, the Gaussian test channel built for Q_hat at
      D_hat = D (1 - eps_- - eps_h)/(1 + nu_plus) (the frontier point at weight alpha) has
      Monte Carlo consumer loss at most D (1 + 0.005) + 4 SE, n_mc = 2e5, for every alpha and
      seed (Theorem 11(b))
  H3_price: on the same seeds, its weighted cost alpha R + (1 - alpha) L is at most
      V_Q(alpha, D/(1 - nu_minus)) + tau + 1e-6 bits,
      tau = (p/2) log2[(1 + nu_plus)(1 + eps_+ + eps_h)/((1 - nu_minus)(1 - eps_- - eps_h))],
      for every alpha and seed (Theorem 11(b))
  H4_benefit: rate-only slice (alpha = 1), matched rate R = 2 bits per symbol: the consumer
      quadratic distortion tr(Q Delta) of the design for Q_hat is lower than that of the
      reconstruction design (water-filling on Sigma) by at least half the closed-form
      reduction for the true Q, in at least 14 of 20 seeds per cell, for m in {32, 128, 512}
  recorded_without_bar: per seed, the one-sided errors lambda_max(M) - 1 and 1 - lambda_min(M);
      per seed and alpha, tr(Q Delta_hat), tr(Q_hat Delta_hat) and loss / tr(Q Delta_hat)
      (Theorem 5's quantity; its bound rho is 16-76% of tr(Q Delta_hat) here, so no bar);
      the gap to the design for the true Q at the full budget D; the looseness part tau_nu
      of tau, which is an upper bound and not a price shown to be paid; nu_hat
  effect_floor:   # [decided] half the closed-form reductions at R = 2 bits, computed from the
      # instance before any run (design calculation of 2026-11-17, no data):
      # arm L 20.0% -> 10.0%; S(0.05) 19.1% -> 9.5%; S(0.2) 16.8% -> 8.4%.
      # At R = 1 bit the two designs coincide (one active component), which is why the slice
      # is taken at 2 bits.
  margins:        # why no gating bar can fail with a correct instrument (cold reread)
      # H2: on the H1 event, tr(Q Delta_hat) <= D_hat/(1 - eps_- - eps_h) = D/(1 + nu+), and at
      #   every sample the loss is at most (1 + nu+) times the quadratic form (mean value
      #   theorem). Largest tr(Q Delta_hat)/D on the event: 0.9416 (beta 0.05), 0.8108 (beta 0.2).
      #   A fail on arms S needs a Monte Carlo excursion of about 5-6 standard errors. Arm L's
      #   expected loss is exactly D, and its 0.5% margin is 1.9 SE.
      # H3: deterministic given Q_hat. Smallest slack over the event boundary and all alpha:
      #   S(0.05) 0.262 / 0.190 / 0.159 / 0.145 bits and S(0.2) 0.696 / 0.673 / 0.608 / 0.571
      #   bits at m = 8 / 32 / 128 / 512. The solver's noise is at most 7.7e-12 bits.
      # H4: deterministic given Q_hat. On the H1 event the reduction is at least 18.9 / 19.0 /
      #   19.1% (S 0.05) and 15.1 / 16.4 / 16.7% (S 0.2) at m = 32 / 128 / 512, against floors
      #   9.5% and 8.4% (a grid computation, not a proof). H4 first fails at a relative
      #   estimation error of about 0.46 (L), 0.45 (S 0.05), 0.42 (S 0.2); the largest eps in
      #   any H4 cell is 0.208.
  power:          # [decided]
      # H1: each seed fails with probability at most delta = 0.1 (delta/2 per tail), so
      #   P(>= 7 failures of 20) <= 0.0024 per cell; the 8 cells of arms S give a family-wise
      #   false-fail rate <= 0.019 (alpha family-corrected, per the V6 lesson). The statistic's
      #   closed-form relative spread per coordinate is 0.001-0.076, so the bar sits at least
      #   4.7 standard deviations out (prior data: check C2's coverage was 1.0). What H1 can
      #   detect: were the true coverage 0.7, a cell would fail with probability 0.39.
      # H2: 4 SE + 0.5% per test, at most 3e-5 per test (conservative), over at most
      #   2 x 4 x 3 x 20 = 480 tests on arms S: family-wise <= 0.015.
      # H3: deterministic given Q_hat; tolerance 1e-6 bits against solver noise below 1e-11.
      # H4: on every seed inside the H1 event H4 holds (margins), so a cell misses only if H1's
      #   cell does: probability <= 0.0024 per cell, by Lemma 1 and the grid computation.
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
      - the rewrite of 2026-11-18: the closed-form constants of the table below, from the
        instrument's own Arm class (no probe draws); the smoke run of v1.1; guard tests in a
        throwaway repository.
      - smoke runs: t1_worked_result.py --smoke (a different instance); arm R on layer 12
        (results/t1-arm-r-smoke-2026-11-17.json).
      No bar was set or moved in response to any of these. H1 moved from eps_m to eps+- because
      the note's Lemma 1 changed; H4's count moved because of the bound it cites.
design:
  m_probes: [8, 32, 128, 512]                 # [decided] eps_- spans 0.147 to 0.013 at beta = 0.05
  seeds: 20 per (arm, beta, m), base seed 20261117   # [decided]
  clusters: the seed (an independent probe set)       # [decided]
  stopping: fixed-n
  codes: Gaussian test channels at the frontier points of the RLD-I setting (memoryless
      Gaussian vector), computed by the series' solver (`paper/tit-stationary/spectral_core.py`,
      one block). [decided] No practical quantizer in this registration: the leakage of an
      operational code cannot be measured at these sizes, and Theorem 7 of the note makes the
      test channels operational in RLD I; a rate-only entropy-coded dithered quantizer arm is
      named as a follow-on, not run here.
  bits_matched_via: the closed-form rate of the Gaussian test channel   # [decided]
  serving_horizon: K = 1e6 symbols; probing overhead 4pm/K queries per symbol
      (2pm at the learner and 2pm at the decoder under (A3-i))         # [decided]
gates:                    # fixed here, before the run (PE-CLS s3.2)
  instrument: [SC1, SC2, SC3, arm L (H1 exact, H2, H3, H4), shuffled control, seal guard]
      # a miss voids the run; the instrument reports "VOID: <gates>"
  physics: [H1, H2, H3, H4 on arms S(0.05) and S(0.2)]
      # a miss, with every instrument gate passing, refutes; see "What a miss would mean"
runs: one governed run of t1_worked_result.py; one governed capture of arm R on Atlas GPU 1 and
    one governed analysis of it. No reruns. After a void, a rerun needs a fixed instrument,
    hence new hashes, hence a new registration number that cites this one and its void.
results: results/GO-P-2026-NNN-t1-worked-result.json and results/GO-P-2026-NNN-t1-arm-r.json,
    committed with the run
controls: [arm L (nu = 0, exact),
           arm B ((A1a) fails, report-only),
           shuffled estimate (the design for P Q_hat P^T, P reversing the coordinates; a
             guaranteed H4 miss, reductions -70.0 / -66.2 / -57.1% against floors
             10.0 / 9.5 / 8.4%: the witness that the grading code can return a miss),
           reconstruction-optimal code (the H4 comparator)]
template_fields:
  q_family: n/a (the probe law is pi; no family of probes is compared)
  invariant: n/a; nuisance: n/a; predicted_failure_class: n/a
      # this is not a probe-output study; as in 090 and 091, these fields do not apply
  arm_ordering: H4 (the learned design beats the reconstruction design on consumer distortion)
  n: 20 seeds per cell
admissibility:
  exempt: "numerical verification of proved results (Lemma 1, Proposition 2 and Theorem 11(b)
    of the T1 note v4.1) on a synthetic instance; with a correct instrument no gating bar can
    fail (margins above). Witnesses that the grading code can return a miss: the shuffled
    control (a guaranteed H4 miss in every cell) and constructed records (Q_hat = 1.5 Q for
    H1; a loss of 1.1 D for H2)."
amendments: []            # none; an amendment before the run takes a new registration number
hash: sha256:...             # written by scripts/seal.py
```

### The design calculation (closed forms only, no data)

Recomputed 2026-11-18 at full precision from the instrument's own `Arm` class, with ε± and
Proposition 2's ε_h. It agrees with the cold reread's independent values.

| Arm | ν₋ | ν₊ | ε_h | τ_ν (looseness part, bits) | H4 closed-form reduction at R = 2 |
|---|---|---|---|---|---|
| L (β = 0) | 0 | 0 | 0 | 0 | 20.0% |
| S, β = 0.05 | 0.1640 | 0.0621 | 9.2e-10 | 0.345 | 19.1% |
| S, β = 0.2 | 0.5220 | 0.2334 | 3.4e-9 | 1.368 | 16.8% |

| Arm | m | ε₊ | ε₋ | D̂/D | τ (bits per symbol) | of which τ_ε |
|---|---|---|---|---|---|---|
| S(0.05) | 8 | 0.1160 | 0.1473 | 0.8028 | 0.734 | 0.388 |
| S(0.05) | 32 | 0.0532 | 0.0611 | 0.8841 | 0.511 | 0.166 |
| S(0.05) | 128 | 0.0254 | 0.0274 | 0.9158 | 0.422 | 0.076 |
| S(0.05) | 512 | 0.0124 | 0.0129 | 0.9294 | 0.382 | 0.037 |
| S(0.2) | 8 | 0.4069 | 0.4956 | 0.4089 | 2.848 | 1.480 |
| S(0.2) | 32 | 0.1855 | 0.2077 | 0.6424 | 1.949 | 0.581 |
| S(0.2) | 128 | 0.0883 | 0.0938 | 0.7347 | 1.632 | 0.264 |
| S(0.2) | 512 | 0.0430 | 0.0444 | 0.7748 | 1.494 | 0.126 |

Arm L has ε± = ε_h = 0, D̂ = D and τ = 0.

**Read honestly:**
- At β = 0.05 the bound is within half a bit per symbol once m ≥ 128, and most of it is the
  sandwich's looseness, not learning.
- At β = 0.2 the looseness alone is 1.4 bits, which is the sandwich's stated weakness made
  concrete.

The registration verifies the bound where it is proved to hold and reports how loose it is
there.

## The instrument (v1.1, 2026-11-18)

`experiments/t1_worked_result.py` has two modes.

- `--smoke` runs only the smoke instance: p = 3, Σ = I, G = diag(3, 2, 1), β = 0.1,
  H = (1, 0.5, 0.25), 5 seeds, base seed 7, m ∈ {8, 32}.
- `--governed --prereg <file>` runs the registered instance. It refuses unless all of these
  hold:
  - the prereg file is committed and unmodified against HEAD;
  - its status is SEALED;
  - its sha256 verifies by the rule of `scripts/seal.py`, so a file amended after sealing is
    refused (an amendment before the run takes a new registration number);
  - its `governs:` line names the script;
  - its `instruments_sha256:` block records the script and the solver, and every file the
    block lists has exactly that text sha256 now;
  - the script and the solver are committed and unmodified.

  Adding `--verify-only` runs those checks and exits without measuring. Run it right after
  the sealing commit.

**Guard tests.** The guard was tested on 2026-11-18 in a throwaway repository (ten cases). It
accepts a sealed, committed file whose hashes match. It refuses:
- an instrument edited, before or after a commit;
- the solver edited and committed;
- arm R's script edited and committed;
- a prereg amended after sealing;
- a missing block, or a block without the solver;
- a draft status.

**Smoke run.** v1.1 gave ALL PASS in about 6 s.

The instrument fixes these details:

1. **Held-out pairs for ν̂:** 10⁴ pairs of independent draws from π. ν̂₋ = 1 − min r and
   ν̂₊ = max r − 1, where r is the loss divided by (x̂ − x)ᵀQ(x̂ − x).
2. **Arm B:**
   - Q is a Monte Carlo average of the analytic JᵀJ over 10⁶ draws, and its standard error is
     recorded.
   - The design uses the plug-in D̂ = D, because there is no ν.
   - At 2 bits it is compared with the reconstruction design by the Monte Carlo consumer loss.
   - It has no bars.
3. **Arm R** has its own instrument, `experiments/t1_arm_r_llama.py` (v1.1), which runs in
   two stages.
   - **`capture`, on Atlas GPU 1.** It requires `CUDA_VISIBLE_DEVICES=1`, runs under the
     batch-probe thermal controller, and is pinned off CPU 0. It captures post-RoPE q and k
     with the GO-027 patch, frees the model, and then probes the black-box consumer.
   - **`analyze`, local.** For the governed instance it refuses unless all of these hold:
     - the prereg passes the same seal guard, naming both scripts;
     - the capture recorded the prereg's sha256;
     - the capture's recorded script hash equals the prereg's recorded hash for the script;
     - the capture postdates the prereg commit.

   Details it fixes:
   - **Model and data:** `unsloth/Llama-3.2-3B`, in bfloat16. Governed layers are {6, 24},
     held out from 026's {8, 16}, 027's {4, 20} and the smoke's {12}. The corpus is GO-027's
     text, as 8 rows × 256 tokens.
   - **Symbols:** all 8 KV heads per layer. The symbols are the head's 2048 keys.
   - **Consumer:** the group's 768 row-0 queries, C(k) = Qk/√d in bfloat16, with G = (d/n)I,
     so P = QᵀQ/n.
   - **Probing:**
     - probe points are keys drawn with replacement;
     - within a seed the probe sets are nested: each m uses a prefix of one draw of 128
       points, unlike the synthetic arms;
     - each Jacobian uses a random orthonormal basis and the step h = √(tr Σ/d).
   - **Estimators:** plain, at 2d queries per point; paired, with a second independent basis,
     at 4d queries per point (Remark 17). m ∈ {1, 8, 32, 128}, with 5 seeds, from
     `default_rng([20261117, layer, head, seed])`.
   - **Source law:** Σ = Cov + 10⁻⁶I, the GO-027 convention. The holder H is 8 × 128 from
     `default_rng(20261117)`, with noise s² = tr Σ/d.
   - **Designs:** at α = 1, at the matched rates R ∈ {32, 64, 128, 256} bits per key:
     - reconstruction;
     - oracle P;
     - learned: paired and plain at m = 128, and paired at m = 1.
   - **Serving:** each design is applied to the real keys through the forward Gaussian test
     channel.
   - **Reported for each design:**
     - tr(PΔ), and the realized read error;
     - the leakage by the Gaussian formula (see arm R above);
     - the softmax KL of a full, non-causal softmax of the 768 row-0 queries over the 256
       row-0 keys, from 4 common-random-number draws.

   **Disclosure: an exploratory smoke run of arm R was seen.** It ran on 2026-11-17 on layer
   12 only, with its own text and seeds (base seed 7; m ∈ {1, 8, 32}; 3 seeds; R ∈ {64, 128}),
   made by the committed v1.0 script. Its record is
   `results/t1-arm-r-smoke-2026-11-17.json`. Medians over the 8 heads:
   - **Error in Frobenius norm:** plain 5.9% at m = 1 and 1.0% at m = 32; paired 4.2% and
     0.78%.
   - **Error in the whitened metric:** much larger (paired 0.13 at m = 32), because P is
     badly conditioned (condition number about 1700, effective rank about 5 for head 0).
   - **Trace bias:** plain +0.36%; paired −0.03%. This is Remark 17's qualitative prediction,
     already seen, so it is not prospective.
   - **Softmax divergence.** The reconstruction design's median divergence is 0.21 at R = 64
     and 0.076 at R = 128. The oracle's divergence is about 0.28 (R = 64) and 0.26 (R = 128)
     *times* the reconstruction design's. Every learned design, including m = 1, is within
     0.001 of the oracle's ratio.

   Arm R has no bars, so nothing could be tuned on this run. The smoke run never touched
   layers 6 or 24, and no harness on GO-027's corpus has captured them. If the governed run
   repeats this pattern, arm R is a held-out replication of a report-only observation,
   reported at `[exploratory]`.
4. **Seeds:**
   - Every draw comes from `default_rng([20261117, arm code, round(10⁴β), m, seed, purpose,
     …])`.
   - Probe sets are independent across m.
   - W for arm B comes from `default_rng(20261117)`, as registered.
5. **Shuffled control:** the design for PQ̂Pᵀ, the estimate with its coordinates reversed. It
   must miss the H4 criterion (fewer than 14 of 20 seeds at the floor) in every cell; by the
   closed form it misses on every seed.
6. **H2 and H3** are evaluated only on seeds where the H1 event holds. The other seeds are
   recorded as null, and the count per cell is reported.
7. **Self-checks:**
   - SC1: the rate-2 water-filling matches the series' solver.
   - SC2: the held-out ratios lie inside the a priori (ν₋, ν₊).
   - SC3: the closed form of Q for arm S matches a Monte Carlo average of the analytic JᵀGJ.
8. **Verdict.** It follows `gates:`.
   - "VOID: …" if any instrument gate misses.
   - Otherwise "ALL PASS" if every physics gate holds, or "MISS: …" naming the physics gates
     that missed.

## What a miss would mean

These gates are fixed here, before the run.

- **Instrument gates void the run.** A void is recorded as `void: <gate>`. A rerun needs a
  fixed instrument and so a new registration number (`runs:`). The instrument gates are:
  - SC1–SC3;
  - arm L in full: exact recovery to 1e-6, and H2, H3 and H4 on arm L;
  - the shuffled control, which must miss H4 in every cell;
  - the seal guard.
- **Physics gates** are H1–H4 on arms S(0.05) and S(0.2). Each follows from a proved result:
  Lemma 1 with Proposition 2's ε_h; Theorem 11(b) together with the mean value theorem; and the
  deterministic H4 calculation. Their margins are stated in `margins:`.

  A miss on a physics gate, with every instrument gate passing, contradicts a proved result at
  this instance. It is logged as a verification incident against the result named below, and
  it stays in the record whatever a later examination of the code finds.
  - **H1 misses:** Lemma 1, with ε_h, failed on a consumer that meets its hypotheses.
  - **H2 or H3 misses, with H1 holding:** for a Gaussian test channel, either Theorem 11(b)
    failed or arm S's mean-value sandwich did. For H3 this is equivalent to the series' solver
    violating (P1)–(P3).
  - **H4 misses, with H1 holding:** at least 7 seeds had a relative estimation error of about
    0.42 or more, far outside Lemma 1's event. That is a failure of Lemma 1 on seeds that H1's
    rule tolerates. It is not a statement about the consumer's anisotropy, whose value at this
    instance is a closed form.
- **Arms B and R carry no bars.**
  - Theorem 5 applies to arm B, but its derivative bounds are not computed.
  - Arm R's scores are linear only in exact arithmetic. Its bfloat16 noise has no constants
    (Remark 17), and its softmax divergence reads across keys, which the note does not cover
    (Remark 16).

  Results for both arms are reported at `[exploratory]`.

## Not in scope

- The low-rank case with a kernel that moves or a range estimated with error (priced through
  principal angles, the commission tax and the omission floor).
- Consumers that read across dependent symbols.
- Practical quantizers.
- Any monitor or false-clear-rate claim.
- Corollary 8, which this D does not reach.
- The second-order coefficient c₂ of Remark 6, which is formal, below the Monte Carlo
  resolution per seed, and already computed on this instance by check C5.
