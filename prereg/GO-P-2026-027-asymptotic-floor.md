# GO-P-2026-027 — The omission floor bites downstream on trained Llama read operators (asymptotic)

**Prospective** (retrospective:false), **out-of-sample**. Promotes GO-P-2026-026's
*exploratory* finding — that Appendix-E's omission distortion floor manifests downstream, as
an asymptotic (infinite read-rate) phenomenon — to a sealed, held-out confirmation.
Governs `experiments/gateB_llama_asymptotic_floor.py`. **Runs on Atlas GPU 1.**

**Honesty note on informed design.** The gate and bars below were calibrated on
GO-P-2026-026's exploratory follow-up (layers {8,16}, which saw asymptotic ratios ~1e5). To
keep this a genuine prospective test rather than a replay, it is run on **HELD-OUT layers
{4,20}** with a **different text corpus**. A pass is therefore a generalization to unseen
heads/layers, not a re-measurement of the calibration set.

**Claim.** For a trained Llama-3.2-3B read operator $P=\E[qq^\top]$ per KV head and a
rank-$16$ misidentified operator $\hat P$ (truncation to $P$'s top-16 subspace), the
infinite-read-rate error is confined to the whitened kernel $\Pi=\ker(\Sigma_x^{1/2}\hat
P\Sigma_x^{1/2})$ with covariance $\Sigma_x^{1/2}\Pi\Sigma_x^{1/2}$, and the resulting
downstream softmax-KL is a large multiple of the matched operator's (which $\to0$ at high
rate). The read-metric floor $\tr(\tilde P\Pi)$ is also reached under deep $\hat P$
water-filling.

```yaml
id: GO-P-2026-027
date: 2026-07-18
retrospective: false
kind: prospective operational confirmation (real trained model; Atlas GPU 1); out-of-sample vs GO-P-2026-026
informed_by: GO-P-2026-026 exploratory follow-up (layers {8,16}); bars calibrated there, run held-out on {4,20}
requires: Atlas GPU 1 (CUDA_VISIBLE_DEVICES=1), unsloth/Llama-3.2-3B, run by the user or session
harness: experiments/gateB_llama_asymptotic_floor.py
claim: "On held-out Llama layers {4,20}, the omission floor manifests downstream: asymptotic misidentified softmax-KL >> matched, and the read-metric floor is reached."
prediction:
  read_floor_reached: deep P_hat water-fill drives tr(P Sigma_delta) to tr(P~ Pi) on >= 14/16 heads (within a factor 2)
  downstream_floor: >= 14/16 heads have kl_floor/kl_matched >= 100 AND kl_floor >= 0.01 nats, and the MEDIAN ratio >= 100
falsification: fewer than 14/16 heads clearing the downstream bar, or median ratio < 100, or the read-metric
  floor not reached on >= 14/16 heads -> the downstream floor does not generalize; recorded as an honest negative.
verification:
  - sealed + committed BEFORE the run (binding = git commit timestamp).
  - out-of-sample layers {4,20} (GO-P-2026-026 exploratory used {8,16}); different corpus.
  - the theorem (Appendix E) is proved; this confirms its DOWNSTREAM operational relevance on a trained model.
amendments: []
hash: sha256:f172de2f283bea2a4b776a74a3344cca07599ac09a332893c97b85addc1a6893
```

## Falsification
The read-metric floor is a theorem (GO-P-2026-024, fresh-context passed). What is prospective
here is whether the floor's downstream manifestation, seen exploratorily on {8,16}, generalizes
out-of-sample to {4,20}. If it does not clear the sealed bars it is recorded as an honest
negative; if it does, Appendix-E's omission floor is `[demonstrated]` downstream on a trained model.
