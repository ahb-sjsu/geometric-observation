# GO-P-2026-042 — post-run notes (theorem harness, run 2026-08-02)

Harness: [`verify_consumer_landauer.py`](verify_consumer_landauer.py) ·
prereg [GO-P-2026-042](../prereg/GO-P-2026-042-consumer-landauer-region.md) ·
Tier A (CI reruns it; no committed JSON — VERDICT sentinel) · governed run on
Atlas at the sealed commit. **VERDICT: ALL PASS**, every section at machine
precision.

## What it nets

The complete analytic content of the consumer-relative Landauer paper
(Thm 1, Props 1–4, Thm 2, Cors 1–4 in the original numbering), as a
falsification net per charter rule R-IND-5 — the harness is not the proof;
a miss sends the claim back to the proof.

## Per section

| section | result |
|---|---|
| [1] Prop 2 binary frontier | product-BSC channels realize the closed form to 7.8e-16; 2,056 admissible channels (random + the eq.-(20) optimizer at 11 support directions) never beat a support line; matched-rate inversion exact (L 0.1187 vs 1.0000 at tied R=1.1187, ratio 8.42×) |
| [2] Prop 1 fixed point | descent never upticks (0.0e0); eq.-(20) self-consistency 1.6e-7; no random channel beats J*; α=1 reproduces R(D)=1−h₂(D) to 2.2e-16; midpoint convexity of both coordinates 0/2000 violations |
| [3] Thm 1 finite-n converse | 4,048 random deterministic codes (n∈{1,2}, exact H(M\|Sⁿ), optimal decoders) — zero boundary violations |
| [4] Thm 2 materialization | H(A,M\|Sⁿ)=nH(X\|S) + chain rule to 2.2e-15; ΔW never negative |
| [5] Cors 2–3 | exact-consumer endpoints to 1.7e-13; TC ≥ 0 on 400 random 3-consumer reads, up to 2.06 bits saved by coordinated reset |
| [6] Cor 4 water-filling | eq.-(41) = max-det program to 6.9e-15; 6,869 admissible Gaussian codes, zero violations |
| [7] temperature-weighted WF | feasibility+KKT+equal-T to 1.8e-15; zero random-allocation violations |
| [8] staleness | monotone on 40 random chains (exact); binary complement identity to 1.6e-15 |

## Companion verification

Fresh-context R-IND-5 derivation pass on the full paper: **0 errors, 4
sharpenings** (ledger **VI-8**) — all folded into the .tex; see
[`../paper/consumer-relative-landauer-REVISION-NOTES.md`](../paper/consumer-relative-landauer-REVISION-NOTES.md).
The operational face of the same claims is GO-7
([GO-P-2026-043](../prereg/GO-P-2026-043-landauer-operational-separation.md),
[notes](GO-landauer-operational-NOTES.md)).
