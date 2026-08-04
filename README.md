# Geometric Observation

The fourteenth work in the geometric series, and its **evidence repository**. The book
synthesizes:

- **Paper I** — *Keep the Angle* ([`the-angular-observer`](https://github.com/ahb-sjsu/the-angular-observer)): the spectral/angular result.
- **Paper I.5** — *The Angular Observer as a Manifold Recognizer* ([`the-angular-observer/paper2`](https://github.com/ahb-sjsu/the-angular-observer/tree/main/paper2)): the five-instrument recognizer that names a manifold or certifies none — *dimension emerges before shape*.
- **Paper II** — the compression-as-observation work ([`turboquant-pro`](https://github.com/ahb-sjsu/turboquant-pro)): keys/values asymmetry, rank certificates, the (A2) probe, operator-regime tracing.
- **Paper III** — [**Observation Theory**](paper/observation-theory.pdf) ([source](paper/observation-theory.tex)): the information-theoretic synthesis — consumer-relative rate–distortion, the two-observer successive-refinement region ([`paper/two-observer-theorem.tex`](paper/two-observer-theorem.tex)), and the omission floor.
- **Paper IV** — [**The consumer-relative flip**](paper/paper-IV-consumer-relative-flip.pdf) ([source](paper/paper-IV-consumer-relative-flip.tex), [TMLR build](paper/paper-IV-tmlr.tex)): the empirical spine — at matched bits, a code that preserves what the *consumer* reads beats a reconstruction-optimal code on the downstream task *while reconstructing the signal worse*, demonstrated across domains and physics.
- **Paper V** — [**A Rate–Work–Distortion Region for Consumer-Relative Observation**](paper/consumer-relative-landauer.pdf) ([source](paper/consumer-relative-landauer.tex), [Overleaf zip](paper/consumer-relative-landauer-overleaf.zip)): the thermodynamic extension — a stored description carries **two separate resources**, the rate a consumer needs ($I(X;\hat X)$) and the ideal Landauer work its reset costs against retained side information ($I(X;\hat X\mid S)$); the full achievable region, the materialize-then-project barrier, multi-consumer coordinated reset, the Gaussian region with reset side information (scalar single-corner collapse with work discount $\to I(X;S)$; vector "reset water-filling" frontier), temperature-weighted water-filling, the staleness–work complement, and the semantic-invariance-of-erasure locality statement. Verified: **two** R-IND-5 fresh-context passes (0 errors total — ledger VI-8/VI-9; [revision notes](paper/consumer-relative-landauer-REVISION-NOTES.md)), theorem harnesses `verify_consumer_landauer.py` + `verify_gaussian_sideinfo.py` (GO-P-2026-042/044, both ALL PASS, CI-rerun), and three operational faces, each now `[replicated]` on two independent source families: **GO-7** (rate–work separation — 043 PASS 7/7, 045 multi-codebook PASS 6/6, 047 cross-source Gaussian PASS 6/6), **GO-8** (staleness: the reset threshold climbs with the age of the retained side information, tracking the predicted exchange — binary 049, Gaussian AR(1) 053), and **GO-9** (coordinated reset saves the shared-structure information — binary 050, Gaussian 054). ⚠ The GO-8/GO-9 Gaussian verdicts rest on a post-hoc bugfix to a control statistic, recorded in their ledger rows. Archived release: [doi:10.5281/zenodo.21776291](https://doi.org/10.5281/zenodo.21776291) (all versions; v1.2 = tag `paper-v-1.2`); one-click replication: [`notebooks/`](notebooks/).

into one claim: **compression succeeds for a consumer exactly when it preserves
what that consumer's functional distinguishes** — measured on the consumer's own
metric, never on reconstruction error.

## Observation Theory

Geometry, distortion, and reliability are properties of the **observation** — the
consumer's read operator, budget, and channel — not of the object observed. The
operative distortion is the reconstruction error read through the consumer,
`d_O = tr(P_C · Σ_δ)`; reconstruction (`tr Σ_δ`) is the corner `P_C = I`, where
Shannon rate–distortion and Gauss least-squares live. Paper III derives this,
proves the achievability + converse of a consumer-relative rate–distortion function
for a general source, gives the two-observer successive-refinement region, and
positions the framework as the identifiable geometric middle term between Shannon
and the information bottleneck. See
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
| [`claims/REGISTRY-ACCOUNTING.md`](claims/REGISTRY-ACCOUNTING.md) | Every assigned prereg ID with a disposition — the no-file-drawer proof |
| [`DOMAIN-GENERALITY-SWEEP.md`](DOMAIN-GENERALITY-SWEEP.md) | The consumer-relative flip across domains, one row per sealed prereg + result |
| [`experiments/`](experiments/) | The three-arm instance runs (§3) and scripts |
| [`results/`](results/) | Sentinel-delimited result JSONs (committed, CI-rerun) |
| [`chapters/`](chapters/) | Chapter → claim map and drafts |

## Status — falsifiable core resolved; the flip is domain-general; the cost face extends to thermodynamics

| Claim | Class | Evidence |
|---|---|---|
| **GO-1** identifiability | `[predicted]` | blind probe recovers the read subspace at 0.94 vs 0.06 chance; predicts the flip 12/12 |
| **GO-2** distortion (`tr P_C Σ_δ`) | `[demonstrated]` · `[replicated]` · Gate-B | recon-identical code 2.5× worse; the flip inverts with the consumer; holds on attention, retrieval, optimization, a trained Llama-3.2-3B layer (GO-021: reconstruction-invisible worse-arm call 16/16 at recon tied to 7.5e-9), and — via the sealed domain-generality battery — on acoustic and seismic arrays |
| **GO-3** certificate vacuity | `[demonstrated]` | derived EVT threshold locates retrieval death to ~5%, orders 14 corpora (ρ=0.99) |
| **GO-4** budget inversion | `[replicated]` | fixed-budget verdict inverts under budget-matched observation on real embedding manifolds |
| **GO-5** density quotient | `[refuted]` | 4 prospective misses; the density-nuisance mechanism is operator/spectral-confined (NEG-11) |
| **GO-6** output ≤ surrogate ≤ recon | `[demonstrated]` | at matched rate the three coders order on the consumer metric; the gap is the $\ker P_C$ entropy share |
| **GO-7** rate–work separation (Paper V) | `[replicated]` ✅ | the same stored code index decodes from reset side information at ~0.4·R̂, fails below its conditional content, fails absolutely without S — on **two independent source families** (binary two-bit 043/045, incl. 5 codebooks; scalar Gaussian 047 at the paper's §VI corner setting); 046 = logged instrumentation-window miss, physics gates 4/4 |
| **GO-8** staleness–work complement (Paper V) | `[replicated]` ⚠ | one fixed record, one fixed bin assignment: the decodable reset threshold climbs **0.10 → 0.55 bits/symbol** as the retained side information ages, tracking $R_c-1+h_2(\hat d * q_t)$ within one grid step at all eight ages; the same bin rate flips from 1% error (age 0) to 100% (age 32). Relevance lost to time is gained as erasure work. Held on **two source families** (binary Markov 049; Gaussian AR(1) 053, tracking the §VI discount). ⚠ The Gaussian verdict rests on a post-hoc control-statistic bugfix — see the ledger row |
| **GO-9** coordinated reset (Paper V) | `[replicated]` ⚠ | two consumer records sharing a component: resetting either one with the *other intact* lowers the threshold by the shared-structure information — **0.60 / 0.45 bits/symbol measured vs 0.476 predicted** — including on the record whose own reset side information is useless; mismatched pairing saves nothing. The operational face of $\mathrm{TC}(U_1;\ldots;U_m\mid S)$; held on **two source families** (binary 050; Gaussian 054, 0.56× the asymptotic gap on both records). ⚠ Same caveat as GO-8 |
| **GO-10** complementarity tax ([note](paper/complementarity-tax.tex)) | `[demonstrated]` ✅ | one description serving two read operators pays a tax priced by the read-plane Gram determinant $\kappa=\det(B^{\mathsf T}\Sigma_xB)$, and **erasure pays it only against what the reset context doesn't already know**: the rate and work floors differ by exactly $I(u^{\mathsf T}X,v^{\mathsf T}X;S)$. Rate side classical after reduction (Gray 1973; Xiao–Luo 2005 — attributed; the tax quantity and the entire work side found no prior). Theory R-IND-5-verified (VI-10, one error caught pre-assertion), C3 harness **ALL PASS 7/7** (055); operational face **PASS 6/6** (058): measured rate-tax/work-tax gap **0.266 / 0.094 bits** (0.57×/0.37× of asymptotic, matching GO-9's realized fraction) vs shuffled-context nulls ≈ 0, with the coordinated-split eraser tilting its budget to the S-opaque record — reset water-filling made operational. One source family; binary analog + θ-sweep registered as the path to `[replicated]` |

**The flip is a property of observation, not of a regime.** The sealed cross-domain
sweep ([`DOMAIN-GENERALITY-SWEEP.md`](DOMAIN-GENERALITY-SWEEP.md)) carries the
consumer-relative flip — at matched bits, read-preserving beats reconstruction-optimal
downstream while reconstructing worse — across **≥5 domains and ≥3 distinct physics**:
synthetic ULA (031), LLM attention keys (021), acoustic direction-of-arrival
(LOCATA 033, AV16.3 034·D2), and seismic backazimuth (PDAR 034·D3), plus the
non-physical domains of legal-citation retrieval (035→036→039) and sperm-whale coda
dialect (038). Radar (034·D1) is a data-limited partial; gradient/curvature
optimization (034·D4) is an honest negative that *bounds* the flip to consumers whose
read operator is misaligned with signal energy — no file drawer.

Four faces of Observation Theory stand; the fifth is an honest negative. The COST
face now extends to thermodynamics: Paper V's rate–work–distortion region separates
what a consumer must receive from what a reset mechanism must irreversibly discard,
with two 0-error fresh-context verification passes (VI-8/VI-9) and the GO-7
operational demonstration behind it. **57 sealed preregistrations** (040 void,
046/048/051/052 logged instrumentation misses, each superseded and rerun), every one
timestamped before its measurement; standing negatives **NEG-1…16** — NEG-13 (the
omission floor) resolved to `[demonstrated]` downstream on a trained model (GO-027),
and **NEG-15** records the Bell boundary: retrieval geometry does not weaken Bell
([notes](experiments/HUBNESS-BELL-NOTES.md)). Every claim
resolves to a row in [`claims/LEDGER.md`](claims/LEDGER.md).
