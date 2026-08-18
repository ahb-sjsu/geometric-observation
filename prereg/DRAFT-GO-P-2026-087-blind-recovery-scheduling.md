# DRAFT — GO-P-2026-087 — Blind recovery → sensor scheduling (OT-EC Campaign 3, flagship)

**STATUS: DRAFT — not sealed.** This file registers the *design and prediction
structure* of the estimation-and-control flagship experiment
(`paper/ot-estimation-control.tex` §XI, Campaign 3) before any harness code
exists. It becomes a sealed prereg only when the SEAL-TIME FIELDS below are
filled from a committed harness + internal calibration split and the file is
re-committed with its hash. **No governed measurement may run before that
seal.** The git commit of the sealed version is the binding timestamp.

## The claim under test

The conjunction left open by the prior-art sweep
(`paper/PRIOR-ART-SWEEP-estimation-control.md`): a read operator recovered
from a **black-box** consumer under **query access only** and a declared
observation distribution, composed with the Kalman covariance as
`tr(P̂_C Σ)`, prospectively selects sensors that improve the **held-out
actual consumer** at **matched budgets that include probe cost** — matching
the known analytic optimum where one exists (positive control) and beating
consumer-agnostic policies where none does.

## Setup

- **Plant.** Randomly generated stable LTI systems, state dim `d = 12`,
  process noise `Q ≻ 0`; `N_sys` independent draws (seal-time), governed seed.
  Kalman filter as the estimator throughout; no estimator modification in any
  arm (Prop. 1 boundary respected — this is a *scheduling* experiment).
- **Sensor pool.** `M = 30` candidate scalar sensors per system, heterogeneous
  directions `h_i` (random unit vectors, condition-spread) and noise floors
  `r_i` log-uniform over 2 decades; per-use cost `c_i`. Budget: `k` sensor-uses
  per step (seal-time), identical across arms. **Probe queries are charged to
  the same budget line** at a declared exchange rate `λ_p` (seal-time), per
  the policy objective of the paper §V-A.
- **Consumers (two arms).**
  - **Arm P (positive control, analytic).** LQG consumer: quadratic cost with
    known `Q_lqr` of rank 3. The optimal scheduling weight is the
    Riccati-derived analytic weight (LQG co-design / VoI line — cited in the
    paper). Recovery is run *as if black-box* (queries only).
  - **Arm N (non-analytic).** A planted black-box consumer with no analytic
    weight: a frozen randomly-initialized-then-trained 2-layer MLP
    `C: R^12 → R^2` scored by CE against its own clean-state output
    (low-rank by construction, rank ≤ 4 planted via bottleneck), plus a
    smoothed-threshold variant (sigmoid link with steepness at the
    §VI belief-averaging regime boundary). Consumer internals never exposed
    to the scheduler.
- **Recovery (query-only).** Finite-difference probing of consumer output
  under the declared observation distribution `x ~ N(x_op, Σ_probe)` with
  `Σ_probe` = the filter's steady-state prior covariance (declared, not
  tuned); assemble `P̂_C` as the probe-average of `Ĵᵀ G Ĵ` (Arm N smoothed
  variant uses the finite-perturbation operational metric, never a pretended
  Hessian). Probe budget `n_probe` fixed at seal time from the calibration
  split; **no re-probing during the governed run**.
- **Scheduling policies (all arms, matched budget incl. probe charge).**
  1. `OT-blind` — greedy on `V_C = tr(P̂_C ΔΣ)` (greedy caveat: no
     supermodularity guarantee claimed; this experiment tests usefulness, not
     optimality);
  2. `oracle-weight` — greedy on the true weight (analytic Riccati weight in
     Arm P; true planted `P_C` in Arm N) — upper-reference, pays no probe cost;
  3. `iso-trace` — greedy on `tr(ΔΣ)` (consumer-agnostic MSE);
  4. `logdet` — greedy mutual-information;
  5. `random` — uniform over the pool.
- **Endpoint.** Downstream consumer loss on `n_test` held-out rollouts
  (fresh noise seeds, same systems), reported per system and pooled with
  clustered CIs (cluster = system draw).

## Sealed predictions (structure fixed now; floors at seal time)

- **P1 (positive control — recover/match, not beat).** In Arm P, `OT-blind`
  achieves at least `(1 − ε_match)` of the `oracle-weight` policy's downstream
  improvement over `iso-trace`, with probe cost charged. `ε_match` frozen at
  seal time from the internal calibration split (draft target: ε_match ≤ 0.15).
  *This is the calibration proof: the blind pipeline must rediscover the known
  optimum. Failing P1 kills the method regardless of Arm N.*
- **P2 (the flip — win where no analytic weight exists).** In Arm N,
  `OT-blind` beats both `iso-trace` and `logdet` on held-out consumer loss at
  matched total budget by at least the registered effect floor `δ_N`
  (seal-time, from calibration; sign alone insufficient).
- **P3 (reconstruction-matched dissociation).** Among policy pairs whose final
  `tr Σ` agree within a tolerance band (seal-time), the ordering of held-out
  consumer loss is predicted by `tr(P̂_C Σ)` in at least `q%` of pairs
  (seal-time; draft target 80%). Ordinary MSE cannot order these pairs by
  construction.
- **P4 (probe accounting).** P1 and P2 verdicts are computed **with probe cost
  charged**; an additional uncharged sensitivity row is reported but carries
  no verdict weight.

## Controls (must-fail / must-null)

- `shuffled-consumer`: `P̂_C` recovered from a permuted-input consumer →
  OT-blind must degrade to ≈ iso-trace (no free lunch from machinery).
- `noise-floor`: probe budget → 0 → recovery must degrade gracefully toward
  iso-trace, not fail catastrophically (belief-averaged smoothing check).
- `anti-consumer`: schedule on the eigen-complement of `P̂_C` → must be the
  worst non-random arm (direction, not just magnitude, is load-bearing).

## Falsification

Any of: P1 fails (blind pipeline cannot match a known optimum) → the recovery
claim is NOT confirmed and the program's Interface-2 case narrows to analytic
consumers, reported at equal prominence. P2 fails while P1 passes → recovery
works but adds nothing beyond analytic machinery where it exists — the
"operationally unnecessary" falsifier of the paper §XII. P3 fails → the
composition `tr(P_C Σ)` does not carry the ordering information claimed for
it. All outcomes recorded in `claims/LEDGER.md` regardless of sign.

## SEAL-TIME FIELDS (to be filled from a committed harness before sealing)

```yaml
id: GO-P-2026-087
date: <seal date — must predate first governed measurement>
retrospective: false
kind: blind query-only recovery -> sensor scheduling -> held-out consumer,
      with analytic positive-control arm (Campaign 3 flagship, OT-EC paper)
code_hash: sha256:<harness>
governed_seed: <int>
frozen_config:
  N_sys: <int>          # draft target: 20
  k_budget: <int>       # sensor-uses per step
  n_probe: <int>        # probe queries, charged at lambda_p
  lambda_p: <float>     # probe/sensing exchange rate
  eps_match: <float>    # P1 floor, from calibration split
  delta_N: <float>      # P2 effect floor, from calibration split
  trSigma_tol: <float>  # P3 matching band
  q_ordering: <float>   # P3 ordering fraction
internal_calibration: {<cal-split numbers, committed before seal>}
stopping: fixed-n
controls: [shuffled-consumer, noise-floor, anti-consumer]
amendments: []
hash: sha256:<body with this line blanked>
```

## Notes

- Registered separately from any staleness (Interface-3) experiment; S_C(Δ)
  work gets its own ID.
- The greedy-guarantee campaign theorem (paper §V-B) is *not* tested here and
  no optimality is claimed for greedy `V_C`.
- Per CHARTER R-IND: the harness verdict gates are conclusion-grade; any
  analytic claims folded into the paper from this experiment additionally
  need the fresh-context derivation pass before `[proved]` language.
