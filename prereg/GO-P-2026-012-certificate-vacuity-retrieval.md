# GO-P-2026-012 — GO-3: the certificate's vacuity threshold predicts retrieval death (PROSPECTIVE)

The GO-3 test. A computable **margin certificate** for single-stage (top-1)
inner-product retrieval, with a **derived** vacuity threshold, predicts *where*
recall collapses — across ≥5 structurally distinct corpora, ordered by the
certificate. Fresh registration; no edits to prior entries. Governs
`experiments/go3_certificate_vacuity.py` and `results/GO3-certificate-vacuity.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE.** Never run; the threshold is
**derived, not fit**. A pass = GO-3 `[demonstrated]`; a miss (ordering fails, or the
derived threshold mislocates death) bounds the certificate and is carried in Honest
Negatives (and points to the effective-rank refinement).

## Certificate & derived threshold

Top-1 retrieval for query j succeeds iff `s(q_j, t_j) > max_{i≠t_j} s(q_j, e_i)`.
Standardizing distractor scores by their pooled mean/std, the max of N−1 ~iid
distractors sits at `μ_crit = E[max of (N−1) standard normals]` (computed by Monte
Carlo — a derived constant, not fit). The **certificate**
`μ̂ = (mean_j s(q_j,t_j) − mean distractor) / std distractor` is the mean
standardized margin. It goes **vacuous** — cannot certify the true beats the max
distractor — when `μ̂ < μ_crit`, i.e. `ρ ≡ μ̂/μ_crit < 1`. Prediction: recall
collapses at `ρ ≈ 1`, and ordering corpora by ρ orders them by recall.

**Scope:** the derived `μ_crit` assumes ~exchangeable distractors. Corpora are
generated with exchangeable-distractor structure (iso / anisotropic / heavy-tailed
/ varied N, D); strongly low-rank (correlated-distractor) corpora need an
effective-rank refinement and are explicitly out of scope for this certificate
(a future registration / the rank-certificate line).

```yaml
id: GO-P-2026-012
date: 2026-07-17
retrospective: false
claim: GO-3
task: single-stage top-1 inner-product retrieval; recall@1 measured
certificate: mu_hat = (mean_true_score - mean_distractor_score) / std_distractor_score
threshold: mu_crit = E[max of (N-1) standard normals]  (Monte-Carlo derived constant, per corpus N)
statistic: rho = mu_hat / mu_crit    # rho < 1 == certificate vacuous
corpora: >= 5 structural families x difficulty sweep (>=12 corpora total), all exchangeable-distractor:
  - iso Gaussian (D=64, N=2000), query-noise sweep sigma in {1,1.5,2,2.5,3,4}
  - anisotropic (geometric spectrum), sigma in {1.5,2.5}
  - heavy-tailed items (student-t3), sigma in {1.5,2.5}
  - iso D=128, sigma in {2,3}
  - iso N=500 (smaller corpus -> smaller mu_crit), sigma in {2,3}
prediction:
  ordering: Spearman(rho, recall@1) over all corpora >= 0.90
  vacuity_locates_death: rho at which recall@1 = 0.5 (interpolated) is within 20% of 1
                         ( |ln(rho_at_recall50)| <= ln(1.20) )
  sharp_separation: every corpus with rho >= 1.2 has recall >= 0.8 AND every corpus
                    with rho <= 0.83 has recall <= 0.2
  beats_baseline: Spearman(rho, recall) > Spearman(raw mean_true_score, recall)
                  (the normalized certificate beats the un-normalized margin)
design:
  n_corpora: >= 8 (target ~14); Q=400 queries per corpus; seed per corpus fixed
  clusters: corpus
  stopping: fixed grid
gated: [n_corpora, ordering, vacuity_locates_death, sharp_separation, beats_baseline]
diagnostics_reported_not_gated:
  - rho_vs_recall table; mu_crit per corpus; top-10 recall as a fixed-kappa cross-check
controls:
  - the sweep must bracket recall@1=0.5 (else vacuity interpolation is undefined -> reported)
amendments: []
hash: sha256:34f964fa17c85afc8a8901eb834955e467c1b8afbc3a82e7f2b129e3c741ec90   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-3, prospective)

GO-3 is **not supported** if any hold: fewer than 8 corpora or the sweep fails to
bracket recall=0.5; ordering Spearman(ρ, recall) < 0.90; the recall=0.5 crossing ρ
is not within 20% of 1 (the derived threshold mislocates death); the sharp-
separation bands fail; or ρ orders recall no better than the raw un-normalized
margin (the normalization / derived threshold adds nothing).

`GO3_supported` requires all five gated conditions. A pass = GO-3 `[demonstrated]`:
a computable certificate with a **derived** vacuity threshold predicts where
single-stage retrieval dies, across ≥5 corpora. A miss bounds the certificate
(likely → effective-rank refinement) and is carried honestly.
