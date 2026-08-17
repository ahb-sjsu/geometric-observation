# FP3N — the noisy-cliff measurement family

**2026-08-17. Family construction + shakedown for P3's owed
prediction (theorem half: `OT3-NOISY-THEOREM.md`). Per the rate-limit
rule, no appendix may be sealed against this family before a later
working session; this document records the design and its
demonstrated interior, and deliberately sets no bars.**

## Design

The theorem's oracle model, instantiated exactly: planted rank-4 PSD
operators with declared spectra, symmetric Gaussian entry-noise on
the observed block, oblivious designs. Two arms per (d, spectrum, σ)
cell, 20 trials each (`fam_p3n_shakedown.py`, seed 20260817):

- **k = d** — full noisy block in a random basis; graded quantity is
  the rank-4 eigenspace sin Θ against the plant. N2a predicts error
  linear in σ with slope ∝ √d/γ; the σ grid is normalized as
  σ = x·γ/√d so the prediction collapses every cell onto error ≈ C·x.
- **k = d−1, adversarial plant** — leading eigenvector (e + w)/√2
  with w hidden from the design (the T1b worst case, planted on
  purpose: typical-position plants have only ~1/√d in the hidden
  direction and would mask the cliff). N1a predicts error pinned at
  1/√2, σ-independent.

Grid: d ∈ {16, 32, 64}; spectra gapA (γ = 0.2) and gapB (γ = 0.8);
x ∈ {0.03, 0.1, 0.3, 1, 3}. **Decisive band x ≤ 0.3** — above it σ
exceeds the whole spectrum and both faces saturate at ~1, which is
physics, not family.

## Interior: DEMONSTRATED (`results/FP3N-shakedown.json`)

Across all six (d, spectrum) cells:

- **Linearity of the k = d face:** decade ratios 0.97–1.12 (want 1);
  the x-normalization collapses all cells onto error ≈ x, which is
  the √d/γ slope law made visible before any bar grades it.
- **The confined face:** flat to 0.5–9.6% across the decisive band,
  at 0.708–0.715 against the predicted 1/√2 ≈ 0.707, with IQRs at
  the third decimal (d = 64, low σ: IQR 0.000).
- **Face separation:** ≥ 0.427 everywhere in-band, ≥ 10× the trial
  IQRs — the two faces are unambiguously resolvable.
- ≥ 2 interior points (error ∈ (0.05, 0.7)) per cell on the k = d
  face; the grid straddles γ/√d on both sides.

## What a future appendix owes (named, not sealed)

Bars on: the slope's (d, γ) scaling (the collapse quantified, not
eyeballed); the confined face's σ-independence and its 1/√2
location; the side-information shift (N4 arm — cliff at d − k₀ —
not yet in the shakedown and must be added before sealing); MCs on
grid coverage of γ/√d and IQR margins, band-scoped per the OT-13
lesson. Sealing: a later working session.
