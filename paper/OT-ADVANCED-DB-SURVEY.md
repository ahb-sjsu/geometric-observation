# Observation Theory × Advanced Database Systems — literature survey

Written 2026-08-21. Companion to `OT-DATABASES-SURVEY.md` (the
textbook-anchored survey); this one mines the advanced canon: the Red
Book 5/e, Architecture of a Database System, Database Internals, DDIA,
Gray & Reuter, Weikum & Vossen, Özsu & Valduriez, CMU 15-721, the
weak-isolation literature, the self-driving/learned-systems line, and
the 2023–2026 emerging areas (vector DBs, IVM/streaming, lakehouse,
feature stores). Three recon agents, ~60 sources checked with links in
the underlying reports; recon-grade — sealed campaigns owe
quote-verification. Boundaries binding throughout: replica routing /
freshness certificates ceded to the concurrent network-governor
XPROTO-GEO program; basic textbook areas covered in the companion
survey; DB-1 (precision allocation) already sealed `[predicted]`.

The organizing lens that survived contact with all three clusters:
**"declared → probed."** Everywhere the field prices imprecision, the
demand side is DECLARED (error bounds, QoS curves, consistency
categories, SLAs, per-column tolerances) or REACTIVE (traces, feedback,
demand-driven recovery). Recovering the demand curve by query-only
probing of the consumer — quadratic, prospective, probe-cost-charged —
is the recurring unoccupied position. Pattern-validation citations
(fields that already learned the pattern's value in narrower forms):
Monkey (budgeted filter allocation), Flow-Loss (estimate precision
where it matters), budget-aware index tuning (probe cost charged),
ScaNN (loss-aware codebooks for the ranking itself).

## Flagship tier (open, buildable, well-bounded)

### F1. Consumer-probed quantization allocation for vector indexes
Allocate per-dimension/per-subspace quantization bits in a vector
index by min tr(P̂_C Σ(b)), P̂ probed query-only from the downstream
consumer (RAG answer quality, classifier loss), at matched memory —
vs recall-tuned uniform allocation. **Why now:** Extended RaBitQ
(SIGMOD 2025; adopted by LanceDB/Weaviate/Milvus) provides the
per-dimension bit knob WITH theoretical error bounds = a ready-made
Σ(b); "Recall What Matters" (arXiv 2606.04522, June 2026) just
published the motivation — downstream quality is flat until recall
~0.4, recall overstates needed compute 1.9–9.4× — with no allocation
mechanism; Fisher-curvature bit allocation is standard for MODEL
WEIGHTS (FIMA-Q CVPR'25, TAQ) and unclaimed for stored embeddings.
Adversarial baselines to beat: JPQ/RepCONC (white-box, training-time,
encoder-entangled), ScaNN anisotropic VQ (loss = the ranking itself),
BAPQ (distortion-driven unequal bits). Risk: the flatness plateau
means wins must be shown in consumer-sensitive regimes at matched
memory. The window is open and visibly closing. **DB-1's machinery
transplants nearly whole.**

### F2. Consumer-relative isolation (probed anomaly-class sensitivity)
Probe a black-box consumer with MonkeyDB-style injected weak-isolation
behaviors to recover a quadratic sensitivity over Adya anomaly
classes; combine with measured per-class anomaly rates (Elle-style
accounting / PBS-style prediction); choose per-transaction-class
isolation minimizing tr(P̂_C Σ_anomaly) at matched concurrency budget.
Bounded by four citable lines, none of which occupies it: Fekete/
TxnSails (zero-anomaly serializability objective), Kraska consistency
rationing (declared scalar per-item penalties — the economic ancestor
to beat head-to-head), Crooks client-centric isolation (the formal
substrate, qualitative), MonkeyDB/Elle/IsoDiff (binary bug-finding —
and MonkeyDB is the probe instrument, repurposed). Two clauses without
which the claim collapses to 2009: probe cost charged; matched-budget
comparison against rationing. Scope: aggregate/analytic consumers
(damage smooth in anomaly rate), not assertion-style ones.

### F3. Directional optimizer-statistics refresh (optimizer as consumer)
ANALYZE budget allocated by tr(P̂ Σ_staleness) where P̂ = the
optimizer's plan-sensitivity to statistics perturbations, probed
query-only through EXPLAIN (a free what-if interface), and Σ = stats
drift covariance from the update stream. Baselines: Oracle auto-stats
urgency classes, DB2 UDI counters, LEO feedback — all churn/feedback
driven, retrospective, direction-blind. The program's DR result
("directional beats age-based") transplanted onto the canonical
internal consumer. **Lowest risk, fastest to a sealed campaign;
DuckDB/Postgres testbed local.**

### F4. Task-probed lossy encoding in column stores
Per-column codec/bit selection by probed downstream-task sensitivity
(rate-distortion under a probed quadratic consumer geometry) at
matched storage/scan budget. CodecDB (SIGMOD'21, lossless) explicitly
lists query-aware + lossy selection as future work; scientific
compressors take declared bounds. Direct extension of sealed DB-1
from the fine/coarse ladder to real codecs — the byte-realism upgrade
DB-1's prereg already names as future work.

## Second tier (open but narrower, or requiring more setup)

- **S1. Probed recovery prioritization** (instant-recovery redo/restore
  ordering + restore-bandwidth allocation by tr(P_C Σ_unavail)):
  genuinely unoccupied; Graefe's demand-driven ordering is the perfect
  foil (reactive 0/1 vs prospective quadratic); mechanism exists,
  only the allocation theory is missing. Zero boundary risk.
- **S2. Per-operator staleness/precision allocation in IVM dataflows**
  (DBSP/Materialize/Feldera): the purest declared→probed upgrade found
  anywhere — stream load shedding has run on user-declared QoS curves
  since Aurora (2003), unchanged; DBSP's linear-operator algebra
  composes exactly with a quadratic consumer geometry. Interior
  allocation only (refresh-exterior partially claimed by this program;
  routing ceded).
- **S3. The alignment-tax family, industrialized**: geometric pricing
  of shared multi-tenant memory/cache pools (vs MT-LRU/SQLVM hit-rate
  SLAs; Shapley-style DB cost sharing essentially absent) and of
  shared vector-index quantization tiers (one collection, many apps).
  DB-2's result (in flight) is the synthetic core; these are its
  deployment surfaces.
- **S4. Lakehouse cold-start layout** ("layout without a trace"):
  clustering-dimension and zone-map precision selection by probing
  when no trace exists (new consumer / post-drift) — the one regime
  where Qd-tree/MTO/liquid-clustering incumbents are structurally
  blind.
- **S5. Sensitivity-priced error-tolerant tiering**: degraded
  (lossy/stale) cold copies where probed consumer tolerance permits —
  upgrades Siberia-style frequency scoring; no prior art found on
  precision-degraded tiers.
- **S6. Damage-weighted transaction scheduling / victim selection**:
  conflict-prediction schedulers (crowded supply side) given the
  missing objective — probed per-class abort/delay damage.
- **S7. Smaller open cells from the theory cluster**: consumer-
  insensitive transaction chopping (beyond SC-graph correctness, into
  measured-immaterial-damage territory — a strictly larger feasible
  set); probed escrow sizing; per-object durability cadence (probed
  form of async-commit flags); consumer-weighted checkpoint cadence.

## Position/umbrella claim

**The consumer-side complement to self-driving DBMSs.** The entire
self-driving line (NoisePage, Azure auto-everything, SageDB)
instruments the DBMS internally and stops at the SQL boundary; its
behavior models never see the downstream application. OT's query-only
probing of external consumers is a structurally different information
source that composes with, rather than competes against, that line.
This is the honest positioning for any OT-DB paper and could anchor a
vision piece wrapping F1–F4.

## Avoid / conceded (with the reason)

LSM compaction scheduling (EcoTune SIGMOD'25 + an active subfield);
learned cardinality estimation core (Flow-Loss/PARQO already do
precision-where-it-matters); RAG retrieval-depth allocation (2025-26
land rush); knob tuning (OtterTune lineage); Bloom-filter allocation
(Monkey solved it — cite as validation); adaptive compilation (Umbra);
HTAP delta-merge freshness scheduling (PVLDB'26 joint-adaptive work +
ceded-program adjacency); watermark/lateness budgets (open but
boundary-adjacent — coordinate first); versioning retention (open but
dead-cold); replica anything (ceded).

## Suggested sequence

1. **F3** (optimizer-stats refresh) — fastest seal, local, the DR
   transplant with beatable industrial baselines.
2. **F1** (vector-index quantization) — the big bet; build on
   Extended RaBitQ + a local RAG consumer; the window is now.
3. **F4** (lossy codecs) as DB-1's byte-realism successor, then
   **S3** as DB-2's deployment surface.
4. **F2** (consumer-relative isolation) — flagship-grade but heaviest
   instrumentation (MonkeyDB harness); schedule when a systems-venue
   push is wanted.
5. **S1** (recovery prioritization) as the low-collision sleeper.
