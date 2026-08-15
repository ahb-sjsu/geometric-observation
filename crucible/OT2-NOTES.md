# OT-2 notes — loading is a covariance, measured

**Verdict: PASS, B1–B4** (`results/OT2-loading-law.json`, bars sealed
in `PREREG-OT2-APPENDIX.md` before the run).

- **The law's shape:** measured reading error vs the base-measure
  prediction `ε‖E[h·A]‖_F` across the alignment family — max shape
  deviation **0.0031** (bar 0.08). The functional predicted the entire
  curve from under the unshifted measure.
- **Orthogonality:** the 90° shift — same `‖Δμ‖`, same KL as the
  aligned one — produced reading error **7.7e-17, machine zero**. A
  large shift the operator's variation cannot see does nothing, exactly
  as `E[h·A] = 0` prices it.
- **First-order convergence:** relative error 1.05% at ε = 0.05,
  0.62% at ε/2 (ratio 0.59 ≈ the linear-law 0.5).
- **The kill test:** scalar loading was constant across the family by
  construction; measured error varied over the grid and tracked the
  alignment functional at Spearman 1.00. The covariance beat the
  distance because the distance had nothing to say.

**Honesty flag on B3's spread term:** the ≥5× spread was satisfied via
the 90° cell's *exact* zero — for this consumer, `b` lies in the kernel
of every gradient (`span(a₁,a₂)` exhausts the read directions), so
functional orthogonality coincides with exact invariance and the
max/min ratio is degenerate-large. Over the non-degenerate cells
(0°–75°) the spread is **3.8×** — below the bar's number, though the
Spearman-1.00 ordering carries the kill test's substance regardless.
Recorded so nobody reads the astronomical ratio as a generic effect
size: a consumer whose read directions and variation directions
decouple would give a finite (and smaller) orthogonal cell. That
sterner construction is a natural OT-2 hardening if the campaign wants
one; the sealed bars as written are met.

**Descriptive covariance-shift cell:** aligned variance inflation
2.5e-3 vs orthogonal 6e-17 — same law, second shift family.

**For P2:** the three failed scalar corrections now have their closing
statement: the right object was never a distance between distributions
but the covariance of the change of measure with the local operator —
derived in the Crucible, and now measured to first order.
