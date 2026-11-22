/-
Tools on top of the finite entropy layer `ObservationTheory.FiniteEntropy`, written for the
block-level and many-consumer statements of Paper V (`paper/consumer-relative-landauer.tex`).

Contents:
* `push_nonneg`, `sum_push` — pushforwards keep nonnegativity and total mass.
* `H_push_eq_of_factor` — two variables that are functions of each other have equal entropy.
* `condH_relabel`, `condH_eq_of_factor` — the same for conditional entropy, `S` fixed.
* `H_push_const_fst`, `condH_const` — a constant carries no conditional entropy.
* `condH_coarsen` — conditioning on a function of the side information cannot lower the
  conditional entropy: `H(A | S) ≤ H(A | h S)`.
* `condH_le_H_fst`, `H_le_log_card` — `H(A | S) ≤ H(A) ≤ log |A|` for a law of total mass one.
* `mask`, `H_mask_insert` — a tuple with the coordinates outside a finite set hidden, and how
  one more coordinate is revealed.
* `condH_pi_subadd` — conditional subadditivity for a finite family:
  `H(U₁, …, Uₘ | S) ≤ ∑ⱼ H(Uⱼ | S)`.
* `condH_chain` — the chain rule for a sequence of resets:
  `∑ⱼ H(Mⱼ | Mⱼ₊₁, …, Mₘ, S) = H(M₁, …, Mₘ | S)`.
-/
import ObservationTheory.FiniteEntropy

open Real Finset

namespace ObservationTheory.FiniteEntropy

variable {α β γ σ τ : Type*} [Fintype α] [Fintype β] [Fintype γ] [Fintype σ] [Fintype τ]

omit [Fintype β] in
lemma push_nonneg [DecidableEq β] (f : α → β) (p : α → ℝ) (hp : ∀ a, 0 ≤ p a) (b : β) :
    0 ≤ push f p b :=
  Finset.sum_nonneg (fun a _ => hp a)

lemma sum_push [DecidableEq β] (f : α → β) (p : α → ℝ) : ∑ b, push f p b = ∑ a, p a := by
  unfold push
  exact Finset.sum_fiberwise univ f p

/-- Two variables that are functions of each other have equal entropy. -/
lemma H_push_eq_of_factor [DecidableEq β] [DecidableEq γ] (f : α → β) (g : α → γ)
    (φ : β → γ) (ψ : γ → β) (hg : ∀ a, g a = φ (f a)) (hf : ∀ a, f a = ψ (g a))
    (p : α → ℝ) (hp : ∀ a, 0 ≤ p a) : H (push f p) = H (push g p) := by
  have e1 : push g p = push φ (push f p) := by
    rw [push_push]
    have : g = φ ∘ f := funext hg
    rw [this]
  have e2 : push f p = push ψ (push g p) := by
    rw [push_push]
    have : f = ψ ∘ g := funext hf
    rw [this]
  apply le_antisymm
  · calc H (push f p) = H (push ψ (push g p)) := by rw [← e2]
      _ ≤ H (push g p) := H_push_le ψ _ (push_nonneg g p hp)
  · calc H (push g p) = H (push φ (push f p)) := by rw [← e1]
      _ ≤ H (push f p) := H_push_le φ _ (push_nonneg f p hp)

section Conditional

variable [DecidableEq σ]

/-- Relabeling the conditioned variable injectively leaves the conditional entropy unchanged. -/
lemma condH_relabel [DecidableEq β] (e : α → β) (he : Function.Injective e)
    (p : α × σ → ℝ) : condH (push (Prod.map e id) p) = condH p := by
  unfold condH
  have hinj : Function.Injective (Prod.map e (id : σ → σ)) := by
    intro x y h
    have h1 : (Prod.map e id x).1 = (Prod.map e id y).1 := congrArg Prod.fst h
    have h2 : (Prod.map e id x).2 = (Prod.map e id y).2 := congrArg Prod.snd h
    exact Prod.ext (he h1) h2
  have hmarg : push Prod.snd (push (Prod.map e id) p) = push Prod.snd p := by
    rw [push_push]; rfl
  rw [hmarg, H_push_injective _ hinj]

/-- Two conditioned variables that are functions of each other (with `S` kept) have equal
conditional entropy given `S`. -/
lemma condH_eq_of_factor [DecidableEq β] [DecidableEq γ] (f : α × σ → β) (g : α × σ → γ)
    (φ : β → γ) (ψ : γ → β) (hg : ∀ z, g z = φ (f z)) (hf : ∀ z, f z = ψ (g z))
    (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z) :
    condH (push (fun z => (f z, z.2)) p) = condH (push (fun z => (g z, z.2)) p) := by
  unfold condH
  have m1 : push Prod.snd (push (fun z : α × σ => (f z, z.2)) p) = push Prod.snd p := by
    rw [push_push]; rfl
  have m2 : push Prod.snd (push (fun z : α × σ => (g z, z.2)) p) = push Prod.snd p := by
    rw [push_push]; rfl
  rw [m1, m2, H_push_eq_of_factor (fun z => (f z, z.2)) (fun z => (g z, z.2))
    (Prod.map φ id) (Prod.map ψ id) (fun z => Prod.ext (hg z) rfl)
    (fun z => Prod.ext (hf z) rfl) p hp]

/-- A constant beside `S` has the entropy of `S`. -/
lemma H_push_const_fst [DecidableEq β] (c : β) (p : α × σ → ℝ) :
    H (push (fun z : α × σ => (c, z.2)) p) = H (push Prod.snd p) := by
  have e : push (fun z : α × σ => (c, z.2)) p = push (fun s : σ => (c, s)) (push Prod.snd p) := by
    rw [push_push]; rfl
  have hinj : Function.Injective (fun s : σ => (c, s)) := fun s t h => congrArg Prod.snd h
  rw [e, H_push_injective _ hinj]

/-- A constant carries no conditional entropy. -/
lemma condH_const [DecidableEq β] (c : β) (p : α × σ → ℝ) :
    condH (push (fun z : α × σ => (c, z.2)) p) = 0 := by
  unfold condH
  have hmarg : push Prod.snd (push (fun z : α × σ => (c, z.2)) p) = push Prod.snd p := by
    rw [push_push]; rfl
  rw [hmarg, H_push_const_fst, sub_self]

/-- Coarsening the side information cannot lower the conditional entropy:
`H(A | S) ≤ H(A | h S)`. -/
lemma condH_coarsen [DecidableEq α] [DecidableEq τ] (h : σ → τ) (p : α × σ → ℝ)
    (hp : ∀ z, 0 ≤ p z) : condH p ≤ condH (push (Prod.map id h) p) := by
  have hsub := condH_subadd (push (fun z : α × σ => ((z.1, z.2), h z.2)) p) (push_nonneg _ p hp)
  have hWinj : Function.Injective (fun z : α × σ => ((z.1, z.2), h z.2)) := by
    intro x y hxy
    have h1 := congrArg Prod.fst hxy
    exact Prod.ext (congrArg Prod.fst h1) (congrArg Prod.snd h1)
  have hinjB : Function.Injective (fun s : σ => (s, h s)) := fun s t hst => congrArg Prod.fst hst
  have e1 : condH (push (fun z : α × σ => ((z.1, z.2), h z.2)) p)
      = H p - H (push Prod.snd (push (fun z : α × σ => ((z.1, z.2), h z.2)) p)) := by
    unfold condH; rw [H_push_injective _ hWinj]
  have e2 : push (fun x : (α × σ) × τ => (x.1.1, x.2)) (push (fun z : α × σ => ((z.1, z.2), h z.2)) p)
      = push (Prod.map id h) p := by
    rw [push_push]; rfl
  have e3 : condH (push (fun x : (α × σ) × τ => (x.1.2, x.2))
        (push (fun z : α × σ => ((z.1, z.2), h z.2)) p))
      = H (push Prod.snd p) - H (push Prod.snd (push (fun z : α × σ => ((z.1, z.2), h z.2)) p)) := by
    unfold condH
    have hB : push (fun x : (α × σ) × τ => (x.1.2, x.2))
        (push (fun z : α × σ => ((z.1, z.2), h z.2)) p)
        = push (fun s : σ => (s, h s)) (push Prod.snd p) := by
      rw [push_push, push_push]; rfl
    have hmB : push Prod.snd (push (fun x : (α × σ) × τ => (x.1.2, x.2))
        (push (fun z : α × σ => ((z.1, z.2), h z.2)) p))
        = push Prod.snd (push (fun z : α × σ => ((z.1, z.2), h z.2)) p) := by
      rw [push_push]; rfl
    rw [hmB, hB, H_push_injective _ hinjB]
  rw [e2] at hsub
  have e0 : condH p = H p - H (push Prod.snd p) := rfl
  linarith [hsub, e1, e3, e0]

omit [DecidableEq σ] in
lemma push_fst_apply [DecidableEq α] (q : α × σ → ℝ) (a : α) :
    push Prod.fst q a = ∑ s, q (a, s) := by
  unfold push
  rw [Finset.sum_filter, Fintype.sum_prod_type, Finset.sum_eq_single a]
  · simp
  · intro b _ hb
    simp [hb]
  · intro h
    exact absurd (Finset.mem_univ a) h

lemma push_snd_apply (q : α × σ → ℝ) (s : σ) :
    push Prod.snd q s = ∑ a, q (a, s) := by
  unfold push
  rw [Finset.sum_filter, Fintype.sum_prod_type]
  simp [Finset.sum_ite_eq']

/-- `H(A | S) ≤ H(A)` for a law of total mass one. -/
lemma condH_le_H_fst [DecidableEq α] (q : α × σ → ℝ) (hq : ∀ z, 0 ≤ q z)
    (hq1 : ∑ z, q z = 1) : condH q ≤ H (push Prod.fst q) := by
  have key := subadd_unnorm (fun a s => q (a, s)) (fun a s => hq (a, s))
  have hJ : H q = ∑ a, ∑ s, negMulLog (q (a, s)) := by
    unfold H; rw [Fintype.sum_prod_type]
  have hA : H (push Prod.fst q) = ∑ a, negMulLog (∑ s, q (a, s)) := by
    unfold H; simp only [push_fst_apply]
  have hS : H (push Prod.snd q) = ∑ s, negMulLog (∑ a, q (a, s)) := by
    unfold H; simp only [push_snd_apply]
  have ht : ∑ a, ∑ s, q (a, s) = 1 := by rw [← hq1, Fintype.sum_prod_type]
  rw [ht, Real.negMulLog_one, add_zero] at key
  unfold condH
  linarith [key, hJ, hA, hS]

end Conditional

/-- Entropy is at most the logarithm of the alphabet size, for a law of total mass one. -/
lemma H_le_log_card [Nonempty α] (q : α → ℝ) (hq : ∀ a, 0 ≤ q a) (hq1 : ∑ a, q a = 1) :
    H q ≤ log (Fintype.card α) := by
  have hNpos : (0 : ℝ) < Fintype.card α := by exact_mod_cast Fintype.card_pos
  have term : ∀ a, negMulLog (q a) - q a * log (Fintype.card α)
      ≤ 1 / (Fintype.card α : ℝ) - q a := by
    intro a
    rcases (hq a).lt_or_eq with hpos | hzero
    · have hx : 0 < 1 / ((Fintype.card α : ℝ) * q a) := one_div_pos.mpr (mul_pos hNpos hpos)
      have h1 := Real.log_le_sub_one_of_pos hx
      have hlog : log (1 / ((Fintype.card α : ℝ) * q a)) = - log (Fintype.card α) - log (q a) := by
        rw [one_div, Real.log_inv, Real.log_mul hNpos.ne' hpos.ne']; ring
      have h2 : q a * log (1 / ((Fintype.card α : ℝ) * q a))
          ≤ q a * (1 / ((Fintype.card α : ℝ) * q a) - 1) := mul_le_mul_of_nonneg_left h1 hpos.le
      have hq0 : q a ≠ 0 := hpos.ne'
      have hN0 : (Fintype.card α : ℝ) ≠ 0 := hNpos.ne'
      have h3 : q a * (1 / ((Fintype.card α : ℝ) * q a) - 1) = 1 / (Fintype.card α : ℝ) - q a := by
        field_simp
      rw [hlog] at h2
      simp only [Real.negMulLog]
      nlinarith [h2, h3]
    · rw [← hzero]
      simp only [Real.negMulLog_zero, zero_mul, sub_zero]
      exact div_nonneg zero_le_one hNpos.le
  have hsum := Finset.sum_le_sum (fun a (_ : a ∈ (univ : Finset α)) => term a)
  have hR : ∑ a, (1 / (Fintype.card α : ℝ) - q a) = 0 := by
    rw [Finset.sum_sub_distrib, hq1, Finset.sum_const, Finset.card_univ, nsmul_eq_mul,
      mul_one_div_cancel hNpos.ne', sub_self]
  have hL : ∑ a, (negMulLog (q a) - q a * log (Fintype.card α)) = H q - log (Fintype.card α) := by
    rw [Finset.sum_sub_distrib, ← Finset.sum_mul, hq1, one_mul]; rfl
  linarith [hsum, hR, hL]

/-! ### Finite families: masks, subadditivity, the chain rule -/

section Family

variable [DecidableEq σ] {ι : Type*} [Fintype ι] [DecidableEq ι] {υ : ι → Type*}
  [∀ i, Fintype (υ i)] [∀ i, DecidableEq (υ i)]

/-- The coordinates of `u` with index in `s`; the others are hidden (`none`). -/
def mask (s : Finset ι) (u : ∀ i, υ i) : ∀ i, Option (υ i) :=
  fun i => if i ∈ s then some (u i) else none

/-- Revealing one more coordinate: `(Uₐ, U_s)` and `U_{insert a s}` determine each other. -/
lemma H_mask_insert (a : ι) (s : Finset ι) (P : (∀ i, υ i) × σ → ℝ) (hP : ∀ z, 0 ≤ P z) :
    H (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)
      = H (push (fun z : (∀ i, υ i) × σ => (mask (insert a s) z.1, z.2)) P) := by
  have hinj : Function.Injective
      (fun x : (υ a × (∀ i, Option (υ i))) × σ => ((some x.1.1, x.1.2), x.2)) := by
    intro x y h
    simp only [Prod.mk.injEq, Option.some.injEq] at h
    exact Prod.ext (Prod.ext h.1.1 h.1.2) h.2
  calc H (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)
      = H (push (fun x : (υ a × (∀ i, Option (υ i))) × σ => ((some x.1.1, x.1.2), x.2))
          (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)) :=
        (H_push_injective _ hinj _).symm
    _ = H (push (fun z : (∀ i, υ i) × σ => ((some (z.1 a), mask s z.1), z.2)) P) := by
        rw [push_push]; rfl
    _ = H (push (fun z : (∀ i, υ i) × σ => (mask (insert a s) z.1, z.2)) P) := by
        apply H_push_eq_of_factor
          (fun z : (∀ i, υ i) × σ => ((some (z.1 a), mask s z.1), z.2))
          (fun z : (∀ i, υ i) × σ => (mask (insert a s) z.1, z.2))
          (fun x : (Option (υ a) × (∀ i, Option (υ i))) × σ =>
            (Function.update x.1.2 a x.1.1, x.2))
          (fun y : (∀ i, Option (υ i)) × σ =>
            ((y.1 a, fun i => if i ∈ s then y.1 i else none), y.2))
        · intro z
          refine Prod.ext ?_ rfl
          funext i
          by_cases hi : i = a
          · subst hi
            simp [mask]
          · simp [mask, Finset.mem_insert, hi]
        · intro z
          refine Prod.ext (Prod.ext ?_ ?_) rfl
          · simp [mask]
          · funext i
            by_cases hi : i ∈ s
            · simp [mask, hi, Finset.mem_insert]
            · simp [mask, hi]
        · exact hP

/-- **Conditional subadditivity for a finite family:** `H(U₁, …, Uₘ | S) ≤ ∑ⱼ H(Uⱼ | S)`.
Equivalently the conditional total correlation is nonnegative. -/
theorem condH_pi_subadd (P : (∀ i, υ i) × σ → ℝ) (hP : ∀ z, 0 ≤ P z) :
    condH P ≤ ∑ i, condH (push (fun z : (∀ i, υ i) × σ => (z.1 i, z.2)) P) := by
  have key : ∀ s : Finset ι, condH (push (fun z : (∀ i, υ i) × σ => (mask s z.1, z.2)) P)
      ≤ ∑ i ∈ s, condH (push (fun z : (∀ i, υ i) × σ => (z.1 i, z.2)) P) := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      have h0 : (fun z : (∀ i, υ i) × σ => (mask ∅ z.1, z.2))
          = fun z => ((fun _ => none : ∀ i, Option (υ i)), z.2) := by
        funext z; refine Prod.ext ?_ rfl; funext i; simp [mask]
      rw [h0, Finset.sum_empty]
      exact le_of_eq (condH_const _ P)
    | insert a s ha ih =>
      rw [Finset.sum_insert ha]
      have hQ := condH_subadd (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)
        (push_nonneg _ P hP)
      have eA : push (fun x : (υ a × (∀ i, Option (υ i))) × σ => (x.1.1, x.2))
          (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)
          = push (fun z : (∀ i, υ i) × σ => (z.1 a, z.2)) P := by rw [push_push]; rfl
      have eB : push (fun x : (υ a × (∀ i, Option (υ i))) × σ => (x.1.2, x.2))
          (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)
          = push (fun z : (∀ i, υ i) × σ => (mask s z.1, z.2)) P := by rw [push_push]; rfl
      rw [eA, eB] at hQ
      have eQ : condH (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)
          = condH (push (fun z : (∀ i, υ i) × σ => (mask (insert a s) z.1, z.2)) P) := by
        unfold condH
        have m1 : push Prod.snd (push (fun z : (∀ i, υ i) × σ => ((z.1 a, mask s z.1), z.2)) P)
            = push Prod.snd P := by rw [push_push]; rfl
        have m2 : push Prod.snd (push (fun z : (∀ i, υ i) × σ => (mask (insert a s) z.1, z.2)) P)
            = push Prod.snd P := by rw [push_push]; rfl
        rw [m1, m2, H_mask_insert a s P hP]
      linarith [hQ, eQ, ih]
  have hinj : Function.Injective (mask (univ : Finset ι) (υ := υ)) := by
    intro u v h
    funext i
    have := congrFun h i
    simpa [mask] using this
  have hu : condH (push (fun z : (∀ i, υ i) × σ => (mask univ z.1, z.2)) P) = condH P :=
    condH_relabel (mask (univ : Finset ι) (υ := υ)) hinj P
  calc condH P = condH (push (fun z : (∀ i, υ i) × σ => (mask univ z.1, z.2)) P) := hu.symm
    _ ≤ ∑ i ∈ univ, condH (push (fun z : (∀ i, υ i) × σ => (z.1 i, z.2)) P) := key univ

end Family

section Chain

variable [DecidableEq σ] {m : ℕ} {υ : Fin m → Type*} [∀ i, Fintype (υ i)]
  [∀ i, DecidableEq (υ i)]

/-- **The chain rule for a sequence of resets.** Resetting `M₁` while `M₂, …, Mₘ` and `S` are
retained, then `M₂` while `M₃, …, Mₘ` and `S` are retained, and so on, costs in total
`∑ⱼ H(Mⱼ | Mⱼ₊₁, …, Mₘ, S) = H(M₁, …, Mₘ | S)`. The memories not yet reset at step `j` are the
tuple with every index `≤ j` hidden. -/
theorem condH_chain (P : (∀ i, υ i) × σ → ℝ) (hP : ∀ z, 0 ≤ P z) :
    ∑ j : Fin m, condH (push (fun z : (∀ i, υ i) × σ =>
        (z.1 j, (mask (univ.filter (fun i => j < i)) z.1, z.2))) P) = condH P := by
  let F : ℕ → ℝ := fun k => H (push (fun z : (∀ i, υ i) × σ =>
      (mask (univ.filter (fun i : Fin m => k ≤ i.val)) z.1, z.2)) P)
  have step : ∀ j : Fin m, condH (push (fun z : (∀ i, υ i) × σ =>
        (z.1 j, (mask (univ.filter (fun i => j < i)) z.1, z.2))) P) = F j.val - F (j.val + 1) := by
    intro j
    have hfilt1 : univ.filter (fun i : Fin m => j < i)
        = univ.filter (fun i : Fin m => j.val + 1 ≤ i.val) := by
      ext i; simp only [Finset.mem_filter, Finset.mem_univ, true_and, Fin.lt_def]; omega
    have hfilt0 : insert j (univ.filter (fun i : Fin m => j < i))
        = univ.filter (fun i : Fin m => j.val ≤ i.val) := by
      ext i
      simp only [Finset.mem_insert, Finset.mem_filter, Finset.mem_univ, true_and, Fin.lt_def,
        Fin.ext_iff]
      omega
    have hassoc : Function.Injective
        (fun x : (υ j × (∀ i, Option (υ i))) × σ => (x.1.1, (x.1.2, x.2))) := by
      intro x y h
      simp only [Prod.mk.injEq] at h
      exact Prod.ext (Prod.ext h.1 h.2.1) h.2.2
    have h1 : H (push (fun z : (∀ i, υ i) × σ =>
        (z.1 j, (mask (univ.filter (fun i => j < i)) z.1, z.2))) P) = F j.val := by
      calc H (push (fun z : (∀ i, υ i) × σ =>
              (z.1 j, (mask (univ.filter (fun i => j < i)) z.1, z.2))) P)
          = H (push (fun x : (υ j × (∀ i, Option (υ i))) × σ => (x.1.1, (x.1.2, x.2)))
              (push (fun z : (∀ i, υ i) × σ =>
                ((z.1 j, mask (univ.filter (fun i => j < i)) z.1), z.2)) P)) := by
            rw [push_push]; rfl
        _ = H (push (fun z : (∀ i, υ i) × σ =>
              ((z.1 j, mask (univ.filter (fun i => j < i)) z.1), z.2)) P) :=
            H_push_injective _ hassoc _
        _ = H (push (fun z : (∀ i, υ i) × σ =>
              (mask (insert j (univ.filter (fun i => j < i))) z.1, z.2)) P) :=
            H_mask_insert j _ P hP
        _ = F j.val := by rw [hfilt0]
    have hm : push Prod.snd (push (fun z : (∀ i, υ i) × σ =>
        (z.1 j, (mask (univ.filter (fun i => j < i)) z.1, z.2))) P)
        = push (fun z : (∀ i, υ i) × σ => (mask (univ.filter (fun i => j < i)) z.1, z.2)) P := by
      rw [push_push]; rfl
    unfold condH
    rw [hm, h1, hfilt1]
  rw [Finset.sum_congr rfl (fun j _ => step j)]
  have hsum : ∑ j : Fin m, (F j.val - F (j.val + 1)) = F 0 - F m :=
    (Fin.sum_univ_eq_sum_range (fun k => F k - F (k + 1)) m).trans (Finset.sum_range_sub' _ _)
  rw [hsum]
  have hF0 : F 0 = H P := by
    have hf : univ.filter (fun i : Fin m => 0 ≤ i.val) = univ := by
      ext i; simp
    have hinj : Function.Injective
        (fun z : (∀ i, υ i) × σ => (mask (univ : Finset (Fin m)) z.1, z.2)) := by
      intro x y h
      simp only [Prod.mk.injEq] at h
      refine Prod.ext ?_ h.2
      funext i
      have := congrFun h.1 i
      simpa [mask] using this
    show H (push (fun z : (∀ i, υ i) × σ =>
      (mask (univ.filter (fun i : Fin m => 0 ≤ i.val)) z.1, z.2)) P) = H P
    rw [hf, H_push_injective _ hinj]
  have hFm : F m = H (push Prod.snd P) := by
    have hf : univ.filter (fun i : Fin m => m ≤ i.val) = ∅ := by
      ext i; simp [i.isLt]
    show H (push (fun z : (∀ i, υ i) × σ =>
      (mask (univ.filter (fun i : Fin m => m ≤ i.val)) z.1, z.2)) P) = H (push Prod.snd P)
    rw [hf]
    have h0 : (fun z : (∀ i, υ i) × σ => (mask ∅ z.1, z.2))
        = fun z => ((fun _ => none : ∀ i, Option (υ i)), z.2) := by
      funext z; refine Prod.ext ?_ rfl; funext i; simp [mask]
    rw [h0, H_push_const_fst]
  rw [hF0, hFm]
  rfl

end Chain

end ObservationTheory.FiniteEntropy
