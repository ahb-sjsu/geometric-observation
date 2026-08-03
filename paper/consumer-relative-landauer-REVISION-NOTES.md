# consumer-relative-landauer — R-IND-5 revision notes (2026-08-02)

Fresh-context, derivation-grade adversarial pass on every result in
`consumer-relative-landauer.pdf` (charter rule R-IND-5; ledger row VI-8; prereg
GO-P-2026-042). **Verdict: 0 errors, 4 sharpenings, nothing unsalvageable.** All
quoted numbers verified (h2(0.30)=0.88129, R=1.1187, L=0.1187 vs 1, ratio 8.42;
t=D endpoint (0.7803, 0.3902) matches Fig. 2). Fold the following into the .tex
before submission; none changes a theorem statement's truth value.

## S1 — Prop 1 proof: justify convexity of I(X;X̂|S) in q (the load-bearing one)

The proof line "Both mutual informations in (19) are convex in the test channel"
is asserted without argument, and the obvious route fails: under X̂−X−S,
I(X;X̂|S) = I(X;X̂) − I(S;X̂), and I(S;X̂) is **convex** in q (the channel
p(x̂|s) = Σ_x p(x|s)q(x̂|x) is linear in q; MI is convex in the channel at fixed
input) — not concave — so difference-of-convex proves nothing. Insert instead:

> Under the Markov chain X̂−X−S, p(x̂|x,s) = q(x̂|x), so
> I(X;X̂|S) = Σ_s p(s) · I_{p(·|s)}(q), a nonnegative combination of mutual
> informations, each with fixed input distribution p(x|s) and common channel q,
> hence convex in q.

(Numerically confirmed: 20,000 random instances, midpoint slack always ≥ +1.0e-4;
I(S;X̂) also always convex, min slack +3.6e-8.)

## S2 — Theorem 1: the time-sharing remark is vacuous; the region is stronger

"Time sharing among at most three test channels suffices" is true but weaker than
what the machinery gives: both coordinates are convex in q (S1) and T_C(D) is
convex and compact, so the union in (10) is **already closed and convex** — the
closure/conv hull is redundant and every boundary point is attained by a single
test channel. Restate: "the union is already closed and convex; no time sharing
is required." (At minimum, Fenchel–Bunt reduces three to two.)

## S3 — Theorem 1 converse: one missing sentence

State that the induced per-letter channels satisfy X̂_i − X_i − S_i (true because
X̂_i = h(X_i, X_{≠i}) and S_i ⊥ X_{≠i} | X_i for i.i.d. pairs), and that the
Markov constraint survives the Q-mixture because p(s|x) is common across i.

## S4 — Theorem 3 and Prop 4: hypothesis wording

- Thm 3: add the routine remark that joint typicality enforces all m distortion
  constraints simultaneously and the converse applies per constraint (Theorem 1
  was stated for a scalar distortion).
- Prop 4: the proof uses M ⊥ (X_t, X_{t+1}) | X_0 jointly; the stated per-t
  pairwise chain "M − X_0 − X_t" is formally weaker. Say "M is conditionally
  independent of the future trajectory given X_0."
- Prop 2 proof, cosmetic: opens "R = I(A,B;Y)" where it means the rate
  coordinate of the test channel.

## Scope/attribution — checked, no change needed

Physical scope (Remark 1, §II, §IX) correctly excludes acquisition/finite-time/
nondegenerate/quantum costs; [3],[4] used only in the asymptotic classical limit
with the "up to sublinear terms" hedge; Steinberg credited, novelty confined to
the joint-region role of (16); ECVQ presented as precursor. No overclaim found.

## Empirical program

- Tier A falsification net: `experiments/verify_consumer_landauer.py`
  (GO-P-2026-042).
- Tier B operational run (Atlas): `experiments/landauer_operational.py`
  (GO-P-2026-043) — finite-n random-binning conditional reset, genericity sweep,
  staleness Monte Carlo.

**Note:** the repo holds only the compiled PDF; the .tex source for this paper is
not in `paper/`. Apply S1–S4 wherever the source lives, then re-sync the PDF.
