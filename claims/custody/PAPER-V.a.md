# Custody: PAPER-V.a

## Claim

Six results of Paper V (`paper/consumer-relative-landauer.tex`), as statements about the
information quantities and the single-letter region $\mathcal U_{\mathcal C}(D)$:
- **Lemma 1** (`lem:convexity`): $I(X;\hat X)$ and $I(X;\hat X\mid S)$ are convex in the test
  channel.
- **Prop 1** (`prop:pareto-channel`): the Pareto-channel equation (21) holds on the support of a
  minimizer of (20), and an interior KKT solution is globally optimal.
- **Cor 2** (`cor:exact-output`): for a deterministic consumer output $U$, the single-letter
  minima are $R_{\mathcal C}(0)=H(U)$ and $L_{\mathcal C}(0\mid S)=H(U\mid S)$ (23).
- **Prop 2** (`prop:binary-frontier`): the two-bit example's lower boundary (26)–(27).
- **Prop 5** (`prop:thermal-waterfill`): the temperature-weighted water-filling (50)–(51), as the
  solution of its optimization under the independent eigenmode memory model.
- **Prop 6** (`prop:stale`): $L_t=H(M\mid X_t)=H(M)-I(M;X_t)$ (54), nondecreasing in $t$.

The row does not claim the operational reading of Prop 2 (that the boundary of
$\mathcal U_{\mathcal C}(D)$ is the boundary of the achievable region $\mathrm{RW}_{\mathcal C}(D)$).
That is Theorem 1, ledger row PAPER-V.c. Nor does it claim the physics that reads an information
quantity as reset work.

## Proof

In `paper/consumer-relative-landauer.tex`, the proofs following each statement:
`lem:convexity`, `prop:pareto-channel`, `cor:exact-output`, `prop:binary-frontier`,
`prop:thermal-waterfill` and `prop:stale`. None of the six statements or proofs has changed
since commit 44a5039, the text VI-41 read. The two later commits (431bad7, 1e8c5fb) touch other
results only.

## R-IND-5

- **VI-8:** the whole paper, at an earlier draft, with 0 errors. It is the derivation-grade
  reading of Cor 2, whose text has not changed since.
- **VI-41:** re-read the text folded in after VI-8, together with the two nets and their fire
  test. It found no false step. It re-derived Lemma 1 and Prop 2, checked the steps of Props 1,
  5 and 6, and checked Cor 2 through its net only.
- **VI-46:** re-derived all six results at the current text: Lemma 1, Prop 1's KKT step,
  Prop 2, Cor 2, Prop 5 and Prop 6.
- **The split:** VI-41 proposed splitting Paper V into four ledger rows, of which this is (a).
  The author accepted the split on 2026-11-21: "yes, I accept. Proceed as you recommend".
- **VI-41 #10 is not settled, and this row does not rest on it.** That item left it to the
  author whether VI-41 counts as the re-reading of the text folded in after VI-8, and the
  question was never put to the author separately. VI-46's re-derivation is what covers the
  current text.

## C3 harness

| Harness | Tier | CI section |
|---|---|---|
| `experiments/verify_consumer_landauer.py` | re-run | `ci/reproduce.py` [1c]; sealed net of GO-P-2026-042; CI requires `VERDICT: ALL PASS` |
| `experiments/fire_paper5_nets.py` | committed-artifact | not run in CI (about 17 min on 8 cores); its output `results/PAPER5-fire.json` is cited below |

The fire test runs mutated copies of the net. Each gate inserts a wrong claim, and the net must
reject it. All 18 gates fired. The measured values below come from the fire test's unmutated
control run, `results/PAPER5-CL-control.log` (2026-11-21, Atlas, numpy 2.4.6). The JSON records
that log's sha256.

The net is sealed and keeps its old numbering. Its "Prop 3" is the paper's Prop 5, its "Prop 4" is
Prop 6, and its "eq.(20)" is the paper's (21) (VI-41 #1).

## Constants and slack

| Constant | Defined at | Proved bound | Measured | Source | Slack |
|---|---|---|---|---|---|
| Lemma 1, midpoint convexity of both coordinates | `lem:convexity` | 0 violations | `violations = 0/2000` | `results/PAPER5-CL-control.log` | sign tested at 1e-10 (VI-41); 2000 sampled midpoints, a net and not a proof |
| Lemma 1, negated claim (CL5, gate) | `lem:convexity` | must be caught | `FAIL: ['prop1-convexity-violations=2000']` | `results/PAPER5-fire.json#mutations.7.verdict` | caught at every sampled midpoint |
| Prop 1, fixed point (21) at the computed minimizer | (21) | exact | `eq.(20) self-consistency worst = 1.6e-07` | `results/PAPER5-CL-control.log` | an identity of the iteration that produces the channel, so it cannot fail (VI-41 #15, VI-46); the probes CL4 and CL4b mutate both sides of it. Only the optimality net in the next row can fail on Prop 1 |
| Prop 1, no random channel beats the minimum J⋆ | (20) | 0 | `random channels beating J* = 0` | `results/PAPER5-CL-control.log` | the closest random channel is 0.26% above J⋆ (VI-41) |
| Prop 1, mutated equation, S-term halved (CL4, probe) | (21) | must be caught | `True` | `results/PAPER5-fire.json#mutations.5.fired` | probe, not gate |
| Cor 2, both endpoints, 15 random exact consumers | (23) | = 0 | `worst = 1.7e-13` | `results/PAPER5-CL-control.log` | bar 5e-3 |
| Cor 2, claim R_C(0) = H(X) (CL8, gate) | (23) | must be caught | `True` | `results/PAPER5-fire.json#mutations.13.fired` | |
| Prop 2, product-BSC channels realize (26)–(27) | (26)–(27) | exact | `worst residual = 7.8e-16` | `results/PAPER5-CL-control.log` | roundoff |
| Prop 2, no admissible channel below the boundary | (26)–(27) | 0 violations | `2056 admissible channels (random + optimizer), violations = 0` | `results/PAPER5-CL-control.log` | 0.0074 to 0.13 bits, depending on direction; D = 0.15 only (VI-41 #6) |
| Prop 2, boundary raised by 0.05 (CL1, gate) | (26)–(27) | must be caught | `FAIL: ['prop2-converse-violations=6']` | `results/PAPER5-fire.json#mutations.2.verdict` | a raise of 0.01 is caught as a probe (CL1[0.01]); 0.001 is not (CL1[0.001]) |
| Prop 2, closed form lowered by 1e-3 (CL2, gate) | (26)–(27) | must be caught | `True` | `results/PAPER5-fire.json#mutations.3.fired` | |
| Prop 2, worked example at matched rate R = 1.1187 | text after Prop 2 | L = 0.1187 and 1.0000 | `L = 0.1187 vs 1.0000 (ratio 8.42x)` | `results/PAPER5-CL-control.log` | CL3 (L = 0.9 claimed for the second code) is caught |
| Prop 5, feasibility, KKT and the equal-T reduction (one printed residual) | (50)–(51) | exact | `feasibility+KKT+equal-T worst = 1.8e-15` | `results/PAPER5-CL-control.log` | 5.6e-10 relative (VI-41). The equal-T clause is an identity; the feasibility and KKT checks can fail on a wrong formula, and the section catches CL12 (below) |
| Prop 5, random allocations never beat the water-filling | (50)–(51) | 0 violations | `random-allocation violations = 0` | `results/PAPER5-CL-control.log` | a check independent of the formula |
| Prop 5, d⋆ = min{λ, ν√T} (CL12, gate) | (50) | must be caught | `True` | `results/PAPER5-fire.json#mutations.19.fired` | |
| Prop 6, monotonicity on 40 random finite chains | (54) | no decrease | `monotonicity violations = 0, worst decrease = 1.8e-15` | `results/PAPER5-CL-control.log` | 1e-10 (VI-41) |
| Prop 6, monotonicity tested on I(M;X_t) (CL13, gate) | (54) | must be caught | `True` | `results/PAPER5-fire.json#mutations.20.fired` | |
| Prop 6, binary example and the complement to 1 bit | text after Prop 6 | exact | `complement-to-1 worst = 1.6e-15` | `results/PAPER5-CL-control.log` | the complement-to-1 clause is an identity and cannot fail (VI-41 #15); CL14 (wrong q_t) is caught |
| Fire test, gates fired (both nets) | `experiments/fire_paper5_nets.py` | all | `18` | `results/PAPER5-fire.json#counts.gates_fired` | out of 18 gates; 9 of 17 probes fired |

## Known gaps

- **Prop 2's operational reading is not in this row.** The boundary is the boundary of
  $\mathrm{RW}_{\mathcal C}(D)$ only through Theorem 1. Theorem 1 is proved and verified, but no
  check can fail on it (VI-41), so it is ledger row PAPER-V.c, at `[exploratory]`.
- **Prop 2's net is narrow.** It covers D = 0.15 only. Its resolution runs from 0.0074 to
  0.13 bits depending on direction, and a 0.015-bit raise of the boundary for t < 0.9 D was not
  caught (VI-41 #6).
- **Imported physics.** Reading $kT\ln2$ times an information quantity as ideal reset work
  rests on Landauer's bound (7) and its asymptotic tightness. Prop 5's independent eigenmode
  memory model is a modelling assumption. Both are imported, not proved: this row covers the
  information-theoretic statements and the optimization.
- **Checks that cannot fail.** These are noted, not counted as nets: Prop 1's self-consistency
  residual, Prop 5's equal-T clause, the complement-to-1 identity and ΔW ≥ 0 (VI-41 #15,
  VI-46).
- **Fire-test custody.** The fire test was committed only after its two attempts, and its JSONs
  lack the edit texts and the hashes of the script and the mutants (VI-41 #11). A future run
  records all three and is committed before it runs.
- **CI checks the verdict line only.** The measured values above are from the fire test's
  control run, not from each CI run.
