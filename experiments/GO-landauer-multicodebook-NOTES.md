# GO-P-2026-045 — post-run notes (GO-7 multi-codebook replication, run 2026-08-03)

Harness: [`landauer_multicodebook.py`](landauer_multicodebook.py) (imports the
sealed 043 Part-A machinery — no code fork) · prereg
[GO-P-2026-045](../prereg/GO-P-2026-045-landauer-multicodebook.md) (sealed
`28bad3d`) · result
[`GO-landauer-multicodebook.json`](../results/GO-landauer-multicodebook.json)
· Tier B, Atlas, fresh seed 20260804, no pilot (bars derived from 043's
measured run). **Registered verdict: PASS — 6/6 gates.**

## What it resolves

GO-P-2026-043's registered few-cluster caveat (one codebook draw per
blocklength). Five independent codebooks per n; every gate applied
per-codebook, plus a new cross-codebook stability gate.

## Per gated bar (n = 32 unless stated)

| gated bar | registered | result | pass? |
|---|---|---|:--:|
| A1r separation, every codebook | err(r_b=0.26) ≤0.12 each, median ≤0.05 | {0.01, 0.03, 0.02, 0.04, 0.03}, median 0.03 | ✅ |
| A2r bin rate ≤ 0.45·median R̂ | 0.26 ≤ 0.45·R̂ | median R̂ = 0.669 → 0.26 = 0.39·R̂ | ✅ |
| A3r converse, every codebook | err(r_b=0.03) ≥0.40 each; ≥0.30 all n≥16 | {0.63, 0.72, 0.75, 0.64, 0.69} | ✅ |
| A4r no-SI control | ≥0.90, all n≥20 | 1.00 everywhere | ✅ |
| A5r channel realized, every codebook | D̂/L̂/R̂ windows | R̂ 0.658–0.675, L̂ 0.075–0.089, D̂ 0.207–0.213 | ✅ |
| A6r cross-codebook stability | spread(err @ r_b=0.26) ≤ 0.10 | **0.03** | ✅ |

## Reading

The operational rate–work separation is a property of the random-coding
ensemble, not of a codebook draw: five independent draws under a fresh seed
each decode the stored index from side information at ~0.39 of the
description rate, each fail below the conditional content, and each fail
absolutely without S.

## Scope (as sealed)

Same synthetic source and domain as 043 — this resolves the **codebook**
caveat only. GO-7 remained `[demonstrated]` after this run; the
cross-source bar is GO-P-2026-046 (scalar Gaussian source instance).
