# OT-2 instrument appendix — sealed before the run

**Claim frozen in `OT-CRUCIBLE.md` §OT-2: loading is a covariance, not a
distance — `dP_C/dε|₀ = E_D[h·A]`. This appendix fixes the experiment.
Committed before `ot2_check.py` executes.**

## Design: alignment varies, scalar loading cannot

- Base distribution `D_a = N(0, I_d)`, d = 32.
- Consumer (two features, so the operator is genuinely matrix-valued
  and the law is tested beyond rank-1):
  `C(x) = tanh(a₁ᵀx − 1) + tanh(a₂ᵀx + 0.5)`, with `a₁, a₂` random
  orthonormal (seeded); offsets break the odd symmetry that would kill
  the first-order term. `A(x) = ∇C ∇Cᵀ` exactly (analytic gradient —
  the law under test is at operator level; blindness is OT-1's job).
- Shift family (mean shifts, all with **identical scalar loading**):
  `D_α = N(ε·u(α), I)`, `u(α) = cos α · a₁ + sin α · b`, `b ⊥
  span(a₁,a₂)`, α ∈ {0°, 15°, 30°, 45°, 60°, 75°, 90°}, ε = 0.05.
  Every member has the same `‖Δμ‖ = ε` and the same KL to `D_a` — any
  scalar distributional distance is constant across the family by
  construction.
- Measured reading error: `e(α) = ‖E_{D_α}[A] − E_{D_a}[A]‖_F` by
  common-random-numbers Monte Carlo (same base normals, shifted),
  n = 400,000, seed 20260815.
- Law's prediction (computed under the BASE measure only — this is the
  point): `p(α) = ε · ‖E_{D_a}[(u(α)ᵀx) · A(x)]‖_F` (the score of a
  Gaussian mean shift is `h(x) = uᵀx` to first order).
- Descriptive extra (no bar): one covariance shift
  `Σ = I + ε(vvᵀ)` with `v = a₁` vs `v = b`, reported.

## Bars

- **B1 (the law, shape):** max over the α grid of
  `| e(α)/e(0) − p(α)/p(0) |` ≤ **0.08** (second-order contamination at
  ε = 0.05 budgeted).
- **B2 (orthogonal shift does ~nothing):** `e(90°)/e(0°)` ≤ **0.10** —
  a shift of full scalar magnitude, functionally orthogonal to the
  operator's variation, must produce ≤ a tenth of the aligned error.
- **B3 (the kill test, as frozen):** Spearman correlation of `e` with
  `p` over the grid ≥ **0.95**, AND `max e / min e ≥ 5` — the scalar
  loading is constant across the family, so it explains none of a
  ≥ 5× variation; the alignment functional must explain effectively
  all of the ordering. This operationalizes "predicts no better than
  scalar shift magnitude" fairly: the scalar gets every chance and has
  nothing to say.
- **B4 (first-order convergence):** `|e(0) − p(0)| / e(0)` ≤ **0.10**
  at ε = 0.05, and re-running at ε = 0.025 multiplies this relative
  error by ≤ **0.7** (first-order laws converge linearly; 0.5 expected,
  0.7 allows MC noise).

Verdict: B1 ∧ B2 ∧ B3 ∧ B4, else FAIL. Result:
`results/OT2-loading-law.json`; ledger row OT-2.
