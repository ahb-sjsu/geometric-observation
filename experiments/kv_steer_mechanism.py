# Mechanism diagnostic for the KV steering construction (GO-P-2026-055 pre-work).
#
# The task-score pilot at 1.5B was uninformative (floor effects, n=24, +-0.13
# noise) AND its point estimate ran against prediction.  Before spending GPU
# hours on a 7B task run, test the mechanism directly in the CONSUMER'S OWN
# metric on captured activations -- no generation, no task, pure numpy:
#
#   Q1  How much query energy does the top-r eigenspace of P_C = E[q q^T]
#       actually capture?  If r=16 of 128 captures little, then "preserve"
#       still dumps error into directions the queries read, and the contrast
#       between the arms is weak BY CONSTRUCTION.
#   Q2  At matched per-token error norm, does error INSIDE the read subspace
#       raise softmax-attention KL more than error in the complement?
#       This is the claim, stripped of task noise.
#   Q3  Does the ordering hold per layer / per head, and how does it scale
#       with r and with the reference bit-width?
#
# A failure here means the steering construction -- not the task metric -- is
# what needs rethinking, and no amount of 7B compute would fix it.
#
# Usage: python experiments/kv_steer_mechanism.py --model <id> [--layers 0,7,14,21,27]
# Output: sentinel JSON ===KVMECH-JSON===.  MIT.
import argparse
import json
import sys
import time
from collections import defaultdict

import numpy as np
import torch

_cap = defaultdict(dict)
_ctr = {"i": 0}
_on = {"on": False}


def install(mod):
    orig = mod.apply_rotary_pos_emb

    def patched(q, k, cos, sin, unsqueeze_dim=1):
        q2, k2 = orig(q, k, cos, sin, unsqueeze_dim)
        if _on["on"]:
            _cap[_ctr["i"]]["q"] = q2.detach().float().cpu().numpy()
            _cap[_ctr["i"]]["k"] = k2.detach().float().cpu().numpy()
        _ctr["i"] += 1
        return q2, k2

    mod.apply_rotary_pos_emb = patched


def softmax(x):
    x = x - x.max(-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(-1, keepdims=True)


def attn_kl(K, Kq, Q, d):
    p = softmax((Q @ K.T) / np.sqrt(d))
    q = softmax((Q @ Kq.T) / np.sqrt(d))
    return float((p * np.log((p + 1e-12) / (q + 1e-12))).sum(-1).mean())


def uniform_asym(x, axis, bits):
    q = 2 ** bits - 1
    lo, hi = x.min(axis, keepdims=True), x.max(axis, keepdims=True)
    sc = np.where(hi - lo > 0, (hi - lo) / q, 1.0)
    return lo + np.clip(np.round((x - lo) / sc), 0, q) * sc


def steer(g, V, mode):
    """Place g's norm inside (destroy) or outside (preserve) span(V)."""
    r = np.linalg.norm(g, axis=1, keepdims=True)
    proj = (g @ V) @ V.T
    comp = proj if mode == "destroy" else g - proj
    n = np.linalg.norm(comp, axis=1, keepdims=True)
    u = np.where(n > 1e-8, comp / (n + 1e-12), V[:, -1][None, :])
    return r * u


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--layers", default="")
    ap.add_argument("--seq", type=int, default=1024)
    ap.add_argument("--rlist", default="4,8,16,32,64")
    ap.add_argument("--bitlist", default="4,3,2")
    ap.add_argument("--device", default="cpu",
                    help="one 1k-token forward pass is all this needs; CPU by "
                         "default so it never contends with a GPU run")
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.models.qwen2 import modeling_qwen2 as QM

    tok = AutoTokenizer.from_pretrained(a.model)
    dtype = torch.bfloat16 if a.device == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        a.model, dtype=dtype, attn_implementation="sdpa").to(a.device).eval()
    cfg = model.config
    d = getattr(cfg, "head_dim", None) or cfg.hidden_size // cfg.num_attention_heads
    n_kv, n_q = cfg.num_key_value_heads, cfg.num_attention_heads
    grp, nL = n_q // n_kv, cfg.num_hidden_layers
    layers = ([int(x) for x in a.layers.split(",")] if a.layers
              else sorted({0, nL // 4, nL // 2, 3 * nL // 4, nL - 1}))
    print(f"{a.model}: layers={nL} q={n_q} kv={n_kv} grp={grp} d={d}; probing {layers}",
          flush=True)

    install(QM)                      # <- the capture patch must be installed
    rows = [json.loads(l) for l in
            open("/archive/longbench/data/passage_retrieval_en.jsonl", encoding="utf-8")]
    text = rows[0]["context"]
    ids = tok(text, return_tensors="pt", truncation=True,
              max_length=a.seq).input_ids.to(a.device)
    _ctr["i"] = 0
    _cap.clear()
    _on["on"] = True
    with torch.no_grad():
        model(ids)
    _on["on"] = False
    print(f"captured {len(_cap)} layers, seq={ids.shape[1]}", flush=True)

    rlist = [int(x) for x in a.rlist.split(",")]
    bitlist = [int(x) for x in a.bitlist.split(",")]
    energy, kls = [], []
    t0 = time.time()
    for L in layers:
        q, k = _cap[L]["q"][0], _cap[L]["k"][0]
        for h in range(n_kv):
            K = k[h].astype(np.float64)
            Q = q[h * grp:(h + 1) * grp].reshape(-1, d).astype(np.float64)
            Pc = Q.T @ Q / Q.shape[0]
            w = np.sort(np.linalg.eigvalsh(Pc))[::-1]
            tot = w.sum()
            for r in rlist:
                energy.append(dict(layer=L, head=h, r=r,
                                   frac=float(w[:r].sum() / tot)))
            V_all = np.linalg.eigh(Pc)[1]
            for r in rlist:
                V = V_all[:, -r:]
                for b in bitlist:
                    g = uniform_asym(K, 0, b) - K
                    dP, dD = steer(g, V, "preserve"), steer(g, V, "destroy")
                    assert abs(np.linalg.norm(dP) - np.linalg.norm(dD)) < 1e-6 * np.linalg.norm(dP)
                    kls.append(dict(
                        layer=L, head=h, r=r, bits=b,
                        kl_preserve=attn_kl(K, K + dP, Q, d),
                        kl_destroy=attn_kl(K, K + dD, Q, d),
                        ref_norm=float(np.linalg.norm(g, axis=1).mean())))
        print(f"  layer {L} done ({time.time()-t0:.0f}s)", flush=True)

    def agg(sel, key):
        v = [x[key] for x in kls if sel(x)]
        return float(np.mean(v)) if v else float("nan")

    print("\nquery energy captured by the top-r eigenspace of P_C = E[qq^T]:")
    for r in rlist:
        f = [e["frac"] for e in energy if e["r"] == r]
        print(f"  r={r:3d}/{d}: mean {np.mean(f):.3f}  min {np.min(f):.3f}  "
              f"max {np.max(f):.3f}")
    print("\nattention KL at matched error norm (destroy = error in read subspace):")
    summary = {}
    for r in rlist:
        for b in bitlist:
            sel = lambda x, r=r, b=b: x["r"] == r and x["bits"] == b
            kp, kd = agg(sel, "kl_preserve"), agg(sel, "kl_destroy")
            wins = sum(1 for x in kls if sel(x) and x["kl_destroy"] > x["kl_preserve"])
            tot = sum(1 for x in kls if sel(x))
            summary[f"r{r}_b{b}"] = dict(kl_preserve=kp, kl_destroy=kd,
                                         ratio=kd / max(kp, 1e-12),
                                         destroy_worse_frac=wins / max(tot, 1))
            print(f"  r={r:3d} bits={b}: KL_preserve={kp:.4e}  KL_destroy={kd:.4e}  "
                  f"ratio={kd/max(kp,1e-12):6.2f}x  destroy-worse in {wins}/{tot} heads")

    result = dict(model=a.model, seq=int(ids.shape[1]), layers=layers,
                  geometry=dict(layers=nL, q_heads=n_q, kv_heads=n_kv, grp=grp, head_dim=d),
                  rlist=rlist, bitlist=bitlist,
                  energy_fraction={str(r): float(np.mean([e["frac"] for e in energy
                                                          if e["r"] == r]))
                                   for r in rlist},
                  summary=summary, per_head=kls, seconds=round(time.time() - t0, 1))
    print("===KVMECH-JSON===")
    print(json.dumps(result, indent=1))
    print("===END===")


if __name__ == "__main__":
    sys.exit(main())
