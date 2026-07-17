# GO-P-2026-009 — GO-2 instance 2' clean close, well-specified gate (PROSPECTIVE)

Clean re-run of GO-P-2026-008, which demonstrated the mechanism in substance
(total flip at identical reconstruction; proj_var tracks 12/12; recon blind) but
whose registered flag was False on a **mis-specified SNR gate**: it read
`min-arm dO ≥ 10× floor`, and the "blind" arm's dO was *exactly 0* (error
orthogonal to the consumer) — the strongest form of consumer-blindness, wrongly
rejected. This entry fixes the gate (gate the **loser's** distortion) and injects
a small isotropic component so the flip is decisive **but non-degenerate**. Fixes
the gate, not the claim — the four substantive gates already passed 12/12. Fresh
registration; no edits to prior entries. Governs
`experiments/go2_retrieval_matched_v2.py` and
`results/GO2-retrieval-matched-v2.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE** (new injection design; never
run). Controlled matched-distortion probes, as in GO-P-2026-008 (§3-style).

## Changes vs GO-P-2026-008

1. **Injection is a mix:** δ_i = ε_i · (√(1−η)·s_i + √η·g_i) with η=0.1, s_i unit in
   the target subspace, g_i unit in its **orthogonal complement**. Then ‖δ_i‖ = ε_i
   exactly (recon identical, matched), 90% of the error energy sits in the target
   subspace, 10% leaks isotropically — so the "blind" arm's downstream dO is small
   but **nonzero** (no exact zeros), and more realistic than perfect orthogonality.
2. **SNR gate fixed:** require the **loser's** dO (the distorted arm under each
   consumer) ≥ 10× the fp16 floor — the well-specified non-degeneracy (the visible
   distortion is real), instead of the min arm (which is the *winner*, ~0 by design).

```yaml
id: GO-P-2026-009
date: 2026-07-17
retrospective: false
supersedes_test_of: GO-P-2026-008    # same claim; fixed SNR gate + non-degenerate injection
instance: 2-prime
representation: low-rank embeddings E in R^{N x D} (as GO-P-2026-007/008)
consumer: inner-product retrieval ranking. d_O = mean over queries of
          (1 - Spearman(true_scores, recon_scores)) over the N-item corpus.
probes:
  a_err_in_A: eps_i error, 90% in S_A=span(V[:8]) + 10% in complement(S_A)
  b_err_in_B: eps_i error, 90% in S_B=span(V[8:16]) + 10% in complement(S_B)
  c_polar_antiprobe: real per-item polar anti-probe (context)
  d_periitem_uniform4: real per-item uniform 4-bit (sets eps; matched to a,b)
consumers_probed: {read_A: queries in S_A, read_B: queries in S_B, iso: isotropic (diagnostic)}
eta: 0.1                       # isotropic-complement energy fraction of the injected error
probe_output:
  invariant: overlap of the error covariance with the consumer's read subspace, tr(P_C Σ_δ)
  nuisance: total error magnitude (identical across a,b,d) + error outside the read subspace
  predicted_failure_class: subspace-mismatch
prediction:
  mechanism: proj_var governs ranking distortion; reconstruction (identical for a,b,d) cannot
  flip_decisive:                                    # adv = log(dO_b / dO_a)
    dO_median: median adv_dO(read_A) <= -log(1.3)  AND  median adv_dO(read_B) >= log(1.3)
    dO_perseed: read_A dO(a) > dO(b) in >= 10/12  AND  read_B dO(b) > dO(a) in >= 10/12
  proj_tracks_flip: sign(adv_proj(C)) == sign(adv_dO(C)) per seed >= 11/12 for C in {read_A, read_B}
  recon_fails: min_C Spearman(recon_arms, dO_arms) < min_C Spearman(proj_var_arms, dO_arms)
design:
  n: 12 corpus seeds; N=1024 items; D=128; 128 queries per consumer; r=8 per subspace
  clusters: seed
  stopping: fixed-n
  matched_distortion_gate: |median recon(a) - median recon(b)| / median recon(a) <= 0.02
  snr_gate: min over {read_A, read_B} of the LOSER's median dO ( = max(dO(a),dO(b)) )
            >= 10 x the fp16-vs-fp16 rerun floor
gated: [matched_distortion, snr_loser, flip_decisive, proj_tracks_flip, recon_fails]
diagnostics_reported_not_gated:
  - winner_dO: the blind arm's median dO (expect small but > 0 with eta=0.1)
  - iso_consumer: median adv_dO(iso) (expect ~ 0)
  - anti_probe_gap, full_rank_spearman per consumer
controls:
  - noise-floor: d_O against the fp16-vs-fp16 rerun, per consumer.
amendments: []
hash: sha256:0c91db9e8b6023d84fe8c4cc16c65f7159b2d39cd07996597c8baad17e41c401   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (instance 2', clean, prospective)

Fails if any hold at n=12: matched-distortion gate fails (>2%); the loser's dO is
not ≥ 10× floor in either consumer (signal not real); the flip is not decisive
(median adv_dO(read_A) > −log1.3, or read_B < log1.3, or per-seed < 10/12 either
direction); proj_var does not track the flip (< 11/12 either consumer);
reconstruction tracks a,b as well as proj_var.

`GO2_mechanism_replicates` requires all five gated conditions. A pass makes GO-2's
mechanism `[replicated]` — 2 independent instances (softmax attention + retrieval
ranking), in the recon-matched regime NEG-10 delimits, under a well-specified gate.
