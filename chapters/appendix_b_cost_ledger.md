# Appendix B — The COST Ledger: Theorems, Proofs, and Falsification Harnesses

*Staging tier [B].* This appendix carries the statements and proof status of the
COST-face theorems (Paper III).

**What `[proved]` requires.** Under the charter's theorem-custody rule (T-CUST-1), a
theorem reaches `[proved]` only when it ships four things:
1. a written proof;
2. an R-IND-5 fresh-context adversarial pass;
3. a committed C3 numerical falsification harness, built to fail if the theorem is false;
4. a constants/slack and known-gaps table.

A green harness is a net, not a proof (T-CUST-2). Full proofs live in Paper III and its
appendix. This ledger gives each statement, its status, its custody, and the verification
incidents it survived.

**Status as of 2026-11-20.** A custody pass (VI-32, `claims/audits/VI-32-PaperIII-B.md`)
found that this appendix had overstated itself:
- no theorem here has a custody table, so none is `[proved]`;
- three of its statements misstated Paper III (B1, B4, B6);
- one constant was wrong (B7, NEG-18);
- some of the harnesses could not fail.

The classes below are corrected to the ledger, which wins (Appendix F). A theorem whose
statement is netted by a sealed C3 registration is `[predicted]`-grade until its custody
table exists.

## Conventions

- Source $x$ with covariance $\Sigma_x$.
- Observer read metric $P$ (dropping the subscript $C$).
- Coding error $\delta$, with covariance $\Sigma_\delta$.
- Read distortion $D = \operatorname{tr}(P\Sigma_\delta)$.
- The **whitened** basis is $\Sigma_x^{1/2} P \Sigma_x^{1/2}$. Several constants are correct
  only in this basis, the recurring lesson of VI-4 and VI-6.

## Thm B1 — Consumer rate–distortion achievability & converse

**Statement.** For a Gaussian source and read metric $P$, the minimum rate to achieve read
distortion $D$ is $R_C(D)$. It is achieved by a test channel that does reverse
water-filling in the whitened basis, on the tilted source $Y = P^{1/2}X$ (Paper III
`prop:rd`, `lem:tilt`, `thm:coding`, `cor:coding`).

(Paper III's own `thm:B1` is a different result: the coding theorem for the true
divergence. An earlier sentence here, "the reduction in true divergence … is the tilt",
matched no statement and is withdrawn.)

**Status.**
- R-IND-5: VI-3.
- `thm:coding` has no C3 net of its own; `verify_appendixB.py` nets `thm:B2`/`cor:B2a` and
  part of `thm:B3`.
- **`[exploratory]` pending a net and custody.**

**Custody / gaps.**
- Verbatim Kostina–Verdú transfer holds for the fixed-$P$ Gaussian case.
- The true nonlinear consumer keeps its "should port" hedge.
- Constants hold in the whitened basis only.

## Thm B2 — Output ≤ surrogate ≤ reconstruction at matched rate

**Statement.** At matched rate, coding for the consumer's output metric is no worse than
coding for a surrogate read metric, which is no worse than coding for reconstruction, on
the consumer metric. This is Paper III's registered prediction GO-6, not its `thm:B2`,
which is the output-reduction theorem.

**Status.** `[demonstrated]` by the ledger, and **disputed** (VI-32, VI-34): the findings below
mean the harness does not test the claim's matched-rate premise. A re-run at matched rate is
owed, and the class is the author's to set. What GO-6 (GO-P-2026-028) measured:
- the ordering holds at every rate tested;
- reconstruction is up to about 500× worse at high rate;
- the median gap is $+2.45$;
- the isotropic control collapses the three coders.

**What VI-32 found:**
- No theorem gives the ordering, the "kernel entropy share" (which is undefined) or the
  rate dependence, so the earlier "the analytic statement is proved" is withdrawn.
- The harness charges (b) and (c) a backward-channel rate while measuring their
  distortion with forward noise, so the rates are not exactly matched.
- The harness's isotropic control assigns all three curves the same array.

## Thm B3 — The surrogate–output gap vanishes with rate

**Statement.** The relative gap $(b - a)/(c - a)$ between a surrogate-optimal and an
output-optimal code shrinks to zero as the rate grows (GO-6 (iii)). Paper III's `thm:B3` is
the high-resolution formula, a different statement.

**Status.** `[demonstrated]` by the ledger, and **disputed** with B2, since it uses the same
harness: GO-6 measures the gap falling from $0.41$ to $0.005$. There is
no analytic theorem; VI-3 graded the high-resolution argument PLAUSIBLE-with-conditions.
Its Linder–Zamir conditions are cited, not checked, and the formula also needs
$\mathbb E\log\det G<\infty$.

**Consequence.** At high resolution a surrogate for $P$ suffices; at low resolution it does
not. This is why the blind probe (Chapter 10) is load-bearing precisely in the bit-starved
regime.

## Thm B4 — Two-observer region & refinability

**Statement.** The achievable rate region for two observers $(P_1, P_2)$ is the
max-determinant region of Paper III (`thm:region`), with $0\prec\Sigma_f\preceq\Sigma_b\preceq\Sigma_x$.

A single scalable code serves the coarse observer with a prefix of the fine observer's bits
**iff the observers' optimal error covariances nest, $\Sigma_2^\star\preceq\Sigma_1^\star$**
(`thm:multiobs`). This condition depends on $D_1$ and $D_2$.

Non-nested optima incur the exact rate loss of `thm:multiobs-loss`.

**Correction (VI-32).** This appendix used to state the criterion as "iff
$P_1\preceq P_2$". That is false in both directions:
- not refinable although $P_1\preceq P_2$: $\Sigma_x=I_2$, $P_1=\mathrm{diag}(1,0)$, $P_2=I$,
  $D_1=0.5$, $D_2=1.2$;
- refinable although $P_1\not\preceq P_2$: $P_1=2I$, $P_2=I$, $D_1=1$, $D_2=0.2$.

The paper always had it right.

**Status.**
- Proof plus R-IND-5 (VI-4).
- Sealed net 022, but that net is weak. VI-32 re-inserted VI-4's original bug into
  `verify_two_observer.py`, and checks [1]–[3] still pass. Only `verify_rate_region.py` [3]
  catches it.
- **`[predicted]`-grade, with the weak net disclosed, pending a real net and custody.**

**Verification incident (VI-4, standing).**
- *The bug.* An in-context `sigma_star` formula used
  $(\Sigma^\star)^{-1} = \Sigma_x^{-1} + \lambda P$, with the inline claim "the cap never
  binds".
- *The catch.* A fresh-context adversarial pass found that the max-det error covariance is
  reverse water-filling in the whitened basis, and that the cap **does** bind on $\ker P$.
- *The fix.* The formula was corrected and the harness re-run. The analytic theorem
  statement was unaffected; the harness was wrong.
- *Later (VI-32).* The "decisive" check added then is an algebraic identity that holds for
  any nested pair, so it cannot detect the bug.

## Thm B5 — Complete rate region & the $k$-observer chain

**Statement.**
- **Converse and the necessity of nesting:** for $k$ observers in a chain, the achievable
  region is contained in the chain of nested max-det covariances (`cor:kobs`, with
  $0\prec\Sigma_k$), and refinability implies that the single-stage optima nest. Paper III
  proves both, with the $n$-block step added in 2026-11.
- **For $k=2$** the region is equal to that set, and refinability is equivalent to nesting
  (`thm:region`, `thm:multiobs`).
- **Achievability for $k\ge3$, and with it the sufficiency of nesting:** the
  independent-Fisher-increment Gaussian test channel realizes every feasible chain, but
  turning it into codes is not proved in Paper III. The abstract-source region is
  attributed to Kostina–Tuncel, and whether its hypotheses cover this case is to be
  checked at the source.

**Status.**
- $k=2$ (the corner): proof, R-IND-5 (VI-5), and the sealed net 023, whose check [3] is a
  real net for the corner. **`[predicted]`-grade.**
- The region converse: proof and R-IND-5, but no net that can fail. 023's [1] is an
  identity, and [2] cannot fail on the region's coupling. **`[exploratory]` until a net
  exists.**
- Achievability for $k\ge3$: **owed.**

**Verification incident (VI-5).** Two errors were caught before publication:
- (a) the citation: Rimoldi's is the finite-alphabet $L$-stage result;
- (b) the two-stage K-map **does not iterate**: an accumulating rotation ambiguity leaks
  Fisher information by $O(0.1)$ per stage.

Achievability was restated with independent increments. VI-32 found that the follow-on
claim, that the two-stage arguments "extend verbatim", was itself unproved. It is now
withdrawn in Paper III.

## Thm B6 — The price of a misidentified observer: tax and floor

**Statement (tax).** Suppose the coder's metric $\hat P$ and the consumer's $P$ satisfy
$m\hat P\preceq P\preceq M\hat P$ on their shared range (equal ranges, Loewner constants
$0<m\le M$). Then the design built for $\hat P$, $\Sigma^\star(\hat P,D/M)$, meets the
consumer's distortion $D$ at an excess rate of at most $(r/2)\log(M/m)$, in the coding
regime the theorem states, and the $r/2$ is sharp (`thm:commission`, which gives the exact
design and regime).

(This appendix used to say "a rank-$M$ read metric when the consumer's is rank $m<M$",
which confuses the Loewner constants with ranks; VI-32.)

**Statement (floor).** Every allocation in the $\hat P$-water-filling family, when $\hat P$
omits a direction the consumer reads, hits a distortion floor
$D \ge D_{\text{floor}} = \operatorname{tr}(\tilde P\Pi)$, with the whitened kernel.
The achievable band is the compact $[D_{\text{floor}}, \operatorname{tr}(P\Sigma_x)]$: a
floor, not unbounded distortion (`thm:omission`).

**Status.**
- Proof plus R-IND-5 (VI-6), and the sealed net 024. Its commission bound is a real check;
  its omission "alt" floor is a tautology.
- **`[predicted]`-grade, pending custody.**
- The floor is also `[demonstrated]` downstream on a trained model: GO-P-2026-027,
  held-out layers {4,20}, floor 16/16, asymptotic ratio 800–5700×.

**Verification incident (VI-6).** Two corrections were made before publication:
- omission gives a *floor*, not unbounded distortion;
- the floor uses the *whitened* kernel. A naive kernel projector overstates it by about
  30% when $\Sigma_x \ne I$.

The 0.647 Llama overlap is a **conditional** certificate. It holds given omission, equal
weights **and** an isotropic source ($\Sigma_x=I$). VI-32 restored the isotropy
condition, VI-6's own lesson.

**Related negative (NEG-13 → resolved).** The first sealed finite-rate gate for the floor
*missed* (0/16), a shallow-sweep artifact that conflated "floor reached" with "floor
exists". It was resolved by a fresh held-out test, not by relaxing the bar (Chapters
15–16).

## Thm B7 — Dispersion counts at most the read dimensions

**Statement.** The finite-blocklength consumer coding problem is the $r$-dimensional
tilted problem at every blocklength (`prop:dispersion`, by a covering argument). For the
Gaussian quadratic case its dispersion is

$$V_Y(D)=\tfrac12\Bigl[r_D+\sum_{k:\,0<\gamma_k\le\theta}(\gamma_k/\theta)^2\Bigr]\ \text{nats}^2,\qquad r_D\le 2V_Y\le r,$$

with $\gamma_k$ the tilted mode variances, $\theta$ the water level, and $r_D$ the active
modes (`cor:dispersion`). Equality holds on the right iff $\gamma_k\ge\theta$ for every
$k$, which covers the whole low-distortion regime. It counts at most the $r$ read
dimensions, never the ambient $d$. (A first correction wrote "$<r$", which fails when
every mode is active.)

**Correction (NEG-18, VI-32).** This appendix, Paper III and prereg 025 gave the
dispersion as $(r_D/2)\log^2e$, counting only the active modes. The value came from
VI-7's "sharpening". Modes below the water level contribute too, because fluctuations of
their energy are absorbed by the active modes. A Monte Carlo at
$\gamma=(4,2,0.6,0.3)$, $\theta=1$ gives a variance of 1.226 against the claimed 1.0. The
bound survives.

**Status.**
- The finite-$n$ reduction: proof plus R-IND-5 (VI-7), and the sealed net 025. But 025's
  checks C4 and D1–D3 are tautological and C3/C3b are circular, so none of them can fail:
  **`[exploratory]` until a net exists** (VI-34).
- The dispersion formula: `[refuted]` as earlier stated. A fresh context re-derived the
  corrected variance and checked it by Monte Carlo (VI-34), and caught a false strict bound in
  the first correction. Identifying the variance with the dispersion rests on
  Kostina–Verdú's general Gaussian approximation for the vector letter, whose hypotheses are
  to be checked at the source (FRONTIER G12).
- 025's check C3b is circular and samples only the all-active regime. A net with inactive
  modes is owed.
- The scalar constant $\tfrac12\log^2e$ is Kostina–Verdú's. Checking it at the source is
  owed (FRONTIER G12).

**Verification incident (VI-7).** A draft claimed the finite-$n$ equivalence was "exact at
every $n$ because the tilt is a bijection", with "effective dimension $= r$". The
fresh-context pass found that the equivalence rests on a **covering** argument. Its
replacement, "effective dimension $r_D$", was itself wrong for the dispersion (NEG-18).

## Custody summary (corrected 2026-11-20)

| Thm | Statement grade | Harness (C3) | Prereg | Incidents | Class |
|---|---|---|---|---|---|
| B1 | proof + R-IND-5 | none for `thm:coding` | 022 blk | VI-3 | `[exploratory]` (pending net + custody) |
| B2 | — (registered prediction GO-6) | GO-6 (rates not exactly matched) | 028 | VI-32, VI-34 | `[demonstrated]`, disputed; re-run owed |
| B3 | PLAUSIBLE-w/-cond. (high-res.) | GO-6 | 028 | VI-3, VI-34 | `[demonstrated]`, disputed; re-run owed |
| B4 | proof + R-IND-5 | 022 (weak: misses VI-4's bug) | 022 | VI-4, VI-32 | `[predicted]`-grade |
| B5 | proof (converse, $k=2$) + R-IND-5 | `verify_rate_region` [3] (the corner only) | 023 | VI-5, VI-32, VI-34 | corner `[predicted]`-grade; region converse `[exploratory]`; $k\ge3$ achievability owed |
| B6 | proof + R-IND-5 + measured floor | 024 + 027 | 024/026/027 | VI-6, NEG-13 | `[predicted]`-grade; floor `[demonstrated]` |
| B7 | reduction: proof + R-IND-5 | 025 (no check can fail) | 025 | VI-7, **NEG-18**, VI-34 | reduction `[exploratory]`; old constant `[refuted]` |

No row is `[proved]`; none has a custody table yet.

The appendix used to end on "the discipline caught the errors, and the record shows
where". That stays true, with a correction. The first round of passes caught four errors in
seven derivations. A second round, three months later, found that one of the fixes (VI-7's)
was itself an error, and that one net (VI-4's) could not detect the bug it was built
around. The discipline works only if the fixes are checked too.
