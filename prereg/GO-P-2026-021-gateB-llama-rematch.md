# GO-P-2026-021 — Gate B REMATCH: recon-matched dissociation on a REAL Llama layer (PROSPECTIVE)

Fixes the flaw that made GO-P-2026-020 a miss (NEG-12). That entry registered a
quantizer pair (`per-channel asym4`, `per-token uniform4`) that was **not
reconstruction-matched**: per-token error is genuinely worse on *both* reconstruction
and softmax-KL, so plain reconstruction predicted the winner on all 16 heads and
`proj_beats_recon` could not fire. The decisive Observation-Theory claim — a
**reconstruction-identical, P_C-different** pair whose downstream verdict is set by the
read operator — was therefore never put at risk on the trained model.

This rematch constructs the two key-error arms to be **recon-matched by construction**:
identical per-token $\|\delta\|$ to machine precision, but opposite read-subspace
content. Reconstruction is then *provably blind* (an exact tie), and only the
consumer-projected predictor $\tr(\hat\PC\Sigma_\delta)$ can resolve the flip. This is
the GO-2 dissociation (which succeeded synthetically) ported to a real trained layer.
Governs `experiments/gateB_llama_rematch.py` and `results/GateB-llama-rematch.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE, real-model.** Substrate =
`unsloth/Llama-3.2-3B` (real weights, Atlas GPU 1 only; GPU 0 untouched; no processes
killed). GO-P-2026-020 stands as a miss on the ledger; this is a distinct, freshly
sealed test, not a re-score.

## Setup

- **Model/layer:** Llama-3.2-3B, post-RoPE keys $K_h$ and queries $Q_h$ at layers
  $L\in\{8,16\}$ (same as GO-P-2026-020, for a clean comparison); 16 KV-head instances;
  $d=128$. Real text batch ($8$ seqs, seq len $256$).
- **Consumer (per KV head):** softmax attention $p_i=\mathrm{softmax}(q_i^\top K_h/\sqrt d)$
  over the real key set; representation $X=K_h$. True read operator
  $\PC^{\mathrm{true}}=\frac1{|\mathcal I|}\sum_i q_i q_i^\top$, used only for scoring
  and for *constructing* the dissociation, never given to the probe.
- **Blind probe (improved):** receives only the callable $K\mapsto p(K)$ and $d$;
  estimates $\hat\PC$ by finite-difference Jacobian probing, now anchored on
  **32 keys** (up from 12) with $N_{\mathrm{probe}}=160$; top-$r$ eigenspace ($r=16$).
  Never sees $Q_h$, the arms, or the downstream KL.
- **Recon-matched arms (the fix):** base magnitude = real per-channel 4-bit quant error
  $g$, with per-token norm $r_s=\|g_s\|$. Arm **A** places the error in the top-$r$ read
  subspace, arm **B** in its orthogonal complement, each rescaled to the same $r_s$:
  $\delta^A_s = r_s\,\widehat{P_{\mathrm{read}}g_s}$, $\delta^B_s = r_s\,\widehat{P_{\perp}g_s}$
  (unit-normalized components; top / bottom eigvec fallback if a component vanishes).
  Hence $\|\delta^A_s\|=\|\delta^B_s\|=r_s$ **exactly** — reconstruction is tied.
- **Prediction (blind):** worse arm $=\arg\max_{c\in\{A,B\}}\tr(\hat\PC\,\Sigma_\delta^c)$.
- **Ground truth (measured):** worse arm $=\arg\max_c$ per-head softmax-KL(fp vs $K+\delta^c$).

```yaml
id: GO-P-2026-021
date: 2026-07-17
retrospective: false
gate: B-book-rematch
supersedes_design_flaw_of: GO-P-2026-020   # NEG-12: arms were not recon-matched
claim: "On a trained Llama attention layer, a blind probe predicts a reconstruction-invisible key-error flip that reconstruction cannot see."
model: unsloth/Llama-3.2-3B (post-RoPE K,Q; layers {8,16}; KV heads = instances; d=128)
data: real text batch (8 seqs, seq_len 256)
probe: black-box finite-difference Jacobian; 32 anchor keys; N_probe=160; hat_P_C = top-16 eigvecs; BLIND
arms:
  A: per-token error placed in the top-16 read subspace
  B: per-token error placed in the orthogonal complement, SAME per-token norm as A (exact)
predict: argmax_c tr(hat_P_C Sigma_delta^c)   # blind; larger projected trace = worse arm
truth: argmax_c per-head softmax-KL(fp vs quantized keys)
prediction:                                    # GATE = first three (all must hold)
  recon_tied: max over heads |recon_A - recon_B| <= 1e-6            # construction integrity
  arms_downstream_distinct: median over heads of |KL_A-KL_B|/mean(KL_A,KL_B) >= 0.5
  blind_predicts_winner: sign(tr(hat_P_C Sd^A)-tr(hat_P_C Sd^B)) == sign(KL_A-KL_B) on >= 75% heads
  proj_beats_recon: proj agrees with measured winner on strictly more heads than recon (sign of recon_A-recon_B)
diagnostics_reported_not_gated:
  - probe_recovery_diag: median subspace-overlap(hat_P_C_r, P_C_true_r) >= 0.60  (chance r/d=0.125)
  - per-head overlap, pred_A/B, KL_A/B, recon_A/B, rel_kl_gap
design: {clusters: (layer,head), stopping: fixed}
compute: Atlas GPU 1 only (CUDA_VISIBLE_DEVICES=1); GPU 0 untouched; no processes killed
amendments: []
hash: sha256:e398bf0aa372f0fd523e56d2711e7320a085d2676b6fb14d89b81e42c31da73f
```

## Falsification (Gate B rematch, prospective, real model)

**Not supported** if any gate fails: the arms are not exactly recon-tied
(construction bug); or they do not differ downstream (median relative KL gap $<0.5$, so
there is no flip to predict); or the blind $\tr(\hat\PC\Sigma_\delta)$ predicts the
measured worse arm on $<75\%$ of heads; or projection does not strictly beat
reconstruction. A **pass** shows Observation Theory's mechanism operating on a *trained*
model: a reconstruction-invisible flip, set by the read operator, called before
compression by a blind probe. A **miss** (e.g. the blind $\hat\PC$ is too coarse to
resolve in-subspace vs complement error) keeps the theory bounded to synthetic
consumers and is carried honestly as a second Gate-B negative. `probe_recovery` is
reported as a diagnostic: even an imperfectly recovered $\hat\PC$ (overlap $<0.60$) that
still calls the flip $\ge75\%$ is informative, and is stated as such.
