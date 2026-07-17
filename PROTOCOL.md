# Geometric Observation — Test Protocol

> The empirical program of **Observation Theory**.

**Status:** draft v0.1 — adopt (with bars filled in) before any book-cited run
**Scope:** governs every empirical and mathematical claim in *Geometric Observation* (book) and its companion claim ledger.
**House rule:** the book may not assert what the ledger cannot show.

Inherits: PREREG_RUNG discipline (dated amendments, registered before runs), CLAIMS.md
ledger pattern, sentinel-delimited result JSONs, reproducibility tiers.

---

## The framework: Observation Theory

**Observation Theory** is the thesis that **geometry, distortion, and reliability
are properties of the _observation_ — the consumer's read operator, budget, and
channel — not of the object observed.** *Geometric Observation* (this book) is its
empirical program; the falsifiable core (GO-1…GO-5) tests its faces.

Its formal engine is a **consumer-relative rate–distortion–capacity theory**:

- **distortion** — the operative distortion is `tr(P_C · Σ_δ)`, the reconstruction
  error `Σ_δ` seen through the consumer's read operator `P_C` (GO-2);
- **identifiability** — `P_C` is recoverable ex ante from the consumer functional
  alone, blind (GO-1);
- **capacity** — single-stage observation has a vacuity threshold below which it
  fails (GO-3);
- **rate** — the observer's mode/bit budget sets a rate whose allocation flips the
  verdict (GO-4).

Classical error theory (least-squares adjustment of observations) and Shannon
rate–distortion are its **task-agnostic limit** — the `P_C = I`, single-budget
corner where the observer is assumed to read every direction equally. The claim
Observation Theory adds is that no real consumer does, and that the correct
distortion, rate, and capacity are all consumer-relative and computable.

*The name is load-bearing only where the ledger is:* no result earns it until its
row meets its class bar (§1). This section states the frame; §§2–6 keep it honest.

---

## 0. Objects

- **Claim ledger** (`claims/LEDGER.md`) — one row per book claim; every table/figure in
  the book carries a claim ID resolving here.
- **Prediction registry** (`prereg/`) — dated, hashed entries written *before* the first
  measurement they govern. Amendments allowed only dated-and-logged before unblinding.
- **Instance** = (representation X, consumer O, compressor family Q).
  Example: (post-RoPE keys, softmax attention, {PolarQuant, PerChannelKV, asym-NF4}).
- **Consumer metric** d_O(x,x′) := d_Y(O(x), O(x′)) — always *measured* on the actual
  downstream functional, never assumed from the representation's ambient metric.
- **Probe** — the ex-ante procedure that proposes, for a given consumer, the
  invariant/nuisance split (what must be kept, what may be quotiented). §3.

---

## 1. Claim classes

| Tag | Meaning | Minimum evidence |
|---|---|---|
| `[proved]` | theorem | complete written proof + logged independent line-by-line verification; constants/slack table; known-gap notes |
| `[demonstrated]` | pre-registered experiment | registry entry predating run; Tier A/B reproduction; committed result JSON; CI green |
| `[replicated]` | held in ≥2 independent settings | independent models/datasets/domains; cluster-aware statistics |
| `[predicted]` | out-of-sample, registered in advance | §4 gate rules; blinded where feasible |
| `[exploratory]` | suggestive only | labeled in-text; cannot support the umbrella principle |
| `[refuted]` | negative result | reported in the book with the same prominence as positives |

**Rule 1.1** — The umbrella principle (Ch. 11) may cite only `[proved]`, `[replicated]`,
and `[predicted]` rows.
**Rule 1.2** — The Honest Negatives chapter is mandatory and carries every `[refuted]`
row, including any failures of §2 below.

---

## 2. The falsifiable core (GO-1 … GO-5)

The framework is tautology-shaped ("success for O means preserving what O
distinguishes" is true by construction) unless specific claims are put at risk.
These five are the risk-bearing claims. Each gets its own registry entry and bar.

### GO-1 — Identifiability (ex ante)
*The consumer's invariant/nuisance split can be identified from the consumer
functional before any downstream failure is observed.*

- **Test (retrospective, blinded):** re-implement the probe fresh, run it on the three
  known instances (attention keys, MoE gates, SSM decay) with no consumer-specific
  tuning; it must recover per-channel scale / margin structure / log-τ respectively.
- **Test (prospective):** the three-arm design of §3 on ≥1 novel instance.
- **Falsified if:** the probe fails the blinded recovery, fails to predict the
  prospective ordering, or passes the shuffled-consumer control (§3.5) — i.e., "explains"
  consumers that don't exist.

### GO-2 — Transfer (quotient-(A2))
*Downstream preservation is controlled by two-point tangential noncollapse in the
consumer quotient, not by reconstruction error.*

- **Test:** per instance, across ≥4 compressor variants at matched bits, regress the
  downstream outcome on (i) quotient-tangential distortion and (ii) reconstruction
  distortion; (i) must dominate (registered margin, clustered CI).
- **Falsified if:** reconstruction error predicts downstream outcome at least as well
  on ≥2 instances.

### GO-3 — Certificates and vacuity
*τ ≥ 1−2μ̂(κ) is `[proved]`; the risk-bearing claim is that the certificate's vacuity
threshold predicts where single-stage retrieval dies and rerank becomes mandatory.*

- **Test:** ≥5 corpora spanning a range of distance concentration; the registered
  operational "rerank-required" boundary must be ordered by μ̂(κ) at fixed κ.
- **Falsified if:** ordering fails beyond clustered CI.

### GO-4 — Budget/wavelength
*Fixed-budget verdicts invert under budget-matched observation, in the direction the
spectral-wavelength mechanism predicts, in ≥1 substrate beyond Paper I §5.10.*

- **Falsified if:** inversion absent or reversed at registered n.

### GO-5 — Nuisance quotient
*An α=1-style density/hubness quotient restores invariant fidelity in ≥1 non-spectral
domain (e.g., locally-scaled ADC retrieval).*

- **Falsified if:** correction effect ≤ 0 at registered n.

**Standing `[refuted]` rows carried into the book regardless:** fixed-scale
uniform-in-m bi-Lipschitz for the commute filter (Prop. weyl); reconstruction cosine as
a proxy for key quality (ppl 10⁴ at 0.995); heat-taper reversal on BGE-M3 (pending
C2.1 confirmations); plus any GO-1…5 misses.

---

## 3. The three-arm instance design (the workhorse)

Run for every instance (X, O, Q-family) the book cites as evidence.

1. **Register first** (before any downstream measurement): the consumer functional and
   its measured d_O; the probe's output — proposed invariant I_O and nuisance N_O; the
   predicted failure class of the naive compressor (current catalog: radial
   displacement · direction concentration · per-channel offset/DC · margin flip —
   extend by amendment); the predicted ordering of the three arms on the downstream
   metric; n, stopping rule, success bar.
2. **Arms (matched bits, audited):**
   - **(a) invariant-preserving** — fidelity allocated to I_O;
   - **(b) reconstruction-optimal** — minimizes ‖x−Q(x)‖ at the same budget;
   - **(c) anti-probe control** — preserves N_O at the expense of I_O
     (the wrong quotient, on purpose).
3. **Measure** the downstream metric only (perplexity / LongBench / recall@k /
   route agreement / task score). Reconstruction is reported but never scored.
4. **Score:** hit = registered ordering a ≻ b ≻ c on the downstream metric with
   clustered CI excluding reversal of a vs c. Partial-credit rules registered in
   advance; anything else is a miss and enters the ledger as such.
5. **Controls:**
   - **Shuffled-consumer specificity** — run the probe against a permuted/synthetic
     consumer; it must *not* return the same split (guards against a universal probe).
   - **Matched-bits audit** — equal-total-bits accounting verified in an external
     harness where available (llama.cpp-style), not only in-library.
   - **Noise floor** — behavioral-agreement metrics reported against the fp16-vs-fp16
     rerun floor, per the practice paper's convention.

---

## 4. The out-of-sample gate (book Gate B)

- **Domain disjointness:** not spectral graph embeddings, not KV keys/values, not MoE
  gates, not SSM decay, not text-retrieval embeddings — nothing already in Papers I–II.
- **Candidate pool** (register ≥1 choice + rationale): optimizer moments (Adam m/v)
  under compression; distributed-training gradient compression; LoRA adapter deltas;
  graph-transformer positional encodings; audio-codec latents; recommender
  embeddings; neural population codes (public datasets).
- **Discipline:** the full §3 design; the registry entry predates *any* real-data
  pilot in that domain (synthetic pilots only, and logged).
- **Gate:** ≥1 prospective hit. A miss is a `[refuted]` row and narrows the umbrella's
  stated scope in Ch. 11 — the book proceeds either way, but its thesis text differs.
  This is written down now so the outcome cannot silently soften the claim later.

---

## 5. Statistical standards

- **Clustering:** resample at the independent unit (rules over seeds; models over
  tasks; corpora over queries). Report naive and clustered; claims live on clustered.
  Fewer than 8 clusters ⇒ mandatory few-cluster caveat; wild-cluster bootstrap where
  feasible.
- **Pair-resampling CIs** are optimistic floors (shared anchors) — label as such.
- **Errors-in-variables** note whenever the abscissa is estimated.
- **Multiplicity:** GO-1…5 and the vignette battery follow a registered family-wise
  plan (Holm within each family). Exploratory sections exempt but labeled.
- **Effect floors:** registered minimum effect sizes, not just sign
  `[set at registration]`.
- **No optional stopping;** n and stopping rules in the registry entry.

---

## 6. Reproducibility tiers (inherited, binding)

- **Tier A** — CPU/Colab one-click notebook per claim; committed sentinel-delimited
  result JSON; CI reruns the canonical subset on every tagged release.
- **Tier B** — cluster required; scripts, configs, seeds committed; results committed.
- **Tier C** — not externally reproducible ⇒ `[exploratory]` only; never load-bearing.
- **Pinning:** lockfiles; data vendored or DOI-archived (the ~10 MB embedding-export
  rule); the book cites only tagged releases with DOIs; datasets by version.

---

## 7. Theorem verification protocol

- Every `[proved]` item: complete written proof; ≥1 logged independent line-by-line
  verification (verifier, date, findings — e.g., "B=√2 slip found, fixed");
  constants/slack table; known-gap notes (e.g., twin-mode "every eigenvector" scope).
- Elementary results (prop:rank; the transfer-theorem core) queued for optional
  machine-checking; status tracked in the ledger, never claimed until green.
- **Rule 7.1** — the generalized quotient transfer theorem (Paper III) must be
  `[proved]` before Ch. 11 states the umbrella principle as more than a conjecture
  schema.

---

## 8. Chapter → claim map (skeleton; fill as chapters draft)

| Ch. | Claims | Class target | Source of record |
|---|---|---|---|
| 4 Angular Observer | keep-the-angle battery (core table, bake-off, screen, scaling law, α=1) | `[proved]`/`[demonstrated]`/`[replicated]` | Paper I + book-repo CI subset |
| 5 Manifold recognition | dimension consensus, ω-screen as instrument | `[demonstrated]` | Paper I |
| 6–7 Compression as observation | keys/values asymmetry; certificates; probe | `[replicated]`/`[predicted]` | Paper II + §3 runs |
| 8 Scale: signal vs nuisance | the 2×2 (radius-nuisance: manifolds, hubness · scale-signal: keys, margins) | `[replicated]` | I §5.8, App. moral; II keys/gates |
| 9 Phase transitions | operational collapse thresholds (registered change-point definitions) | `[demonstrated]` | II (GQA cliff, margin flips) + new |
| 10 Bounded observers | budget inversion + wavelength mechanism | `[replicated]` (needs GO-4) | I §5.10 + one new substrate |
| 11 The principle | umbrella statement | conditional on GO-1…5 ∧ Rule 7.1 | — |
| Honest Negatives | all `[refuted]` rows | mandatory | — |

---

## 9. Adversarial arm

Standing internal effort plus public invitation to construct:
(i) a consumer whose quotient the probe misidentifies;
(ii) an instance where the reconstruction-optimal arm beats the invariant-preserving
arm downstream at matched bits.
Any success ⇒ `[refuted]` row + framework-revision note. Attempts are logged,
including failures — the absence of counterexamples is only evidence if the search
is visible.

---

## 10. External replication

- Each flagship `[demonstrated]`/`[predicted]` claim ships a public one-click notebook
  and a call for replication; ≥1 independent replication (or its documented absence)
  recorded before the book's final draft. Failures downgrade the claim before print.
- Post-publication, the ledger is the living erratum; the book's tables carry claim
  IDs that resolve to it.

---

## 11. Gates (sequencing)

- **Gate A** — Paper I published/accepted; Paper II consolidated with C2.1
  confirmations done; Paper III `[proved]`.
- **Gate B** — §4 out-of-sample result recorded (hit, or miss + narrowed thesis).
- **Gate C** — ledger complete for Ch. 4–10; CI green on tagged releases; external
  replication status recorded.
- Drafting begins at A ∧ B; final draft requires C.

---

## 12. Templates

### 12.1 Prediction-registry entry (`prereg/GO-<id>-<slug>.md`)

```yaml
id: GO-P-2026-###
date: YYYY-MM-DD          # must predate first governed measurement
instance:
  representation: ...
  consumer: ...            # functional + how d_O is measured
  q_family: [...]
probe_output:
  invariant: ...
  nuisance: ...
  predicted_failure_class: radial-displacement | direction-concentration | dc-offset | margin-flip | other(amend)
prediction:
  arm_ordering: a > b > c on <downstream metric>
  effect_floor: ...        # [set at registration]
design:
  n: ...
  clusters: ...            # independent unit
  stopping: fixed-n
  bits_matched_via: ...    # external harness
controls: [shuffled-consumer, noise-floor]
amendments: []             # dated, pre-unblinding only
hash: sha256:...
```

### 12.2 Ledger row (`claims/LEDGER.md`)

```
| ID | Claim (one sentence) | Class | Chapter | Registry | Notebook | Result JSON | Tier | CI | Replications | Notes |
```

### 12.3 Probe output schema

```yaml
consumer: ...
quotient:
  kept: ...                # e.g., per-channel affine; top-k margins; log-τ coords
  discarded: ...
  justification: ...       # derived from the consumer functional, not from outcomes
tangential_metric: ...     # the (A2) quantity in the quotient
specificity_check: pass|fail   # shuffled-consumer control
```

---

*v0.1 open parameters to fix at adoption: numeric bars in GO-1…5 and §3.4; the §4
domain choice; registry location (book repo aggregating per-project prereg/ dirs, or
centralized).*
