# Appendix G — A Hub-Mechanism Catalog: One Scalar, Many Observer-Induced Geometries

Hubness is the cleanest field instance of this book's category error. In a
high-dimensional embedding corpus a few points appear in *hundreds* of other
points' $k$-nearest-neighbour lists while most appear in almost none; the standard
one-number summary is the skewness of that occurrence count (the `count_skew`
scalar). This appendix catalogues what that scalar *hides*. Every entry is a
distinct **observer-induced quotient geometry** — a different way of arranging a
corpus under a metric — and several of them produce the *same* skewness reading.
The scalar is the reconstruction cosine of Chapter 2 wearing a different costume: a
blind aggregate that summarizes the wrong thing, green while the mechanism that
governs downstream behaviour varies underneath it.

The observer-theoretic reading is exact and worth stating before the list. A
neighbour count is collected over a query set, so hubness is a property of the
*observation* — the tuple $(\text{corpus},\ \text{query measure},\ \text{metric},\
k)$ — and not of the corpus alone. The corpus and metric partition query space into
capture basins (the region where a given row wins the top-$k$); a row's count is the
query mass in its basin. That is a read-metric statement: the "observer" is the
query workload and the ranking rule, the count is what the observer *reads*, and two
corpora that read identically under one workload can read oppositely under another.
The mechanisms below are what fills those basins — centrality, local centrality,
density, a point cluster, a soft gradient — and the discipline the catalogue
enforces is the book's own: **do not certify a corpus on a scalar its consumer's
tail can falsify.**

**Provenance and epistemic standing.** The measurements catalogued here were made
in the companion project `turboquant-pro` on 2026-07-23/24 and are cited by path,
not re-derived under this volume's registration harness. They therefore carry
*companion-project provenance* rather than this book's six-class ledger tags: they
are not GO-P rows, and the house rule (PROTOCOL Rule 1.1 — no umbrella claim leans
on an unregistered row) forbids me from dressing them as `[demonstrated]`. What they
are is a decisive, independently registered instance of the framework's central
phenomenon in a domain — retrieval geometry — the GO-P sweep did not itself enter.
Sources: `turboquant-pro/docs/HUBNESS_PRIMER.md` (the phenomenon and the mechanism
taxonomy); `docs/RESULTS_multilingual_strata.md` and
`docs/RESULTS_strata_phase23_gates.md` (the multilingual and remedy measurements,
each scored against a content-hashed pre-registration); and the confusion-matrix
fixtures in `tests/test_anatomy.py`, whose four planted constructions are the
mechanism definitions used below.

## The catalogue

The entries are ordered from the sharpest observer-induced geometry (a planted
centre) to the most diffuse (a soft gradient), then the guard that says when to stop
attributing at all, then the two findings that make the point at scale — that the
mechanism is *training-objective-dependent* and that *compression destroys exactly
the information its own remedy needs*.

### G-cat-1 — Shell-plus-centre: pure centrality super-hubs

Plant a handful of points at the *centre* of a unit shell. Those points beat every
shell row's nearest neighbour and vacuum up lists: their occurrence counts scale
like $n$, the corpus size, rather than like $k$. This is the pipeline-artifact
mechanism — the fingerprint of an aggressive mean shift, a collapsed subspace, or an
over-regularised compression that has dragged mass toward a single centre. In the
primer's paired-corpus demonstration a synthetic look-alike carried max occurrence
count 369 against a real corpus's 78 *at the same skewness*, with its hubs sitting
34% closer to the corpus mean than the average row (`HUBNESS_PRIMER.md`, "Two
corpora, same hubness number, opposite behaviour"; fixture `_fx_centrality` in
`tests/test_anatomy.py`). The observer geometry is a delta at the centroid: one basin
swallows nearly all the query mass.

### G-cat-2 — Local-centre shells: density at global scope, centrality up close

Now plant points at the *local* centre of off-centre shells. Each planted point is
"too close to everything" within its own region — small $d_k$, large count, occurrence
scaling like $n_{\text{shell}}$ — while sitting mid-pack in the *corpus's* centrality
distribution. Read globally, that is exactly the density signature; there is no global
centrality to detect. This is a **scope-dependence result**, and a pointed one for
observer theory: *global observation cannot distinguish local centrality from
density.* The two are one point of the global observer's quotient — the coarse
observer literally cannot tell them apart — and splitting them requires changing the
observer to a per-area one (the STRATA direction). The correct global remedy
(mutual-proximity / CSLS rescaling) is the same for both, which is *why* the global
observer is allowed to conflate them: on the axis of what to do about it, they are the
same object (fixture `_fx_local_center_shells`, `tests/test_anatomy.py`).

### G-cat-3 — The point-cluster donor ceiling: a $\Theta(k)$ bound in any dimension

Take a point-like cluster and ask how many rows have it in their $k$-NN ball — the
cluster's "donors." That number is $\Theta(k)$ in *any* ambient dimension: the count
maximum stalls at roughly $2k$ and cannot be pushed higher by adding dimensions or
corpus size. It is a universal structural bound, not a tunable one. Its role in the
companion work is a hard negative: it is one of the two ceilings that proved a
generator-*capability* failure rather than a search failure — no optimizer pass over a
point-cluster family can manufacture the long occurrence tail a real hubby corpus has,
because the geometry caps the tail at $\sim 2k$
(`openvector-bench/results/PREREG_ROUND11.md`, citing the `turboquant-pro`
`docs/RESULTS_strata_phase23_gates.md` fixture work). For observer theory the ceiling
is a statement about basin sizes: a point cluster can only ever be the answer to
$\Theta(k)$ queries, no matter how the surrounding space is arranged.

### G-cat-4 — Soft gradients: the diffuse mechanism, and why it needs concentration

The real-corpus pattern (the primer's "corpus A") is not a planted centre at all but a
soft density gradient — a product-of-rings torus, density-graded angles — where hubs
are moderately popular points sitting where the corpus is locally denser (occurrence
correlated with local density, hubs' local scale a few percent below population,
`HUBNESS_PRIMER.md`). It is the healthy, non-artefact hubness, and it is the one that
*requires distance concentration* to appear: without the high-dimensional crowding of
distances into a narrow band, a small density advantage does not translate into many
list memberships. At small corpus size the soft-gradient occurrence tail caps at
roughly $2.2k$ — the second of the two structural ceilings — so even the benign
mechanism cannot fake an extreme tail on a small corpus
(`openvector-bench/results/PREREG_ROUND11.md`). The observer reading: this is the only
mechanism whose basins are shaped by the *query* concentration rather than by a
planted geometry, which is why it is the one that behaves like a distribution rather
than like an artefact.

### G-cat-5 — The materiality guard: when to abstain

Below a count maximum of about $2.5k$, there is no material hub tail: the occurrence
counts are sampling noise, and any "mechanism" read off them is a guess. The
instrument's classifier *abstains* here rather than attributing — the fixture that
forces this is a constant-density ring with negligible hubness, and the correct output
is "unclear, no prescription" (`HUBNESS_PRIMER.md`, "attribution abstains entirely
when there is no material hub tail"; fixture `_fx_unclear`, `tests/test_anatomy.py`).
This is the catalogue's registration discipline in miniature and the direct analogue
of the book's own refusal to over-read a scalar: mechanism attribution is a claim, a
claim needs a signal above noise, and the honest move below threshold is to decline.
Every entry above is conditioned on clearing this guard.

### G-cat-6 — Encoder findings: cross-lingual architecture is training-objective-dependent

The multilingual run (`docs/RESULTS_multilingual_strata.md`, scored 2026-07-23 against
a content-hashed prereg) puts two encoders through the same instrument and refutes two
registered predictions in the informative direction:

- **BGE-M3 homogenizes per-language hubness.** Seven eligible languages spanning three
  scripts and roughly three millennia of text land in a Robin Hood band of width 0.10
  (0.3447 English … 0.4469 Sanskrit, a 1.30 ratio against a registered $\geq 1.5$), and
  all seven classify as their own self-contained hub economies. The prediction of
  strong per-language heterogeneity was **not confirmed**; the encoder flattens the
  geometry far more than expected.
- **A trained interlingua *dissolves* language borders; emergent multilinguality keeps
  them.** LaBSE (translation-ranking objective) produces *more* cross-lingual transit
  overall (mean transit $\bar\tau$ 0.389 vs BGE-M3's 0.291), carried by rows *less*
  central than the population and spread *less* concentratedly — turning seven of
  thirteen eligible languages into backbone-class transit areas. BGE-M3 (emergent
  multilinguality) is the opposite architecture: less transit, concentrated in a
  semantically central hub region (the centrality signal is significant *only* there,
  $+0.0041$, $p<10^{-4}$), and zero backbone areas. The registered thesis that a
  trained interlingua builds a more *concentrated* translationese core had its sign
  flip on both legs.

The observer-theoretic content: hubness geometry is not a property of "language" or of
"embeddings" but of the *training objective* that fixes the metric. Change the
objective and you change which quotient the corpus lives in — borders-with-a-central-hub
under one, borderless-diffuse-transit under the other — while the surface skewness
scalar would have told you almost nothing about which.

### G-cat-7 — The remedy asymmetry: the codes find, the originals decide

The density remedy for hubness is CSLS / mutual-proximity rescaling, and the
compression measurements (`docs/RESULTS_strata_phase23_gates.md`, measured 2026-07-24
at a 27.676× operating point) establish that **the correction is unrecoverable from
the compressed codes**:

- At the *exact* layer CSLS works — it cuts the count skew, the count maximum, the
  Robin Hood index, and the above-threshold fraction (by 20–33%). The remedy is real.
- At the *compressed* layer it fails, and fails in two stages. Shallow candidate lists
  are **coverage-limited**: CSLS promotes exactly the isolated, fine-distinction rows
  that 27.7× quantization damages first, so its true neighbours are frequently not in
  the candidate list at all (min-over-strata anti-hub recall 0.663 against a 0.90 bar).
  Deepening the candidate list raises coverage from 0.696 to 0.926 but fidelity gains
  four points and then flatlines at 0.702 — past the coverage regime the ceiling
  becomes **score precision**: the right neighbour is now *in* the list and the coarse
  27.7× scores cannot place it. Reconstruction rerank cannot fix this, because the
  reconstruction carries exactly the information the codes do.
- Only exact-layer correction, or reranking against *stored* full-precision originals,
  clears the bar (0.923 at depth 501 with originals — a storage trade, not a coding
  one).

This is the book's compression thesis in its sharpest field form. Compression is an
observer coarse-graining — a quotient that identifies points the codes cannot tell
apart — and it destroys **precisely** the fine distinctions the hubness correction
exists to protect. The remedy needs the anti-hubs' small separations; quantization
rounds those away first; so the corrected ranking is *harder* to reproduce from
compressed codes than the uncorrected one. The information the correction needs and the
information the coarse-graining discards are the same information. The operational
summary the companion project settled on — *the codes find, the originals decide* — is
$\operatorname{tr}(P_C\Sigma_\delta)$ read from the retrieval side: the codes are good
enough to locate the read subspace's neighbourhood, and not good enough to be the final
authority inside it.

## What the catalogue is evidence for

Read across the seven entries, the pattern is the book's, restated in a domain the
sweep did not run. **The scalar is non-identifying** (G-cat-1 vs G-cat-4: same
skewness, opposite mechanism). **The mechanism is the observer's, not the corpus's**
(G-cat-2: local centrality and density are one point of the global quotient and two of
the per-area one; G-cat-6: the training objective picks the geometry). **Some bounds
are structural, not tunable** (G-cat-3, G-cat-4: $\Theta(k)$ and $\sim 2.2k$ ceilings).
**Attribution has a noise floor and must abstain below it** (G-cat-5). And
**compression is a coarse-graining that removes exactly the read-relevant structure a
downstream correction depends on** (G-cat-7). None of this is visible from the
occurrence-skewness number, which is why the companion instruments report a vector and
a mechanism rather than a scalar — the same move this book makes when it replaces
reconstruction error with $\operatorname{tr}(P_C\Sigma_\delta)$.

## The security corollary

The same non-identifiability that makes the scalar a poor quality metric makes the
mechanism vector a *poisoning detector*, and two 2026 adversarial results turn the
catalogue's first entry into a threat model. The **Black-Hole Attack** ("Can You Trust
the Vectors in Your Vector Database?", arXiv:2604.05480, Apr 2026) injects a handful of
vectors near the embedding centroid — G-cat-1's centrality super-hub, planted on
purpose on real BGE embeddings — and hijacks the majority of top-10 results; cluster-wise
centroids amplify it, because a *local* centre (G-cat-2) need only dominate its own
neighbourhood. The **Adversarial Hubness Detector** (arXiv:2602.22427, Feb 2026) scans
production indices for exactly this signature using count z-scores and cross-cluster
retrieval-spread. The convergence reads cleanly in the framework: a planted super-hub
*is* a centrality hub, so a sudden per-area shift from a density mechanism to a
centrality one, absent any pipeline change, is a poisoning signature rather than a
quantization artefact. The quality instrument and the security scanner are the same
instrument — which is what one expects when hubness is a property of the observation and
an attacker is simply choosing the observation.
