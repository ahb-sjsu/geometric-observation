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
framing novel; 21-entry citation list carried over.

**Degradation-device flank check EXECUTED (2026-08-05, arXiv-API +
ar5iv full-text mode; report in session task output). Verdicts:**
noise-degradation-to-match as a control device ADJACENT-KNOWN — cite
arXiv:1802.05399 (Lykouris–Vassilvitskii: Gaussian-noise-degraded
oracle predictions in caching experiments, FULL-TEXT VERIFIED — the
mechanism precedent, used for curve-tracing from an oracle, NOT for
titrating one live scorer to a second live scorer's measured
uncertainty followed by an equality test); matched-uncertainty
eviction comparison NOVEL (null set on record); attention-mass
prediction with uncertainty calibration NOVEL (predictor existence
already covered by ForesightKV/KVpop citations). Citations to add at
seal: arXiv:1802.05399; arXiv:2607.11942 (matched-budget
query-visibility audit — the nearest access-structure comparison,
already surfaced in the 075 sweep, now upgraded to must-discuss);
lineage options arXiv:1706.06969, arXiv:2603.22219, arXiv:1610.02413
(re-verify ID at seal). DISCLOSED CHANNEL GAP: the session WebSearch
budget was exhausted pre-check and Semantic Scholar 429'd on all
attempts — coverage is arXiv-API title/abstract + targeted ar5iv
full text; residual risk low, same class as the 075 S2 gap.

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

**PILOT 1 EXECUTED (2026-08-05, seed 20260810, 16 fresh prompts,
21.0 min, peak 79C script / one 81C external transient; instrument
experiments/kv_access_width_v2.py; artifact
results/GO13-kvaw2-pilot-disclosed.json). THE REDESIGN WORKS; THE
QUALITY FACE IS CEILING-SATURATED — one more disclosed iteration
ordered, NO seal yet.** Findings: (1) equal-u control CONSTRUCTIBLE
as designed — sigma* = 2.4625e-4 bisected offline (14 CPU evals,
zero extra GPU decodes), u(w32deg) matches u(w256) to +1.6e-5,
bootstrap SE(sigma*) ~9% (39.8% of resamples non-bracketing on the
cached grid, recorded); disclosed deviation: v1 telemetry kept only
aggregated u, so sigma* is calibrated on this run's own phase-A
telemetry, not v1's. (2) v1 pathology GONE: no consumer-relative arm
near the shuffled null (shuf drops 0.69-0.81; all family arms within
0.125 of fp16 = 0.9375). (3) u-ordering clean at 4-7 SE:
w1024 0.942 > w256 0.910 > w32 0.893; quality never inverts it, but
rho in {0.10, 0.15} leaves w256/w32/w32deg AT the fp16 ceiling —
P1's decode effect unresolved (w1024 +0.125 +/- 0.080 only), P2
passes trivially (0.938 == 0.938 exactly). (4) The width axis is
SHARP in telemetry: w1024 recency-hoards (0.917 retention <512,
0.014-0.016 in 2048+ bands, oracle-miss 0.88 vs w32's 0.49); the
band-restricted decode localizes the entire gap to [512,2048)
(-0.1875 +/- 0.097). PILOT 2 (seed 20260811, disclosed pre-seal
iteration, in flight): n=32, rho {0.03, 0.05, 0.10}, band-restricted
[512,2048) gap promoted to P1's decode statistic, oracle-miss gap in
2048+ bands as P1's telemetry statistic, same task (no new
calibration surface), sigma* recalibrated and stability vs pilot 1
reported. Bars set only from pilot 2; if the ceiling persists at
rho=0.03 the P1 decode face is dropped and P1 seals telemetry-only —
recorded here before the data lands.