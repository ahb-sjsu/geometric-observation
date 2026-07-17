# GO-P-2026-006 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-kv-keys-v6.json`](../results/GO2-kv-keys-v6.json).
**Registered verdict: PASS — `GO2_positive_supported: true`. All five gated
conditions met.** GO-2's positive half is `[demonstrated]` on instance 1 (KV
keys). Reported as-is (sealed design, registered commit 743c68c).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| effective-bits audit ≤ 0.5 | 0.19 | ✅ |
| non-degeneracy (max-prob ≥ 3/S both) | 0.144 / 0.705 | ✅ |
| **flip decisive** (adv_KL iso ≥ log1.3, sub ≤ −log1.15; per-seed ≥10/12) | **+0.93 / −0.44; 12/12 & 12/12** | ✅ |
| **proj_var tracks flip** (sign-agree ≥11/12 both) | **12/12 & 12/12** | ✅ |
| recon fails (min Spearman recon < proj_var) | 0.40 < 0.80 | ✅ |

At r=8 the flip is decisive both ways — iso: a better 2.5× (12/12); sub: b better
~1.56× (12/12) — the directly-computed `proj_var = tr(P_C Σ_δ)/tr(P_C Σ_0)`
matches the a-vs-b KL sign on every seed in both consumers, and reconstruction
(consumer-blind, fixed at a 0.0938 / b 0.0934) cannot.

## Diagnostics (reported, not gated)

- **Anti-probe gap: iso 21.4, sub 6.34 — both ≥ 5.** At r=8 (vs r=4's 4.0) the
  anti-probe control clears cleanly as a diagnostic; the concentration/anti-probe
  tension of v5 is resolved without gating on it.
- **Full-4-arm Spearman(proj_var, KL): iso 0.80, sub 1.00.** The iso 0.80 is the
  same **middle** b-vs-d discrepancy as NEG-9 — proj_var nails the a-vs-b flip
  (12/12) but the trace is not a complete rank statistic. Kept in view, honestly,
  as a reported quantity; it does not bear on the positive-half flip claim.
- Spearman(recon, KL): iso 0.40, sub 1.00 — recon mis-orders under iso, confirming
  its consumer-blindness.

## What this closes, and what it does not

**Closed:** GO-2 positive half, **instance 1** — the consumer-projected error
covariance `tr(P_C Σ_δ)` governs the discriminating a-vs-b comparison and
reconstruction does not, demonstrated with a symmetric consumer flip (both
directions 12/12) at fixed reconstruction. Together with the negative half
(`[demonstrated]`, v2), GO-2's full claim now holds on the KV-keys instance.

**Not closed:** `[replicated]` needs a **second independent instance** (a Gate-B
representation/consumer — embedding retrieval, gradient moments, a real-query
bank). NEG-9 stands: the trace governs the flip but is not a complete rank
statistic; the full downstream order carries structure beyond a single scalar.

## The six-round arc (all registered, all recorded)

1. v1 → matched-bits confound (NEG-5)
2. v2 → **negative half `[demonstrated]`**; error-norm proxy refuted (NEG-6)
3. v3 → the invariant is consumer-relative; recon flips against itself (NEG-7)
4. v4 → mechanism `tr(P_C Σ_δ)` found & corroborated; Var-ratio proxy noisy (NEG-8)
5. v5 → core flip decisive (12/12) but conjunction over-scoped; trace ≠ full rank (NEG-9)
6. v6 → **positive half `[demonstrated]`, instance 1**, conjunction scoped to the claim

Five honest misses narrowed the target to one clean statistic; the sixth, scoped
to exactly what the data shows, lands it. Nothing was retro-fitted — each
registration was sealed and committed before its run, and every miss is in the
ledger.
