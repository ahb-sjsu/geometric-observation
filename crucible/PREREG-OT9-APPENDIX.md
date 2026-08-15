# OT-9 instrument appendix — sealed before the run

**Claim frozen in `OT-CRUCIBLE-2.md`: the activation-measure operator
is predicted from a synthetic-measure probe plus the OT-2 alignment
functional, beating the uncorrected synthetic probe on real heads.
Committed before `ot9_check.py` executes.**

- Heads: all 12 armH cells (Llama-3.2-3B, L{7,14,21} × H{0..3});
  consumer = the OT-1 attention-mass reader at position 96.
- **Target (the truth to predict):** `P_direct` = jacobian_probe over
  **96** real keys (positions subsampled, seed 20260815) — the
  empirical activation measure.
- **Synthetic probe:** `P_syn` = jacobian_probe over 24 draws from
  `D_p = N(μ̂_K, (1.5 σ̂_K)² I)` (mean-matched, isotropic,
  deliberately shape-mismatched; 1.5× width so the importance ratio
  to the fitted target is well-behaved).
- **The correction (the law, made operational):** model the activation
  measure as `D̂_a = N(μ̂_K, Σ̂)` with `Σ̂` = sample covariance of the
  keys + 0.1·(tr/d)·I shrinkage; per synthetic point, `A_i` from a
  single-point jacobian_probe and the change-of-measure weight
  `r_i = dD̂_a/dD_p(x_i)`; `P_corr` = self-normalized weighted mean
  `Σ r_i A_i / Σ r_i` — i.e., `P_syn + Ê[h·A]` in its exact
  importance form under the fitted model. The correction's honest
  imperfection is the Gaussian fit; that is the test.
- Grading: `err(P_x) = ‖P_x − P_direct‖_F / ‖P_direct‖_F`.
- **Manipulation floor:** median uncorrected err ≥ 0.05 across heads,
  else VOID (nothing to correct).
- **Bar T1:** corrected beats uncorrected on ≥ **10/12** heads.
- **Bar T2:** median relative improvement
  `(err_syn − err_corr)/err_syn` ≥ **0.25**.
- Verdict: floor, then T1 ∧ T2. Final instrument revision. Result:
  `results/OT9-forward-transfer.json`; ledger row OT-9.
