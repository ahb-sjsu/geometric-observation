# OT-3 — the identification lower bound

**The theorem half of OT-3 (claim frozen in `OT-CRUCIBLE.md`). Model,
two theorems with proofs, and the honest scope boundary. The numerical
half is sealed in `PREREG-OT3-APPENDIX.md` and run by `ot3_check.py`.**

## The observation model (chosen to be exactly what the instrument does)

**M(k) — subspace-confined second-order transcripts.** The instrument
selects unit directions `v₁, …, v_k ∈ R^d` (adaptively unless stated);
its transcript is the complete compressed block

    T(P, V) = { v_iᵀ P v_j : 1 ≤ i, j ≤ k },     V = span{v_i}.

This is a *stronger* oracle than the physical probe (finite differences
along `v_i` yield the projections `v_iᵀg` per sample; products give
exactly the block entries and nothing outside `V`) — granting the full
block only strengthens a lower bound. An estimator is any measurable
function of the transcript. The operator class: rank-r PSD with a fixed
spectrum `λ₁ ≥ … ≥ λ_r > 0`, orientation unknown.

**What the model deliberately excludes** (the scope boundary, stated
before anyone else states it): measurements in *generic position* — the
phase-retrieval / PhaseLift regime, where ~2d rank-one quadratic
measurements with independently drawn directions identify a rank-1 PSD
operator. The distinction is confinement: there, each measurement
direction is fresh and their span reaches `R^d`; here, k probe
directions confine every observable number to one k-dimensional
subspace. The instrument's sub-budget modes are confined in exactly
this sense; its exact mode (k = d) is the boundary case. The theorem is
about confinement, and claims nothing about generic-position designs.

## Theorem 1 (no side information)

**T1a — adaptive strategies, k ≤ d−2.** For every adaptive strategy
spending k ≤ d−2 directions and every estimator û, there exist two
operators `P± = λ u± u±ᵀ` in the rank-1 class with `⟨u₊, u₋⟩ = 0`
whose transcripts are identical. Consequently

    min± ⟨û, u±⟩² ≤ 1/2,

and identification of the leading eigenvector to arbitrary accuracy is
impossible: the worst-case error is bounded away from zero by an
absolute constant.

*Proof.* Run the strategy against the all-zeros transcript (every query
answered 0). Adaptivity collapses: the direction sequence of this pilot
run is deterministic; let `S⁰` be its span, `dim S⁰ ≤ k ≤ d−2`. Choose
orthonormal `u₊, u₋ ∈ (S⁰)^⊥` (possible since `dim (S⁰)^⊥ ≥ 2`). For
either `P±`, every pilot query `v ∈ S⁰` satisfies `v ᵀP± v' = λ
(vᵀu±)(v'ᵀu±) = 0`, so by induction the actual run against `P±`
reproduces the pilot's queries and answers exactly. The transcripts are
identical, û is the same for both, and it cannot have squared overlap
exceeding 1/2 with both members of an orthonormal pair. ∎

*Machine-checked (2026-08-17): the collapse induction, transcript
identity, and estimator bound are formalized in Lean 4 / Mathlib
(`lean/ObservationTheory/AdaptivePilot.lean`, sorry-free). The
`k ≤ d−2` dimension count enters as its consequence — orthogonality
of the hidden pair to every pilot direction.*

**T1b — oblivious strategies, k = d−1.** For a fixed (data-independent)
direction set with `dim V = d−1`, the same conclusion holds.

*Proof.* Let `w ⊥ V` be unit, pick unit `e ∈ V`, and set
`u± = (e ± w)/√2`. Then `⟨u₊, u₋⟩ = 0`, and for all `v, v' ∈ V`:
`vᵀP±v' = λ (vᵀe)(v'ᵀe)/2` — independent of the sign, so the
transcripts coincide. ∎

**The one open cell, recorded:** adaptive strategies at exactly
k = d−1. The zero-pilot argument needs two hidden dimensions and the
reflection pair breaks adaptivity (nonzero answers can steer later
queries). The instrument's fixed-design modes are oblivious, so the
instrument-relevant statement is fully covered; the adaptive d−1 cell
is left open and honestly so.

**Extension to rank r:** embed the pair in the leading eigendirection
and fix the remaining r−1 eigenvectors inside a common subspace of
`(S⁰)^⊥`'s complement; requires k ≤ d−r−1 for T1a's argument. The
leading-eigenspace version follows identically.

## Theorem 2 (side information — the cliff moves, and stays a cliff)

**Side-information model (promise form):** the estimator additionally
knows a subspace `W`, `dim W = d − k₀`, with the promise
`range(P) ⊆ W`. (This is the exact-seed version of "yesterday's scan
covered k₀ dimensions and excluded them.")

**T2a (lower bound).** Within the promise, all observable information
is confined to `V ∩ W`-spanned blocks; the pilot argument runs verbatim
inside `W`: for adaptive strategies with `k ≤ (d − k₀) − 2` (and
oblivious with `k = (d−k₀) −1`), two orthogonal-leading-eigenvector
operators produce identical transcripts. Identification impossible.

**T2b (upper bound — the cliff is exactly at d − k₀).** With
`k = d − k₀` directions spanning `W`, the transcript is the complete
block of `P` on `W ⊇ range(P)`, which determines `P` exactly:
identification at machine accuracy, in one step, with no excess.

Together: **k_crit = d − k₀, and the transition is a cliff** — below it
the worst case is Θ(1)-wrong regardless of estimator; at it, recovery
is exact. Side information moves the cliff by exactly its dimension; it
never softens it. This is the sealed prediction the numerical half now
tests, including the kill condition: if recovery improved *smoothly*
with k₀ (partial side information buying partial accuracy at fixed k in
the exact-recovery sense), the formulation dies.

## What this buys P3

P3's statement — ambient dimension prices identification, structure
prices only description — is now **definition → theorem → prediction**:
the price of finding `P_C` is `dim` of the *unpromised* space, in every
basis (rank is GL-invariant, OT-7), and no estimator cleverness inside
a confined design can pay less.
