# GO-P-2026-007 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-embed-retrieval.json`](../results/GO2-embed-retrieval.json).
**Registered verdict: MISS — `GO2_mechanism_replicates: false`. A prospective
prediction that missed, and the miss pins down the mechanism's precondition.**
Reported as-is (sealed, PROSPECTIVE, registered commit 1899d27).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| effective-bits audit ≤ 0.5 | 0.22 | ✅ |
| SNR (min-arm dO ≥ 10× floor) | 5.7e-3 vs 9.6e-7 | ✅ |
| **flip decisive** | **no flip: b better both consumers (0/12, 0/12)** | ❌ |
| proj_var tracks flip (sign-agree ≥11/12) | 12/12 both | ✅ |
| **recon fails** (min Spearman recon < proj_var) | 1.00 = 1.00 | ❌ |

## What actually happened — and why it's informative

There is **no consumer flip**: arm b (per-item whole-vector) beats arm a (per-dim
NF4) under **both** the isotropic and the subspace consumer (adv_dO −0.28 / −0.98).
The cause is visible in the fixed reconstruction column:

| arm | recon (rel ‖δ‖) | dO iso | dO sub |
|---|---|---|---|
| a per-dim | **0.1143** | 0.0321 | 0.0151 |
| b per-item | **0.0964** | 0.0246 | 0.0057 |

Unlike instance 1, where a and b were a near-perfect **reconstruction tie**
(0.0938 vs 0.0934) so the consumer decided the winner, here **b reconstructs
strictly better** and therefore **Pareto-dominates** — lower recon *and* lower
ranking distortion in every consumer. With one arm dominating, there is no
dissociation for the consumer to invert.

Consequently `recon_fails` is **false**: reconstruction points the right way in
both consumers (Spearman 1.0), so it is not falsified here. Note that `proj_var`
still tracks the ranking distortion **perfectly** (Spearman 1.0, sign 12/12 both)
— the mechanism (`tr(P_C Σ_δ)` governs dO) is **not contradicted**; it is simply
**indistinguishable from reconstruction** in the absence of a recon-tie.

## The precondition, now explicit (→ NEG-10)

**The reconstruction-blind flip is observable only when the compared arms are
reconstruction-matched.** When one compressor dominates on reconstruction (as b
does here), reconstruction and the consumer-projected covariance agree and no flip
appears. Instance 1's flip was possible *because* its a/b were a tie. This
prospective miss did not tune anything into passing — it revealed the regime the
phenomenon lives in.

## Ledger disposition & next step

- GO-2 `[replicated]`: **not achieved.** Instance 2 (retrieval) did not reproduce
  the *discriminating* flip → replications remain 1/≥2. The mechanism was not
  refuted (proj_var tracks dO 1.0) but was not distinguished from reconstruction.
  → **NEG-10** (prospective): the reconstruction-blind flip does not appear when
  the arms are not reconstruction-matched.
- Diagnostics: anti-probe gap 8.1 (iso) / 6.4 (sub) — the wrong-quotient control
  is catastrophic in retrieval too (a partial positive: the anti-probe half of the
  mechanism *does* transfer); top-10 overlap deficit shows the same b-dominates
  pattern.
- **GO-P-2026-008 (to register, prospective):** retrieval again, but with
  **reconstruction-matched arms** by construction (e.g. bit-allocate b down / a up,
  or pick two schemes tied on rel-‖δ‖ within a tolerance, audited) so the
  dissociation can manifest. Then test whether the flip + recon-blindness
  replicates *in the regime where it is observable*. This is a principled new
  hypothesis (the precondition NEG-10 just taught us), registered before running —
  not tuning-to-pass.

A prospective prediction missed, honestly, and bounded the claim: the flip is a
property of reconstruction-*matched* comparisons, not of every representation.
