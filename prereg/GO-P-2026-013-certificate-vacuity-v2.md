# GO-P-2026-013 — GO-3 v2: certificate vacuity predicts retrieval death, corrected noise scale (PROSPECTIVE)

Corrects GO-P-2026-012, whose run was **degenerate** — a query-noise scale bug
(`z ~ N(0, I_D)` swamped the unit-norm items, ‖z‖≈√D≈8) put all 14 corpora in the
dead regime (ρ 0.07–0.30, recall ~0), so the alive→dead *transition* — the actual
GO-3 claim — was never entered. The certificate was consistent (vacuous→dead held
for all), but untested. This entry fixes the noise scaling so the σ-sweep spans
alive→dead; **certificate and derived threshold are unchanged.** Fresh
registration (v1 was unblinded). Governs
`experiments/go3_certificate_vacuity_v2.py` and
`results/GO3-certificate-vacuity-v2.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE.** The threshold is derived,
not fit; only the noise scale is corrected.

## Change vs GO-P-2026-012

Queries `q = normalize(e_t + σ z)` with `z ~ N(0, I_D/D)` (‖z‖≈1), matching the
unit-norm items. Then `μ̂ ≈ √D / √(1+σ²)`; at D=64 the sweep σ∈{1,…,4} spans
ρ ≈ 1.65 → 0.57, bracketing ρ=1 and recall=0.5. Everything else — certificate
`μ̂ = (mean_true − mean_distractor)/std_distractor`, derived threshold
`μ_crit = E[max of (N−1) standard normals]`, `ρ = μ̂/μ_crit`, corpus families, and
all five gates — is identical to GO-P-2026-012.

```yaml
id: GO-P-2026-013
date: 2026-07-17
retrospective: false
supersedes_test_of: GO-P-2026-012     # same claim; corrected query-noise scale
claim: GO-3
task: single-stage top-1 inner-product retrieval; recall@1
certificate: mu_hat = (mean_true - mean_distractor) / std_distractor
threshold: mu_crit = E[max of (N-1) standard normals]  (Monte-Carlo derived; per corpus N)
statistic: rho = mu_hat / mu_crit
change: query noise z ~ N(0, I_D / D) (was N(0, I_D)); items unit-norm
corpora: iso D64 N2000 sigma{1,1.5,2,2.5,3,4}; aniso & heavytail sigma{1.5,2.5};
         iso D128 sigma{2,3}; iso N500 sigma{2,3}   # 14, exchangeable-distractor
prediction:
  ordering: Spearman(rho, recall@1) over all corpora >= 0.90
  vacuity_locates_death: rho at recall@1 = 0.5 (interpolated) within 20% of 1 ( |ln rho50| <= ln1.20 )
  sharp_separation: rho >= 1.2 => recall >= 0.8 ; rho <= 0.83 => recall <= 0.2
  beats_baseline: Spearman(rho, recall) > Spearman(raw mean_true_score, recall)
design:
  n_corpora: 14; Q=400 queries/corpus; fixed seeds; must bracket recall@1=0.5
  clusters: corpus
  stopping: fixed grid
gated: [n_corpora, sweep_brackets_recall50, ordering, vacuity_locates_death, sharp_separation, beats_baseline]
diagnostics_reported_not_gated: [rho_vs_recall table, mu_crit per corpus, top-10 recall]
controls: [noise-floor n/a; the sweep MUST bracket recall=0.5 -- now a gate]
amendments: []
hash: sha256:4e0b2a882238b8a96912e495e9618a648a96c2bad4a8aa4e84bb5ac49abf12ea   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-3 v2, prospective)

Not supported if: the sweep fails to bracket recall=0.5 (regime coverage); ordering
Spearman < 0.90; the recall=0.5 crossing ρ is not within 20% of 1 (the derived
threshold mislocates death); the sharp-separation bands fail; or ρ orders recall no
better than the raw un-normalized margin.

`GO3_supported` requires all six gated conditions. A pass = GO-3 `[demonstrated]`:
a computable certificate with a **derived** (not fit) vacuity threshold predicts
where single-stage retrieval dies, across ≥5 exchangeable-distractor corpora.
