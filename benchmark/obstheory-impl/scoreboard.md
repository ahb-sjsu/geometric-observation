# ObsTheory-Impl / DOA — scoreboard

Task: derive the read operator and reproduce the DOA Gate-B flip + omission floor
from spec alone. Graded on the sealed held-out instance (M=16, θ0=-7°, κ=4).

| Rank | Model | Source | Score | Verdict | cos | flip | ratios | shuf | omit× |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `claude` | API / frontier (Claude, isolated spec-only subagent) | 4/5 | PARTIAL/FAIL | 1.0 | 6/6 | [4.08, 3.92] | 3 | 2086.8 |
| 2 | `deepseek-v3-0324` | API / open-weight (HF router) | 0/5 | **ERROR** | — | — | — | — | — |
| 3 | `llama-33-70b` | API / open-weight (HF router) | 0/5 | **ERROR** | — | — | — | — | — |
| 4 | `nrp-qwen25-coder-7b` | NRP / open-weight (A10 burst Job, vLLM) | 0/5 | **ERROR** | — | — | — | — | — |
| 5 | `qwen25-coder-32b` | API / open-weight (HF router) | 0/5 | **ERROR** | — | — | — | — | — |
