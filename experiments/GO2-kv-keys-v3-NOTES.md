# GO-P-2026-003 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-kv-keys-v3.json`](../results/GO2-kv-keys-v3.json).
**Registered verdict: MISS (`GO2_positive_supported: false`) — and the miss is
the discovery.** Reported as-is (sealed design, registered commit 07d0201).

## Per registered bar

| bar (registered) | result | pass? |
|---|---|:--:|
| effective-bits audit spread ≤ 0.5 | 0.19 | ✅ |
| anti-probe gap KL(c)/KL(a) ≥ 5 | 6.69× | ✅ |
| ordering KL(a) < KL(b), ≥10/12 | **0/12** (b beats a) | ❌ |
| dominance partialR²(tang_qproj) − partialR²(recon) ≥ 0.10 | +0.007 | ❌ |
| specificity gap_softmax ≥1.5 & gap_linear ≤1.25 | 0.37 / 0.33 | ❌ |

## The discovery: the ranking is consumer-relative at fixed reconstruction

I registered `a < b` (per-channel "invariant-preserving" beats per-token
"invariant-blind"). Under the **structured** consumer (unit queries in the top-16
singular subspace of each head's demeaned keys) the opposite holds — **b beats a
on every seed** (KL 0.0006 vs 0.0016; gap 0.37). The isotropic cross-check gives
the other direction (gap_iso 1.11, a better). So, with **reconstruction held
fixed** (recon(a)=0.0938, recon(b)=0.0934 in *both* consumers):

| consumer | better arm | gap KL(b)/KL(a) |
|---|---|---|
| isotropic queries | a (per-channel) | 1.11 |
| top-16 subspace queries | **b (per-token)** | **0.37** |

**Same compressors, same reconstruction, opposite downstream ranking — purely
from changing the consumer's read directions.** This is the sharpest possible
statement of GO-2's negative half and a direct instance of GO-1: *reconstruction
cannot control downstream* (it is constant while the ranking flips), and
**"invariant-preserving" is not a property of the compressor — it is defined by
the consumer.** My arm *labels* (a = invariant-preserving) were consumer-naive;
that labeling is refuted → **NEG-7**.

Why b wins under the subspace consumer: the top singular directions weight
high-variance (high per-channel-scale) channels. Per-channel arm a spends a
coarse step on exactly those high-scale channels, so its error is *aligned* with
the directions the consumer reads. Per-token arm b spreads error more evenly in
channel space, less aligned with the top directions → smaller logit kick there.

## tang_qproj is the right quantity — the regression statistic was not

Under this consumer, `tang_qproj = mean_{q,h} Var_s(q·δ)/Var_s(q·k0)` orders the
arms **b < a < d < c — exactly the softmax-KL order** — and separates a from b by
2.9×, matching KL's 2.7×, precisely where reconstruction is blind (0.0934 ≈
0.0938). The *linear partial-R²* dominance bar still missed (margin 0.007) because
(i) within-arm across-seed scatter is large relative to between-arm means and (ii)
the anti-probe is a nonlinear outlier a z-score linear fit handles poorly — so a
tiny R² despite a **perfect rank match**. The instrument, not the quantity, is
wrong: use a **rank/separation** test, not linear partial-R².

## Ledger disposition & next step

- GO-2 **negative half** strengthened: same-reconstruction, cross-consumer rank
  flip. (Already `[demonstrated]` from v2; this is corroborating.)
- GO-2 **positive half** still **open**: tang_qproj tracks the KL ranking and
  a-vs-b separation, but the registered regression bar missed in this
  near-uniform-softmax regime; not yet `[demonstrated]`.
- Refuted: consumer-naive arm labeling (**NEG-7**).
- **GO-P-2026-004 (to register):** (i) register the **flip itself** — tang_qproj's
  arm-ranking tracks softmax-KL's ranking under *both* consumers (Spearman ≈ 1)
  while reconstruction's does not; (ii) a **rank/separation** statistic
  (Spearman + a-vs-b separation ratio), not linear partial-R²; (iii) a
  non-degenerate softmax regime (scale the query norm so logits are O(1), not
  near-uniform). Keep the matched-bits audit and both consumers.

Three registered misses, three sharper coordinates: matched-bits (v1) → the
dissociation is real (v2) → the invariant is consumer-relative and reconstruction
flips against itself (v3). The map is filling in.
