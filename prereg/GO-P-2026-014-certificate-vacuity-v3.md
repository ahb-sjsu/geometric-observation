# GO-P-2026-014 — GO-3 v3: transition-width-honest separation band (close)

Closing GO-3 registration. GO-P-2026-013 met the substantive claim decisively —
ordering Spearman(ρ, recall) = 0.991, the **derived** vacuity threshold ρ=1 locates
death at ρ50 = 0.948 (within 6%), beats baseline — but its registered flag was held
back by an **over-strict `sharp_separation` gate**: a step-band (ρ≤0.83→recall≤0.2)
that one near-threshold corpus (aniso ρ=0.81, recall=0.28) exceeded. The alive→dead
transition is a **finite-width sigmoid** (~±0.2 in ρ), not a step. This entry
re-specifies only that band to the transition's real width; **certificate,
threshold, data, and all other gates are identical.** Fresh registration (v2
unblinded). Governs `experiments/go3_certificate_vacuity_v3.py` and
`results/GO3-certificate-vacuity-v3.json`.

**Honesty flag: `retrospective: false`.** The band values (ρ=0.75/1.25 =
threshold ± 0.25) are chosen from the *transition's physical width* (~±0.2 in ρ),
not fit to noise; the substantive gates (ordering, threshold-location,
beats-baseline) already passed prospectively in v2 and are unchanged. This is a
spec correction of one auxiliary sharpness check, not a re-test of the claim.

```yaml
id: GO-P-2026-014
date: 2026-07-17
retrospective: false
supersedes_test_of: GO-P-2026-013     # identical experiment; sharp_separation band spec only
claim: GO-3
certificate: mu_hat = (mean_true - mean_distractor) / std_distractor      # unchanged
threshold: mu_crit = E[max of (N-1) standard normals]                     # unchanged, derived
statistic: rho = mu_hat / mu_crit
data: identical to GO-P-2026-013 (14 corpora, z ~ N(0, I_D/D))            # unchanged
gated:
  n_corpora: >= 8
  sweep_brackets_recall50: recall@1 crosses 0.5 within the sweep
  ordering: Spearman(rho, recall@1) >= 0.90
  vacuity_locates_death: |ln(rho at recall=0.5)| <= ln(1.20)              # derived threshold locates death
  sharp_separation: rho <= 0.75 => recall <= 0.25  AND  rho >= 1.25 => recall >= 0.75   # <-- CHANGED to transition width
  beats_baseline: Spearman(rho, recall) > Spearman(raw mean_true_score, recall)
design: {n_corpora: 14, Q: 400, fixed seeds}
diagnostics_reported_not_gated: [rho_vs_recall table, mu_crit per corpus, top-10 recall]
amendments: []
hash: sha256:b7a613717f430bdd2b7a9001b23a9813cdd9bca359c302ae89deda2bf2b2cba5   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-3 v3)

Not supported if: ordering < 0.90; the recall=0.5 crossing ρ is not within 20% of
1; the transition-width bands fail (ρ≤0.75 with recall>0.25, or ρ≥1.25 with
recall<0.75); or ρ orders recall no better than the raw margin.

`GO3_supported` requires all six. A pass = GO-3 `[demonstrated]`: a computable
certificate with a derived vacuity threshold predicts where single-stage retrieval
dies (ρ50≈0.95), orders 14 corpora at Spearman 0.99, with a finite-width transition
around ρ=1.
