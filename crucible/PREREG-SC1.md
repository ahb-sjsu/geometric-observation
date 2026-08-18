# PREREG-SC1 — the space-comms downlink (a new cross-domain crucible)

**STATUS: UNSEALED.** Construction + shakedown only. This opens a new
domain line for Observation Theory — a bandwidth-starved deep-space
science downlink — the frontier `OWED-V1.md` named but did not mint
("a domain it has never touched … where a genuinely surprising failure
could live"). It is its own crucible, on the model of OT-6 (the
cross-domain gate that carried the theory to embedding retrieval) and
network-governor's BGP/RPKI line: a domain is entered by a sealed
campaign, not a free extension. Bars below bind only on a dated seal, a
day later than this construction (cooling-off), after the shakedown has
shown the family's interior across seeds. No evidential weight until
then.

## The domain and the claim

A spacecraft with a hard downlink budget serves several instruments,
each a *consumer* with its own read operator `P_i` (a tracker reads a
low-order centroid, a spectrometer a narrow band, an imager mid-band).
The bits are scarce (DSN is oversubscribed; deep-space links run
kbps–Mbps). The distortion instrument `i` actually feels is
`tr(P_i·Σ_q)` — the operator-weighted error, `consumer_distortion` in
readscope, not the reconstruction MSE. **P1+P2 predict that allocating
bits by the consumers' operators beats consumer-blind MSE allocation,
and — the v1-line standard — that the margin is derivable a priori.**

## The a-priori law — G = AM(d)/GM(d), derived before the sweep

Code the frame in the basis where the quantization noise `Σ_q` is
diagonal. With source spectrum `σ_k²`, per-coordinate bits `b_k`
(high-rate `Σ_q,k = σ_k² 2^{-2b_k}`), and aggregate instrument
importance `d_k = Σ_i w_i (P_i)_kk`, the consumer distortion is
`D(b) = Σ_k d_k σ_k² 2^{-2b_k}`. Reverse water-filling gives:

- **consumer-optimal** allocation → `D_cons = d · GM(d_k σ_k²) · 2^{-2B/d}`
  (weighted geometric mean),
- **MSE** allocation (`σ_k² 2^{-2b_k} =` const) applied to the consumer
  weights → `D_mse = AM(d_k) · GM(σ_k²) · 2^{-2B/d}` … · d.

The source variance cancels in the ratio, leaving a clean law:

    G = D_mse / D_cons = AM(d) / GM(d)          (high-rate limit)

`G ≥ 1` always (AM ≥ GM), `= 1` iff the instruments read uniformly
(`d_k` flat), and `≈ 1 + ½·CV²(d)` for a small importance spread. **The
gain of consumer relativity on a downlink is exactly the AM/GM gap of
the instrument-importance spectrum** — readscope's core claim, in a new
domain, with the margin derived rather than observed. The composition
law (P1, OT-8) extends it: the ensemble `d = Σ_i w_i d^{(i)}` predicts
the joint gain from the component profiles, cross-terms costing the
predicted cell.

## Shakedown outcome (2026-08-18) — the interior is there, across seeds

`fam_sc1_shakedown.py` (source `α = 1.5`, `d = 64`, 3 instrument
archetypes on random subspaces, 40 scenarios/seed, seeds {0,1,2}, bit
budget swept 1→4 b/coord; `results/SC1-shakedown.json`):

| rate (b/coord) | Spearman(G_meas, AM/GM) | median G_meas / (AM/GM) | G_pred spread |
|---|---|---|---|
| 1 | +0.784 (min +0.75) | 0.898 | 1.16–1.55 |
| 2 | +0.989 | 0.985 | 1.17–1.50 |
| 3 | +0.999 | 1.000 | 1.17–1.50 |
| 4 | +1.000 | 1.000 | 1.18–1.57 |

Two things, both wanted: the AM/GM law is **exact at high rate**
(`meas/pred → 1.000`, Spearman → 1.000) and **departs predictably at
low rate** (0.898 at 1 b/coord, as coordinates drop below the water and
the geometric-mean form breaks) — the same continuous-vs-finite-codebook
departure C-16 measures, now in the downlink. `G_pred` spans 1.16–1.57:
consumer relativity genuinely bites (16–57% gain), neither trivial nor
saturated, stable across seeds. The family has interior.

## Bars (TO BE SEALED on a fresh day; not yet binding)

- **B1 — the AM/GM law.** At high rate (≥ 3 b/coord),
  `median(G_meas / (AM(d)/GM(d)))` within `1.00 ± 0.03`, and
  `Spearman(G_meas, AM/GM) ≥ 0.95`, on each of ≥3 disjoint seeds.
- **B2 — the finite-rate departure is a floor, not noise.** The ratio
  `G_meas/(AM/GM)` is monotone increasing in rate (`≤ 1`, approaching 1)
  — the departure is the codebook floor, not scatter.
- **B3 — composition (P1/OT-8, MC-grade).** The ensemble gain is
  predicted from the component importance profiles `d^{(i)}` to within
  the pre-named cross-term cell.

**Kills.** `G_meas ≈ 1` across the family despite a spread in `d`
(consumer relativity does not bite on a downlink — the strongest
refutation); or `G_meas` not tracking `AM(d)/GM(d)` (Spearman < 0.6 at
high rate, i.e. the margin is not the derived one). Either returns the
downlink claim to revision without touching the frozen principles.

## Discipline and scope

A cross-domain *pass* here does not touch v1.0's frozen statements; it
extends the evidence to a new domain, exactly as OT-6 and the RPKI line
did. A cross-domain *failure* is a scoped refutation of the transfer,
not of the within-ML principles. This substrate is **synthetic** (a
planted source spectrum and archetype instruments), so a pass earns the
*mechanism*, not a systems claim; a real-telemetry substrate (DSN
frames, actual instrument operators) would be its own later campaign.
Scope honestly: this is the deep-space, heterogeneous-instrument case —
a broadband LEO link carrying homogeneous IP traffic has one effectively
uniform consumer, where the AM/GM gap collapses to ≈ 1 and the theory
predicts *no* gain (itself a falsifiable boundary of the claim).

## Heterogeneous-access arm (2026-08-18) — the boundary, measured

The AM/GM law is domain-agnostic in `d`, so it should govern a congested
terrestrial access link / RAN shared by traffic classes (latency-,
throughput-, loss-sensitive) exactly as it governs instruments — and,
crucially, predict *no* gain where consumers homogenize. `fam_sc1_access.py`
(d=64, 4 QoS classes, rate 3 b/unit, heterogeneity knob `h` swept 0→1,
seeds {0,1,2}; `results/SC1-access-shakedown.json`):

| h (heterogeneity) | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---|---|---|---|---|
| mean `AM/GM` | 1.000 | 1.079 | 1.139 | 1.203 | 1.267 |
| median `G_meas/(AM/GM)` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

At `h=0` (identical classes) the gain is exactly 1 — consumer-relative
scheduling buys nothing, the **fiber-core / broadband boundary**. The gap
opens smoothly with heterogeneity and the measured gain tracks `AM/GM`
exactly at this rate. This is the falsifiable boundary of the whole
allocation claim, made concrete: the law applies to the scarce,
heterogeneous edge (RAN slices, QoS), and predicts zero gain for the
homogeneous core — the same statement that sorts deep-space (strong) from
Starlink broadband and fiber WAN (≈ 1).

## Provenance

- Frontier note: `crucible/OWED-V1.md` (the un-minted domain).
- Access arm: `crucible/fam_sc1_access.py`,
  `results/SC1-access-shakedown.json` (no weight).
- Substrate: `crucible/fam_sc1_shakedown.py`;
  record `results/SC1-shakedown.json` (no weight). Graded runner
  `sc1_check.py` added at seal, on disjoint seeds.
- Reused core: readscope `water_fill` (allocate.py),
  `consumer_distortion` = `tr(P·Σ)` (metrics.py) — the same instrument
  as the attention-head campaigns.
