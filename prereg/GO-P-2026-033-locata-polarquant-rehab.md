# GO-P-2026-033 — PolarQuant DOA Gate-B, rehabilitated & re-confirmed (held-out)

An honest second look after `GO-P-2026-032` missed. That miss had two *genuine* methodological
weaknesses, not excuses: (1) the sealed config was **single-bin** (under-powered narrowband DOA in
reverb); (2) the "reconstruction-optimal" baseline was per-coordinate **uniform**, not actually
optimal — its tell was the failed recon-trade gate (PolarQuant *out-reconstructed* it on 4/13).
This prereg fixes both and re-tests on **fresh** data. The `032` negative stands on the record; this
is a corrected re-registration (the program's own `GO-020` miss → `GO-021` rematch pattern).

**Fixes.** (1) **Incoherent wideband MUSIC** — pool many STFT bins with correct per-bin steering
(far lower variance than single-bin). (2) **Lloyd–Max** fixed-rate reconstruction-optimal baseline
instead of uniform. On the now-seen data (dev/task1 + eval/task1, 16 recordings) the fix restores a
**clean trade**: at 8 cm / 48 bits, Lloyd reconstructs better than PolarQuant on **16/16** (so the
baseline is genuinely optimal) and the flip holds **13/16**. That config is frozen below.

**No goalpost-moving.** The `032` cherry (budget-64 / root-MUSIC = 9/13) is *not* used. The config
is developed only on seen data, sealed here, and confirmed on **fresh held-out `eval/task2`** — 13
recordings no test has touched (eval/task1 was consumed by 032). task2 has multiple static sources;
the reference is fixed to the **dominant source identified on the clean data**, so both arms are
scored against the same source (the relative flip stays fair). This is a cross-task generalization
test; a miss may reflect the harder multi-source regime as well as non-transfer, and will be read that way.

```yaml
id: GO-P-2026-033
date: 2026-07-18
retrospective: false
kind: real-data DOA Gate-B, rehabilitated (wideband + Lloyd-Max baseline), held-out re-confirmation
harness: experiments/rehab033.py   # --develop (seen) selects config; --confirm (held-out) governed
data:
  seen: dev/task1 {1,2,3} + eval/task1 {1..13}  # method + config selection ONLY
  heldout: eval/task2 DICIT recordings (13, multiple static loudspeakers), unused at seal time
config_frozen: {aperture: 8cm DICIT ULA, band_hz: [750, 2101], budget_bits: 48, estimator: incoherent-wideband-MUSIC}
arms: [polarquant (angle), lloyd-max (reconstruction-optimal), phase-destroy (anti)]
reference: dominant source identified by wideband MUSIC on the CLEAN snapshots (both arms vs same source)
prediction:   # sealed bars on the 13 held-out eval/task2 recordings
  flip_holds:  clean flip (PolarQuant DOA err <= Lloyd DOA err + 0.5deg AND Lloyd reconMSE <= PolarQuant reconMSE) on >= 7/13
  effect_floor: median flip_fail = median max(0, PolarQuant_DOAerr - Lloyd_DOAerr) <= 1.0 deg
  anti_worst:  phase-destroy DOA err >= max(PolarQuant, Lloyd) on >= 9/13
  recon_trade: Lloyd reconMSE <= PolarQuant reconMSE on >= 10/13 (genuine trade, not dominance)
falsification: flip holds on < 7/13 -> the rehabilitated effect still does not transfer; a STRONGER
  registered negative (both the single-bin under-powering and the baseline were fixed and it still
  failed). No eval/task2 recording was scored before this file was sealed and committed.
amendments: []
hash: sha256:7364092d83806ebff783d6945533b5638c48980a2310ddc19dcb7e37c65992c6
```

## Falsification
A pass rehabilitates the real-data flip on fresh, unseen recordings with the two honest fixes in
place — under-powering and baseline both addressed. A miss is the definitive registered negative:
the subtle consumer-relative flip does not transfer to real reverberant array DOA even when fairly
and powerfully tested; on this evidence the dissociation the theory needs is genuinely weak for this
physical consumer, while the coarse angle-carries-direction claim holds. Sealed and committed before
the governed held-out run per REG-1 (CHARTER §4).
