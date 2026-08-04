# GO-P-2026-059 — GO-10 operational face, second source family (binary)

Registers the **binary replication setting** of the GO-10 complementarity tax
(first family: Gaussian orthogonal, [GO-P-2026-058](GO-P-2026-058-go10-operational-tax.md)
**ALL PASS 6/6**). A pass here puts GO-10's operational face on **two
independent source families** and supports promotion to `[replicated]` per the
§1 bar (subject to the ledger's usual review); a miss leaves GO-10 at
`[demonstrated]` and is reported at full prominence.

**Setting.** Two independent fair bits per symbol; consumer A reads the U bit,
B reads the V bit. Records = random binary codebooks at Hamming distortion
$\hat d$ (GO-7 043/045 lineage; n=24, $2^{13}$ codewords, target d=0.11).
Reset side information $S = U \oplus W$, $W\sim\mathrm{Bern}(q)$,
$q\in\{0.1, 0.25\}$, eraser-only. Joint record = the pair $(M_A, M_B)$, reset
by coordinated-split binning; thresholds, contexts, controls, and split
semantics are byte-identical in shape to the sealed 058 instrument (binary
MAP decode = min Hamming distance to $S$; integer scores tie frequently,
resolved uniformly by `strided_argmin` exactly as in 053/054).

**Binary floor, derived (the pre-seal derivation the 055 sketch required).**
The record's codeword and the context form the BSC cascade
$\hat U \xrightarrow{\hat d} U \xrightarrow{q} S$ with crossover
$\hat d * q = \hat d(1-q) + q(1-\hat d)$, so the per-symbol side information
about A's record is $I(\hat U;S) = 1 - h_2(\hat d * q)$, and
$$\mathrm{thr}_{A|S} \approx R_c - \bigl(1-h_2(\hat d * q)\bigr),\quad
\mathrm{thr}_{B|\cdot}\approx R_c,\quad
\mathrm{GAP}_{\rm pred}(q) = 1 - h_2(\hat d * q)\ \to\ 1\ \text{bit as } \hat d, q\to0.$$
This is the same mechanism GO-8 verified operationally (its thresholds track
$R_c-1+h_2(\hat d * q_t)$); the new content here is the joint record and the
tax quantities, mirroring 058.

**PILOT NOTE (logged, pre-seal; power-first rule).** One pilot at seed
20260821, T=240 (`--pilot`; output in the session transcript; deterministic).
(i) **Instrument crash found and fixed mid-pilot:** the coordinated-split
loop's best-split tracker used `e < best_err` with `best_err = 1.0`, which
never fires when every split's error is exactly 1.0 (binary chance decode at
low joint $r_b$, shuffled context) — fixed to `is None or` with
first-split-wins tie semantics, matching 058's intent. The same initializer
pattern is **latent in the sealed 058 harness** where it cannot fire
(continuous scores always decode something, and 058's committed verdict is
CI-re-derived deterministically on the same path) — noted here for the
record; the 058 artifact is untouched. (ii) **Pilot values** (post-fix, full
run): $\hat d$ = 0.1302/0.1307; thrA|∅=0.516, thrB|∅=0.512, thrAB|∅=1.021,
CT_R=0.504; q=0.1: disc_A=0.257 (pred 0.270), GAP=0.208 (pred 0.270, 0.77×
realized — sharper than the Gaussian family's 0.57×), GAP_shuf=−0.003;
q=0.25: disc_A=0.089 (pred 0.101), GAP=0.039 (pred 0.101), GAP_shuf=−0.004;
opacity ≤0.005; exact-binomial controls clean. (iii) **Two bars calibrated on
the pilot, before this seal:** B2 tightened 0.22→0.12 (binary tracking is
~20× tighter than the bar; 0.12 is the largest bar that still fails a zero
discount at q=0.1); B4's secondary lowered 0.30×→0.20× of prediction
(measured 0.039 vs a 0.30× bar of 0.030 was a 1.29× margin — the 052 failure
mode; 0.20× gives 1.9× and still fails a zero gap). Every other bar passed
the pilot unchanged. Pilot margins over the sealed bars: B4 primary 1.9×,
B4 secondary 1.9×, monotonicity 2.8×, B2 ≥9×, B5 ≥37×.

```yaml
id: GO-P-2026-059
date: 2026-08-04
retrospective: false
kind: operational replication (Tier B, CPU, pure numpy; GO-10's second source family)
claim: "On materialized binary codebook records for two independent-bit consumers,
  the measured rate-tax/work-tax gap CT_R_op - CT_W_op is a substantial fraction of
  the derived binary floor 1 - h2(d^*q), monotone in the reset-context quality q,
  and zero for a shuffled context; the single-record discount tracks the same
  formula tightly and the S-opaque record is undiscounted."
harness: experiments/go10_operational_tax_binary.py   # GOVERNED seed 20260822, T=400; pilot seed 20260821, T=240, disclosed above
prediction:
  B1_channel_window: d^_A and d^_B in [0.06, 0.18]   [pilot 0.130/0.131]
  B2_discount_tracks: |disc_A - (1 - h2(d^_A * q))| <= 0.12 at both q
    [pilot deviations 0.013/0.012; bar chosen as the largest that fails a
    zero discount at q=0.1; at q=0.25 the teeth are in B4]
  B3_opacity: |thr_B|none - thr_B|S| <= 0.12 at both q   [pilot <= 0.005]
  B4_tax_gap: 0.40*GAP_pred(0.1) <= GAP_op(0.1) <= GAP_pred(0.1) + 0.15
    AND GAP_op(0.25) >= 0.20*GAP_pred(0.25)
    AND GAP_op(0.1) - GAP_op(0.25) >= 0.06
    [pilot: 0.208 in [0.108, 0.420]; 0.039 >= 0.020; mono 0.169]
  B5_shuffled_null: |GAP_shuf| <= 0.15 and disc_A(S') <= 0.15 at both q
    [pilot <= 0.004]
  B6_uniform_control_exact: every (record, context, r_b) uniform-control cell
    consistent with chance under the EXACT two-sided binomial test, alpha=5e-4
  reported_not_gated: split allocation at threshold (tilt toward the S-opaque
    record); realized fractions GAP_op/GAP_pred for cross-family comparison
    (Gaussian 058: 0.57x/0.37x; pilot here: 0.77x/0.39x).
falsification: B4's lower bounds failing kills the binary tax-gap claim and blocks
  [replicated]; B5 failing kills context-specificity; B2 failing kills the derived
  binary floor (and with it the cross-family reading); B1 or B6 failing voids the
  run as an instrument fault (logged; rerun only under a dated amendment). Any
  miss is reported at full prominence; GO-10 stays [demonstrated] on a miss.
design:
  n: 24
  trials: 400              # enlarged from the 240-trial pilot, pre-committed
  d_target: 0.11
  q_grid: [0.1, 0.25]
  rb_single: [0.10, 0.175, 0.25, 0.325, 0.40, 0.475, 0.55, 0.625]
  rb_joint: [0.55, 0.65, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25]
  stopping: fixed design, single governed run, seed 20260822, after the one
    disclosed pilot (seed 20260821); no further pilots or attempts under this ID
controls: [shuffled context S' (B5), S-opaque record B (B3), uniform-member
  control with exact binomial (B6), channel window (B1), split allocation
  reported]
amendments: []
hash: sha256:6a96aba33792ddf79419f7fe519878a708f9f7feaee52d1dfd5ce14d1e3b5ef7
```

## Falsification

Any gate miss is reported at full prominence per PROTOCOL Rule 1.2; GO-10
remains `[demonstrated]` (Gaussian family only). A pass puts the operational
face on two independent source families — the `[replicated]` promotion is then
made in the ledger with the realized-fraction comparison carried alongside.
The θ-sweep rate face remains a separate future registration.
