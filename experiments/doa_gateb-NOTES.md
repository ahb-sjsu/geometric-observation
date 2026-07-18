# GO-P-2026-031 — DOA Gate-B (simulated physical): notes

**Result: ALL PASS**, prospective, held-out params ($M=16,\ \theta_0=-7^\circ,\ \kappa=4$),
sealed pre-run at commit `ee85622`. A physical-estimation Gate-B (direction-of-arrival on a
ULA) exhibiting the GO-2 reconstruction flip and the Appendix-E omission floor, with the read
operator verified and confirmed by two estimators sharing no algorithm.

## The design pivot (why v1 failed)
The first attempt (MATLAB MUSIC) shaped the compression error relative to the **signal
subspace** $\mathrm{span}(A)$ and got **RMSE $=0$ for every arm** — a subspace method is
scale-invariant within $\mathrm{span}(A)$, so error placed there never moves the DOA estimate.
The angle-informative read direction is instead the **array-manifold derivative orthogonalised
against the steering vector**, $\hat g = \mathrm{normalize}(P_a^\perp a'(\theta_0))$. This lives
largely in the *noise* subspace, which is exactly why "protect $\mathrm{span}(A)$" starved it.
The empirical read direction (finite-difference gradient of the estimator) matches the analytic
$\hat g$ at $\cos = 1.0000$ — $P_C$'s range verified, not assumed.

## What passed (all five sealed triggers)
1. **Geometry** $\cos(w,\hat g)=1.0000 > 0.99$.
2. **Flip (beamformer-ML)** 6/6: angle MSE invariant $<$ recon $<$ anti at every rate, while the
   recon arm minimizes reconstruction energy at every rate — reconstruction-optimal is
   downstream-worst (GO-2 in a physical DOA domain).
3. **Flip (root-MUSIC, independent estimator)** 6/6 — estimator-agnostic. The reconstruction-energy
   columns match the beamformer-ML harness to 3 sig figs (shared shaping; recon energy is a
   property of the arms, not the estimator).
4. **Effect floor**: MSE step ratios rec/inv $=3.89$, anti/rec $=4.11$, both in the registered
   band $[2.4,6.4]$ around $\kappa=4$ — magnitude tracks $\mathrm{tr}(P_C\Sigma_\delta)\propto$ var
   on $\hat g$, not merely the sign.
5. **Omission floor**: leaving $\hat g$ uncoded floors the angle MSE at $4.8\times10^{-2}\,\deg^2$
   regardless of rate — **1984×** the coded value at the highest rate (App-E omission, physical).

**Shuffled-consumer control** (shaping about a random direction, not $\hat g$): flip 0/6, median
arm-spread 0.113 — no ordering. The effect is specific to the angle-informative direction.

## Scope
One source, single-snapshot beamformer-ML (numpy) and multi-snapshot root-MUSIC ($T=32$, MATLAB
Phased Array). Simulated, physically-grounded — the numerically-simulated companion to
`DRAFT-radar-clutter-gateB` (real X-band, still awaiting capture). Exploratory lineage:
`doa_gateb_v2.py` ($M=12,+12^\circ,3$), `pilot_doa_gateb.py`.
