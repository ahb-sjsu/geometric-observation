# GO-P-2026-003 — Quotient-(A2) transfer on attention keys, v3 (GO-2 positive half)

Third registration on the KV-keys instance. v2 ([GO-P-2026-002]
(GO-P-2026-002-kv-keys-quotient-transfer-v2.md)) **demonstrated** GO-2's negative
half (at matched bits, reconstruction does not control downstream: a recon-identical
arm is 2.53× worse, anti-probe 21×) but **refuted my scalar for the positive half**
(NEG-6: the demeaned-error *norm* fails to order a<b — magnitude ≠ the
downstream-relevant *structure*), and its specificity controls were degenerate
under isotropic queries. This entry tests the positive half with the quantity the
v2 data pointed at, and a consumer for which specificity can bite.
Fresh registration; no edits to prior entries. Governs
`experiments/go2_kv_keys_v3.py` and `results/GO2-kv-keys-v3.json`.

**Honesty flag:** `retrospective: true` (KV-keys instance, Paper II); class
ceiling `[replicated]`. Corrected instance-1 run for the positive half.

## Design changes vs GO-P-2026-002

1. **Tangential quantity = query-projected across-token variance**, not a norm.
   For query q and reconstruction error δ = kr − k0, the softmax over tokens is
   shift-invariant, so the downstream-relevant perturbation is the **across-token
   variance of the logit kick** Var_s(q·δ_{h,s}), relative to the signal's own
   logit variance Var_s(q·k0_{h,s}), averaged over the query bank and heads. This
   is the quantity a magnitude scalar cannot see (NEG-6).
2. **Structured (non-isotropic) consumer.** Queries live in the top-r=16 singular
   directions of each head's clean keys (the dominant directions attention reads),
   not isotropic noise — so a shift-sensitive control can discriminate.
3. **Specificity via consumer shift-sensitivity, not query reshuffling.** The
   registered control is a **linear (shift-sensitive) readout** (relative MSE of
   the raw logits q·k, no softmax) on the same query bank. The a-vs-b advantage is
   claimed to be *specific to the softmax consumer's shift-invariance*: it must be
   present under softmax and **collapse** under the linear readout (where the two
   recon-equal arms are near-equal).

```yaml
id: GO-P-2026-003
date: 2026-07-17
retrospective: true
supersedes_test_of: GO-P-2026-002    # same claim (positive half), corrected metric+consumer
instance:
  representation: post-RoPE attention keys (per-head, per-channel), K in R^{H x S x D}
  consumer: softmax attention over a STRUCTURED query bank q (unit vectors in the
            top-16 singular subspace of each head's clean keys). d_O = mean
            KL( softmax(q.K0^T/sqrt(D)) || softmax(q.Kr^T/sqrt(D)) ), held-out block.
  q_family: [demean_perchan_asym4, wholevec_pertoken_uniform4, polarquant_keys, perchan_uniform4]
probe_output:
  invariant: the across-token (demeaned) key structure as READ by the consumer,
             i.e. the token-varying part of the logit q.k -- captured by
             Var_s(q.delta_s) (query-projected, across-token)
  nuisance: per-channel across-token mean (softmax shift) + per-vector norm/direction
  predicted_failure_class: dc-offset
prediction:
  arm_roles:
    a demean_perchan_asym4       : invariant-preserving (per-channel asym NF4)
    b wholevec_pertoken_uniform4 : recon-oriented, invariant-blind (per-token uniform)
    c polarquant_keys            : anti-probe (norm/direction; drops per-channel scale)
    d perchan_uniform4           : reference (per-channel uniform)
  downstream_ordering: a < d < b < c  on softmax-KL
  go2_dominance: in a joint standardized regression of softmax-KL on
    {tang_qproj = mean_{q,h} Var_s(q.delta)/Var_s(q.k0), reconstruction = rel ||delta||},
    over all FOUR arms x 12 seeds, tang_qproj's partial-R^2 exceeds reconstruction's,
    margin >= 0.10.
  specificity:                                    # advantage is softmax-shift-specific
    gap_softmax: median KL(b) / median KL(a) >= 1.5      # present under softmax
    gap_linear:  relMSE_logit(b) / relMSE_logit(a) <= 1.25   # collapses under shift-sensitive readout
  effect_floor:
    c_gap: median KL(c) / median KL(a) >= 5
    a_lt_b_seeds: KL(a) < KL(b) in >= 10 of 12 seeds
design:
  n: 12 distribution seeds; each = fresh per-channel DC-offset + student-t(3) key
     regime, held-out block, 128 structured-query bank (top-16 key subspace/head)
  clusters: seed (naive + seed-clustered)
  stopping: fixed-n
  bits_matched_via: in-harness metadata-inclusive effective-bits audit (payload
    4-bit + fp16 scalars per row/col; NO per-block codebook). Gate: spread <= 0.5 bit.
controls:
  - shift-sensitive (linear) consumer: relative MSE of raw logits q.k on the same
    structured bank; the a-vs-b gap must collapse (specificity, above).
  - noise-floor: softmax-KL against the fp16-vs-fp16 rerun floor.
  - isotropic-query cross-check: report softmax-KL under an isotropic bank too
    (bridge to v2; not gated).
amendments: []
hash: sha256:afcc7ac689d381b09ecd7e6d1c2a79b81866c540884e3d859c3767c6eac059d9   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (this instance)

GO-2's positive half is **not supported by this instance** if any hold at n=12,
clustered:
- the effective-bits audit fails (spread > 0.5 bit); or
- tang_qproj partial-R² − reconstruction partial-R² < 0.10 (query-projected
  variance no better than reconstruction); or
- the anti-probe gap KL(c)/KL(a) < 5; or
- KL(a) < KL(b) in fewer than 10/12 seeds; or
- specificity fails: the a-vs-b gap does not collapse under the shift-sensitive
  readout (gap_linear > 1.25) or is absent under softmax (gap_softmax < 1.5).

`GO2_supported` (this instance, positive half) requires: audit ∧ dominance ∧
c_gap ∧ a<b ∧ specificity. A miss is a `[refuted]`-leaning ledger row; a pass
gives GO-2's positive half its first `[demonstrated]` on this instance.
