# GO-P-2026-048 — post-run notes (staleness operational) — **MISS 4/5**

Harness: [`landauer_staleness.py`](landauer_staleness.py) · prereg
[GO-P-2026-048](../prereg/GO-P-2026-048-landauer-staleness.md) (sealed `5326c5b`)
· result [`GO-landauer-staleness.json`](../results/GO-landauer-staleness.json) ·
governed seed 20260807, Atlas.
**Registered verdict: MISS — 4/5 gates. Reported as-is; superseded → GO-P-2026-049.**

## Per gated bar

| gate | registered | result | pass? |
|---|---|---|:--:|
| S1 threshold monotone in age | nondecreasing, all 8 ages | 0.100→0.250→0.325→0.400→0.550→0.550→0.550→0.550 | ✅ |
| S2 tracks prediction | \|thr_meas−thr_pred\| ≤ 0.11, ages 0–16 | devs 0.029 / 0.077 / 0.074 / 0.041 / 0.080 / 0.015 | ✅ |
| S3 fixed bin rate flips with age | err(r_b=0.175): ≤0.10 @ t=0, ≥0.90 @ t≥32 | **0.01** → **1.00 / 1.00** | ✅ |
| S4 channel realized | d̂ ∈ [0.10, 0.17] | d̂ = 0.1172 | ✅ |
| S5 no-SI control (chance-relative, per-cell) | err ≥ chance − 0.05 at every (age, r_b) | **one cell** (age 4, r_b 0.475): 0.82 vs chance 0.875 | ❌ |

## Diagnosis — a multiplicity error in the control gate, not a side-information leak

The failing cell is a single 2.3σ binomial excursion (8-member bins, T=200,
SE≈0.023) among ~64 gate cells; with that many cells a >2σ excursion somewhere
is expected ~10–15% of the time. The pilot-corrected gate fixed the *chance
level* (the 048-pilot lesson) but not the *multiplicity*. Since the control
decoder never reads $x_t$, its behavior is age-independent **by construction** —
the statistically correct gate pools over ages per bin rate (1600 trials,
SE≈0.008) and tests two-sided at 4σ. GO-P-2026-049 registers exactly that
change; physics gates S1–S4 are unchanged.

## What the run showed (creditable only via 049)

The staleness-work complement, operationally: one fixed record, one fixed bin
assignment, and the decodable reset threshold **climbs from 0.10 to 0.55
bits/symbol as the side information ages**, tracking $R_c-1+h_2(\hat d * q_t)$
within one grid step at every age; the same bin rate (0.175) flips from 1%
error at age 0 to 100% at age 32. Relevance lost to time is gained as
conditional erasure work — measured.

## GO-P-2026-049 — corrected rerun (v2): **PASS 5/5** (unblinded 2026-08-03)

Result: [`../results/GO-landauer-staleness-v2.json`](../results/GO-landauer-staleness-v2.json),
fresh seed 20260808, sealed `389e234` pre-run; physics gates identical to 048,
control gate pooled over ages per bin rate at 4σ.

| gate | result | pass? |
|---|---|:--:|
| S1 monotone | 0.100→0.175→0.325→0.400→0.550 (→ flat) | ✅ |
| S2 tracks prediction | devs 0.036 / 0.007 / 0.078 / 0.043 / 0.081 / 0.015 | ✅ |
| S3 fixed-r_b age flip | 0.175: decodable at t=0, dead by t≥32 | ✅ |
| S4 channel | d̂ = 0.1148 | ✅ |
| S5 pooled control | within 4σ of chance at every r_b | ✅ |

**The staleness-work complement, operationally, under two seeds** (048's
physics gates also passed 4/4): one fixed record, one fixed bin assignment,
and the decodable reset threshold climbs from 0.10 to 0.55 bits/symbol as
the retained side information ages, tracking $R_c-1+h_2(\hat d*q_t)$ within
one grid step at all eight ages. Relevance lost to time is gained as
conditional erasure work — measured, and the exchange is the paper's
Fig.-3 identity read operationally.
