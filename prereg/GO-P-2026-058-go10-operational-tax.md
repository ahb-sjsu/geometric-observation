# GO-P-2026-058 — GO-10 operational face: the complementarity tax as decode thresholds

Registers the **operational demonstration** of the GO-10 complementarity tax
(theory: [`paper/complementarity-tax.tex`](../paper/complementarity-tax.tex) v0.3,
verified VI-10; C3 harness GO-P-2026-055 ALL PASS 7/7): on materialized
codebook records — not information quantities — a joint record serving two
orthogonal consumers costs more to erase than the more expensive single
record, and the **rate-tax/work-tax gap** equals the side information the
reset context holds about the read plane, discounted to zero for a mismatched
context.

**Instrument** (GO-7/8/9 lineage, 053/054 conventions unchanged): 2-D Gaussian
source, orthogonal rank-one consumers (the note's Sec. 5 instance, θ=90°);
records = random-codebook quantizations (n=12, 2^10 codewords, D=0.35); the
joint record is the pair (M_A, M_B), reset by **coordinated-split binning**
(the eraser allocates bin bits across components — the operational form of the
note's per-coordinate reduction); decodable reset threshold thr = the binning
rate where the MAP-decode error curve crosses 0.25 (`thr_interp`), context ∈
{none, S = X₁+τZ, shuffled S′}. Measured: CT_R_op, CT_W_op, GAP_op =
CT_R_op − CT_W_op vs GAP_pred(s²) = ½log₂(1/(s²+(1−s²)d̂)).

**Scope.** One source family (Gaussian), one geometry (orthogonal); a pass
supports GO-10 at `[demonstrated]` — the binary second family and the
θ-sweep rate face are separate future registrations. Rate-side quantities here
are instrument-internal; novelty scope per the 055 attribution note (the tax
and work side are GO-10's novel content; the rate function itself is
attributed to the Gray/Xiao–Luo line).

**PILOT NOTE (logged, pre-seal — the power-first rule,
[`GO-KV-SERVING-POWER-NOTE.md`](../experiments/GO-KV-SERVING-POWER-NOTE.md), applied).**
One full pilot ran at seed 20260818, T=240 (`--pilot`; output in the session
transcript; deterministic given seed). Results: d̂ = 0.401/0.404;
thrA|∅=0.796, thrB|∅=0.797, thrAB|∅=1.551, CT_R=0.753; s²=0.2: disc_A=0.350
(pred 0.470), GAP=0.255 (pred 0.470), GAP_shuf=0.005; s²=0.5: disc_A=0.160
(pred 0.257), GAP=0.113 (pred 0.257), GAP_shuf=0.009; opacity ≤0.004; exact
binomial controls clean. **Design change made on the pilot, before this
seal (first seal — no amendment needed, disclosed for the record):** the
drafted W4 gate tested |GAP − GAP_pred| ≤ 0.18 — absolute tracking of the
*asymptotic* value — and failed, because the finite-n instrument realizes
0.44–0.54× of the asymptotic gap (cf. GO-9's known 0.56× realized fraction,
053/054). W4 was reshaped to the house fraction-window (GO-9's C2 pattern)
BEFORE sealing; every other drafted bar passed the pilot unchanged. Governed
design enlarged T 240→400 pre-commit (means unchanged; threshold noise
σ_thr ≈ 0.01–0.02 shrinks ~23%; 054 precedent). Pilot margins over the
sealed bars: W4 primary 1.36×, W4 secondary 1.47×, monotonicity 1.78×,
W2 ≥ 5σ, W5 ≥ 16×.

```yaml
id: GO-P-2026-058
date: 2026-08-03
retrospective: false
kind: operational demonstration (Tier B, CPU, pure numpy; GO-10's operational face, one source family)
claim: "On materialized codebook records for two orthogonal consumers of a Gaussian
  source, the measured rate-tax/work-tax gap CT_R_op - CT_W_op is a substantial
  fraction of the predicted plane side information (1/2)log2(1/(s^2+(1-s^2)d^)),
  monotone in the quality of the reset context, and zero for a shuffled context;
  the single-record discount tracks the same formula and the S-opaque record is
  undiscounted."
harness: experiments/go10_operational_tax.py   # GOVERNED seed 20260820, T=400; pilot seed 20260818, T=240, disclosed above
prediction:
  W1_channel_window: d^_A and d^_B in [0.28, 0.48]   [carried byte-identical from 054's C5]
  W2_discount_tracks: |disc_A - (1/2)log2(1/(s^2+(1-s^2)d^_A))| <= 0.22 at both
    s^2 in {0.2, 0.5}   [pilot deviations 0.120, 0.097 -- systematic finite-n
    shortfall; a zero discount fails the gate by construction]
  W3_opacity: |thr_B|none - thr_B|S| <= 0.12 at both s^2   [pilot <= 0.004]
  W4_tax_gap: 0.40*GAP_pred(0.2) <= GAP_op(0.2) <= GAP_pred(0.2) + 0.15
    AND GAP_op(0.5) >= 0.30*GAP_pred(0.5)
    AND GAP_op(0.2) - GAP_op(0.5) >= 0.08
    [pilot: 0.255 in [0.188, 0.620]; 0.113 >= 0.077; mono 0.142]
  W5_shuffled_null: |GAP_shuf| <= 0.15 and disc_A(S') <= 0.15 at both s^2
    [pilot <= 0.009]
  W6_uniform_control_exact: every (record, context, r_b) uniform-control cell
    consistent with chance under the EXACT two-sided binomial test at alpha=5e-4
    (the 051/053 instrument lesson, applied from the start)
  reported_not_gated: the coordinated-split allocation at threshold (predicted to
    tilt bin bits toward the S-opaque record under S); CT_W_op and CT_R_op point
    values; realized-fraction GAP_op/GAP_pred for comparison with GO-9's 0.56x.
falsification: W4's lower bounds failing kills the operational tax-gap claim (the
  novel face of GO-10); W5 failing kills context-specificity (the discount would
  not be information-bearing); W2 failing kills the single-record discount
  mechanism the gap decomposes through; W1 or W6 failing voids the run as an
  instrument fault (logged, rerun only under a dated amendment). Any gate miss is
  reported at full prominence; GO-10 remains [predicted] on a miss.
design:
  n: 12
  trials: 400              # enlarged from the 240-trial pilot, pre-committed
  D_target: 0.35
  s2_grid: [0.2, 0.5]
  rb_single: [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05]
  rb_joint: [0.85, 1.00, 1.15, 1.30, 1.45, 1.60, 1.75, 1.90, 2.05]
  stopping: fixed design, single governed run, seed 20260820, after the one
    disclosed pilot (seed 20260818); no further pilots or attempts under this ID
controls: [shuffled context S' (W5), S-opaque record B (W3), uniform-member
  control with exact binomial (W6), channel window (W1), split allocation
  reported (instrument transparency)]
amendments: []
hash: sha256:69846466f1906dae6b8a18a5ed5f57de216d672f065ad06640fa4ab135e64460
```

## Falsification

Any gate miss is reported at full prominence per PROTOCOL Rule 1.2 and leaves
GO-10 at `[predicted]` (its theory class from GO-P-2026-055); a pass supports
`[demonstrated]` on one source family. The successor registrations named in the
GO-P-2026-055 operational-face sketch (binary family; θ-sweep rate face) carry
their own future IDs and bars.
