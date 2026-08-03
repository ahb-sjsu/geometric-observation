# GO-P-2026-043 — post-run notes (unblinded 2026-08-02)

Result: [`../results/GO-landauer-operational.json`](../results/GO-landauer-operational.json).
Governed full run on Atlas (single process, seed 20260802), sealed pre-run at
`7f688c6` after one logged calibration pilot (pilot seed = SEED+1, n≤24, T=60;
pilot numbers are not evidence).

## What the experiment does

The paper's Theorem 1 says a stored lossy description carries **two different
resource coordinates**: the description rate $I(X;\hat X)$ a consumer needs, and
the conditional Landauer content $I(X;\hat X\mid S)$ a reset mechanism holding
side information $S$ must irreversibly clear. This run makes the separation
operational at finite blocklength, on the paper's own Prop-2 source
($X=(A,B)$ fair bits, $S=A$, target channel BSC(0.08)×BSC(0.32)):

1. build a real random codebook at rate $R+0.03$, encode source blocks by
   ML/typicality scoring — the stored index $M$ **is** the description;
2. random-bin $M$ at bin rate $r_b$ and try to recover it from
   $(\mathrm{bin}, S^n)$ alone — the Wyner–Ziv binning step of the paper's
   achievability proof, run as an actual decoder;
3. controls: a no-side-information decoder at the same bin rate (the gap must
   be bought by $S$, not by binning), a below-content bin rate (must fail),
   and a channel-realization window.

## Per gated bar

**Registered verdict: PASS — `GOL_operational_supported: true`, 7/7 gates.**

| gated bar | registered | result | pass? |
|---|---|---|:--:|
| A1 separation decodes (err @ r_b=0.26) | ≤0.05 @ n=32, ≤0.12 @ n=28, trend | **0.03** @ n=32, **0.05** @ n=28; trend 0.13→0.03 | ✅ |
| A2 bin rate ≤ 0.45·R̂ | 0.26 ≤ 0.45·R̂(n=32) | R̂ = **0.6715** → 0.26 = **0.39·R̂** (≥2.6× separation) | ✅ |
| A3 below-content binning fails (r_b=0.03) | ≥0.30 all n≥16, ≥0.40 @ n=32 | 0.445→**0.67** @ n=32, *rising* with n | ✅ |
| A4 no-SI control fails @ r_b=0.26 | ≥0.90 all n≥20 | **1.00 at every n and every r_b** | ✅ |
| A5 channel realized | \|D̂−0.20\|≤0.04, L̂∈[0.03,0.14], R̂∈[0.62,0.78] | D̂=**0.213**, L̂=**0.069**, R̂=**0.672** | ✅ |
| B sanity (no negative endpoint gaps) | 0 beyond 2e-3 | **0** / 250 sources | ✅ |
| C staleness identity | ≤5e-3 / ≤5e-3 / monotone / ≤1e-2 | **1.5e-3 / 1.2e-6 / True / 1.5e-3** | ✅ |

The full error curve at n=32 (bin rate → error): 0.03→0.67, 0.08→0.43,
0.13→0.15, 0.19→0.06, 0.26→0.03, 0.35→0.01, 0.50→0.00. The decoding
threshold sits between r_b = 0.13 and 0.19 — bracketing the theory value
codebook-rate − Î(X̂;S) ≈ 0.72 − 0.60 ≈ 0.12 from above, at ~1/4 of the
description rate. The empirical conditional content L̂ = 0.069 lower-bounds
where any binning can succeed, and r_b = 0.03 < L̂ indeed fails increasingly
with n (0.445 → 0.67): both sides of Theorem 1, operationally.

## Reading

The same stored index that costs ~0.65–0.69 bits/symbol to *describe* is
recoverable — hence reversibly dischargeable at reset — from retained side
information at a bin rate a small fraction of that. Below the conditional
content the binning fails, and without $S$ it fails at any of these rates:
the saving is the side information's, exactly as $H(M\mid S^n)$ accounting
says. This is the operational, finite-$n$ face of the paper's central claim
that description rate and reset work are different resources.

Part B (genericity sweep over random discrete sources) is a **measurement**,
not a paper claim: the paper exhibits the rate–work separation (Prop 2); the
sweep reports how often random small-alphabet sources show a nontrivial
frontier at matched distortion. Result (250 sources): **29.6%** show both
endpoint gaps >0.01 bits, 2.8% >0.05 bits; median work-gap 0.0038 bits, p90
0.028, max 0.067; zero negative gaps. The separation is real but modest in
unstructured random ensembles — structured side information (as in Prop 2,
where $S$ reveals a coordinate; L-gap there is 0.88 bits at matched rate) is
what makes it large. Useful scoping fact for the paper's discussion, not a
weakness of the theorem.

## Caveats

- One codebook draw per $n$ (few-cluster caveat registered); trial-level
  randomness dominates at these sizes but a multi-codebook replication is the
  natural hardening.
- The encoder is min-weighted-distortion (practical), not strict typicality:
  it realizes a *more asymmetric* channel than the target (registered window
  covers this); all information quantities are recomputed from the empirical
  per-letter channel.
- Ideal-reset accounting only: this demonstrates the *information* coordinate
  $H(M\mid S^n)$ is operationally attainable/blocked at the registered rates;
  no physical work is measured (the paper's own scope, §II Remark 1).

## Multi-codebook replication (GO-P-2026-045, 2026-08-03)

The registered few-cluster caveat (one codebook per n) is resolved:
`experiments/landauer_multicodebook.py` reran the sealed Part-A design with
five independent codebooks per blocklength under a fresh seed (20260804).
**PASS 6/6 gated.** Per codebook at n=32: separation error at r_b=0.26 =
{0.01, 0.03, 0.02, 0.04, 0.03} (spread 0.03 vs the 0.10 stability bar);
below-content error at r_b=0.03 = {0.63, 0.72, 0.75, 0.64, 0.69}; the no-SI
control errs 1.00 everywhere; realized channels R^ in [0.658, 0.675], L^ in
[0.075, 0.089], D^ in [0.207, 0.213] — all inside the sealed windows. The
effect is a property of the random-coding ensemble, not of a codebook draw.
Result: [`../results/GO-landauer-multicodebook.json`](../results/GO-landauer-multicodebook.json).
Scope unchanged: same synthetic source, so GO-7 remains `[demonstrated]`;
a cross-source/domain run would be the `[replicated]` bar.
