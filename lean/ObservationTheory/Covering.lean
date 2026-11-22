/-
A one-shot covering lemma for a random codebook on finite alphabets: the second milestone of
the time-boxed attempt at Paper V's Theorem 1 achievability
(`paper/consumer-relative-landauer.tex`, `thm:main-region`; the box is recorded in
`claims/FRONTIER.md`, row G14).

Setting. A source block `Xⁿ` with i.i.d. law `iid n p`; a test channel `q x y` with output law
`r`; a block kernel `kernel n q x y = ∏ₖ q (x k) (y k)`; a codebook of `N` codewords drawn
i.i.d. from `iid n r`, with law `iid N (iid n r)`; an acceptance relation `A x y`. The encoder
succeeds on `x` if some codeword is accepted with `x`.

Contents:
* `one_sub_pow_le_exp` — `(1 − a)ᴺ ≤ exp(−a N)` for `a ≤ 1`.
* `exp_neg_mul_le` — `exp(−K t) ≤ 1 − t + exp(−K)` for `0 ≤ t ≤ 1` (convexity).
* `codebook_miss` — averaged over the codebook, the probability that no codeword is accepted
  is `∑ₓ pⁿ(x) (rⁿ(A_xᶜ))ᴺ` (independence of the codewords).
* `covering_bound` — if every accepted pair has `qⁿ(y | x) ≤ L rⁿ(y)` (`L > 0`), the averaged
  miss probability is at most `P_joint(not accepted) + exp(−N / L)`.
* `exists_le_of_average` — derandomization: if an average under a law of mass one is at most
  `B`, some point of the law's support attains at most `B`.
-/
import ObservationTheory.BlockLLN

open Real Finset

namespace ObservationTheory.FiniteEntropy

/-- `(1 − a)ᴺ ≤ exp(−a N)` for `a ≤ 1`. -/
lemma one_sub_pow_le_exp (a : ℝ) (ha1 : a ≤ 1) (N : ℕ) :
    (1 - a) ^ N ≤ exp (-(a * N)) := by
  have h1 : (1 - a) ^ N ≤ (exp (-a)) ^ N :=
    pow_le_pow_left₀ (by linarith) (by linarith [Real.add_one_le_exp (-a)]) N
  calc (1 - a) ^ N ≤ (exp (-a)) ^ N := h1
    _ = exp (-(a * N)) := by
        rw [← Real.exp_nat_mul]
        ring_nf

/-- `exp(−K t) ≤ 1 − t + exp(−K)` for `0 ≤ t ≤ 1` (any real `K`), by convexity of `exp`. -/
lemma exp_neg_mul_le (K t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    exp (-(K * t)) ≤ 1 - t + exp (-K) := by
  have hc := convexOn_exp.2 (Set.mem_univ (0 : ℝ)) (Set.mem_univ (-K)) (by linarith : 0 ≤ 1 - t)
    ht0 (by ring)
  simp only [smul_eq_mul, mul_zero, zero_add, Real.exp_zero, mul_one] at hc
  have he : 0 ≤ exp (-K) := (Real.exp_pos _).le
  have hx : t * -K = -(K * t) := by ring
  rw [hx] at hc
  nlinarith [hc, he]

variable {α γ : Type*} [Fintype α] [Fintype γ]

/-- The block kernel `qⁿ(y | x) = ∏ₖ q(xₖ, yₖ)`. -/
noncomputable def kernel (n : ℕ) (q : α → γ → ℝ) (x : Fin n → α) (y : Fin n → γ) : ℝ :=
  ∏ k, q (x k) (y k)

omit [Fintype α] [Fintype γ] in
lemma kernel_nonneg (n : ℕ) (q : α → γ → ℝ) (hq : ∀ a b, 0 ≤ q a b) (x : Fin n → α)
    (y : Fin n → γ) : 0 ≤ kernel n q x y :=
  Finset.prod_nonneg (fun _ _ => hq _ _)

omit [Fintype α] in
lemma sum_kernel (n : ℕ) (q : α → γ → ℝ) (hq1 : ∀ a, ∑ b, q a b = 1) (x : Fin n → α) :
    ∑ y, kernel n q x y = 1 := by
  unfold kernel
  rw [← Fintype.prod_sum (fun k b => q (x k) b)]
  exact Finset.prod_eq_one (fun k _ => hq1 (x k))

/-- **Independence of the codewords.** Averaged over a codebook of `N` i.i.d. codewords with
law `R`, the probability that no codeword is accepted with `x` is `(R(A_xᶜ))ᴺ`. -/
lemma codebook_miss (N : ℕ) {β : Type*} [Fintype β] (R : β → ℝ) (B : β → Prop)
    [DecidablePred B] :
    ∑ c, iid N R c * (if ∀ k, ¬ B (c k) then (1 : ℝ) else 0)
      = (∑ y, R y * (if ¬ B y then (1 : ℝ) else 0)) ^ N := by
  have h : ∀ c : Fin N → β, (if ∀ k, ¬ B (c k) then (1 : ℝ) else 0)
      = ∏ k, (if ¬ B (c k) then (1 : ℝ) else 0) := by
    intro c
    rw [Finset.prod_boole]
    simp
  simp_rw [h]
  rw [sum_iid_mul_prod N R (fun _ y => if ¬ B y then (1 : ℝ) else 0), Finset.prod_const,
    Finset.card_univ, Fintype.card_fin]

/-- **The one-shot covering bound.** Let the codebook be `N` codewords i.i.d. from `iid n r`
(`r` of total mass one), and suppose every accepted pair has `qⁿ(y | x) ≤ L rⁿ(y)` with
`L > 0`. Averaged over the codebook, the probability (under `iid n p`) that no codeword is
accepted with the source block is at most the joint probability of not accepting plus
`exp(−N / L)`. -/
theorem covering_bound (n N : ℕ) (p : α → ℝ) (hp : ∀ a, 0 ≤ p a) (hp1 : ∑ a, p a = 1)
    (q : α → γ → ℝ) (hq : ∀ a b, 0 ≤ q a b) (hq1 : ∀ a, ∑ b, q a b = 1)
    (r : γ → ℝ) (hr : ∀ b, 0 ≤ r b) (hr1 : ∑ b, r b = 1)
    (A : (Fin n → α) → (Fin n → γ) → Prop) [∀ x, DecidablePred (A x)] (L : ℝ) (hL : 0 < L)
    (hA : ∀ x y, A x y → kernel n q x y ≤ L * iid n r y) :
    ∑ c, iid N (iid n r) c * ∑ x, iid n p x * (if ∀ k, ¬ A x (c k) then (1 : ℝ) else 0)
      ≤ (∑ x, iid n p x * ∑ y, kernel n q x y * (if ¬ A x y then (1 : ℝ) else 0))
        + exp (-(N / L)) := by
  -- swap the codebook and source sums, then use independence of the codewords
  have hswap : ∑ c, iid N (iid n r) c * ∑ x, iid n p x * (if ∀ k, ¬ A x (c k) then (1 : ℝ) else 0)
      = ∑ x, iid n p x * (∑ y, iid n r y * (if ¬ A x y then (1 : ℝ) else 0)) ^ N := by
    simp_rw [Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro x _
    rw [← codebook_miss N (iid n r) (A x), Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro c _
    ring
  rw [hswap]
  -- per source block: the miss probability against the joint law
  have hterm : ∀ x : Fin n → α,
      (∑ y, iid n r y * (if ¬ A x y then (1 : ℝ) else 0)) ^ N
        ≤ (∑ y, kernel n q x y * (if ¬ A x y then (1 : ℝ) else 0)) + exp (-(N / L)) := by
    intro x
    set Q := ∑ y, kernel n q x y * (if A x y then (1 : ℝ) else 0) with hQ
    have hsplit : ∀ (w : (Fin n → γ) → ℝ), ∑ y, w y * (if ¬ A x y then (1 : ℝ) else 0)
        = ∑ y, w y - ∑ y, w y * (if A x y then (1 : ℝ) else 0) := by
      intro w
      rw [eq_sub_iff_add_eq, ← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro y _
      by_cases h : A x y <;> simp [h]
    have hQ0 : 0 ≤ Q := Finset.sum_nonneg (fun y _ => mul_nonneg (kernel_nonneg n q hq x y)
      (by split_ifs <;> norm_num))
    have hQ1 : Q ≤ 1 := by
      have := hsplit (kernel n q x)
      rw [sum_kernel n q hq1 x] at this
      have hnn : 0 ≤ ∑ y, kernel n q x y * (if ¬ A x y then (1 : ℝ) else 0) :=
        Finset.sum_nonneg (fun y _ => mul_nonneg (kernel_nonneg n q hq x y)
          (by split_ifs <;> norm_num))
      linarith
    -- the output law gives the accepted set at least `Q / L`
    have hacc : Q / L ≤ ∑ y, iid n r y * (if A x y then (1 : ℝ) else 0) := by
      rw [hQ, Finset.sum_div]
      apply Finset.sum_le_sum
      intro y _
      by_cases h : A x y
      · simp only [h, if_true, mul_one]
        rw [div_le_iff₀ hL]
        linarith [hA x y h]
      · simp [h]
    have hmiss : ∑ y, iid n r y * (if ¬ A x y then (1 : ℝ) else 0) ≤ 1 - Q / L := by
      rw [hsplit (iid n r), sum_iid, hr1, one_pow]
      linarith
    have hmiss0 : 0 ≤ ∑ y, iid n r y * (if ¬ A x y then (1 : ℝ) else 0) :=
      Finset.sum_nonneg (fun y _ => mul_nonneg (iid_nonneg n r hr y) (by split_ifs <;> norm_num))
    have hQL1 : Q / L ≤ 1 := by
      have := hacc
      have h1 : ∑ y, iid n r y * (if A x y then (1 : ℝ) else 0) ≤ 1 := by
        have h2 := hsplit (iid n r)
        rw [sum_iid, hr1, one_pow] at h2
        linarith
      linarith
    have hQL0 : 0 ≤ Q / L := div_nonneg hQ0 hL.le
    calc (∑ y, iid n r y * (if ¬ A x y then (1 : ℝ) else 0)) ^ N
        ≤ (1 - Q / L) ^ N := pow_le_pow_left₀ hmiss0 hmiss N
      _ ≤ exp (-(Q / L * N)) := one_sub_pow_le_exp _ hQL1 N
      _ = exp (-((N / L) * Q)) := by ring_nf
      _ ≤ 1 - Q + exp (-(N / L)) :=
          exp_neg_mul_le _ _ hQ0 hQ1
      _ = (∑ y, kernel n q x y * (if ¬ A x y then (1 : ℝ) else 0)) + exp (-(N / L)) := by
          rw [hsplit (kernel n q x), sum_kernel n q hq1 x]
  calc ∑ x, iid n p x * (∑ y, iid n r y * (if ¬ A x y then (1 : ℝ) else 0)) ^ N
      ≤ ∑ x, iid n p x * ((∑ y, kernel n q x y * (if ¬ A x y then (1 : ℝ) else 0))
          + exp (-(N / L))) :=
        Finset.sum_le_sum (fun x _ => mul_le_mul_of_nonneg_left (hterm x) (iid_nonneg n p hp x))
    _ = (∑ x, iid n p x * ∑ y, kernel n q x y * (if ¬ A x y then (1 : ℝ) else 0))
          + exp (-(N / L)) := by
        simp_rw [mul_add]
        rw [Finset.sum_add_distrib, ← Finset.sum_mul, sum_iid, hp1, one_pow, one_mul]

/-- **Derandomization.** If the average of `F` under a nonnegative law `P` of total mass one is
at most `B`, then `F c ≤ B` at some `c` with `P c > 0`. -/
lemma exists_le_of_average {β : Type*} [Fintype β] (P F : β → ℝ) (hP : ∀ c, 0 ≤ P c)
    (hP1 : ∑ c, P c = 1) (B : ℝ) (h : ∑ c, P c * F c ≤ B) : ∃ c, 0 < P c ∧ F c ≤ B := by
  by_contra hne
  push Not at hne
  have hlt : ∑ c, P c * B < ∑ c, P c * F c := by
    obtain ⟨c0, hc0⟩ : ∃ c, 0 < P c := by
      by_contra hall
      push Not at hall
      have : ∑ c, P c ≤ 0 := Finset.sum_nonpos (fun c _ => hall c)
      linarith
    apply Finset.sum_lt_sum
    · intro c _
      rcases (hP c).lt_or_eq with hpos | hzero
      · exact (mul_lt_mul_of_pos_left (hne c hpos) hpos).le
      · rw [← hzero]; simp
    · exact ⟨c0, Finset.mem_univ _, mul_lt_mul_of_pos_left (hne c0 hc0) hc0⟩
  rw [← Finset.sum_mul, hP1, one_mul] at hlt
  linarith

end ObservationTheory.FiniteEntropy
