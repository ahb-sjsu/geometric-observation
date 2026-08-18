# Observation Theory v1.0 — the owed-prediction ledger

**A sealed revision act, 2026-08-18, under the freeze rules of
`DECLARATION-V1.md` (sealed `7a10867`): *“New owed predictions may be
minted after v1.0 by a sealed revision act; they open a v1-line
exposure ledger without touching the frozen statements. A theory with
zero exposure owes its next risk; v1.0 does not discharge that debt,
it dates it.”* This is that ledger. It edits none of the frozen v1.0
statements (the declaration is immutable); it declares what the
theory now risks. The no-sixth-principle rule holds — these five
extend the five, they do not add a sixth.**

## The through-line of the v1 line

Every v0.2 owed prediction was discharged **descriptively**: the law
was measured to hold. The v1-line raises the bar to **derivability** —
each law must be *predicted a priori*, from the operator spectrum and
the design, before the measurement is taken — with one genuinely new
claim (P1's cross-consumer transfer). A descriptive law that cannot
be predicted in advance is weaker than one that can; closing that gap
is the theory's next exposure. Each prediction below names its first
substrate and its **kill condition** — the outcome that returns its
principle to revision and forces the v2.0 process.

## The five owed predictions

### OP1 — cross-consumer codec transfer *(P1, new claim)*

Composition (OT-8) predicted an *ensemble's* preference from component
traces. The new risk: a codec optimized against consumer A's read
operator `P_A` damages a **different** consumer B by an amount
predicted by the operator overlap `tr(P_A P_B)` alone — no probe of B
under A's codec. Consumer relativity, if it means what it says,
composes *across* consumers, not only within an ensemble.
- **First substrate:** two real attention heads with blind-probed
  operators; predict cross-damage from the trace overlap, grade
  against measured damage.
- **Kill:** if cross-damage is not predictable from the overlap
  (rank correlation < 0.6 against the trace prediction), consumer
  relativity does not transfer across consumers and P1's reach is
  narrower than the statement claims.

### OP2 — the transfer residual, modeled *(P2, closes the L21_H3 cell)*

OT-15 left the transfer residual *measured but unmodeled* (the one
head where even full-sample Gaussian moments sit at 1.0). The new
risk: the moment-matched transfer error is **derivable** from a
measured non-Gaussianity functional of the real activation measure
(operator-weighted excess kurtosis), so the transfer carries an
*a-priori* error bound rather than an empirical one.
- **First substrate:** the 12 Llama-3.2-3B heads; correlate transfer
  error against the kurtosis functional.
- **Kill:** if error does not track the functional (rank correlation
  < 0.6), the residual is structural noise, not modelable, and P2's
  transfer claim stays empirical-only.

### OP3 — the sample-complexity exponent *(P3, C-15's asymptote)*

C-15 measured that the cliff survives equal budget within 8×. The new
risk: the sub-dimensional excess error decays as a **derivable power**
of the budget multiplier `m` — `error ∝ m^(−α)` with `α` predicted
from the spectrum gap — **or** it provably plateaus (`α = 0`). One of
the two must hold and be predicted; a messy, underivable decay is the
kill.
- **First substrate:** the C-15 planted family swept to `m ∈ [1,
  1000]`.
- **Kill:** a decay exponent neither derivable from the gap nor zero
  leaves the noisy-cliff / budget story incomplete.
- *(Carried-forward open theorem cells, not owed predictions: the
  adaptive `k = d−1` cell and the noisy-adaptive quantifier order.
  These are theorem gaps, recorded open in `OT3-THEOREM.md` /
  `OT3-NOISY-THEOREM.md`, and are closed by proof, not measurement.)*

### OP4 — the refresh floor, derived *(P4, closes the recorded edge)*

OT-14's recorded edge: refreshing below drift ≈ 0.1 costs rather than
pays. The new risk: the drift floor `d*` below which refresh hurts is
**derivable** from the operator spectrum and the codec bit budget —
`d*(spectrum, bits)` predicted a priori, matched to measurement.
- **First substrate:** the OT-6 embedding drift dial at several bit
  budgets.
- **Kill:** if the measured floor departs from the derived `d*` by
  more than 2×, the floor is an artifact of the substrate, not a law,
  and P4's cadence claim keeps its empirical caveat.

### OP5 — the floor location, derived *(P5, closes the floor law)*

OT-18 measured the two floor curves and where the informative
fraction collapses. The new risk: the response-floor **location** is
derivable from the consumer's output quantization `g` and the codec
spectrum — predicted a priori, not merely observed after the sweep.
- **First substrate:** the multi-seed-qualified F1′ family at several
  quantization levels.
- **Kill:** if the collapse location does not match the derived
  prediction (outside the family's own interior band), the floor law
  is descriptive only, and P5's revision keeps its scope caveat.

## Cadence and the frontier

Each owed prediction is tested under the full sealed discipline — a
family shaken down and qualified first (across seeds, per the OT-17
lesson), bars sealed before runs with the structural cooling-off, and
manipulation checks graded against the family record at enforcement
granularity (the OT-13 lesson). Bars are **not** minted here; they
are sealed per-test, later, each in its own appendix. This ledger is
live until every line is discharged or refutes; a refutation triggers
the v2.0 revision process on that principle alone.

**The frontier, noted but not minted (it would need its own act):**
the theory has been measured on attention heads, state-space
channels, embedding retrieval, and — cross-program — BGP/RPKI. A
domain it has never touched (a diffusion denoiser's read operator, an
RL value head's) is where a genuinely surprising failure could live.
Naming it here as a direction, not an owed prediction, keeps the v1
line honest: five predictions the theory *commits* to, one frontier
it merely *acknowledges*.
