# Hubness–Bell probe — `[exploratory]`, no sealed prereg, not claim-bearing

Harness: [`hubness_bell_simulator.py`](hubness_bell_simulator.py) ·
result [`GO-hubness-bell-exploratory.json`](../results/GO-hubness-bell-exploratory.json)
· seed 20260816, 168 phase-2 configurations, CPU.

**Status under PROTOCOL §1: `[exploratory]` only.** No prediction registry entry
precedes it, so it cannot support any claim, cannot enter the umbrella, and gets no
ledger row. It was run to size up a conjecture, and this file is the whole record.

## The conjecture

That *query-conditioned hubness* — hubness as a property of the retrieval experiment
(corpus measure, query measure, metric, k) rather than of the corpus, which is the
openvector-bench result — might supply a mechanism for Bell-inequality violation
without action at a distance, by making the effective latent ensemble
setting-dependent: $\rho_{xy}(\lambda)\ne\rho(\lambda)$.

## Design

Latent unit vectors on $S^{d-1}$ with tunable density skew (concentrated core +
uniform shell, plus Zipf atom weights); hubness measured as skewness of the
$k$-occurrence count $N_k$. Local outcomes $A_x=\mathrm{sign}(q^A_x\cdot\lambda)$,
$B_y=-\mathrm{sign}(q^B_y\cdot\lambda)$.

- **Phase 1** (settings-independent sampling): a **falsification net on the
  simulator**, not an experiment — $|K(\lambda)|=2$ pointwise is a theorem, so
  $S\le2$ for any $\rho$ whatever its hubness.
- **Phase 2**: setting-dependent retention $\eta_A(x,\lambda)\eta_B(y,\lambda)$
  (logistic in query alignment) with coincidence postselection; sharpness swept to
  400.

## Results

| | |
|---|---|
| **Phase 1 net** | max $S=\mathbf{2.00000}$, **0/48 violations** — and exactly *at* the classical bound, so the net is tight, not slack. The simulator is validated. |
| Phase 2 max $S$ | 2.6173 (a prior RNG realization gave 2.8205) |
| **Every violation is low-efficiency** | 129/168 configs exceed 2; **all of them at detection efficiency < 0.40**. No configuration anywhere in the sweep reached the 0.667 fair-sampling threshold, so there is no data point at which a violation could be legitimate. |
| **Counting all trials destroys it** | mean $S_{\rm all\,counted}=0.44$ against mean $S=2.10$; at the max-$S$ config, $S$ falls **2.617 → 0.019**. |
| **It signals** | no-signalling residual up to **0.77** (0.62 at max $S$): Alice's conditioned marginal openly depends on Bob's setting. |
| Loose bound | $S\le2+8\delta$ held **168/168** with the exact shift estimator |

**The hubness link does not hold up.** Correlations of CHSH excess with:
hub skew **+0.258**, exact contextual $D_{\rm TV}$ **−0.027**,
$I(\Lambda;X,Y)$ **−0.302** (negative), retention sharpness **−0.343**.
So the excess in this family is driven by the retention geometry's interaction with
the query plane — not by aggregate hubness, and *not* by contextual shift either.
$I(\Lambda;X,Y)$ trending the wrong way is the most direct blow to the
"contextual hubness" formulation: more query–source mutual information gave *less*
violation here.

**My own predicted dissociation also failed.** I expected contextual shift to
dominate hub skew; neither explains much ($r^2\le7\%$).

## Instrument lesson

The first pass estimated contextual shift by histogramming the latent distribution
along one random axis in up to 128 dimensions. That proxy underestimated the shift
(max 0.74 vs exact 0.88), injected noise, and let the loose bound fail 3/168 —
i.e. a bad instrument was manufacturing a null. Replaced with the **exact** shift
computed in closed form from the retention weights
($\rho_{xy}\propto w\,\eta_A\eta_B$ over the atoms), after which the bound holds
everywhere. Same failure mode as the Landauer campaign's control gates: the physics
predictions kept holding while the *instruments* needed fixing.

## Verdict

The **reframing** is legitimate and worth keeping as vocabulary: measurement settings
act as queries, and query-relative accessibility is a natural language for Bell's
measurement-independence assumption. That is a real conceptual bridge from the
openvector-bench query-relative hubness result to the least intuitive Bell premise.

The **mechanism** is not there. In this family the construction reproduces the
detection loophole (Pearle 1970; Gisin & Gisin) and additionally **fails
no-signalling catastrophically**, which disqualifies it as a local causal account
before the loophole objection is even reached. Nothing here approaches the actual
bar: derive $-\cos\theta$, preserve no-signalling *by construction*, and derive
$2\sqrt2$ rather than merely exceeding 2.

**Scope limit, stated plainly:** the retention family (logistic in query alignment)
is one arbitrary choice, so this bounds *that* family, not all contextual-hubness
models — adversarial postselection constructions are known to reach $S=4$. Also,
never exceeding Tsirelson here is **not** evidence of a Tsirelson bound: the two RNG
realizations gave 2.82 and 2.62, so the ceiling is realization-dependent.
And one claim in my first analysis pass was wrong and is corrected here: I said the
contextual shift was saturated and therefore could not covary with $S$; the exact
estimator shows it ranges 0.083–0.883, so the near-zero correlation is a real null,
not a ceiling artifact.

---

# GO-P-2026-057 — Bell geometry audit (constraint-first, **sealed**): ALL PASS 6/6

Harness [`bell_geometry_audit.py`](bell_geometry_audit.py) · prereg
[GO-P-2026-057](../prereg/GO-P-2026-057-bell-geometry-audit.md) (sealed `6e825d8`)
· result [`GO-bell-geometry-audit.json`](../results/GO-bell-geometry-audit.json)
· as-executed [`…-asexecuted.json`](../results/GO-bell-geometry-audit-asexecuted.json)
· seed 20260817, 72 P0 configurations + 72 controls, CPU.

Unlike the exploratory probe above, this one was **designed from the constraints**
and preregistered with an **expected null**.

## The null, cleanly

| test | result |
|---|---|
| **T1** P0 respects the bound | **max S = 2.00000** across all 72 configs (tol 0.0089) ✅ |
| **T2** no-signalling (by construction) | max residual **0.00464**, pure finite-sample ✅ |
| **T5** geometry irrelevant | **corr(S, hub skew) = −0.036** ✅ |
| **T3** angular law is the sawtooth, not the cosine | RMS vs scaled sawtooth 0.20–0.45 **<** RMS vs −cos θ 0.61–0.72 ✅ |
| **T6** same data, postselected instead of counted | **2.7308** ✅ |
| **T4** positive controls fire | P1 **2.748**, P2 **2.386**, P3 **3.174** ✅ |

**Dimension 3→128, Zipf skew, concentrated cores, hub skew, query concentration:
none of it moves S off 2.00000.** The correlation with hub skew is −0.036. This is
the computational demonstration that retrieval geometry does not weaken Bell.

**The controls are what make the null mean anything.** Break one premise and the
instrument sees it immediately: deleting non-detections gives 2.748 with
no-signalling *intact* (0.0022) — the signature of a pure accounting artifact;
measurement dependence gives 2.386; broken locality gives 3.174 with a
no-signalling residual of **1.03**, i.e. it announces itself. Any future geometric
conjecture must declare which column it occupies.

**The before/after that makes the point sharpest:** identical model, identical
geometry, identical trials — S = **2.00000** counting everything, **2.7308**
deleting non-detections. The entire "violation" is the accounting.

## ⚠ Test-wiring correction, on the record

As executed the run scored **5/6**: T4 failed because the verdict read
`S_all_counted` for **all** controls, including P1 — whose premise-break *is*
deleting non-detections, so its violation cannot appear in an all-data score. That
was self-contradictory wiring on my part, not a physics result, and the substantive
requirement behind T4 was already independently met by T6 (2.7308 from P0's own
data), P2 and P3. Fixed to read `S_postselected` for P1 only; **rerun at the same
seed reproduced the simulation data bit-identically** (P0, controls and angular
blocks all compare equal), so only the verdict field changed. The as-executed JSON
is committed unchanged.

That is now the **seventh** instrument-side defect in this session against zero
failed physics predictions — the standing lesson: unit-test the *scoring* against
each arm's definition, not just the simulation.

## Caveats

- P2's crude tilt breaks no-signalling too (residual 0.27), so it does not isolate
  measurement dependence as cleanly as Hall-type models do; it is a positive
  control, not a faithful superdeterministic model.
- Bounds **this** preregistered family only. Adversarial postselection
  constructions reach S = 4.
- Nothing here is new physics. The contribution is an audited, reusable
  falsification harness plus the explicit geometric null.

## Status

`[demonstrated]` as a **negative/harness** result. Per PROTOCOL Rule 1.2 it belongs
in Honest Negatives, not the umbrella. It supports the note the author sketched —
*"Hubness Does Not Weaken Bell: A Retrieval-Geometric Audit of Setting-Dependent
Sampling"* — for which the deliverables now exist: the analytic argument, the
geometric null, the postselection demonstration, the no-signalling failure, the
misleading-coarse-measure lesson, and the harness itself.

---

## Why the audit's baseline is exactly 2.00000 (asked at review, answered from the code)

A reviewer correctly objected that Bell's argument gives an inequality, so a
generic local model sits strictly inside the bound, and equality to five decimals
invites suspicion of clipping or a construction that forces the answer.

The reason is that **the CHSH integrand is a constant for the registered setting
geometry.** All four measurement directions lie in one plane, and a sign response
depends only on the angle of the state's projection into that plane. With one
side's directions at 0 and π/2 and the other's at ±π/4, the combination
K(φ) = A₀(B₀+B₁) + A₁(B₀−B₁) equals **−2 in every one of the eight sectors of
width π/4**, so it is independent of φ and therefore of the state distribution
entirely.

Verified directly:

| check | result |
|---|---|
| distinct values of K over 2e6 sampled angles | **{−2}**, one element |
| ambient d = 3, 8, 128 | unique K = {−2}, S = 2.0000000000 |
| strongly anisotropic cored distribution, d = 32 | unique K = {−2}, S = 2.0000000000 |

Two consequences, both now stated in the article. The measured null is a check
that the code implements the intended construction rather than a discovery, since
the value is forced. And the audit is **maximally sensitive**, because the baseline
carries no statistical scatter at all, so any departure from local realistic
behaviour moves the combination away from a noiseless reference instead of a noisy
one. That is a desirable property for a falsification net and was not by design.

## Other review items applied to the article

- **Efficiency threshold corrected.** The two thirds figure is not a general
  requirement. For the symmetric case with maximally entangled states the critical
  value is 2(√2−1) ≈ 0.83 (Garg and Mermin), while two thirds belongs to Eberhard
  style tests using nonmaximally entangled states in the Clauser and Horne form.
  The conclusion is unchanged because every violating configuration sat below 0.40.
- **Formal section added** defining the all trials statistic with registration
  indicators and the coincidence conditioned measure
  ρ_xy ∝ ρ·η_A(x,·)·η_B(y,·), which is where query dependent accessibility enters.
- **Sealed and exploratory evidence separated** into a status table.
- **Two claims narrowed.** "The entire excess comes from which trials were counted"
  is now scoped to the paired rescoring, and the claim about the only route past
  the bound is scoped to the model family under test, with the controls noted as
  demonstrating other routes exist.
- **Related work section and references added**, with a standing note that the
  bibliographic details need checking against published records before submission.
- **Subtitle sharpened** to the reviewer's wording but rendered without a colon,
  since the standing prose standard forbids colons in headings.
