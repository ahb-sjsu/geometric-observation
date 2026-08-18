/-
Machine-checked core of OT-3's T1a (the adaptive pilot argument), the
one piece `Confinement.lean` left hand-proved. This closes it before
the v1.0 declaration seals.

T1a (`crucible/OT3-THEOREM.md`): against an *adaptive* strategy that
selects up to `k ≤ d-2` directions, two orthogonal rank-one operators
produce identical transcripts, so no estimator identifies the leading
eigenvector to squared overlap `> 1/2` with both. The subtlety over
the oblivious case (T1b, already formalized) is that adaptivity must
be shown to *collapse*: the strategy, run against the all-zeros
pilot, produces a deterministic direction sequence, and against either
operator it reproduces that pilot exactly, by induction on the query
sequence.

What is formalized here, faithfully:

* `overlap_pair_bound` — the estimator conclusion: for an orthonormal
  pair `u₊ ⊥ u₋` and any unit `û`, `⟪û,u₊⟫² + ⟪û,u₋⟫² ≤ 1`, hence the
  worst of the two squared overlaps is `≤ 1/2`. This is why the
  worst-case error is bounded away from zero by an absolute constant.
* `run_answers_zero` — the adaptive collapse: modelling a strategy as
  a map from answer-history to next direction and a run as an
  answer sequence consistent with it, if the operator's quadratic form
  vanishes on every pilot direction then *every* run answer is zero.
  The induction is on the query index (via `List.range`), exactly the
  ``by induction the actual run reproduces the pilot'' step.
* `t1a_transcripts_agree` — the two rank-one operators built on
  vectors orthogonal to the whole pilot span drive the run to the same
  (all-zero) transcript: identical, hence indistinguishable.
* `t1a` — assembled: identical transcripts feed any estimator the same
  input, and its single output cannot overlap both members of the
  orthonormal pair above `1/2`.

Modelled honestly, not formalized here: that `k ≤ d-2` guarantees two
orthonormal vectors orthogonal to the pilot span (a standard
dimension count, `dim (S⁰)^⊥ ≥ 2`). It enters as the hypothesis
`hp₊/hp₋` — orthogonality to every pilot direction — which is exactly
what that count buys. The adaptive `k = d-1` cell remains open, as the
markdown records.
-/

import Mathlib.Analysis.InnerProductSpace.Basic

open RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The estimator conclusion. For an orthonormal pair `u₊ ⊥ u₋` and a
unit `û`, the two squared overlaps sum to at most one (Bessel for the
pair), so their minimum is at most `1/2`: no estimate can be close to
both members. -/
theorem overlap_pair_bound
    (up um uhat : E)
    (hp : ⟪up, up⟫ = 1) (hm : ⟪um, um⟫ = 1) (ho : ⟪up, um⟫ = 0)
    (hu : ⟪uhat, uhat⟫ = 1) :
    ⟪uhat, up⟫ ^ 2 + ⟪uhat, um⟫ ^ 2 ≤ 1 := by
  set a := ⟪uhat, up⟫ with ha
  set b := ⟪uhat, um⟫ with hb
  -- residual r = uhat - a•up - b•um is orthogonal to the pair; its
  -- self-inner product is 1 - a² - b² ≥ 0.
  have hpu : ⟪up, uhat⟫ = a := by rw [ha, real_inner_comm]
  have hmu : ⟪um, uhat⟫ = b := by rw [hb, real_inner_comm]
  have hom : ⟪um, up⟫ = 0 := by rw [real_inner_comm]; exact ho
  set r : E := uhat - a • up - b • um with hr
  have hnn : (0 : ℝ) ≤ ⟪r, r⟫ := real_inner_self_nonneg
  have hexp : ⟪r, r⟫ = 1 - a ^ 2 - b ^ 2 := by
    simp only [hr, inner_sub_left, inner_sub_right, inner_smul_left,
      inner_smul_right, RCLike.conj_to_real, hu, hp, hm, ho, hom,
      hpu, hmu]
    ring
  nlinarith [hnn, hexp]

/-- The answer a single-direction probe returns from the rank-one
operator `P = λ u uᵀ` at direction `v`: the quadratic form
`⟪v, P v⟫ = λ ⟪u,v⟫²`. -/
noncomputable def rankOneQuad (lam : ℝ) (u v : E) : ℝ :=
  lam * ⟪u, v⟫ ^ 2

/-- If the probe direction is orthogonal to `u`, the rank-one operator
answers zero — the confinement fact, at the level of a single query. -/
theorem rankOneQuad_of_perp (lam : ℝ) (u v : E) (h : ⟪u, v⟫ = 0) :
    rankOneQuad lam u v = 0 := by
  simp [rankOneQuad, h]

omit [NormedAddCommGroup E] [InnerProductSpace ℝ E] in
/-- **The adaptive collapse.** A strategy `S` maps the history of
answers to the next query direction; the *pilot* is what it produces
when fed all zeros, `S (List.replicate n 0)`. A run under quadratic
form `q` is an answer sequence `a` consistent with `S`: the answer at
step `n` is `q` applied to the direction `S` picks from the first `n`
answers. If `q` vanishes on every pilot direction, every run answer is
zero — the run reproduces the pilot exactly. (Needs no inner-product
structure: pure induction on the query sequence.) -/
theorem run_answers_zero
    (S : List ℝ → E) (q : E → ℝ)
    (hpilot : ∀ n, q (S (List.replicate n (0 : ℝ))) = 0)
    (a : ℕ → ℝ)
    (hcons : ∀ n, a n = q (S ((List.range n).map a))) :
    ∀ n, a n = 0 := by
  -- the length-n answer history is all zeros, by induction on n
  have key : ∀ n, (List.range n).map a = List.replicate n (0 : ℝ) := by
    intro n
    induction n with
    | zero => simp
    | succ m ih =>
      have ham : a m = 0 := by
        rw [hcons m, ih]; exact hpilot m
      rw [List.range_succ, List.map_append, List.map_cons,
        List.map_nil, ih, ham, List.replicate_add, List.replicate_one]
  intro n
  rw [hcons n, key n]; exact hpilot n

/-- **Transcripts agree (T1a's indistinguishability).** Two rank-one
operators built on `u₊` and `u₋`, each orthogonal to every pilot
direction, drive their runs to the same all-zero transcript. An
adaptive strategy cannot separate them. -/
theorem t1a_transcripts_agree
    (S : List ℝ → E) (lam : ℝ) (up um : E)
    (hp : ∀ n, ⟪up, S (List.replicate n (0 : ℝ))⟫ = 0)
    (hm : ∀ n, ⟪um, S (List.replicate n (0 : ℝ))⟫ = 0)
    (a b : ℕ → ℝ)
    (hca : ∀ n, a n = rankOneQuad lam up (S ((List.range n).map a)))
    (hcb : ∀ n, b n = rankOneQuad lam um (S ((List.range n).map b))) :
    a = b := by
  have hza : ∀ n, a n = 0 :=
    run_answers_zero S (rankOneQuad lam up)
      (fun n => rankOneQuad_of_perp lam up _ (hp n)) a hca
  have hzb : ∀ n, b n = 0 :=
    run_answers_zero S (rankOneQuad lam um)
      (fun n => rankOneQuad_of_perp lam um _ (hm n)) b hcb
  funext n; rw [hza n, hzb n]

/-- **T1a, assembled.** Under an adaptive strategy confined by
`k ≤ d-2` (its consequence, `up, um ⊥` every pilot direction, as
hypotheses), the two orthogonal rank-one operators produce identical
transcripts; any estimator `est` reading the transcript therefore
returns one vector `û` for both, and `û` cannot have squared overlap
exceeding `1/2` with both members of the orthonormal pair. Worst-case
identification error is bounded away from zero. -/
theorem t1a
    (S : List ℝ → E) (lam : ℝ) (up um : E)
    (hpp : ⟪up, up⟫ = 1) (hmm : ⟪um, um⟫ = 1) (hpm : ⟪up, um⟫ = 0)
    (hp : ∀ n, ⟪up, S (List.replicate n (0 : ℝ))⟫ = 0)
    (hm : ∀ n, ⟪um, S (List.replicate n (0 : ℝ))⟫ = 0)
    (a b : ℕ → ℝ)
    (hca : ∀ n, a n = rankOneQuad lam up (S ((List.range n).map a)))
    (hcb : ∀ n, b n = rankOneQuad lam um (S ((List.range n).map b)))
    (est : (ℕ → ℝ) → E)
    (hunit : ⟪est a, est a⟫ = 1) :
    est a = est b ∧
      min (⟪est a, up⟫ ^ 2) (⟪est a, um⟫ ^ 2) ≤ 1 / 2 := by
  have hagree : a = b :=
    t1a_transcripts_agree S lam up um hp hm a b hca hcb
  refine ⟨by rw [hagree], ?_⟩
  have hsum : ⟪est a, up⟫ ^ 2 + ⟪est a, um⟫ ^ 2 ≤ 1 :=
    overlap_pair_bound up um (est a) hpp hmm hpm hunit
  have hsq : (0 : ℝ) ≤ ⟪est a, up⟫ ^ 2 := sq_nonneg _
  have hsq' : (0 : ℝ) ≤ ⟪est a, um⟫ ^ 2 := sq_nonneg _
  rcases le_total (⟪est a, up⟫ ^ 2) (⟪est a, um⟫ ^ 2) with h | h
  · rw [min_eq_left h]; nlinarith [hsum, h, hsq]
  · rw [min_eq_right h]; nlinarith [hsum, h, hsq']
