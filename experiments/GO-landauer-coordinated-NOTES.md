# GO-P-2026-050 — post-run notes (coordinated reset, operational) — **PASS 6/6**

Harness: [`landauer_coordinated.py`](landauer_coordinated.py) · prereg
[GO-P-2026-050](../prereg/GO-P-2026-050-landauer-coordinated.md) (sealed `7397e20`)
· result [`GO-landauer-coordinated.json`](../results/GO-landauer-coordinated.json)
· governed seed 20260809, Atlas. **Registered verdict: PASS — 6/6 gates.**

## Design

$X=(A,B,C)$ fair bits, $S=A$; record $M_1$ describes $U_1=(A,B)$, record $M_2$
describes $U_2=(B,C)$ (shared component $B$; $U_2\perp S$). Each record binned
and recovered in-bin by ML under independent reset $(\mathrm{bin},a^n)$,
coordinated reset (+ the other record's reconstruction), a shuffled-pairing
null, and a uniform control. Realized channel d̂ = 0.0631, predicted
coordination discount $\mathrm{gap}_{TC} = 1-h_2(\hat d*\hat d) = 0.476$
bits/symbol (the operational face of $\mathrm{TC}(U_1;U_2\mid S)=1$ bit at
$d\to0$).

## Per gated bar (thresholds in bits/symbol; grid step 0.15)

| gate | registered | result | pass? |
|---|---|---|:--:|
| C1 S-discount on M₁ | thr ≈ Rc − (1−h₂(d̂)) ± 0.20 | 0.95 vs 0.937 predicted | ✅ |
| C2 coordination saves on M₁ | gap ≥ 0.476 − 0.20 | **0.60** (0.95 → 0.35, grid floor) | ✅ |
| C3 coordination saves on M₂ | gap ≥ 0.476 − 0.20 | **0.45** (1.55 → 1.10) | ✅ |
| C4 shuffled null (one-sided) | no benefit from mismatched pairing | m₁ 1.25 ≥ 0.95; m₂ 1.55 = 1.55 (worse/equal, as theory allows) | ✅ |
| C5 channel realized | d̂ ∈ [0.03, 0.12] | 0.0631 | ✅ |
| C6 uniform control | pooled chance-relative, 4σ | within 4σ at every r_b | ✅ |

## Reading

Coordinated reset is operationally cheaper than independent reset by the
records' shared-structure information, on **both** records — including $M_2$,
whose own side information $S$ is useless ($U_2\perp A$): its reset residual
drops from the full description rate only when the *other consumer's record*
participates. Mismatched pairing saves nothing (and hurts, as ML with garbage
evidence should). This is the several-consumers corollary of Paper V read
operationally: shared consumer structure is conditional entropy that need not
be paid twice at reset — but only if the erasure protocol can use the other
records before they are cleared.

## Design lesson (logged in prereg, pre-seal)

The pilot's shuffled-null gate was first registered two-sided ("equals
independent") and the shuffled threshold landed *above* independent — correct
ML behavior. C4 was corrected to one-sided (no benefit) before sealing.
