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

## List 3 — the grade gap (no ledger row is `[proved]` yet)

The `[proved]` bar has four parts (CHARTER T-CUST-1):
- a complete proof;
- a logged R-IND-5 pass;
- a C3 harness that is committed, CI-run and built to fail;
- a custody table of constants, slack and known gaps.

| ID | Item | Source | State | Missing pieces | Kill criterion |
|---|---|---|---|---|---|
| G1 | RLD-I (Thms 3, 7, 20) | `paper/tit-rate-leakage` | active | R-IND-5 done: **VI-27**, no false step; the ledger row is narrowed; the paper's items go to the owner, since it is under review. Still owed: nets for Theorem 3 (Lemma 1, Prop 2) and a stronger one for Theorem 20; the Lean–statement correspondence for Theorem 7; CI wiring (the scripts exit 0 on failure); custody. **The owner sets the class** | a pass finds an error: report to the owner, the row stays |
| G2 | RLD-II (Thms 4, 16, 20, 22, 23) | `paper/tit-stationary` | pending-custody | CI net; custody (VI-16 on record) | same |
| G3 | RLD-III.1–5 (Thms 13; 18; 2, 3, 5; Cor 6; 26) | `paper/tit-beyond-stationary` | pending-custody | CI net; custody (VI-17) | same |
| G4 | RLD-IV.1, .2, .4 (Thms 1, 10; 11; 18) | `paper/tit-unstable-ergodic` | pending-custody | CI net; custody (VI-18–21) | same |
| G5 | RLD-IV.3 (Thm 13, Prop 14, Cor 15) | same | active | R-IND-5 done: **VI-26**, three fresh-context passes (the original text and two rewrites), no false step; all findings applied to the draft; Tan–Dabora–Poor checked at the source; the harness strengthened (power control, exact example). Still owed: CI wiring; custody | same |
| G6 | T1 note v4.1 (Thms 5, 7, 11, Cor 8, Prop 12) | `paper/t1-learn-then-serve` | pending-custody | custody (VI-22–24); confirm `verify_t1_v4.py` runs in CI. The note is frozen until 092 is sealed | same |
| G7 | GO-12 theorems (065, 066, 070, 071) | `paper/go12-process-region.tex` | pending-custody | Records indexed as **VI-28**; since each record, the theorem text changed only cosmetically. All four nets are in CI's re-run tier. Owed: the custody table, after GO-11 (G16), which Theorem 1 imports | the diff shows unverified changes: fresh pass on those parts |
| G8 | GO-14 theorems (076–086) | `paper/go14-causal-erasure.tex` | pending-custody | index the F/W restatements and prereg records as VI rows; split the row so `[proved]` covers only proved statements; custody (079 sits in the committed-artifact tier) | same |
| G9 | GO-16 Thms 1–3 (090, 091) | `paper/go16-adversarial-observer.tex` | pending-custody | index `GO16-R-IND-5-NOTES.md` (v0.2) as a VI row; custody | same |
| G10 | GO-16 Thms 4–6 (v0.5) | same | pending-custody | R-IND-5 pass on v0.5; CI net for `go16_theory_extensions.py`; custody | a pass finds an error |
| G11 | The book's `[proved]` tags (Appendix B: B1, B4, B5, B7; Appendix F: the legibility theorems) | `chapters/appendix_b_cost_ledger.md`, `appendix_f_mathematical_ledger.md` | open | map the book's B-numbers to Paper III's labels; ledger rows with full custody where all four pieces exist, otherwise retag the book; the legibility custody is in `the-angular-observer` | a missing piece: retag at the true class |
| G12 | Appendix B's `[C7]` flag on the B7 dispersion constants (T-CUST-3: flags never ship) | `appendix_b_cost_ledger.md` (VI-7 paragraph) | open | check the constants against Kostina–Verdú at the source, then remove the flag | the constants disagree with the source: fix and log |
| G13 | Appendix F stops at GO-6 | `appendix_f_mathematical_ledger.md` | open | extend it through GO-16, RLD and T1 | — |
| G14 | Paper V theorems (the rate–work–distortion region; the Gaussian region with reset side information) | `paper/consumer-relative-landauer.tex` | pending-custody | VI-8 and VI-9 on record; nets in CI ([1c] `verify_consumer_landauer.py`, `verify_gaussian_sideinfo.py`); custody; a ledger row for the theorems | a pass finds an error |
| G15 | GO-10 theorems (the complementarity tax) | `paper/complementarity-tax.tex` | pending-custody | VI-10 on record (`paper/complementarity-tax-VERIFICATION.md`); net 055 in CI; custody | same |
| G16 | GO-11 theorems (Theorems 1–10) | `paper/go11-conditional-region.tex` | pending-custody | index the R-IND-5 records in `paper/go11-conditional-region-NOVELTY.md` (addenda) as VI rows, diffed against the current text; nets 060, 063, 064 in CI; custody | same |

**Order of promotion: bottom-up by dependency** (added 2026-11-20). A `[proved]` row may rest
only on `[proved]` rows or on external results checked at the source (T-CUST-3), so the
promotions go in this order:

1. G11, Paper III's B-theorems, which have no ledger rows yet;
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
  - Paper V: a closed form for general Gaussian coupling (now a finite matrix program, GO-11).
  - Paper V: sources with memory, by an information-spectrum route.
  - Paper VIII: layered descriptions; the non-Gaussian tilted filter. The affine case, in
    `paper/TILTED-FILTER-NOTE.md`, will be taken to custody along the way.
  - `observer-representation`: PPAD membership; a two-player version.
  - GO-12, Questions 2–3: a binary process analog; its own operational face.
- **Ch. 17:** the common-observation problem. The verification-methodology frontier
  ("the discipline's own frontier").
