# GO-P-2026-052 — GO-9 second setting: coordinated reset on a Gaussian source

Registers the **second independent setting** for GO-9 (coordinated reset saves the
records' shared-structure information, first held on a binary source —
GO-P-2026-050). A PASS meets the PROTOCOL §1 `[replicated]` bar for GO-9; a miss
leaves GO-9 `[demonstrated]` and is reported at full prominence. Setting:
$X=(V_1,V_2,V_3)$ each $\mathcal N(0,I_n)$; record $M_1$ describes $U_1=(V_1,V_2)$,
$M_2$ describes $U_2=(V_2,V_3)$ (shared $V_2$); reset side information $S=V_1$, so
$M_2$ is $S$-opaque. Coordinated in-bin ML uses the other record's reconstruction of
$V_2$ as a noisy observation with the exact Gaussian weights. For per-component
reverse channels at distortion $d$ the two reconstructions of $V_2$ correlate at
$(1-d)$, so the predicted coordination discount is the Gaussian analogue of the
binary $1-h_2(d*d)$:
$\mathrm{gap}=-\tfrac12\log_2\!\bigl(1-(1-d)^2\bigr)$, and the $S$-discount on $M_1$
is $\tfrac12\log_2(1/d)$. Governs `experiments/landauer_coordinated_gaussian.py`;
result `results/GO-landauer-coordinated-gaussian.json`.

**Pilot history (logged, calibration only; pilot seed = SEED+1, n=10, T=60).**
Two instrument corrections before sealing, neither touching the physics:
1. **Grid-snapped → interpolated thresholds.** The first pilot returned discounts of
   *exactly* one grid step (0.150) for both records against a 0.328 prediction — the
   grid quantizing the effect, and a pass partly bought by tolerance. With
   interpolation the same pilot resolves 0.200 and 0.167.
2. **Gate form.** The asymptotic gap has no exact finite-$n$ counterpart and the
   pilot realized ~50–60% of it at $n=10$. C2/C3 therefore gate that coordination
   saves a **substantial fraction** of the predicted information and **cannot
   materially exceed** it, with the realized fraction reported — rather than a
   symmetric band that happened to straddle the pilot value.

```yaml
id: GO-P-2026-052
date: 2026-08-03
retrospective: false
kind: replication (second independent setting for GO-9, Gaussian source family)
claim: "On a Gaussian source, resetting either of two records that share a component is operationally cheaper when the other record is intact, by a substantial fraction of the shared-structure information -- including for the record whose own reset side information is useless; mismatched pairing saves nothing."
harness: experiments/landauer_coordinated_gaussian.py   # numpy; governed seed 20260811; --pilot used only for calibration
prediction:
  C1_s_discount_m1: |thr(m1 indep) - (Rc - 1/2 log2(1/d^))| <= 0.25
  C2_coordination_m1: 0.40*gap <= thr(m1 indep) - thr(m1 coord) <= gap + 0.15
    [pilot realized 0.61*gap]
  C3_coordination_m2: 0.40*gap <= thr(m2 indep) - thr(m2 coord) <= gap + 0.15
    [pilot realized 0.51*gap]
  C4_shuffled_null: one-sided -- thr(shuffled) >= thr(independent) - 0.16 for both
    records (mismatched coordination provides no benefit; it may be worse)
  C5_channel_realized: d^ in [0.28, 0.48]
  C6_uniform_control: pooled chance-relative at 4 sigma per bin rate
falsification: C2/C3 failing refutes the Gaussian-setting coordinated-reset saving;
  C4 failing (shuffled coordination HELPS) means a decoder artifact rather than
  shared record structure; C5 failing voids the run.
design:
  n: 12
  trials: 150
  D_target: 0.35 per component
  rb_grid: [0.40, 0.55, 0.70, 0.85, 1.00, 1.15, 1.30, 1.45, 1.60, 1.75]
  stopping: fixed design, single governed run, seed 20260811
controls: [shuffled-pairing null (one-sided), uniform control (pooled 4 sigma), channel window, S-opaque record as internal comparison]
amendments: []
hash: sha256:b3a32cd10e37ee040d599374a5ffc057b887f7844c79a6b06b5ecadecb583973
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2 and GO-9 keeps
class `[demonstrated]`. CI re-checks the committed JSON's self-consistency but cannot
re-run Tier B.
