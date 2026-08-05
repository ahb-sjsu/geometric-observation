# Papers VI & VII — evidence-package index (for Syed)

Prepared 2026-08-05. Every result below carries: a fresh-context
R-IND-5 adversarial verification (record cited), a sealed §5.1
preregistration, a governed harness run, and a CI-enforced re-run on
every push. Source manuscripts: `go12-process-region.tex` (v0.6),
`go13-dynamic-tax.tex` (v0.7), with `go11-conditional-region.tex`
(v0.11 + the 074 uniqueness fold) as the static substrate.

## Paper VI — the spectral conditional region (GO-12)

| Result | Source stmt | Prereg | Harness | Artifact | Verification record |
|---|---|---|---|---|---|
| Fact 1: Δ-invariance / recoding identity | go12 tex Fact 1 | 065 | go12_delta_invariance.py | GO12-delta-invariance.json | go12-process-region-VERIFICATION.md pass 1 (draft pairing REFUTED pre-seal, corrected) |
| Fact 2: slice tax, encoder-access dichotomy | go12 tex Fact 2 | 065 | (same) | (same) | same pass |
| Thm 1: conditional-variance reduction (q_G); Kalman family; W(Δ) | go12 tex Thm 1 | 066 | go12_prefix_family.py | GO12-prefix-family.json | VERIFICATION.md pass 2 (exact gap C^{2Δ}(P_f−q_path) derived by verifier) |
| Thm 2-spectral: the spectral conditional RDF (work endpoint) | go12 tex Thm 2 | 070 (+1 warm-start amendment) | go12_spectral_crdf.py | GO12-spectral-crdf.json | 070 verifier final report (convexity PROVEN; Toeplitz scoped imported-with-4-lemmas) |
| Weighted spectral theorem (Conjecture 1 closed, circulant) | go12 tex Thm 3 | 071 | go12_weighted_spectral.py | GO12-weighted-spectral.json | 071 verifier (two engines to 8.2e-15; (w,μ) rescope) |
| Novelty standing | — | — | — | — | go12-process-region-NOVELTY.md: 4 sweeps + Pinsker + Gray-1973 + Leiner–Gray/Wyner checks, all SUSTAINED |

**Paper VI attribution spine** (all sentences drafted in the NOVELTY
records): Gray 1972/73 (conditional RDF, equal-slope decomposition,
sandwich, scalar Gaussian); Leiner–Gray 1974 (stationary-ergodic
limit); Simeone–Permuter 2013 (delayed SI phenomenon + Eq. 49
substitution device); Sun–Cyr 2018 (AoI conditional-MI form);
Gkagkos/Stylianou–Charalambous (vector single-level water-filling);
Kipnis et al. (remote spectral); del Rio/Sagawa–Ueda/Still et
al./delayed-feedback demons (physics side); Kolmogorov–Pinsker–Berger
(marginal water-filling).

**Paper VI open scopings to state**: Toeplitz transfer = four named
lemmas (imported, O(1/n) numerical support); weighted per-mode
converse ingredients; process-rate causal object (Conjecture 2′, with
the Lev–Khina definitional fork).

## Paper VII — the dynamic complementarity tax (GO-13)

| Result | Source stmt | Prereg | Harness | Artifact | Verification record |
|---|---|---|---|---|---|
| Thm 1: matrix-q reduction; equal-q universality (+r≥2 counterexample) | go13 tex Thm 1 | 067 (+det-guard amendment) | go13_matrixq.py | GO13-matrixq.json | 067 verifier (near-invariance note REFUTED as generic) |
| Thm 2: tax-curve envelope sign law; downward kink | go13 tex Thm 2 | 068 (+det-guard amendment) | go13_taxcurve.py | GO13-taxcurve.json | 068 verifier (Danskin hypothesis corrected) |
| Regime map (exploratory, disclosed) | go13 tex remark | — | go13_regime_sweep.py | — | [exploratory] only |
| Operational face: measured rising tax + equal-q control | prereg 069 | 069 (draft frozen pre-instrument; +V6 amendment) | go13_operational_face.py | GO13-operational-face.json (+ -asexecuted) | registry 069 row (miss + rerun on record) |
| Thm 3: binary twin; universality exactly Gaussian | go13 tex Thm 3 | 072 | go13_binary_twin.py | GO13-binary-twin.json | 072 verifier (50-digit non-collapse; 2 numeric corrections) |
| Thm 4: spectral m=2; two common prices | go13 tex Thm 4 | 073 | go13_spectral_m2.py | GO13-spectral-m2.json | 073 verifier (Toeplitz control; KKT scoping) |
| Thm 5: m-record moment-convexity lemma; Thm-9 uniqueness resolved | go13 tex Thm 5 | 074 | go13_m2_convexity.py | GO13-m2-convexity.json | 074 prover report (PROVED, four steps) |
| Novelty standing | — | — | — | — | go13-dynamic-tax-NOVELTY.md (multiterminal sweep; Stylianou et al. find) |

**Paper VII attribution spine**: Xiao–Luo 2005 (static bivariate
kernel); Stylianou–Charalambous–Charalambous ISIT 2021/2024 (tuple
reduction, implicit static two-water-level system — also scopes GO-11
Thm 9's rate face); Heegard–Berger/Kaspi + Timo–Chan–Grant
(multi-decoder SI umbrella); Permuter–Weissman vending-machine line
(SI-affecting agents — ours is neither encoder nor decoder);
GO-11 Thms 5/9 as the static substrate (in-house, netted 060/064/067).

**Paper VII candidate standalone**: Thm 5 as a short matrix-analysis
communication (self-contained; G = −logdet(I−Z); all flats
characterized).

## Pre-submission checklist (both papers)

1. RE-SWEEP the Stylianou–Charalambous line (active as of Aug 2025
   installment) immediately before submission.
2. Library pulls via institutional access: Leiner–Gray 1974 body
   (4 pp), Leiner dissertation (ProQuest), Gray 1973 T-IT body.
   Verdicts currently high-confidence DOES-NOT-CONTAIN via
   triangulation; the pulls close residual risk in minutes.
3. Toeplitz decision for Paper VI: prove the four lemmas (bounded
   analysis project; O(1/n) numerics clean) vs ship circulant-scoped.
4. Physics-side flank for any causal-measurement framing:
   Hartich–Barato–Seifert / Horowitz–Esposito (unswept).
5. Releases already archived under the concept DOI: go12-go13-1.0 /
   1.1 / 1.2; cut 1.3 after Thms 4–5 (074) if desired.
6. Known instrumentation history, all by dated amendment with
   as-executed artifacts preserved: 069 V6 (1/216 cells), 067/068
   det-guards (bit-identical reruns), 070 warm start (same-seed
   rerun, verdicts identical).
