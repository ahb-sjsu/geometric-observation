/-
GO-16 (the adversarial observer) — machine-checked load-bearing algebra
of the revelation reduction (Theorem 1, `paper/go16-adversarial-observer.tex`
v0.2).

The analytic theorem: leakage to a rank-budgeted adversarial reader
depends on the record policy (F, Σ_w) only through the revelation
operator K = FᵀN⁻¹F, and the minimal value cost to achieve K is
tr(S(1−K)Sᵀ), attained by the shrink-and-dither policy F = SK,
Σ_w = SK(1−K)Sᵀ.  Four algebraic facts carry the proof; they are the
ones formalized here:

* `shrink_dither_key` — the noncommutative ring identity
  (1−K)(1−K) + K(1−K) = 1−K, which makes the shrink-and-dither cost
  telescope.
* `shrink_dither_cost` — the achievability side: the exact cost of
  the policy (F = SK, Σ_w = SK(1−K)Sᵀ) is S(1−K)Sᵀ as a matrix
  (trace it to get the scalar cost), for symmetric K.
* `trace_sq_le_trace_mul_transpose` — tr(Z²) ≤ tr(ZZᵀ): the converse
  side's only inequality (it bounds tr(sym Z)² by tr(ZZᵀ) and hence
  the achieved Gram by tr(SKSᵀ)).
* `scalar_shielding_identity` / `scalar_shielding_cost_bound` — the
  per-coordinate exact-completion-of-squares behind the diagonal
  water-level theorem (Theorem 3): shielding a coordinate to SNR ρ
  costs exactly s²(1−ρ), the linear cost that forces the bang-bang /
  water-level structure and the on-support ties.

Unformalized remainder (named, per house rule): Ky Fan's maximum
principle (φ_k as a support function), the minimax/saddle existence,
and the KKT partition bookkeeping of Theorems 2–3.  These are
standard-cited or covered by the numerical harness
`experiments/go16_verify_partition.py` (ALL PASS 9/9).
-/

import Mathlib

set_option linter.unusedSectionVars false

namespace ObservationTheory.AdversarialObserver

open Matrix BigOperators Finset

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq n]

/-- The noncommutative ring identity that makes the shrink-and-dither
cost telescope: `(1−K)(1−K) + K(1−K) = 1−K`. -/
theorem shrink_dither_key {R : Type*} [Ring R] (K : R) :
    (1 - K) * (1 - K) + K * (1 - K) = 1 - K := by
  noncomm_ring

/-- Achievability cost identity (matrix form).  For symmetric `K`, the
shrink-and-dither policy `F = S*K`, `Σ_w = S*K*(1−K)*Sᵀ` has
`(F − S)(F − S)ᵀ + Σ_w = S*(1−K)*Sᵀ`; taking traces gives the cost
`tr(S(1−K)Sᵀ)` of Theorem 1(ii). -/
theorem shrink_dither_cost (S : Matrix m n ℝ) (K : Matrix n n ℝ)
    (hK : Kᵀ = K) :
    (S * K - S) * (S * K - S)ᵀ + S * (K * (1 - K)) * Sᵀ
      = S * (1 - K) * Sᵀ := by
  have h1 : S * K - S = S * (K - 1) := by
    rw [Matrix.mul_sub, Matrix.mul_one]
  have h2 : (S * (K - 1))ᵀ = (K - 1) * Sᵀ := by
    rw [transpose_mul, transpose_sub, transpose_one, hK]
  have key : (K - 1) * (K - 1) + K * (1 - K) = 1 - K := by noncomm_ring
  calc (S * K - S) * (S * K - S)ᵀ + S * (K * (1 - K)) * Sᵀ
      = S * (K - 1) * ((K - 1) * Sᵀ) + S * (K * (1 - K)) * Sᵀ := by
        rw [h1, h2]
    _ = S * ((K - 1) * (K - 1) + K * (1 - K)) * Sᵀ := by
        simp only [Matrix.mul_assoc, Matrix.mul_add, Matrix.add_mul]
    _ = S * (1 - K) * Sᵀ := by rw [key]

/-- `tr(AAᵀ) = Σᵢⱼ Aᵢⱼ²`, hence nonnegative. -/
theorem trace_mul_transpose_self_nonneg (A : Matrix n n ℝ) :
    0 ≤ trace (A * Aᵀ) := by
  have h : trace (A * Aᵀ) = ∑ i, ∑ j, (A i j) ^ 2 := by
    simp [Matrix.trace, Matrix.diag, Matrix.mul_apply,
      Matrix.transpose_apply, sq]
  rw [h]
  positivity

/-- The converse's only inequality: `tr(Z²) ≤ tr(ZZᵀ)` for real square
`Z` (equality iff `Z` symmetric — the case the optimal policy
realizes).  Proof: `0 ≤ tr((Z−Zᵀ)(Z−Zᵀ)ᵀ) = 2tr(ZZᵀ) − 2tr(Z²)`. -/
theorem trace_sq_le_trace_mul_transpose (Z : Matrix n n ℝ) :
    trace (Z * Z) ≤ trace (Z * Zᵀ) := by
  have h0 : 0 ≤ trace ((Z - Zᵀ) * (Z - Zᵀ)ᵀ) :=
    trace_mul_transpose_self_nonneg _
  have hexp : (Z - Zᵀ) * (Z - Zᵀ)ᵀ
      = Z * Zᵀ - Z * Z - Zᵀ * Zᵀ + Zᵀ * Z := by
    rw [transpose_sub, transpose_transpose]
    noncomm_ring
  have htt : trace (Zᵀ * Zᵀ) = trace (Z * Z) := by
    rw [← transpose_mul, trace_transpose]
  have hcomm : trace (Zᵀ * Z) = trace (Z * Zᵀ) := trace_mul_comm _ _
  rw [hexp] at h0
  simp only [trace_add, trace_sub] at h0
  rw [htt, hcomm] at h0
  linarith

/-- Per-coordinate exact completion of squares behind the diagonal
water-level theorem: for SNR `ρ ≠ 0`,
`(f−s)² + f²(1−ρ)/ρ = s²(1−ρ) + (f−ρs)²/ρ`. -/
theorem scalar_shielding_identity (f s ρ : ℝ) (hρ : ρ ≠ 0) :
    (f - s) ^ 2 + f ^ 2 * (1 - ρ) / ρ
      = s ^ 2 * (1 - ρ) + (f - ρ * s) ^ 2 / ρ := by
  field_simp
  ring

/-- The shielding cost bound: achieving SNR `ρ ∈ (0,1]` in a coordinate
with value weight `s` costs at least `s²(1−ρ)`, with the minimum at
the shrink-and-dither point `f = ρs` — the linear cost that forces the
bang-bang / water-level structure of Theorem 3. -/
theorem scalar_shielding_cost_bound (f s ρ : ℝ) (hρ : 0 < ρ) :
    s ^ 2 * (1 - ρ) ≤ (f - s) ^ 2 + f ^ 2 * (1 - ρ) / ρ := by
  rw [scalar_shielding_identity f s ρ (ne_of_gt hρ)]
  have : 0 ≤ (f - ρ * s) ^ 2 / ρ := div_nonneg (sq_nonneg _) (le_of_lt hρ)
  linarith

end ObservationTheory.AdversarialObserver
