# GO-P-2026-057 — Bell geometry audit: hubness does not weaken Bell (constraint-first, expected null)

Registers the **second, justified probe** of the hubness–Bell conjecture, designed from
the *constraints* rather than from a desired violation. The first probe was
`[exploratory]` and unregistered ([notes](../experiments/HUBNESS-BELL-NOTES.md)); it
reached S > 2 only via ~10–40% detection efficiency, collapsed to S = 0.019 when all
trials were counted, and signalled with residual 0.77. This entry preregisters the
model family, the test statistics, and an **expected null**.

**The null is the deliverable.** In the baseline arm P0 every Bell premise holds *by
construction*: source sampling is setting-independent (one λ draw reused across all four
contexts), responses are strictly local so $P(A\mid x,y)=P(A\mid x)$ and
$P(B\mid x,y)=P(B\mid y)$ identically, **every emitted trial is counted**, and
non-detection is an explicit third outcome $0$ rather than a deletion. Since the
pointwise bound needs only $|A|,|B|\le1$, outcomes in $\{-1,0,+1\}$ still give
$|K(\lambda)|\le2$ and hence $S\le2$ for **any** $\rho$. P0's result is therefore a
theorem; the harness exists to demonstrate computationally that it is unmoved by
dimension, density skew, Zipf concentration, corpus hubness and query concentration —
and to be reusable for future geometric hidden-variable conjectures.

**Positive controls make the null meaningful.** A null from a dead instrument is
worthless, so arms P1–P3 each break **exactly one** premise and are *required* to exceed
the bound: P1 outcome accounting (postselect on coincidence), P2 measurement
independence ($\lambda\sim\rho_{xy}$, responses still local), P3 locality (Alice reads
Bob's setting). Any future model that exceeds the bound must land in one of these
columns and name its premise.

**Full angular law, not one CHSH score.** $E(\theta)$ is swept over $[0,\pi]$. A local
sign model on a sphere yields the **sawtooth** $E(\theta)=-(1-2\theta/\pi)$, scaled by
the mean detection product — *not* the quantum $-\cos\theta$. Reporting both gaps shows
precisely where and why the quantum curve escapes, rather than fitting four numbers.

```yaml
id: GO-P-2026-057
date: 2026-08-03
retrospective: false
kind: falsification harness (Tier A, CPU; expected null, with positive controls)
claim: "A genuinely local, measurement-independent model with complete outcome accounting returns S <= 2 regardless of latent geometry -- dimension, density skew, Zipf concentration, hubness or query concentration -- and the harness's positive controls confirm it can detect a violation when exactly one premise is broken."
harness: experiments/bell_geometry_audit.py   # numpy only; governed seed 20260817; no pilot
model_family_preregistered: "latent unit vectors on S^(d-1) with a concentrated-core +
  uniform-shell density mixture and Zipf atom weights; local sign responses
  A_x = sign(q^A_x . lambda), B_y = -sign(q^B_y . lambda); detection probability
  logistic in the LOCAL setting alignment, non-detection emitted as outcome 0.
  d in {3,8,32,128} x core_frac in {0, 0.02, 0.25} x zipf_a in {0, 1.5} x
  detection sharpness in {perfect, 4, 15} = 72 P0 configurations."
prediction:
  T1_P0_respects_bound: max S over ALL P0 configurations <= 2 + 4/sqrt(n_draw)
    (finite-sample tolerance; n_draw = 200000 gives tol ~ 0.0089)
  T2_P0_no_signalling: max no-signalling residual in P0 <= the same tolerance --
    it holds BY CONSTRUCTION, so this is a check on the code, not a hypothesis
  T3_angular_law_is_sawtooth_not_cosine: for every configuration, RMS(E(theta) vs
    scaled sawtooth) < RMS(E(theta) vs -cos theta)
  T4_positive_controls_fire: each of P1, P2, P3 exceeds 2 + tol -- REQUIRED, else the
    null in P0 is uninformative
  T5_geometry_irrelevant_in_P0: |corr(S, hub skew)| < 0.35 across P0 AND max S within
    tolerance of 2
  T6_postselection_alone_breaks_it: the SAME P0 data, rescored by postselecting on
    coincidence instead of counting all trials, exceeds 2 + tol
falsification: T1 or T2 failing means the HARNESS IS WRONG (both are theorems), and the
  code goes back for repair -- it would not be a physics result. T4 failing means the
  instrument cannot see violations and the null is void. T3 or T5 failing would be a
  genuine surprise about the local model's angular structure or a geometry dependence
  where none should exist, and would be reported at full prominence.
scope: this bounds THIS preregistered family. It does not and cannot prove a general
  theorem about all contextual-accessibility constructions; adversarial postselection
  models are known to reach S = 4. Nothing here is new physics -- the contribution is
  an audited, reusable falsification harness plus the explicit demonstration that
  retrieval geometry does not weaken Bell.
amendments: []
hash: sha256:d4fe7136852fcd403fbc1c83f11b179b7797ea517fad39522c2c86a493292221
```

## Falsification
T1/T2 failures indicate a broken harness, not a discovery, and are reported as such.
T4 failure voids the null. Any future geometric conjecture routed through this harness
must declare which of P1–P3 it occupies.
