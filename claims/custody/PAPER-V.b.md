# Custody: PAPER-V.b

## Claim

Paper V's two Gaussian propositions, as statements about the single-letter region
$\mathcal U(D)$, the union over test channels with $\mathbb E\,d\le D$ of the quadrants
$\{R\ge I(X;\hat X),\ L\ge I(X;\hat X\mid S)\}$:
- **Prop 3** (`prop:scalar-corner`). For a scalar jointly Gaussian pair with
  $\rho\in(-1,1)$, squared error and $0<D<\sigma^2$, $\mathcal U(D)$ is the quadrant (44). Both
  bounds are attained by the classical reverse channel. The discount (45) decreases in $D$ and
  increases to $I(X;S)$ as $D\to0$.
- **Prop 4** (`prop:vector-frontier`). For $r$ mutually independent jointly Gaussian pairs with
  $\rho_i\in(-1,1)$, weights $p_i>0$ and $0<D<\sum_ip_i\sigma_i^2$, the lower boundary of
  $\mathcal U(D)$ is traced by the allocation rule (47) and the frontier (48). This includes
  the step its proof takes first, the component inequalities
  $I(X;\hat X)\ge\sum_iI(X_i;\hat X_i)$ and $I(X;\hat X\mid S)\ge\sum_iI(X_i;\hat X_i\mid S_i)$
  for any test channel with $\hat X-X-S$. These are Appendix A's chain-rule step applied across
  the independent pairs of one letter.
- **Cor 4** (`cor:gauss`), added 2026-11-21, as a single-letter statement for
  $\Sigma_X\succ0$. Without reset side information and for $0<D<\sum_i\lambda_i$,
  $R_{\mathcal C}(D)=L_{\mathcal C}(D)=\tfrac12\sum_i[\log_2(\lambda_i/\theta)]_+$ (42), where
  $\lambda_i$ are the nonzero eigenvalues of $\Sigma_X^{1/2}P_{\mathcal C}\Sigma_X^{1/2}$ and
  $\sum_i\min(\lambda_i,\theta)=D$ (41). The work law (43) is the same quantity times
  $k_BT\ln2$, read as work through Landauer's bound.
  - **What is claimed:** every test channel's $I(X;\hat X)$ is at least this, and a Gaussian
    channel attains it.
  - **How it is netted:** it is Paper III's `lem:maxdet` rate identity, with
    $P=P_{\mathcal C}$, in bits. That identity requires $\Sigma_X\succ0$, and its net draws only
    positive definite covariances.

Not claimed in this row:
- **Props 3 and 4, operationally.** That every code's rate–work pair lies in $\mathcal U(D)$ is
  the general-alphabet converse of Appendix A, with the closed-graph property in Prop 4's proof,
  and belongs to ledger row PAPER-V.c. Achievability with side information on continuous
  alphabets is not claimed either.
- **Cor 4's operational reading** (VI-49 #1): that these are also the least rate and the least
  ideal reset work that codes approach at average distortion $D$.
  - **What it would rest on.** External results checked at the source: Polyanskiy and Wu's
    Theorem 24.2 for achievability; for the converse without side information, the classical
    chain $\log M\ge H(M)\ge I(X^n;\hat X^n)\ge n\varphi(D_n)$ (their Theorems 23.2 and 24.1),
    with $\varphi$ continuous (their Theorem 23.3(2)).
  - **Why it stays out.** No check can fail on it: CL's random codes stay at least 6.1% above the
    optimum. The paper's own text takes the converse step through its per-code converse, which
    is PAPER-V.c. The same operational content is Paper III's `thm:coding` (book B1), which is
    `[exploratory]`.
  - **What would bring it in.** A rule from the author for imported operational readings,
    applied to B1 as well.
- **Cor 4 for singular $\Sigma_X$.** The paper's proof covers it, by restriction to the range of
  $\Sigma_X$, but the net does not test it.

## Proof

In `paper/consumer-relative-landauer.tex`, the proofs following `prop:scalar-corner` and
`prop:vector-frontier`. Prop 4's proof includes:
- the component inequalities, by the general-alphabet chain-rule step of Appendix A
  (`app:converse`) applied across the pairs rather than across time;
- the component factorization;
- the allocation characterization of $\mathcal U(D)$ in both directions;
- the box argument for closedness.

These were rewritten in 431bad7 (VI-43), and Prop 4's hypotheses were stated in full there.
The same chain-rule step, applied across time to a code, is the per-code converse in row
PAPER-V.c. Here it is used only within one letter, and it is part of this row's claim.

Cor 4's proof follows `cor:gauss`. It changes variables to $Z=V^\top P_{\mathcal C}^{1/2}X$, gets
the bound from Prop 4 at $\rho_i=0$ with unit weights, and gets attainment from the pull-back
$\hat X=(P_{\mathcal C}^{1/2})^{+}V\hat Z$. This proof was added in 1e8c5fb and given its
exposition edits in 1e9cc77. The paragraph before the corollary cites Theorem 24.2 for the
operational reading, which this row does not claim.

## R-IND-5

- **VI-9:** the original propositions.
- **VI-41:** re-derived Prop 3, and checked Prop 4's steps together with the net GS and its fire
  test.
- **VI-43:** the rescoping to $\mathcal U(D)$, Prop 4's full hypotheses, Prop 3's no-density
  clause, and Appendix A's general-alphabet converse.
- **VI-44:** a confirming pass, with 0 errors. It re-derived both inclusions of the allocation
  characterization, the box argument and closedness, the no-density clause and the worked
  example (ΔL = 0.1105, ΔR = 0.1306).
- **VI-46:** re-derived Prop 3 (the linear estimate and its stationarity condition) and Prop 4
  (the quadratic, the uniqueness of the level μ, the box argument). It also checked Cor 4's new
  proof line by line, including singular $P_{\mathcal C}$, and found it correct.
- **VI-47:** read Theorem 24.2 at the source for Cor 4's operational reading, found it sound, and
  checked Cor 4's two exposition edits.
- **VI-48 and VI-49:** reviewed the rate-identity net. VI-49 also reviewed Cor 4's addition,
  scoped it to the single-letter statement for $\Sigma_X\succ0$, and confirmed Polyanskiy and
  Wu's Theorems 23.2–23.4 and 24.1–24.2 at the source.

The author accepted VI-41's four-row split on 2026-11-21 ("yes, I accept. Proceed as you
recommend"). VI-41's text for this row reads: "(b) Props 3–4 as single-letter statements …
Cor 4 joins them once it has a net that is not circular." Cor 4 joins on that basis. Its
operational reading was not put to the author, and is not claimed.

## C3 harness

| Harness | Tier | CI section |
|---|---|---|
| `experiments/verify_gaussian_sideinfo.py` | re-run | `ci/reproduce.py` [1c]; sealed net of GO-P-2026-044; CI requires `VERDICT: ALL PASS` |
| `experiments/fire_paper5_nets.py` | committed-artifact | not run in CI; its output `results/PAPER5-fire.json` is cited below |
| `experiments/verify_paper3_rate_identity.py` | re-run | `ci/reproduce.py` [2/3], file mode; Cor 4's net: the same identity in Paper III's notation ($P=P_{\mathcal C}$, nats) |

**Cor 4's net.** CL's own Cor 4 check (CL11) computes one closed form twice (VI-41 #4), and its
random-code net tests only the converse side. Cor 4's non-circular net is the rate-identity
harness written for Paper III. It tests quantizer and Gaussian channels against the formula, and
the backward channel's feasibility. Two caveats:
- **Its power gates show nothing.** VI-48 found that its own power gates are passed by the
  formula's own optimum channel (its "bits for nats" gate cannot fail), and showed its power with
  self-consistent mutants instead.
- **Its achievability checks guard one side only.** They pass trivially for the correct closed
  form, but fail on a self-consistent formula that is too low (VI-49). Achievability itself
  rests on the proof.

The limits are in PAPER-III.a's custody file.

The Props 3–4 values below come from the fire test's unmutated control run,
`results/PAPER5-GS-control.log` (2026-11-21, Atlas). Its sha256 is recorded in the fire test's
JSON. GS tests the region through channels (Gaussian channels, scalar quantizers, a discretized
optimizer and random allocations), not through codes.

## Constants and slack

| Constant | Defined at | Proved bound | Measured | Source | Slack |
|---|---|---|---|---|---|
| Prop 3, moment-level minimum of L against the closed form | (44) | exact | `worst dev = 3.5e-04` | `results/PAPER5-GS-control.log` | a numerical minimum over admissible moments; GS2 (ρD written for ρ²D) is caught |
| Prop 3, Gaussian channels lie on one curve (no scalar tradeoff) | the remark after Prop 3 | L a function of R alone within the Gaussian family | `worst = 1.8e-15` | `results/PAPER5-GS-control.log` | roundoff; GS4 (the curve with 1 − ρ) is caught |
| Prop 3, non-Gaussian quantizers never beat either bound | (44) | 0 violations | `quantizer channels tested = 400; bound violations = 0` | `results/PAPER5-GS-control.log` | the quantizers come within 0.019 bits (VI-41); a raise of 0.1 is caught (GS3[0.1], probe), 0.01 is not |
| Prop 3, discretized optimizer at ρ = 0.5, the L corner | (44) | 0.8502 | `L(a=0)=0.8506 (analytic 0.8502)` | `results/PAPER5-GS-control.log` | discretization error |
| Prop 3, discretized optimizer at ρ = 0.9, the L corner | (44) | 0.3254 | `L(a=0)=0.3423 (analytic 0.3254)` | `results/PAPER5-GS-control.log` | 0.017 bits above, from discretization; a corner shifted by 0.1 is caught (GS5[0.1], probe), 0.05 is not |
| Prop 3, the discount (45) | (45) | decreasing, limit I(X;S) | `discount decreasing in D and -> I(X;S) at D->0: True` | `results/PAPER5-GS-control.log` | GS9 (limit claimed as log2(1/(1−ρ²))) is caught |
| Prop 4, allocation (47): feasibility, KKT, omitted modes and the α = 1 case (one printed residual) | (47)–(48) | exact | `feasibility+KKT+omitted+classical worst = 1.75e-14` | `results/PAPER5-GS-control.log` | the omitted-mode and α = 1 clauses are identities (VI-41 #15); the feasibility and KKT checks can fail on a wrong allocation |
| Prop 4, random allocations never beat (47) | (47)–(48) | 0 beats | `random-allocation beats = 0` | `results/PAPER5-GS-control.log` | the closest random allocation sits 0 bits above at r = 2 and 0.14 bits at r = 8 (VI-41) |
| Prop 4, the quadratic's linear term mutated (GS6, gate) | (47) | must be caught | `True` | `results/PAPER5-fire.json#mutations.30.fired` | |
| Prop 4, the strict-frontier example, the L gap | worked example after Prop 4 | 0.1105 | `L-gap=0.1105` | `results/PAPER5-GS-control.log` | GS7's bar of 0.05 is looser than the gap (VI-41 #14) |
| Prop 4, the strict-frontier example, the R gap | worked example after Prop 4 | 0.1306 | `R-gap=0.1306` | `results/PAPER5-GS-control.log` | as above |
| Cor 4, no skew quantizer beats (42) (independent of the formula) | (42) | ≥ 0 | `0.0435` | `results/PAPER3-rate-identity.json#converse.min_gap.skew` | in nats, from Paper III's rate-identity harness |
| Cor 4, no random Gaussian channel beats (42) (independent of the formula) | (42) | ≥ 0 | `1.4e-7` | `results/PAPER3-rate-identity.json#converse.min_gap.gauss_random` | one instance aligned by chance (VI-48) |
| Cor 4, smallest near-optimal gap at eps = 1e-3 | (42) | ≥ 0 | `6.1e-8` | `results/PAPER3-rate-identity.json#attained.near_optimum_min_gap.eps3` | a one-sided first-order descent test around the formula's own optimum. VI-48's self-consistent wrong formulas were caught by it down to a median excess of 1.4e-7 nats; the harness's own power gates do not show this |
| Cor 4, smallest slack of Paper III's `lem:info` step, two-dimensional quantizers | (42), through Paper III's route | ≥ 0 | `0.0164` | `results/PAPER3-rate-identity.json#lemma_info.min_slack.skew` | weak in relative terms: a `lem:info` strengthened by a factor of about 1.26 would pass (VI-48). Cor 4's own proof goes through Prop 4, but the net tests the statement |
| Cor 4, CL's random-code net on the converse side | (42) | 0 violations | `admissible Gaussian codes tested = 6869, violations = 0` | `results/PAPER5-CL-control.log` | random codes come no closer than 6.1% above the optimum (VI-41) |
| Prop 4, two-mode full channel at α = 0 against the per-mode envelope | proof of Prop 4 | ≥ envelope | `weighted objective 1.2832 vs per-mode envelope 1.2836` | `results/PAPER5-GS-control.log` | the measured value is 4e-4 *below* the envelope. It passes because the envelope is taken over a 13-point grid of budget splits with a tolerance of 5e-3 (`verify_gaussian_sideinfo.py`, lines 370 and 390). Separability resolution is 5e-3 to 1e-2 (VI-41); GS8 (envelope raised by 0.01) is caught |

## Known gaps

- **Single-letter statements only.** The code-level converse ($\mathrm{RW}_{\mathcal C}(D)\subseteq
  \mathcal U(D)$) is proved (Appendix A and the closed-graph property, VI-43 and VI-44), but no
  net tests codes on the Gaussian source, so it is in row PAPER-V.c. Achievability on continuous
  alphabets is not claimed.
- **The component inequalities are netted only in part.** GS[6] tests them on one quantized
  two-mode source, at α ∈ {0, 1}, to 5e-3 (VI-46).
- **Cor 4's operational reading and singular $\Sigma_X$ are not claimed.** See the Claim. On
  2026-11-21 the assistant read Polyanskiy and Wu's Definition 23.1 and Theorems 23.2, 23.3 and
  24.1–24.4 at the source; that reading is not recorded except here. VI-47 and VI-49 read them
  independently.
- **Cor 4's net comes from another paper.** It is Paper III's rate-identity harness. Its
  resolution limits are listed in PAPER-III.a. CL11, Cor 4's own check in Paper V's sealed net,
  remains circular.
- **The nets are sealed (044).** GS's checks of degeneracy and of the α = 1 case cannot fail
  (VI-41 #15). GS7 mutates the input rather than the claim (VI-41 #14).
- **Imported physics.** Reading L as reset work rests on Landauer's bound (7).
- **CI checks the verdict line only.** The values above are from the control run.
