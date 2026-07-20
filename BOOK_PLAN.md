# Geometric Observation — Book Plan

**Title:** *Geometric Observation: The Mathematical Structure of What an Observer
Can Use.* Volume 14 of the Geometric Series. Author: Andrew H. Bond.

**Exemplar for voice/structure:** `geometric-ethics` (Book 3) — confessional
first-person Preface with a recurring named running-example protagonist;
"Core Objects at a Glance" reference table; inline epistemic-status tags; a
"How to Read This Book" audience-routing section; Parts → Chapters → Appendices;
a mathematical-ledger appendix that every table ID resolves to.

**House rule (series-inherited, enforced by `CHARTER.md`):** *the book may not
assert what the ledger cannot show.* Epistemic tags are the six ledger classes
`[proved] [demonstrated] [replicated] [predicted] [exploratory] [refuted]`, not
ethics' four — this volume uses its own ledger vocabulary. No umbrella sentence
may cite an `[exploratory]` row (PROTOCOL Rule 1.1).

**Staging (from `OBSERVATION.md` §U5).** Part A material — methodology and
instruments (the ledger, the blind probe, the recognizer, the failure taxonomy) —
documents things that already exist and may be drafted now. Part B — the thesis
chapters and Ch. 18's principle — gates on U0-green **and** ≥1 journal acceptance
among Papers {I, II, III, IV}. The Preface (the manifesto) is standing either way.
Chapters below are marked **[A]** (draftable now) or **[B]** (gated).

---

## Status

| File | Chapter | Stage | Status |
|---|---|---|---|
| `ch00_front_matter.md` | Front matter, Core Objects, TOC, Notation | — | ✅ drafted |
| `preface.md` | Preface (Maya's Cache; the footnote that grew) | — | ✅ drafted |
| `ch01_why_observation_needs_a_theory.md` | 1 — Why Observation Needs a Theory | A | ✅ drafted |
| `ch02_failure_of_observer_free_measurement.md` | 2 — The Failure of Observer-Free Measurement | A | ✅ drafted |
| `ch03_historical_precursors.md` | 3 — Historical Precursors | A | ✅ drafted |
| `ch04_the_observer_triple.md` | 4 — The Observer Triple | A | ✅ drafted |
| `ch05_the_read_metric_and_the_quotient.md` | 5 — The Read Metric and the Quotient | A | ✅ drafted |
| `ch06_mathematical_preliminaries.md` | 6 — Mathematical Preliminaries | A | ✅ drafted |
| `ch07_cost.md` | 7 — COST | B | ✅ drafted |
| `ch08_value.md` | 8 — VALUE (the flip) | B | ✅ drafted |
| `ch09_legibility.md` | 9 — LEGIBILITY (Keep the Angle) | B | ✅ drafted |
| `ch10_the_blind_probe.md` | 10 — The Blind Probe | A | ✅ drafted |
| `ch11_the_recognizer.md` | 11 — The Recognizer | A | ✅ drafted |
| `ch12_failure_taxonomy_and_kappa.md` | 12 — Failure Taxonomy & the κ Law | A/B | ✅ drafted |
| `ch13_the_domain_generality_sweep.md` | 13 — The Domain-Generality Sweep | A | ✅ drafted |
| `ch14_the_falsifiable_core.md` | 14 — The Falsifiable Core | A | ✅ drafted |
| `ch15_registration_first.md` | 15 — Registration-First | A | ✅ drafted |
| `ch16_honest_negatives.md` | 16 — Honest Negatives | A | ✅ drafted |
| `ch17…ch18`, `appendix_*` | Horizons + appendices | B/A | ⏳ planned |

---

## Content sources (map book → repo)

- **Thesis, three shadows, consumer table, boundaries:** `OBSERVATION.md`.
- **Falsifiable core, per-claim status, the 12-domain sweep, Gate B, the honest
  negatives, the verification incidents:** `claims/LEDGER.md`, `DOMAIN-GENERALITY-SWEEP.md`.
- **The discipline (R-IND, seal-before-measure, the AI-assistant conflict, the
  stand-down clause, standards alignment):** `CHARTER.md`, `PROTOCOL.md`.
- **Registry accounting / no-file-drawer:** `claims/REGISTRY-ACCOUNTING.md`, `prereg/`.
- **The three papers:** LEGIBILITY ← Paper I (`the-angular-observer`) + Paper I.5
  (recognizer); VALUE ← Paper II + Paper IV (the sweep) + `turboquant-pro` probe;
  COST ← Paper III (T-IT).

---

## Chapters

### Part I — The Problem

**Ch. 1 — Why Observation Needs a Theory [A].** The running example generalized:
three engineers (KV-cache, embedding index, direction-finder) hit the same wall
from three directions. Thesis stated: geometry/distortion/reliability are relational,
ill-posed until $(x, O, \text{channel}, B)$ are all named. The "one object, three
shadows" map as the book's spine.

**Ch. 2 — The Failure of Observer-Free Measurement [A].** Why reconstruction error
(MSE/PSNR/cosine) is the $P_C=I$ slice masquerading as a universal. NEG-2 (cosine
0.995, perplexity $10^4$) and NEG-4 as the motivating negatives. The category error:
measuring a compressor without naming its consumer.

**Ch. 3 — Historical Precursors [A].** Shannon and rate–distortion; reverse
water-filling; Amari–Čencov information geometry and the pullback metric (the
"we did not invent this object; we claim it is the operative one" positioning
paragraph, written once here and reused); von Luxburg–Radl–Hein resistance collapse;
Ng–Jordan–Weiss row-normalization as folk practice awaiting a reason.

### Part II — The Framework

**Ch. 4 — The Observer Triple $O=(C,G,B)$ [A].** Consumer, output metric, budget.
Worked instances from the consumer table (softmax attention, geodesic rank,
optimizer, retrieval, classifiers, recognizer): what each reads, what each discards.

**Ch. 5 — The Read Metric and the Quotient [A].** $P_C = J^\top G J$; range = read
subspace, kernel = nuisance; the quotient $X/\!\sim_C$; the sense in which the
observer *is* $P_C$ up to budget. GO-1's ex-ante identifiability claim previewed.

**Ch. 6 — Mathematical Preliminaries [A].** Pullbacks, projections, the read
distortion $\operatorname{tr}(P_C\Sigma_\delta)$; why magnitude of error ≠
downstream-relevant structure (the NEG-6 through NEG-9 lesson: the trace governs the
discriminating comparison but is not a complete rank statistic). Assumes linear
algebra + basic probability.

### Part III — One Object, Three Shadows

**Ch. 7 — COST [B].** The consumer rate–distortion function $R_C(D)$: achievability
+ converse; the tilt toward $P_C$; the two-observer region and refinability =
Loewner nesting; the $k$-chain; dispersion counts read dimensions; the mismatch tax
$(r/2)\log(M/m)$ and the omission floor $\operatorname{tr}(\tilde P\Pi)$. GO-6 as
the operational net (output ≤ surrogate ≤ reconstruction) [demonstrated]. Proofs to
Appendix B. *Source: Paper III (T-IT).*

**Ch. 8 — VALUE [B].** The flip, stated and bounded. The dissociation at matched
recon (GO-2) [demonstrated]/[replicated]; the 12-domain sweep spine; ZCA-whitened
codes win end-to-end. The one-sentence boundary that becomes Ch. 12: the flip needs
read/signal *misalignment* and a working consumer. *Source: Paper II + IV.*

**Ch. 9 — LEGIBILITY [B].** Keep-the-Angle. Angle carries geodesics where radius
carries density; the polar decomposition of the collapse theorem; row-normalization
justified; $\alpha=1$ response sign = $\ker P_C$ membership test; "dimension emerges
before shape" (Weyl ordering). The $S^1$ rank-collapse and the flat-torus bounds as
the exactly-solvable cases [proved]. *Source: Paper I + I.5.*

### Part IV — The Instruments

**Ch. 10 — The Blind Probe [A].** Recover $P_C$ from consumer outputs alone —
finite-difference the margin, no labels, no oracle (GO-1) [predicted]; the
real-consumer recovery on legal retrieval (035 miss → 036/039 hit); the
non-oracle 20-Newsgroups partial (041). What the probe can and cannot promise.

**Ch. 11 — The Recognizer [A].** Name the manifold or certify none; low multiplets
+ angular distances; dimension-before-shape. The certificate's vacuity threshold
(GO-3) [demonstrated] as the "single-stage retrieval dies here" line.

**Ch. 12 — The Failure Taxonomy and the $\kappa$ Law [A/B].** The four degeneracies
of $P_C$ as the complete list of ways the flip is absent (coupling / precondition /
identifiability / mechanism-absent). The $\kappa=\operatorname{tr}(\bar P_C\bar\Sigma_x)$
alignment law: flip magnitude decreasing in $\kappa$, $\kappa\to1$ the coupling null
(D4) [refuted-as-null], one sealed prospective point. Converts the boundary from a
bucket into a dial. *[A] for the taxonomy; the κ law's prospective point is [B].*

### Part V — The Evidence

**Ch. 13 — The Domain-Generality Sweep [A].** Twelve domains, three physics, one
compressor. Per-domain: arms, $n$, sealed bars, verdict, tier (sealed/qualified/
exploratory). The three-physics replication (radar D1 partial, acoustic D2/AV16.3 +
LOCATA, seismic D3 PDAR) as the headline; whale-dialect (038) and legal (036/039)
as the non-physical confirmations.

**Ch. 14 — The Falsifiable Core [A].** GO-1…GO-6 and Gate B, each with its class,
registry, harness, and replication count. How a claim moves between classes; the
out-of-sample gate (R-IND-6); why GO-B's gradient-curvature hit and Llama-keys
miss-then-rematch are *both* on the record.

### Part VI — The Discipline

**Ch. 15 — Registration-First [A].** Seal before measure (REG-1); ex-ante bars;
fresh-context adversarial verification (R-IND-1…6); theorem custody (proof +
harness + fresh pass); the standards-alignment table (OSF, ACM badging, Hypothesis,
Lean, CODECHECK) and the honest frontier gap — no mature toolkit for verifying
AI-assisted work independently of the assistant. The verification incidents VI-2…VI-7
as the rule earning its place.

**Ch. 16 — Honest Negatives [A].** NEG-1…NEG-14, carried at full prominence. The
uniform-in-$m$ commute-filter refutation (NEG-1); reconstruction-as-proxy (NEG-2);
the KV-keys ladder of refuted proxies (NEG-5…9) that located the *right* statistic;
the retrieval precondition (NEG-10); the density-quotient refutation (NEG-11); the
Gate-B real-model miss (NEG-12); the over-strict-gate correction (NEG-13 → resolved).
The stand-down clause: losing a bet narrows the claim; hiding it would end the program.

### Part VII — Horizons

**Ch. 17 — Open Problems and the Keystone Theorem [B].** The learn-then-serve
theorem T1 (probe sample-complexity ∘ mismatch bounds) as the COST↔VALUE bridge;
the channel dual and common-observation problem (named, not chased); the
cross-domain magnitude constant (open, per 041); the Green-rank positivity
conjecture from the LEGIBILITY leg.

**Ch. 18 — The Principle [B].** *Keep the structure the observer can use.* The
consumer-relative rate–distortion thesis as the "quantized Shannon" spine: COST /
VALUE / LEGIBILITY / identifiability as four faces of one consumer-relative theory,
with Shannon the $P_C=I$ slice. What the framework does and does not license.

### Appendices

- **A. Related Work and Differentiation [A]** — information geometry, rate–distortion,
  spectral methods, task-aware compression; what is old, what is the synthesis.
- **B. The COST Ledger [B]** — Thms B1–B3 (achievability / output-reduction /
  high-resolution) with proofs and the committed Blahut–Arimoto + falsification
  harnesses; the two-observer and rate-region theorems; constants/slack tables.
- **C. Reproduction Cookbook [A]** — environments, seeds, how to re-run each GO row.
- **D. The Registry [A]** — every `GO-P-2026-###` ID, gap-free disposition
  (reported / superseded / never-run-with-reason); the no-file-drawer accounting.
- **E. Skeptic's Appendix [A]** — objections and answers: "isn't this just
  task-aware compression?", "isn't $P_C$ just Fisher information?", "you fit the
  read operator", the AI-self-grading objection.
- **F. Mathematical Ledger [A]** — status of every formal claim, mirroring
  `claims/LEDGER.md`, one row per claim with its class and custody.

---

## Build / format notes

- Chapters are markdown in `chapters/`, math in `$…$` / `$$…$$` (KaTeX), consistent
  with the repo's existing convention and the series' pandoc→HTML pipeline.
- Consider mirroring `geometric-ethics`'s `.build/` (pandoc `-t html5 --katex`,
  split on `<h1>`, wrap in the shared Geometric-Series template) once the chapter
  set stabilizes, so this volume serves at the same look as the others.
- Every table/figure gets a claim ID resolving to `claims/LEDGER.md` (Appendix F).
- **Heredoc backslash gotcha:** author all math-bearing files with the Write/Edit
  tools, never bash `<<'PY'` heredocs (they corrupt `\` → control chars).
