# GO-P-2026-086 — per-cell convexity: REFUTED after the first cell, and a theorem at the first cell

Resolves the open item `rem:percell` / open-problems (2). Probe and
R-IND-5 record in `paper/go14-causal-erasure-PROBE.md`; the remark is
rewritten in the tex to state the refutation.

**WHAT IS REFUTED.** Theorem C (079) proves n·L_a jointly convex in
(H,Γ) only in **regrouped** form — the block bracket plus the S-side
leak sum. The **individual per-cell CMI terms are not convex** in
(H,Γ). Analytic reason: 2ln2·f_t = ln vnum_t − ln vden_t with
vnum_t = Var(Ŷ_t | S^{se(t)}, Ŷ^{t−1}) and
vden_t = Var(Ŷ_t | W, Ŷ^{t−1}) **both concave** (infima of affine), so
f_t is a convex leg plus a concave leg — a competition, not a sign.

**WHAT IS PROVED.** **Cell t = 0 is convex and was never open.** With no
Ŷ^{t−1} to condition on it collapses *exactly* to the block bracket in
scalar form with a truncated Q:
f_0 = ½log₂[(Γ₀₀ − h₀Q_k h₀ᵀ)/(Γ₀₀ − h₀P h₀ᵀ)],
Q_k = K_[k]ᵀ Σ_{S,[k]}⁻¹ K_[k] — an algebraic rearrangement, so its
convexity is the **074 lift's scalar case** and needs no new argument.

**WHAT IS UNTOUCHED, AND GATED AS SUCH.** Theorem C, Theorem R1, the 079
certificates and the 082/083/084/085 chain. s7 gates it: at the very same
witness pair the **total** n·L_a is convex (gap −3.268e−01), because the
neighbouring cells absorb the concave one. The mass that makes a late cell
concave is precisely what the regrouping moves into the leak sum. **No
result in the document uses a per-cell statement** — the only other mention
is the open-problems list (tex l.4028).

**SCOPE THAT MUST TRAVEL.** 𝒟 = {(H,Γ): Γ − HΣ_W⁻¹Hᵀ ⪰ 0} (tex l.504) is
the full convex cone and 𝓕₀ (hyp:uind) imposes **no triangularity**, so
every witness point is a genuine 𝓕₀ record via A = HP,
N_cov = Γ − HPHᵀ. The refutation additionally holds **inside the causal
class**: {H : HP lower-triangular} is a *linear* subspace, so midpoints stay
causal and a violation there is a violation on 𝒟.

Governs `experiments/go14_percell.py` (numpy/scipy + stdlib
fractions/decimal, CPU, single run; sentinel `===GO14PC-JSON===` with
`===END===`; flag `GO14PC_supported`).

```yaml
id: GO-P-2026-086
date: 2026-08-08
retrospective: false
kind: theorem-verification (C3 net for a REFUTATION plus the cell-0 theorem; probe + R-IND-5 on record)
claim: "The individual per-cell CMI terms of n L_a are NOT convex in (H,Gamma)
  for any cell t >= 1, exhibited by a pinned Jensen witness of three points of
  int D whose exact midpoint is the base point; and cell t = 0 IS convex,
  because it collapses exactly to the block bracket in scalar form with a
  truncated Q_k, i.e. the 074 lift's scalar case. Theorem C is untouched and
  the same witness pair gates it: the TOTAL n L_a remains convex there."
harness: experiments/go14_percell.py   # GOVERNED seed 20261191; pilot seed 20261190, disclosed below
power: |
  Deterministic gates. NO optimizer, fixed point or root find anywhere in
  the file, so no gate can race a solver (the 079 lesson). Every base
  point is either a pinned literal or drawn from an INTERNALLY PINNED
  generator, so pilot and governed payloads are bit-identical apart from
  the seed stamp and pilot flag. Margins: s1 identity 4.0e-15 against
  1e-10 (25000x); s2 gap 6.9516e-2 against 6.9e-2 (1.007x -- deliberately
  tight, it is a committed-value reproduction, and the committed-value
  gate carries it at 2.99e-11 vs 5e-10, 17x); s2 feasibility 7.71e-2
  against 1e-3 (77x); s3 route spread 4.4e-16 against 1e-12 (2200x);
  s4 exact-vs-float64 4.35e-17 against 1e-12 (23000x); s5 identity
  8.9e-16 against 1e-12 (1100x), eigmin(P-Qk) 2.74e-2 against 1e-3 (27x);
  s6 worst t>=1 curvature -3.76 against -0.5 (7.5x), cell-0 -1.0e-15
  against -1e-8 (1e7x); s7 total gap -0.327 against -1e-3 (327x),
  random-pair rate 0.250% against 2% (8x).
pilot: |
  THREE runs, seed 20261190, ALL DISCLOSED.
  iter 1 -- CRASH, not a gate failure: numpy 2.x returns
    'np.float64(...)' from repr(), which Decimal cannot parse. A code
    defect in the s4 comparison; no measurement involved.
  iter 2 -- 15/16, and THE ONE FAILURE WAS A MIS-SPECIFIED GATE OF MINE,
    which the pilot did its job in catching. s7 originally asserted that
    random-pair sampling has ZERO power, taking rem:percell's "no
    violation was found in any sampling ... zero hits" at face value.
    **THAT IS FALSE**: random per-cell pairs violate at 10/4000 = 0.250%
    with worst gap +4.546e-02 -- real violations, not threshold noise.
    A 45k per-cell sweep would therefore have produced of order a hundred
    hits, so whatever sampling produced the "zero hits" note cannot have
    been per-cell pairs of this kind (the 079 harness gates the TOTAL and
    the two REGROUPED pieces, and records per-cell as explicitly NOT
    gated). The gate was REPLACED by two correctly-specified ones: that
    random sampling DOES violate (so the historical note does not
    reproduce) and that its rate is nonetheless low (so sampling is the
    wrong instrument, not a powerless one). **NO OTHER BAR WAS TOUCHED,
    IN EITHER DIRECTION, AND NO MEASUREMENT MOVED.** A second code defect
    (np.bool_ not JSON-serialisable) was fixed in the same iteration.
  iter 3 -- ALL PASS 17/17, 351 s.
  **CONSEQUENT CORRECTION TO THE DOCUMENT**: the tex remark and PROBE.md
  had both attributed the historical null to random pairs being generic.
  That explanation is RETRACTED in both, before this seal, and replaced
  by the measured statement above. The refutation itself never depended
  on it.
prediction:
  s1_object: the per-cell terms sum to the 4n-joint per-cell CMI and to the
    REGROUPED Theorem-R form, < 1e-10 over 108 points (n = 3,4,5 x
    Delta = 0,1,2)
  s2_witness: the pinned triple reproduces its committed values (< 5e-10),
    the Jensen gap at cell 2 EXCEEDS +6.9e-2 THE WRONG WAY, all three
    points are strictly interior (eigmin N_cov > 1e-3), and the midpoint
    is exact (< 1e-15)
  s3_routes: the moment form, the 4n-joint form and a pure log-det form
    agree to < 1e-12, and ALL THREE show the violation
  s4_exact: EXACT rational conditional variances with a 60-digit log
    confirm the gap > 0.069 and match float64 to < 1e-12
  s5_cell0: the scalar-bracket identity holds to < 1e-12 over 180 points
    and 0 <= Q_k < P with eigmin(P - Q_k) > 1e-3
  s6_grid: every cell t >= 1 admits curvature < -0.5 at every (n, Delta)
    in the grid; AND THE CONTROL -- cell 0 NEVER does (min eig >= -1e-8)
  s7_scope: the TOTAL n L_a is CONVEX at the witness pair (gap < -1e-3);
    AND random-pair sampling DOES violate (>= 1 hit, worst > 1e-3) while
    its rate stays < 2%
falsification: s1 fail means the probe measured a lookalike, not the
  document's object, and nothing else here counts; s2/s3/s4 fail refute
  the witness itself (and s4 failing while s2 passes would mean the
  violation is a floating-point artifact); s5 fail refutes the cell-0
  theorem; s6's control failing -- cell 0 showing concavity -- would mean
  the refutation is a bug affecting every cell rather than a statement
  about conditioning; s7 fail would mean the machinery contradicts
  Theorem C, which would refute this registration and not Theorem C.
  Single governed run, no silent reruns.
design:
  stopping: fixed design, single governed run, seed 20261191, after the
    disclosed three-run pilot (seed 20261190); no further pilots or
    attempts under this ID
  runtime: ~6 min single-threaded (pilot iter 3: 351 s)
controls: [the cell-0 must-not-violate control of s6 -- which gates that
  the refutation is about conditioning and not a bug; the Theorem-C
  does-not-prove-too-much control of s7; the random-pair rate control of
  s7, which REFUTES the recorded "zero hits" rather than confirming it;
  the three-route agreement of s3; the exact-arithmetic confirmation of s4]
provenance: |
  THE WITNESSES WERE FOUND ON 2026-08-08, BEFORE THIS HARNESS EXISTED
  (PROBE.md). Every witness gate here is COMMITTED-VALUE REPRODUCTION,
  not discovery; nothing in the file searches. The R-IND-5 pass on the
  refutation was run in the SAME context that produced it, NOT by a
  fresh-context verifier -- it is recorded as a self-audit in PROBE.md,
  and this seal does not claim otherwise.
amendments: []
hash: sha256:bb075c246bb4c4cf442b3a4d5439a3b7fac063265e941d794af8fd4324cf82cc
```

## Falsification

A pass nets the refutation of per-cell convexity for every cell t ≥ 1,
the cell-0 theorem, and the scope statement that Theorem C is untouched.
A failure of s1 would mean the object measured is not the document's
per-cell CMI, in which case nothing else in the registration counts. A
failure of s6's cell-0 control would mean the refutation is a defect
affecting all cells rather than a statement about the Ŷ^{t−1}
conditioning. A failure of s7 would refute **this registration**, not
Theorem C.

## What this registration does not claim

It does not claim novelty for anything: cell 0 is the 074 lift's scalar
case, and a Jensen counterexample is not a new technique. It does not
touch Theorem C, Theorem R1, the 079 certificates or the
082/083/084/085 chain. It does not claim that the recorded "zero hits"
was wrong about whatever it actually sampled — only that per-cell random
pairs violate at 0.250%, so that record does not reproduce for this
object.
