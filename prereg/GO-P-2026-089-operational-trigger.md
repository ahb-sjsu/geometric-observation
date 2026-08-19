# GO-P-2026-089 — Operational event triggering (OT-EC Campaign 4)

**SEALED.** Design registered as DRAFT (commit `a7f5838`, 2026-08-19) before the
harness existed; floors frozen below from three disclosed calibration pilots;
this sealed commit is the binding timestamp. The governed run executes ONCE
after this commit, on the governed seed below, and is reported regardless of
sign in `claims/LEDGER.md`.

## Claim under test

An **operational trigger** — transmit when the consumer-visible realized
error is excessive — beats time-based and isotropic triggers on downstream
consumer performance at matched realized transmission budgets; and a trigger
built from a blindly recovered `P̂_C` (query-only, probe-charged) captures
most of the true-operator trigger's advantage (the 087 recover/match
discipline carried to timing). Analytic ancestor: the value-of-information
trigger line (Soleymani–Baras–Hirche), cited in the paper §V-C.

## Design (smart-sensor remote estimation; three pilot fixes disclosed)

A sensor node sees the state; the remote estimator the consumer reads coasts
on `x̂ = A x̂` between transmissions and receives the exact state on
transmission. Signal-aware trigger: fire when `eᵀ W e > τ` for the realized
gap `e = x − x̂`, with `W` ∈ {true `P_C`; probed `P̂_C` (charged); `I`;
shuffled; anti}, all unit-trace normalized; `periodic` = evenly spaced.
Thresholds calibrated per (system, policy) on CALIBRATION noise bundles to
hit the matched mean budget, frozen, then evaluated on held-out bundles with
common random numbers across policies. Probe recovery exactly as GO-087;
probe cost charged in transmission-equivalents
(`ceil(λ_p·n_queries / K_PER_UPDATE)` deducted from the arm's budget).

**Three disclosed calibration pilots (design fixes only; no sealed bar existed):**
1. **Pilot 1 — the covariance-null (a finding, not just a bug).** With
   covariance-only (signal-agnostic) statistics `tr(P Σ)` vs `tr Σ`, every
   threshold trigger collapses to a quasi-periodic schedule: T1 ≈ −0.01/−0.03,
   T2 degenerate (zero denominator). Direction only matters to WHEN if the
   trigger sees the realized error — consistent with the VoI literature's
   signal-aware designs, and worth stating in the paper: **the operational
   trigger must be belief- or signal-aware; covariance thresholds are
   direction-blind in effect.** Also deviated from the registered
   noise-bundle threshold calibration; the redesign returns to it.
2. **Pilot 2** — signal-aware redesign timed out: `steady_prior` (a 400-step
   recursion) was recomputed inside every rollout. Precomputed per system;
   fires-only fast path added for bisection.
3. **Pilot 3** (T1 armP 0.259 / armN 0.348, T2 0.876, T3 pass, shuffled
   +0.069, anti worst pooled): design frozen. δ_T raised from the 0.05 draft
   to 0.10 (tightened, never loosened).

```yaml
id: GO-P-2026-089
date: 2026-08-19
retrospective: false
kind: signal-aware operational event triggering at matched transmission
      budgets, with blind recover/match positive control (Campaign 4, OT-EC)
harness: experiments/operational_trigger.py
code_hash: sha256:004192a6b10285aa5f1a995420fad2a2dd9f2dab43cbe1020ee8d3e093c590ec
governed_seed: 20260822
calibration_seed: 20260820
frozen_config:
  N_sys: 20
  B_updates: 15
  K_per_update: 3
  lambda_p: 0.002
  delta_T: 0.10       # T1 gate, both arms (cal 0.259 / 0.348; raised from draft 0.05)
  eps_T: 0.25         # T2 gate: blind capture >= 0.75 (cal 0.876)
  budget_band: 0.10   # T3 integrity band on realized mean updates
internal_calibration:
  pilot3: {T1_armP: 0.259, T1_armN: 0.348, T2: 0.876, T3: true,
           shuffled_gap: 0.069, anti_worst_pooled: true}
sealed_predictions:
  T1: ot-true beats best of {periodic, iso} by >= 0.10 mean relative
      improvement, in BOTH arms, at matched realized budgets
  T2: probe-charged ot-blind captures >= 0.75 of ot-true's pooled advantage
      over periodic (arm P)
  T3: verdict arms' realized mean updates within +-10% of their targets
controls: [shuffled-vs-iso gap >= -0.02, anti worst pooled per arm]
stopping: fixed-n, single governed run
falsification: T1 fail -> consumer-weighted timing adds nothing at matched
  budgets; §V-C refuted in this setting. T2 fail with T1 pass -> operational
  triggering needs privileged consumer access ("operationally unnecessary"
  boundary for recovery, in the timing interface). T3 fail -> threshold
  transfer broken; no comparison claimed. All reported at equal prominence.
amendments: []
hash: sha256:18d295b1d10d45b60eaad92a2ce2b47fbd8dbe5b76bf5d74b0c7952498b01293
```

## Scope and non-claims

Exact-state transmission (smart-sensor idealization); noisy links, packet
loss, and the S_C(Δ) staleness quantity (Interface 3) are out of scope, each
with its own future ID. No optimality claim for the threshold form — the
analytic-LQG optimal trigger is the VoI line's result, not ours; matching it
blind is the point.
