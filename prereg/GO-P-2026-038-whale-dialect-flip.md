# GO-P-2026-038 — Sealed consumer-relative flip on sperm-whale coda dialect

Promotes the exploratory whale **(A2) verdict** (an `a2_probe` family recommendation) to a **sealed flip**
— a proper matched-bit R/O/A test with a downstream task metric — so the domain-generality regime map's
load-bearing cell (isotropic *yet* cross-channel correlated) is anchored by a confirmation rather than a
verdict. Cetacean communication: a physically and biologically distinct domain from every other in the
sweep.

## Setup
- **Data.** DominicaCodas.csv (Sharma et al. 2024, `sw-combinatoriality`), 8,718 sperm-whale codas. Each
  coda's rhythm is its inter-click intervals; features = `nClicks, Duration, ICI1..9` (11-d, standardised).
  Deterministic shuffle (seed 0), 2/3 calibration / 1/3 **held-out (disjoint codas)**.
- **Consumer.** A **Clan (dialect) classifier** — different sperm-whale clans use distinct coda dialects —
  trained on calibration. Because the clans are imbalanced (89% EC1), the downstream metric is the
  **Clan-logit AUROC**, not accuracy (accuracy is swamped by the majority).
- **Read operator.** The GO-1 **blind probe** of the classifier: its margin direction `w`, `S = wwᵀ`, kept
  low-rank (top-`r`). Same recovery + eigenbasis quantiser as `GO-P-2026-036` (legal).
- **Three matched-bit codes.** (R) read-preserving — bits to the top-`r` read directions; (O)
  reconstruction-optimal — bits by feature variance (min reconstruction MSE); (A) anti — bits away from the
  read directions. Downstream = held-out Clan-logit AUROC; reconstruction = feature MSE.
- **Flip (per bootstrap query subset):** AUROC(R) ≥ AUROC(O) **and** reconMSE(O) ≤ reconMSE(R); anti check
  AUROC(A) ≤ min. Config chosen on an **internal cal-A/cal-B split** (fit on cal-A, flip scored on disjoint
  cal-B) before sealing, so only a configuration that already generalises once is frozen.

```yaml
id: GO-P-2026-038
date: 2026-07-19
retrospective: false
kind: sealed consumer-relative flip on cetacean coda dialect (promotes the exploratory whale A2 verdict)
domain: sperm-whale coda communication (DSWP / Sharma 2024) -- biologically distinct
consumer: Clan (dialect) classifier; downstream = Clan-logit AUROC (imbalanced -> AUROC not accuracy)
read_operator: GO-1 blind margin probe S=w wᵀ, top-r low-rank; eigenbasis quantiser (as GO-P-2026-036)
data: DominicaCodas.csv, 8718 codas, ICI rhythm features; shuffle seed 0; calibration 2/3, held-out 1/3 (disjoint)
frozen_config: {r: 4, base_bits: 0.5}
internal_split_cal_B: {auroc_R: 0.934, auroc_O: 0.855, auroc_A: 0.715, recon_O: 0.460, recon_R: 0.893,
  flip: 300/300, anti: 300/300, recon_trade: true}
prediction:
  on the held-out disjoint codas at (r=4, bits=0.5): clean flip AUROC(R) >= AUROC(O) on >= 60% bootstraps;
  recon-trade recon(O) <= recon(R); anti worst on >= 70% bootstraps; and read-preserving beats
  reconstruction-optimal on the full-set AUROC.
falsification: the flip FAILS on the held-out -> the whale row stays an exploratory A2 verdict and the
  two-axis map's correlated-isotropic cell is not sealed.
commitment: outcome reported regardless of sign in claims/LEDGER.md (GO-B-whale). No held-out coda is
  scored before this entry is sealed and committed.
hash: sha256:2f458983de307c5e224372d4c0df1f45f707d1c0a4ae5984af42dc638733a55b
```

## Falsification
A pass converts the striking but exploratory whale result into a sealed confirmation, giving the
domain-generality regime map a confirmed anchor in its most novel cell — a representation that is
isotropic (like music) yet requires protecting a low-rank read subspace against a reconstruction-optimal
code (because its channels are correlated). Sealed per REG-1; the git commit is the binding timestamp;
the config is frozen (and already generalised on the internal split) before any held-out coda is scored.
