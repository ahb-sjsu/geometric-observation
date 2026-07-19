# GO-P-2026-035 — Legal-retrieval consumer-relative flip (CourtListener citations)

A sealed, prospective single-domain test extending the confirmed GO-2 instance-2 (embedding retrieval,
`GO-P-2026-009`) to a **real, large corpus with a real trained consumer** in a new content domain:
**legal citation retrieval**. It is also the first domain to satisfy — and exploit — the boundary
condition discovered in the `GO-P-2026-034` D4 negative: the flip needs the read operator **misaligned**
with the signal's dominant energy. Sentence embeddings are strongly **anisotropic** (a high-variance
mean/nuisance cone that carries no ranking signal), so reconstruction-optimal compression spends bits on
the nuisance while read-preserving protects the discriminative directions.

## Setup
- **Corpus / consumer.** CourtListener opinions (`/archive/courtlistener`); relevance = true
  **(citing, cited)** pairs. Consumer = cosine ranking; metric = **retrieval AUROC** (true doc ranks
  above other docs for its query). Embeddings = base **LaBSE** (768-d). Uncompressed AUROC ≈ 0.76;
  **centering the embeddings raises it to 0.84** — direct evidence the anisotropy is nuisance and the
  ranking signal lives in the centered/semantic directions.
- **Read operator.** The **centered (semantic) covariance** of the document embeddings — the directions
  that carry the ranking signal. The **raw** covariance is dominated by the anisotropy/mean cone.
- **Three matched-bit arms** compress the DOCUMENT embeddings (queries uncompressed), quantizing in the
  semantic eigenbasis over a fixed per-direction range, at the SAME total bits, differing only in
  allocation:
  - **(O) reconstruction-optimal** — bits by RAW variance (protects the anisotropy; minimizes ‖b−b̂‖²).
  - **(R) read-preserving** — bits by CENTERED/semantic variance (protects the discriminative directions).
  - **(A) anti** — bits by raw/centered ratio (protects only the mean-dominated nuisance directions).
- **Discipline.** The read operator (μ, V, σ²) is **fit on calibration** documents (`pairs_train`),
  frozen, and applied unchanged to the **held-out** set (`pairs_eval` — opinions disjoint from training,
  `id%10==7`). The rate is selected on calibration, sealed here, and confirmed on held-out.

```yaml
id: GO-P-2026-035
date: 2026-07-19
retrospective: false
kind: sealed prospective single-domain test (consumer-relative flip on real legal-citation retrieval)
consumer: cosine citation-pair ranking, retrieval AUROC; embeddings = base LaBSE (768-d)
read_operator: centered (semantic) document covariance; nuisance = raw anisotropy/mean cone
arms: three matched-bit codes on the document embeddings (O recon-optimal / R read-preserving / A anti)
data: CourtListener (citing,cited) pairs; calibration = pairs_train (n=4000, read operator fit here);
  heldout = pairs_eval (disjoint opinions id%10==7)
frozen_config: {base_bits: 0.4, quantizer: semantic-eigenbasis scalar, fixed per-direction range}
calibration_result: {auroc_R: 0.746, auroc_O: 0.742, auroc_A: 0.589, auroc_uncompressed: 0.764,
  recon_O: 0.223, recon_R: 0.264, flip_bootstraps: 168/200, anti_bootstraps: 200/200, recon_trade: true}
prediction:
  the flip replicates on the held-out disjoint pairs at the frozen rate:
  clean flip AUROC(R) >= AUROC(O) on >= 60% of bootstrap query subsets; recon-trade recon(O) <= recon(R)
  (recon-optimal reconstructs the embeddings better); anti worst (AUROC(A) <= min(AUROC(R),AUROC(O)))
  on >= 70% of bootstraps; and read-preserving beats reconstruction-optimal on the full-set AUROC.
falsification: the flip FAILS its bars on the held-out disjoint pairs -> the consumer-relative flip
  does not transfer to real legal-citation retrieval (an honest negative, like GO-P-2026-034 D4).
commitment: outcome reported regardless of sign in claims/LEDGER.md (GO-B-legal). No held-out pair is
  scored before this entry is sealed and committed.
hash: sha256:a386ca4507e6d490df2bcf985b60f34254859ebda683e39eabae3173cbb03268
```

## Falsification
A pass demonstrates the consumer-relative flip on a real, high-stakes, non-physical retrieval consumer
in a new content domain — reconstruction-optimal embedding compression is downstream-worse for legal
citation ranking than an anisotropy-aware read-preserving code at matched bits, while reconstructing the
embeddings better. A miss bounds the flip further. Sealed per REG-1 (CHARTER §4); the git commit is the
binding timestamp. The rate is frozen on calibration before any held-out pair is scored.
