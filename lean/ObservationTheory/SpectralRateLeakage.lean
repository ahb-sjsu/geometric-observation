/-
Rate and leakage for stationary Gaussian sources: machine-checked algebraic cores for
`paper/tit-stationary/`.

The spectral (Szegő / Toeplitz) limit theorems of the paper are not formalized here. This file
checks, with explicit hypotheses, the per-direction (per-frequency) algebra and the allocation and
symmetry arguments their proofs rely on. In a direction with decoder weight q > 0 and holder
information j ≥ 0, a description leaving normalized error variance x ∈ (0,1] has

  rate     r(x)   = ½ log(1/x)                      (`rate`)
  leakage  l(x,j) = ½ log((1 + j x)/(x (1 + j)))    (`leak`)

(natural logarithm).

* `leak_nonneg`, `leak_le_rate`, `leak_one`, `leak_zero`
                              leakage bounds: 0 ≤ l ≤ r on (0,1], l(1,j) = 0, l(x,0) = r(x).
* `leak_antitone_holder`      a better-informed holder leaks less: j₁ ≤ j₂ ⇒ l(x,j₂) ≤ l(x,j₁).
* `hasDerivAt_tradeoff`       slope: φ = α r + (1-α) l(·,j) has derivative
                              -(1 + α j x)/(2 x (1 + j x)) at x > 0.
* `stationarity_iff_quad`     the stationarity condition (1 + α j x)/(2x(1 + j x)) = θ q/2 is the
                              quadratic θ q j x² + (θ q - α j) x - 1 = 0.
* `quad_pos_root_exists`, `quad_pos_root_unique`, `stationarity_quad_existsUnique`
                              the quadratic a x² + b x - 1 (a > 0) has exactly one positive root.
* `quad_pos_root_lt_one_iff`, `activation_threshold`
                              the positive root is < 1 iff θ > (1 + α j)/(q (1 + j)).
* `equal_slope_finite`        equal-slope allocation is optimal, finite form: if -θ q_k is a
                              subgradient of φ_k at x_k (evaluated at y_k) and Σ q y ≤ Σ q x, then
                              Σ φ_k(x_k) ≤ Σ φ_k(y_k).
* `equal_slope_integral`      the same over a measure space (the spectral form).
* `allpass_scalar`, `allpass_matrix`
                              all-pass invariance: a unimodular scalar factor on the channel does
                              not change h* h / s, resp. Hᴴ M H.
* `sign_symmetry_blockDiagonal`
                              a block matrix fixed by conjugation with diag(1, -1) is block-diagonal.
* `commute_J_blocks`, `commute_J_of_blocks`
                              a real 2n×2n matrix commutes with J = [[0, -1], [1, 0]] iff it has the
                              form [[A, B], [-B, A]], the realification (real part stacked over
                              imaginary part) of the complex matrix A - iB.
* `affine_commute`            two affine functions a C + b 1 of the same matrix C commute.
-/
import Mathlib

namespace ObservationTheory.SpectralRateLeakage

open MeasureTheory
open scoped Matrix

/-- Rate of a description leaving normalized error variance `x`: ½ log(1/x). -/
noncomputable def rate (x : ℝ) : ℝ := 1 / 2 * Real.log (1 / x)

/-- Leakage to a holder with information `j`: ½ log((1 + j x)/(x (1 + j))). -/
noncomputable def leak (x j : ℝ) : ℝ := 1 / 2 * Real.log ((1 + j * x) / (x * (1 + j)))

/-! ### Leakage bounds -/

/-- Leakage is nonnegative on (0,1]. -/
theorem leak_nonneg (x j : ℝ) (hx : 0 < x) (hx1 : x ≤ 1) (hj : 0 ≤ j) : 0 ≤ leak x j := by
  unfold leak
  refine mul_nonneg (by norm_num) (Real.log_nonneg ?_)
  rw [le_div_iff₀ (by positivity)]
  nlinarith [mul_nonneg hj (sub_nonneg.2 hx1)]

/-- Leakage never exceeds the rate. -/
theorem leak_le_rate (x j : ℝ) (hx : 0 < x) (hx1 : x ≤ 1) (hj : 0 ≤ j) : leak x j ≤ rate x := by
  unfold leak rate
  refine mul_le_mul_of_nonneg_left (Real.log_le_log (by positivity) ?_) (by norm_num)
  rw [div_le_div_iff₀ (by positivity) hx]
  nlinarith [mul_nonneg (mul_nonneg hj hx.le) (sub_nonneg.2 hx1)]

/-- No description (x = 1), no leakage. -/
theorem leak_one (j : ℝ) (hj : 0 ≤ j) : leak 1 j = 0 := by
  unfold leak
  have h : (1 : ℝ) + j ≠ 0 := by positivity
  rw [mul_one, one_mul, div_self h, Real.log_one, mul_zero]

/-- An uninformed holder (j = 0) learns the whole description. -/
theorem leak_zero (x : ℝ) : leak x 0 = rate x := by
  unfold leak rate
  rw [zero_mul, add_zero, mul_one]

/-- A better-informed holder leaks less. -/
theorem leak_antitone_holder (x j₁ j₂ : ℝ) (hx : 0 < x) (hx1 : x ≤ 1) (hj₁ : 0 ≤ j₁)
    (h12 : j₁ ≤ j₂) : leak x j₂ ≤ leak x j₁ := by
  have hj₂ : 0 ≤ j₂ := hj₁.trans h12
  unfold leak
  refine mul_le_mul_of_nonneg_left (Real.log_le_log (by positivity) ?_) (by norm_num)
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith [mul_nonneg (mul_nonneg hx.le (sub_nonneg.2 h12)) (sub_nonneg.2 hx1)]

/-! ### Slope -/

/-- The trade-off cost φ = α r + (1-α) l(·,j) has slope -(1 + α j x)/(2 x (1 + j x)). -/
theorem hasDerivAt_tradeoff (x j α : ℝ) (hx : 0 < x) (hj : 0 ≤ j) :
    HasDerivAt (fun y : ℝ => α * rate y + (1 - α) * leak y j)
      (-(1 + α * j * x) / (2 * x * (1 + j * x))) x := by
  have hx0 : x ≠ 0 := hx.ne'
  have hjx : (1 : ℝ) + j * x ≠ 0 := by positivity
  have hlog : HasDerivAt Real.log x⁻¹ x := Real.hasDerivAt_log hx0
  have hlin : HasDerivAt (fun y : ℝ => 1 + j * y) (j * 1) x :=
    ((hasDerivAt_id' x).const_mul j).const_add 1
  have hlog2 : HasDerivAt (fun y : ℝ => Real.log (1 + j * y)) (j * 1 / (1 + j * x)) x :=
    hlin.log hjx
  have hg : HasDerivAt
      (fun y : ℝ => α * (-(1 / 2) * Real.log y)
        + (1 - α) * (1 / 2 * (Real.log (1 + j * y) - Real.log y - Real.log (1 + j))))
      (α * (-(1 / 2) * x⁻¹) + (1 - α) * (1 / 2 * (j * 1 / (1 + j * x) - x⁻¹))) x :=
    ((hlog.const_mul (-(1 / 2))).const_mul α).add
      ((((hlog2.sub hlog).sub_const (Real.log (1 + j))).const_mul (1 / 2)).const_mul (1 - α))
  have heq : (fun y : ℝ => α * rate y + (1 - α) * leak y j) =ᶠ[nhds x]
      (fun y : ℝ => α * (-(1 / 2) * Real.log y)
        + (1 - α) * (1 / 2 * (Real.log (1 + j * y) - Real.log y - Real.log (1 + j)))) := by
    filter_upwards [eventually_gt_nhds hx] with y hy
    have hy0 : y ≠ 0 := hy.ne'
    have hjy : (1 : ℝ) + j * y ≠ 0 := by positivity
    have hj1 : (1 : ℝ) + j ≠ 0 := by positivity
    have hr : rate y = -(1 / 2) * Real.log y := by
      unfold rate
      rw [one_div y, Real.log_inv]
      ring
    have hl : leak y j = 1 / 2 * (Real.log (1 + j * y) - Real.log y - Real.log (1 + j)) := by
      unfold leak
      rw [Real.log_div hjy (mul_ne_zero hy0 hj1), Real.log_mul hy0 hj1]
      ring
    rw [hr, hl]
  have hd := hg.congr_of_eventuallyEq heq
  refine hd.congr_deriv ?_
  field_simp
  ring

/-! ### Stationarity quadratic -/

/-- Setting the slope to -θ q / 2 is the quadratic θ q j x² + (θ q - α j) x - 1 = 0. -/
theorem stationarity_iff_quad (θ q j α x : ℝ) (hj : 0 ≤ j) (hx : 0 < x) :
    (1 + α * j * x) / (2 * x * (1 + j * x)) = θ * q / 2
      ↔ θ * q * j * x ^ 2 + (θ * q - α * j) * x - 1 = 0 := by
  have hden : 2 * x * (1 + j * x) ≠ 0 := by positivity
  rw [div_eq_div_iff hden two_ne_zero]
  constructor
  · intro h
    linear_combination (-1 / 2) * h
  · intro h
    linear_combination (-2) * h

/-- The quadratic a x² + b x - 1 with a > 0 has a positive root. -/
theorem quad_pos_root_exists (a b : ℝ) (ha : 0 < a) : ∃ x : ℝ, 0 < x ∧ a * x ^ 2 + b * x - 1 = 0 := by
  have hdisc : 0 ≤ b ^ 2 + 4 * a := by positivity
  set s := Real.sqrt (b ^ 2 + 4 * a) with hs_def
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hs : s * s = b ^ 2 + 4 * a := Real.mul_self_sqrt hdisc
  have hsb : b < s := by
    by_contra h
    have h' : s ≤ b := not_lt.mp h
    nlinarith [mul_self_le_mul_self hs0 h']
  have h2a : (2 * a) ≠ 0 := by positivity
  have h2' : (s - b) / (2 * a) * (2 * a) = s - b := div_mul_cancel₀ _ h2a
  obtain ⟨x, hx_def⟩ : ∃ x : ℝ, x = (s - b) / (2 * a) := ⟨_, rfl⟩
  have hxpos : 0 < x := by
    rw [hx_def]
    exact div_pos (sub_pos.2 hsb) (by positivity)
  have h2 : 2 * a * x = s - b := by
    rw [hx_def]
    linear_combination h2'
  refine ⟨x, hxpos, ?_⟩
  have h3 : a * (a * x ^ 2 + b * x - 1) = 0 := by
    linear_combination (1 / 4) * (2 * a * x + s + b) * h2 + (1 / 4) * hs
  exact (mul_eq_zero.mp h3).resolve_left ha.ne'

/-- The quadratic a x² + b x - 1 with a > 0 has at most one positive root. -/
theorem quad_pos_root_unique (a b x₁ x₂ : ℝ) (ha : 0 < a) (h₁ : 0 < x₁) (h₂ : 0 < x₂)
    (r₁ : a * x₁ ^ 2 + b * x₁ - 1 = 0) (r₂ : a * x₂ ^ 2 + b * x₂ - 1 = 0) : x₁ = x₂ := by
  by_contra hne
  have hsub : (x₁ - x₂) * (a * (x₁ + x₂) + b) = 0 := by linear_combination r₁ - r₂
  have hb : a * (x₁ + x₂) + b = 0 := (mul_eq_zero.mp hsub).resolve_left (sub_ne_zero.mpr hne)
  have hp : 0 < a * x₁ * x₂ := mul_pos (mul_pos ha h₁) h₂
  have hm : a * x₁ * x₂ = -1 := by linear_combination x₁ * hb - r₁
  linarith

/-- The stationarity quadratic has exactly one positive root. -/
theorem stationarity_quad_existsUnique (θ q j α : ℝ) (hθ : 0 < θ) (hq : 0 < q) (hj : 0 < j) :
    ∃! x : ℝ, 0 < x ∧ θ * q * j * x ^ 2 + (θ * q - α * j) * x - 1 = 0 := by
  have ha : 0 < θ * q * j := by positivity
  obtain ⟨x, hx, hr⟩ := quad_pos_root_exists (θ * q * j) (θ * q - α * j) ha
  exact ⟨x, ⟨hx, hr⟩, fun y hy => quad_pos_root_unique _ _ y x ha hy.1 hx hy.2 hr⟩

/-! ### Activation threshold -/

/-- The positive root of a x² + b x - 1 (a > 0) is below 1 iff the quadratic is positive at 1. -/
theorem quad_pos_root_lt_one_iff (a b x : ℝ) (ha : 0 < a) (hx : 0 < x)
    (hr : a * x ^ 2 + b * x - 1 = 0) : x < 1 ↔ 0 < a + b - 1 := by
  have hxc : x * (a * (1 + x) + b) = a * x + 1 := by linear_combination hr
  have hax : 0 < a * x := mul_pos ha hx
  have hc : 0 < a * (1 + x) + b := by
    by_contra h
    have h' : a * (1 + x) + b ≤ 0 := not_lt.mp h
    nlinarith [mul_nonneg hx.le (neg_nonneg.2 h')]
  have key : a + b - 1 = (1 - x) * (a * (1 + x) + b) := by linear_combination hr
  constructor
  · intro h
    rw [key]
    exact mul_pos (sub_pos.2 h) hc
  · intro h
    by_contra hlt
    have hge : 1 ≤ x := not_lt.mp hlt
    nlinarith [mul_nonneg (sub_nonneg.2 hge) hc.le]

/-- Activation threshold: the positive root ξ of the stationarity quadratic satisfies ξ < 1
(the direction is described) iff θ > (1 + α j)/(q (1 + j)). -/
theorem activation_threshold (θ q j α ξ : ℝ) (hθ : 0 < θ) (hq : 0 < q) (hj : 0 < j) (hξ : 0 < ξ)
    (hr : θ * q * j * ξ ^ 2 + (θ * q - α * j) * ξ - 1 = 0) :
    ξ < 1 ↔ (1 + α * j) / (q * (1 + j)) < θ := by
  have ha : 0 < θ * q * j := by positivity
  rw [quad_pos_root_lt_one_iff (θ * q * j) (θ * q - α * j) ξ ha hξ hr,
    div_lt_iff₀ (by positivity)]
  constructor <;> intro h <;> linarith

/-! ### Equal-slope allocation -/

/-- Equal-slope allocation is optimal (finite form): if every φ_k admits the slope -θ q_k at x_k
as a supporting line evaluated at y_k, and y spends no more weighted budget than x, then x has no
larger total cost than y. -/
theorem equal_slope_finite {ι : Type*} [Fintype ι] (φ : ι → ℝ → ℝ) (q x y : ι → ℝ) (θ : ℝ)
    (hθ : 0 ≤ θ)
    (hsub : ∀ k, φ k (x k) - θ * q k * (y k - x k) ≤ φ k (y k))
    (hc : ∑ k, q k * y k ≤ ∑ k, q k * x k) :
    ∑ k, φ k (x k) ≤ ∑ k, φ k (y k) := by
  have h1 : ∑ k, (φ k (x k) - θ * q k * (y k - x k)) ≤ ∑ k, φ k (y k) :=
    Finset.sum_le_sum (fun k _ => hsub k)
  have h2 : ∑ k, (φ k (x k) - θ * q k * (y k - x k))
      = ∑ k, φ k (x k) - θ * (∑ k, q k * y k - ∑ k, q k * x k) := by
    rw [← Finset.sum_sub_distrib, Finset.mul_sum, ← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl (fun k _ => by ring)
  nlinarith [mul_nonneg hθ (sub_nonneg.2 hc)]

/-- Equal-slope allocation is optimal (integral form, e.g. over frequency). -/
theorem equal_slope_integral {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) (φ : Ω → ℝ → ℝ)
    (q x y : Ω → ℝ) (θ : ℝ) (hθ : 0 ≤ θ)
    (hsub : ∀ᵐ ω ∂μ, φ ω (x ω) - θ * q ω * (y ω - x ω) ≤ φ ω (y ω))
    (hφx : Integrable (fun ω => φ ω (x ω)) μ) (hφy : Integrable (fun ω => φ ω (y ω)) μ)
    (hqx : Integrable (fun ω => q ω * x ω) μ) (hqy : Integrable (fun ω => q ω * y ω) μ)
    (hc : ∫ ω, q ω * y ω ∂μ ≤ ∫ ω, q ω * x ω ∂μ) :
    ∫ ω, φ ω (x ω) ∂μ ≤ ∫ ω, φ ω (y ω) ∂μ := by
  have hd : Integrable (fun ω => θ * (q ω * y ω - q ω * x ω)) μ := (hqy.sub hqx).const_mul θ
  have hint : Integrable (fun ω => φ ω (x ω) - θ * (q ω * y ω - q ω * x ω)) μ := hφx.sub hd
  have hle : ∀ᵐ ω ∂μ, φ ω (x ω) - θ * (q ω * y ω - q ω * x ω) ≤ φ ω (y ω) := by
    filter_upwards [hsub] with ω h
    linarith
  have h1 : ∫ ω, (φ ω (x ω) - θ * (q ω * y ω - q ω * x ω)) ∂μ ≤ ∫ ω, φ ω (y ω) ∂μ :=
    integral_mono_ae hint hφy hle
  have h2 : ∫ ω, (φ ω (x ω) - θ * (q ω * y ω - q ω * x ω)) ∂μ
      = ∫ ω, φ ω (x ω) ∂μ - θ * (∫ ω, q ω * y ω ∂μ - ∫ ω, q ω * x ω ∂μ) := by
    rw [integral_sub hφx hd, integral_const_mul, integral_sub hqy hqx]
  nlinarith [mul_nonneg hθ (sub_nonneg.2 hc)]

/-! ### All-pass invariance -/

/-- A unimodular factor on a scalar channel does not change h* h / s. -/
theorem allpass_scalar (h c : ℂ) (s : ℝ) (hc : ‖c‖ = 1) :
    star (c * h) * (c * h) / (s : ℂ) = star h * h / (s : ℂ) := by
  have hc' : star c * c = 1 := by
    rw [Complex.star_def, Complex.conj_mul', hc]
    simp
  have key : star (c * h) * (c * h) = star h * h := by
    rw [star_mul]
    linear_combination (star h * h) * hc'
  rw [key]

/-- A unimodular scalar factor on a matrix channel does not change Hᴴ M H. -/
theorem allpass_matrix {m n : Type*} [Fintype m] [Fintype n] (H : Matrix m n ℂ)
    (M : Matrix m m ℂ) (c : ℂ) (hc : star c * c = 1) :
    (c • H)ᴴ * M * (c • H) = Hᴴ * M * H := by
  rw [Matrix.conjTranspose_smul, Matrix.smul_mul, Matrix.smul_mul, Matrix.mul_smul, smul_smul,
    hc, one_smul]

/-! ### Symmetry reductions -/

/-- A real matrix equal to its own negative is zero. -/
theorem matrix_eq_zero_of_neg_eq {n m : Type*} (B : Matrix n m ℝ) (h : -B = B) : B = 0 := by
  ext i j
  have hij := congrFun (congrFun h i) j
  simp only [Matrix.neg_apply] at hij
  simp only [Matrix.zero_apply]
  linarith

/-- Sign symmetry forces block-diagonal form: if conjugation by diag(1, -1) fixes
[[A, B], [C, D]], then B = 0 and C = 0. -/
theorem sign_symmetry_blockDiagonal {n m : Type*} [Fintype n] [Fintype m] [DecidableEq n]
    [DecidableEq m] (A : Matrix n n ℝ) (B : Matrix n m ℝ) (C : Matrix m n ℝ) (D : Matrix m m ℝ)
    (h : Matrix.fromBlocks (1 : Matrix n n ℝ) (0 : Matrix n m ℝ) (0 : Matrix m n ℝ)
          (-1 : Matrix m m ℝ) * Matrix.fromBlocks A B C D
          * Matrix.fromBlocks (1 : Matrix n n ℝ) (0 : Matrix n m ℝ) (0 : Matrix m n ℝ)
            (-1 : Matrix m m ℝ)
        = Matrix.fromBlocks A B C D) :
    B = 0 ∧ C = 0 := by
  have h1 : Matrix.fromBlocks (1 : Matrix n n ℝ) (0 : Matrix n m ℝ) (0 : Matrix m n ℝ)
          (-1 : Matrix m m ℝ) * Matrix.fromBlocks A B C D
          * Matrix.fromBlocks (1 : Matrix n n ℝ) (0 : Matrix n m ℝ) (0 : Matrix m n ℝ)
            (-1 : Matrix m m ℝ)
        = Matrix.fromBlocks A (-B) (-C) D := by
    simp [Matrix.fromBlocks_multiply]
  rw [h1, Matrix.fromBlocks_inj] at h
  obtain ⟨-, hB, hC, -⟩ := h
  exact ⟨matrix_eq_zero_of_neg_eq B hB, matrix_eq_zero_of_neg_eq C hC⟩

/-- Complex structure: a real block matrix [[A, B], [C, D]] commuting with J = [[0, -1], [1, 0]]
has D = A and C = -B, i.e. it is [[A, B], [-B, A]]. -/
theorem commute_J_blocks {n : Type*} [Fintype n] [DecidableEq n] (A B C D : Matrix n n ℝ)
    (h : Matrix.fromBlocks (0 : Matrix n n ℝ) (-1) 1 0 * Matrix.fromBlocks A B C D
        = Matrix.fromBlocks A B C D * Matrix.fromBlocks (0 : Matrix n n ℝ) (-1) 1 0) :
    D = A ∧ C = -B := by
  have hl : Matrix.fromBlocks (0 : Matrix n n ℝ) (-1) 1 0 * Matrix.fromBlocks A B C D
      = Matrix.fromBlocks (-C) (-D) A B := by
    simp [Matrix.fromBlocks_multiply]
  have hr : Matrix.fromBlocks A B C D * Matrix.fromBlocks (0 : Matrix n n ℝ) (-1) 1 0
      = Matrix.fromBlocks B (-A) D (-C) := by
    simp [Matrix.fromBlocks_multiply]
  rw [hl, hr, Matrix.fromBlocks_inj] at h
  obtain ⟨h1, -, h3, -⟩ := h
  exact ⟨h3.symm, by rw [← h1, neg_neg]⟩

/-- Converse: every [[A, B], [-B, A]] commutes with J = [[0, -1], [1, 0]]. -/
theorem commute_J_of_blocks {n : Type*} [Fintype n] [DecidableEq n] (A B : Matrix n n ℝ) :
    Matrix.fromBlocks (0 : Matrix n n ℝ) (-1) 1 0 * Matrix.fromBlocks A B (-B) A
      = Matrix.fromBlocks A B (-B) A * Matrix.fromBlocks (0 : Matrix n n ℝ) (-1) 1 0 := by
  simp [Matrix.fromBlocks_multiply]

/-- Common context: two affine functions of the same matrix commute. -/
theorem affine_commute {n : Type*} [Fintype n] [DecidableEq n] (C A B : Matrix n n ℝ)
    (a b c d : ℝ) (hA : A = a • C + b • (1 : Matrix n n ℝ))
    (hB : B = c • C + d • (1 : Matrix n n ℝ)) : A * B = B * A := by
  have h1 : Commute C (c • C + d • (1 : Matrix n n ℝ)) :=
    ((Commute.refl C).smul_right c).add_right ((Commute.one_right C).smul_right d)
  have h2 : Commute (1 : Matrix n n ℝ) (c • C + d • (1 : Matrix n n ℝ)) := Commute.one_left _
  have h3 : Commute (a • C + b • (1 : Matrix n n ℝ)) (c • C + d • (1 : Matrix n n ℝ)) :=
    (h1.smul_left a).add_left (h2.smul_left b)
  rw [hA, hB]
  exact h3.eq

end ObservationTheory.SpectralRateLeakage
