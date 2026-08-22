/-
GO-16 discrete/commuting extensions — machine-checked load-bearing
algebra for statement v0.5 (`paper/go16-adversarial-observer.tex`):
Theorem 4 (the binary water-level theorem), Theorem 5 (commuting
scope), and Theorem 6 (no fixed-instrument commitment gap at
commuting scope).

* `evar_closed_form` / `rho_closed_form` — the exact channel algebra:
  for a binary symmetric source and policy (a, b) = (q₀, q₁), the
  posterior-variance average is 1/4 − (b−a)²/(4(a+b)(2−a−b)), hence
  the resolved-variance ratio is ρ = (b−a)²/((a+b)(2−a−b)).
* `frontier_bound` / `frontier_attained` / `symmetric_rho` — the
  frontier THEOREM: err ≥ (1−√ρ)/2 always (since u(2−u) ≤ 1), with
  equality on the symmetric channel. Supersedes the numerical SLSQP
  validation of GO-P-2026-091's pilot.
* `sqrt_midpoint_concave` — midpoint concavity of √, i.e. midpoint
  convexity of the frontier cost s²(1−√ρ)/2.
* `shield_foc_identity` / `shield_foc_bound` — the per-coordinate
  completion of squares s²(1−x)/2 + cx² = s²/2 − s⁴/(16c) +
  c(x − s²/(4c))², x = √ρ, c = λθμ: the fifth-class FOC algebra.
* `sign_flip_average` — one step of the sign-symmetrization that
  yields diagonal optima (Theorems 3/5): averaging K with its
  conjugation by a single-coordinate sign flip kills exactly the
  off-diagonal entries touching that coordinate.
* `attention_exchange` / `fractional_pair_tie` — the reader-side
  exchange lemma: an optimal attention vector cannot be interior at
  a strictly better coordinate while positive at a worse one; hence
  any two fractional coordinates carry EQUAL g — the discrete tie,
  alphabet-independent.
* `junk_domination` — the row-reduction inequality behind Theorem 6:
  against axis reads, moving cross-signal mass into dither never
  increases the leakage term at equal value cost.

Unformalized remainder (named): the probabilistic derivation of EVar
(finite conditional expectation over the four (X, A) cells), the
water-level assembly and integer-k counting of Theorem 4, the
joint-diagonalization and convex-averaging steps of Theorem 5, and
Theorem 6's assembly (row separation, scalar reduction via
`scalar_shielding_identity`, and the saddle property). These are
standard-cited or netted by `experiments/go16_theory_extensions.py`
(S3 gates) and the governed 090/091 harnesses.
-/

import Mathlib

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace ObservationTheory.AdversarialObserverDiscrete

open Real BigOperators Finset

/-! ## The exact channel algebra -/

theorem evar_closed_form (a b : ℝ) (h0 : a + b ≠ 0) (h2 : 2 - a - b ≠ 0) :
    a * b / (2 * (a + b)) + (1 - a) * (1 - b) / (2 * (2 - a - b))
      = 1 / 4 - (b - a) ^ 2 / (4 * (a + b) * (2 - a - b)) := by
  field_simp
  ring

theorem rho_closed_form (a b : ℝ) (h0 : a + b ≠ 0) (h2 : 2 - a - b ≠ 0) :
    1 - 4 * (a * b / (2 * (a + b)) + (1 - a) * (1 - b) / (2 * (2 - a - b)))
      = (b - a) ^ 2 / ((a + b) * (2 - a - b)) := by
  rw [evar_closed_form a b h0 h2]
  field_simp
  ring

/-! ## The frontier theorem -/

theorem frontier_bound (a b : ℝ) (hw : 0 < (a + b) * (2 - a - b)) :
    (1 - Real.sqrt ((b - a) ^ 2 / ((a + b) * (2 - a - b)))) / 2
      ≤ (a + 1 - b) / 2 := by
  set w := (a + b) * (2 - a - b) with hwdef
  have hw1 : w ≤ 1 := by nlinarith [sq_nonneg (a + b - 1)]
  have hv2 : (b - a) ^ 2 ≤ (b - a) ^ 2 / w := by
    have key : (b - a) ^ 2 / w - (b - a) ^ 2
        = (b - a) ^ 2 * (1 - w) / w := by
      field_simp
    have hnn : 0 ≤ (b - a) ^ 2 * (1 - w) / w :=
      div_nonneg (mul_nonneg (sq_nonneg _) (by linarith)) hw.le
    linarith
  have habs : b - a ≤ Real.sqrt ((b - a) ^ 2 / w) :=
    calc b - a ≤ |b - a| := le_abs_self _
    _ = Real.sqrt ((b - a) ^ 2) := (Real.sqrt_sq_eq_abs _).symm
    _ ≤ Real.sqrt ((b - a) ^ 2 / w) := Real.sqrt_le_sqrt hv2
  linarith

/-- The symmetric channel (a, b) = (ε, 1−ε) has ρ = (1−2ε)². -/
theorem symmetric_rho (ε : ℝ) :
    ((1 - ε) - ε) ^ 2 / ((ε + (1 - ε)) * (2 - ε - (1 - ε)))
      = (1 - 2 * ε) ^ 2 := by
  norm_num
  ring_nf

/-- The symmetric channel attains the frontier: err = ε = (1−√ρ)/2. -/
theorem frontier_attained (ε : ℝ) (_h0 : 0 ≤ ε) (h1 : ε ≤ 1 / 2) :
    (1 - Real.sqrt ((1 - 2 * ε) ^ 2)) / 2 = ε := by
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by linarith)]
  ring

/-! ## Convexity of the frontier cost -/

theorem sqrt_midpoint_concave (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    (Real.sqrt x + Real.sqrt y) / 2 ≤ Real.sqrt ((x + y) / 2) := by
  have h1 : 0 ≤ (Real.sqrt x + Real.sqrt y) / 2 := by positivity
  have key : ((Real.sqrt x + Real.sqrt y) / 2) ^ 2 ≤ (x + y) / 2 := by
    nlinarith [sq_nonneg (Real.sqrt x - Real.sqrt y),
               Real.sq_sqrt hx, Real.sq_sqrt hy,
               Real.sqrt_nonneg x, Real.sqrt_nonneg y]
  calc (Real.sqrt x + Real.sqrt y) / 2
      = Real.sqrt (((Real.sqrt x + Real.sqrt y) / 2) ^ 2) :=
        (Real.sqrt_sq h1).symm
    _ ≤ Real.sqrt ((x + y) / 2) := Real.sqrt_le_sqrt key

/-! ## The per-coordinate FOC (fifth-class algebra) -/

theorem shield_foc_identity (s c x : ℝ) (hc : c ≠ 0) :
    s ^ 2 * (1 - x) / 2 + c * x ^ 2
      = s ^ 2 / 2 - s ^ 4 / (16 * c) + c * (x - s ^ 2 / (4 * c)) ^ 2 := by
  field_simp
  ring

theorem shield_foc_bound (s c x : ℝ) (hc : 0 < c) :
    s ^ 2 / 2 - s ^ 4 / (16 * c) ≤ s ^ 2 * (1 - x) / 2 + c * x ^ 2 := by
  rw [shield_foc_identity s c x (ne_of_gt hc)]
  nlinarith [mul_nonneg hc.le (sq_nonneg (x - s ^ 2 / (4 * c)))]

/-! ## The sign-symmetrization step (Theorems 3/5) -/

variable {n : Type*} [Fintype n] [DecidableEq n]

theorem sign_flip_average (K : Matrix n n ℝ) (i j l : n) :
    ((2⁻¹ : ℝ) •
      (K + (Matrix.diagonal fun t => if t = i then (-1 : ℝ) else 1) * K *
        (Matrix.diagonal fun t => if t = i then (-1 : ℝ) else 1))) j l
      = if ((j = i) ↔ (l = i)) then K j l else 0 := by
  simp only [Matrix.smul_apply, Matrix.add_apply, Matrix.diagonal_mul,
    Matrix.mul_diagonal, Matrix.of_apply, smul_eq_mul]
  by_cases hj : j = i <;> by_cases hl : l = i <;>
    simp [hj, hl] <;> ring

/-! ## The reader-side exchange lemma and the discrete tie -/

theorem attention_exchange (g θ : n → ℝ) (k : ℝ)
    (hθ0 : ∀ t, 0 ≤ θ t) (hθ1 : ∀ t, θ t ≤ 1) (hsum : ∑ t, θ t = k)
    (hmax : ∀ φ : n → ℝ, (∀ t, 0 ≤ φ t) → (∀ t, φ t ≤ 1) →
        (∑ t, φ t = k) → ∑ t, φ t * g t ≤ ∑ t, θ t * g t)
    {i j : n} (hij : i ≠ j) (hg : g j < g i) :
    θ i = 1 ∨ θ j = 0 := by
  by_contra hcon
  rw [not_or] at hcon
  obtain ⟨hi1, hj0⟩ := hcon
  have hi : θ i < 1 := lt_of_le_of_ne (hθ1 i) hi1
  have hj : 0 < θ j := lt_of_le_of_ne (hθ0 j) (Ne.symm hj0)
  set ε := min (1 - θ i) (θ j) with hεdef
  have hε0 : 0 < ε := lt_min (by linarith) hj
  have hεi : ε ≤ 1 - θ i := min_le_left _ _
  have hεj : ε ≤ θ j := min_le_right _ _
  set φ := fun t => θ t + (if t = i then ε else 0) - (if t = j then ε else 0)
    with hφdef
  have hφ0 : ∀ t, 0 ≤ φ t := by
    intro t
    by_cases ht : t = i
    · have htj : t ≠ j := by rw [ht]; exact hij
      simp only [hφdef, if_pos ht, if_neg htj]
      linarith [hθ0 t, hε0.le]
    · by_cases ht2 : t = j
      · simp only [hφdef, if_neg ht, if_pos ht2]
        rw [ht2]
        linarith [hθ0 j, hεj]
      · simp only [hφdef, if_neg ht, if_neg ht2]
        linarith [hθ0 t]
  have hφ1 : ∀ t, φ t ≤ 1 := by
    intro t
    by_cases ht : t = i
    · have htj : t ≠ j := by rw [ht]; exact hij
      simp only [hφdef, if_pos ht, if_neg htj]
      rw [ht]
      linarith [hεi]
    · by_cases ht2 : t = j
      · simp only [hφdef, if_neg ht, if_pos ht2]
        linarith [hθ1 t, hε0.le]
      · simp only [hφdef, if_neg ht, if_neg ht2]
        linarith [hθ1 t]
  have hφsum : ∑ t, φ t = k := by
    simp only [hφdef]
    rw [Finset.sum_sub_distrib, Finset.sum_add_distrib,
      Finset.sum_ite_eq' Finset.univ i (fun _ => ε),
      Finset.sum_ite_eq' Finset.univ j (fun _ => ε)]
    simp [hsum]
  have hexpand : ∀ t, φ t * g t
      = θ t * g t + (if t = i then ε * g i else 0)
        - (if t = j then ε * g j else 0) := by
    intro t
    by_cases ht : t = i
    · have htj : t ≠ j := by rw [ht]; exact hij
      simp only [hφdef, if_pos ht, if_neg htj]
      rw [ht]
      ring
    · by_cases ht2 : t = j
      · simp only [hφdef, if_neg ht, if_pos ht2]
        rw [ht2]
        ring
      · simp only [hφdef, if_neg ht, if_neg ht2]
        ring
  have himp : ∑ t, φ t * g t = (∑ t, θ t * g t) + ε * (g i - g j) := by
    rw [Finset.sum_congr rfl fun t _ => hexpand t]
    rw [Finset.sum_sub_distrib, Finset.sum_add_distrib,
      Finset.sum_ite_eq' Finset.univ i (fun _ => ε * g i),
      Finset.sum_ite_eq' Finset.univ j (fun _ => ε * g j)]
    simp
    ring
  have hle := hmax φ hφ0 hφ1 hφsum
  rw [himp] at hle
  nlinarith [mul_pos hε0 (show (0 : ℝ) < g i - g j by linarith)]

/-- Any two coordinates where an optimal attention vector is strictly
fractional carry equal g — the discrete tie, from the exchange lemma
alone (reader-side, alphabet-independent). -/
theorem fractional_pair_tie (g θ : n → ℝ) (k : ℝ)
    (hθ0 : ∀ t, 0 ≤ θ t) (hθ1 : ∀ t, θ t ≤ 1) (hsum : ∑ t, θ t = k)
    (hmax : ∀ φ : n → ℝ, (∀ t, 0 ≤ φ t) → (∀ t, φ t ≤ 1) →
        (∑ t, φ t = k) → ∑ t, φ t * g t ≤ ∑ t, θ t * g t)
    {i j : n} (hij : i ≠ j)
    (hi0 : 0 < θ i) (hi1 : θ i < 1) (hj0 : 0 < θ j) (hj1 : θ j < 1) :
    g i = g j := by
  rcases lt_trichotomy (g i) (g j) with h | h | h
  · rcases attention_exchange g θ k hθ0 hθ1 hsum hmax hij.symm h with h1 | h1
    · exact absurd h1 (ne_of_lt hj1)
    · exact absurd h1 (ne_of_gt hi0)
  · exact h
  · rcases attention_exchange g θ k hθ0 hθ1 hsum hmax hij h with h1 | h1
    · exact absurd h1 (ne_of_lt hi1)
    · exact absurd h1 (ne_of_gt hj0)

/-! ## The row-reduction inequality (Theorem 6) -/

/-- Against an axis read, replacing cross-signal mass by dither leaves
the value cost and the read variance unchanged while weakly reducing
the resolved numerator: the leakage term never increases. -/
theorem junk_domination (c num extra denom : ℝ) (hc : 0 ≤ c)
    (hx : 0 ≤ extra) (hd : 0 < denom) :
    c * (num / denom) ≤ c * ((num + extra) / denom) := by
  have h2 : (num + extra) / denom - num / denom = extra / denom := by
    field_simp
    ring
  have h3 : 0 ≤ extra / denom := div_nonneg hx hd.le
  have h1 : num / denom ≤ (num + extra) / denom := by linarith
  exact mul_le_mul_of_nonneg_left h1 hc

end ObservationTheory.AdversarialObserverDiscrete
