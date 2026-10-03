/-
Log-concavity of the determinant on positive definite real matrices, toward formalizing the convexity results of
`paper/tit-rate-leakage/tit-rate-leakage.tex` (Theorem convex). Mathlib (v4.32.2) has the spectral theorem for
Hermitian matrices but not the concavity of log det, so it is built here.

* `det_conj_unitary`   det (U Z Uᴴ) = det Z for a unitary U.
* `det_affine_herm`    det (a I + b M) = ∏ (a + b λᵢ) for a symmetric M with eigenvalues λ.
* `det_rpow_le_det_combo`  det X ^ (1 - t) det Y ^ t ≤ det ((1 - t) X + t Y) for positive definite X, Y.
* `log_det_concave`    log det is concave on positive definite matrices.
* `neg_log_det_convex` the rate part of Theorem convex: -log det is convex.

Not yet formalized: convexity of the leakage, which needs the Loewner monotonicity of log det and the
matrix concavity of X ↦ (X⁻¹ + J)⁻¹ (provable from the fixed-gain variational bound).
-/
import Mathlib

open Matrix

namespace ObservationTheory.LogDet

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Conjugation by a unitary matrix preserves the determinant. -/
theorem det_conj_unitary (U : unitary (Matrix n n ℝ)) (Z : Matrix n n ℝ) :
    ((U : Matrix n n ℝ) * Z * star (U : Matrix n n ℝ)).det = Z.det := by
  have h : (U : Matrix n n ℝ) * star (U : Matrix n n ℝ) = 1 := Unitary.mul_star_self_of_mem U.2
  calc ((U : Matrix n n ℝ) * Z * star (U : Matrix n n ℝ)).det
      = (U : Matrix n n ℝ).det * Z.det * (star (U : Matrix n n ℝ)).det := by rw [det_mul, det_mul]
    _ = Z.det * ((U : Matrix n n ℝ).det * (star (U : Matrix n n ℝ)).det) := by ring
    _ = Z.det := by rw [← det_mul, h, det_one, mul_one]

/-- For a symmetric real matrix with eigenvalues λ, det (a I + b M) = ∏ (a + b λᵢ). -/
theorem det_affine_herm {M : Matrix n n ℝ} (hM : M.IsHermitian) (a b : ℝ) :
    (a • (1 : Matrix n n ℝ) + b • M).det = ∏ i, (a + b * hM.eigenvalues i) := by
  set U := hM.eigenvectorUnitary
  have hU : (U : Matrix n n ℝ) * star (U : Matrix n n ℝ) = 1 := Unitary.mul_star_self_of_mem U.2
  have hspec : M = (U : Matrix n n ℝ) * diagonal (RCLike.ofReal ∘ hM.eigenvalues) * star (U : Matrix n n ℝ) := by
    conv_lhs => rw [hM.spectral_theorem]
    rfl
  have hsum : a • (1 : Matrix n n ℝ) + b • M =
      (U : Matrix n n ℝ) * (a • (1 : Matrix n n ℝ) + b • diagonal (RCLike.ofReal ∘ hM.eigenvalues)) *
        star (U : Matrix n n ℝ) := by
    conv_lhs => rw [hspec]
    simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_one, hU]
  rw [hsum, det_conj_unitary U]
  have hd : a • (1 : Matrix n n ℝ) + b • diagonal (RCLike.ofReal ∘ hM.eigenvalues) =
      diagonal (fun i => a + b * hM.eigenvalues i) := by
    ext i j
    by_cases h : i = j
    · subst h; simp [diagonal]
    · simp [diagonal, h]
  rw [hd, det_diagonal]

/-- Conjugating a diagonal matrix by a unitary, multiplicatively. -/
theorem conj_diag_mul (U : unitary (Matrix n n ℝ)) (f g : n → ℝ) :
    ((U : Matrix n n ℝ) * diagonal f * star (U : Matrix n n ℝ)) *
      ((U : Matrix n n ℝ) * diagonal g * star (U : Matrix n n ℝ)) =
      (U : Matrix n n ℝ) * diagonal (fun i => f i * g i) * star (U : Matrix n n ℝ) := by
  have h : star (U : Matrix n n ℝ) * (U : Matrix n n ℝ) = 1 := Unitary.star_mul_self_of_mem U.2
  calc ((U : Matrix n n ℝ) * diagonal f * star (U : Matrix n n ℝ)) *
        ((U : Matrix n n ℝ) * diagonal g * star (U : Matrix n n ℝ))
      = (U : Matrix n n ℝ) * diagonal f * (star (U : Matrix n n ℝ) * (U : Matrix n n ℝ)) * diagonal g *
          star (U : Matrix n n ℝ) := by simp only [Matrix.mul_assoc]
    _ = (U : Matrix n n ℝ) * (diagonal f * diagonal g) * star (U : Matrix n n ℝ) := by
          rw [h, Matrix.mul_one]; simp only [Matrix.mul_assoc]
    _ = _ := by rw [diagonal_mul_diagonal]

/-- A unitarily conjugated real diagonal matrix is symmetric. -/
theorem conj_diag_herm (U : unitary (Matrix n n ℝ)) (f : n → ℝ) :
    ((U : Matrix n n ℝ) * diagonal f * star (U : Matrix n n ℝ))ᴴ =
      (U : Matrix n n ℝ) * diagonal f * star (U : Matrix n n ℝ) := by
  rw [Matrix.conjTranspose_mul, Matrix.conjTranspose_mul, Matrix.diagonal_conjTranspose,
    Matrix.star_eq_conjTranspose, Matrix.conjTranspose_conjTranspose, Matrix.mul_assoc]
  simp

/-- The determinant of a unitarily conjugated diagonal matrix. -/
theorem det_conj_diag (U : unitary (Matrix n n ℝ)) (f : n → ℝ) :
    ((U : Matrix n n ℝ) * diagonal f * star (U : Matrix n n ℝ)).det = ∏ i, f i := by
  rw [det_conj_unitary, det_diagonal]

/-- **Log-concavity of the determinant.** For positive definite X, Y and t ∈ [0, 1],
det X ^ (1 - t) * det Y ^ t ≤ det ((1 - t) X + t Y). -/
theorem det_rpow_le_det_combo {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef) {t : ℝ}
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    X.det ^ (1 - t) * Y.det ^ t ≤ ((1 - t) • X + t • Y).det := by
  set d := hX.1.eigenvalues with hd_def
  set U := hX.1.eigenvectorUnitary with hU_def
  have hdpos : ∀ i, 0 < d i := fun i => hX.eigenvalues_pos i
  have hXs : X = (U : Matrix n n ℝ) * diagonal d * star (U : Matrix n n ℝ) := by
    rw [hd_def, hU_def]
    conv_lhs => rw [hX.1.spectral_theorem]
    simp [RCLike.ofReal_real_eq_id, Unitary.conjStarAlgAut_apply]
  set S := (U : Matrix n n ℝ) * diagonal (fun i => Real.sqrt (d i)) * star (U : Matrix n n ℝ) with hS
  set Si := (U : Matrix n n ℝ) * diagonal (fun i => (Real.sqrt (d i))⁻¹) * star (U : Matrix n n ℝ) with hSi
  have hsq : ∀ i, Real.sqrt (d i) * Real.sqrt (d i) = d i := fun i => Real.mul_self_sqrt (hdpos i).le
  have hsqpos : ∀ i, 0 < Real.sqrt (d i) := fun i => Real.sqrt_pos.mpr (hdpos i)
  have hSS : S * S = X := by
    rw [hS, conj_diag_mul, hXs]; simp only [hsq]
  have hSSi : S * Si = 1 := by
    rw [hS, hSi, conj_diag_mul]
    have : (fun i => Real.sqrt (d i) * (Real.sqrt (d i))⁻¹) = fun _ => (1 : ℝ) := by
      funext i; exact mul_inv_cancel₀ (hsqpos i).ne'
    rw [this, diagonal_one, Matrix.mul_one]
    exact Unitary.mul_star_self_of_mem U.2
  have hSiS : Si * S = 1 := by
    rw [hS, hSi, conj_diag_mul]
    have : (fun i => (Real.sqrt (d i))⁻¹ * Real.sqrt (d i)) = fun _ => (1 : ℝ) := by
      funext i; exact inv_mul_cancel₀ (hsqpos i).ne'
    rw [this, diagonal_one, Matrix.mul_one]
    exact Unitary.mul_star_self_of_mem U.2
  have hSiH : Siᴴ = Si := by rw [hSi]; exact conj_diag_herm U _
  set Mm := Si * Y * Si with hM
  have hMpd : Mm.PosDef := by
    have hinj : Function.Injective Si.mulVec := by
      intro x y hxy
      have := congrArg (fun v => S *ᵥ v) hxy
      simpa [Matrix.mulVec_mulVec, hSSi] using this
    have := hY.conjTranspose_mul_mul_same hinj
    rwa [hSiH] at this
  have hcombo : (1 - t) • X + t • Y = S * ((1 - t) • (1 : Matrix n n ℝ) + t • Mm) * S := by
    have hY' : S * Mm * S = Y := by
      rw [hM]
      calc S * (Si * Y * Si) * S = (S * Si) * Y * (Si * S) := by simp only [Matrix.mul_assoc]
        _ = Y := by rw [hSSi, hSiS, Matrix.one_mul, Matrix.mul_one]
    rw [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_smul, Matrix.smul_mul,
      Matrix.mul_one, hSS, hY']
  have hdetS : S.det * S.det = X.det := by rw [← det_mul, hSS]
  have hdetSi : Si.det * S.det = 1 := by rw [← det_mul, hSiS, det_one]
  have hXdet : 0 < X.det := hX.det_pos
  have hdetM : Mm.det = Y.det / X.det := by
    have hSi' : Si.det = (S.det)⁻¹ := eq_inv_of_mul_eq_one_left hdetSi
    have hSne : S.det ≠ 0 := by intro h; rw [h, mul_zero] at hdetSi; exact zero_ne_one hdetSi
    rw [hM, det_mul, det_mul, hSi', ← hdetS]
    field_simp
  have hev := hMpd.1
  have hprod : Mm.det = ∏ i, hev.eigenvalues i := by
    simpa [RCLike.ofReal_real_eq_id] using hev.det_eq_prod_eigenvalues
  have hlam : ∀ i, 0 < hev.eigenvalues i := fun i => hMpd.eigenvalues_pos i
  have hamgm : ∀ i, (hev.eigenvalues i) ^ t ≤ (1 - t) + t * hev.eigenvalues i := by
    intro i
    have := Real.geom_mean_le_arith_mean2_weighted (by linarith : (0:ℝ) ≤ 1 - t) ht0
      (zero_le_one) (hlam i).le (by ring : (1 - t) + t = 1)
    simpa [Real.one_rpow] using this
  have hprodle : ∏ i, (hev.eigenvalues i) ^ t ≤ ∏ i, ((1 - t) + t * hev.eigenvalues i) :=
    Finset.prod_le_prod (fun i _ => (Real.rpow_nonneg (hlam i).le t)) (fun i _ => hamgm i)
  have hrpow : ∏ i, (hev.eigenvalues i) ^ t = (Mm.det) ^ t := by
    rw [hprod, Real.finsetProd_rpow _ _ (fun i _ => (hlam i).le)]
  have hYdet : 0 < Y.det := hY.det_pos
  have hlhs : X.det ^ (1 - t) * Y.det ^ t = X.det * (Mm.det) ^ t := by
    rw [hdetM, Real.div_rpow hYdet.le hXdet.le, Real.rpow_sub hXdet, Real.rpow_one]
    field_simp
  have hsplit : (S * ((1 - t) • (1 : Matrix n n ℝ) + t • Mm) * S).det =
      S.det * ((1 - t) • (1 : Matrix n n ℝ) + t • Mm).det * S.det := by
    rw [det_mul (S * _) S, det_mul S _]
  rw [hlhs, hcombo, hsplit, det_affine_herm hev]
  calc X.det * Mm.det ^ t = (S.det * S.det) * Mm.det ^ t := by rw [hdetS]
    _ ≤ (S.det * S.det) * ∏ i, ((1 - t) + t * hev.eigenvalues i) := by
        rw [← hrpow]; exact mul_le_mul_of_nonneg_left hprodle (by rw [hdetS]; exact hXdet.le)
    _ = S.det * (∏ i, ((1 - t) + t * hev.eigenvalues i)) * S.det := by ring

/-- **Concavity of log det** on positive definite matrices. -/
theorem log_det_concave {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef) {t : ℝ}
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    (1 - t) * Real.log X.det + t * Real.log Y.det ≤ Real.log ((1 - t) • X + t • Y).det := by
  have hX0 := hX.det_pos; have hY0 := hY.det_pos
  have h := det_rpow_le_det_combo hX hY ht0 ht1
  have hpos : 0 < X.det ^ (1 - t) * Y.det ^ t := mul_pos (Real.rpow_pos_of_pos hX0 _) (Real.rpow_pos_of_pos hY0 _)
  have := Real.log_le_log hpos h
  rwa [Real.log_mul (Real.rpow_pos_of_pos hX0 _).ne' (Real.rpow_pos_of_pos hY0 _).ne',
    Real.log_rpow hX0, Real.log_rpow hY0] at this

/-- Theorem convex, rate part: the rate r = ½ log det Σ_T - ½ log det Σ_e0 is convex in the error covariance,
because - log det is convex on positive definite matrices. -/
theorem neg_log_det_convex {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef) {t : ℝ}
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    -Real.log ((1 - t) • X + t • Y).det ≤ (1 - t) * (-Real.log X.det) + t * (-Real.log Y.det) := by
  have := log_det_concave hX hY ht0 ht1
  linarith

end ObservationTheory.LogDet
