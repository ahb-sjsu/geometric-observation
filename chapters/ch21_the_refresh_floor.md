# Chapter 21 — The Refresh Floor

> **STUB [A] — draftable now.** Source (`observation-theory-campaigns`): the sealed
> age-horizon sweep XPROTO-CSI-SWEEP2 (`analysis/csi/PREREG-XPROTO-CSI-SWEEP2.md`,
> sealed 2026-08-27, graded PASS); the superseded, unsealed exploration
> `analysis/csi/CSI-refreshfloor.{json,png}` (`csi_sweep.py`), whose fit its source
> records as refuted and keeps as record; the prediction results (`csi_predict.py`,
> `CSI-PREDICT-NOTES.md`); NTN (`csi_ntn.py`). House voice per Ch. 19.

## What this chapter must establish

- **The floor is not a convention, and it is not a fixed fraction of the coherence
  time.** The maximum report/renew interval holding FC at target was first fitted, in
  an unsealed exploration on a real 5G NR physical layer (Sionna LDPC + TR38.901
  fading), as $\phi \approx K\,T_{\mathrm{coh}}$ with $K \approx 0.177$,
  $R^2 \approx 0.92$. Its source records that fit as refuted: the floors were measured
  at a relaxed 0.15 BLER threshold against a 0.10 claim, and the fresh baseline
  (BLER $\approx 0.113$) never met the budget. The sealed rerun (XPROTO-CSI-SWEEP2)
  finds that at the 0.10 budget the largest compliant report period is 4/6/4 TTI at
  10 Hz, 2/2/3 TTI at 25 Hz, and 1 TTI at 50 Hz and above (three seeds): the horizon
  collapses, and there is no proportionality law to fit. (The campaign repository
  called the refuted fit "the OT-14 law"; row OT-14 of this book's ledger is a
  different test, the Third Crucible's test of the revised principle P4, in which
  excess damage tracks drift and a refresh removes most of it.)
- **Prediction cannot buy horizon.** The optimal linear (Wiener) predictor saturates
  within one coherence time; for a memoryless-past-$T_{\mathrm{coh}}$ Gaussian
  process this is information-theoretic, not an engineering limit [exploratory]
  (an unsealed exploration, `CSI-PREDICT-NOTES.md`). That wall sits well outside the
  sealed budget horizon above, so prediction is accurate over a window the budget has
  already closed.
  A wall, not a knob — the freshness dual of the rate–distortion converse.
- **The floor is consumer-relative too.** A stricter target (URLLC 1e-3 vs eMBB
  1e-1) shortens the floor; the same channel, two consumers, two floors.
- **When refreshing cannot close the loop.** If already at the floor and still
  vacuous, the limit is a *mechanism*, not a cadence (deep-fade outage; NTN
  RTT $> T_{\mathrm{coh}}$, stale-on-arrival) — motivates the governor's escalation
  (Ch. 23).

## Key figures / claims (→ ledger)
- The sealed age horizon at the 0.10 budget against Doppler (XPROTO-CSI-SWEEP2); the
  refuted $\phi$-vs-$T_{\mathrm{coh}}$ fit (slope 0.177, $R^2$ 0.92) shown, if at all,
  as the kept record of a superseded exploration.
- Predictor-saturation curve (naive vs Wiener, both saturate ≤ $T_{\mathrm{coh}}$) [exploratory].
- NTN stale-on-arrival regime (RTT vs $T_{\mathrm{coh}}$).

## Boundary
No proportionality constant survives at the true budget (XPROTO-CSI-SWEEP2), so none
is carried to other substrates. Derive-then-measure, never fit-then-assert: the
refuted fit is that rule's own example. None of these results has a row in
`claims/LEDGER.md`.
