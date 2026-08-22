# GO-16 novelty flank — sweep record (2026-08-21)

Agent-run sweep: 17+ web searches + 6 arXiv abstract fetches across
the Başar-school signaling literature, estimation-theoretic privacy,
wiretap/jamming, eigenvalue optimization, rational inattention, and
allocation games. Query list at the bottom (auditable). Surface
limits declared: abstracts only for paywalled Automatica/Econometrica
internals; US-proxied results; DBLP/Scholar not queried natively — a
hidden linear-cost lemma inside the paywalled texts cannot be fully
excluded. **This is one flank pass; the pre-seal must-cite
verification sweep (quote-level) is still owed.**

## Verdict

**The composite game is not occupied; two of its load-bearing
reductions are.** No prior work combines: a committed linear+noise
record that is simultaneously the payoff instrument, an adversary
with a rank-k spectral read budget, leakage priced as resolved
variance, and the partition/tie equilibrium. But:

- **C1 (revelation reduction → SDP): ADJACENT, sub-claim OCCUPIED.**
  Parametrizing Gaussian Stackelberg disclosure by posterior
  covariance and recasting as an SDP is the published
  Sayin–Akyol–Başar / Tamura program. Must be presented as
  **imported machinery**. Surviving novelty: the record-as-payoff-
  instrument value loss, and the theorem that the minimal value cost
  of revelation K is exactly linear — tr(S(I−K)Sᵀ) — with the
  shrink-and-dither attainment. No search hit that formula.
- **C2 (Ky Fan reader + fantope mixing): ADJACENT, machinery
  classical.** Fan 1949; Overton–Womersley (top-k sums, coalescence);
  Warmuth–Kuzmin (fractional W = mixture of rank-k projections).
  Claim only the leakage-game use; cite the operator theory.
- **C3 (partition / indifference pricing / water level / tie iff
  contested): the genuinely novel core.** Nothing close found on any
  search angle. MUST still cite: Overton–Womersley eigenvalue
  coalescence (the tie's optimization-theoretic ancestor),
  water-filling equalization at Gaussian jamming saddles, security-
  game attacker indifference, Blotto equalization (the folklore the
  theorem consciously echoes).
- **C4 (dither necessity + no commitment gap): PARTIALLY OCCUPIED.**
  Idempotent all-or-nothing noiseless Gaussian disclosure is in the
  Sayin–Başar deception line and (2026) arXiv:2602.19292. No-gap is
  minimax folklore (Conitzer) with a Gaussian-privacy-game instance
  in print (arXiv:2005.05743). Position both as corollaries-with-
  teeth of known structure inside the budgeted game, not discoveries.

**Recommended posture: reframe C1/C2/C4 as known machinery with new
theorems on top; headline C3.**

## Must-cite list

1. Sayin, Akyol, Başar — Hierarchical Multistage Gaussian Signaling
   Games (Automatica 2019; arXiv:1609.09448) — the lineage ancestor.
2. Sayin & Başar — Deception-as-Defense (2019; arXiv:1902.01364) —
   Gaussian-quadratic Stackelberg → SDP; idempotent (0/1-eigenvalue)
   optimal deceptive signaling.
3. Sayin & Başar — Persuasion with State-Dependent Quadratic Costs
   (IEEE TAC 2022; arXiv:1907.09070) — MMSE receiver, SDP relaxation.
4. Tamura — Bayesian Persuasion with Quadratic Preferences (SSRN
   1987877) — Gaussian persuasion as PSD-constrained program.
5. Akyol, Langbort, Başar — Strategic Communication as a
   Hierarchical Game (Proc. IEEE 2017; arXiv:1510.00764).
6. Quadratic Privacy-Signaling Games and the MMSE Information
   Bottleneck (arXiv:2005.05743) — Nash = Stackelberg in a Gaussian
   privacy game (prior art for the no-gap phenomenon).
7. Overton & Womersley — SIMAX 1992 + Math. Prog. 1993 — top-k
   eigenvalue sums, dual set {0⪯W⪯I, trW=k}, coalescence
   λ_k = λ_{k+1} at optimizers.
8. Ky Fan 1949; Warmuth & Kuzmin (JMLR 2008, fantope mixing);
   Vu–Cho–Lei–Rohe (NeurIPS 2013, fantope projection).
9. He & Yener — MIMO wiretap with arbitrarily varying eavesdropper
   (arXiv:1007.4801) — antenna-limited (rank-budgeted) eavesdropper
   defeated by artificial noise; secrecy objective, not estimation.
10. Miao, Wu, Young — Multivariate Rational Inattention
    (Econometrica 2022) — LQG attention water-filling, no adversary.
11. Başar-school Gaussian jamming saddle points — classical
    water-filling equalization at minimax.
12. Conitzer — On Stackelberg Mixed Strategies (Synthese 2016) —
    zero-sum commitment-no-value folklore anchor.
13. Farokhi et al. — Estimation with Strategic Sensors
    (arXiv:1402.4031).
14. Strategic Gaussian Signaling under Linear Sensitivity Mismatch
    (arXiv:2602.19292, Feb 2026) — **recent close call**: same
    S-mismatch value instrument, spectral disclosure, noiseless
    all-or-nothing; NO budgeted reader, leakage price, or tie
    theorem. Cite and differentiate explicitly.
15. Semantic Rate Distortion and Posterior Design
    (arXiv:2602.03949) — posterior-covariance design, semantic
    water-filling.
16. Analogy attributions: Roberson 2006 (Blotto), von
    Neumann–Morgenstern (bluffing indifference), Tambe-line security
    games (attacker indifference); sensor-subset zero-sum estimation
    games (arXiv:1502.03531 — subset budgets, not spectral).

## Nearest-work deltas (what each does NOT cover)

- Sayin–Başar/Tamura: disclosure costless or entropy-priced — never
  the payoff-instrument value loss; no linear-cost theorem; no
  budgeted reader.
- Overton–Womersley: ties as optimization geometry — no game, no
  pricing, no partition.
- He–Yener: worst-case nature, secrecy capacity — not a strategic
  priced-estimation reader.
- Miao–Wu–Young: water-filling attention with no adversary.
- 2602.19292: spectral disclosure under S-mismatch — no adversarial
  budget, no ties.

## Search queries run

Sayin Akyol Başar hierarchical Gaussian signaling; strategic
communication LQG Stackelberg leakage; Tamura persuasion quadratic
Gaussian; privacy inference rank-constrained subspace minimax;
zero-sum top-k eigenvalues Ky Fan; Farokhi strategic sensors;
Gaussian jamming water-filling saddle; persuasion limited attention
Gaussian; artificial noise wiretap covariance zero-sum; fantope
mixed strategy eigenvalue tie; Asoodeh estimation privacy; Akyol
privacy water-filling; attacker k sensors Kalman top-k; Gaussian
information design posterior SDP; multivariate rational inattention;
deception requires noise idempotent; Overton Womersley; Sayin SDP
persuasion; commitment zero-sum Stackelberg=Nash; minimax defender
covariance rank-k; matrix Blotto; Bloedel Segal; poker range
balancing leakage subspace; encoder adversary chooses projection;
privacy funnel eavesdropper linear combinations. Fetched abstracts:
2005.05743, 2110.08884, 1510.00764, 2602.19292, 1902.01364,
2602.03949, 1502.03531.
