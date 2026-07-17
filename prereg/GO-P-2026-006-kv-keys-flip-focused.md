# GO-P-2026-006 — The consumer flip, gated exactly (GO-2 positive half, instance-1 closer)

Sixth and closing registration on the KV-keys instance. v5
([GO-P-2026-005](GO-P-2026-005-kv-keys-projected-covariance.md)) showed the core
mechanism **decisively** — a symmetric 12/12 a-vs-b flip, `proj_var` tracking the
KL sign 12/12 in both consumers, reconstruction unable to track — but the
registered *conjunction* missed on two **secondary** gates: an anti-probe control
that fights the concentration the flip needs, and a full-4-arm rank ask that trips
on a *middle* pair (NEG-9), neither of which is the positive-half claim.

This entry **scopes the registered conjunction to exactly GO-2's positive-half
claim**: the a-vs-b *flip* is governed by the consumer-projected covariance and
**not** by reconstruction. The anti-probe gap and the full-4-arm Spearman are kept
as **reported diagnostics**, not gates — the anti-probe is a *negative-half*
control (already `[demonstrated]`), and NEG-9 established the trace is not a
complete rank statistic. This is a precision of scope, not a loosening: the flip
statistics already passed at 12/12 in v5, and the demoted quantities are still
computed and reported in full. Fresh registration; no edits to prior entries.
Governs `experiments/go2_kv_keys_v6.py` and `results/GO2-kv-keys-v6.json`.

**Honesty flag:** `retrospective: true` (KV-keys instance, Paper II); class
ceiling `[replicated]`. A pass gives GO-2's positive half its first
`[demonstrated]` on **instance 1 only**; `[replicated]` still requires a second
independent instance (a Gate-B representation), registered separately.

```yaml
id: GO-P-2026-006
date: 2026-07-17
retrospective: true
supersedes_test_of: GO-P-2026-005    # same positive half; conjunction scoped to the flip
instance:
  representation: post-RoPE attention keys (per-head, per-channel), K in R^{H x S x D}
  consumers:
    iso: softmax over ISOTROPIC unit queries
    sub: softmax over STRUCTURED unit queries in the top-8 subspace of demeaned keys/head
  regime: per (seed,consumer) logits rescaled by g = 1.5 / median_{q,h} std_s(q.k0) (non-degenerate).
  d_O: mean KL( softmax(g q.K0^T/sqrt(D)) || softmax(g q.Kr^T/sqrt(D)) ), held-out block.
  q_family: [demean_perchan_asym4, wholevec_pertoken_uniform4, polarquant_keys, perchan_uniform4]
claim_scope: >
  GO-2 positive half = the DISCRIMINATING a-vs-b comparison flips with the consumer
  and is governed by proj_var = tr(P_C Sigma_delta)/tr(P_C Sigma_0), while
  reconstruction (consumer-blind) cannot track it. Anti-probe gap and full-4-arm
  rank are diagnostics, not part of this claim.
prediction:
  flip_decisive:
    kl_median:  median adv_KL(iso) >= log(1.3)  AND  median adv_KL(sub) <= -log(1.15)   # adv = log(KL_b/KL_a)
    kl_perseed: iso KL(a) < KL(b) in >= 10/12  AND  sub KL(b) < KL(a) in >= 10/12
  proj_tracks_flip: sign(adv_proj(C)) == sign(adv_KL(C)) per seed >= 11/12 in EACH consumer
  recon_fails: min_C Spearman(recon_arms, KL_arms) < min_C Spearman(proj_var_arms, KL_arms)
design:
  n: 12 distribution seeds; held-out block; 128 queries per consumer
  r_sub: 8                 # intermediate: decisive flip AND anti-probe diagnostic naturally >= 5
  clusters: seed
  stopping: fixed-n
  bits_matched_via: in-harness metadata-inclusive effective-bits audit (payload 4-bit +
    fp16 scalars per row/col; NO per-block codebook). Gate: spread <= 0.5 bit.
  nondegeneracy_gate: median max-softmax-prob >= 3/S in BOTH consumers.
gated: [audit, nondegeneracy, flip_decisive, proj_tracks_flip, recon_fails]
diagnostics_reported_not_gated:
  - anti_probe_gap: median KL(c)/KL(a) per consumer (expect iso >> 5, sub >= 5 at r=8)
  - full_rank_spearman: Spearman(proj_var, KL) and Spearman(recon, KL) per consumer (NEG-9 context)
  - tang_qproj_crosscheck: the v4 Var-ratio, to contrast with the direct proj_var
controls:
  - noise-floor: softmax-KL against the fp16-vs-fp16 rerun floor, per consumer.
amendments: []
hash: sha256:553035ce97b77da5b2da6c9abe555f3dac8551a5b58b732ae2ce4825055a1995   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (this instance, positive half)

Not supported if any hold at n=12:
- audit fails (spread > 0.5) or non-degeneracy fails (median max-prob < 3/S either consumer); or
- the flip is not decisive (median adv_KL(iso) < log1.3, or adv_KL(sub) > −log1.15,
  or per-seed KL flip < 10/12 in either direction); or
- proj_var does not track the flip per-seed (< 11/12 in either consumer); or
- reconstruction tracks a,b as well as proj_var (min_C Spearman(recon,KL) not strictly
  < min_C Spearman(proj_var,KL)).

`GO2_positive_supported` requires all five gated conditions. A pass = GO-2 positive
half `[demonstrated]`, instance 1. The diagnostics are reported for completeness
and to keep NEG-9 (trace ≠ complete rank statistic) in view; they do not gate.
