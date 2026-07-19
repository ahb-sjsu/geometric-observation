# GO-P-2026-036 — Legal-retrieval flip rehabilitation via the GO-1 blind-probe read operator

Honest rehabilitation of the `GO-P-2026-035` negative. That miss had a genuine, diagnosable flaw: the
read operator was the **estimated centered doc covariance**, which overfit the calibration document
sample and did not transfer (on held-out, reconstruction-optimal beat read-preserving). This entry
fixes exactly that flaw — the `032 → 033` pattern — using the **GO-1 blind-probe** read operator
(`GO-P-2026-011`): recover what the ranking *consumer* is actually sensitive to, black-box, instead of
guessing it from the document variance.

## The fix
- **GO-1 blind-probe read operator.** For cosine ranking the margin sensitivity is
  `∂cos(a,b)/∂b ≈ â − cos(a,b)·b̂` — the query component **orthogonal to the doc**. This automatically
  strips the anisotropy (it lives in the subtracted `cos·b̂` term) and is tied to the ranking **task**,
  not the doc-sample variance. The read operator is `S = mean_i g_i g_iᵀ`, `g_i = â_i − cos(a_i,b_i)·b̂_i`.
- **Low-rank (r) for robustness.** Protect only the **top-r** sensitivity directions — a low-rank read
  subspace transfers where a full-rank covariance overfit.
- **Internal-split selection (anti-overfit guard).** `r` and the rate were selected by fitting the read
  operator on **cal-A** (first 2000 calibration pairs) and scoring the flip on **DISJOINT cal-B** (last
  2000) — so only a config that already **generalises out-of-fit once** is sealed. Chosen config on
  cal-B (disjoint from the fit): AUROC **R=0.765 > O=0.755**, recon **O=0.222 ≤ R=0.564**, flip
  **200/200**, anti **200/200**, recon-trade true.
- Everything else is unchanged from `035`: same corpus, LaBSE embeddings, citation-AUROC consumer, three
  matched-bit arms (O recon-optimal by raw variance / R read-preserving by blind sensitivity / A anti),
  quantised in the doc semantic eigenbasis. For the held-out confirm the read operator is fit on **all**
  calibration and applied unchanged to the held-out disjoint opinions.

```yaml
id: GO-P-2026-036
date: 2026-07-19
retrospective: false
kind: sealed rehabilitation of GO-P-2026-035 (blind-probe read operator; internal-split-selected)
rehab_of: GO-P-2026-035
read_operator: GO-1 blind margin-sensitivity S=mean g g^T, g=a_hat - cos(a,b) b_hat; top-r low-rank
fix: estimated-covariance read op overfit -> blind-recovered, task-tied, low-rank, internal-split-selected
data: CourtListener (citing,cited) pairs; calibration = pairs_train (n=4000); heldout = pairs_eval
  (n=1293, disjoint opinions id%10==7)
frozen_config: {r: 32, base_bits: 0.4, quantizer: semantic-eigenbasis scalar, fixed per-direction range}
internal_split_result_cal_B: {auroc_R: 0.765, auroc_O: 0.755, auroc_A: 0.688, recon_O: 0.222,
  recon_R: 0.564, flip: 200/200, anti: 200/200, recon_trade: true}
prediction:
  on the held-out disjoint pairs at the frozen (r=32, bits=0.4): clean flip AUROC(R) >= AUROC(O) on
  >= 60% bootstraps; recon-trade recon(O) <= recon(R); anti worst on >= 70% bootstraps; and
  read-preserving beats reconstruction-optimal on the full-set AUROC.
falsification: the flip FAILS on the held-out -> even the blind-recovered read operator does not
  transfer, and the flip on real learned reps is bounded to planted/known read subspaces (035 stands).
commitment: outcome reported regardless of sign in claims/LEDGER.md (GO-B-legal). No held-out pair is
  scored before this entry is sealed and committed.
hash: sha256:84dfad567afaa6596d06de72bd660caf9db3c62995793bdaa80b9725af91e16e
```

## Falsification
A pass shows the consumer-relative flip DOES transfer to real legal-citation retrieval once the read
operator is **recovered blind from the consumer** (GO-1) rather than estimated from the signal — turning
the `035` negative into a demonstration that the earlier miss was a read-operator-identifiability
failure, not a failure of the flip. A miss bounds the flip to planted/known read subspaces. Sealed per
REG-1; the git commit is the binding timestamp; the config is frozen (and already generalised on the
internal split) before any held-out pair is scored.
