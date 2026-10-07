/-
**Theorem tilted** of `paper/tit-rate-leakage/tit-rate-leakage.tex` (water-filling on a tilted weight),
machine-checked except for the existence of Karush–Kuhn–Tucker multipliers (see the scope note below).

Notation follows the paper's whitened coordinates. `X` is the whitened error covariance, `Q` the whitened
decoder weight `Q̃`, `β = 1 - α ∈ [0, 1]` the weight on the holder, and `B` the holder's observation matrix
whitened by its noise, so that `B = Σ_U^{-1/2} H̃` and `H̃ᵀ (H̃ X H̃ᵀ + Σ_U)⁻¹ H̃ = Bᵀ (B X Bᵀ + I)⁻¹ B`
(`Gm B X = B X Bᵀ + I` in `LogDet.lean`). The weighted objective of the paper, in natural units and doubled, is
`obj β B X = -log det X + β log det (B X Bᵀ + I)`.

Reverse water-filling at level one on the spectrum of a symmetric `A` (the paper's `Φ`, eigenvalues
`min {1, 1/λ}`) is written without eigen-decompositions as `waterfill A = (I + (A - I)⁺)⁻¹`, where `⁺` is the
positive part of the continuous functional calculus: `I + (A - I)⁺` has eigenvalues `max {1, λ}`.

* `kkt_iff_waterfill` — the spectral core of the proof. For symmetric `A` and positive definite `X`, the KKT
  system `X ⪯ I`, `Θ ⪰ 0`, `Θ (I - X) = 0`, `X⁻¹ = A + 2Θ` holds for some `Θ` iff `X = waterfill A`. The
  forward direction is uniqueness of the positive/negative-part decomposition of `A - I`.
* `fixed_point_minimizes` — sufficiency. A fixed point `X = waterfill (Ã(X))` with an active budget
  `tr (Q X) = D` and `ν ≥ 0` minimizes the weighted objective over the feasible set
  `{Y ≻ 0, Y ⪯ I, tr (Q Y) ≤ D}`. Calculus-free: tangent bounds from `log x ≤ x - 1` and the fixed-gain
  (completing-the-square) bound `Phi_eq` of `LogDet.lean`.
* `minimizer_unique`, `tilted_waterfilling` — uniqueness by strict midpoint convexity of `log det`, and the
  assembled statement: every budget-active fixed point is THE frontier point.

Scope. This file checks everything after "Suppose these hold" in the paper's proof, and the converse. The
existence of the multipliers `ν > 0` and `Θ` at the frontier point (the paper's appeal to Slater's condition)
is proved in `TiltedExistence.lean` by a problem-specific route, because Mathlib has no KKT theorem for
matrix programs. The complete statement is `tilted_waterfilling_complete` there.
-/
import Mathlib
import ObservationTheory.LogDet

open Matrix
open scoped MatrixOrder

namespace ObservationTheory.Tilted

open ObservationTheory.LogDet

variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ### Small matrix facts -/

theorem isUnit_det_of_posDef {X : Matrix n n ℝ} (hX : X.PosDef) : IsUnit X.det :=
  hX.isUnit.map (Matrix.detMonoidHom)

/-- For positive definite `X = S S` with `S Si = I`, the inverse square root squares to `X⁻¹`. -/
theorem sqrt_inv_sq {X S Si : Matrix n n ℝ} (hX : X.PosDef) (hSS : S * S = X) (hSSi : S * Si = 1) :
    Si * Si = X⁻¹ := by
  have hu := isUnit_det_of_posDef hX
  have h1 : X * (Si * Si) = 1 := by
    rw [← hSS]
    calc S * S * (Si * Si) = S * (S * Si) * Si := by simp only [Matrix.mul_assoc]
      _ = 1 := by rw [hSSi, Matrix.mul_one, hSSi]
  calc Si * Si = X⁻¹ * (X * (Si * Si)) := by
        rw [← Matrix.mul_assoc, nonsing_inv_mul X hu, Matrix.one_mul]
    _ = X⁻¹ := by rw [h1, Matrix.mul_one]

/-- If `0 ≺ X ⪯ I` then `X⁻¹ - I ⪰ 0`. -/
theorem inv_sub_one_psd {X : Matrix n n ℝ} (hX : X.PosDef) (h1X : (1 - X).PosSemidef) :
    (X⁻¹ - 1).PosSemidef := by
  obtain ⟨S, Si, hSS, hSSi, hSiS, hSiH, _⟩ := exists_sqrt hX
  have hsq := sqrt_inv_sq hX hSS hSSi
  have hSiXSi : Si * X * Si = 1 := by
    rw [← hSS]
    calc Si * (S * S) * Si = (Si * S) * (S * Si) := by simp only [Matrix.mul_assoc]
      _ = 1 := by rw [hSiS, hSSi, Matrix.one_mul]
  have h := h1X.conjTranspose_mul_mul_same Si
  rw [hSiH] at h
  have : Si * (1 - X) * Si = X⁻¹ - 1 := by
    rw [Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_one, hsq, hSiXSi]
  rwa [this] at h

/-- If `P ⪰ I` (so `P ≻ 0`) then `I - P⁻¹ ⪰ 0`. -/
theorem one_sub_inv_psd {P : Matrix n n ℝ} (hP : P.PosDef) (hP1 : (P - 1).PosSemidef) :
    (1 - P⁻¹).PosSemidef := by
  obtain ⟨S, Si, hSS, hSSi, hSiS, hSiH, _⟩ := exists_sqrt hP
  have hsq := sqrt_inv_sq hP hSS hSSi
  have hSiPSi : Si * P * Si = 1 := by
    rw [← hSS]
    calc Si * (S * S) * Si = (Si * S) * (S * Si) := by simp only [Matrix.mul_assoc]
      _ = 1 := by rw [hSiS, hSSi, Matrix.one_mul]
  have h := hP1.conjTranspose_mul_mul_same Si
  rw [hSiH] at h
  have : Si * (P - 1) * Si = 1 - P⁻¹ := by
    rw [Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_one, hsq, hSiPSi]
  rwa [this] at h

/-! ### Reverse water-filling at level one -/

/-- Reverse water-filling at level one on the spectrum of `A`: eigenvalues `min {1, 1/λ}`. -/
noncomputable def waterfill (A : Matrix n n ℝ) : Matrix n n ℝ := (1 + (A - 1)⁺)⁻¹

theorem one_add_posPart_posDef (A : Matrix n n ℝ) : (1 + (A - 1)⁺).PosDef := by
  have h : 0 ≤ (A - 1)⁺ := CFC.posPart_nonneg _
  exact Matrix.PosDef.one.add_posSemidef (Matrix.nonneg_iff_posSemidef.mp h)

theorem waterfill_posDef (A : Matrix n n ℝ) : (waterfill A).PosDef :=
  Matrix.posDef_inv_iff.mpr (one_add_posPart_posDef A)

theorem one_sub_waterfill_psd (A : Matrix n n ℝ) : (1 - waterfill A).PosSemidef := by
  apply one_sub_inv_psd (one_add_posPart_posDef A)
  have : 1 + (A - 1)⁺ - 1 = (A - 1)⁺ := by abel
  rw [this]
  exact Matrix.nonneg_iff_posSemidef.mp (CFC.posPart_nonneg _)

/-- **The spectral core of Theorem tilted.** For symmetric `A` and positive definite `X`, the KKT system
`X ⪯ I`, `Θ ⪰ 0`, `Θ (I - X) = 0`, `X⁻¹ = A + 2Θ` is solvable iff `X` is reverse water-filling on `A`. -/
theorem kkt_iff_waterfill {A X : Matrix n n ℝ} (hA : A.IsHermitian) (hX : X.PosDef) :
    ((1 - X).PosSemidef ∧ ∃ Θ : Matrix n n ℝ, Θ.PosSemidef ∧ Θ * (1 - X) = 0 ∧ X⁻¹ = A + (2 : ℝ) • Θ) ↔
      X = waterfill A := by
  have hXu := isUnit_det_of_posDef hX
  constructor
  · rintro ⟨h1X, Θ, hΘ, hΘX, hinv⟩
    -- Θ = Θ X, hence (transposing) Θ = X Θ, hence X⁻¹ Θ = Θ.
    have hΘeq : Θ = Θ * X := by
      have : Θ * 1 - Θ * X = 0 := by rw [← Matrix.mul_sub]; exact hΘX
      rw [Matrix.mul_one] at this
      exact sub_eq_zero.mp this
    have hXΘ : Θ = X * Θ := by
      have h := congrArg Matrix.conjTranspose hΘeq
      rwa [Matrix.conjTranspose_mul, hΘ.1, hX.1] at h
    have hXiΘ : X⁻¹ * Θ = Θ := by
      conv_lhs => rw [hXΘ]
      rw [← Matrix.mul_assoc, nonsing_inv_mul X hXu, Matrix.one_mul]
    set b := X⁻¹ - 1 with hb
    set c := (2 : ℝ) • Θ with hc
    have hb0 : 0 ≤ b := Matrix.nonneg_iff_posSemidef.mpr (inv_sub_one_psd hX h1X)
    have hc0 : 0 ≤ c := Matrix.nonneg_iff_posSemidef.mpr (hΘ.smul (by norm_num))
    have habc : A - 1 = b - c := by rw [hb, hc, hinv]; abel
    have hbc : b * c = 0 := by
      rw [hb, hc, Matrix.sub_mul, Matrix.mul_smul, Matrix.one_mul, hXiΘ, sub_self]
    have hpos := (CFC.posPart_negPart_unique habc hbc hb0 hc0).1
    have : 1 + (A - 1)⁺ = X⁻¹ := by rw [hpos, hb]; abel
    rw [waterfill, this, Matrix.nonsing_inv_nonsing_inv X hXu]
  · intro hXw
    have hsa : IsSelfAdjoint (A - 1) := (hA.sub Matrix.isHermitian_one)
    set p := (A - 1)⁺
    set q := (A - 1)⁻
    have hp0 : 0 ≤ p := CFC.posPart_nonneg _
    have hq0 : 0 ≤ q := CFC.negPart_nonneg _
    have hpq : p - q = A - 1 := CFC.posPart_sub_negPart (A - 1) hsa
    have hqp : q * p = 0 := CFC.negPart_mul_posPart (A - 1)
    set P := 1 + p with hP
    have hPd : P.PosDef := one_add_posPart_posDef A
    have hPu := isUnit_det_of_posDef hPd
    have hXP : X = P⁻¹ := hXw
    have hXinv : X⁻¹ = P := by rw [hXP, Matrix.nonsing_inv_nonsing_inv P hPu]
    refine ⟨by rw [hXw]; exact one_sub_waterfill_psd A, (1 / 2 : ℝ) • q, ?_, ?_, ?_⟩
    · exact (Matrix.nonneg_iff_posSemidef.mp hq0).smul (by norm_num)
    · -- q P = q, so q P⁻¹ = q, so q (I - X) = 0.
      have hqP : q * P = q := by rw [hP, Matrix.mul_add, Matrix.mul_one, hqp, add_zero]
      have hqPi : q * P⁻¹ = q := by
        calc q * P⁻¹ = q * P * P⁻¹ := by rw [hqP]
          _ = q := by rw [Matrix.mul_assoc, mul_nonsing_inv P hPu, Matrix.mul_one]
      rw [hXP, Matrix.smul_mul, Matrix.mul_sub, Matrix.mul_one, hqPi, sub_self, smul_zero]
    · rw [hXinv, hP, smul_smul]
      norm_num
      have hA' : A = p - q + 1 := by rw [hpq]; abel
      rw [hA']; abel

/-! ### Trace and tangent inequalities -/

/-- `tr (Θ P) ≥ 0` for positive semidefinite `Θ` and `P`. -/
theorem trace_mul_psd_nonneg {Θ P : Matrix n n ℝ} (hΘ : Θ.PosSemidef) (hP : P.PosSemidef) :
    0 ≤ (Θ * P).trace := by
  have hΘ0 : 0 ≤ Θ := Matrix.nonneg_iff_posSemidef.mpr hΘ
  set R := CFC.sqrt Θ with hR
  have hRR : R * R = Θ := CFC.sqrt_mul_sqrt_self Θ hΘ0
  have hRH : Rᴴ = R := (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg Θ)).star_eq
  have hpsd : (R * P * R).PosSemidef := by
    have := hP.conjTranspose_mul_mul_same R
    rwa [hRH] at this
  have : (Θ * P).trace = (R * P * R).trace := by
    rw [← hRR, Matrix.mul_assoc, Matrix.trace_mul_comm R (R * P), Matrix.mul_assoc]
  rw [this]
  exact hpsd.trace_nonneg

/-- **Tangent bound for log det** (from `log x ≤ x - 1` on eigenvalues):
`log det (S + M) ≤ log det S + tr (S⁻¹ M)` for positive definite `S` and `S + M`. -/
theorem log_det_add_le {S M : Matrix n n ℝ} (hS : S.PosDef) (hSM : (S + M).PosDef) :
    Real.log (S + M).det ≤ Real.log S.det + (S⁻¹ * M).trace := by
  obtain ⟨R, Ri, hRR, hRRi, hRiR, hRiH, _⟩ := exists_sqrt hS
  have hsq := sqrt_inv_sq hS hRR hRRi
  set P := Ri * (S + M) * Ri with hPdef
  have hPpd : P.PosDef := by
    have hinj : Function.Injective Ri.mulVec := by
      intro x y hxy
      have := congrArg (fun v => R *ᵥ v) hxy
      simpa [Matrix.mulVec_mulVec, hRRi] using this
    have := hSM.conjTranspose_mul_mul_same hinj
    rwa [hRiH] at this
  have hSMeq : S + M = R * P * R := by
    rw [hPdef]
    calc S + M = (R * Ri) * (S + M) * (Ri * R) := by rw [hRRi, hRiR, Matrix.one_mul, Matrix.mul_one]
      _ = R * (Ri * (S + M) * Ri) * R := by simp only [Matrix.mul_assoc]
  have hdetR : R.det * R.det = S.det := by rw [← det_mul, hRR]
  have hdet : (S + M).det = S.det * P.det := by
    rw [hSMeq, det_mul, det_mul, ← hdetR]; ring
  have hS0 := hS.det_pos
  have hP0 := hPpd.det_pos
  have hlog : Real.log (S + M).det = Real.log S.det + Real.log P.det := by
    rw [hdet, Real.log_mul hS0.ne' hP0.ne']
  -- log det P ≤ tr (P - I)
  have hev := hPpd.1
  have hlam : ∀ i, 0 < hev.eigenvalues i := fun i => hPpd.eigenvalues_pos i
  have hdetP : P.det = ∏ i, hev.eigenvalues i := by
    simpa [RCLike.ofReal_real_eq_id] using hev.det_eq_prod_eigenvalues
  have htrP : P.trace = ∑ i, hev.eigenvalues i := by
    simpa [RCLike.ofReal_real_eq_id] using hev.trace_eq_sum_eigenvalues
  have hlogP : Real.log P.det ≤ (P - 1).trace := by
    rw [hdetP, Real.log_prod (fun i _ => (hlam i).ne'), Matrix.trace_sub, htrP, Matrix.trace_one]
    calc ∑ i, Real.log (hev.eigenvalues i) ≤ ∑ i, (hev.eigenvalues i - 1) :=
          Finset.sum_le_sum (fun i _ => Real.log_le_sub_one_of_pos (hlam i))
      _ = ∑ i, hev.eigenvalues i - (Fintype.card n : ℝ) := by
          rw [Finset.sum_sub_distrib]; simp
  have htr : (P - 1).trace = (S⁻¹ * M).trace := by
    have hRiSRi : Ri * S * Ri = 1 := by
      rw [← hRR]
      calc Ri * (R * R) * Ri = (Ri * R) * (R * Ri) := by simp only [Matrix.mul_assoc]
        _ = 1 := by rw [hRiR, hRRi, Matrix.one_mul]
    have : P - 1 = Ri * M * Ri := by
      rw [hPdef, Matrix.mul_add, Matrix.add_mul, hRiSRi]; abel
    rw [this, Matrix.mul_assoc, Matrix.trace_mul_comm Ri (M * Ri), Matrix.mul_assoc, hsq,
      Matrix.trace_mul_comm]
  linarith [hlog, hlogP, htr]

/-! ### The leakage part: tangent bound, objective identity, gradient -/

section Leak

variable {m : Type*} [Fintype m] [DecidableEq m]

theorem inv_isHermitian {X : Matrix n n ℝ} (hX : X.PosDef) : (X⁻¹)ᴴ = X⁻¹ := by
  rw [conjTranspose_nonsing_inv, hX.1]

theorem Fw_isHermitian (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) : (Fw B X)ᴴ = Fw B X :=
  (Fw_posDef B hX).1

/-- The optimal gain's complement: `I - L B = F(X) X⁻¹` with `L = X Bᴴ G(X)⁻¹`. -/
theorem one_sub_gain (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) :
    1 - X * Bᴴ * (Gm B X)⁻¹ * B = Fw B X * X⁻¹ := by
  have hu := isUnit_det_of_posDef hX
  have h : (1 - X * Bᴴ * (Gm B X)⁻¹ * B) * X = Fw B X := by
    simp only [Fw, Matrix.sub_mul, Matrix.one_mul, Matrix.mul_assoc]
  calc 1 - X * Bᴴ * (Gm B X)⁻¹ * B = (1 - X * Bᴴ * (Gm B X)⁻¹ * B) * X * X⁻¹ := by
        rw [Matrix.mul_assoc _ X, mul_nonsing_inv X hu, Matrix.mul_one]
    _ = Fw B X * X⁻¹ := by rw [h]

/-- **Gradient identity**: `X⁻¹ - X⁻¹ F(X) X⁻¹ = Bᴴ (B X Bᴴ + I)⁻¹ B`, the tilt of Theorem tilted. -/
theorem grad_identity (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) :
    X⁻¹ - X⁻¹ * Fw B X * X⁻¹ = Bᴴ * (Gm B X)⁻¹ * B := by
  have hu := isUnit_det_of_posDef hX
  have h1 : X⁻¹ * X = 1 := nonsing_inv_mul X hu
  have h2 : X * X⁻¹ = 1 := mul_nonsing_inv X hu
  simp only [Fw, Matrix.mul_sub, Matrix.sub_mul]
  have e1 : X⁻¹ * X * X⁻¹ = X⁻¹ := by rw [h1, Matrix.one_mul]
  have e2 : X⁻¹ * (X * Bᴴ * (Gm B X)⁻¹ * B * X) * X⁻¹ = Bᴴ * (Gm B X)⁻¹ * B := by
    simp only [← Matrix.mul_assoc, h1, Matrix.one_mul]
    simp only [Matrix.mul_assoc, h2, Matrix.mul_one]
  rw [e1, e2]; abel

/-- **Objective identity** (Weinstein–Aronszajn): `log det (B X Bᴴ + I) = log det X - log det F(X)`. -/
theorem log_det_Gm (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) :
    Real.log (Gm B X).det = Real.log X.det - Real.log (Fw B X).det := by
  have hu := isUnit_det_of_posDef hX
  have hW : (Gm B X).det = (Bᴴ * B * X + 1).det := by
    rw [Gm, det_mul_add_one_comm (B * X) Bᴴ, Matrix.mul_assoc]
  have hfac : Bᴴ * B * X + 1 = (X⁻¹ + Bᴴ * B) * X := by
    rw [Matrix.add_mul, nonsing_inv_mul X hu, add_comm]
  have hFw : (Fw B X).det * (X⁻¹ + Bᴴ * B).det = 1 := by
    rw [← det_mul, Fw_mul B hX, det_one]
  have hX0 := hX.det_pos
  have hF0 := (Fw_posDef B hX).det_pos
  have hinv : (X⁻¹ + Bᴴ * B).det = ((Fw B X).det)⁻¹ := eq_inv_of_mul_eq_one_right hFw
  rw [hW, hfac, det_mul, hinv, Real.log_mul (inv_pos.mpr hF0).ne' hX0.ne', Real.log_inv]
  ring

/-- **Tangent bound for the leakage part.** `-log det F` lies above its tangent at `X`:
`-log det F(Y) ≥ -log det F(X) - tr (X⁻¹ F(X) X⁻¹ (Y - X))`. Uses the fixed-gain bound `Phi_eq`. -/
theorem neg_log_det_Fw_tangent (B : Matrix m n ℝ) {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef) :
    -Real.log (Fw B X).det - (X⁻¹ * Fw B X * X⁻¹ * (Y - X)).trace ≤ -Real.log (Fw B Y).det := by
  set L := X * Bᴴ * (Gm B X)⁻¹ with hL
  set K := 1 - L * B with hK
  set S := Fw B X with hSdef
  have hSpd : S.PosDef := Fw_posDef B hX
  have hK' : K = S * X⁻¹ := by rw [hK, hL, hSdef]; exact one_sub_gain B hX
  -- Φ_L(Y) = F(Y) + PSD, Φ_L(X) = F(X), Φ_L affine in its argument.
  have hPhiY := Phi_eq B L hY
  have hPhiX : Phi B L X = S := Phi_opt B hX
  have haff : Phi B L Y = Phi B L X + K * (Y - X) * Kᴴ := by
    simp only [Phi, hK, Matrix.mul_sub, Matrix.sub_mul]; abel
  set Mm := K * (Y - X) * Kᴴ with hMm
  have hgap : (S + Mm - Fw B Y).PosSemidef := by
    have : S + Mm - Fw B Y = (L - Y * Bᴴ * (Gm B Y)⁻¹) * Gm B Y * (L - Y * Bᴴ * (Gm B Y)⁻¹)ᴴ := by
      rw [← hPhiX, ← haff, hPhiY]; abel
    rw [this]
    exact (Gm_posDef B hY).posSemidef.mul_mul_conjTranspose_same _
  have hSMpd : (S + Mm).PosDef := by
    have : S + Mm = Fw B Y + (S + Mm - Fw B Y) := by abel
    rw [this]; exact (Fw_posDef B hY).add_posSemidef hgap
  have hmono := det_le_det_of_loewner (Fw_posDef B hY) hgap
  have hlogmono := Real.log_le_log (Fw_posDef B hY).det_pos hmono
  have htan := log_det_add_le hSpd hSMpd
  have htr : (S⁻¹ * Mm).trace = (X⁻¹ * S * X⁻¹ * (Y - X)).trace := by
    have hSu := isUnit_det_of_posDef hSpd
    have hKH : Kᴴ = X⁻¹ * S := by
      rw [hK', conjTranspose_mul, inv_isHermitian hX, Fw_isHermitian B hX]
    have hcore : Kᴴ * S⁻¹ * K = X⁻¹ * S * X⁻¹ := by
      rw [hKH, hK']
      calc X⁻¹ * S * S⁻¹ * (S * X⁻¹) = X⁻¹ * (S * S⁻¹) * S * X⁻¹ := by simp only [Matrix.mul_assoc]
        _ = X⁻¹ * S * X⁻¹ := by rw [mul_nonsing_inv S hSu, Matrix.mul_one]
    rw [hMm, ← hcore]
    rw [show S⁻¹ * (K * (Y - X) * Kᴴ) = (S⁻¹ * K * (Y - X)) * Kᴴ by simp only [Matrix.mul_assoc],
      Matrix.trace_mul_comm]
    simp only [Matrix.mul_assoc]
  linarith [hlogmono, htan, htr]

end Leak

/-! ### Sufficiency: a budget-active fixed point is a minimizer -/

section Program

variable {m : Type*} [Fintype m] [DecidableEq m]

/-- The weighted objective of the paper in natural units, doubled: `-log det X + β log det (B X Bᴴ + I)`,
with `β = 1 - α`. -/
noncomputable def obj (β : ℝ) (B : Matrix m n ℝ) (X : Matrix n n ℝ) : ℝ :=
  -Real.log X.det + β * Real.log (Gm B X).det

/-- The tilted weight `Ã(X) = 2ν Q + β Bᴴ (B X Bᴴ + I)⁻¹ B` of Theorem tilted. -/
noncomputable def tilt (ν β : ℝ) (Q : Matrix n n ℝ) (B : Matrix m n ℝ) (X : Matrix n n ℝ) :
    Matrix n n ℝ :=
  (2 * ν) • Q + β • (Bᴴ * (Gm B X)⁻¹ * B)

/-- The feasible set `{Y ≻ 0, Y ⪯ I, tr (Q Y) ≤ D}` (whitened, so the cap `Σ_e0 ⪯ Σ_T` is `Y ⪯ I`). -/
def Feasible (Q : Matrix n n ℝ) (D : ℝ) (Y : Matrix n n ℝ) : Prop :=
  Y.PosDef ∧ (1 - Y).PosSemidef ∧ (Q * Y).trace ≤ D

theorem tilt_isHermitian (B : Matrix m n ℝ) {Q X : Matrix n n ℝ} (ν β : ℝ) (hQ : Q.IsHermitian)
    (hX : X.PosDef) : (tilt ν β Q B X).IsHermitian := by
  have hG : (Gm B X)ᴴ = Gm B X := (Gm_posDef B hX).1
  unfold Matrix.IsHermitian tilt
  rw [conjTranspose_add, conjTranspose_smul, conjTranspose_smul, conjTranspose_mul, conjTranspose_mul,
    conjTranspose_conjTranspose, conjTranspose_nonsing_inv, hG, hQ.eq]
  simp [Matrix.mul_assoc]

theorem obj_eq (β : ℝ) (B : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) :
    obj β B X = -(1 - β) * Real.log X.det - β * Real.log (Fw B X).det := by
  unfold obj; rw [log_det_Gm B hX]; ring

/-- **Theorem tilted, sufficiency.** If `X = Φ(Ã(X))` for some `ν ≥ 0` and the budget is active,
`tr (Q X) = D`, then `X` minimizes the weighted objective over the feasible set. -/
theorem fixed_point_minimizes (B : Matrix m n ℝ) {Q X Y : Matrix n n ℝ} {β ν D : ℝ}
    (hQ : Q.PosSemidef) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) (hν : 0 ≤ ν)
    (hfix : X = waterfill (tilt ν β Q B X)) (hD : (Q * X).trace = D) (hY : Feasible Q D Y) :
    obj β B X ≤ obj β B Y := by
  have hX : X.PosDef := by rw [hfix]; exact waterfill_posDef _
  obtain ⟨hYpd, h1Y, hQY⟩ := hY
  obtain ⟨_, Θ, hΘ, hΘX, hinv⟩ :=
    (kkt_iff_waterfill (tilt_isHermitian B ν β hQ.1 hX) hX).mpr hfix
  -- tangent bounds
  have hr : Real.log Y.det ≤ Real.log X.det + (X⁻¹ * (Y - X)).trace := by
    have h := log_det_add_le hX (show (X + (Y - X)).PosDef by rwa [add_sub_cancel])
    rwa [add_sub_cancel] at h
  have hl := neg_log_det_Fw_tangent B hX hYpd
  -- the gradient at X equals 2ν Q + 2Θ
  have hgrad : (1 - β) • X⁻¹ + β • (X⁻¹ * Fw B X * X⁻¹) = (2 * ν) • Q + (2 : ℝ) • Θ := by
    have hg := grad_identity B hX
    calc (1 - β) • X⁻¹ + β • (X⁻¹ * Fw B X * X⁻¹) = X⁻¹ - β • (X⁻¹ - X⁻¹ * Fw B X * X⁻¹) := by
          module
      _ = X⁻¹ - β • (Bᴴ * (Gm B X)⁻¹ * B) := by rw [hg]
      _ = (2 * ν) • Q + (2 : ℝ) • Θ := by rw [hinv, tilt]; abel
  set T1 := (X⁻¹ * (Y - X)).trace
  set T2 := (X⁻¹ * Fw B X * X⁻¹ * (Y - X)).trace
  have e1 : (((1 - β) • X⁻¹ + β • (X⁻¹ * Fw B X * X⁻¹)) * (Y - X)).trace = (1 - β) * T1 + β * T2 := by
    simp only [Matrix.add_mul, Matrix.smul_mul, Matrix.trace_add, Matrix.trace_smul, smul_eq_mul, T1, T2]
  have e2 : (((2 * ν) • Q + (2 : ℝ) • Θ) * (Y - X)).trace =
      2 * ν * ((Q * Y).trace - (Q * X).trace) + 2 * ((Θ * Y).trace - (Θ * X).trace) := by
    simp only [Matrix.add_mul, Matrix.smul_mul, Matrix.trace_add, Matrix.trace_smul, smul_eq_mul,
      Matrix.mul_sub, Matrix.trace_sub]
    ring
  -- sign of the two pieces
  have hΘX' : Θ * X = Θ := by
    have : Θ * 1 - Θ * X = 0 := by rw [← Matrix.mul_sub]; exact hΘX
    rw [Matrix.mul_one] at this; exact (sub_eq_zero.mp this).symm
  have hΘY : (Θ * Y).trace ≤ (Θ * X).trace := by
    have h := trace_mul_psd_nonneg hΘ h1Y
    rw [Matrix.mul_sub, Matrix.trace_sub, Matrix.mul_one] at h
    rw [hΘX']; linarith
  have hQpart : 2 * ν * ((Q * Y).trace - (Q * X).trace) ≤ 0 := by
    have : (Q * Y).trace - (Q * X).trace ≤ 0 := by rw [hD]; linarith
    nlinarith
  have hsum : (1 - β) * T1 + β * T2 ≤ 0 := by
    rw [← e1, hgrad, e2]; linarith
  rw [obj_eq β B hX, obj_eq β B hYpd]
  have h1 : (1 - β) * Real.log Y.det ≤ (1 - β) * (Real.log X.det + T1) :=
    mul_le_mul_of_nonneg_left hr (by linarith)
  have h2 : β * (-Real.log (Fw B X).det - T2) ≤ β * (-Real.log (Fw B Y).det) :=
    mul_le_mul_of_nonneg_left hl hβ0
  nlinarith

end Program

/-! ### Uniqueness: strict midpoint convexity -/

/-- A symmetric matrix whose eigenvalues are all `1` is the identity. -/
theorem eq_one_of_eigenvalues_one {M : Matrix n n ℝ} (hM : M.IsHermitian) (h : ∀ i, hM.eigenvalues i = 1) :
    M = 1 := by
  set U := hM.eigenvectorUnitary
  have hspec : M = (U : Matrix n n ℝ) * diagonal (RCLike.ofReal ∘ hM.eigenvalues) * star (U : Matrix n n ℝ) := by
    conv_lhs => rw [hM.spectral_theorem]
    rfl
  have hd : diagonal (RCLike.ofReal ∘ hM.eigenvalues : n → ℝ) = 1 := by
    rw [← diagonal_one]; congr 1; funext i; simp [h i]
  rw [hspec, hd, Matrix.mul_one]
  exact Unitary.mul_star_self_of_mem U.2

/-- `½ log μ ≤ log ((1 + μ)/2)` for `μ > 0` (AM–GM). -/
theorem half_log_le (μ : ℝ) (hμ : 0 < μ) : Real.log μ / 2 ≤ Real.log ((1 + μ) / 2) := by
  rw [← Real.log_sqrt hμ.le]
  apply Real.log_le_log (Real.sqrt_pos.mpr hμ)
  nlinarith [Real.sq_sqrt hμ.le, sq_nonneg (Real.sqrt μ - 1)]

/-- The same, strictly, unless `μ = 1`. -/
theorem half_log_lt (μ : ℝ) (hμ : 0 < μ) (h1 : μ ≠ 1) : Real.log μ / 2 < Real.log ((1 + μ) / 2) := by
  rw [← Real.log_sqrt hμ.le]
  apply Real.log_lt_log (Real.sqrt_pos.mpr hμ)
  have hs : Real.sqrt μ ≠ 1 := by
    intro h; apply h1
    have := Real.sq_sqrt hμ.le; rw [h] at this; linarith
  have hpos : 0 < (Real.sqrt μ - 1) ^ 2 := by
    have : Real.sqrt μ - 1 ≠ 0 := sub_ne_zero.mpr hs
    positivity
  nlinarith [Real.sq_sqrt hμ.le]

/-- **Strict midpoint concavity of log det.** -/
theorem log_det_mid_strict {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef) (hXY : X ≠ Y) :
    Real.log X.det / 2 + Real.log Y.det / 2 < Real.log ((1 / 2 : ℝ) • X + (1 / 2 : ℝ) • Y).det := by
  obtain ⟨S, Si, hSS, hSSi, hSiS, hSiH, _⟩ := exists_sqrt hX
  set Mm := Si * Y * Si with hMdef
  have hMpd : Mm.PosDef := by
    have hinj : Function.Injective Si.mulVec := by
      intro x y hxy
      have := congrArg (fun v => S *ᵥ v) hxy
      simpa [Matrix.mulVec_mulVec, hSSi] using this
    have := hY.conjTranspose_mul_mul_same hinj
    rwa [hSiH] at this
  have hY' : S * Mm * S = Y := by
    rw [hMdef]
    calc S * (Si * Y * Si) * S = (S * Si) * Y * (Si * S) := by simp only [Matrix.mul_assoc]
      _ = Y := by rw [hSSi, hSiS, Matrix.one_mul, Matrix.mul_one]
  have hcombo : (1 / 2 : ℝ) • X + (1 / 2 : ℝ) • Y =
      S * ((1 / 2 : ℝ) • (1 : Matrix n n ℝ) + (1 / 2 : ℝ) • Mm) * S := by
    rw [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_smul, Matrix.smul_mul,
      Matrix.mul_one, hSS, hY']
  have hdetS : S.det * S.det = X.det := by rw [← det_mul, hSS]
  have hX0 := hX.det_pos
  have hM0 := hMpd.det_pos
  have hdetY : Y.det = X.det * Mm.det := by rw [← hY', det_mul, det_mul, ← hdetS]; ring
  have hev := hMpd.1
  have hlam : ∀ i, 0 < hev.eigenvalues i := fun i => hMpd.eigenvalues_pos i
  have hdetM : Mm.det = ∏ i, hev.eigenvalues i := by
    simpa [RCLike.ofReal_real_eq_id] using hev.det_eq_prod_eigenvalues
  have haff : ((1 / 2 : ℝ) • (1 : Matrix n n ℝ) + (1 / 2 : ℝ) • Mm).det =
      ∏ i, ((1 + hev.eigenvalues i) / 2) := by
    rw [det_affine_herm hev]; congr 1; funext i; ring
  have hne : ∃ i, hev.eigenvalues i ≠ 1 := by
    by_contra hall
    push Not at hall
    apply hXY
    have hM1 := eq_one_of_eigenvalues_one hev hall
    rw [← hY', hM1, Matrix.mul_one, hSS]
  have hsum : ∑ i, Real.log (hev.eigenvalues i) / 2 < ∑ i, Real.log ((1 + hev.eigenvalues i) / 2) := by
    obtain ⟨j, hj⟩ := hne
    exact Finset.sum_lt_sum (fun i _ => half_log_le _ (hlam i))
      ⟨j, Finset.mem_univ j, half_log_lt _ (hlam j) hj⟩
  have hpos : ∀ i, 0 < (1 + hev.eigenvalues i) / 2 := fun i => by have := hlam i; positivity
  have hSne : S.det ≠ 0 := by intro h; rw [h, zero_mul] at hdetS; linarith
  have hprod_pos : 0 < ∏ i, ((1 + hev.eigenvalues i) / 2) := Finset.prod_pos (fun i _ => hpos i)
  have hlogZ : Real.log ((1 / 2 : ℝ) • X + (1 / 2 : ℝ) • Y).det =
      Real.log X.det + ∑ i, Real.log ((1 + hev.eigenvalues i) / 2) := by
    rw [hcombo, det_mul, det_mul, haff, Real.log_mul (mul_ne_zero hSne hprod_pos.ne') hSne,
      Real.log_mul hSne hprod_pos.ne', Real.log_prod (fun i _ => (hpos i).ne'), ← hdetS,
      Real.log_mul hSne hSne]
    ring
  have hlogY : Real.log Y.det = Real.log X.det + ∑ i, Real.log (hev.eigenvalues i) := by
    rw [hdetY, Real.log_mul hX0.ne' hM0.ne', hdetM, Real.log_prod (fun i _ => (hlam i).ne')]
  rw [hlogZ, hlogY]
  rw [← Finset.sum_div] at hsum
  linarith

section Unique

variable {m : Type*} [Fintype m] [DecidableEq m]

theorem Fw_injective (B : Matrix m n ℝ) {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef)
    (h : Fw B X = Fw B Y) : X = Y := by
  rw [Fw_eq_inv B hX, Fw_eq_inv B hY] at h
  have hu1 : IsUnit (X⁻¹ + Bᴴ * B).det := isUnit_det_of_posDef
    ((Matrix.posDef_inv_iff.mpr hX).add_posSemidef (Matrix.posSemidef_conjTranspose_mul_self B))
  have hu2 : IsUnit (Y⁻¹ + Bᴴ * B).det := isUnit_det_of_posDef
    ((Matrix.posDef_inv_iff.mpr hY).add_posSemidef (Matrix.posSemidef_conjTranspose_mul_self B))
  have h1 : X⁻¹ + Bᴴ * B = Y⁻¹ + Bᴴ * B := by
    rw [← Matrix.nonsing_inv_nonsing_inv _ hu1, h, Matrix.nonsing_inv_nonsing_inv _ hu2]
  have h2 : X⁻¹ = Y⁻¹ := add_right_cancel h1
  rw [← Matrix.nonsing_inv_nonsing_inv X (isUnit_det_of_posDef hX), h2,
    Matrix.nonsing_inv_nonsing_inv Y (isUnit_det_of_posDef hY)]

theorem posDef_mid {X Y : Matrix n n ℝ} (hX : X.PosDef) (hY : Y.PosDef) :
    ((1 / 2 : ℝ) • X + (1 / 2 : ℝ) • Y).PosDef := by
  have := posDef_combo hX hY (t := 1 / 2) (by norm_num) (by norm_num)
  have h : (1 : ℝ) - 1 / 2 = 1 / 2 := by norm_num
  rwa [h] at this

theorem feasible_mid {Q X Y : Matrix n n ℝ} {D : ℝ} (hX : Feasible Q D X) (hY : Feasible Q D Y) :
    Feasible Q D ((1 / 2 : ℝ) • X + (1 / 2 : ℝ) • Y) := by
  obtain ⟨hXpd, h1X, hQX⟩ := hX
  obtain ⟨hYpd, h1Y, hQY⟩ := hY
  refine ⟨posDef_mid hXpd hYpd, ?_, ?_⟩
  · have : 1 - ((1 / 2 : ℝ) • X + (1 / 2 : ℝ) • Y) = (1 / 2 : ℝ) • (1 - X) + (1 / 2 : ℝ) • (1 - Y) := by
      module
    rw [this]; exact (h1X.smul (by norm_num)).add (h1Y.smul (by norm_num))
  · rw [Matrix.mul_add, Matrix.mul_smul, Matrix.mul_smul, Matrix.trace_add, Matrix.trace_smul,
      Matrix.trace_smul, smul_eq_mul, smul_eq_mul]
    linarith

/-- **Strict midpoint convexity of the weighted objective.** -/
theorem obj_mid_strict (B : Matrix m n ℝ) {β : ℝ} (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) {X Y : Matrix n n ℝ}
    (hX : X.PosDef) (hY : Y.PosDef) (hXY : X ≠ Y) :
    obj β B ((1 / 2 : ℝ) • X + (1 / 2 : ℝ) • Y) < obj β B X / 2 + obj β B Y / 2 := by
  have hZ := posDef_mid hX hY
  have hFX := Fw_posDef B hX
  have hFY := Fw_posDef B hY
  have h12 : (1 : ℝ) - 1 / 2 = 1 / 2 := by norm_num
  have hc := log_det_concave hX hY (t := 1 / 2) (by norm_num) (by norm_num)
  have hcF := neg_log_det_Fw_convex B hX hY (t := 1 / 2) (by norm_num) (by norm_num)
  rw [h12] at hc hcF
  rw [obj_eq β B hX, obj_eq β B hY, obj_eq β B hZ]
  rcases lt_or_eq_of_le hβ1 with hlt | heq
  · have hs := log_det_mid_strict hX hY hXY
    have hb : 0 < 1 - β := by linarith
    have k1 := mul_lt_mul_of_pos_left hs hb
    have k2 := mul_le_mul_of_nonneg_left hcF hβ0
    nlinarith
  · subst heq
    have hFne : Fw B X ≠ Fw B Y := fun h => hXY (Fw_injective B hX hY h)
    have hs := log_det_mid_strict hFX hFY hFne
    have hmid := Fw_concave B hX hY (t := 1 / 2) (by norm_num) (by norm_num)
    rw [h12] at hmid
    have hA := posDef_mid hFX hFY
    have hmono := det_le_det_of_loewner hA hmid
    have hlog := Real.log_le_log hA.det_pos hmono
    nlinarith

/-- **Uniqueness of the minimizer.** -/
theorem minimizer_unique (B : Matrix m n ℝ) {Q : Matrix n n ℝ} {β D : ℝ} (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1)
    {X Y : Matrix n n ℝ} (hX : Feasible Q D X) (hY : Feasible Q D Y)
    (hXmin : ∀ Z, Feasible Q D Z → obj β B X ≤ obj β B Z)
    (hYmin : ∀ Z, Feasible Q D Z → obj β B Y ≤ obj β B Z) : X = Y := by
  by_contra hne
  have h1 := hXmin _ (feasible_mid hX hY)
  have h2 := hXmin _ hY
  have h3 := hYmin _ hX
  have hs := obj_mid_strict B hβ0 hβ1 hX.1 hY.1 hne
  linarith

/-- **Theorem tilted**, all but the existence of the multipliers. If `X = Φ(Ã(X))` for some `ν ≥ 0` with
the budget active, then `X` is feasible, minimizes the weighted objective over the feasible set, and is the
only minimizer. In particular two budget-active fixed points, for any multipliers, coincide. -/
theorem tilted_waterfilling (B : Matrix m n ℝ) {Q X : Matrix n n ℝ} {β ν D : ℝ}
    (hQ : Q.PosSemidef) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) (hν : 0 ≤ ν)
    (hfix : X = waterfill (tilt ν β Q B X)) (hD : (Q * X).trace = D) :
    Feasible Q D X ∧ (∀ Y, Feasible Q D Y → obj β B X ≤ obj β B Y) ∧
      (∀ Y, Feasible Q D Y → (∀ Z, Feasible Q D Z → obj β B Y ≤ obj β B Z) → Y = X) := by
  have hXf : Feasible Q D X := by
    refine ⟨?_, ?_, hD.le⟩
    · rw [hfix]; exact waterfill_posDef _
    · rw [hfix]; exact one_sub_waterfill_psd _
  have hmin : ∀ Y, Feasible Q D Y → obj β B X ≤ obj β B Y :=
    fun Y hY => fixed_point_minimizes B hQ hβ0 hβ1 hν hfix hD hY
  exact ⟨hXf, hmin, fun Y hY hYmin => minimizer_unique B hβ0 hβ1 hY hXf hYmin hmin⟩

/-- Two budget-active fixed points, for any multipliers `ν₁, ν₂ ≥ 0`, are equal. -/
theorem fixed_point_unique (B : Matrix m n ℝ) {Q X₁ X₂ : Matrix n n ℝ} {β ν₁ ν₂ D : ℝ}
    (hQ : Q.PosSemidef) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) (hν₁ : 0 ≤ ν₁) (hν₂ : 0 ≤ ν₂)
    (h₁ : X₁ = waterfill (tilt ν₁ β Q B X₁)) (hD₁ : (Q * X₁).trace = D)
    (h₂ : X₂ = waterfill (tilt ν₂ β Q B X₂)) (hD₂ : (Q * X₂).trace = D) : X₁ = X₂ := by
  obtain ⟨hf₁, hm₁, _⟩ := tilted_waterfilling B hQ hβ0 hβ1 hν₁ h₁ hD₁
  obtain ⟨hf₂, hm₂, _⟩ := tilted_waterfilling B hQ hβ0 hβ1 hν₂ h₂ hD₂
  exact minimizer_unique B hβ0 hβ1 hf₁ hf₂ hm₁ hm₂

end Unique

/-! ### Back to the paper's coordinates: whitening the holder's noise -/

section Whiten

variable {m : Type*} [Fintype m] [DecidableEq m]

omit [DecidableEq n] in
/-- With `Σ_U = R R` for a symmetric invertible `R` (inverse `Ri`) and `B = Ri H`, the paper's tilt term
`Hᴴ (H X Hᴴ + Σ_U)⁻¹ H` equals `Bᴴ (B X Bᴴ + I)⁻¹ B`, and
`log det (H X Hᴴ + Σ_U) = log det (B X Bᴴ + I) + log det Σ_U`. So `obj` and `tilt` are the paper's
objective (up to the constant `β log det Σ_U` and a factor `2`) and tilted weight. -/
theorem whiten_tilt (H : Matrix m n ℝ) (X : Matrix n n ℝ) {R Ri : Matrix m m ℝ}
    (hRRi : R * Ri = 1) (hRH : Rᴴ = R) (hRiH : Riᴴ = Ri) :
    Hᴴ * (H * X * Hᴴ + R * R)⁻¹ * H = (Ri * H)ᴴ * (Gm (Ri * H) X)⁻¹ * (Ri * H) := by
  set B := Ri * H with hB
  have hHB : H = R * B := by rw [hB, ← Matrix.mul_assoc, hRRi, Matrix.one_mul]
  have hBH : Bᴴ = Hᴴ * Ri := by rw [hB, conjTranspose_mul, hRiH]
  have hsplit : H * X * Hᴴ + R * R = R * Gm B X * R := by
    rw [Gm, hHB, conjTranspose_mul, hRH]
    simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_one, Matrix.mul_assoc]
  have hRinv : R⁻¹ = Ri := inv_eq_right_inv hRRi
  have hinv : (R * Gm B X * R)⁻¹ = Ri * (Gm B X)⁻¹ * Ri := by
    rw [Matrix.mul_inv_rev, Matrix.mul_inv_rev, hRinv, Matrix.mul_assoc]
  rw [hsplit, hinv, hBH, hB]
  simp only [Matrix.mul_assoc]

theorem whiten_log_det (H : Matrix m n ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) {R Ri : Matrix m m ℝ}
    (hRRi : R * Ri = 1) (hRH : Rᴴ = R) (hSig : (R * R).PosDef) :
    Real.log (H * X * Hᴴ + R * R).det = Real.log (Gm (Ri * H) X).det + Real.log (R * R).det := by
  set B := Ri * H with hB
  have hHB : H = R * B := by rw [hB, ← Matrix.mul_assoc, hRRi, Matrix.one_mul]
  have hsplit : H * X * Hᴴ + R * R = R * Gm B X * R := by
    rw [Gm, hHB, conjTranspose_mul, hRH]
    simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_one, Matrix.mul_assoc]
  have hG0 := (Gm_posDef B hX).det_pos
  have hR0 : 0 < R.det * R.det := by rw [← det_mul]; exact hSig.det_pos
  rw [hsplit, det_mul, det_mul, det_mul R R,
    show R.det * (Gm B X).det * R.det = (Gm B X).det * (R.det * R.det) by ring,
    Real.log_mul hG0.ne' hR0.ne']

end Whiten

end ObservationTheory.Tilted
