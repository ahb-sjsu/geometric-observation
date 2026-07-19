# GO-P-2026-041 — Blind, non-oracle, prospective flip with a magnitude prediction

The decisive test the reviewer asked for: on a **fresh, untouched** domain, recover the read
operator from the consumer alone (no ground truth, no oracle direction), and **commit the
winning code, the sign of the two-metric reversal, and a magnitude band for the downstream
gap before the held-out test set is opened**. This is the non-oracle counterpart to the
sweep's oracle-informed array rows.

## Setup
- **Domain (fresh).** 20 Newsgroups binary topic classification, `sci.space` vs `rec.autos`
  (headers/footers/quotes stripped) — never used elsewhere in the program. Standard
  train/test split: **train = calibration, test = held-out** (disjoint documents).
- **Frozen representation.** TF-IDF (max 20k features, English stop-words, sublinear) →
  `TruncatedSVD(100)` (LSA), **fit on the calibration (train) split only** and applied
  verbatim to the held-out test split.
- **Consumer.** `LogisticRegression` on the calibration embeddings.
- **Read operator — NON-ORACLE.** Recovered by finite-difference probing of the consumer's
  margin (`decision_function`) with respect to each embedding coordinate — using the
  consumer's output only, **no test labels and no ground-truth direction**. For a linear
  consumer this recovers the margin weight; `P_C = g gᵀ`, kept via the top-`r` projection
  onto the embedding eigenbasis.
- **Three matched-bit codes** in the calibration embedding eigenbasis: R (bits to the read
  directions), O (bits by embedding variance, reconstruction-oriented — MSE-optimal within
  the scalar allocation family), A (anti). Downstream = held-out classifier AUROC;
  reconstruction = embedding relative MSE.
- **Config-frozen on an internal cal-A/cal-B split** before sealing (fit on cal-A, flip
  scored on disjoint cal-B), so only a configuration that already generalised once is sealed.

```yaml
id: GO-P-2026-041
date: 2026-07-19
retrospective: false
kind: blind non-oracle prospective flip with a magnitude prediction on a fresh domain
domain: 20 Newsgroups sci.space vs rec.autos (untouched); frozen LSA (TF-IDF -> SVD100, train-only)
consumer: logistic classifier; downstream = held-out AUROC; reconstruction = embedding rel-MSE
read_operator: NON-ORACLE finite-difference margin probe (consumer output only; no labels, no oracle angle)
frozen_config: {base_bits: 2.0, r: 16}
code_hash: sha256:cf05e7c16c7e4dde7a30e7c0041e5a239e35b18a4731680ca0507089789c7f84
internal_cal_B: {auroc_R: 0.977, auroc_O: 0.947, auroc_A: 0.641, recon_O: 0.286, recon_R: 0.439}
delta_pred: +0.116   # tr[P_C(Sd_O - Sd_R)] on calibration; POSITIVE => predicts R wins downstream
sealed_predictions:
  winner: R (read-preserving)
  sign: "AUROC(R) > AUROC(O)  AND  recon(O) < recon(R)  AND  anti worst"
  magnitude: "held-out AUROC(R) - AUROC(O) in [0.015, 0.045]"   # calibration cal-B gap 0.030 +- 50%
falsification: any of the four sealed bars fails on the held-out 20NG TEST split -> the blind
  non-oracle flip is NOT confirmed (reported regardless of sign).
commitment: outcome reported regardless of sign in claims/LEDGER.md (GO-B-blind). No held-out
  TEST-split document is embedded or scored before this prereg is committed. The winning code,
  sign, and magnitude band are fixed by this seal; the held-out split is untouched.
hash: sha256:1f5974b4197c80efbd3816e4c3f23923e2fa1849c3a0f0dd33b1e759fe5f3f21
```

## Why this is the decisive test
It is the one experiment that predicts the consumer's geometry, the winning code, the sign of
the reversal, and the approximate magnitude **before** the sealed test set is opened, using a
read operator recovered with no oracle information. A pass shows the framework can discover
the operative geometry and choose the better code prospectively; a fail is reported at equal
prominence. Sealed per REG-1; the git commit is the binding timestamp.

## Outcome — PENDING
