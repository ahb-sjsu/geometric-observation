# The Third Crucible — campaign specification

**STATUS: DRAFT-UNSEALED (drafted 2026-08-15, the same calendar day the
families were constructed and qualified). Per the rate-limit rule
earned in `OT-CRUCIBLE-2-VERDICT.md` and restated in
`FAMILIES-CRUCIBLE-3.md`, nothing in this document binds until a dated
SEAL declaration is added in a later working session. The runners
refuse to execute while this status stands. Drafting tonight, sealing
later, is itself the rule working as intended.**

## What this campaign is

Three tests, one per pre-qualified family, consuming the three open
debts left by two campaigns: the v0.2 revisions of **P4** and **P5**
(untested in substance since the Second Crucible's instrument deaths)
and **P2**'s forward-transfer owed prediction (whose OT-9 estimator
died of ESS-1 degeneracy). Canonical principle text: readscope
`PRINCIPLES.md` v0.2; revision record `OT-V0.2-REVISION.md`.

| test | principle / owed prediction | family | appendix |
|---|---|---|---|
| OT-13 | P5 — the two floor curves | F1 log-spread signals | `PREREG-OT13-APPENDIX.md` |
| OT-14 | P4 — feedback-free staleness | F2 mixture-drift dial (qualified v3 config) | `PREREG-OT14-APPENDIX.md` |
| OT-15 | P2 — forward transfer | F3 moment-matched estimator, n ≥ 48 | `PREREG-OT15-APPENDIX.md` |

All three families hold **committed interior evidence**
(`FAMILIES-CRUCIBLE-3.md`, commits `9d782c3` + `eb2f756`;
`results/FAM1-shakedown.json`, `results/FAM2-shakedown-v3.json`,
`results/FAM3-shakedown.json`). The F2 caveats recorded there — (i)
analytic operators declared as the instrument or blind-probe cells
budgeted above the noise floor, (ii) the full fixed cs pool as the
τ = 0 reference (the N_Q = 400 arm is invalid), (iii) eval noise from
proper subsamples only — **bind OT-14's appendix verbatim**, and each
appendix cites the family requirements it inherits.

## Graduation rule (fresh — the Second Crucible's H-rules expired with it)

- **G1 (per-principle graduation).** OT-13 and OT-14 each graduate
  their principle's v0.2 revision individually: PASS moves the
  revision from "untested-in-substance" to **earned**; FAIL returns
  that principle to revision carrying the as-executed record. They do
  not gate each other.
- **G2 (the transfer law).** OT-15 PASS establishes moment-matched
  probing as P2's named transfer estimator, discharging the owed
  prediction. FAIL records the transfer debt open with the *direct*
  estimator also dead — a finding, not a revision trigger (P2's
  statement does not name the estimator).
- **G3 (no vacuous outcomes).** A VOID on a pre-qualified family is
  an appendix-authoring failure, closes that test **unresolved**, and
  may not be regraded or re-familied within this campaign.
- **G4 (campaign close).** The crucible closes when all three tests
  resolve or exhaust their revision budget. 3/3 PASS may be recorded
  as "v0.2 graduated in substance." **No v1.0 declaration follows
  from this campaign under any outcome** — P3's owed prediction (the
  noisy cliff) is not in this test set, and v1.0 is not available
  while any principle's owed prediction is unconsumed.

## Cadence and revision budget

- **No appendix is sealed the day its family was first constructed**
  (kept; the reason this document is a draft tonight).
- Appendices and runners are committed **before** their runs; results
  are committed **as executed**, FAILs kept.
- Each appendix may take at most **two instrument revisions**
  (v2, v3), each sealed before the run it governs, each fixing
  instrument specification only — never the claim, never the
  bar-to-claim mapping. **No final-revision clause may appear in a
  first seal** (the Second Crucible's deadliest habit: it converts
  instrument defects into permanent verdicts).
- One test per sitting where practical; never all three graded from
  runs launched in the same sitting without reading the first result.

## The seven inherited instrumentation lessons

Every appendix and runner in this campaign is checked against these
before sealing; sources in parentheses.

1. **A family must show its interior before bars bind to it** — knob
   sweeps demonstrated in committed shakedowns, never assumed
   (OT-12 v1/v2, OT-11; hence `FAMILIES-CRUCIBLE-3.md`).
2. **Check every bar against the program's own committed record** —
   OT-10 died of a contrast sub-bar that contradicted OT-3's numbers,
   while every theorem quantity held (OT-10-NOTES).
3. **Estimator health is a manipulation check, not an assumption** —
   ESS floors, sampling floors, noise floors measured in-run and
   VOIDing on failure (OT-9's ESS ≈ 1; F2-v2's 0.5 probe floor).
4. **Bar the parent quantity, not a quantized derivative of it**
   (OT-5 v1's flat flip-rate).
5. **Condition recovery claims on the target actually being hidden**
   (OT-3/OT-5 notes).
6. **Verify the consumer realizes the operator before probing it**
   (OT-1 Arm R's 590× error from a rank-1 scalar-sum consumer).
7. **Eval-noise estimates must come from proper subsamples** — a
   resample that draws the whole pool is zero-noise by construction
   (two degenerate zeros caught and recorded in F2 v3's own runs).

## Seal declaration

*(empty until a later working session; the seal is a dated entry here
naming the three appendix files and their commit hashes, after which
the runners will execute)*
