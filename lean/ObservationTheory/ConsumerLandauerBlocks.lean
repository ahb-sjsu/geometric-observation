/-
Paper V (`paper/consumer-relative-landauer.tex`) at block level, on finite alphabets: the
statements that need the source block `(Xⁿ, Sⁿ)` of `n` i.i.d. pairs, many consumers, or a
Markov record. Built on `ObservationTheory.IidBlocks`; the single-letter identities are in
`ObservationTheory.ConsumerLandauerIdentities`.

Conventions, as there: entropies in nats (the paper uses bits; the statements are the same up
to the factor `ln 2`); "reset content" is the conditional entropy of the memory given the
retained side information, and reading `k_B T ln 2` times it as ideal reset work is Landauer's
bound, which the paper imports and which is not formalized. Codes are deterministic: an
encoder `f : 𝒳ⁿ → ℳ` and a decoder `g : ℳ → 𝒳̂ⁿ` (the paper allows randomized encoders in its
converse; they are not covered here). `block n p` is the law of `(Xⁿ, Sⁿ)`.

What is formalized:
* Theorem 2 (`thm:materialization`), block form: `materialization_block`,
  `H(Xⁿ, f(Xⁿ) | Sⁿ) = n H(X | S)` for any description `f`. (The sequential-reset remark in
  its proof, `H(A | M, Sⁿ) + H(M | Sⁿ) = H(A, M | Sⁿ)`, is the chain rule: `condH_chain`, or
  `cor3_coordinated_chain` with the pair `(A, M)`.)
* The exact-tax identity behind (`eq:exact-tax`): `exact_tax_identity`,
  `H(X | S) − H(U | S) = H(X | U, S)` for `U = u(X)`. (That `L_𝒞(0 | S) = H(U | S)` is
  Corollary 2, not formalized here.)
* Corollary 3 (`cor:tc`) for `m` consumers with outputs `Uⱼ = uⱼ(X)`, at every blocklength:
  - `exact_lower`, `cor3m_joint_lower`: a memory from which the consumers decode their output
    blocks exactly has content at least `n H(U₁, …, Uₘ | S)`;
  - `cor3m_coordinated`: separate memories reset in sequence, each against `Sⁿ` and the
    memories not yet reset, cost exactly their joint content, hence at least the same bound;
  - `cor3m_independent`: reset independently, at least `n ∑ⱼ H(Uⱼ | S)`;
  - `cor3m_tc_nonneg`: `H(U₁, …, Uₘ | S) ≤ ∑ⱼ H(Uⱼ | S)`;
  - `cor3m_attained`, `cor3m_coordinated_attained`: storing `Mⱼ = Uⱼⁿ` meets the
    independent bound and the joint (and coordinated) bound with equality.

  Exact decoding (`hex`) is required at every source sequence, including sequences of
  probability zero; the almost-sure reading of "recovers exactly" is not formalized. The
  coordinated reset is formalized in the order `M₁, …, Mₘ` (the paper's); other orders are a
  reindexing, not stated.
* Proposition 6 (`prop:stale`). `pathLaw K q₀ T` is the law of `(M, X₀, …, X_T)` under the
  paper's hypothesis: `(M, X₀)` has law `q₀`, `M` is conditionally independent of the future
  given `X₀`, and the chain moves by one time-homogeneous kernel `K`, so the law is
  `q₀(m, x₀) ∏ₛ K(xₛ, xₛ₊₁)`. The hypothesis enters as this factorization, the standard
  finite-state definition; its equivalence with the conditional-independence phrasing (`K`
  arbitrary on unreachable states) is not proved. A stationary chain is time-homogeneous on
  its support, so the paper's case is an instance. `pathLaw_marginal`: the law of `(M, X_t)`
  is `(ageStep K)^[t] q₀`. `stale_step`: under `M − X_t − X_{t+1}`,
  `H(M | X_t) ≤ H(M | X_{t+1})` (one step, any kernel). `stale_monotone`: the same along the
  iterates of one kernel. `stale_monotone_path`: `L_t = H(M | X_t)` is nondecreasing in
  `t ≤ T`. Stationarity is not used; time homogeneity is (an inhomogeneous chain is not
  formalized; `stale_step`, which takes any kernel, is its one-step form). The identity
  `H(M | X_t) = H(M) − I(M; X_t)` is the definition of mutual information and is not
  restated.
* Theorem 1 (`thm:main-region`), the per-code converse chain (`eq:work-conv`):
  `work_converse` is `H(M | Sⁿ) ≥ ∑ᵢ I(Xᵢ; X̂ᵢ | Sᵢ)`, its outer ends (for deterministic codes
  the intermediate links `I(Xⁿ; M | Sⁿ)` and `I(Xⁿ; X̂ⁿ | Sⁿ)` are absorbed and not stated).
  `content_le_log_card` is `H(M | Sⁿ) ≤ log |ℳ|` (`L_n ≤ R_n`), here for finite source
  alphabets (the paper also uses `L_n ≤ R_n` in its Gaussian section, outside this scope);
  with a one-point side-information type it is the first link of (`eq:rate-conv`).
  Instantiating the side-information alphabet with a one-point type gives the outer ends of
  the rate chain (`eq:rate-conv`), `log |ℳ| ≥ H(M) ≥ ∑ᵢ I(Xᵢ; X̂ᵢ)`, in this encoding; that
  `condH` and `condMI` then reduce to `H` and `I` is not stated as a lemma. Not formalized: the distortion coordinate (`d_𝒞`, `D_n`,
  `𝒯_𝒞(D)`) and the region `𝒰(D)` itself; the per-letter Markov property `X̂ᵢ − Xᵢ − Sᵢ`; the
  mixture channel; Lemma 1 (convexity); the limit in `D`; and achievability.
-/
import ObservationTheory.IidBlocks

open Real Finset

namespace ObservationTheory.ConsumerLandauer

open ObservationTheory.FiniteEntropy

variable {α σ : Type*} [Fintype α] [Fintype σ] [DecidableEq α] [DecidableEq σ]

/-! ### Theorem 2 and the exact tax -/

/-- **Theorem 2 (materialization), block form.** A register holding the full block `A = Xⁿ`
beside a description `M = f(Xⁿ)` has joint reset content `H(A, M | Sⁿ) = n H(X | S)`, whatever
the description. -/
theorem materialization_block {μ : Type*} [Fintype μ] [DecidableEq μ] (n : ℕ)
    (f : (Fin n → α) → μ) (p : α × σ → ℝ) (hp1 : ∑ z, p z = 1) :
    condH (push (fun z : (Fin n → α) × (Fin n → σ) => ((z.1, f z.1), z.2)) (block n p))
      = n * condH p := by
  rw [condH_materialize f (block n p), condH_block n p hp1]

/-- **The exact-tax identity.** For a consumer output `U = u(X)`,
`H(X | S) − H(U | S) = H(X | U, S)`. -/
theorem exact_tax_identity {β : Type*} [Fintype β] [DecidableEq β] (u : α → β)
    (p : α × σ → ℝ) :
    condH p - condH (push (Prod.map u id) p)
      = condH (push (fun z : α × σ => (z.1, (u z.1, z.2))) p) := by
  have hinj : Function.Injective (fun z : α × σ => (z.1, (u z.1, z.2))) := by
    intro x y h
    simp only [Prod.mk.injEq] at h
    exact Prod.ext h.1 h.2.2
  have hs : push Prod.snd (push (Prod.map u id) p) = push Prod.snd p := by
    rw [push_push]; rfl
  have hs2 : push Prod.snd (push (fun z : α × σ => (z.1, (u z.1, z.2))) p)
      = push (Prod.map u id) p := by
    rw [push_push]; rfl
  unfold condH
  rw [hs, hs2, H_push_injective _ hinj]
  ring

/-! ### Corollary 3, `m` consumers, every blocklength -/

/-- **Exact decoding forces content.** If a decoder recovers `v(X₁), …, v(Xₙ)` exactly from
`M = F(Xⁿ)` (at every source sequence), then `H(M | Sⁿ) ≥ n H(v X | S)`. -/
theorem exact_lower {β μ : Type*} [Fintype β] [DecidableEq β] [Fintype μ] [DecidableEq μ]
    (n : ℕ) (v : α → β) (F : (Fin n → α) → μ) (g : μ → (Fin n → β))
    (hex : ∀ x, g (F x) = fun i => v (x i)) (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z)
    (hp1 : ∑ z, p z = 1) :
    n * condH (push (Prod.map v id) p) ≤ condH (push (Prod.map F id) (block n p)) := by
  have h1 := condH_push_le g (push (Prod.map F id) (block n p))
    (push_nonneg _ _ (block_nonneg n p hp))
  rw [push_push] at h1
  have hcomp : (Prod.map g id ∘ Prod.map F id : (Fin n → α) × (Fin n → σ) → (Fin n → β) × (Fin n → σ))
      = Prod.map (fun x : Fin n → α => fun i => v (x i)) id := by
    funext z
    exact Prod.ext (hex z.1) rfl
  rw [hcomp, block_map, condH_block n (push (Prod.map v id) p) (by rw [sum_push, hp1])] at h1
  exact h1

section Corollary3m

variable {m : ℕ} {υ : Fin m → Type*} [∀ j, Fintype (υ j)] [∀ j, DecidableEq (υ j)]

/-- **Corollary 3, joint memory.** If each consumer `j` decodes `Uⱼⁿ = (uⱼ(X₁), …, uⱼ(Xₙ))`
exactly (at every source sequence) from one memory `M = F(Xⁿ)`, then
`H(M | Sⁿ) ≥ n H(U₁, …, Uₘ | S)`. -/
theorem cor3m_joint_lower {μ : Type*} [Fintype μ] [DecidableEq μ] (n : ℕ) (u : ∀ j, α → υ j)
    (F : (Fin n → α) → μ) (g : ∀ j, μ → (Fin n → υ j))
    (hex : ∀ x j, g j (F x) = fun i => u j (x i))
    (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z) (hp1 : ∑ z, p z = 1) :
    n * condH (push (Prod.map (fun a j => u j a) id) p)
      ≤ condH (push (Prod.map F id) (block n p)) :=
  exact_lower n (fun a j => u j a) F (fun mm i j => g j mm i)
    (fun x => by
      funext i j
      show g j (F x) i = u j (x i)
      rw [hex x j]) p hp hp1

/-- **Corollary 3, coordinated reset.** Separate memories `Mⱼ = Fⱼ(Xⁿ)`, consumer `j` decoding
`Uⱼⁿ` exactly (at every source sequence) from `Mⱼ` alone, reset in sequence, each against `Sⁿ` and the memories not yet
reset: the total cost is the joint content `H(M₁, …, Mₘ | Sⁿ)`, which is at least
`n H(U₁, …, Uₘ | S)`. -/
theorem cor3m_coordinated {μ : Fin m → Type*} [∀ j, Fintype (μ j)] [∀ j, DecidableEq (μ j)]
    (n : ℕ) (u : ∀ j, α → υ j) (F : ∀ j, (Fin n → α) → μ j) (g : ∀ j, μ j → (Fin n → υ j))
    (hex : ∀ j x, g j (F j x) = fun i => u j (x i))
    (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z) (hp1 : ∑ z, p z = 1) :
    ∑ j : Fin m, condH (push (fun z : (∀ j, μ j) × (Fin n → σ) =>
        (z.1 j, (mask (univ.filter (fun i => j < i)) z.1, z.2)))
        (push (Prod.map (fun x j => F j x) id) (block n p)))
      = condH (push (Prod.map (fun x j => F j x) id) (block n p))
    ∧ n * condH (push (Prod.map (fun a j => u j a) id) p)
      ≤ condH (push (Prod.map (fun x j => F j x) id) (block n p)) :=
  ⟨condH_chain _ (push_nonneg _ _ (block_nonneg n p hp)),
    cor3m_joint_lower n u (fun x j => F j x) (fun j mm => g j (mm j)) (fun x j => hex j x)
      p hp hp1⟩

/-- **Corollary 3, independent reset.** If consumer `j` decodes `Uⱼⁿ` exactly (at every source
sequence) from `Mⱼ` alone, and each memory is reset seeing `Sⁿ` only, the summed content is at
least `n ∑ⱼ H(Uⱼ | S)`. -/
theorem cor3m_independent {μ : Fin m → Type*} [∀ j, Fintype (μ j)] [∀ j, DecidableEq (μ j)]
    (n : ℕ) (u : ∀ j, α → υ j) (F : ∀ j, (Fin n → α) → μ j) (g : ∀ j, μ j → (Fin n → υ j))
    (hex : ∀ j x, g j (F j x) = fun i => u j (x i))
    (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z) (hp1 : ∑ z, p z = 1) :
    n * ∑ j, condH (push (Prod.map (u j) id) p)
      ≤ ∑ j, condH (push (Prod.map (F j) id) (block n p)) := by
  rw [Finset.mul_sum]
  exact Finset.sum_le_sum (fun j _ => exact_lower n (u j) (F j) (g j) (hex j) p hp hp1)

omit [DecidableEq α] in
/-- **Corollary 3, the gap.** The conditional total correlation is nonnegative:
`H(U₁, …, Uₘ | S) ≤ ∑ⱼ H(Uⱼ | S)`. -/
theorem cor3m_tc_nonneg (u : ∀ j, α → υ j) (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z) :
    condH (push (Prod.map (fun a j => u j a) id) p) ≤ ∑ j, condH (push (Prod.map (u j) id) p) := by
  have h := condH_pi_subadd (push (Prod.map (fun a j => u j a) id) p) (push_nonneg _ _ hp)
  have e : ∀ j, push (fun z : (∀ j, υ j) × σ => (z.1 j, z.2))
      (push (Prod.map (fun a j => u j a) id) p) = push (Prod.map (u j) id) p := fun j => by
    rw [push_push]; rfl
  simp only [e] at h
  exact h

/-- **Corollary 3, attainment.** The code storing `Mⱼ = Uⱼⁿ` has `H(Mⱼ | Sⁿ) = n H(Uⱼ | S)` for
each `j` and joint content `H(M₁, …, Mₘ | Sⁿ) = n H(U₁, …, Uₘ | S)`, at every blocklength. -/
theorem cor3m_attained (n : ℕ) (u : ∀ j, α → υ j) (p : α × σ → ℝ) (hp1 : ∑ z, p z = 1) :
    (∀ j, condH (push (Prod.map (fun x : Fin n → α => fun i => u j (x i)) id) (block n p))
        = n * condH (push (Prod.map (u j) id) p))
    ∧ condH (push (Prod.map (fun x : Fin n → α => fun j i => u j (x i)) id) (block n p))
        = n * condH (push (Prod.map (fun a j => u j a) id) p) := by
  constructor
  · intro j
    rw [block_map, condH_block n (push (Prod.map (u j) id) p) (by rw [sum_push, hp1])]
  · have hswap : Function.Injective (fun w : Fin n → (∀ j, υ j) => fun j i => w i j) := by
      intro w w' h
      funext i j
      exact congrFun (congrFun h j) i
    have e : push (Prod.map (fun x : Fin n → α => fun j i => u j (x i)) id) (block n p)
        = push (Prod.map (fun w : Fin n → (∀ j, υ j) => fun j i => w i j) id)
            (push (Prod.map (fun x : Fin n → α => fun i => (fun a j => u j a) (x i)) id)
              (block n p)) := by
      rw [push_push]; rfl
    rw [e, condH_relabel _ hswap, block_map n (fun a j => u j a) p,
      condH_block n (push (Prod.map (fun a j => u j a) id) p) (by rw [sum_push, hp1])]

/-- **Corollary 3, coordinated attainment.** For the code storing `Mⱼ = Uⱼⁿ`, the coordinated
reset in the order `M₁, …, Mₘ` costs exactly `n H(U₁, …, Uₘ | S)`. -/
theorem cor3m_coordinated_attained (n : ℕ) (u : ∀ j, α → υ j) (p : α × σ → ℝ)
    (hp : ∀ z, 0 ≤ p z) (hp1 : ∑ z, p z = 1) :
    ∑ j : Fin m, condH (push (fun z : (∀ j, Fin n → υ j) × (Fin n → σ) =>
        (z.1 j, (mask (univ.filter (fun i => j < i)) z.1, z.2)))
        (push (Prod.map (fun x : Fin n → α => fun j i => u j (x i)) id) (block n p)))
      = n * condH (push (Prod.map (fun a j => u j a) id) p) := by
  rw [condH_chain _ (push_nonneg _ _ (block_nonneg n p hp))]
  exact (cor3m_attained n u p hp1).2

end Corollary3m

/-! ### Proposition 6 (staleness) -/

section Staleness

variable {μ ξ : Type*} [Fintype μ] [Fintype ξ] [DecidableEq μ] [DecidableEq ξ]

/-- One step of the chain for the record: if `M − X_t − X_{t+1}` and the step has kernel
`K x y = P(X_{t+1} = y | X_t = x)`, the law of `(M, X_{t+1})` is `ageStep K` of the law `q` of
`(M, X_t)`. -/
noncomputable def ageStep (K : ξ → ξ → ℝ) (q : μ × ξ → ℝ) : μ × ξ → ℝ :=
  fun w => ∑ x, q (w.1, x) * K x w.2

/-- The law of `((M, X_t), X_{t+1})` under the same hypothesis. -/
noncomputable def chainJoint (K : ξ → ξ → ℝ) (q : μ × ξ → ℝ) : (μ × ξ) × ξ → ℝ :=
  fun w => q w.1 * K w.1.2 w.2

omit [Fintype μ] [DecidableEq μ] [DecidableEq ξ] in
/-- Entropy of a law that factors through a kernel with rows of mass one. -/
lemma H_kernel {β : Type*} [Fintype β] (c : β → ℝ) (k : β → ξ → ℝ)
    (hk1 : ∀ b, ∑ y, k b y = 1) :
    H (fun w : β × ξ => c w.1 * k w.1 w.2) = H c + ∑ b, c b * ∑ y, negMulLog (k b y) := by
  unfold H
  rw [Fintype.sum_prod_type, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro b _
  simp only [Real.negMulLog_mul, Finset.sum_add_distrib, ← Finset.sum_mul, hk1 b, one_mul,
    Finset.mul_sum]

/-- **Proposition 6, one step.** Under `M − X_t − X_{t+1}`, the content of the record given the
newer state is at least its content given the older one: `H(M | X_t) ≤ H(M | X_{t+1})`. -/
theorem stale_step (K : ξ → ξ → ℝ) (hK : ∀ x y, 0 ≤ K x y) (hK1 : ∀ x, ∑ y, K x y = 1)
    (q : μ × ξ → ℝ) (hq : ∀ w, 0 ≤ q w) : condH q ≤ condH (ageStep K q) := by
  have hr0 : ∀ w, 0 ≤ chainJoint K q w := fun w => mul_nonneg (hq _) (hK _ _)
  have hsub := condH_subadd (chainJoint K q) hr0
  have hA : push (fun w : (μ × ξ) × ξ => (w.1.1, w.2)) (chainJoint K q) = ageStep K q := by
    funext w
    obtain ⟨mm, y⟩ := w
    rw [push_AS_apply]
    rfl
  have hB : push (fun w : (μ × ξ) × ξ => (w.1.2, w.2)) (chainJoint K q)
      = fun w : ξ × ξ => push Prod.snd q w.1 * K w.1 w.2 := by
    funext w
    obtain ⟨x, y⟩ := w
    show _ = push Prod.snd q x * K x y
    rw [push_BS_apply, push_snd_apply, Finset.sum_mul]
    rfl
  have hmB : push Prod.snd (push (fun w : (μ × ξ) × ξ => (w.1.2, w.2)) (chainJoint K q))
      = push Prod.snd (chainJoint K q) := by
    rw [push_push]; rfl
  have hHr : H (chainJoint K q) = H q + ∑ z : μ × ξ, q z * ∑ y, negMulLog (K z.2 y) :=
    H_kernel q (fun z y => K z.2 y) (fun z => hK1 z.2)
  have hHB : H (fun w : ξ × ξ => push Prod.snd q w.1 * K w.1 w.2)
      = H (push Prod.snd q) + ∑ x, push Prod.snd q x * ∑ y, negMulLog (K x y) :=
    H_kernel (push Prod.snd q) K hK1
  have hT : ∑ z : μ × ξ, q z * ∑ y, negMulLog (K z.2 y)
      = ∑ x, push Prod.snd q x * ∑ y, negMulLog (K x y) := by
    rw [Fintype.sum_prod_type, Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro x _
    simp only [push_snd_apply, Finset.sum_mul]
  rw [hA] at hsub
  unfold condH at hsub ⊢
  rw [hmB, hB, hHB, hHr, hT] at hsub
  linarith

/-- **Proposition 6, iterated.** With one time-homogeneous kernel `K` and any law `q₀` of
`(M, X₀)`, the content `H(M | X_t)` of the age-`t` law `(ageStep K)^[t] q₀` is nondecreasing in
`t`. `pathLaw_marginal` shows that this iterate is the law of `(M, X_t)` under the paper's
hypothesis. -/
theorem stale_monotone (K : ξ → ξ → ℝ) (hK : ∀ x y, 0 ≤ K x y) (hK1 : ∀ x, ∑ y, K x y = 1)
    (q₀ : μ × ξ → ℝ) (hq₀ : ∀ w, 0 ≤ q₀ w) :
    Monotone (fun t : ℕ => condH ((ageStep K)^[t] q₀)) := by
  have hnn : ∀ t (w : μ × ξ), 0 ≤ (ageStep K)^[t] q₀ w := by
    intro t
    induction t with
    | zero => exact hq₀
    | succ t ih =>
      intro w
      rw [Function.iterate_succ_apply']
      unfold ageStep
      exact Finset.sum_nonneg (fun x _ => mul_nonneg (ih _) (hK _ _))
  apply monotone_nat_of_le_succ
  intro t
  show condH ((ageStep K)^[t] q₀) ≤ condH ((ageStep K)^[t + 1] q₀)
  rw [Function.iterate_succ_apply']
  exact stale_step K hK hK1 _ (hnn t)

/-- The law of `(M, X₀, X₁, …, X_T)` under Proposition 6's hypothesis: `(M, X₀)` has law `q₀`,
`M` is conditionally independent of `(X₁, …, X_T)` given `X₀`, and the chain is a
time-homogeneous Markov chain with one-step kernel `K`, so the law is
`q₀(m, x₀) ∏ₛ K(xₛ, xₛ₊₁)` (the hypothesis enters as this factorization). -/
noncomputable def pathLaw (K : ξ → ξ → ℝ) (q₀ : μ × ξ → ℝ) (T : ℕ) :
    μ × (Fin (T + 1) → ξ) → ℝ :=
  fun w => q₀ (w.1, w.2 0) * ∏ s : Fin T, K (w.2 s.castSucc) (w.2 s.succ)

omit [Fintype μ] [DecidableEq μ] [DecidableEq ξ] in
/-- The future of the chain has total mass one, from any state. -/
lemma future_mass (K : ξ → ξ → ℝ) (hK1 : ∀ x, ∑ y, K x y = 1) :
    ∀ (T : ℕ) (b : ξ), ∑ y : Fin T → ξ, ∏ s : Fin T,
      K ((Fin.cons b y : Fin (T + 1) → ξ) s.castSucc) ((Fin.cons b y : Fin (T + 1) → ξ) s.succ)
      = 1 := by
  intro T
  induction T with
  | zero => intro b; simp
  | succ T ih =>
    intro b
    calc ∑ y : Fin (T + 1) → ξ, ∏ s : Fin (T + 1),
          K ((Fin.cons b y : Fin (T + 2) → ξ) s.castSucc) ((Fin.cons b y : Fin (T + 2) → ξ) s.succ)
        = ∑ y : Fin (T + 1) → ξ, K b (y 0) * ∏ s : Fin T,
            K ((Fin.cons (y 0) (Fin.tail y) : Fin (T + 1) → ξ) s.castSucc)
              ((Fin.cons (y 0) (Fin.tail y) : Fin (T + 1) → ξ) s.succ) := by
          apply Finset.sum_congr rfl
          intro y _
          rw [Fin.prod_univ_succ, Fin.cons_self_tail]
          simp only [Fin.castSucc_zero, Fin.cons_zero, Fin.succ_zero_eq_one, Fin.cons_one,
            ← Fin.succ_castSucc, Fin.cons_succ]
      _ = ∑ z : ξ × (Fin T → ξ), K b z.1 * ∏ s : Fin T,
            K ((Fin.cons z.1 z.2 : Fin (T + 1) → ξ) s.castSucc)
              ((Fin.cons z.1 z.2 : Fin (T + 1) → ξ) s.succ) :=
          Fintype.sum_equiv (Fin.consEquiv (fun _ : Fin (T + 1) => ξ)).symm _ _ (fun y => rfl)
      _ = ∑ c, K b c * ∑ y' : Fin T → ξ, ∏ s : Fin T,
            K ((Fin.cons c y' : Fin (T + 1) → ξ) s.castSucc)
              ((Fin.cons c y' : Fin (T + 1) → ξ) s.succ) := by
          rw [Fintype.sum_prod_type]
          simp only [Finset.mul_sum]
      _ = 1 := by simp only [ih, mul_one, hK1]

/-- At age zero the path law gives back the law of `(M, X₀)`. -/
lemma pathLaw_zero (K : ξ → ξ → ℝ) (hK1 : ∀ x, ∑ y, K x y = 1) (q₀ : μ × ξ → ℝ) (T : ℕ) :
    push (fun w : μ × (Fin (T + 1) → ξ) => (w.1, w.2 0)) (pathLaw K q₀ T) = q₀ := by
  funext w
  obtain ⟨m, b⟩ := w
  unfold push
  rw [Finset.sum_filter, Fintype.sum_prod_type,
    Finset.sum_eq_single m (fun m' _ hm' => Finset.sum_eq_zero (fun x _ => by simp [hm']))
      (fun h => absurd (Finset.mem_univ m) h)]
  calc ∑ x : Fin (T + 1) → ξ, (if (m, x 0) = (m, b) then pathLaw K q₀ T (m, x) else 0)
      = ∑ z : ξ × (Fin T → ξ), (if z.1 = b then q₀ (m, z.1) * ∏ s : Fin T,
            K ((Fin.cons z.1 z.2 : Fin (T + 1) → ξ) s.castSucc)
              ((Fin.cons z.1 z.2 : Fin (T + 1) → ξ) s.succ) else 0) := by
        refine Fintype.sum_equiv (Fin.consEquiv (fun _ : Fin (T + 1) => ξ)).symm _ _
          (fun x => ?_)
        show _ = (if x 0 = b then q₀ (m, x 0) * ∏ s : Fin T,
            K ((Fin.cons (x 0) (Fin.tail x) : Fin (T + 1) → ξ) s.castSucc)
              ((Fin.cons (x 0) (Fin.tail x) : Fin (T + 1) → ξ) s.succ) else 0)
        rw [Fin.cons_self_tail]
        unfold pathLaw
        simp only [Prod.mk.injEq, true_and]
    _ = q₀ (m, b) := by
        rw [Fintype.sum_prod_type, Finset.sum_comm]
        simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true]
        rw [← Finset.mul_sum, future_mass K hK1 T b, mul_one]

/-- Summing out `X₀`: the law of `(M, X₁, …, X_{T+1})` is the path law started from the law
of `(M, X₁)`. -/
lemma pathLaw_succ_tail (K : ξ → ξ → ℝ) (q₀ : μ × ξ → ℝ) (T : ℕ) :
    push (fun w : μ × (Fin (T + 2) → ξ) => (w.1, Fin.tail w.2)) (pathLaw K q₀ (T + 1))
      = pathLaw K (ageStep K q₀) T := by
  funext w
  obtain ⟨m, y⟩ := w
  unfold push
  rw [Finset.sum_filter, Fintype.sum_prod_type,
    Finset.sum_eq_single m (fun m' _ hm' => Finset.sum_eq_zero (fun x _ => by simp [hm']))
      (fun h => absurd (Finset.mem_univ m) h)]
  calc ∑ x : Fin (T + 2) → ξ,
        (if (m, Fin.tail x) = (m, y) then pathLaw K q₀ (T + 1) (m, x) else 0)
      = ∑ z : ξ × (Fin (T + 1) → ξ), (if z.2 = y then q₀ (m, z.1) * (K z.1 (z.2 0)
            * ∏ s : Fin T, K (z.2 s.castSucc) (z.2 s.succ)) else 0) := by
        refine Fintype.sum_equiv (Fin.consEquiv (fun _ : Fin (T + 2) => ξ)).symm _ _
          (fun x => ?_)
        show _ = (if Fin.tail x = y then q₀ (m, x 0) * (K (x 0) (Fin.tail x 0)
            * ∏ s : Fin T, K (Fin.tail x s.castSucc) (Fin.tail x s.succ)) else 0)
        unfold pathLaw
        rw [Fin.prod_univ_succ]
        simp only [Prod.mk.injEq, true_and, Fin.tail, Fin.castSucc_zero, Fin.succ_zero_eq_one,
          Fin.succ_castSucc]
    _ = pathLaw K (ageStep K q₀) T (m, y) := by
        rw [Fintype.sum_prod_type]
        simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true]
        unfold pathLaw ageStep
        dsimp only
        rw [Finset.sum_mul]
        apply Finset.sum_congr rfl
        intro c _
        ring

/-- **The bridge for Proposition 6.** Under the paper's hypothesis, the law of `(M, X_t)` is
the `t`-th iterate of the one-step map: `(ageStep K)^[t] q₀`. -/
theorem pathLaw_marginal (K : ξ → ξ → ℝ) (hK1 : ∀ x, ∑ y, K x y = 1) :
    ∀ (T : ℕ) (t : Fin (T + 1)) (q₀ : μ × ξ → ℝ),
      push (fun w : μ × (Fin (T + 1) → ξ) => (w.1, w.2 t)) (pathLaw K q₀ T)
        = (ageStep K)^[t] q₀ := by
  intro T
  induction T with
  | zero =>
    intro t q₀
    have ht : t = 0 := Fin.fin_one_eq_zero t
    subst ht
    rw [Fin.val_zero, Function.iterate_zero, id_eq]
    exact pathLaw_zero K hK1 q₀ 0
  | succ T ih =>
    intro t q₀
    cases t using Fin.cases with
    | zero =>
      rw [Fin.val_zero, Function.iterate_zero, id_eq]
      exact pathLaw_zero K hK1 q₀ (T + 1)
    | succ s =>
      have e : push (fun w : μ × (Fin (T + 2) → ξ) => (w.1, w.2 s.succ)) (pathLaw K q₀ (T + 1))
          = push (fun w : μ × (Fin (T + 1) → ξ) => (w.1, w.2 s))
              (push (fun w : μ × (Fin (T + 2) → ξ) => (w.1, Fin.tail w.2))
                (pathLaw K q₀ (T + 1))) := by
        rw [push_push]; rfl
      rw [e, pathLaw_succ_tail, ih s (ageStep K q₀), Fin.val_succ, Function.iterate_succ_apply]

/-- **Proposition 6.** For a record `M` made from `X₀`, conditionally independent of the future
given `X₀`, and a time-homogeneous Markov chain with one-step kernel `K`, the content
`L_t = H(M | X_t)` is
nondecreasing in the age `t`, for every horizon `T` and `t ≤ T`. -/
theorem stale_monotone_path (K : ξ → ξ → ℝ) (hK : ∀ x y, 0 ≤ K x y)
    (hK1 : ∀ x, ∑ y, K x y = 1) (q₀ : μ × ξ → ℝ) (hq₀ : ∀ w, 0 ≤ q₀ w) (T : ℕ) :
    Monotone (fun t : Fin (T + 1) =>
      condH (push (fun w : μ × (Fin (T + 1) → ξ) => (w.1, w.2 t)) (pathLaw K q₀ T))) := by
  intro a b hab
  dsimp only
  rw [pathLaw_marginal K hK1 T a q₀, pathLaw_marginal K hK1 T b q₀]
  exact stale_monotone K hK hK1 q₀ hq₀ hab

end Staleness

/-! ### Theorem 1, the per-code converse -/

section Converse

variable {γ μ : Type*} [Fintype γ] [Fintype μ] [DecidableEq γ] [DecidableEq μ]

/-- `I(X; Y | S) = H(X | S) − H(X | Y, S)`, for a law of `((X, Y), S)`. -/
noncomputable def condMI (r : (α × γ) × σ → ℝ) : ℝ :=
  condH (push (fun w : (α × γ) × σ => (w.1.1, w.2)) r)
    - (H r - H (push (fun w : (α × γ) × σ => (w.1.2, w.2)) r))

/-- The law of the `i`-th letter `((Xᵢ, X̂ᵢ), Sᵢ)` when `X̂ⁿ = φ(Xⁿ)` and `(Xⁿ, Sⁿ)` has law `P`. -/
noncomputable def letterLaw (n : ℕ) (φ : (Fin n → α) → (Fin n → γ)) (i : Fin n)
    (P : (Fin n → α) × (Fin n → σ) → ℝ) : (α × γ) × σ → ℝ :=
  push (fun z : (Fin n → α) × (Fin n → σ) => ((z.1 i, φ z.1 i), z.2 i)) P

/-- **Theorem 1, converse chain for the work coordinate (`eq:work-conv`).** For any code with
encoder `f` and decoder `g` on an i.i.d. block, `H(M | Sⁿ) ≥ ∑ᵢ I(Xᵢ; X̂ᵢ | Sᵢ)`, where
`M = f(Xⁿ)` and `X̂ⁿ = g(M)`. -/
theorem work_converse (n : ℕ) (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z) (hp1 : ∑ z, p z = 1)
    (f : (Fin n → α) → μ) (g : μ → (Fin n → γ)) :
    ∑ i, condMI (letterLaw n (g ∘ f) i (block n p))
      ≤ condH (push (Prod.map f id) (block n p)) := by
  set P := block n p with hPdef
  have hP : ∀ z, 0 ≤ P z := block_nonneg n p hp
  -- (1) `X̂ⁿ` is a function of `M`: `H(X̂ⁿ | Sⁿ) ≤ H(M | Sⁿ)`
  have h1 : condH (push (Prod.map (g ∘ f) id) P) ≤ condH (push (Prod.map f id) P) := by
    have := condH_push_le g (push (Prod.map f id) P) (push_nonneg _ _ hP)
    rw [push_push] at this
    exact this
  -- (2) `H(X̂ⁿ | Sⁿ) = H(Xⁿ | Sⁿ) − H(Xⁿ | X̂ⁿ, Sⁿ)`, with `Q` the law of `(Xⁿ, (X̂ⁿ, Sⁿ))`
  set Q := push (fun z : (Fin n → α) × (Fin n → σ) => (z.1, ((g ∘ f) z.1, z.2))) P with hQdef
  have hQinj : Function.Injective
      (fun z : (Fin n → α) × (Fin n → σ) => (z.1, ((g ∘ f) z.1, z.2))) := by
    intro x y h
    simp only [Prod.mk.injEq] at h
    exact Prod.ext h.1 h.2.2
  have hHQ : H Q = H P := H_push_injective _ hQinj P
  have hsQ : push Prod.snd Q = push (Prod.map (g ∘ f) id) P := by
    rw [hQdef, push_push]; rfl
  have hsY : push Prod.snd (push (Prod.map (g ∘ f) id) P) = push Prod.snd P := by
    rw [push_push]; rfl
  have h2 : condH (push (Prod.map (g ∘ f) id) P) = condH P - condH Q := by
    unfold condH
    rw [hsY, hsQ, hHQ]
    ring
  -- (3) `H(Xⁿ | Sⁿ) = ∑ᵢ H(Xᵢ | Sᵢ)`
  have hletterXS : ∀ i, push (fun w : (α × γ) × σ => (w.1.1, w.2)) (letterLaw n (g ∘ f) i P)
      = p := by
    intro i
    unfold letterLaw
    rw [push_push]
    exact block_letter n i p hp1
  have h3 : condH P
      = ∑ i, condH (push (fun w : (α × γ) × σ => (w.1.1, w.2)) (letterLaw n (g ∘ f) i P)) := by
    simp only [hletterXS]
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, hPdef,
      condH_block n p hp1]
  -- (4) `H(Xⁿ | X̂ⁿ, Sⁿ) ≤ ∑ᵢ H(Xᵢ | X̂ⁿ, Sⁿ) ≤ ∑ᵢ H(Xᵢ | X̂ᵢ, Sᵢ)`
  have h4a := condH_pi_subadd (υ := fun _ : Fin n => α) Q (push_nonneg _ _ hP)
  have h4b : ∀ i, condH (push (fun z : (Fin n → α) × ((Fin n → γ) × (Fin n → σ)) =>
        (z.1 i, z.2)) Q)
      ≤ H (letterLaw n (g ∘ f) i P)
        - H (push (fun w : (α × γ) × σ => (w.1.2, w.2)) (letterLaw n (g ∘ f) i P)) := by
    intro i
    have hc := condH_coarsen (fun c : (Fin n → γ) × (Fin n → σ) => (c.1 i, c.2 i))
      (push (fun z : (Fin n → α) × ((Fin n → γ) × (Fin n → σ)) => (z.1 i, z.2)) Q)
      (push_nonneg _ _ (push_nonneg _ _ hP))
    have e : push (Prod.map id (fun c : (Fin n → γ) × (Fin n → σ) => (c.1 i, c.2 i)))
        (push (fun z : (Fin n → α) × ((Fin n → γ) × (Fin n → σ)) => (z.1 i, z.2)) Q)
        = push (fun w : (α × γ) × σ => (w.1.1, (w.1.2, w.2))) (letterLaw n (g ∘ f) i P) := by
      rw [hQdef, push_push, push_push]
      unfold letterLaw
      rw [push_push]
      rfl
    have hassoc : Function.Injective (fun w : (α × γ) × σ => (w.1.1, (w.1.2, w.2))) := by
      intro x y h
      simp only [Prod.mk.injEq] at h
      exact Prod.ext (Prod.ext h.1 h.2.1) h.2.2
    have hval : condH (push (fun w : (α × γ) × σ => (w.1.1, (w.1.2, w.2)))
          (letterLaw n (g ∘ f) i P))
        = H (letterLaw n (g ∘ f) i P)
          - H (push (fun w : (α × γ) × σ => (w.1.2, w.2)) (letterLaw n (g ∘ f) i P)) := by
      unfold condH
      rw [H_push_injective _ hassoc, push_push]
      rfl
    rw [e, hval] at hc
    exact hc
  have h4 := h4a.trans (Finset.sum_le_sum (fun i _ => h4b i))
  -- (5) assemble
  have h5 : ∑ i, condMI (letterLaw n (g ∘ f) i P)
      = ∑ i, condH (push (fun w : (α × γ) × σ => (w.1.1, w.2)) (letterLaw n (g ∘ f) i P))
        - ∑ i, (H (letterLaw n (g ∘ f) i P)
          - H (push (fun w : (α × γ) × σ => (w.1.2, w.2)) (letterLaw n (g ∘ f) i P))) := by
    unfold condMI
    rw [Finset.sum_sub_distrib]
  linarith [h1, h2, h3, h4, h5]

/-- **The content of a memory is at most its size: `L_n ≤ R_n`.** `H(M | Sⁿ) ≤ log |ℳ|`. -/
theorem content_le_log_card [Nonempty μ] (n : ℕ) (p : α × σ → ℝ) (hp : ∀ z, 0 ≤ p z)
    (hp1 : ∑ z, p z = 1) (f : (Fin n → α) → μ) :
    condH (push (Prod.map f id) (block n p)) ≤ log (Fintype.card μ) := by
  have hnn := push_nonneg (Prod.map f id) _ (block_nonneg n p hp)
  have hmass : ∑ z, push (Prod.map f id) (block n p) z = 1 := by
    rw [sum_push, sum_block n p hp1]
  calc condH (push (Prod.map f id) (block n p))
      ≤ H (push Prod.fst (push (Prod.map f id) (block n p))) := condH_le_H_fst _ hnn hmass
    _ ≤ log (Fintype.card μ) := H_le_log_card _ (push_nonneg _ _ hnn) (by rw [sum_push, hmass])

end Converse

end ObservationTheory.ConsumerLandauer
