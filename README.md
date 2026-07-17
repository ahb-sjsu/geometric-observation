# Geometric Observation

The fourteenth work in the geometric series, and its **evidence repository**. The book
synthesizes:

- **Paper I** — *Keep the Angle* ([`the-angular-observer`](https://github.com/ahb-sjsu/the-angular-observer)): the spectral/angular result and the manifold recognizer.
- **Paper II** — the compression-as-observation work ([`turboquant-pro`](https://github.com/ahb-sjsu/turboquant-pro)): keys/values asymmetry, rank certificates, the (A2) probe, operator-regime tracing.
- **Paper III** — [**Observation Theory**](paper/observation-theory.pdf) ([source](paper/observation-theory.tex)): the information-theoretic synthesis.

into one claim: **compression succeeds for a consumer exactly when it preserves
what that consumer's functional distinguishes** — measured on the consumer's own
metric, never on reconstruction error.

## Observation Theory

Geometry, distortion, and reliability are properties of the **observation** — the
consumer's read operator, budget, and channel — not of the object observed. The
operative distortion is the reconstruction error read through the consumer,
`d_O = tr(P_C · Σ_δ)`; reconstruction (`tr Σ_δ`) is the corner `P_C = I`, where
Shannon rate–distortion and Gauss least-squares live. The paper derives this,
proves the achievability + converse of a consumer-relative rate–distortion function
for a general source, and positions the framework as the identifiable geometric
middle term between Shannon and the information bottleneck. See
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
| [`experiments/`](experiments/) | The three-arm instance runs (§3) and scripts |
| [`results/`](results/) | Sentinel-delimited result JSONs (committed, CI-rerun) |
| [`chapters/`](chapters/) | Chapter → claim map and drafts |

## Status — falsifiable core resolved

| Claim | Class | Evidence |
|---|---|---|
| **GO-1** identifiability | `[predicted]` | blind probe recovers the read subspace at 0.94 vs 0.06 chance; predicts the flip 12/12 |
| **GO-2** distortion (`tr P_C Σ_δ`) | `[demonstrated]` · `[replicated]` · Gate-B | recon-identical code 2.5× worse; flip inverts with the consumer; holds on attention, retrieval, optimization |
| **GO-3** certificate vacuity | `[demonstrated]` | derived EVT threshold locates retrieval death to ~5%, orders 14 corpora (ρ=0.99) |
| **GO-4** budget inversion | `[replicated]` | fixed-budget verdict inverts under budget-matched observation on real embedding manifolds |
| **GO-5** density quotient | `[refuted]` | 4 prospective misses; operator/spectral-confined (NEG-11) |

Four faces of Observation Theory stand; the fifth is an honest negative. ~20
registered runs, all sealed before their measurement; eleven standing negatives
(NEG-5…11). Every claim resolves to a row in [`claims/LEDGER.md`](claims/LEDGER.md).
