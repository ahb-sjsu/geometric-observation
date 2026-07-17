# GO-P-2026-002 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-kv-keys-v2.json`](../results/GO2-kv-keys-v2.json).
**Registered verdict: MISS on the full conjunction (`GO2_supported: false`) —
but the run splits GO-2 into a *demonstrated* half and an *open* half, and is
net-positive for the qualitative claim.** Reported as-is (unblinded; sealed
design, registered commit d30fc36).

## Per registered bar

| bar (registered) | result | pass? |
|---|---|:--:|
| effective-bits audit spread ≤ 0.5 | **0.19** (a,d 4.06 · c 4.13 · b 4.25) | ✅ |
| anti-probe gap KL(c)/KL(a) ≥ 5 | **21.3×** | ✅ |
| ordering KL(a) < KL(b), ≥10/12 seeds | **12/12** | ✅ |
| dominance: partialR²(tang) − partialR²(recon) ≥ 0.10 | **−0.002** | ❌ |

`GO2_supported = audit ∧ dominance ∧ c_gap ∧ a<b = false` (dominance fails).

## What this run *demonstrates* (the "not reconstruction" half of GO-2)

The matched-bits confound of v1 is gone (audit passes), and the dissociation is
now unambiguous:

- arm a (per-channel, invariant-preserving) and arm b (per-token whole-vector,
  invariant-blind) reconstruct the keys **equally well** — relative ‖δ‖/‖k‖ =
  **0.0934 (b) vs 0.0938 (a)**, b marginally *better* —
- yet **KL(b)/KL(a) = 2.53×** worse downstream, on **12/12** seeds, and the
  anti-probe is **21×** worse while only ~4.7× worse on reconstruction.

So at genuinely matched bits, **reconstruction error does not control downstream
preservation** — a compressor with identical reconstruction is 2.5× worse, and
one with 4.7× worse reconstruction is 21× worse. This is a clean `[demonstrated]`
of the negative half of GO-2 (and a fresh confirmation of NEG-2), free of the v1
bit confound.

## What this run *refutes* (my operationalization of the positive half)

GO-2's positive claim is that downstream is controlled by **quotient-tangential
noncollapse**. My scalar proxy for that quantity — relative per-channel-demeaned
error norm — is **also not the controlling quantity**: tang(b)=0.233 <
tang(a)=0.244 while KL(b) > KL(a), so it fails to order a<b, and its regression
partial-R² (0.0006) is *below* reconstruction's (0.0026). → **NEG-6.**

Diagnosis: a,b have near-equal demeaned-error *magnitude* but different error
*structure*. b (per-token) quantizes all D channels of a token with one scale, so
its error is **correlated across channels within a token** → the logit
perturbation q·δ_s has high variance **across tokens** → large softmax
distortion. a (per-channel) has channel-independent error that averages down in
q·δ_s. The controlling quantity is the **across-token variance of the
query-projected error**, Var_s(q·δ_s), not any error-norm scalar. A magnitude
proxy cannot see this; the right proxy must be query/token-aware.

## Controls were degenerate (a real lesson)

gap_real 2.53, head-shuffled 2.49, channel-rotated 2.58 — all equal. With
**isotropic** random queries the setup is rotationally symmetric, so orthogonal
reshuffles of the consumer (head permutation, channel rotation) cannot
discriminate and provide **no specificity evidence either way**. A genuine
specificity control needs a **structured, non-isotropic consumer** (real query
statistics, or a shift-sensitive consumer for which the per-channel mean stops
being nuisance).

## Ledger disposition & next step

- GO-2 **negative half** → `[demonstrated]` on this instance (matched-bits
  dissociation; recon-identical arm 2.5× worse, anti-probe 21×).
- GO-2 **positive half** (tangential noncollapse *controls* downstream) → **open**;
  the demeaned-norm operationalization is **refuted** (NEG-6).
- **GO-P-2026-003 (to register):** (i) tangential metric = Var_s(q·δ_s) over the
  query bank (query-projected, across-token), not a norm; (ii) a structured
  consumer so specificity controls bite; (iii) keep the matched-bits audit and
  the two invariant-blind arms. Re-run for dominance.

The registered conjunction missed; the run nonetheless *demonstrated* the harder,
more important negative claim and told us exactly which scalar to stop using. The
ledger records both.
