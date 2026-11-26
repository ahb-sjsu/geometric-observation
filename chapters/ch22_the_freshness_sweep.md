# Chapter 22 — The Freshness Sweep

> **STUB [A] — draftable now.** Source: the `observation-theory-campaigns`
> freshness tracks + `SEALS.md`. Parallel in form to Ch. 13 (the allocation sweep).
> House rule: the umbrella cites only `[replicated]`/`[demonstrated]` rows; breadth
> rows are carried at their honest class; the negative is kept at full prominence.

## What this chapter must establish

One witnessed-certificate grammar, measured across substrates — the freshness
counterpart of the 12-domain allocation sweep. Per domain: certificate → witness,
sealed bars, naive vs witnessed FC, verdict, tier.

| Domain | Cell(s) | Substrate | naive → witnessed | Class |
|---|---|---|---|---|
| Interdomain routing | BGP/IS-IS/OSPF/RPKI, BMP, D8 | RIS beacons + labs | 0.351/0.184/0.083 → detector band | **[replicated]** |
| Replication & coordination | PG/MG/PGX/GEO/ZK | real PG/Mongo/ZK, NRP | ~0.5 → ~0.02–0.06; ZK 0.99/0.01→0 | **[replicated]** |
| Cellular PHY/RAN | CSI/BEAM/AICSI/HO/URLLC/PHY | Sionna 5G NR | 0.28–0.47 → 0.05–0.13 | **[demonstrated]** |
| Optical | QOT | GNPy GN-model | ~0.40 → ~0 per footprint | `[predicted]` |
| Power grid | GRID | pandapower AC-PF | ~0.25 → ~0.01 | `[predicted]` |
| AI evaluation | LLM | roberta-mnli / HANS | *(shakedown)* | `[predicted]` |
| Quantum devices | QUANTUM | qiskit-aer (hand-built) | 0.28–0.43 → 0 | `[exploratory]` |
| Markets | QUOTE | efficient-price sim | 0.37 → 0.003 | `[exploratory]` |
| Sensing | (sensor) | real UCI field data | drift real; linear recalibration recovers only ~1.6× | **[refuted]** |

![Figure 22.1](figures/ch22_fig1.svg)

*Figure 22.1. The freshness sweep of the outline's table, drawn on one axis. For each domain the upper mark is the false-clear rate of the naive certificate and the lower mark is the rate once the certificate is witnessed. A bar is a range and a single dot is one value, both as the table prints them, approximate values included. The class of each row is at the right, and rows keep their own class: routing and replication are [replicated], cellular is [demonstrated], optical, grid and AI evaluation are [predicted], quantum and markets are [exploratory]. Sensing is [refuted]: the clean template failed and no false-clear pair is printed for it. The outline does not claim that the magnitudes coincide across domains.*

## Narrative beats
- The **replicated core** (routing + replication/coordination): the vacuity result
  reproduced across six independent data substrates and two witness kinds
  (LSN/oplog/zxid). The umbrella rests here.
- The **demonstrated wing** (cellular): the certificate ages under a *physical*
  coherence process, HARQ-witnessed, on standards-grade LDPC. One of its cells is
  scope-corrected and is kept as a negative: the AICSI reconstruction-vs-consumer
  dissociation did not survive the community-standard substrate (real 3GPP CDL-C, a
  CsiNet-class codec, which false-clears 0.0 on every seed; the pre-registered kill
  fired, 2026-08-25), so that row is not a headline.
- The **breadth** (optical/grid/LLM/quantum/markets): the grammar transfers to new
  substrates at `[predicted]`/`[exploratory]` — pre-registered, awaiting sealed
  grading or a real substrate (IBM hardware, tick data).
- The **kept negative** (sensor): drift is real but *linear recalibration* only
  partially recovers; the clean template failed honestly and is recorded, not
  tuned into a pass (the redesign — witness-triggered recalibration — is named,
  not claimed).

## Boundary
Cross-domain magnitude constants are not claimed to coincide; each row stands at its
own class. This is a *generality-of-grammar* result, not a universal-number result.
