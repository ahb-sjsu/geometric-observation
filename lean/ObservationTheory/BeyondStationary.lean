/-
Rate and leakage beyond stationary Gaussian sources: machine-checked algebraic cores for
`paper/tit-beyond-stationary/`.

The coding theorems of the paper, its entropy inequalities, and its limit arguments are not
formalized here. This file checks, with explicit hypotheses, the algebra that their proofs rely on.
The matrix concavity of the linear-estimation error (used in the lower bound for sources that are
not Gaussian) is already in `LogDet.lean` (`Phi_eq`, `Phi_opt`, `Fw_concave`) and is not repeated.

* `neg_log_one_sub_le`      Lemma "cut": -log(1 - x) ≤ (b/a) x for 0 ≤ x ≤ 1 - a/b, the scalar
                            inequality that turns the information across a cut into a multiple of
                            the squared cross-covariance.
* `seed_cross`, `seed_cov`, `seed_remainder`
                            the explicit-seed draw T' = S' S⁻¹ T + C ζ with C Cᵀ = S' - S' S⁻¹ S':
                            Cov(T', T) = S', Cov(T') = S', and Cov(T - T') = S - S'.
* `det_one_add_conj`        Theorem "inner": det(I + G M Gᵀ) = det(I + M Gᵀ G).
* `rate_identity_scalar`, `leak_identity_scalar`
                            Theorem "inner", in one direction: with Gᵀ G = 1/d - 1/k the two
                            determinants are k/d and g(k)/g(d), g(x) = (1/x + j)⁻¹.
* `lin_est_error_ge`        Theorem "outer", scalar form: every linear estimate has error at least
                            d s/(h² d + s) (the matrix form is `LogDet.Phi_eq`).
* `deficit_identity`        the identity ϑ(T|S) = ϑ(T) - ϑ(S) for Gaussian holder noise, as algebra
                            on entropies.
* `Gs_scale_le`, `Gs_scale_ge`, `Gs_shrink`
                            Proposition "rate": the point cost G(d) = ½(-log d + (1-α) log(1 + j d))
                            satisfies G(d) - ½ log(1+x) ≤ G((1+x) d) ≤ G(d), and
                            G(c s) - G(s) ≤ ½ log(1/c) for 0 < c ≤ 1. These are facts (F1) to (F3)
                            at a point, in a direction.
* `ceil_sqrt_div_le`        Proposition "rate": ⌈√N⌉/N ≤ 2/√N for N ≥ 1.
* `sq_two_add_le`, `chebyshev_count`
                            Lemma "seeds": (2a + 2b)² ≤ 8a² + 8b², and k > 3v/δ² gives
                            v/(k δ²) < 1/3.

Natural logarithm throughout.
-/
import Mathlib

open Matrix

namespace ObservationTheory.BeyondStationary

/-! ### Lemma "cut" -/

/-- For `0 ≤ x ≤ 1 - a/b` with `0 < a ≤ b`, `-log(1 - x) ≤ (b/a) x`. -/
theorem neg_log_one_sub_le (a b x : ℝ) (ha : 0 < a) (hab : a ≤ b) (hx0 : 0 ≤ x)
    (hx : x ≤ 1 - a / b) : -Real.log (1 - x) ≤ b / a * x := by
  have hb : 0 < b := lt_of_lt_of_le ha hab
  have hab' : 0 < a / b := div_pos ha hb
  have h1 : 0 < 1 - x := by linarith
  have hlog : -Real.log (1 - x) ≤ (1 - x)⁻¹ - 1 := by
    have h := Real.log_le_sub_one_of_pos (inv_pos.mpr h1)
    rwa [Real.log_inv] at h
  have hy : (1 - x)⁻¹ ≤ b / a := by
    have h2 : a / b ≤ 1 - x := by linarith
    have h3 : (1 - x)⁻¹ ≤ (a / b)⁻¹ := inv_anti₀ hab' h2
    rwa [inv_div] at h3
  have key : (1 - x)⁻¹ - 1 = (1 - x)⁻¹ * x := by
    have h4 : (1 - x)⁻¹ * (1 - x) = 1 := inv_mul_cancel₀ h1.ne'
    have h5 : (1 - x)⁻¹ * x = (1 - x)⁻¹ - (1 - x)⁻¹ * (1 - x) := by ring
    rw [h5, h4]
  calc -Real.log (1 - x) ≤ (1 - x)⁻¹ - 1 := hlog
    _ = (1 - x)⁻¹ * x := key
    _ ≤ b / a * x := mul_le_mul_of_nonneg_right hy hx0

/-! ### The explicit-seed draw of Lemmas "coupling" and "seeds" -/

section Seed

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- `Cov(T', T) = S' S⁻¹ S = S'`. -/
theorem seed_cross (S S' : Matrix n n ℝ) (hS : IsUnit S.det) : S' * S⁻¹ * S = S' := by
  rw [Matrix.mul_assoc, Matrix.nonsing_inv_mul S hS, Matrix.mul_one]

/-- `Cov(T') = A S Aᵀ + C Cᵀ = S'` for `A = S' S⁻¹` and `C Cᵀ = S' - S' S⁻¹ S'`. -/
theorem seed_cov (S S' : Matrix n n ℝ) (hS : IsUnit S.det) (hSs : Sᵀ = S) (hS's : S'ᵀ = S') :
    S' * S⁻¹ * S * (S' * S⁻¹)ᵀ + (S' - S' * S⁻¹ * S') = S' := by
  have hinv : (S⁻¹)ᵀ = S⁻¹ := by rw [Matrix.transpose_nonsing_inv, hSs]
  rw [seed_cross S S' hS, Matrix.transpose_mul, hinv, hS's, ← Matrix.mul_assoc]
  abel

/-- `Cov(T - T') = S - Cov(T', T) - Cov(T', T)ᵀ + S' = S - S'`. -/
theorem seed_remainder (S S' : Matrix n n ℝ) (hS : IsUnit S.det) (hS's : S'ᵀ = S') :
    S - S' * S⁻¹ * S - (S' * S⁻¹ * S)ᵀ + S' = S - S' := by
  rw [seed_cross S S' hS, hS's]
  abel

end Seed

/-! ### Theorem "inner": the determinants of the Gaussian test channel -/

/-- `det(I + G M Gᵀ) = det(I + M Gᵀ G)`. -/
theorem det_one_add_conj {m n : Type*} [Fintype m] [DecidableEq m] [Fintype n] [DecidableEq n]
    (G : Matrix m n ℝ) (M : Matrix n n ℝ) :
    (1 + G * M * Gᵀ).det = (1 + M * (Gᵀ * G)).det := by
  rw [Matrix.mul_assoc, Matrix.det_one_add_mul_comm, Matrix.mul_assoc]

/-- Rate, one direction: `1 + k (1/d - 1/k) = k/d`. -/
theorem rate_identity_scalar (k d : ℝ) (hk : 0 < k) : 1 + k * (1 / d - 1 / k) = k / d := by
  rw [mul_sub, mul_one_div_cancel hk.ne', mul_one_div]
  ring

/-- Leakage, one direction: with `g(x) = (1/x + j)⁻¹`, `1 + g(k) (1/d - 1/k) = g(k)/g(d)`. -/
theorem leak_identity_scalar (k d j : ℝ) (hk : 0 < k) (hj : 0 ≤ j) :
    1 + (1 / k + j)⁻¹ * (1 / d - 1 / k) = (1 / k + j)⁻¹ / (1 / d + j)⁻¹ := by
  have h1 : 0 < 1 / k + j := by positivity
  have hu : (1 / k + j)⁻¹ * (1 / k + j) = 1 := inv_mul_cancel₀ h1.ne'
  have h2 : (1 / k + j)⁻¹ * (1 / d + j) =
      (1 / k + j)⁻¹ * (1 / k + j) + (1 / k + j)⁻¹ * (1 / d - 1 / k) := by ring
  rw [div_inv_eq_mul, h2, hu]

/-! ### Theorem "outer": the linear-estimation error, scalar form -/

/-- The estimate `b S` of a variable of variance `d` from `S = h T + U`, `Var U = s`, has error
`(1 - b h)² d + b² s`, which is at least the best value `d s/(h² d + s)`. -/
theorem lin_est_error_ge (d s h b : ℝ) (hd : 0 ≤ d) (hs : 0 < s) :
    d * s / (h ^ 2 * d + s) ≤ (1 - b * h) ^ 2 * d + b ^ 2 * s := by
  have hden : 0 < h ^ 2 * d + s := by positivity
  rw [div_le_iff₀ hden]
  nlinarith [sq_nonneg (b * (h ^ 2 * d + s) - h * d)]

/-- With `I(T;S) = h(S) - h(U)` and the Gaussian value `h_G(S) - h(U)`, the conditional deficit
`(h_G(T) - I_G) - (h(T) - I)` is the difference of the deficits of `T` and of `S`. -/
theorem deficit_identity (hT hTG hS hSG hU I IG : ℝ) (hI : I = hS - hU) (hIG : IG = hSG - hU) :
    (hTG - IG) - (hT - I) = (hTG - hT) - (hSG - hS) := by
  rw [hI, hIG]
  ring

/-! ### Proposition "rate": scaling of the point cost -/

/-- The point cost in one direction: `G(d) = ½ (-log d + (1 - α) log(1 + j d))`. -/
noncomputable def Gs (α j d : ℝ) : ℝ := 1 / 2 * (-Real.log d + (1 - α) * Real.log (1 + j * d))

/-- `G(d) - ½ log(1 + x) ≤ G((1 + x) d)`. -/
theorem Gs_scale_le (α j d x : ℝ) (hα : α ≤ 1) (hj : 0 ≤ j) (hd : 0 < d) (hx : 0 ≤ x) :
    Gs α j d - 1 / 2 * Real.log (1 + x) ≤ Gs α j ((1 + x) * d) := by
  unfold Gs
  have h1 : (0 : ℝ) < 1 + x := by linarith
  have hlog : Real.log ((1 + x) * d) = Real.log (1 + x) + Real.log d :=
    Real.log_mul h1.ne' hd.ne'
  have hpos : (0 : ℝ) < 1 + j * d := by positivity
  have hmono : Real.log (1 + j * d) ≤ Real.log (1 + j * ((1 + x) * d)) := by
    apply Real.log_le_log hpos
    nlinarith [mul_nonneg (mul_nonneg hj hx) hd.le]
  have hprod := mul_le_mul_of_nonneg_left hmono (sub_nonneg.2 hα)
  rw [hlog]
  linarith

/-- `G((1 + x) d) ≤ G(d)`. -/
theorem Gs_scale_ge (α j d x : ℝ) (hα0 : 0 ≤ α) (hα : α ≤ 1) (hj : 0 ≤ j) (hd : 0 < d)
    (hx : 0 ≤ x) : Gs α j ((1 + x) * d) ≤ Gs α j d := by
  unfold Gs
  have h1 : (0 : ℝ) < 1 + x := by linarith
  have hlog : Real.log ((1 + x) * d) = Real.log (1 + x) + Real.log d :=
    Real.log_mul h1.ne' hd.ne'
  have hpos : (0 : ℝ) < 1 + j * d := by positivity
  have hpos2 : (0 : ℝ) < 1 + j * ((1 + x) * d) := by positivity
  have hle : Real.log (1 + j * ((1 + x) * d)) ≤ Real.log (1 + x) + Real.log (1 + j * d) := by
    rw [← Real.log_mul h1.ne' hpos.ne']
    apply Real.log_le_log hpos2
    nlinarith [mul_nonneg hj hd.le]
  have hl0 : 0 ≤ Real.log (1 + x) := Real.log_nonneg (by linarith)
  have hprod := mul_le_mul_of_nonneg_left hle (sub_nonneg.2 hα)
  have hαl := mul_nonneg hα0 hl0
  rw [hlog]
  nlinarith

/-- `G(c s) - G(s) ≤ ½ log(1/c)` for `0 < c ≤ 1`. -/
theorem Gs_shrink (α j s c : ℝ) (hα : α ≤ 1) (hj : 0 ≤ j) (hs : 0 < s) (hc : 0 < c)
    (hc1 : c ≤ 1) : Gs α j (c * s) - Gs α j s ≤ 1 / 2 * Real.log (1 / c) := by
  have hx : 0 ≤ 1 / c - 1 := by
    rw [sub_nonneg, le_div_iff₀ hc]
    linarith
  have h := Gs_scale_le α j (c * s) (1 / c - 1) hα hj (by positivity) hx
  have e2 : 1 + (1 / c - 1) = 1 / c := by ring
  have e1 : (1 + (1 / c - 1)) * (c * s) = s := by
    rw [e2, ← mul_assoc, one_div, inv_mul_cancel₀ hc.ne', one_mul]
  rw [e1, e2] at h
  linarith

/-- `⌈√N⌉ / N ≤ 2 / √N` for `N ≥ 1`. -/
theorem ceil_sqrt_div_le (N : ℕ) (hN : 1 ≤ N) :
    ((⌈Real.sqrt (N : ℝ)⌉₊ : ℕ) : ℝ) / (N : ℝ) ≤ 2 / Real.sqrt (N : ℝ) := by
  have hN1 : (1 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hNpos : (0 : ℝ) < (N : ℝ) := by linarith
  have hs1 : 1 ≤ Real.sqrt (N : ℝ) := by
    rw [Real.one_le_sqrt]
    exact hN1
  have hs0 : 0 < Real.sqrt (N : ℝ) := by linarith
  have hceil : ((⌈Real.sqrt (N : ℝ)⌉₊ : ℕ) : ℝ) < Real.sqrt (N : ℝ) + 1 :=
    Nat.ceil_lt_add_one hs0.le
  have hsq : Real.sqrt (N : ℝ) * Real.sqrt (N : ℝ) = (N : ℝ) := Real.mul_self_sqrt hNpos.le
  have h2 : ((⌈Real.sqrt (N : ℝ)⌉₊ : ℕ) : ℝ) ≤ 2 * Real.sqrt (N : ℝ) := by linarith
  have h3 := mul_le_mul_of_nonneg_right h2 hs0.le
  rw [div_le_div_iff₀ hNpos hs0]
  nlinarith

/-! ### Lemma "seeds": the two arithmetic steps -/

/-- `(2a + 2b)² ≤ 8a² + 8b²`. -/
theorem sq_two_add_le (a b : ℝ) : (2 * a + 2 * b) ^ 2 ≤ 8 * a ^ 2 + 8 * b ^ 2 := by
  nlinarith [sq_nonneg (a - b)]

/-- If `k > 3 v / δ²` then the Chebyshev bound `v / (k δ²)` is below `1/3`. -/
theorem chebyshev_count (v δ k : ℝ) (hv : 0 ≤ v) (hδ : 0 < δ) (hk : 3 * v / δ ^ 2 < k) :
    v / (k * δ ^ 2) < 1 / 3 := by
  have hδ2 : 0 < δ ^ 2 := by positivity
  have hk0 : 0 < k := lt_of_le_of_lt (by positivity) hk
  rw [div_lt_iff₀ hδ2] at hk
  rw [div_lt_iff₀ (by positivity)]
  linarith

end ObservationTheory.BeyondStationary
