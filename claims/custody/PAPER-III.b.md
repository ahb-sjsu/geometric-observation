# Custody: PAPER-III.b

## Claim

The variance formula of Paper III's `cor:dispersion` (`paper/observation-theory.tex`). Take a
Gaussian source under a fixed read operator, with tilted mode variances $\gamma_k$, water level
$\theta$ and $0<D<\sum_k\gamma_k$. The tilted $\mathbb R^r$-valued letter $Y$, at its Gaussian
optimal output law (PAPER-III.a), has $D$-tilted information with these per-mode terms:
- an active mode contributes $\tfrac12\log(\gamma_k/\theta)+\tfrac12(y_k^2/\gamma_k-1)$;
- a mode below the water level contributes $(y_k^2-\gamma_k)/(2\theta)$.

Its variance is
$V_Y(D)=\tfrac12[r_D+\sum_{0<\gamma_k\le\theta}(\gamma_k/\theta)^2]$ nats², with
$r_D\le2V_Y\le r$, and equality on the right iff $\gamma_k\ge\theta$ for every $k$.

This row rests on PAPER-III.a's rate identity: the Gaussian backward channel attains $R(D)$, and
gives the output law that the tilted information is built on.

**Not claimed** (VI-48 #1, #2):
- **Kernel uniqueness**, that the rate–distortion-achieving kernel is unique. It is proved in the
  paper (VI-37 checked it line by line; VI-38 and VI-48 confirmed it), but no check can fail on it.
- **$V_Y$ as the dispersion of the tilted letter's own coding problem.** That is Kostina and
  Verdú's Theorem 12, checked at the source by the assistant and VI-38. A single $V$ needs kernel
  uniqueness; without it their Remark 9 makes $V$ an extremum over the optimal kernels.
- **$V_Y$ as the dispersion of the consumer coding problem.** That also needs the finite-n
  reduction `prop:dispersion`, which stays `[exploratory]`: the sealed net 025's checks cannot
  fail (Appendix B, B7).

## Proof

In `paper/observation-theory.tex`, the paragraph of `cor:dispersion` that computes the per-mode
terms and the variance of the $D$-tilted information. The definition and its defining property
are Kostina–Verdú's Def. 6 and Property 2, checked at the source. The text of `cor:dispersion`
last changed in 1c155b1.

## R-IND-5

- **VI-32:** the custody pass that found the old constant $r_D/2$ wrong (NEG-18).
- **VI-34:** re-derived the tilted-information terms and the variance, with a Monte Carlo at four
  configurations, including $\gamma_k=\theta$. It found that the first corrected bound, $2V<r$,
  was false.
- **VI-36:** re-derived the variance again.
- **VI-37 and VI-38:** VI-37 checked the uniqueness argument, which is not claimed here. VI-38
  checked Kostina–Verdú at the source.
- **VI-39 and VI-40:** confirmed the later text.
- **VI-46:** found that the row rested on the then-unnetted rate identity.
- **VI-48:** scoped the row to the variance formula, and confirmed the uniqueness chain while
  advising that it be scoped out.

## C3 harness

| Harness | Tier | CI section |
|---|---|---|
| `experiments/verify_paper3_nets.py` | re-run | `ci/reproduce.py` [2/3]; checks m5 and m6, and m7's dispersion clauses |
| `experiments/verify_paper3_rate_identity.py` | re-run | `ci/reproduce.py` [2/3], file mode; nets the rate identity this row rests on (see PAPER-III.a) |

**What the checks are:**
- **m5** compares the per-mode tilted-information terms with Kostina–Verdú's definition (Def. 6),
  computed independently. It also checks the slope λ⋆ = 1/(2θ) and Csiszár's property.
- **m6** is a Monte Carlo of the tilted information's mean and variance, on 15 configurations:
  4 with every mode active and 11 mixed.
- **m7's dispersion clauses** require the old constant $r_D/2$, the formula with the inactive
  terms dropped, and the κ family to fail.

## Constants and slack

| Constant | Defined at | Proved bound | Measured | Source | Slack |
|---|---|---|---|---|---|
| m5, per-mode tilted information against Kostina–Verdú's definition | `cor:dispersion` | equal | `8.9e-16` | `results/PAPER3-nets.json#dispersion.worst_definition_diff` | bar 1e-9 |
| m6, Monte Carlo mean and variance within 5 standard errors | `cor:dispersion` | V_Y(D) | `True` | `results/PAPER3-nets.json#dispersion.mc_ok` | 5 standard errors, on 15 configurations |
| m6, configurations with a mode below the water level | `cor:dispersion` | — | `11` | `results/PAPER3-nets.json#dispersion.mixed` | the inactive terms are what NEG-18 got wrong |
| m7, the old constant r_D/2 fails | m7 | must fail | `9/9` | `results/PAPER3-nets.json#dispersion.old_constant_fired` | |
| m7, dropping the inactive terms fails | m7 | must fail | `21/21` | `results/PAPER3-nets.json#dispersion.drop_inactive_fired` | |
| m7, the κ family passes Csiszár's property but fails the definition | m7 | must fail | `21/21` | `results/PAPER3-nets.json#dispersion.kappa_family_passes_csiszar_fails_definition` | Csiszár's property alone does not pin the terms down |

## Known gaps

- **The dispersion readings are not in this row.** See "Not claimed" above. The book's B7 and
  Chapter 7 call the formula the dispersion; that reading stays `[exploratory]`.
- **Arithmetic consequences.** The bounds $r_D\le2V_Y\le r$ and their equality case follow from
  the formula and cannot fail on their own.
- **Monte Carlo resolution.** m6 is a Monte Carlo at 5 standard errors on 15 configurations. A
  wrong constant smaller than its resolution would pass; m5 checks the per-mode terms exactly.
- **The rate identity's net has limits.** They are in PAPER-III.a.
- **The public versions are stale.** The public Zenodo preprint and the author's IEEE package
  still carry the refuted constant.
