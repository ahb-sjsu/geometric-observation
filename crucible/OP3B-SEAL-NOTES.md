# OP3-B seal outcome — FAIL on B3′ (2026-08-20), kept as executed

Sealed 2026-08-20, graded on fresh seeds {20260901–03} (disjoint from
the shakedown {0,1,2} and the failed OP3 run {20260819–21}). Verdict in
`results/OP3B-graded.json`. **No bar adjusted.**

| seed | best-fit p (B1′) | recovery (B2′) | count m=4 → m=1000 |
|---|---|---|---|
| 20260901 | 5.00, RMS 0.161 ✓ | 0.578 ✓ | 9 → 9 |
| 20260902 | 4.50, RMS 0.151 ✓ | 0.588 ✓ | 8 → 10 |
| 20260903 | 4.50, RMS 0.164 ✓ | 0.594 ✓ | 9 → 9 |

- **B1′ PASS** — the collapse exponent stays in [3.5, 5.5] with clean
  fits on every fresh seed. The derived `s = m·w⁴` collapse holds.
- **B2′ PASS** — recovery at m=1000 lands inside the law's own
  predicted band on every seed. The front law's *level* prediction is
  right.
- **B3′ FAIL** — mean mode-count advance +0.67 (bar ≥ +1.0): the
  integer 0.5-crossing count barely moves over a 250× budget span on
  these seeds.

## Reading, honestly

The corrected front law's **static** predictions are confirmed on fresh
seeds (exponent and recovery level — the substance of the collapse).
Its **dynamic** prediction — the front measurably advancing — failed at
the granularity it was barred at. Notably, the family record passed
this bar (advance ≥ 1 on each shakedown seed, mean +2.0); fresh seeds
gave 0, +2, 0. **The integer mode-count crossing is seed-fragile** —
the same class of lesson as OT-17, now on the statistic rather than the
family: per-mode cos² climbs (B1′/B2′ show that), but modes sit near
the 0.5 crossing and the integer count wobbles across seeds.

## Consequence

- OP3-B: FAIL as sealed. Two of three corrected bars confirmed; the
  campaign does **not** discharge OP3.
- **OP3's owed prediction stays live** — neither discharged (B3′
  failed) nor refuted (the collapse law itself passed twice over).
- A third act, if attempted, must re-operationalize the *advance* as a
  continuous statistic (e.g., the fitted front position from the
  collapse constant, or mean cos² gain on the sub-front modes) and
  demonstrate IT across seeds before barring — the front may simply
  advance more slowly than one integer mode per 250× at this spectrum.
- FrontLaw.lean and the collapse validation stand untouched.

## Ledger note

OP3's campaign history: OT-10-class authoring-defect FAIL (2026-08-19),
then this substantive partial (2026-08-20). Both kept. The discipline's
read: the theory's collapse law survives contact with fresh seeds; its
front-advance claim, even humbled, does not yet have a seed-stable
statistic.
