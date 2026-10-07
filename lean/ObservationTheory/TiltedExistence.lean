/-
**Theorem tilted, existence half**: the frontier point exists and carries KKT multipliers. Together with
`TiltedWaterFilling.lean` this machine-checks Theorem tilted of
`paper/tit-rate-leakage/tit-rate-leakage.tex` in full.

The paper argues by Slater's condition. Mathlib has no inequality-constrained KKT theorem, so this file
uses a problem-specific route.

* E1, `exists_minimizer`: a minimizer of `obj` over the feasible set exists. `obj Y ≥ -log det Y`, so a
  sublevel set lies in a compact set (`0 ⪯ Y ⪯ I` bounds the entries, `det Y ≥ c > 0` keeps it away from
  the singular boundary).
* E2, `first_order`: at a minimizer, `tr (M (Y - X)) ≤ 0` on the feasible set, with
  `M = X⁻¹ - β Bᴴ (B X Bᴴ + I)⁻¹ B`. Calculus-free: `-log (1 + u) ≤ -u + 2u²` on eigenvalues and the
  concave tangent bound `log_det_add_le`.
* E3, `exists_multipliers`: one-variable duality by a supremum of slopes gives `ν ≥ 0`; testing with
  eigen-projections gives `A = M - νQ ⪰ 0`; the trace argument gives `A (I - X) = 0`.
* E4, `tilted_waterfilling_exists`: `M ≻ 0` forces `ν > 0` and an active budget when `D < tr Q`.
-/
import Mathlib
import ObservationTheory.TiltedWaterFilling

open Matrix
open scoped MatrixOrder

namespace ObservationTheory.Tilted

open ObservationTheory.LogDet

variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ### E1: compactness and existence of a minimizer -/

omit [DecidableEq n] in
theorem isClosed_posSemidef : IsClosed {Y : Matrix n n ℝ | Y.PosSemidef} := by
  have h : {Y : Matrix n n ℝ | Y.PosSemidef} =
      {Y | Yᴴ = Y} ∩ ⋂ x : n → ℝ, {Y | 0 ≤ star x ⬝ᵥ (Y *ᵥ x)} := by
    ext Y
    simp only [Set.mem_setOf_eq, Set.mem_inter_iff, Set.mem_iInter, Matrix.posSemidef_iff_dotProduct_mulVec]
    rfl
  rw [h]
  refine IsClosed.inter (isClosed_eq (continuous_id.matrix_conjTranspose) continuous_id) ?_
  refine isClosed_iInter fun x => isClosed_le continuous_const ?_
  exact continuous_const.dotProduct (continuous_id.matrix_mulVec continuous_const)

/-- The quadratic form at `Pi.single i 1 + s • Pi.single j 1`. -/
theorem quad_single (Y : Matrix n n ℝ) (i j : n) (s : ℝ) :
    star (Pi.single i 1 + s • Pi.single j 1 : n → ℝ) ⬝ᵥ (Y *ᵥ (Pi.single i 1 + s • Pi.single j 1)) =
      Y i i + s * Y i j + s * Y j i + s * s * Y j j := by
  simp [Matrix.mulVec_add, Matrix.mulVec_smul, dotProduct_add, add_dotProduct,
    dotProduct_smul, smul_dotProduct, Matrix.mulVec_single,
    single_dotProduct]
  ring

/-- `0 ⪯ Y ⪯ I` bounds every entry by one. -/
theorem entry_bound {Y : Matrix n n ℝ} (hY : Y.PosSemidef) (h1Y : (1 - Y).PosSemidef) (i j : n) :
    |Y i j| ≤ 1 := by
  have q := fun (s : ℝ) => (Matrix.posSemidef_iff_dotProduct_mulVec.mp hY).2
    (Pi.single i 1 + s • Pi.single j 1)
  have q' := fun (s : ℝ) => (Matrix.posSemidef_iff_dotProduct_mulVec.mp h1Y).2
    (Pi.single i 1 + s • Pi.single j 1)
  simp only [quad_single] at q q'
  have hsym : Y j i = Y i j := by
    have := congrFun (congrFun hY.1 i) j
    simpa using this
  by_cases hij : i = j
  · subst hij
    have a := q 0
    have b := q' 0
    simp at a b
    rw [abs_le]; constructor <;> linarith
  · have hone : ∀ k l : n, (1 : Matrix n n ℝ) k l = if k = l then 1 else 0 := fun k l => rfl
    have a1 := q 1
    have a2 := q (-1)
    have b0 := q' 0
    have c0 : (1 - Y) j j = 1 - Y j j := by simp
    have bj := (Matrix.posSemidef_iff_dotProduct_mulVec.mp h1Y).2 (Pi.single j 1)
    have aj := (Matrix.posSemidef_iff_dotProduct_mulVec.mp hY).2 (Pi.single j 1)
    simp [Matrix.mulVec_single] at bj aj b0
    rw [hsym] at a1 a2
    rw [abs_le]; constructor <;> nlinarith

omit [Fintype n] [DecidableEq n] in
theorem isCompact_box :
    IsCompact {Y : Matrix n n ℝ | ∀ i j, Y i j ∈ Set.Icc (-1 : ℝ) 1} := by
  have h : IsCompact (Set.univ.pi fun _ : n => Set.univ.pi fun _ : n => Set.Icc (-1 : ℝ) 1) :=
    isCompact_univ_pi fun _ => isCompact_univ_pi fun _ => isCompact_Icc
  have e : {Y : Matrix n n ℝ | ∀ i j, Y i j ∈ Set.Icc (-1 : ℝ) 1} =
      Set.univ.pi fun _ : n => Set.univ.pi fun _ : n => Set.Icc (-1 : ℝ) 1 :=
    Set.ext fun Y => ⟨fun h i _ j _ => h i j, fun h i j => h i (Set.mem_univ i) j (Set.mem_univ j)⟩
  rw [e]; exact h

section Exist

variable {m : Type*} [Fintype m] [DecidableEq m]

omit [DecidableEq n] in
theorem one_le_det_Gm (B : Matrix m n ℝ) {Y : Matrix n n ℝ} (hY : Y.PosDef) : 1 ≤ (Gm B Y).det := by
  have hsub : Gm B Y - 1 = B * Y * Bᴴ := by unfold Gm; abel
  have h := det_le_det_of_loewner (A := (1 : Matrix m m ℝ)) (B := Gm B Y) Matrix.PosDef.one
    (by rw [hsub]; exact hY.posSemidef.mul_mul_conjTranspose_same B)
  simpa using h

/-- `obj ≥ -log det` because `det (B Y Bᴴ + I) ≥ 1`. -/
theorem neg_log_det_le_obj (B : Matrix m n ℝ) {β : ℝ} (hβ : 0 ≤ β) {Y : Matrix n n ℝ} (hY : Y.PosDef) :
    -Real.log Y.det ≤ obj β B Y := by
  unfold obj
  have := Real.log_nonneg (one_le_det_Gm B hY)
  nlinarith

theorem continuousOn_obj (B : Matrix m n ℝ) (β : ℝ) {K : Set (Matrix n n ℝ)}
    (hK : ∀ Y ∈ K, Y.PosDef) : ContinuousOn (obj β B) K := by
  have hdet : Continuous fun Y : Matrix n n ℝ => Y.det := continuous_id.matrix_det
  have hG : Continuous fun Y : Matrix n n ℝ => (Gm B Y).det := by
    unfold Gm
    exact (((continuous_const.matrix_mul continuous_id).matrix_mul continuous_const).add
      continuous_const).matrix_det
  unfold obj
  refine ContinuousOn.add (hdet.continuousOn.log fun Y hY => (hK Y hY).det_pos.ne').neg ?_
  exact continuousOn_const.mul (hG.continuousOn.log fun Y hY => (Gm_posDef B (hK Y hY)).det_pos.ne')

/-- The strictly feasible point `εI`. -/
theorem slater_point {Q : Matrix n n ℝ} {D : ℝ} (hD0 : 0 < D) (hDQ : D < Q.trace) :
    ∃ ε : ℝ, 0 < ε ∧ ε < 1 ∧ Feasible Q D (ε • (1 : Matrix n n ℝ)) ∧ (Q * (ε • 1)).trace < D := by
  have hQ0 : 0 < Q.trace := by linarith
  refine ⟨D / (2 * Q.trace), by positivity, ?_, ⟨?_, ?_, ?_⟩, ?_⟩
  · rw [div_lt_one (by positivity)]; linarith
  · exact Matrix.PosDef.one.smul (by positivity)
  · have : (1 : Matrix n n ℝ) - (D / (2 * Q.trace)) • 1 = (1 - D / (2 * Q.trace)) • 1 := by module
    rw [this]
    have : 0 ≤ 1 - D / (2 * Q.trace) := by
      rw [sub_nonneg, div_le_one (by positivity)]; linarith
    exact Matrix.PosSemidef.one.smul this
  · rw [Matrix.mul_smul, Matrix.mul_one, Matrix.trace_smul, smul_eq_mul]
    field_simp; nlinarith
  · rw [Matrix.mul_smul, Matrix.mul_one, Matrix.trace_smul, smul_eq_mul]
    field_simp; nlinarith

/-- **E1.** A minimizer of the weighted objective over the feasible set exists. -/
theorem exists_minimizer (B : Matrix m n ℝ) {Q : Matrix n n ℝ} {β D : ℝ}
    (hβ0 : 0 ≤ β) (hD0 : 0 < D) (hDQ : D < Q.trace) :
    ∃ X, Feasible Q D X ∧ ∀ Y, Feasible Q D Y → obj β B X ≤ obj β B Y := by
  obtain ⟨ε, -, -, hY0, -⟩ := slater_point hD0 hDQ
  set Y0 := ε • (1 : Matrix n n ℝ)
  set c0 := obj β B Y0
  set K := {Y : Matrix n n ℝ | Y.PosSemidef ∧ (1 - Y).PosSemidef ∧ (Q * Y).trace ≤ D ∧
    Real.exp (-c0) ≤ Y.det}
  have hKpd : ∀ Y ∈ K, Y.PosDef := fun Y hY =>
    (hY.1.posDef_iff_det_ne_zero).mpr (lt_of_lt_of_le (Real.exp_pos _) hY.2.2.2).ne'
  have hKc : IsCompact K := by
    refine isCompact_box.of_isClosed_subset ?_ ?_
    · refine IsClosed.inter isClosed_posSemidef (IsClosed.inter ?_ (IsClosed.inter ?_ ?_))
      · exact isClosed_posSemidef.preimage (continuous_const.sub continuous_id)
      · exact isClosed_le ((continuous_const.matrix_mul continuous_id).matrix_trace) continuous_const
      · exact isClosed_le continuous_const continuous_id.matrix_det
    · intro Y hY i j
      exact abs_le.mp (entry_bound hY.1 hY.2.1 i j)
  have hY0K : Y0 ∈ K := by
    refine ⟨hY0.1.posSemidef, hY0.2.1, hY0.2.2, ?_⟩
    have h := neg_log_det_le_obj B hβ0 hY0.1
    have : Real.log Y0.det ≥ -c0 := by linarith
    calc Real.exp (-c0) ≤ Real.exp (Real.log Y0.det) := Real.exp_le_exp.mpr this
      _ = Y0.det := Real.exp_log hY0.1.det_pos
  obtain ⟨X, hXK, hXmin⟩ := hKc.exists_isMinOn ⟨Y0, hY0K⟩ (continuousOn_obj B β hKpd)
  refine ⟨X, ⟨hKpd X hXK, hXK.2.1, hXK.2.2.1⟩, fun Y hY => ?_⟩
  by_cases hc : obj β B Y ≤ c0
  · apply hXmin
    refine ⟨hY.1.posSemidef, hY.2.1, hY.2.2, ?_⟩
    have h := neg_log_det_le_obj B hβ0 hY.1
    have : Real.log Y.det ≥ -c0 := by linarith
    calc Real.exp (-c0) ≤ Real.exp (Real.log Y.det) := Real.exp_le_exp.mpr this
      _ = Y.det := Real.exp_log hY.1.det_pos
  · have := hXmin hY0K
    simp only [Set.mem_setOf_eq] at this
    linarith

end Exist

/-! ### E2: the first-order condition at a minimizer -/

/-- `-log (1 + u) ≤ -u + 2u²` for `u ≥ -1/2`. -/
theorem neg_log_one_add_le {u : ℝ} (hu : -1 / 2 ≤ u) : -Real.log (1 + u) ≤ -u + 2 * u ^ 2 := by
  have h1 : 0 < 1 + u := by linarith
  have hl := Real.log_le_sub_one_of_pos (inv_pos.mpr h1)
  rw [Real.log_inv] at hl
  have key : (1 + u)⁻¹ - 1 ≤ -u + 2 * u ^ 2 := by
    rw [inv_eq_one_div, div_sub_one h1.ne', div_le_iff₀ h1]
    nlinarith [mul_nonneg (sq_nonneg u) (by linarith : (0 : ℝ) ≤ 1 + 2 * u)]
  linarith

/-- **Second-order upper bound for `-log det`.** For `X ≻ 0` and symmetric `Δ` there are `C ≥ 0` and
`t₀ > 0` with `-log det (X + tΔ) ≤ -log det X - t tr (X⁻¹ Δ) + C t²` for `0 < t ≤ t₀`. -/
theorem neg_log_det_expand {X Δ : Matrix n n ℝ} (hX : X.PosDef) (hΔ : Δ.IsHermitian) :
    ∃ C t₀ : ℝ, 0 ≤ C ∧ 0 < t₀ ∧ ∀ t : ℝ, 0 < t → t ≤ t₀ →
      -Real.log (X + t • Δ).det ≤ -Real.log X.det - t * (X⁻¹ * Δ).trace + t ^ 2 * C := by
  obtain ⟨R, Ri, hRR, hRRi, hRiR, hRiH, hRH⟩ := exists_sqrt hX
  have hsq := sqrt_inv_sq hX hRR hRRi
  set N := Ri * Δ * Ri with hNdef
  have hN : N.IsHermitian := by
    unfold Matrix.IsHermitian
    rw [hNdef, conjTranspose_mul, conjTranspose_mul, hRiH, hΔ.eq, Matrix.mul_assoc]
  set μ := hN.eigenvalues
  set S := ∑ i, |μ i|
  have hS0 : 0 ≤ S := Finset.sum_nonneg fun i _ => abs_nonneg _
  refine ⟨2 * ∑ i, μ i ^ 2, 1 / (2 * (S + 1)), by positivity, by positivity, fun t ht0 htt => ?_⟩
  have hμ : ∀ i, -1 / 2 ≤ t * μ i := by
    intro i
    have hi : |μ i| ≤ S := Finset.single_le_sum (f := fun i => |μ i|) (fun j _ => abs_nonneg _)
      (Finset.mem_univ i)
    have h1 : t * |μ i| ≤ t * S := mul_le_mul_of_nonneg_left hi ht0.le
    have h2 : t * S ≤ 1 / 2 := by
      calc t * S ≤ 1 / (2 * (S + 1)) * S := mul_le_mul_of_nonneg_right htt hS0
        _ ≤ 1 / 2 := by rw [div_mul_eq_mul_div, div_le_div_iff₀ (by positivity) (by norm_num)]; nlinarith
    have h3 : -(t * |μ i|) ≤ t * μ i := by
      rw [← mul_neg]; exact mul_le_mul_of_nonneg_left (neg_abs_le _) ht0.le
    linarith
  have hfac : ∀ i, 0 < 1 + t * μ i := fun i => by have := hμ i; linarith
  have hRNR : R * N * R = Δ := by
    rw [hNdef]
    calc R * (Ri * Δ * Ri) * R = (R * Ri) * Δ * (Ri * R) := by simp only [Matrix.mul_assoc]
      _ = Δ := by rw [hRRi, hRiR, Matrix.one_mul, Matrix.mul_one]
  have hsplit : X + t • Δ = R * ((1 : ℝ) • (1 : Matrix n n ℝ) + t • N) * R := by
    have e : R * ((1 : ℝ) • (1 : Matrix n n ℝ) + t • N) * R = R * R + t • (R * N * R) := by
      simp only [one_smul, Matrix.mul_add, Matrix.add_mul, Matrix.mul_one, Matrix.mul_smul, Matrix.smul_mul]
    rw [e, hRR, hRNR]
  have hdetR : R.det * R.det = X.det := by rw [← det_mul, hRR]
  have hX0 := hX.det_pos
  have hprod : ((1 : ℝ) • (1 : Matrix n n ℝ) + t • N).det = ∏ i, (1 + t * μ i) := det_affine_herm hN 1 t
  have hprod0 : 0 < ∏ i, (1 + t * μ i) := Finset.prod_pos fun i _ => hfac i
  have hdet : (X + t • Δ).det = X.det * ∏ i, (1 + t * μ i) := by
    rw [hsplit, det_mul, det_mul, hprod, ← hdetR]; ring
  have htr : (X⁻¹ * Δ).trace = ∑ i, μ i := by
    have h1 : (X⁻¹ * Δ).trace = N.trace := by
      rw [← hsq, hNdef, Matrix.mul_assoc, Matrix.trace_mul_comm Ri (Ri * Δ), Matrix.mul_assoc]
    rw [h1]
    simpa [RCLike.ofReal_real_eq_id] using hN.trace_eq_sum_eigenvalues
  rw [hdet, Real.log_mul hX0.ne' hprod0.ne', Real.log_prod (fun i _ => (hfac i).ne'), htr]
  have hterm : ∀ i, -Real.log (1 + t * μ i) ≤ -(t * μ i) + t ^ 2 * (2 * μ i ^ 2) := by
    intro i
    have := neg_log_one_add_le (hμ i)
    nlinarith
  have hsum := Finset.sum_le_sum fun i (_ : i ∈ Finset.univ) => hterm i
  have hA : ∑ i, (-(t * μ i) + t ^ 2 * (2 * μ i ^ 2)) =
      -(t * ∑ i, μ i) + t ^ 2 * (2 * ∑ i, μ i ^ 2) := by
    rw [Finset.sum_add_distrib, Finset.sum_neg_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
      ← Finset.mul_sum]
  have hB : ∑ i, -Real.log (1 + t * μ i) = -∑ i, Real.log (1 + t * μ i) := Finset.sum_neg_distrib _
  rw [hA, hB] at hsum
  linarith

section FOC

variable {m : Type*} [Fintype m] [DecidableEq m]

/-- The gradient-side matrix `M = X⁻¹ - β Bᴴ (B X Bᴴ + I)⁻¹ B` (minus half the gradient of `obj`). -/
noncomputable def gradM (β : ℝ) (B : Matrix m n ℝ) (X : Matrix n n ℝ) : Matrix n n ℝ :=
  X⁻¹ - β • (Bᴴ * (Gm B X)⁻¹ * B)

theorem feasible_combo {Q X Y : Matrix n n ℝ} {D t : ℝ} (hX : Feasible Q D X) (hY : Feasible Q D Y)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : Feasible Q D ((1 - t) • X + t • Y) := by
  obtain ⟨hXpd, h1X, hQX⟩ := hX
  obtain ⟨hYpd, h1Y, hQY⟩ := hY
  refine ⟨posDef_combo hXpd hYpd ht0 ht1, ?_, ?_⟩
  · have : 1 - ((1 - t) • X + t • Y) = (1 - t) • (1 - X) + t • (1 - Y) := by module
    rw [this]; exact (h1X.smul (by linarith)).add (h1Y.smul ht0)
  · rw [Matrix.mul_add, Matrix.mul_smul, Matrix.mul_smul, Matrix.trace_add, Matrix.trace_smul,
      Matrix.trace_smul, smul_eq_mul, smul_eq_mul]
    nlinarith

/-- **E2.** At a minimizer, `tr (M (Y - X)) ≤ 0` for every feasible `Y`. -/
theorem first_order (B : Matrix m n ℝ) {Q X : Matrix n n ℝ} {β D : ℝ} (hβ0 : 0 ≤ β)
    (hX : Feasible Q D X) (hmin : ∀ Y, Feasible Q D Y → obj β B X ≤ obj β B Y)
    {Y : Matrix n n ℝ} (hY : Feasible Q D Y) : (gradM β B X * (Y - X)).trace ≤ 0 := by
  have hXpd := hX.1
  set Δ := Y - X with hΔdef
  have hΔ : Δ.IsHermitian := by
    unfold Matrix.IsHermitian; rw [hΔdef, conjTranspose_sub, hY.1.1.eq, hXpd.1.eq]
  obtain ⟨C, t₀, hC, ht₀, hexp⟩ := neg_log_det_expand hXpd hΔ
  set g := (gradM β B X * Δ).trace with hg
  have hgsplit : g = (X⁻¹ * Δ).trace - β * (Bᴴ * (Gm B X)⁻¹ * B * Δ).trace := by
    rw [hg, gradM, Matrix.sub_mul, Matrix.smul_mul, Matrix.trace_sub, Matrix.trace_smul, smul_eq_mul]
  -- for every small t, g ≤ t C
  have hstep : ∀ t, 0 < t → t ≤ 1 → t ≤ t₀ → g ≤ t * C := by
    intro t ht0 ht1 htt
    have hZeq : X + t • Δ = (1 - t) • X + t • Y := by rw [hΔdef]; module
    have hZ : Feasible Q D (X + t • Δ) := by rw [hZeq]; exact feasible_combo hX hY ht0.le ht1
    have hmZ := hmin _ hZ
    have hGeq : Gm B (X + t • Δ) = Gm B X + t • (B * Δ * Bᴴ) := by
      unfold Gm
      rw [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul]; abel
    have hGpd : (Gm B X + t • (B * Δ * Bᴴ)).PosDef := by rw [← hGeq]; exact Gm_posDef B hZ.1
    have htan := log_det_add_le (Gm_posDef B hXpd) hGpd
    have htrG : ((Gm B X)⁻¹ * (t • (B * Δ * Bᴴ))).trace = t * (Bᴴ * (Gm B X)⁻¹ * B * Δ).trace := by
      rw [Matrix.mul_smul, Matrix.trace_smul, smul_eq_mul]
      congr 1
      rw [show (Gm B X)⁻¹ * (B * Δ * Bᴴ) = ((Gm B X)⁻¹ * B * Δ) * Bᴴ by simp only [Matrix.mul_assoc],
        Matrix.trace_mul_comm]
      simp only [Matrix.mul_assoc]
    have hex := hexp t ht0 htt
    unfold obj at hmZ
    rw [hGeq] at hmZ
    have hb := mul_le_mul_of_nonneg_left htan hβ0
    rw [htrG] at hb
    -- 0 ≤ obj Z - obj X ≤ -t g + t² C
    have : t * g ≤ t ^ 2 * C := by rw [hgsplit]; nlinarith
    have h2 : t * g ≤ t * (t * C) := by nlinarith
    exact le_of_mul_le_mul_left h2 ht0
  by_contra hpos
  push Not at hpos
  set t := min (min 1 t₀) (g / (2 * (C + 1))) with ht
  have htpos : 0 < t := lt_min (lt_min one_pos ht₀) (by positivity)
  have ht1 : t ≤ 1 := le_trans (min_le_left _ _) (min_le_left _ _)
  have htt : t ≤ t₀ := le_trans (min_le_left _ _) (min_le_right _ _)
  have htg : t ≤ g / (2 * (C + 1)) := min_le_right _ _
  have h := hstep t htpos ht1 htt
  have : t * C < g := by
    calc t * C ≤ g / (2 * (C + 1)) * C := mul_le_mul_of_nonneg_right htg hC
      _ < g := by
        rw [div_mul_eq_mul_div, div_lt_iff₀ (by positivity)]; nlinarith
  linarith

end FOC

/-! ### E3: the multipliers -/

/-- The cap `0 ⪯ Y ⪯ I` (no budget). -/
def Cap (Y : Matrix n n ℝ) : Prop := Y.PosSemidef ∧ (1 - Y).PosSemidef

omit [Fintype n] in
theorem cap_combo {Y Z : Matrix n n ℝ} (hY : Cap Y) (hZ : Cap Z) {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    Cap ((1 - t) • Y + t • Z) := by
  refine ⟨(hY.1.smul (by linarith)).add (hZ.1.smul ht0), ?_⟩
  have : 1 - ((1 - t) • Y + t • Z) = (1 - t) • (1 - Y) + t • (1 - Z) := by module
  rw [this]; exact (hY.2.smul (by linarith)).add (hZ.2.smul ht0)

/-- A real limit step: `(1 - s) a + s b ≤ c` for all `s ∈ (0, 1]` forces `a ≤ c`. -/
theorem le_of_mix_le {a b c : ℝ} (h : ∀ s : ℝ, 0 < s → s ≤ 1 → (1 - s) * a + s * b ≤ c) : a ≤ c := by
  by_contra hac
  push Not at hac
  set s := min 1 ((a - c) / (2 * (|a - b| + 1)))
  have hs0 : 0 < s := lt_min one_pos (by apply div_pos <;> [linarith; positivity])
  have hs1 : s ≤ 1 := min_le_left _ _
  have hs2 : s ≤ (a - c) / (2 * (|a - b| + 1)) := min_le_right _ _
  have h1 := h s hs0 hs1
  have h2 : s * |a - b| < a - c := by
    calc s * |a - b| ≤ (a - c) / (2 * (|a - b| + 1)) * |a - b| := mul_le_mul_of_nonneg_right hs2 (abs_nonneg _)
      _ < a - c := by
        rw [div_mul_eq_mul_div, div_lt_iff₀ (by positivity)]
        nlinarith [abs_nonneg (a - b)]
  have hba : -|a - b| ≤ b - a := by rw [abs_sub_comm]; exact neg_abs_le (b - a)
  have h3 : s * (-|a - b|) ≤ s * (b - a) := mul_le_mul_of_nonneg_left hba hs0.le
  nlinarith

/-- **One-variable duality** by the supremum of slopes. If `f Y ≤ p` on the budget-feasible part of the cap,
and a strictly feasible cap point exists, then some `ν ≥ 0` gives `f Y - ν g Y ≤ p` on the whole cap, with
`f = tr (M ·)` and `g = tr (Q ·) - D`. -/
theorem slope_duality {M Q Y0 : Matrix n n ℝ} {D p : ℝ} (hY0 : Cap Y0) (hY0g : (Q * Y0).trace < D)
    (hfeas : ∀ Y, Cap Y → (Q * Y).trace ≤ D → (M * Y).trace ≤ p) :
    ∃ ν : ℝ, 0 ≤ ν ∧ ∀ Y, Cap Y → (M * Y).trace - ν * ((Q * Y).trace - D) ≤ p := by
  set f := fun Y : Matrix n n ℝ => (M * Y).trace
  set g := fun Y : Matrix n n ℝ => (Q * Y).trace - D
  have hf : ∀ (Y Z : Matrix n n ℝ) (t : ℝ), f ((1 - t) • Y + t • Z) = (1 - t) * f Y + t * f Z := by
    intro Y Z t
    simp only [f, Matrix.mul_add, Matrix.mul_smul, Matrix.trace_add, Matrix.trace_smul, smul_eq_mul]
  have hg : ∀ (Y Z : Matrix n n ℝ) (t : ℝ), g ((1 - t) • Y + t • Z) = (1 - t) * g Y + t * g Z := by
    intro Y Z t
    simp only [g, Matrix.mul_add, Matrix.mul_smul, Matrix.trace_add, Matrix.trace_smul, smul_eq_mul]
    ring
  -- key bound: every slope is at most the slope toward any strictly feasible cap point
  have key : ∀ Z Y, Cap Z → Cap Y → 0 < g Z → g Y < 0 → (f Z - p) / g Z ≤ (p - f Y) / (-g Y) := by
    intro Z Y hZ hY hgZ hgY
    set t := g Z / (g Z - g Y)
    have hden : 0 < g Z - g Y := by linarith
    have ht0 : 0 ≤ t := div_nonneg hgZ.le hden.le
    have ht1 : t ≤ 1 := by rw [div_le_one hden]; linarith
    have hW := cap_combo hZ hY ht0 ht1
    have hgW : g ((1 - t) • Z + t • Y) = 0 := by
      rw [hg]; simp only [t]; field_simp; ring
    have hfW := hfeas _ hW (by have := hgW; simp only [g] at this; linarith)
    have hfW' : (1 - t) * f Z + t * f Y ≤ p := by rw [← hf]; exact hfW
    have h1t : 1 - t = -g Y / (g Z - g Y) := by simp only [t]; field_simp; ring
    rw [h1t] at hfW'
    simp only [t] at hfW'
    rw [div_le_div_iff₀ hgZ (by linarith)]
    have : -g Y * f Z + g Z * f Y ≤ p * (g Z - g Y) := by
      have := mul_le_mul_of_nonneg_right hfW' hden.le
      field_simp at this
      linarith
    nlinarith
  set T := {r : ℝ | ∃ Z, Cap Z ∧ 0 < g Z ∧ r = (f Z - p) / g Z}
  have hY0g' : g Y0 < 0 := by simp only [g]; linarith
  have hbdd : BddAbove T := ⟨(p - f Y0) / (-g Y0), fun r ⟨Z, hZ, hgZ, hr⟩ => hr ▸ key Z Y0 hZ hY0 hgZ hY0g'⟩
  by_cases hT : T.Nonempty
  · refine ⟨max 0 (sSup T), le_max_left _ _, fun Y hY => ?_⟩
    rcases lt_trichotomy (g Y) 0 with hgY | hgY | hgY
    · have hsup : sSup T ≤ (p - f Y) / (-g Y) := csSup_le hT fun r ⟨Z, hZ, hgZ, hr⟩ => hr ▸ key Z Y hZ hY hgZ hgY
      have hfp : f Y ≤ p := hfeas Y hY (by simp only [g] at hgY; linarith)
      have hnn : 0 ≤ (p - f Y) / (-g Y) := div_nonneg (by linarith) (by linarith)
      have hν : max 0 (sSup T) ≤ (p - f Y) / (-g Y) := max_le hnn hsup
      rw [le_div_iff₀ (by linarith)] at hν
      show f Y - max 0 (sSup T) * g Y ≤ p
      nlinarith
    · have hfp : f Y ≤ p := hfeas Y hY (by simp only [g] at hgY; linarith)
      show f Y - max 0 (sSup T) * g Y ≤ p
      rw [hgY, mul_zero, sub_zero]; exact hfp
    · have hmem : (f Y - p) / g Y ∈ T := ⟨Y, hY, hgY, rfl⟩
      have hle : (f Y - p) / g Y ≤ max 0 (sSup T) := le_trans (le_csSup hbdd hmem) (le_max_right _ _)
      rw [div_le_iff₀ hgY] at hle
      show f Y - max 0 (sSup T) * g Y ≤ p
      linarith
  · refine ⟨0, le_refl _, fun Y hY => ?_⟩
    show f Y - 0 * g Y ≤ p
    rw [zero_mul, sub_zero]
    by_cases hgY : 0 < g Y
    · exact absurd ⟨_, ⟨Y, hY, hgY, rfl⟩⟩ hT
    · exact hfeas Y hY (by push Not at hgY; simp only [g] at hgY; linarith)

/-- The trace of a product of positive semidefinite matrices vanishes only if the product does. -/
theorem psd_mul_eq_zero {A P : Matrix n n ℝ} (hA : A.PosSemidef) (hP : P.PosSemidef)
    (h : (A * P).trace = 0) : A * P = 0 := by
  have hA0 : 0 ≤ A := Matrix.nonneg_iff_posSemidef.mpr hA
  have hP0 : 0 ≤ P := Matrix.nonneg_iff_posSemidef.mpr hP
  set S := CFC.sqrt A
  set T := CFC.sqrt P
  have hSS : S * S = A := CFC.sqrt_mul_sqrt_self A hA0
  have hTT : T * T = P := CFC.sqrt_mul_sqrt_self P hP0
  have hSH : Sᴴ = S := (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg A)).star_eq
  have hTH : Tᴴ = T := (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg P)).star_eq
  have htr : ((S * T)ᴴ * (S * T)).trace = 0 := by
    rw [conjTranspose_mul, hSH, hTH]
    have : (T * S * (S * T)).trace = (A * P).trace := by
      rw [← hSS, ← hTT]
      rw [show T * S * (S * T) = T * (S * S * T) by simp only [Matrix.mul_assoc], Matrix.trace_mul_comm]
      simp only [Matrix.mul_assoc]
    rw [this, h]
  have hST : S * T = 0 := Matrix.trace_conjTranspose_mul_self_eq_zero_iff.mp htr
  rw [← hSS, ← hTT]
  calc S * S * (T * T) = S * (S * T) * T := by simp only [Matrix.mul_assoc]
    _ = 0 := by rw [hST, Matrix.mul_zero, Matrix.zero_mul]

/-- A symmetric `A'` with `tr (A' P) ≥ 0` for every `0 ⪯ P ⪯ I` is positive semidefinite (test with the
eigen-projections). -/
theorem psd_of_trace_cap {A' : Matrix n n ℝ} (hA' : A'.IsHermitian)
    (h : ∀ P : Matrix n n ℝ, Cap P → 0 ≤ (A' * P).trace) : A'.PosSemidef := by
  rw [hA'.posSemidef_iff_eigenvalues_nonneg]
  intro i
  set d := hA'.eigenvalues
  set U := hA'.eigenvectorUnitary
  have hspec : A' = (U : Matrix n n ℝ) * diagonal d * star (U : Matrix n n ℝ) := by
    conv_lhs => rw [hA'.spectral_theorem]
    simp [d, U, RCLike.ofReal_real_eq_id, Unitary.conjStarAlgAut_apply]
  have hUU : star (U : Matrix n n ℝ) * (U : Matrix n n ℝ) = 1 := Unitary.star_mul_self_of_mem U.2
  have hUU' : (U : Matrix n n ℝ) * star (U : Matrix n n ℝ) = 1 := Unitary.mul_star_self_of_mem U.2
  set e : n → ℝ := Pi.single i 1
  set P := (U : Matrix n n ℝ) * diagonal e * star (U : Matrix n n ℝ)
  have hconj : ∀ f : n → ℝ, 0 ≤ f → ((U : Matrix n n ℝ) * diagonal f * star (U : Matrix n n ℝ)).PosSemidef := by
    intro f hf
    have := (Matrix.PosSemidef.diagonal hf).conjTranspose_mul_mul_same (star (U : Matrix n n ℝ))
    simpa [Matrix.star_eq_conjTranspose] using this
  have he0 : 0 ≤ e := by
    intro j; by_cases hj : j = i
    · subst hj; simp [e]
    · simp [e, hj]
  have he1 : 0 ≤ (1 : n → ℝ) - e := by
    intro j; by_cases hj : j = i
    · subst hj; simp [e]
    · simp [e, hj]
  have hP : Cap P := by
    refine ⟨hconj e he0, ?_⟩
    have : 1 - P = (U : Matrix n n ℝ) * diagonal (1 - e) * star (U : Matrix n n ℝ) := by
      rw [show diagonal ((1 : n → ℝ) - e) = 1 - diagonal e by
        rw [← diagonal_one, diagonal_sub]; rfl]
      rw [Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_one, hUU']
    rw [this]; exact hconj _ he1
  have htr : (A' * P).trace = d i := by
    rw [hspec, conj_diag_mul, Matrix.trace_mul_comm, ← Matrix.mul_assoc, hUU, Matrix.one_mul,
      Matrix.trace_diagonal]
    simp [e, Pi.single_apply]
  have := h P hP
  rwa [htr] at this

section Mult

variable {m : Type*} [Fintype m] [DecidableEq m]

theorem gradM_isHermitian (B : Matrix m n ℝ) (β : ℝ) {X : Matrix n n ℝ} (hX : X.PosDef) :
    (gradM β B X).IsHermitian := by
  have hG : (Gm B X)ᴴ = Gm B X := (Gm_posDef B hX).1
  unfold Matrix.IsHermitian gradM
  rw [conjTranspose_sub, inv_isHermitian hX, conjTranspose_smul, conjTranspose_mul, conjTranspose_mul,
    conjTranspose_conjTranspose, conjTranspose_nonsing_inv, hG]
  simp [Matrix.mul_assoc]

/-- `M = (1 - β) X⁻¹ + β X⁻¹ F(X) X⁻¹ ≻ 0`. -/
theorem gradM_posDef (B : Matrix m n ℝ) {β : ℝ} (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) {X : Matrix n n ℝ}
    (hX : X.PosDef) : (gradM β B X).PosDef := by
  have hXi : X⁻¹.PosDef := Matrix.posDef_inv_iff.mpr hX
  have hW : (X⁻¹ * Fw B X * X⁻¹).PosDef := by
    have hinj : Function.Injective X⁻¹.mulVec := by
      intro x y hxy
      have := congrArg (fun v => X *ᵥ v) hxy
      simpa [Matrix.mulVec_mulVec, mul_nonsing_inv X (isUnit_det_of_posDef hX)] using this
    have := (Fw_posDef B hX).conjTranspose_mul_mul_same hinj
    rwa [inv_isHermitian hX] at this
  have heq : gradM β B X = (1 - β) • X⁻¹ + β • (X⁻¹ * Fw B X * X⁻¹) := by
    rw [gradM, ← grad_identity B hX]; module
  rw [heq]; exact posDef_combo hXi hW hβ0 hβ1

/-- **E3–E4.** The minimizer is a budget-active fixed point with a positive multiplier. -/
theorem minimizer_is_fixed_point (B : Matrix m n ℝ) {Q X : Matrix n n ℝ} {β D : ℝ}
    (hQ : Q.PosSemidef) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) (hD0 : 0 < D) (hDQ : D < Q.trace)
    (hX : Feasible Q D X) (hmin : ∀ Y, Feasible Q D Y → obj β B X ≤ obj β B Y) :
    ∃ ν : ℝ, 0 < ν ∧ (Q * X).trace = D ∧ X = waterfill (tilt ν β Q B X) := by
  have hXpd := hX.1
  set M := gradM β B X
  obtain ⟨ε, hε0, hε1, hY0, hY0g⟩ := slater_point (Q := Q) hD0 hDQ
  set Y0 := ε • (1 : Matrix n n ℝ)
  have hY0cap : Cap Y0 := ⟨hY0.1.posSemidef, hY0.2.1⟩
  -- the variational inequality on the budget-feasible cap
  have hvi : ∀ Y, Cap Y → (Q * Y).trace ≤ D → (M * Y).trace ≤ (M * X).trace := by
    intro Y hY hQY
    apply le_of_mix_le (b := (M * Y0).trace)
    intro s hs0 hs1
    have hYs : Feasible Q D ((1 - s) • Y + s • Y0) := by
      refine ⟨?_, (cap_combo hY hY0cap hs0.le hs1).2, ?_⟩
      · exact Matrix.PosDef.posSemidef_add (hY.1.smul (by linarith)) (hY0.1.smul hs0)
      · rw [Matrix.mul_add, Matrix.mul_smul, Matrix.mul_smul, Matrix.trace_add, Matrix.trace_smul,
          Matrix.trace_smul, smul_eq_mul, smul_eq_mul]
        nlinarith [mul_nonneg (sub_nonneg.mpr hs1) (sub_nonneg.mpr hQY),
          mul_nonneg hs0.le (sub_nonneg.mpr hY0g.le)]
    have h := first_order B hβ0 hX hmin hYs
    rw [Matrix.mul_sub, Matrix.trace_sub, Matrix.mul_add, Matrix.mul_smul, Matrix.mul_smul, Matrix.trace_add,
      Matrix.trace_smul, Matrix.trace_smul, smul_eq_mul, smul_eq_mul] at h
    linarith
  obtain ⟨ν₀, hν₀, hdual⟩ := slope_duality hY0cap hY0g hvi
  have hQX := hX.2.2
  have hslack : ν₀ * ((Q * X).trace - D) = 0 := by
    have := hdual X ⟨hXpd.posSemidef, hX.2.1⟩
    nlinarith
  set A := M - ν₀ • Q with hAdef
  have hQs : (ν₀ • Q).IsHermitian := by
    unfold Matrix.IsHermitian; rw [conjTranspose_smul, hQ.1.eq]; simp
  have hAH : A.IsHermitian := (gradM_isHermitian B β hXpd).sub hQs
  have hAmax : ∀ Y, Cap Y → (A * Y).trace ≤ (A * X).trace := by
    intro Y hY
    have := hdual Y hY
    simp only [hAdef, Matrix.sub_mul, Matrix.smul_mul, Matrix.trace_sub, Matrix.trace_smul, smul_eq_mul]
    nlinarith
  -- A ⪰ 0
  obtain ⟨R, Ri, hRR, hRRi, hRiR, hRiH, hRH⟩ := exists_sqrt hXpd
  have hA'H : (R * A * R).IsHermitian := by
    unfold Matrix.IsHermitian; rw [conjTranspose_mul, conjTranspose_mul, hRH, hAH.eq, Matrix.mul_assoc]
  have hA' : (R * A * R).PosSemidef := by
    apply psd_of_trace_cap hA'H
    intro P hP
    have hZ : Cap (R * (1 - P) * R) := by
      refine ⟨?_, ?_⟩
      · have := hP.2.conjTranspose_mul_mul_same R; rwa [hRH] at this
      · have : 1 - R * (1 - P) * R = (1 - X) + R * P * R := by
          rw [Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_one, hRR]; abel
        rw [this]
        exact hX.2.1.add (by have := hP.1.conjTranspose_mul_mul_same R; rwa [hRH] at this)
    have h := hAmax _ hZ
    have : (A * X).trace - (A * (R * (1 - P) * R)).trace = (R * A * R * P).trace := by
      rw [← Matrix.trace_sub, ← Matrix.mul_sub, ← hRR]
      rw [show R * R - R * (1 - P) * R = R * P * R by
        rw [Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_one]; abel]
      rw [show A * (R * P * R) = (A * R * P) * R by simp only [Matrix.mul_assoc], Matrix.trace_mul_comm]
      simp only [Matrix.mul_assoc]
    linarith
  have hA : A.PosSemidef := by
    have := hA'.conjTranspose_mul_mul_same Ri
    rw [hRiH] at this
    have e : Ri * (R * A * R) * Ri = A := by
      calc Ri * (R * A * R) * Ri = (Ri * R) * A * (R * Ri) := by simp only [Matrix.mul_assoc]
        _ = A := by rw [hRiR, hRRi, Matrix.one_mul, Matrix.mul_one]
    rwa [e] at this
  -- A (I - X) = 0
  have hAone : (A * (1 - X)).trace = 0 := by
    have h1 := hAmax 1 ⟨Matrix.PosSemidef.one, by simpa using Matrix.PosSemidef.zero⟩
    have h2 := trace_mul_psd_nonneg hA hX.2.1
    rw [Matrix.mul_sub, Matrix.trace_sub, Matrix.mul_one] at h2 ⊢
    rw [Matrix.mul_one] at h1
    linarith
  have hAX := psd_mul_eq_zero hA hX.2.1 hAone
  -- ν₀ > 0 (else M (I - X) = 0 forces X = I, against D < tr Q)
  have hνpos : 0 < ν₀ := by
    rcases eq_or_lt_of_le hν₀ with h | h
    · exfalso
      have hAM : A = M := by rw [hAdef, ← h, zero_smul, sub_zero]
      have hMu := isUnit_det_of_posDef (gradM_posDef B hβ0 hβ1 hXpd)
      have hIX : 1 - X = 0 := by
        have : M⁻¹ * (M * (1 - X)) = 0 := by rw [← hAM, hAX, Matrix.mul_zero]
        rwa [← Matrix.mul_assoc, nonsing_inv_mul M hMu, Matrix.one_mul] at this
      have hX1 : X = 1 := (sub_eq_zero.mp hIX).symm
      rw [hX1, Matrix.mul_one] at hQX
      linarith
    · exact h
  have hD : (Q * X).trace = D := by
    rcases mul_eq_zero.mp hslack with h | h
    · linarith
    · linarith
  refine ⟨ν₀ / 2, by positivity, hD, ?_⟩
  -- assemble the KKT system and apply the spectral core
  apply (kkt_iff_waterfill (tilt_isHermitian B _ β hQ.1 hXpd) hXpd).mp
  refine ⟨hX.2.1, (1 / 2 : ℝ) • A, hA.smul (by norm_num), ?_, ?_⟩
  · rw [Matrix.smul_mul, hAX, smul_zero]
  · rw [smul_smul, tilt, hAdef]
    have h1 : (2 : ℝ) * (1 / 2) = 1 := by norm_num
    have h2 : 2 * (ν₀ / 2) = ν₀ := by ring
    rw [h1, one_smul, h2]
    simp only [M, gradM]
    abel

/-- **Theorem tilted, existence.** For `0 < D < tr Q` there is a budget-active fixed point with `ν > 0`,
and it minimizes the weighted objective. -/
theorem tilted_waterfilling_exists (B : Matrix m n ℝ) {Q : Matrix n n ℝ} {β D : ℝ}
    (hQ : Q.PosSemidef) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) (hD0 : 0 < D) (hDQ : D < Q.trace) :
    ∃ X ν, 0 < ν ∧ (Q * X).trace = D ∧ X = waterfill (tilt ν β Q B X) ∧
      ∀ Y, Feasible Q D Y → obj β B X ≤ obj β B Y := by
  obtain ⟨X, hX, hmin⟩ := exists_minimizer B hβ0 hD0 hDQ
  obtain ⟨ν, hν, hD, hfix⟩ := minimizer_is_fixed_point B hQ hβ0 hβ1 hD0 hDQ hX hmin
  exact ⟨X, ν, hν, hD, hfix, hmin⟩

/-- **Theorem tilted, complete.** For `α ∈ [0, 1]` (`β = 1 - α`) and `0 < D < D_max = tr Q`, the frontier point
of weight `α` (the unique minimizer of the weighted objective over the feasible set) is the unique `X` with
`tr (Q X) = D` and `X = Φ(Ã(X))` for some `ν > 0`. -/
theorem tilted_waterfilling_complete (B : Matrix m n ℝ) {Q : Matrix n n ℝ} {β D : ℝ}
    (hQ : Q.PosSemidef) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1) (hD0 : 0 < D) (hDQ : D < Q.trace) :
    ∃ X, (Feasible Q D X ∧ ∀ Y, Feasible Q D Y → obj β B X ≤ obj β B Y) ∧
      (∀ Y, Feasible Q D Y → (∀ Z, Feasible Q D Z → obj β B Y ≤ obj β B Z) → Y = X) ∧
      (∃ ν, 0 < ν ∧ (Q * X).trace = D ∧ X = waterfill (tilt ν β Q B X)) ∧
      (∀ X' ν', 0 ≤ ν' → (Q * X').trace = D → X' = waterfill (tilt ν' β Q B X') → X' = X) := by
  obtain ⟨X, ν, hν, hD, hfix, hmin⟩ := tilted_waterfilling_exists B hQ hβ0 hβ1 hD0 hDQ
  obtain ⟨hXf, -, huniq⟩ := tilted_waterfilling B hQ hβ0 hβ1 hν.le hfix hD
  refine ⟨X, ⟨hXf, hmin⟩, huniq, ⟨ν, hν, hD, hfix⟩, fun X' ν' hν' hD' hfix' => ?_⟩
  exact fixed_point_unique B hQ hβ0 hβ1 hν' hν.le hfix' hD' hfix hD

end Mult

end ObservationTheory.Tilted
