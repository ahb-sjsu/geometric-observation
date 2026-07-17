# DRAFT (unsealed) — Gate B candidate #2: X-band radar sea-clutter, dispersion-shell consumer

**Status: DRAFT — design registered, NOT yet sealed.** This is a prospective
design locked in advance of data that does not yet exist. It becomes a binding
registration (sealed hash + commit) **the day real X-band clutter is captured**
(swell-radar HLD, Phase 4), and **not before**. Until then it carries no timestamp
claim. Primary book Gate B remains the optimizer/gradient-moment instance
(`GO-P-2026-010` lineage); this is the sealed \emph{second} candidate, measured
whichever arrives first. **Zero schedule coupling:** the trilogy does not wait on
the radar and the radar does not wait on the theory.

## Why this is a clean Gate B

PROTOCOL §4 wants an out-of-sample domain disjoint from Papers I--II. X-band sea
clutter qualifies on every axis: **physical** data (not synthetic, not the training
distribution), a **classical probe-able consumer** (the Young--Rosenthal--Ziemer
1985 dispersion-shell inversion), and **external ground truth** (NDBC buoys /
WaveWatch-III hindcast). The read operator has an analytic prior *and* a real form
that may differ from it --- which is exactly what makes the identifiability test
(GO-1) fail-able.

## Instance

- **Representation $X$:** the radar clutter frame cube (a short stack of range/azimuth
  intensity frames), or its 3-D wavenumber--frequency spectrum $\hat I(k_x,k_y,\omega)$.
- **Consumer $\mathcal{C}$:** the wave-parameter extraction --- dispersion-shell fit
  $\omega^2=g\,k\,\tanh(kd)$ --- returning the wayfinding read: dominant direction
  $\theta$, dominant period $T$, and the surface-current vector $\mathbf{u}$ (from the
  shell's Doppler offset). $H_s$ (amplitude, MTF-owned) is \emph{excluded} from the v1
  consumer and shipped later as a labeled beta (calibration off the critical path).
- **Read operator (analytic prior):** concentration of energy \emph{on/near the
  dispersion surface}; $\ker\PC$ = off-shell energy (clutter, noise, non-Bragg
  harmonics). The real $\PC$ sits downstream of MTF nonlinearity, shadowing, group
  lines, and current advection and need not equal the thin shell.

## Three-arm design (§3) + GO-1 identifiability

Compressors of the frame cube at matched bit budget:
- **(a) shell-aware** --- bits allocated on/near the dispersion surface (Prop.~6
  reverse water-filling on the shell-weighted spectrum), starved off-shell.
- **(b) reconstruction-optimal** at matched bits (MSE water-filling, consumer-blind).
- **(c) anti-probe** --- preserves off-shell energy, degrades on-shell (the wrong
  quotient, on purpose).

```yaml
id: DRAFT-radar-clutter-gateB
date_drafted: 2026-07-17
seal_when: "first real X-band clutter capture (HLD Phase 4); seal + commit before the first measurement"
retrospective: false
gate: B-book (second candidate; optimizer moments primary)
substrate: X-band marine radar sea clutter (physical); ground truth = nearest NDBC buoy / WW3 hindcast
consumer: dispersion-shell inversion (Young-Rosenthal-Ziemer 1985) -> {theta, T, current vector u}; Hs excluded from v1
representation: clutter frame cube -> 3-D k-omega spectrum
arms: [a_shell_aware, b_recon_optimal_matched_bits, c_antiprobe_offshell]
probe: black-box Jacobian-sensitivity probe on the extraction consumer -> hat_P_C; compare to analytic-shell P_C
prediction:
  distortion_flip:   arm a preserves (theta, T, u) at a fraction of the budget while arm c
                     DESTROYS them at MATCHED reconstruction MSE  (GO-2 on physical data)
  external_agreement: arm-a-recovered (theta, T) agree with NDBC/WW3 within registered bars
                      (|Delta theta| <= BAR_THETA deg, |Delta T|/T <= BAR_T) -- BARS FIXED AT SEAL TIME
  identifiability:    subspace-overlap(hat_P_C, analytic-shell P_C) reported; and does hat_P_C
                      predict the arm ranking BETTER than the analytic shell does?  # the strong GO-1
  recon_insufficient: reconstruction MSE does not order the arms by downstream (theta,T,u) error
controls:
  - validity region: calm-sea "insufficient clutter" state, per-sector shadow masks, deep-water
    bathymetry null -> rendered BLIND not blank (the consumer's own ker P_C, shown)
  - the current vector from a noise-dominated (off-shell-dominated) patch must read as invalid
bars: "FIXED EX ANTE AT SEAL TIME (BAR_THETA, BAR_T, overlap floor, arm-ranking agreement)"
compute: local Tier-A + NRP scale (per proof-radar R-NRP-3: no load-bearing check requires NRP)
```

## Deployment corollary (opportunistic, not gated)

Prop.~6 (consumer-relative reverse water-filling on the shell-weighted spectrum) is
the HDF5-log compressor: gigabytes/session become bits on/near the dispersion
surface, and the LoRa three-number telemetry $(\theta,T,\mathbf{u})$ is its
$R_{\mathcal{C}}(0)$ endpoint. If it ships, the consumer-relative rate--distortion
function's first field deployment is a marine data logger --- picked up when the HLD
reaches its logging phase, on no one's critical path.

## Falsification

Not supported if: arm (a) does not beat (c) on downstream $(\theta,T,\mathbf u)$ at
matched MSE; or arm-a $(\theta,T)$ disagree with NDBC/WW3 beyond the sealed bars; or
the probe-recovered $\hat\PC$ does no better than the analytic shell (identifiability
adds nothing). A pass is the strongest possible Observation-Theory result: the read
operator recovered from a \emph{physical} consumer, predicting the winning
compressor on \emph{ocean} data, with a prediction that could have failed at sea.
