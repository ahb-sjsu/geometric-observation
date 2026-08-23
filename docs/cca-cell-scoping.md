# CCA cell — scoping: measuring the interferer-overlap loss rate of 802.11 CCA with a receiver-co-located witness

Companion to `draft-bond-ot80211-freshness-01` (revised per the
2026-08 technical review; terminology and requirements follow the -01
draft). The draft defines *how* to measure the receiver-relative
interferer-overlap loss rate (IOLR) of transmissions attempted after
an idle CCA indication, but reports no number — its example values
are flagged illustrative. This document scopes the experiment that
would produce the **first measured one**: a sealed cell in a
controlled, conducted hidden-node regime with a receiver-co-located
IQ witness. It is a hardware design, not a built cell; deliverable is
the topology, instrumentation, draft bars, and the honest hard parts.

**Revision note (2026-08-22):** the original scoping proposed
`gr-ieee802-11` for the device under test; the review established
that it cannot serve (upstream documents no CSMA/CA and non-working
RTS/CTS — so neither logged CCA decisions in a real DCF nor the
RTS/CTS arm are available). The platform section now names OpenWiFi
as the candidate substrate, pending demonstration. The comparison
design moves from paired runs to randomized interleaving with a
directly computed difference interval, and the interferer must be a
MAC participant for the comparative arm.

## The measurement (from the RFC, -01 terms)

- **Assertion under test:** CCA — the transmitter's "medium idle →
  transmit," performed at the transmitter.
- **Consumer:** the receiver (Rx). The collision CCA is meant to
  prevent happens at Rx, not at the transmitter.
- **IOLR (primary observable):** of transmissions attempted after an
  idle CCA indication, the fraction lost at Rx WITH witnessed
  interferer overlap. The cell's controlled design (known interferer
  schedule + link-sanity check + validated overlap classifier) meets
  the -01 attribution bar, so its IOLR may be described as a
  false-idle rate; overlap alone is never called causation.
- **Witness (compound):** Rx's own per-frame decode log
  (consumer outcome) + an SDR capturing IQ **at the Rx port**
  (overlap), independent of the transmitter's CCA. The overlap
  classifier's detection/false-detection rates are measured with
  injected calibration bursts (a -01 requirement).

The cell also measures the RFC's **comparative claim**: basic-access
IOLR vs RTS/CTS-access IOLR under randomized interleaved assignment,
both graded against the same witness. Note the -01 correction: the
CTS is part of the access *treatment* (it silences C via the NAV iff
C decodes and honors it); the witness is the decode-log + IQ
compound, never the CTS itself.

## Topology: the hidden-node triangle, conducted

Three 802.11 nodes plus the witness:

- **A** — transmitter (station), sends known frames to Rx on a schedule.
- **C** — the "hidden" interferer, transmits on its own schedule.
- **Rx** — receiver/AP, logs per-frame decode success/failure.
- **W** — Pluto witness, RX-only, taps the RF at the Rx port.

The defining relationship: **A cannot sense C** (so A's CCA reads clear
while C transmits) but **C reaches Rx** (so C collides at Rx). Realize
this **conducted** (cabled), not over the air:

```
 A ──[att_A]──┐
              ├── combiner ── splitter ──> Rx
 C ──[att_C]──┘                     └────> W (Pluto witness)
```

- `att_A` on the A→(C-visible) path is set high enough that **A's CCA
  cannot detect C** (the A↔C coupling is below A's CCA threshold), while
  A→Rx passes. `att_C` sets C→Rx to a colliding level.
- Conducted is the rigorous choice: it removes over-the-air regulatory
  exposure, makes the hidden relationship a *set* quantity (the attenuator
  network, not geometry), and is fully reproducible seed-to-seed. Over-the-
  air is Phase B (external validity), not the sealed cell.

## Instrumentation

The crux is **observing A's CCA decision inside a real DCF**, which
commodity Wi-Fi firmware hides. The original candidate,
`gr-ieee802-11`, is **ruled out**: upstream documents that it has no
CSMA/CA mechanism and that RTS/CTS does not work within its timing
constraints — so it can provide neither logged per-opportunity CCA
decisions of a real DCF nor the RTS/CTS arm. Current candidate:
**OpenWiFi** (FPGA-based SDR 802.11), which exposes DCF/CSMA-CA in
fabric, CCA threshold configuration, NAV handling, ACK generation,
and IQ access. Candidate, not validated: its RTS/CTS behavior and
per-opportunity CCA logging must be demonstrated in an unsealed
feasibility shakedown before any prereg bars are fixed.

| node | radio | logs |
|---|---|---|
| A (Tx) | OpenWiFi SDR (candidate) | per-opportunity: TX timestamp, **CCA indication** (idle/busy) at access time, access method (basic / RTS-CTS), retry number |
| C (interferer) | OpenWiFi SDR (candidate) — **MAC participant: decodes CTS, honors NAV** (required for the comparative arm; a scheduled burst generator is valid only for the single-arm IOLR) | its TX schedule (timestamps), NAV deferrals |
| Rx | OpenWiFi SDR (candidate) | per-MPDU decode success/fail, ACK/Block Ack issued, PHY metrics |
| W (witness) | RX-only SDR (ADALM-Pluto adequate at 2.4 GHz / 20 MHz) | raw IQ at the Rx port, timestamped → offline overlap classifier (versioned; calibrated with injected bursts) |

Pluto is 2.4 GHz-native, 20 MHz BW — enough for 802.11g/n 20 MHz OFDM at
low-mid MCS (6–24 Mbps), which is the target regime. (5 GHz needs the
AD9363 frequency hack and is marginal; stay at 2.4 GHz for the sealed
cell.) A and Rx can be Plutos too, or a USRP.

**Time alignment** is the second crux: correlating A's TX time, C's TX
time, Rx's decode, and W's capture needs a common clock. Options, in
order of rigor: (a) a shared 10 MHz + PPS reference distributed to all
SDRs (locks sample clocks; USRPs support natively, Plutos via the
external-ref input/mod); (b) cross-correlation — A emits a known marker
that appears in W's capture and is timestamped by A, aligning by
correlation. The sealed cell SHOULD use (a); alignment residual is a
manipulation check (MC4).

## Grading and statistics (per draft -01)

Atomic unit: one PPDU transmission attempt after an idle CCA
indication; each retry is a distinct opportunity. Per opportunity,
classify the consumer outcome (complete-success / partial-success /
decode-failure / **indeterminate** — counted, never discarded) and
the witness's overlap verdict:

- **overlap-loss** iff Rx failed AND W's classifier shows C's
  waveform overlapping A's PPDU at Rx;
- losses with **no** witnessed overlap are `other-loss` (link/SNR),
  never counted in the IOLR numerator — this is why the witness must
  be independent and Rx-co-located;
- IOLR = overlap-losses / (idle-CCA attempted), per arm.

**Comparison design:** randomized interleaved assignment of access
method (basic vs RTS/CTS) per block, block length preregistered —
NOT paired sequential runs (channel conditions are time-correlated).
Identical traffic and interferer generation rules across arms. The
comparative estimand is the IOLR **difference** with its own CI,
computed by block bootstrap clustered on **interference bursts**;
per-opportunity Wilson intervals are not valid under bursty
interference. Report cluster and opportunity counts per arm, and the
indeterminate-handling sensitivity bounds (indeterminates as losses
/ as successes). **False-alarm is out of this cell's scope** — it is
counterfactual (requires CCA-override intervention) and is the -01
draft's separate OPTIONAL procedure; the -00 requirement to report
both rates (which this cell could not meet) was removed in -01.

## Draft bars (registration-first; validated by shakedown before seal)

- **B1 — CCA vacuity:** basic-access IOLR ≥ **0.15** (bare CCA is
  meaningfully vacuous in the hidden-node regime).
- **B2 — treatment helps:** RTS/CTS-access IOLR ≤ **0.05**.
- **B3 — dominance:** IOLR difference (basic − RTS/CTS) positive with
  its whole block-bootstrap CI above **0.05**, and basic ≥ **3×**
  RTS/CTS point estimate.

**Manipulation checks (bars too):**
- **MC1 — hidden realized:** during C's transmissions, A's CCA reports
  clear ≥ 0.8 of the time (A genuinely cannot sense C).
- **MC2 — interferer reaches the consumer:** W detects C energy at Rx in
  ≥ 0.8 of C's transmissions.
- **MC3 — non-degenerate + link sane:** ≥ N CCA-clear A-frames, ≥ M with
  concurrent C energy (real collision opportunities), AND Rx decodes A ≥
  0.9 when C is silent (failures are attributable to collision, not a
  broken link).
- **MC4 — witness alignment:** cross-correlation timing residual ≤ one
  OFDM symbol (≈ 4 µs).
- **MC5 — classifier calibrated:** overlap-classifier detection ≥ 0.95
  and false-detection ≤ 0.02 on injected calibration bursts.
- **MC6 — randomization balanced:** interferer exposure per arm within
  preregistered tolerance (the interleaving really produced comparable
  conditions).

**Kills:** basic-access IOLR < 0.05 (the bench did not achieve a
hidden-node regime — refuted for this substrate, reported); or the
IOLR difference CI containing zero (RTS/CTS does not help here —
reported).

## The honest hard parts

1. **Regulatory → conducted.** Deliberate interference over the air is
   fraught; the sealed cell is cabled (attenuators/combiners), no OTA
   emission. External validity (real hidden node OTA, low power,
   compliant) is Phase B.
2. **CCA observability → SDR MAC.** Commodity NICs hide the CCA
   decision; an open SDR MAC exposes it. `gr-ieee802-11` is ruled out
   (no CSMA/CA; RTS/CTS non-functional upstream); OpenWiFi is the
   candidate and needs a feasibility shakedown demonstrating RTS/CTS
   and per-opportunity CCA logging BEFORE any bars are fixed.
3. **Time sync → shared reference.** The whole grading rests on aligning
   four streams. Shared 10 MHz/PPS is the clean answer; MC4 guards it.
4. **Pluto bandwidth/quality.** AD9363 at 20 MHz OFDM is workable at
   low-mid MCS on 2.4 GHz; do not push 5 GHz or high MCS in the sealed
   cell.
5. **Cost/complexity.** The OpenWiFi requirement raises the platform
   cost over the original Pluto-only sketch: A, C, and Rx each need an
   OpenWiFi-capable Zynq+AD936x board (e.g., AntSDR/ADRV-class,
   roughly $300–700 ea — verify current hardware support list); W
   stays a Pluto (~$230). Plus SMA cables + attenuators +
   combiner/splitter (~$150) and clock distribution (~$150).
   Meaningfully harder than the docker DB cells — this is a real
   RF-lab build, and the platform feasibility shakedown comes first.

## Phasing

- **Phase A0 — platform feasibility (unsealed).** Demonstrate OpenWiFi
  RTS/CTS operation and per-opportunity CCA logging against the -01
  requirements. No bars are fixed before this passes.
- **Phase A — conducted bench (the sealed cell).** Everything above,
  fully controlled and reproducible → prereg → shakedown → fresh-day seal.
  Produces the first measured 802.11 CCA IOLR.
- **Phase B — over-the-air (external validity).** A real hidden-node
  geometry at compliant low power, same instrumentation → a second,
  transfer-validating cell.

## Relationship to the RFC

A Phase-A PASS replaces the draft's illustrative example with a
measured, sealed CCA IOLR and a measured RTS/CTS difference (with its
own interval) — turning the Experimental draft from "here is how to
measure" into "here is how to measure, and here is the first
measurement," and populating the -01 Implementation Status section.
That is the same shakedown→seal arc the database cells followed, on
an SDR witness instead of a WAL/oplog one.
