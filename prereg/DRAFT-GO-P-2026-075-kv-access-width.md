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

- P1 (RESCOPED per the 2026-08-05 novelty sweep): NOT the directional
  claim "full history beats snapshot" — A2SF (arXiv:2407.20485,
  full-text verified) already swept a history-width knob and found
  less history can win, adverse prior art for the directional form.
  P1 is the QUANTITATIVE prediction no one has tested: at matched
  recomputation budget, the quality gap between full-history and
  snapshot policies, RESOLVED BY ENTRY AGE, follows the theory's
  closed-form staleness tax (rising with age under slice access,
  age-flat under path access) — a shape prediction that accommodates
  the A2SF regime.
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

**Novelty flank SWEPT (2026-08-05, arXiv-API mode; report in the
session task output).** Verdicts: history-width axis ADJACENT-KNOWN
(A2SF's sweep, adverse-direction; SnapKV never compares against full
history; matched-budget age-resolved dissociation absent everywhere);
KV-as-rate-distortion KNOWN including a sequential Wyner-Ziv
side-information formalization (Kim, arXiv:2605.25085 — the closest
theory neighbor, must be DISCUSSED not just cited) — staleness/aging
absent from that wave; age-as-signal thoroughly known
(LRU/Marconi/EntropyCache), age-vs-width dissociation absent;
**equal-uncertainty control NOVEL** (uncertainty-as-signal exists:
CONF-KV, ForesightKV, KVpop — as a matched CONTROL, nowhere);
**Landauer framing for cache eviction NOVEL** (arXiv null result,
verified-empty). Claimable: the access-width framing + closed-form
tax, the age-resolved matched-budget design, P2, the Landauer
interpretation. Full 21-entry attribution list in the sweep report.
Residual before seal: a 10-minute Semantic Scholar/DBLP pass in a
fresh session (rate-limited this session) for non-arXiv systems
venues.
