# GO-P-2026-007 — GO-2 instance 2: embedding retrieval, ranking consumer (PROSPECTIVE)

Second independent instance for GO-2, toward `[replicated]`. Instance 1 (KV keys,
GO-P-2026-002/006) demonstrated both halves. This entry tests whether the **same
mechanism** — downstream distortion governed by the error covariance projected on
the consumer's read subspace, `tr(P_C Σ_δ)`, with a consumer-driven a-vs-b flip
that reconstruction cannot track — transfers to a **different representation**
(low-rank embeddings) and a **different consumer** (retrieval *ranking*, not
softmax-KL).

**Honesty flag: `retrospective: false` — PROSPECTIVE.** This exact experiment has
never been run; the synthetic embeddings are freshly generated and the prediction
below is locked before the first measurement. The representation/consumer are
retrieval-flavored (related to Paper I's domain), so a *fully* Gate-B-disjoint
domain (e.g. optimizer/gradient moments) remains for a later registration; this
one advances GO-2 to a 2nd independent instance. Governs
`experiments/go2_embed_retrieval.py` and `results/GO2-embed-retrieval.json`.

## Mechanism carried over (the prediction)

Retrieval score is s(q, i) = q·e_i. Adding a per-dimension constant to every item
(a per-dim across-item mean) shifts all scores by q·c equally → **ranking
invariant**. So — exactly as softmax was shift-invariant in tokens — the per-dim
across-item mean is a **nuisance**, the across-item-demeaned structure is the
**invariant**, and the ranking distortion is governed by
`proj_var(arm,C) = tr(P_C Σ_δ)/tr(P_C Σ_0)` with Σ = across-ITEM covariance and
P_C the query second-moment. Prediction: the a-vs-b ranking flips between an
isotropic and a subspace query bank, proj_var tracks it, reconstruction cannot.

```yaml
id: GO-P-2026-007
date: 2026-07-17
retrospective: false          # PROSPECTIVE: never run; prediction locked pre-measurement
instance: 2
representation: low-rank embeddings E in R^{N x D}, E = dc + sc * (F L^T + t3-noise),
                rank-16 latent signal + per-dim heavy-tailed noise + per-dim DC offset
consumer: inner-product retrieval ranking. d_O = mean over queries of
          (1 - Spearman(true_scores, recon_scores)) over the N-item corpus.
          (top-10 overlap deficit reported as a second, retrieval-native metric.)
consumers_probed:
  iso: isotropic unit queries                       # P_C ∝ I
  sub: unit queries in the top-8 subspace of demeaned E   # P_C = subspace projector
q_family: [a_demean_perdim_asym4, b_wholevec_peritem_uniform4, c_polar_antiprobe, d_perdim_uniform4]
probe_output:
  invariant: across-item-demeaned embedding structure in the consumer's read subspace, tr(P_C Σ_δ)
  nuisance: per-dim across-item mean (ranking shift) + per-item norm/direction
  predicted_failure_class: dc-offset
prediction:
  mechanism: proj_var = tr(P_C Σ_δ)/tr(P_C Σ_0) governs ranking distortion; recon = rel||δ|| is consumer-blind
  flip_decisive:                                     # adv = log(dO_b / dO_a); dO is a distortion (lower=better)
    dO_median: median adv_dO(iso) >= log(1.3)  AND  median adv_dO(sub) <= -log(1.15)
    dO_perseed: iso dO(a) < dO(b) in >= 10/12  AND  sub dO(b) < dO(a) in >= 10/12
  proj_tracks_flip: sign(adv_proj(C)) == sign(adv_dO(C)) per seed >= 11/12 in EACH consumer
  recon_fails: min_C Spearman(recon_arms, dO_arms) < min_C Spearman(proj_var_arms, dO_arms)
design:
  n: 12 corpus seeds; N=1024 items; D=128; 128 queries per consumer; r_sub=8
  clusters: seed
  stopping: fixed-n
  bits_matched_via: in-harness metadata-inclusive effective-bits audit (payload 4-bit +
    fp16 scalars per row/col; NO per-block codebook). Gate: spread <= 0.5 bit.
  snr_gate: min-arm median d_O >= 10 x the fp16-vs-fp16 rerun floor (ranking signal non-degenerate).
gated: [audit, snr, flip_decisive, proj_tracks_flip, recon_fails]
diagnostics_reported_not_gated:
  - anti_probe_gap: median dO(c)/dO(a) per consumer
  - full_rank_spearman: Spearman(proj_var, dO) and Spearman(recon, dO) per consumer
  - top10_overlap_deficit: retrieval-native flip check per consumer
controls:
  - noise-floor: d_O against the fp16-vs-fp16 rerun, per consumer.
amendments: []
hash: sha256:66fc8ab36490b95b6201a1e1cb21e26d05248191eec9854d7814a19c1a78e0dc   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (instance 2, prospective)

The mechanism **fails to replicate** on this instance if any hold at n=12:
- audit fails (spread > 0.5) or SNR gate fails (signal not ≥ 10× floor); or
- the flip is not decisive (median adv_dO(iso) < log1.3, or adv_dO(sub) > −log1.15,
  or per-seed flip < 10/12 either direction); or
- proj_var does not track the flip per-seed (< 11/12 in either consumer); or
- reconstruction tracks a,b as well as proj_var (min_C Spearman(recon,dO) not
  strictly < min_C Spearman(proj_var,dO)).

`GO2_mechanism_replicates` requires all five gated conditions. A pass makes GO-2's
mechanism `[replicated]` (2 independent instances) — a genuine prospective hit. A
miss is a `[refuted]`-leaning row that bounds the mechanism's domain (e.g. it holds
for softmax but not ranking) — equally informative, carried in Honest Negatives.
