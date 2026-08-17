# F1′ — the log-spread signal family, multi-seed qualified

**2026-08-17. The family OT-18 (if sealed, in a later session) will
cite for P5's fourth attempt. Constructed today; per the rate-limit
rule — and after this session's OT-17 — nothing may be sealed
against it before a later working session, and this document sets
no bars.**

## Changes from F1, each answering a recorded death

- **N_PAIRS 30 → 100** (trace spread widened to
  logspace(−4.5, −0.5)): per-pair quantization aliasing averages
  out; fraction curves are smooth at every seed where F1's jumped.
- **⅓-octave grid** in the band (15 steps, 30×–1732×): the
  informative-fraction transition slides about an octave from seed
  to seed (measured in this qualification's v1, which tried a fixed
  intersection band and watched it collapse to one step); a dense
  grid makes the transition cross many steps *wherever it lands*.
- **The family property is the in-run criterion, not a fixed
  band** — the v2 qualification rule: ≥ 4 interior band steps with
  ≥ 2 straddling margin 3, demonstrated to hold at **every** one of
  five seeds drawn from the same randomness class a sealed run
  would use. This is the OT-17 lesson implemented: a shakedown at
  one seed shows one point of a distribution; this one shows five,
  with margins (8–11 interior, 7–10 straddling) that leave a sixth
  seed real room.

## Qualification record (`results/F1P-shakedown.json`)

| seed | interior steps | straddling |
|---|---:|---:|
| 20260901 | 9 | 9 |
| 20260902 | 8 | 8 |
| 20260903 | 11 | 10 |
| 20260904 | 9 | 7 |
| 20260905 | 10 | 7 |

Requirement at every seed: ≥ 4 / ≥ 2. **DEMONSTRATED.**

## Design trail, kept

v1 of this qualification implemented the Fourth Crucible close-out's
"intersection band" suggestion and measured it into retirement: with
the transition sliding, the five-seed intersection was a single step
at both 3× and ½-octave spacing. The close-out's *diagnosis* (family
interior must be shown across seeds) survives; its proposed
*mechanism* (a fixed intersection band) is superseded by the in-run
criterion + dense grid, and the supersession is recorded here rather
than silently absorbed.

## What OT-18 would owe

The OT-17 appendix's instrument verbatim (smooth-consumer probe,
derived grid — now the dense one, silence = miss, margin ≥ 3
grading, ≥ 8 graded pairs per graded step), a seed disjoint from
{20260901..20260905}, MC1 ≥ 4 interior / MC2 band-level ≥ 2
straddling (now family-demonstrated at exactly this granularity,
five times over), MC3 window, bars B1/B2/B3 unchanged through four
campaigns. Sealed no earlier than the next working session.
