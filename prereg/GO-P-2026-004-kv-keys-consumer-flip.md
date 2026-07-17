# GO-P-2026-004 — Consumer-projected error covariance governs downstream (GO-2 positive half)

Fourth registration on the KV-keys instance. v3 ([GO-P-2026-003]
(GO-P-2026-003-kv-keys-quotient-transfer-v3.md)) refuted the consumer-naive arm
labeling (NEG-7): at **fixed reconstruction** the a-vs-b ranking **flips** with
the consumer, and `tang_qproj` tracked the KL ranking perfectly while a linear
partial-R² could not resolve it. This entry registers the **mechanism** the v3
data pointed at and tests it with a **rank/flip** statistic in a **non-degenerate
softmax** regime. Fresh registration; no edits to prior entries. Governs
`experiments/go2_kv_keys_v4.py` and `results/GO2-kv-keys-v4.json`.

**Honesty flag:** `retrospective: true` (KV-keys instance, Paper II); class
ceiling `[replicated]`.

## Hypothesis (the mechanism)

For error δ = kr − k0 with across-token covariance Σ_δ = Cov_s(δ), and a consumer
whose queries have second-moment P_C (isotropic: P ∝ I; structured: projection
onto the top-r signal subspace), the softmax-downstream distortion is governed by
the **subspace-projected error variance** tr(P_C Σ_δ), relative to the signal's
tr(P_C Σ_0). Reconstruction is tr(Σ_δ) (P = I), **consumer-blind**. Therefore:

- **tang_qproj(C) = mean_{q∼C,h} Var_s(q·δ)/Var_s(q·k0)** estimates tr(P_C Σ_δ)/tr(P_C Σ_0)
  and must **rank-track softmax-KL under every consumer**;
- the a-vs-b ranking **flips** between the isotropic and structured consumers, and
  tang_qproj **flips identically**, while reconstruction (a single consumer-blind
  number) **cannot match both** — it mis-orders a,b under at least one consumer.

```yaml
id: GO-P-2026-004
date: 2026-07-17
retrospective: true
supersedes_test_of: GO-P-2026-003    # same claim (positive half); rank/flip statistic + non-degenerate regime
instance:
  representation: post-RoPE attention keys (per-head, per-channel), K in R^{H x S x D}
  consumers:
    iso: softmax over ISOTROPIC unit queries
    sub: softmax over STRUCTURED unit queries (top-16 singular subspace of demeaned keys/head)
  regime: per (seed,consumer) the query logits are rescaled by g = 1.5 / median_{q,h} std_s(q.k0)
          so the softmax is NON-DEGENERATE (target across-token logit std = 1.5,
          identical scaling for all arms -- an arm-independent consumer property).
  d_O: mean KL( softmax(g q.K0^T/sqrt(D)) || softmax(g q.Kr^T/sqrt(D)) ), held-out block.
  q_family: [demean_perchan_asym4, wholevec_pertoken_uniform4, polarquant_keys, perchan_uniform4]
probe_output:
  invariant: subspace-projected across-token error covariance tr(P_C Cov_s(delta))
  nuisance: total error tr(Cov_s(delta)) outside the consumer's read subspace + per-channel mean
  predicted_failure_class: dc-offset
prediction:
  mechanism: tr(P_C Sigma_delta) governs d_O; tang_qproj estimates it; recon = tr(Sigma_delta) is consumer-blind
  flip: median adv_KL(iso) > 0 AND median adv_KL(sub) < 0     # adv = log(KL_b / KL_a); a-vs-b ranking flips
  tang_tracks_flip: sign(median adv_tang(C)) == sign(median adv_KL(C)) for C in {iso,sub},
                    with per-seed sign agreement >= 10/12 in each consumer
  tang_ranks: median Spearman(tang_qproj_arms, KL_arms) >= 0.9 in BOTH consumers
  recon_fails: recon (fixed) mis-orders a,b under exactly one consumer, so
               min_C Spearman(recon_arms, KL_arms) < min_C Spearman(tang_qproj_arms, KL_arms)
  effect_floor:
    c_gap: median KL(c)/KL(a) >= 5 in BOTH consumers
design:
  n: 12 distribution seeds; each = fresh per-channel DC-offset + student-t(3) key regime,
     held-out block, 128 queries per consumer
  clusters: seed (naive + seed counts reported)
  stopping: fixed-n
  bits_matched_via: in-harness metadata-inclusive effective-bits audit (payload 4-bit +
    fp16 scalars per row/col; NO per-block codebook). Gate: spread <= 0.5 bit.
  nondegeneracy_gate: median max-softmax-prob >= 3/S in BOTH consumers (regime not near-uniform)
controls:
  - noise-floor: softmax-KL against the fp16-vs-fp16 rerun floor, per consumer.
  - covariance-projection corroboration (report, not gated): error-in-subspace fraction
    tr(P_sub Sigma_delta)/tr(Sigma_delta) for arm a vs b (expect a concentrates more in the read subspace).
amendments: []
hash: sha256:4fd21a97acbe184ddcc45eeae3a27d215b41bcfc1634561d1c9c94c5e9864c7f   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (this instance)

The positive half is **not supported** if any hold at n=12:
- effective-bits audit fails (spread > 0.5), or the non-degeneracy gate fails
  (median max-prob < 3/S in either consumer) — the regime is void; or
- the flip is absent (adv_KL does not change sign between consumers); or
- tang_qproj does not track the flip (per-seed sign agreement < 10/12 in either
  consumer) or does not rank-track KL (median Spearman < 0.9 in either consumer); or
- reconstruction ranks a,b as well as tang_qproj under both consumers
  (min_C Spearman(recon,KL) is not strictly < min_C Spearman(tang,KL)); or
- the anti-probe gap KL(c)/KL(a) < 5 in either consumer.

`GO2_positive_supported` requires: audit ∧ non-degeneracy ∧ c_gap(both) ∧
tang_ranks(both) ∧ flip ∧ tang_tracks_flip ∧ recon_fails. A pass gives GO-2's
positive half its first `[demonstrated]` on this instance (the consumer-projected
covariance mechanism); a miss is a `[refuted]`-leaning row that narrows it further.
