# GO-P-2026-087 — Blind recovery → sensor scheduling (OT-EC Campaign 3, flagship)

**SEALED.** Design registered as DRAFT (commit `c4286da`, 2026-08-18) before any
harness existed; floors frozen below from five disclosed calibration pilots;
this sealed commit is the binding timestamp. The governed run executes ONCE
after this commit, on the governed seed below, and is reported regardless of
sign in `claims/LEDGER.md`.

## Claim under test

The conjunction left open by `paper/PRIOR-ART-SWEEP-estimation-control.md`:
a read operator recovered from a **black-box** consumer under **query access
only** and a declared observation distribution, composed with the Kalman
covariance as `tr(P̂_C Σ)`, prospectively selects sensors that improve the
**held-out actual consumer** at **matched sensor-use budgets with probe cost
charged** — matching the known analytic optimum where one exists (positive
control) and beating consumer-agnostic policies where none does.

## Design (as registered in the DRAFT; unchanged)

Two consumer arms (P: analytic rank-3 linear, oracle weight known exactly;
N: frozen low-rank tanh MLP alternating with a smoothed-threshold scalar
consumer). Query-only central-difference recovery under the filter's
steady-state prior (declared, not tuned). Policies: ot-blind (charged),
ot-blind-uncharged (P4 sensitivity row, no verdict weight), oracle,
iso-trace, logdet, random, anti (charged), shuffled-consumer control.
Common random numbers across all policies. Probe charge = λ_p per query,
taken as single sensor-uses removed at evenly spread steps.

## Five disclosed calibration pilots (design fixes only; no sealed bar existed)

1. **Pilot 1** (P1 0.599): probe charge implemented as blacked-out *steps*
   landing on the transient; initial state drawn N(0,I) against a
   steady-prior belief. Both identified as design artifacts.
2. **Pilot 2** (P1 0.779): x₀ drawn from the prior; charged skips spread
   evenly; anti-control gate corrected from per-system-all-comers to pooled
   per-arm (the registered intent).
3. **Pilot 3** (P1 0.316 pooled): adding the P4 row perturbed the shared RNG
   stream — exposed that cross-policy gains were noise-dominated. Metric
   changed to pooled ratio (sum-of-gains); root cause still unfixed.
4. **Pilot 4** (P1 0.681): common random numbers introduced — all policies
   replay identical noise. Decomposition now exact: for arm P, recovery is
   exact (P̂ ≡ LᵀL), so the whole P1 shortfall was the charge implementation.
5. **Pilot 5** (P1 0.874, P2 0.265, P3 0.773/22, P4 +0.0068, controls pass):
   charge corrected from blacked-out steps to single sensor-uses removed at
   spread steps (1.9 uses of 180 now costs proportionately). Design frozen.

No pilot loosened a sealed bar (none existed); floors below are set FROM the
pilot-5 design's calibration observations, conservatively, and are fixed by
this seal.

```yaml
id: GO-P-2026-087
date: 2026-08-18
retrospective: false
kind: blind query-only recovery -> sensor scheduling -> held-out consumer,
      with analytic positive-control arm (Campaign 3 flagship, OT-EC paper)
harness: experiments/blind_scheduling.py
code_hash: sha256:c71f47a82d6ba613763fad9f01ad6a6386414c731e666f66179945e79bf76b08
governed_seed: 20260819
calibration_seed: 20260818          # pilots only; governed systems are fresh draws
frozen_config:
  D: 12
  M_POOL: 30
  K_BUDGET: 3
  T_STEPS: 60
  N_TEST: 24
  N_SYS_GOV: 20
  N_PROBE: 40
  LAMBDA_P: 0.002
  eps_match: 0.25        # P1 gate: pooled match fraction >= 0.75 (cal 0.874)
  delta_N: 0.08          # P2 gate: mean rel. improvement >= 0.08 (cal 0.166-0.265)
  trSigma_tol: 0.05      # P3 matching band
  q_ordering: 0.65       # P3 gate (cal 0.773-0.923 on 11-22 pairs, prop SE ~0.09)
internal_calibration:
  pilot5: {P1: 0.874, P2: 0.265, P3: 0.773, P3_pairs: 22, P4_charge: 0.0068,
           shuffled_gap: 0.067, anti_worst_pooled: true}
sealed_predictions:
  P1: pooled fraction of the oracle-over-iso gain captured by charged ot-blind,
      arm P, >= 0.75  (the recover/match positive control)
  P2: mean relative improvement of charged ot-blind over the best
      consumer-agnostic policy, arm N, >= 0.08  (the win where no analytic
      weight exists)
  P3: trace-matched pair ordering carried by tr(P_hat Sigma) >= 0.65
  P4: sensitivity row only (charged minus uncharged), no verdict weight
controls: [shuffled-consumer >= -0.02 vs iso, anti worst pooled per arm]
stopping: fixed-n, single governed run
falsification: P1 fail -> recovery claim NOT confirmed (Interface-2 narrows to
  analytic consumers). P2 fail with P1 pass -> recovery works but adds nothing
  beyond analytic machinery ("operationally unnecessary" falsifier). P3 fail ->
  the composition does not carry the claimed ordering information. All
  outcomes reported at equal prominence.
amendments: []
hash: sha256:62ca73ed4d8af4528f5dacf05c4eb7747e9170f1f4f4e0286a50dc8abbb1a736
```

## Scope and non-claims

- Greedy `V_C` selection carries **no optimality claim** (Jawaid–Smith
  non-supermodularity acknowledged; "conditions for OT-greedy guarantees" is a
  separate campaign-theorem target).
- Arm N's "oracle" is a lavish uncharged probe (8× budget), an upper
  *reference*, not an analytic optimum — none exists, which is the point.
- Synthetic consumers only; the physical-endpoint version is Campaign 5 and
  gets its own ID. Staleness (Interface 3) likewise.
- Per CHARTER R-IND: harness gates are conclusion-grade; any `[proved]`
  language additionally requires the fresh-context derivation pass.
