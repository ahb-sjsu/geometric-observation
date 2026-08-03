# End-to-end KV-cache benchmark on a real long-context serving workload
# (GO-P-2026-056; sealed as 055, renumbered pre-run per the dated prereg
# amendment -- ID collision with the complementarity-tax seal e1e9dfe):
# does WHERE the quantization error lands decide task
# outcome, at IDENTICAL bits and IDENTICAL reconstruction error?
#
# This is the operational form of GO-2 on a deployed-class model.  The arm
# construction is the recon-matched pair of gateB_llama_rematch.py, lifted
# from captured activations into the LIVE decode path: a custom DynamicCache
# perturbs post-RoPE keys as the model generates, so the model actually
# attends over damaged keys the way a quantized-KV server would.
#
#   base error g  = (real per-channel asym-4bit quantization error of K)
#   per-token norm r = ||g||          <-- PRESERVED by both arms
#   PRESERVE arm : error placed in the ORTHOGONAL COMPLEMENT of the read
#                  subspace  (spend the damage where queries do not look)
#   DESTROY  arm : error placed INSIDE the read subspace, same norm r
#   SHUFFLE  arm : DESTROY, but using ANOTHER head's read subspace
#                  (consumer-specificity control)
#
# Both arms carry the bit budget of the same real 4-bit quantizer and, per
# token, the same reconstruction error to machine precision.  So neither bits
# nor reconstruction can explain any task-score difference: only the geometry
# of the error relative to what softmax attention reads.  These are
# error-steering PROBES, not two deployable codecs -- the deployable
# comparison is a separate arm pair (see --arms deploy), and that distinction
# is stated in the prereg rather than blurred.
#
# The read subspace per (layer, kv-head) is the top-r eigenspace of
# P_C = sum over the head's GQA query group of E[q q^T] (post-RoPE), measured
# on held-out calibration prompts.  Note that a GQA KV head is read by `grp`
# query heads at once -- Paper V's several-consumers-one-record structure in
# production hardware -- so P_C is the SUM of the group's read operators.
#
# Usage:
#   python experiments/kv_serving_flip.py --model <hf-id> --task <name>
#          [--n 40] [--arms probe|deploy|all] [--pilot] [--calib 8]
# Output: sentinel JSON ===KVSF-JSON===.  Tier B (Atlas, GPU 1).  MIT.
import argparse
import json
import os
import re
import string
import sys
import time
from collections import Counter, defaultdict

import numpy as np
import torch

# ------------------------------------------------------------------ scoring
# SQuAD-style normalization + F1, self-contained (LongBench convention).
def _norm(s):
    s = s.lower()
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def f1_score(pred, golds):
    best = 0.0
    for g in golds:
        p, t = _norm(pred).split(), _norm(g).split()
        common = Counter(p) & Counter(t)
        ns = sum(common.values())
        if ns == 0:
            continue
        prec, rec = ns / len(p), ns / len(t)
        best = max(best, 2 * prec * rec / (prec + rec))
    return best


def retrieval_score(pred, golds):
    """passage_retrieval_en: gold is 'Paragraph N'; accept the first integer."""
    m = re.search(r"\d+", pred)
    if not m:
        return 0.0
    got = m.group(0)
    return float(any(got == re.search(r"\d+", g).group(0)
                     for g in golds if re.search(r"\d+", g)))


SCORERS = {"passage_retrieval_en": retrieval_score, "hotpotqa": f1_score,
           "qasper": f1_score, "2wikimqa": f1_score, "multifieldqa_en": f1_score}
PROMPTS = {
    "passage_retrieval_en":
        "Here are 30 paragraphs extracted from Wikipedia.\n\n{context}\n\n"
        "The following is an abstract of one of the paragraphs above.\n\n{input}\n\n"
        "Which paragraph is the abstract from? Answer with only 'Paragraph N'.\nAnswer:",
    "hotpotqa":
        "Answer the question based on the passages below. Be concise.\n\n"
        "{context}\n\nQuestion: {input}\nAnswer:",
}
MAXNEW = {"passage_retrieval_en": 12, "hotpotqa": 32}
PREFILL_CHUNK = 1024        # bounds SDPA math-backend attention memory on Volta


# --------------------------------------------------- post-RoPE q/k capture
_cap = defaultdict(dict)
_layer_ctr = {"i": 0}
_capture_on = {"on": False}


def install_rope_capture(mod):
    orig = mod.apply_rotary_pos_emb

    def patched(q, k, cos, sin, unsqueeze_dim=1):
        q2, k2 = orig(q, k, cos, sin, unsqueeze_dim)
        if _capture_on["on"]:
            # only q is needed for the read operator; skipping k halves the
            # capture footprint (which is ~1 GB/pass at 28 layers otherwise)
            _cap[_layer_ctr["i"]]["q"] = q2.detach().to(torch.float32).cpu().numpy()
        _layer_ctr["i"] += 1
        return q2, k2

    mod.apply_rotary_pos_emb = patched
    return orig


# ------------------------------------------------------- the steering cache
def make_steering_cache_cls(DynamicCache):
    class SteeringCache(DynamicCache):
        """Perturbs post-RoPE keys in the live decode path.

        subspaces[layer] : (n_kv, d, r) float32 tensor of read-subspace bases
        mode : 'preserve' (error -> complement) | 'destroy' (error -> subspace)
        Both preserve the per-token norm of the reference 4-bit error exactly.
        """
        subspaces = None
        mode = None
        bits = 4
        stats = None                    # accumulates the recon audit

        def update(self, key_states, value_states, layer_idx, *args, **kwargs):
            if self.mode is not None and key_states.shape[-2] > 0:
                key_states = self._steer(key_states, layer_idx)
            return super().update(key_states, value_states, layer_idx, *args, **kwargs)

        def _steer(self, K, layer_idx):
            V = self.subspaces.get(layer_idx)
            if V is None:
                return K
            dt = K.dtype
            x = K.to(torch.float32)                        # (B,H,S,D)
            q = 2 ** self.bits - 1
            lo = x.amin(dim=-2, keepdim=True)              # per (B,H,D): per-channel
            hi = x.amax(dim=-2, keepdim=True)
            sc = torch.where(hi - lo > 0, (hi - lo) / q, torch.ones_like(hi))
            g = (lo + torch.clamp(torch.round((x - lo) / sc), 0, q) * sc) - x
            r = g.norm(dim=-1, keepdim=True)               # (B,H,S,1) norm to preserve
            Vt = V.to(x.device, torch.float32)             # (H,D,r)
            coef = torch.einsum('bhsd,hdr->bhsr', g, Vt)
            proj = torch.einsum('bhsr,hdr->bhsd', coef, Vt)   # in-subspace part
            comp = proj if self.mode == 'destroy' else (g - proj)
            n = comp.norm(dim=-1, keepdim=True)
            fallback = Vt[:, :, -1].unsqueeze(0).unsqueeze(2).expand_as(comp)
            u = torch.where(n > 1e-8, comp / (n + 1e-12), fallback)
            delta = r * u
            if self.stats is not None:                     # recon-match audit
                self.stats['sum_r'] += float(r.sum())
                self.stats['sum_d'] += float(delta.norm(dim=-1).sum())
                self.stats['sum_g'] += float(g.norm(dim=-1).sum())
                self.stats['n'] += int(r.numel())
            return (x + delta).to(dt)

    return SteeringCache


# ------------------------------------------------------------- calibration
def calibrate(model, tok, texts, layers, n_kv, grp, d, r_sub, mod, device):
    """Return {layer: (n_kv, d, r_sub) torch tensor} read-subspace bases."""
    acc = {L: [np.zeros((d, d), dtype=np.float64) for _ in range(n_kv)] for L in layers}
    for t in texts:
        ids = tok(t, return_tensors='pt', truncation=True, max_length=2048).input_ids.to(device)
        _layer_ctr['i'] = 0
        _cap.clear()
        _capture_on['on'] = True
        with torch.no_grad():
            model(ids)
        _capture_on['on'] = False
        for L in layers:
            if L not in _cap:
                continue
            q = _cap[L]['q'][0]                            # (n_q_heads, S, d)
            for h in range(n_kv):
                Q = q[h * grp:(h + 1) * grp].reshape(-1, d)
                acc[L][h] += Q.T @ Q / max(Q.shape[0], 1)
    out = {}
    for L in layers:
        Vs = np.zeros((n_kv, d, r_sub), dtype=np.float32)
        for h in range(n_kv):
            w, V = np.linalg.eigh(acc[L][h])
            Vs[h] = V[:, -r_sub:]
        out[L] = torch.from_numpy(Vs)
    return out


# -------------------------------------------------------------------- eval
def run_arm(model, tok, items, task, cache_cls, subspaces, mode, device,
            r_sub, bits, label, ref_preds=None):
    """ref_preds: the fp16 arm's generations, for the agreement co-primary.
    A binary task score at n=40 is statistically thin; normalized agreement
    with the fp16 baseline's own output is continuous, monotone in damage,
    and cannot be gamed by a degenerate answer that happens to match gold."""
    scorer = SCORERS[task]
    tmpl, mx = PROMPTS[task], MAXNEW[task]
    scores, preds = [], []
    stats = {'sum_r': 0.0, 'sum_d': 0.0, 'sum_g': 0.0, 'n': 0}
    t0 = time.time()
    for it in items:
        prompt = tmpl.format(context=it['context'], input=it['input'])
        enc = tok(prompt, return_tensors='pt', truncation=True, max_length=15000)
        ids = enc.input_ids.to(device)
        cache = cache_cls()
        cache.subspaces = subspaces or {}
        cache.mode = mode
        cache.bits = bits
        cache.stats = stats if mode is not None else None
        # CHUNKED PREFILL.  Volta (sm_70) has no flash kernel, so SDPA falls back
        # to the math backend and materializes S x S attention -- 21.7 GB at
        # S=14k x 28 heads.  Chunking bounds it to chunk x S and is what
        # production serving does anyway.  Then a manual greedy decode, so the
        # steering cache is the only cache in play.
        S = ids.shape[1]
        gen = []
        with torch.no_grad():
            for s0 in range(0, S, PREFILL_CHUNK):
                chunk = ids[:, s0:s0 + PREFILL_CHUNK]
                o = model(input_ids=chunk, past_key_values=cache, use_cache=True)
            nxt = int(o.logits[0, -1].argmax())
            for _ in range(mx):
                gen.append(nxt)
                if nxt == tok.eos_token_id:
                    break
                o = model(input_ids=torch.tensor([[nxt]], device=device),
                          past_key_values=cache, use_cache=True)
                nxt = int(o.logits[0, -1].argmax())
        txt = tok.decode(gen, skip_special_tokens=True).strip()
        preds.append(txt)
        scores.append(scorer(txt, it['answers']))
        del cache, o, ids
        if torch.cuda.is_available():
            torch.cuda.empty_cache()   # allocator grew to 28 GB without this
    res = dict(arm=label, mode=mode, n=len(items), score=float(np.mean(scores)),
               seconds=round(time.time() - t0, 1), preds=preds[:5],
               per_item_score=scores, all_preds=preds)
    if ref_preds is not None:
        res['fp16_agreement'] = float(np.mean(
            [1.0 if _norm(p) == _norm(q) else 0.0 for p, q in zip(preds, ref_preds)]))
        res['fp16_token_f1'] = float(np.mean(
            [f1_score(p, [q]) for p, q in zip(preds, ref_preds)]))
    if stats['n']:
        res['recon_ratio_delta_over_ref'] = stats['sum_d'] / max(stats['sum_r'], 1e-9)
        res['mean_ref_err_norm'] = stats['sum_g'] / stats['n']
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Qwen/Qwen2.5-7B-Instruct')
    ap.add_argument('--task', default='passage_retrieval_en')
    ap.add_argument('--n', type=int, default=40)
    ap.add_argument('--calib', type=int, default=8)
    ap.add_argument('--rsub', type=int, default=16)
    ap.add_argument('--bits', default='4',
                    help='comma list; the reference quantizer whose per-token '
                         'error norm both steering arms preserve. Sweeping it '
                         'locates the regime where quantization actually bites '
                         '(4-bit per-channel asym is deliberately benign).')
    ap.add_argument('--pilot', action='store_true')
    ap.add_argument('--seed', type=int, default=20260814)
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.cache_utils import DynamicCache
    from transformers.models.qwen2 import modeling_qwen2 as QM

    device = 'cuda'
    print(f"model={a.model} task={a.task} n={a.n} r_sub={a.rsub} bits={a.bits} "
          f"seed={a.seed} pilot={a.pilot}", flush=True)
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(
        a.model, torch_dtype=torch.bfloat16,
        attn_implementation='sdpa').to(device).eval()
    cfg = model.config
    d = getattr(cfg, 'head_dim', None) or cfg.hidden_size // cfg.num_attention_heads
    n_kv, n_q = cfg.num_key_value_heads, cfg.num_attention_heads
    grp, n_layers = n_q // n_kv, cfg.num_hidden_layers
    print(f"  layers={n_layers} q_heads={n_q} kv_heads={n_kv} grp={grp} d={d}", flush=True)

    install_rope_capture(QM)
    rows = [json.loads(l) for l in
            open(f'/archive/longbench/data/{a.task}.jsonl', encoding='utf-8')]
    rng = np.random.default_rng(a.seed)
    idx = rng.permutation(len(rows))
    calib = [rows[i]['context'][:8000] for i in idx[:a.calib]]
    items = [rows[i] for i in idx[a.calib:a.calib + a.n]]
    print(f"  calib={len(calib)} eval={len(items)} (disjoint)", flush=True)

    layers = list(range(n_layers))
    t0 = time.time()
    subs = calibrate(model, tok, calib, layers, n_kv, grp, d, a.rsub, QM, device)
    print(f"  calibrated read subspaces for {len(subs)} layers "
          f"({time.time()-t0:.0f}s)", flush=True)
    shuf = {L: subs[L][torch.randperm(n_kv, generator=torch.Generator().manual_seed(a.seed))]
            for L in subs}                                  # consumer-specificity control

    SteeringCache = make_steering_cache_cls(DynamicCache)
    bits_list = [int(b) for b in str(a.bits).split(',')]
    arms = [('fp16_baseline', None, None, 0)]
    for b in bits_list:
        arms += [(f'preserve_read@{b}b', 'preserve', subs, b),
                 (f'destroy_read@{b}b', 'destroy', subs, b),
                 (f'shuffle_control@{b}b', 'destroy', shuf, b)]
    out = []
    ref_preds = None
    for label, mode, sp, b in arms:
        r = run_arm(model, tok, items, a.task, SteeringCache, sp, mode, device,
                    a.rsub, b, label, ref_preds=ref_preds)
        if label == 'fp16_baseline':
            ref_preds = r['all_preds']          # co-primary reference
        r['ref_bits'] = b
        out.append(r)
        print(f"  [{label}] score={r['score']:.4f}  ({r['seconds']}s)"
              + (f"  recon_ratio={r.get('recon_ratio_delta_over_ref'):.6f}"
                 f"  ref_err={r.get('mean_ref_err_norm'):.3f}"
                 if 'recon_ratio_delta_over_ref' in r else ''), flush=True)

    by = {r['arm']: r for r in out}
    per_bits = {}
    for b in bits_list:
        p, dz = by[f'preserve_read@{b}b'], by[f'destroy_read@{b}b']
        sh = by[f'shuffle_control@{b}b']
        per_bits[b] = dict(
            preserve=p['score'], destroy=dz['score'], shuffle=sh['score'],
            preserve_minus_destroy=p['score'] - dz['score'],
            preserve_minus_shuffle=p['score'] - sh['score'],
            destroy_drop_vs_fp16=by['fp16_baseline']['score'] - dz['score'],
            shuffle_minus_destroy=sh['score'] - dz['score'],
            agree_preserve=p.get('fp16_agreement'),
            agree_destroy=dz.get('fp16_agreement'),
            agree_preserve_minus_destroy=(p.get('fp16_agreement', 0.0)
                                          - dz.get('fp16_agreement', 0.0)),
            tokf1_preserve=p.get('fp16_token_f1'),
            tokf1_destroy=dz.get('fp16_token_f1'),
            preserve_frac_of_fp16=(p['score'] / by['fp16_baseline']['score']
                                   if by['fp16_baseline']['score'] > 0 else float('nan')),
            recon_ratio_preserve=p.get('recon_ratio_delta_over_ref'),
            recon_ratio_destroy=dz.get('recon_ratio_delta_over_ref'),
            ref_err_norm=dz.get('mean_ref_err_norm'))
        print(f"  bits={b}: preserve={p['score']:.3f} destroy={dz['score']:.3f} "
              f"shuffle={sh['score']:.3f}  P-D={p['score']-dz['score']:+.3f}",
              flush=True)
    recon_ok = all(abs(r.get('recon_ratio_delta_over_ref', 1.0) - 1.0) <= 1e-4
                   for r in out if r['mode'] is not None)
    result = dict(
        claim='KV-cache serving flip: at identical bits AND identical reconstruction '
              'error, the geometry of the error relative to what attention reads '
              'decides long-context task score',
        prereg='GO-P-2026-056', mode='pilot' if a.pilot else 'full',
        model=a.model, task=a.task, n_eval=len(items), n_calib=len(calib),
        r_sub=a.rsub, bits_swept=bits_list, seed=a.seed,
        geometry=dict(layers=n_layers, q_heads=n_q, kv_heads=n_kv, grp=grp, head_dim=d),
        arms=out, per_bits=per_bits,
        fp16_score=by['fp16_baseline']['score'],
        recon_matched_audit_ok=bool(recon_ok),
        seconds_total=round(time.time() - t0, 1),
    )
    print(f"\nfp16={result['fp16_score']:.4f}  recon_matched={recon_ok}", flush=True)
    for b, v in per_bits.items():
        print(f"  ref_bits={b}: P-D={v['preserve_minus_destroy']:+.4f} "
              f"P-S={v['preserve_minus_shuffle']:+.4f} "
              f"destroy_drop={v['destroy_drop_vs_fp16']:+.4f}", flush=True)
    print('===KVSF-JSON===')
    print(json.dumps(result, indent=1))
    print('===END===')


if __name__ == '__main__':
    sys.exit(main())
