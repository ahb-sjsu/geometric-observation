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
re-derivation (both grades) + a constants/slack and known-gaps table (T-CUST-1). `[demonstrated]` — sealed prediction passed its ex-ante bar on
a governed run. `[replicated]` — `[demonstrated]` reproduced on a second independent
instance. `[predicted]` — sealed, gate stated, prospective/single-instance. `[exploratory]`
— green check, unproven derivation; **may not support an umbrella claim**. `[refuted]` — a
lost bet, carried at full prominence.

## The falsifiable core

| Claim | Class | Chapters | Registry |
|---|---|---|---|
| GO-1 — read/nuisance split identifiable ex ante from the consumer | `[predicted]` ✅ | 5, 10, 14 | 011 |
| GO-2 (neg-half) — downstream preservation is **not** reconstruction | `[demonstrated]` | 2, 6, 8, 14 | 002 |
| GO-2 (pos-half) — controlled by $\operatorname{tr}(P_C\Sigma_\delta)$ | `[replicated]` (2 instances) | 6, 8, 14 | 006 + 009 |
| GO-3 — certificate vacuity threshold predicts single-stage death | `[demonstrated]` | 11, 14 | 014 |
| GO-4 — fixed-budget verdicts invert under budget-matched observation | `[replicated]` | 4, 14 | 015 |
| GO-5 — α=1 density quotient restores fidelity outside diffusion | **`[refuted]`** (NEG-11) | 9, 12, 14, 16 | 019 |
| GO-6 — output ≤ surrogate ≤ reconstruction at matched rate | `[demonstrated]`, disputed (VI-32, VI-34; re-run owed) | 7, 14, App. B | 028 |

The ledger's later core rows, GO-7 to GO-14 and GO-16, are indexed under "Beyond one
consumer" below.

## COST-face theorems (Appendix B)

*Corrected 2026-11-20 (VI-32). No COST-face theorem was `[proved]`, since none had a custody
table; since 2026-11-21 ledger rows PAPER-III.a and PAPER-III.b cover the max-det corner
identity of B4 and B5, `lem:maxdet`'s rate identity, and B7's corrected $V$ as a variance. Appendix B also misstated B4 and B6, and B7's constant was wrong (NEG-18). The
full corrected custody summary is in Appendix B.*

| Claim | Class | Registry | Incident |
|---|---|---|---|
| B1 — consumer $R_C(D)$ achievability + converse | `[exploratory]` (pending net + custody) | 022 blk | VI-3, VI-32, VI-38 |
| B2 — output ≤ surrogate ≤ reconstruction (GO-6) | `[demonstrated]`, **disputed** (harness off the matched-rate premise; re-run owed) | 028 | VI-32, VI-34 |
| B3 — surrogate–output gap vanishes with rate | `[demonstrated]`, **disputed** (same harness) | 028 | VI-3, VI-32, VI-34 |
| B4 — two-observer region; refinability ⇒ $\Sigma_2^\star\preceq\Sigma_1^\star$ (⇔ under Assumption SR) | max-det corner identity `[proved]` (ledger row PAPER-III.a); region, refinability and rate loss as coding statements `[exploratory]` | 022, 023 | **VI-4**, VI-32, VI-36, VI-37, VI-38, VI-39, VI-40, VI-42, VI-45, VI-46, VI-47 |
| B5 — rate region: the converse for every $k$; equality and the sufficiency of nesting under Assumption SR (successive-refinement achievability, attributed to Effros, unchecked), for every $k$ | corner identity `[proved]` (ledger row PAPER-III.a); region `[exploratory]` (converse: no net that can fail; equality: Assumption SR) | 023 | VI-5, VI-32, VI-34, VI-37, VI-38, VI-39, VI-40 |
| B6 — mismatch tax $(r/2)\log(M/m)$ for $m\hat P\preceq P\preceq M\hat P$ + omission floor $\operatorname{tr}(\tilde P\Pi)$ | `[predicted]`-grade / floor `[demonstrated]` | 024/027 | VI-6, NEG-13, VI-32, VI-38 |
| B7 — dispersion counts at most the read dimensions, $r_D\le 2V\le r$ (nats$^2$) | reduction `[exploratory]` (025's checks cannot fail); corrected $V$ as a variance `[proved]` (ledger row PAPER-III.b), as the dispersion `[exploratory]`; the $r_D/2$ constant `[refuted]` | 025 | VI-7, **NEG-18**, VI-34, VI-36, VI-37, VI-38, VI-45, VI-46, VI-48, VI-49 |

## LEGIBILITY-face theorems (Chapter 9)

*No ledger row carries the results below. Their custody (proofs, R-IND-5 records, nets)
lives in the sibling repository `the-angular-observer` and has not yet been audited against
T-CUST-1 (FRONTIER G11). Until it is, and a row records the class, the book gives them no
class tag: the column says what Paper I holds. (Until 2026-11-26 this table, and Chapter 9,
tagged them `[proved]` and `[demonstrated]`.)*

| Claim | Status |
|---|---|
| Angle carries geodesics; radius carries density (polar decomposition of the collapse) | proved in Paper I; not yet a ledger row |
| Row-normalization = angular read-subspace projection (NJW justified) | proved in Paper I; not yet a ledger row |
| Tangential-noncollapse (A2) normalization identity locates the mechanism | proved in Paper I; not yet a ledger row |
| $S^1$ exact rank collapse (plain commute filter, rank 1) | proved in Paper I; not yet a ledger row |
| Flat-torus uniform lower angular bound (dyadic-block, co-Lipschitz) | proved in Paper I; not yet a ledger row |
| Exact upper-Lipschitz divergence (commute filter) | proved in Paper I; not yet a ledger row |
| Spectral-filter phase diagram; critical dimension $d = 4$ | proved in Paper I; not yet a ledger row |
| Green-kernel rank-limit theorem, $d \le 3$; rank 1 on $S^2,S^3,\mathbb{RP}^2,\mathbb{RP}^3$ | proved in Paper I; not yet a ledger row |
| Green-rank positivity beyond two-point homogeneous spaces | **conjectured** (Ch. 17) |
| Heat filter uniform-in-truncation bi-Lipschitz | proved in Paper I; not yet a ledger row |
| α=1 as the $\ker P_C$ membership-test sign (spectral/operator setting) | measured in Paper I; not yet a ledger row |
| Dimension emerges before shape (Weyl ordering) | measured in Paper I; not yet a ledger row |

## Beyond one consumer (Chapters 17 and 24 to 29)

*Added 2026-11-25. Each line is the class the ledger row carried on that date; the row,
not this table, is the record.*

| Claim | Class | Chapter | Registry |
|---|---|---|---|
| RLD-I, RLD-II, RLD-III.1 to III.5, RLD-IV.1 to IV.4 (rate, leakage and distortion with a holder: vectors, stationary processes, slowly varying, cyclostationary, non-Gaussian, unstable and ergodically driven sources) | `[exploratory]` (written proofs and fresh-context audits; no sealed registration, no constants table) | 24 | none |
| T1 (learn-then-serve) and T1-MK (a read kernel that moves with the point) | `[exploratory]` | 17 | none |
| PAPER-V.a (convexity, Pareto channel, exact-output minima, two-bit boundary, thermal water-filling, staleness complement) | `[proved]` | 25 | 042 |
| PAPER-V.b (Gaussian region: scalar quadrant, reset water-filling, the minima without side information) | `[proved]` | 25 | 044 |
| PAPER-V.c (coding theorems, several consumers, the work endpoint) | `[exploratory]` (no check can fail) | 25 | none |
| PAPER-V.d (materialization identity, conditional total correlation) | `[exploratory]` | 25 | none |
| GO-7 (rate and reset content are separate resources) | `[replicated]` | 25 | 043, 045, 047 (046 a logged miss) |
| GO-8 (reset threshold rises with the age of the side information) | `[replicated]`, with a recorded post-hoc fix to a control statistic | 25 | 049, 053 |
| GO-9 (coordinated reset is cheaper by the shared structure) | `[replicated]`, same caveat | 25 | 050, 054 |
| GO-10 (the complementarity tax in rate and in reset work) | `[replicated]` | 26 | 055, 058, 059 |
| GO-11 (the conditional rate and work region behind the tax) | `[replicated]` | 26 | 060 to 064 |
| GO-12 (staleness is access width, not delay; spectral conditional function at circulant scope) | `[predicted]` | 27 | 065, 066, 070, 071 |
| GO-13 (the dynamic complementarity tax) | `[demonstrated]` | 27 | 067 to 069, 072 to 074 |
| GO-14 (causal erasure) | `[predicted]` | 27 | 076, 078 to 086 |
| Access width on a serving stack | P1 `[demonstrated]`; P2 **`[refuted]`** as sealed | 27 | 077 |
| GO-16 (the adversarial observer) | Theorems 1 and 2 and the discrete twin `[predicted]`; Theorem 3 as sealed **`[refuted]`** (NEG-17); the campaign `[exploratory]` | 28, 16 | 090, 091 |
| GO-EC-2 to GO-EC-7 (sensor schedules, triggers, a simulated optical link, the two-consumer tax, closed loop) | `[predicted]` | 29 | 087 to 089 and the campaign registrations named in the rows |

## The domain sweep (VALUE face; Chapter 13)

| Domain | Class | Registry |
|---|---|---|
| A1 synthetic ULA / A3 LOCATA | `[predicted]`, hit (confirmed anchors, sealed flips) | 031 / 033 |
| A2 Llama rematch | `[predicted]`, hit (reconstruction-invisible worse-arm discrimination on one consumer, **not** a flip) | 021 |
| D2 AV16.3 acoustic / D3 PDAR seismic | `[predicted]`, hit (battery ≥2-of-3 met) | 034 |
| W whale coda-dialect | `[predicted]`, hit (sealed flip) | 038 |
| L legal citation retrieval | `[predicted]`, hit (035→036→039) | 039 |
| M moral / K KV-keys / Mu music | `[exploratory]` (A2 verdicts — **not** flips) | 037 |
| D1 RaDICaL radar | `[predicted]` → **partial** (data-limited) | 034 |
| D4 optimization (gradient) | **`[refuted]`** as a flip (coupling null) | 034 |
| GO-B-blind 20 Newsgroups | `[predicted]` → **partial** (direction yes, magnitude no) | 041 |

## Standing negatives (Chapter 16), each carried at full prominence

NEG-1 (uniform-in-$m$ commute bi-Lipschitz) · NEG-2 (reconstruction cosine as proxy) ·
NEG-3 (heat-taper reversal, pending confirm) · NEG-4 (Lloyd recalibration) · NEG-5…9 (the
KV-key proxy ladder) · NEG-10 (flip needs recon-matched arms) · NEG-11 (α=1 outside
diffusion) · NEG-12 (real-model blind probe sub-bar) · NEG-13→resolved (omission floor
shallow-sweep gate) · NEG-14 (one-number regime shortcut) · NEG-15 (hubness as a Bell
mechanism) · NEG-16 (KV serving, end task) · NEG-17 (GO-16's tie theorem as sealed) ·
NEG-18 (the dispersion constant). All `[refuted]` except NEG-13 (resolved to
`[demonstrated]` by a fresh held-out test) and NEG-15 (`[demonstrated]`, a negative with a
reusable harness); NEG-16 is `[refuted]` for the end task with its behavioural co-primary
`[demonstrated]`.

The other `[refuted]` rows of the ledger, also carried in Chapter 16: OT-4 and OT-5
(`[refuted]`) and OT-9 and OT-10 (`[refuted]` as sealed) from Observation Theory's graduation
campaigns, and prediction P2 of registration 077 (`[refuted]` as sealed). OT-11 and OT-12 are
void.

## Verification incidents (R-IND-5), caught pre-publication

VI-2 (extreme-value scaling) · VI-3 (App-B derivation-grade caveats) · **VI-4** (the
`sigma_star` false-pass — the standing reminder that the assistant may not grade itself) ·
VI-5 (k-chain non-iteration; its citation correction proved unchecked or wrong, VI-36 to VI-40) · VI-6 (omission floor: whitened kernel, floor not
unbounded) · VI-7 (dispersion: covering argument; its replacement "effective dimension
$r_D$" was itself refuted later, NEG-18).

The later incidents, VI-8 to VI-57, are in the ledger. They audit Paper V, the
complementarity tax and GO-11 to GO-16, the estimation-and-control campaign (VI-11 to VI-15),
the RLD papers, T1 and T1-MK, and the custody passes on Paper III; the chapters cite them
where they bear on the text (Chapters 7, 16, 17 and 24 to 29, Appendix B). Not all were
caught before publication: VI-30 (NEG-17) and VI-32 (NEG-18) found errors after a seal.

## How to read this appendix

Every claim above resolves to a row in `claims/LEDGER.md` with its notebook, result JSON,
CI status, and replication count, except the LEGIBILITY results and the COST theorems B1 and
B6, which have no row of their own yet. The umbrella text of this book cites only rows at or
above their class bar; no sentence in the main chapters leans on an `[exploratory]` row
(PROTOCOL Rule 1.1), and every `[refuted]` row appears in Chapter 16 at the prominence of
the win it bounds. That is the whole contract: the book asserts exactly what the ledger can
show, and this appendix is the map between the two.
