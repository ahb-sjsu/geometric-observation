# GO-P-2026-050 — Coordinated reset saves the conditional total correlation, operationally

Registers the **operational demonstration** of the paper's several-consumers corollary
(coordinated reset): resetting one record with the *other consumer's record intact as
side information* lowers the decodable bin-rate threshold by the shared-structure
information — the operational face of $\mathrm{TC}(U_1;U_2\mid S)$. Design: $X=(A,B,C)$
i.i.d. fair bits, reset side information $S=A$; records $M_1$ (codebook description of
$U_1=(A,B)$) and $M_2$ (of $U_2=(B,C)$) at per-component Hamming target $d=0.05$. Each
record is binned and recovered in-bin by ML under independent reset $(\mathrm{bin},a^n)$,
coordinated reset $(\mathrm{bin},a^n,\hat u_{\text{other}}^n)$, a shuffled-pairing null,
and a uniform control. Predicted coordination discount for both records (from the
measured channel): $\mathrm{gap}_{TC}=1-h_2(\hat d*\hat d)$, the empirical
shared-$B$-component information, $\to$ the exact-consumer
$\mathrm{TC}=1$ bit as $d\to0$. $M_2$ is $S$-opaque ($U_2\perp A$) so its independent
threshold sits at the full description rate; $M_1$'s already carries the $S$ discount
$1-h_2(\hat d)$. Governs `experiments/landauer_coordinated.py`;
result `results/GO-landauer-coordinated.json`.

**Pilot (logged, calibration, pilot seed = SEED+1, n=14, T=60).** d̂=0.068,
gap_TC(pred)=0.454; measured discounts 0.30 ($M_1$) and 0.45 ($M_2$, near-exact);
$S$-discount threshold 0.80 vs 0.857 predicted; channel and pooled control in range.
One gate corrected pre-seal: the shuffled null was registered two-sided ("equals
independent") and the shuffled threshold landed 0.3 *above* independent — correct
behavior, since a decoder weighting garbage evidence degrades ML relative to ignoring
it. C4 is therefore **one-sided**: mismatched coordination must provide no *benefit*.

```yaml
id: GO-P-2026-050
date: 2026-08-03
retrospective: false
kind: operational Monte Carlo (Tier B, Atlas; several-consumers face of Paper V)
claim: "Coordinated reset is operationally cheaper than independent reset by the records' shared-structure information: the other consumer's intact record lowers the decodable bin-rate threshold by ~gap_TC = 1 - h2(d*d) on BOTH records, mismatched coordination provides no benefit, and the saving is the operational face of TC(U1;U2|S)."
harness: experiments/landauer_coordinated.py   # numpy; governed seed 20260809; --pilot used only for calibration
prediction:
  C1_s_discount_m1: |thr(m1 independent) - (Rc - (1 - h2(d^)))| <= 0.20
  C2_coordination_m1: thr(m1 indep) - thr(m1 coord) >= gap_TC - 0.20
  C3_coordination_m2: thr(m2 indep) - thr(m2 coord) >= gap_TC - 0.20
  C4_shuffled_null: one-sided -- thr(shuffled) >= thr(independent) - 0.16 for both
    records (mismatched coordination provides no benefit; it may be worse)
  C5_channel_realized: d^ in [0.03, 0.12]
  C6_uniform_control: pooled chance-relative at 4 sigma per bin rate (the
    GO-P-2026-049 gate design)
falsification: C2/C3 failing refutes the operational coordinated-reset saving; C4
  failing (shuffled coordination HELPS) means the saving is an artifact of the decoder
  rather than of shared record structure; C5 failing voids the run.
design:
  n: 16
  trials: 150
  rb_grid: [0.35, 0.50, 0.65, 0.80, 0.95, 1.10, 1.25, 1.40, 1.55, 1.70]
  stopping: fixed design, single governed run, seed 20260809
controls: [shuffled-pairing null (one-sided), uniform control (pooled 4 sigma), channel window, S-opaque record as internal comparison]
amendments: []
hash: sha256:5c55ae91fb3e7e858733b171aea878e6a39dc7f781015cc78c3556f2ec9e9d91
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2. CI re-checks the
committed JSON's self-consistency (tamper check) but cannot re-run Tier B.
