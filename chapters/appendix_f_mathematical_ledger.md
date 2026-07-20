# Appendix F — Mathematical Ledger: Status of Formal Claims

*This appendix is the book's index into `claims/LEDGER.md`: every formal claim the text
makes, with its class, its registry, and its custody. It exists so that a reader can audit
any sentence tag-first — follow a `[proved]` to its harness, a `[demonstrated]` to its
sealed prereg, a `[refuted]` to the negative it stands as. The living record of record is
`claims/LEDGER.md`; if this appendix and the ledger ever disagree, **the ledger wins** — it
is the post-publication erratum, and a claim can be downgraded there after this book is in
print. Nothing here is load-bearing until its class bar is met and CI is green.*

## The six classes

`[proved]` — written proof + committed falsification harness + fresh-context adversarial
re-derivation (both grades). `[demonstrated]` — sealed prediction passed its ex-ante bar on
a governed run. `[replicated]` — `[demonstrated]` reproduced on a second independent
instance. `[predicted]` — sealed, gate stated, prospective/single-instance. `[exploratory]`
— green check, unproven derivation; **may not support an umbrella claim**. `[refuted]` — a
lost bet, carried at full prominence.

## The falsifiable core

| Claim | Class | Chapters | Registry |
|---|---|---|---|
| GO-1 — read/nuisance split identifiable ex ante from the consumer | `[predicted]` ✅ | 5, 10, 14 | 011 |
| GO-2 (neg-half) — downstream preservation is **not** reconstruction | `[demonstrated]` | 2, 6, 8 | 002 |
| GO-2 (pos-half) — controlled by $\operatorname{tr}(P_C\Sigma_\delta)$ | `[replicated]` (2 instances) | 6, 8 | 006 + 009 |
| GO-3 — certificate vacuity threshold predicts single-stage death | `[demonstrated]` | 11 | 014 |
| GO-4 — fixed-budget verdicts invert under budget-matched observation | `[replicated]` | 4, 14 | 015 |
| GO-5 — α=1 density quotient restores fidelity outside diffusion | **`[refuted]`** (NEG-11) | 9, 16 | 019 |
| GO-6 — output ≤ surrogate ≤ reconstruction at matched rate | `[demonstrated]` | 7, App. B | 028 |

## COST-face theorems (Appendix B)

| Claim | Class | Registry | Incident |
|---|---|---|---|
| B1 — consumer $R_C(D)$ achievability + converse | `[proved]` | 022 blk | — |
| B2 — output ≤ surrogate ≤ reconstruction | `[proved]`/`[demonstrated]` | 028 | — |
| B3 — surrogate–output gap vanishes with rate | `[demonstrated]` | 028 | VI-3 |
| B4 — two-observer region; refinability = Loewner nesting | `[proved]` | 022 | **VI-4** |
| B5 — complete rate region + k-observer chain | `[proved]` | 023 | VI-5 |
| B6 — mismatch tax $(r/2)\log(M/m)$ + omission floor $\operatorname{tr}(\tilde P\Pi)$ | `[proved]`/`[demonstrated]` | 024/027 | VI-6, NEG-13 |
| B7 — dispersion counts read dimensions ($r_D \le r$) | `[proved]` | 025 | VI-7 |

## LEGIBILITY-face theorems (Chapter 9)

| Claim | Class |
|---|---|
| Angle carries geodesics; radius carries density (polar decomposition of the collapse) | `[proved]` |
| Row-normalization = angular read-subspace projection (NJW justified) | `[proved]` |
| Tangential-noncollapse (A2) normalization identity locates the mechanism | `[proved]` |
| $S^1$ exact rank collapse (plain commute filter, rank 1) | `[proved]` |
| Flat-torus uniform lower angular bound (dyadic-block, co-Lipschitz) | `[proved]` |
| Exact upper-Lipschitz divergence (commute filter) | `[proved]` |
| Spectral-filter phase diagram; critical dimension $d = 4$ | `[proved]` |
| Green-kernel rank-limit theorem, $d \le 3$; rank 1 on $S^2,S^3,\mathbb{RP}^2,\mathbb{RP}^3$ | `[proved]` |
| Green-rank positivity beyond two-point homogeneous spaces | **conjectured** (Ch. 17) |
| Heat filter uniform-in-truncation bi-Lipschitz | `[proved]` |
| α=1 as the $\ker P_C$ membership-test sign (spectral/operator setting) | `[demonstrated]` |
| Dimension emerges before shape (Weyl ordering) | `[demonstrated]` |

## The domain sweep (VALUE face; Chapter 13)

| Domain | Class | Registry |
|---|---|---|
| A1 synthetic ULA / A2 Llama rematch / A3 LOCATA | `[demonstrated]` (confirmed anchors) | 031 / 021 / 033 |
| D2 AV16.3 acoustic / D3 PDAR seismic | `[demonstrated]` (battery ≥2-of-3 met) | 034 |
| W whale coda-dialect | `[demonstrated]` (sealed flip) | 038 |
| L legal citation retrieval | `[demonstrated]` (035→036→039) | 039 |
| M moral / K KV-keys / Mu music | `[exploratory]` (A2 verdicts — **not** flips) | 037 |
| D1 RaDICaL radar | `[predicted]` → **partial** (data-limited) | 034 |
| D4 optimization (gradient) | **`[refuted]`** as a flip (coupling null) | 034 |
| GO-B-blind 20 Newsgroups | `[predicted]` → **partial** (direction yes, magnitude no) | 041 |

## Standing negatives (Chapter 16), each carried at full prominence

NEG-1 (uniform-in-$m$ commute bi-Lipschitz) · NEG-2 (reconstruction cosine as proxy) ·
NEG-3 (heat-taper reversal, pending confirm) · NEG-4 (Lloyd recalibration) · NEG-5…9 (the
KV-key proxy ladder) · NEG-10 (flip needs recon-matched arms) · NEG-11 (α=1 outside
diffusion) · NEG-12 (real-model blind probe sub-bar) · NEG-13→resolved (omission floor
shallow-sweep gate) · NEG-14 (one-number regime shortcut). All `[refuted]` except
NEG-13 (resolved to `[demonstrated]` by a fresh held-out test).

## Verification incidents (R-IND-5), caught pre-publication

VI-2 (extreme-value scaling) · VI-3 (App-B derivation-grade caveats) · **VI-4** (the
`sigma_star` false-pass — the standing reminder that the assistant may not grade itself) ·
VI-5 (k-chain non-iteration + citation) · VI-6 (omission floor: whitened kernel, floor not
unbounded) · VI-7 (dispersion: covering argument, $r_D \le r$).

## How to read this appendix

Every claim above resolves to a row in `claims/LEDGER.md` with its notebook, result JSON,
CI status, and replication count. The umbrella text of this book cites only rows at or
above their class bar; no sentence in the main chapters leans on an `[exploratory]` row
(PROTOCOL Rule 1.1), and every `[refuted]` row appears in Chapter 16 at the prominence of
the win it bounds. That is the whole contract: the book asserts exactly what the ledger can
show, and this appendix is the map between the two.
