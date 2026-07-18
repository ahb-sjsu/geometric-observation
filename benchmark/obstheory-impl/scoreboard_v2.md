# ObsTheory-Impl / DOA — scoreboard

Task: derive the read operator and reproduce the DOA Gate-B flip + omission floor
from spec alone. Graded on the sealed held-out instance (M=16, θ0=-7°, κ=4).

| Rank | Model | Source | Score | Verdict | cos | flip | ratios | shuf | omit× |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `llama-33-70b` | API / open-weight (HF router) | 1/5 | PARTIAL/FAIL | 0.4036 | 6/6 | [1.01, 1.01] | 325 | 1.3 |
| 2 | `deepseek-v3-0324` | API / open-weight (HF router) | 0/5 | **ERROR** | — | — | — | — | — |
| 3 | `qwen25-coder-32b` | API / open-weight (HF router) | 0/5 | **ERROR** | — | — | — | — | — |
