# GO-P-2026-001 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-kv-keys.json`](../results/GO2-kv-keys.json).
**Registered verdict: MISS (2 of 4 bars failed) → `GO2_supported: false`.**
Reported as-is; the design was registered before this run, so it is not
retro-fitted to pass.

## What happened, per registered bar

| bar (registered) | result | pass? |
|---|---|:--:|
| anti-probe gap: KL(c)/KL(a) ≥ 5 | **21.3×** | ✅ |
| ordering a ≻ b ≻ c (12/12 seeds) | **1/12** (actual: b < a < d ≪ c) | ❌ |
| recon-optimal ≥10% worse: KL(b)/KL(a) ≥ 1.10 | **0.77** (b is *better*) | ❌ |
| tangential dominates: ΔpartialR² ≥ 0.10 | **−0.005** (recon predicts as well) | ❌ |

Median softmax-KL: b_lloyd 0.039 < a_asym_nf4 0.051 < d_uniform 0.070 ≪
c_polar 1.076. Median relative reconstruction: b 0.058 < a 0.094 < d 0.114 <
c 0.443.

## Diagnosis (honest)

1. **The strong GO-2 signal holds:** the anti-probe (PolarQuant — keeps
   norm/direction, discards per-channel scale) is **21× worse** downstream while
   its reconstruction error (0.44) is only ~5× the invariant arm's. Reconstruction
   badly **under-predicts** the wrong-quotient failure. That is the load-bearing
   claim, and it is confirmed.

2. **The `a ≻ b` miss is a matched-bits violation — one the protocol's own §3.5
   audit is designed to catch, and this test failed to enforce.** The
   reconstruction-optimal arm (per-block Lloyd-Max) stores an **uncounted per-block
   codebook** — `(H, D, 16)` fp32 levels ≈ 64 KB against 256 KB of 4-bit indices,
   i.e. ~+25 % → arm b runs at ~5 effective bits, not 4. asym-NF4 stores only
   compact per-channel scalars. So arm b was **over budget**; the comparison was
   never matched-bits. This does not confirm *or* cleanly refute GO-2 — it refutes
   **this test**.

3. **The regression is outlier-dominated.** With the anti-probe included, both
   tangential and reconstruction distortion capture the same c-vs-rest split, so
   neither dominates (both partial-R² ≈ 0.005–0.01). The discriminating question —
   *does reconstruction under-predict specifically the anti-probe's failure* — is
   answered "yes" by the raw numbers (point 1) but is not what the
   variance-explained regression measures.

## Ledger disposition & next step

Enters the ledger as a **miss** (§3.4). It neither establishes nor cleanly
refutes GO-2; it refutes the registered *test design* and yields two concrete
lessons. The corrected experiment must be **newly registered** (no post-hoc
edits to GO-P-2026-001):

- **GO-P-2026-002 (to register):** (a) a bit-matched reconstruction-optimal arm —
  either a **fixed shared codebook** fit once (no per-block level table) or
  explicit codebook-bit accounting enforced by the matched-bits audit; (b) a
  discriminating statistic for GO-2 — e.g. regress the **residual** of
  softmax-KL after reconstruction on the tangential distortion, or test whether
  reconstruction alone mis-orders the anti-probe — rather than a variance metric
  an outlier dominates.

The first registered book experiment missing, transparently, is the protocol
working: the ledger shows what the run showed, not what we hoped.
