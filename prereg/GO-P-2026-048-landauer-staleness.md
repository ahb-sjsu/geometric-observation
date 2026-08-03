# GO-P-2026-048 — Staleness-work complement, operational: aging side information raises the reset threshold

Registers the **operational demonstration** of the paper's staleness proposition
(stale Markov record): a stored record's conditional Landauer content grows with the
age of the retained side information, and the growth is exactly the predictive
information lost. Design: one random-codebook description $M$ of $X_0^n$ (binary
symmetric Markov chain, flip $p=0.05$/step, per-symbol Hamming target $d=0.11$),
binned ONCE; the reset decoder recovers $M$ from $(\mathrm{bin}, X_t^n)$ at ages
$t\in\{0,1,2,4,8,16,32,64\}$. Same record, same bins, same decoder — only the age
changes. Prediction: the decodable bin-rate threshold rises with $t$ tracking
$\mathrm{thr}(t)=R_c-1+h_2(\hat d * q_t)$ ($*$ = binary convolution,
$q_t=(1-(1-2p)^t)/2$), from $\approx0.10$ at $t=0$ toward the full description rate
as correlation dies. Governs `experiments/landauer_staleness.py`;
result `results/GO-landauer-staleness.json`.

**Pilot (logged, calibration, pilot seed = SEED+1, n=32, T=80).** Physics gates all
passed with the threshold tracking prediction to 0.001–0.05 (age 1: 0.175 vs 0.176;
age 2: 0.250 vs 0.249; monotone throughout; the fixed bin rate 0.175 flips from
3% error at age 0 to 100% at age ≥32). The no-SI control gate FAILED as designed —
a flat 0.90 bar misreads *chance* as side information when high-$r_b$ bins hold only
2–8 members (uniform picking succeeds at $1/|\mathrm{bin}|$). Corrected pre-seal to
a **chance-relative** gate: control error ≥ (its own measured chance level) − 0.05
at every (age, $r_b$). Same lesson class as GO-P-2026-046; caught in pilot this time.

```yaml
id: GO-P-2026-048
date: 2026-08-03
retrospective: false
kind: operational Monte Carlo (Tier B, Atlas; staleness face of Paper V)
claim: "Aging the retained side information raises the operational reset threshold of a fixed stored record exactly as the staleness-work complement prices it: relevance lost to time is gained as conditional erasure work."
harness: experiments/landauer_staleness.py   # numpy; governed seed 20260807; --pilot used only for calibration
prediction:
  S1_threshold_monotone: the measured threshold (smallest r_b with err <= 0.25) is
    nondecreasing across all eight ages
  S2_tracks_prediction: |thr_meas - thr_pred| <= 0.11 (about one grid step) for every
    age in {0,1,2,4,8,16}, thr_pred computed from the MEASURED d^ via
    Rc - 1 + h2(d^ * q_t)
  S3_same_binrate_flips_with_age: at fixed r_b = 0.175, err <= 0.10 at age 0 and
    >= 0.90 at both ages {32, 64} -- the identical bins go from dischargeable to
    irreducible purely by record age
  S4_channel_realized: d^ in [0.10, 0.17]
  S5_no_si_control: control error >= (measured chance level 1 - E[1/|bin|]) - 0.05
    at every (age, r_b)  [chance-relative; corrected pre-seal per pilot]
falsification: S1/S2 failing refutes the operational reading of the staleness
  proposition (monotone data-processing loss priced as work); S3 failing breaks the
  headline exchange; S5 failing means a binning artifact; S4 failing voids the run.
design:
  n: 40
  trials: 200 (one codebook, one bin assignment; the record is FIXED across ages by
    design -- age is the only manipulated variable)
  ages: [0, 1, 2, 4, 8, 16, 32, 64]
  rb_grid: [0.10, 0.175, 0.25, 0.325, 0.40, 0.475, 0.55, 0.625]
  stopping: fixed design, single governed run, seed 20260807
controls: [no-side-information decoder (chance-relative), fixed-bin-rate age flip, channel window]
amendments: []
hash: sha256:16f1890a98c5b717a39f0f4eddde08b5800b6f50b4744287b834e7dd58f071cc
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2. CI re-checks the
committed JSON's self-consistency (tamper check) but cannot re-run Tier B.
