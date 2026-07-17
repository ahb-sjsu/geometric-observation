# GO-P-2026-002 — Quotient-(A2) transfer on attention keys, v2 (GO-2, bit-matched redesign)

Corrects [GO-P-2026-001](GO-P-2026-001-kv-keys-quotient-transfer.md), which
missed as registered (see `../experiments/GO2-kv-keys-NOTES.md`, ledger NEG-5)
for two reasons: (1) the reconstruction-optimal arm stored an **uncounted
per-block codebook** — a matched-bits violation the §3.5 audit is meant to catch;
(2) the dominance regression was dominated by a lone anti-probe outlier that
*both* predictors fit. This entry fixes both and sharpens the GO-2 test.
No post-hoc edits are made to GO-P-2026-001; this is a fresh registration.
Governs `experiments/go2_kv_keys_v2.py` and `results/GO2-kv-keys-v2.json`.

**Honesty flag:** `retrospective: true` (KV-keys instance seen in Paper II);
class ceiling `[replicated]`. This is the corrected instance-1 run.

## Design changes vs GO-P-2026-001

1. **Matched-bits, no codebook tables.** Every arm stores 4-bit payload +
   O(1) fp16 metadata per row *or* column (never a per-block level table). A
   metadata-inclusive **effective-bits audit** is a registered gate: all arms
   must land within 0.5 bit of each other.
2. **The dissociation is populated, not a lone outlier.** A second
   invariant-blind arm (whole-vector per-token uniform) is added alongside the
   anti-probe, so the regression sees *multiple* points where reconstruction and
   tangential distortion disagree — reconstruction moderate, tangential high,
   downstream bad. The dominance test is no longer carried by one outlier.
3. **Fair `a`-vs-`b` clause.** Because a per-channel invariant-preserving
   quantizer tends to Pareto-dominate on this instance (demeaning is a free,
   orthogonal reconstruction gain), we do **not** demand the recon-optimal arm
   reconstruct *strictly better*. We demand it be **downstream-worse while
   reconstruction stays comparable** — i.e. reconstruction fails to explain the
   downstream gap.

```yaml
id: GO-P-2026-002
date: 2026-07-17
retrospective: true
supersedes_test_of: GO-P-2026-001   # same claim, corrected design; NOT an amendment
instance:
  representation: post-RoPE attention keys (per-head, per-channel), K in R^{H x S x D}
  consumer: softmax attention. d_O = mean KL( softmax(q.K0^T/sqrt(D))
            || softmax(q.Kq^T/sqrt(D)) ) over a fixed bank of random unit queries q,
            on a held-out block. Never reconstruction cosine.
  q_family: [demean_perchan_asym4, wholevec_pertoken_uniform4, polarquant_keys, perchan_uniform4]
probe_output:
  invariant: per-channel token-varying structure (the per-(head,channel) signal
             AFTER removing its across-token mean) -- this is what the softmax
             logit q.k discriminates on
  nuisance: (i) per-channel across-token mean  [softmax logit shift = constant over
            tokens => shift-invariant], and (ii) per-vector L2 norm + direction
            (the polar quotient) -- what norm-then-quantize-direction preserves
  predicted_failure_class: dc-offset            # bits spent on the nuisance mean / cross-channel magnitude
prediction:
  arm_roles:
    a demean_perchan_asym4     : invariant-preserving  (demean per channel, 4-bit asym on residual)
    b wholevec_pertoken_uniform4 : reconstruction-oriented but invariant-blind
                                   (per-token min-max uniform 4-bit across the D channels)
    c polarquant_keys          : anti-probe (per-vector normalize; keeps norm/direction, drops per-channel scale)
    d perchan_uniform4         : reference (per-channel uniform 4-bit)
  downstream_ordering: a < d < b < c  on softmax-KL     # invariant-preserving best; anti-probe worst
  go2_dominance: in a joint standardized regression of softmax-KL on
    {quotient-tangential distortion, reconstruction distortion} across ALL FOUR
    arms x 12 seeds, tangential's partial-R^2 exceeds reconstruction's, margin >= 0.10.
  recon_does_not_explain_gap:                            # fair a-vs-b clause
    kl_gap:   median KL(b) / median KL(a) >= 1.10        # b clearly downstream-worse
    recon_comparable: median recon(b) / median recon(a) <= 1.25   # while recon is NOT the story
  effect_floor:
    c_gap: median KL(c) / median KL(a) >= 5              # anti-probe catastrophic (retained)
    a_lt_b_seeds: KL(a) < KL(b) in >= 10 of 12 seeds     # clustered ordering consistency
design:
  n: 12 distribution seeds (independent unit); each = fresh per-channel DC-offset +
     heavy-tailed (student-t(3)) key regime, held-out block, 128 random-unit-query bank
  clusters: seed (report naive + seed-clustered; wild-cluster bootstrap where feasible)
  stopping: fixed-n
  bits_matched_via: metadata-inclusive effective-bits audit computed IN-HARNESS
    (payload 4-bit + fp16 scalars per row/col; NO per-block codebook). Registered
    gate: max_arm_effective_bits - min_arm_effective_bits <= 0.5 bit.
controls:
  - shuffled-consumer: re-run softmax-KL against a PERMUTED query bank (queries
    shuffled across heads). The a-vs-b downstream gap must shrink toward 1
    (specificity: the invariant advantage is tied to the real consumer).
  - noise-floor: report softmax-KL against the fp16-vs-fp16 rerun floor.
amendments: []
hash: sha256:a9a7ed5dddb791aef64560f675324f99e41bd33fc38bf81744f85e4db5d1342e   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (this instance)

GO-2 is **not supported by this corrected instance** if any hold at n=12, clustered:
- the effective-bits audit fails (arms differ by > 0.5 bit) — the comparison is void; or
- reconstruction distortion predicts softmax-KL at least as well as tangential
  (tangential partial-R² − reconstruction partial-R² < 0.10); or
- the anti-probe gap KL(c)/KL(a) < 5; or
- KL(a) < KL(b) in fewer than 10/12 seeds; or
- the shuffled-consumer control reproduces the a-vs-b gap (the probe "explains" a
  consumer that isn't there).

`GO2_supported` (this instance) requires: audit-pass AND dominance AND c_gap AND
a<b-consistency. The `recon_does_not_explain_gap` clause is reported as
corroborating evidence. A miss is a `[refuted]`-leaning ledger row; combined with
a second-instance miss it refutes GO-2 as `[replicated]`.
