# OT-5 notes — FAIL, and what actually happens at the boundary

**Verdict: FAIL** (V3: Spearman(accuracy, DF) = 0.543 vs bar 0.80;
v2 was the declared final revision). v1 VOID (knob never reached
selection — float64 softmax stays measurably responsive until
gap/T ≈ 700) and v2 results are both committed as executed.

The measured shape, which is the valuable thing:

| T | measured DF | trace-metric accuracy |
|---|---|---|
| 3 … 0.01 | 1.00 – 0.98 | 0.93 – 1.00 |
| 0.003 | 0.63 | **1.00** |
| 0.001 | **0.094** | **1.00** (30/30 informative) |
| 0.0003 | 0.016 | — (0/30 informative → chance convention) |
| 0.0001 | 0.000 | — (0/30) |

**The frozen claim predicted monotone degradation. The truth is a
step.** `tr(P_C Σ_δ)` does not slowly rot as the consumer sharpens —
it stays at ceiling accuracy even at DF = 0.094, where the consumer
responds to fewer than one in ten perturbations, and then it goes
*silent* (every trace difference and damage difference exactly zero)
rather than wrong. The failure mode at the regime boundary is
**refusal, not error** — which is a kinder boundary than the theory
predicted, and, notably, exactly the behavior readscope's regime gate
was built around.

Scoring, as sealed: V1 PASS (smooth end at ceiling), V2 PASS (sharpest
cell at chance by the declared convention), **V3 FAIL** (no monotone
coupling — the step breaks it), V4 PASS (the metric never lied while
DF was high; the *kill* condition of the original claim did not
occur). The claim as frozen dies; the campaign records its first
failed test.

**What may and may not be concluded.** P5's *principle* ("the quadratic
form predicts damage exactly where the consumer is differential") is,
if anything, over-satisfied — it kept predicting far deeper into the
sharp regime than the owed prediction dared. What died is the owed
prediction's *shape*: "degrades monotonically" was the wrong
sharpening. Under the freeze rules, no principle text changes before
campaign closure; the post-campaign revision candidate is recorded
here for then: *a floor law — the metric holds while any differential
signal exists, and fails closed (silence) at the response floor* —
which would need its own registration and a family where the
informative count decays gradually, to distinguish it from this
family's sharp float64 floor.

**Campaign arithmetic after OT-5:** G1 now requires OT-4 to pass
(3 of the needed 4 are banked; OT-5 is spent), OT-6 remains necessary,
G3 already satisfied by OT-3. The Crucible has teeth; this is what
they look like.
