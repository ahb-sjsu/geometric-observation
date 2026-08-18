/-
Machine-checked cores of the v1-line owed-prediction margins
(`crucible/OWED-V1-DERIVATIONS.md`). The load-bearing decision rules:

* `op4_refresh_helps` — OP4's refresh crossover: refresh helps iff the
  staleness cost `κ_s·d²` exceeds the re-estimation error `E_est`, i.e.
  iff the drift `d` exceeds the floor `d* = √(E_est/κ_s)`.
* `op5_resolve` — OP5's response floor: a quantization step `g` is
  cleared iff the operator-weighted perturbation `t` exceeds `g²`, i.e.
  `g ≤ √t ↔ g² ≤ t`. The response-floor location is `t* ≈ g²/κ_p`.

Davis–Kahan-style spectral constants (`κ_s`, `κ_p`) enter as cited
scalars, per the program's standing standard; what is formalized is the
threshold algebra the campaigns bar against.
-/

import Mathlib

namespace ObservationTheory.OwedLaws

/-- OP5 response floor. For a nonnegative quantization step `g` and a
nonnegative operator-weighted perturbation `t`, the step is cleared
(`g ≤ √t`) exactly when `g² ≤ t`. So the response floor sits at
`t* = g²` (times the spectrum constant folded into `t`). -/
theorem op5_resolve (g t : ℝ) (hg : 0 ≤ g) (ht : 0 ≤ t) :
    g ≤ Real.sqrt t ↔ g ^ 2 ≤ t := by
  constructor
  · intro h
    have : g ^ 2 ≤ Real.sqrt t ^ 2 := by
      have hs : 0 ≤ Real.sqrt t := Real.sqrt_nonneg t
      nlinarith [h, hg, hs]
    rwa [Real.sq_sqrt ht] at this
  · intro h
    calc g = Real.sqrt (g ^ 2) := (Real.sqrt_sq hg).symm
      _ ≤ Real.sqrt t := Real.sqrt_le_sqrt h

/-- OP4 refresh crossover. For staleness coefficient `κs > 0`,
re-estimation error `E ≥ 0`, and drift `d ≥ 0`, refresh helps
(`E ≤ κs·d²`) exactly when the drift clears the floor
`d* = √(E/κs)`. -/
theorem op4_refresh_helps (κs E d : ℝ) (hκ : 0 < κs) (hE : 0 ≤ E)
    (hd : 0 ≤ d) :
    E ≤ κs * d ^ 2 ↔ Real.sqrt (E / κs) ≤ d := by
  have hfloor : 0 ≤ E / κs := div_nonneg hE (le_of_lt hκ)
  constructor
  · intro h
    have hEks : E / κs ≤ d ^ 2 := by rw [div_le_iff₀ hκ]; nlinarith [h]
    calc Real.sqrt (E / κs) ≤ Real.sqrt (d ^ 2) := Real.sqrt_le_sqrt hEks
      _ = d := Real.sqrt_sq hd
  · intro h
    have h2 : Real.sqrt (E / κs) ^ 2 ≤ d ^ 2 := by
      nlinarith [h, Real.sqrt_nonneg (E / κs), hd]
    rw [Real.sq_sqrt hfloor, div_le_iff₀ hκ] at h2
    nlinarith [h2]

end ObservationTheory.OwedLaws
