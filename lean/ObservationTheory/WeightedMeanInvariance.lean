/-
WeightedMeanInvariance.lean — machine-checked boundary results for
"Observation Theory for Estimation and Control".

Formalizes, against Mathlib:

  1. **Proposition 1 (weighted posterior-mean invariance, discrete form).**
     For ANY matrix P with nonnegative quadratic form and any finite
     probability weighting, the mean minimizes the expected quadratic loss
     E[(X-a)ᵀP(X-a)] over the reference point a. Hence a fixed consumer
     weighting P_C does not move the optimal estimate off the (posterior)
     mean — OT does not create a new Kalman filter by reweighting state
     error. (The algebra needs surprisingly little: not even nonnegative
     weights — only that they sum to 1 and that m is the weighted mean.)

  2. **The rank-one value-of-observation identity (paper §5).**
     For a symmetric prior covariance Σ, a scalar measurement y = hᵀx + v
     with noise variance r, and a rank-one consumer P_C = g gᵀ, the
     consumer-relative value of observation is

        V_C = tr(P_C (Σ⁻ − Σ⁺)) = (gᵀ Σ h)² / (hᵀ Σ h + r).

     A sensor is valuable when its direction h, propagated through Σ,
     overlaps a direction g the consumer actually reads.

  Caveat recorded here on purpose: Proposition 1 is for FIXED P. A
  state-dependent consumer geometry P_C(x) breaks the argument, and the
  optimal estimate need no longer be the posterior mean.
-/
import Mathlib

namespace ObservationTheory

open Finset Matrix

variable {Ω : Type*} [Fintype Ω] {n : ℕ}

/-- The quadratic form `vᵀ P v` of a square matrix. -/
def quad (P : Matrix (Fin n) (Fin n) ℝ) (v : Fin n → ℝ) : ℝ :=
  v ⬝ᵥ P.mulVec v

/-- Bilinear expansion of the quadratic form — no symmetry needed. -/
lemma quad_add (P : Matrix (Fin n) (Fin n) ℝ) (u d : Fin n → ℝ) :
    quad P (u + d)
      = quad P u + u ⬝ᵥ P.mulVec d + d ⬝ᵥ P.mulVec u + quad P d := by
  simp only [quad, Matrix.mulVec_add, dotProduct_add, add_dotProduct]
  ring

/-- Swap a vector across the matrix in a dot product: `d ⬝ᵥ P u = u ⬝ᵥ Pᵀ d`. -/
lemma dot_mulVec_swap (P : Matrix (Fin n) (Fin n) ℝ) (d u : Fin n → ℝ) :
    d ⬝ᵥ P.mulVec u = u ⬝ᵥ Pᵀ.mulVec d := by
  simp only [dotProduct, Matrix.mulVec, dotProduct, Matrix.transpose_apply,
    Finset.mul_sum]
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => by ring

/-- Discrete expectation with weight function `w`. -/
def expec (w : Ω → ℝ) (f : Ω → ℝ) : ℝ := ∑ ω, w ω * f ω

/-- The centered process is orthogonal to constants: for any fixed vector `c`,
`E[(X − m) ⬝ᵥ c] = 0` whenever `m` is the `w`-mean of `X` and `∑ w = 1`. -/
lemma expec_centered_dot (w : Ω → ℝ) (X : Ω → Fin n → ℝ) (m c : Fin n → ℝ)
    (hw1 : ∑ ω, w ω = 1) (hm : ∀ i, ∑ ω, w ω * X ω i = m i) :
    expec w (fun ω => (X ω - m) ⬝ᵥ c) = 0 := by
  unfold expec
  have step1 : ∀ ω, w ω * ((X ω - m) ⬝ᵥ c)
      = ∑ i, (w ω * X ω i * c i - w ω * (m i * c i)) := by
    intro ω
    simp only [dotProduct, Pi.sub_apply, Finset.mul_sum]
    exact Finset.sum_congr rfl fun i _ => by ring
  calc ∑ ω, w ω * ((X ω - m) ⬝ᵥ c)
      = ∑ ω, ∑ i, (w ω * X ω i * c i - w ω * (m i * c i)) :=
        Finset.sum_congr rfl fun ω _ => step1 ω
    _ = ∑ i, ∑ ω, (w ω * X ω i * c i - w ω * (m i * c i)) := Finset.sum_comm
    _ = ∑ i, ((∑ ω, w ω * X ω i) * c i - (∑ ω, w ω) * (m i * c i)) := by
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [Finset.sum_sub_distrib, Finset.sum_mul, Finset.sum_mul]
    _ = ∑ i, (m i * c i - 1 * (m i * c i)) := by
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [hm i, hw1]
    _ = 0 := by simp

/-- **Proposition 1 — weighted posterior-mean invariance (discrete form).**
For any `P` with a nonnegative quadratic form, the expected weighted quadratic
loss about an arbitrary point `a` decomposes as the loss about the mean plus a
nonnegative bias term; hence the mean is optimal for EVERY such `P`.
This is the paper's boundary theorem: a fixed consumer weighting does not
move the optimal (posterior-mean / Kalman) estimate. -/
theorem weighted_mean_invariance
    (P : Matrix (Fin n) (Fin n) ℝ) (hP : ∀ v, 0 ≤ quad P v)
    (w : Ω → ℝ) (X : Ω → Fin n → ℝ) (m a : Fin n → ℝ)
    (hw1 : ∑ ω, w ω = 1) (hm : ∀ i, ∑ ω, w ω * X ω i = m i) :
    expec w (fun ω => quad P (X ω - m)) ≤ expec w (fun ω => quad P (X ω - a)) := by
  have decomp : ∀ ω, quad P (X ω - a)
      = quad P (X ω - m) + (X ω - m) ⬝ᵥ P.mulVec (m - a)
        + (X ω - m) ⬝ᵥ Pᵀ.mulVec (m - a) + quad P (m - a) := by
    intro ω
    have hx : X ω - a = (X ω - m) + (m - a) := by abel
    rw [hx, quad_add, dot_mulVec_swap P (m - a) (X ω - m)]
  have expand : expec w (fun ω => quad P (X ω - a))
      = expec w (fun ω => quad P (X ω - m))
        + expec w (fun ω => (X ω - m) ⬝ᵥ P.mulVec (m - a))
        + expec w (fun ω => (X ω - m) ⬝ᵥ Pᵀ.mulVec (m - a))
        + quad P (m - a) := by
    unfold expec
    rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    have : quad P (m - a) = ∑ ω, w ω * quad P (m - a) := by
      rw [← Finset.sum_mul, hw1, one_mul]
    rw [this, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun ω _ => ?_
    dsimp only
    rw [decomp ω]; ring
  rw [expand,
      expec_centered_dot w X m (P.mulVec (m - a)) hw1 hm,
      expec_centered_dot w X m (Pᵀ.mulVec (m - a)) hw1 hm]
  have := hP (m - a)
  linarith

/-! ### The rank-one consumer-relative value of observation (paper §5) -/

/-- Trace of a product of two rank-one matrices. -/
lemma trace_vecMulVec_mul (a b c d : Fin n → ℝ) :
    (Matrix.vecMulVec a b * Matrix.vecMulVec c d).trace = (b ⬝ᵥ c) * (d ⬝ᵥ a) := by
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.mul_apply,
    Matrix.vecMulVec_apply, dotProduct]
  rw [Finset.sum_mul_sum]
  conv_rhs => rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => by ring

/-- Scalar-measurement Kalman covariance update:
`Σ⁺ = Σ − (hᵀΣh + r)⁻¹ (Σh)(hᵀΣ)`. -/
noncomputable def kalmanUpdate (S : Matrix (Fin n) (Fin n) ℝ) (h : Fin n → ℝ) (r : ℝ) :
    Matrix (Fin n) (Fin n) ℝ :=
  S - (h ⬝ᵥ S.mulVec h + r)⁻¹ • Matrix.vecMulVec (S.mulVec h) (Sᵀ.mulVec h)

/-- **The rank-one value-of-observation identity.** For symmetric `Σ` and a
rank-one consumer `P_C = g gᵀ`, the consumer-relative value of a scalar
measurement `y = hᵀx + v`, `Var v = r`, is

  `V_C = tr(P_C (Σ − Σ⁺)) = (gᵀΣh)² / (hᵀΣh + r)`.

A sensor is operationally valuable exactly when its direction `h`, propagated
through the prior uncertainty `Σ`, overlaps a direction `g` the consumer
actually reads. -/
theorem value_of_observation_rank_one
    (S : Matrix (Fin n) (Fin n) ℝ) (hS : Sᵀ = S)
    (g h : Fin n → ℝ) (r : ℝ) (_hr : h ⬝ᵥ S.mulVec h + r ≠ 0) :
    (Matrix.vecMulVec g g * (S - kalmanUpdate S h r)).trace
      = (g ⬝ᵥ S.mulVec h) ^ 2 / (h ⬝ᵥ S.mulVec h + r) := by
  have hdiff : S - kalmanUpdate S h r
      = (h ⬝ᵥ S.mulVec h + r)⁻¹ • Matrix.vecMulVec (S.mulVec h) (S.mulVec h) := by
    unfold kalmanUpdate
    rw [hS, sub_sub_cancel]
  rw [hdiff, Matrix.mul_smul, Matrix.trace_smul, trace_vecMulVec_mul,
      dotProduct_comm (S.mulVec h) g, smul_eq_mul, pow_two, div_eq_mul_inv]
  ring

end ObservationTheory
