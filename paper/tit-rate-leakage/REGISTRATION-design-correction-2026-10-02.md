# Design correction: frozen directions in the replicate designs

Registered 2026-10-02, before any number under it was computed. Code:
`ot_crossfit_c.py`. It supersedes phase B of the protocol amendment
(`ot_crossfit_b.py`), which was stopped part-way. Its partial output is
discarded as confounded.

## The error

Registrations 4 (`ot_s2noise.py`, fec42f0) and 5 (`ot_nearboundary.py`,
ae487c4) describe the measured directions as frozen from split 0. Their code
recomputed two things on every replicate split:

1. **The principal read b_R.** In the GaussCoupled controls the top
   eigenvalue of the decoder's pencil is nearly degenerate (relative eigengap
   0.005–0.020), so b_R switches between two orthogonal directions on some
   splits (`diag_s21-2026-10-02.txt`).
2. **The context column of the rotated (mix and orth) views,** the column
   least correlated with Z_R. It changes between splits on most real
   datasets, on up to every seed (`bR_stability-2026-10-02.txt`).

So on most splits a rotated-view case measured the frozen aware code against
a view it was not built for. Views that are a single context column are not
affected, and neither are the single-split registrations: the boundary test,
the Gaussian-departure registration, registration 3, and phase A.

## Measured impact on registration 4's real cases (descriptive)

| Views | Cases | Median shortfall (pred − mean over splits) | More than 3 SE from the prediction |
|---|---|---|---|
| Context-column views, unaffected | 20 | +0.010 bit | 90% |
| Mix and orth views, affected | 51 | +0.047 bit | 76% |

## The correction

- For every case, b_R and the context column are computed once on split 0
  and frozen.
- On each split the view is rebuilt from them under that split's
  standardization, and both codes use the frozen directions.
- Measurement follows the corrected protocol (`ot_crossfit.py`): cross-fitted
  adversary selection and paired per-sample differences.

**Controls.** The GaussCoupled controls are excluded from scoring and
reported separately, because their principal read is not well defined. The
Gauss8 controls (eigengap about 0.27) remain the control group. For
registration 5 that leaves P1c with 20 control cases, above its vacuity
threshold of 10.

**Unchanged:** case rules, seeds, adversary families, criteria, and the
scoring code. Registration 4's scoring block is copied verbatim. Registration
5 is scored by `ot_nearboundary.score`.

## Reporting

The original replicate results of registrations 4 and 5 stay on record,
marked as confounded for rotated views. The corrected results are reported
beside them.
