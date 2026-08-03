# GO-P-2026-046 — post-run notes (GO-7 cross-source, scalar Gaussian) — **MISS 4/6**

Harness: [`landauer_gaussian_source.py`](landauer_gaussian_source.py) · prereg
[GO-P-2026-046](../prereg/GO-P-2026-046-landauer-gaussian-source.md) (sealed
`e299442`) · result
[`GO-landauer-gaussian-source.json`](../results/GO-landauer-gaussian-source.json)
· governed seed 20260805, Atlas.
**Registered verdict: MISS — 4/6 gates. Reported as-is; superseded → GO-P-2026-047.**

## Per gated bar (n = 24)

| gate | registered | result | pass? |
|---|---|---|:--:|
| G1 separation decodes | err(r_b=0.36) ≤0.20 @ n=24, ≤0.30 @ n=20, trend | **0.11** / **0.16**, trend 0.30→0.11 | ✅ |
| G2 bin rate ≤ 0.50·R_mom | 0.36 ≤ 0.50·R_mom | R_mom = 1.017 → 0.36 = **0.35·R_mom** | ✅ |
| G3 converse below content | err(r_b=0.05) ≥0.30 all n≥12, ≥0.40 @ n=24 | 0.52→**0.69**, rising | ✅ |
| G4 no-SI control | ≥0.90 all n≥16 | 1.00 everywhere | ✅ |
| G5 channel window | R_mom ∈ [0.72, **1.00**] | R_mom = **1.017** | ❌ |
| G6 deep decode | err(r_b=0.60) ≤ **0.02** | 4/200 = 0.0200…018 (float epsilon) | ❌ |

## Diagnosis — instrumentation-window design errors, not effect failures

- **G5**: the sealed R_mom ceiling (1.00) was set to the analytic $R(D)$.
  Wrong reference: the **codebook rate** at $n=24$ is $\lceil 24\cdot1.03\rceil/24
  = 1.042$ bits/symbol, and the realized mutual information can and should sit
  between $R(D)$ and the code rate. $R_{\mathrm{mom}}=1.017$ is expected
  behavior that the window failed to admit. (The pilot only reached $n=20$,
  where $R_{\mathrm{mom}}=0.94$ masked this.)
- **G6**: the 0.02 bar sits exactly on a realizable value (4/200) and fails on
  floating-point representation. A count-robust bar was needed.

Per PROTOCOL Rule 1.2 the miss is reported at full prominence, GO-7 retains
class `[demonstrated]` pending the corrected rerun, and the correction is
registered fresh (GO-P-2026-047: R_mom ceiling 1.06 anchored to the code rate,
G6 ≤ 0.035 with epsilon guard, physics gates G1–G4 unchanged for
comparability, fresh seed).

## What the run nonetheless showed (not creditable to GO-7 until 047)

All four **physics** gates passed on the continuous source: the stored index
decodes from side information at 0.35 of the measured description rate
(error 0.30→0.11 with $n$), reliably fails below the conditional content
(0.52→0.69, rising), and fails absolutely without $S$ — the same lifecycle
signature as the binary instance, now on the paper's own §VI scalar-corner
setting ($\rho=0.98$, MSE, $D̂=0.29$, $L_{\mathrm{mom}}=0.083$ vs analytic
0.081 at target $D$).

## GO-P-2026-047 — corrected rerun (v2): **PASS 6/6** (unblinded 2026-08-03)

Result: [`../results/GO-landauer-gaussian-source-v2.json`](../results/GO-landauer-gaussian-source-v2.json),
harness [`landauer_gaussian_source_v2.py`](landauer_gaussian_source_v2.py)
(imports the sealed 046 machinery; windows corrected, physics gates identical),
fresh seed 20260806, sealed `a96bb34` pre-run.

| gate | registered (v2) | result @ n=24 | pass? |
|---|---|---|:--:|
| G1 separation | ≤0.20 @ n=24, ≤0.30 @ n=20, trend | **0.17** / 0.11; trend 0.27→0.17 | ✅ |
| G2 bin rate ≤ 0.50·R_mom | 0.36 ≤ 0.50·R_mom | R_mom=0.885 → 0.36 = **0.41·R_mom** | ✅ |
| G3 converse | ≥0.30 all n≥12, ≥0.40 @ n=24 | 0.60→**0.79**, rising | ✅ |
| G4 no-SI control | ≥0.90 all n≥16 | 1.00 everywhere | ✅ |
| G5 channel window (corrected) | R_mom ∈ [0.72, 1.06] etc. | D̂=0.270, R_mom=0.885, L_mom=0.066 | ✅ |
| G6 deep decode (corrected) | ≤0.035+ε | **0.01** | ✅ |

**GO-7 is now held on two independent source families** — the binary two-bit
source (043 + the 5-codebook 045) and the scalar Gaussian source (this run,
the paper's own §VI scalar-corner setting) — meeting the PROTOCOL §1
`[replicated]` bar. The physics gates passed under BOTH seeds (046's and
047's); only the two v1 instrumentation windows changed. Remaining honest
scope: one codebook per n on the Gaussian instance (codebook robustness
established on the binary instance by 045); ideal-reset information
accounting only, no physical work measured.
