# The Crucible — a guide

This directory is where Observation Theory was made to hurt. Every
principle the theory now states was frozen here as a falsifiable claim
with a **kill condition**, tested under a sealed instrument committed
*before* the run, and recorded regardless of outcome — including the
two refutations that rewrote statements and the six instrument deaths
that rewrote practice. Nothing in this directory is a demo. If you
want the theory's statements, read readscope's `PRINCIPLES.md`; if you
want to know **why you should believe them — or exactly where they
broke** — read this directory.

## The arc, in order

| stage | documents | outcome |
|---|---|---|
| **v0.1 freeze** (2026-08-15) | [`OT-V0.1-FREEZE.md`](OT-V0.1-FREEZE.md) | five principles frozen verbatim (pinned commit + sha256); no-sixth-principle rule; graduation rule G1–G4 declared before any test ran |
| **First Crucible** | [`OT-CRUCIBLE.md`](OT-CRUCIBLE.md) → [`OT-CAMPAIGN-VERDICT.md`](OT-CAMPAIGN-VERDICT.md) | seven sealed tests (OT-1…OT-7). **v1.0 NOT declared**: OT-4 and OT-5 refuted as frozen; the rule was applied exactly as written |
| **v0.2 revision** | [`OT-V0.2-REVISION.md`](OT-V0.2-REVISION.md) | the two refutations became revised statements (P4: feedback compounding, not drift; P5: a floor, not a slope) — revision only after closure, as the freeze required |
| **Second Crucible** | [`OT-CRUCIBLE-2.md`](OT-CRUCIBLE-2.md) → [`OT-CRUCIBLE-2-VERDICT.md`](OT-CRUCIBLE-2-VERDICT.md) | the v0.2 exposures tested; close-out rule: the next campaign starts with **families, not principles** |
| **Third Crucible** | [`FAMILIES-CRUCIBLE-3.md`](FAMILIES-CRUCIBLE-3.md) → [`OT-CRUCIBLE-3.md`](OT-CRUCIBLE-3.md) → [`OT-CRUCIBLE-3-VERDICT.md`](OT-CRUCIBLE-3-VERDICT.md) | one experiment family designed per recorded debt, each with *interior requirements* a shakedown must show before any bar may bind |
| **Fourth Crucible** | [`OT-CRUCIBLE-4.md`](OT-CRUCIBLE-4.md) | one test (OT-17→OT-18): P5's floor law, twice dead by instrument, graded on a fresh seed — the last owed prediction discharged |
| **v1.0 declaration** (2026-08-18) | [`DECLARATION-V1.md`](DECLARATION-V1.md) | the v0.2 text frozen verbatim as v1.0, with the full evidential census, refutation-and-instrument ledger, and freeze rules forward |
| **The v1 line** (post-declaration) | [`OWED-V1.md`](OWED-V1.md), `PREREG-OP*.md`, `OP3*-SEAL-NOTES.md` | new owed predictions minted by sealed revision act — the bar raised from *descriptive* (the law holds) to *derivable* (the law predicted a priori). A theory with zero exposure owes its next risk |
| **New domains** | `PREREG-SC1.md`, `PREREG-SC2.md`, `PREREG-SC2R.md` | the space-communications downlink line — a domain is entered by a sealed campaign, never a free extension |

## How a test lives (the lifecycle every file belongs to)

1. **The claim is frozen first**, in a crucible declaration, with a
   prospective statement *and* a kill condition. Claims may later be
   narrowed by an appendix, never widened.
2. **The instrument appendix is committed before the run**
   (`PREREG-OTn-APPENDIX.md`): grids, tolerances, seeds, model lists.
   A `-V2`/`-V3` suffix is a *disclosed* instrument revision — the
   earlier version stays in the tree as the record of what was tried.
3. **The harness runs** (`otn_check.py`, with `_v2`/`_v3` matching the
   appendix revisions). Harnesses are plain Python (numpy/scipy, sympy
   where symbolic), seeded, and print their verdict.
4. **The verdict is recorded** in `OTn-NOTES.md` — PASS, FAIL, or
   VOID (instrument death), with the measured numbers and the lesson.
   Failed bars stand as written; a refuted claim is *absorbed into the
   revised statement*, not deleted.
5. **The ledger row lands** in [`../claims/LEDGER.md`](../claims/LEDGER.md),
   and CI's Tier-A job re-runs the CPU-only harnesses on every push,
   asserting the committed verdicts still reproduce.

## File taxonomy

| pattern | what it is |
|---|---|
| `OT-CRUCIBLE*.md`, `*-VERDICT.md` | campaign declarations and their verdicts |
| `OT-V0.1-FREEZE.md`, `OT-V0.2-REVISION.md`, `DECLARATION-V1.md` | the version acts: freeze → revision → declaration |
| `PREREG-OTn-APPENDIX*.md` | sealed instrument appendices for tests OT-1…OT-18 |
| `otn_check.py` | the test harnesses (one per appendix revision) |
| `OTn-NOTES.md` | per-test verdicts and lessons |
| `OT3-THEOREM.md`, `OT3-NOISY-THEOREM.md`, `OT10-THEOREM.md` | the stated-and-proved results (identification lower bound, the noisy cliff) |
| `verify_theorems.py` | the theorem algebra re-verified in exact rational arithmetic + SymPy (11/11); the Lean formalizations live in [`../lean/ObservationTheory/`](../lean/ObservationTheory/) |
| `FAMILIES-CRUCIBLE-3.md`, `fam*_shakedown.py`, `FAMILY-*.md` | experiment families and the shakedowns that must show a family's *interior* (across seeds) before bars may bind to it |
| `OWED-V1.md`, `PREREG-OP*.md`, `op*_check.py`, `op3_graded.py`, `OP3*-SEAL-NOTES.md`, `OP3C-DESK.md` | the v1-line owed predictions (OP1: cross-consumer codec transfer; OP3: the sample-complexity exponent, whose *shakedown falsified the a-priori prediction before sealing* — the corrected law was derived, validated, and sealed with the original preserved verbatim) |
| `PREREG-SC*.md`, `sc*_check.py`, `sc2r_pipeline.py`, `fam_sc*_shakedown.py` | the space-comms downlink crucible (multi-instrument consumers under a hard bit budget) |
| `verify_tilted_filter.py` | exploratory: the tilted-filter closed form (see `../paper/TILTED-FILTER-NOTE.md`) |
| `armH_data/`, `ot6_data/` | committed run data for the real-head and cross-domain tests |
| `SEAL-TOMORROW.md` | the overnight rule in action: constructions queued for a compliant next-day seal |

## Reproducing

```
pip install numpy scipy sympy
python crucible/verify_theorems.py          # 11/11 exact identities
python crucible/ot7_check_v3.py             # invariance taxonomy
python crucible/ot2_check.py                # the change-of-measure law
```

Each `ot*_check.py` prints its gate results and verdict; the sealed
seeds are inside the harnesses and their appendices. The repository's
CI re-runs the CPU-only subset on every push and fails if any committed
verdict stops reproducing — the record is not allowed to rot silently.

## The rules that make the record honest

- **Registration first.** Claims and kill conditions are committed
  before instruments; instruments before runs. Appendices narrow,
  never widen.
- **Cooling-off.** Bars are never sealed on the day of first
  construction; families qualify their interior across seeds first,
  and seals wait for the next day (the overnight rule; its recorded
  override ledger — seven exceptions, each with mitigation named — is
  part of the v1.0 declaration).
- **No sixth principle.** Surprises are queued, not promoted;
  a framework that grows a principle per surprise forbids nothing.
- **Refutations are statements.** OT-4 and OT-5 failed as frozen; the
  revised P4 and P5 carry those failures as content. Instrument deaths
  (OT-9, OT-10, OT-12, OT-13, OT-17, and BMP-V1 in the sister program)
  became binding practice.
- **Verdicts stand.** Failed bars are never edited; VOID campaigns
  close unresolved rather than retry silently; the graduation rule was
  applied against the program's own hopes the first time — v1.0 was
  refused in 2026-08-15's verdict and earned three days later.

## A reading path

1. [`OT-V0.1-FREEZE.md`](OT-V0.1-FREEZE.md) — the rules of the game.
2. [`OT-CRUCIBLE.md`](OT-CRUCIBLE.md) — seven claims that could die.
3. [`OT-CAMPAIGN-VERDICT.md`](OT-CAMPAIGN-VERDICT.md) — two of them did.
4. [`OT5-NOTES.md`](OT5-NOTES.md) — what a refutation looks like when
   the measurement is better than the prediction (a step, not a slope;
   *refusal, not error*).
5. [`DECLARATION-V1.md`](DECLARATION-V1.md) — the census of what was
   earned, and at what cost.
6. [`OWED-V1.md`](OWED-V1.md) — what the theory risks next.
