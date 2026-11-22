/-
Blocks of independent, identically distributed letters, on finite alphabets, for Paper V
(`paper/consumer-relative-landauer.tex`), whose source block is `n` i.i.d. copies of `(X, S)`.

Contents:
* `iid n p` — the law of `n` independent copies of a letter with law `p`:
  `iid n p x = ∏ᵢ p (x i)`. `sum_iid`: its mass is `(∑ p)ⁿ`.
* `H_iid` — `H(Xⁿ) = n H(X)` for a law of total mass one.
* `push_iid` — a letterwise map of an i.i.d. block is the i.i.d. block of the mapped letter.
* `push_iid_eval` — each letter of the block has the letter law.
* `block n p` — the law of `(Xⁿ, Sⁿ)` when the pairs `(Xᵢ, Sᵢ)` are i.i.d. with law `p`
  (the i.i.d. law of the pairs, with the block of pairs read as a pair of blocks).
* `condH_block` — `H(Xⁿ | Sⁿ) = n H(X | S)`.
* `block_map` — `(v(X₁), …, v(Xₙ), Sⁿ)` is the block of the letter `(v X, S)`.
* `block_letter` — the `i`-th letter `(Xᵢ, Sᵢ)` of the block has law `p`.
-/
import ObservationTheory.EntropyTools

open Real Finset

namespace ObservationTheory.FiniteEntropy

variable {α β σ : Type*} [Fintype α] [Fintype β] [Fintype σ]

/-- The law of `n` independent copies of a letter with law `p`. -/
noncomputable def iid (n : ℕ) (p : α → ℝ) : (Fin n → α) → ℝ := fun x => ∏ i, p (x i)

omit [Fintype α] in
lemma iid_nonneg (n : ℕ) (p : α → ℝ) (hp : ∀ a, 0 ≤ p a) (x : Fin n → α) : 0 ≤ iid n p x :=
  Finset.prod_nonneg (fun i _ => hp (x i))

lemma sum_iid (n : ℕ) (p : α → ℝ) : ∑ x, iid n p x = (∑ a, p a) ^ n := by
  unfold iid
  rw [Fintype.sum_pow]

/-- **`H(Xⁿ) = n H(X)`** for i.i.d. letters with a law of total mass one. -/
theorem H_iid (n : ℕ) (p : α → ℝ) (hp1 : ∑ a, p a = 1) : H (iid n p) = n * H p := by
  induction n with
  | zero =>
    unfold H iid
    simp
  | succ n ih =>
    have hsplit : H (iid (n + 1) p) = H (fun z : α × (Fin n → α) => p z.1 * iid n p z.2) := by
      unfold H
      refine Fintype.sum_equiv (Fin.consEquiv (fun _ : Fin (n + 1) => α)).symm _ _ (fun x => ?_)
      show negMulLog (iid (n + 1) p x) = negMulLog (p (x 0) * iid n p (Fin.tail x))
      unfold iid
      rw [Fin.prod_univ_succ]
      rfl
    rw [hsplit, H_prod p (iid n p) hp1 (by rw [sum_iid, hp1, one_pow]), ih]
    push_cast
    ring

omit [Fintype β] in
/-- A letterwise map of an i.i.d. block is the i.i.d. block of the mapped letter. -/
lemma push_iid [DecidableEq α] [DecidableEq β] (n : ℕ) (f : α → β) (p : α → ℝ) :
    push (fun x : Fin n → α => fun i => f (x i)) (iid n p) = iid n (push f p) := by
  funext y
  unfold push iid
  simp_rw [Finset.sum_filter]
  rw [Fintype.prod_sum]
  apply Finset.sum_congr rfl
  intro x _
  rw [Finset.prod_ite_zero]
  by_cases h : ∀ i, f (x i) = y i
  · simp [h]
  · have h' : (fun i => f (x i)) ≠ y := fun hh => h (fun i => congrFun hh i)
    simp [h, h']

/-- Each letter of an i.i.d. block has the letter law. -/
lemma push_iid_eval [DecidableEq α] (n : ℕ) (i : Fin n) (p : α → ℝ) (hp1 : ∑ a, p a = 1) :
    push (fun x : Fin n → α => x i) (iid n p) = p := by
  funext a
  unfold push iid
  rw [Finset.sum_filter]
  have hterm : ∀ x : Fin n → α, (if x i = a then ∏ j, p (x j) else 0)
      = ∏ j, (if j = i then (if x j = a then p (x j) else 0) else p (x j)) := by
    intro x
    rw [Fintype.prod_eq_mul_prod_compl i (fun j => p (x j)),
      Fintype.prod_eq_mul_prod_compl i
        (fun j => if j = i then (if x j = a then p (x j) else 0) else p (x j))]
    have hrest : ∏ j ∈ ({i} : Finset (Fin n))ᶜ,
        (if j = i then (if x j = a then p (x j) else 0) else p (x j))
        = ∏ j ∈ ({i} : Finset (Fin n))ᶜ, p (x j) := by
      apply Finset.prod_congr rfl
      intro j hj
      have hji : j ≠ i := by simpa using hj
      rw [if_neg hji]
    rw [hrest, if_pos rfl]
    by_cases hx : x i = a <;> simp [hx]
  rw [Finset.sum_congr rfl (fun x _ => hterm x)]
  rw [← Fintype.prod_sum (fun j b => if j = i then (if b = a then p b else 0) else p b)]
  rw [Fintype.prod_eq_mul_prod_compl i]
  have hrest : ∏ j ∈ ({i} : Finset (Fin n))ᶜ,
      ∑ b, (if j = i then (if b = a then p b else 0) else p b) = 1 := by
    apply Finset.prod_eq_one
    intro j hj
    have hji : j ≠ i := by simpa using hj
    simp only [if_neg hji]
    exact hp1
  rw [hrest, mul_one]
  simp

/-! ### Blocks of pairs -/

variable [DecidableEq α] [DecidableEq σ]

/-- Read a block of pairs as a pair of blocks. -/
def blockSplit (n : ℕ) : (Fin n → α × σ) → (Fin n → α) × (Fin n → σ) :=
  fun x => (fun i => (x i).1, fun i => (x i).2)

omit [Fintype α] [Fintype σ] [DecidableEq α] [DecidableEq σ] in
lemma blockSplit_injective (n : ℕ) : Function.Injective (blockSplit (α := α) (σ := σ) n) := by
  intro x y h
  funext i
  have h1 : (blockSplit n x).1 i = (blockSplit n y).1 i := congrFun (congrArg Prod.fst h) i
  have h2 : (blockSplit n x).2 i = (blockSplit n y).2 i := congrFun (congrArg Prod.snd h) i
  exact Prod.ext h1 h2

/-- The law of `(Xⁿ, Sⁿ)` when the pairs `(Xᵢ, Sᵢ)` are i.i.d. with law `p`. -/
noncomputable def block (n : ℕ) (p : α × σ → ℝ) : (Fin n → α) × (Fin n → σ) → ℝ :=
  push (blockSplit n) (iid n p)

lemma block_nonneg (n : ℕ) (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z) (z : (Fin n → α) × (Fin n → σ)) :
    0 ≤ block n p z :=
  push_nonneg _ _ (iid_nonneg n p hp) z

lemma sum_block (n : ℕ) (p : α × σ → ℝ) (hp1 : ∑ z, p z = 1) : ∑ z, block n p z = 1 := by
  unfold block
  rw [sum_push, sum_iid, hp1, one_pow]

/-- **`H(Xⁿ | Sⁿ) = n H(X | S)`** for i.i.d. pairs with a law of total mass one. -/
theorem condH_block (n : ℕ) (p : α × σ → ℝ) (hp1 : ∑ z, p z = 1) :
    condH (block n p) = n * condH p := by
  unfold condH block
  have hS : push Prod.snd (push (blockSplit n) (iid n p)) = iid n (push Prod.snd p) := by
    rw [push_push, ← push_iid]
    rfl
  rw [hS, H_push_injective _ (blockSplit_injective n), H_iid n p hp1,
    H_iid n (push Prod.snd p) (by rw [sum_push, hp1])]
  ring

/-- A letterwise map of the block: `(v(X₁), …, v(Xₙ), Sⁿ)` is the block of `(v X, S)`. -/
lemma block_map [DecidableEq β] (n : ℕ) (v : α → β) (p : α × σ → ℝ) :
    push (Prod.map (fun x : Fin n → α => fun i => v (x i)) id) (block n p)
      = block n (push (Prod.map v id) p) := by
  unfold block
  rw [push_push, ← push_iid, push_push]
  rfl

/-- The `i`-th letter `(Xᵢ, Sᵢ)` of the block has the letter law. -/
lemma block_letter (n : ℕ) (i : Fin n) (p : α × σ → ℝ) (hp1 : ∑ z, p z = 1) :
    push (fun z : (Fin n → α) × (Fin n → σ) => (z.1 i, z.2 i)) (block n p) = p := by
  unfold block
  rw [push_push]
  exact push_iid_eval n i p hp1

end ObservationTheory.FiniteEntropy
