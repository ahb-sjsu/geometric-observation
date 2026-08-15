# OT-7 notes — as-executed v1 FAIL, diagnosed; v2 instrument fixes

**v1 (appendix `PREREG-OT7-APPENDIX.md`, `ot7_check.py`, seed 20260815):
FAIL as sealed.** The JSON (`results/OT7-invariance.json`) is committed
unchanged. Per-cell failures and their diagnoses:

| cell | failing row | diagnosis | claim-relevant? |
|---|---|---|---|
| d8_r1, d32_r1 | frag: eff_rank, energy_rank, waterfill | **class constants at rank 1** (≡1, ≡1, ≡[budget]) — fragility undemonstrable in principle; d32 waterfill additionally unstable: eigh noise eigenvalues (~1e-15) receive bits once the water level θ = λ·2^(−2d) drops below them | no — degenerate corner of the *instrument*, quantity has nowhere to move |
| d8_r4, d32_r4 | frag: energy_rank 0.90/0.94 vs 0.95 | **integer-valued quantity coincides by chance** in ~6–10% of GL draws; the 95% bar was written for continuous quantities | no — bar mis-specified for integers |
| d8_r8, d32_r32 | invO/frag: angles | **complete subspaces have all principal angles ≡ 0** at r = d; arccos noise near 1 (~1e-8) makes the relative comparison read O(1) | no — degenerate corner |
| d32_r32 | exact: rank | congruence amplifies cond by cond(A)² ≤ 1e8; true smallest singulars of a rank-full operator fall below the fixed threshold `s₀·1e-9·d`. Sylvester's law guarantees rank invariance; the **detection threshold** did not account for the amplification | no — numerical threshold, not the law |

**What v1 already established:** the four exact rows — damage form,
trace pairing, loading covariance, and rank away from the threshold
corner — held at ≤ 2e-10 across 600 transforms, and every
non-degenerate fragile row demonstrated non-invariance under GL while
holding invariant under O(d).

**v2 fixes (all instrument, no claim touched):** degenerate quantities
are *annotated per cell* (r=1: eff_rank, energy_rank, waterfill; r=d:
angles) and excluded from grading — the taxonomy's fragile rows are
claims about cells where the quantity can move; integer quantities
carry a ≥50% deviation-share bar; GL condition cap tightened 1e4 → 1e2
so the rank threshold has 30× margin at d=32 with no threshold
gymnastics. Sealed as `PREREG-OT7-APPENDIX-V2.md`, run by
`ot7_check_v2.py`; v1 files remain as executed.
