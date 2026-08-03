# GO-P-2026-049 — Staleness operational v2: pooled chance-relative control gate

Supersedes **GO-P-2026-048** (registered MISS 4/5, reported at full prominence in
[`experiments/GO-landauer-staleness-NOTES.md`](../experiments/GO-landauer-staleness-NOTES.md)):
all four physics gates passed — the reset threshold climbed 0.100→0.550 with record
age, tracking $R_c-1+h_2(\hat d*q_t)$ within one grid step at every age — and the
single failure was a **multiplicity error in the control gate**: one 2.3σ binomial
excursion (age 4, $r_b$ 0.475: 0.82 vs chance 0.875) among ~64 per-cell tests, each
slack-set at ~2σ. The control decoder never reads $x_t$, so its behavior is
age-independent by construction; v2 pools the control over ages per bin rate (1600
trials, SE≈0.008) and gates two-sided at 4σ of the pooled binomial SE. Physics gates
S1–S4 are **identical** to 048 for comparability; fresh seed. Governs
`experiments/landauer_staleness.py` (v2 gate + seed);
result `results/GO-landauer-staleness-v2.json`.

```yaml
id: GO-P-2026-049
date: 2026-08-03
retrospective: false
kind: operational Monte Carlo (Tier B, v2; supersedes GO-P-2026-048 -- control-gate statistics corrected, physics gates unchanged)
claim: "Aging the retained side information raises the operational reset threshold of a fixed stored record exactly as the staleness-work complement prices it."
harness: experiments/landauer_staleness.py   # v2 gate, fresh governed seed 20260808
prediction:
  S1_threshold_monotone: nondecreasing across all eight ages  [identical to 048;
    measured there 0.100 -> 0.550]
  S2_tracks_prediction: |thr_meas - thr_pred| <= 0.11 for ages {0,1,2,4,8,16}
    [identical; measured devs 0.015-0.080]
  S3_same_binrate_flips_with_age: err(r_b=0.175) <= 0.10 at age 0 and >= 0.90 at
    ages {32,64}  [identical; measured 0.01 -> 1.00/1.00]
  S4_channel_realized: d^ in [0.10, 0.17]  [identical; measured 0.1172]
  S5_no_si_control: per r_b, |pooled-over-ages control error - pooled chance level|
    <= 4 sigma of the pooled binomial SE  [CORRECTED: pooling is exact since the
    control never reads x_t; kills the per-cell multiplicity that failed 048]
falsification: as GO-P-2026-048; additionally a physics-gate miss under the fresh
  seed is reported as seed instability of the staleness instance.
design:
  n: 40
  trials: 200
  ages: [0, 1, 2, 4, 8, 16, 32, 64]
  rb_grid: [0.10, 0.175, 0.25, 0.325, 0.40, 0.475, 0.55, 0.625]
  stopping: fixed design, single governed run, seed 20260808
controls: [no-side-information decoder (pooled chance-relative, 4 sigma), fixed-bin-rate age flip, channel window]
amendments: []
hash: sha256:f1c5a01563ae565f60c59c5c3911e2c873e6ebc16b65b6db04748461772705b2
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2. CI re-checks the
committed JSON's self-consistency (tamper check) but cannot re-run Tier B.
