# GO-P-2026-046 — GO-7 cross-source replication: scalar Gaussian source

Registers the **cross-source replication** of GO-7 (the operational rate–work
separation, GO-P-2026-043/045, both PASS on the binary two-bit source): the same
lifecycle — random codebook, ML encoding, random binning, in-bin ML recovery from
$(B,S^n)$, no-side-information control — on a **continuous source family**: scalar
$X\sim\mathcal N(0,1)$ with jointly Gaussian reset side information at $\rho=0.98$,
MSE distortion, target $D=0.25$. This is the paper's own scalar-corner setting (new
§VI), so the run also exercises the Gaussian theory operationally: analytic
$R=1.000$, $L=0.081$ bits/symbol, $I(\hat X;S)=0.919$. A PASS on this second,
independent source family meets the PROTOCOL §1 `[replicated]` bar for GO-7
("held in ≥2 independent settings"); a miss is reported at full prominence and
GO-7 stays `[demonstrated]`.

**Scheme.** Per $n$: one codebook of $2^{\lceil n(R+0.03)\rceil}$ i.i.d.
$\mathcal N(0,1-D)$ codewords (the reverse-channel marginal); minimum-distortion
(= ML) encoding; bins $= M \bmod 2^{\lceil n r_b\rceil}$; side-information decoder
$=$ nearest in-bin codeword to $\hat c\,\rho\,s^n$ (the conditional mean of
$\hat X$ given $S$ at the realized channel moments); control $=$ uniform in-bin
pick. Channel reported via second moments with the jointly-Gaussian surrogates
$R_{\mathrm{mom}}$, $L_{\mathrm{mom}}$.

**Pilot (logged, calibration only, pilot seed = SEED+1, n ≤ 20, T ≤ 100, 13 s).**
D̂ ≈ 0.28–0.29 (finite-$n$ distortion penalty as in 043), $R_{\mathrm{mom}}$ ≈
0.93, $L_{\mathrm{mom}}$ ≈ 0.07; converse side 0.56→0.74 rising with $n$; deep
decode (r_b=0.60) 0.00–0.03; control 1.00. Separation errors at $r_b=0.36$ were
noisy across $n$ (0.13–0.30) — integer-ceiling jumps in the effective bin rate
$\lceil n r_b\rceil/n$ plus $T\le100$ binomial noise — so the full design raises
all trial counts to 200, extends to $n=24$, and the G1 bars carry that spread.

```yaml
id: GO-P-2026-046
date: 2026-08-03
retrospective: false
kind: replication (cross-source; second independent source family for GO-7; PROTOCOL [replicated] bar)
claim: "The operational rate-work separation is source-family-general: on a scalar Gaussian source with strong reset side information, the stored index decodes from (bin, S^n) at a bin rate well below the description rate, fails below the conditional content, and fails absolutely without S."
harness: experiments/landauer_gaussian_source.py   # numpy; governed seed 20260805; --pilot used only for calibration
prediction:
  G1_separation: err(r_b=0.36) <= 0.20 at n=24 and <= 0.30 at n=20, with mean error
    over the larger half of the n-grid <= mean over the smaller half
  G2_bin_rate: 0.36 <= 0.50 * R_mom(n=24) -- >= 2x operational separation (pilot
    R_mom ~ 0.93 implies ~0.39*R_mom)
  G3_converse: err(r_b=0.05) >= 0.30 for every n >= 12 and >= 0.40 at n=24
  G4_side_info_specific: no-SI control err >= 0.90 at r_b=0.36 for all n >= 16
  G5_channel_realized: D_hat in [0.22,0.36], R_mom in [0.72,1.00],
    L_mom in [0.02,0.15] at n=24
  G6_deep_decode: err(r_b=0.60) <= 0.02 at n=24
falsification: G1/G2 failing refutes the cross-source generality of the operational
  separation at these blocklengths; G3 failing (reliable decode below content) would
  contradict the conditional-entropy accounting; G4 failing means a binning artifact;
  G5 failing voids the run (channel not realized; redesign, log, re-register).
design:
  n: [8, 12, 16, 20, 24]
  trials: [200, 200, 200, 200, 200]
  stopping: fixed-n, single governed run, seed 20260805
  clusters: one codebook per n (the codebook-draw robustness of this scheme was
    established by GO-P-2026-045 on the binary instance; carried as a noted caveat
    for the Gaussian instance, not re-gated here)
controls: [no-side-information decoder, below-content bin rate, channel window, deep-decode sanity]
amendments: []
hash: sha256:8f1a7d82a26df3d4b2226ef408c7eb66b77c832186cfd9cffc976b389b42b9b5
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2 and GO-7 keeps
class `[demonstrated]`. CI re-checks the committed JSON's self-consistency (tamper
check) but cannot re-run Tier B.
