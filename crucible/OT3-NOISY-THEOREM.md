# OT-3N — the noisy cliff

**The theorem half of P3's open owed prediction (readscope
`PRINCIPLES.md` v0.2): with observation noise of scale σ on each
scalar reading, identification at k ≥ d floors at an error derivable
from σ and the spectrum gap, while the cliff's location does not
move. This document is desk work in the OT-3 model — extension,
proofs, and honest scope boundaries. It declares no campaign, no
family, and no bars: per the Third Crucible close-out, those are
separate acts with their own seals. Measurement discharges the owed
prediction; this only arms it.**

## The noisy observation model

Everything is as `OT3-THEOREM.md` — the instrument selects unit
directions `v₁, …, v_k` and would receive the compressed block
`T(P, V) = {vᵢᵀ P vⱼ}` — except each scalar entry is now read
through a noisy channel:

    T_σ(P, V) = { vᵢᵀ P vⱼ + ξᵢⱼ },   ξᵢⱼ iid N(0, σ²), ξⱼᵢ = ξᵢⱼ.

`m` independent re-reads of an entry are equivalent to one read at
scale σ/√m and are folded in silently. The operator class is
unchanged: rank-r PSD with fixed spectrum λ₁ ≥ … ≥ λ_r > 0,
orientation unknown; write γ_r = λ_r (the gap of the rank-r
spectrum to the null space) and, for eigenspace statements at rank
s < r, γ_s = λ_s − λ_{s+1}. As before, granting the whole block
only strengthens lower bounds, and generic-position designs remain
explicitly out of scope.

## Theorem N1 — the cliff does not move (lower bounds survive noise)

**N1a (oblivious designs, every σ ≥ 0).** For a fixed direction set
with `dim V = d−1` and any σ, the two operators of T1b
(`u± = (e ± w)/√2`, `w ⊥ V`) induce **identical distributions** on
the noisy transcript. Consequently no estimator attains squared
overlap > 1/2 with both, and worst-case identification error is
bounded below by the same absolute constant as in the noiseless
theorem — *independently of σ*.

*Proof.* By T1b the noiseless blocks coincide entrywise:
`vᵢᵀP₊vⱼ = vᵢᵀP₋vⱼ` for all `vᵢ, vⱼ ∈ V`. The noisy transcript is
this common mean plus noise whose law does not depend on the
operator, so the two transcript distributions are equal — total
variation distance zero. An estimator is a measurable function of
the transcript; its distribution is identical under P₊ and P₋, and
the noiseless two-point conclusion applies verbatim to every
realization. ∎

Noise cannot un-confine a design: no amount of it, and no averaging
of it, manufactures information outside `span V`. Smaller σ helps
nothing below the cliff because there was never a signal to clean.

**N1b (adaptive designs — what carries over, and the recorded
gap).** For σ = 0, T1a bounds adaptive strategies at k ≤ d−2. For
σ > 0 a simulation argument shows noise never *helps*: an adaptive
noisy-transcript strategy is simulated exactly by a *randomized*
adaptive noiseless strategy (draw the ξ's internally, add them to
the exact answers, follow the noisy strategy's decisions). The
noiseless lower bound needed here is T1a extended to randomized
strategies; the zero-pilot argument conditions on the internal
randomness, but the adversary pair may then depend on it, and
closing the resulting sup–average order of quantifiers is not done
in this document. **Recorded open, in the same spirit as OT-3's
adaptive k = d−1 cell.** The instrument's fixed-design modes are
oblivious, so the instrument-relevant statement is N1a, fully
proved.

## Theorem N2 — the σ-floor at full coverage

Let k = d with `{vᵢ}` orthonormal (the instrument's exact mode).
Observe `Y = VᵀPV + Ξ` with Ξ the symmetric Gaussian noise above,
and estimate `P̂ = V Y Vᵀ`.

**N2a (upper bound).** `P̂ − P = V Ξ Vᵀ`, so `‖P̂ − P‖₂ = ‖Ξ‖₂`,
and by the standard operator-norm bound for symmetric matrices with
independent N(0, σ²) entries (e.g. via the moment method or
Bandeira–van Handel), `E‖Ξ‖₂ ≤ C σ √d` with an absolute constant C
(≤ 3 suffices; concentration around the mean is subgaussian at
scale σ). By the Davis–Kahan theorem in the Yu–Wang–Samworth form,
the leading rank-s eigenspace satisfies

    E ‖sin Θ_s(P̂, P)‖₂ ≤ 2 E‖Ξ‖₂ / γ_s ≤ 2C σ √d / γ_s.

With m re-reads: `2C σ √(d/m) / γ_s`. Identification at k = d is
therefore never lost to noise — the error floor is **linear in σ,
inversely proportional to the spectrum gap**, and vanishes as
σ → 0 at fixed design. That is the derivable floor the owed
prediction names.

**N2b (matching lower bound in σ and γ, two-point).** Take the
rank-1 class `P_u = λ u uᵀ` and rotate the planted vector by angle
θ: `‖P_{u_θ} − P_u‖_F ≤ √2 λ θ`. The KL divergence between the two
noisy-transcript distributions is exactly
`(‖ΔP‖_F² + ‖diag ΔP‖²) / (4σ²) ≤ ‖ΔP‖_F² / (2σ²) ≤ λ²θ²/σ²`
(machine-verified symbolically, `verify_theorems.py`),
so for `θ = c₀ σ / λ` the two hypotheses are indistinguishable with
constant probability (Pinsker), and any estimator errs by
`sin Θ ≥ c₁ σ / λ` in the worst case over the pair. The floor is
real, not an artifact of the estimator choice: **noise prices
accuracy at rate Θ(σ/γ)** (the √d sharpening of the lower bound to
match N2a's `σ√d/γ` follows from the standard Fano argument over a
packing of the rotation orbit; cited, not reproved here — the
two-point version above is what this document proves).

## Corollary N3 — the step survives noise

Fix the spectrum and s, and let `σ < γ_s / (4C√d)`. Then:

- at `k = d`: worst-case eigenspace error ≤ 1/2 by N2a, and → 0
  linearly as σ → 0;
- at `k = d−1` (oblivious): worst-case error ≥ the absolute
  constant of N1a, **for every σ, including σ → 0**.

The transition in k is a step whose location is *invariant in σ*:
its upper side scales as O(σ√d/γ), its lower side is Ω(1)
identically. **Noise prices accuracy, never admission** — which is
P3's sentence, now a theorem in the confined-transcript model.

## Theorem N4 — side information, noisy (one paragraph)

Under the promise `range(P) ⊆ W`, `dim W = d − k₀`: N1a's
total-variation argument runs verbatim inside W (the T2a pair's
blocks coincide on any oblivious V with `dim(V) = d − k₀ − 1`), and
N2 applies with d replaced by `d − k₀` once V spans W. The cliff
sits at exactly `d − k₀` for every σ, with the same O(σ√(d−k₀)/γ)
upper face and Ω(1) lower face. Side information moves the cliff by
its dimension; noise still cannot soften it.

## Two remarks that tie the theorem to the instrument

1. **Physical-probe noise is isotropic in the bias, Davis–Kahan in
   the fluctuation.** The oracle model reads block entries; the
   physical probe reads finite differences and squares gradient
   estimates, so per-reading noise enters `ĝĝᵀ` as an isotropic
   bias `σ_eff² I` plus zero-mean fluctuation. The bias is exactly
   the eigenvector-preserving structure of the Isserlis inflation
   (C-2b) and is removable in closed form; the fluctuation is what
   N2 prices. C-15's measured refusal of sub-dimensional budgets to
   converge at 8× total budget is the finite-sample face of the
   same fluctuation term — variance, not bias, is the enemy at
   every layer of this instrument, and the noisy cliff says it is
   the *only* enemy above the cliff.
2. **What a future measurement family owes** (sketch only, not
   declared): a planted-spectrum sweep in (σ, k) around k = d must
   show the two faces — error linear in σ with slope ∝ √d/γ_s at
   k ≥ d (N2a, with the slope itself the graded quantity), and
   σ-independent Θ(1) error at k < d (N1a) — plus the side-
   information shift of N4. Its interior requirements (a σ grid
   with points on both sides of γ/√d, and margins against the
   estimator's own sampling noise) are exactly the lessons the
   Second and Third Crucibles paid for. Constructing and
   shakedown-qualifying that family is the next act; it is not this
   one.

## Verification status (added 2026-08-17, pre-v1.0)

Hand-proved and reviewed; **machine-verified where machine
verification reaches**: the N1a/T1b confinement identity, the
reflection pair's orthogonality, and the T2b/N4 exactness are
checked in exact rational arithmetic and symbolically
(`crucible/verify_theorems.py`, 11/11) and formalized in
Lean 4 / Mathlib (`lean/ObservationTheory/Confinement.lean`); the
Isserlis chain and the N2b KL constant are verified symbolically
(the KL line above was tightened by that check). **Not
machine-checked:** the adaptive pilot argument (T1a), Davis–Kahan,
and the Gaussian operator-norm bound — cited standard results,
hand-applied. The measured instantiation is OT-16 (PASS, fresh
seed).
