# GO-P-2026-055 — KV-cache serving flip: at identical bits AND identical reconstruction error, where the error lands decides the task

Registers the **end-to-end long-context benchmark** on a deployed-class model: does the
*geometry* of KV quantization error relative to what softmax attention reads decide
task outcome, when bits and reconstruction error are both held fixed? This is the
operational form of **GO-2** on a real serving path, and the experiment I flagged as
the one most likely to move the program's significance.

**Construction.** The recon-matched arm pair of `gateB_llama_rematch.py:99`, lifted from
captured activations into the **live decode path**: a `DynamicCache` subclass perturbs
post-RoPE keys as the model generates, so the model actually attends over damaged keys.
Reference error $g$ = real per-channel asymmetric $b$-bit quantization error of $K$;
per-token norm $r=\lVert g\rVert$ is **preserved by both arms**:

- **preserve_read** — error placed in the orthogonal complement of the read subspace
- **destroy_read** — error placed *inside* it, same norm $r$
- **shuffle_control** — destroy, but using **another KV head's** subspace (specificity)

Read subspace per (layer, KV head) = top-$r_{\rm sub}$ eigenspace of
$P_C=\sum_{\text{GQA group}}\mathbb E[qq^{\mathsf T}]$ (post-RoPE), measured on
**held-out calibration prompts disjoint from eval**. A GQA KV head is read by `grp`
query heads at once, so $P_C$ is the sum of the group's read operators — Paper V's
several-consumers-one-record structure in production hardware.

These are **error-steering probes, not two deployable codecs**: they isolate the
mechanism at fixed bits and fixed reconstruction. No claim is made here about a
shippable quantizer.

**Prior evidence this run is built on (both logged, both on Qwen2.5-1.5B):**
1. *Mechanism* (`kv_steer_mechanism.py`, CPU, captured activations): at matched error
   norm, in-subspace error raises softmax-attention KL by **15–36×** over
   complement error, in **10/10 heads in all 15 $(r_{\rm sub},b)$ configurations**.
   Query energy captured by the top-$r_{\rm sub}$ eigenspace: r=16 → 0.795,
   r=32 → 0.881, r=64 → 0.953. Chosen $r_{\rm sub}=32$: the KL ratio stays 18.8× while
   $\mathrm{KL}_{\rm preserve}$ is 40% lower than at r=16, i.e. a genuinely gentle
   preserve arm.
2. *Task pilot* (`kv_serving_flip.py --pilot`, n=24, disjoint calib): located the
   damage threshold. 4-bit reference is **below** it (all arms within ±0.13 noise;
   point estimate adverse, P−D=−0.21 — reported, not hidden). 3-bit reference is at it
   (**preserve 0.167 vs destroy 0.000**, shuffle 0.167 = preserve, so the damage needs
   the *correct* subspace). 2-bit floors everything (preserve 0.042).
   fp16 = 0.292 — the 1.5B is too weak at this task to be an effect-size instrument,
   which is why the governed run uses the 7B.

```yaml
id: GO-P-2026-055
date: 2026-08-03
retrospective: false
kind: end-to-end benchmark (Tier B, Atlas GPU 1; operational GO-2 on a deployed-class model)
claim: "On Qwen2.5-7B-Instruct serving a 14k-token LongBench retrieval workload, at IDENTICAL bit budget and IDENTICAL per-token reconstruction error, steering KV quantization error into the attention read subspace destroys task score while steering it into the complement preserves it; the damage requires that head's own read subspace."
harness: experiments/kv_serving_flip.py   # governed seed 20260815; pilots on 1.5B logged above
model: Qwen/Qwen2.5-7B-Instruct           # 28 layers, 28 q heads, 4 KV heads (GQA 7:1), head_dim 128
task: passage_retrieval_en                # 200 items; gold near-uniform over 30 paragraphs, so a
                                          # degenerate constant answer scores only 0.055 (checked)
prediction:
  K1_recon_matched_audit: |mean ||delta|| / mean ||g|| - 1| <= 1e-4 for every steering
    arm (pilot achieved 1e-9). If this fails the run is VOID -- the arms are not
    reconstruction-matched and nothing else can be interpreted.
  K2_fp16_competence: fp16 task score >= 0.50. VALIDITY GATE: a model that cannot do
    the task cannot show degradation on it (the 1.5B at 0.292 could not). A miss voids
    the run as an effect-size test rather than refuting the claim.
  K3_primary_flip_3bit: at 3-bit reference, preserve_read - destroy_read >= +0.15 on
    task score
  K4_specificity_3bit: at 3-bit, shuffle_control - destroy_read >= +0.10 -- the wrong
    head's subspace must do materially less damage than the right one
  K5_agreement_co_primary_3bit: at 3-bit, fp16_agreement(preserve) -
    fp16_agreement(destroy) >= +0.15 (continuous, cannot be gamed by a degenerate
    answer that happens to match gold)
  K6_preserve_usable_3bit: preserve_read >= 0.50 * fp16 score
  reported_not_gated: the 4-bit condition (pilot showed it below the damage threshold,
    with an adverse point estimate); per-item scores for paired tests; fp16 token-F1.
falsification: K3 or K5 failing at 3-bit with K1/K2 satisfied refutes the operational
  claim on this model and task, and is reported at full prominence -- the mechanism
  result (attention KL) would then stand as a consumer-metric-only effect that does not
  survive to end-task score. K4 failing means the effect is subspace-concentration, not
  consumer-specific. K1 failing voids. K2 failing voids as an effect-size test.
design:
  n_eval: 40
  n_calib: 6                        # disjoint from eval by construction
  r_sub: 32                         # chosen from the mechanism sweep, pre-registered
  ref_bits: [3, 4]                  # 3 = registered primary; 4 = reported only
  arms: [fp16_baseline, preserve_read, destroy_read, shuffle_control]
  seed: 20260815
  stopping: fixed design, single governed run
  clusters: items (n=40); per-item scores retained so a paired McNemar can be computed
    post hoc -- the gates above are on point estimates, and the few-item caveat applies
controls: [shuffle_control (wrong head's subspace), fp16 baseline, recon-match audit,
           degenerate-answer check on the gold label distribution, calib/eval disjoint]
scope: real model, real long-context workload, real per-token KV quantization inside the
  generation loop, end-to-end task metric. NOT a throughput/latency serving benchmark --
  no QPS or TTFT claim is made. Keys only; values remain bf16 so the read operator is
  unambiguous.
amendments: []
hash: sha256:1b84e1256bc5e028b1e8f7f184cf4021d76ef6e78a4c3cc73b1fae4d75dfe399
```

## Falsification
Any gate miss is reported at full prominence per PROTOCOL Rule 1.2. This is a single
governed run; if it passes, the natural hardening is a second task (hotpotqa, F1) and a
second model family, each separately registered.
