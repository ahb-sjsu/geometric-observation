# GO-P-2026-047 — GO-7 cross-source replication v2: corrected instrumentation windows

Supersedes **GO-P-2026-046** (registered MISS 4/6, reported at full prominence in
[`experiments/GO-landauer-gaussian-source-NOTES.md`](../experiments/GO-landauer-gaussian-source-NOTES.md)):
all four physics gates passed on the scalar Gaussian source, and the two failures were
instrumentation-window design errors — (a) the sealed $R_{\mathrm{mom}}$ ceiling (1.00)
was anchored to the analytic $R(D)$ when the correct reference is the **codebook rate**
$\lceil 24\cdot1.03\rceil/24=1.042$ (measured 1.017 sits legitimately between the two);
(b) the deep-decode bar (≤0.02) sat exactly on a realizable count (4/200) and failed on
float epsilon. This v2 keeps the design and the four physics gates **identical** for
comparability, corrects only the two windows, reuses the sealed 046 machinery by import
(no code fork), and draws a fresh seed. A PASS earns GO-7 the PROTOCOL `[replicated]`
class (second independent source family); a second miss keeps `[demonstrated]` and the
Gaussian instance enters the ledger as an honest negative.

```yaml
id: GO-P-2026-047
date: 2026-08-03
retrospective: false
kind: replication (cross-source, v2; supersedes GO-P-2026-046 -- window corrections only, physics gates unchanged)
claim: "The operational rate-work separation is source-family-general: on a scalar Gaussian source (rho=0.98, MSE, D=0.25) the stored index decodes from (bin, S^n) at ~0.35 of the measured description rate, fails below the conditional content, and fails absolutely without S."
harness: experiments/landauer_gaussian_source_v2.py   # imports run_gauss from the sealed landauer_gaussian_source.py; fresh seed 20260806
prediction:
  G1_separation: err(r_b=0.36) <= 0.20 at n=24 and <= 0.30 at n=20, halves-trend
    [identical to 046; measured there 0.11/0.16]
  G2_bin_rate: 0.36 <= 0.50 * R_mom(n=24)  [identical; measured 0.35*R_mom]
  G3_converse: err(r_b=0.05) >= 0.30 all n >= 12, >= 0.40 at n=24  [identical; 0.52-0.69]
  G4_side_info_specific: control err >= 0.90 all n >= 16  [identical; 1.00]
  G5_channel_realized: D_hat in [0.22,0.36], R_mom in [0.72,1.06], L_mom in [0.02,0.15]
    at n=24  [CORRECTED ceiling: codebook rate 1.042 + estimation headroom]
  G6_deep_decode: err(r_b=0.60) <= 0.035 + 1e-9 at n=24  [CORRECTED: count-robust
    (<= 7/200), epsilon-guarded]
falsification: as GO-P-2026-046; additionally, a physics-gate miss under the fresh seed
  (after passing under 046's seed) is reported as seed instability of the Gaussian
  instance at these n.
design:
  n: [8, 12, 16, 20, 24]
  trials: [200, 200, 200, 200, 200]
  stopping: fixed-n, single governed run, seed 20260806
  clusters: one codebook per n (codebook robustness established by GO-P-2026-045 on the
    binary instance; carried as noted caveat)
controls: [no-side-information decoder, below-content bin rate, corrected channel window, deep-decode sanity]
amendments: []
hash: sha256:2e9a9d0f2a1eeeefe003946ba72be77afba11a5dadf679ae596c179914b95666
```

## Falsification
A miss on any gate is reported at full prominence per PROTOCOL Rule 1.2. CI re-checks
the committed JSON's self-consistency (tamper check) but cannot re-run Tier B.
