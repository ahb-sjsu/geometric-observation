# GO-13 planning note

2026-08-05. Status of the ladder at planning time: GO-10 (the
complementarity tax) and GO-11 (the exact static region, Thms 1–10)
both [replicated]; GO-12 (the dynamic region) at Theorem 1 + Facts 1–2
netted, with two open conjectures (spectral program; process-rate
causal object) and the novelty landscape fully swept. This note is the
planning input for what GO-13 should be — decision owner: the user
(with Syed on venue implications).

## Candidate directions

### C1 — The dynamic complementarity tax (RECOMMENDED)

Two consumers reading one process, with an aging/access-limited eraser:
the merge of all three campaigns. CT_R and CT_W per symbol, as
functions of the eraser's access class and staleness.

Why this is the natural rung: every ingredient exists and is netted —
GO-10's tax definitions, GO-11's Theorem 9 (m=2 matrix water levels),
GO-12's conditional-variance reduction (q_G) and access-class family.
The obvious opening theorems look reachable with current machinery:

1. **Matrix-q reduction (candidate Theorem 1).** For m=2 single-letter
   records, any observation-subset σ-algebra G should enter Theorem
   9's program only through the conditional covariance Σ_{T|G} — the
   matrix analog of q_G — by the same channel-agnostic sufficiency
   argument (project T on the closed span of G; the residual is
   independent of the span; the record noises never see G). If it
   holds, the m=2 access-class family (slice/prefix/path, now with
   matrix Kalman/Wiener objects) comes for free, and the DYNAMIC TAX
   CT_W(D_A, D_B; G) is exactly computable.
2. **Does staleness pay the tax or the consumers?** CT_W(Δ) =
   R_AB-coordinate minus max single-consumer coordinate, all at access
   class G(Δ): a fresh, sharply falsifiable question — does the
   complementarity tax grow, shrink, or stay invariant as the eraser's
   context ages? (Naive guess from the m=1 structure: both coordinates
   inflate through the same s_eff, so the tax could be *invariant* in
   some regimes — an analytically-zero-style prediction if true, and a
   GO-10-grade finding either way.)
3. **Operational face.** 058-lineage decode-threshold instruments with
   two consumers and an aged/filtered context; the encoder-tilt and
   eraser-allocation mechanisms both have dynamic versions.
4. **Later/big:** the spectral m=2 program (couples to GO-12
   Conjecture 1; matrix water levels per frequency — the full
   "third promotion" picture).

Novelty flanks to sweep before any seal (predictable from the GO-12
sweeps): multiterminal/CEO with stale observations; Heegard–Berger
with degraded SI at two decoders; the Simeone–Permuter line's
multi-decoder variants. The third-party eraser framing and the tax
coordinates remain the program's own throughout.

### C2 — The process-rate causal object (GO-12 Conjecture 2′ residue)

Block records + Markov-constrained causal conditioning. Honest
assessment from Sweep C: exceeds the current state of the art (the
simpler decoder-SI object is explicitly open, Lev–Khina), needs the
definitional fork handled with care, and risks reading as a
Kalman-exercise unless the operational definition carries weight. Keep
as GO-12's long-game item, not GO-13.

### C3 — Empirical/systems face: staleness in a real serving system

The KV-cache line (NEG-16 successor): KV entries as records, model
context as the aging reference, eviction/recomputation as erasure —
GO-12's access-width dichotomy has a measurable analog (full-history
vs sliding-window attention). Blocked on the standing GPU-budget
decision; ride-along lane, not the theory rung.

### C4 — Quantum extension

Flagged since the original GO-10 pitch ("quantum caution"). del
Rio-style conditional erasure with quantum side information is the
obvious substrate, but the program's comparative advantage (exact
Gaussian machinery + governed operational faces) doesn't transfer
cheaply. Defer.

## Recommendation

Open GO-13 as C1 (the dynamic complementarity tax), first move the
matrix-q reduction (candidate Theorem 1) — it is the exact
intersection of Thm 9 and the q_G reduction, both freshly netted, and
its sanity numerics reuse `sanity_m2sys.py` + `sanity_go12_prefix.py`
machinery nearly verbatim. Second move: the tax-vs-staleness question
(item 2), which is cheap once item 1 lands and is the kind of sharp
falsifiable claim the house style is built for. C3 rides along when
the GPU budget unblocks. House rules as always: problem statement
first, novelty sweeps before novelty language, §5.1 on every seal.
