# GO-P-2026-062 — GO-11 encoder-tilt face, second source family (binary)

Registers the **binary replication setting** of GO-11's encoder-side tilt
(first family: Gaussian, [GO-P-2026-061](GO-P-2026-061-go11-encoder-tilt.md)
**ALL PASS 6/6**, tilt advantage 0.595 b/sym). A pass puts the encoder-side
mechanism on **two independent source families** and supports GO-11 at
`[replicated]` per the §1 bar; a miss leaves `[demonstrated]` and is
reported at full prominence.

**Setting.** Iid pairs (Y, V), fair bits, P(Y≠V) = p = 0.25; context S = V
(X-measurable attainment face); consumer reads Y at Hamming D = 0.2. Three
records: **MARG** covers Y alone (marginalized-class content, BA-exact
target **0.2121** b/sym); **TILT** implements the pair-BA L-optimal channel
q\*(ŷ|y,v) (content target **0.0894** = h₂(p) − h₂(D) — the pair-BA optimum
lands \*exactly\* on binary Gray, confirming Prop 1's mechanism discretely;
rate premium 0.3975 b/sym, reported); **FLIP** covers W = Y⊕V, which is
**exactly independent of V** under the symmetric coupling — the analytic
context-blindness probe, audit-exempt (W alone is useless to the consumer,
distortion ≈ ½), gated on S-vs-S′ independence only. Instrument = 053/059
decode-threshold lineage with per-symbol log-likelihood context scores;
noisy-context face S = V⊕Bern(0.1) measured and REPORTED.

**Pre-seal derivation (the house obligation).** The tilted channel and both
content targets are computed in-harness by exact conditional-BA on the
4-state joint (044-validated machinery; exact at this alphabet size, no
seed involved); the committed numeric targets are L_marg = 0.2121,
L_tilt = 0.0894, R_tilt = 0.6755, asymptotic tilt advantage
(R_t − L_t) − (R_m − L_m) = **0.5203** b/sym. The hand-derivable warm-start
channel ("flip Y toward V only on disagreement", content 0.106) brackets
the BA optimum from above.

Governs `experiments/go11_encoder_tilt_binary.py` (numpy, ~1 min; sentinel
`===GO11ETB-JSON===`; summary flag `GO11ETB_supported`).

```yaml
id: GO-P-2026-062
date: 2026-08-05
retrospective: false
kind: operational replication (Tier B, CPU; GO-11's encoder-side face, second source family)
claim: "On a binary pair source with X-measurable context, the pair-BA
  L-optimal record carries a strictly larger context-decode discount than
  the marginalized record at matched consumer Hamming distortion -- by a
  substantial fraction of the BA-committed advantage 0.5203 b/sym -- with
  the content ordering matching the Gray-vs-marginalized targets; the
  analytically context-independent XOR record shows zero S-specific decode
  gain; mismatched contexts save nothing."
harness: experiments/go11_encoder_tilt_binary.py   # GOVERNED seed 20260902, T=400; pilot seed 20260901, disclosed below
power: |
  Deterministic-at-seed instrument; per PROTOCOL 5.1 the bars carry pilot
  margins: B2 lower 0.40x pred (0.208) vs pilot 0.5212 (2.5x), upper
  pred+0.30 (0.820) vs 0.5212 (headroom 0.30 >> threshold noise ~0.02);
  B3 bar 0.40x content gap (0.049) vs pilot 0.104 (2.1x); B4 bar 0.10 vs
  pilot 0.002 (50x); B5 bar 0.15 vs pilot <= 0.003; B1 window [0.14, 0.30]
  with matched-arms bar 0.06 vs pilot diff 0.019 (3.1x). Every margin
  >= 1.3x.
pilot: |
  ONE pilot, seed 20260901, T=250, 39 s: ALL PASS with the drafted bars
  unchanged (zero bar recalibrations -- second registration of the
  campaign, after 060, for which the pilot forced no instrument changes).
  Values: BA targets L_marg/L_tilt/R_tilt = 0.2121/0.0894/0.6755 (L_tilt
  = h2(p) - h2(D) exactly -- pair-BA lands on binary Gray); consumer
  distortions 0.2215/0.2022 (matched, diff 0.019; FLIP 0.5107 as expected
  for the blindness probe); discounts MARG 0.052, TILT 0.573, FLIP 0.012;
  tilt advantage 0.5212 vs asymptotic 0.5203 (agreement 0.001!); contents
  0.281/0.177 vs targets 0.212/0.089 (ordering gap 0.104); flip S-vs-S' =
  0.002; shuffled nulls <= 0.003; noisy face q=0.1 disc = 0.346 (REPORTED).
prediction:
  B1_consumer_audit: MARG and TILT consumer distortions in [0.14, 0.30]
    and matched within 0.06 (FLIP exempt; its distortion reported)
  B2_tilt_advantage: 0.40*0.5203 <= disc(TILT) - disc(MARG) <= 0.5203+0.30
  B3_content_ordering: Lhat(MARG) - Lhat(TILT) >= 0.40 * (0.2121 - 0.0894)
  B4_flip_context_blindness: |thr(FLIP|S) - thr(FLIP|S')| <= 0.10
  B5_shuffled_null: |disc_S'(MARG)|, |disc_S'(TILT)| <= 0.15
  B6_uniform_control_exact: every uniform-control cell consistent with
    chance under the exact two-sided binomial test, alpha = 5e-4
  reported_not_gated: the tilt's rate premium 0.3975 b/sym; the noisy-
    context face q = 0.1 discount; FLIP consumer distortion; realized
    fraction of the advantage for cross-family comparison (Gaussian 061:
    0.595 measured vs 0.322 asymptotic).
falsification: B2 failing kills the binary encoder-tilt claim and blocks
  [replicated]; B3 failing kills the content-ordering (Gray-vs-Steinberg-
  class) reading; B4 or B5 failing kills context-specificity; B1 or B6
  failing voids the run as an instrument fault (logged; rerun only under a
  dated amendment). Any miss is reported at full prominence; GO-11 stays
  [demonstrated] on a miss.
design:
  n: 24
  trials: 400            # enlarged from the 250-trial pilot, pre-committed
  p_YV: 0.25
  D_target: 0.20
  context: [S = V (gated), S = V xor Bern(0.1) (reported)]
  rb_grid: [0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.60, 0.70, 0.80]
  stopping: fixed design, single governed run, seed 20260902, after the one
    disclosed pilot (seed 20260901); no further pilots or attempts under
    this ID
controls: [XOR probe with exact independence (B4), shuffled context (B5),
  consumer-distortion matched-arms audit (B1), exact-binomial uniform
  control (B6), BA-committed numeric targets (pre-seal derivation)]
amendments: []
hash: sha256:4f50578c308c8cdb6a9db9447568252bd01d08cf777bd76930015165d7dbbccf
```

## Falsification

Any gate miss is reported at full prominence per PROTOCOL Rule 1.2; GO-11
remains `[demonstrated]` (Gaussian face only). A pass puts the encoder-side
tilt on two independent source families — the `[replicated]` promotion is
then made in the ledger with the cross-family realized-fraction comparison
carried alongside.
