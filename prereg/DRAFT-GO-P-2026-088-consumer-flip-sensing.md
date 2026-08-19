# DRAFT — GO-P-2026-088 — The consumer-relative flip in sensing (OT-EC Campaign 2)

**STATUS: DRAFT — not sealed.** Registers the design and prediction structure of
Campaign 2 (`paper/ot-estimation-control.tex` §XI) before the harness exists.
Seals when the SEAL-TIME FIELDS are filled from a committed harness + internal
calibration; the sealed commit is the binding timestamp. No governed
measurement before the seal.

## The claim under test

The program's signature experiment, transferred from coding (Paper IV) to
**sensing**: two sensing policies with essentially identical reconstruction
uncertainty (`tr Σ` matched) but differently shaped uncertainty produce a
**two-consumer verdict inversion** — each consumer is better served by the
policy that shapes uncertainty away from its read directions — and the
composition `tr(P_C Σ̄)` predicts the ordering in every cell, while ordinary
state MSE cannot order the pair by construction. This is GO-2's flip with
sensor schedules in place of codes.

## Setup

- **Plant/pool.** As GO-P-2026-087 (`experiments/blind_scheduling.py` machinery
  reused verbatim): random stable LTI, `d = 12`, `M = 30` heterogeneous scalar
  sensors, `k` sensor-uses per step, Kalman filter, common random numbers
  across policies. No probing and no probe charge — this campaign uses
  **planted (known) consumers**; blind recovery was Campaign 3's question.
- **Two consumers per system.** Linear consumers `z_i = L_i x`, rank 3 each,
  with **mutually orthogonal row spaces** (drawn from disjoint blocks of a
  random orthonormal basis), so their read operators `P_i = L_iᵀL_i` claim
  disjoint state subspaces.
- **Policies.** `align-1` = greedy V_C on P_1; `align-2` = greedy V_C on P_2;
  `iso-trace`; `random`. All at identical sensor budgets.
- **Trace matching (the flip gate's entry condition).** A system enters the
  flip count only if `|tr Σ̄(align-1) − tr Σ̄(align-2)| / max(...) ≤ tol`
  (seal-time). Excluded systems are reported, never silently dropped.

## Sealed predictions (structure fixed now; floors at seal time)

- **F1 (the flip).** In at least `q_flip` of trace-matched systems, BOTH
  `loss_1(align-1) < loss_1(align-2)` AND `loss_2(align-2) < loss_2(align-1)`
  — the full two-consumer verdict inversion at matched reconstruction.
- **F2 (the composition predicts).** The sign of
  `tr(P_i Σ̄(align-1)) − tr(P_i Σ̄(align-2))` predicts consumer `i`'s loss
  ordering in at least `q_pred` of (system × consumer) cells.
- **F3 (magnitude).** Mean relative consumer-loss gap between aligned and
  anti-aligned policy ≥ `δ_flip` (registered floor, not just sign) while the
  trace gap stays inside the matching band.
- **Controls.** `iso-trace` never beats the aligned policy on its own
  consumer in more than a registered fraction of cells; `random` worst
  overall.

## Falsification

F1 fails → uncertainty *shape* at matched size does not carry a two-consumer
verdict inversion in sensing — the flip does not transfer from codes to
schedules, reported at equal prominence. F2 fails → `tr(P_C Σ)` does not
predict which schedule serves which consumer — the composition loses its
ordering claim in the dynamic setting.

## SEAL-TIME FIELDS

```yaml
id: GO-P-2026-088
date: <seal date>
retrospective: false
kind: two-consumer verdict inversion between trace-matched sensor schedules
      (Campaign 2, OT-EC paper); planted consumers, no recovery
code_hash: sha256:<harness>
governed_seed: <int>
frozen_config: {N_sys: <int>, k_budget: <int>, trace_tol: <float>,
                q_flip: <float>, q_pred: <float>, delta_flip: <float>}
internal_calibration: {<cal numbers>}
stopping: fixed-n, single governed run
controls: [iso-not-better-than-aligned, random-worst]
amendments: []
hash: sha256:<body with this line blanked>
```
