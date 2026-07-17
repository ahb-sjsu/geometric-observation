# GO-P-2026-010 — Gate B: gradient compression, curvature consumer (PROSPECTIVE, out-of-sample)

The GO-B / Gate-B out-of-sample instance for the GO-2 mechanism, in a domain
**disjoint from Papers I–II**: optimization. GO-2's mechanism —
`tr(P_C Σ_δ)` governs downstream, not reconstruction — has held for a query
second-moment `P_C` (attention softmax, GO-P-2026-006) and a subspace projector
(retrieval ranking, GO-P-2026-009). Here `P_C` becomes a **Hessian** (a continuous
PSD curvature operator) and the consumer is a **gradient-descent optimizer**: the
downstream damage of a compressed gradient is read through the loss curvature. If
the flip + reconstruction-blindness survive this, the mechanism is about consumers
reading linear functionals in general — not attention or retrieval. Fresh
registration; no edits to prior entries. Governs
`experiments/go2_gradient_curvature.py` and `results/GO2-gradient-curvature.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE, out-of-sample.** Never run;
optimization is disjoint from Papers I–II. A pass is a genuine Gate-B `[predicted]`
hit; a miss bounds the Ch. 11 umbrella (the mechanism holds for query/subspace
consumers but not curvature consumers).

## Mechanism carried over (the prediction)

For a quadratic loss L(θ)=½θᵀHθ, a gradient error δ = ĝ−g corrupts the update; to
leading order the excess loss and the H-metric update-direction error are governed
by **δᵀHδ = tr(H δδᵀ)** — the error read through the curvature. So the consumer's
read operator is `P_C = H`; the downstream distortion is governed by
`proj_var = tr(H Σ_δ)/tr(H Σ_0)` (Σ = across-gradient covariance), and
reconstruction `‖δ‖ = tr(Σ_δ)` (H = I) is **curvature-blind**. Prediction: at
matched reconstruction, the update-direction distortion flips between two curvature
profiles (H_A curved in S_A, H_B curved in S_B), tracked by proj_var, not by recon.

```yaml
id: GO-P-2026-010
date: 2026-07-17
retrospective: false          # PROSPECTIVE, out-of-sample (optimization)
gate: B                        # fills the GO-B row
representation: gradient population g in R^{N x D}, g = sc * (F L^T + t3-noise) (mean~0, no DC)
consumer: gradient-descent optimizer on quadratic loss L=0.5 θ^T H θ. d_O = mean over
          gradients of (1 - cos_H(g+δ, g)), cos_H(x,y)=x^T H y / sqrt(x^T H x · y^T H y)
          -- the update-direction distortion in the curvature (H) metric.
consumers_probed:
  H_A: I + kappa * P_{S_A},  S_A = span(V[:8])    # high curvature in S_A
  H_B: I + kappa * P_{S_B},  S_B = span(V[8:16])  # high curvature in S_B
  H_iso: I (diagnostic; expect a ~ b)
  kappa: 20
probes:
  a_err_in_A: eps_i error, 90% in S_A + 10% complement (eta=0.1)
  b_err_in_B: eps_i error, 90% in S_B + 10% complement
  c_polar_antiprobe: real per-gradient polar anti-probe (context)
  d_percoord_uniform4: real per-coordinate uniform 4-bit (sets eps; matched to a,b)
probe_output:
  invariant: curvature-weighted error tr(H Σ_δ) (error in high-curvature directions)
  nuisance: total error magnitude (identical across a,b,d) + error in flat directions
  predicted_failure_class: curvature-mismatch
prediction:
  mechanism: proj_var = tr(H Σ_δ)/tr(H Σ_0) governs d_O; reconstruction (identical a,b,d) cannot
  flip_decisive:                                    # adv = log(dO_b / dO_a)
    dO_median: median adv_dO(H_A) <= -log(1.3)  AND  median adv_dO(H_B) >= log(1.3)
    dO_perseed: H_A dO(a) > dO(b) in >= 10/12  AND  H_B dO(b) > dO(a) in >= 10/12
  proj_tracks_flip: sign(adv_proj(C)) == sign(adv_dO(C)) per seed >= 11/12 for C in {H_A, H_B}
  recon_fails: min_C Spearman(recon_arms, dO_arms) < min_C Spearman(proj_var_arms, dO_arms)
design:
  n: 12 gradient-population seeds; N=1024 gradients; D=128; r=8 per subspace; kappa=20; eta=0.1
  clusters: seed
  stopping: fixed-n
  matched_distortion_gate: |median recon(a) - median recon(b)| / median recon(a) <= 0.02
  snr_gate: min over {H_A, H_B} of the LOSER's median dO ( = max(dO(a),dO(b)) ) >= 10 x fp16 floor
gated: [matched_distortion, snr_loser, flip_decisive, proj_tracks_flip, recon_fails]
diagnostics_reported_not_gated:
  - winner_dO, iso_adv_dO, anti_probe_gap, full_rank_spearman per consumer
  - tstep_excess_loss: 30-step GD excess loss under each H (real-optimization cross-check)
controls:
  - noise-floor: d_O against the fp16-vs-fp16 gradient rerun, per consumer.
amendments: []
hash: sha256:fcea7e2498ecd1e9cc223eb06ef3039b317ba7dc6129b53acaedec05380ca594   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (Gate B, prospective, out-of-sample)

The mechanism **fails to generalize to a curvature consumer** if any hold at n=12:
matched-distortion gate fails; the loser's dO not ≥ 10× floor (either consumer);
the flip is not decisive (median adv_dO(H_A) > −log1.3, or H_B < log1.3, or
per-seed < 10/12 either direction) — i.e. curvature-metric update distortion does
**not** follow the injected error's curvature overlap; proj_var does not track the
flip (< 11/12 either consumer); reconstruction tracks a,b as well as proj_var.

`GO2_mechanism_generalizes` requires all five gated conditions. A pass fills GO-B
with a genuine out-of-sample `[predicted]` hit — the mechanism holds for a Hessian
read operator in optimization, not just attention/retrieval. A miss bounds the
Ch. 11 umbrella and is carried in Honest Negatives.
