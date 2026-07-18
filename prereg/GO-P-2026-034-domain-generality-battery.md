# GO-P-2026-034 — Domain-generality battery for the consumer-relative flip

A sealed **replication battery**. The consumer-relative reconstruction-flip — at matched bits, a
code that preserves what the consumer *reads* beats a genuinely reconstruction-optimal code on the
downstream task, while the reconstruction-optimal code reconstructs the signal better — has been
shown in simulation, on LLM attention keys, and on one acoustic mic-array DOA corpus. The open
question is whether it is a **property of the observation** (domain-general) or an artifact of those
regimes. This battery fixes, *before running any new domain*, a uniform protocol, the full domain
roster, per-domain pass bars, and a binding commitment to run and report **every** registered domain
— positive or negative. Accumulating only positives across domains would itself be p-hacking; the
`GO-P-2026-032` miss is the template for how negatives are reported.

## Uniform protocol (identical across all domains)
On the domain's native representation, three quantizers at **matched total bits/sample**:
- **(R) read-preserving** — the angle/read-operator-aligned allocation (PolarQuant angle-favoring,
  or the domain read operator recovered black-box per GO-P-2026-033).
- **(O) reconstruction-optimal** — Lloyd–Max fixed-rate (the neutral baseline that minimizes MSE).
- **(A) anti** — destroys the read direction (e.g. phase-coarse / read-subspace-starved).

Consumer = the domain's own mature estimator (independent of the compressor). Per held-out instance,
score the **downstream error** and the **reconstruction MSE**. **Clean flip (per instance):**
`error(R) ≤ error(O) + tol` **and** `reconMSE(O) ≤ reconMSE(R)` (O reconstructs better yet is
downstream-worse). **Anti check:** `error(A) ≥ max(error(R), error(O))`. Config/hyperparameters are
selected on a **calibration/seen** split and **frozen** before the **held-out** run (per domain).

```yaml
id: GO-P-2026-034
date: 2026-07-18
retrospective: false   # prospective for the NEW domains D1-D4; anchors A1-A3 are prior confirmed evidence
kind: sealed multi-domain replication battery (domain-generality of the consumer-relative flip)
protocol: three matched-bit codes (read-preserving / reconstruction-optimal / anti); consumer-native
  estimator; flip = O reconstructs better yet downstream-worse than R; calibration->sealed->held-out
anchors_already_confirmed:   # cited as prior evidence, NOT part of the sealed prospective prediction
  A1_synthetic:   {ref: GO-P-2026-031, consumer: beamformer-ML + root-MUSIC, status: confirmed}
  A2_llm_keys:    {ref: GO-B-Llama-rematch, consumer: softmax attention (Llama-3.2-3B), status: confirmed}
  A3_acoustic_doa:{ref: GO-P-2026-033, dataset: LOCATA, consumer: wideband MUSIC, status: confirmed}
prospective_domains:
  D1_radar_doa:
    domain: automotive/RF radar (electromagnetic — DIFFERENT PHYSICS, same DOA consumer)
    dataset: RADIal or RaDICaL raw-ADC MIMO radar (verify availability/licensing pre-run)
    consumer: MVDR/ESPRIT DOA on the virtual array; ground truth from co-registered camera/lidar
    calibration: designated calibration recordings; heldout: disjoint recordings
    bar: clean flip on >= 60% held-out frames/scenes; recon-trade >= 60%; anti worst >= 70%
  D2_acoustic_2:
    domain: acoustic mic-array DOA, INDEPENDENT corpus (within-domain robustness)
    dataset: DCASE SELD / STARSS23 or AV16.3 (verify pre-run)
    consumer: wideband MUSIC; ground truth = tracked source DOA
    bar: clean flip on >= 60% held-out; recon-trade >= 60%; anti worst >= 70%
  D3_seismic_doa:
    domain: geophysics — seismic array backazimuth/slowness (natural sources)
    dataset: a public array + catalogued event (IRIS/USArray; verify pre-run)
    consumer: array beamforming / MUSIC backazimuth; ground truth = catalogue backazimuth
    bar: clean flip on >= 55% held-out events; recon-trade >= 60%; anti worst >= 70%
  D4_optimization:   # optional stretch; extends the confirmed synthetic GO-B (Hessian consumer)
    domain: optimization — gradient compression, curvature (Hessian) consumer, on a real training step
    dataset: a small real model + task (self-contained)
    consumer: single-step update-direction distortion under the Gauss-Newton/Fisher metric
    bar: clean flip on >= 60% of held-out steps; recon-trade >= 60%; anti worst >= 70%
prediction:
  per_domain: a domain "replicates" if its clean-flip bar is met on its held-out split.
  battery: the flip replicates in >= 2 of the 3 core prospective domains {D1, D2, D3}; combined with
    the 3 confirmed anchors this establishes the flip across >= 5 independent domains spanning >= 3
    distinct physics (synthetic, EM/radar, acoustic, seismic) and non-physical consumers (LLM, optimizer).
falsification: the flip FAILS its bar in the MAJORITY of the run prospective domains -> the
  consumer-relative flip is domain-specific (an artifact of the DOA/LLM regimes), NOT a property of
  observation. Each domain's outcome is reported regardless of sign.
commitment_no_file_drawer: every domain listed here is run if its dataset is accessible (accessibility
  verified pre-run and stated), and its outcome — pass or miss — is recorded in claims/LEDGER.md.
  "Not run" is reserved solely for genuinely inaccessible data and must be stated explicitly with reason.
amendments: []
hash: sha256:ff1131d8e13fd9d25ab22b31bf28c299c55e54d5ffd246898fff6bc272ab0aba
```

## Falsification
A pass is the strongest form of the theory: the reconstruction-metric fallacy demonstrated as a
property of **observation itself** — the same flip across radar (electromagnetic), acoustic, and
seismic arrays, LLM attention, and optimization, each pre-registered and held-out. A majority miss
refutes domain-generality and bounds the claim to the regimes already shown. No prospective domain's
held-out data is scored before this battery is sealed and committed; each domain additionally freezes
its own config on calibration before its held-out run. Sealed per REG-1 (CHARTER §4).
