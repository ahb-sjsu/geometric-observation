/-
Rate, leakage, and distortion for Gaussian sources: machine-checked scalar algebra for
`paper/tit-rate-leakage/tit-rate-leakage.tex`.

The matrix-analytic theorems of the paper (water-filling on a tilted weight, convexity in the error
covariance, the rank bound, convergence of the iteration) are not formalized here. This file checks,
over ℝ with explicit hypotheses, the closed-form and scalar steps their proofs rely on:

* `scalarpath_root_ratio`   Theorem scalarpath: at a root, (1-Δv)/(1-Δu) = (1-α)/ρ, so L = ½ log((1-α)/ρ).
* `scalarpath_alpha_zero`   Theorem scalarpath, α = 0: with ρ = μ/(Δ+μ) the root equation is Δu + μ(u-v) = 1.
* `pencil_rho`              ρ = μ/(Δ+μ) from 1-Δu = μw and 1-Δv = (μ+Δ)w.
* `rate_active_noise`       Theorem scalarpath: 1 + u/σ² = 1/(1-Δu) at σ² = (1-Δu)/Δ.
* `quad_iff_stationary`     Theorems lowdist, commuting: the quadratic is the stationarity condition.
* `quad_pos_root_unique`    the quadratic has at most one positive root.
* `fixedread_ratio`         Proposition fixedread: the exact ratio identity.
* `fixedread_mono`          x ↦ x/(μ₁-x) is strictly increasing on [0, μ₁).
* `mm_step_monotone`        Proposition mm: a majorize-minimize step does not increase the cost.
* `log_tangent_le`          Proposition mm: the tangent of log at x₀ majorizes log (scalar majorizer).
-/
import Mathlib

namespace ObservationTheory.RateLeakage

/-- Theorem scalarpath: at a root of ρ(1-Δv) = (1-α)(1-Δu), the leakage ratio is (1-α)/ρ. -/
theorem scalarpath_root_ratio (Δ u v ρ α : ℝ) (hρ : ρ ≠ 0) (hu : 1 - Δ * u ≠ 0)
    (h : ρ * (1 - Δ * v) = (1 - α) * (1 - Δ * u)) :
    (1 - Δ * v) / (1 - Δ * u) = (1 - α) / ρ := by
  rw [div_eq_div_iff hu hρ]
  linarith [h]

/-- Theorem scalarpath at α = 0: with ρ = μ/(Δ+μ), ρ(1-Δv) - (1-Δu) = Δ(Δu + μ(u-v) - 1)/(Δ+μ). -/
theorem scalarpath_alpha_zero (Δ u v μ : ℝ) (h : Δ + μ ≠ 0) :
    μ / (Δ + μ) * (1 - Δ * v) - (1 - Δ * u) = Δ * (Δ * u + μ * (u - v) - 1) / (Δ + μ) := by
  field_simp
  ring

/-- The pencil relation ρ = μ/(Δ+μ). -/
theorem pencil_rho (Δ u v μ w : ℝ) (hw : w ≠ 0) (hm : μ + Δ ≠ 0)
    (h1 : 1 - Δ * u = μ * w) (h2 : 1 - Δ * v = (μ + Δ) * w) :
    (1 - Δ * u) / (1 - Δ * v) = μ / (Δ + μ) := by
  rw [h1, h2, add_comm Δ μ]
  field_simp

/-- Theorem scalarpath: the rate at the active noise level. -/
theorem rate_active_noise (Δ u : ℝ) (_hΔ : Δ ≠ 0) (hu : 1 - Δ * u ≠ 0) :
    1 + u / ((1 - Δ * u) / Δ) = 1 / (1 - Δ * u) := by
  rw [div_div_eq_mul_div, eq_div_iff hu, add_mul, div_mul_cancel₀ _ hu]
  ring

/-- Theorems lowdist and commuting: the per-direction quadratic equals minus the stationarity
condition multiplied by (1 + πξ). -/
theorem quad_iff_stationary (θ π α ξ : ℝ) (h : 1 + π * ξ ≠ 0) :
    (α + (1 - α) / (1 + π * ξ) - θ * ξ) * (1 + π * ξ)
      = -(θ * π * ξ ^ 2 + (θ - α * π) * ξ - 1) := by
  field_simp
  ring

/-- The per-direction quadratic aξ² + bξ - 1 with a > 0 has at most one positive root. -/
theorem quad_pos_root_unique (a b ξ₁ ξ₂ : ℝ) (ha : 0 < a) (h₁ : 0 < ξ₁) (h₂ : 0 < ξ₂)
    (r₁ : a * ξ₁ ^ 2 + b * ξ₁ - 1 = 0) (r₂ : a * ξ₂ ^ 2 + b * ξ₂ - 1 = 0) : ξ₁ = ξ₂ := by
  by_contra hne
  have hsub : (ξ₁ - ξ₂) * (a * (ξ₁ + ξ₂) + b) = 0 := by nlinarith [r₁, r₂]
  have hb : a * (ξ₁ + ξ₂) + b = 0 := by
    rcases mul_eq_zero.mp hsub with h | h
    · exact absurd (sub_eq_zero.mp h) hne
    · exact h
  have : a * ξ₁ * ξ₂ = -1 := by nlinarith [r₁, hb]
  nlinarith [mul_pos (mul_pos ha h₁) h₂]

/-- Proposition fixedread: the exact ratio identity, with x = μ₁ - μ_b. -/
theorem fixedread_ratio (Δ μ₁ x : ℝ) (h1 : μ₁ ≠ 0) (h2 : μ₁ - x ≠ 0) (h3 : μ₁ + Δ ≠ 0) :
    (1 + Δ / (μ₁ - x)) / (1 + Δ / μ₁) = 1 + Δ * x / ((μ₁ - x) * (μ₁ + Δ)) := by
  have h4 : (1 + Δ / μ₁) ≠ 0 := by
    rw [show 1 + Δ / μ₁ = (μ₁ + Δ) / μ₁ by field_simp]
    exact div_ne_zero h3 h1
  field_simp
  ring

/-- Proposition fixedread: x ↦ x/(μ₁-x) is strictly increasing on [0, μ₁). -/
theorem fixedread_mono (μ₁ x y : ℝ) (hx : 0 ≤ x) (hxy : x < y) (hy : y < μ₁) :
    x / (μ₁ - x) < y / (μ₁ - y) := by
  have hpx : 0 < μ₁ - x := by linarith
  have hpy : 0 < μ₁ - y := by linarith
  rw [div_lt_div_iff₀ hpx hpy]
  nlinarith

/-- Proposition mm: if g majorizes f and touches it at xₜ, a step that does not increase g
does not increase f. -/
theorem mm_step_monotone {X : Type*} (f g : X → ℝ) (xt xn : X) (hmaj : ∀ x, f x ≤ g x)
    (htouch : g xt = f xt) (hstep : g xn ≤ g xt) : f xn ≤ f xt := by
  have := hmaj xn
  linarith

/-- Proposition mm, scalar majorizer: log lies below its tangent at x₀ > 0. -/
theorem log_tangent_le (x x₀ : ℝ) (hx : 0 < x) (hx₀ : 0 < x₀) :
    Real.log x ≤ Real.log x₀ + (x - x₀) / x₀ := by
  have h := Real.log_le_sub_one_of_pos (div_pos hx hx₀)
  rw [Real.log_div hx.ne' hx₀.ne'] at h
  have : x / x₀ - 1 = (x - x₀) / x₀ := by field_simp
  linarith

end ObservationTheory.RateLeakage
