# ObsTheory-Impl — implementing the theory as a benchmark

LLMs are asked to **independently implement an Observation-Theory result from a spec alone**
and are graded on a **hidden, sealed oracle**. This serves two purposes at once:

1. **Implementation-independent verification (R-IND).** If several models, each given only the
   specification (no reference code), independently reproduce a sealed prediction, the result is
   shown to be implementation-independent — an automated extension of the CHARTER's R-IND
   discipline. *"Reproduced by K independent from-spec reimplementations."*
2. **A contamination-resistant LLM benchmark.** "Implement this consumer-relative RD result and
   reproduce its sealed Gate-B predictions" is hard, well-specified scientific coding with an
   **objective oracle**. Because the registration pipeline manufactures fresh sealed instances
   (held-out params), the benchmark renews itself: keep the reference harnesses private, publish
   only specs, and every new prereg is a new clean task. Static coding benchmarks rot as solutions
   leak; this one does not.

It benchmarks a model's ability to *implement the theory*, not the theory's truth (already
established by the sealed runs). Keep the two framings distinct.

## The pilot task — DOA (GO-P-2026-031)

`spec_doa.md` describes direction-of-arrival on a ULA and the three-arm matched-bits protocol,
but **withholds the read operator** — deriving that the angle-informative direction is the
array-manifold derivative orthogonalized against the steering vector,
`ĝ = P_a^⊥ a'(θ0)` (not the signal subspace `span(A)`), is the actual test. A model that gets it
wrong shapes its arms wrong and the flip does not appear.

Each candidate returns a module `impl.py` with `solve(M, θ0, κ, s0sq_list, n, seed)`. The grader
(`grade.py`) runs it on the sealed held-out instance (M=16, θ0=−7°, κ=4) and scores five criteria:

| # | check | bar |
|---|---|---|
| 1 | geometry: cos(read_dir, analytic ĝ) | > 0.99 |
| 2 | flip: angle MSE invariant≤recon≤anti & recon min. reconstruction energy | 6/6 rates |
| 3 | effect floor: MSE step ratios track κ | median in [2.4, 6.4] |
| 4 | shuffled-consumer control (random read dir → no ordering) | flip ≤ 1 |
| 5 | omission floor (ĝ uncoded floors the angle) | ≥ 100× |

## Roster (both NRP open-weights and API)

- **Claude** — frontier API, via an isolated spec-only subagent (forbidden from reading the repo).
- **HF-router open-weights** — Qwen2.5-Coder-32B, Llama-3.3-70B, DeepSeek-V3 (`run_hf.py`, one HF token).
- **NRP open-weight** — Qwen2.5-Coder-7B on a Nautilus **A10 burst Job** running vLLM offline
  (`nrp/job.yaml` + `nrp/gen.py`): does work and exits (respects the no-idle rule). Launched and
  collected via the `atlas` skill's NRP module.

## Results

See `scoreboard.md` (regenerate with `python scoreboard.py`). Headline from the pilot: the
benchmark **discriminates** — the frontier model derives the read operator exactly (`cos=1.0`) and
reproduces the flip, while one-shot open-weights mostly produce code that crashes on the R²ᴹ↔Cᴹ
embedding / estimator numerics.

## Caveats & next iteration

- **One-shot vs. agentic.** This pilot is *single-shot* generation. A write-run-debug loop (feed
  the crash back, allow N fixes) would lift the open-weights, whose failures are mechanical. That
  is the natural next version and the fairer comparison.
- **Contamination.** Keep oracles (`grade.py`, the reference harnesses) private; publish only specs.
  The Zenodo deposits publish specs, not oracles.
- **NRP etiquette.** GPU work runs as burst Jobs (not idle pods); A100/H100 need the access form
  (hard-0 quota), so the fleet targets on-demand A10s. See the `atlas` skill `modules/nrp.md`.

## Files
```
spec_doa.md        the task given to models (answer-free)
grade.py           sandboxed grader -> models/<m>/score.json
run_hf.py          query HF-router open-weights
nrp/gen.py         in-pod vLLM offline generation
nrp/job.yaml       A10 burst Job manifest
scoreboard.py      aggregate score.json -> scoreboard.md/json
models/<m>/impl.py each candidate's implementation (+ score.json)
```
