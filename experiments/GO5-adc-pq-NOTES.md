# GO-P-2026-018 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO5-adc-pq.json`](../results/GO5-adc-pq.json).
**Registered verdict: MISS — `GO5_supported: false`. Third consistent GO-5 miss;
the substrate is now genuinely hubbed, so this is a real bound, not a bug.**
Reported as-is (sealed, registered commit 5ec52c5).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| baseline_hubness (skew(α=0) ≥ 0.5) | **2.45 / 2.87 / 2.34** (strongly hubbed) | ✅ |
| restoration (recall gain ≥ 0.02) | **−0.07** (recall *falls*) | ❌ |
| alpha1_optimal | α=0 is best | ❌ |
| hubness_reduced (skew ↓ 0→1) | skew *rises* 2.45→3.6→11.6 | ❌ |

Per-α (seed0): recall 0.341 / 0.315 / 0.269 / 0.193; hubness skew 2.45 / 2.67 / 3.60 / 11.56.

## The unifying diagnosis (across v1/v2/v3)

The α=1 density quotient `s_qj = W_qj / q_j^α` down-weights db points by their
density q_j. Three prospective misses — direct self-tuning affinity (v1), global
affinity on clustered density (v2), and ADC/PQ on real embeddings (v3) — all show
it **hurts** recall and **raises** hubness. The reason is now clear and it is *not*
a bug:

1. **The density-quotient only helps if density lives in the retrieval BASE.** In
   direct-distance and ADC retrieval, the base distance is *not* density-biased
   (ADC distance is a genuine per-vector distance, not a random-walk operator). So
   there is no density bias in the ranking for the quotient to remove — dividing by
   q_j^α just re-weights candidates and distorts the ranking.
2. **db density is entangled with the invariant in concentrated real data.**
   High-q db points (central, close to the reference bank) are *legitimately* close
   to many queries — they are true neighbors, not spurious hubs. Down-weighting
   them removes signal. And dividing by a heavy-tailed q amplifies the low-density
   tail into **anti-hubs**, so hubness skew *increases* (11.6 at α=1.5).

The α=1 = Laplace–Beltrami density cancellation is a property of the diffusion
**operator** (a random walk that lingers in dense regions), not of a direct
distance. GO-5's transfer to *direct / ADC* retrieval therefore does **not** hold —
and this is what all three runs, prospectively, show.

## Status: a bounded negative, and the one untested domain

- **Bounded negative (candidate NEG-11):** the α=1 density quotient does **not**
  restore invariant fidelity in *direct-distance / ADC* non-spectral retrieval — it
  hurts recall (density is not in the base and is entangled with the invariant).
  Three prospective misses, real hubness in v2/v3.
- **The theoretically-correct domain is untested:** diffusion / commute-distance
  retrieval, where the base *is* density-biased (the random walk) and computable
  without a full eigendecomposition ("non-spectral"). GO-5's α=1 should hold there;
  ADC (chosen for v3) was the wrong base by this diagnosis.
- GO-5 is the only core claim not yet demonstrated; GO-1…GO-4 (all four Observation-
  Theory faces) stand regardless.

Rather than keep hunting substrates until one passes (three misses is enough to
stop and think), the choice is: test the diffusion-distance domain (the one the
theory actually predicts), or record GO-5 as this bounded negative and let the
framework rest on the four demonstrated faces. Consulting before GO-P-2026-019.
