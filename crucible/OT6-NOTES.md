# OT-6 notes — the laws leave home

**Verdict: PASS** (`results/OT6-transfer.json`; appendix sealed, one
pre-measurement amendment for the applicability gate's single-point
trial heuristic — an instrument quirk now worth a readscope issue).

Real substrate (768-d book-paragraph embeddings, the GO-4 manifold),
two ranking consumers the theory never met during development, probe
and trace machinery verbatim:

| cell | damage A (trace-aligned) | damage B (trace-orthogonal, equal energy) | ratio | paired CI | per-query sign |
|---|---|---|---|---|---|
| dot margin | 0.527 | 0.045 | **11.8×** | [0.464, 0.499] | **200/200** |
| cosine margin | 0.206 | 0.057 | **3.6×** | [0.137, 0.162] | **200/200** |

Two perturbations with *identical* Euclidean energy — the substrate
metric had literally nothing to say — and the blind-recovered
operator's trace picked the ranking-destroyer on every query, in both
consumer classes, at effect ratios of 3.6–11.8×. The claim's exact
shape held: recover `P_C` blind, compute `tr(P_CΣ)`, predict which
codec kills retrieval; zero modification to any estimator.

Worth noting for the record: the damage metric (top-10 overlap) is
*selection-flavored* — rank sets are discrete — yet the differential
margin's operator predicted it flawlessly at this perturbation scale.
Read alongside OT-5: the quadratic form's writ runs right up to the
response floor, including into discrete downstream metrics, and stops
only where the consumer's differential signal does.

**Campaign consequence:** G2 (cross-domain, necessary) is satisfied.
The graduation now rests entirely on OT-4's verdict.
