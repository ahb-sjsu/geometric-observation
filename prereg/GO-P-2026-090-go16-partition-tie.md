# GO-P-2026-090 — GO-16 Theorems 1–3: the revelation reduction and the partition/tie theorem (C3 net)

Governs `experiments/go16_verify_partition.py` for the theorems of
`paper/go16-adversarial-observer.tex` v0.3: the revelation reduction
(leakage through K = FᵀN⁻¹F only; minimal cost of K exactly linear,
tr(S(I−K)Sᵀ); shrink-and-dither attainment; convex SDP with bilinear
saddle), the general partition/tie structure, the diagonal water-level
closed form with the fractional/integral two-regime alternative, and
dither necessity. Sentinel `GO16_PARTITION_VERIFY_BEGIN/END`; flag
`ALL_PASS`.

Distinct from every prior GO-16 run: this seal names a GOVERNED seed
(20260822) at which all randomly drawn objects — the V1 instance, the
V2 policy sample, the V3/V4 random policies, V567's saddle
perturbations and optimizer restarts, V9's rotation and general
instance — are FRESH. The theorem-carrying identity gates therefore
run genuinely out-of-sample; the pinned-instance values (V5/V6/V8
hand-derived numbers) are committed-value reproductions and declared
as such. V10 recreates the v0.1 probe instance from its own internal
seed by design and is independent of the governed seed.

```yaml
id: GO-P-2026-090
date: 2026-08-21
retrospective: false
kind: theorem-verification (C3 net; theorems PROVED in the statement and
  R-IND-5-verified by an INDEPENDENT fresh-context verifier BEFORE this
  seal — paper/GO16-R-IND-5-NOTES.md — including the verifier's own
  byte-identical harness rerun and independent recompute of both hand
  instances; stronger provenance than a self-audit, and the seal says so)
claim: "Leakage to a rank-k-budgeted reader depends on the record policy
  (F, Sigma_w) only through the revelation operator K = F'N^-1F, with
  phi_k(G) = phi_k(M^1/2 K M^1/2); the minimal value cost of achieving K
  is exactly tr(S(I-K)S'), attained by F = SK, Sigma_w = SK(I-K)S'; the
  reduced game is a convex SDP whose bilinear saddle yields the
  four-way partition with encoder-indifference pricing and the spectral
  tie under fractional attention; the diagonal closed form is the
  attention water level with tie iff contested; noiseless records have
  idempotent revelation (dither necessity)."
harness: experiments/go16_verify_partition.py   # GOVERNED seed 20260822
hash: sha256:a5ed1dab5ac39f578b04eb3bd2ee8a582a0cddb5f99de796b89bd662c8156491
power: |
  Identity/reproduction gates with pilot-measured margins (dev seed
  20260821, final pilot): V1 cost error 0.0 vs 1e-9; K-error 1.3e-11 vs
  1e-7 (7700x); spectrum 5.9e-11 vs 1e-7 (1700x). V2: 0 violations in
  2000, worst SLACK +1.33. V3 5.5e-14 vs 1e-6 (1.8e7x). V4 2.9e-14 vs
  1e-8 (3.4e5x). V6 ties/budget/theta exact to 1e-9-1e-12. V7 saddle
  0.0 vs 1e-9 both sides. V8 closed form exact to 1e-12, direct 5.6e-6
  vs 1e-3 (180x). V9 rotated: spectrum err 6.6e-3 vs 5e-2 (7.6x), tie
  gap 7.0e-4 vs 5e-2 (71x), J err 1.1e-3-ish vs 2e-2 rel. TIGHT GATES,
  named: V5 direct-vs-closed gap 3.7e-3 vs 5.05e-3 (1.36x, above the
  1.3x house floor but barely — INSTRUMENT gate, optimizer-dependent);
  V9b general-instance J-match (subgradient convergence — INSTRUMENT).
pilot: |
  ALL RUNS TO DATE DISCLOSED (dev seed 20260821 throughout):
  run 1 (v0.2 instrument) — ALL PASS 9/9; committed as
    results/go16-partition-verify.json at commit 4b942a2.
  R-IND-5 verifier rerun — byte-identical (UTF-8 BOM aside), plus the
    verifier's INDEPENDENT solvers reproducing both hand instances
    exactly (its report, findings 10).
  run 2 (v0.3 instrument, post-R-IND-5 revisions: V9 de-vacuated onto
    the rotated known-fractional instance, V10 measurement added, JIT
    comment) — ALL PASS 9/9.
  run 3 (comment-only edit; regenerated artifact) — ALL PASS 9/9,
    committed at 42c54ac.
  Gate-history honesty: V9's original tie gate PASSED VACUOUSLY in run
  1 (fractional_K false) — caught by R-IND-5, replaced by the rotated
  known-fractional instance where it now bites (tie gap 7e-4 measured).
  No physics bar was loosened at any point; the V9 replacement
  STRENGTHENED the gate. V6 is circular with the theorem by
  construction (declared in-code and in the statement); the
  non-circular support is V5 + V7 + V9 + the R-IND-5 independent
  reproduction.
prediction:
  V1_achievability: cost identity exact (<1e-9), K-verification <1e-7,
    spectrum equality <1e-7, at a FRESH random (S, K, M)
  V2_lower_bound: 0 violations in 2000 FRESH random policies
  V3_spectrum_reduction: phi_k equality <1e-6 over 200 FRESH policies,
    all k
  V4_idempotency: noiseless-record K idempotent <1e-8 over 200 FRESH F
  V5_closed_form_vs_direct: |J_direct - 4.052777...| < 1e-3*(1+J) with
    FRESH optimizer restarts (instrument)
  V6_partition: t*=1.0, theta=(0.125, 1, 0.2222..., 0.652777..., 0, 0),
    budget exact, tie gap <1e-12 (committed-value reproduction)
  V7_saddle: 0 violations in 500 FRESH perturbations per side; dither
    trace at optimum > 1e-3
  V8_m2: J* = 7/4 exact; direct within 1e-3 (instrument)
  V9_rotated_and_general: FRESH rotation — fractional K detected,
    spectrum err <5e-2 vs (0.25, 1, 5/9, 1, 1, 1), tie rel gap <5e-2,
    J within 2e-2 rel of 4.052777...; FRESH general instance J-match
    within 2e-2 rel (instrument)
  V10: measurement only (ungated; numbers recorded for the corrected
    C4 diagnosis)
falsification: physics gates are V1, V2, V3, V4, V6, V7, V9a
  (known-fractional): a fail refutes this registration's netting claim
  and reopens the corresponding theorem's verification (the theorems
  are proved and independently verified, so a physics fail indicts the
  proof chain or the harness and blocks any [predicted]-grade citation
  until resolved). Instrument gates are V5, V8-direct, V9b (optimizer
  races): a fail voids the run — logged instrumentation miss, rerun
  only under a dated amendment. Single governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20260822, after the
    disclosed pilots above; no further pilots under this ID
  runtime: ~2 min CPU single-threaded
controls: [V4 idempotency (dither necessity's mechanism), V7 two-sided
  saddle perturbations, V9a known-value recovery in a rotated basis
  (non-circular), V10 pinned-seed instance recreation (governed-seed
  independent by design)]
provenance: |
  The hand-derived instance values (t*=1, J*=4.052777..., theta vector,
  m=2 J*=7/4) were derived BEFORE the harness existed (same session,
  committed with v0.2 at 4b942a2 before this seal) and were reproduced
  independently by the R-IND-5 verifier's own solvers. The R-IND-5 pass
  was FRESH-CONTEXT (independent agent), unlike 086's disclosed
  self-audit.
amendments: []
```

## What this registration does not claim

No novelty is claimed here (the flank record
`paper/GO16-NOVELTY-FLANK.md` governs posture: SDP machinery imported,
partition/pricing/water-level/tie-iff headlined pending the quote-level
sweep). It does not claim the general-scope converse (Conjecture 1),
the fixed-instrument commitment gap, or anything about the discrete
twin (091's object). A pass nets Theorems 1–3 + corollaries at their
stated scopes for [predicted]-grade citation.
