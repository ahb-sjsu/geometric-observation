# DRAFT amendment to PROTOCOL.md — the power-first rule (§5.1)

**Status: PROPOSAL for review, not enacted.** PROTOCOL.md is untouched; if
adopted, the section below slots into §5 (Statistical standards) as rule 5.1,
and the two template touches follow. Drafted 2026-08-04 at the user's request,
from the campaign's own record.

## Motivation, from the ledger

Eleven instrument or design defects are on record against zero failed
mechanism predictions (count per `GO-KV-SERVING-POWER-NOTE.md` and the
GO-P-2026-056 addendum). The recurring failure is never the physics — it is a
bar that the design could not resolve: 046's instrumentation windows, 048's
per-cell control multiplicity, 051's invalid normal approximation, 052's
1.1%-margin miss, 056's K3 gate with 56% power at its own bar. Conversely,
every registration that ran a **logged pilot before sealing** caught its
defect in time: 044's net-design artifact (redesigned pre-seal), 055's
boundary-bracket bar (corrected pre-seal), 058's W4 gate shape (reshaped
pre-seal), 059's split-tracker crash and two bar calibrations (fixed
pre-seal). The pattern is consistent enough to be a rule rather than an
observation — this amendment makes it one.

## Proposed text (insert as §5, first bullet block, numbered 5.1)

> **5.1 Power before bars (binding).** A registration may not seal a numeric
> gate without stating, in the prereg, how the bar was sized. Concretely:
>
> - **Binary/count gates:** a power statement is mandatory — the probability
>   that a true effect exactly at the bar clears its own gate, at the
>   registered n (exact test or Monte Carlo; method named). Designs below
>   80% power at the bar may still seal, but the prereg must carry the
>   number, and a miss is then reported as *"effect below the bar,
>   unresolvable at this n"* — never as absence.
> - **Continuous gates** (thresholds, discounts, gaps): the bar must be
>   stated as a multiple of the expected noise scale or of a pilot-measured
>   value, with the margin printed (house floor: ≥ 1.3× over the
>   pilot-measured value for pass-bars; bars within ~1σ of a pilot value
>   may not seal — the 052 lesson).
> - **Pilots are the default, and they are logged.** One pre-seal pilot at a
>   distinct, disclosed seed is the expected path for any new instrument;
>   its full values go in the prereg PILOT NOTE, and every bar changed
>   between pilot and seal is itemized with its reason. Sealing a novel
>   instrument with no pilot requires an explicit "NO pilot was run"
>   declaration (053/054 style, for designs inheriting a piloted
>   predecessor's instrument unchanged).
> - **Instrument-vs-physics separation in the falsification clause:** every
>   prereg names which gates are physics (a miss refutes the claim) and
>   which are instrument/validity (a miss voids the run — logged
>   instrumentation miss, rerun only under a dated amendment). The 056
>   convention (K1/K2 void, K3–K5 refute) is the model.
> - **Prefer continuous co-primaries.** Where a continuous quantity carries
>   more information per unit of data than the binary endpoint (agreement,
>   divergence, threshold position), it should be primary or co-primary;
>   a binary endpoint alone must justify itself against the power table.
>
> *Provenance: the eleven-defects-zero-mechanism-failures record; the
> pre-verdict power note of GO-P-2026-056 (commit 936e699); the pilot-caught
> defects of GO-P-2026-044/055/058/059.*

## Template touches (if adopted)

1. **§12.1 prereg template**: add two required fields under `prediction:`
   ```yaml
   power: <for each gated bar: how it was sized — exact/MC power at the bar,
           or pilot value × margin; "inherited from GO-P-XXXX" allowed when
           the instrument is unchanged>
   pilot: <seed + disposition of the logged pilot, or the explicit
           declaration "NO pilot was run">
   ```
2. **§5 clustering bullet**: append one sentence — *"Control statistics use
   exact tests from the start where cell counts can be small (the 051/053
   lesson); a normal approximation must justify its validity range in the
   prereg."*

## What this does NOT change

- No sealed prereg is reopened; the rule binds registrations sealed after
  adoption.
- It does not forbid underpowered runs — it forbids *unknowing* ones, and
  fixes how their misses must be worded (the 056 addendum's distinction
  between "refuted at its registered floors" and "absent").
- `[exploratory]` work remains exempt (§5 multiplicity bullet's existing
  carve-out), consistent with Tier C.

## Adoption

If this text is approved: move §5.1 + the two template touches into
PROTOCOL.md in one commit titled "PROTOCOL §5.1: power before bars", delete
this draft file in the same commit, and add a line to the ledger's
verification-incidents preamble noting the rule's provenance.
