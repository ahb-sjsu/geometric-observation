# GO-P-2026-045 — GO-7 multi-codebook replication: the separation is the ensemble's, not one draw's

Registers the **replication run** resolving GO-P-2026-043's registered few-cluster caveat
(one codebook per blocklength). Same sealed Part-A design (Prop-2 source, BSC(0.08)×
BSC(0.32) target, ML encoding, random binning, in-bin ML recovery from $(B,S^n)$, no-SI
control), executed with **five independent codebooks per $n$** under a **fresh seed**, and
gated per-codebook plus a new cross-codebook stability gate. No pilot: the design and its
operating point are exactly the sealed 043 run; bars below derive from 043's measured
values with per-codebook binomial-noise headroom ($T{=}100$ at $n{=}32$: SE $\approx$
1.7\% at $p{=}0.03$). Reuses the committed 043 machinery by import (no code fork).
Governs `experiments/landauer_multicodebook.py`;
result `results/GO-landauer-multicodebook.json`.

```yaml
id: GO-P-2026-045
date: 2026-08-03
retrospective: false
kind: replication (R-IND-6-style hardening of GO-7's registered caveat; same source/domain, new codebook draws + fresh seed)
claim: "The operational rate-work separation of GO-7 holds for every independent codebook draw, not one lucky codebook: decode above conditional content at ~0.4R, failure below content, total failure without S, stable across the random-coding ensemble."
harness: experiments/landauer_multicodebook.py   # imports run_partA from the sealed landauer_operational.py; seed 20260804, 5 codebooks
prediction:
  A1r: err(r_b=0.26, n=32) <= 0.12 for EVERY codebook (5/5) and median <= 0.05
    (043 measured 0.03)
  A2r: 0.26 <= 0.45 * median R_hat(n=32)  (043 measured R_hat = 0.6715)
  A3r: err(r_b=0.03, n=32) >= 0.40 for EVERY codebook and >= 0.30 at every n >= 16,
    every codebook  (043 measured 0.67 at n=32, min 0.455 over n >= 16)
  A4r: no-SI control err >= 0.90 at r_b=0.26 for all n >= 20, every codebook
    (043 measured 1.00 everywhere)
  A5r: channel realized per codebook: |D_hat-0.20| <= 0.04, L_hat in [0.03,0.14],
    R_hat in [0.62,0.78] at n=32  (043: 0.213 / 0.069 / 0.672)
  A6r: cross-codebook stability: max-min spread of err(r_b=0.26, n=32) <= 0.10
falsification: any codebook violating A1r/A3r/A4r/A5r, or spread beyond A6r, means the
  GO-7 effect is codebook-dependent -- reported at full prominence and the GO-7 ledger
  row keeps its few-cluster caveat (and gains a draw-dependence note).
design:
  n: [12, 16, 20, 24, 28, 32]
  trials_per_codebook: [200, 200, 200, 200, 120, 100]
  codebooks: 5 independent per n (rng streams [SEED, cb])
  stopping: fixed-n, single governed run, seed 20260804
  clusters: codebooks are the independent unit (5 clusters; few-cluster caveat applies
    to any statistic beyond the per-codebook gates -- gates are therefore per-codebook)
scope: same synthetic source and domain as 043 -- this resolves the CODEBOOK caveat
  only; GO-7 remains class [demonstrated] (a cross-source/domain replication would be
  the [replicated] bar, not claimed here)
amendments: []
hash: sha256:e5ceca6e4be746188baee27328976e0ca430764f90dda8e111ad86e8aa9af8ba
```

## Falsification
A miss on any per-codebook gate is a `[refuted]`-prominence report per PROTOCOL Rule 1.2
and the ledger caveat stands. CI re-checks the committed JSON's self-consistency (tamper
check) but cannot re-run Tier B.
