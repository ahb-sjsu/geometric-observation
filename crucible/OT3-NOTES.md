# OT-3 notes — theorem proved, cliff measured, one instrument seal burned

**Verdict: PASS** (theorem: `OT3-THEOREM.md`; numerics v2:
`results/OT3-cliff-v2.json`; v1 FAIL committed as executed in
`results/OT3-cliff.json`).

- **Theorem:** T1a (adaptive, k ≤ d−2, zero-pilot construction), T1b
  (oblivious, k = d−1, reflection pair), T2 (side-information promise
  subspace: cliff at exactly d − k₀, lower and upper). One cell honestly
  open: adaptive k = d−1. Scope boundary vs generic-position phase
  retrieval stated in the theorem file.
- **Numerics:** cliff top 1.00 and bottom clean in all six cells at the
  predicted location d − k₀ for k₀ ∈ {0, 8, 16}; ramp bounded by
  confinement mass k/m + 0.10 throughout; **zero recoveries of a
  genuinely hidden component in any sub-cliff cell** (the
  theorem-faithful bar).
- **The v1 lesson, promoted to a v2 prediction:** raw exact-recovery
  share at k = m−1 for rank-1 is *not* zero — it is the Haar
  chance-alignment rate p_chance(m) = 2√(1−τ)·Γ(m/2)/(√π Γ((m−1)/2)),
  and the measured shares sat inside 3σ of it in all three cells while
  rank-4 (four simultaneous alignments needed) sat at exactly zero.
  Instrumentation rule worth keeping: **a recovery bar near a cliff
  must condition on the target actually being hidden** — raw success
  shares conflate identification with luck, in both directions.
- P3 now has the reviewer's requested ladder complete: definition
  (P_C) → theorem (confined transcripts cannot identify hidden
  components; cost = unpromised dimension, GL-invariantly by OT-7) →
  novel prediction (cliff shifts to d − k₀, stays a cliff) →
  experiment (six cells, predicted location, no smoothing).
