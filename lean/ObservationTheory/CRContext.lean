/-
The common-reconstruction rate--distortion function with noisy context —
machine-checked load-bearing algebra for the T-IT manuscript
(`paper/tit-cr-context/tit-cr-context.tex`, Sections IV–VII).

The manuscript's central object is the quadratic (eq:Pg)

  P(g) = D·s·g² − (D + s − ρ²)·g + (1 − ρ²),   s = 1 + τ²,

whose larger root g⋆ gives the function L(D) = ½ log₂ g⋆ (Theorem 2).
This file machine-checks, over ℝ with explicit hypotheses:

* `P_at_one` / `P_at_one_neg` — the root-bracketing identity
  P(1) = (D−1)τ², and P(1) < 0 under 0 < D < 1 (well, D < 1), τ² > 0:
  the reason exactly one root exceeds 1.
* `discriminant_pos` — (D+s−ρ²)² − 4Ds(1−ρ²) > 0 under 0 < D < 1,
  τ² > 0, with NO hypothesis on ρ²: proved from the completed-square
  identity  disc = (2Ds − (D+s−ρ²))² − 4Ds·P(1)  and P(1) < 0.
* `gstar_root` — the closed-form larger root
  g⋆ = ((D+s−ρ²) + √disc)/(2Ds) satisfies P(g⋆) = 0 (Theorem 2's
  closed form), under discriminant nonnegativity and D ≠ 0, s ≠ 0.
* `gstar_gt_one` — the larger root strictly exceeds 1 under
  0 < D < 1, τ² > 0: with r = √disc, r² = disc > (2Ds − (D+s−ρ²))²
  because the difference is 4Ds·P(1) < 0, so r > 2Ds − (D+s−ρ²).
* `P_at_floor` — the floor identity of Theorem 5's single-variable
  corollary: at g_f = (s−ρ²)/(Ds), P(g_f) = −ρ²τ²/s (so the
  determinant floor is attained iff ρτ = 0 on the active regime).
* `anchor_rho_zero` / `anchor_clean_context` / `anchor_merged` — the
  three degeneration factorizations of Corollary 3:
  ρ = 0 ⇒ P = (Dg−1)(sg−1); τ² = 0 ⇒ P = (g−1)(Dg−(1−ρ²));
  ρ² = 1 ⇒ P = g(Dsg − (D+τ²)).
* `content_at_rate_channel` / `misalignment_endpoint` — Corollary 4's
  L(1) algebra: at the classical reverse channel (a,b,n) =
  (1−D, 0, D(1−D)), Q₁ = (1−D)²(1−ρ²/s) and (Q₁+n)/n =
  ((1−D)(1−ρ²/s) + D)/D.
* `surd_root_D_tenth` / `surd_root_D_threetenths` — Corollary 5's two
  exact surds: (17+√229)/6 is a root of (3/20)g² − (17/20)g + 1/4,
  and (21+√261)/18 of (9/20)g² − (21/20)g + 1/4 (the two instances
  with the same (Y,S) law and different L).
* `binary_u_half_anchor` — Theorem 7's q = ½ anchor: with
  a = (1−p)d₀ + p(1−d₁) and u = a(1−q) + (1−a)q, q = ½ gives u = ½
  (for every a: the side information is useless).
* `binary_rate_minus_content` — Theorem 7's chain-rule bookkeeping:
  R − L = (1 − (1−p)h₂(d₀) − p h₂(d₁)) − (h₂(u) − (1−p)h₂(d₀) −
  p h₂(d₁)) = 1 − h₂(u), function-agnostic (h₂ a free function).

Unformalized remainder (named, for the manuscript's honest-scope
statement): the measure-theoretic converse steps (Lemma 1's
max-entropy bound and Step-2 determinant identity in matrix form,
single-letterization, the operational theorem's covering/binning),
the matrix-convexity Lemma 4 and uniqueness Proposition (Prop. 6),
the existence/coercivity argument, and the binary symmetrization.
These are covered by the manuscript's independent numerical
harnesses (`verify_converses.py` and the two verifier scripts) and,
for the matrix determinant identity, FOC solution, reduction
identity, and gradient identities, by the third-engine MATLAB
symbolic check `paper/tit-cr-context/matlab_checks.m`.
-/

import Mathlib

set_option linter.unusedSectionVars false

namespace ObservationTheory.CRContext

open Real

/-- The load-bearing quadratic of Theorem 2 (eq:Pg):
`P D s ρ2 g = D·s·g² − (D + s − ρ²)·g + (1 − ρ²)`, with `s = 1 + τ²`
and `ρ2` standing for ρ². -/
noncomputable def P (D s ρ2 g : ℝ) : ℝ :=
  D * s * g ^ 2 - (D + s - ρ2) * g + (1 - ρ2)

/-! ## Root bracketing: P(1) = (D−1)τ² -/

/-- The identity `P(1) = (D−1)τ²` (proof of Theorem 2, root bracketing). -/
theorem P_at_one (D ρ2 τ2 : ℝ) :
    P D (1 + τ2) ρ2 1 = (D - 1) * τ2 := by
  unfold P; ring

/-- `D < 1` and `τ² > 0` force `P(1) < 0`: the value of the quadratic at
`g = 1` is negative, so (leading coefficient positive) exactly one root
exceeds 1 and `g⋆` is well defined. -/
theorem P_at_one_neg (D ρ2 τ2 : ℝ) (hD1 : D < 1) (hτ : 0 < τ2) :
    P D (1 + τ2) ρ2 1 < 0 := by
  rw [P_at_one]
  exact mul_neg_of_neg_of_pos (by linarith) hτ

/-! ## The discriminant and the closed-form root -/

/-- The discriminant `(D+s−ρ²)² − 4Ds(1−ρ²)` is strictly positive under
`0 < D < 1`, `τ² > 0` — no hypothesis on `ρ²` is needed. The engine is
the completed-square identity
`disc = (2Ds − (D+s−ρ²))² − 4Ds·P(1)` with `P(1) = (D−1)τ² < 0`. -/
theorem discriminant_pos (D ρ2 τ2 : ℝ)
    (hD0 : 0 < D) (hD1 : D < 1) (hτ : 0 < τ2) :
    0 < (D + (1 + τ2) - ρ2) ^ 2 - 4 * (D * (1 + τ2)) * (1 - ρ2) := by
  nlinarith [sq_nonneg (2 * (D * (1 + τ2)) - (D + (1 + τ2) - ρ2)),
    mul_pos (mul_pos hD0 (show (0:ℝ) < 1 + τ2 by linarith))
      (mul_pos (show (0:ℝ) < 1 - D by linarith) hτ)]

/-- The closed-form root of Theorem 2 (eq:quadratic): under discriminant
nonnegativity and `D ≠ 0`, `s ≠ 0`,
`g⋆ = ((D+s−ρ²) + √((D+s−ρ²)² − 4Ds(1−ρ²)))/(2Ds)` satisfies
`P(g⋆) = 0`. -/
theorem gstar_root (D s ρ2 : ℝ) (hD : D ≠ 0) (hs : s ≠ 0)
    (hdisc : 0 ≤ (D + s - ρ2) ^ 2 - 4 * (D * s) * (1 - ρ2)) :
    P D s ρ2
      (((D + s - ρ2) +
        Real.sqrt ((D + s - ρ2) ^ 2 - 4 * (D * s) * (1 - ρ2))) /
        (2 * (D * s))) = 0 := by
  set r := Real.sqrt ((D + s - ρ2) ^ 2 - 4 * (D * s) * (1 - ρ2)) with hr
  have hr2 : r ^ 2 = (D + s - ρ2) ^ 2 - 4 * (D * s) * (1 - ρ2) :=
    Real.sq_sqrt hdisc
  have expand : P D s ρ2 (((D + s - ρ2) + r) / (2 * (D * s)))
      = (r ^ 2 - ((D + s - ρ2) ^ 2 - 4 * (D * s) * (1 - ρ2))) /
        (4 * (D * s)) := by
    unfold P
    field_simp
    ring
  rw [expand, hr2, sub_self, zero_div]

/-- The closed-form root strictly exceeds 1 under `0 < D < 1`, `τ² > 0`:
`r² = disc` exceeds `(2Ds − (D+s−ρ²))²` (their difference is
`4Ds·P(1) < 0`), so `r > 2Ds − (D+s−ρ²)` and `g⋆ > 1`. -/
theorem gstar_gt_one (D ρ2 τ2 : ℝ)
    (hD0 : 0 < D) (hD1 : D < 1) (hτ : 0 < τ2) :
    1 < ((D + (1 + τ2) - ρ2) +
        Real.sqrt ((D + (1 + τ2) - ρ2) ^ 2 -
          4 * (D * (1 + τ2)) * (1 - ρ2))) /
        (2 * (D * (1 + τ2))) := by
  set s := 1 + τ2 with hs
  have hspos : (0:ℝ) < s := by rw [hs]; linarith
  have ha : (0:ℝ) < D * s := mul_pos hD0 hspos
  set disc := (D + s - ρ2) ^ 2 - 4 * (D * s) * (1 - ρ2) with hdisc
  have hP1 : (0:ℝ) < D * s * ((1 - D) * τ2) :=
    mul_pos ha (mul_pos (by linarith) hτ)
  -- (2Ds − (D+s−ρ²))² < disc, since disc − (…)² = 4Ds(1−D)τ² > 0
  have hlt : (2 * (D * s) - (D + s - ρ2)) ^ 2 < disc := by
    rw [hdisc, hs]; nlinarith [hP1]
  have habs : |2 * (D * s) - (D + s - ρ2)| < Real.sqrt disc := by
    have h1 : Real.sqrt ((2 * (D * s) - (D + s - ρ2)) ^ 2)
        < Real.sqrt disc :=
      Real.sqrt_lt_sqrt (sq_nonneg _) hlt
    rwa [Real.sqrt_sq_eq_abs] at h1
  have hkey : 2 * (D * s) - (D + s - ρ2) < Real.sqrt disc :=
    lt_of_le_of_lt (le_abs_self _) habs
  rw [lt_div_iff₀ (by positivity : (0:ℝ) < 2 * (D * s))]
  linarith

/-! ## The floor identity (Theorem 5, single-variable corollary) -/

/-- The floor identity: at `g_f = (s−ρ²)/(Ds)`,
`P(g_f) = −ρ²τ²/s`. Hence the determinant floor is attained
(`g⋆ = g_f`) exactly when `ρτ = 0`, and is strictly exceeded when
`ρτ ≠ 0` (the misaligned branch). -/
theorem P_at_floor (D ρ2 τ2 : ℝ) (hD : D ≠ 0) (hs : (1:ℝ) + τ2 ≠ 0) :
    P D (1 + τ2) ρ2 ((1 + τ2 - ρ2) / (D * (1 + τ2)))
      = -(ρ2 * τ2) / (1 + τ2) := by
  unfold P
  field_simp
  ring

/-! ## The three anchor factorizations (Corollary 3) -/

/-- Anchor (i), ρ = 0: `P(g) = (Dg−1)(sg−1)` — the classical
rate–distortion function corner (`g⋆ = 1/D`). -/
theorem anchor_rho_zero (D s g : ℝ) :
    P D s 0 g = (D * g - 1) * (s * g - 1) := by
  unfold P; ring

/-- Anchor (ii), τ² = 0 (s = 1): `P(g) = (g−1)(Dg−(1−ρ²))` — Gray's
conditional rate–distortion function corner (`g⋆ = max{1,(1−ρ²)/D}`). -/
theorem anchor_clean_context (D ρ2 g : ℝ) :
    P D 1 ρ2 g = (g - 1) * (D * g - (1 - ρ2)) := by
  unfold P; ring

/-- Anchor (iii), ρ² = 1: `P(g) = g(Dsg − (D+τ²))` — Steinberg's
common-reconstruction corner (`g⋆ → (D+τ²)/(Ds)`). -/
theorem anchor_merged (D τ2 g : ℝ) :
    P D (1 + τ2) 1 g = g * (D * (1 + τ2) * g - (D + τ2)) := by
  unfold P; ring

/-! ## The misalignment endpoint L(1) (Corollary 4) -/

/-- At the classical reverse channel `(a,b) = (1−D, 0)`, the conditional
form `Q₁ = Q₀ − (aρ+b)²/s` evaluates to `(1−D)²(1−ρ²/s)`
(here `ρ` is the correlation itself, not its square). -/
theorem content_at_rate_channel (D ρ s : ℝ) (hs : s ≠ 0) :
    ((1 - D) ^ 2 + 0 ^ 2 + 2 * (1 - D) * 0 * ρ)
        - ((1 - D) * ρ + 0) ^ 2 / s
      = (1 - D) ^ 2 * (1 - ρ ^ 2 / s) := by
  field_simp
  ring

/-- Corollary 4's displayed value: with `Q₁ = (1−D)²(1−ρ²/s)` and
`n = D(1−D)`, the ratio `(Q₁+n)/n` equals `((1−D)(1−ρ²/s)+D)/D`,
so `L(1) = ½ log₂ [((1−D)(1−ρ²/s)+D)/D]`. -/
theorem misalignment_endpoint (D ρ2 s : ℝ)
    (hD : D ≠ 0) (hD1 : D ≠ 1) (hs : s ≠ 0) :
    ((1 - D) ^ 2 * (1 - ρ2 / s) + D * (1 - D)) / (D * (1 - D))
      = ((1 - D) * (1 - ρ2 / s) + D) / D := by
  have h1D : (1:ℝ) - D ≠ 0 := sub_ne_zero.mpr (Ne.symm hD1)
  field_simp

/-! ## The two exact surds of Corollary 5 (cor:notmarginal) -/

/-- At `(ρ², τ², D) = (3/4, 1/2, 1/10)`: `g⋆ = (17+√229)/6` is an exact
root of `P(g) = (3/20)g² − (17/20)g + 1/4`. -/
theorem surd_root_D_tenth :
    P (1/10) (3/2) (3/4) ((17 + Real.sqrt 229) / 6) = 0 := by
  have h : Real.sqrt 229 ^ 2 = 229 :=
    Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 229)
  unfold P
  linear_combination h / 240

/-- At `(ρ², τ², D) = (3/4, 1/2, 3/10)`: `g⋆ = (21+√261)/18` is an exact
root of `P(g) = (9/20)g² − (21/20)g + 1/4`. -/
theorem surd_root_D_threetenths :
    P (3/10) (3/2) (3/4) ((21 + Real.sqrt 261) / 18) = 0 := by
  have h : Real.sqrt 261 ^ 2 = 261 :=
    Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 261)
  unfold P
  linear_combination h / 720

/-! ## Binary theorem bookkeeping (Theorem 7) -/

/-- The `q = ½` anchor of the tilt system: with
`a = (1−p)d₀ + p(1−d₁)` and `u = a(1−q) + (1−a)q`, setting `q = ½`
gives `u = ½` for every `(p, d₀, d₁)`: the side information is useless
and the tilt equation forces `d₀ = d₁ = D`. -/
theorem binary_u_half_anchor (p d0 d1 : ℝ) :
    ((1 - p) * d0 + p * (1 - d1)) * (1 - 1/2)
      + (1 - ((1 - p) * d0 + p * (1 - d1))) * (1/2) = 1/2 := by
  ring

/-- The chain-rule bookkeeping `R − L = 1 − h₂(u)`: with
`R = 1 − (1−p)h₂(d₀) − p h₂(d₁)` and
`L = h₂(u) − (1−p)h₂(d₀) − p h₂(d₁)`, the conditional-entropy terms
cancel. Function-agnostic: `h2` is an arbitrary function `ℝ → ℝ`. -/
theorem binary_rate_minus_content (h2 : ℝ → ℝ) (p d0 d1 u : ℝ) :
    (1 - (1 - p) * h2 d0 - p * h2 d1)
      - (h2 u - (1 - p) * h2 d0 - p * h2 d1) = 1 - h2 u := by
  ring

end ObservationTheory.CRContext
