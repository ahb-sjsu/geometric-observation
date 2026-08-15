# OT-7 notes — v1 FAIL, v2 FAIL, v3 PASS; the full instrument trail

**Final verdict: PASS (v3, `results/OT7-invariance-v3.json`).** All four
exact laws (damage form, trace pairing, rank, loading covariance) held
at ≤ 4e-13 across every cell and transform; every graded fragile row
demonstrated GL non-invariance at share ≥ 0.95 while holding
O(d)-invariant. Three seals were needed, all instrument-side; each FAIL
JSON is committed as executed, and v3 was declared the final revision
before it ran.

**v2 → v3 (the second lesson):** v2's integer bar (0.50) failed at
d32_r4 with energy_rank flipping in only 32% of the *gentler* cond ≤ 1e2
transforms (0.94 under v1's cond ≤ 1e4, same seed): an integer
quantization's flip share measures the transform-ensemble strength, not
the taxonomy. v3 grades quantized-derived quantities on exact O(d)
invariance only, with GL fragility inherited from the parent spectrum
row — the flip share is reported descriptively. This is itself a small
finding about invariance instrumentation: **never put a bar on the flip
rate of a quantized quantity; bar the parent, require exactness under
the invariance group.**

---

Original v1 diagnosis follows.

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
