# Geometric Observation

The fourteenth work in the geometric series, and its **evidence repository**. The book
synthesizes:

- **Paper I** — *Keep the Angle* ([`the-angular-observer`](https://github.com/ahb-sjsu/the-angular-observer)): the spectral/angular result.
- **Paper I.5** — *The Angular Observer as a Manifold Recognizer* ([`the-angular-observer/paper2`](https://github.com/ahb-sjsu/the-angular-observer/tree/main/paper2)): the five-instrument recognizer that names a manifold or certifies none — *dimension emerges before shape*.
- **Paper II** — the compression-as-observation work ([`turboquant-pro`](https://github.com/ahb-sjsu/turboquant-pro)): keys/values asymmetry, rank certificates, the (A2) probe, operator-regime tracing.
- **Paper III** — [**Observation Theory**](paper/observation-theory.pdf) ([source](paper/observation-theory.tex)): the information-theoretic synthesis — consumer-relative rate–distortion, the two-observer successive-refinement region ([`paper/two-observer-theorem.tex`](paper/two-observer-theorem.tex)), and the omission floor.
- **Paper IV** — [**The consumer-relative flip**](paper/paper-IV-consumer-relative-flip.pdf) ([source](paper/paper-IV-consumer-relative-flip.tex), [TMLR build](paper/paper-IV-tmlr.tex)): the empirical spine — at matched bits, a code that preserves what the *consumer* reads beats a reconstruction-optimal code on the downstream task *while reconstructing the signal worse*, demonstrated across domains and physics.

into one claim: **compression succeeds for a consumer exactly when it preserves
what that consumer's functional distinguishes** — measured on the consumer's own
metric, never on reconstruction error.

## Observation Theory

Geometry, distortion, and reliability are properties of the **observation** — the
consumer's read operator, budget, and channel — not of the object observed. The
operative distortion is the reconstruction error read through the consumer,
`d_O = tr(P_C · Σ_δ)`; reconstruction (`tr Σ_δ`) is the corner `P_C = I`, where
Shannon rate–distortion and Gauss least-squares live. Paper III derives this,
proves the achievability + converse of a consumer-relative rate–distortion function
for a general source, gives the two-observer successive-refinement region, and
positions the framework as the identifiable geometric middle term between Shannon
and the information bottleneck. See
[`paper/observation-theory.pdf`](paper/observation-theory.pdf).

## House rule

> The book may not assert what the ledger cannot show.

Everything here is governed by [`PROTOCOL.md`](PROTOCOL.md): registration precedes
measurement, claims carry a class (`[proved]` / `[demonstrated]` / `[replicated]`
/ `[predicted]` / `[exploratory]` / `[refuted]`), and the umbrella principle
(Ch. 11) may cite only `[proved]`, `[replicated]`, and `[predicted]` rows.

## The falsifiable core

The framework is tautology-shaped unless specific claims are put at risk. Five
are (`PROTOCOL.md` §2): **GO-1** identifiability · **GO-2** quotient-(A2) transfer
· **GO-3** certificate vacuity · **GO-4** budget/wavelength inversion · **GO-5**
nuisance quotient. Each has a registry entry, a bar, and a falsification
condition. The Honest Negatives chapter carries every `[refuted]` row.

## Layout

| Path | What |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | Test protocol (governs every book claim) |
| [`prereg/`](prereg/) | Dated, hashed prediction-registry entries — written *before* the runs they govern ([`TEMPLATE.md`](prereg/TEMPLATE.md)) |
| [`claims/LEDGER.md`](claims/LEDGER.md) | One row per book claim; every table/figure resolves here |
| [`DOMAIN-GENERALITY-SWEEP.md`](DOMAIN-GENERALITY-SWEEP.md) | The consumer-relative flip across domains, one row per sealed prereg + result |
| [`experiments/`](experiments/) | The three-arm instance runs (§3) and scripts |
| [`results/`](results/) | Sentinel-delimited result JSONs (committed, CI-rerun) |
| [`chapters/`](chapters/) | Chapter → claim map and drafts |

## Status — falsifiable core resolved; the flip is domain-general

| Claim | Class | Evidence |
|---|---|---|
| **GO-1** identifiability | `[predicted]` | blind probe recovers the read subspace at 0.94 vs 0.06 chance; predicts the flip 12/12 |
| **GO-2** distortion (`tr P_C Σ_δ`) | `[demonstrated]` · `[replicated]` · Gate-B | recon-identical code 2.5× worse; the flip inverts with the consumer; holds on attention, retrieval, optimization, a trained Llama-3.2-3B layer (GO-021: reconstruction-invisible worse-arm call 16/16 at recon tied to 7.5e-9), and — via the sealed domain-generality battery — on acoustic and seismic arrays |
| **GO-3** certificate vacuity | `[demonstrated]` | derived EVT threshold locates retrieval death to ~5%, orders 14 corpora (ρ=0.99) |
| **GO-4** budget inversion | `[replicated]` | fixed-budget verdict inverts under budget-matched observation on real embedding manifolds |
| **GO-5** density quotient | `[refuted]` | 4 prospective misses; the density-nuisance mechanism is operator/spectral-confined (NEG-11) |

**The flip is a property of observation, not of a regime.** The sealed cross-domain
sweep ([`DOMAIN-GENERALITY-SWEEP.md`](DOMAIN-GENERALITY-SWEEP.md)) carries the
consumer-relative flip — at matched bits, read-preserving beats reconstruction-optimal
downstream while reconstructing worse — across **≥5 domains and ≥3 distinct physics**:
synthetic ULA (031), LLM attention keys (021), acoustic direction-of-arrival
(LOCATA 033, AV16.3 034·D2), and seismic backazimuth (PDAR 034·D3), plus the
non-physical domains of legal-citation retrieval (035→036→039) and sperm-whale coda
dialect (038). Radar (034·D1) is a data-limited partial; gradient/curvature
optimization (034·D4) is an honest negative that *bounds* the flip to consumers whose
read operator is misaligned with signal energy — no file drawer.

Four faces of Observation Theory stand; the fifth is an honest negative. **40 sealed
preregistrations**, every one timestamped before its measurement; standing negatives
**NEG-1…14** (NEG-13, the omission floor, resolved to `[demonstrated]` downstream on a
trained model — GO-027). Every claim resolves to a row in
[`claims/LEDGER.md`](claims/LEDGER.md).
