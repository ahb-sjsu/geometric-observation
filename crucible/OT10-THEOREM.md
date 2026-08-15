# OT-10 — the noisy cliff: derivation before measurement

**The theorem half of OT-10 (claim frozen in `OT-CRUCIBLE-2.md`).
Model, two statements with proofs, sealed tolerance for the numerical
half (`PREREG-OT10-APPENDIX.md`).**

## Model

The confinement model of OT-3, plus noise: the transcript is the
compressed block corrupted by symmetric iid noise,

    B = VᵀPV + E,    E = Eᵀ,  E_ij ~ N(0, σ²) independent for i ≤ j.

## Statement 1 — the cliff's location does not move

For every k < d (adaptive to d−2, oblivious to d−1, as in OT-3), the
noiseless indistinguishable-pair construction transfers verbatim: the
two operators produce *identical* noiseless transcripts, and adding
noise drawn from the same distribution to identical transcripts yields
*identically distributed* observations. No estimator distinguishes
them at any σ; identification of a hidden leading eigenspace remains
impossible below the cliff. **Noise never buys admission and never
revokes it: the location is σ-independent.** ∎

## Statement 2 — the floor above the cliff, to first order

At k = d (V an orthonormal basis), the natural estimator is the top
eigenvector û₁ of `V B Vᵀ = P + Ẽ` with `Ẽ = VEVᵀ` (same law as E).
For rank-1 `P = λ₁u₁u₁ᵀ`, first-order eigenvector perturbation gives

    û₁ ≈ u₁ + Σ_{j≥2} (u_jᵀẼu₁ / λ₁) u_j,

and with `u_jᵀẼu₁ ~ N(0, σ²)` (orthonormal frames, the symmetric-iid
convention above),

    E[ sin²θ(û₁, u₁) ] = σ²(d−1)/λ₁² + O(σ⁴/λ₁⁴).

**The floor is σ²(d−1)/λ₁²**: noise prices accuracy at k = d,
quadratically in σ, linearly in the unread dimensions, inversely in
the spectral gap squared (for rank-1, the gap is λ₁). Sealed validity
condition: the first-order expression is claimed only where it
predicts error ≤ 0.1; the sealed numerical tolerance is a factor of
**2** either side (eigenvector perturbation at this order carries
O(σ⁴) corrections and the u_jᵀẼu₁ variance convention contributes
O(1/d) diagonal effects — a factor-2 band is honest, and tighter
claims wait for a sharper convention).

## What the two statements jointly forbid

- Recovery of a hidden component below k = d at any noise level
  (Statement 1) — graded by OT-3's inherited no-hidden-recovery bar.
- A floor that scales other than σ² (log-log slope 2), or sits outside
  the factor-2 band of σ²(d−1)/λ₁², or a cliff-edge contrast that
  erodes as σ grows within the validity range (Statement 2).
