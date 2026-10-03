# Amendment: corrected measurement protocol (cross-fitted selection, paired differences)

Registered 2026-10-02, after an external review, before any number under the
new protocol was computed. Code: `ot_crossfit.py`.

## The problem

Every leakage measured on real data is a proxy: the cross-entropy of an
adversary q(m|s) that predicts the code from the holder's view. Its
population value is H(M|S) + E_S D(p(M|S) ‖ q(M|S)), so a difference of two
proxies mixes a difference of conditional entropies with a difference of
adversary errors. The original measurement (`ot_boundary.leak_with_se`)
also had two procedural flaws.

- **Selection on the scored samples.** It chose the lowest-loss of three
  adversaries on the same held-out samples on which it then reported the
  loss.
- **Unpaired standard errors.** It combined two separate bootstraps as
  though the two codes were independent, although they are scored on the
  same samples.

## The corrected protocol

1. **Cross-fitting.** The held-out half is split once, at random (seed
   12345), into two folds. For each code the adversary is selected on one
   fold and scored on the other, and the folds are then swapped. Every
   held-out sample is scored by an adversary chosen without it.
2. **Paired differences.** The measured removal is the mean of the
   per-sample loss difference between the two codes, on the same samples.
   Its SE is a bootstrap of that mean (200 resamples, seed 0).

Nothing else changes:
- the splits (seed 0), the frozen directions and the codes;
- the adversary families and their training data;
- every case list, prediction and criterion, and every scoring script.

The quantity is still a proxy for H(M|S). This amendment removes the
selection bias and the unpaired SE. It does not remove adversary error.

## What is re-measured

**Phase A (this run).** Each registration is re-scored by its own frozen
scoring script on the re-measured file.

| Registration | Re-measured file | Scored by |
|---|---|---|
| Boundary test | `boundary_measured_crossfit.json` | `boundary_score.py` |
| Gaussian-departure registration | `boundary_measured_crossfit.json` (retrodiction) and `fresh_measured_crossfit.json` (blind) | `gauss_score.py` |
| Registration 3 | `scope_measured_crossfit.json` | `scope_score.py` |

The Gaussian-departure scores take Gamma from the frozen predictions file,
so they are unchanged.

**Phase B (later).** Registrations 4 and 5 use replicate splits and need
several hours.

## How results are reported

The original verdicts stand as the record under the original protocol. The
re-measured verdicts are reported beside them, criterion by criterion,
whether they agree or not.
