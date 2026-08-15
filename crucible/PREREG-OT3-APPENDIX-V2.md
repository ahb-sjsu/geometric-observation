# OT-3 instrument appendix v2 — sealed before the v2 run; final revision

**Supersedes v1 after its as-executed FAIL (`results/OT3-cliff.json`,
committed unchanged). Diagnosis: v1's cliff-bottom bar graded raw
exact-recovery share as 0.00 at k = m−1, but a Haar-random rank-1
target lands within affinity 0.999 of the probed span with analytic
probability p_chance(m) = 2√(1−0.999) · Γ(m/2)/(√π Γ((m−1)/2)) —
0.143 / 0.123 / 0.101 for m = 32/24/16 — and the observed shares
(0.12 / 0.10 / 0.04, n = 50) are exactly that. Those trials recover a
target that was never hidden; the theorem forbids extracting *hidden*
components, not being lucky. Rank-4 requires four simultaneous
alignments and showed 0.00 everywhere, as the same analysis predicts.**

## v2 bars (constants unchanged from v1: d=32, ranks {1,4},
## k0 ∈ {0,8,16}, 50 trials, seed 20260815, exact = affinity ≥ 0.999)

Per trial, record `hidden = 1 − ‖VᵀU_r‖_F²/r` (true leading-eigenspace
mass outside the probed span), and call a trial **genuinely hidden**
when `hidden ≥ 1e-3` (the complement of the exactness threshold).

- **B1 cliff-top (unchanged):** at k = m: exact share **1.00**, all cells.
- **B2 no-hidden-recovery (the theorem-faithful bar, replaces v1's
  cliff-bottom and no-smoothing):** for every k < m, every cell: share
  of trials that are simultaneously exact and genuinely hidden =
  **0.00**. This is the cliff and the no-smoothing kill test in one
  statement, at every sub-cliff k and every k₀.
- **B3 chance-rate (new — the diagnosis promoted to a prediction):** at
  k = m−1, r = 1: observed exact share within
  `p_chance(m) ± 3·√(p_chance(1−p_chance)/50)`. The confinement model
  *predicts* the lucky-recovery rate; if the estimator recovered more
  often than chance alignment allows, the transcript leaks orientation.
- **B4 ramp (unchanged):** for k ≤ m−1, median affinity ≤ k/m + 0.10.

Verdict: all four bars, all cells, else FAIL. Result:
`results/OT3-cliff-v2.json`. **Declared final instrument revision: a v2
FAIL closes OT-3's numerical half as FAIL for the campaign.**
