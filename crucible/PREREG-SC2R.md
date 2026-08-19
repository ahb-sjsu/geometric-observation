# PREREG-SC2R — SC-2 on real Starlink traces (fielded evidence)

**STATUS: UNSEALED — and DATA-GATED.** Construction + synthetic
shakedown only. This moves SC-2 from synthetic mechanism toward fielded
evidence, testing the read-operator account on **real** Starlink RTT/loss
traces. It cannot be graded until a real trace is loaded; sealing also
requires the usual fresh-day cooling-off. No evidential weight until
both.

## The claim (fielded analogue of SC-2)

On a real Starlink trace, without being told the schedule: (i) the
handover cadence (~15 s) is **detectable from the data**; (ii) apparent
congestion — loss bursts / RTT step-spikes — **clusters at handover
boundaries** well above chance; and (iii) a schedule-aware reader that
masks the detected handover windows **removes false-congestion** by an
amount consistent with the handover duty cycle. This is SC-2's
`κ = 1−2c` masking gain, measured on hardware traffic instead of a
planted Markov channel.

## Substrate — public datasets (the run gate)

The graded run consumes a real trace with per-sample RTT and/or a loss
indicator. Candidate public datasets (searched 2026-08-19):
- **WetLinks** — six months (Oct'23–Mar'24) of orchestrated Starlink
  measurements, two European sites, with RTT, throughput, **packet
  loss**, traceroutes, co-located weather.
- **clarkzjw / mmsys24** — fine-grained Starlink RTT since Nov 2023
  (low-latency video-streaming measurement set); RTT step-changes at the
  ~15 s handover are visible.
- **LENS** — geographically distributed dish RTT with PoP metadata.

`sc2r_pipeline.py trace.csv` runs the pipeline on a CSV with a `loss`
column or an `rtt_ms` column (loss thresholded from RTT spikes).
Acquiring and formatting one of these datasets is the gating step.

## The pipeline (`sc2r_pipeline.py`)

1. **Cadence detection** — autocorrelation of the loss/step signal; the
   peak lag in an 8–25 s band is the handover period. Blind to the true
   schedule.
2. **Handover mask** — best-phase alignment of a periodic mask at the
   detected period.
3. **Masking test** — naive reader signals on all loss; schedule-aware
   reader ignores loss inside handover windows; compare false-congestion.

## Bars (TO BE SEALED on a fresh day, with a real trace; not binding)

- **B1 — cadence detectable.** Detected period ∈ [12, 18] s with an
  autocorrelation peak ≥ 0.3 (significant), on ≥3 disjoint trace
  segments.
- **B2 — congestion clusters at handovers.** ≥ 50 % of loss / RTT-spike
  events fall in detected handover windows (handovers explain much of
  the apparent congestion), above a phase-shuffled chance baseline.
- **B3 — masking removes false-congestion.** Schedule-masking reduces
  the false-congestion signal rate by ≥ 40 % relative to naive, on each
  segment.

**Kills.** No detectable cadence (period undetermined or acf < 0.3); or
loss not concentrated at handovers (≤ chance) — the handover-as-false-%
congestion mechanism does not appear in real traffic; or masking gives
no reduction. Any scopes the transfer to fielded systems; the synthetic
SC-2 result and the frozen principles are untouched.

## Shakedown outcome (2026-08-19) — synthetic trace-shaped signal

`sc2r_pipeline.py` (no argument) on a synthetic Starlink-shaped trace
(15 s-periodic RTT step-changes + Markov congestion + measurement noise),
seeds {0,1,2} (`results/SC2R-shakedown.json`): the detector recovered the
cadence **exactly (15.0 s, acf 0.89–0.99)**, 90–99 % of non-congestion
loss sat at handover boundaries, and masking cut false-congestion to
zero. The near-total reduction is **idealized** — in the synthetic trace
non-congestion loss is entirely handover-aligned by construction; a real
trace will be messier, which is why B2/B3 use loose, honest thresholds
(≥50 %, ≥40 %), not the synthetic's ~100 %. The shakedown demonstrates
the pipeline, not the result.

## Provenance

- Parent: `crucible/PREREG-SC2.md` (synthetic SC-2, sealed + PASSed
  2026-08-19), `paper/space-comms.tex`.
- Pipeline: `crucible/sc2r_pipeline.py`; shakedown record
  `results/SC2R-shakedown.json` (no weight).
- Datasets (searched): WetLinks (TMA 2024), clarkzjw/mmsys24, LENS.
