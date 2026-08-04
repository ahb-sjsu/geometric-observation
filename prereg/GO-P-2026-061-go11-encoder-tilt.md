# GO-P-2026-061 — GO-11 operational face: the encoder-side tilt

Registers the **operational demonstration** of GO-11's mechanism prediction
([`paper/go11-conditional-region.tex`](../paper/go11-conditional-region.tex)
v0.8, Remark rem:mechanism + Prop. 1 / Thm. 2 / Thm. 6(a)): an L-optimal
record **writes itself into the reset context's X-measurable directions** —
the encoder-side complement of the eraser-side allocation tilt measured in
GO-P-2026-058/059. Canonical instance ρ² = ½, D = 0.25, τ² = 0 (S = V);
Theorem-2 coefficients a = 0.5, b = √2·D ≈ 0.3536.

**Three records, one consumer.** MARG encodes Y alone (Steinberg-corner
content 0.661 b/sym predicted); TILT encodes the Theorem-2 statistic
z₊ = aY + bV at covering distortion D(1−2D) (content = **Gray floor 0.500**
— Theorem 6 case (a) attainment, made operational; rate premium
R_t − R_m = 0.161 b/sym = Cor. 2's cost, **reported**); TILT⁻ encodes
z₋ = aY − bV, whose correlation with V is **exactly zero by construction**
(aρ − b = 0 at this instance) — the analytic context-blindness probe. TILT⁻
is *not* a consumer arm: its channel distortion (0.625 > D) makes consumer
matching impossible at these coefficients — itself part of the point — so
it is audit-exempt and gated on S-vs-S′ independence only. Instrument =
053/058 decode-threshold lineage (bin, MAP from context over strided
members, thr = 0.25-crossing); discount disc = thr(|none) − thr(|S).

Governs `experiments/go11_encoder_tilt.py` (numpy, ~1 min; sentinel
`===GO11ET-JSON===`; summary flag `GO11ET_supported`).

```yaml
id: GO-P-2026-061
date: 2026-08-05
retrospective: false
kind: operational demonstration (Tier B, CPU; GO-11's encoder-side face, one instance)
claim: "At matched consumer distortion, a record tilted into the reset
  context's X-measurable direction (Theorem-2 coefficients) carries a
  strictly larger context-decode discount than the marginalized record —
  by a substantial fraction of the predicted content gap — with its
  measured conditional content at the Gray floor (Theorem 6(a) attainment);
  the analytically context-blind flipped record shows zero S-specific
  decode gain; mismatched contexts save nothing."
harness: experiments/go11_encoder_tilt.py   # GOVERNED seed 20260830, T=400; pilots seed 20260828, disclosed below
power: |
  Deterministic-at-seed instrument; per PROTOCOL 5.1 the bars carry pilot
  margins: E2 lower bar 0.40x pred (0.129) vs pilot 0.497 (3.9x), upper
  pred+0.35 (0.672) vs 0.497 (headroom 0.175 >> threshold noise ~0.02);
  E3 tolerance 0.28 vs pilot |dev| 0.193 (1.45x), content-gap bar 0.064 vs
  pilot 0.297 (4.6x); E4 bar 0.10 vs pilot 0.000; E5 bar 0.15 vs pilot
  <= 0.002; E1 audit window [0.18, 0.36] with matched-arms bar 0.06 vs
  pilot diff 0.014. Every margin >= 1.3x.
pilot: |
  TWO pilot runs, both seed 20260828, both disclosed. RUN 1 exposed three
  GATE defects (physics clean): (i) the flip arm cannot be consumer-
  distortion-matched (channel distortion 0.625 > D) -- reclassified as an
  audit-exempt context-blindness probe; (ii) its drafted disc-vs-none gate
  measured a min-norm-prior artifact, not context (thr(S) = thr(S') =
  0.920 exactly -- the aρ−b = 0 prediction landing perfectly) -- E4
  restated as S-vs-S' independence; (iii) E2 upper / E3 tolerance widened
  for the finite-n instrument (MARG's Steinberg content realizes slowly:
  0.990 vs 0.661 asymptotic). RUN 2 (gate logic only changed; identical
  draws): ALL PASS. Values: consumer distortions 0.3125/0.3261 (matched,
  diff 0.014); discounts MARG 0.110, TILT 0.607, tilt advantage 0.4970
  (asymptotic 0.3219); contents 0.990/0.693 vs 0.661/0.500 predicted;
  flip S-vs-S' = 0.000; shuffled nulls <= 0.002; strict face tau^2 = 0.5
  disc = 0.275 (REPORTED); rate premium 0.161 b/sym (REPORTED).
prediction:
  E1_consumer_audit: MARG and TILT consumer distortions in [0.18, 0.36]
    and matched within 0.06 (flip exempt; its distortion reported)
  E2_tilt_advantage: 0.40*0.3219 <= disc(TILT) - disc(MARG) <= 0.3219+0.35
  E3_floor_attainment: |Lhat(TILT) - 0.500| <= 0.28 AND
    Lhat(MARG) - Lhat(TILT) >= 0.40 * 0.161
  E4_flip_context_blindness: |thr(flip|S) - thr(flip|S')| <= 0.10
  E5_shuffled_null: |disc_S'(MARG)|, |disc_S'(TILT)| <= 0.15
  E6_uniform_control_exact: every uniform-control cell consistent with
    chance under the exact two-sided binomial test, alpha = 5e-4
  reported_not_gated: the tilt's rate premium (Cor 2); the strict face
    tau^2 = 0.5 discount (Theorem 6's deficits ~0.02-0.05 b/sym are below
    instrument resolution -- not gated, per the power-first rule); flip
    arm consumer distortion.
falsification: E2 failing kills the encoder-side tilt claim (GO-11's
  operational face); E3 failing kills the Gray-floor attainment reading
  (Theorem 6(a) operationally); E4 or E5 failing kills context-specificity;
  E1 or E6 failing voids the run as an instrument fault (logged; rerun only
  under a dated amendment). Any miss is reported at full prominence; GO-11
  stays [predicted] on a miss; a pass supports [demonstrated] on one
  instance (a second instance/family would be a separate registration).
design:
  n: 10
  trials: 400            # enlarged from the 250-trial pilots, pre-committed
  rho2: 0.5
  D_target: 0.25
  tau2: [0 (gated), 0.5 (reported)]
  rb_grid: [0.15, 0.275, 0.40, 0.525, 0.65, 0.775, 0.90, 1.025, 1.15, 1.275]
  stopping: fixed design, single governed run, seed 20260830, after the two
    disclosed pilot runs (seed 20260828); no further pilots or attempts
    under this ID
controls: [flip probe with analytic zero coupling (E4), shuffled context
  (E5), consumer-distortion matched-arms audit (E1), exact-binomial uniform
  control (E6), no-context anchor thresholds]
amendments: []
hash: sha256:90987042670c1a89706c08a0bd7e5a025a864998e0843f580a46cede71b7ae22
```

## Falsification

Any gate miss is reported at full prominence per PROTOCOL Rule 1.2 and
leaves GO-11 at `[predicted]`. A pass supports GO-11 at `[demonstrated]` on
one instance: the encoder-side tilt is then measured physics — records
optimally "written in ink the eraser can read," completing the pair with
058/059's eraser-side allocation tilt.
