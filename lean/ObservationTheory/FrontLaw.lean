/-
Machine-checked algebra of the OP3 corrected front law (the v1-line's
first campaign, `crucible/PREREG-OP3.md`).

The shakedown refuted the naive `m^{-1/2}`-to-zero rate model. The
corrected law is a spectrum-ordered recovery front, derived from the
C-15 sketch identity carried one step further:

  M = E[Ŝ] = (1 + 1/k) S + (tr S / k) I         (the sketch identity)

`M` is an *affine* function of the population operator `S`, so it has
`S`'s eigenvectors with eigenvalues `μ_i = (1+1/k) λ_i + tr(S)/k`. For
the planted geometric spectrum `λ_i = λ₀ ρ^i` (ρ = w², w = 0.75), the
eigengap obeys `gap_i / gap₀ = ρ^i`. Davis–Kahan (cited, as in
`DECLARATION-V1`'s stated standard) gives `sinθ_i ≲ ‖Ŝ_n − M‖ / gap_i`,
and the isotropic fluctuation floor `‖Ŝ_n − M‖ ∝ tr(S)/(k√n)` is common
to all modes — the cross-mode interference. Hence
`sin²θ_i ∝ 1/(n·gap_i²) ∝ 1/(n·w^{4i})`: the per-mode recovery collapses
onto one curve in `s_i = m·w^{4i}`. The exponent is **p = 4**.

What is machine-checked here, faithfully:

* `affine_hasEigenvector` — the *mechanism*: an affine image `a•f + b•1`
  of an operator keeps every eigenvector of `f`, with eigenvalue
  `a·μ + b`. This is why sub-dimensional averaging recovers the
  population eigenspaces at all (recovery, not a plateau) — the door
  single-shot confinement leaves open.
* `affine_eigengap` — the affine map scales every eigengap by exactly
  `a` and leaves the eigenvectors fixed, so the gap *ordering* is the
  spectrum's ordering.
* `geometric_gap_ratio` — for a geometric spectrum the gap ratio to the
  leading gap is `ρ^i`: the front is ordered by the spectrum, gap `∝ ρ^i`.
* `frontlaw_exponent` — with `ρ = w²`, `(gap_i/gap₀)² = w^{4i}`: the
  collapse variable is `m·w^{4i}`, exponent `p = 4`, machine-checked.
  (The naive `p = 2` guess omits the squaring that Davis–Kahan's
  `sinθ ∝ 1/gap` and the `s = n·gap²` collapse together force.)

Cited, not formalized (per the program's standing standard): the
Davis–Kahan sinΘ bound and the Gaussian operator-norm rate for the
fluctuation `‖Ŝ_n − M‖ ∝ n^{-1/2}`. The numeric collapse validation
lives in `readscope/calibration/op3_frontlaw.py`.
-/

import Mathlib.Analysis.InnerProductSpace.Basic

variable {E : Type*} [NormedAddCommGroup E] [Module ℝ E]

/-- The mechanism. An affine image `a • f + b • 1` of an operator keeps
every eigenvector `v` of `f` (`f v = μ • v`), with eigenvalue
`a * μ + b`. Affine functions of an operator share its eigenvectors —
the reason sub-dimensional averaging can recover the population
eigenspaces even below the sketch width. -/
theorem affine_hasEigenvector
    (f : Module.End ℝ E) (v : E) (μ a b : ℝ) (hv : f v = μ • v) :
    (a • f + b • (1 : Module.End ℝ E)) v = (a * μ + b) • v := by
  simp only [LinearMap.add_apply, LinearMap.smul_apply, Module.End.one_apply,
    hv, smul_smul]
  rw [add_smul]

/-- The affine map scales every eigengap by exactly `a`. With `a > 0`
the gap *ordering* is preserved, so the recovery front is ordered by the
population spectrum. -/
theorem affine_eigengap (a b μi μj : ℝ) :
    (a * μi + b) - (a * μj + b) = a * (μi - μj) := by ring

/-- For a geometric spectrum `λ_i = λ₀ ρ^i`, the eigengap ratio to the
leading gap is `ρ^i`: the gap decays geometrically down the spectrum,
`gap_i ∝ ρ^i`. Needs `λ₀ ≠ 0` and `ρ ≠ 1` (else the leading gap is
zero). -/
theorem geometric_gap_ratio (lam0 rho : ℝ) (i : ℕ)
    (h0 : lam0 ≠ 0) (hr : rho ≠ 1) :
    (lam0 * rho ^ i - lam0 * rho ^ (i + 1)) /
      (lam0 * rho ^ 0 - lam0 * rho ^ 1) = rho ^ i := by
  have e1 : lam0 * rho ^ i - lam0 * rho ^ (i + 1)
      = (lam0 * (1 - rho)) * rho ^ i := by ring
  have e2 : lam0 * rho ^ 0 - lam0 * rho ^ 1 = lam0 * (1 - rho) := by ring
  have hne : lam0 * (1 - rho) ≠ 0 :=
    mul_ne_zero h0 (sub_ne_zero.mpr (Ne.symm hr))
  rw [e1, e2, mul_comm, mul_div_assoc, div_self hne, mul_one]

/-- The exponent. With `ρ = w²` (eigenvalues scale as the squared
amplitude), the squared gap ratio — the collapse variable's mode factor,
since `sinθ ∝ 1/gap` and the statistical collapse is in `n · gap²` — is
`w^{4i}`. Hence the recovery collapses in `s_i = m · w^{4i}`: **p = 4**,
not the naive `p = 2`. -/
theorem frontlaw_exponent (w : ℝ) (i : ℕ) :
    ((w ^ 2) ^ i) ^ 2 = w ^ (4 * i) := by
  rw [← pow_mul, ← pow_mul]
  congr 1
  ring
