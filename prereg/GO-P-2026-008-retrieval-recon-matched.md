# GO-P-2026-008 — GO-2 instance 2', retrieval with reconstruction-matched probes (PROSPECTIVE)

Re-attempt of the instance-2 (retrieval) replication in the regime NEG-10
identified: the reconstruction-blind flip is observable **only when the compared
arms are reconstruction-matched**. GO-P-2026-007 missed because a real per-item
quantizer Pareto-dominated on reconstruction, leaving no dissociation. This entry
constructs the matched regime deliberately with **matched-distortion controlled
probes** and tests whether the flip + proj_var-tracking + reconstruction-blindness
replicates in retrieval ranking. Fresh registration; no edits to prior entries.
Governs `experiments/go2_retrieval_matched.py` and
`results/GO2-retrieval-matched.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE.** Never run; prediction
locked pre-measurement. The probes are **controlled** (matched-magnitude error
placed in a designated subspace — like the anti-probe, a §3 constructed probe),
not deployment compressors; the *real*-compressor emergent flip is instance 1's
contribution. The falsifiable content here is whether the **nonlinear retrieval
ranking** actually follows `proj_var` when reconstruction is held identical.

## Construction & prediction

Per corpus: demean E over items, SVD → orthonormal directions V (ordered). Fix a
4-bit distortion budget ε_i = ‖(per-item-uniform-4bit(E) − E)_i‖ per item. Two
subspaces S_A = span(V[:8]), S_B = span(V[8:16]). Arms:
- **a_err_in_A**: inject a random error of norm ε_i into S_A. E_rec = E + δ_A.
- **b_err_in_B**: inject a random error of norm ε_i into S_B. E_rec = E + δ_B.
- **c_polar_antiprobe**: real anti-probe (wrong-quotient control, context).
- **d_periitem_uniform4**: the real per-item 4-bit quantizer (its distortion is ε).

By construction rel-‖δ‖ is **identical** for a, b, d (all = ε_i/‖E_i‖ per item) →
reconstruction cannot order them. Consumers read_A (queries in S_A) and read_B
(queries in S_B). Prediction: read_A sees a's error but not b's → a worse; read_B
sees b's error but not a's → b worse — a **flip at identical reconstruction**,
tracked by `proj_var = tr(P_C Σ_δ)/tr(P_C Σ_0)`, which reconstruction cannot.

```yaml
id: GO-P-2026-008
date: 2026-07-17
retrospective: false          # PROSPECTIVE; controlled matched-distortion probes
instance: 2-prime
representation: low-rank embeddings E in R^{N x D} (as GO-P-2026-007)
consumer: inner-product retrieval ranking. d_O = mean over queries of
          (1 - Spearman(true_scores, recon_scores)) over the N-item corpus.
probes:
  a_err_in_A: matched-magnitude (eps_i) random error injected into S_A = span(V[:8])
  b_err_in_B: matched-magnitude (eps_i) random error injected into S_B = span(V[8:16])
  c_polar_antiprobe: real per-item polar anti-probe (context)
  d_periitem_uniform4: real per-item uniform 4-bit (its distortion sets eps; matched to a,b)
consumers_probed:
  read_A: unit queries in S_A
  read_B: unit queries in S_B
  iso: isotropic unit queries (diagnostic; expect a ~ b)
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
  snr_gate: min-arm median d_O (over read_A, read_B) >= 10 x the fp16-vs-fp16 rerun floor
gated: [matched_distortion, snr, flip_decisive, proj_tracks_flip, recon_fails]
diagnostics_reported_not_gated:
  - iso_consumer: median adv_dO(iso) (expect ~ 0; no flip under isotropic read)
  - anti_probe_gap: median dO(c)/dO(a) per consumer
  - full_rank_spearman: Spearman(proj_var, dO) and Spearman(recon, dO) per consumer
controls:
  - noise-floor: d_O against the fp16-vs-fp16 rerun, per consumer.
amendments: []
hash: sha256:937151301c6843f2a560d6a9d8ae869d735730f2583ab28550e54f5874245085   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (instance 2', prospective)

The mechanism **fails to replicate in retrieval** if any hold at n=12:
- matched-distortion gate fails (recon(a), recon(b) differ > 2%) — regime void; or
- SNR gate fails; or
- the flip is not decisive (median adv_dO(read_A) > −log1.3, or adv_dO(read_B) < log1.3,
  or per-seed flip < 10/12 in either direction) — i.e. the nonlinear ranking does
  **not** follow the injected error's subspace; or
- proj_var does not track the flip per-seed (< 11/12 in either consumer); or
- reconstruction tracks a,b as well as proj_var (min_C Spearman(recon,dO) not
  strictly < min_C Spearman(proj_var,dO)).

`GO2_mechanism_replicates` requires all five gated conditions. A pass makes GO-2's
mechanism `[replicated]` (2 independent instances: softmax attention + retrieval
ranking), in the recon-matched regime NEG-10 delimits. A miss bounds it further
(e.g. ranking is governed by something other than the projected error covariance).
