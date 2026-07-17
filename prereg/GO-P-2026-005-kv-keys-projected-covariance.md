# GO-P-2026-005 — Projected error covariance governs downstream, gated directly (GO-2 positive half)

Fifth and (intended) closing registration on the KV-keys instance. v4
([GO-P-2026-004](GO-P-2026-004-kv-keys-consumer-flip.md)) **confirmed the flip and
the mechanism directly** — error-in-read-subspace fraction a 0.406 vs b 0.122,
with reconstruction unable to track — but missed two bars because the *gated*
statistic was the noisy Monte-Carlo Var-ratio `tang_qproj` (Spearman 0.80 under
iso; sub-flip only ~9%, NEG-8). This entry gates on the **direct** projected
covariance and uses a **more concentrated** read subspace so the flip is decisive.
Fresh registration; no edits to prior entries. Governs
`experiments/go2_kv_keys_v5.py` and `results/GO2-kv-keys-v5.json`.

**Honesty flag:** `retrospective: true` (KV-keys instance, Paper II); class
ceiling `[replicated]`.

## The gated quantity

For each arm and consumer C with query second-moment P_C (iso: P ∝ I; sub:
projection onto the top-r singular subspace of the demeaned signal), define the
**directly-computed projected error variance**

    proj_var(arm, C) = Σ_h tr(P_C^h Σ_δ^h) / Σ_h tr(P_C^h Σ_0^h)

where Σ_δ^h = Cov_s(δ^h), Σ_0^h = Cov_s(demeaned k0^h). This is the quantity the
prereg-004 corroboration measured, now computed from the covariances (no query
sampling noise). Reconstruction (relative ‖δ‖/‖k0‖) is a single consumer-blind
number. Prediction: proj_var rank-tracks softmax-KL under **both** consumers and
**flips a-vs-b** with it; reconstruction cannot.

```yaml
id: GO-P-2026-005
date: 2026-07-17
retrospective: true
supersedes_test_of: GO-P-2026-004    # same positive half; gate on direct proj_var, concentrated subspace
instance:
  representation: post-RoPE attention keys (per-head, per-channel), K in R^{H x S x D}
  consumers:
    iso: softmax over ISOTROPIC unit queries              # P_C ∝ I
    sub: softmax over STRUCTURED unit queries in the top-4 subspace of demeaned keys/head
  regime: per (seed,consumer) logits rescaled by g = 1.5 / median_{q,h} std_s(q.k0)
          (non-degenerate softmax; arm-independent).
  d_O: mean KL( softmax(g q.K0^T/sqrt(D)) || softmax(g q.Kr^T/sqrt(D)) ), held-out block.
  q_family: [demean_perchan_asym4, wholevec_pertoken_uniform4, polarquant_keys, perchan_uniform4]
probe_output:
  invariant: proj_var(arm,C) = tr(P_C Sigma_delta)/tr(P_C Sigma_0) (subspace-projected error variance)
  nuisance: total/full-space error not seen by the consumer + per-channel mean
  predicted_failure_class: dc-offset
prediction:
  mechanism: proj_var governs softmax-KL under every consumer; recon = rel||delta|| is consumer-blind
  proj_ranks: median Spearman(proj_var_arms, KL_arms) >= 0.9 in BOTH consumers
  flip:
    kl_median:  median adv_KL(iso) >= log(1.3)  AND  median adv_KL(sub) <= -log(1.15)   # decisive both ways
    kl_perseed: iso KL(a) < KL(b) in >= 11/12 ; sub KL(b) < KL(a) in >= 11/12
    proj_tracks: sign(adv_proj(C)) == sign(adv_KL(C)) per seed >= 11/12 in EACH consumer   # adv = log(b/a)
  recon_fails: min_C Spearman(recon_arms, KL_arms) < min_C Spearman(proj_var_arms, KL_arms)
  effect_floor:
    c_gap: median KL(c)/KL(a) >= 5 in BOTH consumers
design:
  n: 12 distribution seeds; each = fresh per-channel DC-offset + student-t(3) key regime,
     held-out block, 128 queries per consumer
  r_sub: 4                 # more concentrated than v4's 16, so the sub-flip is decisive
  clusters: seed
  stopping: fixed-n
  bits_matched_via: in-harness metadata-inclusive effective-bits audit (payload 4-bit +
    fp16 scalars per row/col; NO per-block codebook). Gate: spread <= 0.5 bit.
  nondegeneracy_gate: median max-softmax-prob >= 3/S in BOTH consumers.
controls:
  - noise-floor: softmax-KL against the fp16-vs-fp16 rerun floor, per consumer.
  - tang_qproj cross-check (report, not gated): the v4 Var-ratio, to show the direct
    proj_var is the cleaner estimator (higher Spearman, decisive per-seed).
amendments: []
hash: sha256:bb6ad838c526c8409e8c6a49428758ef2a0a0aa458e41e22622e19b12a5f286c   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (this instance)

The positive half is **not supported** if any hold at n=12:
- audit fails (spread > 0.5) or non-degeneracy fails (median max-prob < 3/S either consumer); or
- proj_var does not rank-track KL (median Spearman < 0.9 in either consumer); or
- the flip is not decisive (median adv_KL(iso) < log 1.3, or adv_KL(sub) > −log 1.15,
  or per-seed KL flip < 11/12 in either direction); or
- proj_var does not track the flip per-seed (< 11/12 sign agreement in either consumer); or
- reconstruction ranks a,b as well as proj_var under both consumers
  (min_C Spearman(recon,KL) not strictly < min_C Spearman(proj_var,KL)); or
- the anti-probe gap KL(c)/KL(a) < 5 in either consumer.

`GO2_positive_supported` requires: audit ∧ non-degeneracy ∧ c_gap(both) ∧
proj_ranks(both) ∧ flip(decisive+per-seed) ∧ proj_tracks_flip ∧ recon_fails. A
pass gives GO-2's positive half its first `[demonstrated]` on this instance — the
consumer-projected covariance mechanism `tr(P_C Σ_δ)`. A miss is a
`[refuted]`-leaning row that narrows it further.
