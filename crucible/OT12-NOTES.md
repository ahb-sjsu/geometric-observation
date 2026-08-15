# OT-12 notes — VOID, final; and the void contains adverse evidence

**Verdict: VOID** (v2 window: zero cells with informative fraction
strictly inside (0.10, 0.90) against a required 3; v2 was the declared
final instrument revision, so OT-12 closes VOID). v1's vacuous pass and
v2's results are both committed as executed.

## What the two runs established about the instrument

The informative-fraction transition of this family is intrinsically
cliff-like: 30/30 → 0/30 across one grid step in v1 (coarse grid) and
0/30 → 30/30 across one step in v2 (rms-derived grid, from the other
side). The claim's first curve — a *gradually decaying* informative
fraction — does not exist in this family at any grid we are permitted
to try. A family with a genuinely gradual informative decay (e.g.,
per-pair heterogeneous response scales) was not designed in advance,
and the final-revision rule forbids designing it after seeing this.

## The adverse evidence, recorded but ungraded

In v2's graded cells the *second* curve did the failing:

| g (step/rms) | DF | informative | accuracy |
|---|---|---|---|
| 1546 (≈1×) | 0.031 | **30/30** | **0.633** |
| 5152 (≈0.3×) | 0.062 | **30/30** | **0.633** |
| 15456 (≈0.1×) | 0.156 | 30/30 | 0.833 |
| 51521 (≈0.03×) | 0.406 | 30/30 | 0.867 |

Every pair informative, and accuracy well below ceiling — the exact
shape the frozen kill condition names ("accuracy sags below ceiling
while informative pairs remain in meaningful number"). Two readings
are compatible with this instrument and cannot be separated by it:
(a) the revised floor law is wrong — near the floor there is a *band*
of degraded fidelity, not a clean step; (b) the damage estimator is
contaminated — at step ≈ rms, quantization noise on the measured
damage differences flips signs that the true damage ordering does not
flip, so the sag is in the measurement, not the metric. v0.1's OT-5
saw no such band because its family (temperature) hit a float64 cliff
rather than a resolution-scaled floor. Distinguishing (a) from (b)
requires an estimator-noise-aware design that would have to be sealed
fresh — it cannot be bolted onto this test after the fact.

## Campaign consequence, applied without flinching

`OT-CRUCIBLE-2.md` H2 requires **both revision tests to PASS**. VOID
is not PASS. **The Second Crucible's graduation is foreclosed as of
its first test**, whatever OT-8/9/10/11 do. The remaining tests retain
full value for the record (three of them test the *unrevised*
survivors), but v1.0 cannot be declared on this arc. The P5 revision
now carries: refuted-as-monotone (v0.1), floor-law untested-with-
adverse-signals (v0.2). Any v0.3 must first build the family this
test needed — gradual informative decay with an estimator-noise
budget — and must treat the 0.633 band as the thing to predict.

Instrumentation lesson added to the earned list: **a two-curve claim
needs a family where both curves have interior points, verified before
sealing bars on either** — the interior-coverage check must be part of
the *family design*, not just the run window.
