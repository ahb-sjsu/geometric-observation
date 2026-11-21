/-
The identity layer of Paper V (`paper/consumer-relative-landauer.tex`): the information
statements behind Theorem 2 (`thm:materialization`) and Corollary 3 (`cor:tc`), machine-checked
on finite alphabets with the entropy layer `ObservationTheory.FiniteEntropy`.

What is formalized, and what is not:
* Entropies are Shannon entropies in nats of finite laws; "reset content" is the conditional
  entropy of the memory given the retained side information. Reading `k_B T ln 2` times that
  content as ideal reset work is Landauer's bound, which the paper imports; it is not
  formalized here.
* Laws are given as functions to ℝ; each theorem lists the hypotheses it uses (nonnegativity).
  Total mass one is never needed by these identities.
* Theorem 2: `materialization` is the identity `H(A, f A | S) = H(A | S)`, for any law of
  `(A, S)` and any description map `f`. With `A = Xⁿ` and `S = Sⁿ` it is the paper's statement
  that the joint reset content is `H(Xⁿ | Sⁿ)` whatever the description is; the further step
  `H(Xⁿ | Sⁿ) = n H(X | S)` for an i.i.d. block is not in this file.
* Corollary 3, for two consumers (the paper states it for `m`): memories `M₁, M₂`, from which
  consumer `j` decodes `Uⱼ = gⱼ Mⱼ` alone, and retained side information `S`, with any joint law.
  - `cor3_joint_lower`: a joint (or fully coordinated) reset has content at least
    `H(U₁, U₂ | S)`;
  - `cor3_coordinated_chain`: resetting `M₁` with `(M₂, S)` retained, then `M₂` with `S`
    retained, costs exactly the joint content `H(M₁, M₂ | S)`;
  - `cor3_independent_lower`: independent resets, each seeing `S` only, cost at least
    `H(U₁ | S) + H(U₂ | S)`;
  - `cor3_tc_nonneg`: the gap between the two minima, the conditional total correlation
    `H(U₁ | S) + H(U₂ | S) − H(U₁, U₂ | S)`, is nonnegative;
  - `cor3_attained`: the code that stores `Mⱼ = Uⱼ` attains both minima.
  The per-symbol normalization for i.i.d. blocks, and general `m`, are not in this file.
-/
import ObservationTheory.FiniteEntropy

open Real Finset

namespace ObservationTheory.ConsumerLandauer

open ObservationTheory.FiniteEntropy

variable {α μ σ : Type*} [Fintype α] [Fintype μ] [Fintype σ]
  [DecidableEq α] [DecidableEq μ] [DecidableEq σ]

/-- **Theorem 2 (materialization), information form.** Storing a deterministic description
`M = f A` beside the full record `A` leaves the joint reset content at `H(A | S)`, whatever the
description: `H(A, f A | S) = H(A | S)`. -/
theorem materialization (f : α → μ) (p : α × σ → ℝ) :
    condH (push (fun x : α × σ => ((x.1, f x.1), x.2)) p) = condH p :=
  condH_materialize f p

section Corollary3

variable {μ₁ μ₂ υ₁ υ₂ : Type*} [Fintype μ₁] [Fintype μ₂] [Fintype υ₁] [Fintype υ₂]
  [DecidableEq μ₁] [DecidableEq μ₂] [DecidableEq υ₁] [DecidableEq υ₂]

/-- The law of the two consumers' outputs `(U₁, U₂) = (g₁ M₁, g₂ M₂)` with `S`. -/
noncomputable def outputLaw (g₁ : μ₁ → υ₁) (g₂ : μ₂ → υ₂) (p : (μ₁ × μ₂) × σ → ℝ) :
    (υ₁ × υ₂) × σ → ℝ :=
  push (Prod.map (Prod.map g₁ g₂) id) p

/-- `H(M₁ | M₂, S) = H(M₁, M₂, S) − H(M₂, S)`, for a law of `((M₁, M₂), S)`. -/
noncomputable def condH_first_given_rest (p : (μ₁ × μ₂) × σ → ℝ) : ℝ :=
  H p - H (push (fun x : (μ₁ × μ₂) × σ => (x.1.2, x.2)) p)

omit [DecidableEq μ₁] [DecidableEq μ₂] in
/-- **Corollary 3, joint minimum.** Any code's joint content is at least `H(U₁, U₂ | S)`. -/
theorem cor3_joint_lower (g₁ : μ₁ → υ₁) (g₂ : μ₂ → υ₂) (p : (μ₁ × μ₂) × σ → ℝ)
    (hp : ∀ x, 0 ≤ p x) :
    condH (outputLaw g₁ g₂ p) ≤ condH p :=
  condH_push_le (Prod.map g₁ g₂) p hp

omit [DecidableEq μ₁] in
/-- **Corollary 3, coordinated resets.** Resetting `M₁` while `M₂` and `S` are retained, then
`M₂` while `S` is retained, costs exactly the joint content `H(M₁, M₂ | S)`. -/
theorem cor3_coordinated_chain (p : (μ₁ × μ₂) × σ → ℝ) :
    condH_first_given_rest p + condH (push (fun x : (μ₁ × μ₂) × σ => (x.1.2, x.2)) p)
      = condH p := by
  unfold condH_first_given_rest condH
  have hS : push Prod.snd (push (fun x : (μ₁ × μ₂) × σ => (x.1.2, x.2)) p)
      = push Prod.snd p := by rw [push_push]; rfl
  rw [hS]
  ring

/-- **Corollary 3, independent minimum.** If each memory is reset seeing `S` only, the summed
content is at least `H(U₁ | S) + H(U₂ | S)`. -/
theorem cor3_independent_lower (g₁ : μ₁ → υ₁) (g₂ : μ₂ → υ₂) (p : (μ₁ × μ₂) × σ → ℝ)
    (hp : ∀ x, 0 ≤ p x) :
    condH (push (fun x : (μ₁ × μ₂) × σ => (g₁ x.1.1, x.2)) p)
      + condH (push (fun x : (μ₁ × μ₂) × σ => (g₂ x.1.2, x.2)) p)
      ≤ condH (push (fun x : (μ₁ × μ₂) × σ => (x.1.1, x.2)) p)
      + condH (push (fun x : (μ₁ × μ₂) × σ => (x.1.2, x.2)) p) := by
  have hnn1 : ∀ y, 0 ≤ push (fun x : (μ₁ × μ₂) × σ => (x.1.1, x.2)) p y := fun y =>
    Finset.sum_nonneg (fun x _ => hp x)
  have hnn2 : ∀ y, 0 ≤ push (fun x : (μ₁ × μ₂) × σ => (x.1.2, x.2)) p y := fun y =>
    Finset.sum_nonneg (fun x _ => hp x)
  have e1 : push (fun x : (μ₁ × μ₂) × σ => (g₁ x.1.1, x.2)) p
      = push (Prod.map g₁ id) (push (fun x : (μ₁ × μ₂) × σ => (x.1.1, x.2)) p) := by
    rw [push_push]; rfl
  have e2 : push (fun x : (μ₁ × μ₂) × σ => (g₂ x.1.2, x.2)) p
      = push (Prod.map g₂ id) (push (fun x : (μ₁ × μ₂) × σ => (x.1.2, x.2)) p) := by
    rw [push_push]; rfl
  rw [e1, e2]
  exact add_le_add (condH_push_le g₁ _ hnn1) (condH_push_le g₂ _ hnn2)

/-- **Corollary 3, the gap.** The conditional total correlation of the outputs is nonnegative:
`H(U₁, U₂ | S) ≤ H(U₁ | S) + H(U₂ | S)`, for the law of the outputs. -/
theorem cor3_tc_nonneg (q : (υ₁ × υ₂) × σ → ℝ) (hq : ∀ x, 0 ≤ q x) :
    condH q ≤ condH (push (fun x : (υ₁ × υ₂) × σ => (x.1.1, x.2)) q)
      + condH (push (fun x : (υ₁ × υ₂) × σ => (x.1.2, x.2)) q) :=
  condH_subadd q hq

/-- **Corollary 3, attainment.** For the code that stores `Mⱼ = Uⱼ` (identity decoders), the
output law is the memory law, so both lower bounds hold with equality. -/
theorem cor3_attained (p : (υ₁ × υ₂) × σ → ℝ) :
    outputLaw (id : υ₁ → υ₁) (id : υ₂ → υ₂) p = p := by
  unfold outputLaw
  have : Prod.map (Prod.map (id : υ₁ → υ₁) (id : υ₂ → υ₂)) (id : σ → σ) = id := by
    funext x; rfl
  rw [this, push_id]

end Corollary3

end ObservationTheory.ConsumerLandauer
