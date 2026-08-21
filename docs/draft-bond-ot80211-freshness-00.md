---
title: "Observation-Governed Channel Access: Consumer-Relative, Witnessed Freshness Certificates for IEEE 802.11"
abbrev: "OT-Governed 802.11 Freshness"
docname: draft-bond-ot80211-freshness-00
category: exp
ipr: trust200902
area: "Operations and Management"
workgroup: "Individual Submission"
keyword:
 - 802.11
 - Wi-Fi
 - clear channel assessment
 - hidden node
 - measurement
 - freshness
 - false-clear rate
 - observation theory
stand_alone: yes
pi: [toc, sortrefs, symrefs, comments]
author:
 -
    ins: A. H. Bond
    name: Andrew H. Bond
    organization: San José State University
    email: andrew.bond@sjsu.edu

normative:
  RFC2119:
  RFC8174:

informative:
  IEEE802.11:
    target: https://standards.ieee.org/standard/802_11-2020.html
    title: "IEEE Standard for Information Technology--Telecommunications and Information Exchange between Systems--Local and Metropolitan Area Networks--Specific Requirements--Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications"
    author:
      - org: IEEE
    date: 2020
    seriesinfo:
      IEEE: "Std 802.11-2020"
  MACA:
    title: "MACA - A New Channel Access Method for Packet Radio"
    author:
      - ins: P. Karn
    date: 1990
  MACAW:
    title: "MACAW: A Media Access Protocol for Wireless LAN's"
    author:
      - ins: V. Bharghavan
      - ins: A. Demers
      - ins: S. Shenker
      - ins: L. Zhang
    date: 1994
    seriesinfo:
      ACM: SIGCOMM 1994
  BIANCHI:
    title: "Performance Analysis of the IEEE 802.11 Distributed Coordination Function"
    author:
      - ins: G. Bianchi
    date: 2000
    seriesinfo:
      IEEE: "JSAC 18(3)"
  OT:
    title: "Observation Theory: Consumer-Relative, Witnessed, Calibrated Reliability Claims for Observed Systems (preprint)"
    author:
      - ins: A. H. Bond
    date: 2026
  VACUITY:
    target: https://github.com/ahb-sjsu/geometric-observation/blob/master/docs/replication-vacuity-survey.md
    title: "The Vacuity of 'Fresh': A Survey of Replication and Consistency Schemes through the Consumer-Relative Witnessed Certificate"
    author:
      - ins: A. H. Bond
    date: 2026

--- abstract

IEEE 802.11 channel-access decisions rest on liveness and quiescence
signals: Clear Channel Assessment (CCA), the Network Allocation Vector
(NAV), and rate-selection state. Each is, in effect, a certificate
issued by one station asserting a condition -- the medium is clear, the
reservation has expired, the link supports rate R -- on which a
*different* party, the intended receiver and the flow it carries,
depends. Such certificates can be vacuous: CCA can report the medium
clear at the transmitter while the receiver collides with a hidden node.

This document defines an EXPERIMENTAL methodology for measuring the
false-clear rate of 802.11 channel-access certificates, and an
interoperable telemetry format for a "freshness certificate" that is
consumer-relative (graded against the receiving party that depends on
the claim), witnessed (graded against an independent ground-truth
channel such as CTS, Block Ack, or monitor capture), and calibrated
(carrying a measured false-clear rate). It specifies measurement,
instrumentation, and format only. Normative changes to 802.11 PHY or MAC
behavior are out of scope and are the remit of IEEE 802.11; this document
is intended to inform such work with a common measurement vocabulary.

--- middle

# Introduction

Carrier-sense multiple access with collision avoidance (CSMA/CA), as
specified for IEEE 802.11 [IEEE802.11], makes each transmission
conditional on an assessment that the medium is available. That
assessment -- Clear Channel Assessment (CCA), possibly refined by the
Network Allocation Vector (NAV) -- is performed at the *transmitter*.
The event it is meant to prevent, a collision, occurs at the *receiver*.
Whenever the transmitter's local view of the medium differs from the
receiver's, the assessment can be wrong in the dangerous direction: the
transmitter senses the medium idle and transmits, and the receiver, in
range of a station the transmitter cannot hear, experiences a collision.
This is the classical hidden-node problem [MACA] [MACAW], and it is the
canonical instance of a broader pattern this document names.

We treat each such assessment as a **channel-access certificate**: an
assertion, implicit in a channel-access decision, that a favorable
condition holds. A certificate is **vacuous**, or exhibits a
**false-clear**, when it asserts the favorable condition while the party
that depends on it experiences the adverse outcome. The complementary
error, a **false-alarm**, defers a transmission that would in fact have
succeeded (the exposed-node case). Neither the false-clear rate nor the
false-alarm rate of deployed 802.11 certificates is routinely measured;
they are trusted by construction.

This document does not propose to change how 802.11 stations sense the
medium. It proposes, as an experiment, to *measure* how often their
"clear" is wrong for the party that depends on it, and to express the
result in an interoperable form. It adopts three properties, drawn from
a broader program on reliability of observed systems [OT] [VACUITY], as
the target for a channel-access certificate:

- **consumer-relative**: graded against the party whose successful
  reception depends on the claim -- for a transmission, the intended
  receiver, and transitively the upper-layer flow it carries -- rather
  than against the transmitter's local sensing;
- **witnessed**: graded against an independent ground-truth channel that
  the certifying station does not itself produce, such as the CTS from
  the receiver, the Block Ack that evidences reception, or a monitoring
  capture at the receiver's location;
- **calibrated**: carrying a *measured* false-clear rate, with a
  confidence interval and provenance, rather than an assumed one.

RTS/CTS [MACA] [MACAW] is, in these terms, already a partially witnessed
certificate: the CTS returned by the receiver silences the receiver's
neighborhood, evidencing the receiver-side condition. What 802.11 does
not do is *measure* the residual false-clear rate of CCA alone versus
CTS-witnessed access, per flow, or gate the use of RTS/CTS on that
measured rate. That measurement and its expression are the subject of
this document.

## Scope and Non-Goals

This document specifies:

1. terminology for channel-access certificates and their error rates
   (Section 3);
2. a measurement methodology for the consumer-relative, witnessed
   false-clear rate of 802.11 channel-access certificates (Section 5);
3. an interoperable Freshness Certificate telemetry format (Section 6).

This document does NOT specify, and explicitly defers to IEEE 802.11:

- any change to CCA, NAV, RTS/CTS, rate selection, spatial reuse, or any
  other PHY or MAC behavior;
- any new frame format transmitted over the air as part of the MAC.

The Freshness Certificate defined here is a management/telemetry object,
carried out of band (Section 6.4), describing measurements of unmodified
802.11 operation. Section 10 states the relationship to IEEE 802.11.

# Conventions and Definitions

{::boilerplate bcp14-tagged}

The key words are to be interpreted as described in BCP 14 [RFC2119]
[RFC8174]. In this document they constrain conformance to the
measurement methodology (Section 5) and the certificate format
(Section 6), NOT the behavior of any 802.11 station.

Channel-Access Certificate (CAC):
: An assertion, implicit in an 802.11 channel-access decision or explicit
  in signaling, that a condition favorable to transmission holds --
  e.g., "the medium is idle" (CCA), "no reservation is outstanding" (NAV
  expired), or "the link supports modulation and coding scheme m" (rate
  selection).

Consumer:
: The party whose successful reception depends on a CAC's asserted
  condition. For a data transmission this is the intended receiver and,
  transitively, the upper-layer flow the transmission carries. A CAC
  MAY have multiple consumers (e.g., a multicast group).

Consumer Footprint:
: The set of receivers and/or flows that constitute the consumers of a
  CAC over a measurement interval. The footprint is the 802.11 analogue
  of the general consumer footprint P used in [OT]; a certificate is
  consumer-relative when it is graded over its footprint.

False-Clear:
: An outcome in which a CAC asserts the favorable condition (clear,
  ready, rate supported) but a consumer experiences the adverse outcome
  (collision, loss, decode failure) attributable to that condition. The
  false-clear is the safety-relevant error.

False-Alarm:
: An outcome in which a CAC withholds or defers (asserts busy or
  unsupported) though a consumer would have succeeded. The false-alarm
  is the availability-relevant error (e.g., the exposed-node case).

Witness / Witness Channel:
: A signal, independent of the certifying station's own sensing, that
  evidences a consumer-side condition. Examples: the CTS returned by the
  receiver (evidencing the receiver-side clear), the Ack or Block Ack
  (evidencing reception), or a PHY capture recorded at or near the
  receiver.

Freshness Certificate:
: A CAC augmented with (a) its consumer scope, (b) its witness source,
  (c) a measured false-clear rate with a confidence interval, and (d) a
  validity horizon or refresh floor (Section 6).

Calibrated:
: Carrying a measured false-clear rate. A CAC is calibrated when its
  error rate is a measured quantity of known provenance rather than an
  assumption.

Registration-First Measurement:
: A measurement discipline in which the pass/fail thresholds and
  manipulation checks are committed before the measurement is run, and
  every outcome -- including negative results -- is retained
  (Section 5.4). This document RECOMMENDS it as the method for producing
  false-clear rates that carry evidential weight.

# The Grammar Applied to 802.11

The three target properties map onto 802.11 as follows; the mapping
motivates the measurement methodology (Section 5) and is not itself
normative.

Consumer-relative (receiver-relative):
: 802.11 CCA is performed at the transmitter, but the consumer is the
  receiver. A consumer-relative assessment grades "clear" against the
  receiver's condition. The hidden-node false-clear and the exposed-node
  false-alarm are exactly the gap between transmitter-relative sensing
  and receiver-relative truth.

Witnessed:
: The receiver-side condition is not directly observable by the
  transmitter, but it is *evidenced* by independent channels: a CTS
  witnesses that the receiver's neighborhood was silenced; a successful
  Ack/Block Ack witnesses that reception in fact occurred; a monitor at
  the receiver witnesses the medium the receiver actually saw. A
  witnessed assessment grades against these rather than against the
  transmitter's CCA alone.

Calibrated:
: A calibrated assessment reports the measured rate at which CCA-alone
  "clear" is a false-clear for the footprint, and the rate at which a
  witnessed assessment reduces it. This turns "use RTS/CTS below
  threshold T" from a static heuristic into a decision informed by a
  measured error rate.

# Channel-Access Certificates in 802.11 and Their Failure Modes

This section enumerates the certificates an experiment MAY target. For
each, it identifies the consumer, the false-clear and false-alarm
failure modes, and a candidate witness. It is informational.

## Clear Channel Assessment (CCA)

- Assertion: the medium is idle and the frame MAY be transmitted.
- Consumer: the intended receiver.
- False-clear: hidden node -- a station out of the transmitter's sensing
  range but in the receiver's range transmits concurrently; the receiver
  collides though CCA reported clear.
- False-alarm: exposed node -- the transmitter senses energy that would
  not have harmed its receiver and defers unnecessarily.
- Witness: CTS (receiver-neighborhood clear) and Ack/Block Ack
  (reception succeeded); monitor capture at the receiver.

## Network Allocation Vector (NAV) / Virtual Carrier Sense

- Assertion: no reservation is outstanding; the medium is available at
  the end of any pending duration.
- Consumer: the intended receiver.
- False-clear: a NAV that was cleared or never set (e.g., a missed
  RTS/CTS exchange elsewhere) leaves a reservation unaccounted for.
- Witness: observed on-air reservations from a monitor; Ack outcomes.

## Rate Selection

- Assertion: the link supports modulation and coding scheme m at
  acceptable error rate.
- Consumer: the intended receiver over the current channel realization.
- False-clear: a rate certificate that has gone stale as the channel
  changed (mobility, fading) -- the selected rate no longer decodes,
  producing loss. The maximum tolerable staleness before re-probe is a
  refresh floor in the sense of [OT].
- Witness: per-frame Ack/Block Ack success and PHY-reported metrics
  (RSSI, EVM) at the receiver.

## Spatial Reuse / BSS Color

- Assertion (802.11ax and later): a concurrent transmission will not
  harm the overlapping BSS.
- Consumer: receivers in the overlapping BSS.
- False-clear: a reuse decision that in fact degrades an OBSS receiver.
- Witness: OBSS receiver outcomes; coordinated monitor capture.

## Roaming Triggers

- Assertion: the current association remains adequate (or a candidate is
  better).
- Consumer: the station's active flows, whose requirements differ (a
  real-time flow versus a background transfer).
- False-clear: a consumer-blind trigger (e.g., a fixed RSSI threshold)
  that retains an association inadequate for a specific flow, or roams
  when the flow did not require it.
- Witness: per-flow delivery outcomes and latency.

# Measurement Methodology

An experiment conformant with this document produces, for a chosen CAC
and consumer footprint, a measured false-clear rate and false-alarm
rate, each graded against a declared witness, under a
registration-first discipline. This section is normative for such
experiments.

## Consumer Footprint

The experiment MUST declare the consumer footprint: the set of receivers
and/or flows over which the certificate is graded. Results MUST be
reported per footprint element and in aggregate; a single
device-global number is NOT a consumer-relative result and MUST NOT be
reported as one.

## Witness Selection

The experiment MUST declare the witness channel used as ground truth and
MUST justify its independence from the certifying station's own sensing.
Acceptable witnesses include, in increasing order of directness: the CTS
of an RTS/CTS exchange; the Ack or Block Ack of the frame; and a PHY
capture recorded at or adjacent to the receiver (e.g., monitor-mode or
software-defined-radio capture). Where a monitor capture is used, its
placement relative to the receiver MUST be reported, because the witness
is only as good as its co-location with the consumer.

## Grading

For each transmission opportunity in the interval, the experiment
classifies the CAC outcome against the witness:

- false-clear: CAC asserted clear/ready AND the witness indicates the
  consumer's adverse outcome (collision or decode failure attributable
  to the asserted condition);
- false-alarm: CAC deferred/withheld AND the witness indicates the
  consumer would have succeeded;
- otherwise: a true outcome.

The false-clear rate is the count of false-clears divided by the count
of opportunities in which the CAC asserted the favorable condition. The
false-alarm rate is defined analogously over deferrals. Both MUST be
reported with a confidence interval and the interval's method.

## Registration-First Discipline

To carry evidential weight, an experiment SHOULD commit, before the
measurement is run and in a form that cannot be silently revised, (a)
the pass/fail thresholds it will apply, and (b) manipulation checks that
confirm the measurement exercised the intended regime (for example, that
the footprint experienced a non-degenerate rate of the adverse
condition, and that the witness observed the intended events). Every
outcome, including a negative result, SHOULD be retained and reported.
An experiment that adjusts its thresholds after seeing its results, or
that discards negative runs, MUST disclose that it did so; results so
produced do not carry the evidential weight this methodology is designed
to confer. This discipline is described in [OT] and exercised across the
substrates surveyed in [VACUITY].

## Comparative Claims

A claim that a witnessed assessment dominates CCA-alone (e.g., that
RTS/CTS reduces the false-clear rate for a footprint) MUST be graded as
the difference of two measured rates over the same footprint and
interval, each with a confidence interval. The claim MUST NOT rest on a
model alone.

# The Freshness Certificate Format

A Freshness Certificate is a structured object describing a measured
CAC. It is a telemetry/management object; see Section 6.4 for transport.
Conformant producers MUST emit the fields in Section 6.1 and MUST NOT
misrepresent provenance (Section 6.3).

## Fields

A Freshness Certificate MUST contain:

- `signal`: the certificate type being described (one of: `cca`, `nav`,
  `rate`, `spatial-reuse`, `roam`, or an experimental value per
  Section 8);
- `issuer`: an identifier for the station or measurement point that
  produced the certificate;
- `consumer-scope`: a description of the footprint (Section 5.1) over
  which the rates were graded;
- `witness`: the witness source (Section 5.2) and, for a capture,
  its placement;
- `false-clear-rate`: the measured rate, with `ci-low`, `ci-high`, and
  `ci-method`;
- `false-alarm-rate`: the measured rate, with its confidence interval;
- `interval`: the measurement interval (start, end) and opportunity
  count;
- `refresh-floor`: for time-varying certificates (notably `rate`), the
  maximum staleness, as a duration, beyond which the asserted condition
  MUST be treated as unwitnessed; absent for time-invariant signals;
- `provenance`: whether the thresholds were registered before the run
  (Section 5.4), and a reference to the registration if any.

A Freshness Certificate MAY contain implementation-specific extension
fields; consumers of the format MUST ignore fields they do not
understand.

## Example (informative)

~~~
{
  "signal": "cca",
  "issuer": "urn:ap:example:radio0",
  "consumer-scope": { "flows": ["sta-7:voip", "sta-7:bulk"],
                      "footprint": "per-flow" },
  "witness": { "source": "block-ack", "placement": "receiver" },
  "false-clear-rate": { "value": 0.14, "ci-low": 0.12,
                        "ci-high": 0.16, "ci-method": "wilson" },
  "false-alarm-rate": { "value": 0.03, "ci-low": 0.02,
                        "ci-high": 0.05, "ci-method": "wilson" },
  "interval": { "start": "2026-08-21T18:00:00Z",
                "end": "2026-08-21T18:10:00Z", "opportunities": 41822 },
  "refresh-floor": null,
  "provenance": { "registered": true, "ref": "PREREG-CCA-001" }
}
~~~

The numeric values above are ILLUSTRATIVE. This document defines how to
measure and express such a certificate; it does not report a measured
false-clear rate for any deployment.

## Provenance Integrity

A producer MUST NOT mark `provenance.registered` true unless the
thresholds and manipulation checks were committed before the run in a
form that a third party could verify. Misrepresenting provenance
defeats the purpose of the format and is a conformance violation.

## Transport

Freshness Certificates are carried out of band, as management or
telemetry data (for example, in an existing network-telemetry transport,
a log, or an experiment artifact). This document does NOT define an
over-the-air frame and does not modify the 802.11 MAC. Selection of a
concrete transport encoding is left to the experiment or to a future
document.

# Experimental Mechanisms (Informative)

The methodology and format above enable, but do not specify, mechanisms
that a future IEEE 802.11 effort might evaluate. These are listed to
motivate the measurement work and are explicitly not proposed for
standardization here:

- receiver-witnessed CCA: gating RTS/CTS use on the measured, per-flow
  false-clear rate rather than a static frame-length threshold;
- calibrated rate refresh floors: re-probing the rate certificate no
  later than its measured staleness horizon;
- flow-relative roaming: grading the roam decision against the active
  flows' measured delivery, not a device-global RSSI threshold.

# Deployment and Experiment Design (Informative)

A minimal experiment comprises a transmitter/receiver pair (or an
AP/STA), a controllable interferer to induce the adverse condition at a
non-degenerate rate, and a witness -- most directly, a monitor-mode or
software-defined-radio capture co-located with the receiver. The
experiment registers its thresholds and manipulation checks
(Section 5.4), runs the footprint under alternating clear and contended
regimes, grades CCA-alone and CTS-witnessed access against the witness,
and emits a Freshness Certificate (Section 6) per footprint element. The
witness's co-location with the receiver is the dominant design risk: a
witness that observes the transmitter's medium rather than the
receiver's re-introduces the very transmitter-relativity the experiment
is meant to measure.

# Relationship to IEEE 802.11

IEEE 802.11 [IEEE802.11] is the normative authority for the PHY and MAC
behavior discussed here, including CCA, the NAV, RTS/CTS, rate selection,
and spatial reuse. This document defines neither new on-air behavior nor
new MAC frames. It offers a measurement vocabulary, a measurement
methodology, and an out-of-band telemetry format, so that the
false-clear rate of unmodified 802.11 channel-access certificates can be
measured and compared on a common basis. Its intended contribution to
IEEE work is that vocabulary and those measurements, not a MAC change.

# Security Considerations

A Freshness Certificate carries measurement data about a deployment.
Three considerations follow.

Witness integrity: because the certificate's value rests on its witness,
a forged or misplaced witness undermines it. A witness derived from
frames an adversary can spoof (e.g., unauthenticated control frames) can
be manipulated to understate or overstate a false-clear rate; experiments
SHOULD prefer witnesses that are hard to forge (reception outcomes,
authenticated captures) and MUST report witness placement.

Privacy: a consumer footprint expressed per flow can reveal which flows a
station carries and their delivery characteristics. Producers SHOULD
minimize footprint granularity to what the experiment requires and
SHOULD apply the deployment's normal telemetry-privacy protections to
emitted certificates.

Resource use: mechanisms motivated by these measurements (e.g., increased
RTS/CTS) consume airtime; an adversary able to influence the measured
rate could induce unnecessary overhead. Such mechanisms are out of scope
here, but experiments that actuate on measured rates SHOULD bound the
airtime they can induce.

Provenance is itself a security property of the format: a certificate
whose `provenance.registered` flag is not trustworthy provides no
assurance, and Section 6.3 makes misrepresenting it a conformance
violation.

# IANA Considerations

This document requests that IANA consider establishing, in a future
revision, a registry of Freshness Certificate `signal` values and
`witness` source types, to allow interoperable extension (Section 8).
The initial `signal` values are `cca`, `nav`, `rate`, `spatial-reuse`,
and `roam`; the initial `witness` source types are `cts`, `ack`,
`block-ack`, and `capture`. As an Experimental document, it makes no
other request; a decision on a permanent registry is deferred to any
standards-track successor.

--- back

# Acknowledgements
{:numbered="false"}

This work applies the consumer-relative, witnessed, calibrated framing of
Observation Theory [OT] and the cross-substrate survey [VACUITY] to
IEEE 802.11 channel access. It takes the hidden- and exposed-node framing
from the MACA/MACAW line of work [MACA] [MACAW] and the DCF analysis of
[BIANCHI].
