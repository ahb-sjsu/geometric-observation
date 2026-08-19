# DRAFT — GO-P-2026-089 — Operational event triggering (OT-EC Campaign 4)

**STATUS: DRAFT — not sealed.** Registers the design and prediction structure of
Campaign 4 (`paper/ot-estimation-control.tex` §XI) before the harness exists.
Seals when the SEAL-TIME FIELDS are filled from a committed harness + internal
calibration; the sealed commit is the binding timestamp. No governed
measurement before the seal.

## The claim under test

An **operational trigger** — update when the uncertainty visible to the
consumer becomes excessive, `tr(P_C Σ_t) > τ` — beats time-based and
isotropic-covariance triggers on **downstream consumer performance at matched
realized update budgets**; and a trigger built from a **blindly recovered**
`P̂_C` (query-only, probe-charged) captures most of the true-operator
trigger's advantage. The analytic ancestor is the value-of-information
trigger line (Soleymani–Baras–Hirche, cited in the paper §V-C); for the
linear positive-control consumer the `tr(P_C Σ)` threshold *is* the analytic
task-weighted trigger, so matching it blind is the calibration proof.

## Setup

- **Plant/pool/consumers.** Machinery reused from GO-P-2026-087
  (`experiments/blind_scheduling.py`): random stable LTI `d = 12`, Kalman
  filter, arm P (linear rank-3, analytic weight known) and arm N (low-rank
  MLP / smoothed-threshold), common random numbers across trigger policies.
- **Update model.** At each step the trigger decides whether to spend an
  update: an update takes the same fixed number of greedy-selected
  measurements for every policy (selection held fixed across triggers — the
  *scheduling* question was Campaigns 2/3; here only the *when* varies).
  Budget = updates per rollout, matched at `B` (seal-time) by per-system
  threshold calibration on calibration noise bundles; governed rollouts use
  the frozen thresholds on held-out bundles.
- **Trigger policies.** `ot-true` (tr(P_C Σ) > τ_C); `ot-blind` (tr(P̂_C Σ) >
  τ̂, P̂_C recovered query-only as in 087, probe cost charged against the
  update budget at λ_p); `iso` (tr Σ > τ_iso); `periodic` (every ⌈T/B⌉
  steps); `shuffled` and `anti` controls (as 087).

## Sealed predictions (structure fixed now; floors at seal time)

- **T1 (the operational trigger wins).** At matched realized updates,
  `ot-true` beats BOTH `periodic` and `iso` on held-out consumer loss by at
  least `δ_T` (mean relative improvement, registered floor), in both arms.
- **T2 (blind positive control).** Probe-charged `ot-blind` captures at least
  `1 − ε_T` of `ot-true`'s pooled advantage over `periodic` (arm P; the
  recover/match discipline of 087 carried to triggering).
- **T3 (budget integrity gate).** Realized update counts of all verdict arms
  fall within a registered band of `B` (governed rollouts, frozen
  thresholds); a policy outside the band voids its own comparison rather
  than the run.
- **Controls.** `shuffled` degrades toward `iso`; `anti` is the worst
  informed trigger, pooled per arm.

## Falsification

T1 fails → consumer-weighted timing adds nothing over isotropic/time-based
triggering at matched budgets — §V-C's proposal is refuted in this setting
and reported at equal prominence. T2 fails while T1 passes → operational
triggering works only with privileged access to the consumer — the
"operationally unnecessary" boundary for recovery, in the triggering
interface. T3 fails → the threshold-calibration transfer is broken and no
comparison is claimed.

## SEAL-TIME FIELDS

```yaml
id: GO-P-2026-089
date: <seal date>
retrospective: false
kind: operational event triggering at matched update budgets, with blind
      recover/match positive control (Campaign 4, OT-EC paper)
code_hash: sha256:<harness>
governed_seed: <int>
frozen_config: {N_sys: <int>, B_updates: <int>, k_per_update: <int>,
                lambda_p: <float>, delta_T: <float>, eps_T: <float>,
                budget_band: <float>}
internal_calibration: {<cal numbers>}
stopping: fixed-n, single governed run
controls: [shuffled-toward-iso, anti-worst-pooled]
amendments: []
hash: sha256:<body with this line blanked>
```
