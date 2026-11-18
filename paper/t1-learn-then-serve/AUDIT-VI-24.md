# Audit VI-24 — T1 note, version 4 (2026-11-18)

A fresh-context general-purpose agent audited `t1-learn-then-serve.tex` v4 at commit
3b60d31 (md5 13716f7ad117b95500f3bd387eb1ade0; unchanged when the audit returned). It
was given the note and paper one's Appendix A, not the author's conclusions, and asked to
try to break the new parts first. It wrote its own numerics (`audit-vi24/`, seven scripts
with their outputs; none imports `verify_t1_v4.py`). Its verdict: **no false
mathematical step.** Version 4.1 applies every finding below (2026-11-18).

## Findings and what was done

| # | Where (v4) | Class | Finding | Disposition in v4.1 |
|---|---|---|---|---|
| 1–3 | Theorem 7, its three properties and the L² claims | confirmed | d_k bounded on the finite alphabets; the code's consumer loss equals its surrogate distortion; the surrogate joint law of (T_k, T̂_k) is the true one, and the surrogate distortion converges to E ℓ_C(T, T̂) at about 4^{-k} (four consumers, one Lipschitz but not C¹, three channels) | — |
| 4 | Theorem 7, proof | wording | two places in paper one's proof use the quadratic form: its opening line (E‖Ŷ‖² < ∞ from a finite distortion and W ≻ 0) and the second half of Step C (identifying the region); neither is needed, but the proof should say so | the proof names both: the opening line is replaced by the hypothesis E‖T̂‖² < ∞, and only the diagonal part of Step C is used |
| 5 | Theorem 7, hypotheses; r, ℓ = I(T;T̂), I(T;T̂\|S) | confirmed | 200 random instances, error 9.6e-13 bits | — |
| 6 | Corollary 8(a), (b) | confirmed | adversarial Q̂ on the boundary of the event and adversarial designs: loss/D at most 0.9964 | — |
| 7 | Corollary 8 | wording | Q ≻ 0 needed (Lemma 1) but only implied | added to the hypotheses |
| 8 | Theorem 11(c) | overstatement | "in the memoryless setting neither do codes" — (A1) does not give three bounded derivatives, and the codes depend on the consumer | qualified: for a consumer whose weighted map has three bounded derivatives, codes built for that consumer (Corollary 8, Remark 9) |
| 9 | abstract | overstatement (mild) | the certificate reads as if the learner's (A3) codes achieve the frontier at D | now: the frontier for Q̂ at a budget D̂ slightly below D, achievable by codes built for the consumer |
| 10 | Proposition 2 | confirmed | both constants attained (g = x³: error exactly M₃h²/6; g = x\|x\|/2 at 0: exactly M₂h/2); 1798 random cases with singular G, no violation | — |
| 11 | Corollary 3 | confirmed | 20000 random instances at the threshold, no failure | — |
| 12 | Proposition 4, the matrix sandwich and B | confirmed | 24000 cases, no violation; the lower bound attained | — |
| 13 | Proposition 4 | wording | the O(·) hides log((1+e₊)/(1−e₋)), which grows when ν₋ = 1; the decoder must also know e± | the O(·) is written out; e± are listed as known to both ends |
| 14 | Proposition 4, its proof, abstract ("at no leakage") | **gap (definitional)** | I(T;Q̃,M\|S) = I(T;M\|S,Q̃) is right, but the series' leakage is the entropy form H(M\|S^N)/N, which with randomness counts H(Q̃): the message adds up to B/K per symbol, not zero; the same under (A3-i) if the holder does not know the probe seed | the proposition now says: the message carries no information about the source; with the realized calibration part of the code and known, as a code is, to every party, the leakage is the designed one; in the series' entropy form it adds at most B/K bits per symbol; the proof covers (A3-i). Abstract: "bits that carry no information about the source" |
| 15 | (A3) | wording | under (A3-i) the decoder also queries (4pm in all); "construct" presumes an agreed selection rule among the codes the theorem asserts | both stated |
| 16 | Remark 9; (A3) | wording | Corollary 8(a)'s budget D̂ uses M₁, M₂, M₃, which (A3) did not list | (A3) and Remark 9 list them among the shared constants |
| 17 | Theorem 5, rewritten for g | confirmed | every step re-derived; 96 cases (singular G, non-diagonal G, rank-one G, softmax), no violation, min ρ/\|excess\| = 87 | — |
| 18 | Setting; Remark 13 | wording | "components of C that G does not see" should be the part of C in ker G | reworded in both places |
| 19 | Remark 13 | **overstatement** (in v3 too) | "excludes a ReLU without leak" is false for expanding layers: g(x) = (ReLU x, ReLU(−x)) is bi-Lipschitz and satisfies (A1a) with Q = I, ν₋ = 1/2, ν₊ = 0 (τ_ν = p/2 bits) | now "a square ReLU layer, which is not injective", and the expanding example is stated; check C13 of `verify_t1_v4.py` |
| 20 | title footnote | wording | the numbering map omitted the remarks | completed: Remarks 9–12 → 13–16; Remark 13 → Proposition 2 and Remark 17; Remarks 14–16 → 18–20 |
| 21 | Lemma 1, Propositions 10 and 12 | confirmed unchanged | identical to v3 up to punctuation | — |

## What the audit did not check

The series' own theorems (region identification, the converse with private randomness,
(P1)–(P3) with shifts beyond paper one); Remarks 14, 16, 18 and the noise constants of
Remark 17; Linder–Zamir; the author's numbers in checks C5 and C6; Remark 9's conjecture
of one code for a class. External results: Tropp's Theorem 1.4 was read at first hand
(arXiv:1004.4389v7; journal numbering not checked); of Villard–Piantanida only the arXiv
abstract was read, so Theorem 7 rests on paper one's restatement of their theorem for
distortions bounded in [0, d_max].

## Files

`audit-vi24/`: `thm7_surrogate.py`, `thm5_cor8.py`, `prop2_fd.py`, `cor3_probes.py`,
`prop4_calib.py`, `rem13_maps.py`, `numbering.py`, each with its `.out.txt`.
