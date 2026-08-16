# OT-14 instrument appendix — P4's feedback-free staleness on the F2 dial

**STATUS: SEALED 2026-08-16. Drafted unsealed 2026-08-15 at
`afdae4d`; sealed the following working session per the rate-limit
rule, with no edits to bars, constants, or claim between draft and
seal. Runner: `ot14_check.py`. Result: `results/OT14-staleness-dial.json`.**

## Claim under test

P4 v0.2 (readscope `PRINCIPLES.md`), the owed prediction:
**feedback-free staleness** — streaming-retrieval damage grows with
measured drift of the query-side operator and is removed by refreshing
the codec at the measured cadence; and the severing control passes
trivially, *predicted in advance*, per the dominance obligation the
v0.2 revision added after OT-4.

**The severing declaration (made now, graded by construction):** this
family has no feedback channel — retrieval outputs never enter the
query stream, and no state is carried between evaluation queries.
The feedback-severed control is therefore the experiment itself, and
P4 predicts *in advance* that severing changes nothing because there
is nothing to sever. This is the trivial pass the owed prediction
names; the runner asserts statelessness structurally and records the
declaration. OT-4's failure mode (assuming the discriminator after
the fact) is thereby avoided by the only means P4 now permits.

## Family (cited in its QUALIFIED configuration only)

F2 v3 per `FAMILIES-CRUCIBLE-3.md` ("F2 redesign trail") and
`results/FAM2-shakedown-v3.json` (dial Spearman 1.000, range 16.9×,
5 interior strata; lever +72.5×/+37.0× noise at 1 bit/dim). The three
binding caveats are inherited verbatim:

- **(i)** operators are **analytic** (the dot consumer's gradient is
  the query, so P(τ) = mean qq^T is exact) and this appendix declares
  the analytic operator as its instrument — no blind-probe cells at
  a budget the noise floor is known to bury (24 cells ≈ 0.5 relative
  Frobenius on a 768² operator).
- **(ii)** the τ = 0 reference is the **full fixed cs pool** (100
  queries, drawn whole, permutation-invariant); no bootstrap
  reference (the N_Q = 400 arm is invalid by the family record).
- **(iii)** eval-noise estimates use **proper subsamples** —
  80-of-pool draws without replacement; a zero noise estimate VOIDs
  the run (two degenerate zeros are on record in the family's own
  history).

Substrate: the OT-6 embedding books (`ot6_data/`), index = first 100
rows of each of the 6 books (600 × 768); cs pool = the held-out 100
Czech rows; de pool = the held-out 500 German rows. Strata
τ ∈ {0, 0.01, 0.03, 0.06, 0.125, 0.25, 0.5, 1.0}; stratum τ draws
(1−τ)·N from the cs pool and τ·N from the de pool.

## Instrument

- **Dial:** drift(τ) = ‖P(τ) − P(0)‖_F / ‖P(0)‖_F with P from 100
  queries per stratum; sampling floor = median drift of 5 fresh τ = 0
  redraws against the reference.
- **Lever:** stale codec = `quantize_against(index, P(0), 1 bit/dim)`
  (from `ot11_check.py`); fresh codec at stratum τ =
  `quantize_against(index, P(τ), 1 bit/dim)` — refresh at the
  stratum cadence. Damage = top-10 overlap damage of the quantized
  index against the fp index, per stratum, over 10 eval resamples of
  80 stratum-mixture queries each (without replacement from both
  pools; guard enforced). Excess(τ) = mean(stale − fresh), paired per
  resample; noise(τ) = std of the paired differences.
- Constants: SEED 20260817, D 768, BITS 1.0, N_DIAL 100, N_EVAL 80,
  N_RESAMPLE 10, FLOOR_REDRAWS 5.

## Manipulation checks (any failure → VOID)

- **MC1 (dial interior, the family's own requirements):**
  Spearman(drift, τ) ≥ 0.9 over nonzero strata; ≥ 5 strata above 2×
  the sampling floor; range ≥ 3× among above-floor strata; ≥ 3
  interior strata (between 10% and 90% of max drift).
- **MC2 (lever resolvability):** excess(τ=1) ≥ 3 × noise(τ=1).
- **MC3 (noise honesty):** every eval draw without replacement; no
  noise estimate exactly zero.

## Bars

- **B1 (damage tracks drift):** Spearman(excess(τ), drift(τ)) ≥ 0.8
  across the 7 nonzero strata.
- **B2 (removal at cadence):** at τ = 1, refreshing removes at least
  half the stale damage — excess(1) ≥ 0.5 × stale(1). (The family
  record shows 80% removed; the bar asks for half.)

**PASS = B1 ∧ B2** (given no VOID), with the severing declaration
recorded. Any bar failing → FAIL as executed.

## Recorded ungraded (no evidential weight, by prior declaration)

The full excess(τ) and fresh(τ) curves — the finer cadence question
(the drift level at which excess first clears 3× noise) is recorded
descriptively, not barred; and stale/fresh top-1 damages alongside
the graded top-10.
