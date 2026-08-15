# OT-1 notes — the geometry law, synthetic to real, zero refit

**Verdict: PASS — S1 ∧ S2 ∧ R1 ∧ H1 all hold**
(`results/OT1-arms-sr.json`, `results/OT1-arm-h.json`; sealed bars in
`PREREG-OT1.md`, untouched since the Crucible seal).

- **S1 (the derived curve):** measured damage ratio vs cos²θ across
  {0°…90°}: maximum deviation **0.0008** against a 0.05 bar — the
  zero-parameter law to four decimals.
- **S2 (the 45° flip):** consumer 1 prefers codec B at every θ (as
  derived); consumer 2 flips B→A between 30° and 45° — disagreement
  switches on inside the sealed bracket, at the predicted boundary.
- **R1 (rank-4, no refit):** trace-ratio prediction vs measurement over
  20 random constructions: max relative error **0.0015** (bar 0.10).
- **H1 (real heads, the transfer):** eight Llama-3.2-3B head-pairs
  sharing a KV stream (GQA share verified bit-exact), consumers = each
  head's attention mass on the probed key for its 24 real queries,
  operators recovered **blind** (readscope `jacobian_probe`,
  k/d = 1.25), codecs random equal-trace rank-4 drawn independently of
  the probes. `sign(tr((P̂₁−P̂₂)(Σ_A−Σ_B)))` predicted the measured
  preference disagreement **8/8** (bar 7/8). Recorded θ̂ spread
  58°–80° — no degenerate near-parallel pairs occurred, so the sealed
  threat ("θ̂ < 10° predicts weak signals") never activated.

**One runner defect, fixed before any verdict and worth keeping:** the
first Arm R implementation built the rank-4 consumer as a *scalar sum*
of features, whose true read operator is rank-1 (`E[ggᵀ]` keeps the
gradient cross-terms; they do not average away), and the "prediction"
was computed for an operator the consumer did not realize — max error
590×. The vector-valued consumer (damage in its own G-norm) realizes
the declared `P` exactly and the error fell to 0.0015. Lesson, same
family as OT-3's: **verify that the constructed consumer realizes the
operator the prediction is computed for** — a sum of features and a
vector of features have different read geometries (this is P1 applied
to one's own instruments).

**What OT-1 establishes for the campaign:** the P1 prediction ladder —
derive curve → seal curve → measure curve → transfer to real consumers
with no refit — completed end to end. Consumer disagreement follows
read-subspace geometry, measured by an instrument that never saw the
consumers' internals.
