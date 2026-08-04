# GO-P-2026-069 — GO-13 operational face: the dynamic complementarity tax on materialized records

Third GO-13 registration; the operational face of Theorems 1–2.
Design and instances were registered as a committed DRAFT (b1984fb)
**before any instrument code existed**, fixed by the exploratory
regime map; the instrument is the 058-lineage decode-threshold
protocol, conventions unchanged, extended to a correlated triple with
both consumers context-coupled.

Governs `experiments/go13_operational_face.py` (numpy, Tier B, single
run; sentinel `===GO13OP-JSON===` with `===END===`; flag
`GO13OP_supported`).

```yaml
id: GO-P-2026-069
date: 2026-08-05
retrospective: false
kind: operational (B: decode-threshold instrument; the dynamic tax measured on materialized codebook records)
claim: "GO-13 operationally: the dynamic complementarity tax measured
  by decode thresholds RISES with context staleness at the regime
  map's rising instance (Thm 2 sign law's face); two access classes
  tuned to equal q give equal thresholds and equal taxes (Thm 1
  universality's face); the flat instance shows a paired near-zero
  contrast; shuffled context nulls the discounts."
harness: experiments/go13_operational_face.py   # GOVERNED seed 20260927; pilot seed 20260926, disclosed below
power: |
  Per PROTOCOL 5.1, bars carry pilot margins: V3 rising bar 0.03 vs
  pilot dCT_rise 0.073 (2.4x; asymptotic prediction +0.286 x
  Delta-q 0.30 = 0.086, realized fraction 0.85x -- above the
  058-lineage 0.44-0.54x window, noted); V2 universality bars 0.12
  vs 0.007 (tax) and 0.010 (worst threshold) (12-17x); V4 paired
  flat bar 0.5*dCT_rise + 0.06 vs |0.001| (~96x); V5 shuffled bar
  0.15 vs 0.015 (10x); V1 channel windows vs realized d^ =
  0.228/0.252 (rising, target 0.2) and 0.180/0.447 (flat, targets
  0.15/0.4); V6 exact-binomial on all uniform-control cells. Every
  margin >= 1.3x.
pilot: |
  ONE pilot, seed 20260926, full harness, ~10 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: rising
  CT 1.152 (q=0.35) -> 1.225 (q=0.65), dCT_rise = +0.0727; equal-q
  two-sample class CT 1.159 vs 1.152 (gap 0.007, worst threshold
  gap 0.010); flat CT 0.676 -> 0.677 (dCT_flat = +0.001); shuffled
  discount 0.015; rate-face CT_none 1.285 (rising) / 0.670 (flat).
prediction:
  V1_channel: realized d^ within (0.1/0.08/0.15) windows of targets
  V2_universality: equal-q classes agree -- tax gap <= 0.12 AND worst
    per-record threshold gap <= 0.12
  V3_rising_tax: CT_W(q=0.65) - CT_W(q=0.35) >= 0.03 at the rising
    instance r=(0.0,0.8,0.3), D=(0.2,0.2)
  V4_flat_paired: |dCT_flat| <= 0.5*dCT_rise + 0.06 at the flat
    instance r=(0.3,0.7,0.2), D=(0.15,0.4)
  V5_shuffled_null: shuffled-context discount <= 0.15
  V6_uniform_exact: exact-binomial consistency on every
    uniform-control cell
falsification: V3 failing (or a rising-instance DECREASE beyond bar)
  refutes Theorem 2's sign law operationally; V2 failing refutes
  Theorem 1's access-class universality operationally; V4 failing
  refutes the regime map's flat classification; V5/V6 are instrument
  gates -- their failure is instrumentation per PROTOCOL 5.1
  (dated-amendment rerun only), as is a V1 channel-window miss.
design:
  stopping: fixed design, single governed run, seed 20260927
  (T=400 vs pilot 240, means unchanged per the 054 precedent), after
  the one disclosed pilot (seed 20260926); no further pilots or
  attempts under this ID
  runtime: ~20 s single-threaded (pilot: ~10 s at T=240)
controls: [equal-q analytic-equality (V2), paired flat contrast
  never a bare sign gate (V4), shuffled-context null (V5),
  exact-binomial uniform cells (V6), pre-instrument design freeze at
  commit b1984fb]
amendments:
  - date: 2026-08-05
    what: "Governed run (seed 20260927) FAILED V6 only -- one
      uniform-control cell of 216 (rising q=0.65, consumer-B curve,
      rb=0.95: pooled control error 0.805 vs chance 0.875, control
      luckier than chance at z~4.2). Physics gates 5/5 PASS
      (dCT_rise +0.084, universality 0.009/0.005, flat -0.002,
      shuffled 0.011). Per this prereg's falsification clause V6 is
      an instrument gate: logged instrumentation miss, dated-
      amendment rerun ONLY -- all bars held unchanged, no code
      change; as-executed artifact preserved at
      results/GO13-operational-face-asexecuted.json. Rerun governed
      seed 20260928. Known-fragility note for FUTURE registrations
      (not this one): 216 cells at per-cell alpha=5e-4 carries
      family-wise false-positive mass ~0.1; successors should
      family-correct. Prior hash:
      e70170ba2081c05a94587265866f723919b93de0a738c3cf2476c09a10679303"
hash: sha256:4c7ee404e441ed8bc4191a0227c0943cff9e9edece257cf938b1421c5425330c
```

## Falsification

A pass makes GO-13 `[demonstrated]` at the operational tier: both
theorems carry a measured face — the tax's rise under staleness and
the equal-q equivalence of structurally different access classes —
on materialized records with the sealed instrument lineage.
