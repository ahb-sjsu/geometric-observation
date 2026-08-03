# GO-P-2026-043 — Operational rate–work separation: finite-n conditional reset by random binning

Registers the **Tier-B operational run** for the consumer-relative Landauer paper
([`paper/consumer-relative-landauer.pdf`](../paper/consumer-relative-landauer.pdf), Thm 1 +
Prop 2): a finite-blocklength Monte Carlo in which the *same stored index* is (i) a lossy
description serving a consumer at ~0.7 bits/symbol and (ii) a reset residual recoverable
from retained side information at a bin rate near its conditional Landauer content
L = I(X;X̂|S) ≪ R — the paper's two-resource separation made operational, with a
no-side-information control showing the gap is bought by S, not by binning. Plus a
genericity sweep of frontier-endpoint gaps over random sources (measurement, sanity-gated)
and a staleness Monte Carlo (Prop 4). Governs `experiments/landauer_operational.py`;
result `results/GO-landauer-operational.json`.

**Design (Part A).** Prop-2 source X=(A,B) i.i.d. fair bits, reset side information S=A.
Target test channel BSC(0.08)×BSC(0.32): analytic R=0.6934, L=0.0956, I(X̂;S)=0.5978
bits/symbol. One random uniform codebook of 2^⌈n(R+0.03)⌉ codewords per n; ML/typicality
encoding (weighted Hamming, weights log((1−Dᵢ)/Dᵢ)); the stored index M is random-binned
at bin rate r_b and recovered from (bin, S^n) by in-bin ML (min Hamming(cw_A, a^n)).
n ∈ {12,16,20,24,28,32}, trials {200,200,200,200,120,100}, r_b ∈
{0.03,0.08,0.13,0.19,0.26,0.35,0.50}. Theory predicts a decoding threshold near
codebook-rate − I(X̂;S) ≈ 0.13 ≪ R̂: the residual uncertainty a reset mechanism holding
S must irreversibly clear is a small fraction of the description rate.

**Pilot (logged, per PROTOCOL §4 synthetic-pilot rule).** One calibration pilot was run
2026-08-02 on Atlas (`--pilot`: n≤24, T=60, pilot seed = SEED+1, distinct from the
governed seed) to center the bars; its numbers are not evidence and are superseded by the
full run. Pilot findings folded into the bars below: min-distortion encoding realizes a
*more* asymmetric channel than the target (L̂ ≈ 0.05, D̂ ≈ 0.22, R̂ rising to ~0.66 by
n=24), so the channel-realization window is set to L̂ ∈ [0.03,0.14], |D̂−0.20| ≤ 0.04;
the low-rate converse error sits near 0.5, so its floor is 0.30/0.40 not 0.60; the
separation factor gate uses 0.45·R̂. One pilot artifact fixed pre-seal: endpoint-gap
sign in Part B requires both bisections to hit the common distortion (guard added,
skip-if-unconverged, negativity gated beyond 2e-3 numerical slack).

```yaml
id: GO-P-2026-043
date: 2026-08-02
retrospective: false
kind: operational Monte Carlo (Tier B, Atlas CPU, single process)
claim: "The conditional Landauer content of a stored lossy description is operationally separable from its description rate: random binning + retained side information recovers the full index at a bin rate far below R, a no-SI control fails at the same bin rate, and below-threshold binning fails."
harness: experiments/landauer_operational.py   # numpy only; governed seed 20260802; --pilot used only for calibration
prediction:
  A1_separation_decodes: at r_b = 0.26, error <= 0.05 at n=32 and <= 0.12 at n=28,
    with mean error over the larger half of the n-grid <= mean over the smaller half
  A2_bin_rate_below_045R: 0.26 <= 0.45 * R_hat(n=32) — >= 2.2x operational separation
    between description rate and decodable reset-residual rate
  A3_converse_low_rb_fails: at r_b = 0.03 (below L_hat), error >= 0.30 for every
    n >= 16 and >= 0.40 at n=32 — below-content binning must not decode reliably
  A4_side_info_specific: the no-side-information control decoder errs >= 0.90 at
    r_b = 0.26 for all n >= 20 — the separation is bought by S
  A5_channel_realized: |D_hat - 0.20| <= 0.04, L_hat in [0.03, 0.14],
    R_hat in [0.62, 0.78] at n=32
  B_sanity: over ~250 random sources, endpoint gaps (L(min-R) - L(min-L)) and
    (R(min-L) - R(min-R)) never negative beyond 2e-3; separation-fraction and gap
    distribution REPORTED as measurement (the paper claims existence, not genericity)
  C_staleness: plug-in H(X0|Xt) from 1e6 simulated chains matches h2(q_t) to 5e-3,
    complement I+L = 1 bit to 5e-3, monotone; 4-state chain plug-in vs exact <= 1e-2
falsification: A1/A2 failing refutes the operational reading of Thm 1 achievability at
  these n; A3 failing (reliable decode below content) would contradict the converse
  accounting; A4 failing means the effect is a binning artifact, not side information;
  A5 failing voids the run (channel not realized; redesign, log, re-register).
design:
  n: [12, 16, 20, 24, 28, 32]
  trials: [200, 200, 200, 200, 120, 100]
  stopping: fixed-n, single governed run, seed 20260802
  clusters: independent trials within one codebook draw per n (few-codebook caveat:
    one codebook per n; codeword-level randomness dominates at these sizes)
controls: [no-side-information decoder, below-content bin rate, channel-realization window]
amendments: []
hash: sha256:d0a6985e51ab2c21882180f3ee2a8fdc3cce0639db9254354278063a7fa99ee9
```

## Falsification
Any A-gate miss is reported as a `[refuted]`/miss row at full prominence per PROTOCOL
Rule 1.2; B is sanity-gated measurement; C nets Prop 4. The registered verdict is the
committed JSON's `verdict` dict; CI re-checks self-consistency (tamper check) but cannot
re-run Tier B.
