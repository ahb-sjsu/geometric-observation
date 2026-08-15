# OT-3 instrument appendix — sealed before the run

**Committed before `ot3_check.py` executes. Tests T2's cliff prediction
(`OT3-THEOREM.md`): k_crit = d − k₀ exactly, a cliff at every k₀, no
smooth improvement from side information.**

## Cells

- d = 32; ranks r ∈ {1, 4}; spectrum log-uniform [0.1, 1] descending.
- Side information k₀ ∈ {0, 8, 16}: promise subspace `W` of dim
  m = d − k₀, `range(P) ⊆ W` by construction, `W` known to the
  estimator.
- Probe: oblivious — V = first k columns of a uniformly random
  orthonormal basis of `W`; transcript = the full k×k block `VᵀPV`.
- Estimator: embed the block (`V M Vᵀ`), top-r eigenspace `Û_r`.
- k sweep: m−6 … m for each cell.
- 50 trials per (r, k₀, k); seed 20260815.
- Metric: subspace affinity `a = ‖U_rᵀÛ_r‖_F² / r` (r = 1: squared
  overlap). Exact recovery: `a ≥ 0.999`.

## Bars (all sealed)

- **B-cliff-top:** at k = m: exact-recovery share = **1.00** (50/50)
  in every cell.
- **B-cliff-bottom:** at k = m−1: exact-recovery share = **0.00**
  (0/50) in every cell — one missing direction forbids exact recovery.
- **B-no-smoothing (the kill test):** at fixed k below the cliff, the
  exact-recovery share is 0.00 for **every** k₀ — partial side
  information may shift the cliff (it does, by construction of m) but
  must never buy exact recovery early: grade at k = m−1 and k = m−3
  across all k₀.
- **B-ramp (below-cliff mass bound):** for k ≤ m−1, median affinity
  ≤ k/m + 0.10 — the projected estimator's affinity is confinement
  mass, not identification; a median above the bound would mean the
  estimator extracts orientation information the theorem says is not in
  the transcript, killing the model (and the theorem's relevance).
- Verdict: all four bars in all cells, else FAIL. Result JSON:
  `results/OT3-cliff.json`; ledger row OT-3 (theorem + numerics).

## What would kill what

- A single exact recovery below k = d − k₀ → the confinement model is
  wrong about the instrument → OT-3 FAIL (and OT3-THEOREM's relevance,
  not its algebra, collapses).
- Smooth improvement with k₀ at fixed sub-cliff k → the sealed
  formulation of P3's side-information prediction dies (the Crucible's
  named kill condition).
- Ramp median exceeding confinement mass → transcript leaks
  orientation → model mis-specified.
