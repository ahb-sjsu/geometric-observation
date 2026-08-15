# Observation Theory v0.1 — the freeze

**Sealed 2026-08-15.** This document freezes the theory's principle set
and binds the admission and graduation rules for the Crucible campaign
(`OT-CRUCIBLE.md`). Proposed by external review of readscope
(2026-08-15); adopted with the co-author's directive: *stop adding
principles and make the existing five hurt.*

## The frozen object

For a consumer `C` with Jacobian `J_C(x) = ∂C/∂x`, output metric `G`,
and probing distribution `D`:

    P_C(D) = E_{x~D}[ J_C(x)ᵀ G J_C(x) ]

Everything in v0.1 is a statement about this object: what it induces
(P1), how it depends on `D` (P2), what identifying it costs (P3), how it
moves in time (P4), and what its quadratic form predicts (P5).

## The frozen principles

P1–P5 are frozen **as written** in readscope's `PRINCIPLES.md` at:

- commit `a490e4eae6c518457aaed93043a9c52564e12e88`
  (github.com/ahb-sjsu/readscope)
- sha256 of the file at that commit:
  `58821eb9c9cabbd6d3f71ef21e466a73065b46ea71ec9cd647aeda7c47eaf5dd`

The frozen text lives immutably in git history at that commit. Later
commits to `PRINCIPLES.md` may touch only non-principle framing (e.g.,
a freeze banner); the verdict step diffs the five principle sections
against the frozen commit (`git diff a490e4e..verdict -- PRINCIPLES.md`)
and any change inside a principle statement voids the campaign (rule G4
below) — corrections wait for closure, then diff against the frozen text.

## Admission rule (binding)

**No sixth principle is admitted until the Crucible resolves.** A
surprising result during the campaign is recorded in the claims ledger
and, if it demands new structure, that demand is *queued*. This is the
guard against the failure mode the reviewer named: a framework that
grows a principle per surprise explains everything because it forbids
nothing.

## Graduation rule (binding, declared before any test runs)

**Observation Theory v1.0** may be declared if and only if:

- **G1.** At least **4 of the 5** core tests OT-1…OT-5 survive their
  sealed bars.
- **G2.** OT-6 (cross-domain transfer) survives — generality is
  necessary, not optional; a theory of KV caches is not this theory.
- **G3.** At least one of the two mechanism-grade results lands:
  OT-4's *intervention* arm succeeds (predicted refresh cadence moves a
  real degradation onset), **or** OT-3 yields a stated-and-proved lower
  bound whose side-information prediction survives measurement.
- **G4.** The frozen-hash check passes: zero edits to the five principle
  statements between freeze and verdict.

If the rule is not met, the campaign **closes with a recorded verdict**:
the five principles were an attractive post-hoc organization, not yet a
predictive theory. Revision happens only after closure. Partial credit
is recorded per-test in the ledger; there is no partial graduation.

The thresholds are the co-author's to have vetoed at this freeze and are
binding thereafter. They deliberately differ from the reviewer's sketch
in one place: OT-6 is elevated from "at least one cross-domain
prediction" to a necessary condition, because the program's charter
(`PROTOCOL.md`) claims consumer-relativity as a *general* thesis.

## What graduation buys

The sentence that may be written only if G1–G4 hold: *"Here are the
principles. Here are the invariants (OT-7). Here is a theorem (OT-3).
Here are predictions registered before measurement, the experiments that
could have killed them, the ones that survived, and a phenomenon outside
the originating application that the framework predicted (OT-6)."*
