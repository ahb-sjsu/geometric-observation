# GO-P-2026-053 — GO-8 Gaussian setting, second (and final) attempt

Supersedes **GO-P-2026-051** (registered MISS 3/5, reported at full prominence in
[`experiments/GO-landauer-gaussian-secondsettings-NOTES.md`](../experiments/GO-landauer-gaussian-secondsettings-NOTES.md)).
In 051 the **physics gate passed** — the paper's §VI Gaussian discount predicted the
measured age-dependence to 0.154 bits/symbol over a 0.90-bit range — and the two
failures were:

1. **G3 short by one trial**: 13 errors of 120 against a bar allowing 12 (0.108 vs
   ≤0.10). This bar is **NOT moved**.
2. **G5 failing an invalid test**: at $r_b=0.35$ chance error is 0.99994, so
   $Np(1-p)=0.05\ll5$ and the normal approximation's SE is meaningless; the exact tail
   for the single observed lucky hit is $P(X\ge1)\approx5\%$.

**This attempt changes exactly two things.** G5 becomes an **exact two-sided binomial
test** (replacing an invalid instrument — a correction, not a bar move; unit-tested to
accept 051's failing cell and still reject a genuine leak). The design is **larger and
pre-committed here**: $n$ 20→22, $T$ 120→250, affordable because in-bin member sets are
now strided views rather than copies (verified index-identical on 200 random cases).
**G1, G2, G3, G4 carry over byte-identical bars.** Declared in advance: this is the
final attempt — if G3's one-trial margin was luck, the run fails again and GO-8 remains
`[demonstrated]`, and no third attempt will be registered.

```yaml
id: GO-P-2026-053
date: 2026-08-03
retrospective: false
kind: replication (final attempt at GO-8's second setting; one invalid instrument replaced, all physics bars unchanged)
claim: "On a Gaussian AR(1) source, a fixed record's operational reset threshold rises with the age of the retained side information as the paper's Gaussian side-information discount predicts."
harness: experiments/landauer_staleness_gaussian_v2.py   # imports the sealed 051 constants; governed seed 20260812; NO pilot was run
prediction:
  G1_threshold_monotone: nondecreasing across all seven ages  [unchanged from 051]
  G2_tracks_gaussian_discount: >= 6 of 7 uncensored, max|thr_meas - thr_pred| <= 0.20,
    rise ratio in [0.70, 1.30]  [unchanged from 051]
  G3_same_binrate_flips_with_age: err(r_b=0.35) <= 0.10 at age 0 and >= 0.90 at both
    ages {16, 32}  [UNCHANGED -- this is the bar 051 missed by one trial]
  G4_channel_realized: D_hat in [0.22, 0.36]  [unchanged from 051]
  G5_no_si_control_exact: pooled control success count consistent with its own chance
    level under an EXACT two-sided binomial test at alpha = 5e-4, at every r_b
    [the only gate CHANGED; the 051 normal approximation was invalid here]
falsification: any gate missing leaves GO-8 at [demonstrated]; no further attempt.
design:
  n: 22
  trials: 250
  phi: 0.9
  ages: [0, 1, 2, 4, 8, 16, 32]
  rb_grid: [0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.95, 1.10, 1.25]
  stopping: fixed design, single governed run, seed 20260812, no pilot
controls: [no-side-information decoder (exact binomial), fixed-bin-rate age flip, channel window]
amendments: []
hash: sha256:925bee580261f627bd462cc50f5798ff38a942ee2af4c796fe1e07fba369a3bf
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2, GO-8 keeps
`[demonstrated]`, and the Gaussian setting is recorded as a standing near-miss.
