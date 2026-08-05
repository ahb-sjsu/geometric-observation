# V2 PILOT instrument for GO-P-2026-075 (DRAFT, UNSEALED): CONSUMER-RELATIVE
# access width on a real serving system -- KV-cache eviction as access classes.
#
# STATUS: PILOT / DISCLOSED / pilot_only.  The v1 pilot (kvaw_pilot.json,
# GO13-kvaw-pilot-disclosed.json) FAILED as an instrument: its "path" arm
# scored entries by raw cumulative attention mass, which hoards sinks/old
# entries (a broken consumer proxy -- path:full scored at the shuffled-null
# level at low rho), and its equal-uncertainty control was unconstructible
# (no u-crossing: u improves monotonically as the scoring window NARROWS).
#
# V2 REDESIGN (user-approved): every arm scores entries by predicted future
# attention mass from a QUERY WINDOW (one consumer-relative family, one axis
# = window width W):
#   w1024   mean attention of the last 1024 query positions onto each entry
#   w256    mean attention of the last  256 query positions onto each entry
#   w32     mean attention of the last   32 query positions (v1 slice:32)
#   w32deg  EQUAL-U CONTROL, constructible by degradation:
#             score_i = w32_score_i + sigma * Z_i, Z fixed-seed N(0,1)/entry;
#           sigma* bisected OFFLINE (CPU, no extra GPU decodes) on this run's
#           recorded telemetry so pooled mean u(w32deg) == pooled mean
#           u(w256).  (The raw per-cell (score, future-mass) arrays of the v1
#           pilot were never dumped -- its artifact holds aggregates only --
#           so the calibration uses the v2 phase-A telemetry, disclosed.)
#   shuf    shuffled-score null (seeded uniform random scores)
# The raw-cumulative ("path:full") arm is DROPPED entirely.
#
# u = same definition as v1: per (layer, kv-head) cell, fraction of
# Var(log1p(future attention mass over 48 greedy steps)) left unexplained by
# 20-quantile-bin conditioning on the policy score, excluding the always-kept
# last WIN_KEEP positions; pooled by averaging cells.
#
# Kept v1 machinery: Qwen2.5-7B-Instruct, LongBench passage_retrieval_en,
# chunked prefill with fp32 rescoring, prefill reuse, matched budget
# B_keep = max(rho*S, 64) always including the last 32 positions,
# cache_position-correct decode, age bands [32,512)/[512,2048)/[2048,8192)/
# 8192+, future-attention-mass telemetry over 48 greedy steps, in-script
# thermal gate (pause >80C, abort >83C persistent).
#
# Phases:
#   A  (GPU) per fresh prompt: prefill+telemetry, fp16 baseline decode with
#      future-mass telemetry, pruned decodes for {w1024,w256,w32,shuf} x
#      rho in {0.10,0.15}; KV offloaded to host RAM for reuse.
#   B  (CPU) sigma* bisection + u tables + age-band mistake tables.
#   C  (GPU) w32deg pruned decodes (both rhos) from the offloaded KV.
#   D  (GPU) age-band-restricted eviction decodes at rho=0.10 (w1024 vs w32).
#
# Fresh prompts: permutation under --seed of the LongBench indices, EXCLUDING
# the 12 calibration indices (GO13-kvaw-calibration-exploratory.json) AND the
# 16 v1-pilot indices (GO13-kvaw-pilot-disclosed.json), both read from those
# artifacts and hardcoded here with provenance.
#
# Usage (Atlas GPU 1):
#   CUDA_VISIBLE_DEVICES=1 /archive/kvbench/venv/bin/python \
#       kv_access_width_v2.py [--n 16] [--seed 20260810] \
#       [--out /home/claude/kvaw2_pilot.json]
# Output: JSON written to --out AND printed between ===KVAW2-JSON=== /
# ===END=== sentinels.  Tier B (Atlas, GPU 1).  MIT.
import argparse
import json
import math
import os
import re
import string
import subprocess
import sys
import time
from collections import Counter, deque

import numpy as np
import torch

PREFILL_CHUNK = 1024   # bounds SDPA math-backend attention memory on Volta
QBLK = 256             # query sub-block for the fp32 rescoring pass
WIN_KEEP = 32          # local window every arm always retains
TAIL_W = 32            # captured terminal-query tail (w32 scoring)
FINE_BLK = 128         # tail-aligned query sub-block granularity
WINDOWS = [1024, 256, 32]          # consumer window widths (one axis)
ARMS = ['w1024', 'w256', 'w32', 'w32deg', 'shuf']
# PILOT-2 REVISION (2026-08-05, disclosed): rho=0.15 dropped (pure ceiling in
# pilot 1); 0.03/0.05 added to move the quality face off the fp16 ceiling.
RHOS = [0.03, 0.05, 0.10]
BANDS = [(32, 512), (512, 2048), (2048, 8192), (8192, 10 ** 9)]
BAND_ARMS = ['w1024', 'w32']       # widest vs narrowest window (P1 axis)
RHO_BAND = 0.10

# Provenance: GO13-kvaw-calibration-exploratory.json calibration_indices
CAL_EXCLUDE = {36, 45, 57, 74, 94, 114, 117, 159, 166, 179, 180, 196}
# Provenance: GO13-kvaw-pilot-disclosed.json pilot_indices
V1_PILOT_EXCLUDE = {175, 69, 10, 96, 40, 140, 150, 25, 101, 128, 162, 197,
                    192, 177, 157, 18}
# Provenance: GO13-kvaw2-pilot-disclosed.json v2_pilot_indices (v2 pilot 1,
# seed 20260810)
V2_PILOT1_EXCLUDE = {154, 3, 26, 165, 48, 85, 138, 133, 80, 168, 112, 13,
                     104, 89, 194, 68}
# Provenance: GO13-kvaw2-pilot2-disclosed.json v2_pilot_indices (v2 pilot 2,
# seed 20260811)
V2_PILOT2_EXCLUDE = {103, 149, 59, 55, 21, 146, 0, 75, 34, 41, 187, 190, 73,
                     160, 37, 62, 46, 27, 181, 152, 188, 155, 42, 176, 93,
                     153, 135, 110, 139, 5, 19, 130}
EXCLUDE = CAL_EXCLUDE | V1_PILOT_EXCLUDE | V2_PILOT1_EXCLUDE | V2_PILOT2_EXCLUDE

# ------------------------------------------------------------------ scoring
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


# --------------------------------------------------- post-RoPE q capture
_cap = {}
_layer_ctr = {"i": 0}
_capture_on = {"on": False}


def install_rope_capture(mod):
    orig = mod.apply_rotary_pos_emb

    def patched(q, k, cos, sin, unsqueeze_dim=1):
        q2, k2 = orig(q, k, cos, sin, unsqueeze_dim)
        if _capture_on["on"]:
            _cap[_layer_ctr["i"]] = q2.detach().to(torch.float32)
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


def make_telemetry_cache_cls(DynamicCache):
    class TelemetryCache(DynamicCache):
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
    """Per-entry attention mass contributed by one block of prefill queries.
    qc (n_q, C, d) fp32 GPU; K (n_kv, S, d) GPU.  Returns (n_kv, S) fp32 cpu.
    Causal: query at global position s0+i attends keys 0..s0+i."""
    n_kv, S, d = K.shape
    C = qc.shape[1]
    out = torch.zeros(n_kv, S, dtype=torch.float32, device=qc.device)
    j = torch.arange(S, device=qc.device).view(1, 1, S)
    for h in range(n_kv):
        Kh = K[h].float()
        for q0 in range(0, C, QBLK):
            Q = qc[h * grp:(h + 1) * grp, q0:q0 + QBLK]
            logits = torch.einsum('gcd,sd->gcs', Q, Kh) * scale
            i = torch.arange(q0, q0 + Q.shape[1], device=qc.device).view(1, -1, 1)
            logits.masked_fill_(j > s0 + i, float('-inf'))
            out[h] += torch.softmax(logits, -1).sum((0, 1))
    return out.cpu()


def rowwise_mass(qt, K, grp, scale):
    """Per-QUERY-row per-entry mass for the terminal tail.  As in v1: no key
    masking (the <=31 future keys a tail query would not see lie inside the
    always-kept WIN_KEEP window, which is excluded from u and never evicted).
    qt (n_q, W, d) fp32 GPU; K (n_kv, S, d).  Returns (n_kv, W, S) cpu."""
    n_kv, S, d = K.shape
    out = torch.zeros(n_kv, qt.shape[1], S, dtype=torch.float32, device=qt.device)
    for h in range(n_kv):
        Kh = K[h].float()
        Q = qt[h * grp:(h + 1) * grp]
        logits = torch.einsum('gwd,sd->gws', Q, Kh) * scale
        out[h] = torch.softmax(logits, -1).sum(0)
    return out.cpu()


# ------------------------------------------------------------------ statistics
def unexplained_frac(score, y, nbins=20):
    """Fraction of Var(y) not explained by 20-quantile-bin conditioning on the
    score (v1 definition, verbatim)."""
    tv = float(y.var())
    if tv <= 0:
        return 1.0
    order = np.argsort(score)
    rv, n = 0.0, len(y)
    for b in np.array_split(y[order], nbins):
        if len(b):
            rv += float(b.var()) * len(b)
    return float(rv / n / tv)


def u_cells(sc, fm, cut, n_layers, n_kv):
    """Per-(L,h) u values for one prompt.  sc, fm: (L, n_kv, S)."""
    us = []
    for L in range(n_layers):
        for h in range(n_kv):
            y = np.log1p(fm[L, h, :cut].astype(np.float64))
            us.append(unexplained_frac(sc[L, h, :cut].astype(np.float64), y))
    return us


def boot_se(vals, nboot=2000, seed=0, stat=np.mean):
    rng = np.random.default_rng(seed)
    v = np.asarray(vals, dtype=np.float64)
    n = len(v)
    if n < 2:
        return 0.0
    bs = [float(stat(v[rng.integers(0, n, n)])) for _ in range(nboot)]
    return float(np.std(bs))


def znoise(seed, longbench_idx, shape):
    """Fixed-seed standard-normal noise field for w32deg (deterministic per
    prompt; identical in calibration and in the decode arm)."""
    rng = np.random.default_rng(seed * 7919 + longbench_idx)
    return rng.standard_normal(shape, dtype=np.float32)


def shuf_scores(seed, longbench_idx, shape):
    """Seeded uniform random scores for the shuffled null (v1 convention)."""
    rng = np.random.default_rng(seed * 100003 + longbench_idx)
    return rng.random(shape).astype(np.float32)


# ------------------------------------------------------------------- prefill
def prefill_v2(model, ids, cache, n_layers, n_kv, grp, d, device):
    """Chunked prefill + fp32 rescoring restricted to the last max(WINDOWS)
    query rows (tail-aligned FINE_BLK blocks; exact windows).  Returns
    (last_logits, {w: (L, n_kv, S) mean-attention scores for w in WINDOWS
    with w > TAIL_W}, tail_q{L})."""
    S = ids.shape[1]
    scale = 1.0 / math.sqrt(d)
    fine_span = max(WINDOWS)
    bounds = sorted({max(S - k * FINE_BLK, 0)
                     for k in range(fine_span // FINE_BLK, 0, -1)} | {S})
    fblocks = [(bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    fine_acc = [np.zeros((n_layers, n_kv, S), dtype=np.float32) for _ in fblocks]
    tail_q = {}
    o = None
    for s0 in range(0, S, PREFILL_CHUNK):
        chunk = ids[:, s0:s0 + PREFILL_CHUNK]
        C = chunk.shape[1]
        fr = [(k, max(ga, s0), min(gb, s0 + C))
              for k, (ga, gb) in enumerate(fblocks)
              if gb > s0 and ga < s0 + C]
        with _CapCtx(), torch.no_grad():
            o = model(input_ids=chunk, past_key_values=cache, use_cache=True)
        with torch.no_grad():
            for L in range(n_layers):
                qc = _cap[L][0]                        # (n_q, C, d) GPU
                K = cache.snap[L][0][0]                # (n_kv, S_sofar, d)
                for k, ga, gb in fr:
                    mf = chunk_mass(qc[:, ga - s0:gb - s0], K, ga,
                                    grp, scale).numpy()
                    fine_acc[k][L, :, :mf.shape[1]] += mf
                t_prev = tail_q.get(L)
                t_new = qc.detach().cpu()
                tail_q[L] = (t_new if t_prev is None
                             else torch.cat([t_prev, t_new], dim=1))[:, -TAIL_W:]
        _cap.clear()
    win = {}
    for w in WINDOWS:
        if w <= TAIL_W:
            continue                                   # handled by tail scoring
        lo = max(S - w, 0)
        sel = [fine_acc[k] for k, (ga, gb) in enumerate(fblocks) if ga >= lo]
        win[w] = np.sum(np.stack(sel), axis=0) / float(S - lo)
    return o.logits[0, -1], win, tail_q


def tail_window_scores(tail_q, cache, n_layers, n_kv, grp, d, S, device, w=32):
    """(L, n_kv, S) mean attention of the last w terminal query rows."""
    scale = 1.0 / math.sqrt(d)
    out = np.zeros((n_layers, n_kv, S), dtype=np.float32)
    with torch.no_grad():
        for L in range(n_layers):
            K = cache.snap[L][0][0][:, :S]
            rm = rowwise_mass(tail_q[L].to(device), K, grp, scale).numpy()
            ww = min(w, rm.shape[1])
            out[L] = rm[:, -ww:, :].sum(1) / float(ww)
    return out


# -------------------------------------------------------------------- decode
def decode_with_telemetry(model, tok, cache, first_logits, S, n_layers, n_kv,
                          grp, d, steps, device):
    """Greedy decode with per-step manual attention rows accumulated into
    future_mass over the PREFILL entries (v1, verbatim)."""
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
                q1 = _cap[L][0]
                K = cache.snap[L][0][0]
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


def kept_indices(score_lh, S, B_keep):
    """Top-B_keep entries by score, always including the last WIN_KEEP."""
    forced = np.arange(max(S - WIN_KEEP, 0), S)
    cand = np.argsort(score_lh[:max(S - WIN_KEEP, 0)])[::-1][:max(B_keep - len(forced), 0)]
    return np.sort(np.concatenate([cand, forced]))


def greedy_decode(model, tok, cache, first_logits, S, task, device):
    """cache_position-correct greedy decode of the task answer."""
    gen = []
    nxt = int(first_logits.argmax())
    with torch.no_grad():
        for t in range(MAXNEW[task]):
            gen.append(nxt)
            if nxt == tok.eos_token_id:
                break
            o = model(input_ids=torch.tensor([[nxt]], device=device),
                      past_key_values=cache, use_cache=True,
                      cache_position=torch.tensor([S + t], device=device))
            nxt = int(o.logits[0, -1].argmax())
    return tok.decode(gen, skip_special_tokens=True).strip()


def pruned_decode_gpu(model, tok, cache_cls, full_cache, scores, S, B_keep,
                      first_logits, task, n_layers, device):
    """Matched-budget pruned decode from the GPU-resident telemetry cache."""
    cache = cache_cls()
    kept_count = 0
    for L in range(n_layers):
        K, V = full_cache.snap[L]
        K, V = K[:, :, :S], V[:, :, :S]
        ks, vs = [], []
        for h in range(K.shape[1]):
            idx = kept_indices(scores[L, h], S, B_keep)
            kept_count += len(idx)
            ii = torch.tensor(idx, device=K.device, dtype=torch.long)
            ks.append(K[:, h].index_select(1, ii))
            vs.append(V[:, h].index_select(1, ii))
        with torch.no_grad():
            cache.update(torch.stack(ks, dim=1), torch.stack(vs, dim=1), L)
    txt = greedy_decode(model, tok, cache, first_logits, S, task, device)
    del cache
    torch.cuda.empty_cache()
    return txt, kept_count / n_layers


def pruned_decode_cpu(model, tok, cache_cls, kv_cpu, scores, S, B_keep,
                      first_logits, task, n_layers, device):
    """Matched-budget pruned decode from host-offloaded KV (prefill reuse)."""
    cache = cache_cls()
    kept_count = 0
    for L in range(n_layers):
        K, V = kv_cpu[L]
        ks, vs = [], []
        for h in range(K.shape[1]):
            idx = kept_indices(scores[L, h], S, B_keep)
            kept_count += len(idx)
            ii = torch.tensor(idx, dtype=torch.long)
            ks.append(K[:, h].index_select(1, ii))
            vs.append(V[:, h].index_select(1, ii))
        with torch.no_grad():
            cache.update(torch.stack(ks, dim=1).to(device),
                         torch.stack(vs, dim=1).to(device), L)
    txt = greedy_decode(model, tok, cache, first_logits, S, task, device)
    del cache
    torch.cuda.empty_cache()
    return txt, kept_count / n_layers


def band_pruned_decode(model, tok, cache_cls, kv_cpu, scores, S, band,
                       keep_frac, first_logits, task, n_layers, device):
    """Band-restricted matched eviction (v1 pilot, verbatim semantics)."""
    a1, a2 = band
    ages = S - np.arange(S)
    inb = np.where((ages >= a1) & (ages < a2)
                   & (np.arange(S) < S - WIN_KEEP))[0]
    n_keep = int(math.ceil(keep_frac * len(inb)))
    n_evict = max(len(inb) - n_keep, 0)
    cache = cache_cls()
    for L in range(n_layers):
        K, V = kv_cpu[L]
        ks, vs = [], []
        for h in range(K.shape[1]):
            drop = inb[np.argsort(scores[L, h][inb])[:n_evict]]
            idx = np.setdiff1d(np.arange(S), drop)
            ii = torch.tensor(idx, dtype=torch.long)
            ks.append(K[:, h].index_select(1, ii))
            vs.append(V[:, h].index_select(1, ii))
        with torch.no_grad():
            cache.update(torch.stack(ks, dim=1).to(device),
                         torch.stack(vs, dim=1).to(device), L)
    txt = greedy_decode(model, tok, cache, first_logits, S, task, device)
    del cache
    torch.cuda.empty_cache()
    return txt, int(len(inb)), int(n_evict)


# --------------------------------------------------------- sigma calibration
def calibrate_sigma(store, seed, n_layers, n_kv, tol=5e-5, max_iter=30):
    """Bisect sigma so pooled mean u(w32 + sigma*Z) == pooled mean u(w256),
    using ONLY the recorded phase-A telemetry (CPU; no GPU decodes).
    Returns a JSON-ready calibration block; every evaluated (sigma,
    per-prompt mean-u) pair is cached for the bootstrap."""
    target_pp = [st['u_mean']['w256'] for st in store]
    target = float(np.mean(target_pp))
    evals = {}                                # sigma -> per-prompt mean u

    def f(sigma):
        if sigma not in evals:
            pp = []
            for st in store:
                if sigma == 0.0:
                    pp.append(st['u_mean']['w32'])
                    continue
                Z = znoise(seed, st['longbench_idx'], st['w32'].shape)
                us = u_cells(st['w32'] + sigma * Z, st['fm'], st['cut'],
                             n_layers, n_kv)
                pp.append(float(np.mean(us)))
            evals[sigma] = pp
        return float(np.mean(evals[sigma])) - target

    f0 = f(0.0)
    out = dict(u_target_w256=target, u_w32_sigma0=target + f0, f0=f0)
    if f0 >= 0:
        out.update(sigma_star=0.0, status='NO_CROSSING_f0_nonneg',
                   note='u(w32) already >= u(w256); degradation cannot help.')
        return out, evals
    hi, lo = 1e-6, 0.0
    while f(hi) < 0:
        lo, hi = hi, hi * 4.0
        if hi > 1e4:
            out.update(sigma_star=None, status='NO_CROSSING_hi_exhausted')
            return out, evals
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        fm_ = f(mid)
        if abs(fm_) < tol:
            lo = hi = mid
            break
        if fm_ < 0:
            lo = mid
        else:
            hi = mid
    sigma_star = 0.5 * (lo + hi)
    resid = f(sigma_star)
    # bootstrap sigma* over prompts from the cached evaluation curves
    sig_sorted = sorted(s for s in evals if s > 0.0)
    curve = np.array([[evals[s][p] for s in sig_sorted]
                      for p in range(len(store))])   # (P, n_sig)
    u32_pp = np.array([st['u_mean']['w32'] for st in store])
    t_pp = np.array(target_pp)
    rng = np.random.default_rng(seed + 13)
    boots, miss = [], 0
    for _ in range(1000):
        idx = rng.integers(0, len(store), len(store))
        tb = float(t_pp[idx].mean())
        cb = curve[idx].mean(axis=0)
        db = np.concatenate([[u32_pp[idx].mean()], cb]) - tb
        sg = np.concatenate([[0.0], sig_sorted])
        w = None
        for i in range(len(sg) - 1):
            if db[i] <= 0 <= db[i + 1] and db[i + 1] > db[i]:
                w = sg[i] + (0 - db[i]) * (sg[i + 1] - sg[i]) / (db[i + 1] - db[i])
                break
        if w is None:
            miss += 1
        else:
            boots.append(w)
    out.update(
        sigma_star=float(sigma_star), status='OK',
        residual=float(resid), tol=tol, n_evals=len(evals),
        boot_se=float(np.std(boots)) if len(boots) > 1 else None,
        boot_p10=float(np.percentile(boots, 10)) if boots else None,
        boot_p90=float(np.percentile(boots, 90)) if boots else None,
        boot_frac_no_crossing=miss / 1000.0,
        eval_curve={f'{s:.8g}': float(np.mean(pp)) for s, pp in evals.items()})
    return out, evals


# ---------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='Qwen/Qwen2.5-7B-Instruct')
    ap.add_argument('--task', default='passage_retrieval_en')
    ap.add_argument('--n', type=int, default=64)
    ap.add_argument('--maxlen', type=int, default=15000)
    ap.add_argument('--decode-steps', type=int, default=48)
    ap.add_argument('--seed', type=int, default=20260812)
    ap.add_argument('--out', default='/home/claude/kvaw2_governed.json')
    ap.add_argument('--band-phase', action='store_true',
                    help='band-restricted decode phase (pilots only; the '
                         'sealed governed design DROPS it -- statistic dead '
                         'at n=32, pre-recorded in GO-P-2026-077)')
    ap.add_argument('--max-minutes', type=float, default=150.0)
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.cache_utils import DynamicCache
    from transformers.models.qwen2 import modeling_qwen2 as QM

    device = 'cuda'
    temps = [gpu_temp()]
    print(f"KVAW2 PILOT model={a.model} task={a.task} n={a.n} seed={a.seed} "
          f"rhos={RHOS} arms={ARMS} temp0={temps[0]}C", flush=True)
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(
        a.model, torch_dtype=torch.bfloat16,
        attn_implementation='sdpa').to(device).eval()
    cfg = model.config
    d = getattr(cfg, 'head_dim', None) or cfg.hidden_size // cfg.num_attention_heads
    n_kv, n_q = cfg.num_key_value_heads, cfg.num_attention_heads
    grp, n_layers = n_q // n_kv, cfg.num_hidden_layers
    install_rope_capture(QM)
    TelemetryCache = make_telemetry_cache_cls(DynamicCache)

    rows = [json.loads(l) for l in
            open(f'/archive/longbench/data/{a.task}.jsonl', encoding='utf-8')]
    rng = np.random.default_rng(a.seed)
    perm = rng.permutation(len(rows))
    used = [int(i) for i in perm if int(i) not in EXCLUDE][:a.n]
    items = [rows[i] for i in used]
    print(f"  v2 pilot prompts (calib + v1-pilot indices excluded): {used}",
          flush=True)

    tmpl = PROMPTS[a.task]
    scorer = SCORERS[a.task]
    per_prompt, sweep_rows, store = [], [], []
    t_start = time.time()
    timing = {}
    try:
        with open(os.path.abspath(__file__), 'rb') as f:
            import hashlib
            inst_sha = hashlib.sha256(f.read()).hexdigest()
    except Exception:
        inst_sha = None
    result = dict(
        prereg='GO-P-2026-077', phase='governed',
        disclosure='GOVERNED SINGLE RUN under sealed GO-P-2026-077 (hash '
                   'sha256:79a731c9...). Fixed design: seed 20260812, n=64 '
                   'fresh prompts (76 prior indices excluded with '
                   'provenance), arms x rho {0.03 measured-only, 0.05, '
                   '0.10}, NO band-restricted decode phase (dropped '
                   'pre-seal on its n=32 replication failure). sigma* '
                   'recalibrated in-run from phase-A telemetry per the '
                   'sealed V5 health gates. Gate verdicts V1-V6 computed '
                   'by the analysis, not by this script.',
        instrument_sha256=inst_sha,
        model=a.model, task=a.task, seed=a.seed, n_prompts_planned=a.n,
        maxlen=a.maxlen, decode_steps=a.decode_steps, rhos=RHOS, arms=ARMS,
        windows=WINDOWS, bands=[list(b) for b in BANDS], rho_band=RHO_BAND,
        band_arms=BAND_ARMS, win_keep=WIN_KEEP, tail_w=TAIL_W,
        score_convention='window-MEAN attention mass per entry (ranking-'
                         'equivalent to v1 window sums; sigma* is in '
                         'mean-mass units)',
        excluded_calibration_indices=sorted(CAL_EXCLUDE),
        excluded_v1_pilot_indices=sorted(V1_PILOT_EXCLUDE),
        v2_pilot_indices=used,
        geometry=dict(layers=n_layers, q_heads=n_q, kv_heads=n_kv, grp=grp,
                      head_dim=d),
        versions=dict(torch=torch.__version__,
                      transformers=__import__('transformers').__version__),
    )

    def dump(tag):
        result['seconds_total'] = round(time.time() - t_start, 1)
        result['timing'] = timing
        result['temps_c'] = temps
        result['temp_max'] = max((t for t in temps if t >= 0), default=None)
        result['dump_tag'] = tag
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=1)

    # ------------------------------------------------------------- phase A
    tA = time.time()
    for pi, it in enumerate(items):
        if (time.time() - t_start) / 60 > a.max_minutes:
            print(f"  [budget] {a.max_minutes} min reached at prompt {pi}",
                  flush=True)
            break
        thermal_gate(temps)
        prompt = tmpl.format(context=it['context'], input=it['input'])
        ids = tok(prompt, return_tensors='pt', truncation=True,
                  max_length=a.maxlen).input_ids.to(device)
        S = ids.shape[1]
        t0 = time.time()
        cache = TelemetryCache()
        first_logits, win, tail_q = prefill_v2(
            model, ids, cache, n_layers, n_kv, grp, d, device)
        w32 = tail_window_scores(tail_q, cache, n_layers, n_kv, grp, d, S,
                                 device, w=32)
        fm, base_txt, eos_at, gen_frac = decode_with_telemetry(
            model, tok, cache, first_logits, S, n_layers, n_kv, grp, d,
            a.decode_steps, device)
        base_score = float(scorer(base_txt, it['answers']))
        scores_by = {'w1024': win[1024], 'w256': win[256], 'w32': w32,
                     'shuf': shuf_scores(a.seed, used[pi], (n_layers, n_kv, S))}
        cut = max(S - WIN_KEEP, 1)

        # u per arm (per-cell, this prompt) -- w32deg comes later (needs sigma*)
        u_mean, u_median = {}, {}
        for key in ('w1024', 'w256', 'w32', 'shuf'):
            us = u_cells(scores_by[key], fm, cut, n_layers, n_kv)
            u_mean[key] = float(np.mean(us))
            u_median[key] = float(np.median(us))

        # pruned decodes for the sigma-free arms (GPU-resident cache)
        for rho in RHOS:
            B_keep = max(int(rho * S), 64)
            for arm in ('w1024', 'w256', 'w32', 'shuf'):
                ptxt, kept = pruned_decode_gpu(
                    model, tok, TelemetryCache, cache, scores_by[arm], S,
                    B_keep, first_logits, a.task, n_layers, device)
                sweep_rows.append(dict(
                    prompt=pi, longbench_idx=used[pi], rho=rho, arm=arm,
                    task_score=float(scorer(ptxt, it['answers'])),
                    pred=ptxt[:60], B_keep=int(B_keep),
                    kept_per_layer=float(kept)))
            print(f"    rho={rho:.2f} " + " ".join(
                f"{r['arm']}={r['task_score']:.2f}" for r in sweep_rows[-4:]),
                flush=True)

        # offload KV for phases C/D (prefill reuse, host RAM)
        kv_cpu = []
        for L in range(n_layers):
            K, V = cache.snap[L]
            kv_cpu.append((K[:, :, :S].detach().cpu().clone(),
                           V[:, :, :S].detach().cpu().clone()))
        store.append(dict(
            longbench_idx=used[pi], S=S, cut=cut, kv=kv_cpu,
            first_logits=first_logits.detach().cpu(), answers=it['answers'],
            fm=fm, w32=w32, w1024=win[1024], w256=win[256],
            u_mean=u_mean, u_median=u_median))

        temps.append(gpu_temp())
        per_prompt.append(dict(
            i=pi, longbench_idx=used[pi], S=int(S), fp16_score=base_score,
            eos_at=eos_at, gen_mass_frac=round(gen_frac, 4),
            pred=base_txt[:60], sec_total=round(time.time() - t0, 1),
            temp_after=temps[-1]))
        print(f"  [{pi}] idx={used[pi]} S={S} fp16={base_score:.2f} "
              f"t={time.time() - t0:.0f}s temp={temps[-1]}C", flush=True)
        del cache, tail_q, win
        torch.cuda.empty_cache()

    n_done = len(per_prompt)
    timing['sec_phase_a'] = round(time.time() - tA, 1)
    result.update(n_prompts=n_done, per_prompt=per_prompt)
    result['u_per_prompt'] = [
        {k: dict(mean=st['u_mean'][k], median=st['u_median'][k])
         for k in ('w1024', 'w256', 'w32', 'shuf')} for st in store]
    dump('after_phase_A')

    # ------------------------------------------- phase B (CPU): sigma* + u
    tB = time.time()
    print("  [calib] bisecting sigma* on recorded telemetry ...", flush=True)
    calib, _evals = calibrate_sigma(store, a.seed, n_layers, n_kv)
    sigma_star = calib.get('sigma_star')
    print(f"  [calib] {calib.get('status')} sigma*={sigma_star} "
          f"resid={calib.get('residual')}", flush=True)

    # exact u(w32deg @ sigma*) per prompt (mean AND median)
    if sigma_star:
        for st in store:
            Z = znoise(a.seed, st['longbench_idx'], st['w32'].shape)
            us = u_cells(st['w32'] + sigma_star * Z, st['fm'], st['cut'],
                         n_layers, n_kv)
            st['u_mean']['w32deg'] = float(np.mean(us))
            st['u_median']['w32deg'] = float(np.median(us))
        calib['u_w32deg_at_sigma_star'] = float(
            np.mean([st['u_mean']['w32deg'] for st in store]))
        calib['u_match_residual_exact'] = (
            calib['u_w32deg_at_sigma_star'] - calib['u_target_w256'])
    result['sigma_calibration'] = calib

    u_keys = ['w1024', 'w256', 'w32'] + (['w32deg'] if sigma_star else []) + ['shuf']
    result['u_per_prompt'] = [
        {k: dict(mean=st['u_mean'][k], median=st['u_median'][k])
         for k in u_keys if k in st['u_mean']} for st in store]
    result['u_table'] = {
        key: dict(
            mean=float(np.mean([st['u_mean'][key] for st in store])),
            mean_se=boot_se([st['u_mean'][key] for st in store]),
            median=float(np.mean([st['u_median'][key] for st in store])),
            median_se=boot_se([st['u_median'][key] for st in store]))
        for key in u_keys}

    # age-band occupancy / mass / mistake tables at rho=RHO_BAND (telemetry only)
    nb = len(BANDS)
    occ = np.zeros(nb)
    mass = np.zeros(nb)
    retain = {arm: np.zeros(nb) for arm in ARMS}
    ret_n = {arm: np.zeros(nb) for arm in ARMS}
    evmass = {arm: np.zeros(nb) for arm in ARMS}
    omiss = {arm: np.zeros(nb) for arm in ARMS}
    omiss_n = {arm: np.zeros(nb) for arm in ARMS}
    for st in store:
        S, cut, fm = st['S'], st['cut'], st['fm']
        ages = S - np.arange(S)
        band_of = [(ages >= a1) & (ages < a2) & (np.arange(S) < cut)
                   for a1, a2 in BANDS]
        fm_tot = fm.sum(axis=(0, 1))
        B_keep = max(int(RHO_BAND * S), 64)
        for b in range(nb):
            occ[b] += band_of[b].mean()
            mass[b] += fm_tot[band_of[b]].sum() / max(fm_tot.sum(), 1e-9)
        arm_sc = {'w1024': st['w1024'], 'w256': st['w256'], 'w32': st['w32'],
                  'shuf': shuf_scores(a.seed, st['longbench_idx'],
                                      st['w32'].shape)}
        if sigma_star:
            arm_sc['w32deg'] = st['w32'] + sigma_star * znoise(
                a.seed, st['longbench_idx'], st['w32'].shape)
        for arm, sc in arm_sc.items():
            for L in range(n_layers):
                for h in range(n_kv):
                    kmask = np.zeros(S, bool)
                    kmask[kept_indices(sc[L, h], S, B_keep)] = True
                    okeep = np.zeros(S, bool)
                    okeep[kept_indices(fm[L, h], S, B_keep)] = True
                    cellm = fm[L, h]
                    tot = max(cellm.sum(), 1e-9)
                    for b in range(nb):
                        m = band_of[b]
                        if m.sum():
                            retain[arm][b] += kmask[m].mean()
                            ret_n[arm][b] += 1
                            evmass[arm][b] += cellm[m & ~kmask].sum() / tot
                            ob = m & okeep
                            if ob.sum():
                                omiss[arm][b] += (ob & ~kmask).sum() / ob.sum()
                                omiss_n[arm][b] += 1
    result['age_band'] = dict(
        rho=RHO_BAND, edges=[32, 512, 2048, 8192, 10 ** 9],
        occupancy=[float(x) for x in occ / max(n_done, 1)],
        future_mass_share=[float(x) for x in mass / max(n_done, 1)],
        retain_frac={arm: [float(x) for x in retain[arm] / np.maximum(ret_n[arm], 1)]
                     for arm in retain},
        evicted_mass_share={arm: [float(x / max(n_done * n_layers * n_kv, 1))
                                  for x in evmass[arm]] for arm in evmass},
        oracle_miss_frac={arm: [float(x) for x in
                                omiss[arm] / np.maximum(omiss_n[arm], 1)]
                          for arm in omiss})
    timing['sec_phase_b_cpu'] = round(time.time() - tB, 1)
    dump('after_calibration')

    # ---------------------------------------- phase C (GPU): w32deg decodes
    tC = time.time()
    if sigma_star:
        for pi, st in enumerate(store):
            if (time.time() - t_start) / 60 > a.max_minutes:
                print(f"  [budget] reached in phase C at prompt {pi}", flush=True)
                break
            thermal_gate(temps)
            sc = st['w32'] + sigma_star * znoise(
                a.seed, st['longbench_idx'], st['w32'].shape)
            for rho in RHOS:
                B_keep = max(int(rho * st['S']), 64)
                ptxt, kept = pruned_decode_cpu(
                    model, tok, TelemetryCache, st['kv'], sc, st['S'], B_keep,
                    st['first_logits'], a.task, n_layers, device)
                sweep_rows.append(dict(
                    prompt=pi, longbench_idx=st['longbench_idx'], rho=rho,
                    arm='w32deg', task_score=float(scorer(ptxt, st['answers'])),
                    pred=ptxt[:60], B_keep=int(B_keep),
                    kept_per_layer=float(kept)))
            temps.append(gpu_temp())
            print(f"  [C {pi}] w32deg done temp={temps[-1]}C", flush=True)
    result['sweep'] = sweep_rows
    timing['sec_phase_c'] = round(time.time() - tC, 1)

    # drop table
    base = np.array([p['fp16_score'] for p in per_prompt])
    result['fp16_mean'] = float(base.mean())
    drop_table = {}
    for rho in RHOS:
        drop_table[f'{rho:.2f}'] = {}
        for arm in ARMS:
            sc = np.array([r['task_score'] for r in sweep_rows
                           if r['rho'] == rho and r['arm'] == arm])
            if not len(sc):
                continue
            dd = base[:len(sc)] - sc
            drop_table[f'{rho:.2f}'][arm] = dict(
                n=len(sc), mean_score=float(sc.mean()), drop=float(dd.mean()),
                drop_se=boot_se(dd))
    result['drop_table'] = drop_table
    dump('after_sweep')

    # -------- phase D (GPU): band-restricted decodes -- PILOTS ONLY.
    # The sealed governed design (GO-P-2026-077) drops this phase: the
    # statistic failed its own n=32 replication test, recorded pre-seal.
    if a.band_phase:
        tD = time.time()
        band_rows = []
        for pi, st in enumerate(store):
            if (time.time() - t_start) / 60 > a.max_minutes:
                print(f"  [budget] reached in phase D at prompt {pi}", flush=True)
                break
            thermal_gate(temps)
            for band in BANDS:
                for arm in BAND_ARMS:
                    btxt, n_band, n_evict = band_pruned_decode(
                        model, tok, TelemetryCache, st['kv'], st[arm],
                        st['S'], band, RHO_BAND, st['first_logits'], a.task,
                        n_layers, device)
                    band_rows.append(dict(
                        prompt=pi, band=list(band), arm=arm,
                        task_score=float(scorer(btxt, st['answers'])),
                        pred=btxt[:60], band_n=n_band, band_evicted=n_evict))
            temps.append(gpu_temp())
            print(f"  [D {pi}] bands done temp={temps[-1]}C", flush=True)
        result['band_rows'] = band_rows
        timing['sec_phase_d'] = round(time.time() - tD, 1)

        band_table = []
        for band in BANDS:
            cols = {}
            for arm in BAND_ARMS:
                v = [r['task_score'] for r in band_rows
                     if r['band'] == list(band) and r['arm'] == arm]
                cols[arm] = np.array(v)
            n = min((len(v) for v in cols.values()), default=0)
            if n:
                g = cols[BAND_ARMS[0]][:n] - cols[BAND_ARMS[-1]][:n]
                band_table.append(dict(
                    band=list(band), n=int(n),
                    **{f'{arm}_mean': float(cols[arm][:n].mean()) for arm in BAND_ARMS},
                    **{f'{arm}_drop': float((base[:n] - cols[arm][:n]).mean())
                       for arm in BAND_ARMS},
                    gap_mean=float(g.mean()), gap_se=boot_se(g)))
        result['band_table'] = band_table

    dump('final')
    print('===KVAW2-JSON===')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('sweep', 'band_rows', 'u_per_prompt')},
                     indent=1))
    print('===END===')


if __name__ == '__main__':
    sys.exit(main())
