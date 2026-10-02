# Registration 3 (DRAFT, not frozen): the boundary theory inside its Gaussian scope

Drafted 2026-10-02. Code `ot_scope.py`, scoring `scope_score.py`. Builds on the
boundary test (scored daca788) and the Gaussian-departure registration
(predictions ec3300d, scored 9f2a61b, blind forecast 6 of 6).

## Why

A post-hoc split (`posthoc_gamma.py`, labelled post hoc in the supplement)
suggested that the boundary test's unmet criteria hold where the departure
index Gamma is at most the frozen cut of 0.835 bit:
- C5 rank correlation 0.77 (old data) and 0.74 (fresh) below the cut;
- C2 at 64% (old) and 100% (fresh, 9 cases).

Post-hoc readings are not results. This registration tests them blind. It
also tests the onset order with the right predictor, the pencil class.

## Data

Six UCI datasets never loaded by this program before the loader check of
2026-10-02:
- Gas Turbine CO/NOx (2015 file);
- Electrical Grid Stability;
- QSAR Fish Toxicity;
- QSAR Aquatic Toxicity;
- Temperature Forecast Bias Correction;
- Appliances Energy.

Two Gaussian controls use new seeds (11, 12). The loader check computed
nothing else.

## Scope and views

A case is in scope when Gamma is at most CUT = 0.835 bit, the frozen B3 cut.

Every dataset gets the boundary test's views (each context column, and the mix
families at 5, 15, 30 and 60 degrees) at slack 0.05, 0.15 and 0.4. Two onset
families are also evaluated at slack 0.02, 0.05, 0.10 and 0.20, both built
from the context column least correlated with the principal read:
- `mix15` is not an eigenvector of the pencil, so the theory predicts a
  first-order onset;
- `orth` is that column made Sigma-orthogonal to the principal read. The read
  is then a non-top eigenvector, with zero squared correlation (the refuted
  "uncorrelated view"), so the theory predicts a second-order onset.

## Criteria

- **S0** Replication of B3: each dataset is forecast TRACK or MISS from its
  median Gamma against the cut. At least five of six correct.
- **S1** In scope, the measured removal is positive in ≥ 80% of cases
  predicted ≥ 0.10 bit, and the Spearman correlation with the prediction is
  ≥ 0.6.
- **S2** In scope, among cases predicted < 0.05 bit, |measured| ≤ 2 SE in
  ≥ 80%. Vacuous below 15 cases.
- **S3** In scope, the mix families have Spearman ≥ 0.6. Vacuous below 15
  cases.
- **S4a** In scope, the onset families are within 2 SE of their predictions
  in ≥ 80% of cases.
- **S4b** At slack 0.02, in scope, two conditions both hold:
  - `orth` cases predicted < 0.02 bit are within 2 SE of zero in ≥ 80%;
  - `mix15` cases predicted ≥ 0.05 bit are above 2 SE in ≥ 80%.

  Vacuous if either group has fewer than 3 cases.
- **K1** On the controls, Gamma = 0 in ≥ 70% of cases. This corrects the
  earlier 90% bar: four 95% tests give about 81% when every null holds.
- **K2** (reported) S1–S3 on out-of-scope cases.

## Status

Draft, committed locally, not pushed. Not frozen until pushed.
