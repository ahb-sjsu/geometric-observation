# Registration 4: why do near-zero predictions fail?

Registered 2026-10-02. Code `ot_s2noise.py`. Builds on the boundary test
(daca788), the Gaussian-departure registration (9f2a61b) and registration 3
(scored in c14e579).

## The return to explain

Where the theory predicts a removal below 0.05 bit, the near-boundary
criterion asks that the measured removal sit within 2 bootstrap SE of zero
in at least 80% of cases. It has failed three times:

| Test | Result |
|---|---|
| boundary test | 56% |
| post-hoc in-scope split | 64% |
| registration 3, blind, in scope | 35% |

It fails inside the Gaussian scope, so non-Gaussianity does not explain it.

## Two competing accounts

- **NOISE.** The SE understates the measurement's variability. It is a
  bootstrap over held-out points for one fixed train/test split and one
  fixed set of fitted adversaries. It omits the variability of the split,
  and of the adversaries' training, behind any single measured removal.
- **BIAS.** Near the boundary the measured removal is systematically
  nonzero, so the theory misses there.

## Design

The rule in `ot_s2noise.py` fixes the cases, using only published
quantities. They are the in-scope cases of all three registrations with
predicted removal < 0.05 bit:
- excluding principal-copy views and the orth family;
- for registration 3, slack 0.05, 0.15 and 0.4, its S2 set.

That gives 71 cases on real datasets (the test group) and 14 on synthetic
Gaussian sources (a control group, reported, not scored). The warped
Gauss8-exp control is dropped, because it is deliberately non-Gaussian and
so belongs to neither group.

Each case is measured again on 20 fresh random splits (seeds 1–20). The
directions b_R and b_aware stay frozen. The codes, the three adversaries
(refit on each split) and the bootstrap SE are the same as before. Seed 0
is the original measurement.

## Criteria (real group; vacuous below 15 cases)

- **N1** The median over cases of SD_rep / mean bootstrap SE is ≥ 1.5. The
  bootstrap SE understates the variability.
- **N2** |original measured| ≤ 2·SD_rep in ≥ 80% of cases. With the full
  SE, the criterion would hold.
- **B1** |mean of the 20 replicates| > 3·SD_rep/√20 in ≥ 50% of cases.
  There is systematic nonzero removal near the boundary.

## Reading, fixed in advance

- N1 and N2 pass and B1 fails: **NOISE**.
- B1 passes: **BIAS**, whatever N1 and N2 say about the noise.
- Neither: unresolved, reported as such.

The control group is reported with the same three statistics.

## Disclosure

The cases were measured before (seed 0), and their single-split outcomes
are public. The replicate measurements on seeds 1–20 are new. This tests a
claim about the measurement, not a new prediction of the theory.
