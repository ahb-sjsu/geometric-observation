# Registration 5: the corrected near-boundary test

Registered 2026-10-02. Code `ot_nearboundary.py`. Builds on registration 4
(9fa0d23).

## Why

Registration 4 scored BIAS by its fixed reading. A post-hoc comparison
(`posthoc_s2noise.py`) then showed two things.

1. Every earlier near-boundary criterion compared the measured removal with
   zero, although its cases are predicted at 0.03–0.05 bit.
2. Compared with the prediction instead:
   - on Gaussian controls, the 20-split means sat within 0.006 bit of it;
   - on real in-scope data, they sat near zero, a shortfall of about
     0.04 bit.

Those readings were made after the scoring. This registration tests them
blind and asks which form the real-data shortfall takes.

## Data and cases

Six public datasets never loaded by this program before the loader check of
2026-10-02:
- Seoul Bike Sharing;
- Liver Disorders;
- Computer Hardware;
- AI4I 2020 Predictive Maintenance;
- Metro Interstate Traffic;
- Beijing PM2.5.

Two new Gaussian controls use seeds 21 and 22.

Views are rotated from the decoder's principal read toward the
least-correlated context column by 1, 2, 3, 5 and 8 degrees, at slack 0.02,
0.05, 0.10 and 0.20. The predict stage selects the cases with
0 < predicted removal ≤ 0.15 bit and records each case's Gaussian departure
and scope flag (cut 0.835 bit, frozen in registration 2). It is pushed
before the measure stage runs. Each selected case is measured on 10 splits,
with frozen directions and with the adversaries refit on each split.

## Criteria

Notation: m is the mean over splits, and s its standard error.

- **P1c** On the Gaussian controls, |m − pred| ≤ max(3s, 0.01 bit) in
  ≥ 80% of selected cases.
- **P1r** The same agreement on real in-scope cases, in ≥ 80%. The
  post-hoc reading of registration 4 predicts that this fails.
- **SH** On real in-scope cases, the median shortfall (pred − m) is > 0, with
  its 2.5th bootstrap percentile above 0.
- **Form of the shortfall.** Fit m = α + β·pred by least squares over the
  real in-scope selected cases, with standard errors from a bootstrap over
  cases:
  - **D1 offset:** α + 3·SE(α) < 0 and |β − 1| ≤ 2·SE(β);
  - **A1 attenuation:** |α| ≤ 2·SE(α) and β + 3·SE(β) < 1;
  - neither: the form is unresolved, and that is reported.
- **Vacuity.** The real-data criteria are vacuous below 20 cases, and P1c
  below 10.
- **Reported, not scored:** the fit clustered by dataset, and all statistics
  for out-of-scope cases.

## Order of operations

1. Push this file and `ot_nearboundary.py`.
2. Run `predict` and push `nb_predictions.json` with its sha256.
3. Run `measure`.
4. Run `score`, and report every verdict as scored.
