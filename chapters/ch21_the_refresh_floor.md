# Chapter 21 — The Refresh Floor

> **STUB [A] — draftable now.** Source: OT-14 law
> (`analysis/csi/CSI-refreshfloor.{json,png}`, `csi_sweep.py`); the prediction
> results (`csi_predict.py`, `CSI-PREDICT-NOTES.md`); NTN (`csi_ntn.py`). House
> voice per Ch. 19.

## What this chapter must establish

- **The floor is not a convention.** The maximum report/renew interval holding FC at
  target is proportional to the certified condition's **coherence time**:
  $\phi \approx K\,T_{\mathrm{coh}}$. Measured on a real 5G NR physical layer (Sionna
  LDPC + TR38.901 fading): $K \approx 0.177$, $R^2 \approx 0.92$ [demonstrated]
  (the OT-14 law).
- **Prediction cannot buy horizon.** The optimal linear (Wiener) predictor saturates
  within one coherence time; for a memoryless-past-$T_{\mathrm{coh}}$ Gaussian
  process this is information-theoretic, not an engineering limit [demonstrated].
  A wall, not a knob — the freshness dual of the rate–distortion converse.
- **The floor is consumer-relative too.** A stricter target (URLLC 1e-3 vs eMBB
  1e-1) shortens the floor; the same channel, two consumers, two floors.
- **When refreshing cannot close the loop.** If already at the floor and still
  vacuous, the limit is a *mechanism*, not a cadence (deep-fade outage; NTN
  RTT $>$ $T_{\mathrm{coh}}$, stale-on-arrival) — motivates the governor's escalation
  (Ch. 23).

## Key figures / claims (→ ledger)
- The $\phi$-vs-$T_{\mathrm{coh}}$ line, slope 0.177, $R^2$ 0.92 [demonstrated].
- Predictor-saturation curve (naive vs Wiener, both saturate ≤ $T_{\mathrm{coh}}$) [demonstrated].
- NTN stale-on-arrival regime (RTT vs $T_{\mathrm{coh}}$).

## Boundary
$K$ is measured on one substrate; cross-substrate universality of the constant is
`[predicted]`, not claimed. Derive-then-measure, never fit-then-assert.
