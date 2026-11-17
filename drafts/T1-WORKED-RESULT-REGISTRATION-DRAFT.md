# DRAFT — T1 worked result: learn a consumer's read operator, pay for the probing, serve it, and bound the downstream loss against the RLD frontier

**Status: DRAFT, NOT SEALED, NO REGISTRATION NUMBER.** Drafted 2026-11-17 by
Claude (Opus 5.5) at the owner's request, from the T1 proof sketch
(`paper/t1-learn-then-serve`) and an outside reader's recommendation that the next
synthesis centre on one worked result. **The items formerly marked OWNER were
filled the same day by Claude at the owner's instruction**; each is marked
*[decided]* with its reason, and the owner may override any of them at the cold
reread. Under PE-CLS-1.0 (procedure 1b) the draft must be reread cold in a later
session, and rewritten as needed, before it is sealed; it then takes the next free
`GO-P-2026-NNN` (092 at the time of writing) and moves to `prereg/`. No governed
measurement may be run before the sealing commit exists.

## What it would show

The complete chain from an observer to an achievable resource limit: (1) recover the
consumer's read operator from queries alone, (2) charge the queries, (3) build the
description for the recovered operator with the coding theorems of the
rate–leakage–distortion (RLD) series, and (4) measure its downstream loss and its rate
and leakage against the frontier computed with the true operator. The T1 sketch
predicts all four under its assumption (A1); the run tests the predictions where (A1)
holds with constants known in advance, measures the looseness the sketch admits, and
records how far the same recipe lands for a consumer that fails (A1).

## The consumer — [decided]

The sketch covers a consumer that (a) acts on each symbol separately, (b) has a read
metric of full rank on the symbols' space, or of lower rank with a kernel that does
not move (then only in the settings of RLD I–III), and (c) has a loss between 1 − ν₋
and 1 + ν₊ times a quadratic form, with constants well below one, **known in
advance**, for all pairs of points in the source's support. A fresh-context audit of
the sketch (ledger VI-22) found that for a Gaussian source (c) forces a globally
bi-Lipschitz consumer, so the sketch speaks only near linearity. Consumers the ledger
already instruments:

| Candidate | Existing instrument | (a) per symbol | (b) full rank | (c) near-quadratic |
|---|---|---|---|---|
| attention heads of a trained language model, keys as symbols | GO-P-2026-027 harness `experiments/gateB_llama_asymptotic_floor.py` (Llama-3.2-3B, Atlas GPU 1) | the softmax reads across tokens and fails (c); the scores before it, for a fixed set of queries, are a per-key linear consumer with read operator P = QᵀQ/n, as that harness computes it | full rank iff the queries span the key space | the scores: ν = 0 exactly; the softmax: fails |
| MUSIC direction-of-arrival on radar snapshots | DOA rows 031/033/034 | not checked | not checked | not checked |
| a citation-ranking consumer | legal rows 035/036/039 | not checked | not checked | not checked |

*[decided]* **Three arms gate the verdict, all synthetic, on CPU; one real arm is
optional and report-only.** Reason: the theorem can be tested only where (c) holds
with constants known in advance, and no trained consumer in the ledger is known to
satisfy (c) except through a linear layer, where (c) holds with ν = 0 and the
prediction is exact by construction. So:

- **Arm L — linear control.** C(x) = x, output metric G = diag(4, 1). Then ν₋ = ν₊ = 0,
  Q = G, and the prediction is exact.
- **Arm S — smooth monotone consumer, the theorem's regime.**
  C(x) = x + β sin x componentwise, G = diag(4, 1), β ∈ {0.05, 0.2}. The constants are
  known in advance exactly: by the mean value theorem each coordinate's difference
  quotient lies in [1 − β, 1 + β], so with q(s²) = E(1 + β cos X)² for X ~ N(0, s²),
  q(s²) = 1 + 2β e^{−s²/2} + (β²/2)(1 + e^{−2s²}), and Q = G·diag(q(σ₁²), q(σ₂²)),
  1 − ν₋ = minᵢ (1 − β)²/qᵢ and 1 + ν₊ = maxᵢ (1 + β)²/qᵢ.
- **Arm B — boundary, report-only.** A softmax read-out C(x) = softmax(Wx), W a fixed
  3×2 matrix drawn with seed 20261117 and scaled to unit spectral norm, G = I₃. (c)
  fails (its read metric is not bounded below and has a kernel), so there is no
  prediction to test; the run applies the same recipe and records the outcome.
- **Arm R — real consumer, optional, report-only.** The per-key attention-score
  consumer of the GO-P-2026-027 harness on held-out layers, keys as symbols, with the
  true operator P = QᵀQ/n from that harness. It needs the owner's compute go-ahead for
  Atlas GPU 1 (not given at drafting); without it the arm is dropped at sealing and
  nothing else changes. If run: report the recovery error of P from black-box score
  queries in bfloat16 (with the paired finite-difference estimator), the probing
  count, and, at matched rate, the softmax divergence of the learned design against
  the reconstruction design. The keys are not Gaussian; by RLD-III.3 the Gaussian
  frontier with the keys' covariance is achievable for them, so the computed rate and
  leakage are upper bounds there.

## The holder — [decided]

S = H T + U with H = (1, 0.5) and U ~ N(0, 1), as in the series' existing checks
(`verify_vector_ergodic.py`, `verify_ergodic_memory.py`); all three weights
α ∈ {0, 0.5, 1}. Reason: the holder is what distinguishes the RLD frontier from a
rate–distortion function, and the slice α = 1, where it plays no part, comes free in
the same run. Arm R, if run, uses a fixed random 8×d_head Gaussian H drawn with seed
20261117 and noise variance equal to the mean per-coordinate key variance.

## Instance

```yaml
id: GO-P-2026-NNN            # assigned at sealing
date: YYYY-MM-DD             # must predate the first governed measurement
status: DRAFT                # set to "SEALED <date>" before seal.py, never after
governs: experiments/t1_worked_result.py   # v1.0, written 2026-11-17 BEFORE sealing;
    # smoke-tested only on a different instance (p = 3, Sigma = diag(1, 1, 1), beta = 0.1),
    # so no governed number has been seen; see "The instrument" below
instance:
  representation: T ~ N(0, Sigma), Sigma = diag(2, 0.5), p = 2      # [decided]
      # anisotropic, so that the consumer's weight and the source disagree in their
      # ordering of the two coordinates' value per bit at moderate rate
  consumer: arms L, S (beta in {0.05, 0.2}), B, and optional R, as above   # [decided]
      # loss: ||C(x_hat) - C(x)||_G^2, measured by Monte Carlo
  holder: S = H T + U, H = (1, 0.5), U ~ N(0, 1); alpha in {0, 0.5, 1}   # [decided]
  probe_distribution: pi = N(0, Sigma), the source law                    # [decided]
  distortion: D = 0.3 * tr(Q Sigma)                                        # [decided]
      # the series' check convention (0.3 D_max)
probe_output:
  read_operator: Q_hat = mean of J(x_i)^T G J(x_i) over m probe points
  jacobians: central differences, step h = 1e-4, noiseless outputs (arms L, S, B):
      # [decided] truncation bias O(h^2) ~ 1e-8 relative, negligible against eps_m;
      # arm R: the paired estimator, two independent difference Jacobians per point
  nu_bounds: arms L, S: the closed forms above, computed before the run and written into
      the sealed document; arm B: none (fails (c)). nu_hat is also measured on 10^4
      held-out pairs and reported, never used for a bar.
  queries: 2 p m consumer evaluations per probe set (4 m for p = 2)
prediction:               # [decided] bars set from closed forms; see power
  H1_estimation: per arm in {L, S(0.05), S(0.2)} and m in {8, 32, 128, 512}: the relative
      error ||Q^{-1/2} Q_hat Q^{-1/2} - I|| is at most eps_m = nu (sqrt(2L/m) + 2L/(3m)),
      L = ln(2p/delta) = ln 40, delta = 0.1, in at least 14 of 20 seeds per cell
      (arm L: nu = 0, so the bar is an exact recovery to 1e-6)
  H2_loss: on the seeds where the H1 event holds, the Gaussian test channel built for
      Q_hat at D_hat = D (1 - eps_m)/(1 + nu_plus) (the frontier point at weight alpha)
      has Monte Carlo consumer loss at most D (1 + 0.005) + 4 SE, n_mc = 2e5, for every
      alpha and seed
  H3_price: on the same seeds, its weighted cost alpha R + (1 - alpha) L is at most
      V_Q(alpha, D/(1 - nu_minus)) + tau + 1e-6 bits, tau = (p/2) log2[(1+nu_plus)(1+eps_m)
      /((1-nu_minus)(1-eps_m))], for every alpha and seed (a theorem consequence; any
      violation is an error in the theorem or the instrument). Also reported, with no
      bar: the gap to the code designed for the true Q at the full budget D, and the
      looseness part of tau, which is an upper bound and not a price shown to be paid.
  H4_benefit: rate-only slice (alpha = 1), matched rate R = 2 bits per symbol: the
      consumer quadratic distortion tr(Q Delta) of the design for Q_hat is lower than
      that of the reconstruction design (water-filling on Sigma) by at least half the
      closed-form reduction for the true Q, in at least 18 of 20 seeds per cell, for
      m in {32, 128, 512}
  effect_floor:   # [decided] half the closed-form reductions at R = 2 bits, computed
      # from the instance before any run (design calculation of 2026-11-17, no data):
      # arm L 20.0% -> 10.0%; S(0.05) 19.1% -> 9.5%; S(0.2) 16.8% -> 8.4%.
      # At R = 1 bit the two designs coincide (one active component), which is why
      # the slice is taken at 2 bits.
  power:          # [decided]
      # H1: if Lemma 1 holds, each seed fails with probability at most 0.1, so
      #   P(>= 7 failures of 20) <= 0.0024 per cell; 12 cells give a family-wise
      #   false-fail rate <= 0.03 (alpha family-corrected, per the V6 lesson). The
      #   audit's Monte Carlo found Lemma 1's coverage near 0.999, far above 0.9.
      # H2: 4 SE + 0.5% per test, about 3e-5 per test, over at most 3 x 4 x 3 x 20 = 720
      #   tests: family-wise <= 0.03.
      # H3: deterministic given Q_hat; tolerance = solver tolerance 1e-6 bits.
      # H4: deterministic given Q_hat. Checked by closed forms (drafts/t1-design/h4robust.py,
      #   20 000 random symmetric perturbations): for every Q_hat within relative error
      #   0.3 of Q, the reduction stays at least 16.2% (L), 15.2% (S, 0.05), 12.8% (S, 0.2),
      #   above the floors 10.0 / 9.5 / 8.4%; and eps_m <= 0.3 in every H4 cell (m >= 32:
      #   at most 0.291, at beta = 0.2, m = 32). A random search, not a proof.
  pilot: "NO pilot was run." The bars rest on closed forms; the design calculation of
      2026-11-17 used the instance's parameters only and no simulated data.
design:
  m_probes: [8, 32, 128, 512]                 # [decided] eps_m spans 0.2 to 0.02 at beta = 0.05
  seeds: 20 per (arm, beta, m), base seed 20261117   # [decided]
  clusters: the seed (an independent probe set)       # [decided]
  stopping: fixed-n
  codes: Gaussian test channels at the frontier points of the RLD-I setting (memoryless
      Gaussian vector), computed by the series' solver (`paper/tit-stationary/spectral_core.py`,
      one block). [decided] No practical quantizer in this registration: the leakage of
      an operational code cannot be measured at these sizes, and the series' coding
      theorems already supply achievability; a rate-only entropy-coded dithered
      quantizer arm is named as a follow-on, not run here.
  bits_matched_via: the closed-form rate of the Gaussian test channel   # [decided]
  serving_horizon: K = 1e6 symbols for the per-symbol probing overhead 2pm/K  # [decided]
controls: [arm L (nu = 0, exact), arm B (fails (A1), report-only),
           shuffled-consumer (Q_hat from a consumer with permuted coordinates; H4 must fail),
           reconstruction-optimal code (the H4 comparator)]
amendments: []
hash: sha256:...             # written by scripts/seal.py
```

### The design calculation (2026-11-17, closed forms only, no data)

| Arm | ν₋ | ν₊ | looseness part of τ (p = 2) | τ at m = 8 / 32 / 128 / 512 (bits per symbol) | H4 closed-form reduction at R = 2 |
|---|---|---|---|---|---|
| L (β = 0) | 0 | 0 | 0 | 0 / 0 / 0 / 0 | 20.0% |
| S, β = 0.05 | 0.164 | 0.062 | 0.345 | 0.954 / 0.610 / 0.468 / 0.404 | 19.1% |
| S, β = 0.2 | 0.522 | 0.233 | 1.368 | 3.664 / 2.231 / 1.760 / 1.556 | 16.8% |

Read honestly: at β = 0.05 the bound is within half a bit per symbol once m ≥ 128, and
most of it is the sandwich's looseness, not learning; at β = 0.2 the looseness alone is
1.4 bits, which is the sketch's stated weakness made concrete. The registration tests
the bound where it is supposed to hold and reports how loose it is there.

## The instrument (v1.0, written 2026-11-17, for the cold reread)

`experiments/t1_worked_result.py` has two modes.

- `--smoke` runs only the smoke instance: p = 3, Σ = I, G = diag(3, 2, 1), β = 0.1,
  H = (1, 0.5, 0.25), 5 seeds, base seed 7, m ∈ {8, 32}.
- `--governed --prereg <file>` runs the registered instance. It refuses unless all of
  these hold:
  - the prereg file is committed and unmodified against HEAD;
  - its status is SEALED;
  - its sha256 verifies by the rule of `scripts/seal.py`;
  - its `governs:` line names the script;
  - the script itself is committed and unmodified.

  Adding `--verify-only` runs those checks and exits without measuring. Run it right
  after sealing.

The guard was tested in a throwaway repository. It accepts a sealed, committed file. It
refuses a draft, a prereg edited after sealing, and a modified script.

The smoke run gave ALL PASS in about 2 s, and two runs were bit-identical apart from
wall time. No governed instance has been run.

The instrument fixes these details, which the text above does not state. The reread
should adopt them into the registration or change the script before sealing:

1. **Held-out pairs for ν̂:** 10⁴ pairs of independent draws from π. ν̂₋ = 1 − min r and
   ν̂₊ = max r − 1, where r is the loss divided by (x̂ − x)ᵀQ(x̂ − x).
2. **Arm B:**
   - Q is a Monte Carlo average of the analytic JᵀJ over 10⁶ draws, and its standard
     error is recorded.
   - The design uses the plug-in D̂ = D, because there is no ν.
   - At 2 bits it is compared with the reconstruction design by the Monte Carlo consumer
     loss.
   - It has no bars.
3. **Arm R** is not implemented. Drop it at sealing unless the owner gives the GPU
   go-ahead first; in that case write a separate instrument and amend `governs:`.
4. **Seeds:**
   - Every draw comes from `default_rng([20261117, arm code, round(10⁴β), m, seed,
     purpose, …])`.
   - Probe sets are independent across m.
   - W for arm B comes from `default_rng(20261117)`, as registered.
5. **Shuffled control:** the design for PQ̂Pᵀ, where P reverses the coordinates. It must
   miss the H4 criterion (fewer than 18 of 20 seeds at the floor) in every cell.
6. **H2 and H3** are evaluated only on seeds where the H1 event holds. The other seeds
   are recorded as null.
7. **Self-checks:**
   - SC1: the rate-2 water-filling matches the series' solver.
   - SC2: the held-out ratios lie inside the a priori (ν₋, ν₊).
   - SC3: the closed form of Q for arm S matches a Monte Carlo average of the analytic
     JᵀGJ.

   Any self-check failure makes the verdict "INSTRUMENT ERROR", not a pass or a miss.
8. **Verdict:** ALL PASS needs H1–H4, the shuffled control, arm L's exact recovery, and
   all three self-checks.

## What a miss would mean

- **H1 misses** (arms L or S): the matrix-Bernstein bound fails on a consumer that meets
  its hypotheses, or the instrument is wrong. Either is a finding against Lemma 1 or
  against the harness, and the instrument is checked first.
- **H1 holds, H2 or H3 misses:** a theorem consequence failed for Gaussian test
  channels; an error in the sketch's Theorem 2 or in the instrument. It would be logged
  as a verification incident and the sketch downgraded.
- **H4 misses with H1–H3 holding:** at this instance the consumer's anisotropy buys less
  than half its closed-form value; a boundary of the flip, not of T1.
- **Arm B and arm R** carry no bars; whatever they show is reported at the class
  `[exploratory]`, with the sentence that the sketch makes no prediction for them.

## Not in scope

The low-rank case with a kernel that moves or a range estimated with error (priced
through principal angles, the commission tax, and the omission floor), consumers that
read across dependent symbols, practical quantizers, and any monitor or
false-clear-rate claim.
