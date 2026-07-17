# GO-P-2026-020 — Gate B (book): blind probe on a REAL Llama attention layer (PROSPECTIVE)

The decisive validation. Sections 4--5 of the Observation-Theory paper use
\emph{synthetic} consumers (planted read operators, chosen query banks). This entry
runs the whole loop on an \emph{actual trained} attention layer: recover the read
operator (query second moment) from the softmax consumer by a \textbf{blind probe},
and use it to predict which key-quantizer wins \emph{before} compressing---then
verify against the layer's real softmax-KL. Converts ``the theory's logic is
validated'' into ``the theory works on a trained model.'' Fresh registration.
Governs `experiments/gateB_llama_keys.py` and `results/GateB-llama-keys.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE, real-model.** Substrate =
`unsloth/Llama-3.2-3B` (real weights, on Atlas). Genuine risk: GQA, RoPE, real
noise, and the probe must recover a real (not planted) $\PC$. Runs on Atlas GPU 1
only (GPU 0 is busy; never disturbed).

## Setup

- **Model/layer:** Llama-3.2-3B, post-RoPE keys $K_h$ and queries $Q_h$ extracted at
  layers $L\in\{8,16\}$ via forward hooks on a real text batch (wikitext / Gutenberg
  passage, $\ge 8$ sequences, seq len $\ge 256$). Head dim $d=128$; the KV heads of
  each layer are the independent instances ($n=$ #KV-heads $\times$ #layers, $\ge 16$).
- **Consumer (per KV head):** softmax attention $p_i=\mathrm{softmax}(q_i^\top K_h/\sqrt d)$
  over the real key set; representation $X=K_h$ to be quantized. True read operator
  $\PC^{\mathrm{true}}=\frac1{|\mathcal I|}\sum_{i}q_i q_i^\top$ (the real query second
  moment), used only for scoring, never given to the probe.
- **Blind probe:** receives only the callable consumer $K\mapsto p(K)$ and $(d)$;
  estimates $\hat\PC$ by finite-difference Jacobian probing of the softmax output
  w.r.t.\ key perturbations, top-$r$ eigenspace ($r=16$). Never sees $Q_h$, the
  quantizers, or the downstream KL.
- **Quantizers:** $a$ = per-channel asymmetric 4-bit; $b$ = per-token whole-vector
  uniform 4-bit. Across-token error covariance $\Sigma_\delta^{a},\Sigma_\delta^{b}$.
- **Prediction (blind):** winner $=\arg\min_{c\in\{a,b\}} \tr(\hat\PC\,\Sigma_\delta^{c})$,
  using the \emph{recovered} $\hat\PC$.
- **Ground truth (measured):** actual per-head softmax-KL between full-precision and
  quantized-key attention, $\mathrm{KL}^{a},\mathrm{KL}^{b}$; winner $=\arg\min$.

```yaml
id: GO-P-2026-020
date: 2026-07-17
retrospective: false
gate: B-book
claim: "Observation Theory on a trained model: the blind probe recovers the real read operator and predicts the winning key-quantizer."
model: unsloth/Llama-3.2-3B (post-RoPE K,Q; layers {8,16}; KV heads = instances; d=128)
data: real text batch (>=8 seqs, seq_len>=256)
probe: black-box finite-difference Jacobian on softmax output; hat_P_C = top-16 eigvecs; BLIND
quantizers: [a_perchannel_asym4, b_pertoken_uniform4]
predict: argmin_c tr(hat_P_C Sigma_delta^c)   # blind
truth: argmin_c per-head softmax-KL(fp vs quantized keys)
prediction:
  probe_recovery: median over heads of subspace-overlap(hat_P_C_r, P_C_true_r) >= 0.60   # r=16; chance r/d=0.125
  blind_predicts_winner: sign(tr(hat_P_C Sd^b) - tr(hat_P_C Sd^a)) == sign(KL^b - KL^a)
                         on >= 75% of heads
  proj_beats_recon: the projected predictor agrees with the measured winner on strictly more
                    heads than the reconstruction predictor (argmin ||delta||) does
design: {clusters: (layer,head), stopping: fixed}
compute: Atlas GPU 1 only (CUDA_VISIBLE_DEVICES=1); GPU 0 untouched; no processes killed
diagnostics_reported_not_gated:
  - per-head KL^a,KL^b, tr(hat_P_C Sd^{a,b}), recon^{a,b}, overlap; recovery-vs-chance
amendments: []
hash: sha256:5cbffe27246107567570f5af987d40b240c5cacbdda0a8acc23d6929d691218f   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (Gate B, prospective, real model)

Not supported if: the probe fails to recover the read operator (median overlap
$<0.60$, i.e.\ near chance); or the blind $\tr(\hat\PC\Sigma_\delta)$ predicts the
measured winner on $<75\%$ of heads; or it does no better than reconstruction. A
pass makes Observation Theory `[predicted]` on a trained model---the read operator
recovered blind from a real softmax layer, predicting the real winning quantizer
before compression. A miss bounds the theory to synthetic consumers and is carried
honestly.
