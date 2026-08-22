# GO-16 novelty flank — sweep record (2026-08-21)

Agent-run sweep: 17+ web searches + 6 arXiv abstract fetches across
the Başar-school signaling literature, estimation-theoretic privacy,
wiretap/jamming, eigenvalue optimization, rational inattention, and
allocation games. Query list at the bottom (auditable). Surface
limits declared: abstracts only for paywalled Automatica/Econometrica
internals; US-proxied results; DBLP/Scholar not queried natively — a
hidden linear-cost lemma inside the paywalled texts cannot be fully
excluded. **Quote-level sweep COMPLETE (2026-08-21, second agent
pass): 13 verified, 2 corrected, 1 unverifiable-at-primary of 16 —
record in §"Quote-level sweep" below; corrections folded into the
list in place.**

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
    (Econometrica 90(2):907–945, 2022) — LQG attention via
    rate-distortion + SDP; generalized reverse water-filling in
    special cases; no adversary. [CORRECTED at quote level: the
    general solution is SDP, water-filling only in special cases.]
11. Başar 1983 — "The Gaussian test channel with an intelligent
    jammer," IEEE T-IT 29(1):152–157 — the SCALAR Gaussian minimax
    saddle point (linear amplification vs. linear-or-independent-
    noise jamming). [CORRECTED at quote level: no water-filling in
    this paper; attach equalization/water-filling language to the
    vector/MIMO jamming extensions or drop it from this cite.]
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

## Quote-level sweep (2026-08-21) — record

Second agent pass; every item checked against its primary page with a
supporting verbatim quote captured (report retained in the session
transcript; key dispositions here). **VERDICT: 13 verified, 2
corrected, 1 unverifiable-at-primary of 16.**

- **Verified with quotes** (1, 2, 3, 5, 6, 7, 8, 9, 12, 13, 14, 15,
  16), including the two load-bearing ones: item 2's idempotent
  structure verbatim from the paper body ("P_k … is a symmetric
  idempotent matrix, … eigenvalues … either 0 or 1") and its SDP
  ("min Tr{SV} subject to Σ₁ ⪰ S ⪰ O_m"); and **item 14 (the close
  call, arXiv:2602.19292 — Munif, Varma, Lasaulce, IFAC WC 2026)
  fully verified against its full text with all four claimed
  ABSENCES confirmed**: no rank-budgeted reader, no leakage
  price/resolved-variance pricing, no eigenvalue-tie or partition
  theorem, no linear cost of revelation; its Remark 9 itself reduces
  the sender problem to the Tamura/Sayin–Başar formulations.
- **Corrected**: items 10 and 11 (folded into the list above).
- **Unverifiable-at-primary**: item 4 (Tamura; SSRN 403s) — doubly
  corroborated via Malamud–Schrimpf (arXiv:2110.08884): "He shows
  the existence of a linear optimal information design, given by a
  linear projection." Carried with this caveat.
- **Bibliographic upgrades to use at citation time**: item 9's
  journal version (IEEE T-IT 60(11):6844–6869, 2014); item 3's exact
  title/venue ("…State-Dependent Quadratic Cost Measures," TAC
  67(3):1241–1252, 2022; the exact equivalence is
  copositive-programming, the SDP is a relaxation/lower bound);
  item 7's venue is SIAM J. Matrix Anal. Appl. 13(1):41–45 (guard
  against the mislabeled "J. Numer. Anal." floating in indices);
  author names for 6 (Kazıklı–Gezici–Yüksel), 14, 15 (Akyol).
- **The load-bearing nuance (danger framing (a))**: the linear-cost
  clearance HOLDS — no source states tr(S(I−K)Sᵀ) or the
  record-as-payoff-instrument cost — but the Sayin–Başar SDP
  objective is ALREADY linear in the posterior covariance
  (min Tr{SV}). The GO-16 novelty must therefore be phrased as the
  **identification of the minimal value cost of revelation K with
  tr(S(I−K)Sᵀ) inside the record-as-instrument game (with its
  explicit shrink-and-dither attainment)** — never as "the cost is
  linear in a covariance variable," which is standard in that line.
  The statement (v0.4) adopts this phrasing.
- Danger framing (b) HOLDS: Overton–Womersley 1993 is literally
  about *minimizing* sums of largest eigenvalues, with multiplicity
  ("splitting a multiple eigenvalue if necessary") at optimizers.

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
