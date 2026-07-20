# Chapter 14 — The Falsifiable Core: GO-1 … GO-6 and Gate B

The sweep (Chapter 13) is the framework's breadth. This chapter is its spine: six
risk-bearing claims, GO-1 through GO-6, each a sentence the program could have been
wrong about, each with a registry entry sealed before measurement, a result, a class
tag, and a replication count. Together with the out-of-sample Gate B, they are the
minimal set of bets that, had they gone the other way, would have falsified the theory
rather than dented it. This is what "falsifiable" means in this book: not a rhetorical
posture but a list.

## How a claim earns its class

Every row carries one of six tags, and the tags are ordered by how much they demand.

- **`[predicted]`** — a sealed prediction, gate stated, confirmed prospectively or on a
  single instance.
- **`[demonstrated]`** — a sealed prediction that passed its ex-ante bar on a governed run.
- **`[replicated]`** — `[demonstrated]`, then reproduced on a second independent instance
  or representation.
- **`[proved]`** — a written proof *and* a committed falsification harness *and* a
  fresh-context adversarial re-derivation. Both grades.
- **`[exploratory]`** — a green numerical check with an unproven derivation; may not
  support an umbrella claim.
- **`[refuted]`** — a bet lost, carried at full prominence (Chapter 16).

A claim *moves* between classes by earning the next bar, and the movement is auditable in
git. The rule that makes this honest is **R-IND-6**: promoting an `[exploratory]` finding
to `[demonstrated]` requires a *fresh sealed prereg* and a run on *held-out* data — never
a replay of the set the effect was calibrated on. (Reference: GO-P-2026-027 confirmed the
omission floor on held-out layers {4,20} after it was first seen on {8,16}.) You cannot
promote a claim by looking at the same data harder.

## The six

**GO-1 — the read/nuisance split is identifiable ex ante from the consumer.**
`[predicted]` ✅. A black-box sensitivity probe recovers the read subspace at overlap
0.936 vs 0.059 chance (~16×), seeing only $C(\cdot)$; blind proj-var predicts the flip
12/12 both consumers, Spearman 1.00; recon can't (0.40) [GO-P-2026-011, blinded,
prospective, PASS 5/5]. Scope: planted low-rank subspace; the real-model consumer is the
hardening carried by the legal sequence (Chapter 10).

**GO-2 — downstream preservation is not reconstruction, but $\operatorname{tr}(P_C
\Sigma_\delta)$.** Two halves. The negative half — *not* reconstruction — is
`[demonstrated]`: a recon-identical arm (0.0934 vs 0.0938) is 2.53× worse downstream
(12/12), anti-probe 21× [GO-P-2026-002]. The positive half — the projected covariance
*controls* — is `[replicated]`: softmax attention (GO-P-2026-006, symmetric flip) and
prospective embedding retrieval at identical recon 0.0964 (GO-P-2026-009), two
representations, two consumers, one mechanism. The regime bound (needs recon-matched
arms) is NEG-10.

**GO-3 — the certificate's vacuity threshold predicts where single-stage retrieval
dies.** `[demonstrated]`. A *derived* (not fit) threshold $\rho = 1$ locates death at
$\rho_{50} = 0.948$ (6%); ordering Spearman 0.991; beats raw margin 0.873; 14 corpora,
6/6 gated [GO-P-2026-014].

**GO-4 — fixed-budget verdicts invert under budget-matched observation.**
`[replicated]`. On real Atlas book embeddings: fixed $m=10$ → angle-ρ *rises* with $N$;
budget-matched $m$ grows 10→121/126/159 → angle-ρ *collapses*; same substrate, opposite
refinement verdict, set by the observer budget, 3/3 gated across 3 seeds
[GO-P-2026-015]. This is the empirical face of budget-relativity: the observer's budget,
not the substrate, sets the verdict.

**GO-5 — an $\alpha = 1$ density quotient restores fidelity in a non-spectral domain.**
**`[refuted]`** (4 attempts). Across four prospective non-spectral domains the restoration
is $<2\%$ and not density-specific (a uniform control gains as much); the mechanism is
absent [GO-P-2026-019 → NEG-11]. The retained positive: $\alpha = 1$ is the optimal
diffusion exponent, non-spectrally. A bet placed, lost, and carried.

**GO-6 — at matched rate, output ≤ surrogate ≤ reconstruction on the consumer metric.**
`[demonstrated]`. The operational net for the COST theorems (B2/B3): the ordering holds at
every rate; reconstruction up to ~500× worse at high rate; the surrogate→output gap shrinks
0.41→0.005 as rate grows; the isotropic control $P_C = I$ collapses the three coders
[GO-P-2026-028, all pass]. This closes the last promised registration.

## Gate B: the out-of-sample discipline

The six are the spine; **Gate B** is the stress test — confirmation in domains *disjoint*
from the papers the theory was built on, so no result can be a memory of its training
data. Gate B's rows are exactly where the theory could have died in the open, and its
mixed record is the point.

- **GO-B (gradient curvature)** — `[predicted]` ✅ **hit**, PASS 5/5. The read operator
  generalizes to a *Hessian*: at identical recon the curvature-metric distortion flips
  with $H$, proj-var tracks 12/12, recon uninformative [GO-P-2026-010].
- **GO-B-Llama (frontier LLM keys)** — `[predicted]` → **MISS** → **rematch HIT**. The
  first sealed real-model test recovered the read operator (median 0.567) but *sub-bar*,
  and lacked recon-matched arms → 2 of 3 triggers missed → NEG-12, theory bounded to
  synthetic consumers *on that evidence* [GO-P-2026-020]. The corrected rematch, with
  recon-matched arms, passed 4/4 [GO-P-2026-021]. Both rows stand.
- **GO-B-DOA / LOCATA / AV16.3 / PDAR** — the physical replications of Chapter 13, each a
  Gate-B row (simulated ULA hit; LOCATA 032 miss → 033 rehab hit; AV16.3 and PDAR hits).
- **GO-B-legal / whale** — the blind-probe and cetacean confirmations of Chapter 13.
- **GO-B-blind (20 Newsgroups)** — `[predicted]` → **PARTIAL**: blind non-oracle
  *direction* confirmed, full flip and point-magnitude not (the open magnitude constant,
  Chapter 17) [GO-P-2026-041].

## Why both the hits and the misses are load-bearing

A reader could ask why the misses — NEG-12, LOCATA-032, D1, D4 — are printed beside the
hits at all. Because a falsifiable core is defined by what would have refuted it, and a
program that reports only its confirmations has, in effect, no core. The Llama miss
bounded the theory (and was later cleared by a *corrected* design, not a relaxed bar); the
LOCATA miss caught a GT-leakage artifact and forced the rehab; D1 says "data-limited" out
loud; D4 is a true boundary the $\kappa$ law now predicts. Each miss either bounded the
claim or improved the instrument, and none was quietly dropped. That is the difference
between a falsifiable core and a highlight reel — and it is why the next part, on the
discipline that produces this behavior, is a part and not an appendix.
