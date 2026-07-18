# GO-P-2026-032 — PolarQuant DOA Gate-B, held-out LOCATA confirmation

The real-data companion to `GO-P-2026-031`, done with the registration-first calibration/held-out
discipline after a reviewer critique collapsed an earlier (leaky, same-recording) exploratory
positive. The compressor is the **real PolarQuant** transform (turboquant-pro foundation; Han et al.
arXiv:2502.02617) — decompose each snapshot into radius + angles and quantize separately. The
consumer is a **mature, independent** MATLAB Phased Array estimator (ESPRIT + root-MUSIC), exact
because the 8 cm DICIT ULA is at exactly λ/2 (2144 Hz). PolarQuant is what the program exists to
validate: for an angle-reading consumer, "spend bits on the angle" and "preserve the read operator"
coincide, so this tests the thesis on a real physical consumer.

**Calibration → held-out separation.** A structural-fuzzing search over
{bandwidth, aperture, bits, energy%} on **dev/task1** calibration recordings only
(`fuzz_doa_technique.py`) mapped where the flip holds (134/180 configs; robust for small aperture +
moderate bits). The single config below was selected there. It is now frozen and evaluated on the
**13 unseen `eval/task1` DICIT recordings** — no eval data was scored before this seal.

**Frozen config.** 8 cm DICIT ULA (channels {3,4,6,9,10}), single STFT bin at 2144 Hz (exact λ/2),
matched-bit budget 48 (64 reported as support). Three quantizers on the real-embedded snapshot:
**PolarQuant** (angle-favoring), **scalar-uniform** (reconstruction-optimal, neutral baseline),
**phase-destroy** (magnitude-fine/phase-coarse, anti).

**Clean flip (both halves)** per recording: `PolarQuant DOA err ≤ scalar DOA err + 0.5°`
**and** `scalar reconstruction MSE ≤ PolarQuant reconstruction MSE` (so PolarQuant genuinely trades
reconstruction for angle, not wins everywhere).

```yaml
id: GO-P-2026-032
date: 2026-07-18
retrospective: false
kind: real-data DOA Gate-B, held-out (PolarQuant compressor + mature MATLAB estimator)
harness: experiments/confirm_locata.py     # governed; reuses polarquant_doa_gateb.py + pq_doa.m (MATLAB)
data:
  calibration: dev/task1 recordings {1,2,3}  # config selection ONLY (fuzz_doa_technique.py)
  heldout: eval/task1 DICIT recordings (13, single static loudspeaker) — unseen at seal time
config_frozen: {array: 8cm DICIT ULA, bin_hz: 2144, budgets_bits: [48, 64], estimators: [esprit, rootmusic]}
arms: [polarquant (angle), scalar-uniform (recon-optimal), phase-destroy (anti)]
prediction:   # sealed bars, evaluated at budget 48, "either estimator" = esprit or root-MUSIC
  flip_holds:  clean flip (DOA half + reconstruction half) holds on >= 8/13 held-out recordings
  effect_floor: median flip_fail = median max(0, PolarQuant_DOAerr - scalar_DOAerr) <= 1.5 deg
  anti_worst:  phase-destroy DOA err >= max(PolarQuant, scalar) on >= 10/13
  recon_trade: scalar reconstruction MSE <= PolarQuant's on >= 10/13 (a genuine trade, not dominance)
falsification: flip holds on < 8/13 held-out recordings -> the calibration-selected effect does NOT
  transfer; recorded as an honest negative (candidate NEG entry). A miss on anti_worst/recon_trade
  qualifies the mechanism. No eval recording was scored before this file was sealed and committed.
amendments: []
hash: sha256:fecdd68f3ae5af7eb7c0c4c8a7d768c7929dd156869751c903dbd071db3a3a6a
```

## Falsification
A pass is the consumer-relative flip demonstrated on **real, unseen microphone-array recordings**
with the program's own compressor (PolarQuant) and an **independent mature** estimator, config chosen
on calibration and confirmed out-of-sample. A miss is an honest negative: the effect selected on
calibration does not generalize. Sealed and committed before the governed held-out run per REG-1
(CHARTER §4).
