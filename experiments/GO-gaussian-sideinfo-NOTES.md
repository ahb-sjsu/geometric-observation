# GO-P-2026-044 — post-run notes (Gaussian side-information harness, run 2026-08-03)

Harness: [`verify_gaussian_sideinfo.py`](verify_gaussian_sideinfo.py) ·
prereg [GO-P-2026-044](../prereg/GO-P-2026-044-gaussian-sideinfo-region.md)
(sealed `6dd944f`) · Tier A (CI) · governed run on Atlas at the sealed commit.
**VERDICT: ALL PASS.**

## What it nets

The paper's Gaussian-with-reset-side-information section (Props "scalar
Gaussian corner" and "vector frontier / reset water-filling", added for the
T-IT revision): the scalar region is a single-corner quadrant with no
rate–work tradeoff and side-information discount → I(X;S) as D→0; the vector
frontier reappears through distortion allocation across modes the reset
context knows unequally well.

## Per section

| section | result |
|---|---|
| [1] moment converse | LMMSE algebra e_lin=(1−ρ²)(v−c²)/(v−ρ²c²) exact to 3.2e-16 on 2,000 random (ρ,c,v); grid min of ℓ(c,v) matches the closed form and minimizer (1−D,1−D) to 3.5e-4 |
| [2] Gaussian family | L pinned by R (single curve) to 1.8e-15 on 3,000 channels |
| [3] quantizer net | 400 non-Gaussian K-level quantizer channels (erf-exact R, L, D) — zero bound violations |
| [4] discrete corner | 41×21-quantized source + eq.-(20) optimizer reproduces the analytic corner ≤0.017 bits; the corner **degeneracy** (α=0 and α=1 same point) holds to 4 decimals |
| [5] allocation program | KKT+feasibility 1.75e-14 over 30 instances × 4 α; 600k random allocations never beat the frontier |
| [6] strictness + separability | registered example ρ=(0.95,0), D=0.5: L-gap **0.1105**, R-gap **0.1306** (the paper's "about 0.11 / 0.13 bits"); full-channel optimizer never beats the per-mode envelope on the same grids (α=1 exact to 4 decimals) |
| [7] discount | monotone in D, → I(X;S) at D→0 |

## Net-design lesson (logged in the prereg, pre-seal)

The first pilot gated the full-channel (R,L) against the **analytic
continuous endpoints** and failed at α=0 — a design artifact: the α=0
minimizer does not pin R, and coarse grids push the discrete optimum above
the continuous value in the unconstrained coordinate. Redesigned before
sealing into the **exact-to-exact separability net** (full-channel vs
per-mode envelope on the same quantized source), which is strictly stronger:
grid coarseness cannot false-fail it, and a joint channel beating the
envelope would refute the separability step of the vector converse.

## Companion verification

Fresh-context R-IND-5 pass on both propositions: **CONFIRMED, 0 errors, 5
sharpenings** (ledger **VI-9**), including exact refutation of the suspected
non-convexity of the per-mode work term. All sharpenings folded into the .tex
before seal.
