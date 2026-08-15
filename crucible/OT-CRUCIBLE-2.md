# The Second Crucible — Observation Theory v0.2 under fire

**Sealed 2026-08-15, before any test runs. This document is both the
v0.2 freeze and the campaign seal, on the v0.1 protocol
(`OT-CRUCIBLE.md`): claims and kill conditions frozen here; each test's
instrument appendix committed before that test runs, narrowing only;
failed bars stand as written.**

## The freeze

P1–P5 as revised are frozen at readscope:

- commit `8bebe5eaa0ba5cbca6ad3c51b09b556588d68cdf`
- sha256 of `PRINCIPLES.md` at that commit:
  `40a7a5062a889a87ce8c959f281968ab5adb9594e4416bdaed701b3499ed3a0f`

No sixth principle and no edit to any principle statement until this
campaign's verdict; later commits may touch only non-principle framing,
checked at verdict by `git diff 8bebe5e..verdict -- PRINCIPLES.md`.

## The tests — the five v0.2 owed predictions, one each

| test | principle | prospective claim (frozen) | kill condition (frozen) |
|---|---|---|---|
| OT-12 | P5 (revised) | **The two floor curves.** In a consumer family with output quantized to g levels, the informative fraction of codec comparisons decays as g falls while accuracy *on informative pairs* stays at ceiling, at every g | accuracy on informative pairs sags below ceiling while informative pairs remain in meaningful number — the floor law dies exactly where the monotone law died before it |
| OT-10 | P3 | **The noisy cliff.** With iid noise of scale σ on each scalar observation, identification at k ≥ d floors at an error derived from σ and the spectrum (stated and proved before measurement), while the cliff's *location* does not move | the cliff location shifts with σ, or the measured floor deviates from the derivation beyond its stated tolerance, or the bound cannot be proved in the declared model |
| OT-8 | P1 | **Composition.** For weighted ensembles of real attention heads reading one KV stream, `sign(Σᵢ wᵢ tr(P̂ᵢ(Σ_A−Σ_B)))` from component probes alone predicts the measured ensemble codec preference — no probe of the ensemble, no refit | component-trace prediction fails its bar on real ensembles, or succeeds only after any ensemble-level fitting |
| OT-9 | P2 | **Forward transfer.** The activation-measure operator is predicted from a synthetic-measure probe plus the OT-2 alignment functional, beating the uncorrected synthetic probe on real heads | the corrected prediction is no closer to the direct activation-measure probe than the uncorrected one — the law reads backward but not forward |
| OT-11 | P4 (revised) | **Feedback-free staleness.** In streaming retrieval (no autoregression, so the severing control passes by construction), an index quantized against the day-0 query operator degrades in proportion to measured `d(P_C(t₀), P_C(t))` across drift strata, and re-allocation at the drift-derived cadence removes the excess | damage uncorrelated with measured drift across strata, or the derived-cadence re-allocation fails to remove its bar's share of the excess — the revised P4 falls in the very setting chosen to be fair to it |

## Run order, and why

**OT-12 → OT-10 → OT-8 → OT-9 → OT-11.**
The revised principles' tests bracket the campaign: P5's floor curves
first (cheapest, and v0.2's most direct self-test), the theorem work
early (OT-10 gates on its proof), the two real-head tests in the
middle on already-extracted data, and P4's staleness system last
because its drift strata need the most design care. Every test is
CPU-runnable on data already in the repos (armH head cells, the OT-6
embedding corpus) — no GPU dependency this campaign.

## Graduation rule (binding, declared before any test runs)

**Observation Theory v1.0** may be declared if and only if:

- **H1.** At least **4 of 5** tests survive their sealed bars.
- **H2.** **Both revision tests pass** — OT-11 and OT-12. A revised
  principle that fails the prediction written into its own revision is
  refuted, not revisable-again on this arc; the campaign closes without
  graduation regardless of the other three.
- **H3.** The freeze check passes (zero principle-statement edits since
  `8bebe5e`).

If the rule is not met, the campaign closes with a recorded verdict and
the same discipline as before: revision only after closure. There is no
third revision of a principle inside this program without a recorded
argument that the *program*, not the principle, is what failed.

## Instrument-appendix protocol (inherited, with the earned lessons)

Appendices before runs; manipulation checks on every knob (OT-5's
lesson); recovery bars conditioned on the target being genuinely hidden
(OT-3's); integer/quantized quantities graded on exactness under the
invariance group with continuous parents carrying fragility (OT-7's);
constructed consumers verified to realize the operator the prediction
is about (OT-1's); declared final-revision limits per test. Ledger rows
OT-8…OT-12 in `claims/LEDGER.md` as they resolve.
