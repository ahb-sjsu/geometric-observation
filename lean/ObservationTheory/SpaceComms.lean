/-
Machine-checked algebra of SC-2 Arm A — the corrected masking coefficient
(`crucible/PREREG-SC2.md`).

A congestion controller reads `loss → congestion` on a channel whose loss
is `L = H ∨ C`: a deterministic, known handover schedule `H` (duty `ρ`)
ORed with a Markov congestion state `C` (rate `c`, lag-D correlation
`r = λ^D`). Feedback is delayed by `D`. Two read operators:
`naive = L(t−D)`, `aware = L(t−D) ∧ ¬H(t−D)` (masks the known schedule).

Enumerating the joint `(H', C', C)` (verified exhaustively in
`fam_sc2_shakedown.py`) gives the two error rates as linear expressions
in the lag-D joint probabilities `p11, p00, p10, p01`. The load-bearing
step is that their difference collapses to `(1 − 2c)·ρ` — the delay `r`
cancels, and the coefficient is `κ = 1 − 2c`, NOT the naive `1 − c`.

* `joint_gap` — the diagonal joint probabilities of the 2-state chain
  differ by exactly `2c − 1`, independent of the lag-D correlation `r`
  (the delay cancels — the source of Arm B's D-invariance).
* `sc2_excess` — the naive-minus-aware error, as a function of `(c, r, ρ)`,
  equals `(1 − 2c)·ρ`. The masking gain is the false-positive benefit
  `(1−c)` minus the masking-miss cost `c`; it is net-positive iff
  `c < 1/2` (`κ > 0`).
-/

import Mathlib

namespace ObservationTheory.SpaceComms

/-- The lag-D joint of the 2-state congestion chain. With rate `c` and
lag-D correlation `r`, the diagonal joint probabilities `p11 = c² + c(1−c)r`
and `p00 = (1−c)² + c(1−c)r` differ by exactly `2c − 1`, independent of
`r`: the delay cancels. This is why Arm A's coefficient — and hence Arm
B's schedule excess — is delay-invariant. -/
theorem joint_gap (c r : ℝ) :
    (c ^ 2 + c * (1 - c) * r) - ((1 - c) ^ 2 + c * (1 - c) * r)
      = 2 * c - 1 := by ring

/-- SC-2 Arm A, the corrected coefficient. With handover duty `ρ`,
congestion rate `c`, and lag-D correlation `r`, and the enumerated error
rates
  `naive_err = (1−c) − (1−ρ)p00 + (1−ρ)p01`,
  `aware_err = (1−ρ)p10 + c − (1−ρ)p11`,
the excess `naive_err − aware_err` collapses to `(1 − 2c)·ρ`. The lag-D
correlation `r` cancels (delay-invariant), and the coefficient is
`κ = 1 − 2c`, not the naive `1 − c`. -/
theorem sc2_excess (c r rho : ℝ) :
    ((1 - c) - (1 - rho) * ((1 - c) ^ 2 + c * (1 - c) * r)
        + (1 - rho) * (c * (1 - c) * (1 - r)))
      - ((1 - rho) * (c * (1 - c) * (1 - r)) + c
        - (1 - rho) * (c ^ 2 + c * (1 - c) * r))
      = (1 - 2 * c) * rho := by ring

end ObservationTheory.SpaceComms
