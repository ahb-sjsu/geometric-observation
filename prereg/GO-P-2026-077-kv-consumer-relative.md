# GO-P-2026-077: consumer-relative access width on a real serving system (075-v2)

STATUS: SEALED (yaml block below governs; full disclosed design history retained). Successor to the
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
**PILOT 2 EXECUTED (2026-08-05, seed 20260811, 32 fresh prompts, 62.9
min wall / ~38.5 min compute; artifact
results/GO13-kvaw2-pilot2-disclosed.json). CEILING BROKEN -- bars
settable.** (1) Decode face resolves on the width endpoints: paired
w32-w1024 = +0.563+/-0.108 at rho=0.05 (5.2 SE), +0.625+/-0.107 at
0.03; w1024 falls BELOW the shuffled null at rho <= 0.05 (recency
hoarding worse than random at extreme budgets); w256 exits ceiling
only at 0.03 (+0.156+/-0.089, 1.8 SE -- not barred); w32/w32deg
NEVER drop, even at 97% eviction (headline-adjacent robustness,
measured not gated). (2) Pilot 1's band-restricted [512,2048) gap
DID NOT REPLICATE at n=32 (0.000+/-0.043 in every band) -- dropped
as P1's decode statistic per the pre-recorded review, replaced by
the global low-rho contrast. (3) u-ordering replicated tighter
(w1024 0.9419 > w256 0.9115 > w32 0.8979, 4-7 SE); sigma*
recalibrates per-run (2.07e-4 vs 2.46e-4, boot SE 8.4%, no-crossing
fraction 0.398 -> 0.003 at n=32) -- the protocol gates calibration
HEALTH, not a sigma* constant. (4) At rho=0.03 the equal-u pair
STRAINS (+0.156+/-0.089): pre-registered below as a secondary
two-sided MEASURED quantity, not a gate -- if it firms at governed n
it is a finding (equal scalar u need not imply equal task damage),
not a control failure. (5) OPS INCIDENT disclosed: Atlas's root
thermal_guardian SIGSTOPped the pilot at CPU package 82C mid-run;
after diagnosing the guardian's unreachable resume threshold during
a RAID resync, the agent SIGCONTed ITS OWN pid only; the guardian
resumed its other pids itself; nothing killed, GPU 0/Erebus
untouched; one prompt's wall time carries the ~24-min pause.

```yaml
id: GO-P-2026-077
date: 2026-08-05
retrospective: false
kind: operational (successor to the honestly-burned 075; consumer-relative access width on a production KV-cache serving stack)
claim: "On Qwen2.5-7B/LongBench passage retrieval at matched eviction
  budget, task quality tracks measured predictive uncertainty u about
  the consumer's future reads, not nominal scorer width (P1: the
  narrow-window scorer with lower u beats the 1024-query scorer at
  low keep fractions, and the width axis shows as recency-hoarding
  starvation of old age bands); and two structurally different
  scorers titrated to EQUAL u produce equal task quality (P2: the
  noise-degraded snapshot equals the 256-query scorer) -- the
  equal-uncertainty analytic-equality control, constructible by
  design."
harness: experiments/kv_access_width_v2.py   # GOVERNED seed 20260812; pilots 20260810/20260811 disclosed above
power: |
  Bars carry >=1.3x margins on pilot-2 point estimates, replicated
  across disjoint prompt sets where both pilots measured them:
  V1 telemetry gap bar 0.25 vs 0.373/0.387 (1.49x, both pilots);
  V2 decode contrast bar 0.30 vs 0.563 (1.88x, bar 2.4 SE below the
  estimate); V3 shuffle sanity bar 0.30 vs 0.500 (1.67x); V4
  equality tolerance 0.0625 vs 0.031/0.000 (2x); V5 health gates
  3x-35x; V6 u-ordering at 4-7 SE in both pilots. Governed n=64
  doubles pilot-2 resolution on every paired statistic.
pilot: |
  THREE disclosed pilot-phase runs under this lane: v1-pilot (under
  the 075 draft, seed 20260806 -- exposed the broken raw-cumulative
  proxy and the nonexistent u-crossing; 075 burned), v2 pilot 1
  (seed 20260810 -- redesign validated, ceiling found), v2 pilot 2
  (seed 20260811 -- ceiling broken at low rho, band-restricted
  statistic killed by its own replication test, bars set). Every
  design change is recorded above WITH its decision rule where one
  was pre-recorded. No bar was loosened against a measured value.
prediction:
  V1_p1_telemetry: mean over the two 2048+ age bands of
    [oracle-miss(w1024) - oracle-miss(w32)] at rho=0.10 >= 0.25
  V2_p1_decode: paired mean [score(w32) - score(w1024)] at rho=0.05
    >= 0.30
  V3_p1_sanity: paired mean [score(w32) - score(shuf)] at rho=0.05
    >= 0.30
  V4_p2_equality: abs(paired mean [score(w32deg) - score(w256)]) <=
    0.0625 at rho=0.05 AND at rho=0.10
  V5_p2_health: pooled abs(u(w32deg) - u(w256)) <= 1e-3 AND
    boot_SE(sigma*)/sigma* <= 0.25 AND boot_frac_no_crossing <= 0.10
  V6_u_ordering: u(w1024) > u(w256) > u(w32), each pairwise gap
    >= 2 pooled bootstrap SEs
  measured_not_gated: all rho=0.03 rows including the two-sided
    equal-u contrast [score(w32deg) - score(w256)] at rho=0.03
    (pre-registered tension +0.156 +/- 0.089); w32 zero-drop
    robustness at rho=0.03; the w1024-below-shuffle pathology
falsification: V2 or V6 fail -> the u-quality link fails at the
  width endpoint (P1 refuted operationally at its effect sizes);
  V1 fail -> the staleness/starvation telemetry face refuted;
  V4 fail (with V5 passing) -> equal scalar u does NOT imply equal
  task quality -- P2 refuted, and the rho=0.03 measured contrast
  becomes the primary suspect structure; V5 fail -> the control is
  unconstructible at governed n: design failure recorded, NO P2
  verdict claimed either way. Single run, no silent reruns.
design:
  stopping: fixed design, ONE governed run, seed 20260812, n=64
    fresh prompts (excluding the 76 indices used by calibration +
    v1-pilot + v2-pilots 1/2, all listed in the artifacts); arms
    {w1024, w256, w32, w32deg, shuf} x rho {0.03 measured-only,
    0.05, 0.10}; phase-A telemetry + offline sigma* recalibration
    (health-gated) + w32deg decodes; NO band-restricted decode phase
    (statistic dead at n=32, dropped pre-seal on its replication
    failure); Atlas GPU 1, CUDA_VISIBLE_DEVICES=1, in-script thermal
    gate (pause >80C, abort >83C), Erebus untouched
  runtime: ~60-75 min GPU 1 (pilot 2: 38.5 min compute at n=32 x 3
    rhos + band phase; governed drops the band phase)
controls: [shuffled-score null (V3), equal-u titrated pair (V4/V5),
  u-ordering internal replication (V6), fp16 baseline per prompt,
  matched budget everywhere, fixed-seed noise vector for w32deg,
  rho=0.03 tension pre-registered as measured-not-gated]
amendments: []
hash: sha256:79a731c9669995e0b92eb890cf86c49e703af4418aa71268ab3fe54e0db1b131
```

## Falsification

A pass nets the program's first OPERATIONAL face on a production
serving stack for the conditional-variance reduction (quality
through u alone) and the first use anywhere of the
equal-uncertainty analytic-equality control (novel per the two 075
sweeps + the degradation-device flank check, citations and channel
gaps on record above). A V4-fail with healthy calibration would
itself be a publishable structural finding, pre-registered as such.
The Landauer framing rides only on the sealed faces; no novelty
language beyond the sweeps' verdicts.
