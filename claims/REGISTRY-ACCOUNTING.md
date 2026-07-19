# Registry ID accounting — GO-P-2026 series

*U0 deliverable (Observation.md §U0). The "no file drawer" claim rides on the
registration sequence having **no unexplained holes**. This table gives every
assigned `GO-P-2026-NNN` ID a disposition, so any reader can verify the sequence
is gap-free and every sealed run is reported at equal prominence — confirmations
and misses alike. Authoritative outcomes live in [`LEDGER.md`](LEDGER.md); this
table is the index that proves completeness.*

**Disposition classes.** `sweep` = reported in the Paper IV domain-generality
sweep (VALUE face). `core` = a falsifiable-core row (GO-1…GO-6) reported in
Papers I/I.5/II. `cost` = a COST-face theorem harness reported in Paper III.
`superseded→NNN` = a registered miss/flawed design corrected by a successor
(the miss is still reported — see LEDGER). `never-run` = ID never assigned to a
file or a run (numbering skip); proven absent from git history.

| ID | Registration | Disposition | Outcome (per LEDGER) | Reported in | Result JSON |
|---|---|---|---|---|---|
| 001 | KV-keys quotient transfer (GO-2, known instance) | core · superseded→002 | miss → NEG-5 (matched-bits confound) | Paper II · LEDGER NEG-5 | GO2-kv-keys.json |
| 002 | KV-keys transfer v2 (bit-matched redesign) | core | GO-2 neg-half `[demonstrated]`; NEG-6 | Paper II · LEDGER | GO2-kv-keys-v2.json |
| 003 | KV-keys transfer v3 | core | NEG-7 (invariant-preservation is a pair property) | Paper II · LEDGER | GO2-kv-keys-v3.json |
| 004 | Consumer-projected covariance governs downstream | core | NEG-8 (tang_qproj noisy proxy) | Paper II · LEDGER | GO2-kv-keys-v4.json |
| 005 | Projected covariance, gated directly | core | NEG-9 (trace governs flip, not full order) | Paper II · LEDGER | GO2-kv-keys-v5.json |
| 006 | The consumer flip, gated exactly (instance 1) | core | GO-2 pos-half `[replicated]` Instance 1 | Paper II · LEDGER | GO2-kv-keys-v6.json |
| 007 | Embedding retrieval, ranking consumer (prospective) | core · superseded→008 | NEG-10 (flip needs recon-matched arms) | Paper II · LEDGER NEG-10 | GO2-embed-retrieval.json |
| 008 | Retrieval, recon-matched probes | core · superseded→009 | substance + gate bug | Paper II · LEDGER | GO2-retrieval-matched.json |
| 009 | Retrieval matched, clean gate (prospective) | core | GO-2 pos-half `[replicated]` Instance 2 | Paper II · LEDGER | GO2-retrieval-matched-v2.json |
| 010 | Gradient compression, curvature consumer (Gate B) | core | GO-B `[predicted]` ✅ PASS 5/5 | Paper II / Gate B · LEDGER | GO2-gradient-curvature.json |
| 011 | GO-1 blind probe identifiability (blinded) | core | GO-1 `[predicted]` ✅ PASS 5/5 | Paper I.5 · LEDGER | GO1-blinded-probe.json |
| 012 | GO-3 certificate vacuity v1 | core · superseded→013 | v1 degenerate | Paper I.5 · LEDGER | GO3-certificate-vacuity.json |
| 013 | GO-3 vacuity v2 (corrected noise scale) | core · superseded→014 | core + step-band | Paper I.5 · LEDGER | GO3-certificate-vacuity-v2.json |
| 014 | GO-3 vacuity v3 (transition-width-honest) | core | GO-3 `[demonstrated]` 6/6 gated | Paper I.5 · LEDGER | GO3-certificate-vacuity-v3.json |
| 015 | GO-4 budget inversion (real Atlas embeddings) | core | GO-4 `[replicated]` 3/3 gated | Paper I.5 / III · LEDGER | GO4-budget-inversion.json |
| 016 | GO-5 α=1 density quotient v1 | core · superseded→017 | α hurts (density not in base) | LEDGER NEG-11 chain | GO5-alpha1-quotient.json |
| 017 | GO-5 α=1 quotient v2 (global-scale kernel) | core · superseded→018 | α hurts | LEDGER NEG-11 chain | GO5-alpha1-quotient-v2.json |
| 018 | GO-5 α=1 quotient v3 (ADC/PQ retrieval) | core · superseded→019 | α hurts | LEDGER NEG-11 chain | GO5-adc-pq.json |
| 019 | GO-5 α=1 diffusion distance v4 | core | GO-5 **`[refuted]`** NEG-11 (restoration <2%, not density-specific) | Honest Negatives · LEDGER | GO5-diffusion-distance.json |
| 020 | Gate B blind probe on a real Llama layer | core · superseded→021 | MISS (2/3 triggers) → NEG-12 | Honest Negatives · LEDGER NEG-12 | GateB-llama-keys.json |
| 021 | Gate B **rematch**, recon-matched dissociation | **sweep (A2)** | GO-B-Llama-rematch **HIT** 4/4 | Paper IV sweep · LEDGER | GateB-llama-rematch.json |
| 022 | Two-observer successive-refinement theorem (C3 harness) | cost | theorem confirmed; VI-4 false-pass logged + corrected | **Paper III** · LEDGER VI-4 | (harness / CI) |
| 023 | Complete rate region + k-observer chain (C3 harness) | cost | region confirmed; VI-5 (2 errors caught pre-pub) | **Paper III** · LEDGER VI-5 | (harness / CI) |
| 024 | The price of a misidentified observer (C3 harness) | cost | floor theorems confirmed; VI-6 | **Paper III** · LEDGER VI-6 | (harness / CI) |
| 025 | Dispersion counts read dimensions + separation (C3) | cost | confirmed with sharpenings; VI-7 | **Paper III** · LEDGER VI-7 | (harness / CI) |
| 026 | Omission floor unconditional on a trained Llama layer | cost · superseded→027 | read-floor 16/16 ✓, finite-rate gate MISSED (shallow-sweep) → NEG-13 | **Paper III** · LEDGER NEG-13 | GateB-weighted-floor.json · mismatch-asymptotic-floor.json |
| 027 | Omission floor bites downstream (asymptotic, held-out layers) | cost | NEG-13 **resolved** → `[demonstrated]` (downstream floor 16/16) | **Paper III** · LEDGER | GateB-asymptotic-floor.json |
| 028 | GO-6 output vs surrogate vs reconstruction at matched rate | core (App. B) | GO-6 `[demonstrated]` ALL PASS | **Paper III** App. B · LEDGER | (CI sentinel / verify_go6) |
| **029** | — | **never-run** | *numbering skip — no file, no run, no result; absent from full git history* | — | — |
| **030** | — | **never-run** | *numbering skip — no file, no run, no result; absent from full git history* | — | — |
| 031 | DOA Gate-B, simulated physical estimator | **sweep (A1)** | GO-B-DOA **HIT** 5/5 | Paper IV sweep · LEDGER | GO-DOA-gateb.json |
| 032 | PolarQuant DOA, held-out LOCATA | **sweep (A3)** · superseded→033 | MISS (flip 6/13 < 8/13); robust anti | Paper IV sweep · LEDGER | GO-LOCATA-polarquant.json |
| 033 | PolarQuant DOA, rehabilitated (fresh held-out) | **sweep (A3)** | GO-B-LOCATA **CONFIRMED** (flip 11/13) | Paper IV sweep · LEDGER | GO-LOCATA-polarquant-rehab.json |
| 034 | Domain-generality battery (D1–D4) | **sweep (D1–D4)** | D1 partial · D2/D3 confirmed · D4 honest null | Paper IV sweep · LEDGER | GO-{RaDICaL-radar,AV163-doa,PDAR-seismic,D4-optim}.json |
| 035 | Legal-retrieval flip (CourtListener) | **sweep (L)** · superseded→036 | MISS (estimated read op overfit, O>R held-out) | Paper IV sweep · LEDGER | GO-legal-retrieval.json |
| 036 | Legal-retrieval rehab via GO-1 blind probe | **sweep (L)** | GO-B-legal **CONFIRMED** (R 0.779 > O 0.771) | Paper IV sweep · LEDGER | GO-legal-retrieval-rehab.json |
| 037 | Reconcile the flip with turboquant-pro's (A2) probe | **sweep (M/K/Mu)** | (A2) verdicts (moral/music/KV); NEG-14 (unit_disp shortcut refuted) | Paper IV sweep · LEDGER NEG-14 | music-a2-reconciliation.json · whale-ketos-a2.json |
| 038 | Sealed whale coda-dialect flip | **sweep (W)** | GO-B-whale **CONFIRMED** 4/4 (held-out R 0.934 > O 0.883) | Paper IV sweep · LEDGER | GO-whale-dialect.json |

## Completeness argument

The assigned sequence is **001–038 with exactly two skips (029, 030)**, and every
other ID resolves to a registered run reported in the ledger. The three ID blocks
the sweep document does not enumerate are accounted for here:

- **022–028** are the **COST-face** theorem harnesses (successive refinement, rate
  region, observer mismatch, dispersion, omission floor, GO-6). They belong to
  **Paper III**, not the VALUE sweep — a different shadow of the same object
  (Observation.md). Four carry logged fresh-context verification incidents
  (VI-4…VI-7), all caught pre-publication. Their absence from the sweep doc is a
  scope boundary, not a suppression.
- **029, 030** were **never assigned** — no prereg file, no run, no result JSON
  ever existed under these IDs at any commit (verified: no filename containing
  `029`/`030` appears in `git log --all --name-only` over `prereg/`). The sequence
  jumped from the COST block (…028) to the physical-array block (031…). A
  numbering skip, documented here so it cannot be mistaken for a removed result.
- **032** is a **registered miss** (LOCATA held-out), reported at equal prominence
  and superseded by the sealed rehabilitation **033** — the same 020→021 and
  035→036 pattern (principled fix to a registered flaw, internal-split-guarded,
  sealed pre-run, fresh held-out data). The miss stays in the ledger; it is not
  a file-drawer.

**Supersession chains** (each miss/flaw reported, then corrected): 001→002 ·
007→008→009 · 012→013→014 · 016→017→018→019 · 020→021 · 032→033 · 035→036.

**No file drawer holds:** every sealed run appears in the ledger regardless of
sign; the only gaps in the ID sequence (029, 030) carried no run.

## Commit-ordering audit (seal predates run)

For every sealed confirmation the registration commit must be a genuine **ancestor**
in the git DAG of the commit that first added its result — not merely an earlier
calendar date (several share a day). Checked with
`git merge-base --is-ancestor <seal> <result-add>`; all pass:

| Row | Seal commit | Run commit (result added) | Ancestry |
|---|---|---|---|
| A2 021 (Llama rematch) | 3336594 | d72c2d7 | ✅ ancestor |
| A1 031 (DOA simulated) | ee85622 | e2c4bda | ✅ ancestor |
| A3 033 (LOCATA rehab) | 9c08089 | ee14f44 | ✅ ancestor |
| D2 034 (AV16.3) | 3b76e11* | a08febb | ✅ ancestor |
| D3 034 (PDAR seismic) | 3b76e11* | cbc1242 | ✅ ancestor |
| L 036 (legal rehab) | a6016bf | d9c5376 | ✅ ancestor |
| W 038 (whale dialect) | 0a7368a | 44cfbbd | ✅ ancestor |

\*034's battery file was created at `3b76e11`; the per-domain frozen configs were
sealed at `1843ebd` (D2) / `2de7927` (D3) — both descendants of `3b76e11` and
ancestors of their runs, so the seal-before-run chain holds a fortiori. Every
result commit is strictly downstream of its seal; the ordering is verifiable at
any snapshot (including the DOI'd release).

