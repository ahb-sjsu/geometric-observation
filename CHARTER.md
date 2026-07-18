# Geometric Observation — Research-Conduct Charter

> The independence and verification regime of **Observation Theory**.
> Companion to `PROTOCOL.md`: PROTOCOL governs *what counts as evidence* for an
> empirical claim; this CHARTER governs *how the program keeps itself honest* —
> independent verification, the AI-assistant conflict, theorem custody, and the
> discipline of losing in public.

**Status:** v1.0 — in force. **Scope:** every `[proved]` and `[demonstrated]`
claim in the trilogy (Papers I–III) and the claim ledger.
**House rule (inherited):** the book may not assert what the ledger cannot show.
**Standing fact:** much of this program is co-designed and co-authored with an
embedded AI assistant. This charter exists because that assistant **may not be
the sole grader of its own work** (§2), and because the program must be able to
**lose in public and continue smaller** (§6).

---

## 1. The R-IND independent-verification rules

Analytic and load-bearing claims are verified by a context **independent of the
author's chain of reasoning** — not merely re-read by the same author.

- **R-IND-1 (separation).** The verifier operates in a fresh context with no
  access to the derivation's working notes; it receives the claim and the
  toolkit, and reconstructs the argument itself.
- **R-IND-2 (adversarial default).** The verifier is tasked to **refute**, not
  confirm; it defaults to "wrong/unproven" and must be moved off that prior by
  its own reconstruction.
- **R-IND-3 (two grades).** *Derivation-grade* = the argument re-derived and
  checked line by line. *Conclusion-grade* = a committed numerical falsification
  net (§3, "C3") that would fail if the result were false. A result is not
  `[proved]` until it has both.
- **R-IND-4 (record before assertion).** The verifier's verdict, any
  corrections, and any citation flags are logged **before** any paper asserts the
  result. A pass with caveats is a caveated pass, not a clean one.
- **R-IND-5 (the fresh-context derivation-grade pass).** The operative instance
  of R-IND-1–4 for a theorem: a fresh-context, adversarial, derivation-grade pass
  on every lemma and theorem it will support, logged with its verdict. This is
  the rule cited by name throughout the ledger and preregs.
- **R-IND-6 (out-of-sample for confirmatory upgrades).** Promoting an
  `[exploratory]` finding to `[demonstrated]` requires a **fresh sealed prereg**
  and a run on **held-out** data/instances — never a replay of the set the effect
  was calibrated on. (Reference instance: GO-P-2026-027 confirmed the omission
  floor on held-out layers {4,20} after it was first seen on {8,16}.)

**Track record (the corpus of Verification Incidents, §5).** R-IND has caught,
before publication: an extreme-value scaling error (VI-2), an over-claimed
Appendix-B condition (VI-3), a **false-pass of the assistant's own `sigma_star`
formula** (VI-4), a non-iterating k-stage construction and a mis-attributed
citation (VI-5), a naive-kernel floor error (VI-6), and a "bijection" argument
that needed to be a covering argument (VI-7). The rule earns its place by its
catches.

---

## 2. The AI-assistant conflict

- **C-AI-1.** The embedded assistant may propose, derive, implement, and draft.
  It may **not** be the sole grader of an item it authored. Independence is
  supplied by R-IND-5 (a separate context) and, for confirmatory claims, by
  R-IND-6 (held-out, sealed-first runs).
- **C-AI-2.** When the assistant reports its own work as verified, it must state
  the grade (derivation vs conclusion), the verifier's identity (fresh context /
  committed harness), and any caveat — never "verified" unqualified. VI-4 is the
  standing reminder: an in-context self-check was partly tautological and passed a
  wrong formula; the fresh-context pass caught it.
- **C-AI-3.** Human authorship and accountability are unchanged: the human author
  owns every claim; the charter constrains *how* the assistant's contributions are
  admitted, not *whether* they are used.

---

## 3. Theorem custody

- **T-CUST-1.** Every `[proved]` item ships: a complete written proof; the R-IND-5
  fresh-context pass (verdict + findings logged); a **C3 numerical falsification
  harness** — pure, CPU-reproducible, committed, CI-run, and constructed to *fail*
  if the theorem is false; and a constants/slack + known-gaps table.
- **T-CUST-2 (C3 is a net, not a proof).** The harness cannot establish a theorem;
  it can only refute one. A green C3 with an unproven or unverified derivation is
  `[exploratory]`, not `[proved]`.
- **T-CUST-3 (citation flags).** External results a proof leans on are marked
  `[C7]`-style in the working notes and checked against the source before the
  paper asserts them; the flag never ships in the manuscript (grep before export).

---

## 4. Registration custody

- **REG-1 (seal before measure).** A prereg is hashed (`scripts/seal.py`) and
  **git-committed before** the first governed measurement it covers. The binding
  registration timestamp is the git commit, not the file mtime.
- **REG-2 (amendments dated, pre-unblinding).** Corrections to a sealed prereg are
  appended as dated amendments and re-sealed, with the reason stated; the original
  remains in git history. (Reference: GO-P-2026-022 amended when `sigma_star` was
  corrected.)
- **REG-3 (custody chain).** Sealed preregs, results, and harnesses are archived
  in the DOI deposit (Zenodo concept DOI 10.5281/zenodo.21423315), so the
  registered state is externally anchored, not only local.
- **REG-4 (counter).** Registration IDs are a single monotone sequence
  `GO-P-2026-###`; **the counter stands at 027**; the next free number is **028**.
  Never reuse or backfill a number.

---

## 5. Verification-Incident logging

- **VI-1.** Every false-pass, over-strict or mis-specified gate, or correction
  caught by the independence machinery is logged as a **Verification Incident**
  (`VI-n`) in the ledger, reported with the **same prominence as a positive**.
- **VI-2 (the over-strict-gate correction, standing).** A sealed gate can fail for
  gate-design reasons (a threshold too strict, a sweep too shallow) while the
  claim is true. When diagnosed, the gate flaw is logged and the claim is resolved
  by a *fresh* R-IND-6 test — not by quietly relaxing the sealed bar. (Reference:
  NEG-13 → GO-P-2026-027; the "<20% in a shallow sweep" criterion conflated
  *floor-reached* with *floor-exists*.)
- **VI-3 (misses are first-class).** A `[refuted]` or missed-gate row is carried
  into every downstream artifact (book, ledger, paper) as prominently as a win it
  bounds; softening a sealed miss after the fact is prohibited.

---

## 6. The stand-down clause

- **SD-1.** The program's pre-committed kill/narrow criteria (PROTOCOL §4 and the
  Phase-II gates) may fire. When they do, the **claims** narrow — publicly, in the
  ledger and the umbrella text — and the program **continues smaller**. Losing a
  bet does not end the program; hiding the loss would.
- **SD-2.** No umbrella statement may cite `[exploratory]` rows (PROTOCOL Rule 1.1);
  no result earns the name "Observation Theory" until its ledger row meets its
  class bar. The name is load-bearing only where the ledger is.

---

*v1.0. This charter codifies rules already in force through GO-P-2026-027; it adds
no retroactive burden to sealed claims that already satisfy them.*
