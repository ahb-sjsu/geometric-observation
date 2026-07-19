# Placement drafts — the domain-generality sweep across three venues

Source of record: `DOMAIN-GENERALITY-SWEEP.md` + `results/`. Three homes, three jobs: a **standalone
empirical paper** (reach), a **subsection of the TurboQuant-Pro foundation paper** (engineering), and the
**domain-generality chapter of the Observation Theory volume** (rigor).

---

## 1 · Standalone paper — intro + figure plan

**Working title.** *Preserve what the reader reads: a dissociation between reconstruction and downstream
fidelity across acoustic, seismic, neural, and biological signals.*
(Alt: *The reconstruction fallacy is domain-general.*)

**Target register.** Broad-audience empirical (Nat. Commun. / PNAS / Sci. Adv.) — the memorable object is
the *breadth*, not any single derivation.

### Introduction (draft)

> Almost every system that compresses a signal is judged by how faithfully it can reconstruct it —
> mean-squared error for images, perplexity-blind cosine similarity for embeddings, PSNR for audio. The
> assumption underneath is so ingrained it is rarely stated: that a code which reconstructs the signal
> better is a code that serves whatever reads the signal next better. For a decoder that consumes only
> part of what the signal carries, this assumption is not merely loose — it is *directionally wrong*.
>
> The quantity that governs a consumer's downstream error is not the total reconstruction error
> `tr(Σ_δ)` but its projection onto the consumer's **read operator**, `tr(P_C·Σ_δ)` — the error in the
> directions the consumer actually reads. When a fixed bit budget is spent to minimise reconstruction, it
> is spent largely on directions the consumer ignores; a code that instead protects the read directions
> reconstructs the raw signal *worse* yet serves the consumer *better*. We call this dissociation the
> **flip**: at matched bits, read-preserving coding beats reconstruction-optimal coding on the downstream
> task, precisely while reconstruction-optimal coding wins on reconstruction. The two fidelities move in
> opposite directions.
>
> The flip was first isolated in two narrow settings — the direction of arrival read by a sensor array,
> and the keys read by softmax attention in a language model — where it could be dismissed as an artifact
> of the geometry. Here we ask whether it is instead a **property of observation**. We test the same
> matched-bits dissociation, with the same discipline (each configuration frozen on a calibration split
> and scored on held-out data, every outcome pre-registered and reported regardless of sign), across
> twelve domains spanning three distinct physics — direction finding on automotive radar, hearing-aid
> microphone arrays, and a seismic array reading earthquake back-azimuth; the attention keys of a
> transformer; a fine-tuned moral-judgment classifier; music genre and, strikingly, the dialect of sperm
> whales in their click-rhythm codas.
>
> The dissociation reproduces across all three physics and every consumer type wherever a single condition
> holds: the **read operator is identifiable** — given by the geometry, or recovered blind from the
> consumer by probing what its output is sensitive to. Where it is not identifiable, or where it is
> *coupled* to the signal's own energy (as it is for gradient compression under a curvature metric, whose
> high-curvature and high-energy directions coincide), the flip provably cannot appear — and it does not.
> These failures are not noise; they are the theory's scope conditions, and they let us state, before any
> experiment, which domains admit the flip and which encoding best exposes it. That predictor turns out to
> live on two axes — how *concentrated* a representation's directions are and how *correlated* its
> channels are — and no single summary statistic (we pre-register one and refute it) can stand in for the
> full two-axis diagnostic.

**Contributions (bulleted, for the intro's close).**
1. The flip demonstrated as **domain-general** — ≥5 domains, ≥3 physics, non-physical consumers — under
   sealed pre-registration.
2. A **blind read-operator probe** that recovers what a consumer reads without its ground truth, turning
   a failed retrieval test into a confirmation (the identifiability boundary made constructive).
3. A **two-axis regime map** (concentration × correlation) that predicts the winning code per domain, with
   a validated diagnostic and a refuted single-statistic shortcut.
4. **Honest negatives as boundary conditions** — coupling, precondition, mechanism-absence — that bound
   the claim precisely rather than inflate it.

### Figure plan

| Fig | Title | Content | Makes the point |
|-----|-------|---------|-----------------|
| **1** | The dissociation | (a) schematic: signal → lossy code → consumer, with `P_C` shading the read directions; (b) one exemplar domain (LOCATA): reconstruction error ↓ and downstream DOA error ↑ as bits shift from read-preserving to recon-optimal — the crossing. | Defines the flip in one panel; `tr(P_C Σ_δ)` vs `tr(Σ_δ)`. |
| **2** | Domain sweep | forest/grid of all 12 domains grouped by physics (synthetic · EM/radar · acoustic · seismic · neural · biological), plotting held-out flip fraction with CIs; confirmed/partial/negative encoded by colour + marker. | The breadth — the memorable image. |
| **3** | The read operator, recovered blind | legal retrieval: estimated-covariance read op (miss, O>R on held-out) vs GO-1 blind-probe read op (hit, R>O) on the *same* held-out; recon-trade bar alongside. | Identifiability is the fixable failure. |
| **4** | Where the flip cannot appear | two panels: D4 coupling (anti-probe robust 300/300 while the subtle flip sits at chance — read op governs the task but is energy-coupled); moral precondition (flip fraction vs consumer accuracy — appears only once the classifier works). | The scope conditions, shown not asserted. |
| **5** | The two-axis regime map | 3×2 grid (concentration × correlation), domains placed, cells coloured by winning code (polar / whitened / per-channel); inset: the refuted single-statistic shortcut (unit_disp) mispredicting the correlated-isotropic cell. | Two axes, not one; the diagnostic that decides the code. |
| **6** | The biological case | sperm-whale codas: example ICI rhythm; the read-operator-distortion (DRI) framing; whitened-code win across bit budgets. Doubles as the paper's "reach" figure. | The dissociation reaches animal communication. |

---

## 2 · TurboQuant-Pro foundation paper ("Keep the Geometry")

**Placement.** *Not* a new domain — the sweep **upgrades an existing contribution.** §cert already ships
"a consumer-metric probe that reproduces the keys catastrophe at calibration time"; §laws already gives
"two empirical laws with their boundaries." The sweep promotes the (A2) probe from a **one-incident
detector** to a **validated, two-axis regime diagnostic with an adaptive family selector and a new code
family** — the practical engineering result. Scope it to the paper's remit (KV caches + retrieval
embeddings); the full cross-domain evidence is cited to the companion empirical paper.

**Draft subsection — "§cert.x  From incident to diagnostic: the (A2) probe generalises."**

> The keys catastrophe (§keys) motivated the (A2) probe as a calibration-time guard: run each candidate
> family's quotient on a sample, measure the *declared consumer's* rank agreement, and refuse polar when
> it collapses. We now show the same probe is a general **regime diagnostic**. Across the compression-
> relevant regimes — post-RoPE attention keys (attention-logit consumer) and retrieval embeddings (cosine
> consumer) — `probe_quotient` recovers *which* family the geometry demands, and the answer is governed by
> two independent axes: **direction concentration** (a shared offset squeezing directions into a cone, the
> keys regime) and **cross-channel correlation** (structure the per-channel/diagonal code cannot remove).
> Concentration alone is not sufficient — a single summary statistic we pre-registered as a predictor is
> refuted on its first out-of-sample test; the family verdict requires the full end-to-end probe.
>
> This exposes a gap the two shipped families (polar, per-channel) leave open: the *correlated* regime,
> where per-channel removes per-channel scale but not cross-channel correlation. We add a third candidate —
> a per-vector polar quotient applied in a **ZCA-whitened basis** — which closes it: on real post-RoPE
> keys it edges both polar and per-channel at matched bits. The runtime policy (§system) selects among the
> three per deployment, and the streaming quality monitor tracks the (A2) statistic for drift. *The
> domain-dependence of the right code is not a gap to close with a universal quotient; it is why the
> selector exists.* (The same probe, applied beyond compression — moral, music, and bioacoustic consumers —
> is reported in the companion empirical study; here it stays within KV/retrieval.)

**Concrete deltas to the paper.**
- Contributions list: extend the §cert bullet — "…a consumer-metric probe that reproduces the keys
  catastrophe **and generalises to a two-axis regime diagnostic with a ZCA-whitened third family and
  adaptive per-domain selection**."
- Abstract: after "reproduces the keys catastrophe at calibration time," add "…and, generalised, selects
  among polar, per-channel, and a whitened family by a two-axis regime diagnostic."
- One new figure: the probe's polar/per-channel/whitened rank agreement vs bits on post-RoPE keys +
  retrieval embeddings (the compression-scoped slice of Fig 5 above).
- Cite the merged instrument change (PR #159) and the companion empirical paper.

---

## 3 · Observation Theory volume — the domain-generality chapter

**Role.** The empirical spine: it validates two of the theory's faces at once — **GO-2** (the flip /
distortion face) across domains, and **GO-1** (identifiability) *on real consumers*, which was the standing
"next hardening." Pairs directly with the Honest Negatives chapter: the four failure kinds are the
theory's **scope conditions**, stated as theorems-with-boundaries, not anecdotes.

**Outline.**
1. **The claim, restated for breadth.** `tr(P_C·Σ_δ)`; the flip; why reconstruction is the `P_C = I` slice.
2. **The sweep, in full rigour.** All 12 rows with the sealed-prereg / calibration-frozen / held-out
   discipline; the anchors; the battery (GO-P-2026-034) prediction and its outcome; per-domain methods.
3. **GO-1 hardened on real consumers.** The blind probe: legal 035→036 as the worked example; moral;
   why an *estimated* read operator overfits and a *recovered* one generalises.
4. **The scope conditions (with Honest Negatives).** Identifiability / coupling / precondition /
   mechanism-absence as the four ways the flip fails, each an instance the ledger carries; D4 as the
   coupling theorem's empirical face.
5. **The regime map.** Two axes; the refuted single-statistic shortcut (NEG-14) as a discipline anecdote;
   the (A2) probe as the bridge to the engineering volume.
6. **Synthesis.** Observation theory ↔ the compression engine as one object; the DRI = Bond Index
   instance; the flip as a property of observation wherever the read operator is identifiable.

**Reuse.** The chapter's figures = the standalone paper's Figs 1–6 at full resolution; its prose is the
long-form of the standalone intro; the ledger rows are the chapter's claim IDs. Write the standalone first
(tightest telling), then expand into the chapter; carve the §cert.x subsection into the foundation paper.
