# PREREG-OT1 — consumer disagreement follows read-subspace geometry

**Sealed 2026-08-15 with the Crucible. The curve below is derived before
measurement; the experiment's job is to hit it or kill it. No constant
in this file may change after this commit.**

## The derived law (rank-1 core)

Two consumers with unit read directions `a₁, a₂`, `a₁ᵀa₂ = cos θ`,
equal sensitivity `λ`:

    P₁ = λ a₁a₁ᵀ,    P₂ = λ a₂a₂ᵀ

For a zero-mean perturbation `δ` with covariance `Σ_δ`, predicted damage
is `D_i = tr(P_i Σ_δ)`. Two sealed consequences:

**(L1) The ratio curve.** For directional perturbations along `a₁`
(`Σ_δ = ε² a₁a₁ᵀ`):

    D₂ / D₁ = cos²θ            — exactly, no free parameter.

**(L2) The 45° flip.** Two codecs of equal Euclidean energy ε²: codec A
concentrates distortion along `a₁`; codec B along `b ⊥ a₁` in
`span{a₁,a₂}`. Then `D₁(A) = λε², D₁(B) = 0`; `D₂(A) = λε²cos²θ,
D₂(B) = λε²sin²θ`. Consumer 1 always prefers B; consumer 2 prefers B
iff `θ < 45°`. **Codec-preference disagreement switches on at exactly
θ = 45°**, a zero-parameter prediction.

Damage is *measured* as mean squared output change (the consumer's own
`G`-norm), never assumed: the law says measured damage matches
`tr(P_iΣ_δ)` within linearization tolerance.

## Arms and bars

**Arm S (synthetic, the sealed curve).**
- Consumers: `C_i(x) = φ(λ¹ᐟ² a_iᵀ x)` with φ = tanh, operated in its
  differential region (inputs scaled so |pre-activation| ≤ 0.5).
- d = 64; θ grid **{0°, 15°, 30°, 45°, 60°, 75°, 90°}**; spectrum,
  rank, substrate distribution `N(0, I_d)`, and perturbation energy
  `ε = 0.01` all held fixed across θ.
- n = 10,000 perturbation draws per cell; seed 20260815.
- **Bar S1:** max over the grid of `|D̂₂/D̂₁ − cos²θ| ≤ 0.05` (at θ=90°
  the ratio's denominator convention: report `D̂₂/(λε²)` vs cos²θ).
- **Bar S2:** the preference flip lands in (30°, 60°) — i.e., agreement
  at ≤30°, disagreement at ≥60°, with the crossing bracketing 45°.

**Arm R (rank-r generalization, same law, no refit).**
- `P_i` random rank-4 with matched spectra, principal angles set by
  construction; prediction `D̂₂/D̂₁ = tr(P₂Σ_δ)/tr(P₁Σ_δ)` computed
  before each run from the constructed operators.
- **Bar R1:** relative error of predicted vs measured ratio ≤ 10%
  across 20 random constructions (seed 20260815).

**Arm H (real heads, the transfer that makes it theory).**
- 8 head-pairs reading the same KV position, Llama-3.2-3B (the
  calibration model already characterized at resolution 1.000);
  operators recovered blind at `k/d = 1.25` per the readscope spec.
- For each pair: two codecs, equal reconstruction error (the C-12-style
  tied construction), preference of each head computed from measured
  downstream damage.
- **Bar H1:** the sign of preference disagreement is predicted by
  `sign(tr((P₁−P₂)(Σ_A−Σ_B)))` on **≥ 7 of 8** pairs, with all
  quantities from the blind probes — **zero refit of anything in this
  file against Arm H data**.

## Multiplicity and verdict

OT-1 survives iff **S1 ∧ S2 ∧ R1 ∧ H1**. Any single bar failing kills
the test as sealed (partial results recorded in the ledger, not
graded up). The synthetic arms are necessary — a theory that only works
where it cannot be checked analytically is not being tested — and Arm H
is the claim: geometry measured by one instrument predicts the
disagreement of real consumers it never touched.

## Threats, named now

- tanh saturation would corrupt L1 → the |pre-activation| ≤ 0.5
  operating rule, checked and logged per cell.
- Codec ties must be exact as in the C-12 construction; a tie broken at
  1e-9 re-admits reconstruction as a hidden variable — tie verification
  is part of Arm H's record.
- Head pairs with near-parallel read subspaces (θ̂ < 10°) predict weak
  disagreement signals; pairs are drawn across layers to spread θ̂, and
  θ̂ is recorded before preferences are measured.
