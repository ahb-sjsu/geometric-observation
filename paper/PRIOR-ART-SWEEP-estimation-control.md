# Prior-Art Sweep — Observation Theory for Estimation and Control

**Date:** 2026-08-18 · **Scope:** the sweep §11 of
`paper/Observation Theory for Estimation and Control.docx` calls for, run before
publication. Three parallel slices: (I) control theory & estimation,
(II) machine learning & inference, (III) communications, networked control &
the FSO application domain. Searches were live web sweeps; each entry was found
in actual results (nothing cited from memory); items examined only at
abstract/snippet level are flagged. Residual coverage gaps are listed at the end.

**Scoring key** used throughout, matching the paper's novelty hypothesis:
- **(a)** task metric derived *from the consumer itself* (vs hand-specified)
- **(b)** with *black-box / query access only* (vs analytic model or autodiff)
- **(c)** composed with an *explicit estimator covariance* (a `tr(P_C Σ)`-type object)
- **(d)** validated *prospectively on the actual downstream consumer at matched budgets*

---

## Headline verdict

**No single found work combines (a) + (b) + (c) + (d).** But every conjunct
separately has close prior art, several of it very close:

- **(a)+(b) exists**: LODL (Shah et al., NeurIPS 2022) recovers local *quadratic
  task metrics* (explicitly Hessian-surrogate ≈ P_C) from a **black-box decision
  oracle** by sampled perturbations under a declared distribution.
- **(a)+(c) exists, white-box**: LQG sensing co-design (Tzoumas, Carlone,
  Pappas, Karaman, IEEE TAC 2021) composes a **Riccati-derived consumer weight**
  with the Kalman covariance for prospective sensor selection; goal-oriented
  Bayesian OED (Attia et al. 2018; quadratic-approximation extension 2025)
  optimizes exactly `tr(J Σ Jᵀ)`-type objectives, including **Jacobian/Hessian
  pullbacks of nonlinear goal maps** — with adjoint/analytic access.
- **Consumer-derived scheduling exists, analytic-LQG**: the Value-of-Information
  program (Soleymani, Baras, Hirche, Johansson; TAC 2022/2023, 2024) derives the
  transmit-trigger metric from the downstream control cost and proves it beats
  age-based policies.
- **FD-probing methodology exists**: empirical observability Gramians
  (Krener–Ide lineage) recover sensitivity geometry by perturb-and-simulate —
  of the *plant*, not of a downstream *consumer*.

**Therefore the paper's §11 hypothesis must be stated as the conjunction, and
the analytic-LQG case must be conceded entirely.** A referee holding LODL in one
hand and GO-OED/LQG-co-design in the other could reasonably call OT an
integration; the answer is the integration *plus the validation protocol*
(reconstruction-matched flips, held-out consumers, matched budgets, physical
endpoints) — which no found work runs.

---

## Slice I — Control theory & estimation

### Functional observability / functional observers — clean daylight, must cite
- Darouach (IEEE TAC 2000) and successors; Automatica 2025 papers on
  [functional observer design](https://www.sciencedirect.com/science/article/abs/pii/S0005109825000068)
  and [PBH tests](https://www.sciencedirect.com/science/article/abs/pii/S0005109825000135);
  [structural functional observability](https://arxiv.org/html/2409.17100).
  All: recoverability of a **hand-specified linear functional z = Lx**;
  binary/subspace-theoretic. (a)(b)(c)(d) all no.
- Montanari, Duan, Aguirre, Motter, **PNAS 2022**,
  [Functional observability and target state estimation in large-scale networks](https://www.pnas.org/doi/10.1073/pnas.2113750119)
  ([arXiv:2201.07256](https://arxiv.org/abs/2201.07256)) — minimal sensors +
  minimum-order observers for a target state subset; hand-specified target;
  [duality with target control](https://arxiv.org/pdf/2401.16372).
- [arXiv:2512.06614](https://arxiv.org/pdf/2512.06614) (Zhang, …, Darouach,
  Fernando) — data-driven functional estimation: plant-model-free, but the
  functional is still engineer-given.
- **Positioning:** OT §2's linear special case (consumer C(x)=Lx) sits inside
  functional observability's subject matter; OT adds the *metric* (not
  subspace) structure, nonlinear consumers, and recovery-from-consumer. The
  related-work section must engage this literature by name.

### Task-driven estimation / LQG sensing co-design — closest structural prior
- **Tzoumas, Carlone, Pappas, Karaman**,
  [Sensing-Constrained LQG Control](https://arxiv.org/pdf/1709.08826) (ACC 2018);
  [LQG Control and Sensing Co-Design](https://arxiv.org/pdf/1802.08376) (IEEE TAC
  2021). LQG cost reduces to a weighted trace of Kalman covariance with weights
  from the control Riccati recursion — **consumer-derived weight, analytically**,
  composed with Σ, prospective selection, suboptimality guarantees. (a) yes
  (white-box, LTI-quadratic); (b) no; (c) yes; (d) in-model.
  *(Sweep note: the Riccati-weight reduction is standard for this line but was
  verified at abstract level, not quoted verbatim.)*
- **Pacelli & Majumdar**,
  [Task-Driven Estimation and Control via Information Bottlenecks](https://arxiv.org/abs/1809.07874)
  (ICRA 2019) — task-relevant representation co-designed via IB; different math,
  closest in spirit on "derive relevance from the task."
- **Carlone & Karaman**,
  [Attention and Anticipation in Fast Visual-Inertial Navigation](https://arxiv.org/abs/1610.03344)
  (IEEE T-RO 2018) — task-projected covariance metrics drive prospective visual
  feature selection under budget, closed loop. Metric designer-specified
  *(inference from paper structure — flagged uncertain by the sweep)*.
- [A Unified Approach to Optimally Solving Sensor Scheduling and Selection in
  Kalman Filtering](https://arxiv.org/html/2304.02692) — objective = trace of
  Kalman covariance weighted by an **arbitrary PSD matrix**; confirms
  weighted-trace-given-W is fully established.

### Submodularity of weighted-trace objectives — fully mapped, cite to preempt
- **Jawaid & Smith**, Automatica 2015,
  [Submodularity and greedy algorithms in sensor scheduling](https://www.sciencedirect.com/science/article/abs/pii/S0005109815003489)
  ([PDF](https://ece.uwaterloo.ca/~sl2smith/papers/2015Aut_Greedy_Submodularity.pdf)) —
  **counterexamples: trace / max-eigenvalue covariance objectives are not in
  general supermodular**; log-det is (under conditions). `tr(P_C ΔΣ)` inherits
  the loss of constant-factor greedy guarantees.
- [Tzoumas et al., sensor placement submodularity](https://www.researchgate.net/publication/282266868_Sensor_Placement_for_Optimal_Kalman_Filtering_Fundamental_Limits_Submodularity_and_Algorithms);
  Summers et al., [Gramian metric submodularity](https://www.researchgate.net/publication/261100835_Submodularity_of_Energy_Related_Controllability_Metrics)
  (trace modular; log-det/rank submodular); Zhang/Ayoub/Sundaram, Automatica 2017,
  [complexity & greedy limitations](https://www.sciencedirect.com/science/article/abs/pii/S0005109816305337).
- **Chamon et al.**,
  [Approximately Supermodular Scheduling](https://arxiv.org/pdf/2003.08841) —
  approximate-supermodularity bounds for MSE/trace objectives: the guarantee
  machinery an OT weighted-trace objective should plug into.

### Event-triggered estimation
- **Soleymani, Baras, Hirche**,
  [Value of Information in Feedback Control: Quantification](https://arxiv.org/pdf/1812.07534)
  (TAC 2022) and [Global Optimality](https://people.kth.se/~kallej/papers/ncs_tac23sol.pdf)
  (TAC 2023) — optimal transmit trigger derived from downstream LQG cost;
  symmetric threshold + certainty equivalence globally optimal. The analytic
  special case of an OT operational trigger; must be cited and beaten/generalized.
- Standard triggers ([Trimpe line](https://www.researchgate.net/publication/308631361_On_the_choice_of_the_event_trigger_in_event-based_estimation),
  [surveys](https://link.springer.com/article/10.1007/s11633-021-1306-z)):
  innovation/variance thresholds, task-agnostic. Weighted-trace triggers with
  hand-chosen weights appear (e.g.
  [cooperative localization, arXiv:1802.07346](https://arxiv.org/pdf/1802.07346)).
  Nothing consumer-recovered.

### Output-weighted Gramians / goal-oriented OED
- **Enns (1984) frequency-weighted balanced truncation** + successors
  ([error bounds](https://ieeexplore.ieee.org/document/788542/),
  [extended FWBT 2025](https://arxiv.org/html/2512.02298)) — output weighting
  since 1984, weight = hand-specified filter. For linear consumers, the
  observability Gramian of (A, C·H) is essentially the dynamic P_C — the paper
  should say so explicitly.
- **Empirical Gramians** (Krener–Ide;
  [PMU placement](https://arxiv.org/pdf/1411.7016),
  [nonlinear sensor selection](https://arxiv.org/pdf/1706.05462)) — sensitivity
  geometry by perturb-and-simulate: **the FD-probing methodology is prior art;
  the probed object (plant vs downstream consumer) is OT's delta.**
- **Attia, Alexanderian, Saibaba**,
  [Goal-Oriented Optimal Design of Experiments](https://arxiv.org/abs/1802.06517)
  (Inverse Problems 2018) — A-GOODE: minimize goal-operator-weighted posterior
  covariance trace under budget. **The `tr(P Σ Pᵀ)` composition, prospectively
  optimized.** Goal map known/linear.
- [Quadratic-approximation GO-OED](https://arxiv.org/html/2411.07532)
  (J. Sci. Comput. 2025) — **nonlinear goal functionals via Jacobian/Hessian
  approximation: the closest found object to P_C = JᵀGJ pulled back from a
  nonlinear downstream map.** Adjoint/derivative access, no probing, no
  matched-budget downstream validation. Also
  [Wu, Chen, Ghattas, SISC 2023](https://arxiv.org/abs/2102.06627);
  [coupled dimension reduction for GO-BOED](https://arxiv.org/pdf/2406.13425);
  [Zhong, Shen, Huan 2024](https://arxiv.org/abs/2403.18072).

---

## Slice II — Machine learning & inference

### Decision-focused learning — pillar (a)+(b) is substantially anticipated
- **Shah, Wang, Wilder, Perrault, Tambe — LODL**, NeurIPS 2022,
  [Learning Locally Optimized Decision Losses](https://arxiv.org/abs/2203.16067).
  **The single closest hit on recovery.** Samples perturbed predictions under a
  declared distribution, queries a **black-box decision oracle**, fits convex
  surrogates — including Quadratic / DirectedQuadratic families explicitly
  interpreted as second-order Taylor/Hessian approximations of the decision
  loss, i.e. a locally recovered PSD task metric ≈ P_C. (a) yes; (b) **yes**;
  (c) **no** — no covariance/uncertainty object anywhere (verified from full
  text); (d) validated on decision regret, never on upstream
  sensing/communication allocation.
- **EGL** (Shah et al., AAAI 2024, [arXiv:2305.16830](https://arxiv.org/abs/2305.16830)) —
  feature-based global learned losses, ~10× more query-efficient.
  **LANCER** (NeurIPS 2023,
  [record](https://www.researchgate.net/publication/401454890_Landscape_Surrogate_Learning_Decision_Losses_for_Mathematical_Optimization_Under_Partial_Information)) —
  global surrogate decision-loss landscape from oracle evaluations.
  **Score-function DFL** ([arXiv:2307.05213](https://arxiv.org/abs/2307.05213), JAIR) —
  fully black-box gradient estimation, no materialized metric.
  **Black-box PTO regret** ([arXiv:2406.07866](https://arxiv.org/abs/2406.07866)).
- SPO (Elmachtoub & Grigas), OptNet (Amos & Kolter), and the
  [DFL survey (Mandi et al., JAIR 2024)](https://www.researchgate.net/publication/398903131_Decision-Focused_Learning_Foundations_State_of_the_Art_Benchmark_and_Future_Opportunities)
  — differentiate through a *known* optimizer: (b) no.
- **TaskMet** (Bansal, Chen, Mukadam, Amos, NeurIPS 2023,
  [arXiv:2312.05250](https://arxiv.org/abs/2312.05250)) — learns a Mahalanobis
  **task-induced metric on prediction space** (bilevel, gradient access). The
  named object "task-induced metric" is already in the literature.

### Loss-calibrated inference / VOI
- Lacoste-Julien, Huszár, Ghahramani, AISTATS 2011
  ([PMLR](https://proceedings.mlr.press/v15/lacoste_julien11a.html));
  LCBNN ([arXiv:1805.03901](https://arxiv.org/abs/1805.03901));
  Kuśmierczyk et al., NeurIPS 2019. Loss is *given*, not recovered. Conceptual
  overlap only.
- VOI/EVSI, [Krause & Guestrin](https://arxiv.org/pdf/1401.3474), decision-aware
  active learning ([arXiv:2201.02555](https://arxiv.org/pdf/2201.02555),
  [arXiv:2409.00049](https://arxiv.org/pdf/2409.00049)) — requires an explicit
  decision-theoretic model of the consumer.

### Pullback metrics from models
- **Arvanitidis et al.** latent pullback geometry
  ([AISTATS 2022](https://proceedings.mlr.press/v151/arvanitidis22b/arvanitidis22b.pdf),
  [AISTATS 2021](http://proceedings.mlr.press/v130/arvanitidis21a/arvanitidis21a.pdf)) —
  G = JᵀGJ from decoder Jacobians, white-box, for geodesics; mathematically the
  identical form. Also pullback Fisher on inputs
  ([PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10606266/); FishBack,
  [arXiv:2605.17231](https://arxiv.org/abs/2605.17231), authors unverified).
- **LPIPS** (Zhang et al., CVPR 2018) — a metric derived *from a network
  consumer*, already steering codec bit allocation in practice. Weakens any
  claim that "consumer-derived metrics driving compression" is new **in
  spirit**; OT's per-point pullback + query-only access + covariance
  composition remain distinct.
- Blau & Michaeli rate-distortion-perception
  ([arXiv:1901.07821](https://arxiv.org/abs/1901.07821)) — distributional
  constraint, orthogonal axis. Ganguli & Simoncelli efficient sensory coding
  ([PDF](https://www.cns.nyu.edu/pub/lcv/ganguli13-reprint.pdf)) — normative
  resource allocation against Fisher information, analytic.

### Task-aware compression & sensitivity-guided allocation
- **Shlezinger, Eldar, Rodrigues**, IEEE TSP 2019,
  [Hardware-Limited Task-Based Quantization](https://arxiv.org/abs/1807.08305) —
  task-weighted error covariances under hard bit budgets, matched-budget
  validation, analytic tasks. Deep variants
  ([arXiv:2201.12634](https://arxiv.org/pdf/2201.12634)) train end-to-end.
- Task-oriented semantic comms (Shao–Mao–Zhang JSAC 2022
  [PDF](https://ira.lib.polyu.edu.hk/bitstream/10397/107084/1/Shao_Learning_Task-Oriented_Communication.pdf);
  surveys [arXiv:2207.09353](https://arxiv.org/pdf/2207.09353),
  [arXiv:2504.20441](https://arxiv.org/html/2504.20441v1)) — end-to-end
  differentiable; sets the empirical bar for matched-rate validation.
- Zeroth-order estimation is commodity (SPSA; minimax FD
  [arXiv:2007.04443](https://arxiv.org/abs/2007.04443); ZOO
  [arXiv:1708.03999](https://arxiv.org/pdf/1708.03999)) — none assemble a
  pullback metric composed with estimator covariance for upstream allocation.
  Hessian/Fisher-weighted quantization (HAWQ/EPTQ,
  [arXiv:2309.11531](https://arxiv.org/pdf/2309.11531)) applies
  sensitivity→budget logic to model weights with autodiff.
- [Decision-focused sensing for flood response, arXiv:2510.16015](https://arxiv.org/html/2510.16015)
  (2025, authors unverified) — OT's exact application shape, gradient-based.

---

## Slice III — Communications, networked control, FSO

### VoI / goal-oriented comms
- **Soleymani, Baras, Hirche, Johansson VoI program** — the closest single
  research program:
  [Foundations of VoI (arXiv:2403.11927)](https://arxiv.org/pdf/2403.11927),
  [VoI vs AoI (arXiv:2403.11926)](https://arxiv.org/pdf/2403.11926),
  [delay (CDC 2021)](https://dl.acm.org/doi/10.1109/CDC45484.2021.9683717),
  [consistency (arXiv:2403.11932)](https://arxiv.org/abs/2403.11932).
  Consumer-derived anisotropic value metric (variation of the LQG value
  function), prospective transmit decisions, provably beats AoI/periodic.
  White-box LQG. **If OT cannot beat or generalize VoI in the LQG case, there
  is nothing left there.**
- **Goal-oriented quantization** — Zou, Lasaulce et al.
  ([arXiv:2209.15347](https://arxiv.org/abs/2209.15347); thesis
  [tel-03714487](https://theses.hal.science/tel-03714487v1/file/2022UPASG021_ZOU_archivage.pdf)) —
  high-resolution analysis yields a **task-Hessian metric**: conceptually the
  pullback P_C for quantizer design, from a known f.
- Sequential rate-distortion / rate-cost: Tanaka SDP
  ([arXiv:1510.04214](https://arxiv.org/abs/1510.04214)),
  **Kostina–Hassibi** TAC 2019
  ([arXiv:1612.02128](https://arxiv.org/pdf/1612.02128); nonlinear
  [arXiv:2604.20369](https://arxiv.org/pdf/2604.20369); continuous-time
  [arXiv:2510.21612](https://arxiv.org/pdf/2510.21612)) — control cost induces a
  weighted-MSE distortion (Riccati pullback), bits allocated against it, SDPs
  with explicit covariances. White-box.
- Learned task-oriented comms: Shao–Mao–Zhang (JSAC 2022, above);
  GOS-VAE ([arXiv:2502.17842](https://arxiv.org/abs/2502.17842));
  closed-loop hierarchical semantic error levels
  ([arXiv:2512.19177](https://arxiv.org/html/2512.19177)).

### AoI vs VoI — "relevance is not age"
- Sun, Polyanskiy, Uysal ([arXiv:1707.02531](https://arxiv.org/abs/1707.02531)):
  signal-aware sampling beats age-minimization. Age of Incorrect Information
  (Maatouk et al., TWC 2022, [arXiv:2012.13214](https://arxiv.org/pdf/2012.13214)).
  [VoI–AoI relation (arXiv:2403.11926)](https://arxiv.org/pdf/2403.11926).
  Surveys: [arXiv:2512.12758](https://arxiv.org/pdf/2512.12758),
  [arXiv:2304.00848](https://arxiv.org/pdf/2304.00848).
- **No found work weights staleness by task-relevant *directions* of state
  uncertainty** (anisotropic, consumer-pulled-back staleness). OT §10's dynamic
  quantity appears open; nearest is VoI's analytic quadratic form.

### FSO/HAPS pointing-acquisition-tracking — the exemplar gap looks real
- PAT surveys: Kaymak et al. (IEEE COMST,
  [record](https://www.researchgate.net/publication/323088080_A_Survey_on_Acquisition_Tracking_and_Pointing_Mechanisms_for_Mobile_Free-Space_Optical_Communications));
  [gimbal/pointing modules review (MDPI Photonics 2025)](https://www.mdpi.com/2304-6732/12/10/1001);
  HAPS dynamic pointing with IUKF
  ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0030402623001171)).
- Forward maps (attitude error → coupling/BER) as static link-budget models:
  [fiber coupling with pointing errors](https://www.sciencedirect.com/science/article/abs/pii/S0030402619314561);
  [few-mode coupling (arXiv:2009.14392)](https://ar5iv.labs.arxiv.org/html/2009.14392);
  UAV jitter models ([arXiv:2406.05444](https://arxiv.org/pdf/2406.05444),
  [arXiv:2004.10071](https://arxiv.org/pdf/2004.10071)).
- Reverse direction found only as link-aids-attitude patents (US6195044).
- **No found work pulls the coupling/BER Jacobian geometry back onto the
  navigation/attitude estimator covariance to prospectively allocate
  estimation/sensing resources.** Standard practice is a static top-down
  pointing-error budget. Caveat: SPIE PAT proceedings are imperfectly indexed
  by web search — see residual gaps.

---

## Consolidated top-10 closest works (all slices)

| # | Work | Anticipates | OT's remaining delta |
|---|---|---|---|
| 1 | LODL (NeurIPS 2022) | (a)+(b): black-box quadratic task-metric recovery | covariance composition; upstream resource allocation |
| 2 | LQG co-design (Tzoumas et al., TAC 2021) | (a)+(c)+(d-ish), white-box LQG | black-box, non-LQG consumers, out-of-family validation |
| 3 | GO-OED + quadratic-approx (Attia 2018; JSC 2025) | (a)+(c): JᵀGJ-weighted posterior covariance under budget | query access (no adjoints), dynamic estimators, downstream validation |
| 4 | VoI program (Soleymani et al.) | consumer-derived scheduling that beats AoI | black-box, non-LQG, anisotropic staleness, physical endpoint |
| 5 | Tanaka SDP / Kostina–Hassibi | bits vs control-cost-induced weighted distortion | model-free P_C, online, hardware endpoint |
| 6 | Goal-oriented quantization (Zou et al.) | task-Hessian pullback metric for quantizer design | probed (not analytic) metric; dynamic Σ; scheduling |
| 7 | TaskMet (NeurIPS 2023) | the named "task-induced metric" object | black-box; covariance; allocation |
| 8 | Carlone–Karaman attention (T-RO 2018) | prospective task-projected sensing under budget | recovered (not designed) metric; comms dimension |
| 9 | Task-based quantization (Shlezinger et al., TSP 2019) | (c)+(d) with analytic tasks | black-box nonanalytic consumers |
| 10 | Empirical Gramians (Krener–Ide) | the FD-probing methodology | probed object: consumer utility, not plant observability |

## What this means for the paper

1. **Rewrite §11's hypothesis as an explicit conjunction** and concede the
   analytic cases by name: "each pillar exists separately — black-box metric
   recovery (LODL/EGL), consumer-derived weight composed with covariance
   (LQG co-design, GO-OED, VoI, rate-cost) — no work combines black-box probed
   consumer geometry with explicit estimator covariance and prospective
   matched-budget validation on the actual consumer."
2. **Mandatory citations** now: Darouach + Montanari (functional observability),
   Tzoumas/Carlone/Pappas/Karaman, Soleymani/Baras/Hirche/Johansson,
   Attia/Alexanderian/Saibaba (+ 2025 quadratic extension), Kostina–Hassibi,
   Tanaka, LODL/EGL, TaskMet, Zou goal-oriented quantization, Shlezinger
   task-based quantization, Jawaid–Smith + Chamon (submodularity), Enns FWBT,
   empirical Gramians, Carlone–Karaman, LPIPS (as narrative caution).
3. **Campaign implications:**
   - Campaign 1 (null result): reframe as *verification*, not discovery — the
     invariance is classical and now machine-checked
     (`lean/ObservationTheory/WeightedMeanInvariance.lean`).
   - Campaign 2/4 baselines must include the analytic consumer-derived weights
     (Riccati/VoI) where the model is available — beating hand-tuned isn't
     enough; OT must match the analytic weight where it exists and win where it
     doesn't.
   - Campaign 3 (blind recovery → scheduling) is **the** novel experiment; no
     found work runs probed-consumer-metric → sensor scheduling. Make it the
     flagship.
   - Campaign 5 (FSO): the gap is real on current evidence; the literature runs
     attitude→link forward only.
   - §9/§10: anisotropic consumer-weighted staleness appears open.
   - Greedy scheduling claims need the Jawaid–Smith caveat + Chamon
     approximate-supermodularity machinery.

## Residual coverage gaps (honest limits of this sweep)

- SPIE PAT/FSO proceedings are poorly indexed by general web search; a targeted
  SPIE Digital Library pass is warranted before Campaign 5 claims a gap.
- Very recent (2025–26) semantic-communications and Soleymani-group output
  deserve a Google Scholar alert; a targeted pass on "goal-oriented
  quantization data-driven" was recommended by the comms slice.
- A few entries were verified at abstract/snippet level only (flagged inline);
  quote-level verification should precede citation in a submitted manuscript.
- No systematic patent search beyond the one FSO hit.
