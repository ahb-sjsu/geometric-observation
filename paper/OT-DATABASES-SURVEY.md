# Observation Theory × Database Systems — an opportunity survey

Written 2026-08-21. Anchors: Silberschatz–Korth–Sudarshan, *Database
System Concepts* 7/e (2019) chapter structure, and the CMPE 180B
lecture sequence (Bond, FA26) mapped lecture-by-lecture. Scope note:
the textbook PDF was not on disk at survey time, so anchors are at
chapter level, not page level. The prior-art layer below is
RECON-GRADE (one web pass, key claims verified, a few venue/dates
from memory flagged by the recon agent) — a sealed campaign owes the
usual quote-verification sweep first.

## 0. The dictionary

| OT object | Database instantiation |
|---|---|
| Consumer C | an application / workload / query class / dashboard / downstream model reading the database |
| Read operator P_C = JᵀGJ | quadratic sensitivity of the consumer's ANSWER QUALITY to perturbations of stored values, per attribute/column — recoverable by query-only probing (run the workload against perturbed data, read the loss) |
| Uncertainty Σ | whatever the system's resource decision controls: staleness covariance of cached/replicated/materialized data; statistics-estimation error; sampling error; lossy-encoding quantization error |
| Composition tr(P_C Σ) | the consumer-relative cost of the system's current imprecision |
| Matched budget | refresh bandwidth, statistics space, sample size, storage bytes, buffer frames — held equal across policies |
| Probe cost charged | probing runs consume the same resources being allocated; the ledger is part of the claim |

The program's transplant results: DR-3 (directional staleness beats
age-based AND isotropic signal-aware refresh at matched budgets),
LM-2 (precision allocation by probed geometry captures the full
known-geometry advantage; coarsening what the consumer does not read
can actively help), EC-6 (a multi-consumer tax with angular shape
prices one resource serving divergent read geometries).

## 1. Per-area assessment (ranked by promise)

### A. Lossy encoding / column precision by probed workload sensitivity — ★★★ headline candidate
**Book/course anchor:** ch. 12–13 (storage, column organization,
compression); course L10 (physical storage).
**OT instantiation:** choose per-column encoding precision (bit
width, decimal truncation, dictionary coarseness) to minimize
tr(P̂_C Σ_quant) at a storage budget, P̂ probed from the actual
workload. Includes the LM-2 discovery as a PHYSICAL-DESIGN
phenomenon: coarsening columns the workload does not read can
IMPROVE downstream answer quality (regularization at the storage
layer), not merely save bytes.
**Nearest prior art (conceded):** compression-aware physical design
(Kimura et al., PVLDB 2011 — lossless, cost-only); SPARTAN semantic
compression (SIGMOD 2001 — user-DECLARED per-column tolerances);
QoI-preserving scientific compression (PVLDB 2023, QPET — requires
the downstream function in CLOSED FORM).
**Open conjunction:** probed sensitivity (no closed form, no declared
tolerances) → budgeted allocation → and the coarsening-helps effect,
which the recon found NOWHERE in the DB literature.
**First experiment (cheap, local, campaign-shaped):** DuckDB or
SQLite column store; planted analytic workloads with known read
structure; probe by perturb-rerun; arms aligned/oracle/anti/
mean-4-task-blind at matched bytes (the LM2-002 harness pattern
transplants nearly verbatim, degeneracy-proof baseline included).
Zero API cost, fully deterministic — EC-grade seals possible.

### B. Multi-workload physical design as the alignment tax — ★★★ headline candidate
**Book/course anchor:** ch. 13–14 (indexing), ch. 25 (tuning);
course L11 (indexing), L14 (architectures).
**OT instantiation:** one index set / materialized-view set / layout
serving consumers C1, C2 with read geometries P_1, P_2: the
egalitarian best-shared-over-utopia tax as a function of the
principal angles between P_1 and P_2 — EC-6 transplanted from sensor
schedules to physical design.
**Nearest prior art (conceded):** view selection benefit functions
(Gupta ICDT 1997; Gupta–Mumick); multi-query optimization sharing
(Mistry et al., SIGMOD 2001); CloudViews subexpression reuse at
datacenter scale (PVLDB 2018); SQLVM multi-tenant isolation (CIDR
2013). All price sharing SYNTACTICALLY (subexpression overlap) or
PHYSICALLY (resource contention).
**Open conjunction:** a GEOMETRIC price of sharing — tax as a
function of read-geometry alignment, shown non-derivable from
additive benefit functions. Recon's judgment: genuinely unoccupied.
**First experiment:** two planted workloads at controlled angles over
one table; shared vs dedicated index budgets; measure the tax curve
(the EC-6 harness shape).

### C. Materialized-view / replica / cache refresh by directional staleness — ★★☆ (strong, but a live competitor)
**Book/course anchor:** ch. 16 (materialized views in optimization),
ch. 23 (replication/consistency); course 10b (Ceph), L15b (pipelines).
**OT instantiation:** refresh budget allocated by
S_C(Δ) = tr[P_C Σ_staleness(Δ)] — the DR track verbatim: refresh what
the consumers READ, not what is oldest nor what changed most in
aggregate.
**Nearest prior art (conceded, and one DANGER work):** crawler
freshness (Cho & Garcia-Molina, TODS 2003 — change-rate-aware, not
consumer-aware); TRAPP/divergence caching (Olston & Widom — DECLARED
per-value precision); QoD WebView materialization (Labrinidis &
Roussopoulos); relaxed currency bounds (Guo et al., SIGMOD 2004).
**RALF (PVLDB 2024) is the danger work**: consumer-accuracy-aware
feature-store refresh beating staleness-based scheduling — REACTIVE
(needs post-hoc error labels), scalar per-key regret. The OT claim
survives ONLY in the strictly stronger form: PROSPECTIVE, QUERY-ONLY
probed, DIRECTIONAL (cross-attribute quadratic), with RALF-style
reactive scheduling as a required baseline. Weaker phrasings are
taken.
**First experiment:** materialized aggregates over drifting base
tables; refresh-k-of-n per epoch; arms directional / age (LRU-ish) /
change-volume (isotropic signal-aware) / RALF-style reactive.

### D. Statistics/histogram precision by consumer geometry — ★★☆
**Book/course anchor:** ch. 15–16 (query processing/optimization);
course L12.
**OT instantiation:** continuous per-attribute statistics precision
(bucket counts, sample sizes for stats) minimizing tr(P̂ Σ_est) at a
stats-space budget — where the consumer can be the OPTIMIZER (plan
quality) or the APPLICATION (answer quality on approximate plans).
**Conceded:** self-tuning histograms (SIGMOD 1999), STHoles, LEO
feedback (VLDB 2001), essential-statistics selection (ICDE 2000),
SITs/CORDS. All allocate by access pattern or optimizer benefit,
binary build/skip, never probed answer-quality curvature.
**Open conjunction:** per the recon — continuous precision allocation
from probed quadratic loss composed with estimation error; unclaimed.

### E. What-if interfaces as formal P̂ recovery — ★★☆ (theory-first)
**Book/course anchor:** ch. 25 (tuning/advisors).
**OT instantiation:** the DBMS world has practiced query-only probing
since AutoAdmin's what-if interface (SIGMOD 1998) — but always
probing the OPTIMIZER's cost model. OT's contribution is a formal
identification statement: the conditions under which query-only
probing of the downstream APPLICATION's loss identifies P_C (the
LM-1 recovery result, with its held-out predictive gate), plus probe
cost as a first-class budget term. Biathlon (PVLDB 2024) probes a
served model's input-resilience per inference — the nearest work; it
does not identify a quadratic form nor drive offline physical design.
**Deliverable shape:** a short formal paper + the LM-1-style
recover/match experiment on a DB application.

### F. Approximate query processing allocation — ★☆☆
Conceded heavily (BlinkDB declared error targets; ABae/SUPG
statistical guarantees; visualization-aware sampling as fixed-metric
task-awareness). The open cell — probed downstream loss across
attributes/strata at matched sample budgets — is real but crowded,
and Biathlon-adjacent. Fold into A or D rather than standalone.

### G. Buffer management / eviction — ★☆☆
LRU is the age heuristic; DR says direction beats age. But the
caching literature (including cost-aware and ML-based eviction) is
vast and the win over frequency+cost-aware policies is uncertain.
Exploratory only.

### H. Course-specific hooks (beyond the textbook)
- **Ceph/CRUSH placement (course 10b):** replica placement and
  recovery prioritization weighted by consumer read geometry —
  the tax (B) and refresh (C) questions at the object-store layer.
- **Data-lake tiering (L15b):** hot/warm/cold tier assignment as
  precision allocation; quantize-the-unread maps to aggressive
  compaction of unread partitions with a measured quality claim.
- **Governance/quality (L17):** data-quality effort prioritized by
  tr(P_C Σ_quality) — which fields' errors actually reach consumers;
  thin as research, good as a lecture example.

## 2. Recommended sequence

1. **DB-A (quantize-the-unread as physical design)** — cheapest,
   local, deterministic, reuses the LM2-002 harness discipline, and
   carries the survey's most surprising headline if it replicates on
   a real engine. Candidate track: DB, first seal PREREG-DB1-001.
2. **DB-B (the alignment tax for shared indexes)** — the second
   unoccupied cell; EC-6 harness shape.
3. **DB-C (directional refresh)** — biggest practical stakes, but
   sealed only with RALF-style reactive as a required baseline and
   the beats-isotropic-signal-aware bar (the DR-3 anchor discipline).
4. **E as a companion formal note** (identification conditions),
   citing the LM-1 three-seal record as the existing evidence.

## 3. Teaching tie-ins (CMPE 180B)

Low-effort, high-signal classroom uses: (i) L10/L11 — a 15-minute
segment on "what does the workload actually read?" with the
quantize-the-unread demo on DuckDB (a one-notebook experiment);
(ii) L12 — histogram budgets as precision allocation; (iii) 10b —
CRUSH placement as consumer-blind vs consumer-aware allocation;
(iv) a semester project template: probe a workload, recover P̂,
allocate an index/statistics budget, evaluate at matched cost —
the whole OT loop at course scale.

## 4. Novelty posture (binding for any seal)

Claim only the conjunction — (query-only recovery of P_C) ×
(analytic Σ-composition) × (prospective matched-budget allocation
with probe cost charged) — as one indivisible claim; cite RALF,
Biathlon, QoI-compression, and TRAPP as taking each pairwise
projection. The two headline cells (alignment tax; coarsening-unread
-helps) are unoccupied per this recon but owe quote-verification
before any sealed prereg quotes them.
