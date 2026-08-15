# OT-6 instrument appendix — sealed before the run

**Claim frozen in `OT-CRUCIBLE.md` §OT-6: the laws transfer outside
compression with zero modification — blind-recovered `P_C` of a ranking
consumer over embeddings; two perturbations of equal Euclidean energy,
opposite `tr(P_C Σ_δ)`; the trace picks the ranking-destroyer.
Committed before `ot6_check.py` executes.**

## Substrate (real, and outside the originating application)

768-d unit-normalized book-paragraph embeddings from Atlas
`/archive/results_aesthetics/book_translation_cache` (the GO-4
manifold): six files (cs_34225, de_10426, de_13451, de_15559,
de_17622, de_19530; 200 × 768 each), shuffled with seed 20260815;
first 1,000 = the retrieval index, next 200 = queries.

## Consumers (two cells; both must pass every bar)

Ranking-margin consumers reading one index embedding `x = e_j`:
- **dot cell:** `C(x) = qᵀx − max_{i≠j} qᵀe_i`
- **cosine cell:** `C(x) = cos(q,x) − max_{i≠j} cos(q,e_i)`

Operator: readscope `blind_probe` **verbatim** (mode lstsq,
sketch_dim = 960 = 1.25 d, eps 1e-3, regime check on), one probe per
(query, its clean top-1 item) cell over the first 24 queries, `P̂` =
the mean of the 24 recovered operators. No estimator code is written
for this test — that is the "zero modification" clause, structurally.

## Perturbations (equal Euclidean energy by construction)

From `P̂`'s eigendecomposition: `Σ_A` = spectrum-shaped on the top-8
eigenvectors, trace normalized to ε²; `Σ_B` = uniform on eigenvectors
65–72 (deep tail, orthogonal to the top-64), trace ε². ε = 0.15.
Assert `|tr Σ_A − tr Σ_B| < 1e-9`. Damage: 20 independent corpus
perturbations per codec (`δ_i ~ N(0, Σ)` per item); per query, damage
= 1 − (top-10 overlap with the clean ranking)/10, averaged over draws;
`D` = mean over the 200 queries.

## Bars

- **Manipulation window (OT-5's lesson):** 0.01 ≤ D_A ≤ 0.95 in both
  cells, else the run is VOID (perturbation scale failed, not the
  theory).
- **X1:** D_A > D_B with paired bootstrap over queries (B = 2000, seed
  20260815) CI excluding 0 — both cells.
- **X2:** D_A / D_B ≥ **2** — both cells.
- **X3 (the frozen kill test):** Euclidean energies are identical by
  construction, so energy predicts nothing; the trace's per-query sign
  (D_A,q > D_B,q among queries with any damage) must hold on ≥ **75%**
  — both cells.
- **X4 (zero modification, structural):** the probe, spectrum, and
  trace machinery are readscope's shipped functions, uninstrumented
  for this domain; any domain-specific estimator change voids the
  transfer claim.

Verdict: window, then X1 ∧ X2 ∧ X3 (∧ X4 structurally), both cells,
else FAIL. Result: `results/OT6-transfer.json`; ledger row OT-6.

**Amendment (2026-08-15, before any measurement):** the first
invocation crashed at readscope's applicability gate — with a single
operating point the gate's distinct-values heuristic can only ever see
two outputs and misreads a smooth margin as an indicator (an
instrument quirk worth its own readscope issue). Accommodation: the
operating point is passed replicated ×4 per probe cell, solely to give
the gate its trials; the gate stays ON (bypassing it would undercut
X4's zero-modification spirit). No other constant changes; no data had
been observed at amendment time.
