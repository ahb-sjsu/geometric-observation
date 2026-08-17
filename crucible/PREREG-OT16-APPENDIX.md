# OT-16 appendix — the noisy cliff, measured

**STATUS: SEALED 2026-08-17 02:55 PDT, BY RECORDED OWNER OVERRIDE of
the same-day rate-limit rule — the program's sixth recorded
exception, and the first on the crucible side since the Third
Crucible's seal.** The family (FP3N, `FAMILY-P3N.md`) was
constructed and interior-qualified earlier this same session,
including the N4 arm added at the owner's instruction immediately
before this seal. Mitigation as in the RPKI cell: **the graded run
uses a fresh seed (20260818)** — every number below binds to draws
no eye has seen; the shakedown (seed 20260817) qualified knobs, not
outcomes. Runner: `ot16_check.py` (refuses unsealed appendices; one
of two budgeted instrument revisions available, no final-revision
clause). Result: `results/OT16-noisy-cliff.json`, committed as
executed.**

## Claim under test

P3's owed prediction (readscope `PRINCIPLES.md` v0.2), armed by
`OT3-NOISY-THEOREM.md`: observation noise floors identification at
`k ≥ d` at an error **derivable from σ and the spectrum gap**
(N2a: ∝ σ√d/γ), while **the cliff's location does not move** (N1a:
Ω(1) below full coverage at every σ; N4: relocated to d−k₀ by side
information, never softened). PASS discharges the owed prediction —
theorem and measurement agreeing on both faces and the shift. FAIL
is a model-mismatch finding against the oracle instantiation and is
kept as executed.

## Sealed design (family constants inherited from FP3N verbatim)

Seed **20260818**; d ∈ {16, 32, 64}; spectra gapA (γ = 0.2), gapB
(γ = 0.8); x ∈ {0.03, 0.1, 0.3, 1, 3} with σ = x·γ/√d (main) and
σ = x·γ/√(d−k₀) (N4, d = 32, k₀ ∈ {8, 16}); 20 trials/cell; decisive
band x ≤ 0.3; arms `cell_full`, `cell_confined`, `cell_sideinfo`
imported unchanged from the family module.

## Manipulation checks (any failure → VOID)

- **MC1 (interior on the fresh seed):** every main (d, spectrum)
  cell has ≥ 2 interior points (full-face median ∈ (0.05, 0.7));
  in-band trial IQR ≤ ⅓ of the face separation, per cell.

## Bars

- **B1 (linearity and the √d/γ collapse):** every main cell's
  decade ratios (x = 0.03→0.1→0.3) lie in [0.8, 1.25]; and the
  per-cell slope s = mean over in-band x of (median error)/x
  satisfies max(s)/min(s) ≤ **1.5** across all six (d, γ) cells —
  the collapse is the scaling law, quantified.
- **B2 (the confined face):** every in-band confined median ∈
  [0.65, 0.78] (1/√2 ± 10%), and each cell's in-band range ≤ 10% of
  its max.
- **B3 (the step, resolved):** at x = 0.03, confined/full median
  ratio ≥ **10** in every main cell.
- **B4 (N4 — the cliff moves and stays a cliff):** for every
  (k₀, spectrum): W-full median at x = 0.1 ∈ [0.05, 0.2] and every
  in-band W-minus-one median ∈ [0.65, 0.78].

**Kill conditions, named in advance:** any in-band confined median
< 0.5 refutes confinement itself (the cliff leaking); any main-cell
decade ratio outside [0.5, 2] refutes the linear-floor model. Either
is a FAIL with that specific meaning, not a VOID.

**PASS = MC1 ∧ B1 ∧ B2 ∧ B3 ∧ B4.** On PASS, P3's owed prediction
is discharged and `PRINCIPLES.md` records it as an instance; on
FAIL, the record stands and the owed prediction remains open with
the mismatch named.
