# GO-P-2026-015 — GO-4: fixed-budget verdict inverts under budget-matched observation, on real book embeddings (PROSPECTIVE)

The GO-4 test, on a substrate **beyond Paper I §5.10** (PREREG_RUNG4): real
768-dim book-paragraph embeddings from Atlas `/archive`, not RGG / Wolfram-model
graphs. §5.10 showed that a **fixed** observer mode-budget verdict inverts when the
budget is **spectral-gap-matched** (m grows with N to hold the resolved eigenvalue
scale τ fixed) — the added high modes inject sub-wavelength detail, so a manifold
that looks clean at a fixed low-mode band *falls* under budget-matched observation.
GO-4 claims this is a general property of the fixed-budget observer; this entry
tests it on a real embedding manifold. Fresh registration; no edits to prior
entries. Governs `experiments/go4_budget_inversion.py` and
`results/GO4-budget-inversion.json`.

**Honesty flag: `retrospective: false` — PROSPECTIVE, real-data.** Substrate =
`/archive/results_aesthetics/book_translation_cache` (4683 files, (≤200,768)
float16). The inversion could fail on real embeddings (they need not be
manifold-like enough for the wavelength mechanism) — a genuine risk. A pass = GO-4
`[replicated]` (≥1 substrate beyond §5.10); a miss bounds the mechanism to
synthetic manifolds and is carried in Honest Negatives.

## Substrate, observer, metric

- **Substrate:** per substrate-seed, sample S=250 book `.npy` files (seeded),
  concatenate their paragraph embeddings, L2-normalize (angular), shuffle → a
  nested pool; refinement axis N ∈ {2000, 4000, 8000, 16000, 32000} = prefixes.
- **Observer:** k-NN graph (k=15, cosine), symmetric normalized Laplacian
  L = I − D^{-1/2} W D^{-1/2}; NJW angular embedding = row-normalized bottom-m
  nontrivial eigenvectors.
- **Metric (angle-ρ):** Spearman between angular-embedding Euclidean distance and
  graph **geodesic** distance (shortest path on the k-NN graph), over pairs sampled
  from A=200 anchor nodes — geometry preservation, higher = cleaner (as §5.10).
- **Budgets:** fixed m=10 at all N; budget-matched m(N) = #{eigenvalues ≤ τ},
  τ = λ_10 at N=2000 (so m grows with N, holding the resolved scale fixed).

```yaml
id: GO-P-2026-015
date: 2026-07-17
retrospective: false
claim: GO-4
substrate: Atlas /archive/results_aesthetics/book_translation_cache (real 768-d book-paragraph embeddings)
observer: kNN(k=15,cosine) symmetric normalized Laplacian; NJW angular embedding (row-normalized bottom-m eigvecs)
metric: angle_rho = Spearman(angular-embedding dist, graph geodesic dist) over 200-anchor sampled pairs
budgets: {fixed: m=10 all N; matched: m(N)=#{lambda<=tau}, tau=lambda_10(N=2000)}
refinement: N in {2000,4000,8000,16000,32000}   # nested prefixes of the shuffled pool
seeds: 3 substrate seeds (disjoint-ish 250-book samples)
prediction:
  # trend_b = Spearman(angle_rho_b vs N) per seed, b in {fixed, matched}
  inversion_per_seed: trend_fixed - trend_matched >= 1.0  AND  trend_matched < 0  AND  trend_fixed > 0
  # i.e. fixed-budget geometry holds/improves with refinement; budget-matched FALLS -> opposite verdict
  mechanism: m_matched(N) strictly increasing in N (budget grows); median angle_rho_matched declines
  convergence: |angle_rho_fixed(N_min) - angle_rho_matched(N_min)| <= 0.05  (budgets agree at N_min)
gated:
  inversion: holds on >= 2 of 3 substrate seeds
  convergence: holds on >= 2 of 3 seeds
  mechanism_m_grows: m_matched strictly increasing (all seeds)
diagnostics_reported_not_gated:
  - angle_rho tables (fixed & matched, per N per seed); m_matched(N); magnitude of the matched fall
  - per-seed trend_fixed, trend_matched
design:
  clusters: substrate seed
  stopping: fixed grid
  compute: local, on a subsample pulled read-only from Atlas (scipy sparse eigsh, bottom modes)
controls:
  - the fixed and matched budgets coincide at N_min by construction (convergence gate audits it)
amendments: []
hash: sha256:8b0482f18c0e71545de7b9a775b68309ef769eadd3b2d4ed09ab156b434e6a05   # filled by scripts/seal.py; git commit is the binding timestamp
```

## Falsification (GO-4, prospective, real substrate)

GO-4 is **not supported** if any hold at 3 seeds: the inversion fails on ≥2/3 seeds
(the two budgets do not give opposite refinement verdicts / do not diverge by ≥1.0
in trend); the convergence audit fails (budgets already disagree at N_min — the
divergence was baked in, not emergent); or m_matched does not grow with N (the
budget-matching is degenerate).

`GO4_supported` requires inversion ∧ convergence ∧ mechanism_m_grows. A pass = GO-4
`[replicated]` on a real embedding substrate beyond §5.10 — the fixed-budget
verdict is an observer property, not a substrate invariant. A miss bounds the
wavelength mechanism to synthetic manifolds.
