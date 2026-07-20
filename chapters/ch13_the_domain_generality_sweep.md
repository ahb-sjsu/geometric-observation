# Chapter 13 — The Domain-Generality Sweep: Twelve Domains, Three Physics

A mechanism first shown on transformer keys and graph embeddings could be a fact about
transformer keys and graph embeddings. The only way to know whether the flip is a
*property of observation* or an artifact of its birth regimes is to put it at risk
somewhere it has no right to work. This chapter is that sweep: twelve domains, three
distinct branches of physics, one compressor, every row config-frozen on a calibration
split and scored on held-out data, every outcome reported regardless of sign. It is the
book's broadest empirical claim, and its most important negatives are in it, not
quarantined into Chapter 16.

## The claim under test, once more

At matched bits, a code that preserves what the *consumer* reads beats a genuinely
reconstruction-optimal code on the consumer's downstream task — *while the
reconstruction-optimal code reconstructs the signal better.* A row is a **flip** only
if, on held-out data: the read-preserving arm wins downstream, the reconstruction-optimal
arm reconstructs better (the trade), and the anti-arm (read direction destroyed) is worst
(the control). The reference for GT and thresholds is frozen *before* the held-out run.

## The sweep

| # | Domain | Consumer | Read operator | Outcome | Registry |
|---|--------|----------|---------------|---------|----------|
| A1 | Synthetic ULA | beamformer-ML + root-MUSIC | array manifold $\hat g = P_a^\perp a'$ | ✅ 6/6 | GO-P-2026-031 |
| A2 | LLM attention keys (Llama-3.2-3B) | softmax attention | query 2nd-moment (blind probe) | ✅ 16/16 | GO-P-2026-021 |
| A3 | LOCATA acoustic array | wideband MUSIC | array manifold | ✅ 11/13 | GO-P-2026-033 |
| **D1** | **RaDICaL 77 GHz FMCW radar** | MUSIC DOA | 8-elem virtual array | ◐ **partial** | GO-P-2026-034 D1 |
| **D2** | **AV16.3 acoustic (2nd corpus)** | wideband MUSIC (circular) | array manifold | ✅ **confirmed** | GO-P-2026-034 D2 |
| **D3** | **PDAR seismic array** | wideband MUSIC backazimuth | array manifold | ✅ **confirmed** | GO-P-2026-034 D3 |
| **D4** | **Optimization (gradient)** | update distortion (Hessian metric) | the loss Hessian | ⊘ **honest negative** | GO-P-2026-034 D4 |
| L | Legal citation retrieval | cosine ranking (LaBSE) | blind probe | ✗035 → ✅036 → ✅039 | GO-P-2026-035/036/039 |
| M | Moral judgment (ETHICS) | fine-tuned classifier | classifier weight (blind) | ✅ (A2) verdict | GO-P-2026-037 |
| K | LLM KV-keys (post-RoPE) | attention logits | (regime reconciled) | ✅ (A2) verdict | a2_probe |
| Mu | Music aesthetics (FMA CLAP) | genre classifier | classifier weight | ✅ (A2) verdict | a2_probe |
| W | Whale codas (DSWP) | Clan/dialect classifier | blind probe (top-4) | ✅ **sealed flip** | GO-P-2026-038 |

## The three physics

The headline is not the count of domains; it is that the flip crosses *physical media*.
The read operator in each physical case is the array manifold — the geometry of how a
wavefront maps to sensor responses — and the flip says a codec that reconstructs the raw
array signal better points *worse* at the source. That this holds across three distinct
wave physics is the strongest evidence that the mechanism is about observation, not about
any one substrate.

**Electromagnetic (D1, RaDICaL radar) — partial, no file-drawer.** On a real
automotive-grade 77 GHz FMCW radar, the core dissociation *replicates*: the angle-favoring
code beats reconstruction-optimal Lloyd–Max at matched bits on 25/25 held-out frames while
Lloyd reconstructs the raw signal better on 25/25 (the textbook flip, median flip_fail
0.41°). But the **anti control is 60% < the sealed 70%** — the tiny 8-element array's ~15°
resolution lets phase-destroyed snapshots occasionally land near the reference — and the
data was download-limited (the disjoint-recording set is 310 GB behind a 403), forcing a
within-recording split. Two of three sealed bars pass; the anti control and the disjoint
held-out do not → **partial** [predicted → partial, registered miss]. The flip mechanism
transfers to a different physics; a *clean* D1 confirm awaits the full data.

**Acoustic (D2, AV16.3) — confirmed.** A genuinely independent corpus from LOCATA:
different array (8-mic circular), room, speakers; camera-tracked 3D-mouth GT (1.2 cm).
Scored against *absolute* tracked GT, no reference amendment. Held-out disjoint
recordings, $n = 201$: flip 148/201 (74%), recon-trade 201/201, anti 152/201, median
flip_fail 0.28° [demonstrated — GO-P-2026-034 D2]. The strongest of the real-data domains.

**Elastic (D3, PDAR) — confirmed.** A third distinct physics: elastic waves from real
M≥6.5 earthquakes, a 13-element IMS short-period array, incoherent wideband MUSIC over
backazimuth at the theoretical teleseismic-P slowness. Scored against the *absolute*
USGS catalogue backazimuth (great-circle array→epicentre; no reference amendment — the
array resolves baz to a few degrees). Held-out disjoint ~2018 events, $n = 17$: flip
13/17 (76%), recon-trade 17/17, anti 13/17, median flip_fail 0.00° [demonstrated —
GO-P-2026-034 D3]. A quantizer that reconstructs the seismogram better locates the
earthquake worse.

With D2 and D3 confirmed, the battery's own sealed prediction — flip in ≥2 of the 3 core
prospective domains — is **met** [predicted → met].

## The non-physical confirmations

Beyond physics, the flip appears in consumers of pure information geometry.

**Whale codas (W) — sealed flip.** Sperm-whale coda dialect, a clan classifier, 8718
codas of inter-click-interval rhythm. Held-out read-preserving AUROC 0.934 > recon-optimal
0.883, recon-trade (O reconstructs 2× better yet downstream-worse), flip 300/300
[demonstrated — GO-P-2026-038, promoted from an (A2) verdict]. Distinct biology from every
other row, and the clean proof (Chapter 12) that the regime map needs two axes.

**Legal (L) — the identifiability story.** Citation-ranking, read operator recovered
blind, 035 miss → 036/039 hit on a virgin split (R=0.796 > O=0.780, double the margin)
[demonstrated — GO-P-2026-039]. The first real-consumer demonstration that the blind probe
recovers a read operator that is both misaligned-with-energy and generalizing.

**Moral, music, KV-keys (M, Mu, K) — (A2) verdicts.** Consistent with the flip via the
proxy probe but *not* sealed two-metric flips, and labeled as verdicts, not flips. The
book does not upgrade them.

## What the negatives bought

The sweep's honest negatives were more informative than its confirmations, and they are
the reason the boundary conditions of Chapter 12 exist. **D4 (optimization)** is a true
coupling null — anti-probe 300/300 but flip 27%, because curvature and gradient energy
coincide in a trained model; not a data gap, a boundary [refuted, as a flip]. **035** was
an identifiability failure that the blind probe fixed. **D1** is data-limited and says so.
The registration discipline caught its own over-reach *twice* in this sweep — the NEG-14
shortcut and the 035 estimated read operator — which is exactly what the discipline is
for.

## The verdict of the sweep

The consumer-relative flip is a property of observation **wherever the read operator can
be identified.** It confirms across acoustic, seismic, and synthetic physics; LLM
attention; moral, genre, and dialect classifiers; and citation retrieval. It fails,
*informatively*, exactly where the read operator is unidentifiable (fixable), coupled to
the signal (a boundary), or attached to a consumer that does not work (a precondition).
The one-encoder question is thereby answered — **adapt, don't universalize** — and the
diagnostic that decides the encoding is `probe_quotient`, per domain, on two axes. Chapter
14 zooms from the sweep's breadth to the falsifiable core's depth: the GO-1…GO-6 spine and
how a claim earns each of its class tags.
