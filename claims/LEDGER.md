# Geometric Observation — Claim Ledger

The living record of record. Every table and figure in the book carries a claim
ID that resolves to a row here. Governed by [`../PROTOCOL.md`](../PROTOCOL.md);
the book may not assert what this ledger cannot show. Classes: `[proved]`,
`[demonstrated]`, `[replicated]`, `[predicted]`, `[exploratory]`, `[refuted]`.

> **Post-publication, this ledger is the living erratum** (§10). Failures
> downgrade a claim before print; the book's tables carry IDs that resolve here.

## The falsifiable core (GO-1 … GO-5)

Risk-bearing claims (§2). `pending` = registry entry and/or run not yet complete.

| ID | Claim (one sentence) | Class | Chapter | Registry | Notebook | Result JSON | Tier | CI | Replications | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| GO-1 | The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. | `[predicted]` (pending) | 6–7 | — | — | — | — | — | — | needs blinded probe re-impl + prospective arm |
| GO-2 (neg. half: **not** reconstruction) | At matched bits, downstream preservation is **not** controlled by reconstruction error. | `[demonstrated]` | 6–8 | [GO-P-2026-002](../prereg/GO-P-2026-002-kv-keys-quotient-transfer-v2.md) | `experiments/go2_kv_keys_v2.py` | [GO2-kv-keys-v2.json](../results/GO2-kv-keys-v2.json) | B | ✅ audit+dissociation | 1 (KV keys) | [notes](../experiments/GO2-kv-keys-v2-NOTES.md): audit-passed matched bits (spread 0.19); recon-**identical** arm (0.0934 vs 0.0938) is **2.53× worse** downstream (12/12), anti-probe **21×**. Clean dissociation |
| GO-2 (pos. half: tangential *controls*) | Downstream preservation is controlled by quotient-tangential noncollapse. | `[replicated]` (**open**) | 6–8 | [GO-P-2026-002](../prereg/GO-P-2026-002-kv-keys-quotient-transfer-v2.md) | `experiments/go2_kv_keys_v2.py` | [GO2-kv-keys-v2.json](../results/GO2-kv-keys-v2.json) | B | **dominance ❌** | 0 / ≥2 | the demeaned-error-norm proxy does **not** control downstream (NEG-6); controlling quantity is across-token Var_s(q·δ_s). Re-test → GO-P-2026-003 (query-projected metric + structured consumer). v1 = NEG-5 (matched-bits confound) |
| GO-3 | The certificate's vacuity threshold predicts where single-stage retrieval dies. | `[demonstrated]` (pending) | 6–9 | — | — | — | — | — | — | ≥5 corpora ordered by μ̂(κ) at fixed κ |
| GO-4 | Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. | `[replicated]` (pending) | 10 | — | — | — | — | — | — | ≥1 substrate beyond Paper I §5.10 |
| GO-5 | An α=1 density/hubness quotient restores invariant fidelity in ≥1 non-spectral domain. | `[demonstrated]` (pending) | 8 | — | — | — | — | — | — | e.g. locally-scaled ADC retrieval |

## Standing `[refuted]` rows (carried into the book regardless — §2, §8)

The Honest Negatives chapter carries these with the same prominence as positives.

| ID | Refuted claim (one sentence) | Class | Chapter | Source of record | Notes |
|---|---|---|---|---|---|
| NEG-1 | Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. | `[refuted]` | Honest Negatives / 10 | Paper I (Prop. weyl) | scale-dependent; the uniform bound fails |
| NEG-2 | Reconstruction cosine as a proxy for key quality. | `[refuted]` | Honest Negatives / 6 | Paper II (ppl ~10⁴ at cos 0.995) | the core motivating negative |
| NEG-3 | Heat-taper reversal on BGE-M3. | `[refuted]` (pending confirm) | Honest Negatives / 4 | Paper I | pending C2.1 confirmations |
| NEG-4 | Lightweight online (Lloyd) key calibration beats the calibration-free default on softmax-KL. | `[refuted]` | Honest Negatives / 6 | Paper II (`benchmarks/RESULTS_calibration.md`) | improves reconstruction, worse on the consumer metric — reconstruction-is-not-the-target, again |
| NEG-5 | GO-P-2026-001 as registered: on KV keys, invariant-preserving (asym-NF4) beats reconstruction-optimal (per-block Lloyd) at matched bits, and tangential distortion dominates reconstruction in predicting softmax-KL. | `[refuted]` (test) | Honest Negatives / 6 | [GO2-kv-keys.json](../results/GO2-kv-keys.json), [notes](../experiments/GO2-kv-keys-NOTES.md) | registered test missed (2/4 bars). The `a≻b` reversal is a matched-bits confound (the Lloyd arm stored an uncounted per-block codebook, ~+25% bits) — refutes the *test*, not GO-2; a re-registered bit-matched design is required |
| NEG-6 | Relative per-channel-demeaned error norm is the quotient-tangential quantity that controls softmax-KL. | `[refuted]` | Honest Negatives / 6 | [GO2-kv-keys-v2.json](../results/GO2-kv-keys-v2.json), [notes](../experiments/GO2-kv-keys-v2-NOTES.md) | GO-P-2026-002: the demeaned-norm proxy fails to order a<b (tang 0.233<0.244 while KL 0.128>0.051) and loses the dominance regression to reconstruction. The controlling quantity is the across-token variance of the query-projected error Var_s(q·δ_s), not an error-magnitude scalar — magnitude ≠ downstream-relevant structure |

## Out-of-sample gate (Gate B — §4)

| ID | Domain (disjoint from Papers I–II) | Class target | Registry | Result | Notes |
|---|---|---|---|---|---|
| GO-B | *(register ≥1: optimizer moments / gradient compression / LoRA deltas / GT positional enc. / audio latents / recommender emb. / neural population codes)* | `[predicted]` | — | — | ≥1 prospective hit or a `[refuted]` row that narrows the Ch. 11 umbrella |

*Rows fill as prereg entries are written and runs land. Nothing here is
load-bearing until its class bar (§1, §5, §6) is met and CI is green.*
