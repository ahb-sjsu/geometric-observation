# GO-P-2026-019 — GO-5 v4: α=1 restores geodesic recall in diffusion-distance retrieval (PROSPECTIVE)

Fourth and (intended) resolving GO-5 registration, in the domain the diagnosis of
v1–v3 pointed at: **diffusion-distance retrieval**, where sampling density lives
**in the retrieval base** (the random walk lingers in dense regions) and is
**orthogonal** to the geometry. v1–v3 missed because direct/ADC distance is not a
density-biased operator, so the α quotient had nothing to correct (NEG-11
candidate). Here the base *is* density-biased, so the α=1 Laplace–Beltrami
cancellation can restore the geodesic invariant. Fresh registration.

**Non-spectral:** the diffusion distance is computed by **iterating the transition
matrix** (`P^t` via t matrix powers), with **no eigendecomposition** — the
non-spectral qualifier the claim requires. Governs
`experiments/go5_diffusion_distance.py` and `results/GO5-diffusion-distance.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE.** α=1 could still fail
(density bias too weak, or α≠1 optimal). If this misses too, GO-5 is `[refuted]`
(the α=1 quotient does not transfer out of the spectral operator at all).

## Substrate, operator, metric

- **Substrate (density ⟂ geometry):** latent `u ∈ [0,1]²` sampled with a strong
  **density gradient** `p(u) ∝ exp(3 u₁)` (dense at u₁=1); geometry uniform. The
  **invariant** = geodesic (2-D Euclidean) neighbors; the **nuisance** = sampling
  density. Observation `x = u Aᵀ + noise ∈ R^50`.
- **α-diffusion operator (Coifman–Lafon):** `W_ij=exp(−d²_ij/ε)` (k=15 graph);
  `q_i=Σ_j W_ij`; `W^(α)=W/(q_i q_j)^α`; row-normalize `P^(α)=D⁻¹W^(α)`.
- **Diffusion distance (non-spectral):** `Ψ=P^t` by **t=3 matrix powers**;
  `D_t(i,j)=‖Ψ_i/√π − Ψ_j/√π‖`, π = stationary (∝ D^(α) degrees). Rank by D_t.
- **Metric:** recall@10 of the true geodesic (latent-2D) 10-NN.
- **α sweep:** {0, 0.5, 1.0, 1.5} (0 = density-biased walk; 1 = Laplace–Beltrami).

```yaml
id: GO-P-2026-019
date: 2026-07-17
retrospective: false
supersedes_test_of: GO-P-2026-018    # same claim; diffusion-distance (density-in-base) domain
claim: GO-5
domain: non-spectral diffusion-distance retrieval (P^t by matrix powers; NO eigendecomposition)
substrate: latent u in [0,1]^2, density p(u) ∝ exp(3 u1) (density ⟂ geometry) -> x=uA^T+noise in R^50; N=4000, Q=1000
operator: W=exp(-d^2/eps) kNN(15); W_alpha=W/(q_i q_j)^alpha; P=D^-1 W_alpha
diffusion_distance: Psi=P^t (t=3, matrix powers); D_t(i,j)=||Psi_i/sqrt(pi) - Psi_j/sqrt(pi)||
metric: recall@10 of true geodesic (latent-2D) 10-NN
alpha_sweep: [0.0, 0.5, 1.0, 1.5]
seeds: 3
prediction:
  density_regime: max/min local-density ratio >= 5 on >= 2/3 seeds   # substrate genuinely non-uniform (regime gate)
  restoration: median recall@10(1) - recall@10(0) >= 0.03, and > 0 on 3/3 seeds
  alpha1_optimal: recall@10(1) >= max_alpha recall@10 - 0.005 AND > recall@10(0), on >= 2/3 seeds
gated: [density_regime, restoration, alpha1_optimal]
diagnostics_reported_not_gated:
  - per-alpha recall; ambient-distance recall baseline; density ratio; recall(alpha=1) vs a uniform-density control
design: {clusters: seed, stopping: fixed grid}
amendments: []
hash: sha256:62af709364de67662ac3133ead7e00f2bb73f16403d0b13e85b021ef92e8fd39   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-5 v4, prospective)

Not supported if: the substrate is not non-uniform (density ratio < 5 on ≥2/3 —
regime void); the α=1 quotient does not restore geodesic recall (median gain <
0.03 or not positive on all seeds); or α=1 is not (near-)optimal over the sweep.

`GO5_supported` requires density_regime ∧ restoration ∧ alpha1_optimal. A pass =
GO-5 `[demonstrated]`: the α=1 density quotient restores the geodesic invariant in
non-spectral diffusion-distance retrieval — the **quotient** face of Observation
Theory, in the operator domain where density actually biases the base. A miss makes
GO-5 `[refuted]` (α=1 does not transfer out of the spectral eigen-basis).
