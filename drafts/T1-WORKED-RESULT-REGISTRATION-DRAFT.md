# DRAFT — T1 worked result: learn a consumer's read operator, pay for the probing, serve it, and bound the downstream loss against the RLD frontier

**Status: DRAFT, NOT SEALED, NO REGISTRATION NUMBER.** Drafted 2026-11-17 by
Claude (Opus 5.5) at the owner's request, from the T1 proof sketch
(`paper/t1-learn-then-serve`) and an outside reader's recommendation that the next
synthesis centre on one worked result. Under PE-CLS-1.0 (procedure 1b) it must be
reread cold in a later session, and rewritten as needed, before it is sealed; it then
takes the next free `GO-P-2026-NNN` (092 at the time of writing) and moves to
`prereg/`. Every item marked **OWNER** is the owner's decision. No governed
measurement may be run before the sealing commit exists.

## What it would show

The complete chain from an observer to an achievable resource limit, on one real
consumer: (1) recover the consumer's read operator from queries alone, (2) charge the
queries, (3) build the description for the recovered operator, and (4) measure its
downstream loss and its rate and leakage against the frontier of the
rate–leakage–distortion (RLD) series computed with the true operator. The T1 sketch
predicts all four quantities under its assumption (A1); the run tests whether a real
consumer meets (A1) closely enough for the predictions to hold, and reports by how
much they miss if it does not.

## The consumer — OWNER

The sketch covers a consumer that (a) acts on each symbol separately, (b) has a
read metric of full rank on the symbols' space, or of lower rank with a kernel that
does not move (then only in the settings of RLD I–III), and (c) has a loss between
1 − ν₋ and 1 + ν₊ times a quadratic form, with constants well below one, known in
advance, for all pairs of points in the source's support. A fresh-context audit of
the sketch (ledger VI-22) found that for a Gaussian source (c) forces a globally
bi-Lipschitz consumer, so the sketch speaks only near linearity: a leaky ReLU of slope
a already pays p·log₂(1/a) bits per symbol of looseness. A softmax fails (c) outright.
Consumers the ledger already instruments, with what is known against those three
conditions (to be checked, not assumed):

| Candidate | Existing instrument | (a) per symbol | (b) full rank | (c) near-quadratic |
|---|---|---|---|---|
| attention heads of a trained language model, keys as symbols | GO-P-2026-027 (Llama-3.2-3B read operators) | the softmax reads across tokens and fails (c); the scores before it, for a fixed set of queries, are a per-key linear consumer | full rank iff the queries span the key space (to be measured) | the scores: ν = 0 exactly; the softmax: fails |
| MUSIC direction-of-arrival on radar snapshots | DOA rows 031/033/034 | to be checked | to be measured | to be measured |
| a citation-ranking consumer | legal rows 035/036/039 | to be checked | to be measured | to be measured |
| a linear read-out with a known output metric | none (a control) | yes | by construction | ν = 0 exactly |

A linear consumer is the positive control: (A1) holds with ν = 0, so the prediction
is exact up to the coding theorems' finite-blocklength effects. **OWNER:** choose the
primary consumer, and whether to run the linear control first.

## The holder — OWNER

The RLD series charges leakage to a holder with a stated observation model. A real
consumer comes with no holder, so the run must declare one: for instance a noisy
linear observation S = H T + U of the source symbols, with H and the noise level
fixed at sealing. **OWNER:** the holder model, or the decision to run the rate-only
slice (α = 1) first, where the holder plays no part.

## Instance

```yaml
id: GO-P-2026-NNN            # assigned at sealing
date: YYYY-MM-DD             # must predate the first governed measurement
status: DRAFT                # set to "SEALED <date>" before seal.py, never after
instance:
  representation: OWNER       # the symbols T_t in R^p the consumer reads
  consumer: OWNER             # the functional C, its output metric G, and how its loss is measured
  holder: OWNER               # S = H T + U, or rate-only
  probe_distribution: OWNER   # pi; the sketch needs it inside the source's support
probe_output:
  read_operator: Q_hat = mean of J(x_i)^T G J(x_i) over m probe points
  nu_bounds: nu_minus, nu_plus -- the theorem needs them KNOWN IN ADVANCE (no finite probe
      set certifies them; e.g. from Lipschitz/monotonicity constants of the consumer, OWNER).
      The run also measures nu_hat on a held-out probe set, and reports both; whether
      nu_hat can stand in for the a-priori bounds in practice is itself a finding.
  queries: 2 p m by central differences; with output noise, two independent difference
      Jacobians per point and the symmetrized cross product (the plain estimator has a
      bias of order sigma^2/h^2 that does not shrink with m), or the consumer's own
      Jacobian if exposed (OWNER)
prediction:               # all bars OWNER, set at sealing
  H1_estimation: relative error of Q_hat against a high-sample reference Q_ref is at most
      the Lemma-1 bound eps_m = nu (sqrt(2L/m) + 2L/(3m)), nu = max(nu_minus, nu_plus),
      L = ln(2p/delta), at m in {OWNER}, in at least {OWNER} of {OWNER} seeds
  H2_loss: the code built for Q_hat at distortion D(1 - eps_m)/(1 + nu_plus) has measured
      downstream consumer loss at most D (+ a tolerance OWNER)
  H3_price: its rate (and, with a holder, its leakage) exceeds the frontier computed with
      Q_ref at distortion D/(1 - nu_minus) by at most
      tau = (p/2) log[(1+nu_plus)(1+eps_m)/((1-nu_minus)(1-eps_m))] bits per symbol; also
      report the gap to a code designed for Q_ref at the full budget D, since the
      looseness part of tau is an upper bound, not a price shown to be paid
  H4_benefit: at matched rate it beats the reconstruction-optimal code on consumer loss
      (the flip direction), with effect floor OWNER
  effect_floor: OWNER
  power: OWNER               # §5.1: how each gated bar was sized
  pilot: OWNER               # §5.1: a logged pilot, or "NO pilot was run"
design:
  m_probes: OWNER
  seeds: OWNER
  clusters: OWNER            # the independent unit
  stopping: fixed-n
  codes: Gaussian test-channel allocation (water-filling for Q_hat) and a practical
      quantizer realizing it at matched rate (OWNER: which); the RLD frontier is computed
      by the series' solver (`paper/tit-stationary/spectral_core.py`) for memoryless
      symbols, or its process version
  bits_matched_via: OWNER
controls: [linear-consumer (nu = 0), shuffled-consumer, noise-floor, reconstruction-optimal code]
amendments: []
hash: sha256:...             # written by scripts/seal.py
```

## What a miss would mean

- **H1 misses:** the matrix-Bernstein bound fails on this consumer, or ν̂ was
  mis-measured; the sketch's Lemma 1 hypotheses (bounded relative read metrics,
  independent probes) are then the first thing to check.
- **H1 holds, H2 or H3 misses:** (A1) is too strong an idealization for this consumer
  — most likely a loss that saturates or cross-symbol structure — and the size of the
  miss measures the gap the sketch's remarks name as open.
- **H4 misses with H1–H3 holding:** the consumer is nearly isotropic, so serving it
  buys little; that is a boundary of the flip, not of T1.

## Not in scope

The low-rank case (the read subspace of rank below p, priced through principal
angles, the commission tax, and the omission floor), consumers that read across
symbols, and any monitor or false-clear-rate claim. Probing cost is reported as a
count of queries and their compute; turning it into a per-symbol cost needs a serving
horizon K (**OWNER**).
