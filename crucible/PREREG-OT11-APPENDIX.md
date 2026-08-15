# OT-11 instrument appendix — sealed before the run

**Claim frozen in `OT-CRUCIBLE-2.md`: feedback-free staleness —
streaming-retrieval damage tracks measured operator drift, and
re-allocation at the drift-derived cadence removes the excess; the
feedback-severing control passes by construction (retrieval has no
autoregression). This is the revised P4's own prediction. Committed
before `ot11_check.py` executes.**

- Substrate: the six OT-6 books. **Index** = first 100 paragraphs of
  each book (600 items, fixed). **Query strata** = each book's
  remaining 100 paragraphs; **t₀ = cs_34225** (the lone Czech book),
  t₁…t₅ = the five German books in filename order — language and book
  identity as the drift axis.
- Consumers and probes: the OT-6 dot cell verbatim (ranking margin,
  blind_probe lstsq 960, ×4 replicated point, 24 (query, top-1)
  cells per stratum) → `P̂(t)` per stratum.
- **Drift measure:** `drift(t) = 1 − ‖U₈(t₀)ᵀU₈(t)‖_F²/8` (leading-8
  subspace affinity distance).
- **Quantizer:** the Stage-D water-fill allocator (ported verbatim):
  index embeddings rotated into an operator's eigenbasis, 3 bits/dim
  total budget water-filled against the spectrum, per-direction
  uniform quantization. **Stale arm:** allocated against `P̂(t₀)`
  once. **Fresh arm (the refresh):** allocated against `P̂(t)` per
  stratum — the drift-derived cadence operationalized at stratum
  granularity, declared as such.
- **Damage:** per stratum, mean over its 100 queries of
  1 − (top-10 overlap between the fp index and the quantized index)/10,
  dot scoring.
- **Feedback-severing control:** structural — the pipeline contains no
  autoregression; stated, not measured.

## Bars

- **Manipulation check:** drift must vary — max stratum drift ≥ 2×
  min, and median stale damage ≥ 0.02, else VOID.
- **S1 (damage tracks drift):** Spearman(damage_stale(t), drift(t))
  over the five non-t₀ strata ≥ **0.8**.
- **S2 (the refresh works):** fresh ≤ stale on **every** stratum with
  above-median drift, and median relative reduction
  `1 − D_fresh/D_stale` over all five strata ≥ **0.30**.
- Verdict: check, then S1 ∧ S2. Final instrument revision. Result:
  `results/OT11-staleness.json`; ledger row OT-11.
