# Appendix D — The Registry: Every GO-P-2026 ID and Its Disposition

*The "no file drawer" claim rides on the registration sequence having no unexplained
holes. This appendix gives every assigned `GO-P-2026-NNN` ID a disposition, so any reader
can verify the sequence is gap-free and every sealed run is reported at equal prominence
— confirmations and misses alike. Authoritative outcomes are in `claims/LEDGER.md`; this
table is the index that proves completeness. It mirrors `claims/REGISTRY-ACCOUNTING.md`.*

*Classical names used in the rows.* A "flip" is a ranking reversal between
reconstruction error and task loss (Shlezinger, Eldar and Rodrigues 2019). The "read
operator" is the consumer's active-subspace matrix (Constantine 2015). The "blind probe"
is finite-difference active-subspace estimation. "Two-observer successive-refinement"
is Gaussian successive refinement under individual distortion criteria (Equitz and
Cover 1991; Nayak, Tuncel, Gündüz and Erkip 2010). Appendix A has the references.

**Disposition classes.** `core` = falsifiable-core row GO-1…GO-6 (Papers I/I.5/II);
`cost` = a COST-face theorem harness (Paper III); `sweep` = a domain-generality row
(Paper IV, VALUE face); `superseded→NNN` = a registered miss/flawed design corrected by a
successor (the miss is still reported); `never-run` = an ID never assigned to a file or a
run; `void` = a reservation abandoned unsealed.

| ID | Registration | Disposition | Outcome (per LEDGER) |
|---|---|---|---|
| 001 | KV-keys quotient transfer | core · superseded→002 | miss → NEG-5 (matched-bits confound) |
| 002 | KV-keys transfer v2 (bit-matched) | core | GO-2 neg-half `[demonstrated]`; NEG-6 |
| 003 | KV-keys transfer v3 | core | NEG-7 (invariant-preservation is a pair property) |
| 004 | Consumer-projected covariance governs | core | NEG-8 (tang_qproj noisy proxy) |
| 005 | Projected covariance, gated directly | core | NEG-9 (trace governs flip, not full order) |
| 006 | The consumer flip, gated (instance 1) | core | GO-2 pos-half `[replicated]` Instance 1 |
| 007 | Embedding retrieval (prospective) | core · superseded→008 | NEG-10 (flip needs recon-matched arms) |
| 008 | Retrieval, recon-matched probes | core · superseded→009 | substance + gate bug |
| 009 | Retrieval matched, clean gate | core | GO-2 pos-half `[replicated]` Instance 2 |
| 010 | Gradient compression, curvature (Gate B) | core | GO-B `[predicted]` ✅ PASS 5/5 |
| 011 | GO-1 blind probe identifiability | core | GO-1 `[predicted]` ✅ PASS 5/5 |
| 012 | GO-3 certificate vacuity v1 | core · superseded→013 | v1 degenerate |
| 013 | GO-3 vacuity v2 | core · superseded→014 | core + step-band |
| 014 | GO-3 vacuity v3 | core | GO-3 `[demonstrated]` 6/6 gated |
| 015 | GO-4 budget inversion (Atlas embeddings) | core | GO-4 `[replicated]` 3/3 gated |
| 016 | GO-5 α=1 density quotient v1 | core · superseded→017 | α hurts |
| 017 | GO-5 α=1 quotient v2 | core · superseded→018 | α hurts |
| 018 | GO-5 α=1 quotient v3 (ADC/PQ) | core · superseded→019 | α hurts |
| 019 | GO-5 α=1 diffusion distance v4 | core | GO-5 **`[refuted]`** NEG-11 |
| 020 | Gate B blind probe, real Llama layer | core · superseded→021 | MISS (2/3 triggers) → NEG-12 |
| 021 | Gate B **rematch**, recon-matched | sweep (A2) | GO-B-Llama-rematch **HIT** 4/4 |
| 022 | Two-observer successive-refinement | cost | confirmed; **VI-4** false-pass logged + corrected |
| 023 | Complete rate region + k-chain | cost | confirmed; VI-5 (2 errors caught pre-pub) |
| 024 | Price of a misidentified observer | cost | floor theorems confirmed; VI-6 |
| 025 | Dispersion counts read dimensions | cost | confirmed w/ sharpenings; VI-7 |
| 026 | Omission floor on a trained Llama layer | cost · superseded→027 | read-floor 16/16 ✓, finite-rate gate MISSED → NEG-13 |
| 027 | Omission floor bites downstream (held-out) | cost | NEG-13 **resolved** → `[demonstrated]` |
| 028 | GO-6 output vs surrogate vs reconstruction | core (App. B) | GO-6 `[demonstrated]` ALL PASS |
| **029** | — | **never-run** | numbering skip — absent from full git history |
| **030** | — | **never-run** | numbering skip — absent from full git history |
| 031 | DOA Gate-B, simulated estimator | sweep (A1) | GO-B-DOA **HIT** 5/5 |
| 032 | PolarQuant DOA, held-out LOCATA | sweep (A3) · superseded→033 | MISS (flip 6/13); robust anti |
| 033 | PolarQuant DOA, rehabilitated | sweep (A3) | GO-B-LOCATA **CONFIRMED** (flip 11/13) |
| 034 | Domain-generality battery (D1–D4) | sweep (D1–D4) | D1 partial · D2/D3 confirmed · D4 honest null |
| 035 | Legal-retrieval flip | sweep (L) · superseded→036 | MISS (estimated read op overfit) |
| 036 | Legal-retrieval rehab via blind probe | sweep (L) | GO-B-legal **CONFIRMED** (R 0.779 > O 0.771) |
| 037 | Reconcile flip with (A2) probe | sweep (M/K/Mu) | (A2) verdicts; NEG-14 (shortcut refuted) |
| 038 | Sealed whale coda-dialect flip | sweep (W) | GO-B-whale **CONFIRMED** 4/4 |
| 039 | Legal flip on a fresh virgin split | sweep (L) | **CONFIRMED** 4/4 (margin 2× of 036) |
| **040** | κ magnitude-law prospective (reserved) | **void** | not sealed — κ magnitude law failed validation; reservation abandoned |
| 041 | Blind non-oracle flip + magnitude (20NG) | sweep (blind) | **PARTIAL** — blind code prediction held; magnitude band missed |

## Completeness argument

The assigned sequence is **001–041 with two skips (029, 030) and one void (040)**, and
every other ID resolves to a registered run reported in the ledger.

- **022–028** are the COST-face theorem harnesses (Paper III), a different shadow of the
  same object; their absence from the VALUE sweep is a scope boundary, not suppression.
  Four carry logged verification incidents (VI-4…VI-7), all caught pre-publication.
- **029, 030** were never assigned — no prereg, no run, no result JSON at any commit
  (verified: no filename containing `029`/`030` in `git log --all --name-only` over
  `prereg/`). A documented numbering skip.
- **040** was an unsealed reservation for the κ *magnitude* law, which failed validation
  and was abandoned (Paper IV Remark; the κ *ordering* law stands, Chapter 12). A void, not
  a removed result.

**Supersession chains** (each miss reported, then corrected): 001→002 · 007→008→009 ·
012→013→014 · 016→017→018→019 · 020→021 · 032→033 · 035→036 (→039).

**No file-drawer holds:** every sealed run appears in the ledger regardless of sign; the
only gaps carried no run.

## Commit-ordering audit (seal predates run)

For every sealed confirmation the registration commit is a genuine **ancestor** in the git
DAG of the commit that first added its result — not merely an earlier calendar date.
Checked with `git merge-base --is-ancestor <seal> <result-add>`; all pass (A2-021,
A1-031, A3-033, D2/D3-034, L-036, W-038). Every result commit is strictly downstream of
its seal; the ordering is verifiable at any snapshot, including the DOI'd release. (Full
commit hashes in `claims/REGISTRY-ACCOUNTING.md`.)

## Statistical audit (headline rows)

Every reported percentage carries its $n$, its sealed bar, and its null. Flip/recon-trade
nulls are a per-query coin flip ($p = 0.5$); the anti null is worst-of-three ($p = 1/3$).

| Row | Arm | Count | Bar | `P(≥k | null)` | Read |
|---|---|---|---|---|---|
| D2 AV16.3 | flip | 148/201 | ≥60% | 7.0e-12 | decisive |
| D3 PDAR | flip | 13/17 | ≥55% | 2.5e-2 | modest alone → carried by recon-trade 17/17 (7.6e-6) |
| A3 LOCATA | flip | 11/13 | ≥8/13 | 1.1e-2 | supported |
| W 038 | flip | 300/300 | ≥60% | 2⁻³⁰⁰ | decisive |
| L 039 | flip | 200/200 boot | ≥60% | 2⁻²⁰⁰ | virgin split, margin 2× of 036 |
| **D1 radar** | anti | 15/25 | ≥70% | 5.6e-3 | above chance, below bar → registered MISS (partial) |
| **D4 optim** | flip | 82/300 | >50% | ≈1.0 | at/below chance → honest NULL (correct) |

The two non-confirmations are kept explicit: D1's anti control is above its worst-of-three
chance but below the sealed bar (the tiny array's ~15° resolution) → **partial**; D4's flip
sits at the coin-flip null while its anti arm is 300/300 → the read operator governs the
task but the flip is genuinely absent (curvature ≡ signal-energy coupling) → **honest
null**. Legal-036's thin margin (Δ=0.008) is the one row that needed a caveat, and it was
resolved by the virgin-split rerun 039 (Δ=0.016, double), removing the held-out-reuse
asterisk.
