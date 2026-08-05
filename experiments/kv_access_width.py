# CALIBRATION instrument for GO-P-2026-075 (DRAFT, UNSEALED): access width on
# a real serving system -- KV-cache eviction policies as access classes.
#
# STATUS: EXPLORATORY / UNREGISTERED / DISCLOSED.  This run calibrates the
# instrument only.  It must NOT measure the gated quantities in anger: no P1
# age-resolved gap estimates are computed here beyond a pipeline sanity check
# whose task scores are flagged sanity_only.  The seal (and the pilot and
# governed runs) come later, by the main session.
#
# Mapping (056 lineage, GO-12/13 access-width theory):
#   record          = a KV-cache entry (layer, kv-head, position)
#   aging reference = the rolling context (entry age = S - position)
#   erasure         = eviction under a fixed retention budget
#   PATH  access    = cumulative full-history attention-mass scoring
#                     (every query the entry ever served votes)
#   SLICE access    = terminal-window snapshot scoring (SnapKV-style,
#                     only the last-w queries vote)
#   CONTROL (P2)    = an equal-uncertainty pair: one path-family and one
#                     slice-family policy calibrated to EQUAL predictive
#                     uncertainty about an entry's future attention mass.
#                     THIS run measures the uncertainty-vs-width curves the
#                     pairing needs; the pair itself is chosen at seal time.
#
# Matched recomputation budget: every arm retains exactly the same number of
# entries per (layer, kv-head) -- B_keep = max(rho*S, 64), always including
# the last 32 positions (the local window every deployed policy keeps) -- so
# neither memory nor recompute budget can explain an arm difference.
#
# What this calibration measures:
#   (i)   uncertainty proxy for P2: per policy family x width, how well the
#         policy score predicts an entry's FUTURE attention mass during
#         decode -- spearman rho and the unexplained-variance fraction u
#         (residual var of log1p(future mass) after 20-bin conditioning on
#         the score, over total var), pooled over (prompt, layer, kv-head).
#   (ii)  age-bin occupancy + future-mass share + hypothetical retention
#         fraction per bin per policy at budget rho (sizes P1's bins).
#   (iii) runtime per prompt and GPU-1 temperature (thermal discipline).
#
# Usage (Atlas GPU 1, 056 conventions):
#   CUDA_VISIBLE_DEVICES=1 /archive/kvbench/venv/bin/python kv_access_width.py \
#       [--n 12] [--task passage_retrieval_en] [--maxlen 15000]
#       [--decode-steps 48] [--rho 0.25] [--sanity 2] [--band-sanity]
# Output: sentinel JSON ===KVAW-JSON===.  Tier B (Atlas, GPU 1).  MIT.
import argparse
import json
import math
import os
import re
import string
import subprocess
import sys
import time
from collections import Counter, defaultdict, deque

import numpy as np
import torch

PREFILL_CHUNK = 1024   # bounds SDPA math-backend attention memory on Volta (056)
QBLK = 256             # query sub-block for the fp32 rescoring pass
WIN_KEEP = 32          # local window every arm always retains (SnapKV convention)
TAIL_W = 128           # captured terminal-query tail for slice-family scoring
AGE_EDGES = [1, 32, 128, 512, 2048, 8192, 10 ** 9]
PATH_WIDTHS = ['full', 4096, 1024]           # chunk-granular history widths
SLICE_WIDTHS = [8, 16, 32, 64, 128]          # exact terminal windows

# ------------------------------------------------------------------ scoring
# SQuAD-style normalization + F1 / retrieval, verbatim 056 conventions.
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
    m = re.search(r"\d+", pred)
    if not m:
        return 0.0
    got = m.group(0)
    return float(any(got == re.search(r"\d+", g).group(0)
                     for g in golds if re.search(r"\d+", g)))


SCORERS = {"passage_retrieval_en": retrieval_score, "hotpotqa": f1_score}
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


# ------------------------------------------------------------ thermal guard
def gpu_temp():
    """Physical GPU 1 (the one CUDA_VISIBLE_DEVICES=1 exposes as logical 0)."""
    try:
        out = subprocess.check_output(
            ['nvidia-smi', '--query-gpu=temperature.gpu', '-i', '1',
             '--format=csv,noheader'], timeout=10)
        return int(out.decode().strip())
    except Exception:
        return -1


def thermal_gate(log):
    """Block until GPU 1 <= 80 C; abort the whole run above 83 C persistent."""
    for _ in range(20):
        t = gpu_temp()
        log.append(t)
        if t < 0 or t <= 80:
            return t
        print(f"  [thermal] GPU1 at {t}C, pausing 30s", flush=True)
        time.sleep(30)
    raise SystemExit(f"THERMAL ABORT: GPU1 stuck above 80C (last={log[-1]}C)")


# --------------------------------------------------- post-RoPE q capture (056)
_cap = {}
_layer_ctr = {"i": 0}
_capture_on = {"on": False}


def install_rope_capture(mod):
    orig = mod.apply_rotary_pos_emb

    def patched(q, k, cos, sin, unsqueeze_dim=1):
        q2, k2 = orig(q, k, cos, sin, unsqueeze_dim)
        if _capture_on["on"]:
            _cap[_layer_ctr["i"]] = q2.detach().to(torch.float32)   # stays on GPU
        _layer_ctr["i"] += 1
        return q2, k2

    mod.apply_rotary_pos_emb = patched


class _CapCtx:
    def __enter__(self):
        _layer_ctr['i'] = 0
        _cap.clear()
        _capture_on['on'] = True

    def __exit__(self, *a):
        _capture_on['on'] = False


# ------------------------------------------------------------ telemetry cache
def make_telemetry_cache_cls(DynamicCache):
    class TelemetryCache(DynamicCache):
        """Plain cache that keeps references to the full K/V per layer, so the
        instrument can rescore and prune without version-fragile attribute
        access into the transformers Cache internals."""
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self.snap = {}

        def update(self, key_states, value_states, layer_idx, *a, **kw):
            ko, vo = super().update(key_states, value_states, layer_idx, *a, **kw)
            self.snap[layer_idx] = (ko, vo)
            return ko, vo

    return TelemetryCache


# --------------------------------------------------- attention-mass rescoring
def chunk_mass(qc, K, s0, grp, scale):
    """Per-entry attention mass contributed by one prefill chunk's queries.
    qc (n_q, C, d) fp32 GPU; K (n_kv, S, d) GPU.  Returns (n_kv, S) fp32 cpu.
    Causal: query at global position s0+i attends keys 0..s0+i."""
    n_kv, S, d = K.shape
    C = qc.shape[1]
    out = torch.zeros(n_kv, S, dtype=torch.float32, device=qc.device)
    j = torch.arange(S, device=qc.device).view(1, 1, S)
    for h in range(n_kv):
        Kh = K[h].float()
        for q0 in range(0, C, QBLK):
            Q = qc[h * grp:(h + 1) * grp, q0:q0 + QBLK]        # (grp, c, d)
            logits = torch.einsum('gcd,sd->gcs', Q, Kh) * scale
            i = torch.arange(q0, q0 + Q.shape[1], device=qc.device).view(1, -1, 1)
            logits.masked_fill_(j > s0 + i, float('-inf'))
            out[h] += torch.softmax(logits, -1).sum((0, 1))
    return out.cpu()


def rowwise_mass(qt, K, grp, scale):
    """Per-QUERY-row per-entry mass for the terminal tail (no masking needed:
    all tail queries sit at positions >= every prefill key).
    qt (n_q, W, d) fp32 GPU; K (n_kv, S, d).  Returns (n_kv, W, S) cpu."""
    n_kv, S, d = K.shape
    W = qt.shape[1]
    out = torch.zeros(n_kv, W, S, dtype=torch.float32, device=qt.device)
    for h in range(n_kv):
        Kh = K[h].float()
        Q = qt[h * grp:(h + 1) * grp]                          # (grp, W, d)
        logits = torch.einsum('gwd,sd->gws', Q, Kh) * scale
        out[h] = torch.softmax(logits, -1).sum(0)
    return out.cpu()


# ------------------------------------------------------------------ statistics
def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(np.float64)
    ry = np.argsort(np.argsort(y)).astype(np.float64)
    rx -= rx.mean()
    ry -= ry.mean()
    den = math.sqrt((rx * rx).sum() * (ry * ry).sum())
    return float((rx * ry).sum() / den) if den > 0 else 0.0


def unexplained_frac(score, y, nbins=20):
    """Fraction of Var(y) not explained by 20-quantile-bin conditioning on the
    score.  This is the operational q_G proxy for P2's equal-uncertainty
    pairing: u -> 0 means the policy is near-certain about future mass."""
    tv = float(y.var())
    if tv <= 0:
        return 1.0
    order = np.argsort(score)
    rv, n = 0.0, len(y)
    for b in np.array_split(y[order], nbins):
        if len(b):
            rv += float(b.var()) * len(b)
    return float(rv / n / tv)


def pct(a):
    a = np.asarray(a, dtype=np.float64)
    return dict(mean=float(a.mean()), p10=float(np.percentile(a, 10)),
                p50=float(np.percentile(a, 50)), p90=float(np.percentile(a, 90)))


# ------------------------------------------------------------------- prefill
def prefill_with_telemetry(model, ids, cache, n_layers, n_kv, grp, d, device):
    """Chunked prefill (056 Volta convention) + fp32 attention-mass rescoring.
    Returns (last_logits, path_scores{width: (L, n_kv, S)}, tail_q{L})."""
    S = ids.shape[1]
    scale = 1.0 / math.sqrt(d)
    acc_full = np.zeros((n_layers, n_kv, S), dtype=np.float32)
    last_chunks = deque(maxlen=4)          # per-chunk masses for width 4096/1024
    tail_q = {}                            # layer -> (n_q, <=TAIL_W, d) cpu fp32
    o = None
    for s0 in range(0, S, PREFILL_CHUNK):
        chunk = ids[:, s0:s0 + PREFILL_CHUNK]
        with _CapCtx(), torch.no_grad():
            o = model(input_ids=chunk, past_key_values=cache, use_cache=True)
        cm = np.zeros((n_layers, n_kv, S), dtype=np.float32)
        with torch.no_grad():
            for L in range(n_layers):
                qc = _cap[L][0]                                # (n_q, C, d) GPU
                K = cache.snap[L][0][0]                        # (n_kv, S_sofar, d)
                m = chunk_mass(qc, K, s0, grp, scale).numpy()
                cm[L, :, :m.shape[1]] = m
                t_prev = tail_q.get(L)
                t_new = qc.detach().cpu()
                tail_q[L] = (t_new if t_prev is None
                             else torch.cat([t_prev, t_new], dim=1))[:, -TAIL_W:]
        _cap.clear()
        acc_full += cm
        last_chunks.append(cm)
    path = {'full': acc_full,
            4096: np.sum(np.stack(list(last_chunks)), axis=0),
            1024: last_chunks[-1]}
    return o.logits[0, -1], path, tail_q


def slice_scores(tail_q, cache, n_layers, n_kv, grp, d, S, device):
    """{width: (L, n_kv, S)} from exact terminal-window rows."""
    scale = 1.0 / math.sqrt(d)
    out = {w: np.zeros((n_layers, n_kv, S), dtype=np.float32) for w in SLICE_WIDTHS}
    with torch.no_grad():
        for L in range(n_layers):
            K = cache.snap[L][0][0][:, :S]
            rm = rowwise_mass(tail_q[L].to(device), K, grp, scale).numpy()
            W = rm.shape[1]
            for w in SLICE_WIDTHS:
                out[w][L] = rm[:, -min(w, W):, :].sum(1)
    return out


# -------------------------------------------------------------------- decode
def decode_with_telemetry(model, tok, cache, first_logits, S, n_layers, n_kv,
                          grp, d, steps, device):
    """Greedy decode with per-step manual attention rows accumulated into
    future_mass over the PREFILL entries.  Continues past EOS for telemetry;
    the task prediction uses tokens up to EOS."""
    scale = 1.0 / math.sqrt(d)
    fm = np.zeros((n_layers, n_kv, S), dtype=np.float32)
    gen, eos_at, gen_mass = [], None, 0.0
    nxt = int(first_logits.argmax())
    for t in range(steps):
        gen.append(nxt)
        if eos_at is None and nxt == tok.eos_token_id:
            eos_at = t
        with _CapCtx(), torch.no_grad():
            o = model(input_ids=torch.tensor([[nxt]], device=device),
                      past_key_values=cache, use_cache=True)
        with torch.no_grad():
            for L in range(n_layers):
                q1 = _cap[L][0]                                # (n_q, 1, d)
                K = cache.snap[L][0][0]                        # (n_kv, S+t+1, d)
                for h in range(n_kv):
                    row = torch.softmax(
                        (q1[h * grp:(h + 1) * grp, 0] @ K[h].float().T) * scale,
                        -1).sum(0)
                    fm[L, h] += row[:S].cpu().numpy()
                    gen_mass += float(row[S:].sum())
        _cap.clear()
        nxt = int(o.logits[0, -1].argmax())
    n_upto = (eos_at if eos_at is not None else len(gen))
    txt = tok.decode(gen[:n_upto], skip_special_tokens=True).strip()
    gen_frac = gen_mass / max(steps * n_layers * n_kv * grp, 1)
    return fm, txt, eos_at, gen_frac


# -------------------------------------------------- pruned-cache sanity decode
def kept_indices(score_lh, S, B_keep):
    """Top-B_keep entries by score, always including the last WIN_KEEP."""
    forced = np.arange(max(S - WIN_KEEP, 0), S)
    cand = np.argsort(score_lh[:max(S - WIN_KEEP, 0)])[::-1][:max(B_keep - len(forced), 0)]
    return np.sort(np.concatenate([cand, forced]))


def pruned_decode(model, tok, cache_cls, full_cache, scores, S, B_keep,
                  first_logits, task, n_layers, device, band=None):
    """Build a pruned cache from per-(L,h) scores and greedy-decode the task
    answer.  band=(a1,a2): band-restricted eviction (P1 mechanism check) --
    evict the bottom half of the band by score, keep everything else."""
    cache = cache_cls()
    kept_count = 0
    for L in range(n_layers):
        K, V = full_cache.snap[L]
        K, V = K[:, :, :S], V[:, :, :S]
        ks, vs = [], []
        for h in range(K.shape[1]):
            if band is None:
                idx = kept_indices(scores[L, h], S, B_keep)
            else:
                a1, a2 = band
                ages = S - np.arange(S)
                inb = np.where((ages >= a1) & (ages < a2))[0]
                drop = inb[np.argsort(scores[L, h][inb])[:len(inb) // 2]]
                idx = np.setdiff1d(np.arange(S), drop)
            kept_count += len(idx)
            ii = torch.tensor(idx, device=K.device, dtype=torch.long)
            ks.append(K[:, h].index_select(1, ii))
            vs.append(V[:, h].index_select(1, ii))
        # per-head keep-counts are equal by construction inside a mode
        kk = torch.stack(ks, dim=1)
        vv = torch.stack(vs, dim=1)
        with torch.no_grad():
            cache.update(kk, vv, L)
    gen = []
    nxt = int(first_logits.argmax())
    mx = MAXNEW[task]
    with torch.no_grad():
        for t in range(mx):
            gen.append(nxt)
            if nxt == tok.eos_token_id:
                break
            o = model(input_ids=torch.tensor([[nxt]], device=device),
                      past_key_values=cache, use_cache=True,
                      cache_position=torch.tensor([S + t], device=device))
            nxt = int(o.logits[0, -1].argmax())
    del cache
    torch.cuda.empty_cache()
    txt = tok.decode(gen, skip_special_tokens=True).strip()
    return txt, kept_count / n_layers


# ---------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Qwen/Qwen2.5-7B-Instruct')
    ap.add_argument('--task', default='passage_retrieval_en')
    ap.add_argument('--n', type=int, default=12)
    ap.add_argument('--maxlen', type=int, default=15000)
    ap.add_argument('--decode-steps', type=int, default=48)
    ap.add_argument('--rho', type=float, default=0.25)
    ap.add_argument('--sanity', type=int, default=2,
                    help='prompts to run through the pruned-decode arms '
                         '(pipeline check only; scores flagged sanity_only)')
    ap.add_argument('--band-sanity', action='store_true',
                    help='also exercise the age-band-restricted eviction '
                         'mechanism on one prompt (P1 machinery check)')
    ap.add_argument('--seed', type=int, default=20260805)
    ap.add_argument('--max-minutes', type=float, default=75.0)
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.cache_utils import DynamicCache
    from transformers.models.qwen2 import modeling_qwen2 as QM

    device = 'cuda'
    temps = [gpu_temp()]
    print(f"KVAW calibration model={a.model} task={a.task} n={a.n} "
          f"maxlen={a.maxlen} steps={a.decode_steps} rho={a.rho} "
          f"seed={a.seed} temp0={temps[0]}C", flush=True)
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(
        a.model, torch_dtype=torch.bfloat16,
        attn_implementation='sdpa').to(device).eval()
    cfg = model.config
    d = getattr(cfg, 'head_dim', None) or cfg.hidden_size // cfg.num_attention_heads
    n_kv, n_q = cfg.num_key_value_heads, cfg.num_attention_heads
    grp, n_layers = n_q // n_kv, cfg.num_hidden_layers
    print(f"  layers={n_layers} q_heads={n_q} kv_heads={n_kv} grp={grp} d={d}",
          flush=True)
    install_rope_capture(QM)
    TelemetryCache = make_telemetry_cache_cls(DynamicCache)

    rows = [json.loads(l) for l in
            open(f'/archive/longbench/data/{a.task}.jsonl', encoding='utf-8')]
    rng = np.random.default_rng(a.seed)
    idx = rng.permutation(len(rows))
    used = [int(i) for i in idx[:a.n]]
    items = [rows[i] for i in used]
    print(f"  calibration prompts: indices {used} of {len(rows)} "
          f"(EXCLUDE from pilot/governed eval sets at seal)", flush=True)

    tmpl = PROMPTS[a.task]
    scorer = SCORERS[a.task]
    widths = [('path', w) for w in PATH_WIDTHS] + [('slice', w) for w in SLICE_WIDTHS]
    agg = {f"{f}:{w}": dict(rho=[], u=[]) for f, w in widths}
    nb = len(AGE_EDGES) - 1
    bin_occ = np.zeros(nb)
    bin_mass = np.zeros(nb)
    bin_keep = {f"{f}:{w}": np.zeros(nb) for f, w in widths}
    bin_keep_n = np.zeros(nb)
    per_prompt, sanity_rows, band_row = [], [], None
    t_start = time.time()

    for pi, it in enumerate(items):
        if (time.time() - t_start) / 60 > a.max_minutes:
            print(f"  [budget] {a.max_minutes} min reached, stopping at "
                  f"prompt {pi}", flush=True)
            break
        thermal_gate(temps)
        prompt = tmpl.format(context=it['context'], input=it['input'])
        ids = tok(prompt, return_tensors='pt', truncation=True,
                  max_length=a.maxlen).input_ids.to(device)
        S = ids.shape[1]
        t0 = time.time()
        cache = TelemetryCache()
        first_logits, path, tail_q = prefill_with_telemetry(
            model, ids, cache, n_layers, n_kv, grp, d, device)
        t_pref = time.time() - t0
        sl = slice_scores(tail_q, cache, n_layers, n_kv, grp, d, S, device)
        t_slice = time.time() - t0 - t_pref
        fm, txt, eos_at, gen_frac = decode_with_telemetry(
            model, tok, cache, first_logits, S, n_layers, n_kv, grp, d,
            a.decode_steps, device)
        t_dec = time.time() - t0 - t_pref - t_slice
        task_s = scorer(txt, it['answers'])

        # ---- (i) uncertainty proxy per family x width, pooled over (L, h)
        scores_by = {f"path:{w}": path[w] for w in PATH_WIDTHS}
        scores_by.update({f"slice:{w}": sl[w] for w in SLICE_WIDTHS})
        cut = max(S - WIN_KEEP, 1)           # exclude the always-kept window
        for key, sc in scores_by.items():
            for L in range(n_layers):
                for h in range(n_kv):
                    y = np.log1p(fm[L, h, :cut].astype(np.float64))
                    x = sc[L, h, :cut].astype(np.float64)
                    agg[key]['rho'].append(spearman(x, y))
                    agg[key]['u'].append(unexplained_frac(x, y))

        # ---- (ii) age bins: occupancy, future-mass share, retention at rho
        ages = S - np.arange(cut)
        which = np.digitize(ages, AGE_EDGES[1:-1] + [AGE_EDGES[-1]])
        fm_tot = fm[:, :, :cut].sum(axis=(0, 1))
        B_keep = max(int(a.rho * S), 64)
        for b in range(nb):
            m = which == b
            bin_occ[b] += m.mean()
            bin_mass[b] += (fm_tot[m].sum() / max(fm_tot.sum(), 1e-9))
            bin_keep_n[b] += 1
        for key, sc in scores_by.items():
            keep_frac = np.zeros(nb)
            cnt = np.zeros(nb)
            for L in range(n_layers):
                for h in range(n_kv):
                    kept = kept_indices(sc[L, h], S, B_keep)
                    kmask = np.zeros(S, bool)
                    kmask[kept] = True
                    for b in range(nb):
                        m = which == b
                        if m.sum():
                            keep_frac[b] += kmask[:cut][m].mean()
                            cnt[b] += 1
            bin_keep[key] += np.where(cnt > 0, keep_frac / np.maximum(cnt, 1), 0)

        temps.append(gpu_temp())
        per_prompt.append(dict(
            i=pi, longbench_idx=used[pi], S=int(S), task_score=float(task_s),
            eos_at=eos_at, gen_mass_frac=round(gen_frac, 4),
            sec_prefill=round(t_pref, 1), sec_slice=round(t_slice, 1),
            sec_decode=round(t_dec, 1), sec_total=round(time.time() - t0, 1),
            temp_after=temps[-1]))
        print(f"  [{pi}] S={S} fp16_task={task_s:.2f} "
              f"prefill={t_pref:.0f}s slice={t_slice:.0f}s decode={t_dec:.0f}s "
              f"temp={temps[-1]}C", flush=True)

        # ---- pipeline sanity: pruned-decode arms on the first --sanity prompts
        if pi < a.sanity:
            for key in ('path:full', 'slice:32'):
                ptxt, kept_per_layer = pruned_decode(
                    model, tok, TelemetryCache, cache, scores_by[key], S,
                    B_keep, first_logits, a.task, n_layers, device)
                sanity_rows.append(dict(
                    prompt=pi, arm=key, sanity_only=True,
                    task_score=float(scorer(ptxt, it['answers'])),
                    pred=ptxt[:60], kept_per_layer=float(kept_per_layer),
                    budget=int(B_keep * n_kv)))
                print(f"    sanity[{key}] score={sanity_rows[-1]['task_score']:.2f} "
                      f"pred={ptxt[:40]!r}", flush=True)
        if a.band_sanity and pi == 0:
            btxt, _ = pruned_decode(
                model, tok, TelemetryCache, cache, scores_by['path:full'], S,
                B_keep, first_logits, a.task, n_layers, device,
                band=(128, 2048))
            band_row = dict(band=[128, 2048], ran_ok=True, pred=btxt[:60],
                            sanity_only=True)
            print(f"    band-sanity ran_ok pred={btxt[:40]!r}", flush=True)

        del cache, tail_q, path, sl, fm
        torch.cuda.empty_cache()

    n_done = len(per_prompt)
    result = dict(
        prereg='GO-P-2026-075-DRAFT',
        phase='instrument_calibration',
        disclosure='EXPLORATORY, UNREGISTERED, disclosed in the prereg. '
                   'No gated quantity measured: no age-resolved P1 gaps, no '
                   'equal-q P2 comparison. Sanity task scores are pipeline '
                   'checks only. Calibration prompt indices must be excluded '
                   'from pilot/governed eval sets.',
        model=a.model, task=a.task, n_prompts=n_done, maxlen=a.maxlen,
        decode_steps=a.decode_steps, rho=a.rho, seed=a.seed,
        win_keep=WIN_KEEP, tail_w=TAIL_W, qblk=QBLK,
        calibration_indices=used[:n_done],
        geometry=dict(layers=n_layers, q_heads=n_q, kv_heads=n_kv, grp=grp,
                      head_dim=d),
        versions=dict(torch=torch.__version__,
                      transformers=__import__('transformers').__version__),
        uncertainty_by_width={
            key: dict(spearman=pct(v['rho']), unexplained=pct(v['u']),
                      n_cells=len(v['rho']))
            for key, v in agg.items() if v['rho']},
        age_bins=dict(
            edges=AGE_EDGES,
            occupancy=[float(x) for x in bin_occ / max(n_done, 1)],
            future_mass_share=[float(x) for x in bin_mass / max(n_done, 1)],
            retain_frac_at_rho={
                key: [float(x) for x in v / max(n_done, 1)]
                for key, v in bin_keep.items()}),
        per_prompt=per_prompt,
        sanity_arms=sanity_rows,
        band_sanity=band_row,
        temps_c=temps,
        temp_max=max(t for t in temps if t >= 0) if temps else None,
        seconds_total=round(time.time() - t_start, 1),
    )
    print('===KVAW-JSON===')
    print(json.dumps(result, indent=1))
    print('===END===')


if __name__ == '__main__':
    sys.exit(main())
