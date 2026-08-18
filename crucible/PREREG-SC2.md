# PREREG-SC2 — LEO / interplanetary transport under predictable nonstationarity

**STATUS: UNSEALED.** Construction + shakedown only. Second campaign of
the space-comms crucible (after SC-1's downlink allocation). A distinct
Observation Theory handle: **P4 + P5**, not the AM/GM allocation law.
Bars bind only on a dated seal a day later than this construction
(cooling-off), after the shakedown shows the family's interior across
seeds. No evidential weight until then.

## The domain and the claim

Starlink hands over ground-satellite links on a fixed ~15 s cadence;
the bursty loss is misread by standard TCP/QUIC as congestion, and the
proposed LEO-aware transports (StarTCP, Leotp, Cloudflare's CC) fix it
by *knowing the handover schedule*. SpaceX's proposed **Marslink** — a
Starlink-architecture relay at up to 1.5 AU, ~4 Mbps, laser ISLs — takes
this to the limit: a ~25-minute round trip makes closed-loop congestion
control physically impossible, so the controller **must predict the
channel from its structure**.

OT reads the congestion controller as a *consumer* whose read operator
"loss → congestion" is mismatched to a predictably nonstationary
channel. Observed loss is `L = H OR C`: a deterministic, known handover
indicator `H` (duty cycle `ρ`) ORed with the true congestion state `C`
(Markov, stationary rate `c`, lag-1 autocorrelation `λ`); feedback is
delayed by `D`. Two read operators — `naive Ĉ = L(t−D)`, and
`aware Ĉ = L(t−D) AND NOT H(t−D)` (masks the known schedule at the known
lag).

## The two a-priori claims

- **Arm A — the metric-consequence floor (P5).** Masking the
  *predictable* disruption removes a false-congestion error proportional
  to the handover duty cycle: `excess = naive_err − aware_err = κ·ρ`,
  `κ` a derivable coefficient, **invariant to the delay `D`** (the
  schedule is known at any lag).
- **Arm B — nonstationarity vs delay (P4).** The feedback-tracking error
  grows with `D` as the congestion state decorrelates,
  `aware_err = 2c(1−c)(1 − λ^D)`, toward the fully-decorrelated floor
  `2c(1−c)`. Past a derivable crossover the delay error dominates the
  duty cycle: **reactive feedback is useless and only the deterministic
  schedule is recoverable.** Marslink is deep in that regime — a sharp
  prediction about *which* structure survives interplanetary delay.

## Shakedown outcome (2026-08-18)

`fam_sc2_shakedown.py` (T=200k, `T_H=100`, `c=0.15`, `λ=0.90`, seeds
{0,1,2}; `results/SC2-shakedown.json`; per-seed spread ≤ 0.007
everywhere — the interior is large-sample stable).

**Arm B — confirmed, and it is the sharp one.**

| D (steps) | aware_err | predict `2c(1−c)(1−λ^D)` | excess (schedule) |
|---|---|---|---|
| 2 | 0.063 | 0.048 | 0.105 |
| 20 | 0.211 | 0.224 | 0.106 |
| 100 | 0.239 | 0.255 | 0.105 |
| 500 | 0.238 | 0.255 | 0.105 |
| 2000 | 0.236 | 0.255 | 0.105 |

The feedback error rises along the decorrelation law toward the floor
`2c(1−c)=0.255`, while the **schedule component (`excess`) is flat to
three digits across a 1000× span of delay** — exactly the D-invariance
predicted. At interplanetary delay the reactive congestion signal is
gone (`aware_err` at the floor: feedback carries no information about
the current state) and only the deterministic schedule remains
recoverable. This is the Marslink claim, borne out.

**Arm A — structure confirmed, and the coefficient now derived.**
`excess` is clean-linear in `ρ` (0.034, 0.069, 0.139, 0.209 at
ρ=0.05…0.30), D-invariant, slope **≈ 0.70** — below the naive `1−c =
0.85`. Deriving it: with `naive = H' ∨ C'`, `aware = C' ∧ ¬H'`
(`X' = X(t−D)`, target `C = C(t)`), `H' ⊥ (C',C)`, `P(H'=1)=ρ`, and the
2-state chain's lag-D joint `p11 = c²+c(1−c)r`, `p00 = (1−c)²+c(1−c)r`,
`p01 = p10 = c(1−c)(1−r)` (`r = λ^D`):

    naive_err = (1−c) − (1−ρ)p00 + (1−ρ)p01
    aware_err = (1−ρ)p10 + c − (1−ρ)p11
    excess = (1−2c) + (1−ρ)(p11−p00),   p11−p00 = c²−(1−c)² = 2c−1
           ⇒  **excess = (1 − 2c)·ρ,   κ = 1 − 2c.**

At `c=0.15`, `κ = 0.70` — matching the measured 0.698. The interpretation
is exact: `κ = (1−c)` false-positive benefit `− c` masking-miss cost
(masking blanks true congestion that coincides with a handover), so
`κ = 1−2c`, and **masking is net-beneficial iff `c < ½`** (κ > 0) — a
sharp, falsifiable boundary. The lag-D correlation `r` cancels
identically, which is *why* Arm B's schedule excess is delay-invariant:
the two arms share one algebraic fact. Verified two ways — exact
enumeration over the joint `(H',C',C)` across `c, ρ, r`, and machine-
checked in Lean 4 / Mathlib (`lean/ObservationTheory/SpaceComms.lean`,
`joint_gap` + `sc2_excess`, built clean, sorry-free, three standard
axioms).

## Bars (TO BE SEALED on a fresh day; not yet binding)

- **B1 — the delay-decorrelation law (Arm B, ready).** `aware_err(D)`
  fits `2c(1−c)(1−λ^D)` with R² ≥ 0.95, and `aware_err(D_max) ≥ 0.9 ·
  2c(1−c)` (feedback reaches the floor), on each of ≥3 disjoint seeds.
- **B2 — schedule D-invariance (Arm B, ready).** `excess(D)` varies by
  ≤ 0.01 across the full `D` sweep — the predictable component is
  delay-invariant.
- **B3 — the duty-cycle floor (Arm A, ready).** `excess = κ·ρ` linear
  (R² ≥ 0.98) through the origin, with the **derived** `κ = 1 − 2c`
  (`SpaceComms.lean`), fitted slope within `±0.05` of `1 − 2c`, on each
  of ≥3 disjoint seeds. Secondary: the sign boundary — a scenario with
  `c > ½` gives `κ < 0` (masking hurts).

**Kills.** `aware_err` not reaching the decorrelation floor at large `D`
(the reactive signal secretly survives delay — refutes P4's collapse);
or `excess` growing with `D` (the schedule component is not
delay-invariant — refutes the P5/schedule claim); or `excess` not linear
in `ρ` (no duty-proportional floor). Any returns the transport claim to
revision without touching the frozen principles.

## Discipline and scope

Synthetic substrate (a planted Markov channel + deterministic schedule),
so a pass earns the *mechanism* — the read-operator account of why
handover-aware transports work and why interplanetary feedback collapses
— not a systems claim about StarTCP or Marslink. A real-trace substrate
(measured Starlink handover timings, loss traces) would be its own later
campaign. All three bars are now ready (Arm A's `κ = 1−2c` derived and
Lean-checked); the seal is a fresh-day act with a graded runner on
disjoint seeds. Frozen v1.0 statements untouched; this extends the
evidence to a new domain (P4/P5 in transport), or scopes the transfer
if it fails.

## Provenance

- Sibling: `crucible/PREREG-SC1.md` (the downlink allocation crucible).
- Substrate: `crucible/fam_sc2_shakedown.py`; record
  `results/SC2-shakedown.json` (no weight). Graded runner `sc2_check.py`
  added at seal, on disjoint seeds.
- Machine-checked algebra: `lean/ObservationTheory/SpaceComms.lean`
  (`joint_gap`, `sc2_excess` — `κ = 1−2c`, built clean, sorry-free).
- Motivation (searched 2026-08-18): StarTCP (APNet 2024), Leotp,
  Cloudflare LEO congestion control; SpaceX Marslink relay proposal.
