# Custody: PAPER-III.a

## Claim

Two Gaussian results of Paper III (`paper/observation-theory.tex`), each an analytic statement
about a max-det program:
- **The capped max-det closed form** (`lem:maxdet`, its closed-form clause).
  - **The program.** For any cap $C\succ0$, $P\succeq0$ and $0<D<\operatorname{tr}(PC)$, the
    program $\max\{\log\det\Sigma: 0\preceq\Sigma\preceq C,\ \operatorname{tr}(P\Sigma)\le D\}$
    has a unique maximizer.
  - **The maximizer.**
    $\Sigma^\star(P,D;C)=C^{1/2}V\,\mathrm{diag}(\min(1,\theta/\tilde p_k))V^\top C^{1/2}$,
    where $C^{1/2}PC^{1/2}=V\,\mathrm{diag}(\tilde p_k)V^\top$ and
    $\sum_k\min(\tilde p_k,\theta)=D$.
  - **Two cases of interest.** With $C=\Sigma_x$ this is $\Sigma^\star(P,D)$, the formula of the
    region's consequence (ii). With $C=\Sigma_1^\star$ it is $\Sigma^\circ$.
- **The rate-loss corner step** (`thm:multiobs-loss`). On the two-stage region's single-letter
  set, the pairs with the least first-stage rate have $\Sigma_b=\Sigma_1^\star$. Among them the
  least total rate is $\tfrac12\log\det\Sigma_x-\tfrac12\log\det\Sigma^\circ$. Moreover
  $L=\tfrac12\log(\det\Sigma_2^\star/\det\Sigma^\circ)\ge0$, with $L=0$ iff
  $\Sigma_2^\star\preceq\Sigma_1^\star$.

Not claimed in this row:
- **Attainment of the rate-loss bound, and the region's equality** (`thm:region`). Both are
  stated under Assumption SR.
- **The code-level reading of the corner step.** It rests on `thm:region`'s converse, which is
  proved but has no net that can fail (VI-32).
- **`lem:maxdet`'s rate identity**
  $R_P(D)=\tfrac12\log\det\Sigma_x-\tfrac12\log\det\Sigma^\star$, which no net here covers.
- **The dispersion formula.** It rests on that rate identity, and is row PAPER-III.b.

## Proof

In `paper/observation-theory.tex`:
- **The closed form.** The closed-form clause of `lem:maxdet` and the "Closed form" paragraph of
  its proof were added on 2026-11-21, after VI-46 found the formula asserted but never derived.
  The derivation whitens by the cap, applies Hadamard's inequality in the eigenbasis of
  $C^{1/2}PC^{1/2}$, and solves the scalar program by its KKT conditions. Uniqueness is the
  lemma's strict-concavity argument, which holds for any cap $C\succ0$.
- **The corner step.** In the proof of `thm:multiobs-loss`. Its "only if" direction (L = 0
  forces nesting, by uniqueness) was written out on the same day, also after VI-46.

## R-IND-5

- **VI-4:** the max-det closed form, in the harness. It caught the bug that assumed the cap never
  binds.
- **VI-32:** a custody pass on B4 (the region, refinability and rate loss).
- **VI-37 and VI-38:** derivation-grade readings of the rate-loss text.
- **VI-39:** read 287f349, the last change to `thm:multiobs-loss` before 2026-11-21 (its title).
  `lem:maxdet` had not changed since ab63c7c (2026-07-17).
- **VI-45:** net version 4, its run and its CI wiring, with 0 errors.
- **VI-46:** found the derivation gap that the text added on 2026-11-21 closes.
- **VI-47:** the first fresh-context reading of that derivation and of the "only if" half, with
  0 errors. It re-derived both by hand and checked the closed form numerically on 2,342 random
  instances (worst dual gap 4.6e-12).

**Timing.** The draft of this row was marked `[proved]` before VI-47 had read the new
derivation. Nothing was committed until after VI-47.

**What the author agreed to.** On 2026-11-21 the author agreed that Paper III's netted results
get a ledger row of their own ("yes, I accept. Proceed as you recommend"). At that point they
included the dispersion formula. The split into this row and PAPER-III.b came after VI-46 and
was not put to the author. The class follows T-CUST-1.

## C3 harness

| Harness | Tier | CI section |
|---|---|---|
| `experiments/verify_paper3_nets.py` | re-run | `ci/reproduce.py` [2/3]: the re-run tier must reproduce the `verdict` dict and `PAPER3NETS_supported` of `results/PAPER3-nets.json` |

**How the net was run:**
- **Version 4** was committed (57bccec) before its first run. The values below are from
  attempt 2 at seed 20261127; attempt 1 crashed on an environment fault
  (`results/PAPER3-nets-RUNS.md`).
- **On GitHub:** in GitHub Actions run 44928434935 (commit 1e8c5fb), job 136919564164
  (shard 1/3) re-ran it in 13.8 s and reproduced the verdict and `PAPER3NETS_supported=True`.
- **Its own fire test is check m7.** For this row, m7 confirms that VI-4's bug, a wrong water
  level and "always refinable" all fail.

## Constants and slack

| Constant | Defined at | Proved bound | Measured | Source | Slack |
|---|---|---|---|---|---|
| m1, logdet of the closed form against a conic solver, 150 instances with random positive definite caps | `lem:maxdet` | equal | `3.6e-7` | `results/PAPER3-nets.json#maxdet.worst_logdet_vs_solver` | bar 1e-5 |
| m1, the matrix against the solver (Frobenius, relative to the cap) | `lem:maxdet` | equal | `5.2e-5` | `results/PAPER3-nets.json#maxdet.worst_matrix_vs_solver` | bar 1e-3 |
| m1, trace at the budget (relative residual) | `lem:maxdet` | tr(PΣ⋆) = D | `2.8e-15` | `results/PAPER3-nets.json#maxdet.worst_trace_residual_rel` | an identity of the closed form, which can fail only on a bug (VI-45 #1) |
| m2, two-sided duality gap of the closed form | `lem:maxdet` | 0 | `6.6e-14` | `results/PAPER3-nets.json#maxdet.worst_abs_dual_gap` | bar 1e-8; a weak-duality certificate, independent of the solver |
| m7, a wrong level of 1.2θ fails m2 | m7 | all fail | `150 of 150` | `results/PAPER3-nets-RUNS.md` | bar 90% |
| m7, VI-4's bug beaten by the solver | m7 | must be beaten | `101` | `results/PAPER3-nets.json#maxdet.vi4_bug_beaten_by_solver` | bar 10, of 150 |
| m3, Σ° (cap Σ₁⋆) against a direct solve of its program | `lem:maxdet`, `thm:multiobs-loss` | equal | `7.5e-8` | `results/PAPER3-nets.json#corner.worst_corner_logdet_vs_solver` | bar 1e-5, on the 70 pairs whose cap binds |
| m3, L = 0 iff nesting, on all 82 pairs | `thm:multiobs-loss` | iff | `True` | `results/PAPER3-nets.json#corner.iff_ok` | |
| m4, worst intercept of the corner gap against the region's joint program | `thm:multiobs-loss` | 0 | `3.6e-6 nats` | `results/PAPER3-nets-RUNS.md` | bar 1e-5 absolute. The intercept is fit bias, so the resolution is asymmetric: about 6.4e-6 nats for a corner too high, 1.36e-5 for one too low (VI-45 #2) |
| m4, informative pairs | m4 | at least 20 | `28` | `results/PAPER3-nets.json#corner.m4_informative_pairs` | on nested pairs the gap is 0 by construction |
| m4, joint solves returned "optimal_inaccurate" | m4 | at most 5% | `12` | `results/PAPER3-nets.json#corner.joint_solves_optimal_inaccurate` | of 574 solves; one solver failure would fail m4 (VI-45 #4) |
| m7, "always refinable" refuted | m7 | must be refuted | `40` | `results/PAPER3-nets.json#corner.always_refinable_refuted` | bar 10 |

## Known gaps

- **Assumption SR.** Attaining the rate-loss bound, and the region's equality, rest on
  successive-refinement achievability for this continuous source. That is attributed to Effros
  1999, whose hypotheses have not been checked at the source.
- **Not netted:**
  - `thm:region`'s converse (VI-32), so the corner step is claimed on the region's single-letter
    set only;
  - `lem:maxdet`'s rate identity.
- **What m1 to m3 cover.** m1 and m2 draw 150 random positive definite caps (the lemma's
  $\Sigma_x$ is any such matrix, so these are generic caps). m3 tests the caps $\Sigma_1^\star$ of
  the 70 pairs whose cap binds.
- **A stale docstring.** The harness's docstring says `lem:maxdet` states only the program and
  its uniqueness. That was true when it was written; since 2026-11-21 the lemma also states the
  closed form. The harness is hash-bound and is left as it ran; version 5 fixes the docstring.
- **Points VI-45 recorded about version 4:**
  - m1's trace clause cannot fail except on a bug;
  - m4's resolution is asymmetric;
  - m4's two solver-status clauses make the CI verdict sensitive to one solver failure, and
    Clarabel is not pinned (0.11.1 on Atlas);
  - the JSON records no commit, start time, Clarabel version or thread count.

  A version 5 is owed (`results/PAPER3-nets-RUNS.md`).
- **The public versions are stale.** The Zenodo preprint and the author's IEEE package lack
  the closed-form derivation, and still carry the old dispersion constant and attribution.
  They are the author's to update.
