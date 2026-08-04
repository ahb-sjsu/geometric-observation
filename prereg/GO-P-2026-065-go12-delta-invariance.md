# GO-P-2026-065 — GO-12 opening control: the staleness tax is access-width, not delay

First registration out of the GO-12 problem statement
([`paper/go12-process-region.tex`](../paper/go12-process-region.tex),
Remark 1): decides the causal-origin question for the staleness tax
before any heavy process theory is attempted.

**The dichotomy under test.** Model: V_t stationary AR(1) (pole a,
unit variance); Y_t = ρV_t + N_t (unit variance); aged noisy context
S_t = V_{t−Δ} + U_t, Var U = τ².

- **Path access ⇒ zero staleness tax.** If the eraser sees the whole
  context path, pure delay is information-free: in the circulant
  embedding the cyclic shift commutes with every circulant covariance,
  so Σ_{Y|S} is **exactly** Δ-invariant at every finite n — an
  analytic-zero control of the 061/062 kind; the airtight general form
  is the recoding identity (Y,V,S^Δ) =d (Y,V,P^Δ S⁰), which makes every
  σ(S)-measurable conditional functional invariant. Finite Toeplitz
  windows leak only edge terms, O(1/n) at fixed Δ (empirically ≈ linear
  in Δ over the probed range).
- **Slice access ⇒ the static staleness tax, with the encoder's access
  width mattering too** (pairing corrected by the R-IND-5 pass, which
  refuted the first draft's formula/scope pairing):
  - **(B) Single-letter records** built from the time-t variables
    (Y_t, V_t) — GO-8's per-symbol-codebook situation — pay the GO-11
    static quadratic-root CR function at **ρ unchanged,
    s → s/a^{2Δ}** (τ²_eff = (τ² + 1 − a^{2Δ})/a^{2Δ}); derivation:
    S = a^Δ·V_t + (W + U) with W ⊥ (Y_t, V_t), then an MI-invariant
    rescaling lands in the static normal form (AR(1) reversibility
    covers the past-slice direction; for future context — "erased Δ
    later" — the same numbers hold by reversibility).
  - **(A) Records granted the context-epoch latent** V_{t±Δ} (the
    path-encoder single-record benchmark: by pair sufficiency the whole
    path collapses to (Y_t, V_{t±Δ})) pay the static quadratic at
    **ρ_eff = ρ·a^Δ, τ² unchanged** — strictly smaller, by up to
    ≈0.05 bits on the probe grid.
  - Both are strictly increasing in Δ with the common Δ→∞ limit
    ½log₂(1/D). L(D,Δ) here is a single-record benchmark: block records
    amortized across symbols achieve strictly smaller per-symbol
    coordinates.

Scope: the path arm is a statement about σ(S)-measurable conditioning
(the recoding identity (Y,V,S^Δ) =d (Y,V,P^Δ S⁰)) and holds for any
record; the slice arm is single-record, with the two encoder scopes (A)
and (B) gated separately and their strict ordering gated at the probe
point.

Governs `experiments/go12_delta_invariance.py` (numpy+scipy, single
run; sentinel `===GO12DI-JSON===` with `===END===`; summary flag
`GO12DI_supported`).

```yaml
id: GO-P-2026-065
date: 2026-08-04
retrospective: false
kind: theory-control (C3: analytic-zero control + static-theory reduction, deciding GO-12's causal-origin question)
claim: "Staleness is an access-width phenomenon, at the eraser AND the
  encoder: with full context-path access, pure-delay aging is
  information-free -- the recoding identity (Y,V,S^Delta) =d
  (Y,V,P^Delta S^0) makes every sigma(S)-measurable conditional
  functional exactly Delta-invariant (circulant-exact; O(1/n) edge
  leakage on finite windows at fixed Delta) -- so noncausal block
  erasure pays zero staleness tax; with time-local slice access,
  single-letter (Y_t,V_t)-records pay the static quadratic at rho
  unchanged, s -> s/a^{2Delta}, while records granted the
  context-epoch latent pay the strictly smaller rho -> rho a^Delta
  value; both strictly increasing in Delta with common limit
  (1/2)log2(1/D). GO-8's age-dependence originates in access width,
  not delay."
harness: experiments/go12_delta_invariance.py   # GOVERNED seed 20260915; pilot-2 seed 20260914, disclosed below
power: |
  Deterministic analytic-reproduction gates; per PROTOCOL 5.1 the bars
  carry pilot margins (pilot-2, the harness as sealed): s1 bar 1e-12 vs
  3.3e-16 (~3000x); s2 smallness bar 0.05 vs 0.0127 (3.9x), ratio
  window [0.35, 0.65] vs 0.5000 (dead-center); s3 gap bars 1e-6 vs
  1.9e-13 (A) and 2.1e-13 (B), limit bar 1e-9 vs 2.2e-16, probe-gap bar
  0.01 vs 0.0529 (5.3x); s4 margin bar 0.05 vs 0.170 (3.4x). Every
  margin >= 1.3x.
pilot: |
  TWO pilots, both disclosed. Pilot-1 (seed 20260912, 1.6 s, ALL PASS)
  ran an earlier harness draft whose s3 tested only the (A) pairing;
  the R-IND-5 pass then REFUTED the draft claim's formula/scope pairing
  (rho -> rho a^Delta asserted for single-letter records understates
  that tax by up to ~0.05 bits), so s3 was rebuilt to gate both
  pairings and their ordering -- a claim correction caught before
  seal, not a bar recalibration. Pilot-2 (seed 20260914, the harness
  as sealed, 2.4 s): ALL PASS with drafted bars unchanged. Values:
  circulant invariance 3.3e-16; edge leakage 0.0127 -> 0.0063, ratio
  0.5000000000; s3 gap (A) 1.9e-13, gap (B) 2.1e-13, both monotone,
  ordering L_B >= L_A everywhere, probe gap 0.0529 (reproducing the
  verifier's maximum), limit 2.2e-16; path 0.2138 vs slice 0.0437.
prediction:
  s1_circ_invariance: max |Sigma_{Y|S}(Delta) - Sigma_{Y|S}(0)| <= 1e-12
    over Delta in {1,4,16}, two instances (a,rho,tau2,n) =
    (0.8,0.7,0.4,96) and (0.55,0.45,1.1,128)
  s2_edge_leakage: finite-window per-symbol information deviation
    |M_128(8) - M_128(0)| <= 0.05 bits AND the n-doubling ratio
    d_256/d_128 in [0.35, 0.65] (O(Delta/n) scaling)
  s3_slice_tax: BOTH pairings vs their own 40-start direct channel
    programs at Delta in {0,1,2,4,8}, two instances -- (A) T=(Y_t,
    V_{t+/-Delta}) at (rho a^Delta, tau2) and (B) T=(Y_t,V_t) at
    (rho, s/a^{2Delta}) -- gaps <= 1e-6 bits each; both strictly
    increasing in Delta; L_B >= L_A at every grid point; strict
    encoder-access gap >= 0.01 bits at the probe point
    (a,rho,tau2,D,Delta) = (0.9,0.95,0.25,0.25,1); rho_eff -> 0 limit
    within 1e-9 of (1/2) log2(1/D)
  s4_ordering: per-symbol path information exceeds slice information by
    >= 0.05 bits at (a,rho,tau2) = (0.8,0.7,0.4), Delta = 4
falsification: s1 failing refutes the Delta-invariance lemma (and
  Remark 1 of the GO-12 statement); s2 outside its window refutes the
  edge-term account of finite-window deviation; s3 failing refutes the
  corresponding slice-to-static reduction (or the static Thm-2
  quadratic, already netted by 060 -- a cross-contradiction to
  investigate), and a probe gap below 0.01 refutes the encoder-access
  strictness; s4 failing refutes the eraser-access ordering.
  Instrument-vs-physics per PROTOCOL 5.1: SLSQP non-convergence in s3
  is a logged instrumentation miss (dated-amendment rerun only).
design:
  stopping: fixed design, single governed run, seed 20260915, after the
    two disclosed pilots (20260912 on the refuted draft, 20260914 on
    the harness as sealed); no further pilots or attempts under this ID
  runtime: ~2 s single-threaded (pilot-2: 2.4 s)
controls: [analytic-zero circulant control (s1), O(1/n) scaling gate
  rather than a bare smallness gate (s2), independent direct
  optimization against BOTH closed forms + encoder-access ordering with
  a strict probe gate (s3), eraser-access information ordering (s4)]
amendments: []
hash: sha256:db8b84d14a5b73b106de78e19ea70ddcde908383efb6f58d7657d14fbccffaba
```

## Falsification

A pass upgrades GO-12's Remark 1 to a proved-and-netted lemma and
grounds Conjecture 2's causal-origin claim; a s1/s2 fail kills the
spectral program's premise cheaply, which is the point of running this
first.
