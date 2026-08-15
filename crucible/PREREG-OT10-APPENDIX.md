# OT-10 instrument appendix — sealed before the run

Constants for the numerical half of `OT10-THEOREM.md`. Committed
before `ot10_check.py` executes.

- d = 32; rank 1 (the proved case; rank-4 reported descriptively with
  gap = λ₁−λ₂ in the predictor, no bar). λ₁ = 1.0 fixed for the graded
  cells (removes spectrum-draw variance from the floor comparison).
- σ grid: {1e-4, 3e-4, 1e-3, 3e-3, 1e-2}; validity rule: a σ cell is
  graded only where the predicted floor σ²(d−1)/λ₁² ≤ 0.1 (all five
  qualify: max prediction 3.1e-3).
- 50 trials per (σ, k) cell; k ∈ {d−2, d−1, d}; seed 20260815.
- Noise: symmetric iid N(0, σ²) on the compressed block, fresh per
  trial.
- **N1 (floor):** at k = d, median measured sin²θ within a factor of
  **2** of σ²(d−1)/λ₁² in every graded σ cell.
- **N2 (scaling):** OLS slope of log median error vs log σ across the
  grid within **[1.8, 2.2]**.
- **N3 (location, inherited from OT-3):** at k < d, zero recoveries of
  a genuinely hidden component (hidden mass ≥ 1e-3, affinity ≥ 0.999)
  at every σ; and the cliff-edge contrast persists: median affinity at
  k = d minus at k = d−1 ≥ **0.5** at every graded σ.
- Verdict: N1 ∧ N2 ∧ N3, else FAIL. Result:
  `results/OT10-noisy-cliff.json`. Final instrument revision unless a
  manipulation-style defect (a cell numerically unmeasurable) voids a
  cell, in which case the cell is dropped with the reason printed —
  bars are never adjusted.
