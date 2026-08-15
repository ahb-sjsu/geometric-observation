# OT-7 instrument appendix — sealed before the run

**Committed before `ot7_check.py` executes. Claims and the invariance
taxonomy are frozen in `OT-CRUCIBLE.md`; this fixes every constant.**

## Cells

- Dimensions d ∈ {8, 32}; ranks r ∈ {1, 4, d} per dimension.
- 50 random GL(d) transforms per cell (i.i.d. N(0,1) entries, rejected
  until condition number ≤ 1e4 — keeps float64 inversion error ~1e-12,
  two orders under the exact-row tolerance).
- 50 random O(d) transforms per cell (QR of a Gaussian matrix).
- Operators: `P = V Λ Vᵀ`, V a random orthonormal d×r frame, Λ
  log-uniform on [1e-2, 1], descending. A second independent `P₂` of the
  same rank for the principal-angle row. `Σ_δ` full-rank PSD, same
  construction.
- 100 random perturbations δ ~ N(0, I) per transform for the damage row.
- Seed **20260815** throughout (numpy default_rng).

## Transformation conventions (as derived in OT-CRUCIBLE §OT-7)

`x' = Ax` ⇒ `P' = A⁻ᵀPA⁻¹`, `δ' = Aδ`, `Σ' = AΣAᵀ`. The loading check
uses consumer `C(x) = tanh(aᵀx)` (so `A(x) = (1−tanh²)² aaᵀ`), weight
`h(x) = bᵀx` (zero-mean under N(0,I)), n = 20,000 shared Monte Carlo
samples on both sides of the identity `E'[h'A'] = A⁻ᵀ E[hA] A⁻¹`.

## Bars

- **Exact ("yes") rows** — damage form, `tr(PΣ)` pairing, rank, loading
  covariance: max relative deviation ≤ **1e-9** over every transform in
  every cell. One violation kills the row; a killed "yes" row kills OT-7.
- **Fragile ("no") rows** — spectrum, effective rank (participation
  ratio), energy rank(0.9), principal angles, water-filling allocation
  (budget 2d bits, reverse water-fill, compared as sorted multisets):
  under GL, relative deviation > **1e-6** in ≥ **95%** of transforms
  (non-invariance must be demonstrated, not presumed); under O(d), the
  same quantities must be invariant to ≤ 1e-8. A fragile row that turns
  out GL-invariant kills OT-7 exactly as a broken exact row does.
- Verdict: **ALL rows pass in ALL cells**, else FAIL. Result JSON:
  `results/OT7-invariance.json`; ledger row OT-7.
