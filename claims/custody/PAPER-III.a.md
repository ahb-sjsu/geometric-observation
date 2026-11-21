# Custody: PAPER-III.a

## Claim

Three Gaussian results of Paper III (`paper/observation-theory.tex`):
- **The rate identity** (`lem:maxdet`, its first clause). For $X\sim\mathcal N(0,\Sigma_x)$,
  $\Sigma_x\succ0$, $P\succeq0$ and $D>0$, the single-letter rate–distortion function under
  $d(x,\hat x)=(x-\hat x)^\top P(x-\hat x)$ is
  $R_P(D)=\tfrac12\log\det\Sigma_x-\tfrac12\log\det\Sigma^\star(P,D)$. Both halves are claimed:
  every test channel has $I(X;\hat X)\ge R_P(\mathbb E\,d)$, and the Gaussian backward channel
  attains it.
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
- **The variance formula of `cor:dispersion`.** It rests on the rate identity and is row
  PAPER-III.b.
- **The operational coding theorem** (`thm:coding`). The rate identity here is the single-letter
  function.

## Proof

In `paper/observation-theory.tex`:
- **The rate identity.** The proof of `lem:maxdet`:
  - the converse is `lem:cm` (the conditional mean serves every observer) then `lem:info`
    (conditioning and Gaussian maximum entropy), followed by the max-det program;
  - achievability is the Gaussian backward channel.

  Unchanged since ab63c7c (2026-07-17).
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
- **VI-32:** a custody pass on B4 (the region, refinability and rate loss). It checked `lem:cm`,
  `lem:info` and `lem:maxdet` and found them correct (`claims/audits/VI-32-PaperIII-B.md`).
- **VI-37 and VI-38:** derivation-grade readings of the rate-loss text.
- **VI-39:** read 287f349, the last change to `thm:multiobs-loss` before 2026-11-21 (its title).
  `lem:maxdet` had not changed since ab63c7c (2026-07-17).
- **VI-45:** net version 4, its run and its CI wiring, with 0 errors.
- **VI-46:** found the derivation gap that the text added on 2026-11-21 closes.
- **VI-47:** the first fresh-context reading of that derivation and of the "only if" half, with
  0 errors. It re-derived both by hand and checked the closed form numerically on 2,342 random
  instances (worst dual gap 4.6e-12).
- **VI-48:** re-derived the rate identity's proof line by line, including singular P (the
  converse through `lem:cm` and `lem:info`, achievability, and the KKT step). It also reviewed
  the rate-identity net, its version history and its CI file mode.
- **VI-49:** a confirming pass on VI-48's dispositions, with 0 errors. It re-ran the net and
  checked the achievability checks against a lowered formula.

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
| `experiments/verify_paper3_rate_identity.py` | re-run | `ci/reproduce.py` [2/3], in file mode: CI moves the committed `results/PAPER3-rate-identity.json` aside, reruns the harness, and compares the `verdict` and `PAPER3RATE_supported` of the fresh JSON |

The rate identity's net, version 2, was committed (69c4359) before its first run, on seed
20261129. Version 1 failed one r3 clause, a wrong expectation about the check; it is kept as
`results/PAPER3-rate-identity-v1.json`. The run account is `results/PAPER3-rate-identity-RUNS.md`.

It tests three channel families:
- non-Gaussian product quantizers;
- skew-rectangle quantizers, on which `lem:info` is a strict two-dimensional inequality;
- random and near-optimal Gaussian channels.

Information and distortion are computed from the joint law in every case. VI-48 found that its
five power gates are passed by the formula's own optimum channel, and showed its power with its
own mutants instead (Known gaps).

**How the net was run:**
- **Version 4** was committed (57bccec) before its first run. The values below are from
  attempt 2 at seed 20261127; attempt 1 crashed on an environment fault
  (`results/PAPER3-nets-RUNS.md`).
- **On GitHub:** in GitHub Actions run 44928434935 (commit 1e8c5fb), job 136919564164
  (shard 1/3) re-ran it in 13.8 s and reproduced the verdict and `PAPER3NETS_supported=True`.
- **The rate-identity net on GitHub:** in GitHub Actions run 44955486964 (commit 235ba32), job
  137002514952 (shard 2/3) re-ran it in file mode in 9.7 s, and reproduced the verdict and
  `PAPER3RATE_supported=True`.
- **Its own fire test is check m7.** For this row, m7 confirms that VI-4's bug, a wrong water
  level and "always refinable" all fail.

## Constants and slack

| Constant | Defined at | Proved bound | Measured | Source | Slack |
|---|---|---|---|---|---|
| rate identity: smallest gap I − R_P(E d), skew quantizers (independent of the formula) | `lem:maxdet` | ≥ 0 | `0.0435` | `results/PAPER3-rate-identity.json#converse.min_gap.skew` | bar −1e-7 |
| rate identity: smallest gap, random Gaussian channels (independent of the formula) | `lem:maxdet` | ≥ 0 | `1.4e-7` | `results/PAPER3-rate-identity.json#converse.min_gap.gauss_random` | one instance aligned by chance; the per-instance median of the best formula-independent gap is 0.31 nats (VI-48) |
| rate identity: smallest near-optimal Gaussian gap at eps = 1e-3 | `lem:maxdet` | ≥ 0 | `6.1e-8` | `results/PAPER3-rate-identity.json#attained.near_optimum_min_gap.eps3` | not evidence on its own: these channels perturb the formula's own Λ⋆. They are a one-sided first-order descent test of its optimality, and VI-48's self-consistent wrong formulas were caught by them down to a median excess of 1.4e-7 nats |
| rate identity: smallest `lem:info` slack, skew quantizers | `lem:info` | ≥ 0 | `0.0164` | `results/PAPER3-rate-identity.json#lemma_info.min_slack.skew` | absolute; informative product quantizers reach 0.0050. Relative to I the smallest slack is 0.207 (skew) and 0.101 (product), so a `lem:info` strengthened by a factor of about 1.26 or 1.11 would pass (VI-48) |
| rate identity: `lem:info` raised by 0.05, skew quantizers catching it | r5(b) | recorded only | `4` | `results/PAPER3-rate-identity.json#power.b_lemma_info_raised_counts.skew.s_5e-2` | the r5(b) gate counts product channels, trivial ones included; 18 informative product catches were confirmed after the run |
| rate identity: the optimum attains the formula | `lem:maxdet` | 0 | `4.4e-15` | `results/PAPER3-rate-identity.json#attained.worst_abs_gap_at_optimum` | passes trivially for the correct closed form (VI-48 #5), but fails on a self-consistent formula that is too low: a water level raised by 0.1% failed it at 1.5e-3 (VI-49). It guards the formula's lower side; achievability itself rests on the proof |
| rate identity: the backward channel's feasibility, min eig(Σx − Σ⋆)/‖Σx‖ | `lem:maxdet` | ≥ 0 | `-2.5e-15` | `results/PAPER3-rate-identity.json#backward.worst_min_eig_rel` | holds by the closed form (w ≤ 1). The trace residual, by contrast, failed at 1e-3 on VI-49's lowered formula; the Monte Carlo adds nothing (VI-48 #5) |
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
- **Not netted:** `thm:region`'s converse (VI-32), so the corner step is claimed on the region's
  single-letter set only.
- **The rate identity's net: what it shows and what it does not** (VI-48):
  - **Its power gates show nothing.** The formula's own optimum channel passes all five r5
    gates, and (a) and (e) cannot fail at all. Its power was shown after the fact, by VI-48's
    self-consistent wrong formulas (VI-4's Σ, and water-filling in a basis rotated by as little
    as 0.001 rad). All of them failed r2 and r3, through the near-optimal and random Gaussian
    channels. The power is thin per instance: VI-49's rotation by 0.001 (median excess 3.4e-7
    nats) was caught on only 2 of 120 instances, though that still fails the verdict.
  - **The `lem:info` test is weak in relative terms.** The maximum-entropy step is tested only by
    non-Gaussian channels, which carry little information (H ≤ 0.13 nats at the catches). A
    `lem:info` strengthened by a factor of about 1.11 (product) or 1.26 (two-dimensional) would
    pass. Near the optimum the converse is tested by Gaussian channels only.
  - **The achievability checks guard one side only.** r3's optimum check and r4's trace check
    pass trivially for the correct closed form, but fail on a self-consistent formula that is too
    low (VI-49). r4's feasibility check holds by the closed form, and its Monte Carlo adds
    nothing. Achievability itself rests on the proof.
  - **Owed in a version 3:**
    - self-consistent mutant gates, including a lowered formula, with catches reported per
      family and the formula's own channels excluded;
    - r5(b) counting only channels with H > 0;
    - r3's first-order prediction as a clause (VI-48 confirmed it to 0.998–1.003);
    - a lowered-formula gate on the achievability checks (VI-49);
    - catch counts per instance.
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
