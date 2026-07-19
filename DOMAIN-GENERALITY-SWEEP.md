# The consumer-relative flip across domains — a sweep

*Synthesis of the domain-generality program (July 2026). Every row resolves to a sealed prereg and a
result JSON under `prereg/` and `results/`; nothing here asserts what those cannot show.*

## The claim under test

At **matched bits**, a code that preserves what the *consumer* reads beats a genuinely
reconstruction-optimal code on the consumer's downstream task — **while the reconstruction-optimal code
reconstructs the signal better.** Downstream distortion is governed by `tr(P_C·Σ_δ)` — the error
covariance projected onto the consumer's read operator `P_C` — not by total reconstruction `tr(Σ_δ)`.
The two move in opposite directions: this is the *flip*. The question this sweep answers is whether the
flip is a **property of observation** or an artifact of the regimes it was first shown in.

## The sweep

Three prior anchors, a sealed four-domain battery (`GO-P-2026-034`), and five extension domains. Each was
config-frozen on a calibration split and scored on held-out data; outcomes are reported regardless of
sign (no file drawer).

| # | Domain | Consumer | Read operator | Outcome | Registry |
|---|--------|----------|---------------|---------|----------|
| A1 | Synthetic ULA | beamformer-ML + root-MUSIC | array manifold `ĝ = P_a^⊥ a′` | ✅ confirmed 6/6 | GO-P-2026-031 |
| A2 | LLM attention keys (Llama-3.2-3B) | softmax attention | query 2nd-moment (blind probe) | ✅ confirmed 16/16 | GO-P-2026-021 |
| A3 | LOCATA acoustic array | wideband MUSIC | array manifold | ✅ confirmed 11/13 | GO-P-2026-033 |
| **D1** | **RaDICaL radar (77 GHz FMCW)** | MUSIC DOA | 8-elem virtual array | **◐ partial** — flip+recon 25/25, anti 60%, data-limited | GO-P-2026-034 D1 |
| **D2** | **AV16.3 acoustic (2nd corpus)** | wideband MUSIC (circular array) | array manifold | ✅ **confirmed** 74% flip, 100% recon, disjoint held-out, tracked GT | GO-P-2026-034 D2 |
| **D3** | **PDAR seismic array** | wideband MUSIC backazimuth | array manifold | ✅ **confirmed** 76% flip, 100% recon, catalogue GT | GO-P-2026-034 D3 |
| **D4** | **Optimization (gradient)** | update distortion under Hessian metric | the loss Hessian | **⊘ honest negative** — anti 300/300, flip 27% | GO-P-2026-034 D4 |
| L | Legal citation retrieval | cosine ranking (LaBSE) | *estimated* covariance → **blind probe** | **✗ 035 → ✅ 036 → ✅ 039** (virgin split R 0.796 > O 0.780, margin 2×) | GO-P-2026-035/036/039 |
| M | Moral judgment (ETHICS) | fine-tuned classifier | classifier weight (blind) | ✅ confirmed via a2_probe (polar 0.994 > per-ch 0.956) | GO-P-2026-037 |
| K | LLM KV-keys (post-RoPE) | attention logits | — (regime reconciled) | ✅ reconciled (whitened 0.853 best) | a2_probe |
| Mu | Music aesthetics (FMA CLAP) | genre classifier | classifier weight | ✅ reconciles `signflip_music` (6σ) | a2_probe |
| W | Whale codas (DSWP) | Clan/dialect classifier | blind probe (top-4) | ✅ **sealed flip** — held-out R 0.934 > O 0.883, 300/300 (was a2_probe verdict) | GO-P-2026-038 |

**Result:** the flip **confirms wherever the read operator is identifiable** — given by geometry (the
physical arrays), planted (synthetic, LLM rematch), or recovered blind from the consumer (legal, moral).
The battery's own prediction (flip in ≥2 of the 3 core prospective domains) was met by D2 + D3. Across
anchors + confirmations the flip spans **≥5 independent domains and ≥3 distinct physics** (synthetic,
acoustic, seismic) plus non-physical consumers (LLM attention, classifiers, retrieval).

## What the flip needs — the boundary conditions

The honest negatives were more informative than the confirmations. They sort into four kinds, and only
one is fixable, which tells you exactly what the flip requires:

1. **Identifiability** — the read operator is mis-*estimated*. **Legal 035** used the document
   covariance as a stand-in for the read operator; it overfit and reconstruction-optimal won on held-out.
   → **Fixed by the GO-1 blind probe** (`036`): recover what the *consumer* is sensitive to, not what the
   *signal* varies in. On the identical held-out set the verdict flipped (R 0.779 > O 0.771). *The 035
   miss was a read-operator-identifiability failure, not a failure of the flip.*
2. **Coupling** — the read operator is *intrinsically* aligned with the signal's energy. **D4**: the
   Hessian's high-curvature directions coincide with the high-gradient-energy directions (both from
   `XᵀX`), so reconstruction-optimal already protects the read directions. The anti-probe stays robust
   (300/300 — the read operator *does* govern the task), but the subtle read-vs-recon flip cannot appear.
   → **Not fixable by any read-operator recovery** — the read operator was already exact. A true boundary.
3. **Precondition** — no working consumer. **Moral** on frozen embeddings sits at chance (LaBSE 0.60,
   BGE-M3 0.58 vs 0.63 majority): there is no moral read direction to protect until the consumer is
   fine-tuned (bert-base → 0.74, at which point the flip appears). → Needs a competent consumer, not a
   read-operator fix.
4. **Mechanism-absent** — the claimed effect does not exist (e.g. `GO-5`/NEG-11: α=1 density restoration
   <2%, not density-specific). → A genuine refutation, not rehabilitatable.

So the flip requires a read operator that is **identifiable**, **misaligned with the signal energy**, and
(on real learned representations) **generalizing** — and a consumer that actually reads the task.

## The engineering instrument — turboquant-pro's (A2) probe

These conditions are not just diagnosed after the fact; they are **measurable before any flip experiment**
by turboquant-pro's `a2_probe` (the program's own foundation, `C:\source\turboquant-pro`):

- `tangential_fraction` — is the consumer carried by the *direction* part? (≈1 ⇒ angular consumer.)
- `probe_quotient(batch, consumer, bits)` — at matched bits, which quantizer family preserves the
  *declared consumer's* rank ordering: polar (angular / read-preserving), per-channel (reconstruction-
  oriented), or — new (turboquant-pro PR #159) — **ZCA-whitened**.
- `TQPRuntimePolicy` + `QualityMonitor` — the **adaptive** layer that picks the family per domain and
  watches for drift. *The flip's domain-dependence is not a gap to be closed by one universal code; it is
  the reason the adaptive selector exists.*

A tempting shortcut was sealed and **refuted** (`GO-P-2026-037`, NEG-14): a single summary statistic
(`median_unit_displacement`) does **not** predict the regime — it broke on the first prospective test.
The reliable diagnostic is `probe_quotient` run per domain, at low bits.

## The regime map — two axes, not one

Characterizing every embedding-consumer domain with `a2_probe` reveals the flip's regime is governed by
**two** independent axes — concentration *and* correlation — which is exactly why no single statistic
(and no single encoder) suffices:

| | **isotropic** (unit_disp ≈ √2) | **concentrated** (unit_disp small) |
|---|---|---|
| **low correlation** | moral, music → **generic polar** | *(rare)* |
| **cross-channel correlated** | **whale → whitened** | KV-keys → **whitened** |
| **channel-structured** | — | legal → **per-channel / blind-probe** |

**Whale codas** are the clean proof the map needs two axes: isotropic like moral, yet they require
whitening like KV-keys — because the inter-click intervals are *correlated*. Concentration alone
(`unit_disp`) cannot tell moral from whale; the correlation axis, which `probe_quotient` measures
directly, is decisive. Whale is also the clearest real-world validation of the whitening candidate (it
wins at every bit level: 0.83 / 0.85 / 0.97 vs per-channel 0.41 / 0.80 / 0.89).

## Synthesis

Observation theory and turboquant-pro are one system seen from two ends. Theory: *preserve what the
consumer reads* (`tr(P_C·Σ_δ)`), and the read operator is either given, recoverable (the GO-1 blind
probe), or a regime you can diagnose. Engineering: `a2_probe` measures the regime, `TQPRuntimePolicy`
adaptively picks the code, `QualityMonitor` guards against drift. Even eris-ketos's **Decoder Robustness
Index** — "Bond Index (ethics) → DRI (bioacoustics)" — is the same read-operator-distortion methodology,
already instantiated for whale decoders (invariant transforms = `ker P_C`; stress transforms = the read
direction).

**The consumer-relative flip is a property of observation — wherever the read operator can be
identified.** It confirms across acoustic, seismic, and synthetic physics, LLM attention, moral and genre
and dialect classifiers, and citation retrieval; it fails, informatively, exactly where the read operator
is unidentifiable, coupled to the signal, or attached to a consumer that does not work. The one-encoder
question is answered — *adapt, don't universalize* — and the diagnostic that decides the encoding is
`probe_quotient` per domain, on two axes.

## Caveats kept honest

A **flip** is the sealed two-metric dissociation (read-preserving beats reconstruction-optimal downstream
*while* reconstruction-optimal reconstructs better); an **(A2) verdict** is a one-metric family
recommendation from the proxy probe — evidence consistent with the flip, not the sealed test. Whale is now
a **sealed flip** (`GO-P-2026-038`, held-out R 0.934 > O 0.883, 300/300), promoted from its earlier verdict;
**music and KV-keys remain (A2) verdicts.** D1 is data-limited (within-recording split; the 310 GB disjoint
set is inaccessible); D4 is a genuine negative (intrinsic coupling), not a data gap; the audio-level DRI
needs raw audio not to hand. The registration discipline caught its own over-reach twice (NEG-14 shortcut;
the 035 estimated read operator) — which is the point of it.

## Registry

Sealed preregs: `GO-P-2026-{031,033,021,034,035,036,037}`. Results: `results/GO-{DOA-gateb,
LOCATA-polarquant-rehab,GateB-llama-rematch,RaDICaL-radar,AV163-doa,PDAR-seismic,D4-optim,
legal-retrieval,legal-retrieval-rehab}.json`, `results/{music-a2-reconciliation,whale-ketos-a2}.json`.
Ledger rows: `claims/LEDGER.md` (GO-B-* + NEG-14). Instrument: `turboquant-pro` `a2_probe` / `runtime_policy`
(whitening candidate merged as PR #159).
