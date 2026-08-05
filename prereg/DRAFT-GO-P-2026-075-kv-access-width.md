# DRAFT (UNSEALED) — GO-P-2026-075: access width on a real serving system (KV-cache staleness)

STATUS: DRAFT. ID 075 reserved; NO hash, NO seed; §5.1 requires the
instrument pilot before seal, and the governed GPU run additionally
awaits the user's explicit compute go-ahead (Atlas GPU 1; checked
idle 2026-08-05, 9 MiB / 50 °C; house Atlas rules apply:
CUDA_VISIBLE_DEVICES=1, thermal caps, no process interference).

**The claim family under design (successor to 056/NEG-16, now with
the GO-12/13 access-width theory behind it).** KV-cache entries are
records; the model's rolling context is the aging reference; eviction
and recomputation are erasure. The access-width dichotomy predicts:

- P1 (path vs slice, the 065 analog): a KV-eviction policy with
  access to the FULL attention history of an entry (path) pays no
  staleness penalty in downstream task quality at matched
  recomputation budget, while a policy restricted to the entry's most
  recent attention snapshot (slice) pays a penalty growing with entry
  age — measured on the consumer's task metric, never reconstruction.
- P2 (equal-q universality, the 067/069 analog): two structurally
  different access policies calibrated to equal predictive uncertainty
  about an entry's future attention mass score equal task quality —
  the analytic-equality control, instrument-friendly.
- P3 (sign law, the 068 analog, exploratory first): whether the
  multi-consumer (multi-head / multi-query) sharing penalty rises or
  falls with context staleness, classified by the binding-consumer
  coupling heuristic before any gate is set.

**Instrument sketch**: Qwen2.5-7B on Atlas GPU 1 (056 lineage);
long-context eval set with per-entry attention-mass telemetry;
eviction policies as the access classes; task metric per the 056
conventions; shuffled-reference null; §5.1 pilot to calibrate bars
with ≥1.3× margins. Design freeze BEFORE instrument code, per the 069
precedent.

**Open design questions for the pilot phase**: the operational
mapping from q_G to attention-mass predictive variance (needs an
exploratory calibration run, disclosed); eval-set choice (long-context
QA vs retrieval); runtime budget (~hours on GPU 1, thermally capped).

Novelty flank owed before any seal: KV-eviction/compression
literature (H2O, StreamingLLM, SnapKV lineage, attention-sink work)
— the access-width FRAMING and the equal-uncertainty control appear
unclaimed, but the sweep must run first.
