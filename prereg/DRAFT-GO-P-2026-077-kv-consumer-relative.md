# DRAFT (UNSEALED) — GO-P-2026-077: consumer-relative access width on a real serving system (075-v2)

STATUS: DRAFT. ID 077 reserved; NO hash, NO seed. Successor to the
honestly-burned GO-P-2026-075 (design failure disclosed pre-seal: the
raw-cumulative "path" score was a broken consumer proxy and the
equal-uncertainty crossing did not exist — full record in the 075
draft + results/GO13-kvaw-pilot-disclosed.json). Redesign direction
(a) consumer-relative scoring, approved by the user 2026-08-05.

**The v2 claim family.** KV entries are records; the rolling context
is the aging reference; eviction is erasure. ALL scorers are now one
consumer-relative family — predicted future attention mass estimated
from a query window of width W (the access-width axis): w1024, w256,
w32, plus w32deg (see P2) and the shuffled null. The 075 pilot's
central measurement stands: on an aging reference, predictive
uncertainty u IMPROVES as the window narrows (0.982 → 0.892 from
full history to the 32-query snapshot) — unweighted wide access
includes staler evidence. The theory (GO-12/13 conditional-variance
reduction) says access class enters task-relevant quality only
through u:

- **P1-v2 (u-monotonicity of quality).** At matched budget, decode
  quality across {w1024, w256, w32} is ordered by measured u (lower
  u → better quality) at every rho — the nominal window width is
  irrelevant given u. This operationalizes the reduction on a
  production serving stack, and its direction is FIXED BY THE
  MEASURED u-ordering, not by the naive width intuition the 075
  pilot refuted (A2SF-consistent).
- **P2-v2 (equal-u analytic-equality control, constructible by
  design).** w32deg = the snapshot scorer degraded with fixed-seed
  Gaussian score noise, sigma calibrated OFFLINE so u(w32deg) =
  u(w256) — the crossing exists by construction (continuous knob),
  repairing 075's unconstructible control. Theory: equal u ⇒ equal
  quality at matched budget, despite structurally different scorers
  (32 fresh queries + noise vs 256-query history).
- **P3 (exploratory, ungated).** Age-band mistake profiles per
  scorer — the staleness-tax face; disclosed as exploratory.

**Inherited novelty record (075 draft, two sweeps + residual pass,
CLEAR TO SEAL there):** history-width axis adjacent-known (A2SF
adverse-direction, cited); equal-uncertainty CONTROL novel; Landauer
framing novel; 21-entry citation list carried over. OWED BEFORE
SEAL: one flank check on the u-matching-by-degradation device
(noise-calibrated scorer equivalence) — if published, cite; the
control's use as an analytic-equality gate is still ours.

**Instrument**: experiments/kv_access_width_v2.py (056/075 lineage;
Qwen2.5-7B-Instruct, LongBench passage_retrieval_en, prefill-reuse,
cache_position-correct decode, matched budget B_keep = max(rho·S,64),
always-keep last 32, bands [32,512)/[512,2k)/[2k,8k)/8k+, thermal
gate, sentinel ===KVAW2-JSON===). Arms × rho ∈ {0.10, 0.15} on
prompts excluding the 12 calibration and 16 v1-pilot indices. Pilot
seed 20260810 (16 fresh prompts); governed n=64, seed assigned at
seal. Atlas GPU 1 under house rules; the standing GPU authorization
covers the v2 sequence (user 2026-08-05: proceed per recommendation).

**Pre-seal checklist**: pilot report (sigma*, u-match residual +
bootstrap SE, drop table, band table) → P1/P2 bars with ≥1.3×
margins (P2 tolerance from bootstrap SEs; P1 ordering margins from
pilot gaps) → degradation-device flank check → seal → ONE governed
run.
