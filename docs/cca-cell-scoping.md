# CCA cell — scoping: measuring the false-clear rate of 802.11 Clear Channel Assessment with a Pluto SDR witness

Companion to `draft-bond-ot80211-freshness-00`. That draft defines *how*
to measure the false-clear rate of an 802.11 channel-access certificate
but reports no number — its example values are flagged illustrative. This
document scopes the experiment that would produce the **first measured
one**: a sealed cell measuring the false-clear rate of Clear Channel
Assessment (CCA) in a controlled hidden-node regime, with an ADALM-Pluto
SDR as the receiver-co-located witness. It is a hardware design, not a
built cell; deliverable is the topology, instrumentation, draft bars, and
the honest hard parts.

## The measurement (from the RFC)

- **Certificate:** CCA — the transmitter's assertion "medium idle →
  transmit," performed at the transmitter.
- **Consumer:** the receiver (Rx). The collision the certificate is meant
  to prevent happens at Rx, not at the transmitter.
- **False-clear:** the transmitter's CCA reports clear, it transmits, and
  Rx fails to receive *because* a station the transmitter could not sense
  transmitted concurrently and collided at Rx — the hidden-node case.
- **Witness:** a Pluto SDR capturing the RF **at the Rx port**,
  independently of the transmitter's CCA and of Rx's own decode, so we can
  establish the *cause* of a loss (concurrent interferer energy present at
  Rx = collision, versus mere weak signal).

The cell also measures the RFC's **comparative claim**: CCA-alone
false-clear vs RTS/CTS-enabled false-clear, both graded against the same
Pluto witness — RTS/CTS being the already-witnessed-but-uncalibrated
certificate (the CTS from Rx silences the interferer *if* it can hear Rx).

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

The crux is **observing A's CCA decision**, which commodity Wi-Fi
firmware hides. Solution: run A (and Rx) as **SDR 802.11** via GNU Radio +
`gr-ieee802-11` (Bloessl's 802.11a/g OFDM transceiver), where carrier
sense / CCA lives in the flowgraph and is loggable.

| node | radio | logs |
|---|---|---|
| A (Tx) | SDR + `gr-ieee802-11` | per-frame: TX timestamp, **CCA decision** (clear/busy) at TX time, RTS/CTS mode |
| C (interferer) | SDR (OFDM burst / 802.11) | its TX schedule (timestamps) |
| Rx | SDR + `gr-ieee802-11` | per-frame decode success/fail, Ack outcome, PHY metrics |
| W (witness) | **ADALM-Pluto**, RX-only | raw IQ at the Rx port, timestamped → offline: concurrent-energy detection per A-frame |

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

## Grading

Per A transmission opportunity where **A's CCA reported clear** (A
transmitted):

- **false-clear** iff Rx decode failed AND W shows concurrent C energy at
  Rx overlapping A's frame (collision-attributable loss);
- losses where W shows **no** concurrent energy are *not* counted as CCA
  false-clears (they are link/SNR losses) — this is exactly why the
  witness must be independent and Rx-co-located.

False-clear rate = false-clears / CCA-clear transmissions. Run twice per
seed: **CCA-alone** and **RTS/CTS-enabled**, both graded against W.

## Draft bars (registration-first; validated by shakedown before seal)

- **B1 — CCA vacuity:** CCA-alone false-clear rate ≥ **0.15** (bare CCA is
  meaningfully vacuous in the hidden-node regime).
- **B2 — witness helps:** RTS/CTS false-clear rate ≤ **0.05**.
- **B3 — dominance:** CCA-alone ≥ **3×** RTS/CTS false-clear.

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

**Kills:** CCA-alone false-clear < 0.05 (the bench did not achieve a
hidden-node regime — refuted for this substrate, reported); or witnessed
false-clear not below CCA-alone (RTS/CTS does not help here — reported).

## The honest hard parts

1. **Regulatory → conducted.** Deliberate interference over the air is
   fraught; the sealed cell is cabled (attenuators/combiners), no OTA
   emission. External validity (real hidden node OTA, low power,
   compliant) is Phase B.
2. **CCA observability → SDR MAC.** Commodity NICs hide the CCA decision;
   `gr-ieee802-11` exposes it. This is the reason A/Rx are SDRs, not cards.
3. **Time sync → shared reference.** The whole grading rests on aligning
   four streams. Shared 10 MHz/PPS is the clean answer; MC4 guards it.
4. **Pluto bandwidth/quality.** AD9363 at 20 MHz OFDM is workable at
   low-mid MCS on 2.4 GHz; do not push 5 GHz or high MCS in the sealed
   cell.
5. **Cost/complexity.** ~3–4 SDRs (Pluto ~$230 ea; or 2 Plutos + a USRP
   B210 ~$1.2k), SMA cables + attenuators + combiner/splitter (~$150),
   clock distribution (~$150, or a USRP's ref-out), GNU Radio +
   `gr-ieee802-11` (free). Meaningfully harder than the docker DB cells —
   this is a real RF-lab build.

## Phasing

- **Phase A — conducted bench (the sealed cell).** Everything above,
  fully controlled and reproducible → prereg → shakedown → fresh-day seal.
  Produces the first measured 802.11 CCA false-clear rate.
- **Phase B — over-the-air (external validity).** A real hidden-node
  geometry at compliant low power, same instrumentation → a second,
  transfer-validating cell.

## Relationship to the RFC

A Phase-A PASS replaces `draft-bond-ot80211-freshness-00`'s illustrative
example with a measured, sealed CCA false-clear rate and a measured
RTS/CTS reduction — turning the Experimental draft from "here is how to
measure" into "here is how to measure, and here is the first
measurement." That is the same shakedown→seal arc the database cells
followed, on an SDR witness instead of a WAL/oplog one.
