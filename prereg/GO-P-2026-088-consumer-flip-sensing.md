# GO-P-2026-088 — The consumer-relative flip in sensing (OT-EC Campaign 2)

**SEALED.** Design registered as DRAFT (commit `a7f5838`, 2026-08-19) before the
harness existed; floors frozen below from two disclosed calibration pilots;
this sealed commit is the binding timestamp. The governed run executes ONCE
after this commit, on the governed seed below, and is reported regardless of
sign in `claims/LEDGER.md`.

## Claim under test

The program's signature experiment transferred from codes to **sensor
schedules**: two schedules with matched time-average reconstruction
uncertainty but differently shaped covariance produce the full two-consumer
verdict inversion; `tr(P_i Σ̄)` predicts the ordering; ordinary state MSE
cannot order the pair by construction.

## Design (as registered; two pilot fixes disclosed)

Machinery reused from the sealed `blind_scheduling.py` (unmodified). Two
planted rank-3 linear consumers per system on mutually orthogonal row spaces;
policies `align-1`, `align-2` (greedy V_C on each consumer's read operator),
`iso-trace`, `random`, common random numbers, identical budgets, no probing.
Trace-matching entry band on `tr Σ̄`; excluded systems reported.

**Two disclosed calibration pilots (design fixes only; no sealed bar existed):**
1. **Pilot 1** (F1 1.000, F2 1.000, F3 0.303, but 4/8 matched and
   random-worst False): (a) only half the systems land in the 0.10 matching
   band → added the `I_min_matched` integrity gate rather than widening the
   band; (b) the random-worst control was mis-specified per-cell — an
   anti-aligned policy legitimately serves the *other* consumer worse than
   broad random sensing, so "random worst in every cell" was never the right
   prediction; corrected to pooled random-vs-own-aligned per consumer.
2. **Pilot 2** (F1 1.000, F2 1.000, F3 0.303, iso 0.125, random-worst True):
   corrected design confirmed; frozen.

```yaml
id: GO-P-2026-088
date: 2026-08-19
retrospective: false
kind: two-consumer verdict inversion between trace-matched sensor schedules
      (Campaign 2, OT-EC paper); planted consumers, no recovery
harness: experiments/consumer_flip_sensing.py
code_hash: sha256:92143271659b47933529833da9415290192aa86f3beef608ce371cc66bd9c831
governed_seed: 20260821
calibration_seed: 20260819
frozen_config:
  N_sys: 20
  trace_tol: 0.10
  q_flip: 0.80        # F1 gate (cal 1.000 on 4 matched)
  q_pred: 0.85        # F2 gate (cal 1.000)
  delta_flip: 0.10    # F3 gate (cal 0.303)
  min_matched: 6      # integrity gate on matched-system count
  iso_frac: 0.25      # control ceiling (cal 0.125)
internal_calibration:
  pilot2: {F1: 1.000, F2: 1.000, F3: 0.303, iso_frac: 0.125,
           random_worst: true, matched: 4, of: 8}
sealed_predictions:
  F1: full two-consumer inversion in >= 80% of trace-matched systems
  F2: tr(P_i Sigma_bar) sign predicts the loss ordering in >= 85% of cells
  F3: mean relative consumer-loss gap >= 0.10 inside the matching band
controls: [iso-beats-aligned <= 0.25 of cells, random worse than own-aligned pooled]
stopping: fixed-n, single governed run
falsification: F1 fail -> the flip does not transfer from codes to schedules.
  F2 fail -> the composition loses its ordering claim in the dynamic setting.
  I_min_matched fail -> the matching construction itself failed; no flip claim
  is made either way. All outcomes reported at equal prominence.
amendments:
  - date: 2026-08-19
    what: "Governed invocation 1 (seed 20260821, sealed code_hash 92143271...)
      completed its full measurement and CRASHED in json.dump: the
      random-worst control produced a numpy bool_ (not JSON serializable).
      The complete stdout/stderr are committed as
      results/GO88-governed-invocation1-{stdout,stderr}.log — F1 1.000,
      F2 1.000, F3 0.318, iso_frac 0.250, matched 6/20, random_worst True.
      Fix is a serializer-only bool() cast (no bar, seed, or measurement
      logic touched); new code_hash sha256:c80c0644a66bf2ae459e2c6832307d0a462bcf48a536ba66c6fa5b229c0e62e9.
      The run is deterministic given the seed, so invocation 2 must
      REPRODUCE the invocation-1 printed metrics exactly; any deviation
      voids the run. Original sealed body hash:
      sha256:78e8a8e03d0b5cb1522468b6ba790eac617d4b1284a60f3d6ab2a8c3e4dac70c."
hash: sha256:150fb2807efbdb2f1c2347639a78c82e323fd9025abc9ce0fa84ee008f2affcd
```

## Scope and non-claims

Planted linear consumers only (the recovery question is 087's; the physical
endpoint is Campaign 5). Greedy V_C carries no optimality claim. Orthogonal
read subspaces are the *clean* case; overlapping-consumer geometry is
Campaign 6's question.
