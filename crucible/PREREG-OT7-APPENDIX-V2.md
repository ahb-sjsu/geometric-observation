# OT-7 instrument appendix v2 — sealed before the v2 run

**Supersedes `PREREG-OT7-APPENDIX.md` after the as-executed v1 FAIL;
diagnosis in `OT7-NOTES.md`. Every change repairs the instrument at a
degenerate corner; the claims and taxonomy of `OT-CRUCIBLE.md` are
untouched. Committed before `ot7_check_v2.py` executes.**

Changes from v1, exhaustively:

1. **Degenerate-cell annotation.** A fragile-row quantity that is a
   class constant in a cell is annotated `degenerate`, not graded:
   r = 1 → eff_rank, energy_rank, waterfill; r = d → principal angles.
   Rationale: fragility is a claim about cells where the quantity can
   move; a constant of the rank class demonstrates nothing either way.
2. **Integer quantities** (energy_rank): GL deviation-share bar is
   ≥ **0.50** (chance coincidence of an integer under a generic
   transform is common at small d); continuous quantities keep 0.95.
3. **GL condition cap 1e4 → 1e2.** Sole purpose: the rank-detection
   threshold `s₀ · 1e-9 · d` then has ≥ 30× margin over the smallest
   true singular value at d = 32 (class floor λ_min = 1e-2, congruence
   amplification ≤ cond² = 1e4). No other constant changes.

All else identical to v1: d ∈ {8, 32}, r ∈ {1, 4, d}, 50 GL + 50 O(d)
per cell, exact rows ≤ 1e-9, O(d) invariance ≤ 1e-8, fragility floor
1e-6, water-fill budget 2d bits, loading identity on 20k shared
samples, seed 20260815. Result: `results/OT7-invariance-v2.json`.
Verdict rule unchanged: all graded rows pass in all cells, else FAIL.
