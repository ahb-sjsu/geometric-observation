# OT-7 instrument appendix v3 — sealed before the v3 run

**Supersedes v2 after its as-executed FAIL (d32_r4: energy_rank GL flip
share 0.32 vs bar 0.50; every other row 1.00). One change; claims
untouched; committed before `ot7_check_v3.py` executes.**

**The change — quantized-derived quantities.** `energy_rank` is an
integer quantization of the spectrum. Its GL flip *share* is a function
of the transform-ensemble strength (0.94 under cond ≤ 1e4 in v1, 0.32
under cond ≤ 1e2 in v2, same seed): a fact about the dial, not about
the taxonomy. v3 therefore grades quantized-derived quantities as
follows:

- **O(d) half (graded):** the integer must be *exactly* invariant under
  every orthogonal transform (deviation 0).
- **GL half (inherited):** fragility is carried by the parent
  continuous row (spectrum, bar unchanged at 0.95/1e-6); the integer's
  own flip share is *reported descriptively*, not graded.

Rationale: the taxonomy row "energy rank: GL-fragile, O-invariant"
means the quantity offers no GL-stable information beyond the spectrum
it quantizes — which is exactly what parent-fragility plus exact-O
invariance establishes. A bar on the flip share itself would be a bar
on the ensemble dial.

All other constants identical to v2. Result:
`results/OT7-invariance-v3.json`. Verdict rule: all graded rows pass in
all cells, else FAIL. This is the third seal; a v3 FAIL closes OT-7 as
FAIL for the campaign — no fourth instrument revision inside the
Crucible.
