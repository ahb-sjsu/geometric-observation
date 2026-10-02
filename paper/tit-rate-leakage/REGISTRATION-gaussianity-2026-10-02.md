# Registration: does Gaussian departure predict where the boundary theory misses?

Drafted 2026-10-02. Companion to the boundary test of the two-observer flip
(`ot_boundary.py`, predictions `boundary_predictions.json` pushed in 7332b8c,
scoring `boundary_score.py` pushed in 86eccd7, measurement
`boundary_measured.json` and scores `boundary_score-2026-10-02.txt` in daca788).

## Why

The boundary test scored C1 PASS, C2 not met (56.1% vs 80%), C3 PASS, C5 not
met (Spearman 0.560 vs 0.6). On the two synthetic Gaussian sources every case
matched its prediction within 2 SE. Nine of eleven real datasets tracked the
prediction (per-dataset Spearman 0.81 to 0.98). Bike tracked the ranking at a
tenth of the size; Wine and Zoo were reversed.

The leakage predictions rest on one modelling step. The leakage of a 3-bit
index of a standardized projection Z depends on the second party's view S
only through the linear R²(Z; S). That is exact when (Z, S) is jointly
Gaussian. The reading under test: the misses are returns from the edge of
that model, so a measured departure from Gaussianity, computed without any
outcome, should predict where they fall. If it does, the theory forecasts
its own boundary.

## The measure (training halves only)

For one code direction b, on at most 2000 training rows:

- **dependence departure** `dep = I_np(Z;S) - I_G(Z;S)`, where I_np is the
  mixed k-NN estimator of Gao, Kannan, Oh and Viswanath (NeurIPS 2017; k = 5;
  valid with ties) and I_G = -½ log2(1 - r²);
- **marginal departure** `marg = KL(p̂ || p_G)` in bits, where p̂ is the
  occupancy of the code's eight cells and p_G their Gaussian design
  probabilities.

Each is compared with 100 bivariate Gaussian samples with the same n and r.
Its excess over the null's 95th percentile, floored at zero, is the departure
in bits. The case index is

    Gamma = excess(dep) + excess(marg), summed over the case's two codes
            (principal read b_R and aware direction b_aware).

Gamma = 0 means the case cannot be told apart from Gaussian on either count.
The outcome is `miss = |measured removal - predicted removal|`, and a case
agrees when miss ≤ 2 bootstrap SE (the boundary test's rule).

## Criteria (frozen in `ot_gaussianity.py`, copied into the predictions file)

Retrodiction on the 13 measured sources. **Not blind at the dataset level**,
because the datasets that missed are known. Nobody has computed the
case-level index before this registration is committed.

- **R1** Real datasets, principal-copy views excluded: Spearman(Gamma, miss)
  ≥ 0.3.
- **R2** Agreement rate among Gamma = 0 cases ≥ 70%, and at least 20 points
  above the rate among Gamma > 0 cases. Vacuous if either group has fewer than
  15 cases.
- **K1** Calibration: Gamma = 0 in ≥ 90% of the synthetic Gaussian cases.

Blind, on six public datasets never measured in this program (UCI Combined
Cycle Power Plant, Airfoil Self-Noise, Yacht Hydrodynamics, Forest Fires, Red
Wine Quality, Real Estate Valuation), plus a positive control (Gauss8 with
every coordinate passed through exp(0.8x)):

- **B1** Spearman(Gamma, miss) ≥ 0.3 over the fresh cases (control excluded).
- **B2** As R2, on the fresh cases.
- **B3** A dataset tracks when its per-dataset Spearman between predicted
  and measured removal is at least 0.8. The cut on median Gamma is calibrated
  on the eleven real datasets of the boundary test (by that rule nine tracked,
  and Wine and Zoo did not). It is the midpoint between the largest median
  Gamma among those that tracked and the smallest among those that did not,
  or the median of the eleven medians if the ranges overlap. Each fresh
  dataset is forecast TRACK at or below the cut, otherwise MISS. At least five of six forecasts must be correct. The forecast is
  written into `gauss_predictions.json` before any fresh code is measured.
- **K2** (reported, not scored) Gauss8-exp has median Gamma > 0 and a larger
  mean miss than Gauss8.

## Order of operations

1. Commit and push `ot_gaussianity.py`, `gauss_score.py` and this file. Run
   nothing that touches Gamma before the push.
2. `python ot_gaussianity.py predict` on Atlas. It writes
   `gauss_predictions.json` (Gamma for the retrodiction cases, the boundary
   predictions and Gamma for the fresh datasets, and the B3 forecast). Commit
   and push it with its sha256.
3. `python ot_gaussianity.py measure` writes `fresh_measured.json`.
4. `python gauss_score.py` scores everything. Report every verdict as scored.

The loader check (`ot_gaussianity.py check`, 2026-10-02) only loaded the six
datasets and ran the estimator on a synthetic Gaussian pair. It computed no
Gamma and no outcome.
