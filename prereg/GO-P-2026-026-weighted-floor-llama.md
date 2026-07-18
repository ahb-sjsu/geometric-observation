# GO-P-2026-026 — Making the omission floor unconditional on a trained Llama layer

**Prospective** (retrospective:false). Turns Appendix `app:mismatch`'s omission floor from a
*conditional projector-model certificate* (the "0.647 → 35.3%" reading, which assumes
omission + equal weights + $\Sigma_x=I$) into a **measured, operationally-validated** floor
on the real Llama-3.2-3B read operators. Governs a harness that EXTENDS
`experiments/gateB_llama_rematch.py` (probe unchanged; it already computes everything
needed — see the audit note below). **Runs on Atlas GPU 1 — to be executed by the user;
the sealed commit is the binding timestamp.**

## Audit note (what the existing probe already produces)
`gateB_llama_rematch.py` computes, per KV head: the true consumer operator
`Pc_true = Qᵀ Q / n` (line 140, full spectrum available), the recovered `Phat = Σ_s Jᵀ J`
(line 84, full spectrum available), and has the post-RoPE keys `K` in hand (so
`Σx = Cov(K)` is one line). It currently keeps only the top-`r` eigenVECTORS and a
symmetric overlap `o = (1/r) tr(Π_R Π_R̂)` (audited: `_overlap`, lines 88–89 — this is
exactly mean-cos², matching the appendix). The weighted floor needs the eigenVALUES and
`Σx`, both already present and discarded. So the certificate below is a **logging +
one operational sweep** on top of an existing, sealed probe — not a new probe.

## What makes E conditional, and what removes each (the four bridges)
1. **omission vs over-cover** — replace symmetric `o` by the **directed** miss
   `f_out = tr(Π_R (I−Π_R̂)) / r` and the containment test `range(P_top) ⊄ range(P̂_top)`.
2. **equal weights** — use the recovered spectrum of `Phat` (blind) and the true spectrum
   of `Pc_true` as the read weights; floor `= tr(P̃ Π)` with the actual weighted `P`.
3. **`Σx = I`** — whiten by the measured key covariance `Σx = Cov(K)`; `Π` = projector onto
   `Σx^{-1/2} ker P̂` (the whitened kernel, per Theorem `thm:omission`).
4. **overlap definition / rank** — DISCHARGED by audit: `o` is mean-cos², ranks matched by
   construction (both top-`r`). No change needed.

## Claim + sealed predictions
```yaml
id: GO-P-2026-026
date: 2026-07-17
retrospective: false
kind: prospective operational validation (real trained model; Atlas GPU 1)
requires: Atlas GPU 1 (CUDA_VISIBLE_DEVICES=1), unsloth/Llama-3.2-3B, run by the user
harness: experiments/gateB_llama_weighted_floor.py   # extends gateB_llama_rematch.py; to be written BEFORE running
claim: "The omission distortion floor D_floor=tr(P~ Pi) (whitened kernel, measured weights) is a real,
  rate-irreducible operational floor on trained Llama read operators -- not just a projector-model figure."
validation_gate_synthetic:   # blind weight recovery must be trustworthy BEFORE trusting it on Llama
  weight_recovery: on >=20 planted synthetic read operators, the recovered Phat top-r spectrum
    (normalized) rank-correlates with the true weights at Spearman >= 0.9 (blind)
prediction_llama:
  directed_floor: per head report f_out and D_floor = tr(P~ Pi) using measured Sigma_x=Cov(K),
    measured weights, and the WHITENED kernel; classify each head omission (D_floor>0) vs contained
  floor_vs_naive: the whitened-kernel D_floor differs from the naive-kernel r(1-o) reading (quantify)
  operational_floor (DECISIVE): compress the keys with the MISIDENTIFIED operator P_hat at a sweep of
    rates R; for omission heads (a) the true read distortion tr(P_true Sigma_delta) floors at the
    predicted D_floor (within a factor 2, units-matched) and (b) the downstream softmax-KL stops
    improving -- doubling R past read-mode saturation cuts KL by < 20% -- while a CORRECT-operator
    (P_true) control keeps driving KL down. Contained heads show no floor.
falsification: added rate keeps reducing tr(P_true Sigma_delta) / softmax-KL past the predicted floor
  for omission heads (no floor), or a floor appears where no omission is diagnosed -> the omission
  floor's operational relevance to trained models is refuted (an honest negative, as NEG-x).
verification:
  - derivation is GO-P-2026-024 (fresh-context passed); this entry validates its OPERATIONAL claim.
  - synthetic weight-recovery gate must pass before the Llama numbers are trusted (guards a new
    dependency: that the probe's eigenvalues, not just eigenvectors, are recoverable blind).
amendments: []
hash: sha256:a947dce551e94b9836611f252a4785ff2962d4d1ce2522ed259d360a082adeeb
```

## Falsification
The floor theorem is proved (GO-P-2026-024); what is prospective here is whether the *measured*
Llama operators exhibit it operationally. Per the sealed gate, if added rate keeps buying distortion
reduction past the predicted floor on omission heads, the theorem's operational relevance to trained
models is refuted and recorded as an honest negative. The synthetic weight-recovery gate is sealed
first because the whole certificate rests on recovering the read *weights* blind, which GO-1 did not
previously claim (it recovered the subspace only).
