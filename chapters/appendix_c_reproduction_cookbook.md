# Appendix C — Reproduction Cookbook

Every headline number in this book is reproducible from committed scripts. This appendix
says how, without reproducing the repository's own READMEs. The governing facts: results
are sealed-before-run (Chapter 15), archived at the DOI deposit, and re-run by CI. A
reader who wants to *verify* rather than *trust* starts here.

## Where everything lives

- **Ledger of record:** `claims/LEDGER.md` — every table/figure ID in the book resolves
  to a row; the row names its registry, notebook, result JSON, class, and replications.
- **Registry accounting:** `claims/REGISTRY-ACCOUNTING.md` — the gap-free ID disposition
  table (Appendix D), the commit-ordering audit, and the statistical audit.
- **Sealed preregs:** `prereg/GO-P-2026-###-*.md` — each hashed and git-committed before
  its run.
- **Scripts:** `experiments/*.py` — one driver per GO row.
- **Results:** `results/*.json` — per-run outputs (note: `results/` JSONs are tracked
  even though `*.json` is broadly gitignored; force-added).
- **DOI archive:** Zenodo concept DOI `10.5281/zenodo.21423315` — the externally-anchored
  snapshot of preregs, results, and harnesses (REG-3).

## The general recipe

1. **Read the ledger row** for the claim you want to check; note its registry ID, script,
   and result JSON.
2. **Verify the seal predates the run.** Use the commit-ordering audit (Appendix D):
   `git merge-base --is-ancestor <seal-commit> <result-add-commit>` must return true. The
   binding timestamp is the git ancestry, not the file mtime.
3. **Re-run the script** for that row from a clean environment (below). Fixed seeds make
   the governed rows deterministic on CPU where the theory harnesses are concerned.
4. **Compare** against the committed result JSON and the sealed bar in the prereg. A pass
   is a pass only if it clears the bar written *before* the run.

## Environments

- **Theory / C3 harnesses (COST, Appendix B):** pure, CPU-reproducible, fixed-seed;
  CI-run. No GPU. These are the falsification nets — they are meant to be cheap to re-run.
- **CPU experiment rows** (spectral, synthetic, retrieval, classifier sweeps): standard
  scientific-Python; pin versions from the repo lockfile.
- **GPU rows** (real-LLM Gate-B: Llama-3.2-3B keys, GO-P-2026-020/021/026/027): run on the
  Atlas GPU host; environment `torch 2.10 / transformers 4.46.3` (thread caps affect
  execution only, not results). These need the model weights and are the most involved to
  reproduce.
- **MATLAB rows** (root-MUSIC cross-check for DOA, GO-P-2026-031): the Phased Array
  toolbox reproduction; its reconstruction-energy columns match the numpy harness to 3
  significant figures, giving an independent-implementation check (R-IND-3).

## Data provenance (the physical domains)

- **A3 LOCATA / D2 AV16.3** — public microphone-array corpora; held-out splits are
  disjoint recordings, named in the preregs.
- **D3 PDAR seismic** — USGS M≥6.5 earthquakes 2017–2018, teleseismic 30–95°, via
  IRIS/EarthScope FDSN; 34 events cached; calibration ~2017, held-out ~2018 (disjoint
  events). Ground truth is the USGS catalogue backazimuth.
- **D1 RaDICaL radar** — *data-limited and stated so*: the full disjoint-recording set is
  ~800 GB (indoor alone 310 GB, ROS-bag, endpoint 403), forcing a within-recording split;
  the reproduction is therefore partial by construction, not by choice.
- **W whale** — Sharma-2024 DSWP sperm-whale codas (8718 codas, 11-d inter-click-interval
  rhythm); held-out disjoint codas.

## Known reproduction gotchas (banked)

- **`results/*.json` are tracked despite `.gitignore`** — force-add (`git add -f`) if you
  regenerate them.
- **Real-model runs need `python -u`** and `setsid`/detached execution on the Atlas host
  for long jobs; obspy is required for the seismic pipeline.
- **The recognizer's `max_gen` must scale with the budget** (Chapter 11) — reading an
  emergent-geometry substrate before its geometry settles is a measurement artifact.
- **Author math-bearing files with an editor, not a bash heredoc** — heredocs corrupt
  backslashes (`\ref` → carriage return), which silently breaks LaTeX/Python source.

## What "reproducible" claims, exactly

The program claims: every *sealed* row's result JSON is regenerable from its committed
script, its seal is a git ancestor of its run, and its verdict is scored against a bar
fixed before the run. It does **not** claim that the data-limited D1 radar row is fully
disjoint-reproducible (it is within-recording, and says so), nor that GPU rows are
bit-identical across hardware (they are result-identical to stated tolerance). The
honesty of the cookbook is the honesty of the ledger: what can be reproduced, and the
named exceptions.
