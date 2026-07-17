# Gate B (book) — Llama-3.2-3B keys — NOTES

**Prereg:** GO-P-2026-020 (sealed `5cbffe27`, registered commit `907d55a`).
**Substrate:** `unsloth/Llama-3.2-3B`, real weights, Atlas GPU 1. Post-RoPE K,Q at
layers {8,16}; 16 KV-head instances; d=128.
**Result file:** `results/GateB-llama-keys.json`.

## Verdict against the sealed bar: NOT SUPPORTED

| Sealed criterion | Bar | Observed | Outcome |
|---|---|---|---|
| `probe_recovery` | median subspace overlap ≥ 0.60 | **0.567** (chance 0.126, ≈4.5×) | **MISS** (short by 0.033) |
| `blind_predicts_winner` | tr(P̂ Σ_δ) agrees with softmax-KL winner on ≥75% heads | **16/16** | pass |
| `proj_beats_recon` | projection agrees on *strictly more* heads than argmin‖δ‖ | **16 vs 16** | **MISS** (not strictly more) |

`GateB_supported = false`. Two of the three sealed falsification triggers fired
(median overlap < 0.60; "no better than reconstruction"). Per the registration, this
**bounds the theory to synthetic consumers on this evidence, and is carried
honestly.** GO-P-2026-020 stands as a miss on the ledger — not retracted, not re-scored.

## What actually happened (diagnosis — post-hoc, not part of the sealed test)

1. **Recovery is real but sub-bar.** Blind finite-difference Jacobian probing of the
   real softmax layer recovered the query second moment at median overlap 0.567 —
   4.5× chance, and strong on individual heads (L8h2 = 0.815, L16h6 = 0.958). But the
   trained-model read operator is noisier to recover than the synthetic planted case
   (GO-1: 0.936), and the median fell 0.033 short of the 0.60 bar. Point-dependent,
   GQA-shared, RoPE-rotated real keys are a harder recovery target than a clean
   plant — consistent with the reviewer's "point-dependent P_C(x) gap."

2. **The registered design could not exhibit the dissociation.** The sealed quantizer
   pair — `a = per-channel asym4`, `b = per-token uniform4` — is **not
   reconstruction-matched**: per-token (b) is genuinely worse than per-channel (a) on
   *both* reconstruction (recon_adv_b−a > 0 on all 16 heads) *and* softmax-KL
   (kl_adv_b−a > 0 on all 16). So plain reconstruction already predicts the winner
   everywhere (recon_hits = 16/16), and projection has no headroom to *beat* it. The
   decisive Observation-Theory claim — a **reconstruction-identical, P_C-different**
   pair whose downstream verdict flips — was demonstrated synthetically in GO-2 but
   **was not put at risk by this registered design.** The bar `proj_beats_recon` was
   therefore un-winnable given non-recon-matched codes, and it correctly reads MISS.

## Corrected decisive experiment (fresh registration required)

The rematch must make the dissociation *possible*, i.e. codes that agree on
reconstruction ‖δ‖ but differ on the consumer projection tr(P̂ Σ_δ):

- **Recon-matched key codes**: construct A/B (or a code family) constrained to equal
  per-token ‖δ‖ (±ε) while differing in *where* the error sits relative to the
  recovered read subspace — exactly the GO-2 construction, now on real keys.
- **Dynamic per-x P_C**: recover and apply P̂_C(x) locally rather than a single
  head-averaged operator (frontier #1 in situ).
- **Multi-layer, larger head count** for a tighter median (mitigates the 0.033 shortfall).
- Seal *before* running (Atlas GPU 1 / NRP scale). This becomes GO-P-2026-021.

The first native-LLM attempt is engaged and honestly scored a miss; the corrected,
recon-matched, dynamic-P_C rematch is the real decisive test.
