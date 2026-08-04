# GO-12 novelty record

Four parallel sweeps, 2026-08-04/05, per the obligations in the problem
statement (v0.2 §Verification obligations). House rule: no novelty
language in any GO-12 document beyond what this record supports.

## Sweep D — technical devices + physics framing (COMPLETE)

~18 WebSearch queries + 5 arXiv metadata probes + full-PDF page
verification of Simeone–Permuter arXiv:1109.1293 (31 pp incl. App. C–D).

**(D1) Recoding-invariance device — NOVEL as a stated lemma; ingredients
ADJACENT-KNOWN.** Bijective-recoding invariance of conditional
functionals is textbook folklore; circulant-vs-Toeplitz O(1/n) control
is standard (Gray's review — not page-verified this session). No source
states the packaged finite-n lemma (Y,V,S^Δ) =d (Y,V,P^ΔS⁰) for delayed
side channels. Closest: Simeone–Permuter Lemma 1 (memoryless collapse
under delay), proved by single-letterization, not recoding.

**(D2) Slice-reduction substitutions — ADJACENT-KNOWN, borderline
KNOWN. THE SWEEP'S MAIN FIND, mandatory rescope.** Simeone & Permuter,
"Source Coding When the Side Information May Be Delayed" (IEEE T-IT;
arXiv:1109.1293), §V-B + App. D, **page-verified**: hidden Gauss-Markov
source, decoder holds d-step delayed SI; their Eq. (49)
R_d(D) = ½log₂((1−ρ^{2d}+σ_N²)/D) with test channel X = ρ^d·Y_d + S + Z
(Eq. 67). This is exactly the absorption of Markov decay into effective
SI noise — our s → s/a^{2Δ} in a different normalization — and their
test channel carries the ρ→ρ^d absorption. The outdated-CSI wireless
literature uses the same device routinely. **What remains ours: the
encoder-access dichotomy** — whether a^Δ lands on the read correlation
(context-epoch-latent records) or on the effective SI noise
(single-letter records) is decided by which variable the record may
depend on; not stated as a dichotomy in any found source; our
conditioner also holds a noisy future value vs their clean past one
(packaging-level distinctions only).

**(D3) Landauer framing with an aging reference — framing
ADJACENT-KNOWN, the specific quantity NOVEL.** Hemmed on three sides,
all to be cited: static conditional erasure = del Rio–Åberg–Renner–
Dahlsten–Vedral (Nature 2011) + Sagawa–Ueda (PRL 2009); "stale
information is thermodynamically penalized" as a principle = Still–
Sivak–Bell–Crooks "Thermodynamics of Prediction" (PRL 2012, the
"nostalgia" term — closest conceptual prior art, engage head-on);
delay-degraded WORK EXTRACTION = time-delayed-feedback demons
(Rosinberg–Munakata–Tarjus PRE 2015; arXiv:2405.05123; Debiossac et
al.); mismatch cost = Kolchinsky–Wolpert 2017. NOT found anywhere: the
exact dynamic conditional-Landauer curve W(Δ) for erasing a record
against a reference decorrelated by a^Δ.

**(D4) AoI × Landauer — NOVEL (unclaimed bridge).** arXiv metadata:
"age of information" AND "Landauer" → 0 results; "thermodynamic" AND
"information freshness" → 0. Caveat on record: metadata-level search
only; run a full-text scholar pass before printing "first".

**Demanded attributions (D), to fold into the problem statement:**
1. Fact 1 must attribute bijective-recoding invariance (folklore) and
   circulant-Toeplitz asymptotics (Gray); ours is only the packaged
   finite-n delayed-side-channel statement.
2. Fact 2 must cite Simeone–Permuter Eq. (49)/(67) as the source of the
   substitution device and present ONLY the dichotomy as new.
3. The physics framing must cite del Rio et al. + Sagawa–Ueda (static
   conditional erasure), Still et al. (stale-information penalty
   principle), and the delayed-feedback-demon line (work-extraction
   side), scoping our claim to the erasure-side W(Δ) curve.
4. Any AoI-bridge sentence carries the metadata-only caveat.

## Sweep B — delayed side information in source coding (COMPLETE)

13 queries + page-level reads: Simeone–Permuter full PDF (independently
of Sweep D), Weissman–El Gamal T-IT 2006 pp. 1–4, Sun–Cyr SPAWC 2018.

**(B-i) Path-access Δ-invariance — ADJACENT-KNOWN asymptotically, NOVEL
as stated.** Simeone–Permuter Lemma 1 (page-verified): for MEMORYLESS
pairs, noncausal SI availability makes zero-delay conditional RD
delay-proof, while any positive causal delay makes SI useless.
Matsuta–Uyematsu (IEICE 2014/2019): known-delay block coding treated as
trivial; characterization of when unknown delay leaves WZ-RD unchanged.
NOT found anywhere: the exact finite-n recoding identity, any version
for a third-party conditioner, or the every-finite-n circulant
statement. Claim the identity and framing, not the asymptotic
phenomenon.

**(B-ii) Slice tax — decay form KNOWN, dichotomy NOVEL.** Beyond
Simeone–Permuter Eq. (49) (see D2): **Sun & Cyr, "Information Aging
through Queues" (SPAWC 2018, page-verified), Eq. (7)**: for Gaussian
AR(1), the delivered-history mutual information is −½log₂(1−a^{2Δ}) —
the conditional-MI form of the AR(1) staleness tax is explicitly in the
AoI literature; their Lemma 1: for noiseless Markov sampling the causal
path collapses to the freshest sample. None of the found sources has a
noisy delayed slice, a third-party conditioner, or the encoder-access
substitution dichotomy. Also cite quadratic-Gaussian WZ no-rate-loss
when positioning (encoder-side S-availability is rate-irrelevant in the
Gaussian block setting).

**(B-iii) Causal-path interpolation — OPEN, conjecture NOVEL.**
Weissman–El Gamal: causality kills the binning term (memoryless;
lookahead only in infinite-letter form; "if the future is not allowed
to be looked into, the past is useless"). Sun–Cyr Lemma 1 pins the
noiseless endpoint — the conjectured interpolation is nontrivial
PRECISELY because our slice is noisy (U ≠ 0); fold this sanity check
into the conjecture text.

## Sweep C — causal/sequential RD substrate (COMPLETE)

21 queries + page-verified: Lev–Khina arXiv:2004.08409 (full 6 pp),
Weissman–El Gamal (3 pp), Stavrou–Tanaka–Tatikonda arXiv:1711.09853,
Derpich–Østergaard abs, Simeone–Permuter abs, DI monograph abs.

**Substrate map for Conjecture 2′ (causal-path eraser):**
- Scalar Gauss-Markov sequential RDF closed form
  ½log⁺((λ²D+σ_v²)/D): Gorbunov–Pinsker 1974; Tatikonda–Sahai–Mitter
  TAC 2004; Derpich–Østergaard T-IT 2012 (+ operational gap
  ≤ ½log 2πe).
- **Vector caution:** the NRDF "dynamic reverse water-filling" closed
  forms were REFUTED in general by Stavrou–Tanaka–Tatikonda
  (arXiv:1711.09853, counterexample); the correct general object is
  Tanaka et al.'s SDP. Scalar AR(1) closed forms realistic; do not
  assume vector water-filling.
- **Nearest neighbor, cite in the first paragraph of any causal-path
  section: Lev & Khina (ISIT 2020, arXiv:2004.08409)** — Gauss-Markov
  tracking with causal decoder SI; information CRDF defined via
  causally conditioned DI with a Markov constraint; proved strictly
  larger than the noncausal value; **exact value explicitly left open**
  ("yet to be determined even for the simpler memoryless batch").
- **Definitional fork is REAL and already exhibited:** Kostina–Hassibi
  (TAC 2019) causally-conditioned-DI definition COLLAPSES to the
  two-sided/noncausal Gaussian closed form (Lev–Khina Lemma 2 proves
  the strict gap to the Markov-constrained definition). Consequence
  folded into Conjecture 2′: the conjectured strict interpolation is
  only well-posed under the Markov-constrained (Lev–Khina-style)
  conditioning; the Kostina–Hassibi choice provably degenerates to the
  full-path endpoint.
- Third-party access distinction: everything found puts causal SI at
  the decoder (Weissman–El Gamal; Lev–Khina) or at an actively
  communicating helper (Bross, MDPI Information 2020, i.i.d. only);
  the passive evaluative conditioner is ours.
- Honesty caveat (verifier-grade): under causal-prefix conditioning the
  mathematical core may reduce to the classical Kalman
  filtering-vs-smoothing gap; the operational definition + the strict
  interpolation theorem must carry the weight, or a referee reads the
  closed form as an exercise.
- Unswept flank flagged: stochastic-thermodynamics information-flow
  line (Hartich–Barato–Seifert; Horowitz–Esposito) not page-verified
  (search budget); the eraser framing's physics-side novelty for
  CAUSAL measurement remains unchecked.

**What would be genuinely new on this rung:** the third-party
conditioner coordinate; delay INSIDE the SI process with a proven
Δ-interpolation between exact endpoints; an exact Kalman/innovations
closed form (would exceed the decoder-SI state of the art, where only
bounds exist).

## Sweep A — conditional RD for stationary processes (COMPLETE)

11 queries + page-level verification: **Gray's 1972 Stanford tech report
read in full (all 30 pp., Wayback scan — Gray's own link is dead)**;
Le–Tan–Motani, Zamir–Kochman–Erez, Stylianou–Gkagkos–Charalambous 2021,
Gkagkos–Charalambous 2024 full texts; Kipnis et al. abstracts; Crossref
DOI checks (Iwata 2000, Matsuta 2012, Wyner 1978).

**Verdict on Conjecture 1: ADJACENT-KNOWN — the object is classical,
the spectral theorem appears to be ours.**

KNOWN (attribute): L = min I(X;X̂|S) is **Gray's conditional RDF**
(Stanford ISL TR 6502-2, Oct 1972; IEEE T-IT 19(4):480–489, 1973);
operational meaning = SI at BOTH ends (Thm 6, page-verified);
per-symbol limit for stationary-ergodic pairs exists = **Leiner–Gray
1974** (T-IT 20(5):672–675); scalar Gaussian evaluation at conditional
variance σ²(1−ρ²) = Gray 1972 Thm 7 (page-verified, incl. a σ_Y²/σ_X²
typo in the scan); vector-Gaussian conditional/WZ water-filling with a
SINGLE water level over eigenvalues of Q_{X|Y} = Gkagkos–Charalambous
(Entropy 26(4):306, 2024) and Stylianou–Gkagkos–Charalambous
(arXiv:2108.13488 — structurally the closest published object,
explicitly vector-only); marginal spectral water-filling =
Kolmogorov/Pinsker/Berger; remote-source spectral water-filling
(single level, no auxiliary conditioning) = Kipnis–Goldsmith–Eldar–
Weissman (T-IT 62(1), 2016). **Gray 1972 Thm 5 (page-verified)** is the
discrete-conditioning ancestor of our allocation structure: equal-slope
distortion allocation across conditioning letters.

NOT FOUND (remains ours, two must-do checks pending): (1) the
spectral/frequency-integral conditional RDF for jointly stationary
Gaussian pairs with per-frequency coherence; (2) the two coupled
spectral water levels; (3) the third-party/eraser conditioning
semantics (L as a consumer-relative coordinate, not an operational
rate — no precedent anywhere); (4) the delayed-noisy S_t = V_{t−Δ}+U_t
structure and the R-vs-L dissociation program. Even Gaussian-process
WZ = reverse water-filling over S_X(ω)(1−|γ(ω)|²) has apparently never
been written down as a theorem.

**MUST-DO before any Conjecture-1 novelty language ships:** page-level
read of Gray 1973 (IEEE 403/418-blocked in the sweep) and of Pinsker's
*Information and Information Stability* Ch. 10 (Soviet conditional
ε-entropy — unswept, budget). Both cheap library pulls; if either
contains a Toeplitz-limit Gaussian conditional formula, novelty
rescopes to items (2)–(4), which stand regardless.

**Pinsker pull RESOLVED (2026-08-05): DOES NOT CONTAIN — high
confidence.** The Feinstein translation (Holden-Day 1964; archive.org
scan `informationinfor0000pins`, lending-restricted) was checked via
Open Library's full-text-search index over the actual scan's OCR, with
verified AND-of-phrases semantics (nonsense-phrase + book-unique-anchor
control). The words "fidelity", "distortion", "reproduction",
"accuracy", "message", "epsilon" occur NOWHERE in the book — it
contains no ε-entropy or fidelity-criterion quantity of any kind. Ch. 9
§9.3 is conditional MUTUAL INFORMATION of Gaussian variables; Ch. 10 is
spectral mutual-information RATES of Gaussian process pairs; §10.5
"entropy rate of one stationary gaussian process with respect to
another" is a KL-DIVERGENCE rate (terminology trap: Pinsker's "entropy
of X w.r.t. Y" always means relative entropy). Secondary corroboration:
Gray's *Entropy and Information Theory* attributes nothing RD-flavored
to Pinsker; conditional RD is standardly attributed to Gray 1972/73.
Residual caveat on record: verdict rests on whole-book term-absence
over OCR + reconstructed ToC + secondary attribution, not page-by-page
reading (a 1-hour archive.org borrow of pp. 159–201 would close the
last gap).

**Gray-1973 pull RESOLVED (2026-08-05): DOES NOT CONTAIN — high
confidence, journal text itself unobtainable.** The published T-IT
paper could not be legitimately obtained (exhaustive: Gray's Stanford
page + full Wayback CDX sweep — the 1973 paper was never hosted there;
Unpaywall/S2/OpenAlex all closed; DTIC down; no infringing sources
used). Verdict rests on four lines: (1) Gray's own companion report
SEL-72-047 — his self-described "complete background reference" for
the paper, read cover to cover — contains ONLY the scalar-pair
Gaussian conditional-variance result and explicitly cross-references
it as "the examples of [8]"; zero spectral/Toeplitz content anywhere;
(2) the paper's abstract: lower bounds for stationary sources with
single-letter vector distortions, conditioning as a bounding device;
(3) Gibson (Entropy 2017, CC-BY, read in full), who built his career
on Gray 1973, constructs Gaussian-memory conditional bounds himself
via finite correlation matrices — he would have used a spectral
formula had one existed; (4) pair-process side information first
enters this line in the SEPARATE Leiner–Gray 1974 correspondence +
Leiner's dissertation. **Consequences:** cede to Gray 1972/73 the
definition, equal-slope decomposition, sandwich inequality,
innovations reduction, and static scalar Gaussian conditional RDF;
the spectral pair-process formula and coupled water levels remain
claimable. **Residual obligations before final claim wording:** (a)
an institutional pull of T-IT 19(4) closes the last Gray-1973 risk in
minutes (Syed's access — flag for the venue package); (b) the same
page-level treatment of **Leiner–Gray 1974** (+ Leiner's Stanford
dissertation, + the Wyner 1976–78 Gaussian-SI line) — the natural
next places a spectral conditional formula could first appear.

**Leiner–Gray/Wyner check RESOLVED (2026-08-05): claim SUSTAINED.**
Leiner–Gray 1974: DOES NOT CONTAIN (abstract page-verified via
Wayback/Xplore + 9 citers' contexts — abstract-ergodic existence/coding
theorem + inequalities; no citer ever attributes a Gaussian evaluation
to it). Wyner–Ziv 1976: finite-alphabet i.i.d. (abstract
page-verified). Wyner 1978: Gaussian case is SCALAR memoryless
(abstract page-verified + the 2024 Entropy structural-properties paper,
read in full via PMC, which derives the multivariate I.I.D. conditional
water-filling as a NEW 2020–2024 contribution and cites no
stationary-process spectral antecedent — the decisive structural
corroboration). Gray 1972 TR re-verified full-text on the archive.org
DTIC mirror (AD-753260): zero occurrences of spectr/Toeplitz/water.
Named residual checks before print: page-read the 4-pp LG74 body via
IEEE-subscribed library; Leiner dissertation via ProQuest/Stanford
(never entered DTIC); Gray-73 body; a post-1990 flank sweep
(Oohama/Zamir/WZ-video surveys). Nothing found contradicts the claim;
the spectral conditional RDF for jointly stationary Gaussian pairs
remains unwritten in everything reachable.

## Standing after the four sweeps

- Fact 1: ours as a packaged finite-n lemma; ingredients + asymptotic
  phenomenon attributed (folklore, Gray Toeplitz review,
  Simeone–Permuter Lemma 1, Matsuta–Uyematsu).
- Fact 2: substitution DEVICE published (Simeone–Permuter Eq. 49;
  Sun–Cyr Eq. 7) — rescoped; the encoder-access dichotomy + noisy
  third-party slice are ours.
- Conjecture 1: object classical (Gray/Leiner–Gray); spectral form +
  coupled water levels + framing apparently ours, pending Gray-1973 and
  Pinsker library pulls.
- Conjecture 2′: open at the state of the art (Lev–Khina leave the
  simpler decoder-SI object open); well-posed only under
  Markov-constrained conditioning; third-party + in-process delay ours.
- Physics: static conditional erasure, nostalgia principle, and
  delayed-feedback work extraction all attributed; the dynamic
  erasure-side W(Δ) curve and the AoI–Landauer bridge (metadata-only
  caveat) unclaimed.
- ~63 queries + 10 page-verified documents across the four sweeps;
  sweep transcripts in the session task outputs; per-sweep query lists
  reproduced in each agent report.
