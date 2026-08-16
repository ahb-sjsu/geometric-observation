# OT-14 instrument appendix v2 — sealed before the v2 run

**STATUS: SEALED 2026-08-16. First instrument revision (one remains
in the budget; no final-revision clause, per `OT-CRUCIBLE-3.md`).
The v1 run is recorded FAIL-as-executed
(`results/OT14-staleness-dial.json`, kept); diagnosis in
`OT14-NOTES.md`: the fresh codecs were fitted to sampled-mixture
operators (25 German draws estimating a 768² operator at τ = 0.25),
departing from the family's qualified lever configuration and taking
caveat (i) in its weaker form. Runner: `ot14_check_v2.py`. Result:
`results/OT14-staleness-dial-v2.json`.**

One instrument change; the claim, the dial measurement, the eval
protocol, the severing declaration, all manipulation checks, and
bars B1–B2 are **unchanged from the v1 appendix**.

1. **Codec-fitting operators are the exact pool blends** — the
   strongest reading of the family's own caveat (i): the population
   mixture operator is (1−τ)·P_cs + τ·P_de exactly, with P_cs and
   P_de computed from the full fixed pools (100 and 500 rows; no
   sampling, no replacement, no noise). Stale codec =
   `quantize_against(index, P_cs, 1 bit)`; fresh codec at stratum τ
   = `quantize_against(index, (1−τ)·P_cs + τ·P_de, 1 bit)`. v1's
   sampled 100-query mixture operators put waterfiller bit
   allocation at the mercy of component sampling noise; the blend
   removes that confound entirely, so a recurrence of v1's
   intermediate-stratum inversion would be a clean adverse finding
   against the refresh claim, not an instrument artifact.

Everything else binds as sealed in `PREREG-OT14-APPENDIX.md`: the
dial from sampled strata with MC1's monotonicity/range/interior
requirements (noting, per the family record, that the sampling floor
is zero by construction under the full-pool reference, so the
above-floor clause is vacuous and the dial's content is its
monotonicity, range, and interior); MC2 lever resolvability ≥ 3× at
τ = 1; MC3 proper-subsample noise with the no-replacement guard;
B1 Spearman(excess, drift) ≥ 0.8 over the 7 nonzero strata;
B2 excess(1) ≥ 0.5 × stale(1); severing declared
trivial-by-construction in advance. SEED 20260817 unchanged.
