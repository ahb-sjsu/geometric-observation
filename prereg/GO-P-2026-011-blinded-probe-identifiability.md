# GO-P-2026-011 — GO-1: the invariant/nuisance split is identifiable ex ante (BLINDED, PROSPECTIVE)

The GO-1 test. GO-2 established that downstream distortion is governed by the error
covariance projected on the consumer's read operator `P_C` (across attention,
retrieval, optimization — GO-P-2026-006/009/010). GO-1 is the **prior** claim: that
`P_C` (the invariant/nuisance split, i.e. the read subspace) is **identifiable ex
ante from the consumer functional alone** — recoverable by *querying* the consumer,
blind to any compressor or downstream result — and that the recovered split
predicts the flip. Fresh registration; no edits to prior entries. Governs
`experiments/go1_blinded_probe.py` and `results/GO1-blinded-probe.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE, and BLINDED.** Never run. The
probe is a pure function of a black-box consumer handle `C(·)` and receives
**nothing else** — not the planted read subspace, not the compression arms, not
`d_O`. Structurally enforced in code. A pass gives GO-1 a genuine `[predicted]`
class; a miss (probe cannot recover the split, or the recovered split does not
predict downstream) bounds identifiability and is carried in Honest Negatives.

## The blinded probe (committed algorithm)

Given only a callable consumer `C: R^D → R^m` and (D, r):
1. Sample `n_base=8` base points x0 from the representation distribution.
2. At each base, sample `n_probe=256 ≥ D` random unit directions U; central
   finite differences `ΔC_j = (C(x0 + h u_j) − C(x0 − h u_j))/(2h)`, h=1e-2, give
   `ΔC ≈ U Ĵᵀ`. Solve `Ĵᵀ = pinv(U) ΔC` (least squares) → local Jacobian.
3. Accumulate `M̂ = Σ_base Ĵᵀ Ĵ` (D×D input-space sensitivity operator).
4. Return `Ŝ` = top-r eigenvectors of M̂ — the estimated read subspace.

The probe never sees S_true, the arms, or d_O. We (not the probe) then score
recovery and downstream prediction.

## Consumers & flip (to score the recovery)

Per seed, a random orthonormal basis; two **planted** read subspaces S_A=span(rows
of W_A), S_B=span(rows of W_B), disjoint (r=8 each). Consumers
`C_A(x)=tanh(W_A x)`, `C_B(x)=tanh(W_B x)` (nonlinear, so finite-diff recovery is
nontrivial). d_O(arm, C) = mean_i ‖C(x_i+δ_i) − C(x_i)‖ / mean_i ‖C(x_i)‖. Matched-
distortion probes inject error into S_A (arm a) / S_B (arm b), η=0.1 mix, plus real
anti-probe c and per-coord uniform d (as in GO-P-2026-009/010). Under C_A arm a is
worse; under C_B arm b — a flip governed by the read subspace.

```yaml
id: GO-P-2026-011
date: 2026-07-17
retrospective: false          # PROSPECTIVE and BLINDED
claim: GO-1
representation: low-rank embeddings x in R^{N x D} (N=512, D=128)
consumers: C_A(x)=tanh(W_A x), C_B(x)=tanh(W_B x); W_A rows = S_A=span(V[:8]),
           W_B rows = S_B=span(V[8:16]) of a per-seed random orthonormal basis V
probe: black-box Jacobian-sensitivity probe (above); input = C(.) handle + (D,r); output = Ŝ (D x r)
probes_compressors: [a_err_in_A, b_err_in_B, c_polar_antiprobe, d_percoord_uniform4]  # as GO-P-2026-009
prediction:
  identifiability: the blind probe recovers the read subspace: overlap(Ŝ_C, S_true_C) high for C in {A,B}
  blind_predicts_flip: proj_var computed with the BLIND Ŝ (not S_true) predicts the d_O flip
  recon_fails: reconstruction (identical a,b,d) cannot
gated:
  subspace_recovery: median min_C overlap(Ŝ_C, S_true_C) >= 0.90
                     # overlap(U,V) = (1/r)||U^T V||_F^2 in [0,1] (mean sq principal-angle cosine)
  blind_predicts_flip: sign(adv_projhat(C_A)) == sign(adv_dO(C_A)) per seed >= 11/12
                       AND sign(adv_projhat(C_B)) == sign(adv_dO(C_B)) per seed >= 11/12
                       AND median adv_dO(C_A) <= -log(1.3) AND median adv_dO(C_B) >= log(1.3)
  recon_fails: min_C Spearman(recon_arms, dO_arms) < min_C Spearman(projhat_arms, dO_arms)
  matched_distortion: |median recon(a) - median recon(b)| / median recon(a) <= 0.02
  snr_loser: min over {C_A,C_B} of the LOSER's median dO >= 10 x the fp16 floor
design:
  n: 12 seeds; N=512 items; D=128; r=8; eta=0.1; n_base=8; n_probe=256; h=1e-2
  clusters: seed
  stopping: fixed-n
diagnostics_reported_not_gated:
  - overlap_random_baseline: overlap(random r-subspace, S_true) (chance ~ r/D = 0.0625)
  - projtrue_vs_projhat: Spearman(proj_var with S_true, dO) vs with Ŝ (blind should ~ match true)
  - iso_consumer: C reading a random subspace disjoint from S_A,S_B (expect a~b)
controls:
  - noise-floor: d_O against the fp16-vs-fp16 rerun, per consumer.
amendments: []
hash: sha256:2ec99ec4bf106eaf946d75b1cadc340a2b14356f82666b2800d3c4b7aff6e268   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-1, blinded, prospective)

GO-1 is **not supported** if any hold at n=12:
- the blind probe does not recover the read subspace (median min-overlap < 0.90 —
  identifiability fails); or
- the blind Ŝ does not predict the flip (per-seed sign agreement < 11/12 either
  consumer, or the flip is not decisive); or
- reconstruction predicts downstream as well as the blind projection; or
- the matched-distortion or SNR gate fails (regime void).

`GO1_supported` requires all five gated conditions. A pass = GO-1 `[predicted]`:
the invariant/nuisance split is recoverable ex ante from the consumer functional,
blind, and the recovery predicts downstream. The overlap-vs-chance baseline
(~0.0625) makes the recovery bar non-trivial.
