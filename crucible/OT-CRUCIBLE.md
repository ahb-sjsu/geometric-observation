# The Observation Theory Crucible

**Sealed at claim level 2026-08-15, before any test runs.** Seven tests,
one campaign, one verdict under the graduation rule of
`OT-V0.1-FREEZE.md`. Claims below are frozen with this commit; each
test's *instrument appendix* (grids, tolerances, seeds, model lists) is
committed before that test runs and never after. OT-1's appendix is
already full (`PREREG-OT1.md`). Ledger entries go to `claims/LEDGER.md`
under IDs OT-1…OT-7.

| test | principle | prospective claim (frozen) | kill condition (frozen) |
|---|---|---|---|
| OT-7 | foundation | Transformation and invariance laws hold as derived below | any derived invariant fails numerically under random `A ∈ GL(d)` |
| OT-3 | P3 | A lower bound theorem: under the stated observation model, `< d` scalar directional observations cannot uniformly identify even the leading eigenspace; side information of a known `k₀`-subspace moves the cliff to `≈ d − k₀` **and it stays a cliff** | recovery improves *smoothly* with side information, or the bound cannot be proved in the declared model |
| OT-1 | P1 | Consumer disagreement follows read-subspace geometry: damage ratio `cos²θ` on synthetic consumers, codec-preference flip at `θ = 45°`, both transferring to real heads with **no refit** | sealed curve misses tolerance on synthetics, or real heads need refitting |
| OT-2 | P2 | Loading is a covariance, not a distance: first-order reading error is `dP/dε|₀ = E_D[h·A]` (change-of-measure × local operator), so damage tracks the derived alignment functional and a large orthogonal shift does ~nothing | alignment functional predicts no better than scalar shift magnitude |
| OT-5 | P5 | The metric fails where the theory says it stops: `tr(P_C Σ_δ)` damage-ranking accuracy degrades **monotonically** in measured differential fraction along a smooth→selection consumer family (temperature knob), with the ordering preregistered | accuracy is flat, non-monotone, or fails while differential fraction is still high |
| OT-4 | P4 | Drift is the mechanism: short-sequence `d(P_C(t₁), P_C(t₂))` predicts a degradation onset `t*` for a codec calibrated at `t₀`, **and** refreshing `P_C` every `R` tokens (R derived, sealed) moves/eliminates the onset in turboquant-pro | onset appears far from prediction, or the predicted intervention does not move it |
| OT-6 | P1+P5 | The laws transfer outside compression with **zero modification**: blind-recovered `P_C` of a ranking consumer over embeddings; two perturbations of equal Euclidean energy, opposite `tr(P_C Σ_δ)`; the trace picks the ranking-destroyer | the trace does no better than Euclidean energy on the new consumer class |

## Run order, and why

**OT-7 → OT-3 → OT-1 → OT-2 → OT-5 → OT-4 → OT-6.**
Mathematics first (OT-7 costs a derivation and a numerical check; OT-3's
theorem work gates its experiment), then the cleanest synthetic
experiment (OT-1), then the two lab curves (OT-2, OT-5), then the
highest-stakes real-system test (OT-4), and cross-domain transfer (OT-6)
last so the laws it transfers are already verdict-bearing.

## OT-7 — the derivations put on record now (predictions, not results)

Under substrate reparameterization `x' = Ax`, `A ∈ GL(d)`:
`J' = J A⁻¹`, hence

    P'_C = A⁻ᵀ P_C A⁻¹      and      δx'ᵀ P'_C δx' = δxᵀ P_C δx.

The quadratic damage form is a **geometric scalar** — consumer-weighted
damage is not an artifact of coordinates. The invariance taxonomy to be
verified numerically (random `A`, both classes, multiple spectra):

| quantity | invariant under GL(d)? | under O(d)? |
|---|---|---|
| `δxᵀP_Cδx` (damage form) | **yes** | yes |
| `tr(P_C Σ_δ)` (with `Σ' = AΣAᵀ`) | **yes** | yes |
| rank | **yes** | yes |
| eigenvalue spectrum, effective rank, energy rank | no | **yes** |
| principal angles between read subspaces | no | **yes** |
| water-filling allocation | no | **yes** (as a set, rotated) |
| loading functional `E[hA]` (as an operator, covariantly) | transforms as `P_C` | yes |

The GL-fragile rows are predictions too: OT-7 fails if a "no" row turns
out invariant or a "yes" row breaks. Consequence worth sealing: **P3's
cliff is at ambient `d` in every basis** (rank is GL-invariant, spectrum
is not — identification cost cannot be bought down by reparameterization).

## OT-2 — the mathematical heart, put on record now

With `A(x) = J(x)ᵀGJ(x)` and a change of measure
`dD_ε = (1 + εh(x)) dD`:

    dP_C/dε |₀ = E_D[ h(x) A(x) ]        (E_D[h] = 0)

Loading error is the **covariance between the change of measure and the
local observation operator** — not a scalar distance between
distributions. This is why three scalar corrections failed and why a
large shift orthogonal (in this functional sense) to the variation of
`A` does nothing. OT-2's experiment measures exactly this: damage vs the
derived alignment functional, against the scalar-loading baseline.
Closed-form special case for the appendix: Gaussian `D`, mean shift
`Δμ` and covariance shift `ΔΣ`, where the first-order terms reduce to
`Δμᵀ(∇ₓ⊙A)`-type and `tr`-type functionals — the appendix fixes these
before the run; the *claim* (covariance beats distance) is frozen here.

## Sealing protocol

- This commit seals: the seven claims, the kill conditions, the run
  order, OT-7's derivations and taxonomy, OT-2's first-order law, and
  OT-1's complete appendix.
- Before each remaining test runs: its instrument appendix is committed
  (grids, tolerances, seeds, models, and for OT-4 the derived `R`);
  appendices may **narrow** claims, never widen them.
- Every run appends to the claims ledger; failed bars stand as written.
- The campaign verdict recomputes the v0.1 freeze hash (rule G4).
