# GO-P-2026-010 — post-run notes (unblinded 2026-07-17)

Result: [`../results/GO2-gradient-curvature.json`](../results/GO2-gradient-curvature.json).
**Registered verdict: PASS — `GO2_mechanism_generalizes: true`. All five gated
conditions met, PROSPECTIVE, out-of-sample.** GO-2's mechanism generalizes to a
**Hessian read operator** in optimization — a domain disjoint from Papers I–II.
Fills the GO-B / Gate-B row with a genuine `[predicted]` hit. Reported as-is
(sealed, registered commit d3860e9).

## Per gated condition

| gated bar | result | pass? |
|---|---|:--:|
| matched-distortion (recon a≈b within 2%) | recon a=b=d=0.298, gap 0.0 | ✅ |
| SNR (loser's dO ≥ 10× floor) | 0.119 / 0.171 vs 1.1e-8 | ✅ |
| **flip decisive** (adv_dO H_A ≤ −log1.3, H_B ≥ log1.3; ≥10/12) | −2.57 / +2.51; 12/12 & 12/12 | ✅ |
| **proj_var tracks flip** (≥11/12 both) | 12/12 & 12/12 | ✅ |
| recon fails (min Spearman recon < proj_var) | −0.20 < 1.00 | ✅ |

## The result: the read operator can be a Hessian

At **identical reconstruction** (a=b=d=0.298), the update-direction distortion in
the curvature metric flips with the consumer's curvature profile:

| consumer | dO(a) | dO(b) | winner |
|---|---|---|---|
| H_A (curved in S_A) | **0.119** | 0.009 | b |
| H_B (curved in S_B) | 0.014 | **0.171** | a |
| H_iso = I (diagnostic) | 0.0416 | 0.0420 | tie (adv 0.008) |

`proj_var = tr(H Σ_δ)/tr(H Σ_0)` tracks the flip 12/12 in both curvature
consumers; reconstruction (identical across a/b/d) is uninformative — Spearman
−0.20 / 0.40, and under the identity metric H_iso it tracks perfectly (1.00),
confirming reconstruction is exactly the H = I special case. So the same mechanism
that governed a softmax (query second-moment) and a retrieval ranking (subspace
projector) governs a **gradient-descent optimizer reading through loss curvature**.
The consumer's read operator `P_C` is general: query bank, projector, or Hessian.

## Honest caveat: the multi-step loss diagnostic washed out

The registered **gated** downstream is the single-step update-direction (cos_H)
distortion — a legitimate optimization quantity — and it flipped cleanly (12/12).
The **reported-only** 30-step GD excess-loss cross-check came back near the
numerical floor (~1e-4) and did **not** show a clean flip (a_H_A 1e-4, b_H_A ~0,
a_H_B 4e-4, b_H_B 1e-4): the convergent quadratic trajectory drives θ→0 and the
per-step error damage washes out. I therefore **do not claim** the multi-step-loss
version — only the single-step update-direction claim, which is what was gated. A
sharper multi-step test (non-convergent / stochastic / fixed-horizon regime) is a
future registration, not claimed here.

## Ledger disposition

- **GO-B / Gate B: filled with a `[predicted]` hit** — the GO-2 mechanism holds
  out-of-sample for a Hessian read operator (optimization), for the single-step
  curvature-metric update-direction consumer.
- GO-2 mechanism `tr(P_C Σ_δ)` now stands across **three read operators**: query
  second-moment (attention, GO-P-2026-006), subspace projector (retrieval,
  GO-P-2026-009), Hessian (optimization, GO-P-2026-010). One mechanism, three
  consumer families.
- Scope honesty: single-step update-direction only for the curvature case;
  regime bound NEG-10 (recon-matched arms) intact; multi-step loss unclaimed.

## Arc to date (10 registered runs, all sealed-before-run, all recorded)

instance 1 (attention): v1…v6 → both halves `[demonstrated]`.
instance 2 (retrieval): 007 miss (NEG-10) → 008 substance+gate-bug → 009 `[replicated]`.
Gate B (optimization): 010 `[predicted]` hit (single-step update direction).
Six standing negatives (NEG-5…10). Nothing retro-fitted.
