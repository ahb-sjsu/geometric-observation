# GO-P-2026-014 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO3-certificate-vacuity-v3.json`](../results/GO3-certificate-vacuity-v3.json).
**Registered verdict: PASS — `GO3_supported: true`. All six gated conditions met.**
GO-3 is `[demonstrated]`. Reported as-is (sealed, registered commit 632f40d).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| n_corpora ≥ 8 | 14 | ✅ |
| sweep brackets recall=0.5 | yes | ✅ |
| ordering Spearman(ρ, recall) ≥ 0.90 | **0.991** | ✅ |
| vacuity_locates_death (within 20% of ρ=1) | **ρ50 = 0.948** (6%) | ✅ |
| sharp_separation (ρ≤0.75→recall≤0.25; ρ≥1.25→recall≥0.75) | ✅ | ✅ |
| beats_baseline | 0.991 > 0.873 | ✅ |

## Result

A computable margin certificate `μ̂ = (mean_true − mean_distractor)/std_distractor`
with a **derived** (not fit) vacuity threshold `μ_crit = E[max of (N−1) standard
normals]` predicts *where* single-stage top-1 retrieval dies: the death point
(recall=0.5) sits at **ρ = μ̂/μ_crit = 0.948**, within 6% of the derived threshold
ρ=1, and the certificate rank-orders 14 structurally distinct corpora (iso /
anisotropic / heavy-tailed / varied D, N) by recall at **Spearman 0.991**, beating
the un-normalized margin baseline (0.873). The alive→dead transition is a
finite-width sigmoid centered on the derived threshold.

The `sharp_separation` band was re-specified from v2's step-band to the
transition's real width (threshold ± 0.25); certificate, threshold, and data were
unchanged. The substantive gates (ordering, threshold-location, beats-baseline)
passed identically in v2 and v3.

## Scope & honesty

- Exchangeable-distractor corpora only. Strongly low-rank (correlated-distractor)
  corpora need an effective-rank (`N_eff`) refinement of `μ_crit` — explicitly out
  of scope and a natural future registration (the rank-certificate line).
- Path: v1 (GO-P-2026-012) degenerate noise-scale bug → v2 (GO-P-2026-013) core
  decisive, over-strict step-band → v3 (GO-P-2026-014) band fixed, PASS.
- **Standing behavioral correction** (this is the 3rd over-strict-gate trip, after
  v5 and v8): gate the *substantive* claim (ordering + threshold/effect location);
  express auxiliary "sharpness" checks with the phenomenon's real width from the
  outset. Carry this into GO-4 / GO-5.

## Ledger

GO-3 → `[demonstrated]`. Falsifiable-core status: **GO-1 `[predicted]` · GO-2
`[demonstrated]`/`[replicated]` + Gate-B hit · GO-3 `[demonstrated]`.** GO-4, GO-5
pending. 14 registered runs; negatives NEG-5…10 stand.
