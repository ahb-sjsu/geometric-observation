# GO-P-2026-037 — Reconciling the consumer-relative flip with turboquant-pro's (A2) probe

The consumer-relative flip has been shown across many domains with bespoke harnesses. This entry
**re-grounds the two embedding-consumer domains (moral, legal) in turboquant-pro's validated `a2_probe`
metric** (`turboquant_pro/a2_probe.py`), and seals the (A2) diagnostic that predicts *which regime* a
domain is in — i.e. whether a generic angular code exposes the flip or the GO-1 blind-probe read operator
is required. The `a2_probe` module's two documented failure classes turn out to *be* the empirical
taxonomy (identifiability vs the direction-concentration regime).

## The validated metric
`a2_probe.probe_quotient(batch, consumer, queries, bits)` quantizes `batch` under a **polar/angular**
proxy (norm + direction, the read-preserving family) and a **per-channel/affine** proxy (the
reconstruction-oriented family) at matched bits, and returns the Spearman rank-agreement of the
**declared consumer's** scores under each. Plus two diagnostics: `tangential_fraction` (is the consumer
carried by the direction part? ≈1 = angular consumer) and `median_unit_displacement` (√2≈1.414 =
isotropic directions; small = the **direction-concentration** regime).

## Anchors (retrospective; `a2_probe` values already computed on held-out data)
- **MORAL** — fine-tuned bert-base ETHICS-commonsense classifier (held-out acc 0.736, vs 0.53 chance),
  consumer = classifier logit (`attention_logits`, query = the judgment direction `W₁−W₀`). Diagnostics:
  tangential **0.943**, unit_disp **1.195** (near-isotropic). probe_quotient at **1 bit: polar 0.994 >
  per_channel 0.956** → the flip is visible to a *generic* angular code.
- **LEGAL** — CourtListener citation retrieval, LaBSE, consumer = cosine ranking. Diagnostics: tangential
  **1.000**, unit_disp **0.927** (**direction-concentration**). probe_quotient: per_channel ≥ polar at
  every bit (generic polar 0.92–0.99 < per_channel) → the flip is **not** visible to a generic angular
  code; it required the GO-1 blind-probe low-rank read operator (`GO-P-2026-036` CONFIRMED, R 0.779 > O).

## The sealed diagnostic prediction (prospective for future domains)
```yaml
id: GO-P-2026-037
date: 2026-07-19
retrospective: true    # moral/legal anchors known; the DIAGNOSTIC RULE below is prospective
kind: reconciliation of the consumer-relative flip with turboquant-pro a2_probe; sealed (A2) regime rule
metric: turboquant_pro.a2_probe (probe_quotient polar-vs-per_channel Spearman; tangential_fraction; median_unit_displacement)
anchors:
  moral: {consumer: attention_logits, tangential: 0.943, unit_disp: 1.195, probe_1bit: "polar 0.994 > per_channel 0.956", regime: generic-angular-flip}
  legal: {consumer: cosine, tangential: 1.000, unit_disp: 0.927, probe: "per_channel >= polar (generic)", regime: direction-concentration -> needs blind-probe read op (GO-P-2026-036)}
diagnostic_rule:   # the falsifiable, prospective claim -- tested on every future embedding-consumer domain
  premise: an ANGULAR consumer has tangential_fraction >= 0.9 (else the flip is not an angular phenomenon)
  rule: median_unit_displacement predicts the regime -- unit_disp >~ 1.0 (isotropic) => the flip is
    visible to a GENERIC polar/angular code (probe_quotient polar > per_channel at low bits);
    unit_disp <~ 1.0 (direction-concentration) => generic polar FAILS and the flip requires the GO-1
    blind-probe LOW-RANK read operator (per GO-P-2026-036).
prediction: on any new angular-consumer (tangential >= 0.9) embedding domain, the sign of
  (unit_disp - 1.0) predicts whether generic probe_quotient shows the flip; where it does not, the
  blind-probe read operator recovers it.
falsification: a domain with tangential >= 0.9 and unit_disp >~ 1.0 where generic polar does NOT beat
  per_channel at low bits, OR unit_disp <~ 1.0 where generic polar DOES -- refutes the (A2) regime rule.
scope: EMBEDDING-consumer domains where a2_probe's consumers apply (cosine / l2 / attention_logits):
  retrieval, classification, KV-keys, recommender. Physical-array DOA (LOCATA/AV16.3/PDAR) uses a
  subspace/beamforming consumer NOT in a2_probe's set -- reconcilable in CONCEPT (angular read operator)
  but not via this probe; the coupling failure (D4, gradient/curvature) is the radial/non-angular class.
hash: sha256:afd3e8ac4dfa56bb0c30f3048e7f31160e4b0935fb138d0da534f580b16f1a0e
```

## Falsification
A pass makes the flip's domain-dependence *predictable from a single validated statistic*: `a2_probe`'s
`median_unit_displacement` says, before any flip experiment, whether a generic angular code suffices or
the blind-probe read operator is needed. The `035→036` arc becomes an instance of the rule rather than a
one-off fix. Sealed per REG-1; the git commit is the binding timestamp; the diagnostic rule is
prospective for every future embedding-consumer domain.

## Outcome — the DIAGNOSTIC RULE is REFUTED (the reconciliation stands), 2026-07-19
First prospective test, on synthetic embeddings dialled between regimes (probe_quotient, cosine, 1 bit):

| domain | tangential | unit_disp | 1-bit polar vs per_channel | rule predicts | holds? |
|---|---|---|---|---|---|
| moral (real) | 0.943 | 1.195 | polar 0.994 > 0.956 | generic flip | ✓ |
| legal (real) | 1.000 | 0.927 | per_channel ≥ polar | needs blind-probe | ✓ |
| synth isotropic dc=0 | 0.988 | 1.416 | polar 0.849 > 0.600 | generic flip | ✓ |
| **synth concentrated dc=6** | 0.995 | **0.649** | **polar 0.722 > 0.346** | needs blind-probe | **✗** |

The `unit_displacement` threshold is **REFUTED**: the concentrated synthetic has `unit_disp=0.649` (< 1.0)
yet generic polar *wins*. Diagnosis — the synthetic concentration is a **per-dimension (axis-aligned)
offset**, which is a different structure from legal's **shared-direction** anisotropy; `unit_displacement`
cannot distinguish them, but `probe_quotient` (the full polar-vs-per_channel test) can. **Conclusion:**
the *reconciliation* of the flip to `a2_probe` stands and is solid — moral and legal are both correctly
characterised by `probe_quotient`, and the (A2) tangential_fraction correctly flags both as angular
consumers. But the *predictive shortcut* (a single summary statistic standing in for the probe) does
**not** generalise. The reliable diagnostic is `probe_quotient` itself, run at low bits, per domain —
there is no one-number substitute. Recorded honestly (NEG-14) in `claims/LEDGER.md`; the discipline
caught the over-simple rule on its first prospective test.
