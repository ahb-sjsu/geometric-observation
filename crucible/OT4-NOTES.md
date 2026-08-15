# OT-4 notes — FAIL: the degradation is real, and drift is not its mechanism

**Verdict: FAIL as sealed** (A0 ∧ A1 ∧ B1 ∧ T\* ∧ D1 required; A1, B1,
and T\* failed; Stage D correctly never ran — its gate is A0∧A1∧B1).
Record: `readscope/calibration/records/c12-longgen-drift-sym.json`
(n = 40, the signed nf4-SYM amendment).

| stage | result |
|---|---|
| A0 (phenomenon) | **PASS** — free-running ROUGE gap **+13.39** (bar 5.0); the amendment targeted the right codebook |
| A1 (survives teacher forcing) | **FAIL** — median rise +0.25 nats on a base of 4.34 (≈6%), sign test p = 0.42: severing the feedback loop removes the *consistent* growth |
| B1 (orientation does work) | **FAIL** — positional growth −0.015 vs rotated +0.005, margin −0.020 against a 0.05 bar: the error's orientation relative to the moving operator does nothing |
| B2 | FAIL (ρ = −0.13, p = 0.45; pre-flagged underpowered, and null) |
| T\* (sealed band [32,192] for doubling) | **FAIL/moot** — the teacher-forced excess never approaches doubling anywhere in 512 tokens |
| D1 (intervention) | **not run** — gate not met; `c12_stage_d.py` stands implemented and unused, as the rules require |

**What the experiment actually established** (and it is a real result):
the symmetric-codebook long-generation collapse is **H_compound** — a
large *constant* injected error (≈4.3 nats of teacher-forced excess
from the first token) that the model then compounds through its own
autoregressive feedback — and **not H_drift**. The declaration
pre-wrote this outcome's meaning and it now executes: *"If A1 fails,
H_drift contributes essentially nothing to this curve, C-11c is
demoted to a real effect that is not this mechanism, and that is the
result."* C-11c's operator drift remains measured and null-corrected;
its claim to explain TurboQuant's degradation is dead.

**For P4:** the principle (operators move; staleness is priced) keeps
its direct measurements (C-11c, OT-7's drift-distance row). Its *owed
prediction* — that drift explains a real production degradation —
is refuted. The queued post-campaign revision inherits both facts.
