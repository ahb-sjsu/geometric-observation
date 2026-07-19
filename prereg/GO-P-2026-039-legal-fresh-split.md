# GO-P-2026-039 — Legal-retrieval flip on a fresh virgin split (strengthens GO-P-2026-036)

Closes the one honest soft spot in the sweep's `036` row (flagged in the U0 statistical
audit, [`claims/REGISTRY-ACCOUNTING.md`](../claims/REGISTRY-ACCOUNTING.md)): the `036`
held-out set (`pairs_eval`, opinions `id%10==7`) had **already been scored** for the `035`
verdict, and its headline AUROC margin was thin (R 0.779 vs O 0.771, Δ=0.008). This test
re-rolls **both** the read-operator fit and the evaluation onto **fresh, never-scored**
opinion partitions, holding the `036` recipe **frozen** — the strongest available rebuttal to
the held-out-reuse concern. It changes **only the data split**, nothing in the method.

## Setup
- **Frozen recipe (verbatim `036`, no re-tuning).** GO-1 blind margin-sensitivity read operator
  `S = mean_i g_i g_iᵀ`, `g_i = â − cos(a,b)·b̂`; kept low-rank **r=32**; three matched-bit arms
  in the doc semantic-eigenbasis (scalar quant, fixed per-direction range), **base_bits=0.4**.
  Harness = `experiments/legal_flip{,_v2}.py`, code-binding
  `sha256:72b6157ead586dba41dcb7a578ad408c15cb0b1d19a2359faf929f49566e9034` (cat of the two
  files). The read operator is **refit** on the fresh fit split (same recipe, same frozen
  hyper-parameters) — the claim under test is that the *recipe* generalises, not one frozen vector.
- **Virgin split (the only change).** Opinion-level clean split, both endpoints of a pair in the
  same partition (as `cl_citation_pairs.py`):
  - **eval = residue 3** — pairs with both `citing%10==3` and `cited%10==3` (~1.3k after the
    `MIN_SNIP=400`/electronic-era filter; matches the old eval's n). **Never scored before**
    (035/036 only ever scored residue 7).
  - **fit = both endpoints `%10 ∉ {3,7}`** — first 4000 snippet-filtered pairs (matches the `036`
    fit size). Opinion-disjoint from eval-3 by construction (no residue-3 opinion in the fit).
  - Fit and eval are opinion-disjoint within this run; eval-3 is disjoint from the 035/036 eval-7.
- **Consumer / metrics (unchanged).** Citation-pair cosine ranking; downstream = retrieval AUROC;
  reconstruction = relative MSE on the doc embeddings; LaBSE, GPU 1.
- **Same four sealed bars**, 200 bootstrap query-subsets, seed 0.

```yaml
id: GO-P-2026-039
date: 2026-07-19
retrospective: false
kind: fresh-virgin-split rerun of the legal flip; frozen 036 recipe, re-rolled fit + eval
strengthens: GO-P-2026-036 (held-out reuse + thin margin, per U0 statistical audit)
recipe_frozen: {read_op: GO-1 blind margin S=mean g gᵀ g=â−cos(a,b)b̂, r: 32, base_bits: 0.4,
  quantizer: semantic-eigenbasis scalar, fixed per-direction range}
code_hash: sha256:72b6157ead586dba41dcb7a578ad408c15cb0b1d19a2359faf929f49566e9034
data: CourtListener (citing,cited) snippet pairs; eval = both endpoints id%10==3 (virgin, ~1.3k);
  fit = both endpoints id%10 ∉ {3,7}, first 4000; opinion-disjoint fit/eval; eval-3 never scored
sealed_bars:
  flip_boots: ">= 60% (AUROC_R >= AUROC_O per bootstrap query subset)"
  recon_trade: "recon(O) <= recon(R) (reconstruction-optimal reconstructs better)"
  anti_boots: ">= 70% (AUROC_A worst)"
  full_auroc: "AUROC_R >= AUROC_O on the full eval set"
prediction:
  the frozen 036 recipe reproduces the flip on the virgin eval-3: all four sealed bars pass;
  in particular AUROC_R >= AUROC_O with the recon-trade intact (O reconstructs better yet loses
  downstream).
falsification:
  the flip FAILS on the virgin split -> the 036 result is split-dependent; the legal row drops to
  the disclosed-caveat tier (recon-trade + anti carry it, the two-consumer verdict does not seal).
commitment: outcome reported regardless of sign in claims/LEDGER.md (GO-B-legal-virgin). No eval-3
  pair is embedded or scored before this prereg is committed. The virgin eval residue (3) and the
  frozen hyper-parameters (r=32, bits=0.4) are fixed by this seal; nothing is selected on eval-3.
hash: sha256:786b2c7a0608d737d47f0a99f4c5a4ac7cda57abec5bdcc1f083481a5fd8250f
```

## Falsification
A pass converts `036` from "confirmed on a reused thin-margin split" to "confirmed on a fully
virgin, opinion-disjoint split under the frozen recipe" — removing the last asterisk on the
sweep's legal row. A fail is reported at equal prominence and demotes the row to the disclosed
caveat tier (the qualitatively large recon-trade dissociation would still stand; only the sealed
two-metric flip would not). Sealed per REG-1; the git commit is the binding timestamp; the eval
residue and all hyper-parameters are frozen here before any eval-3 embedding exists.

## Outcome — CONFIRMED, 2026-07-19
Frozen `036` recipe (r=32, base_bits=0.4, blind-probe read op **refit** on the fresh fit) scored on
the **virgin** eval-3 (n=1342, opinion-disjoint from the fit, never scored in 035/036). Fit n=4000
(both endpoints `%10 ∉ {3,7}`). All four sealed bars pass:
- **AUROC read-preserving R=0.796 > recon-optimal O=0.780** ✓ (anti A=0.695; uncompressed 0.794 —
  R edges *above* the uncompressed embedding: stripping nuisance directions denoises the ranking).
  Margin R−O = **0.016 — double `036`'s 0.008**.
- recon **O=0.223 ≤ R=0.561** ✓ (recon-optimal reconstructs 2.5× better yet is downstream-worse).
- **flip 200/200** ✓, **anti 200/200** ✓ → **4/4 CONFIRMED.**

The frozen recipe reproduces the flip on a **fully virgin, opinion-disjoint** split; the last
asterisk on the sweep's legal row (held-out reuse + thin margin, flagged in the U0 statistical
audit) is removed. Recorded in `claims/LEDGER.md` (GO-B-legal) and
[`results/GO-legal-fresh-split.json`](../results/GO-legal-fresh-split.json). Run on Atlas GPU 1,
env `/home/claude/env` (torch 2.10.0+cu128, LaBSE).
