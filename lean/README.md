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

## Estimation-and-control boundary results

`ObservationTheory/WeightedMeanInvariance.lean` machine-checks the two
algebraic anchors of the estimation-and-control paper
(`paper/Observation Theory for Estimation and Control.docx`):

- `weighted_mean_invariance` — **Proposition 1** (discrete form): for ANY
  matrix `P` with nonnegative quadratic form and any finite weighting
  summing to 1, the weighted mean minimizes the expected quadratic loss
  `E[(X−a)ᵀP(X−a)]` over `a`. A fixed consumer weighting therefore does
  not move the optimal (posterior-mean / Kalman) estimate — OT does not
  create a new Kalman filter by reweighting state error. The formal
  hypotheses are *weaker* than the paper's prose: neither symmetry/PSD
  structure beyond `∀v, 0 ≤ vᵀPv`, nor nonnegative weights, are needed.
- `value_of_observation_rank_one` — the §5 identity: for symmetric prior
  covariance `Σ`, scalar measurement `(h, r)`, and rank-one consumer
  `P_C = ggᵀ`, the consumer-relative value of observation is
  `V_C = tr(P_C(Σ−Σ⁺)) = (gᵀΣh)² / (hᵀΣh + r)`.
- Recorded caveat (in the file header): Proposition 1 is for FIXED `P`;
  a state-dependent `P_C(x)` breaks the argument, and the optimal
  estimate need no longer be the posterior mean.

**Build record:** Lean `leanprover/lean4:v4.32.2`, Mathlib tag `v4.32.2`,
built clean 2026-08-18 on the Atlas workstation (`lake build`, 8659 jobs,
zero errors, zero `sorry`).
