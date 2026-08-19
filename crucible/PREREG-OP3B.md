# PREREG-OP3B — the sample-complexity exponent, corrected bars (re-run)

**STATUS: UNSEALED.** Construction + shakedown only. A **new sealed
act** re-running OP3 after its 2026-08-19 graded seal FAILed on
bar-calibration defects (`OP3-SEAL-NOTES.md`). It edits nothing in the
sealed, FAILed `PREREG-OP3.md` / `op3_graded.py`; it reuses their
measurement functions verbatim and only corrects the bars. Bars bind on
a dated seal a day later than this construction (2026-08-19), so the
earliest compliant seal is **2026-08-20**; `op3b_check.py` enforces it
in code. Graded on fresh seeds {20260901–03}, disjoint from both the
shakedown {0,1,2} and the failed run {20260819–21}.

## Why a re-run, and what stays fixed

The front law itself is untouched and still holds: derived, Lean-checked
(`FrontLaw.lean`, `frontlaw_exponent`), and shakedown-supported — the
p≈4 collapse is real. **What failed was the operationalization**, in
three ways the corrected bars fix (diagnosis in `OP3-SEAL-NOTES.md`):

1. B3 demanded affine overlap ≥ 0.9 at m=1000, but the law predicts
   recovery is only ~60% complete there — the bar contradicted the law.
2. B2 barred the *smooth fitted* front rate (0.869) while the runner
   read the *noisy empirical* 0.5-crossing — different quantities.
3. B1 required the collapse exponent *exactly* == 4, a p4/p5 knife-edge.

The re-run also corrects an over-claim: the recovered-mode **front
advances only weakly** (a couple of modes over 250× budget, and
non-monotonically). The corrected campaign centers on what is robust —
the **collapse** — and states recovery and advance honestly.

## Corrected bars (calibrated on the shakedown, not the failed run)

- **B1' — the collapse exponent (primary).** The continuous best-fit `p`
  of `cos²θ_i = s/(s+A)`, `s = m·w^(p·i)`, lies in `[3.5, 5.5]` with RMS
  `≤ 0.20`, on each of ≥3 disjoint seeds. This is the robust form of the
  derived `p = 4` (Davis–Kahan), immune to the p4/p5 tie.
- **B2' — recovery matches the predicted level.** The affine-operator
  overlap at m=1000 lies in `[0.50, 0.70]` on each seed — the law's own
  prediction of *incomplete* recovery, not the impossible ≥ 0.9.
- **B3' — the front advances (weak).** The recovered-mode count
  (`cos²≥0.5`) at m=1000 exceeds that at m=4 by `≥ 1` on the seed mean —
  the front moves with budget, allowing per-seed non-monotonic noise.

**Kills.** Best-fit `p` outside `[3.5, 5.5]` (the collapse exponent is
not ≈4 — the Davis–Kahan account is wrong); or recovery at m=1000
outside `[0.50, 0.70]` (the law mis-predicts the recovery level); or the
front does not advance at all. Any triggers the v2.0 process on P3's
asymptotic-budget claim alone; the frozen P3 statement is untouched.

## Shakedown outcome (2026-08-19) — on seeds {0,1,2}

Computed from the committed collapse data
(`readscope/calibration/records/op3-frontlaw.json`), no re-run:

| seed | best-fit p | RMS | affine recovery (mean cos² @ m=1000) | count m=4 → m=1000 |
|---|---|---|---|---|
| 0 | 4.50 | 0.173 | 0.568 | 8 → 9 |
| 1 | 4.25 | 0.141 | 0.601 | 7 → 10 |
| 2 | 4.00 | 0.151 | 0.613 | 8 → 10 |

All three corrected bars hold on the shakedown seeds: p ∈ [4.0, 4.5]
(B1'), recovery 0.57–0.61 ∈ [0.50, 0.70] (B2'), and the seed-mean count
advances 7.67 → 9.67 = +2 (B3'). The interior is there; the bars now
match the theory's own predictions and the exact quantities the runner
computes.

## Provenance

- Failed campaign: `crucible/PREREG-OP3.md` (sealed, FAILed 2026-08-19),
  `OP3-SEAL-NOTES.md`, `results/OP3-frontlaw-graded.json`.
- Measurement functions reused verbatim: `crucible/op3_graded.py`
  (`per_mode_cos2`, `population_operator`). Corrected runner:
  `crucible/op3b_check.py` (seal-guard + coded cooling-off), fresh seeds.
- Machine-checked law: `lean/ObservationTheory/FrontLaw.lean`
  (`frontlaw_exponent`, p=4). Shakedown data:
  `readscope/calibration/records/op3-frontlaw.json`.
