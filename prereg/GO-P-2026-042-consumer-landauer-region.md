# GO-P-2026-042 — Consumer-relative Landauer: rate–work–distortion region, C3 numerical harness

Registers the **numerical falsification harness** for the analytic results of the paper
*A Rate–Work–Distortion Region for Consumer-Relative Observation*
([`paper/consumer-relative-landauer.pdf`](../paper/consumer-relative-landauer.pdf)) — the
thermodynamic extension of Observation Theory (COST face). Analytic results; the harness
is a falsification net per charter rule R-IND-5. Governs
`experiments/verify_consumer_landauer.py`.

**Claims under net.** (Thm 1) the region
$\mathcal{RW}_\mathcal{C}(D)=\overline{\mathrm{conv}}\bigcup_{q\in\mathcal T_\mathcal C(D)}\{(R,L):R\ge I(X;\hat X),\ L\ge I(X;\hat X\mid S)\}$,
converse at every finite $n$; (Prop 1) the Pareto-channel fixed point, eq. (20), with both
coordinates convex in the test channel; (Prop 2) the exact binary frontier
$R(t)=2-h_2(t)-h_2(2D-t)$, $L(t)=1-h_2(2D-t)$ and the matched-rate inversion
($L=0.1187$ vs $1$ at tied $R=1.1187$, $D=0.15$); (Thm 2) the materialization barrier
$H(A,M\mid S^n)=nH(X\mid S)$ and $\Delta W\ge 0$; (Cor 2/3) exact-consumer endpoints
$H(U)$, $H(U\mid S)$ and conditional total correlation $\ge 0$; (Cor 4) Gaussian
read-operator water-filling, eq. (41) $=$ the max-det program; (Prop 3)
temperature-weighted water-filling $d_i^\star=\min\{\lambda_i,\nu T_i\}$; (Prop 4)
staleness monotonicity and the binary predictive complement.

```yaml
id: GO-P-2026-042
date: 2026-08-02
retrospective: false
kind: theorem-verification (C3 numerical falsification of analytic results)
claim: "Rate-work-distortion region RW_C(D); Pareto-channel equation; binary frontier + matched-rate inversion; materialization barrier; multi-consumer TC; Gaussian + temperature-weighted water-filling; staleness complement."
harness: experiments/verify_consumer_landauer.py   # pure numpy, Tier A, deterministic seed 20260802
prediction:
  prop2: product-BSC channels realize the closed form to 1e-10; no admissible channel
    (4000 random + the eq.-(20) optimizer at 11 support directions) beats any support
    line of the frontier by 1e-7; matched-rate inversion exact (ratio 8.42)
  prop1: the eq.-(20) alternating update never increases J (worst uptick < 1e-9);
    converged channels satisfy eq. (20) to 1e-6 on their support; no random channel
    beats J*; alpha=1 reproduces R(D)=1-h2(D) to 1e-6; midpoint convexity of BOTH
    coordinates holds on 2000 random instances
  thm1_converse: no random deterministic finite-n code (n in {1,2}, exact H(M|S^n),
    optimal decoder) lands below the closed-form boundary at its own distortion
  thm2: H(A,M|S^n) = nH(X|S) and the chain rule to 1e-9; Delta-W never negative
  cor23: R_C(0)=H(U), L_C(0|S)=H(U|S) to 5e-3 via the optimizer; TC >= 0 on 400
    random 3-consumer reads, strictly positive somewhere (> 0.05 bits)
  cor4: eq.-(41) water-filling equals the max-det reverse water-filling program to
    1e-7 (rank-deficient reads included); no admissible random Gaussian code beats it
  prop3: dual-bisection d* feasible + KKT to 1e-6; no random feasible allocation
    beats W*; equal-T reduces to the isothermal water level
  prop4: L_t nondecreasing on 40 random finite chains (exact); binary example
    identity + complement-to-1 to 1e-10
falsification: any section failing its bar refutes the corresponding claim and sends
  it back to the proof; the harness prints VERDICT ALL PASS / FAIL per section.
verification:
  - R-IND-5 derivation-grade fresh-context adversarial pass on the full paper,
    logged 2026-08-02 (ledger VI-8). VERDICT: 0 errors, 4 sharpenings, nothing
    unsalvageable. SHARPENINGS the pass caught before the paper asserts them:
    (a) Prop 1's proof asserts convexity of I(X;Xh|S) in q without argument, and the
    difference route FAILS (I(S;Xh) is convex in q, not concave); the correct
    argument is the per-s decomposition I(X;Xh|S) = sum_s p(s) I_{p(x|s)}(q), each
    term convex at fixed input; (b) "time sharing among at most three test channels"
    is true but vacuous -- the union in (10) is already closed and convex (both
    coordinates convex in q, T_C(D) convex/compact), so no time sharing is needed;
    (c) the converse should state that the induced per-letter channels satisfy
    Xh_i - X_i - S_i (true for i.i.d. pairs; survives the Q-mixture since p(s|x) is
    common); (d) Thm 3 needs a one-line vector-distortion remark, and Prop 4's
    hypothesis should read "M independent of the future trajectory given X_0"
    (what the proof uses) rather than the pairwise chain. Paper revision notes:
    paper/consumer-relative-landauer-REVISION-NOTES.md.
amendments: []
hash: sha256:ad0c0f32c64034e7fb7dcdfdc97c3bd40d9c05cff9f39ecc087ab5094b932041
```

## Falsification
The results are analytic; the harness is a falsification net, not the proof. A mismatch
on any registered prediction sends the corresponding claim back to the proof. The
derivations are additionally checked by the fresh-context adversarial pass above, whose
verdict and sharpenings are recorded before the paper asserts the results (charter
rules R-IND-5, C-AI-2).
