# GO-P-2026-051 / 052 — post-run notes (Gaussian second settings) — **BOTH MISS**

Governed runs on Atlas at sealed commit `b834e79`; results
[`GO-landauer-staleness-gaussian.json`](../results/GO-landauer-staleness-gaussian.json)
and [`GO-landauer-coordinated-gaussian.json`](../results/GO-landauer-coordinated-gaussian.json).
**Registered verdicts: MISS (3/5 and 5/6).** GO-8 and GO-9 therefore **keep class
`[demonstrated]`** — the `[replicated]` upgrade did not happen.

## GO-P-2026-051, staleness on Gaussian AR(1): 3/5

| gate | registered | result | pass? |
|---|---|---|:--:|
| G1 monotone | nondecreasing over 7 ages | 0.256→0.583→0.725→0.892→1.018→1.038→1.042 | ✅ |
| **G2 tracks the §VI Gaussian discount** | max\|dev\| ≤ 0.20, rise ratio 0.70–1.30 | **max\|dev\| 0.154, ratio 0.874** | ✅ |
| G3 fixed-r_b age flip | err ≤ 0.10 @ age 0; ≥ 0.90 @ ages 16,32 | **0.108** @ age 0 (13/120 errors, bar = 12); 1.00/1.00 | ❌ |
| G4 channel | D̂ ∈ [0.22,0.36] | 0.2875 | ✅ |
| G5 pooled no-SI control | within 4σ of chance at every r_b | fails at r_b=0.35: 0.9988 vs 0.9999, 4σ = 0.00113, \|dev\| = 0.00119 | ❌ |

**The physics claim passed.** G2 is the substantive gate — the paper's Gaussian
side-information discount predicts the measured age-dependence to within 0.154
bits/symbol at every age, over a 0.90-bit dynamic range, with the rise ratio 0.87.

**G3 failed by one trial.** 13 errors out of 120 where the sealed bar allowed 12.
This is the data disagreeing with a bar I chose; it is *not* an instrument defect.

**G5 failed on an invalid statistical test — my error.** At r_b=0.35 the chance error
is 0.99994 (bins hold 16 384 codewords), so over 840 pooled trials the expected
number of lucky uniform hits is **0.05**; one occurred. Exact/Poisson tail:
P(X≥1) ≈ 5%, entirely ordinary. But the gate used a *normal* approximation, whose SE
is 2.7e-4 here — and the normal approximation requires $Np(1-p)\gtrsim5$ while this
regime has $Np(1-p)=0.05$. The test was wrong as designed, not the control.

## GO-P-2026-052, coordinated reset on a Gaussian source: 5/6

| gate | registered | result | pass? |
|---|---|---|:--:|
| C1 S-discount on M₁ | within 0.25 of prediction | 0.823 measured | ✅ |
| C2 coordination on M₁ | ≥ 0.40·gap = **0.1331** | **0.1316** (short by 0.0015, 1.1% relative) | ❌ |
| C3 coordination on M₂ | ≥ 0.40·gap | **0.216** = 0.65·gap | ✅ |
| C4 shuffled null | no benefit | 1.121 vs 0.823; 1.515 vs 1.518 | ✅ |
| C5 channel | d̂ ∈ [0.28,0.48] | 0.3921 | ✅ |
| C6 uniform control | pooled 4σ | pass | ✅ |

Coordination saved **0.216 bits/symbol on the S-opaque record** (65% of the
asymptotic information) but only **0.1316 on M₁**, 1.1% under the sealed bar. The
asymmetry is real and interesting: M₁ already enjoys the S-discount, so the shared
component is worth less to it at finite *n*.

## Methodological note — why no v3 was launched automatically

Across this campaign five governed runs have now missed, every one on
instrument design rather than physics (046 window anchor, 048 gate multiplicity,
050-pilot two-sided null, and these two). Continuing to re-register adjusted gates
until a run passes would be **gate-tuning toward the data** — sealed preregistrations
prevent post-hoc reinterpretation of a single run, but they do not prevent that loop
across runs. The distinction that matters:

- **G5 is a genuinely invalid test** (normal approximation where $Np(1-p)=0.05$).
  Replacing it with an exact binomial/Poisson tail is a correction any statistician
  would demand, independent of the outcome.
- **G3's 0.108-vs-0.10 and C2's 1.1% shortfall are the data disagreeing with bars I
  chose.** Moving those bars would be tuning, and this file records that they stood.

The decision on whether to attempt these settings once more — and if so, only with
the invalid test replaced, the G3/C2 bars held **exactly** as sealed, and a
pre-committed larger design ($n$, $T$) — is the author's, not the assistant's.
