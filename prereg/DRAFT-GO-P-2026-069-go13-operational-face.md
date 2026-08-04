# DRAFT (UNSEALED) — GO-P-2026-069: GO-13 operational face — the dynamic tax on materialized records

STATUS: DRAFT. ID 069 reserved; NO hash, NO seed commitment; PROTOCOL
§5.1 requires the harness pilot before seal, and the harness
(058-lineage, two consumers + aged context) is not yet built. This
draft registers the DESIGN so the instance choices and gates are
fixed by the regime map before any instrument code exists.

**Design.** 058/061-lineage decode-threshold instrument (materialized
codebook records, MAP decode via strided argmin, thr_interp
0.25-crossing), extended to two consumers reading one Gaussian triple
(Y_A, Y_B, V) with 2-D records, eraser context S built at controlled
access classes. Instances FIXED by the exploratory regime map
(experiments/go13_regime_sweep.py, seed 20260925, committed):

- RISING instance: r = (0.0, 0.8, 0.3), D = (0.2, 0.2), w-face 0.5 —
  predicted dCT_W/dq = +0.286 bits/unit-q (the grid maximum; binding
  consumer context-poor), measured across two staleness levels with
  Δq ≈ 0.3 → predicted tax increase ≈ 0.086 bits, an order of
  magnitude above the known decode-threshold bias (~0.007–0.008,
  paired-bias device of the 064 cross-net to be used).
- UNIVERSALITY control: two access classes tuned to equal q (slice vs
  prefix, per Theorem 1) — equal measured taxes, the
  analytic-equality control of the 065 kind.
- FLAT contrast: r = (0.3, 0.7, 0.2), D = (0.15, 0.4) — predicted
  |dCT_W/dq| < 1e-3; gate is PAIRED (tax change small relative to the
  rising instance's), never a bare sign gate at instrument
  resolution.

Gates to be finalized at pilot per §5.1 (power/pilot fields, ≥1.3×
margins, instrument-vs-physics separation). Falsification shape: a
measured tax DECREASE at the rising instance beyond the paired-bias
envelope refutes Theorem 2's sign law operationally; unequal taxes at
tuned-equal q refutes Theorem 1's universality operationally.

Novelty flanks owed before any GO-13 novelty language (unchanged from
the problem statement): multiterminal/CEO with stale SI,
Heegard–Berger degraded-SI, Simeone–Permuter multi-decoder variants.
