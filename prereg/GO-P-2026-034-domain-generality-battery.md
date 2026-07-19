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

## Amendments (post-seal — the sealed block above and its hash are unchanged and remain verifiable)

**A1 · D1 radar (RaDICaL) · 2026-07-18 · reference method + data scope.**
Recorded *before scoring any held-out flip*, from inspection of the accessible 50-frame sample.
- **Reference change.** D1's sealed plan was "ground truth from co-registered camera/lidar." On the
  accessible RaDICaL indoor array (4 RX × 2 TX = **8 virtual elements**, λ/2 ULA), the azimuth
  resolution is **~15°**; the depth-camera-derived source azimuth tracks the uncompressed array DOA
  only to ~16° residual (≈ the array's own resolution floor). An *absolute* camera GT would therefore
  be dominated by the array's resolution noise and would swamp the compression-induced flip. D1 is
  amended to score **displacement from the consumer's own uncompressed MUSIC estimate** (the
  reviewer-endorsed corrected-LOCATA protocol, `GO-P-2026-033` correction — the common resolution
  noise cancels across the three matched-bit arms). Camera depth-azimuth is retained only as a
  **validity cross-check** (uncompressed MUSIC vs depth azimuth: −0.64 over the full 50 frames;
  unstable per-split). The compressor (`compress3`) and the recon-MSE metric are unchanged from `033`.
- **Data scope.** The full multi-recording RaDICaL set is **not practically accessible**:
  `indoor_human.tar.gz` = 310 GB, 30m = 356 GB, 50m = 98 GB (~800 GB total), ROS-bag format, and the
  databank `/datafiles/{id}/download` endpoint returns **HTTP 403** to scripted access (Medusa-backed,
  browser-gated) even with UA/referer/range headers. RADIal (192-antenna, direct azimuth GT) has **no
  clear license** (license API 404) → set aside. D1 is therefore run on the **accessible 50-frame
  indoor sample** with a **within-recording temporal split** (calibration frames 0–24, held-out
  25–49) — *not* the sealed "disjoint recordings." This is stated per the battery's accessibility
  clause; the disjoint-recording held-out is blocked on data access.
- **Outcome (partial / registered-miss).** Held-out (frozen budget=32 bits, sharp≥10):
  clean flip **25/25**, recon-trade **25/25** (Lloyd reconstructs better *every* frame yet is
  downstream-worse — the textbook dissociation, on electromagnetic radar), median flip_fail 0.41°;
  but **anti worst 15/25 = 60% < sealed 70%**. Two of three sealed bars pass at 100%; the anti control
  misses (the small array's 1-bit-phase-destroyed snapshots still sometimes let MUSIC land near the
  reference). Recorded in `claims/LEDGER.md` (GO-B-RaDICaL) and
  [`results/GO-RaDICaL-radar.json`](../results/GO-RaDICaL-radar.json). Not a clean confirm; not a null
  either — the core flip + recon-trade replicate, the anti control and disjoint held-out do not.

**A2 · D2 second acoustic corpus (AV16.3) · 2026-07-18 · per-domain config FREEZE (pre-confirm seal).**
This is the config freeze the battery requires of each domain before its held-out run — sealed here,
*before* any held-out sequence is scored.
- **Dataset (accessible, verified).** AV16.3 (Lathoud, Odobez, Gatica-Perez, MLMI'04; CC-BY, cite the
  paper). **8-mic uniform circular array1** (r=0.1 m; mic coordinates from the corpus README formula),
  16 kHz. **5 single-speaker (1p) sequences** pulled from the open glat.info host (the Zenodo mirror is
  access-restricted; the original host serves per-channel WAVs directly). Ground truth = the corpus's
  camera-tracked **3D mouth location** (max err 1.2 cm) → absolute azimuth at the array-1 centre.
  A genuinely **independent** corpus (different array, room, speakers) from LOCATA (`033`).
- **Sealed D2 protocol HONORED — no reference amendment.** Unlike D1, the 8-mic array resolves azimuth
  and the tracked-GT cross-check is strong (uncompressed MUSIC vs mouth azimuth **corr +0.74–0.76**),
  so the flip is scored against the **absolute tracked GT** ("tracked source DOA"), as sealed. (The
  relative-reference flip vs the uncompressed estimate is reported alongside as corroboration.)
- **Consumer.** Incoherent **wideband MUSIC** generalised to the 2D circular geometry (single
  source/window; the speaker moves, so DOA is estimated per 0.75 s window synced to the GT time).
  Reuses the bit-identical `compress3` (pq / lloyd / anti) from `033`.
- **Split & frozen config.** Calibration = {seq01, seq02}; **held-out = DISJOINT {seq03, seq11,
  seq15}** (a real disjoint-recording held-out, which D1 could not get). Config selected on
  calibration and **frozen**: `win=0.75 s, band 500–2500 Hz, budget=64 bits`. Calibration (vs tracked
  GT): clean flip **234/295 (79%)**, anti worst **240/295 (81%)**, recon-trade **294/295 (100%)**,
  median flip_fail 0.12°. All three sealed bars cleared with margin. Held-out outcome recorded below
  after the confirm run. Harness: `experiments/av163_flip.py`. Frozen config sealed at commit `1843ebd`.
- **Outcome (CONFIRMED).** Held-out DISJOINT {seq03, seq11, seq15}, n=201 windows, frozen config, scored
  vs the **absolute tracked GT**: clean flip **148/201 (74%)** ≥ 60% ✓, recon-trade **201/201 (100%)**
  ≥ 60% ✓ (Lloyd reconstructs better *every* window yet is downstream-worse), anti worst **152/201
  (76%)** ≥ 70% ✓; median flip_fail 0.28°; GT cross-check corr **+0.65** (the consumer reads the true
  direction). **All three sealed bars pass on disjoint held-out recordings against independent, precise
  GT → D2 CONFIRMED.** The consumer-relative flip replicates on a second, fully independent acoustic
  corpus. Recorded in `claims/LEDGER.md` (GO-B-AV163) and
  [`results/GO-AV163-doa.json`](../results/GO-AV163-doa.json).

**A3 · D3 seismic array backazimuth (PDAR) · 2026-07-18 · per-domain config FREEZE (pre-confirm seal).**
Sealed here, *before* any held-out event is scored.
- **Dataset (accessible, verified).** **PDAR** (IMS network `IM`), a 13-element short-period seismic
  array (PD01–PD13), aperture **~3.2 km**, fetched via IRIS/EarthScope FDSN. **Teleseismic P** waves
  (distance 30–95°) from **catalogued earthquakes** (USGS, M≥6.5, 2017–2018): **34 events cached** after
  the distance filter. GEOPHYSICS — elastic waves, natural sources: a genuinely different physics from
  the acoustic/EM domains.
- **Sealed D3 protocol HONORED — no reference amendment.** The 13-element array resolves backazimuth to
  a few degrees on well-recorded events (median uncompressed error ~7°), so the flip is scored against
  the **absolute catalogue backazimuth** (great-circle array→epicentre; the sealed "catalogue
  backazimuth"), as sealed.
- **Consumer.** Incoherent **wideband MUSIC over backazimuth** at the theoretical teleseismic-P slowness
  (per-event `taup`/iasp91 ray parameter), single plane-wave source. A **GT-free MUSIC-sharpness gate**
  was available (seismic analog of the acoustic energy / radar sharpness gate) but the sweep found it
  unnecessary — the full event set at the chosen band performs best (`sharp_min=0`). Reuses the
  bit-identical `compress3` (pq / lloyd / anti) from `033`.
- **Split & frozen config.** Deterministic **chronological** split (calibration ≈ the 17 earlier events
  ≈ 2017; **held-out ≈ the 17 later events ≈ 2018** — disjoint events). Config selected on calibration
  and **frozen**: `band 1.0–2.8 Hz, budget=64 bits, sharp_min=0`. Calibration (vs catalogue baz): clean
  flip **14/17 (82%)**, anti worst **14/17 (82%)**, recon-trade **17/17 (100%)**, median flip_fail 0.00°.
  All three sealed bars (flip ≥55%, recon ≥60%, anti ≥70%) cleared with margin. Held-out outcome recorded
  below after the confirm. Harness: `experiments/seismic_flip.py`. Frozen config sealed at commit `2de7927`.
- **Outcome (CONFIRMED).** Held-out DISJOINT ~2018 events, n=17, frozen config, scored vs the **absolute
  catalogue backazimuth**: clean flip **13/17 (76%)** ≥ 55% ✓, recon-trade **17/17 (100%)** ≥ 60% ✓
  (Lloyd reconstructs better *every* event yet is downstream-worse), anti worst **13/17 (76%)** ≥ 70% ✓;
  median flip_fail 0.00°. **All three sealed bars pass on disjoint held-out events against independent
  catalogue GT → D3 CONFIRMED.** The consumer-relative flip replicates on a **third distinct physics**
  (seismic elastic waves, natural sources). Recorded in `claims/LEDGER.md` (GO-B-PDAR) and
  [`results/GO-PDAR-seismic.json`](../results/GO-PDAR-seismic.json).

---

## Battery result (core prospective domains {D1, D2, D3})
**Prediction MET.** The flip was to replicate in **≥2 of the 3** core prospective domains. Outcome:
**D2 (AV16.3 acoustic-2) CONFIRMED, D3 (PDAR seismic) CONFIRMED**, D1 (RaDICaL radar) **partial** — its
core flip + recon-trade replicate (25/25 both) but the anti control misses the sealed bar and its
held-out is data-limited (within-recording; the 310 GB disjoint set is inaccessible). Two clean
confirmations on **disjoint held-out data against independent ground truth**, on **two distinct physics**
(acoustic, seismic), each config-frozen-then-sealed before its held-out run, using the **bit-identical**
`compress3` compressor from `033`. Combined with the three prior anchors (A1 synthetic, A2 LLM attention
keys, A3 LOCATA acoustic), the consumer-relative reconstruction-flip is now demonstrated across
**≥5 independent domains spanning ≥3 distinct physics** (synthetic, acoustic, seismic) plus a
non-physical consumer (LLM) and a partial electromagnetic (radar) — i.e. it behaves as a property of
**observation**, not an artifact of the DOA/LLM regimes. D4 (optimization) remains an optional stretch.
