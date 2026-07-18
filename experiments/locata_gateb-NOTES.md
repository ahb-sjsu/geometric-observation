# Real-data DOA Gate-B on LOCATA — exploratory notes

## ⚠️ CORRECTION (rigorous black-box protocol) — the exploratory result does NOT survive
A reviewer critique (2026-07-18) flagged that the exploratory recovery (i) built its probe
subspace from the ground-truth angle and (ii) recovered and evaluated on the same recording. A
rebuilt **fully black-box** protocol (`--confirm`) fixes both: recover in the **full ambient
R^{2M}** (or a subspace at the consumer's OWN clean DOA estimate) via random probes + low-rank
LS, scoring **displacement from the consumer's own estimate** (no ground truth in recovery); a
temporal **calibration/evaluation frame split**; and a **cross-recording transfer** test
(recover on i, evaluate on j) plus **bootstrap stability** of the recovered direction.

On the same dev/task1 recordings, the effect **collapses**: recovered-operator bootstrap
stability is marginal (0.31–0.89 ambient, 0.69–0.87 subspace); the operator is not clearly
rank-1 (eigengaps ~1.3–1.9); and the recovered operator does **not** beat the analytic tangent —
median flip over 3 recordings: analytic ĝ = 5/8, recovered-same = 1–4/8, recovered-transfer =
1–5/8, with no consistent winner. **The "recovered ≫ ĝ, 8/8" advantage was an artifact of the
truth-built subspace + same-recording recover-and-evaluate.** Under a black-box, calibration-
separated protocol the real-data DOA flip is **not demonstrated**. The simulated result
(GO-P-2026-031) stands on its own; real-data transfer is, on this evidence, an honest negative /
open question (candidate NEG entry). The exploratory numbers below are retained for the record but
are superseded by this correction.

---


Empirical companion to `GO-P-2026-031` (simulated DOA Gate-B). Data: LOCATA corpus
(Open Data Commons Attribution v1.0; Zenodo 3630471), `dev/task1` (single static loudspeaker),
DICIT array. We pull the **8 cm 5-element nested ULA** (channels {3,4,6,9,10}, x = ±16/±8/0 cm,
y≈0) — real recordings, OptiTrack ground-truth azimuth. Narrowband snapshots = STFT bin ≈ 2016 Hz
(≈ λ/2 at 8 cm) over high-energy frames, power-normalised. Runs on Atlas (`/archive/locata`) via
`/home/claude/env/bin/python`.

## Self-test (synthetic ULA, no LOCATA) — PASS
`--selftest`: `cos(empirical read dir, analytic ĝ)=1.0000`, flip 6/6. The geometry-agnostic core
reproduces `GO-P-2026-031` in real units (m / Hz / c=343) before touching real data.

## The single-snapshot vs covariance tension (why naive shaping fails)
- **Single-snapshot matched filter** — read operator IS `ĝ = P_a^⊥ a'` (cos 1.0), but single-bin
  reverberant DOA scatters ~70° ⇒ the flip is real but buried under the reverb floor (MSE ~5000 deg²).
- **SRP / covariance beamformer** — low floor (2.2°) but a *different* read operator, so `ĝ`-shaping
  does not cleanly flip it. The read operator is consumer-specific (GO-1), not a property of the array.

## Autotune-to-the-scale: manifold denoising + recovered operator
"Clean up the signals" honestly: project the (compressed) snapshots onto the **signal subspace**
(rank-1) of their own covariance — uses the array manifold / the data's structure, **never the
ground-truth angle**. Then **recover the cleaned consumer's read operator empirically** (probe the
quadratic MSE response within span{a, ia, a', ia'}, take the top eigendirection) and shape the three
arms by *it*.

Result across `task1/recording{1,2,3}` (exploratory):

| rec | denoised \|Δ\| | GO-1 cos(recovered, ĝ) | flip (recovered op) | flip (assumed ĝ) |
|-----|-----|-----|-----|-----|
| 1 | 2.1° | 0.78 | **8/8** | 3/8 |
| 2 | 7.1° | 0.36 | **8/8** | 8/8 |
| 3 | 0.6° | 0.01 | **7/8** | 4/8 |

- **GO-1:** the cleaned consumer's read operator is markedly different from the manifold tangent
  (cos 0.78 → 0.36 → **0.01**, nearly orthogonal in rec3) and varies by recording — it must be
  recovered, not assumed.
- **GO-2:** shaped by the **recovered** operator the flip holds **23/24** rate points; shaped by the
  assumed `ĝ` only **15/24**. Recovering the operator is necessary *and* sufficient for the flip.
- Rate-0 (heaviest compression) can invert via estimator saturation; the sweep top is trimmed to
  `s0sq ≤ 1.0` to stay below it.

## Significance (`--sig`, n=400 compression draws/arm, recovered operator)
Within-recording (randomness = the compression draws; signal + operator fixed), all 3 recordings:
- **anti > invariant** (destroy vs protect the recovered read direction): **13–89σ** across all rates.
- **recon > invariant** (uniform vs protect, at matched bits): **≥5σ** for `s0sq ≥ 0.03`, softening to
  ~2.6–5σ at the lightest compression (effect approaches the reverb floor).

The effect is real at tens of sigma *per recording*. The **generalization** sigma is separate: the
independent unit is the recording, and this is **n=3** (3/3, ~1.5σ under a coin-flip null) — breadth
needs the sealed multi-recording confirmatory below.

## Resolution — GO-P-2026-032 held-out confirmation (PolarQuant + mature MATLAB, sealed pre-run)
The redesign (per the user): real **PolarQuant** compressor (turboquant-pro foundation) + a mature,
independent **MATLAB ESPRIT/root-MUSIC** consumer (exact at λ/2), config **selected on calibration**
(dev/task1) via a **structural-fuzzing** search, **frozen + sealed**, then scored on **13 unseen
eval/task1 recordings** (`confirm_locata.py`). Result: **NOT CONFIRMED** at the sealed bars (budget 48).
- **Robust positive:** destroying phase/angle destroys DOA on **13/13** held-out (anti worst) — the
  directional information lives in the angle.
- **Registered negative:** the *subtle* flip (angle-favoring PolarQuant beats reconstruction-optimal
  scalar at matched bits) held only **6/13** (< sealed 8/13); median flip_fail 0.00° = parity, not a
  win. The calibration map's 74% was over-optimistic selection — the discipline caught it.
- Bearing: the **simulation** `GO-P-2026-031` stands; its real-data transfer of the *subtle* effect
  is an honest negative. Result: [GO-LOCATA-polarquant.json](../results/GO-LOCATA-polarquant.json).

## Status
Real-data arc **closed** as a registered honest negative (subtle flip does not transfer; coarse
angle-carries-direction claim holds). Harnesses: `locata_gateb.py`, `polarquant_doa_gateb.py` +
`pq_doa.m` (MATLAB), `fuzz_doa_technique.py` (calibration search), `confirm_locata.py` (held-out).
