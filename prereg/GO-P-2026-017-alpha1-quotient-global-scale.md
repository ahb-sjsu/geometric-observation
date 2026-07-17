# GO-P-2026-017 — GO-5 v2: α=1 density quotient restores fidelity, global-scale kernel (PROSPECTIVE)

Corrects GO-P-2026-016, whose run was degenerate: a **self-tuning** local-scale
kernel already density-normalized the affinity (baseline hubness skew ≈ 0.01 —
nothing to restore), so the α quotient stacked a *second* normalization and
over-corrected. This entry uses a **global-scale** kernel so density stays in the
affinity and raw (α=0) retrieval is genuinely hubbed; the α=1 quotient is then the
*only* density normalization. Adds a **baseline-hubness regime gate** so the
substrate must actually be hubbed for the test to count. Fresh registration (v1
unblinded). Certificate/claim otherwise unchanged. Governs
`experiments/go5_alpha1_quotient_v2.py` and `results/GO5-alpha1-quotient-v2.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE.** α=1 could still fail to be
optimal / to restore; genuine risk. Only the kernel scaling and the regime gate
change vs v1.

## Change vs GO-P-2026-016

- Kernel: **global** bandwidth `W_ij = exp(−d²_ij / ε)`, `ε = median_i (7th-NN
  dist)²` (a single global scale — keeps density in the affinity), replacing the
  self-tuning per-point `σ_i σ_j`. Density `q_i = Σ_j W_ij` now varies with local
  density; ranking score `s_ij = W_ij / (q_i q_j)^α` unchanged.
- New regime gate: baseline hubness `skew(k-occurrence at α=0) ≥ 0.5` (the raw
  retrieval must be hubbed; else the test is void — mirrors GO-3's bracket gate).

```yaml
id: GO-P-2026-017
date: 2026-07-17
retrospective: false
supersedes_test_of: GO-P-2026-016    # same claim; global-scale kernel + regime gate
claim: GO-5
domain: non-spectral (locally-scaled NN retrieval; no eigendecomposition)
substrate: latent z in R^8 (non-uniform 30-cluster Dirichlet(0.3) density) -> x=zA^T+noise in R^128; N=8000, Q=1000
kernel: W_ij = exp(-d^2_ij / eps), eps = median_i(7th-NN dist)^2   # GLOBAL scale
quotient: s_ij = W_ij / (q_i q_j)^alpha, q_i = sum_j W_ij
metric: recall@10 of true latent 10-NN; hubness = skew of k-occurrence
alpha_sweep: [0.0, 0.5, 1.0, 1.5]
seeds: 3
prediction:
  baseline_hubness: skew(k-occ at alpha=0) >= 0.5 on >= 2/3 seeds   # REGIME gate (substrate is hubbed)
  restoration: median recall@10(1) - recall@10(0) >= 0.05, and > 0 on 3/3 seeds
  alpha1_optimal: recall@10(1) >= max_alpha recall@10 - 0.01 AND > recall@10(0), on >= 2/3 seeds
  hubness_reduced: skew(alpha=1) < skew(alpha=0) on 3/3 seeds
gated: [baseline_hubness, restoration, alpha1_optimal, hubness_reduced]
diagnostics_reported_not_gated:
  - specificity control: uniform-density substrate; alpha=1 should not materially help
  - per-alpha recall + hubness curves
design: {clusters: seed, stopping: fixed grid}
amendments: []
hash: sha256:a1c9faa9c5c119cacbc6e8e33f609043bbadc7621cc7181817da3fb928850f48   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-5 v2, prospective)

Not supported if: the substrate is not hubbed (baseline skew < 0.5 on ≥2/3 seeds —
regime void, re-scope); the α=1 quotient does not restore fidelity (median recall
gain < 0.05 or not positive on all seeds); α=1 is not (near-)optimal over the
sweep; or hubness does not fall from α=0 to α=1.

`GO5_supported` requires baseline_hubness ∧ restoration ∧ alpha1_optimal ∧
hubness_reduced. A pass = GO-5 `[demonstrated]`: the α=1 density quotient restores
invariant fidelity in a non-spectral, genuinely-hubbed domain — the **quotient**
face of Observation Theory.
