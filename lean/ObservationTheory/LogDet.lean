/-
Log-concavity of the determinant on positive definite real matrices, toward formalizing the convexity results of
`paper/tit-rate-leakage/tit-rate-leakage.tex` (Theorem convex). Mathlib (v4.32.2) has the spectral theorem for
Hermitian matrices but not the concavity of log det, so it is built here.

* `det_conj_unitary`   det (U Z Uᴴ) = det Z for a unitary U.
* `det_affine_herm`    det (a I + b M) = ∏ (a + b λᵢ) for a symmetric M with eigenvalues λ.
* `det_rpow_le_det_combo`  det X ^ (1 - t) det Y ^ t ≤ det ((1 - t) X + t Y) for positive definite X, Y.
* `log_det_concave`    log det is concave on positive definite matrices.
* `neg_log_det_convex` the rate part of Theorem convex: -log det is convex.
* `det_le_det_of_loewner`  det is monotone in the Loewner order on positive definite matrices.
* `Phi_eq`, `Fw_concave`   completing the square for the fixed-gain error covariance, and matrix concavity of
                       F(X) = X - X Bᴴ (B X Bᴴ + I)⁻¹ B X = (X⁻¹ + Bᴴ B)⁻¹ (`Fw_eq_inv`).
* `neg_log_det_Fw_convex`  the leakage part of Theorem convex: -log det F is convex, so the leakage
                       ½ log det K - ½ log det (Σ_e0⁻¹ + J)⁻¹ is convex in Σ_e0 for J = Bᴴ B.
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

/-! ### The leakage part of Theorem convex -/

/-- Every positive definite real matrix has a symmetric square root with a symmetric inverse. -/
theorem exists_sqrt {X : Matrix n n ℝ} (hX : X.PosDef) :
    ∃ S Si : Matrix n n ℝ, S * S = X ∧ S * Si = 1 ∧ Si * S = 1 ∧ Siᴴ = Si ∧ Sᴴ = S := by
  set d := hX.1.eigenvalues with hd_def
  set U := hX.1.eigenvectorUnitary with hU_def
  have hdpos : ∀ i, 0 < d i := fun i => hX.eigenvalues_pos i
  have hXs : X = (U : Matrix n n ℝ) * diagonal d * star (U : Matrix n n ℝ) := by
    rw [hd_def, hU_def]
    conv_lhs => rw [hX.1.spectral_theorem]
    simp [RCLike.ofReal_real_eq_id, Unitary.conjStarAlgAut_apply]
  have hsq : ∀ i, Real.sqrt (d i) * Real.sqrt (d i) = d i := fun i => Real.mul_self_sqrt (hdpos i).le
  have hsqpos : ∀ i, 0 < Real.sqrt (d i) := fun i => Real.sqrt_pos.mpr (hdpos i)
  refine ⟨(U : Matrix n n ℝ) * diagonal (fun i => Real.sqrt (d i)) * star (U : Matrix n n ℝ),
    (U : Matrix n n ℝ) * diagonal (fun i => (Real.sqrt (d i))⁻¹) * star (U : Matrix n n ℝ), ?_, ?_, ?_,
    conj_diag_herm U _, conj_diag_herm U _⟩
  · rw [conj_diag_mul, hXs]; simp only [hsq]
  · rw [conj_diag_mul]
    have : (fun i => Real.sqrt (d i) * (Real.sqrt (d i))⁻¹) = fun _ => (1 : ℝ) := by
      funext i; exact mul_inv_cancel₀ (hsqpos i).ne'
    rw [this, diagonal_one, Matrix.mul_one]; exact Unitary.mul_star_self_of_mem U.2
  · rw [conj_diag_mul]
    have : (fun i => (Real.sqrt (d i))⁻¹ * Real.sqrt (d i)) = fun _ => (1 : ℝ) := by
      funext i; exact inv_mul_cancel₀ (hsqpos i).ne'
    rw [this, diagonal_one, Matrix.mul_one]; exact Unitary.mul_star_self_of_mem U.2

/-- **Loewner monotonicity of det.** If A is positive definite and B - A is positive semidefinite, then
det A ≤ det B. -/
theorem det_le_det_of_loewner {A B : Matrix n n ℝ} (hA : A.PosDef) (hBA : (B - A).PosSemidef) :
    A.det ≤ B.det := by
  obtain ⟨S, Si, hSS, hSSi, hSiS, hSiH, hSH⟩ := exists_sqrt hA
  set N := Si * (B - A) * Si with hN
  have hNpsd : N.PosSemidef := by
    have := hBA.conjTranspose_mul_mul_same Si
    rwa [hSiH] at this
  have hB : B = S * ((1 : ℝ) • (1 : Matrix n n ℝ) + (1 : ℝ) • N) * S := by
    have hSNS : S * N * S = B - A := by
      rw [hN]
      calc S * (Si * (B - A) * Si) * S = (S * Si) * (B - A) * (Si * S) := by simp only [Matrix.mul_assoc]
        _ = B - A := by rw [hSSi, hSiS, Matrix.one_mul, Matrix.mul_one]
    rw [one_smul, one_smul, Matrix.mul_add, Matrix.add_mul, Matrix.mul_one, hSS, hSNS]
    abel
  have hdet1 : 1 ≤ ((1 : ℝ) • (1 : Matrix n n ℝ) + (1 : ℝ) • N).det := by
    rw [det_affine_herm hNpsd.1]
    exact Finset.one_le_prod (fun i _ => by have := hNpsd.eigenvalues_nonneg i; linarith)
  have hS2 : S.det * S.det = A.det := by rw [← det_mul, hSS]
  have hA0 : 0 < A.det := hA.det_pos
  rw [hB, det_mul, det_mul]
  nlinarith [hdet1, hS2, hA0]

/-- A convex combination of positive definite matrices is positive definite. -/
theorem posDef_combo {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef) {t : ℝ} (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1) : ((1 - t) • X + t • Y).PosDef := by
  rcases eq_or_lt_of_le ht0 with h | h
  · subst h; simpa using hX
  · exact Matrix.PosDef.posSemidef_add (hX.posSemidef.smul (by linarith)) (hY.smul h)

section Leak

variable {m : Type*} [Fintype m] [DecidableEq m]

/-- G(X) = B X Bᴴ + I. -/
def Gm (B : Matrix m n ℝ) (X : Matrix n n ℝ) : Matrix m m ℝ := B * X * Bᴴ + 1

/-- F(X) = X - X Bᴴ G(X)⁻¹ B X, which equals (X⁻¹ + Bᴴ B)⁻¹ (`Fw_eq_inv`). -/
noncomputable def Fw (B : Matrix m n ℝ) (X : Matrix n n ℝ) : Matrix n n ℝ := X - X * Bᴴ * (Gm B X)⁻¹ * B * X

/-- The error covariance of the affine estimate with gain K: (I - K B) X (I - K B)ᴴ + K Kᴴ. -/
def Phi (B : Matrix m n ℝ) (K : Matrix n m ℝ) (X : Matrix n n ℝ) : Matrix n n ℝ :=
  (1 - K * B) * X * (1 - K * B)ᴴ + K * Kᴴ

theorem Gm_posDef (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) : (Gm B X).PosDef :=
  Matrix.PosDef.posSemidef_add (hX.posSemidef.mul_mul_conjTranspose_same B) Matrix.PosDef.one

/-- **Completing the square.** For every gain K, Φ_K(X) = F(X) + (K - K*) G (K - K*)ᴴ with
K* = X Bᴴ G⁻¹. -/
theorem Phi_eq (B : Matrix m n ℝ) (K : Matrix n m ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) :
    Phi B K X = Fw B X + (K - X * Bᴴ * (Gm B X)⁻¹) * Gm B X * (K - X * Bᴴ * (Gm B X)⁻¹)ᴴ := by
  have hXH : Xᴴ = X := hX.1
  set G := Gm B X with hG
  set P := G⁻¹ with hP
  have hGu : IsUnit G.det := (Gm_posDef B hX).isUnit.map (Matrix.detMonoidHom)
  have hGP : G * P = 1 := mul_nonsing_inv G hGu
  have hPG : P * G = 1 := nonsing_inv_mul G hGu
  have hGH : Gᴴ = G := (Gm_posDef B hX).1
  have hPH : Pᴴ = P := by rw [hP, conjTranspose_nonsing_inv, hGH]
  have hGPY : G * (P * (B * X)) = B * X := by rw [← Matrix.mul_assoc, hGP, Matrix.one_mul]
  have hPGY : P * (G * Kᴴ) = Kᴴ := by rw [← Matrix.mul_assoc, hPG, Matrix.one_mul]
  have hL : Phi B K X = X - K * (B * X) - X * (Bᴴ * Kᴴ) + K * (G * Kᴴ) := by
    simp only [Phi, hG, Gm, conjTranspose_sub, conjTranspose_one, conjTranspose_mul, Matrix.sub_mul,
      Matrix.mul_sub, Matrix.one_mul, Matrix.mul_one, Matrix.mul_add, Matrix.add_mul, Matrix.mul_assoc]
    abel
  rw [hL]
  simp only [Fw, ← hG, ← hP, conjTranspose_sub, conjTranspose_mul, conjTranspose_conjTranspose, hPH, hXH,
    Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_assoc, hGPY, hPGY]
  abel

/-- At the optimal gain the correction vanishes. -/
theorem Phi_opt (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) :
    Phi B (X * Bᴴ * (Gm B X)⁻¹) X = Fw B X := by
  rw [Phi_eq B _ hX]; simp

/-- **Matrix concavity of F.** F((1 - t) X₀ + t X₁) - ((1 - t) F(X₀) + t F(X₁)) is positive semidefinite. -/
theorem Fw_concave (B : Matrix m n ℝ) {X₀ X₁ : Matrix n n ℝ} (h₀ : X₀.PosDef) (h₁ : X₁.PosDef) {t : ℝ}
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    (Fw B ((1 - t) • X₀ + t • X₁) - ((1 - t) • Fw B X₀ + t • Fw B X₁)).PosSemidef := by
  have ht : (Matrix.PosDef ((1 - t) • X₀ + t • X₁)) := posDef_combo h₀ h₁ ht0 ht1
  set K := ((1 - t) • X₀ + t • X₁) * Bᴴ * (Gm B ((1 - t) • X₀ + t • X₁))⁻¹
  have haff : Phi B K ((1 - t) • X₀ + t • X₁) = (1 - t) • Phi B K X₀ + t • Phi B K X₁ := by
    simp only [Phi, Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul, smul_add]
    module
  rw [← Phi_opt B ht, haff, Phi_eq B K h₀, Phi_eq B K h₁]
  set P₀ := (K - X₀ * Bᴴ * (Gm B X₀)⁻¹) * Gm B X₀ * (K - X₀ * Bᴴ * (Gm B X₀)⁻¹)ᴴ
  set P₁ := (K - X₁ * Bᴴ * (Gm B X₁)⁻¹) * Gm B X₁ * (K - X₁ * Bᴴ * (Gm B X₁)⁻¹)ᴴ
  have hP₀ : P₀.PosSemidef := (Gm_posDef B h₀).posSemidef.mul_mul_conjTranspose_same _
  have hP₁ : P₁.PosSemidef := (Gm_posDef B h₁).posSemidef.mul_mul_conjTranspose_same _
  have : (1 - t) • (Fw B X₀ + P₀) + t • (Fw B X₁ + P₁) - ((1 - t) • Fw B X₀ + t • Fw B X₁) =
      (1 - t) • P₀ + t • P₁ := by
    simp only [smul_add]; abel
  rw [this]
  exact (hP₀.smul (by linarith)).add (hP₁.smul ht0)

/-- F(X) (X⁻¹ + Bᴴ B) = I. -/
theorem Fw_mul (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) : Fw B X * (X⁻¹ + Bᴴ * B) = 1 := by
  set G := Gm B X with hG
  set P := G⁻¹ with hP
  have hGu : IsUnit G.det := (Gm_posDef B hX).isUnit.map (Matrix.detMonoidHom)
  have hPG : P * G = 1 := nonsing_inv_mul G hGu
  have hXu : IsUnit X.det := hX.isUnit.map (Matrix.detMonoidHom)
  have hXX : X * X⁻¹ = 1 := mul_nonsing_inv X hXu
  have hBXB : B * X * Bᴴ = G - 1 := by rw [hG, Gm]; abel
  have hkey : P * (B * (X * (Bᴴ * B))) = B - P * B := by
    have : B * (X * (Bᴴ * B)) = (G - 1) * B := by rw [← hBXB]; simp only [Matrix.mul_assoc]
    rw [this, Matrix.sub_mul, Matrix.mul_sub, ← Matrix.mul_assoc, hPG, Matrix.one_mul]
  simp only [Fw, ← hG, ← hP, Matrix.sub_mul, Matrix.mul_add, Matrix.mul_assoc, hXX, hkey, Matrix.mul_one,
    Matrix.mul_sub]
  abel

/-- F(X) = (X⁻¹ + Bᴴ B)⁻¹, so F(X) is positive definite. -/
theorem Fw_eq_inv (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) : Fw B X = (X⁻¹ + Bᴴ * B)⁻¹ :=
  (inv_eq_left_inv (Fw_mul B hX)).symm

theorem Fw_posDef (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) : (Fw B X).PosDef := by
  rw [Fw_eq_inv B hX]
  exact Matrix.posDef_inv_iff.mpr ((Matrix.posDef_inv_iff.mpr hX).add_posSemidef
    (Matrix.posSemidef_conjTranspose_mul_self B))

/-- **Theorem convex, leakage part.** The leakage ½ log det K - ½ log det (Σ_e0⁻¹ + J)⁻¹ is convex in the error
covariance Σ_e0, with J = Bᴴ B: -log det F is convex on positive definite matrices. -/
theorem neg_log_det_Fw_convex (B : Matrix m n ℝ) {X₀ X₁ : Matrix n n ℝ} (h₀ : X₀.PosDef) (h₁ : X₁.PosDef)
    {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    -Real.log (Fw B ((1 - t) • X₀ + t • X₁)).det ≤
      (1 - t) * (-Real.log (Fw B X₀).det) + t * (-Real.log (Fw B X₁).det) := by
  have hF₀ := Fw_posDef B h₀; have hF₁ := Fw_posDef B h₁
  have hA := posDef_combo hF₀ hF₁ ht0 ht1
  have hmono := det_le_det_of_loewner hA (Fw_concave B h₀ h₁ ht0 ht1)
  have hlog := Real.log_le_log hA.det_pos hmono
  have hcc := log_det_concave hF₀ hF₁ ht0 ht1
  linarith

end Leak

end ObservationTheory.LogDet
