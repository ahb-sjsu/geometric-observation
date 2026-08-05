# GO-P-2026-067 — GO-13 Theorem 1: the matrix-q reduction and access-class universality of the dynamic tax

First GO-13 registration. Settles Conjecture 1 of the problem statement
(`paper/go13-dynamic-tax.tex`) and nets the equal-q universality
control plus the q→1 endpoint of Conjecture 2.

**The theorem under net.** For m=2 single-letter records with the
conditional-independence embedding (reads touch the context process
only through V_t): any observation-subset σ-algebra G enters all
coordinates only through Σ_{T|G} = Σ_T − (1−q_G)·cc′ (c = Cov(T,V_t),
q_G = Var(V_t|G)) — Theorem 9's program evaluated at (Σ_T, Σ_{T|G}).
Hence for scalar context every coordinate and both taxes are functions
of q_G alone: **equal-q access classes give identical coordinates and
identical taxes**. Coordinates are nondecreasing in q_G (pointwise
log-det Loewner argument); at q_G → 1 conditional coordinates converge
to the marginal program, so CT_W → CT_R. The tax curve itself is
REPORTED, not gated. R-IND-5 pre-seal verdict on the curve: the pilot
instance's near-invariant decreasing curve is INSTANCE-SPECIFIC, not
generic — the verifier exhibited a regime with the tax monotone
INCREASING by 0.16 nats and another with a non-monotone kink exactly
where argmax(L_A, L_B) switches consumers. Conjecture 2's monotone
clause is thereby refuted in general; what this registration nets is
the reduction, universality (scalar context, subset-of-{S_s} access,
CI embedding, w∈[0,1] — all stated hypotheses per the verifier's
sharpenings), weak coordinate monotonicity, and the q→1 endpoint
(continuity via concavity of the value in q).

Governs `experiments/go13_matrixq.py` (numpy+scipy, single run;
sentinel `===GO13MQ-JSON===` with `===END===`; flag `GO13MQ_supported`).

```yaml
id: GO-P-2026-067
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of an R-IND-5-verified analytic result)
claim: "GO-13 Theorem 1: the m=2 coordinates depend on the eraser's
  observation-subset sigma-algebra only through Sigma_{T|G} = Sigma_T
  - (1-q_G) cc' (matrix-q reduction; Theorem 9's program at the
  conditional pair), so with scalar context all coordinates and both
  taxes are functions of q_G alone -- equal-q access classes give
  identical taxes -- with coordinates nondecreasing in q_G and
  CT_W -> CT_R at q_G -> 1."
harness: experiments/go13_matrixq.py   # GOVERNED seed 20260921; pilot seed 20260920, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the bars
  carry pilot margins: s1 reduction bar 1e-6 vs pilot 6.7e-15; s2
  universality bar 1e-6 vs 6.7e-15; s3 endpoint bar 1e-4 vs 1.4e-7
  (700x) with weak-monotonicity gate; s4 tax-endpoint bar 1e-3 vs
  3.0e-10. Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20260920, full harness, 22.3 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: s1
  6.7e-15 over slice/prefix/gapped-straddle classes; s2 6.7e-15
  (slice tau2=0.4 vs prefix tuned to tau2=5.4589 at equal q=0.7074);
  s3 monotone, endpoint 1.4e-7; s4 tax endpoint 3.0e-10; reported tax
  curve monotone DECREASING 1.09345 -> 1.09293 = CT_R (amplitude
  <5e-4 bits -- near-invariance, exploratory). R-IND-5 pass completed
  pre-seal; harness computationally unchanged from the piloted
  version (see amendments if any wording-driven edits).
prediction:
  s1_reduction: program at (Sigma_T, Sigma_{T|G}) matches direct
    optimization conditioning on the actual S-set to 1e-6, on slice
    [+2], prefix [-25..+2], and straddle [-1,+3] classes
  s2_universality: two access classes tuned to equal q agree to 1e-6
  s3_mono_endpoint: L_AB nondecreasing over q in {0.2, 0.6, 0.95,
    ~1}; q->1 value within 1e-4 of the marginal program
  s4_tax_endpoint: |CT_W(q~1) - CT_R| <= 1e-3; full tax curve
    reported (not gated)
falsification: s1 refutes the matrix-q reduction; s2 refutes
  access-class universality (and hence the r=1 corollary of the
  reduction); s3 refutes coordinate monotonicity or the endpoint; s4
  refutes the CT_W -> CT_R convergence. Instrument-vs-physics per
  PROTOCOL 5.1: SLSQP non-convergence is a logged instrumentation
  miss (dated-amendment rerun only).
design:
  stopping: fixed design, single governed run, seed 20260921, after
    the one disclosed pilot (seed 20260920); no further pilots or
    attempts under this ID
  runtime: ~25 s single-threaded (pilot: 22.3 s)
controls: [gapped-straddle access class (s1), equal-q tuning across
  DIFFERENT class types (s2), marginal-program endpoint anchor (s3),
  tax curve reported unaged so Conjecture 2 stays falsifiable by a
  future registration rather than absorbed here (s4)]
amendments:
  - date: 2026-08-05
    what: "Defensive numerical guard added to the harness objective
      (det <= 1e-280 -> penalty 90.0, the 064-lineage convention that
      was omitted here): the CI runner's scipy walked SLSQP through a
      degenerate probe our local runs never visited, crashing with a
      math domain error at the 070 seal-commit CI run. The guard
      cannot alter any finite objective value; reruns under the
      governed seed reproduce the sealed artifact's values and
      verdicts BIT-IDENTICALLY (checked field-by-field). No bar, seed,
      gate, or measurement path changed. Prior hash: d3d5cde8d724431a4a2e418b28a30c3beffe95c90f4bc2c5c52f4cf5202732ae"
hash: sha256:d7cddf7913dd8ae61638033ed865df739fd07a4adb1ff0bd5f0c609dc1d0748c
```

## Falsification

A pass makes GO-13 Theorem 1 citable at `[predicted]`-grade and
converts the problem statement's Conjecture 1 to a settled theorem
with the universality clause of Conjecture 2 proven; the monotone
near-invariance of the tax curve remains open for a dedicated
registration.
