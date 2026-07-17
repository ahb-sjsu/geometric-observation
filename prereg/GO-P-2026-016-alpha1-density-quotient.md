# GO-P-2026-016 — GO-5: the α=1 density/hubness quotient restores invariant fidelity, non-spectral (PROSPECTIVE)

The GO-5 test. In diffusion-maps theory the anisotropic α-normalization at **α=1**
cancels sampling density and recovers the Laplace–Beltrami (pure-geometry) operator
— but that is a *spectral* (eigenvector) construction. GO-5 asks whether the same
**α=1 density quotient** restores the invariant in a **non-spectral** domain:
locally-scaled nearest-neighbor retrieval, ranking directly by a density-normalized
affinity, no eigendecomposition. Fresh registration; no edits to prior entries.
Governs `experiments/go5_alpha1_quotient.py` and `results/GO5-alpha1-quotient.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE.** Never run; could fail
(α=1 need not be optimal, or the quotient need not help retrieval). A pass = GO-5
`[demonstrated]`; a miss bounds the density-quotient benefit to the spectral domain
and is carried in Honest Negatives.

## Substrate, quotient, metric

- **Substrate (planted invariant + nuisance density):** latent `z ∈ R^8` from a
  **non-uniform-density** mixture (30 centers, Dirichlet(0.3) weights → a few dense
  clusters = hubs); observation `x = z Aᵀ + noise ∈ R^128`. The **invariant** = the
  latent neighbor geometry; the **nuisance** = the sampling density (hubness in x).
- **Locally-scaled affinity (non-spectral):** self-tuning `W_ij = exp(−d²_ij/(σ_i σ_j))`,
  σ_i = distance to the 7th neighbor; density `q_i = Σ_j W_ij`. Density-quotient
  ranking score `s_ij = W_ij / (q_i q_j)^α`. Retrieval = rank candidates by s_ij,
  take top-k. **No eigenvectors.**
- **Invariant fidelity:** recall@10 of the true latent (z-space) neighbors.
- **α sweep:** {0, 0.5, 1.0, 1.5}. α=0 = raw (density-corrupted); α=1 = full
  density cancellation (Laplace–Beltrami exponent); α=1.5 = over-correction.

```yaml
id: GO-P-2026-016
date: 2026-07-17
retrospective: false
claim: GO-5
domain: non-spectral (locally-scaled nearest-neighbor retrieval; no eigendecomposition)
substrate: latent z in R^8 (non-uniform mixture density) -> x = z A^T + noise in R^128; N=8000, Q=1000
quotient: s_ij = W_ij / (q_i q_j)^alpha,  W_ij=exp(-d^2/(sig_i sig_j)) self-tuning, q_i=sum_j W_ij
metric: recall@10 of true latent (z-space) 10-NN (invariant fidelity); hubness = skew of k-occurrence
alpha_sweep: [0.0, 0.5, 1.0, 1.5]
seeds: 3 (distinct mixture-density draws)
prediction:
  restoration: median recall@10(alpha=1) - recall@10(alpha=0) >= 0.05, and > 0 on 3/3 seeds
  alpha1_optimal: recall@10(alpha=1) >= max_alpha recall@10(alpha) - 0.01  AND  > recall@10(alpha=0),
                  on >= 2/3 seeds  (alpha=1, the density-canceling exponent, is (near-)best; not arbitrary)
  hubness_reduced: skew(k-occurrence at alpha=1) < skew(at alpha=0), on 3/3 seeds
gated: [restoration, alpha1_optimal, hubness_reduced]
diagnostics_reported_not_gated:
  - specificity control: a UNIFORM-density substrate (single Gaussian latent); alpha=1 should NOT
    materially help (expect |recall(1)-recall(0)| small) -- the restoration is nuisance-specific
  - per-alpha recall curves; hubness skew per alpha; per-seed values
design: {clusters: seed, stopping: fixed grid}
amendments: []
hash: sha256:3906cac4d0a6806d624a56a83274b60ac1fcdc737c36ba5003a47dc3eaf08a9f   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-5, prospective)

GO-5 is **not supported** if any hold at 3 seeds: the α=1 quotient does not restore
fidelity (median recall gain < 0.05, or not positive on all seeds); α=1 is not
(near-)optimal over the sweep (some other α clearly beats it, on ≥2/3 seeds — the
benefit is not the *density-canceling* exponent); or hubness does not fall from
α=0 to α=1 (the mechanism is absent).

`GO5_supported` requires restoration ∧ alpha1_optimal ∧ hubness_reduced. A pass =
GO-5 `[demonstrated]`: the α=1 density quotient restores invariant fidelity in a
non-spectral domain — the **quotient** face of Observation Theory (nuisance removal
recovers the invariant), transferred out of the spectral setting.
