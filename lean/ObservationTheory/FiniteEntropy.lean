/-
A minimal finite-alphabet Shannon-entropy layer, written for the identity layer of Paper V
(`paper/consumer-relative-landauer.tex`). The pinned Mathlib (v4.32.2) has `Real.negMulLog`,
the binary entropy and Kullback–Leibler divergence for measures, but no entropy of finitely
supported random variables. This file supplies only what the identities need.

Conventions. A "law" on a finite type is any function `p : α → ℝ`; the lemmas state the
hypotheses they use (nonnegativity, total mass one) explicitly. Entropy is in nats:
`H p = ∑ a, negMulLog (p a)`, with `negMulLog x = -x * log x`. Laws of functions of a random
variable are pushforwards `push f p`. Conditional entropy is defined by the chain rule,
`H(A | S) = H(A, S) − H(S)`, on a law of the pair.

Contents:
* `negMulLog_sum_le` — `negMulLog` of a sum of nonnegative terms is at most the sum of the
  `negMulLog`s (the elementary fact behind coarse-graining).
* `H_push_le` — coarse-graining: `H (push f p) ≤ H p` (entropy cannot grow under a map).
* `H_push_injective` — relabeling: an injective map preserves entropy.
* `push_push` — pushforwards compose.
* `H_prod` — additivity on product laws: `H (p ⊗ q) = H p + H q` for laws of total mass one.
-/
import Mathlib

open Real Finset

namespace ObservationTheory.FiniteEntropy

variable {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]

/-- Shannon entropy, in nats, of a weight function on a finite type. -/
noncomputable def H (p : α → ℝ) : ℝ := ∑ a, negMulLog (p a)

/-- The law of `f X` when `X` has law `p`. -/
noncomputable def push [DecidableEq β] (f : α → β) (p : α → ℝ) : β → ℝ :=
  fun b => ∑ a ∈ univ.filter (fun a => f a = b), p a

omit [Fintype α] in
/-- `negMulLog` of a sum of nonnegative terms is at most the sum of the terms' `negMulLog`s. -/
lemma negMulLog_sum_le (s : Finset α) (x : α → ℝ) (hx : ∀ a ∈ s, 0 ≤ x a) :
    negMulLog (∑ a ∈ s, x a) ≤ ∑ a ∈ s, negMulLog (x a) := by
  set T := ∑ a ∈ s, x a with hT
  have hsplit : negMulLog T = ∑ a ∈ s, -(x a) * log T := by
    simp only [Real.negMulLog]
    rw [← Finset.sum_mul, Finset.sum_neg_distrib]
  rw [hsplit]
  apply Finset.sum_le_sum
  intro a ha
  have hxa := hx a ha
  simp only [Real.negMulLog]
  rcases hxa.lt_or_eq with hpos | hzero
  · have hle : x a ≤ T := Finset.single_le_sum hx ha
    have hlog : log (x a) ≤ log T := Real.log_le_log hpos hle
    nlinarith
  · rw [← hzero]; simp

/-- Coarse-graining: the entropy of `f X` is at most that of `X`. -/
lemma H_push_le [DecidableEq β] (f : α → β) (p : α → ℝ) (hp : ∀ a, 0 ≤ p a) :
    H (push f p) ≤ H p := by
  unfold H push
  calc ∑ b, negMulLog (∑ a ∈ univ.filter (fun a => f a = b), p a)
      ≤ ∑ b, ∑ a ∈ univ.filter (fun a => f a = b), negMulLog (p a) := by
        apply Finset.sum_le_sum
        intro b _
        exact negMulLog_sum_le _ _ (fun a _ => hp a)
    _ = ∑ a, negMulLog (p a) := Finset.sum_fiberwise univ f (fun a => negMulLog (p a))

/-- Relabeling: an injective map preserves entropy. -/
lemma H_push_injective [DecidableEq β] (f : α → β) (hf : Function.Injective f)
    (p : α → ℝ) : H (push f p) = H p := by
  unfold H push
  rw [← Finset.sum_fiberwise univ f (fun a => negMulLog (p a))]
  apply Finset.sum_congr rfl
  intro b _
  by_cases h : ∃ a, f a = b
  · obtain ⟨a, rfl⟩ := h
    have hs : univ.filter (fun a' => f a' = f a) = {a} := by
      ext a'
      simp [hf.eq_iff]
    rw [hs]
    simp
  · simp only [not_exists] at h
    have hs : univ.filter (fun a' => f a' = b) = ∅ := by
      ext a'
      simp [h a']
    rw [hs]
    simp

omit [Fintype γ] in
/-- Pushforwards compose. -/
lemma push_push [DecidableEq β] [DecidableEq γ] (g : α → β) (f : β → γ) (p : α → ℝ) :
    push f (push g p) = push (f ∘ g) p := by
  funext c
  unfold push
  rw [Finset.sum_filter, Finset.sum_filter,
    ← Finset.sum_fiberwise univ g (fun a => if (f ∘ g) a = c then p a else 0)]
  apply Finset.sum_congr rfl
  intro b _
  by_cases hb : f b = c
  · rw [if_pos hb]
    apply Finset.sum_congr rfl
    intro a ha
    have hga : g a = b := (Finset.mem_filter.mp ha).2
    simp [Function.comp, hga, hb]
  · rw [if_neg hb]
    symm
    apply Finset.sum_eq_zero
    intro a ha
    have hga : g a = b := (Finset.mem_filter.mp ha).2
    simp [Function.comp, hga, hb]

/-- Additivity on product laws of total mass one. -/
lemma H_prod (p : α → ℝ) (q : β → ℝ) (hp : ∑ a, p a = 1) (hq : ∑ b, q b = 1) :
    H (fun x : α × β => p x.1 * q x.2) = H p + H q := by
  unfold H
  rw [Fintype.sum_prod_type]
  simp only [Real.negMulLog_mul, Finset.sum_add_distrib]
  simp only [← Finset.sum_mul, ← Finset.mul_sum, hq, one_mul]
  rw [hp, one_mul]

omit [Fintype β] in
/-- Pushing forward along the identity changes nothing. -/
lemma push_id [DecidableEq α] (p : α → ℝ) : push id p = p := by
  funext b
  unfold push
  have hs : univ.filter (fun a : α => id a = b) = {b} := by
    ext a
    simp
  rw [hs, Finset.sum_singleton]

/-! ### Conditional entropy -/

variable {σ : Type*} [Fintype σ] [DecidableEq σ]

/-- `H(A | S) = H(A, S) − H(S)` for a law `p` of the pair `(A, S)`. -/
noncomputable def condH (p : α × σ → ℝ) : ℝ := H p - H (push Prod.snd p)

/-- Conditional coarse-graining: `H(g A | S) ≤ H(A | S)`. -/
lemma condH_push_le [DecidableEq β] (g : α → β) (p : α × σ → ℝ) (hp : ∀ x, 0 ≤ p x) :
    condH (push (Prod.map g id) p) ≤ condH p := by
  unfold condH
  have hmarg : push Prod.snd (push (Prod.map g id) p) = push Prod.snd p := by
    rw [push_push]
    rfl
  rw [hmarg]
  linarith [H_push_le (Prod.map g id) p hp]

/-- The materialization identity behind Paper V's Theorem 2: storing a deterministic
description `M = f A` beside `A` adds no conditional entropy, whatever `f` is,
`H(A, f A | S) = H(A | S)`. -/
lemma condH_materialize [DecidableEq α] [DecidableEq β] (f : α → β) (p : α × σ → ℝ) :
    condH (push (fun x : α × σ => ((x.1, f x.1), x.2)) p) = condH p := by
  unfold condH
  have hinj : Function.Injective (fun x : α × σ => ((x.1, f x.1), x.2)) := by
    intro x y h
    simp only [Prod.mk.injEq] at h
    exact Prod.ext h.1.1 h.2
  have hmarg : push Prod.snd (push (fun x : α × σ => ((x.1, f x.1), x.2)) p) =
      push Prod.snd p := by
    rw [push_push]
    rfl
  rw [hmarg, H_push_injective _ hinj]

omit [Fintype α] [Fintype β] [Fintype σ] [DecidableEq σ] in
/-- The termwise Gibbs step: with `r ≤ x`, `r ≤ y`, `r ≤ z` all nonnegative,
`r (log x + log y − log r − log z) ≤ x y / z − r`. -/
lemma gibbs_term (r x y z : ℝ) (hr : 0 ≤ r) (hx : r ≤ x) (hy : r ≤ y) (hz : r ≤ z)
    (hx0 : 0 ≤ x) (hy0 : 0 ≤ y) (hz0 : 0 ≤ z) :
    r * (log x + log y - log r - log z) ≤ x * y / z - r := by
  rcases hr.lt_or_eq with hpos | hzero
  · have hxp : 0 < x := lt_of_lt_of_le hpos hx
    have hyp : 0 < y := lt_of_lt_of_le hpos hy
    have hzp : 0 < z := lt_of_lt_of_le hpos hz
    have hq : 0 < x * y / (r * z) := by positivity
    have hlog : log x + log y - log r - log z = log (x * y / (r * z)) := by
      rw [Real.log_div (by positivity) (by positivity), Real.log_mul hxp.ne' hyp.ne',
        Real.log_mul hpos.ne' hzp.ne']
      ring
    rw [hlog]
    have h1 := Real.log_le_sub_one_of_pos hq
    have h2 : r * log (x * y / (r * z)) ≤ r * (x * y / (r * z) - 1) :=
      mul_le_mul_of_nonneg_left h1 hpos.le
    have h3 : r * (x * y / (r * z) - 1) = x * y / z - r := by
      field_simp
    linarith
  · rw [← hzero]
    simp only [zero_mul, sub_zero]
    positivity

omit [Fintype β] [Fintype σ] [DecidableEq σ] in
/-- `negMulLog` of a sum, spread over its terms with the sum's own logarithm. -/
lemma negMulLog_sum_eq (s : Finset β) (x : β → ℝ) :
    negMulLog (∑ b ∈ s, x b) = ∑ b ∈ s, -(x b) * log (∑ b' ∈ s, x b') := by
  simp only [Real.negMulLog]
  rw [← Finset.sum_mul, Finset.sum_neg_distrib]

omit [Fintype σ] [DecidableEq σ] in
/-- Subadditivity for nonnegative weights of any total mass `t`:
`H(A, B) + negMulLog t ≤ H(A) + H(B)`, i.e. `I(A; B) ≥ 0` (normalized). -/
lemma subadd_unnorm (r : α → β → ℝ) (hr : ∀ a b, 0 ≤ r a b) :
    (∑ a, ∑ b, negMulLog (r a b)) + negMulLog (∑ a, ∑ b, r a b)
      ≤ (∑ a, negMulLog (∑ b, r a b)) + ∑ b, negMulLog (∑ a, r a b) := by
  set rA : α → ℝ := fun a => ∑ b, r a b with hrA
  set rB : β → ℝ := fun b => ∑ a, r a b with hrB
  set t : ℝ := ∑ a, ∑ b, r a b with ht
  have hrA0 : ∀ a, 0 ≤ rA a := fun a => Finset.sum_nonneg (fun b _ => hr a b)
  have hrB0 : ∀ b, 0 ≤ rB b := fun b => Finset.sum_nonneg (fun a _ => hr a b)
  have ht0 : 0 ≤ t := Finset.sum_nonneg (fun a _ => hrA0 a)
  have hleA : ∀ a b, r a b ≤ rA a := fun a b =>
    Finset.single_le_sum (f := fun b => r a b) (fun b _ => hr a b) (Finset.mem_univ b)
  have hleB : ∀ a b, r a b ≤ rB b := fun a b =>
    Finset.single_le_sum (f := fun a => r a b) (fun a _ => hr a b) (Finset.mem_univ a)
  have hleT : ∀ a b, r a b ≤ t := fun a b =>
    le_trans (hleA a b) (Finset.single_le_sum (f := rA) (fun a _ => hrA0 a) (Finset.mem_univ a))
  have hsumB : ∑ b, rB b = t := by
    simp only [hrB, ht]
    exact Finset.sum_comm
  -- express every term as a double sum over (a, b)
  have eR : ∑ a, ∑ b, negMulLog (r a b) = ∑ a, ∑ b, -(r a b) * log (r a b) := by
    simp only [Real.negMulLog]
  have eT : negMulLog t = ∑ a, ∑ b, -(r a b) * log t := by
    have hdef : negMulLog t = -t * log t := rfl
    rw [hdef]
    simp only [neg_mul, Finset.sum_neg_distrib, ← Finset.sum_mul]
    rfl
  have eA : ∑ a, negMulLog (rA a) = ∑ a, ∑ b, -(r a b) * log (rA a) := by
    apply Finset.sum_congr rfl
    intro a _
    rw [hrA]
    exact negMulLog_sum_eq _ _
  have eB : ∑ b, negMulLog (rB b) = ∑ a, ∑ b, -(r a b) * log (rB b) := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro b _
    rw [hrB]
    exact negMulLog_sum_eq _ _
  -- the Gibbs bound, termwise, and its sum
  have key : ∑ a, ∑ b, r a b * (log (rA a) + log (rB b) - log (r a b) - log t)
      ≤ ∑ a, ∑ b, (rA a * rB b / t - r a b) :=
    Finset.sum_le_sum (fun a _ => Finset.sum_le_sum (fun b _ =>
      gibbs_term _ _ _ _ (hr a b) (hleA a b) (hleB a b) (hleT a b) (hrA0 a) (hrB0 b) ht0))
  have zero : ∑ a, ∑ b, (rA a * rB b / t - r a b) = 0 := by
    have h1 : ∑ a, ∑ b, rA a * rB b / t = (∑ a, rA a) * (∑ b, rB b) / t := by
      rw [Finset.sum_mul_sum, Finset.sum_div]
      apply Finset.sum_congr rfl
      intro a _
      rw [Finset.sum_div]
    have h2 : ∑ a, ∑ b, (rA a * rB b / t - r a b)
        = ∑ a, ∑ b, rA a * rB b / t - ∑ a, ∑ b, r a b := by
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro a _
      rw [Finset.sum_sub_distrib]
    have hsumA : ∑ a, rA a = t := rfl
    rw [h2, h1, hsumB, hsumA, mul_self_div_self]
    show t - t = 0
    exact sub_self t
  rw [eR, eT, eA, eB]
  have expand : ∑ a, ∑ b, r a b * (log (rA a) + log (rB b) - log (r a b) - log t)
      = (∑ a, ∑ b, -(r a b) * log (r a b)) + (∑ a, ∑ b, -(r a b) * log t)
        - (∑ a, ∑ b, -(r a b) * log (rA a)) - (∑ a, ∑ b, -(r a b) * log (rB b)) := by
    simp only [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro a _
    apply Finset.sum_congr rfl
    intro b _
    ring
  linarith [key, zero, expand]

omit [DecidableEq σ] in
/-- Conditional subadditivity, explicit form: `H(A, B | S) ≤ H(A | S) + H(B | S)` for any
nonnegative law `r a b s` of `(A, B, S)`. Equivalently the conditional mutual information
`I(A; B | S)` is nonnegative. -/
lemma condSubadd_explicit (r : α → β → σ → ℝ) (hr : ∀ a b s, 0 ≤ r a b s) :
    (∑ s, ∑ a, ∑ b, negMulLog (r a b s)) + ∑ s, negMulLog (∑ a, ∑ b, r a b s)
      ≤ (∑ s, ∑ a, negMulLog (∑ b, r a b s)) + ∑ s, ∑ b, negMulLog (∑ a, r a b s) := by
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  exact Finset.sum_le_sum (fun s _ => subadd_unnorm (fun a b => r a b s) (fun a b => hr a b s))

/-! ### Marginals of a law of `(A, B, S)`, evaluated -/

section Marginals

variable [DecidableEq α] [DecidableEq β]

omit [DecidableEq β] in
lemma push_AS_apply (p : (α × β) × σ → ℝ) (a : α) (s : σ) :
    push (fun x : (α × β) × σ => (x.1.1, x.2)) p (a, s) = ∑ b, p ((a, b), s) := by
  unfold push
  rw [Finset.sum_filter, Fintype.sum_prod_type, Fintype.sum_prod_type]
  simp [Prod.mk.injEq, ite_and, Finset.sum_ite_eq']

omit [DecidableEq α] in
lemma push_BS_apply (p : (α × β) × σ → ℝ) (b : β) (s : σ) :
    push (fun x : (α × β) × σ => (x.1.2, x.2)) p (b, s) = ∑ a, p ((a, b), s) := by
  unfold push
  rw [Finset.sum_filter, Fintype.sum_prod_type, Fintype.sum_prod_type]
  simp [Prod.mk.injEq, ite_and, Finset.sum_ite_eq']

omit [DecidableEq α] [DecidableEq β] in
lemma push_S_apply (p : (α × β) × σ → ℝ) (s : σ) :
    push (fun x : (α × β) × σ => x.2) p s = ∑ a, ∑ b, p ((a, b), s) := by
  unfold push
  rw [Finset.sum_filter, Fintype.sum_prod_type, Fintype.sum_prod_type]
  simp [Finset.sum_ite_eq']

/-- Conditional subadditivity for a law of `(A, B, S)`:
`H(A, B | S) ≤ H(A | S) + H(B | S)`. -/
lemma condH_subadd (p : (α × β) × σ → ℝ) (hp : ∀ x, 0 ≤ p x) :
    condH p ≤ condH (push (fun x : (α × β) × σ => (x.1.1, x.2)) p)
      + condH (push (fun x : (α × β) × σ => (x.1.2, x.2)) p) := by
  unfold condH
  have mA : push Prod.snd (push (fun x : (α × β) × σ => (x.1.1, x.2)) p)
      = push (fun x : (α × β) × σ => x.2) p := by rw [push_push]; rfl
  have mB : push Prod.snd (push (fun x : (α × β) × σ => (x.1.2, x.2)) p)
      = push (fun x : (α × β) × σ => x.2) p := by rw [push_push]; rfl
  have mS : push Prod.snd p = push (fun x : (α × β) × σ => x.2) p := rfl
  rw [mA, mB, mS]
  have hJ : H p = ∑ s, ∑ a, ∑ b, negMulLog (p ((a, b), s)) := by
    unfold H
    rw [Fintype.sum_prod_type, Fintype.sum_prod_type]
    calc ∑ a, ∑ b, ∑ s, negMulLog (p ((a, b), s))
        = ∑ a, ∑ s, ∑ b, negMulLog (p ((a, b), s)) := by
          apply Finset.sum_congr rfl
          intro a _
          exact Finset.sum_comm
      _ = ∑ s, ∑ a, ∑ b, negMulLog (p ((a, b), s)) := Finset.sum_comm
  have hA : H (push (fun x : (α × β) × σ => (x.1.1, x.2)) p)
      = ∑ s, ∑ a, negMulLog (∑ b, p ((a, b), s)) := by
    unfold H
    rw [Fintype.sum_prod_type, Finset.sum_comm]
    simp only [push_AS_apply]
  have hB : H (push (fun x : (α × β) × σ => (x.1.2, x.2)) p)
      = ∑ s, ∑ b, negMulLog (∑ a, p ((a, b), s)) := by
    unfold H
    rw [Fintype.sum_prod_type, Finset.sum_comm]
    simp only [push_BS_apply]
  have hS : H (push (fun x : (α × β) × σ => x.2) p)
      = ∑ s, negMulLog (∑ a, ∑ b, p ((a, b), s)) := by
    unfold H
    simp only [push_S_apply]
  rw [hJ, hA, hB, hS]
  have := condSubadd_explicit (fun a b s => p ((a, b), s)) (fun a b s => hp _)
  linarith

end Marginals

end ObservationTheory.FiniteEntropy
