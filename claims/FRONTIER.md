# Frontier register: what is still open in Observation Theory

This file tracks every open item on the programme's frontier. Each item has its own row
and ends in exactly one of four states:

- **Proved:** CHARTER T-CUST-1 is met (written proof, logged R-IND-5 pass, CI-run C3
  harness, custody table). The row is `[proved]`.
- **Netted:** a sealed registration passed its gates. The row is `[predicted]`, or
  `[demonstrated]` for an operational face.
- **Refuted:** a counterexample, certified exactly and checked by a fresh context.
- **Scoped-open:** a written obstruction, checked by a fresh context. It records what was
  tried, why each route fails, and the sharpest true statement short of the target.

[`LEDGER.md`](LEDGER.md) remains the record of claims. This file only says what is still
owed and where it stands. Opened 2026-11-20, when the owner set the scope to three lists:

1. the open items in the GO-12 to GO-16 rows and in T1;
2. Paper III's open problems and two conjectures from book Ch. 17;
3. the grade gap.

**Legend.**

- **Tract.:** (a) standard tools; (b) research with an uncertain outcome; (c) blocked.
- **Box:** the time box, in working sessions. a = 1, M = 3, L = 6. When it expires without
  a result, the obstruction is written up and the item becomes scoped-open.
- **Track:** P leads to `[proved]` with no seal. N is a sealed registration, which the owner
  reads before it is sealed.
- **State codes:**
  - `open`: not started;
  - `active`: work has started;
  - `pending-custody`: proof done, `[proved]` pieces missing;
  - `owner`: waiting on the owner;
  - `named`: tracked, not being chased.

## List 3 — the grade gap (first `[proved]` rows, 2026-11-21: PAPER-III.a, PAPER-V.a, PAPER-V.b)

The `[proved]` bar has four parts (CHARTER T-CUST-1):
- a complete proof;
- a logged R-IND-5 pass;
- a C3 harness that is committed, CI-run and built to fail;
- a custody table of constants, slack and known gaps.

| ID | Item | Source | State | Missing pieces | Kill criterion |
|---|---|---|---|---|---|
| G1 | RLD-I (Thms 3, 7, 20) | `paper/tit-rate-leakage` | active | R-IND-5 done: **VI-27**, no false step; the ledger row is narrowed; the paper's items go to the owner, since it is under review. Nets added and in CI (**VI-29**, two rounds): `verify_rld1_lemma1.py` (Lemma 1, Prop 2's identity) and `verify_rld1_turning.py` (Theorem 20). Still owed: a net for Theorem 3's achievability (the coding argument); the Lean–statement correspondence for Theorem 7; CI wiring of the paper's own scripts (they exit 0 on failure); custody. **The owner sets the class** | a pass finds an error: report to the owner, the row stays |
| G2 | RLD-II (Thms 4, 16, 20, 22, 23) | `paper/tit-stationary` | pending-custody | CI net; custody (VI-16 on record) | same |
| G3 | RLD-III.1–5 (Thms 13; 18; 2, 3, 5; Cor 6; 26) | `paper/tit-beyond-stationary` | pending-custody | CI net; custody (VI-17) | same |
| G4 | RLD-IV.1, .2, .4 (Thms 1, 10; 11; 18) | `paper/tit-unstable-ergodic` | pending-custody | CI net; custody (VI-18–21) | same |
| G5 | RLD-IV.3 (Thm 13, Prop 14, Cor 15) | same | active | R-IND-5 done: **VI-26**, three fresh-context passes (the original text and two rewrites), no false step; all findings applied to the draft; Tan–Dabora–Poor checked at the source; the harness strengthened (power control, exact example). Still owed: CI wiring; custody | same |
| G6 | T1 note v4.1 (Thms 5, 7, 11, Cor 8, Prop 12) | `paper/t1-learn-then-serve` | pending-custody | custody (VI-22–24); confirm `verify_t1_v4.py` runs in CI. The note is frozen until 092 is sealed | same |
| G7 | GO-12 theorems (065, 066, 070, 071) | `paper/go12-process-region.tex` | pending-custody | Records indexed as **VI-28**; since each record, the theorem text changed only cosmetically. All four nets are in CI's re-run tier. Owed: the custody table, after GO-11 (G16), which Theorem 1 imports | the diff shows unverified changes: fresh pass on those parts |
| G8 | GO-14 theorems (076–086) | `paper/go14-causal-erasure.tex` | pending-custody | index the F/W restatements and prereg records as VI rows; split the row so `[proved]` covers only proved statements; custody (079 sits in the committed-artifact tier) | same |
| G9 | GO-16 Thms 1–3 (090, 091) | `paper/go16-adversarial-observer.tex` | active | **VI-30, the re-check: Theorem 3 is FALSE as stated (NEG-17: blackout regime t* = 0 omitted; 090's "tie iff contested" refuted).** Theorems 1–2 hold at their scope, but with gaps (hypotheses Σ_S ≻ 0 and k ≤ n missing) and three overclaims (Corollaries 1–2, "must mix"). Owed: the corrected Theorem 3 (F16.0), the fixes, a new net with blackout and contested-empty instances, custody | the corrected Theorem 3 is false too: refuted |
| G10 | GO-16 Thms 4–6 (v0.5) | same | active | **VI-31: the core holds; Theorem 4(ii)'s equality clause is wrong** (correct: q₁ ≥ q₀ and (q₀+q₁ = 1 or q₀ = q₁)). **Theorem 6 holds for k = 1 only.** Theorem 4(iii)'s classes are not derived. Owed: the fixes, S2's gate made two-sided, an S1 gate against Theorem 5's closed form, a CI net, custody | a pass finds an error |
| G11 | The book's `[proved]` tags (Appendix B: B1, B4, B5, B7; Appendix F: the legibility theorems) | `chapters/appendix_b_cost_ledger.md`, `appendix_f_mathematical_ledger.md` | active | **VI-32, the custody pass: 4 errors** (the B7 dispersion constant, NEG-18; the book's B4 and B6 statements; Paper III's region omits Σ_f ≻ 0), 4 gaps, 5 overclaims (incl. VI-4's net, which cannot detect the bug it was built for); the book's B1–B3 do not match the paper's thm:B1–B3. **VI-36 and VI-37 (2026-11-21): all findings applied. Multi-observer achievability is now a named Assumption SR (Effros, unchecked; G12b), with converses unconditional; B4's max-det corner identity `[predicted]`-grade, its coding statements `[exploratory]`; Chapter 7 and Appendix A corrected; the net `verify_paper3_nets.py` at version 3, 7/7 on seed 20261126.** **VI-38 (2026-11-21): 3 errors** (Kostina–Verdú's restriction (iv) is a ninth moment, misread by the assistant, who had overruled VI-37's verifier with it; the refuted "Loewner nesting of read metrics" in six places; Chapter 7's tax), 2 gaps (m4's tolerance doubled undisclosed; the source checks were the assistant's own reading), 6 overclaims, 7 exposition; all applied. **VI-39 (2026-11-21): 1 error** (introduced: B4's statement dropped the corner rates), 4 gaps, 6 overclaims, 7 exposition, mostly older text; all applied except the author's IEEE package (reported). **VI-40: 1 error** (old text: Chapter 7's refinability without the corner rates), 2 gaps, 3 overclaims, 5 exposition; applied (one finding declined, then settled by VI-42). **VI-42: 0 errors**, 2 gaps, 1 overclaim, 5 exposition; applied. The text round has converged. **Net version 4 (2026-11-21): committed before its first run (57bccec); attempt 1 crashed at import (environment), attempt 2 passed 7/7 on seed 20261127; in CI's re-run tier; VI-45: 0 errors, its points disclosed in `results/PAPER3-nets-RUNS.md`, a version 5 owed.** **Custody and ledger rows (2026-11-21).** The author agreed that Paper III's netted results get a row of their own ("yes, I accept. Proceed as you recommend"); the classes follow T-CUST-1. **PAPER-III.a is `[proved]`**: the capped max-det closed form and the rate-loss corner step (custody file `claims/custody/PAPER-III.a.md`). VI-46 found the closed form asserted but never derived; the derivation, and the "only if" half of L = 0 iff nesting, were added to Paper III and read by VI-47 (0 errors; the round has converged). The split into PAPER-III.a and PAPER-III.b came after VI-46 and was not put to the author. **PAPER-III.b, the dispersion formula, is `[exploratory]`**: it rests on `lem:maxdet`'s rate identity, which nothing nets yet. Owed next: a net for that identity (Polyanskiy–Wu ch. 25, read 2026-11-21 with the author's permission, proves only the scalar case); B1 and B5's region converse, on which no net can fail yet; Assumption SR (Effros); net version 5. (Was: "Owed next: custody, and a ledger row scoped to what is proved".) Before that: **Corrections written and re-checked by VI-34** (2 errors: the corrected dispersion bound "<r" is false in the all-active regime; `cor:kobs` still stated $k\ge3$ achievability; 4 gaps, 4 overclaims, all applied): B5's region converse and B7's reduction retagged `[exploratory]` (no net can fail); GO-6 (B2/B3) disputed, class left to the author. Owed: new nets (max-det optimality, region coupling, dispersion with inactive modes and at $2V=r$), ledger rows, a confirming pass; the legibility custody audit in `the-angular-observer` | a missing piece: retag at the true class |
| G12 | Appendix B's `[C7]` flag on the B7 dispersion constants (T-CUST-3: flags never ship), and since VI-34 the hypotheses of Kostina–Verdú's general Gaussian approximation for the vector letter behind `cor:dispersion` | `appendix_b_cost_ledger.md` (VI-7 paragraph); `observation-theory.tex` `cor:dispersion` | **closed 2026-11-21**: checked at the source (arXiv:1102.3944) by the assistant (VI-36), then independently by VI-38, which corrected restriction (iv) to $\mathbb E[d^9]<\infty$ (the assistant had read a third moment): Theorem 12 holds for abstract alphabets, its restrictions (i)–(iv) and basic conditions (a)–(c) hold for the vector letter, the scalar constant is eq. (94); written into `cor:dispersion` and Appendices A and B. Was: open | check the scalar constant and the general theorem's hypotheses (unique optimal kernel, moment conditions) against Kostina–Verdú at the source, then remove the flag; a recollection that the formula matches Tian–Kostina's Gauss–Markov dispersion is unverified | the constants disagree with the source: fix and log |
| G12b | The successive-refinement achievability behind `thm:region` (k = 2), `cor:kobs` (k ≥ 3) and the sufficiency of nesting: Paper III cited Kostina–Tuncel as the coding theorem, but it is a two-stage characterization that cites Effros (IEEE T-IT 45(6), 1999) for the continuous-alphabet extension (VI-36) | `observation-theory.tex` §multiobs | open | check Effros at the source: whether it proves achievability for continuous alphabets with unbounded quadratic distortion, and for how many stages (Kostina–Tuncel cite it for two; the k ≥ 3 reading rests on its title, VI-38); settle too VI-5's contrary reading that "Effros gives bounds, not the tight region" (VI-39), and Rimoldi's L-stage form; its PDF is a file download, held for the author's permission | the hypotheses exclude the Gaussian quadratic case: prove achievability directly or rescope to the converse |
| G13 | Appendix F stops at GO-6 | `appendix_f_mathematical_ledger.md` | open | extend it through GO-16, RLD and T1 | — |
| G14 | Paper V theorems (the rate–work–distortion region; the Gaussian region with reset side information) | `paper/consumer-relative-landauer.tex` | active | VI-8 and VI-9 on record. **VI-41 (2026-11-21): no false step; a fire test (`fire_paper5_nets.py`, 18/18 gates) and the verifier's coverage table show which results a net can fail on.** Proposed split: (a) Lemma 1, Props 1, 2, 5, 6, Cor 2 and (b) Props 3–4 (after fixing their hypotheses) can reach `[proved]` with a custody table; (c) Thms 1, 3 and Cor 1 have no net that can fail; (d) Thm 2 and Cor 3 are identities, and **Cor 3 has no written proof** (at VI-41). **VI-43 (2026-11-21): the text fixes have no false step** (0 errors, 3 gaps, applied, #4 by rescoping with its citation owed: Cor 3's statement had omitted that consumer j reads M_j alone). **VI-44 (2026-11-21): confirming pass, 0 errors; the text round has converged.** Cor 3 now has a finite-blocklength proof; Thm 1's converse has its limit step; Prop 4 states its hypotheses; Cor 4 and Props 3–4 are statements about the single-letter region, with the converse proved for Gaussian sources and achievability with side information open. **The author accepted the split on 2026-11-21 ("yes, I accept. Proceed as you recommend"). Ledger rows PAPER-V.a (Lemma 1, Props 1, 2, 5, 6, Cor 2) and PAPER-V.b (Props 3–4) are `[proved]`, with custody files; PAPER-V.c (Thms 1, 3, Cor 1) and PAPER-V.d (Thm 2, Cor 3) are `[exploratory]`, (d) under the rule its row records.** **VI-46 (2026-11-21): no false mathematics; Cor 4's new proof is correct. VI-47: 0 errors; the round has converged.** **Citation (2026-11-21):** with the author's permission ("yes, download the Polyanskiy–Wu chapters"), the assistant read Theorem 24.2 of Polyanskiy and Wu's MIT 6.441 notes (2016) at the source, and Paper V now cites it for Cor 4's operational equality; VI-47 read it independently and found it sound. Owed: a non-circular net for Cor 4; nets on PAPER-V.c's converse steps and binning; the search net for Cor 3's independent-reset minimum. (Until 2026-11-21 the owed list also had the author's decision on the split and on (d), custody tables and ledger rows.) (Before VI-43 the owed list also had Cor 3's proof, the continuous-alphabet extension and Prop 4's hypotheses.) Was: VI-8 and VI-9 on record; nets in CI ([1c] `verify_consumer_landauer.py`, `verify_gaussian_sideinfo.py`); custody; a ledger row for the theorems | a pass finds an error |
| G15 | GO-10 theorems (the complementarity tax) | `paper/complementarity-tax.tex` | pending-custody | VI-10 on record (`paper/complementarity-tax-VERIFICATION.md`); net 055 in CI; custody | same |
| G16 | GO-11 theorems (Theorems 1–10) | `paper/go11-conditional-region.tex` | pending-custody | index the R-IND-5 records in `paper/go11-conditional-region-NOVELTY.md` (addenda) as VI rows, diffed against the current text; nets 060, 063, 064 in CI; custody | same |

**Order of promotion: bottom-up by dependency** (added 2026-11-20). A `[proved]` row may rest
only on `[proved]` rows or on external results checked at the source (T-CUST-3), so the
promotions go in this order:

1. G11, Paper III's B-theorems (rows PAPER-III.a and PAPER-III.b since 2026-11-21);
2. G14, Paper V;
3. G15 and G16, GO-10 and GO-11;
4. G7, GO-12, whose Theorem 1 imports GO-11's static converse;
5. GO-13;
6. G8, GO-14;
7. G9 and G10, GO-16.

The RLD series (G1–G5) and the T1 note (G6) form a separate chain, since T1 uses RLD I–IV.

## List 1 — GO-12 to GO-16 and T1

| ID | Item | Source | Tract. | Box | Track | State | Kill criterion |
|---|---|---|---|---|---|---|---|
| F12.1 | Toeplitz transfer, lemmas 1, 2, 4: reduction to single-sequence Toeplitz theory; continuity of the allocation value under weak spectral convergence; window-vs-path definition pinning | `go12-process-region.tex`, `thm:spectral` part (b) | a | M | P | open | a lemma is false as stated: give a counterexample, restate |
| F12.2 | Toeplitz lemma 3: the two-sided sandwich with a blocking lower bound | same | a/b | M | P | open | a counterexample to the sandwich: the transfer stays scoped to the circulant numerics |
| F12.3 | Spectral tilt: definition of "precision" and the zero-coherence control | `conj:tilt` | a | a | P | open | — |
| F12.4 | Spectral tilt: the monotone "concentrates" clause | `conj:tilt` | a/b | M | P | open | an exact counterexample (the saturation threshold depends jointly on three parameters) |
| F12.5 | Library pulls (Gray 1973 T-IT 19(4); Leiner–Gray 1974; Wyner 1976–78) | `go12-process-region.tex` sweep debts | c | — | — | owner | needs an institutional library |
| F13.1 | The m-consumer price rule (GO-11 Thm 5 at general m), containing GO-11 Thm 9 and GO-13 Thm 4 | `paper/go13-m-consumer-PROBE.md` | a | M | P | open | the m=2-specific step does not generalize: a scoped statement |
| F13.2 | Regime map over (ρ_AB, ρ_AV, ρ_BV, D_A, D_B, w, q), certified densely using Thm 5's convexity | `go13-dynamic-tax.tex`, regime-map remark | a | M | N or net | open | — (it is a net, not a proof) |
| F13.3 | A sign theorem replacing the refuted iff-law | same | b | M | P | open | an exact-arithmetic counterexample to each candidate law |
| F13.4 | Operational face: the tax curve across staleness, with its downward kink | `go13-dynamic-tax.tex` status | a | M | N | open | gates set in the prereg after the pilot |
| F13.5 | Operational face: Thm 4's two common prices on materialized process records | same | a/b | M | N | open | same |
| F13.6 | Operational face: prefix and path access classes (equal-q universality on records) | same | a | M | N | open | same |
| F13.7 | Operational face: the binary twin (Thm 3) | same | a/b | M | N | open | same |
| F14.1 | Minimizer uniqueness, modulo gauge (define the gauge first) | `go14-causal-erasure.tex`, near tex:851 | b | M | P | open | a non-gauge flat direction at an optimizer: refuted |
| F14.2 | The reset protocol realizing definition (a) (shared with F15.7) | tex:479-481, `q:open` (4) | b | L | P | open | a cost gap between any sequential protocol and the coordinate: scoped-open |
| F14.3 | The rwf pole (≈0.255/lag ≈ λ_s²/ρ² = 0.2565) | tex:439-441 | a/b | M | P | open | the derived pole differs from λ_s²/ρ²: the match is recorded as coincidental |
| F14.4 | The value of Ψ: the end state is the certified bracket (cor:brackets, unconditional) | tex:3307-3323 | c | — | — | open | to record as the end state; a closed form has no route ("not rational at any finite order") |
| F14.5 | Sharpness of Theorem D's modulus | `q:open` | b | M | P | open | — |
| F14.6 | Uniform-in-m decay of the cross-block kernel (Demko/Jaffard) | tex:4017-4045 | b | M | P | open | — |
| F14.7 | The innovations form; the closure constant beyond Δ≈6 | tex:916-928, 4058-4063 | b | M | P | open | — |
| F14.8 | The sign change exactly at lag Δ | `conj:proc`(4) | b | M | P | open | a counterexample |
| F14.9 | Two owed novelty sweeps (Lemma A′ packaging, Lemma W's combination); the window-side `la_cmi` cross-check | tex:3963-3971 | a | a | P | open | — |
| F15.1 | Theorem R⁺: R-IND-5 pass, novelty re-sweeps, ledger row, custody | `go15-reference-coupled.tex`, Theorem R⁺ | a | M | P | open | a pass finds an error |
| F15.2 | A lower bound for the F_S/F_U families (DC branch-and-bound on the H_u block, after matched-floor reruns) | `go15-reference-coupled.tex`, question "A lower bound for the headline cell" | b | L | net | open | boxes cannot close the 62× cancellation within the box: scoped-open |
| F15.3 | Strict lookahead hierarchy | conjecture of that name | c→b | M | P | open | blocked on F15.2 |
| F15.4 | Δ-reversal | conjecture of that name | c→b | M | P | open | blocked on F15.2 |
| F15.5 | Boundary attainment and the floor law | conjecture of that name | a/b | M | P | open | — |
| F15.6 | Horizon-matched anti-coupling | conjecture of that name | b | M | P | open | — |
| F15.7 | The Landauer face: which reset protocol realizes the discount, and what it costs to write (shared with F14.2) | `go15-reference-coupled.tex`, Landauer question | b | L | P | open | as F14.2 |
| F16.0 | GO-16 Theorem 3 corrected: three regimes (blackout t* = 0; a positive level with or without contested coordinates); tie iff contested or blacked out; λ > 0, Σ_S ≻ 0, k < n; uniqueness iff ρ(t) constant on the minimizer interval | VI-30, NEG-17, VI-33 | a | M | P | active: **written and re-checked (VI-33: core right; its findings applied); net `verify_go16_diagonal.py` in CI, 6/6.** **Confirmed by VI-35 (2026-11-21): core holds, 0 violations on 803 instances; 1 minor error (fractional entry vs eigenvalue), 1 gap, 3 overclaims, 6 exposition, all applied; the net gains d7–d9 (9/9, fires on VI-33's errors put back).** Owed: custody (the diagonalization step is proved, not netted); a rotated face for the blackout regime | the corrected statement fails at an instance: refuted |
| F16.0b | GO-16 Theorem 6 at k ≥ 2: the rank-k joint-subset commitment gap (VI-31 found no gap on two instances; evidence, not proof) | VI-31 | b | M | P | open | a certified gap at some instance: refuted |
| F16.1 | The phase-boundary alignment functional (the general-scope converse, Conj. 1) | `go16-adversarial-observer.tex`, Conjecture 1 | b | M | P (+net) | open | the scan finds no separating functional: scoped-open |
| F16.2 | The rank-k joint-subset converse | go16, after Theorem 6 | a/b | M | P | open | — |
| F16.3 | The non-commuting fixed-instrument game | go16, Cor. 2 and after Theorem 6 | b | M | P | open | a numerical commitment gap, certified: refuted ("no gap") |
| F16.4 | The m &lt; n case (constraint rank K ≤ m) | go16, model section | a/b | a | P | open | — |
| F16.5 | The ε-limit step, written out | `GO16-R-IND-5-NOTES.md` | a | a | P | open | — |
| F16.6 | Operational face: a frozen CFR bot in Kuhn or Leduc poker as the rank-k reader | go16, operational face; `OT-POKER-SURVEY.md` | b | L | N | open | gates set in the prereg after the pilot |
| FT.1 | The T1 worked result (092) | `drafts/T1-WORKED-RESULT-REGISTRATION-DRAFT.md` | — | — | N | owner | awaits the owner's read |
| FT.2 | Statistical (minimax) lower bounds on learning the read metric | T1 Thm 11(c), Prop 12 | a | M | P | open | — |
| FT.3 | Constants for noisy consumers (sub-exponential matrix Bernstein) | T1 Rem 17 | a | a | P | open | — |
| FT.4 | One code, chosen from Q̂ alone, serving every consumer of a class (the Ch. 17 keystone's heart) | T1 Rem 9 | b | L | P | open | a class with no uniform code: refuted for that class |
| FT.5 | Codes in the process settings of RLD II–IV | T1 Rem 6, 9 | b | L | P | open | — |
| FT.6 | A converse without the sandwich (fix the object first; the circle consumer may refute it as posed) | T1 Rem 6, 9 | b | M | P | open | the circle consumer beats every candidate bound: refuted as posed |
| FT.7 | A kernel that moves with the point; a range estimated with error | T1, open list | b | M | P | open | — |
| FT.8 | Consumers that read across dependent symbols | T1, open list | b | M | P | open | — |
| FT.9 | A combined budget of queries and bits (a price of a query in bits) | T1 tex:175-176 | b | M | P | open | — |
| FT.10 | Tighter constants (ρ is at least 30× the measured excess; c₂ is formal) | T1 tex:461-468 | b | M | P | open | — |

## List 2 — Paper III's open problems and two Ch. 17 conjectures

| ID | Item | Source | Tract. | Box | Track | State | Kill criterion |
|---|---|---|---|---|---|---|---|
| P3.a | The curved-image case (U on a submanifold, no ambient density) | Paper III `subsec:open` (a) | b | M | P | open | — |
| P3.b | The consumer-relative channel coding theorem (step 1: define the channel; the capacity section's median threshold is its degenerate case) | Paper III `subsec:open` (b) | b | L | P | open | no definition admits both a coding theorem and a converse: scoped-open |
| P3.c | Multi-observer beyond the Gaussian case: non-Gaussian sources; the region under the true divergence | Paper III `subsec:open` (c) | b | M | P | open | — |
| P3.d | Non-i.i.d. sources under the true divergence (Thm B2 on ergodic sources) | Paper III `subsec:open` (d) | a/b | M | P | open | — |
| P3.e | "The flip is R_C's argmin migrating with P_C" (formalize, then settle) | Paper III, after the separation result | b | M | P | open | — |
| P3.f | Kostina–Verdú dispersion under the true divergence | Paper III, high-resolution section | a/b | M | P | open | — |
| C17.1 | The cross-domain magnitude constant (041: band [0.015, 0.045], measured 0.064). Hypothesis: a per-domain slope of AUROC against margin SNR | Ch. 17; prereg 041 | b | M | N | open | the held-out test misses its sealed band |
| C17.2 | Green-rank positivity: (i) bring Ch. 17 up to the sibling repo's state; (ii) explicit Li–Yau constants; (iii) past φ₀‖R₀‖∞ &lt; 1/12, and d = 4 | Ch. 17; `the-angular-observer/paper/simods/` | (i) a, (ii) a, (iii) b | M | P | open | — |

## Named, tracked, not chased in this plan

These are recorded so that nothing is silently dropped.

- **RLD conclusion lists:**
  - **RLD-I:** decoder side information with neither side dominating; the main open question,
    side information at both receivers.
  - **RLD-II:** the rate of convergence in the blocklength; whether the window gap is exactly
    of order 1/N; block codes against a causal-prefix holder; delay; non-Gaussian processes.
  - **RLD-III:** time-varying parties; weaker conditions than (L3); tightness away from high
    resolution.
  - **RLD-IV:** non-rational infinite memory; vector poles on the unit circle; non-Gaussian
    linear processes.
- **Other papers:**
  - `tit-cr-context`: dispersion of the content coordinate L_n.
  - `tit-vector`: the coupled function below the one-dimensional regime, and its boundary D_star.
  - Paper V: achievability of the Gaussian region with reset side information, on continuous alphabets with unbounded squared error (VI-43; the converse is proved).
  - Paper V: a closed form for general Gaussian coupling (now a finite matrix program, GO-11).
  - Paper V: sources with memory, by an information-spectrum route.
  - Paper VIII: layered descriptions; the non-Gaussian tilted filter. The affine case, in
    `paper/TILTED-FILTER-NOTE.md`, will be taken to custody along the way.
  - `observer-representation`: PPAD membership; a two-player version.
  - GO-12, Questions 2–3: a binary process analog; its own operational face.
- **Ch. 17:** the common-observation problem. The verification-methodology frontier
  ("the discipline's own frontier").
