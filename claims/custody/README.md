# Custody files for `[proved]` rows

A ledger row reaches `[proved]` only when CHARTER T-CUST-1 holds:

1. a complete written proof;
2. a logged R-IND-5 fresh-context pass, a VI row in [`LEDGER.md`](../LEDGER.md);
3. a C3 harness that is pure CPU, committed, CI-run, and built to fail if the result is false;
4. a table of constants, slack and known gaps.

This directory holds item 4, one file per ledger row, named `<row ID>.md`. Each file
also points to items 1 to 3. The format is in the docstring of
[`scripts/check_custody.py`](../../scripts/check_custody.py), which CI runs in shard 0.

**What `check_custody.py` checks:**
- every required section is present;
- every cited VI row exists in the ledger;
- every harness either runs in CI or is declared committed-artifact with its JSON cited;
- every measured value matches the committed JSON it cites, or, for a harness that prints
  instead of writing JSON, appears verbatim in the text file it cites (for example a sealed
  prereg's recorded outcome, whose text `verify_seals.py` guards);
- no `[C7]`-style citation flag or `TODO:` is left.

**What it cannot check** is whether the proof is right. That judgement rests on the
R-IND-5 verifier and the owner. A file is written only after its VI row exists
(R-IND-4: record before assertion).

Floating-point certificates are nets, not proofs (T-CUST-2). They can appear here as
measured values with their slack, never as the proof.
