# Chapter 23 — The Governor

> **STUB [A] — draftable now.** Source: `governor.sealed` / `governor.detector`
> (network-governor), `analysis/ran` (RAN rApp core), `analysis/quantum`
> (quantum_governor), `freshread` (ZK/PG/Mongo witness-gate); `standards/
> ieee-sa-ic-freshness-whitepaper.md`. House voice per Ch. 19. The instrument
> chapter of the Reliability Part — the freshness counterpart of the blind probe
> (Ch. 10) and the recognizer (Ch. 11).

## What this chapter must establish

- **The operational loop**: observe (certificate + witness streams) → measure FC per
  `(certificate, consumer)` → govern → certify. The governor is what turns FC from a
  post-mortem into a control signal.
- **The escalation ladder** (encodes the cells' lessons):
  1. **refresh faster** — vacuous and reporting above the floor → shrink the period
     to the floor (Ch. 21);
  2. **change mechanism** — already at the floor and still vacuous → refreshing
     cannot close the loop → add diversity (link certs) / re-route (serving certs) /
     re-layout (quantum) / mitigate;
  3. **certify per consumer** — the reliability target *is* the read operator; the
     same certificate certified for a lax consumer, vacuous for a strict one.
- **The witness-gate** (`freshread`): certify a local read iff the applied watermark
  ≥ the reader's requirement, else refresh — the ZK/PG/Mongo generalization; sound
  witness ⇒ FC = 0 at a stated refresh cost.
- **Where it lives**: an O-RAN non-RT rApp / near-RT xApp (E2SM-KPM ingest, E2SM-RC
  actuation); a governed qiskit backend; a Postgres read-router. One core, many
  actuation surfaces.
- **Standards**: the certificate/witness/false-clear/refresh-floor grammar as a
  cross-domain measurement methodology → the IEEE-SA Industry Connections path (the
  false-clear rate as a first-class KPI), complementing 3GPP/O-RAN/IETF/IEEE 802.

![Figure 23.1](figures/ch23_fig1.svg)

*Figure 23.1. A schematic of the governor as the outline describes it. Top: the operational loop, which observes the certificate and witness streams, measures the false-clear rate per certificate and consumer, governs, and certifies. Below: the escalation ladder that the govern step follows. It first shrinks the refresh period to the floor, then changes the mechanism when refreshing at the floor still leaves the certificate vacuous, and certifies per consumer, since the same certificate can hold for a lax consumer and be vacuous for a strict one. The diagram shows structure only; the outline calls the governor a reference implementation.*

## Boundary / honesty
The governor adds no new physics and does not replace domain machinery (QEC, EMS
state estimation, HARQ) — it *measures and governs* the certificate those systems
already issue. Reference implementation, not a production controller; the integration
surface is named, not claimed complete.

## Close
The governor completes the Part's sentence: keep the structure the observer can use,
keep it current, grade the claim that it is — **and act on the grade.**
