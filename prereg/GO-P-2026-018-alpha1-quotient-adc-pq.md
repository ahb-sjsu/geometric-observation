# GO-P-2026-018 — GO-5 v3: α=1 density quotient restores exact-NN recall in ADC/PQ retrieval (PROSPECTIVE)

Third GO-5 registration, in the domain the ledger names: **locally-scaled ADC
retrieval** (product quantization). v1/v2 failed on substrate design — v1
double-normalized (self-tuning kernel), v2 confounded density with the invariant
(unequal clusters) in a direct-affinity retrieval that isn't density-biased. ADC/PQ
fixes both: **quantization-induced hubness** is a genuine density nuisance
*orthogonal* to the exact (full-precision) neighbor invariant, and ADC distance is
density-biased, so the α=1 quotient has something real to correct. Fresh
registration (v2 unblinded). Governs `experiments/go5_adc_pq.py` and
`results/GO5-adc-pq.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE.** Substrate = real 768-d
Atlas book embeddings (`go4_seed{0,1,2}`, from `/archive/.../book_translation_cache`).
α=1 could still fail to be optimal (ADC hubness reduction need not peak at the
Laplace–Beltrami exponent) — genuine risk.

## Setup

- **Data (per seed):** a real 768-d book-embedding pool → db (N=10000), queries
  (Q=1000), reference (R=1000), disjoint; L2-normalized.
- **Invariant:** exact full-precision 10-NN of each query in the db (the neighbors
  quantization must not destroy).
- **ADC/PQ:** m=16 subquantizers (48-d each), k=256 centroids (MiniBatchKMeans on
  db subvectors). Query full-precision (asymmetric); db quantized. ADC distance via
  per-subspace lookup tables.
- **Locally-scaled (density quotient):** affinity `W_qj = exp(−ADC²_qj/ε)`,
  ε = median ADC². db density `q_j = Σ_{r∈ref} W_rj` (centrality over a held-out
  reference bank — no circularity). Ranking score `s_qj = W_qj / q_j^α`.
- **Metric:** recall@10 of the exact full-precision 10-NN, using s_qj ranking;
  hubness = skew of db k-occurrence over the query set.
- **α sweep:** {0, 0.5, 1.0, 1.5} (0 = raw ADC, hubbed; 1 = full density cancel).

```yaml
id: GO-P-2026-018
date: 2026-07-17
retrospective: false
supersedes_test_of: GO-P-2026-017     # same claim; ADC/PQ domain (the ledger's named example)
claim: GO-5
domain: non-spectral, locally-scaled ADC / product-quantization retrieval
substrate: real 768-d Atlas book embeddings (go4_seed0/1/2); N_db=10000, Q=1000, R=1000
invariant: exact full-precision 10-NN (quantization-independent)
pq: {m_subq: 16, k_centroids: 256, encoder: MiniBatchKMeans on db subvectors}
affinity: W_qj = exp(-ADC^2_qj / eps), eps=median ADC^2 ; density q_j = sum_{r in ref} W_rj
score: s_qj = W_qj / q_j^alpha ; retrieve top-10 by s
metric: recall@10 of exact full-precision 10-NN ; hubness = skew(db k-occurrence over queries)
alpha_sweep: [0.0, 0.5, 1.0, 1.5]
seeds: 3 (go4_seed0/1/2)
prediction:
  baseline_hubness: skew(k-occ at alpha=0) >= 0.5 on >= 2/3 seeds   # ADC is hubbed (regime gate)
  restoration: median recall@10(1) - recall@10(0) >= 0.02, and > 0 on 3/3 seeds
  alpha1_optimal: recall@10(1) >= max_alpha recall@10 - 0.005 AND > recall@10(0), on >= 2/3 seeds
  hubness_reduced: skew(alpha=1) < skew(alpha=0) on 3/3 seeds
gated: [baseline_hubness, restoration, alpha1_optimal, hubness_reduced]
diagnostics_reported_not_gated:
  - full-precision exact recall ceiling; raw-ADC recall; per-alpha recall + hubness curves
design: {clusters: seed, stopping: fixed grid}
amendments: []
hash: sha256:50a18fcb821e7148025e4ee4cf5008a90d61433004a1b6d59cab6af7973233e6   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-5 v3, prospective)

Not supported if: ADC is not hubbed (baseline skew < 0.5 on ≥2/3 — regime void);
the α=1 quotient does not restore exact-NN recall (median gain < 0.02 or not
positive on all seeds); α=1 is not (near-)optimal over the sweep (the benefit is
not the density-canceling exponent); or hubness does not fall α=0→α=1.

`GO5_supported` requires baseline_hubness ∧ restoration ∧ alpha1_optimal ∧
hubness_reduced. A pass = GO-5 `[demonstrated]`: the α=1 density quotient restores
invariant (exact-NN) fidelity in locally-scaled ADC retrieval — the **quotient**
face of Observation Theory, in the domain the ledger named.
