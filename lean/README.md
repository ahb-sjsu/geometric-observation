# Lean formalization — the confinement engine

`ObservationTheory/Confinement.lean` machine-checks the load-bearing
algebra of `crucible/OT3-THEOREM.md` and `crucible/OT3-NOISY-THEOREM.md`:

- `reflection_pair_orthogonal` — the T1b adversary pair is a genuine
  orthonormal pair (so the ≤ 1/2 overlap conclusion bites);
- `confined_entry_identity` — the transcript identity: probing
  vectors orthogonal to the hidden direction cannot distinguish the
  two operators, entry by entry (the engine of T1b, and of N1a since
  the noise law is operator-independent);
- `promise_entry_identity` — the same, relativized (T2a / N4): why
  the cliff relocates to d − k₀ and never softens.

**Build record:** Lean `leanprover/lean4:v4.32.2`, Mathlib tag
`v4.32.2`, built clean 2026-08-17 on the Atlas workstation
(`lake build`, 1937 jobs, zero errors, zero `sorry`). Reproduce:
install elan, then `lake update && lake exe cache get && lake build`
in this directory.

`ObservationTheory/AdaptivePilot.lean` closes the piece
`Confinement.lean` left hand-proved: OT-3's **T1a**, the adaptive
pilot argument. It machine-checks the adaptive collapse
(`run_answers_zero`: a strategy fed the all-zeros pilot reproduces it
against either operator, by induction on the query sequence),
transcript indistinguishability (`t1a_transcripts_agree`), and the
estimator bound (`overlap_pair_bound`: no unit vector overlaps both
members of an orthonormal pair above ½), assembled in `t1a`. The
`k ≤ d−2` dimension count enters as the hypothesis it buys
(orthogonality to every pilot direction); the adaptive `k = d−1`
cell stays open, as the theorem doc records.

**Scope, stated as in the theorem docs:** Davis–Kahan and the
Gaussian operator-norm bound remain cited standard results, not
formalized. The symbolic/exact-arithmetic
layer (`crucible/verify_theorems.py`) covers the Isserlis chain, the
KL constant, T2b exactness, and the cos²θ / change-of-measure laws.
