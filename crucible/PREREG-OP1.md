# PREREG-OP1 — cross-consumer codec transfer (v1-line, novel claim)

**STATUS: SEALED 2026-08-20.** Construction + shakedown only. Discharges owed
prediction **OP1** of `OWED-V1.md` — the genuinely *new* v1-line claim,
the one that extends P1's reach *across* consumers rather than within an
ensemble. Bars bind only on a dated seal a day later than this
construction (cooling-off, `op1_check.py` guard), after the shakedown
shows the family's interior across seeds. No evidential weight until
then.

## The claim

A codec optimized against consumer A's read operator `P_A` damages a
*different* consumer B by an amount predictable from the operator
overlap `tr(P_A P_B)` **alone** — no probe of B under A's codec. If
consumer relativity means what v1.0 says, it composes across consumers.

## The a-priori law (sign derived; leading form linear)

Code the frame in A's eigenbasis. The A-optimal codec water-fills its
rate budget against A's sensitivity spectrum `s_A`, spending bits where
A is sensitive and leaving quantization noise where A is not — so the
distortion `Σ_δ^A` is large exactly in A's low-sensitivity directions.
B's damage `tr(P_B Σ_δ^A)` is therefore large when B reads where A does
*not*, and **decreases as `tr(P_A P_B)` grows**: when B reads what A
protects, B is spared. To leading order the damage is affine in the
overlap, `damage ≈ α − β·tr(P_A P_B)` (β > 0). The falsifiable content
is that one scalar `tr(P_A P_B)`, computed with no probe of B under A's
codec, predicts B's measured damage.

## Shakedown outcome (2026-08-18)

`fam_op1_shakedown.py` (d=48, soft PSD operators tr(P)=8, rate budget
2 b/dim, 60 pairs/seed, overlap swept via B tilted toward A;
`results/OP1-shakedown.json`):

| seed | overlap range | Spearman(overlap, damage) | linear R² | slope |
|---|---|---|---|---|
| 0 | 1.11–5.06 | −0.816 | 0.968 | −0.567 |
| 1 | 1.12–5.19 | −0.729 | 0.951 | −0.565 |
| 2 | 1.07–5.02 | −0.797 | 0.966 | −0.579 |

The predicted **negative** relationship holds on every seed, the single
overlap scalar carries the leading law (R² ≈ 0.96), and the slope is
stable (≈ −0.57). The family spans a real overlap range. Cross-consumer
transfer is predictable from `tr(P_A P_B)` without probing B — the novel
claim survives its first look.

## Bars (TO BE SEALED on a fresh day; not yet binding)

- **B1 — the transfer correlation.** `Spearman(tr(P_A P_B), damage) ≤
  −0.6` on each of ≥3 disjoint seeds (OWED-V1's stated kill is
  `|rank corr| < 0.6`).
- **B2 — the overlap is a sufficient single predictor.** The leading
  affine fit `damage ≈ α − β·tr(P_A P_B)` holds with `R² ≥ 0.9`, `β > 0`,
  per seed — the one scalar, not a multi-feature model, carries it.
- **B3 — no-probe-of-B (MC-grade).** The prediction is computed from
  `tr(P_A P_B)` and A's codec only; B's response to A's codec is used
  *only* to grade, never to fit. (Definitional in the runner; asserted
  as a check so the transfer is genuinely blind to B.)

**Kill.** `|Spearman| < 0.6` at high family spread — cross-consumer
transfer is not predictable from the overlap, and P1's reach is narrower
than v1.0's statement claims (a scoped refutation of the *new* claim,
not of the frozen within-consumer principle).

## Discipline and scope

Synthetic (planted soft operators + a water-filled codec), so a pass
earns the *mechanism* — that the overlap trace is the sufficient
statistic for cross-consumer damage — not a claim about specific real
models; a real-head pair substrate (two Llama heads, blind-probed
operators) is the named next campaign in OWED-V1 and would be its own
unit. A corrected slope coefficient (`β` derived from the codec's
water-level, as OP3/SC-2 required) is a later refinement; the sealed
claim here is the *predictive correlation*, not the exact slope. Frozen
v1.0 statements untouched.

## Provenance

- Owed prediction: `crucible/OWED-V1.md` OP1 (`1c18e31`).
- Substrate: `crucible/fam_op1_shakedown.py`; record
  `results/OP1-shakedown.json` (no weight). Graded runner
  `crucible/op1_check.py` (built, seal-guard + coded cooling-off,
  refuses until sealed), disjoint seeds {20260819, 20260820, 20260821}.
  B3 is an out-of-fold test: fit the affine law on half the pairs,
  predict the held-out half's damage from the overlap scalar alone.
- Reused core: readscope `water_fill`, the operator-overlap trace
  (`consumer_distortion` = `tr(P·Σ)`, metrics.py).
