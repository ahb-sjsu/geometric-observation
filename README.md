# Geometric Observation

The third work in the geometric series, and its **evidence repository**. The book
synthesizes:

- **Paper I** — *Keep the Angle* ([`the-angular-observer`](https://github.com/ahb-sjsu/the-angular-observer)): the spectral/angular result and the manifold recognizer.
- **Paper II** — the compression-as-observation work ([`turboquant-pro`](https://github.com/ahb-sjsu/turboquant-pro)): keys/values asymmetry, rank certificates, the (A2) probe, operator-regime tracing.
- **Paper III** — the generalized quotient-transfer theorem (`[proved]` gate for the umbrella principle).

into one claim: **compression succeeds for a consumer exactly when it preserves
what that consumer's functional distinguishes** — measured on the consumer's own
metric, never on reconstruction error.

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

## Status

**Bootstrapping.** Repo scaffolded to the protocol; the claim ledger carries the
standing `[refuted]` rows and the GO-1…5 core as *registered/pending*. Drafting
begins at Gate A ∧ B (`PROTOCOL.md` §11); no book-cited run happens before its
prereg entry exists.
