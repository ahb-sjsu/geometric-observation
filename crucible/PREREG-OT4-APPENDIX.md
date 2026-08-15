# OT-4 instrument appendix — sealed before the run

**OT-4 adopts readscope's `DECLARATION-C12.md` (stages, bars, seeds,
fixed configuration) with one recorded amendment, plus the two sealed
additions the Crucible claim requires (onset prediction, refresh
statement). Committed before the amended run starts.**

## Amendment 1 (co-author signed, 2026-08-15): CODEBOOK nf4a → nf4

The declared config's phenomenon does not exist: re-validation at n=40
with LongBench's own metrics (`/archive/c12/reval/MATRIX.txt`,
2026-08-08) measured the gov_report/qwen/512 **nf4a** gap at **−0.31**
against the recorded 13.70 — A0-void — while the **symmetric nf4**
codebook reproduces a **26.64**-point gap. The amendment re-targets the
identical stages at the codebook where the phenomenon demonstrably
lives. Everything else in the declaration is unchanged (N_DOCS 40,
layers {4,14,24}, MAXGEN 512, windows, seeds, bars A0/A1/B1/B2/D1).
Side finding, filed separately: turboquant-pro's recorded nf4a
long-generation curve is irreproducible as labeled — an errata-grade
issue for that repo independent of OT-4.

Mechanism note, recorded before data: a symmetric codebook on
asymmetric key distributions injects a *biased* error (nonzero mean),
so the P2 channel (structured shift through the read operator) may
carry damage alongside or instead of P4 drift. Teacher forcing, the
rotation null, and Stage D apportion this; OT-4's claim stays as
frozen and can die on it.

## Sealed addition 1 — the onset prediction t*

Derived from C-11c's short-sequence drift measurements
(`c11c-operator-drift.json`, 16 cells, Llama-3.2-3B — a cross-model
extrapolation, stated as such):

- staleness inflation rate γ = median misprice gap / window separation
  = 2.2518 / 144 ≈ **0.0156 per token**;
- predicted doubling point of teacher-forced excess degradation:
  Δt ≈ 1/γ ≈ **64 tokens** past the early window;
- **sealed band (bar T\*):** the measured doubling point — first t
  where the across-doc median of the harness's windowed `d_tf_curve`
  reaches 2× its first-window median, by linear interpolation — falls
  in **[32, 192] tokens**. Outside the band, T\* fails.

## Sealed addition 2 — the refresh statement R

At γ ≈ 0.0156/token, holding staleness inflation under 10% would need
refresh every ~6 tokens — impractical, and recorded here as the design
implication. The *testable* intervention is the declaration's Stage D:
one union-operator allocation (prefill + decode queries) at matched
total bits — the coarsest refresh — with **D1 as sealed: median
late-window D_tf falls ≥ 10%** versus the early-operator allocation.

**Stage D implementation spec (not yet coded; to be committed before
Stage D runs, gated on A0∧A1∧B1):** per (layer, kv-head), rotate
settled prefill keys into the operator eigenbasis, allocate a fixed
total bit budget across directions by reverse water-filling against
the operator spectrum (readscope `allocate.py`), quantize per
direction, rotate back; arm E uses the early-window operator, arm U
the union operator, identical budgets by construction; teacher-forced
re-scoring of both.

## OT-4 verdict mapping (sealed)

**PASS iff A0 ∧ A1 ∧ B1 ∧ T\* ∧ D1.** B2 and Stage C are reported
(B2 pre-flagged underpowered by the declaration). A0 failing under the
amendment voids rather than fails OT-4 — but it is pre-verified at
n=40 by the reval matrix, so a void here would itself be a finding.
Execution: Atlas GPU 1, `~/env` venv, harness from
`~/turboquant-pro/benchmarks/kvquant_matrix`, OUTDIR
`/archive/c12/out-sym`, CODEBOOK=nf4 via environment (one-line
passthrough patch to the c12 script, committed).
