---
title: "Receiver-Relative Measurement of False-Idle CCA Outcomes in IEEE 802.11"
abbrev: "Receiver-Relative CCA Measurement"
docname: draft-bond-cca-measurement-00
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
 - false-idle
 - interferer-overlap loss
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
  RFC7942:
  IEEE802.11:
    target: https://standards.ieee.org/ieee/802.11/7028/
    title: "IEEE Standard for Information Technology--Telecommunications and Information Exchange between Systems--Local and Metropolitan Area Networks--Specific Requirements--Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications"
    author:
      - org: IEEE
    date: 2024
    seriesinfo:
      IEEE: "Std 802.11-2024"
  MACA:
    title: "MACA - A New Channel Access Method for Packet Radio"
    author:
      - ins: P. Karn
    date: 1990
    seriesinfo:
      "ARRL/CRRL Amateur Radio 9th Computer Networking Conference": "pp. 134-140"
  MACAW:
    title: "MACAW: A Media Access Protocol for Wireless LAN's"
    author:
      - ins: V. Bharghavan
      - ins: A. Demers
      - ins: S. Shenker
      - ins: L. Zhang
    date: 1994
    seriesinfo:
      "Proc. ACM SIGCOMM 1994": "pp. 212-225"
      DOI: 10.1145/190314.190334
  BIANCHI:
    title: "Performance Analysis of the IEEE 802.11 Distributed Coordination Function"
    author:
      - ins: G. Bianchi
    date: 2000
    seriesinfo:
      "IEEE Journal on Selected Areas in Communications": "vol. 18, no. 3, pp. 535-547"
      DOI: 10.1109/49.840210
  OT:
    target: https://github.com/ahb-sjsu/geometric-observation/blob/38c682571f8345a6bffe6a29699e4d307988609d/paper/ot-estimation-control.pdf
    title: "Observation Theory for Estimation and Control: Consumer-Induced Geometry as a Complement to Observability, Filtering, and Feedback"
    author:
      - ins: A. H. Bond
    date: 2026
  VACUITY:
    target: https://github.com/ahb-sjsu/geometric-observation/blob/e8edc78c9b1302b3787a069152a60b0e871a5239/docs/replication-vacuity-survey.md
    title: "The Vacuity of 'Fresh': A Survey of Replication and Consistency Schemes through the Consumer-Relative Witnessed Certificate"
    author:
      - ins: A. H. Bond
    date: 2026

--- abstract

IEEE 802.11 Clear Channel Assessment (CCA) is performed at the
transmitter, but the harm it is meant to prevent -- a collision --
occurs at the receiver. Whenever the transmitter's view of the medium
differs from the receiver's, CCA can report idle while the receiver is
being interfered with by a station the transmitter cannot sense: the
classical hidden-node case.

This document defines an EXPERIMENTAL methodology for measuring, at
the receiver, the rate at which transmissions attempted after an idle
CCA indication are lost with witnessed interferer overlap
(the interferer-overlap loss rate), and for comparing that rate
between basic access and RTS/CTS access under randomized, interleaved
assignment. It also defines a CCA Measurement Report information model
for expressing such measurements with their witness, statistical
method, context, and provenance. It specifies measurement and
reporting only. Normative changes to IEEE 802.11 PHY or MAC behavior
are out of scope and are the remit of IEEE 802.11; this document is
intended to inform such work with a common measurement vocabulary.

--- middle

# Introduction

Carrier-sense multiple access with collision avoidance (CSMA/CA), as
specified for IEEE 802.11 {{IEEE802.11}}, makes each transmission
conditional on an assessment that the medium is available. That
assessment -- Clear Channel Assessment (CCA) -- is performed at the
*transmitter*. The event it is meant to prevent, a collision, occurs
at the *receiver*. Whenever the transmitter's local view of the medium
differs from the receiver's, the assessment can be wrong in the
dangerous direction: the transmitter senses the medium idle and
transmits, and the receiver, in range of a station the transmitter
cannot hear, experiences interference. This is the classical
hidden-node problem {{MACA}} {{MACAW}}.

How often this actually happens for a given link -- the rate at which
"idle" at the transmitter coincides with witnessed interference at the
receiver -- is not routinely measured in deployed networks. RTS/CTS
access {{MACA}} {{MACAW}} exists to reduce it, and its cost/benefit has
been analyzed extensively since {{BIANCHI}}, but the residual rate for
a specific link, receiver, and traffic class is generally unmeasured,
and there is no common form in which to express such a measurement.

This document defines:

1. terminology that separates the access method, the CCA observation,
   the consumer outcome, and the outcome witness ({{definitions}});
2. a receiver-relative measurement methodology for the
   interferer-overlap loss rate of transmissions attempted after an
   idle CCA indication ({{model}});
3. a randomized comparative procedure for grading basic access against
   RTS/CTS access on the same link ({{comparative}});
4. an OPTIONAL active procedure for the counterfactual false-alarm
   (exposed-node) direction ({{false-alarm}});
5. a CCA Measurement Report information model for expressing results
   ({{infomodel}}).

The methodology is motivated by a broader program on receiver-relative
(consumer-relative) reliability measurement {{OT}} {{VACUITY}}; the
motivation is summarized in {{framing}} and is not normative.

## Scope and Non-Goals

This document's normative scope is the measurement of CCA outcomes for
unicast data transmissions and the comparison of basic access with
RTS/CTS access, together with the report format for those
measurements.

This document does NOT specify, and explicitly defers to IEEE 802.11:

- any change to CCA, NAV, RTS/CTS, rate selection, spatial reuse, or
  any other PHY or MAC behavior;
- any new frame format transmitted over the air as part of the MAC.

Other channel-access decisions to which a receiver-relative
measurement discipline might later be applied (NAV expiry, rate
selection, spatial reuse, roaming triggers) are NOT covered by the
normative sections of this document; {{profiles}} records them as
candidate future measurement profiles and the reasons they are harder
than CCA. The relationship to IEEE 802.11 is stated in {{ieee}}.

The CCA Measurement Report defined here is a management/telemetry
information model ({{infomodel}}); this document does not select a
wire encoding or transport.

# Conventions and Definitions {#definitions}

{::boilerplate bcp14-tagged}

The requirement keywords in this document constrain conformance to the
measurement methodology ({{model}}, {{comparative}}, {{false-alarm}})
and to the report model ({{infomodel}}), NOT the behavior of any
802.11 station.

Access Method:
: The channel-access procedure in use for an opportunity: `basic`
  (data transmission following CCA and backoff) or `rts-cts` (the
  RTS/CTS exchange preceding the data transmission). Both access
  methods use CCA; "basic access" is therefore the correct name for
  what earlier drafts called "CCA-alone".

CCA Observation:
: The transmitter's CCA indication (idle or busy) for the primary
  channel at the moment a transmission opportunity arises, together
  with the CCA configuration under which it was made (energy-detect
  and preamble-detect thresholds, channel, and bandwidth).

Transmission Opportunity (atomic unit):
: A single PPDU transmission attempt initiated after an idle CCA
  observation. Each retry attempt is a distinct opportunity, tagged
  with its retry number. For an A-MPDU, the PPDU is the opportunity
  and per-MPDU outcomes are recorded within it ({{outcomes}}).

Consumer:
: The party whose successful reception the CCA indication is meant to
  protect: the intended receiver of the PPDU and, transitively, the
  traffic class (TID) it carries.

Consumer Footprint:
: The set of receivers and/or TIDs over which a measurement is graded.
  Results are reported per footprint element with a declared
  aggregation rule ({{infomodel}}).

Consumer Outcome:
: The receiver-side result of one opportunity: `complete-success`,
  `partial-success` (a proper subset of an A-MPDU's MPDUs delivered,
  per Block Ack), `decode-failure`, or `indeterminate` ({{outcomes}}).

Outcome Witness:
: The evidence channel used to establish the consumer outcome and the
  presence or absence of interferer overlap, independent of the
  transmitter's own sensing: `receiver-trace` (the receiver's own
  per-MPDU decode log), `ack-evidence` (ACK or Block Ack received at
  the transmitter), `iq-capture` (a synchronized IQ recording at or
  adjacent to the receiver), or `compound` (a declared combination).
  Witness requirements are given in {{witness}}.

Interferer-Overlap Loss:
: An opportunity in which the CCA observation was idle, the
  transmission was attempted, the consumer outcome was
  `decode-failure` (or `partial-success`, counted per {{outcomes}}),
  AND the witness confirms interfering energy or a decodable
  interfering waveform overlapping the PPDU at the receiver.
  Overlap is an observed coincidence; it is causal attribution only
  under a controlled design that identifies causation
  ({{attribution}}).

Interferer-Overlap Loss Rate (IOLR):
: N(interferer-overlap losses) / N(opportunities with idle CCA and an
  attempted transmission), for a declared footprint element and
  interval.

False-Idle Outcome:
: An interferer-overlap loss under an experimental design that
  identifies the overlap as causal ({{attribution}}). The IOLR of
  such a design MAY be described as a false-idle rate; otherwise the
  neutral term IOLR MUST be used.

CCA Measurement Report (CMR):
: The structured object defined in {{infomodel}} expressing one
  measurement: profile, subject, access method, footprint, witness,
  counts, rate estimates with their statistical method, context, and
  provenance.

Registration-First Measurement:
: A measurement discipline in which the analysis plan, thresholds, and
  manipulation checks are committed immutably before the measurement
  is run, and every outcome -- including negative results -- is
  retained ({{registration}}).

# Receiver-Relative Framing (Informative) {#framing}

In the vocabulary of {{OT}}, the CCA indication is an assertion made
by one party (the transmitter) on which a different party (the
receiver, and the flow it carries) depends. Three properties make such
an assertion meaningful to its consumer: it is *consumer-relative*
(graded against the receiver's condition, not the transmitter's
sensing), *witnessed* (graded against evidence independent of the
asserting party), and *calibrated* (carrying a measured error rate
with known provenance rather than an assumed one). The hidden-node
case is precisely the gap between transmitter-relative sensing and
receiver-relative truth; the exposed-node case is the availability
analogue. This document instantiates that framing for exactly one
assertion -- CCA idle -- and otherwise leaves the general program to
{{OT}} and {{VACUITY}}.

# Measurement Model {#model}

## Separation of Concerns

An experiment conformant with this document records, for every
transmission opportunity, four separate facts:

1. the **access method** in effect (`basic` or `rts-cts`);
2. the **CCA observation** (idle or busy) and its configuration;
3. the **consumer outcome** ({{outcomes}});
4. the **outcome witness** evidence used, and what it shows about
   interferer overlap.

Conflating these was the central defect of draft -00: an RTS/CTS
exchange is part of the access *treatment* (it changes other
stations' behavior via the NAV), not an independent witness of the
data transmission's outcome; a received ACK or Block Ack evidences
reception, but a *missing* ACK does not distinguish collision, fading,
rate mismatch, receiver failure, ACK loss, or implementation error;
and an IQ capture establishes overlapping energy, not causation.

## Consumer Footprint

The experiment MUST declare the consumer footprint. Results MUST be
reported per footprint element together with the aggregation rule and
weighting used for any aggregate ({{infomodel}}); a single
device-global number without a declared footprint is not a
receiver-relative result and MUST NOT be presented as one.

## Outcome Taxonomy {#outcomes}

Every opportunity MUST be classified into exactly one consumer
outcome:

- `complete-success`: all MPDUs of the PPDU acknowledged;
- `partial-success`: a proper subset of an A-MPDU's MPDUs
  acknowledged (the Block Ack bitmap is recorded; the delivered and
  total MPDU counts are reported);
- `decode-failure`: no MPDU acknowledged and the witness establishes
  the receiver did not deliver the frame(s);
- `indeterminate`: the outcome cannot be established from the
  declared witness (for example, the ACK itself may have been lost).

`indeterminate` opportunities MUST be counted and reported, not
discarded. Rate estimates MUST be accompanied by a sensitivity bound
computed with indeterminate outcomes counted first as losses and then
as successes.

For rate computation, a `partial-success` PPDU contributes its lost
MPDUs to the loss numerator only if per-MPDU overlap evidence is
available; otherwise the experiment MUST declare, in the plan, whether
partial successes are graded at PPDU or MPDU granularity, and report
both counts.

## Witness Requirements {#witness}

The experiment MUST declare the outcome witness and MUST justify its
independence from the transmitter's own sensing. For each witness
class:

- `receiver-trace`: the receiver's per-MPDU decode log. Establishes
  the consumer outcome directly; establishes overlap only if the
  receiver also records PHY-level indications, which MUST then be
  described.
- `ack-evidence`: ACK/Block Ack reception at the transmitter.
  Establishes success; on its own it CANNOT establish the cause of a
  failure and an experiment using it alone MUST classify unexplained
  failures as `indeterminate` or `decode-failure` without overlap
  attribution, never as interferer-overlap losses.
- `iq-capture`: a synchronized IQ recording at or adjacent to the
  receiver. Establishes overlap; establishes the consumer outcome
  only in combination with a receiver trace or ACK evidence.
- `compound`: a declared combination (for example receiver-trace +
  iq-capture, the reference design of {{sketch}}).

For any witness the report MUST include: the witness source and
physical placement relative to the receiver; the overlap classifier
and its version; the synchronization method between witness and
transmitter timelines; and the measured or bounded timing error.
The witness classifier's detection performance MUST be checked by
manipulation checks using injected calibration events (interferer
transmissions at known times), and the measured detection and
false-detection rates MUST be reported ({{infomodel}}).

## Rate Definition and Attribution {#attribution}

The primary observable is:

~~~
IOLR = N(CCA idle AND attempted AND loss AND witnessed overlap)
       / N(CCA idle AND attempted)
~~~

per footprint element, access method, and interval.

Overlap is not causation: capture effect can deliver a frame despite
overlap, and a loss can coincide with overlap yet be caused by fading
or rate mismatch. An experiment MAY describe its IOLR as a
*false-idle rate* only when its design identifies causation, at
minimum: (a) a controlled interferer whose transmission schedule is
known and manipulable; (b) a link-sanity manipulation check showing
the same link delivers at or above a declared success rate when the
interferer is silenced; and (c) an overlap classifier validated per
{{witness}}. Reports of designs not meeting these conditions MUST use
the neutral term IOLR.

## Registration-First Discipline {#registration}

To carry evidential weight, an experiment SHOULD commit, before the
measurement is run and in an immutable, third-party-verifiable form:
(a) the analysis plan including thresholds and estimators, (b) the
manipulation checks and their bars, and (c) the handling of
indeterminate outcomes. Every outcome, including a negative result,
SHOULD be retained and reported. An experiment that adjusts
thresholds after seeing results, or discards runs, MUST disclose
this; such results do not carry the evidential weight this
methodology is designed to confer. The provenance fields of the CMR
({{infomodel}}) carry the plan URI, plan digest, commitment time, and
result digest.

# Comparative Procedure: Basic Access versus RTS/CTS {#comparative}

A claim that RTS/CTS access reduces the IOLR for a footprint relative
to basic access MUST be produced by the following procedure.

## Treatment Assignment

Basic and RTS/CTS access cannot be applied to the same opportunity,
and channel conditions are correlated over time. The experiment MUST
therefore assign access method by randomized interleaving: either
per-opportunity randomization or randomized blocks with a declared,
pre-registered block length. Alternating fixed schedules ("same
footprint and interval") do NOT satisfy this requirement.

## Held-Constant Conditions

Traffic generation rules, interferer generation rules, PHY
configuration, and CCA configuration MUST be identical across
treatments, and MUST be recorded in the report context
({{infomodel}}).

## Interferer Requirements

If the interferer does not decode CTS and honor the NAV, RTS/CTS
cannot causally reduce interference and the comparison is void by
construction. For the comparative claim the interferer MUST be a MAC
participant: it MUST decode the receiver's CTS and defer per the NAV.
A scheduled burst generator that ignores CTS MAY be used only for the
single-arm IOLR measurement of {{model}}, and this MUST be disclosed.

## Statistics

The comparative estimand is the difference (or ratio) of the two
IOLRs. The experiment MUST:

- compute a confidence interval for the difference or ratio directly,
  not merely separate intervals per arm;
- declare the clustering unit (RF run, interference burst, or time
  block) and use an interval method valid under that clustering --
  block bootstrap, run-level resampling, or cluster-robust variance.
  A Wilson interval on per-opportunity counts is acceptable ONLY with
  a demonstrated justification of independence, which bursty
  interference generally defeats;
- report the number of clusters and opportunities per arm;
- state how indeterminate outcomes were handled in the comparison,
  with the sensitivity bounds of {{outcomes}};
- report the manipulation checks of {{model}} and, additionally, a
  check that the randomization produced comparable interferer
  exposure across arms.

# Active False-Alarm Procedure (Optional) {#false-alarm}

When CCA reports busy, no frame is sent; whether the transmission
*would have* succeeded is a counterfactual that passive observation
cannot establish. Measuring the false-alarm (exposed-node) direction
therefore requires an intervention: transmitting on a controlled
subset of busy indications under conditions that bound the harm, or a
disclosed counterfactual model.

This procedure is OPTIONAL and is NOT required for conformance with
{{model}} or {{comparative}}. An experiment implementing it MUST:
randomize the override decision within declared safety bounds; grade
outcomes with the same witness discipline as {{model}}; report the
override rate and its selection rule; and hold a regulatory posture
appropriate to deliberate transmission during busy indications (a
conducted, cabled environment is RECOMMENDED). Reports MUST keep
false-alarm estimates in fields distinct from IOLR fields, with their
own denominators ({{infomodel}}); the two rates have different
denominators and MUST NOT be pooled.

# CCA Measurement Report Information Model {#infomodel}

This section defines an information model: named fields, their
semantics, and presence requirements. It deliberately does not select
an encoding (JSON, CBOR, YANG) or transport; interoperable exchange
requires a future companion document binding this model to a concrete
schema. The example in {{example}} is illustrative pseudo-JSON, not a
wire format.

## Report Structure

A CMR consists of the following groups. Fields are REQUIRED unless
marked optional.

`schema`:
: `name` (fixed: `cca-measurement-report`) and `version` (this model:
  `1`). A consumer MUST NOT interpret a report whose `schema.version`
  it does not implement.

`profile`:
: The measurement profile and its version. This document defines
  profile `cca-iolr/1` ({{model}}), `cca-comparative/1`
  ({{comparative}}), and `cca-false-alarm/1` ({{false-alarm}}).

`subject`:
: The measured entity: transmitter identifier and link (transmitter,
  receiver, BSS). Identifiers SHOULD be stable pseudonyms
  ({{security}}).

`producer`:
: The entity that produced the report, when distinct from the
  subject (for example an offline grader). Distinguishing the
  measured subject from the report producer is REQUIRED whenever they
  differ.

`access-method`:
: `basic` or `rts-cts`; for profile `cca-comparative/1`, both arms
  appear with per-arm counts.

`consumer-scope`:
: The footprint: receiver identifier(s), TID(s) or access
  categories, the aggregation rule for any pooled figures, and the
  weighting (for example opportunity-weighted).

`witness`:
: Source (`receiver-trace`, `ack-evidence`, `iq-capture`,
  `compound`), placement relative to the receiver, synchronization
  method, measured timing-error bound, and for overlap classifiers:
  classifier identifier, version, and measured detection /
  false-detection rates from calibration events ({{witness}}).

`counts`:
: Per footprint element and access method: `eligible`, `cca-idle`,
  `cca-busy`, `attempted`, `complete-success`, `partial-success`
  (with delivered/total MPDU counts), `overlap-loss`, `other-loss`,
  `indeterminate`. False-alarm profiles add `override-attempted` and
  its outcome counts under a distinct group, preserving the separate
  denominators.

`estimates`:
: For each reported rate: `value`, `ci-low`, `ci-high`, `ci-level`
  (for example 0.95), `estimator` (for example `block-bootstrap`),
  `clustering-unit`, `assumptions` (free text, REQUIRED), and the
  sensitivity bounds for indeterminate handling ({{outcomes}}). For
  profile `cca-comparative/1`, the difference or ratio estimate with
  its own interval is REQUIRED.

`context`:
: Channel, bandwidth, PHY, MCS or rate-control setting, transmit
  powers, CCA thresholds (energy detect and preamble detect), retry
  limit, aggregation settings, topology reference (for a conducted
  bench: the attenuation network), and software/firmware versions of
  every measurement component.

`interval`:
: Measurement start and end times and the time source.

`max-age` (optional):
: A duration after which the producer advises the report no longer
  be treated as current. (This replaces the -00 field
  `refresh-floor`; a validity duration is advisory metadata, not a
  measured quantity.)

`provenance`:
: `plan-uri` (immutable URI of the registered plan), `plan-digest`
  (cryptographic digest of the plan), `commit-time`, and
  `result-digest` (digest of the raw result artifact). A bare
  assertion of registration without these fields carries no weight
  and MUST NOT be emitted in their place.

`extensions` (optional):
: A container for implementation-specific members. Consumers MUST
  ignore unrecognized members inside `extensions` and MUST NOT
  ignore unrecognized members elsewhere; a report with unrecognized
  members outside `extensions` is malformed under this model.

## Example (Illustrative Only) {#example}

~~~
{
  "schema": { "name": "cca-measurement-report", "version": "1" },
  "profile": { "id": "cca-comparative", "version": "1" },
  "subject": { "tx": "sta-anon-12", "rx": "sta-anon-7",
               "bss": "bss-anon-3" },
  "producer": { "id": "grader-bench-1" },
  "consumer-scope": { "receivers": ["sta-anon-7"],
                      "tids": [0, 5],
                      "aggregation": "per-tid",
                      "weighting": "opportunity-weighted" },
  "witness": { "source": "compound",
               "components": ["receiver-trace", "iq-capture"],
               "placement": "rx-port-conducted-tap",
               "sync-method": "shared-10mhz-pps",
               "timing-error-bound-us": 1.0,
               "classifier": { "id": "overlap-xcorr", "version":
                 "0.3", "detection-rate": 0.98,
                 "false-detection-rate": 0.01 } },
  "counts": { "basic":   { "eligible": 24011, "cca-idle": 20110,
                "cca-busy": 3901, "attempted": 20110,
                "complete-success": 16221, "partial-success": 1120,
                "overlap-loss": 2410, "other-loss": 201,
                "indeterminate": 158 },
              "rts-cts": { "eligible": 23987, "cca-idle": 20066,
                "cca-busy": 3921, "attempted": 20066,
                "complete-success": 18804, "partial-success": 704,
                "overlap-loss": 322, "other-loss": 196,
                "indeterminate": 40 } },
  "estimates": { "iolr-basic": { "value": 0.120, "ci-low": 0.101,
                   "ci-high": 0.141, "ci-level": 0.95,
                   "estimator": "block-bootstrap",
                   "clustering-unit": "interference-burst",
                   "assumptions": "bursty interferer; 412 bursts" },
                 "iolr-rts-cts": { "value": 0.016, "ci-low": 0.011,
                   "ci-high": 0.023, "ci-level": 0.95,
                   "estimator": "block-bootstrap",
                   "clustering-unit": "interference-burst",
                   "assumptions": "as above" },
                 "difference": { "value": 0.104, "ci-low": 0.083,
                   "ci-high": 0.125, "ci-level": 0.95,
                   "estimator": "block-bootstrap",
                   "clustering-unit": "interference-burst",
                   "assumptions": "paired within block" } },
  "context": { "channel": 6, "bandwidth-mhz": 20, "phy": "erp-ofdm",
               "mcs": "12mbps", "tx-power-dbm": -30,
               "cca-ed-dbm": -62, "cca-pd-dbm": -82,
               "retry-limit": 4, "ampdu": false,
               "topology": "conducted-triangle-rev2",
               "versions": { "platform": "openwifi-x.y",
                             "grader": "cca-grader-0.4" } },
  "interval": { "start": "2026-09-01T18:00:00Z",
                "end": "2026-09-01T19:00:00Z",
                "time-source": "gps-pps" },
  "provenance": { "plan-uri":
      "https://example.org/prereg/PREREG-CCA-001/immutable",
      "plan-digest": "sha256:...", "commit-time":
      "2026-08-30T12:00:00Z", "result-digest": "sha256:..." }
}
~~~

All numeric values above are ILLUSTRATIVE. This document defines how
to measure and express such a report; it does not report a measured
rate for any deployment, and no conformant experiment has yet been
run ({{status}}).

# Implementation Status {#status}

(This section follows the spirit of {{RFC7942}} and is to be removed
before any publication as an RFC.)

No implementation of this methodology exists at the time of writing,
and no conformant experiment has been run. All numeric examples in
this document are illustrative.

Platform assessment for the reference experiment ({{sketch}}):

- `gr-ieee802-11` (GNU Radio 802.11a/g/p transceiver) is NOT suitable
  for the comparative procedure: its upstream documentation states
  that it implements no CSMA/CA mechanism and that RTS/CTS does not
  work within its timing constraints. It is therefore also unable to
  provide the logged per-opportunity CCA decisions this methodology
  requires of the device under test.
- OpenWiFi (FPGA-based SDR 802.11 stack) is the current candidate
  substrate: it exposes DCF/CSMA-CA in the FPGA, CCA threshold
  configuration, NAV handling, ACK generation, and IQ access. It is
  a candidate, not a validated platform: its RTS/CTS behavior and
  per-opportunity CCA logging have not yet been demonstrated against
  the requirements of this document.
- The interferer for the comparative procedure must itself be a MAC
  participant ({{comparative}}); a scheduled burst generator does not
  qualify.

# Relationship to IEEE 802.11 {#ieee}

IEEE 802.11 {{IEEE802.11}} is the normative authority for the PHY and
MAC behavior discussed here, including CCA, the NAV, RTS/CTS, and
channel access generally. This document defines neither new on-air
behavior nor new MAC frames. It offers a measurement vocabulary, a
measurement methodology, and a report information model, so that the
receiver-relative error rate of unmodified 802.11 CCA can be measured
and compared on a common basis. Its intended contribution to IEEE
work is that vocabulary and those measurements, not a MAC change.

# Security Considerations {#security}

A CMR is measurement telemetry about a deployment; it is not a
cryptographic certificate and carries no intrinsic authentication.
The following considerations apply.

Producer authentication and authorization:
: A consumer acting on CMRs MUST be able to authenticate the producer
  and decide whether it is authorized to describe the claimed
  subject. This document does not define the mechanism; deployments
  MUST protect CMRs with the authentication and integrity mechanisms
  of their telemetry transport, or detached signatures.

Tampering, replay, and rollback:
: An attacker who can modify, replay, or re-present old reports can
  misrepresent current conditions. The `interval`, `provenance`
  digests, and transport integrity together allow a consumer to
  detect stale or altered reports; consumers SHOULD reject reports
  older than `max-age` and SHOULD verify `result-digest` against the
  artifact when acting on a report.

Clock manipulation:
: Both the witness alignment ({{witness}}) and replay detection
  depend on time. The time source MUST be reported; a consumer
  SHOULD treat reports with unverifiable synchronization claims as
  unwitnessed.

Witness compromise:
: The report's value rests on its witness. A forged or misplaced
  witness (for example, a capture at the transmitter presented as
  receiver-adjacent) reintroduces the transmitter-relativity the
  method exists to remove. Placement, classifier version, and
  calibration performance are REQUIRED fields for this reason;
  experiments SHOULD prefer witness components that an adversary in
  the measured environment cannot spoof.

Linkability and privacy:
: Per-TID footprints reveal which traffic classes a station carries
  and how well they are delivered. Subject and receiver identifiers
  SHOULD be stable pseudonyms scoped to the measurement context;
  footprint granularity SHOULD be minimized to what the experiment
  requires; and emitted reports SHOULD receive the deployment's
  normal telemetry confidentiality protections.

Induced overhead:
: Mechanisms that actuate on measured rates (for example enabling
  RTS/CTS more aggressively) consume airtime. Actuation is out of
  scope here, but a consumer that actuates on CMRs SHOULD bound the
  overhead an adversarially inflated rate could induce, and SHOULD
  weigh reports by their provenance ({{registration}}).

# IANA Considerations

This document has no IANA actions.

--- back

# Candidate Future Measurement Profiles (Informative) {#profiles}

Draft -00 of this document enumerated NAV expiry, rate selection,
spatial reuse, and roaming triggers alongside CCA. They are removed
from the normative scope because they do not share CCA's event unit,
witness availability, or validity model:

- NAV expiry: an expired NAV means the station has no currently known
  virtual-carrier-sense reservation, not that no reservation exists;
  grading it requires global on-air state that a single monitor does
  not establish.
- Rate selection: IEEE 802.11 defines rates, MCSs, and signaling, not
  a rate-selection algorithm; the "assertion" being graded is an
  implementation choice and differs per vendor.
- Spatial reuse: the reuse condition is more conditional than "will
  not harm the overlapping BSS", and the affected consumers are in
  another BSS, complicating both footprint and witness.
- Roaming triggers: policy is implementation- and
  deployment-specific, and the event unit (a roam decision) is rare
  and confounded.

Each could become a measurement profile with its own event unit,
witness, and validity analysis; none is defined here.

# Conducted Hidden-Node Experiment Sketch (Informative) {#sketch}

The reference experiment is a conducted (cabled) hidden-node
triangle: transmitter A, interferer C, receiver Rx, and a witness tap
W at the Rx port. Attenuators set the defining relationship -- A
cannot sense C (A's CCA reads idle while C transmits) but C's signal
reaches Rx at colliding level. A conducted bench removes over-the-air
regulatory exposure, makes the hidden relationship a set quantity,
and is reproducible; over-the-air replication is external-validity
work, not the first experiment.

Requirements flowing from the normative sections: A and Rx must be a
platform exposing per-opportunity CCA decisions and RTS/CTS operation
(see {{status}} for the platform assessment); C must be a MAC
participant that decodes CTS and honors the NAV for the comparative
arm; W must be synchronized to the transmitter timeline with a
reported timing-error bound, and its overlap classifier calibrated
with injected events; treatment assignment must be randomized
interleaving; and the plan, bars, and manipulation checks must be
registered immutably before the run, with an unsealed feasibility
shakedown first. This experiment has not been run ({{status}}).

# Changes from the Precursor Draft {#changes}

(To be removed before publication.) This document replaces the
never-submitted precursor draft-bond-ot80211-freshness-00, renamed to
match its narrowed scope; the changes below are relative to that
precursor.

- Narrowed normative scope to CCA measurement and the basic-access
  versus RTS/CTS comparison; NAV, rate selection, spatial reuse, and
  roaming moved to {{profiles}} with the reasons they are harder.
- Separated access method, CCA observation, consumer outcome, and
  outcome witness; retitled the document accordingly.
- Replaced "false-clear rate attributable to the condition" with the
  neutral interferer-overlap loss rate and an explicit attribution
  bar ({{attribution}}); "CCA-alone" replaced by "basic access".
- Defined the atomic transmission opportunity, the outcome taxonomy
  including partial Block Ack and indeterminate outcomes, and their
  handling in estimates.
- Moved false-alarm measurement to a separate OPTIONAL active
  procedure with its own denominators; passive experiments are no
  longer required to report it.
- Replaced the "Freshness Certificate" format with the CCA
  Measurement Report information model: schema/versioning,
  subject/producer split, witness classifier and synchronization
  fields, full count vector with distinct denominators, estimator
  and clustering fields, context, `max-age` (was `refresh-floor`),
  and digest-based provenance; removed the claim of wire
  interoperability.
- Added the comparative-procedure statistics requirements
  (randomized interleaving, direct interval on the difference,
  declared clustering, indeterminate sensitivity bounds) and the
  MAC-participant interferer requirement.
- Added an Implementation Status section recording that no
  experiment has been run and that `gr-ieee802-11` cannot support
  the required behavior; OpenWiFi is the unvalidated candidate.
- Rewrote Security Considerations (producer authentication,
  tampering/replay/rollback, clock manipulation, witness compromise,
  linkability, induced overhead).
- Updated the IEEE reference to Std 802.11-2024; fixed internal
  cross-references; removed the duplicated BCP 14 paragraph; "no
  IANA actions"; archival citations pinned (MACA, MACAW, BIANCHI
  publication data; {{OT}} title corrected; {{VACUITY}} pinned to an
  immutable commit).

# Acknowledgements
{:numbered="false"}

This work applies the consumer-relative, witnessed, calibrated
framing of Observation Theory {{OT}} and the cross-substrate survey
{{VACUITY}} to IEEE 802.11 channel access. It takes the hidden- and
exposed-node framing from the MACA/MACAW line of work {{MACA}}
{{MACAW}} and the DCF analysis of {{BIANCHI}}. The -01 revision
responds to a detailed technical review; the reviewer's separation of
access method, observation, outcome, and witness now structures the
measurement model.
