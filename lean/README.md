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
(`lake build`, 1936 jobs, zero errors, zero `sorry`). Reproduce:
install elan, then `lake update && lake exe cache get && lake build`
in this directory.

**Scope, stated as in the theorem docs:** the adaptive pilot
argument (T1a), Davis–Kahan, and Gaussian operator-norm bounds are
NOT formalized — hand-proved or cited. The symbolic/exact-arithmetic
layer (`crucible/verify_theorems.py`) covers the Isserlis chain, the
KL constant, T2b exactness, and the cos²θ / change-of-measure laws.
