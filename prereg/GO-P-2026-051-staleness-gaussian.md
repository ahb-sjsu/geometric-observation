# GO-P-2026-051 — GO-8 second setting: staleness on a Gaussian AR(1) source

Registers the **second independent setting** for GO-8 (staleness–work complement,
first held on a binary symmetric Markov chain — GO-P-2026-048/049). A PASS here
meets the PROTOCOL §1 `[replicated]` bar for GO-8 ("held in ≥2 independent
settings"); a miss leaves GO-8 `[demonstrated]` and is reported at full prominence.
The setting also puts the paper's new §VI **scalar-corner discount formula** under
operational test: with $X_0\sim\mathcal N(0,I_n)$, side information
$X_t=\phi^tX_0+\sqrt{1-\phi^{2t}}Z$ has correlation $\rho_t=\phi^t$, so the
predicted threshold is
$\mathrm{thr}(t)=R_c-\tfrac12\log_2\!\bigl(1/(1-\rho_t^2+\rho_t^2\hat D)\bigr)$,
rising with age from $R_c-R$ (fresh record) to $R_c$ (dead correlation).
Governs `experiments/landauer_staleness_gaussian.py`;
result `results/GO-landauer-staleness-gaussian.json`.

**Pilot history (logged, calibration only; pilot seed = SEED+1, n=14, T=80).**
Three instrument corrections, all before sealing, none touching the physics:
1. **Grid-snapped thresholds → interpolated.** Reporting the smallest grid point
   with error ≤ 0.25 quantizes every threshold to a 0.15 step. Replaced with linear
   interpolation of the error curve's crossing.
2. **Censoring.** The rb grid topped out at 1.10, below the old-age thresholds, so
   two ages were censored; grid extended to 1.25 and censored ages excluded from the
   tracking gate by rule.
3. **Gate form.** The first form assumed a *constant* finite-$n$ offset; with
   interpolation the deviation is small but age-dependent (+0.15 young → −0.04 old,
   i.e. the measured rise is slightly compressed). Since the asymptotic formula has
   no exact finite-$n$ counterpart, G2 now gates **absolute agreement at every
   uncensored age** plus the **dynamic range ratio** — over a predicted rise of
   ~0.92 bits/symbol, that is a ~20% test. Pilot values under the sealed gate:
   max\|dev\| = 0.154, rise ratio 0.86, monotone, 7/7 uncensored.

```yaml
id: GO-P-2026-051
date: 2026-08-03
retrospective: false
kind: replication (second independent setting for GO-8; also an operational test of the Sec.-VI Gaussian discount)
claim: "On a Gaussian AR(1) source, a fixed record's operational reset threshold rises with the age of the retained side information as the paper's Gaussian side-information discount predicts."
harness: experiments/landauer_staleness_gaussian.py   # numpy; governed seed 20260810; --pilot used only for calibration
prediction:
  G1_threshold_monotone: the interpolated threshold is nondecreasing across all
    seven ages {0,1,2,4,8,16,32} (phi = 0.9)
  G2_tracks_gaussian_discount: at every uncensored age (>= 6 of 7),
    |thr_meas - thr_pred| <= 0.20 bits/symbol, and the measured dynamic range is
    0.70-1.30x the predicted range  [pilot: 0.154 max dev, 0.86 ratio]
  G3_same_binrate_flips_with_age: at fixed r_b = 0.35, err <= 0.10 at age 0 and
    >= 0.90 at both ages {16, 32}
  G4_channel_realized: D_hat in [0.22, 0.36]
  G5_no_si_control: pooled-over-ages control error within 4 sigma of its own
    chance level at every r_b (the GO-P-2026-049 gate design)
falsification: G1/G2 failing refutes the Gaussian-setting reading of the staleness
  complement (and, for G2, the operational adequacy of the Sec.-VI discount formula
  at these blocklengths); G3 failing breaks the headline exchange; G5 failing means a
  binning artifact; G4 failing voids the run.
design:
  n: 20
  trials: 120 (one codebook, one bin assignment; the record is FIXED across ages --
    age is the only manipulated variable)
  phi: 0.9
  ages: [0, 1, 2, 4, 8, 16, 32]
  rb_grid: [0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 0.95, 1.10, 1.25]
  stopping: fixed design, single governed run, seed 20260810
controls: [no-side-information decoder (pooled 4 sigma), fixed-bin-rate age flip, channel window]
amendments: []
hash: sha256:fe8fe1b5cb52942237b3e64c30678cea1347da0f3d4e2386b513eb5c8fdf43f0
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2 and GO-8 keeps
class `[demonstrated]`. CI re-checks the committed JSON's self-consistency but cannot
re-run Tier B.
