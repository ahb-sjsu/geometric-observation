# GO-P-2026-054 — GO-9 Gaussian setting, second (and final) attempt

Supersedes **GO-P-2026-052** (registered MISS 5/6, reported at full prominence in
[`experiments/GO-landauer-gaussian-secondsettings-NOTES.md`](../experiments/GO-landauer-gaussian-secondsettings-NOTES.md)).
In 052 coordination saved **0.216 bits/symbol on the $S$-opaque record** — 65% of the
asymptotic shared-structure information — and every gate passed **except C2**: the
$M_1$ discount came in at 0.1316 against the sealed $0.40\times\mathrm{gap}=0.1331$
bar, short by 1.1%.

**That bar is NOT moved.** The only changes are a **larger pre-committed design**
($n$ 12→14, $T$ 150→250, affordable via strided member views, verified
index-identical) and the same exact-binomial replacement for the normal-approximation
control test used in GO-P-2026-053. **C1–C5 carry over byte-identical bars.**
Declared in advance: this is the final attempt — if the 1.1% shortfall was real rather
than noise, the run fails again, GO-9 remains `[demonstrated]`, and no third attempt
will be registered.

```yaml
id: GO-P-2026-054
date: 2026-08-03
retrospective: false
kind: replication (final attempt at GO-9's second setting; design enlarged, all physics bars unchanged)
claim: "On a Gaussian source, resetting either of two records that share a component is operationally cheaper when the other record is intact, by a substantial fraction of the shared-structure information; mismatched pairing saves nothing."
harness: experiments/landauer_coordinated_gaussian_v2.py   # imports the sealed 052 constants; governed seed 20260813; NO pilot was run
prediction:
  C1_s_discount_m1: |thr(m1 indep) - (Rc - 1/2 log2(1/d^))| <= 0.25   [unchanged]
  C2_coordination_m1: 0.40*gap <= thr(m1 indep) - thr(m1 coord) <= gap + 0.15
    [UNCHANGED -- this is the bar 052 missed by 1.1%]
  C3_coordination_m2: 0.40*gap <= thr(m2 indep) - thr(m2 coord) <= gap + 0.15  [unchanged]
  C4_shuffled_null: thr(shuffled) >= thr(independent) - 0.16, both records  [unchanged]
  C5_channel_realized: d^ in [0.28, 0.48]  [unchanged]
  C6_uniform_control_exact: control success count consistent with chance under an
    EXACT two-sided binomial test at alpha = 5e-4, every r_b  [instrument corrected]
falsification: any gate missing leaves GO-9 at [demonstrated]; no further attempt.
design:
  n: 14
  trials: 250
  D_target: 0.35 per component
  rb_grid: [0.40, 0.55, 0.70, 0.85, 1.00, 1.15, 1.30, 1.45, 1.60, 1.75]
  stopping: fixed design, single governed run, seed 20260813, no pilot
controls: [shuffled-pairing null (one-sided), uniform control (exact binomial), channel window, S-opaque record as internal comparison]
amendments: []
hash: sha256:8e38755318dbedd6617673c6d48d98a6e491ce5b25ed2590998e88f353b242bf
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2, GO-9 keeps
`[demonstrated]`, and the Gaussian setting is recorded as a standing near-miss.
