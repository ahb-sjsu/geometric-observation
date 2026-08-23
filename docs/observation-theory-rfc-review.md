# Review of `draft-bond-ot80211-freshness-00`

## Overall verdict

The receiver-relative reframing of IEEE 802.11 channel access is strong and worth pursuing. The draft is a useful `-00` problem statement, but it needs a major revision before it is technically sound as either a measurement specification or an interoperable telemetry format.

The central weakness is identifiability: Section 5 assumes that CTS, ACK/Block Ack, or a monitor can establish facts that they do not, by themselves, establish. The supporting experiment also relies on a software platform that cannot implement its required CSMA/CA and RTS/CTS behavior.

| Area | Assessment |
|---|---|
| Problem framing | Strong and memorable |
| Receiver-relative insight | Substantive contribution |
| Measurement definition | Major rewrite needed |
| Statistical methodology | Incomplete |
| Telemetry interoperability | Information model only, not yet a format |
| Security and provenance | Incomplete |
| Experiment implementation | Currently blocked |
| RFC hygiene | Mostly straightforward fixes |

## Critical findings

### 1. CTS is being confused with a witness

CTS is part of the access treatment: it changes other stations' behavior by causing stations that decode it and honor the NAV to defer. It is not an independent ground-truth observation of whether the subsequent data transmission would collide.

Similarly:

- A received ACK or Block Ack establishes some degree of successful reception.
- A missing ACK does not distinguish collision, fading, rate mismatch, receiver failure, ACK loss, or implementation error.
- A receiver-adjacent IQ capture can establish overlapping energy or waveforms, but overlap is not automatically causal. Capture effect and unrelated link errors remain possible.

The model should separate four concepts:

1. `access-method`: basic access or RTS/CTS access.
2. `cca-observation`: idle/busy plus threshold and configuration.
3. `consumer-outcome`: complete success, partial Block Ack, decode failure, or indeterminate.
4. `outcome-witness`: receiver trace, ACK evidence, synchronized IQ capture, or a compound witness.

The basic observable metric could be defined as:

```
FCR = N(CCA idle AND attempted AND receiver failure
        AND witness-confirmed interferer overlap)
      / N(CCA idle AND attempted)
```

This is an *interferer-overlap loss rate* unless the experimental design actually identifies causation. The phrase "attributable to" in Sections 2 and 5.3 currently hides the hardest part of the method.

Also replace "CCA-alone" with "basic access." Both basic access and RTS/CTS access still use CCA.

### 2. False alarms are counterfactual

When CCA reports busy, no frame is sent. Therefore neither an ACK nor a passive monitor can establish that the receiver "would have succeeded."

The desired quantity is a potential outcome:

```
P(success if transmitted | CCA busy)
```

It requires an intervention, such as occasionally overriding CCA under controlled conditions, or a clearly disclosed counterfactual model. Section 5 currently requires every conformant experiment to report both false-clear and false-alarm rates, while the supporting CCA cell measures only false-clears. The planned cell is therefore nonconformant with the draft it supports.

For the next revision, either make false-alarm measurement optional and define a separate active-measurement procedure, or remove it from the first document.

### 3. The proposed experiment platform cannot run the experiment

The CCA cell plan correctly labels itself a hardware design rather than a built experiment, but it proposes `gr-ieee802-11` for logged CCA and the RTS/CTS comparison.

The upstream `gr-ieee802-11` README states that it currently has no CSMA/CA mechanism and that RTS/CTS does not work because of its timing limitations. This invalidates the proposed experimental path.

OpenWiFi appears much closer to the required substrate because it exposes FPGA-based DCF/CSMA/CA, CCA thresholds, NAV, ACK controls, and IQ capture. It should be treated as a candidate until its exact RTS/CTS behavior and per-opportunity logging have been demonstrated.

The interferer must also be a MAC participant that decodes CTS and honors NAV. A scheduled OFDM burst generator will not demonstrate an RTS/CTS benefit unless it implements that behavior.

### 4. The comparison and statistics are underspecified

"Same footprint and interval" does not make two rate estimates comparable. Basic and RTS/CTS access cannot both occur on the same opportunity, and channel conditions are correlated over time.

The method should require:

- randomized, interleaved treatment assignment or randomized blocks;
- identical traffic and interferer-generation rules;
- a directly computed confidence interval for the rate difference or ratio, not merely separate intervals;
- a declared clustering unit such as RF run, interference burst, or time block;
- handling of unknown and censored outcomes;
- manipulation checks for timestamp error and witness-classifier performance.

A Wilson interval is appropriate only under its sampling assumptions. Wi-Fi losses are bursty, so naive per-frame Wilson intervals may badly understate uncertainty. Block bootstrap, run-level intervals, or cluster-robust methods are safer.

The atomic opportunity also needs a precise definition: PPDU, MPDU, retry attempt, or TXOP. A-MPDU and partial Block Ack outcomes must be addressed explicitly.

## Scope and IEEE 802.11 accuracy

The next revision should be narrowed to CCA and the basic-access-versus-RTS/CTS experiment.

NAV, rate selection, spatial reuse, and roaming do not share a common event unit, witness, adverse outcome, or validity model. In particular:

- An expired NAV means that the station has no currently known virtual-carrier-sense reservation, not that no reservation exists globally.
- Rate-selection algorithms are generally implementation choices; IEEE 802.11 defines rates, MCSs, and relevant signaling, not a universal rate-selection algorithm.
- Roaming policy is substantially implementation and deployment specific.
- A spatial-reuse decision is more conditional than "will not harm the overlapping BSS."

These may become future measurement profiles, but including them now makes the generic format appear broader than the methodology can support.

A more standards-facing title would be:

> Receiver-Relative Measurement of False-Idle CCA Outcomes in IEEE 802.11

Observation Theory can remain the motivation. "Freshness" is not the natural term for an instantaneous CCA decision, and "certificate" often implies a signed security object. "CCA Measurement Report" or "Channel-Access Calibration Record" would carry less semantic baggage.

## Telemetry model

Section 6 defines field names and an illustrative JSON object, but not an encoding, schema, types, allowed ranges, extension rules, versioning, confidence level, or machine-readable consumer scope. It is currently an information model, not an interoperable format.

| Current field | Needed revision |
|---|---|
| `signal` | `measurement-profile` with a profile version |
| `issuer` | Separate measured `subject` from report `producer` |
| `consumer-scope` | Defined receiver/TID/traffic-class identifiers and aggregation rules |
| `witness` | Source, placement, classifier/version, synchronization method, and timing error |
| `interval.opportunities` | Eligible, idle, busy, attempted, success, overlap-loss, other-loss, and unknown counts |
| CI fields | Confidence level, estimator, sampling assumptions, and clustering unit |
| Missing context | Channel, bandwidth, PHY, MCS, powers, CCA threshold, retries, aggregation, topology, and software/firmware versions |
| `provenance` | Immutable plan URI, digest, seal time, and result digest |
| `refresh-floor` | Rename to `max-age` or `validity-duration` |
| Missing | Schema/version identifier |

Other defects:

- Section 6.1 says `refresh-floor` is absent for time-invariant signals, but the example includes it as `null`.
- `interval.opportunities` cannot represent the different false-clear and false-alarm denominators.
- "Ignore unknown fields" is unsafe without versioning and rules distinguishing optional extensions from interpretation-changing semantics.
- Per-footprint aggregation has no defined weighting rule.
- `provenance.registered: true` is an assertion, not evidence.

If no JSON/YANG/CBOR encoding and transport are to be selected yet, rename Section 6 to "Freshness Certificate Information Model" and remove the claim of wire interoperability.

## Security and provenance

The security section should cover:

- producer authentication and authorization;
- report tampering;
- replay and rollback of old reports;
- clock manipulation and synchronization failure;
- witness compromise;
- identifiers' linkability across reports;
- maliciously inflated rates that trigger airtime-consuming behavior;
- confidentiality of per-flow telemetry.

A preregistration reference should include an immutable URI, plan digest, commitment time, and result digest. If "certificate" remains the term, define how it is authenticated or explicitly state that it is not a cryptographic certificate and must be protected by its transport.

## Repository assessment

The linked `observation-theory` repository is a front door containing a README and license. The actual draft source, generated artifacts, survey, and cell design live under `geometric-observation/docs`.

For RFC support, create a focused repository or a prominent RFC area containing:

- source plus generated XML, TXT, and HTML;
- pinned build instructions;
- CI running the draft generator and `idnits`;
- a machine-readable schema and example validation;
- acquisition and grading code;
- the experimental profile and preregistration;
- an Implementation Status section;
- an explicit statement that the hardware experiment has not yet been run.

The existing general CI compiles research papers but does not validate or regenerate the RFC artifacts.

## Standards and editorial fixes

- Replace IEEE 802.11-2020 with the active IEEE 802.11-2024 revision.
- Section 1.1 says Section 10 describes the IEEE relationship; it is Section 9.
- Remove the duplicated BCP 14 paragraph.
- Use `ACK` consistently.
- Lowercase descriptive `MAY` uses that are not normative requirements.
- Section 6.1 refers to experimental values "per Section 8," but Section 8 defines no extension-value syntax.
- `[OT]` has no URL and its cited title does not match the current paper. Use the actual archived citation or DOI.
- `[VACUITY]` points to a mutable `master` branch and labels itself a working survey. Cite an immutable commit or archived release.
- Add complete publication information and persistent identifiers for MACA, MACAW, and Bianchi.
- The IANA section must either request a fully specified registry now or state: "This document has no IANA actions." "Consider establishing, in a future revision" is not an actionable IANA request.

## Recommended revision sequence

1. Narrow the normative document to receiver-relative CCA false-clear measurement.
2. Separate access treatment, CCA observation, consumer outcome, and witness.
3. Define the atomic opportunity and all outcomes, including unknown/censored cases.
4. Move false-alarm measurement to a separate active procedure or make it optional.
5. Replace the generic JSON format with a precise CCA information model.
6. Correct the experimental platform and conduct an unsealed feasibility shakedown before fixing preregistered bars.
7. Add RFC build and schema validation plus an Implementation Status section.
8. Update the IEEE reference, IANA text, cross-references, and archival citations.
9. Decide whether the intended venue is IEEE 802.11, IETF/IRTF measurement work, or the Independent Stream.

## Publication recommendation

Circulate the concept and problem statement now, but do not ask for adoption or claim an interoperable format until the measurement semantics and experimental platform are repaired.

The receiver-relative insight survives the critique and is the draft's real contribution. The present witness, attribution, false-alarm, and calibration machinery does not yet.
