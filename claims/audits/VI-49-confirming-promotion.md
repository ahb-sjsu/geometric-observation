# VI-49: confirming pass on VI-48's dispositions, and Cor 4 joining PAPER-V.b (2026-11-21)

**Target.** The promotion drafts after VI-48 (commit 2 of 2), and the material of commit 1
(235ba32), which landed while this pass ran:
- the rate identity of `lem:maxdet` joining ledger row PAPER-III.a;
- PAPER-III.b, scoped to the variance formula of `cor:dispersion`, becoming `[proved]`;
- **new and never reviewed before:** Paper V's Corollary 4 joining PAPER-V.b, netted by Paper
  III's rate-identity harness;
- the run account, the VI-48 record, the custody files, the ledger rows, FRONTIER, the README
  and Appendices B, D and F and Chapter 7.

**Verifier.** A fresh-context general-purpose agent, local files only, with no browser,
connector or network tools and no access to the assistant's verdict. It also read Polyanskiy
and Wu's notes, as downloaded with the author's permission. Its checks:
- **re-ran version 2 of the net** in a scratch copy: 12.9 s, ALL PASS, JSON identical apart from
  the timestamp and git fields, hash matching;
- **regenerated the channels** and recomputed every figure the run account and custody files
  quote;
- **ran its own mutants:** a lowered formula, and a rotation by 0.001;
- **read Polyanskiy and Wu's Theorems 23.2–23.4 and 24.1–24.2** at the source (ch. 24,
  pp. 246–250).

**Verdict.**
- **No false mathematics; 0 errors.** With no error, the round has converged.
- **The rate identity can join PAPER-III.a,** once a green GitHub run is cited and the
  "identity" labels are corrected.
- **PAPER-III.b, scoped to the variance formula, can become `[proved]`.** Every clause left has a
  check that can fail on it, apart from the disclosed arithmetic bounds.
- **Cor 4 can join PAPER-V.b only as a single-letter statement, scoped to Σ_X ≻ 0.** Its clause
  "which are also the operational minima" should not enter the row at `[proved]`.
- **Counts:** 1 overclaim, 5 gaps and exposition items.

## Findings and dispositions (applied 2026-11-21)

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | OVERCLAIM | Cor 4's operational clause. The paper's written proof takes the L-step through the per-code converse (PAPER-V.c); the route through Polyanskiy–Wu alone exists only in the custody file. No check can fail on it, since CL's random codes stay at least 6.1% above the optimum. The same operational content is book B1 and Paper III's `thm:coding`, both `[exploratory]`. VI-41's accepted split framed row (b) as single-letter statements. | **Removed from the row.** It is recorded under "Not claimed", as an imported reading checked at the source, with what would bring it in: a rule from the author, applied to B1 too. |
| 2 | GAP | The custody file's converse chain omitted the continuity of φ (Polyanskiy–Wu Thm 23.3(2)), needed to pass from the codes' D_n to D. | Added to the "Not claimed" note. |
| 3 | GAP | "The same identity" fails for singular Σ_X. Paper V does not assume Σ_X ≻ 0, while `lem:maxdet` does and the net draws only positive definite covariances. Units, eigenvalue sets and L = R were confirmed to match. | Cor 4's row is scoped to Σ_X ≻ 0. The singular case is listed as proved but not netted. |
| 4 | GAP (consistency) | The achievability checks were called "identities", but a self-consistent lowered formula (water level ×1.001, median 5e-4 lower) fails r3's optimum check at 1.5e-3 and r4's trace check at 1e-3. PAPER-V.b's custody file described the feasibility test without any caveat. | Relabelled everywhere: they pass trivially for the correct formula but guard against one that is too low. Achievability rests on the proof. A lowered-formula gate is owed in version 3. PAPER-V.b now carries the caveat. |
| 5 | GAP (procedure) | Commit 1's VI-48 row says the scoping was applied, but the committed PAPER-III.b row is still unscoped. No green GitHub run of the net is cited. | Commit 2 lands the scoping. The GitHub run is cited in the custody file and the ledger once it is green. |
| 6 | GAP (the author's words) | PAPER-V.b's custody file said "This is row (b) of that split" without quoting VI-41's text for row (b). | VI-41's text is quoted ("(b) Props 3–4 as single-letter statements … Cor 4 joins them once it has a net that is not circular"). The custody file says the operational clause was not put to the author. |
| 7 | exposition | Several items: the README and FRONTIER called PAPER-V.b "(Props 3–4)"; the README's trailing "VI-41)" attached to the new claim; PAPER-III.a still called PAPER-III.b "the dispersion formula"; the B7 incident columns omitted VI-48; a `lem:info` row cited (42) as its definition; Cor 4's hypothesis 0 < D < Σλ_i was missing; the `lem:info` resolution was stated in two inconsistent measures; the run account omitted r5(a)'s random-Gaussian catch, and quoted the median of 0.31 without saying it excludes trivial channels; the record of the assistant's own reading of Theorems 23.2 and 24.1 was missing. | All fixed. The factor measure (about 1.11 and 1.26) is used throughout. The custody file records the assistant's reading of Definition 23.1 and Theorems 23.2, 23.3 and 24.1–24.4 on 2026-11-21. |
| 8 | exposition | The net's power is thin per instance: a rotation by 0.001 (median excess 3.4e-7) is caught on only 2 of 120 instances, though that still fails the verdict. | Recorded in the run account and in PAPER-III.a. Version 3 owes counts per instance. |

**Confirmed right by the verifier:**
- the re-run and the hash;
- the regenerated figures:
  - slack/I of 0.101 and 0.207;
  - informative slacks of 0.0050 and 0.0142;
  - the 18/4 split, with 2 + 4 trivial channels;
  - formula-independent catches of (c) on 5 instances and (d) on 2;
- every custody value in PAPER-III.a, PAPER-III.b and PAPER-V.b, including the CL log's 6869;
- VI-48's dispositions #1 to #9, apart from the points above;
- that PAPER-III.b rests only on PAPER-III.a and on Kostina–Verdú's Def. 6 and Property 2,
  which were checked at the source (VI-38);
- that Polyanskiy and Wu's Theorems 23.2–23.4 and 24.1–24.2 say what the records say;
- the CI file mode's logic;
- no stale text.

**Not checked:**
- the GitHub CI run;
- `pe_lint`, the LaTeX builds and `check_custody.py`;
- VI-48's mutant code;
- Kostina–Verdú at the source;
- the author's original messages;
- pages 251–255 of chapter 24.
