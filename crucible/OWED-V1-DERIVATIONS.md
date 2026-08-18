# v1-line owed predictions — a-priori margin derivations

Desk work (no seal): the derivable a-priori laws for the v1-line owed
predictions that do not yet have a campaign, so each future campaign
seals against a *derived* margin, not a guessed one. Companion to
`OWED-V1.md` (the mint) and the per-prediction appendices. OP1 and OP3
have their own appendices; this covers **OP4, OP5, OP2**. Clean cores
are machine-checked in `lean/ObservationTheory/OwedLaws.lean`.

## OP4 — the refresh floor `d*` (P4)

A codec fitted at time 0 serves until refresh. Two costs to the
consumer: **staleness**, the operator drifts by `d` since the fit,
costing excess distortion `≈ κ_s·d²` to leading order (quadratic in
drift); and **re-estimation**, refitting from `n` samples with a
`b`-bit codec injects error `E_est(b) = σ²/n + c·2^{-2b}` (sampling
variance plus quantization variance). Refresh removes the staleness bias
but pays `E_est`. So **refresh helps iff `κ_s·d² > E_est`**, i.e. iff
the drift exceeds the floor

    d* = √(E_est / κ_s),   E_est(b) = σ²/n + c·2^{-2b}.

`d*` is **derivable** from the spectrum (through `κ_s`, how the drifted
directions load the consumer) and the bit budget (through `E_est`): a
finer codec lowers `E_est`, hence lowers `d*` — refresh pays at lower
drift. This is OT-14's recorded edge (refresh below drift ≈ 0.1 costs)
turned into a predicted crossover. **Kill:** the measured floor departs
from the derived `d*` by more than 2×. The decision rule
`E_est ≤ κ_s·d² ⇔ √(E_est/κ_s) ≤ d` is Lean-checked (`op4_refresh_helps`).

## OP5 — the response-floor location (P5)

A consumer with output quantization step `g` resolves an input
perturbation only if the induced output change clears the step. A
perturbation of operator-weighted size `t` (`t = tr(P·Σ_δ)`) produces an
RMS output change `≈ √t` (up to a spectrum constant `√κ_p`). The
consumer resolves it iff `√(κ_p·t) ≳ g`, i.e. above the floor

    t* ≈ g² / κ_p.

The response-floor **location is derivable** from the output
quantization `g` and the codec spectrum (through `κ_p`): below `t*` the
informative fraction collapses (OT-18's floor), above it the consumer
resolves. **Kill:** the measured collapse location departs from `t*`
outside the family's interior band. The threshold `g² ≤ κ_p·t ⇔
g ≤ √(κ_p·t)` is Lean-checked (`op5_resolve`).

## OP2 — the transfer residual (P2)

Moment-matched (Gaussian) transfer captures a real activation measure to
second order; the residual is the part carried by higher moments. To
leading correction the moment-matched transfer error is governed by the
**operator-weighted excess kurtosis** of the activation measure,

    err ≈ κ_4 · ( E[(u_P)⁴] − 3·E[(u_P)²]² ),   u_P = P-weighted activation,

so the residual carries an *a-priori* bound from a measured
non-Gaussianity functional rather than an empirical one. The pre-named
L21_H3 head (OT-15) is the high-non-Gaussianity case where even
full-sample Gaussian moments sit at 1.0 — the prediction is that its
residual is the largest *because* its excess kurtosis is. **Kill:** the
residual does not track the kurtosis functional (rank correlation <
0.6). This one is a statistical functional (not a closed algebraic
identity), so it is stated here and tested empirically at its campaign,
not Lean-formalized.

## Status

OP4, OP5 cores machine-checked (`OwedLaws.lean`, sorry-free). Each still
needs its own substrate + shakedown + fresh-day seal before it
discharges; this file fixes the *targets* those campaigns will bar
against.
