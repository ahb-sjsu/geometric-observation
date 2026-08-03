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
