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

### Abstract (draft)

> Signals are almost universally compressed to minimise reconstruction error, on the assumption that a
> more faithfully reconstructed signal better serves whatever reads it next. For a consumer that reads only
> part of what a signal carries, this assumption is directionally wrong: downstream error is governed not
> by the total reconstruction error but by its projection onto the consumer's *read operator*. A code that
> spends a fixed budget minimising reconstruction spends it largely on directions the consumer ignores; a
> code that instead protects the read directions reconstructs the signal worse yet serves the consumer
> better — a dissociation we call the **flip**. We test the flip under a single pre-registered protocol
> across twelve domains spanning three distinct physics: direction finding on automotive radar,
> microphone, and seismic arrays; the attention keys of a language model; and learned classifiers of moral
> judgment, music genre, and sperm-whale dialect. The flip reproduces wherever the consumer's read operator
> is **identifiable** — given by the geometry, or recovered blind from the consumer by probing what its
> output is sensitive to — and fails, informatively, exactly where the read operator is coupled to the
> signal's own energy or the consumer does not function. Which code best exposes the flip is set not by one
> statistic but by two axes of the representation's geometry, a diagnostic that also selects the code at
> deployment. Reconstruction fidelity is the special case of a consumer that reads everything; observation,
> in general, is selective — and compression should be too.

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

### Methods (draft)

**A domain-general protocol.** Every domain is tested by the same design. On the domain's native
representation we build **three codes at matched total bits per sample**: a *read-preserving* code (R)
that allocates bits to the consumer's read directions; a *reconstruction-optimal* code (O) that minimises
reconstruction error (Lloyd–Max, or the reconstruction-optimal bit allocation); and an *anti* code (A)
that destroys the read directions. The consumer is the domain's own mature estimator, independent of the
compressor. For each held-out instance we record the **downstream error** (the consumer's task error) and
the **reconstruction error**. The per-instance **flip** is `error(R) ≤ error(O) + tol` *and*
`reconMSE(O) ≤ reconMSE(R)` — O reconstructs better yet is downstream-worse; the **anti check** is
`error(A) ≥ max(error(R), error(O))`. All configuration is chosen on a **calibration split** and frozen
before the **held-out** run; each domain is pre-registered (a content hash sealed and git-timestamped
before any held-out instance is scored), and outcomes are recorded regardless of sign.

**The read operator and its provenance.** The consumer's read operator `P_C` enters three ways.
*Geometric* — for sensor arrays it is the array-manifold derivative orthogonalised against the steering
vector, `ĝ = P_a^⊥ a′(θ₀)`, known in closed form. *Planted* — in the synthetic and LLM-rematch anchors it
is constructed from a known subspace and the prediction made blind to it. *Recovered* — on real learned
representations it is obtained by the **blind probe**: perturb the consumer's input and read its output
sensitivity. For a cosine-ranking consumer the margin sensitivity is `∂cos(a,b)/∂b ≈ â − cos(a,b)·b̂` (the
query component orthogonal to the item), and the read operator is the top-*r* eigenspace of
`S = ⟨g gᵀ⟩` — low-rank for robustness, with *r* and the rate selected on an internal calibration split so
only a configuration that already generalises once is sealed.

**The three matched-bit codes.** For the array/DOA and gradient domains, R/O/A are the bit-identical
PolarQuant (angle-favouring) / Lloyd–Max / phase-destroy triple. For embedding consumers, all three
quantise in a fixed eigenbasis over a shared per-direction range at equal total bits, differing only in
allocation (bits by read-importance / by reconstruction variance / by the anti weight). Matched bits are
audited (spread ≤ 1–2%).

**The (A2) regime diagnostic.** For embedding consumers we additionally run `probe_quotient` (turboquant-
pro): at matched bits it applies a polar (angular), a per-channel (reconstruction-oriented), and a
ZCA-whitened proxy code and reports the Spearman rank agreement of the *declared consumer's* scores under
each. Two summary statistics characterise the regime: `tangential_fraction` (≈1 ⇒ an angular consumer)
and `median_unit_displacement` (√2 ⇒ isotropic directions; small ⇒ a concentrated offset cone).

**Domains and data.** *Arrays* — a simulated λ/2 ULA; LOCATA (8 cm nested ULA, OptiTrack ground truth);
AV16.3 (8-mic circular array, camera-tracked 3-D mouth); PDAR (13-element IMS seismic array, USGS
catalogue back-azimuth, 34 teleseismic events); RaDICaL (8-element 77 GHz FMCW virtual array). *Neural* —
Llama-3.2-3B attention keys (layers 8/16); a logistic-regression training step (loss Hessian as the read
metric). *Learned representations* — CourtListener citation pairs with LaBSE (cosine ranking); ETHICS
commonsense with a bert-base classifier fine-tuned to 0.74 (frozen embeddings sit at chance); FMA music
with CLAP-PCA embeddings and a genre classifier; sperm-whale codas (DSWP / Sharma 2024) with a
clan/dialect classifier on the inter-click-interval rhythm. *Statistics.* Flip fractions are on held-out
instances (disjoint recordings/events/opinions where obtainable); bootstrap over query subsets for the
retrieval/classifier consumers; the pre-existing music sign-flip carries a 6σ / Bonferroni gate.

### Results (draft)

**The flip reproduces across three physics.** On the physical arrays it holds under the mature
subspace estimator and against independent ground truth: LOCATA **11/13** held-out recordings with the
reconstruction-trade at **13/13** (Lloyd reconstructs better every time yet is downstream-worse); AV16.3
**74%** of held-out windows with recon-trade **100%** and anti-worst **76%**, scored against the
camera-tracked angle on *disjoint* recordings; PDAR seismic back-azimuth **76%** of held-out events,
recon-trade **100%**, anti **76%**, against catalogue ground truth. The synthetic anchor flips 6/6 under
two independent estimators; the Llama-3.2-3B key consumer shows the read-operator-projected error
predicting the softmax-KL loser on **16/16** heads while exactly-tied reconstruction cannot. The battery's
pre-registered prediction — a flip in ≥2 of its three core prospective domains — is met by the two
confirmed arrays.

**Recovering the read operator makes the flip transfer.** On real legal-citation retrieval an *estimated*
read operator (document covariance) overfits: on held-out opinions reconstruction-optimal *beats*
read-preserving (AUROC 0.773 vs 0.757), a registered miss. Replacing it with the blind-probe read
operator — the only change — reverses the verdict on the identical held-out set (read-preserving 0.779 vs
reconstruction-optimal 0.771; flip on **200/200** bootstraps) while reconstruction-optimal still
reconstructs 2.6× better. Moral judgment shows the consumer precondition: frozen sentence embeddings
classify at chance (0.58–0.60 vs 0.63 majority) and the flip is ill-posed; a classifier fine-tuned to 0.74
makes it appear (the angular code preserves the class logit at 0.994 vs the reconstruction-oriented code's
0.956 at 1 bit).

**Two boundary conditions bound the claim.** Gradient compression under a curvature metric is the
*coupling* boundary: the anti-probe is worst on **300/300** held-out steps — the Hessian read operator
genuinely governs the update — yet the subtle read-vs-reconstruction flip sits at chance (**27%**), because
the high-curvature and high-gradient-energy directions coincide (both from `XᵀX`), so reconstruction
already protects the read directions. No read-operator recovery can rescue it; the read operator was
already exact. Radar is the data limit: the flip and reconstruction-trade hold **25/25** on real 77 GHz
FMCW returns, but the anti control reaches only 60% on the 8-element array and the disjoint-recording
held-out is inaccessible (the full set is 310 GB) — recorded as a partial, not inflated to a confirmation.

**The winning code is set by two axes, and no single statistic suffices.** Characterising every embedding
consumer with `probe_quotient` places them on two independent axes — direction concentration and
cross-channel correlation. Music (isotropic, low correlation) is preserved by the generic angular code and
reconciles the pre-existing 6σ music sign-flip; legal (concentrated, channel-structured) needs the
per-channel or blind-probe code; post-RoPE keys and sperm-whale codas both need the whitened code, but for
different reasons — the keys are concentrated-correlated, the codas isotropic-correlated (their inter-click
intervals are temporally correlated). Whale is the decisive case: isotropic like music yet whitening-
dependent like the keys, so a single concentration statistic cannot predict it — indeed a pre-registered
`unit_displacement` threshold is refuted on its first out-of-sample test. The whitened code, added to the
diagnostic here, wins at every bit budget on the codas (0.83 / 0.85 / 0.97 vs the per-channel code's
0.41 / 0.80 / 0.89) — the clearest of the correlated-regime gains.

### Discussion (draft)

**What is established, and at what tier.** The load-bearing result is **five sealed confirmations across
three distinct physics** — synthetic, LLM attention, and the LOCATA / AV16.3 / PDAR arrays — each scored
on held-out data against independent ground truth under a pre-registered protocol. Around them the sweep
carries, and labels, weaker evidence: one **partial** (radar, where the flip and reconstruction-trade
hold 25/25 but the anti control and a disjoint held-out are data-limited), one **sealed null** (gradient
compression), and three **exploratory reconciliations** (KV-keys, music, whale). Each wears its tier. We
draw this line deliberately, because it is what lets a reader trust the confirmations without re-running
them: the same registration machinery that seals a confirmation also makes an exploratory row *legible as
exploratory*.

**The flip and the (A2) verdict are not the same claim.** We reserve *flip* for the two-metric
dissociation established by the sealed protocol — read-preserving coding beats reconstruction-optimal
coding on the downstream task *while* reconstruction-optimal coding reconstructs the signal better. The
**(A2) verdict** is a distinct, one-metric quantity: which quantizer family (angular, per-channel, or
whitened) best preserves the consumer's rank ordering at matched bits. A verdict is *evidence consistent
with* the flip — it shows the read-aligned family is preferred — but it does not by itself establish the
reconstruction-trade, and it is not a sealed flip. The exploratory rows report verdicts; the confirmations
report flips; the two terms are kept apart throughout.

**The failure taxonomy is what makes this a theory rather than a demonstration.** A demonstration shows
only the wins. What bounds a claim is where it *fails*, and the four failure kinds do exactly that:
**identifiability** (the read operator mis-estimated — fixable by recovery), **coupling** (the read
operator intrinsically aligned with the signal's energy — a wall), **precondition** (no working consumer),
and **mechanism-absence** (a genuine refutation). The gradient-compression null is the coupling boundary's
empirical face: the anti-probe is worst on 300/300 held-out steps, so the read operator plainly governs
the task, yet the flip cannot appear because reconstruction already protects the read directions. And the
two-axis refutation — a single summary statistic pre-registered as the regime predictor and refuted on its
first out-of-sample test — is what forces the regime to be characterised, not asserted. Together these let
the theory state, before any experiment, which domains admit the flip and which code exposes it.

**Identifiability, made constructive.** One rarely has a consumer's read operator in closed form. The
blind probe recovers it from the consumer's own output sensitivity, and on real legal-citation retrieval
this is the difference between a miss and a confirmation on the *same* held-out set. This is the practical
core of the identifiability face: the flip is available on any real learned representation whose consumer
can be probed.

**Convergent evidence, and the information-theoretic frame.** That reconstruction fidelity is the special
case `P_C = I` — a consumer that reads everything — places the flip inside rate–distortion theory as its
consumer-relative generalisation. Independent arrival at the same object is telling: a bioacoustics
decoder-robustness index, developed for whale communication, measures precisely read-operator distortion
(invariant acoustic transforms leave the decoder's read unchanged; stress transforms move it), i.e. the
same methodology reached from a different field.

**Limitations.** The three reconciliations are (A2) verdicts, not sealed flips; radar is data-limited; each
domain uses a single model and dataset; the audio-level decoder-robustness measurement was not run. To
keep the two-axis map from resting entirely on exploratory verdicts, one exploratory domain — the codas,
the load-bearing isotropic-yet-correlated cell — is promoted to a sealed flip (its own pre-registration
and held-out confirmation), so the map's novel axis is anchored by a confirmation rather than a verdict.
The remaining reconciliations are left explicitly as the exploratory frontier.

**Outlook.** The operational reading is direct: for compression under a known consumer, *measure the
regime and adapt the code* — certify what the consumer reads rather than promise reconstruction. There is
no universal code; there is a diagnostic, on two axes, and a selector that reads it.

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
