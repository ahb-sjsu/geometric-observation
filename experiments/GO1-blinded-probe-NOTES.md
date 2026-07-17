# GO-P-2026-011 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO1-blinded-probe.json`](../results/GO1-blinded-probe.json).
**Registered verdict: PASS — `GO1_supported: true`. All five gated conditions met,
PROSPECTIVE and BLINDED, first run.** GO-1 — the consumer's invariant/nuisance
split is identifiable ex ante from the consumer functional — is `[predicted]`.
Reported as-is (sealed, registered commit 73e03d3).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| subspace_recovery (median min-overlap ≥ 0.90) | **0.936** (chance 0.059) | ✅ |
| **blind_predicts_flip** (sign-agree ≥11/12 both; decisive) | −2.38 / +2.38; **12/12 & 12/12** | ✅ |
| recon_fails (min Spearman recon < projhat) | 0.40 < 1.00 | ✅ |
| matched_distortion (recon a≈b) | gap 0.0 | ✅ |
| snr_loser (loser dO ≥ 10× floor) | 0.49 vs 2.6e-4 | ✅ |

## The result: the split is recoverable from the consumer alone

A black-box sensitivity probe — central finite differences along 256 random
directions at 8 base points, least-squares Jacobian, top-r eigenvectors of the
summed input-space sensitivity operator — receiving **only** the consumer handle
`C(·)` and `(D, r)`, recovers the planted read subspace at **overlap 0.936**
against a **0.059 chance baseline** (~16× above chance). It never saw the planted
subspace, the compression arms, or `d_O`; the blinding is structural (the probe is
a pure function of the callable).

Crucially, the recovery is **downstream-useful**: `proj_var` computed with the
**blind** `Ŝ` predicts the a-vs-b flip — sign-agreement **12/12** in both
consumers — and its arm-ranking Spearman with `d_O` is **1.00, identical to the
true subspace's 1.00**. The blind estimate is as good as ground truth for
prediction; reconstruction (identical across a/b/d) is not (Spearman 0.40).

## What GO-1 + GO-2 now say together

- **GO-1** (this run): given only the consumer functional, you can *recover* its
  read operator `P_C` — the invariant/nuisance split — ex ante, blind.
- **GO-2** (GO-P-2026-006/009/010): that read operator governs downstream
  distortion, `tr(P_C Σ_δ)`, across attention / retrieval / optimization.

Composed: **from the consumer alone you can predict which compressor wins, before
compressing anything** — the split is identifiable and the identification is
sufficient for the downstream verdict. That is the book's core loop closed on
synthetic instances.

## Scope & honesty

- Consumers here are `tanh(W x)` with a **planted low-rank read subspace** — a
  clean identifiability testbed, not a trained model. The probe assumes the read
  operator is approximately low-rank (top-r recoverable); a consumer with a
  diffuse or strongly input-dependent Jacobian is a harder, unclaimed case.
- Single representation family (low-rank embeddings); the recovery bar is
  non-trivial (16× chance) but a real-model consumer (an actual attention head or
  retrieval encoder) is the natural next hardening.

## Ledger

GO-1 → `[predicted]` (blinded prospective probe recovers the split at 0.936 vs
0.059 chance; blind proj_var predicts the flip 12/12, Spearman 1.00 = true).
Falsifiable-core status now: **GO-1 `[predicted]`, GO-2 `[demonstrated]`/`[replicated]`
+ Gate-B hit.** 11 registered runs, all sealed-before-run; negatives NEG-5…10 stand.
