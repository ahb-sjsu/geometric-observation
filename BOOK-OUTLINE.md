# Book Outline — integrating the Freshness program into Volume 14

**This EXTENDS [`BOOK_PLAN.md`](BOOK_PLAN.md); it does not replace it.** The volume
is already fully drafted (front matter + 18 chapters + 7 appendices, ~33.8k words /
~100 pp). This file is the **annotated integration plan** for the material that
*postdates* that draft — the **freshness / witnessed-certificate program** (20
domain cells, the refresh-floor law, the governor) now living in
`observation-theory-campaigns`. Author with Write/Edit (never heredocs); markdown +
KaTeX; every claim carries a ledger class `[proved] [demonstrated] [replicated]
[predicted] [exploratory] [refuted]`; no umbrella sentence cites an `[exploratory]`
row (PROTOCOL Rule 1.1).

## 1. The gap (surfaced, not assumed)

The drafted volume is the **allocation** book: `tr(P_C·Σ)` read as *what to keep*
— COST / VALUE / LEGIBILITY, the blind probe, the recognizer, the κ-law, the
12-domain allocation sweep, GO-1…GO-6. A grep of `chapters/` finds **zero**
mentions of *false-clear*, *refresh floor*, *freshness*, *witnessed certificate*,
or any *XPROTO* cell. The freshness program — `tr(P_C·Σ)` read as *whether the read
is still true* — is a **second, disjoint reading of the same object** and is
entirely unrepresented. That is the whole integration.

## 2. The reconciliation (why it belongs)

The book's spine is "one object, three shadows" (COST/VALUE/LEGIBILITY), and Ch. 18
already names "identifiability" as a fourth face. **Freshness is the temporal/
operational face:** the same read operator `P_C`, but now the question is whether a
*certificate about the read* is still valid. The title — *what an observer can
**use*** — already implies it: you can only use what is still true. So freshness is
not a bolt-on; it is the reading the title promises and the drafted volume omits.

**Grammar (one thesis, many domains):** a **certificate** asserts a decision is
safe; it is (1) **consumer-relative** — evaluated through `P_C`, not an aggregate;
(2) **witnessed** — graded against an independent measurement; (3) refreshed within
a **coherence floor**. The reported metric is the **false-clear rate**. This is the
`tr(P_C·Σ)` staleness reading, dual to the allocation reading.

## 3. Structural decision — **Option A chosen (owner, 2026-08-24)**

Freshness is a **new Part in Volume 14** (Ch. 19–23), making it the complete
consumer-relative-observation thesis — both readings of `tr(P_C·Σ)`, allocation and
freshness, in one volume (~140–160 pp). Ch. 19–23 stay `chapters/ch19…ch23`; the
Vol-15 spin-out option below is retained only as a contingency if the Part outgrows
the volume.

### Options (for the record)

- **Option A — a new Part in Volume 14** (recommended). The volume is lean (~100
  pp); a ~30–40 pp freshness Part makes it the *complete* consumer-relative-
  observation thesis (both readings of `tr(P_C·Σ)`), ~140–160 pp total. Keeps the
  thesis unified. Chapters below (19–23) are written to be **relocatable** — if the
  Part outgrows the volume, the same files become Volume 15 wholesale.
- **Option B — Volume 15, "Reliability: The Witnessed Certificate."** A companion
  volume in the series. Cleaner if the freshness program keeps growing (its own
  metric, law, sweep, instrument, and standards path); Vol 14 gets a forward
  pointer. Choose this if you want each volume to stay a single coherent reading.

Either way the *chapter content is identical*; only the wrapper differs. The stubs
are authored as `chapters/ch19…ch23` for Option A; moving them is a rename.

## 4. The new Part — RELIABILITY: The Witnessed Certificate

Lean house density (~1.5–2.5k words/chapter), ledger-pointing (cites the campaigns
`SEALS.md`, not inlined runs). ~30–40 pp.

| Ch | Title | Draftable | Source material |
|---|---|---|---|
| **19** | The Certificate That Ages | **[A]** now | the grammar; `FRESHNESS-PROGRAM.md`; the read-operator's temporal face |
| **20** | The False-Clear Rate | **[A]** now | vacuity + consumer-relativity; the ZK hot/cold 99× (`analysis/zk`); routing 0.351/0.184/0.083 |
| **21** | The Refresh Floor | **[A]** now | OT-14 law ≈ 0.177·T_coh, R²=0.915 (`analysis/csi/CSI-refreshfloor`); prediction ≤ one coherence time (Gaussian → Wiener-optimal) |
| **22** | The Freshness Sweep | **[A]** now | the domain-generality table (below) — parallel to Ch. 13's allocation sweep |
| **23** | The Governor | **[A]** now | `governor.sealed/detector/ran/quantum`, `freshread`; O-RAN rApp; standards (`standards/ieee-sa-ic-...`) |

### Ch. 22 sweep table (honest tiers — the umbrella rests only on the sealed rows)

| Domain | Cell(s) | Substrate | naive → witnessed | Class |
|---|---|---|---|---|
| Interdomain routing | BGP/IS-IS/OSPF/RPKI/BMP, D8 | RIS beacons, live labs | 0.351 / 0.184 / 0.083 → detector band | **[replicated]** |
| Replication & coordination | PG/MG/PGX/GEO/ZK | real PG/Mongo/ZK, NRP fleet | ~0.5 → ~0.02–0.06; ZK 0.99/0.01→0 | **[replicated]** |
| Cellular PHY/RAN | CSI/BEAM/AICSI/HO/URLLC/PHY | Sionna 5G NR | 0.28–0.47 → 0.05–0.13 | **[demonstrated]** |
| Optical | QOT | GNPy GN-model | ~0.40 → ~0 (per footprint) | `[predicted]` (seal ≥08-25) |
| Power grid | GRID | pandapower AC-PF | ~0.25 → ~0.01 | `[predicted]` (seal ≥08-25) |
| AI evaluation | LLM | roberta-mnli / HANS | (shakedown running) | `[predicted]` |
| Quantum devices | QUANTUM | qiskit-aer (hand-built) | 0.28–0.43 → 0 | `[exploratory]` (gated: IBM hw) |
| Markets | QUOTE | efficient-price sim | 0.37 → 0.003 | `[exploratory]` (gated: tick data) |
| Sensing | (sensor) | real UCI field data | drift real, linear recal only ~1.6× | **[refuted]** (kept negative) |

The OT-14 refresh-floor law is **[demonstrated]** (measured, R²=0.915). The
umbrella thesis ("the witnessed certificate recurs across observation") cites only
the **[replicated]/[demonstrated]** rows; the rest establish breadth as `[predicted]`
/`[exploratory]`, and the sensor row is carried as an honest negative (Ch. 16 style).

## 5. Updates to the existing volume (small, surgical)

- **Ch. 13 (Domain-Generality Sweep):** a bridging paragraph — two sweeps now, the
  *allocation* sweep (12 domains) and the *freshness* sweep (Ch. 22); together the
  domain-generality of the read operator across both readings.
- **Ch. 18 (The Principle):** "four faces" → **five**: COST / VALUE / LEGIBILITY /
  identifiability / **reliability(freshness)** — all faces of one consumer-relative
  theory; Shannon the `P_C=I`, static slice.
- **Appendix D (Registry):** add the `XPROTO-*` IDs + the campaigns `SEALS.md`
  cross-repo provenance (sealing commit + SHA-256).
- **Appendix F (Mathematical Ledger):** add the freshness claims + the OT-14 law
  with classes; reconcile the campaigns `SEALS.md` into the ledger vocabulary.
- **Appendix C (Reproduction Cookbook):** add the freshness cells' run instructions
  (Sionna/GNPy/pandapower/qiskit substrates).
- **Preface / Ch. 1:** one line adding the freshness engineers (the operator who
  trusts a converged-routing signal / a fresh replica / a calibrated device) to the
  running "three engineers hit the same wall" opening.

## 6. Revised page estimate (correcting the earlier figure)

The earlier 400–700 pp was the *inline-everything* figure. The book's actual design
is lean-thesis + ledger-pointer, so:

- Current Vol 14: **~100 pp** (~33.8k words).
- + Freshness Part (Ch. 19–23, house density): **~30–40 pp**.
- + surgical updates to existing chapters/appendices: **~8–12 pp**.
- **Integrated Vol 14: ~140–160 pp.** The exhaustive catalog (20 cells, 24
  campaigns, 218 results, 32 preregs) stays in the repos + ledger *by design*, cited
  not reprinted. A companion "campaigns catalog" (Appendix D expanded, or the repo
  itself) is the reference volume.

## 7. Build status (this scaffold)

Stubs authored in `chapters/` for Ch. 19–23 (headers + source maps + content bullets
+ honest tags), Ch. 19 drafted as the voice/structure sample. `BOOK_PLAN.md` status
table to gain the five rows once the owner picks Option A vs B.
