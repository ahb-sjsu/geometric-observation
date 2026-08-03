# R-IND-5 verification record — `complementarity-tax.tex` (incident VI-10)

**Date:** 2026-08-03 · **Verifier:** fresh-context general-purpose agent (saw only the
manuscript and the two cited companion papers; instructed to refute, ran its own
independent numerical nets, seeds 774421–774426, independent of the author-side
sanity seed 20260803) · **Manuscript version verified:** v0.1 · **Disposition:**
all findings folded into v0.2 same day.

## Verdict

**1 ERROR, 5 SHARPENINGS — core results all survived.** Theorems 1 (rate product
floor) and 4 (work floor), Proposition 2's matrix "iff" (exactness ⟺
diag(D_A,D_B) ⪯ B′Σ_xB), Corollaries 3 (closed-form tax) and 5 (discount identity
= I(Y;S)), the entire Section 5 worked instance (all 13 quoted numbers reproduced
independently), the delineation, and the abstract were CONFIRMED by full
re-derivation plus adversarial numerics.

## The error (fixed in v0.2)

Prop. 2's isotropic specialization read "D ≤ σ²(1−cos θ)". False for obtuse θ:
eigenvalues of Σ_Y are σ²(1±cos θ), so the condition is **D ≤ σ²(1−|cos θ|)**.
Counterexample executed by the verifier: θ=120°, D=0.7 — printed condition holds,
but Δ⪯Σ_Y fails (λ_min = −0.2) and the SDP exceeds the floor by +0.0614 bits.
The printed condition also violated the v↦−v symmetry (θ↦π−θ) that the problem
must have. All downstream uses (Sec. 5 sweep, remark, sanity run) were acute-angle
only and unaffected. **Fix applied:** statement and proof now carry
1−|cos θ| with the symmetry remark; the obtuse probe is added to the harness spec
and the DRAFT prereg.

## Sharpenings (all folded into v0.2)

1. **Lemma 2 / Theorem 4 — superfluous Markov hypothesis.** The conditional half
   of Lemma 2 nowhere uses V−X−S; only joint Gaussianity of (X,S) is used (once,
   exactness of h(Y|S)). The work floor therefore holds for arbitrary joints; the
   Markov condition only scopes the operational model in which I(X;X̂_A,X̂_B|S)
   *is* the reset-work coordinate. Lemma restated without Markov; scoping note
   added to Theorem 4's proof. (A strengthening.)
2. **Lemma 1 restatement dropped the equality clause** ("conditional mean attains
   tr(PΣ(V))") that Remark 1's WLOG replacement step needs. Restored.
3. **Finite-alphabet gap in the eq. (2) citation.** Paper V's multi-consumer
   theorem is proved for finite alphabets/bounded distortion; the Gaussian
   quadratic use is the standard abstract-alphabet extension. Now flagged in a
   comment rather than silently assumed (the note's own inequalities are
   alphabet-agnostic).
4. **Prop. 2 necessity — attainment micro-gap.** "If some admissible V attains…"
   now preceded by the one-sentence attainment argument (Remark 1 + compactness
   of the max-det feasible set + Gaussian backward channel).
5. **Citation labels.** [bondtwoobserver]'s environments compile globally:
   "Prop. 7.1" → *Simultaneous service*, §7; "Ex. 6.1" → orthogonal-observers
   example, §6 — and that example is a successive-refinement statement whose
   *value* coincides with the simultaneous-service optimum
   (Σ^s = diag(D₁,D₂)); the recovery remark now says so. Also κ > 0 (strict)
   under the standing hypotheses.

## Prime suspect

The verifier attacked Prop. 2's "iff" on three lines: necessity's
tightness-propagation (needs only det Σ_W = D_A·D_B + Hadamard equality + law of
total covariance), achievability edge cases (Δ = Σ_Y degenerate; Σ_Y − Δ singular
but nonzero — backward-channel disintegration survives), and numerics (135-instance
iff net with independent regime/exactness classification, 0 mismatches; boundary
bracket at θ* = arccos(1−D): exactness switches exactly at θ*). The matrix
statement survived; only its scalar translation fell (the error above).

## Verifier's independent nets (all clean unless noted)

- Thm 1: 4000 random Gaussian channels (d∈{2,3,4}, correlated reproduction
  noises) — 0 violations, worst margin +1.311 bits; 1999 adversarial near-tight
  channels (optimal backward channel + jitter) — 0 violations, worst +7.6e−10
  bits (bound grazed, never crossed); 40 **non-Gaussian** quantized/binned
  channels with exact cell probabilities — 0 violations.
- Thm 4: 4000 random Gaussian (X,S) channels — 0 violations, worst +3.379 bits;
  30 quantized channels (Gauss–Hermite × bivariate-normal rectangle
  probabilities) — 0 violations.
- Discount identity vs independently computed I(Y;S): 4000 instances, max
  deviation 2.4e−9.
- Own multi-start SLSQP max-det solves: exact floor agreement (<1e−7) at
  θ=30–90°, D=0.1; θ=15° gap +0.4114 with CT_R = 0.1223 (manuscript's ≈0.122
  confirmed); obtuse probe θ=120°, D=0.7 gap +0.0614 (the error).
- Worked instance: Gaussian common- and pair-channel minimizations (65
  multi-starts) never beat L_A + L_B (to 1e−9); 25 quantized joint channels
  respect the pointwise converse; L_A ≤ L_B proved analytically and verified on
  a 199×199 grid; scalar-corner formula vs 400k-point grid minimization to
  1e−11.

## Citation-accuracy findings

Both companion papers' characterizations verified accurate; Prop. 2 appears in
neither (the two-observer paper has the SDP but no closed-form floor, no
Δ⪯Σ_Y corner, no tax; Paper V's coordinated-reset corollary is a different
comparison). Paper V references by name are covered by the bibliography's
"as of the VI-9 revision" hedge; the two-observer numeric labels were not, and
are fixed per sharpening 5.

## Standing

This pass clears the R-IND-5 gate for the note's derivations. The
[NOVELTY-CHECK] prior-art sweeps were subsequently executed the same day
(record: `paper/complementarity-tax-NOVELTY.md`) with a major rescoping folded
into v0.3: the rate-side results (Thm. 1, Prop. 2) are, after the read-plane
reduction, prior art (Gray 1973; Xiao–Luo 2005; Lapidoth–Tinguely 2010;
Stylianou et al. 2021; Chen et al. 2026) and are now attributed; the tax
quantity, the read-operator packaging, and the entire work side survived the
sweeps with no prior found. Note the derivations verified by this pass are
unchanged by the rescoping — only their attribution changed. Still required
before the note may be cited above `[predicted]`: the governed C3 harness run
(`experiments/verify_complementarity_tax.py`, to be committed and run under the
sealed successor of `prereg/DRAFT-GO10-complementarity-tax.md`) and the flagged
manual read of Kastner–Schlatter 2024.
