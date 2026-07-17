# GO-P-2026-008 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-retrieval-matched.json`](../results/GO2-retrieval-matched.json).
**Registered verdict: MISS — `GO2_mechanism_replicates: false` — but 4/5 gated
conditions pass 12/12, and the ONLY failure is a mis-specified SNR gate that
rejects the mechanism's ideal case.** Reported as-is (sealed, PROSPECTIVE,
registered commit 74b29a1).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| matched-distortion (recon a≈b within 2%) | **recon a=b=d=0.0964, gap 0.0** | ✅ |
| **flip decisive** (adv_dO read_A ≤ −log1.3, read_B ≥ log1.3; per-seed ≥10/12) | **−18.7 / +19.1; 12/12 & 12/12** | ✅ |
| **proj_var tracks flip** (≥11/12 both) | **12/12 & 12/12** | ✅ |
| recon fails (min Spearman recon < proj_var) | 0.40 < 1.00 | ✅ |
| SNR (min-arm dO ≥ 10× floor) | **min-arm dO = 0.0** | ❌ |

## The result: a total flip at identical reconstruction

Reconstruction is **exactly identical** across a, b, d (0.0964). Yet:

| consumer | dO(a) | dO(b) | winner |
|---|---|---|---|
| read_A (queries in S_A) | **0.0812** | **0.0** | b (a fully distorted, b untouched) |
| read_B (queries in S_B) | **0.0** | **0.1317** | a (b fully distorted, a untouched) |
| iso (diagnostic) | 0.0229 | 0.0239 | ~tie (adv 0.035, no flip) |

Same arms, identical reconstruction, **opposite winner** by consumer — the flip is
total. `proj_var` tracks it perfectly (sign 12/12 both consumers); reconstruction,
being identical, cannot order a vs b (Spearman 0.40). This is GO-2's positive-half
mechanism in its purest form, now in retrieval ranking (a nonlinear consumer):
**the nonlinear ranking does follow the injected error's subspace overlap**, which
was the genuine, falsifiable question. It did not have to.

## Why the registered flag is nonetheless False (a mis-specified gate)

The SNR gate reads `min-arm dO ≥ 10× floor`. Here the "blind" arm has its entire
error in a subspace **orthogonal** to the consumer, so its downstream distortion
is **exactly 0** — the *strongest possible* demonstration of consumer-blindness.
The gate was meant to ensure the ranking signal is real (above the fp16 floor),
but it should have gated the **loser's** distortion (0.081 / 0.132, both ≫ the
~1e-6 floor), not the min arm. The SNR *spirit* is decisively met; the *letter*
(min arm) fails precisely because the mechanism worked perfectly. This is the same
class of error as v5 (a gate fighting the phenomenon), not a failure of the claim.

## Ledger disposition & next step

- GO-2 mechanism in retrieval: **demonstrated in substance** — total flip at
  identical reconstruction, proj_var tracks 12/12, recon blind. The registered
  conjunction missed only on a mis-specified SNR gate.
- `[replicated]` — I am **not** claiming it on this run, because the registered
  flag is False; discipline says a mis-specified gate is still a miss.
- **GO-P-2026-009 (to register), the clean close:** (i) fix the SNR gate to require
  the **loser's** dO ≥ 10× floor (well-specified non-degeneracy); (ii) inject the
  error as a mix — √(1−η)·subspace + √η·isotropic, η≈0.1, same total norm — so no
  arm is *exactly* zero (a decisive-but-non-degenerate flip, more realistic than
  perfect orthogonality) while reconstruction stays identical. Register
  prospectively. This fixes the gate, not the claim: the four substantive gates
  already passed 12/12.

Two prospective retrieval runs: 007 bounded the phenomenon to the recon-matched
regime (NEG-10); 008 demonstrated it there, decisively, and caught a gate bug. The
mechanism transfers; the clean registered `[replicated]` is one gate-fix away.
