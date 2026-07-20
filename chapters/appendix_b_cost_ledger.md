# Appendix B — The COST Ledger: Theorems, Proofs, and Falsification Harnesses

*Staging tier [B]. This appendix carries the statements and proof-status of the
COST-face theorems (Paper III). Each theorem ships, per the charter's theorem-custody
rule (T-CUST-1), four things: a written proof, an R-IND-5 fresh-context adversarial
pass, a committed C3 numerical falsification harness built to fail if the theorem is
false, and a constants/slack + known-gaps table. Full proofs live in Paper III and its
appendix; this ledger gives statements, status, custody, and the verification incidents
each one survived. Nothing here is `[proved]` without **both** grades (T-CUST-2: a green
harness is a net, not a proof).*

## Conventions

Source $x$ with covariance $\Sigma_x$; observer read metric $P$ (dropping the subscript
$C$); coding error $\delta$ with covariance $\Sigma_\delta$; read distortion
$D = \operatorname{tr}(P\Sigma_\delta)$. The **whitened** basis is $\Sigma_x^{1/2} P
\Sigma_x^{1/2}$; several constants are correct only in this basis (the recurring lesson
of VI-4/VI-6).

## Thm B1 — Consumer rate–distortion achievability & converse

**Statement.** For a Gaussian source and read metric $P$, the minimum rate to achieve
read distortion $D$ is $R_C(D)$, achieved by a test channel that does reverse water-
filling in the whitened basis; the tilt relative to Shannon's source-only allocation is
exactly $P$. The reduction in true divergence relative to reconstruction coding is the
tilt.

**Status.** `[proved]` — derivation-grade via written proof + R-IND-5 pass; conclusion-
grade via a committed Blahut–Arimoto harness reproducing the optimum. Registry 022 block
/ Paper III.

**Custody / gaps.** Verbatim Kostina–Verdú transfer holds for the fixed-$P$ Gaussian
case; the true-nonlinear consumer keeps a "should port" hedge (VI-7). Constants in the
whitened basis only.

## Thm B2 — Output ≤ surrogate ≤ reconstruction at matched rate

**Statement.** At matched rate, coding for the consumer's output metric is no worse than
coding for a surrogate read metric, which is no worse than coding for reconstruction, on
the consumer metric; the output–reconstruction gap is governed by the $\ker P$ entropy
share.

**Status.** `[demonstrated]` operationally by GO-6 (GO-P-2026-028): the ordering holds at
*every* rate, reconstruction up to ~500× worse at high rate, median gap $+2.45$ (strict,
kernel positive), isotropic control $P = I$ collapses the three coders. The analytic
statement is proved; the harness is the conclusion-grade net.

**Custody / gaps.** Nonlinear consumer $d = 8, r = 4$, $\dim\ker P = 4$; synthetic. The
gap's dependence on the kernel entropy share is the load-bearing structural claim.

## Thm B3 — The surrogate–output gap vanishes with rate

**Statement.** The relative gap $(b - a)/(c - a)$ between a surrogate-optimal and an
output-optimal code shrinks to zero as the rate grows.

**Status.** `[demonstrated]` — GO-6 measures it $0.41 \to 0.005$ as rate grows. Analytic
statement PLAUSIBLE-with-conditions on the R-IND-5 pass (VI-3), pinned by the harness.

**Consequence.** At high resolution a surrogate for $P$ suffices; at low resolution it
does not — which is why the blind probe (Chapter 10) is load-bearing precisely in the
bit-starved regime.

## Thm B4 — Two-observer region & refinability = Loewner nesting

**Statement.** The achievable rate region for two observers $(P_1, P_2)$ is
characterized; a single scalable code serves the coarse observer with a prefix of the
fine observer's bits **iff** $P_1 \preceq P_2$ (Loewner). Non-nested read metrics incur
an exact rate loss.

**Status.** `[proved]` — the two-observer max-determinant program; prereg 022.

**Verification incident (VI-4, standing).** An in-context `sigma_star` formula used
$(\Sigma^\star)^{-1} = \Sigma_x^{-1} + \lambda P$ with the inline claim "the cap never
binds"; a fresh-context adversarial pass found the max-det error covariance is reverse
water-filling in the whitened basis and the cap **does** bind on $\ker P$. Corrected;
harness re-run with a nested-Gaussian sufficiency check reproducing both single-stage
optima to $10^{-10}$; prereg amended and re-sealed; false pass logged. *The analytic
theorem statement was unaffected — the harness was wrong.* This is the textbook case for
why `[proved]` demands both grades.

## Thm B5 — Complete rate region & the $k$-observer chain

**Statement.** For $k \ge 3$ observers in a chain the tight region is Kostina–Tuncel's;
achievability is via independent Fisher increments from physically-degraded channels.

**Status.** `[proved]`, corrected. Prereg 023.

**Verification incident (VI-5).** Two errors caught pre-publication: (a) the $k \ge 3$
region is Kostina–Tuncel, not Rimoldi (which is the finite-alphabet $L$-stage carrier);
(b) the two-stage K-map **does not iterate** — an accumulating rotation ambiguity $B =
Q\Lambda^{1/2}$ leaks Fisher information by $O(0.1)$ per stage. Achievability restated via
independent increments, exact to $10^{-14}$; the $k = 2$ corner unaffected.

## Thm B6 — The price of a misidentified observer: tax and floor

**Statement (tax).** Coding for a rank-$M$ read metric when the consumer's is rank $m <
M$ costs excess rate $\sim (r/2)\log(M/m)$. **Statement (floor).** A code blind to a
direction the consumer reads hits a distortion floor $D \ge D_{\text{floor}} =
\operatorname{tr}(\tilde P\Pi)$ (whitened kernel), a compact band $[D_{\text{floor}},
\operatorname{tr}(P\Sigma_x)]$ — a floor, not unbounded distortion.

**Status.** `[proved]` (prereg 024) and, for the floor, `[demonstrated]` downstream on a
trained model (GO-P-2026-027, held-out layers {4,20}, floor 16/16, asymptotic ratio
800–5700×).

**Verification incident (VI-6).** Two corrections pre-publication: omission gives a
*floor*, not unbounded distortion; and the floor uses the *whitened* kernel
$\Sigma_x^{-1/2}\ker\hat P$ — a naive kernel projector overstates it by ~30% when
$\Sigma_x \ne I$. The 0.647 Llama overlap is written as a **conditional** certificate
(omission + equal weights), not a flat number.

**Related negative (NEG-13 → resolved).** The first sealed finite-rate gate for the floor
*missed* (0/16, shallow-sweep artifact conflating floor-reached with floor-exists);
resolved by a fresh held-out test, not by relaxing the bar (Chapters 15–16).

## Thm B7 — Dispersion counts read dimensions

**Statement.** The finite-blocklength dispersion counts the *read* dimensions: effective
dimension $r_D \le r$, equal to $r$ only as $D \to 0$.

**Status.** `[proved]`, sharpened. Prereg 025.

**Verification incident (VI-7).** A draft claimed "exact at every $n$ because the tilt is
a bijection" and "effective dimension $= r$"; the fresh-context pass found the finite-$n$
equivalence rests on a **covering** argument (not a first-order data-processing bound),
and $r_D \le r$ (not flat $r$). Dispersion constants flagged [C7] to Kostina–Verdú.

## Custody summary

| Thm | Statement grade | Harness (C3) grade | Prereg | Incident | Class |
|---|---|---|---|---|---|
| B1 | proof + R-IND-5 | Blahut–Arimoto | 022 blk | — | `[proved]` |
| B2 | proof | GO-6 | 028 | — | `[proved]`/`[demonstrated]` |
| B3 | PLAUSIBLE-w/-cond. | GO-6 | 028 | VI-3 | `[demonstrated]` |
| B4 | proof + R-IND-5 | nested-Gaussian | 022 | **VI-4** | `[proved]` |
| B5 | proof, corrected | verify_rate_region | 023 | VI-5 | `[proved]` |
| B6 | proof + measured floor | verify_observer_mismatch + 027 | 024/026/027 | VI-6, NEG-13 | `[proved]`/`[demonstrated]` |
| B7 | proof, sharpened | verify_dispersion_separation | 025 | VI-7 | `[proved]` |

Every row that says `[proved]` carries both grades and a logged fresh-context pass; every
incident was caught **before** the paper asserted the result. That is the appendix's whole
claim: not that the derivations were right the first time — four of seven were not — but
that the discipline caught the errors, and the record shows where.
