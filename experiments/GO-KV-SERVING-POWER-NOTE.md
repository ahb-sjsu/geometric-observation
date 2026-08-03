# GO-P-2026-056 design defect — the K3 gate was underpowered, computed after the fact

Written while the governed run is still executing, before its verdict is recorded,
so that the verdict is read correctly rather than reinterpreted afterwards.

## What the sealed design could actually detect

K3 required `preserve_read − destroy_read ≥ +0.15` on task score at n=40 with a
binary scorer. That is **6 of 40 items**. Exact two sided McNemar on the
discordant pairs gives, for a clean split favouring preserve,

| net discordant items | score difference | exact p |
|---|---|---|
| 3 | 0.075 | 0.250 |
| 4 | 0.100 | 0.125 |
| 5 | 0.125 | 0.0625 |
| 6 | **0.150 (the bar)** | 0.0312 |
| 8 | 0.200 | 0.0078 |

Monte Carlo power to *observe* a margin of at least 0.15 at n=40, given a true
per item effect:

| true effect | P(observed margin ≥ 0.15) |
|---|---|
| 0.05 | 0.10 |
| 0.10 | 0.30 |
| **0.15** | **0.56** |
| 0.20 | 0.78 |
| 0.30 | 0.97 |

**A true effect exactly equal to the registered bar would fail its own gate 44% of
the time.** The design can only reliably clear the bar for true effects near 0.20
to 0.30.

## Consequence for how the verdict must be read

Observed after two steering arms is `preserve 0.9250, destroy 0.8500`, a margin of
0.075, which is 3 of 40 items and McNemar p = 0.25.

Under the sealed prereg that is a **miss on K3**, and it will be recorded as a miss.
But a miss here is **weak evidence about the effect**, because the design had no
power to detect anything below roughly 0.20. The defensible statement is that the
end to end task effect on this model and task is **smaller than 0.15 and not
resolvable at n=40**, not that it is absent. Those are different claims and only
the first is supported.

The mechanism result is unaffected and rests on separate evidence. In the
consumer's own metric, error steered into the read subspace raises attention KL by
15 to 36 times over error steered into the complement, unanimously across 10 of 10
heads in all 15 configurations tested. That measurement has enormous power because
it is a continuous quantity measured per head, not a binary outcome over 40 items.

## Sample sizes this question actually needs

Items required for 80% power to reach p < 0.05, same paired binary setting.

| true effect | items needed |
|---|---|
| 0.20 | 80 |
| 0.15 | 150 |
| 0.10 | 300 |
| 0.075 | 300 |
| 0.05 | 1200 |

At roughly 43 minutes per steering arm for 40 items on this hardware, n = 300 for a
four arm comparison is about 130 GPU hours, which is a different class of run and
should be planned rather than improvised.

## The design lesson

**Compute power before setting a bar.** I set +0.15 from the 1.5B pilot's observed
0.167 without asking whether n=40 could resolve it. The pilot's own margin was
4 of 24 items with p = 0.125, which was itself not significant, so the bar was
calibrated against a number that was mostly noise.

Two structural fixes for any successor design. Make the continuous quantity the
primary rather than a co-primary, since agreement with the fp16 generation and
per head attention divergence carry far more information per item than a binary
task score. And size n from a power calculation at the smallest effect worth
detecting, stated in the registration.

This is the tenth instrument or design defect recorded in this campaign against
zero failed mechanism predictions. The pattern is consistent enough to be a rule
rather than an observation.
