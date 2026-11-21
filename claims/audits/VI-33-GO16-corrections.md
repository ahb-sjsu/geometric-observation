# VI-33: R-IND-5 re-check of the GO-16 corrections (2026-11-20)

**Target.** The corrections made after VI-30 and VI-31 to
`paper/go16-adversarial-observer.tex`:
- Theorem 3, rewritten with the blackout regime;
- Theorem 4(ii)–(iv);
- Theorems 5 and 6;
- the corollaries, title block and abstract.

The pass also covered the new net `experiments/verify_go16_diagonal.py` and the revised gates
of `experiments/go16_theory_extensions.py` (S1, S2).

**Verifier.** A fresh-context general-purpose agent, working from local files only. It ran its
own primal–dual LP check over 3000 instances, 517 of them with constructed flat stretches of
J, and found **0 violations** of the tie characterization, of "the diagonal optima are
exactly ρ(t*)", or of any attention claim.

**Verdict.** The corrected Theorem 3 core is right, once λ > 0 is assumed. The counts are 3
errors, 3 gaps, 4 overclaims and 8 exposition items; all errors are in new or unchanged
sentences around the core, not in the core itself.

## Findings and dispositions (all applied, 2026-11-20)

| # | Severity | Finding | Applied |
|---|---|---|---|
| E1 | error | "The optimum is not unique when the interval is nondegenerate" is false. The theorem's own integral example has J flat on [1.8, 2.5] with ρ = (1, 1, 1) throughout. | Now reads: unique iff ρ(t) is constant on the minimizer interval, that is, iff the interval is a point or no i ∈ S has μ_i above its left endpoint. |
| E2 | error | "θ_j ∈ (0, 1) in the fractional regime" is false at the ends of flat stretches (VI-30's N2 instance forces θ₃ = 0). | Now θ_j = J′(μ_j+)/λ ∈ [0, min(1, s_j²/(λμ_j))], interior unless t* ends a flat stretch, with the example. I re-derived it from J′(μ_j−) ≤ 0 ≤ J′(μ_j+). |
| E3 | error | The poker remark says mixing happens "only" on contested coordinates. The blackout regime and level coordinates contradict that. | Remark rewritten: contested coordinates are part of the mixing support, not all of it. |
| G1 | gap | λ > 0 was never stated. At λ = 0 the iff fails. | λ > 0 added to Theorem 3. |
| G2 | gap | The contested condition covers S at t* = 0. | t* > 0 added. |
| G3 | gap | The net had no reader-side check, and no check of the ⊆ half of "exactly". | d5 added: LP-dual attention claims. d6 added: the LP's vertex lies in the ρ(t*) family. Flat stretches are scoped to the verifier's run. |
| O1 | overclaim | The abstract's "R-IND-5 pass complete — core intact" is stale. | Qualified, and points to VI-30/NEG-17. |
| O2 | overclaim | The novelty and gates section still headlines "tie-iff-contested" and calls the gate "cleared, verified, governed". | Corrected: the gate is not cleared, 090 governs the refuted statement, and the corrected Theorem 3 is ungoverned. The v0.4 title line is qualified the same way. |
| O3 | overclaim | The netting claims (KKT bookkeeping "harness-netted"; the water-level and Theorem 6 assembly "netted by S1–S3 plus 090/091") are false. | Both withdrawn in the text. |
| O4 | overclaim | Corollary 1's "demands fractional revelation whenever a coordinate is contested" fails at J′(0+) = 0. | Now "exactly when it has a contested coordinate", noting that blackout and contested optima coexist when J′(0+) = 0. |

**Exposition, ten items (all applied; this heading said "X1–X8" until VI-35 counted the bullets, 2026-11-21):**
- "Every saddle W* has a fractional entry on S", with the PSD-block reason.
- Undefined "fractional/integral regime" references replaced.
- Theorem 6: q_i defined; the reader strategy set of case (b) named; 4.88 vs 3.50 cited.
- Theorem 4(iii): D(t) defined.
- The `frontier_attained` coverage scoped.
- The verification paragraph now describes the S1/S2 gates and the new net, and says that
  `go16_theory_extensions.py` is not in CI.
- The date bumped to v0.6.
- The V9b numbers attributed to their seeds.
- The abstract's "pinned" scoped to contested coordinates.
- The second Lean module carries the not-re-checked caveat.

## Net results after the changes

| Net | Result |
|---|---|
| `verify_go16_diagonal.py` | 6/6 PASS on 601 instances: value against exact LP 1.4e-15; blackout condition; tie characterization; sealed statement violated on every blackout optimum; attention duals; LP vertex in family |
| `go16_theory_extensions.py` S1 | 0.6896 vs closed form 0.6944 |
| `go16_theory_extensions.py` S2 | no encoder below V* (1.749999999999 vs 7/4; 4.052777777957 vs 4.052777777778) |
| `go16_theory_extensions.py` S3 | exact identities |

## Still owed before `[proved]`

- A confirming fresh pass on this round's changes. They are small, and the verifier's own
  primal–dual run already covers the core numerically.
- A net for Theorem 5's blackout regime at rotated scope.
- Custody tables.
- **The corrected Theorem 3 is ungoverned.** 090 governs only the refuted sealed statement.
