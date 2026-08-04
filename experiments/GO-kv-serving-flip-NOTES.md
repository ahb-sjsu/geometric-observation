# GO-P-2026-056 — KV-cache serving flip on Qwen2.5-7B: governed-run report

**Registered MISS, reported at full prominence per PROTOCOL Rule 1.2.**
Governed run 2026-08-03, seed 20260815, Atlas GPU 1, single run as sealed
(prereg [`GO-P-2026-056-kv-serving-flip.md`](../prereg/GO-P-2026-056-kv-serving-flip.md),
sealed 2d5794a as 055, renumbered 056 pre-run by dated amendment). Result JSON:
[`results/GO-KV-serving-flip-7B.json`](../results/GO-KV-serving-flip-7B.json).

## Verdict: 4/6 gates pass; K3 (primary) and K4 (specificity) MISS

| Gate | Bar | Measured | Verdict |
|---|---|---|---|
| K1 recon-matched audit | \|ratio−1\| ≤ 1e-4, every arm | 1.000000, all six steering arms | **PASS** |
| K2 fp16 competence | ≥ 0.50 | **0.925** | **PASS** |
| K3 primary flip @3b | preserve − destroy ≥ +0.15 | **+0.075** | **MISS** |
| K4 specificity @3b | shuffle − destroy ≥ +0.10 | **+0.050** | **MISS** |
| K5 agreement co-primary @3b | agree(P) − agree(D) ≥ +0.15 | **+0.175** (0.175 vs 0.000) | **PASS** |
| K6 preserve usable @3b | ≥ 0.5 × fp16 | 0.925 = fp16 | **PASS** |

Per the sealed falsification clause, **K3 failing with K1/K2 satisfied refutes
the operational claim at its registered effect sizes on this model and task.**
No bar is moved post hoc; no second attempt is registered under this ID.

## The arms (n=40, passage_retrieval_en, 14k-token contexts)

| Arm | @3-bit | @4-bit |
|---|---|---|
| fp16_baseline | 0.925 | — |
| preserve_read | 0.925 | 0.925 |
| shuffle_control | 0.900 | 0.925 |
| destroy_read | **0.850** | 0.925 |

recon_ratio = 1.000000 on every steering arm (the arms are genuinely
bits-identical and reconstruction-identical to machine precision; ref_err
3.48–3.51 @3b, 1.62 @4b).

## Honest reading

**What missed.** The registered effect floors. P−D came in at +0.075 (half the
+0.15 bar); shuffle−destroy at +0.050 (half the +0.10 bar). The paired
McNemar (reported, not gated; per-item scores in the JSON) is 3–0 discordant
in the predicted direction, exact two-sided p = 0.25 — n=40 at a 0.925
ceiling cannot separate these floors from noise, and the sealed design
accepted that risk knowingly ("the few-item caveat applies").

**What held anyway.** Every directional prediction: destroy < shuffle <
preserve = fp16 at 3-bit; 4-bit inert (exactly as the 1.5B pilot placed the
damage threshold — all three 4-bit arms tie fp16 at 0.925); and the
**continuous co-primary passed**: destroy_read never once reproduced the
fp16 generation (exact-match agreement 0.000 vs preserve's 0.175; token-F1
vs fp16: 0.282 vs 0.438). At identical bits and identical reconstruction
error, where the error lands demonstrably changes *what the model says*; at
this n and task ceiling it did not change *whether the answer is right*
often enough to clear the sealed floors.

**Instrument diagnosis — see the pre-verdict power note.** The K3 power
defect was recorded *while the run was still executing*, before the verdict
landed ([`GO-KV-SERVING-POWER-NOTE.md`](GO-KV-SERVING-POWER-NOTE.md),
commit 936e699): a true effect exactly at the +0.15 bar clears its own gate
only 56% of the time at n=40, so the defensible reading is that the
end-task effect on this model/task is **smaller than 0.15 and not
resolvable at n=40** — not that it is absent. The bar itself was calibrated
against a pilot margin (4/24, p=0.125) that was mostly noise. That note also
fixes the successor-design rules: make the continuous quantity primary
(K5-style agreement / per-head attention divergence carry far more
information per item than a binary score) and size n by power calculation at
the smallest effect worth detecting (~150 items for 0.15, ~300 for 0.10).
Add to that the ceiling observation from the data: fp16 = preserve = 0.925
leaves only 3 wrong items of headroom, so hotpotqa (continuous F1) is the
natural next task. The mechanism result (15–36× attention-KL, 10/10 heads)
stands on its own power; K5 shows the effect survives to output text; the
registered end-task binary claim at these effect sizes is refuted on this
model/task.

## Chain of custody

- 1.5B mechanism + pilot: logged in-prereg pre-seal (`GO-KV-mechanism-1p5B.json`,
  `GO-KV-pilot-1p5B.json`).
- Governed run launched from `/archive/kvbench` (venv) against
  `/home/claude/kv_serving_flip.py` (the renumbered 056 script), log
  `/tmp/kv7bgov.log`, PID 3954870, GPU 1, ~4.7 h wall.
- Sentinel JSON extracted verbatim to `results/GO-KV-serving-flip-7B.json`;
  gates evaluated by script against the sealed bars.

---

## Addendum — paired significance on the co-primary, and the strongest single result

Added after the report above. Nothing here changes a gate or a verdict. It supplies
the paired tests that the report leaves as point values, and it records one harness
defect.

**Exact two-sided McNemar, preserve against destroy, from the committed per-item
data.**

| condition | statistic | discordant | p |
|---|---|---|---|
| 3 bit | task score | 3 to 0 | 0.250 |
| 3 bit | fp16 agreement | **7 to 0** | **0.016** |
| 4 bit | task score | 0 to 0 | 1.000 |
| 4 bit | fp16 agreement | **16 to 3** | **0.0044** |

**The 4-bit condition carries the strongest result in the run, and the report above
understates it.** The report correctly calls 4 bit inert, which it is on task score,
where all three arms tie fp16 at 0.925. On what the model actually emits it is not
inert at all.

| 4-bit agreement with the fp16 generation | value |
|---|---|
| preserve_read | **0.550** |
| shuffle_control | 0.300 |
| destroy_read | **0.225** |

Token F1 against the fp16 generation orders the same way, 0.741 against 0.572
against 0.494. So in a condition where the bit budget, the per-token reconstruction
error, and the task score are all identical to six decimal places or exactly, the
output distribution differs at p = 0.0044, and the wrong head's subspace again sits
between the complement and the correct subspace.

That is the cleanest available statement of the mechanism reaching serving
behaviour, because it removes task score from the argument entirely rather than
relying on it. It is a behavioural claim and not a task-quality claim. Nothing here
rescues K3, which remains a registered miss, and the report's reading of the
falsification clause stands unchanged.

**Specificity holds on the co-primary at both bit-widths**, preserve above shuffle
above destroy, which the task score could only show at 3 bit and only within noise.

## Defect — the harness emitted no verdict dict

The governed run produced no self-scored gates. A per-bits refactor dropped the
verdict block, so the sealed bars had to be applied to the run data afterwards.
Evaluating one's own gates after seeing the numbers is precisely what the
registration discipline exists to prevent, even when the bars are transcribed
unchanged and the data is untouched, because nothing in the artifact proves that.

Fixed. The harness now computes the six sealed gates itself and prints them, the
block is checked to reproduce the hand evaluation exactly on the committed data,
and the verdict together with a note on how it was produced is now written into
[`GO-KV-serving-flip-7B.json`](../results/GO-KV-serving-flip-7B.json) so the result
file is self-describing.

This is the eleventh instrument or design defect recorded in this campaign against
zero failed mechanism predictions.
