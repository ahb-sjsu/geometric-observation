# Deduction first: the non-Gaussian defect of a leakage prediction

Written 2026-10-02 BEFORE any of the quantities below were computed on any
dataset. The induction step (data mining on the residuals, `ot_mining.py`)
comes after this file is committed, and only on what the deduction leaves
unexplained.

## Setting

A code is M = q(Z): Z is a standardized projection of the source, and q is the
3-bit Lloyd–Max quantizer for N(0,1). The cells have design probabilities p_G.
The second party sees S. The theory predicts the leakage H(M|S) as

    l_G = h_gauss(R²),

where R² is the linear predictability of Z from S. This is exact when (Z, S)
is jointly Gaussian.

## An exact identity

H(M|S) = H(M) − I(M;S). Under the Gaussian model, H_G(M) = H(p_G) and
I_G(M;S) = H(p_G) − h_gauss(R²). So the prediction error of one code is

    e := H(M|S) − l_G = δ_marg − δ_dep,
    δ_marg = H(p) − H(p_G)          (marginal defect: cell occupancy p vs design),
    δ_dep  = I(M;S) − I_G(M;S)      (dependence defect: information beyond the Gaussian).

This is an identity, not an approximation. The measured leakage is the best
adversary's cross-entropy, which exceeds H(M|S) by an adversary gap g ≥ 0. So
the measured error is e + g.

For a case (principal code R, aware code A), the error in predicted removal is

    measured removal − predicted removal = (e_R + g_R) − (e_A + g_A).

## Estimating the two defects from training data, with no fitted parameters

- **δ_marg** is computed exactly from the training-half occupancy of the
  code's cells.
- **δ_dep**: data processing gives I(M;S) ≤ I(Z;S) = I_G(Z;S) + dep, where
  dep = I(Z;S) − I_G(Z;S) is the continuous dependence defect. dep is
  estimated by the mixed k-NN estimator, minus the mean of a Gaussian null of
  the same n and r, which removes the estimator's bias. To first order, assume
  quantization keeps the same fraction of the excess information as it keeps
  of the Gaussian information:

      δ_dep ≈ κ · dep,   κ = I_G(M;S) / I_G(Z;S) = (H(p_G) − h_gauss(R²)) / (−½ log2(1 − R²)).

  κ is fixed by R² and the quantizer.

**Formula.**

    ê = δ_marg − κ·dep,
    corrected removal = h_gauss(R²_R) − h_gauss(R²_A) + ê_R − ê_A,
    predicted miss    = |ê_R − ê_A|.

It has no free parameters. It reduces to the Gaussian theory when both
defects vanish.

## What the deduction predicts, stated before computing

- **P1.** The corrected removal tracks the measured removal better than the
  Gaussian prediction: higher Spearman, lower mean |miss|.
- **P2.** The predicted miss |ê_R − ê_A| ranks the actual miss at least as
  well as Gamma does (retrodiction R1 was 0.708).
- **P3 (mechanism).** On the held-out half, δ_marg can be computed exactly.
  The remainder (δ_marg − measured error) is the dependence defect plus the
  adversary gap. The datasets that missed (Wine, Zoo, Fires, Yacht, RedWine)
  should show large defects. Which defect dominates is not predicted here. It
  is what the mechanism measurement is for.
- **P4 (limits).** κ·dep is an upper-bound-style first-order term. The
  adversary gap is not modelled. Where the formula fails, the induction step
  looks for the characteristic responsible. Any term it finds is a hypothesis
  for registration 3, not a result.

## Ablation, fixed in advance

Three variants are compared:
- marginal defect only (ê = δ_marg);
- dependence defect only (ê = −κ·dep);
- both.

No other variants are tried.
