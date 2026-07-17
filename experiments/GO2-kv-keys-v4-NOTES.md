# GO-P-2026-004 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-kv-keys-v4.json`](../results/GO2-kv-keys-v4.json).
**Registered verdict: MISS (`GO2_positive_supported: false`) — 5/7 bars pass; the
mechanism is directly confirmed, two *proxy-precision* bars miss.** Reported
as-is (sealed design, registered commit bde4172).

## Per registered bar

| bar | result | pass? |
|---|---|:--:|
| effective-bits audit ≤ 0.5 | 0.19 | ✅ |
| non-degeneracy (max-prob ≥ 3/S both) | 0.144 / 0.472 | ✅ |
| anti-probe gap ≥ 5 both consumers | 21.4 / 8.7 | ✅ |
| **flip**: adv_KL(iso) > 0 ∧ adv_KL(sub) < 0 | **+0.93 / −0.07** | ✅ |
| recon fails: min Spearman(recon) < min Spearman(tang) | 0.40 < 0.80 | ✅ |
| tang tracks flip (sign-agree ≥10/12 both) | 12/12 iso, **9/12 sub** | ❌ |
| tang ranks (Spearman ≥ 0.9 both) | **0.80 iso**, 1.00 sub | ❌ |

## What this establishes (strong)

**The flip, in a clean non-degenerate regime.** Softmax max-prob 0.14 (iso) /
0.47 (sub) — nowhere near uniform. At **fixed reconstruction** (a 0.0938,
b 0.0934):

| consumer | KL(a) | KL(b) | better | sign-agree |
|---|---|---|---|---|
| iso | 0.046 | 0.116 | **a** (2.5×) | 12/12 |
| sub | 0.0351 | 0.0319 | **b** | — |

Reconstruction is a single consumer-blind number and provably cannot track this:
Spearman(recon, KL) = 0.40 (iso) / 0.80 (sub), always below tang's. The negative
half of GO-2 — reconstruction does not control downstream — is now airtight, with
a crisp same-reconstruction consumer flip.

**The mechanism, confirmed directly.** The un-gated covariance-projection
corroboration is decisive: arm a places **40.6%** of its across-token error
covariance in the consumer's read subspace (top-16), arm b only **12.2%** — a
3.3× concentration that exactly predicts a's disadvantage under the subspace
consumer. This is `tr(P_C Σ_δ)` — the governing quantity the prereg named — read
off directly, and it separates a from b far more cleanly than the gated rank
statistics did.

## What misses, and why (proxy precision, not mechanism)

`tang_qproj = mean Var_s(q·δ)/Var_s(q·k0)` is a **noisy linear estimator** of
`tr(P_C Σ_δ)/tr(P_C Σ_0)`:
- **Spearman 0.80 under iso** — it misorders the *middle* pair (b vs d), not a,b.
  The a-vs-b call (the flip pair) is correct in both consumers.
- **sign-agreement 9/12 under sub** — the sub-flip is only ~9% at the median in
  the sharpened regime, so per-seed KL sign is noisy; tang (adv_tang −1.07, a
  much larger signal) says b-better every seed, disagreeing on the 3 seeds where
  KL narrowly lands a-better. tang *over-scales* the sub-flip (linear proxy vs
  nonlinear KL).

Both are estimator issues. The mechanism (`tr(P_C Σ_δ)` governs, recon does not)
is confirmed by the flip + the projection fractions.

## Ledger disposition & next step

- GO-2 **negative half**: further strengthened (clean-regime consumer flip at
  fixed reconstruction). Stays `[demonstrated]`.
- GO-2 **positive half**: mechanism strongly corroborated (`tr(P_C Σ_δ)`:
  proj-frac 0.406 vs 0.122; flip confirmed; recon can't track) but the registered
  proxy-conjunction misses on two precision bars → still not `[demonstrated]` by
  the registered test. NEG-8: the Var-ratio `tang_qproj` is not a ≥0.9-Spearman
  rank proxy under all consumers (0.80 iso); the **direct** covariance projection
  is the better statistic.
- **GO-P-2026-005 (to register):** gate on `tr(P_C Σ_δ)` (the projection fraction)
  **directly** — it cleanly separates the arms and matches the flip — and
  strengthen the subspace consumer (smaller r, or a more concentrated read
  subspace) so the sub-flip is decisive rather than 9%. Keep the audit,
  non-degeneracy, and flip/recon-fails structure.

Four registered misses; the mechanism is now in hand. v5 is a statistic swap, not
a new idea — the map has a road to the summit.
