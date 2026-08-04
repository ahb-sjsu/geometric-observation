# GO-P-2026-068 — GO-13 Theorem 2: the tax-curve characterization (envelope sign law)

Second GO-13 registration. Settles the open object left by 067: which
regimes make staleness raise, lower, or leave the dynamic tax.

**The theorem under net.** Envelope (Danskin) derivatives of the
weighted coordinates in the access parameter q:
dJ/dq = (1−w)/(2ln2)·(Ac)ᵀM₁⁻¹(Ac) for the joint 2-D record and
dL_i/dq = (1−w)/(2ln2)·(uᵀc)²/(Q₁+n) per consumer, at the optimal
channels. Away from the max-switch locus the tax obeys the SIGN LAW:
dCT_W/dq = (1−w)/(2ln2)·[(Ac)ᵀM₁⁻¹(Ac) − binding-consumer
sensitivity] — staleness raises the tax iff the joint record's
context coupling in the M₁⁻¹ metric exceeds the binding consumer's.
At the max-switch locus (L_A = L_B) the curve is continuous with a
kink of magnitude (1−w)/(2ln2)·|s_A − s_B|. At w = 1 the curve is
exactly flat. This registration also nets the 067 clarification: at
the 067 pilot instance the max-based tax RISES (dCT = +0.177) while
the A-referenced difference is near-flat (−0.0007) — the sealed s4
label imprecision, now instrumented.

Governs `experiments/go13_taxcurve.py` (numpy+scipy, single run;
sentinel `===GO13TC-JSON===` with `===END===`; flag `GO13TC_supported`).

```yaml
id: GO-P-2026-068
date: 2026-08-05
retrospective: false
kind: theorem-verification (C3 numerical falsification of an R-IND-5-verified analytic result)
claim: "GO-13 Theorem 2: the dynamic tax's q-derivative is the
  envelope difference (1-w)/(2ln2)[(Ac)'M1^{-1}(Ac) - binding-consumer
  sensitivity] -- staleness raises the tax iff the joint record's
  context coupling exceeds the binding consumer's -- with a
  max-switch kink of magnitude (1-w)/(2ln2)|s_A - s_B| and exact
  flatness at w=1; the 067 pilot instance's max-based tax rises while
  its A-referenced difference is near-flat."
harness: experiments/go13_taxcurve.py   # GOVERNED seed 20260924; pilot seed 20260923, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the
  bars carry pilot margins: s1 envelope-vs-FD bar 5e-4 vs pilot
  3.5e-9 (~1e5x), both-signs requirement satisfied (3 up, 1 down);
  s2 gates dCT_max > 0.05 vs 0.177 (3.5x) and |dCT_Aref| < 0.05 vs
  0.0007 (70x margin inside); s3 kink bracket (0.05, 0.6) vs q* =
  0.1084, magnitude bar 1e-4 vs 0.4608; s4 w=1 bar 1e-5 vs 1.8e-11.
  Every margin >= 1.3x.
pilot: |
  ONE pilot, seed 20260923, full harness, 43.5 s: ALL PASS with
  drafted bars unchanged (zero bar recalibrations). Values: envelope
  3.5e-9; signs [+,+,-,+]; binding consumer B confirmed, dCT_max
  +0.1772 vs dCT_Aref -0.0007; q* = 0.10843 (independently matching
  the R-IND-5 verifier's ~0.11 kink locus), kink magnitude 0.4608;
  w=1 slope 1.8e-11. R-IND-5 pass completed pre-seal (see amendments
  for any wording-driven notes; harness computationally unchanged
  from the piloted version unless amended).
prediction:
  s1_envelope: |envelope - central FD| <= 5e-4 for the joint and
    binding-consumer derivatives at four instances; dCT signs must
    include both positive and negative
  s2_disambiguation: at (r=(0.3,0.7,0.2), D=(0.2,0.2), w=0.5, q=0.5)
    the binding consumer is B, dCT_max > 0.05, |dCT_Aref| < 0.05
  s3_kink: a max-switch q* exists in (0.05, 0.6) on the
    (0.3,0.7,0.2)/(0.25,0.35)/w=0.25 instance with kink magnitude
    > 1e-4
  s4_w1_flat: |dJ/dq| at w=1 <= 1e-5
falsification: s1 refutes the envelope formulas (or Danskin
  applicability); s2 refutes the sign law or the 067 clarification;
  s3 refutes the kink structure; s4 refutes the (1-w) factor.
  Instrument-vs-physics per PROTOCOL 5.1: SLSQP non-convergence or a
  brentq bracket failure is a logged instrumentation miss
  (dated-amendment rerun only).
design:
  stopping: fixed design, single governed run, seed 20260924, after
    the one disclosed pilot (seed 20260923); no further pilots or
    attempts under this ID
  runtime: ~45 s single-threaded (pilot: 43.5 s)
controls: [both-signs requirement (s1), max-vs-A-reference paired
  disambiguation at the sealed 067 instance (s2), independent kink
  locus vs the verifier's (s3), exact w=1 zero (s4)]
amendments: []
hash: sha256:16b537c9284aa649b59e71861c5e920c7c268ca24046d8b66e3edde1fd6df241
```

## Falsification

A pass makes GO-13 Theorem 2 citable at `[predicted]`-grade: the
dynamic tax's response to staleness is exactly characterized by the
envelope sign law, closing the question the 067 verifier opened.
