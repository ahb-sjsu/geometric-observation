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

## N4 arm: DEMONSTRATED (added 2026-08-17, same record)

Side-information cells at d = 32, k₀ ∈ {8, 16}, both spectra, σ
normalized by √(d−k₀): **W-full behaves exactly as the upper face
with d_eff = d−k₀** (medians 0.027–0.032 / 0.076–0.105 / 0.254–0.316
at x = 0.03/0.1/0.3 — the error ≈ x collapse again), and
**W-minus-one pins at 0.707–0.774** across the decisive band. The
cliff relocates to d − k₀ with both faces intact inside W.

## What the appendix owes (now sealed separately)

Bars on: the slope's (d, γ) scaling (collapse quantified); the
confined face's σ-independence and 1/√2 location; the N4 shift; MCs
on grid coverage and IQR margins, band-scoped per the OT-13 lesson.
The sealed test is `PREREG-OT16-APPENDIX.md`, graded on a **fresh
seed** so this shakedown's numbers cannot grade themselves.
