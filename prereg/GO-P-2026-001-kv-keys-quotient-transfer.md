# GO-P-2026-001 — Quotient-(A2) transfer on attention keys (GO-2, known instance)

Registers the design and bars for the GO-2 test on the KV-attention-keys
instance — the workhorse three-arm design (§3) plus the (i)-dominates-(ii)
regression (§2, GO-2). Governs `experiments/go2_kv_keys.py` and
`results/GO2-kv-keys.json`.

**Honesty flag:** `retrospective: true`. The KV-keys data was already observed in
Paper II, so this is **not** an ex-ante prediction. It supplies **one of the ≥2
independent settings** GO-2 needs for `[replicated]`, and locks the specific
regression design + bars in advance of *this* harness's run. The truly
`[predicted]` (ex-ante, blinded) GO-2 evidence is the Gate B out-of-sample
instance (§4), registered separately.

```yaml
id: GO-P-2026-001
date: 2026-07-17          # predates this harness's first measurement
retrospective: true       # known instance (Paper II); class ceiling = [replicated]
instance:
  representation: post-RoPE attention keys (per-head, per-channel), K in R^{H x S x D}
  consumer: softmax attention. d_O measured as the mean KL( softmax(q.K0^T/sqrt(D))
            || softmax(q.Kq^T/sqrt(D)) ) over a fixed bank of random unit queries
            q, on a held-out block. Never reconstruction cosine.
  q_family: [asym_nf4_2pct, perchannel_lloyd_nuq, uniform_perchannel, polarquant_keys]
probe_output:
  invariant: per-channel scale + per-channel DC offset (the affine structure the
             softmax logit q.k depends on channel-by-channel)
  nuisance: per-vector L2 norm + direction (the polar quotient) -- what a
            norm-then-quantize-direction scheme preserves
  predicted_failure_class: dc-offset            # per-channel offset/scale discarded
prediction:
  arm_ordering: a > b > c on softmax-KL   # a=invariant-preserving, b=recon-optimal, c=anti-probe
  # arms:
  #   a invariant-preserving   = asym_nf4_2pct     (per-channel zero-point + NF4 + 2% fp16 outliers)
  #   b reconstruction-optimal = perchannel_lloyd_nuq (per-channel Lloyd-Max; min ||x-Q(x)|| at matched bits)
  #   c anti-probe control     = polarquant_keys   (per-vector normalize: keeps norm/direction, drops per-channel scale)
  go2_dominance: in a joint regression of softmax-KL on {quotient-tangential
    distortion, reconstruction distortion} across all four variants x seeds, the
    tangential term's standardized |coef| exceeds reconstruction's, and its
    partial-R^2 is the larger.
  effect_floor:
    a_vs_b: median softmax-KL(b) / median softmax-KL(a) >= 1.10   # recon-optimal >=10% worse
    c_gap:  median softmax-KL(c) / median softmax-KL(a) >= 5      # anti-probe catastrophic
    dominance: tangential partial-R^2 - reconstruction partial-R^2 >= 0.10
design:
  n: 12 distribution seeds (independent unit); each seed = a fresh per-channel
     DC-offset + heavy-tailed key regime, held-out block, 128-query bank
  clusters: seed (cluster the CI over the 12 seeds; report naive + clustered;
            <8-cluster caveat N/A at 12, wild-cluster bootstrap where feasible)
  stopping: fixed-n           # no optional stopping
  bits_matched_via: in-library 4-bit accounting; external llama.cpp-style audit = PENDING (logged as a gap)
controls:
  - shuffled-consumer: re-run the invariant/nuisance split against a permuted
    query bank / a synthetic consumer whose sensitive directions are rotated;
    the per-channel-scale split must NOT transfer (specificity).
  - noise-floor: report softmax-KL against the fp16-vs-fp16 rerun floor.
amendments: []
hash: sha256:f0828efc7418a94633fed3a7d57e04589e350305b8590dc6b5e50b93680a9285   # filled by scripts/seal.py after write; git commit is the binding timestamp
```

## Falsification (this instance)

GO-2 is **not supported by this instance** if any hold at registered n, clustered:
- the ordering reverses a vs c (recon/anti-probe not worse than invariant), or
- reconstruction distortion predicts softmax-KL at least as well as tangential
  distortion (its partial-R² ≥ tangential's), or
- the shuffled-consumer control returns the same per-channel-scale split (the
  probe "explains" a consumer that isn't there).

A miss here is a `[refuted]`-leaning row in the ledger and, combined with a
second-instance miss, refutes GO-2 as `[replicated]`.
