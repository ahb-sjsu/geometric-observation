# Seal checklist — OP3, SC-1, SC-2 (fresh day, 2026-08-19+)

All three campaigns are prepped and their graded runners are built,
tested, and **refuse to grade until sealed** (seal-guard + coded
cooling-off keyed to family-construction date 2026-08-18). Tomorrow is
a deterministic act: flip the STATUS token, run the runner, commit.
Nothing here is judgement-heavy — the bars are already committed in each
appendix. **Keep any FAIL as executed; do not adjust a bar to make it
pass.**

Cooling-off is code-enforced: each runner refuses unless the appendix
STATUS is `SEALED <date>` with `<date> ≥ 2026-08-19`. A same-day or
missing-date seal is refused by the runner, not just by discipline.

## The seal, per campaign

For each, replace the `STATUS: UNSEALED` token with
`STATUS: SEALED 2026-08-19` (keep the surrounding prose), commit the
seal, run the runner, then commit the result JSON. GPG signing may
prompt — that needs a human "try now".

### OP3 — the front-law bars (`crucible/PREREG-OP3.md`)

1. In `PREREG-OP3.md`, change `**STATUS: UNSEALED.**` →
   `**STATUS: SEALED 2026-08-19.**`
2. `git add crucible/PREREG-OP3.md && git commit` (seal message).
3. `python crucible/op3_graded.py` → writes
   `results/OP3-frontlaw-graded.json`. Bars: B1 best-collapse exponent
   `p=4` per seed; B2 front-advance rate `0.869 ± 0.10`, all seeds
   `>0.5`; B3 affine-operator overlap `≥ 0.9`. Seeds
   {20260819,20260820,20260821}.
4. `git add results/OP3-frontlaw-graded.json && git commit` (verdict).

### SC-1 — downlink allocation (`crucible/PREREG-SC1.md`)

1. `STATUS: UNSEALED` → `STATUS: SEALED 2026-08-19`.
2. Commit the seal.
3. `python crucible/sc1_check.py` → `results/SC1-graded.json`. Bars:
   B1 AM/GM law at high rate (`|median(G_meas/G_pred)−1| ≤ 0.03`,
   Spearman `≥ 0.95`); B2 finite-rate ratio monotone in rate; B3 linear
   composition of importance.
4. Commit the verdict.

### SC-2 — LEO/interplanetary transport (`crucible/PREREG-SC2.md`)

1. `STATUS: UNSEALED` → `STATUS: SEALED 2026-08-19`.
2. Commit the seal.
3. `python crucible/sc2_check.py` → `results/SC2-graded.json`. Bars:
   B1 delay-decorrelation fit `R² ≥ 0.95` + reaches `0.9·floor`;
   B2 schedule D-invariance (`excess` spread `≤ 0.01`); B3
   `excess = κ·ρ`, `R² ≥ 0.98`, slope within `0.05` of derived
   `κ = 1−2c = 0.70`.
4. Commit the verdict.

## After sealing

- Record each verdict (PASS/FAIL) in `project_ot_crucible.md` memory and
  close tasks #17 (OP3), #18 (SC-1), #19 (SC-2).
- A PASS on OP3 discharges the first v1-line owed prediction (updates
  the OP3 line in `OWED-V1.md`'s status — but `OWED-V1.md` is the sealed
  mint; record the discharge in the appendix/verdict, not by editing the
  mint).
- A PASS on SC-1/SC-2 extends OT to the space-comms domain (does not
  touch frozen v1.0 statements). A FAIL scopes the transfer — keep it.
- Push all commits (GPG "try now" as needed).

## One-line resume

Say **"seal them"** and follow this file top to bottom.
