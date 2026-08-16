# OT-14 notes — the v1 instrument death, diagnosed from its own record

**2026-08-16. v1 verdict: FAIL as executed
(`results/OT14-staleness-dial.json`, kept).**

## What the record shows

The dial did everything the family promised: Spearman 1.000, range
17.4×, 5 interior strata. And the theory-side parent quantity behaved:
**stale-codec damage grows monotonically with measured drift**
(0.0097 → 0.402 across τ = 0.01 → 1). The bars died on the *fresh*
arm: excess = stale − fresh was **negative at every intermediate
stratum** (refresh made things worse until τ = 1), so B1's ordering
bar failed at Spearman −0.179; and removal at τ = 1 was 36% against
the 50% bar — versus the family record's 80%.

## The diagnosed defect: caveat (i) under-implemented

The appendix fitted every fresh codec to the operator of a *sampled*
100-query mixture. At τ = 0.25 that estimates the German component of
a 768² operator from 25 draws; the waterfiller then allocates 1
bit/dim against sampling noise. The family's qualified lever used a
400-draw German operator (`FAMILIES-CRUCIBLE-3.md`, v3 trail); the
appendix's uniform N_DIAL = 100 departed from the qualified
configuration, and caveat (i) — *analytic operators* — was available
in a stronger form the appendix didn't take: the population mixture
operator is exactly the pool blend (1−τ)·P_cs + τ·P_de, computable
with zero sampling noise from the full fixed pools. A related
degeneracy is recorded for completeness: under the full-pool τ = 0
reference the dial's sampling floor is zero by construction (as it
already was in the family record), so the above-floor clause of MC1
is vacuous; the dial's non-vacuous content is its monotonicity,
range, and interior, all of which held.

## What v2 changes (instrument spec only; claim, bars, dial, eval untouched)

Per `PREREG-OT14-APPENDIX-V2.md`: codec-fitting operators become the
exact pool blends — stale = quantize_against(index, P_cs);
fresh(τ) = quantize_against(index, (1−τ)·P_cs + τ·P_de) with P_cs,
P_de from the full 100/500-row pools. The dial measurement (sampled
strata, as the family qualified it), the eval protocol (80-query
proper subsamples), B1, B2, the severing declaration, and all MCs
bind unchanged. **The substantive risk this leaves is real and is
the point:** if mixture-fitted codecs genuinely underperform the
stale codec at intermediate mixing (bit dilution), v2 fails B1 on
clean instruments, and P4's revision carries that adverse finding.
One revision remains in the budget after this.
