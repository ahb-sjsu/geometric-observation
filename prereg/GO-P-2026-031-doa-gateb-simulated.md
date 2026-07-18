# GO-P-2026-031 — DOA Gate-B: the reconstruction flip + omission floor on a simulated physical estimator

A **simulated-physical** Gate-B: direction-of-arrival (DOA) on a uniform linear array — a classical
physical estimation problem, standing in as the numerically-simulated companion to the physical-data
`DRAFT-radar-clutter-gateB` (which waits on real X-band capture). It exhibits GO-2 (the reconstruction
flip) and Appendix-E's omission floor in a **physical estimation** domain, with the read operator
**verified**, not assumed, and confirmed by **two independent estimators**.

**The corrected read operator.** The v1 attempt shaped compression relative to the signal subspace
$\mathrm{span}(A)$ and MUSIC returned RMSE $=0$ for every arm — a subspace method is scale-invariant
within $\mathrm{span}(A)$, so error placed there does not move the estimate (logged below). The
angle-informative read direction is the **array-manifold derivative orthogonalised against the
steering vector**, $\hat g = \mathrm{normalize}\!\big(P_a^\perp\,a'(\theta_0)\big)$,
$P_a^\perp = I - aa^{H}/(a^{H}a)$; a measurement perturbation moves the angle estimate only through
its projection on $\hat g$. This is $P_C$'s range for a DOA consumer.

**Setup.** $M$-element half-wavelength ULA, source at $\theta_0$. Compression error $\delta$ in the
real embedding $\mathbb C^M\!\cong\mathbb R^{2M}$, shaped symmetrically about $\hat g$ (1 informative
real dim, $2M-1$ others) at **matched total log-precision** (identical rate): **(a) invariant** — var
$s_0^2/\kappa$ on $\hat g$; **(b) recon** — uniform $s_0^2$ (minimises $\|x-\hat x\|$); **(c) anti** —
var $s_0^2\kappa$ on $\hat g$. Consumer $\mathcal C$ = continuous beamformer-ML (matched filter,
Newton-refined; no subspace scale-invariance, no grid snapping). Independent cross-check: MATLAB
Phased Array **root-MUSIC** (multi-snapshot subspace method) on the same arms.

**Held-out.** Confirmatory params $M=16,\ \theta_0=-7^\circ,\ \kappa=4$ are out-of-sample from the
exploratory `doa_gateb_v2.py` ($M=12,\ +12^\circ,\ \kappa=3$). Sealed before the governed run.

```yaml
id: GO-P-2026-031
date: 2026-07-18
retrospective: false
kind: simulated-physical Gate-B (DOA on a ULA; GO-2 flip + App-E omission floor; independent-estimator net)
harness: experiments/doa_gateb.py            # pure numpy, beamformer-ML, CI sentinel "VERDICT: ALL PASS"
reference: experiments/doa_gateb_rootmusic.m  # MATLAB Phased Array root-MUSIC, independent estimator (Atlas)
instance:
  representation: ULA snapshot x = a(theta0) s + noise on M=16 sensors, half-wavelength
  read_operator: ghat = normalize(P_a^perp a'(theta0)); P_C = ghat ghat^T (rank 1), dim ker = 2M-1
  consumer: continuous beamformer-ML angle estimate; d_O = (theta_hat - theta0)^2 [deg^2]
  arms: [invariant (var s0^2/kappa on ghat), recon (uniform s0^2), anti (var s0^2*kappa on ghat)]
  held_out: {M: 16, theta0_deg: -7, kappa: 4}   # exploratory: {12, +12, 3}
prediction:
  geometry: cos(empirical read direction w, analytic ghat) > 0.99   # P_C's range verified, not assumed
  flip_ml:  angle MSE invariant <= recon <= anti at ALL 6 rates AND reconstruction energy minimized by
            recon at ALL 6 rates (beamformer-ML)                     # 6/6
  flip_rootmusic: same ordering at ALL 6 rates under MATLAB root-MUSIC (independent subspace estimator)
  effect_floor: beamformer-ML MSE step ratios median(MSE_rec/MSE_inv), median(MSE_anti/MSE_rec) each in
            [2.4, 6.4] around kappa=4   # magnitude tracks tr(P_C Sigma_delta) ~ var on ghat, not just sign
  omission: leaving ghat UNCODED floors invariant MSE at >= 100x the coded value at the highest rate
controls:
  - shuffled-consumer: shaping about a RANDOM unit direction (not ghat) yields NO arm ordering
    (flip <= 1/6, median arm-MSE spread ~ 0)
  - cross-implementation: root-MUSIC REC_* columns match doa_gateb.py's (reconstruction energy is a
    property of the arms, not the estimator)
design:
  n: 2500 (flip) / 1500 (shuffled, omission); MATLAB nTrials=500, T=32 snapshots
  clusters: independent Monte-Carlo trials (fixed-n)
  bits_matched_via: total log-precision conserved across arms by construction (audited: sum over dims equal)
falsification: any ordering violation beyond MC noise in EITHER estimator; reconstruction not minimized by
  the recon arm; cos(w, ghat) <= 0.99; a step ratio outside [2.4, 6.4]; the shuffled control showing an
  ordering; or the omission floor < 100x. Any one refutes the corresponding claim.
prior_negative: v1 (MATLAB MUSIC, read operator = span(A)) gave RMSE 0 for all arms — subspace
  scale-invariance within span(A). Corrected read operator = P_a^perp a'(theta0). Logged as the design pivot.
amendments: []
hash: sha256:a5df3f77573ed2167bf3905d4334d8b2d5464bf799a7a404bc960eb0cdb7df17
```

## Falsification
A pass is Observation Theory's read operator, **verified from the estimator's own sensitivity**
($\cos=1$ to the analytic $P_a^\perp a'$), predicting the winning compressor on a **physical estimation**
task, and reproduced by **two estimators that share no algorithm** — while the omission of a single
read direction imposes a rate-irreducible angular floor. A miss on any sealed trigger downgrades the
corresponding claim. Sealed and committed before the governed run per REG-1 (CHARTER §4).
