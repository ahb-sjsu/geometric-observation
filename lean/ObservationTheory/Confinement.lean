/-
Machine-checked core of the OT-3 / OT-3N confinement arguments
(`crucible/OT3-THEOREM.md`, `crucible/OT3-NOISY-THEOREM.md`).

What is formalized — deliberately the load-bearing algebra, where a
quantifier or sign error would be fatal and quiet:

* `reflection_pair_orthogonal` : u₊ = (e+w)/√2 and u₋ = (e-w)/√2 are
  orthogonal when e, w are orthonormal (the T1b adversary pair is a
  genuine orthonormal pair, so the ≤ 1/2 overlap conclusion bites).
* `confined_entry_identity` : for any v, v′ with ⟪v,w⟫ = ⟪v′,w⟫ = 0,
  the rank-one blocks agree: ⟪v, P₊ v′⟫ = ⟪v, P₋ v′⟫ where
  P± x = λ ⟪u±, x⟫ u±. This is the entire engine of T1b (noiseless
  oblivious indistinguishability) and of N1a (the noisy transcript
  distributions coincide because their means do and the noise law is
  operator-independent).
* `promise_entry_identity` : the same identity relativized to a
  subspace (the N4 / T2a side-information form): the hypotheses only
  ever mention orthogonality to w, so confinement inside any W
  containing e and w is literal reuse.

What is NOT formalized (and remains hand-proved / cited in the
markdown): the adaptive pilot argument (T1a), Davis–Kahan, Gaussian
operator-norm bounds, and the KL computation (the last is
machine-verified symbolically in `crucible/verify_theorems.py`).
-/

import Mathlib.Analysis.InnerProductSpace.Basic

open RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The T1b reflection pair is orthogonal: for orthonormal `e ⊥ w`,
`⟪e + w, e - w⟫ = 0`. (Normalization by √2 does not affect
orthogonality and is omitted.) -/
theorem reflection_pair_orthogonal
    (e w : E) (he : ⟪e, e⟫ = 1) (hw : ⟪w, w⟫ = 1)
    (hew : ⟪e, w⟫ = 0) :
    ⟪e + w, e - w⟫ = 0 := by
  have hwe : ⟪w, e⟫ = 0 := by
    rw [real_inner_comm]; exact hew
  simp only [inner_add_left, inner_sub_right, he, hw, hew, hwe]
  ring

/-- The rank-one read operator `P u x = λ ⟪u, x⟫ u` evaluated as a
block entry `⟪v, P u v′⟫`. -/
noncomputable def blockEntry (lam : ℝ) (u v v' : E) : ℝ :=
  lam * ⟪u, v'⟫ * ⟪v, u⟫

/-- **The confinement engine (T1b / N1a).** If the probing vectors
`v, v′` are orthogonal to the hidden direction `w`, the block entries
of the two adversary operators built on `e + w` and `e - w` coincide
exactly. Every observable number is therefore identical for the two
operators — the transcript identity of T1b, and (adding
operator-independent noise) the distribution identity of N1a. -/
theorem confined_entry_identity
    (lam : ℝ) (e w v v' : E)
    (hv : ⟪v, w⟫ = 0) (hv' : ⟪v', w⟫ = 0) :
    blockEntry lam (e + w) v v' = blockEntry lam (e - w) v v' := by
  have hwv : ⟪w, v'⟫ = 0 := by
    rw [real_inner_comm]; exact hv'
  unfold blockEntry
  simp only [inner_add_left, inner_sub_left, inner_add_right,
             inner_sub_right, hv, hwv]
  ring

/-- **The side-information form (T2a / N4).** The identity above never
mentions anything outside `{e, w, v, v′}`, so it holds verbatim inside
any promise subspace `W` containing `e` and `w`: confinement composes
with side information, which is why the cliff relocates to `d - k₀`
and never softens. Stated as a corollary to make the reuse explicit. -/
theorem promise_entry_identity
    (lam : ℝ) (e w v v' : E)
    (hv : ⟪v, w⟫ = 0) (hv' : ⟪v', w⟫ = 0) :
    blockEntry lam (e + w) v v' = blockEntry lam (e - w) v v' :=
  confined_entry_identity lam e w v v' hv hv'
