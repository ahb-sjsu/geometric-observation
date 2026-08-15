# OT-8 instrument appendix — sealed before the run

**Claim frozen in `OT-CRUCIBLE-2.md`: ensemble codec preference from
weight-averaged component traces, no ensemble probe, no refit.
Committed before `ot8_check.py` executes.**

- Substrate: the OT-1 Arm H head cells (Llama-3.2-3B, layers
  {7, 14, 21}, heads {0,1,2} sharing each layer's KV stream; data in
  `crucible/armH_data`, GQA share verified there).
- **Ensemble consumer (the risky construction, chosen deliberately):**
  the weighted mixture reader `C_ens(key) = Σᵢ wᵢ α⁽ⁱ⁾(key)` — the
  heads' 24-slot attention-mass vectors summed with weights. Its true
  damage carries cross-head covariance terms
  `Σᵢⱼ wᵢwⱼ E[ΔCᵢᵀΔCⱼ]`; the prediction formula
  `Σᵢ wᵢ tr(P̂ᵢ Σ_δ)` ignores them by construction. If cross-terms
  dominate on real heads, the claim dies — that is the point.
- Component operators: exactly OT-1 Arm H's probes (jacobian_probe,
  k/d = 1.25, eps 1e-3, probed key position 96, seed 20260815 per
  head) — recomputed by the same code, nothing ensemble-level probed.
- Cells: per layer, 10 weight vectors w ~ Dirichlet(1,1,1) (seed
  20260815) over the three same-KV heads → **30 ensembles**.
- Codecs: one pair per ensemble, the OT-1 construction (random rank-4,
  trace 0.01 exactly equal), seed 20260816 (independent of probes).
- Measurement: ensemble damage `E‖ΔC_ens‖²` over 20,000 draws per
  codec (seed 20260817+cell); measured sign = sign(D_A − D_B);
  predicted sign = `sign(Σᵢ wᵢ tr(P̂ᵢ(Σ_A − Σ_B)))`.
- **Manipulation floor:** a cell is graded only if the measured sign
  is nonzero; ≥ 25 graded cells required, else VOID.
- **Bar E1:** predicted sign matches measured on ≥ **25/30** graded
  cells (≥ 83%; scaled proportionally if 25–29 graded).
- Verdict: floor, then E1. Final instrument revision. Result:
  `results/OT8-composition.json`; ledger row OT-8.
