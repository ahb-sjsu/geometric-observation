/-
Independence and Chebyshev's bound for i.i.d. blocks on finite alphabets: the first
milestone of the time-boxed attempt at Paper V's Theorem 1 achievability
(`paper/consumer-relative-landauer.tex`, `thm:main-region`).

Contents:
* `sum_push_mul` — an expectation of a function of `f X` is an expectation under the law of
  `f X`.
* `sum_iid_mul_prod` — independence: `E[∏ⱼ hⱼ(Xⱼ)] = ∏ⱼ E[hⱼ(X)]` under `iid n p`.
* `sum_iid_mul_eval`, `sum_iid_mul_two` — one letter, and two distinct letters.
* `iid_second_moment` — for a centred `W`, `E[(∑ₖ W(Xₖ))²] = n E[W(X)²]`.
* `iid_chebyshev` — `P(|∑ₖ W(Xₖ)| ≥ n δ) ≤ E[W(X)²] / (n δ²)`.
-/
import ObservationTheory.IidBlocks

open Real Finset

namespace ObservationTheory.FiniteEntropy

variable {α β : Type*} [Fintype α] [Fintype β]

/-- An expectation of a function of `f X` is an expectation under the law of `f X`. -/
lemma sum_push_mul [DecidableEq β] (f : α → β) (p : α → ℝ) (F : β → ℝ) :
    ∑ a, p a * F (f a) = ∑ b, push f p b * F b := by
  unfold push
  simp only [Finset.sum_mul]
  rw [← Finset.sum_fiberwise univ f (fun a => p a * F (f a))]
  apply Finset.sum_congr rfl
  intro b _
  apply Finset.sum_congr rfl
  intro a ha
  show p a * F (f a) = p a * F b
  rw [(Finset.mem_filter.mp ha).2]

/-- **Independence:** `E[∏ⱼ hⱼ(Xⱼ)] = ∏ⱼ E[hⱼ(X)]` for an i.i.d. block. -/
lemma sum_iid_mul_prod (n : ℕ) (p : α → ℝ) (h : Fin n → α → ℝ) :
    ∑ x, iid n p x * ∏ j, h j (x j) = ∏ j, ∑ b, p b * h j b := by
  unfold iid
  simp_rw [← Finset.prod_mul_distrib]
  rw [Fintype.prod_sum]

/-- One letter of an i.i.d. block. -/
lemma sum_iid_mul_eval [DecidableEq α] (n : ℕ) (k : Fin n) (p : α → ℝ) (hp1 : ∑ a, p a = 1)
    (Z : α → ℝ) : ∑ x, iid n p x * Z (x k) = ∑ a, p a * Z a := by
  rw [sum_push_mul (fun x : Fin n → α => x k) (iid n p) Z, push_iid_eval n k p hp1]

/-- Two distinct letters of an i.i.d. block are independent. -/
lemma sum_iid_mul_two (n : ℕ) (k l : Fin n) (hkl : k ≠ l) (p : α → ℝ) (hp1 : ∑ a, p a = 1)
    (Z W : α → ℝ) :
    ∑ x, iid n p x * (Z (x k) * W (x l)) = (∑ a, p a * Z a) * (∑ a, p a * W a) := by
  have hprod : ∀ x : Fin n → α, Z (x k) * W (x l)
      = ∏ j, (if j = k then Z (x j) else 1) * (if j = l then W (x j) else 1) := by
    intro x
    rw [Finset.prod_mul_distrib, Finset.prod_ite_eq', Finset.prod_ite_eq']
    simp
  simp_rw [hprod]
  rw [sum_iid_mul_prod n p (fun j b => (if j = k then Z b else 1) * (if j = l then W b else 1)),
    Fintype.prod_eq_mul_prod_compl k]
  have hk : ∑ b, p b * ((if k = k then Z b else 1) * (if k = l then W b else 1))
      = ∑ a, p a * Z a := by
    simp [hkl]
  have hrest : ∏ j ∈ ({k} : Finset (Fin n))ᶜ,
      ∑ b, p b * ((if j = k then Z b else 1) * (if j = l then W b else 1))
      = ∏ j ∈ ({k} : Finset (Fin n))ᶜ, (if j = l then ∑ a, p a * W a else 1) := by
    apply Finset.prod_congr rfl
    intro j hj
    have hjk : j ≠ k := by simpa using hj
    by_cases hjl : j = l
    · subst hjl
      simp [hjk]
    · simp [hjk, hjl, hp1]
  rw [hk, hrest, Finset.prod_ite_eq']
  have hl : l ∈ ({k} : Finset (Fin n))ᶜ := by simpa using hkl.symm
  rw [if_pos hl]

/-- **Second moment of a centred i.i.d. sum:** `E[(∑ₖ W(Xₖ))²] = n E[W(X)²]` when `E[W(X)] = 0`. -/
theorem iid_second_moment [DecidableEq α] (n : ℕ) (p : α → ℝ) (hp1 : ∑ a, p a = 1)
    (W : α → ℝ) (hW : ∑ a, p a * W a = 0) :
    ∑ x, iid n p x * (∑ k, W (x k)) ^ 2 = n * ∑ a, p a * W a ^ 2 := by
  have expand : ∀ x : Fin n → α, iid n p x * (∑ k, W (x k)) ^ 2
      = ∑ k, ∑ l, iid n p x * (W (x k) * W (x l)) := by
    intro x
    rw [sq, Finset.sum_mul_sum, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro k _
    rw [Finset.mul_sum]
  have hkl : ∀ k l : Fin n, ∑ x, iid n p x * (W (x k) * W (x l))
      = if k = l then ∑ a, p a * W a ^ 2 else 0 := by
    intro k l
    by_cases h : k = l
    · subst h
      rw [if_pos rfl]
      have := sum_iid_mul_eval n k p hp1 (fun a => W a * W a)
      simp only [sq]
      exact this
    · rw [if_neg h, sum_iid_mul_two n k l h p hp1 W W, hW, zero_mul]
  calc ∑ x, iid n p x * (∑ k, W (x k)) ^ 2
      = ∑ x, ∑ k, ∑ l, iid n p x * (W (x k) * W (x l)) :=
        Finset.sum_congr rfl (fun x _ => expand x)
    _ = ∑ k, ∑ l, ∑ x, iid n p x * (W (x k) * W (x l)) :=
        Finset.sum_comm.trans (Finset.sum_congr rfl (fun k _ => Finset.sum_comm))
    _ = ∑ k : Fin n, ∑ l : Fin n, (if k = l then ∑ a, p a * W a ^ 2 else 0) := by
        apply Finset.sum_congr rfl
        intro k _
        apply Finset.sum_congr rfl
        intro l _
        exact hkl k l
    _ = n * ∑ a, p a * W a ^ 2 := by
        simp [Finset.sum_ite_eq]

/-- **Chebyshev's bound, the quantitative weak law** (the limit `n → ∞` is not stated): for a
centred `W`,
`P(|∑ₖ W(Xₖ)| ≥ n δ) ≤ E[W(X)²] / (n δ²)` under `iid n p`. -/
theorem iid_chebyshev [DecidableEq α] (n : ℕ) (hn : 0 < n) (p : α → ℝ) (hp : ∀ a, 0 ≤ p a)
    (hp1 : ∑ a, p a = 1) (W : α → ℝ) (hW : ∑ a, p a * W a = 0) (δ : ℝ) (hδ : 0 < δ) :
    ∑ x ∈ univ.filter (fun x : Fin n → α => n * δ ≤ |∑ k, W (x k)|), iid n p x
      ≤ (∑ a, p a * W a ^ 2) / (n * δ ^ 2) := by
  have hn' : (0 : ℝ) < n := by exact_mod_cast hn
  have hnδ : 0 < (n : ℝ) * δ := mul_pos hn' hδ
  have key : ∀ x ∈ univ.filter (fun x : Fin n → α => n * δ ≤ |∑ k, W (x k)|),
      iid n p x ≤ iid n p x * (∑ k, W (x k)) ^ 2 / (n * δ) ^ 2 := by
    intro x hx
    have h := (Finset.mem_filter.mp hx).2
    have hsq : (n * δ) ^ 2 ≤ (∑ k, W (x k)) ^ 2 := by
      rw [← sq_abs (∑ k, W (x k))]
      exact pow_le_pow_left₀ hnδ.le h 2
    rw [le_div_iff₀ (pow_pos hnδ 2)]
    exact mul_le_mul_of_nonneg_left hsq (iid_nonneg n p hp x)
  calc ∑ x ∈ univ.filter (fun x : Fin n → α => n * δ ≤ |∑ k, W (x k)|), iid n p x
      ≤ ∑ x ∈ univ.filter (fun x : Fin n → α => n * δ ≤ |∑ k, W (x k)|),
          iid n p x * (∑ k, W (x k)) ^ 2 / (n * δ) ^ 2 := Finset.sum_le_sum key
    _ ≤ ∑ x, iid n p x * (∑ k, W (x k)) ^ 2 / (n * δ) ^ 2 :=
        Finset.sum_le_sum_of_subset_of_nonneg (Finset.filter_subset _ _)
          (fun x _ _ => div_nonneg (mul_nonneg (iid_nonneg n p hp x) (sq_nonneg _)) (sq_nonneg _))
    _ = (n * ∑ a, p a * W a ^ 2) / (n * δ) ^ 2 := by
        rw [← Finset.sum_div, iid_second_moment n p hp1 W hW]
    _ = (∑ a, p a * W a ^ 2) / (n * δ ^ 2) := by
        rw [div_eq_div_iff (pow_pos hnδ 2).ne' (mul_pos hn' (pow_pos hδ 2)).ne']
        ring

end ObservationTheory.FiniteEntropy
