#!/usr/bin/env python
"""T1 arm R: the real consumer. Learn a Llama attention head's read operator from black-box
bfloat16 score queries, and serve keys described for the learned operator.

Report-only arm of the T1 registration (drafts/T1-WORKED-RESULT-REGISTRATION-DRAFT.md; theory:
the T1 note, paper/t1-learn-then-serve, version 4.1). There are no bars. Under the registration
the governed instance runs once after the seal (owner, 2026-11-18). v1.1 (2026-11-18): the
governed analysis checks the instrument hashes recorded in the prereg (cold reread, finding B6).

THE CONSUMER
  Symbols are the post-RoPE key vectors k in R^d of one KV head of unsloth/Llama-3.2-3B
  (d = 128). The consumer is that head group's attention scores for a fixed set of n queries
  (the group's 3 query heads at row 0 of the batch, n = 3 x 256):

      C(k) = Q k / sqrt(d),   computed in bfloat16 on the GPU,   output metric G = (d/n) I.

  So the read operator is P = Q^T Q / n, as the GO-P-2026-027 harness computes it. C is
  linear, so in exact arithmetic (A1) holds with nu = 0 and one probe point would recover P.
  The black box returns bfloat16 scores of bfloat16 inputs, so it is a noisy consumer in the
  sense of the note's Remark 17, and every Jacobian carries rounding noise. That is what this
  arm measures.

PROBING (on Atlas GPU 1)
  Probe points are keys drawn uniformly with replacement from the source keys of the head
  (all 8 rows x 256 tokens).

  At each point, one Jacobian estimate uses a random orthonormal basis v_1..v_d and central
  differences with step h = sqrt(tr Sigma / d):
      J_hat = sum_j [C(x + h v_j) - C(x - h v_j)] / (2h) v_j^T,
  which costs 2d queries.

  Two estimators:
  - plain: mean of J1^T G J1, costing 2d queries per point;
  - paired (the note's Remark 17): mean of sym(J1^T G J2) with an independent
    second basis, costing 4d queries per point. It removes the noise bias E[N^T G N] when
    the two noises are independent. A fixed rounding rule is deterministic, so this
    independence comes only from the random bases. Whether it is enough is part of what
    the arm reports.

  Each estimator is saved at the probe counts m in `ms`, for several seeds. Within a seed the
  probe sets are nested: each m uses a prefix of one draw of max(ms) points.

DESCRIPTION AND SERVING (local CPU)
  Source law: the head's keys. mu is their mean and Sigma = Cov + 1e-6 I (the GO-027
  convention). The holder sees S = H k + U, where:
  - H is 8 x d Gaussian, drawn with default_rng(holder_seed);
  - U ~ N(0, s2 I) with s2 = tr Sigma / d.

  At each matched rate R (bits per key vector, alpha = 1) there are these designs:
  - reconstruction: water-filling on Sigma;
  - oracle: the true P;
  - learned: P_hat (paired and plain at the largest m, and paired at the smallest m),
    one design per seed.

  Each design is applied to the real keys through the forward Gaussian test channel
      k_hat = mu + Sigma^{1/2} [ (I - X) Sigma^{-1/2} (k - mu) + v ],  v ~ N(0, (I - X) X),
  which has error covariance Delta = Sigma^{1/2} X Sigma^{1/2} for any source with
  covariance Sigma.

  Reported for each design:
  - tr(P Delta), and the realized read error on the keys;
  - the leakage given by the Gaussian formula for the design (the frontier for a Gaussian
    source with the keys' covariance; RLD-III.3, an [exploratory] ledger row, makes that
    region achievable for a memoryless non-Gaussian source). It is not the leakage of the
    forward channel actually applied to the keys;
  - the softmax divergence KL(softmax(Q K^T / sqrt d) || softmax(Q K_hat^T / sqrt d)),
    taken over the row-0 queries and keys, with a full (non-causal) softmax of the 768
    queries over the 256 keys. The draws are common random numbers across designs.

COMMANDS
  On Atlas, GPU 1 only, CPUs pinned away from CPU 0, thermally throttled:
    CUDA_VISIBLE_DEVICES=1 HF_HUB_OFFLINE=1 taskset -c 12-15 nice -n 19 \\
      python t1_arm_r_llama.py capture --instance smoke --out smoke.npz
    (for the governed instance: --instance governed --sealed <prereg sha256>)
  Locally, in the repo:
    python experiments/t1_arm_r_llama.py analyze --capture smoke.npz [--out smoke.json]
    python experiments/t1_arm_r_llama.py analyze --capture gov.npz --governed --prereg <file>

  The governed analysis refuses unless all of these hold:
  - the prereg passes the guard of t1_worked_result.check_governed, naming both T1 scripts
    (which also checks that both scripts and the solver match the hashes recorded in the
    prereg's `instruments_sha256:` block);
  - the capture recorded that prereg's sha256;
  - the capture was made by the sealed version of this script: its recorded script hash (taken
    over the text, with line endings normalized) equals the prereg's recorded hash;
  - the capture's UTC time is later than the prereg's commit.
  The smoke instance (layer 12, its own text and seeds) is the only one that may run
  before the seal.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

MODEL = "unsloth/Llama-3.2-3B"
SCRIPT_REL = "experiments/t1_arm_r_llama.py"
VERSION = "1.1"

SMOKE_TEXT = (
    "The survey crew left the harbour before dawn and followed the coast north for three days. "
    "They measured the depth of every inlet, logged the tides, and sketched the cliffs where the "
    "charts disagreed. On the fourth morning fog closed in, so they anchored behind a low island "
    "and spent the day copying their notes into the ledger. The cook argued that the old maps were "
    "better than the new ones; the navigator said that every map is right about something. When "
    "the fog lifted they found that the island was not on either chart, and they named it after "
    "the cook, who refused the honour and asked for a second ration of coffee instead. ")

# the GO-P-2026-027 corpus (literary openings), for the governed instance
GOVERNED_TEXT = (
    "In the beginning the Universe was created. This has made a lot of people very angry and "
    "been widely regarded as a bad move. It was the best of times, it was the worst of times. "
    "Stately, plump Buck Mulligan came from the stairhead, bearing a bowl of lather. Mother died "
    "today. Or maybe yesterday, I don't know. The past is a foreign country; they do things "
    "differently there. Who is John Galt? Ships at a distance have every man's wish on board. "
    "You don't know about me without you have read a book by the name of Tom Sawyer, but that "
    "ain't no matter. It was a bright cold day in April, and the clocks were striking thirteen. ")

INSTANCES = {
    "smoke": dict(layers=[12], text=SMOKE_TEXT, rows=8, seq=256, seeds=3, ms=[1, 8, 32],
                  rates=[64.0, 128.0], kl_draws=2, base_seed=7, holder_seed=7, holder_rows=8),
    # held out from GO-P-2026-026's exploratory {8, 16}, GO-P-2026-027's {4, 20}, and the smoke {12}
    "governed": dict(layers=[6, 24], text=GOVERNED_TEXT, rows=8, seq=256, seeds=5, ms=[1, 8, 32, 128],
                     rates=[32.0, 64.0, 128.0, 256.0], kl_draws=4, base_seed=20261117,
                     holder_seed=20261117, holder_rows=8),
}


def text_sha256(path):
    return hashlib.sha256(Path(path).read_text(encoding="utf-8").encode("utf-8")).hexdigest()


# ============================================================================ capture (Atlas)
def capture(args):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers.models.llama import modeling_llama
    from batch_probe import ThermalController   # required on Atlas (thermal rule)

    inst = INSTANCES[args.instance]
    if args.instance == "governed" and not (args.sealed and len(args.sealed) == 64):
        raise SystemExit("refusing a governed capture without --sealed <prereg sha256>")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "1":
        raise SystemExit("run with CUDA_VISIBLE_DEVICES=1 (Atlas GPU 1 only)")
    thermal = ThermalController(target_temp=80.0, max_threads=4, min_threads=1)
    thermal.start()
    torch.set_num_threads(max(1, min(4, thermal.get_threads())))
    t0 = time.time()

    layers = inst["layers"]
    cap, ctr = {}, {"i": 0}
    orig = modeling_llama.apply_rotary_pos_emb

    def patched(q, k, cos, sin, *a, **kw):
        q2, k2 = orig(q, k, cos, sin, *a, **kw)
        if ctr["i"] in layers:
            cap[ctr["i"]] = (q2.detach().float().cpu().numpy(), k2.detach().float().cpu().numpy())
        ctr["i"] += 1
        return q2, k2
    modeling_llama.apply_rotary_pos_emb = patched

    dev = "cuda"
    tok = AutoTokenizer.from_pretrained(MODEL)
    try:
        model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16)
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16)
    model = model.to(dev).eval()
    d = model.config.head_dim
    nkv = model.config.num_key_value_heads
    grp = model.config.num_attention_heads // nkv
    rows, S = inst["rows"], inst["seq"]
    ids = tok(inst["text"], return_tensors="pt").input_ids
    ids = ids.repeat(1, int(np.ceil(rows * S / ids.shape[1])))[:, :rows * S].reshape(rows, S).to(dev)
    with torch.no_grad():
        model(ids)
    if sorted(cap) != sorted(layers):
        raise SystemExit(f"RoPE capture failed: got layers {sorted(cap)}, wanted {layers}")
    del model
    torch.cuda.empty_cache()
    print(f"captured layers {sorted(cap)}; d={d} n_kv={nkv} grp={grp} ({time.time() - t0:.1f} s)", flush=True)

    out = {}
    ms = inst["ms"]
    mmax = max(ms)
    for L in layers:
        q, k = cap[L]
        for h in range(nkv):
            K = k[:, h].reshape(-1, d).astype(np.float32)                       # rows*S x d
            Qc = q[0, h * grp:(h + 1) * grp].reshape(-1, d).astype(np.float32)  # n x d
            n = Qc.shape[0]
            Kd = K.astype(np.float64)
            hstep = float(np.sqrt(np.trace(np.cov(Kd, rowvar=False)) / d))
            Qg = torch.tensor(Qc, dtype=torch.bfloat16, device=dev)
            scale = torch.tensor(1.0 / np.sqrt(d), dtype=torch.bfloat16, device=dev)

            def consumer(X):   # black box: bf16 in, bf16 scores out
                return (X.to(torch.bfloat16) @ Qg.T) * scale

            Pplain = np.zeros((inst["seeds"], len(ms), d, d), np.float64)
            Ppair = np.zeros_like(Pplain)
            idx_all = np.zeros((inst["seeds"], mmax), np.int64)
            for s in range(inst["seeds"]):
                rng = np.random.default_rng([inst["base_seed"], L, h, s])
                idx = rng.integers(0, K.shape[0], size=mmax)
                idx_all[s] = idx
                acc_plain = torch.zeros((d, d), dtype=torch.float64, device=dev)
                acc_pair = torch.zeros_like(acc_plain)
                im = 0
                for i in range(mmax):
                    x = torch.tensor(K[idx[i]], dtype=torch.float32, device=dev)
                    Js = []
                    for _ in range(2):
                        V = torch.tensor(np.linalg.qr(rng.standard_normal((d, d)))[0], dtype=torch.float32, device=dev)
                        Xp, Xm = x[None, :] + hstep * V.T, x[None, :] - hstep * V.T     # row j = x +- h v_j
                        A = (consumer(Xp).double() - consumer(Xm).double()) / (2 * hstep)  # d x n, row j = (J v_j)^T
                        Js.append(A.T @ V.T.double())                                    # n x d
                    J1, J2 = Js
                    acc_plain += (d / n) * (J1.T @ J1)
                    M12 = (d / n) * (J1.T @ J2)
                    acc_pair += (M12 + M12.T) / 2
                    if i + 1 == ms[im]:
                        Pplain[s, im] = (acc_plain / (i + 1)).cpu().numpy()
                        Ppair[s, im] = (acc_pair / (i + 1)).cpu().numpy()
                        im += 1
            key = f"L{L}_h{h}"
            out[key + "_K"], out[key + "_Q"] = K, Qc
            out[key + "_Pplain"], out[key + "_Ppaired"] = Pplain.astype(np.float32), Ppair.astype(np.float32)
            out[key + "_hstep"], out[key + "_idx"] = np.array(hstep), idx_all
            print(f"  L{L} h{h}: n={n} h={hstep:.4f} done ({time.time() - t0:.1f} s)", flush=True)
    thermal.stop()

    import transformers
    meta = dict(instrument=SCRIPT_REL, version=VERSION, instance=args.instance, model=MODEL,
                d=d, n_kv=nkv, grp=grp, layers=layers, ms=ms, seeds=inst["seeds"],
                script_sha256=text_sha256(__file__), sealed=args.sealed,
                capture_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                torch=torch.__version__, transformers=transformers.__version__,
                gpu=torch.cuda.get_device_name(0), cuda_visible_devices=os.environ.get("CUDA_VISIBLE_DEVICES"),
                wall_seconds=round(time.time() - t0, 1))
    np.savez_compressed(args.out, meta=json.dumps(meta), **out)
    print(f"wrote {args.out}: {json.dumps(meta)}", flush=True)


# ============================================================================ analyze (local)
def _sym(A):
    return (A + A.T) / 2


def _msqrt(A, inv=False):
    w, V = np.linalg.eigh(_sym(A))
    w = np.clip(w, 1e-300, None)
    return (V * (w ** (-0.5 if inv else 0.5))) @ V.T


def _wf(Qt, R):
    """Rate-R (bits) reverse water-filling on the whitened weight Qt; returns whitened X."""
    w, U = np.linalg.eigh(_sym(Qt))
    w = np.clip(w, 1e-300, None)
    o = np.argsort(w)[::-1]
    w, U = w[o], U[:, o]
    p = len(w)
    for k in range(1, p + 1):
        th = 2.0 ** ((np.sum(np.log2(w[:k])) - 2 * R) / k)
        if w[k - 1] > th and (k == p or w[k] <= th):
            break
    return _sym((U * np.minimum(1.0, th / w)) @ U.T)


def _softmax(Z):
    Z = Z - Z.max(-1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(-1, keepdims=True)


def _kl(K, Kh, Q, d):
    p = _softmax(Q @ K.T / np.sqrt(d))
    q = _softmax(Q @ Kh.T / np.sqrt(d))
    return float((p * np.log((p + 1e-12) / (q + 1e-12))).sum(-1).mean())


def _rel_errs(Ph, P):
    relF = float(np.linalg.norm(Ph - P) / np.linalg.norm(P))
    w, U = np.linalg.eigh(_sym(P))
    keep = w > 1e-10 * w.max()
    Wm = U[:, keep] / np.sqrt(w[keep])
    relW = float(np.linalg.norm(_sym(Wm.T @ Ph @ Wm) - np.eye(int(keep.sum())), 2))
    return relF, relW


def analyze(args):
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "paper" / "tit-stationary"))
    sys.path.insert(0, str(root / "experiments"))
    import spectral_core as sc
    import t1_worked_result as t1

    z = np.load(args.capture)
    meta = json.loads(str(z["meta"]))
    inst = INSTANCES[meta["instance"]]
    seal = None
    if args.governed:
        if meta["instance"] != "governed":
            raise SystemExit("refusing: --governed analysis of a non-governed capture")
        seal = t1.check_governed(args.prereg, scripts=(t1.SCRIPT_REL, SCRIPT_REL))
        problems = []
        if meta.get("sealed") != seal["sha256"]:
            problems.append("the capture did not record this prereg's sha256")
        if meta.get("script_sha256") != seal["instruments_sha256"].get(SCRIPT_REL):
            problems.append("the capture was not made by the sealed version of this script")
        ct = t1._git("log", "-1", "--format=%cI", "--", seal["path"]).stdout.strip()
        if not ct or dt.datetime.fromisoformat(meta["capture_utc"]) <= dt.datetime.fromisoformat(ct):
            problems.append(f"the capture ({meta['capture_utc']}) does not postdate the prereg commit ({ct})")
        if problems:
            raise SystemExit("refusing the governed analysis: " + "; ".join(problems))
    elif meta["instance"] == "governed":
        raise SystemExit("refusing: a governed capture can only be analyzed with --governed --prereg")

    d, ms, seeds = meta["d"], meta["ms"], meta["seeds"]
    S = inst["seq"]
    heads = []
    for L in meta["layers"]:
        for h in range(meta["n_kv"]):
            key = f"L{L}_h{h}"
            K = z[key + "_K"].astype(np.float64)
            Qc = z[key + "_Q"].astype(np.float64)
            n = Qc.shape[0]
            P = Qc.T @ Qc / n
            Pplain = z[key + "_Pplain"].astype(np.float64)
            Ppair = z[key + "_Ppaired"].astype(np.float64)
            mu = K.mean(0)
            Sig = np.cov(K, rowvar=False) + 1e-6 * np.eye(d)
            s2 = float(np.trace(Sig) / d)
            S12, Sm12 = _msqrt(Sig), _msqrt(Sig, inv=True)
            Hh = np.random.default_rng(inst["holder_seed"]).standard_normal((inst["holder_rows"], d))
            Ht, SU = Hh @ S12, s2 * np.eye(inst["holder_rows"])
            wP = np.linalg.eigvalsh(P)
            rec = dict(layer=L, head=h, n_queries=n, h_step=float(z[key + "_hstep"]),
                       P_cond=float(wP.max() / max(wP.min(), 1e-300)),
                       P_eff_rank=float(wP.sum() ** 2 / (wP ** 2).sum()))

            # recovery of P
            recov = {}
            for name, arr, qpp in (("plain", Pplain, 2 * d), ("paired", Ppair, 4 * d)):
                for im, m in enumerate(ms):
                    errs = [_rel_errs(arr[s, im], P) for s in range(seeds)]
                    recov[f"{name}_m{m}"] = dict(queries=qpp * m, relF=[e[0] for e in errs], relW=[e[1] for e in errs])
                bias = arr[:, -1].mean(0) - P
                recov[f"{name}_bias_relF_at_mmax"] = float(np.linalg.norm(bias) / np.linalg.norm(P))
                recov[f"{name}_bias_trace_rel_at_mmax"] = float(np.trace(bias) / np.trace(P))
            rec["recovery"] = recov

            # matched-rate designs served to the real keys
            K0 = K[:S]                         # row 0 keys (rows are stored row-major)
            Z0 = (K0 - mu) @ Sm12
            crn = np.random.default_rng([inst["base_seed"], L, h, 99])
            E = [crn.standard_normal(Z0.shape) for _ in range(inst["kl_draws"])]
            Qt_true = _sym(S12 @ P @ S12)
            weights = {"reconstruction": [np.eye(d)], "oracle": [P],
                       f"learned_paired_m{ms[-1]}": [Ppair[s, -1] for s in range(seeds)],
                       f"learned_plain_m{ms[-1]}": [Pplain[s, -1] for s in range(seeds)],
                       f"learned_paired_m{ms[0]}": [Ppair[s, 0] for s in range(seeds)]}
            serve = {}
            for R in inst["rates"]:
                row = {}
                for name, Ws in weights.items():
                    vals = []
                    for W in Ws:
                        X = _wf(_sym(S12 @ W @ S12), R)
                        B = _msqrt((np.eye(d) - X) @ X)
                        kls, realized = [], []
                        for e in E:
                            Kh = mu + (Z0 @ (np.eye(d) - X) + e @ B) @ S12
                            kls.append(_kl(K0, Kh, Qc, d))
                            dk = Kh - K0
                            realized.append(float(np.einsum("ni,ij,nj->n", dk, P, dk).mean()))
                        vals.append(dict(read=float(np.trace(Qt_true @ X)), read_realized=float(np.mean(realized)),
                                         rate=float(-0.5 * sc.logdet2(X)), leak=float(sc.leak(X, Ht, SU)),
                                         kl=float(np.mean(kls))))
                    row[name] = vals
                kl_rec = row["reconstruction"][0]["kl"]
                row["kl_ratio_to_reconstruction"] = {nm: [v["kl"] / kl_rec for v in vs]
                                                     for nm, vs in row.items() if nm != "reconstruction"}
                serve[str(R)] = row
            rec["serve"] = serve
            heads.append(rec)
            print(f"  L{L} h{h}: relW paired m{ms[-1]} median {np.median(recov[f'paired_m{ms[-1]}']['relW']):.3g}, "
                  f"plain {np.median(recov[f'plain_m{ms[-1]}']['relW']):.3g}; KL ratio learned/rec at R={inst['rates'][-1]:.0f}: "
                  f"{np.median(serve[str(inst['rates'][-1])]['kl_ratio_to_reconstruction'][f'learned_paired_m{ms[-1]}']):.3f}",
                  file=sys.stderr)

    # summary across heads
    summ = dict(n_heads=len(heads))
    for name in ("plain", "paired"):
        for m in ms:
            summ[f"median_relW_{name}_m{m}"] = float(np.median([np.median(r["recovery"][f"{name}_m{m}"]["relW"]) for r in heads]))
            summ[f"median_relF_{name}_m{m}"] = float(np.median([np.median(r["recovery"][f"{name}_m{m}"]["relF"]) for r in heads]))
        summ[f"median_bias_trace_rel_{name}"] = float(np.median([r["recovery"][f"{name}_bias_trace_rel_at_mmax"] for r in heads]))
    for R in inst["rates"]:
        for nm in ("oracle", f"learned_paired_m{ms[-1]}", f"learned_plain_m{ms[-1]}", f"learned_paired_m{ms[0]}"):
            summ[f"median_kl_ratio_{nm}_R{R:.0f}"] = float(np.median(
                [np.median(r["serve"][str(R)]["kl_ratio_to_reconstruction"][nm]) for r in heads]))
        summ[f"median_kl_reconstruction_R{R:.0f}"] = float(np.median([r["serve"][str(R)]["reconstruction"][0]["kl"] for r in heads]))
    out = dict(instrument=SCRIPT_REL, version=VERSION, mode=meta["instance"],
               note=None if args.governed else "SMOKE: layer and text differ from the registration; not a governed result",
               capture_meta=meta, prereg=seal, instance={k: v for k, v in inst.items() if k != "text"},
               summary=summ, heads=heads)
    payload = json.dumps(out, indent=1)
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    print("===T1R-JSON===")
    print(payload)
    print("===END===")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("capture", help="on Atlas GPU 1: capture q/k and probe the black-box consumer")
    c.add_argument("--instance", choices=sorted(INSTANCES), required=True)
    c.add_argument("--out", required=True)
    c.add_argument("--sealed", help="sha256 of the sealed prereg (governed instance only)")
    a = sub.add_parser("analyze", help="locally: recovery, matched-rate designs, softmax divergence")
    a.add_argument("--capture", required=True)
    a.add_argument("--governed", action="store_true")
    a.add_argument("--prereg")
    a.add_argument("--out")
    args = ap.parse_args()
    if args.cmd == "capture":
        capture(args)
    else:
        if args.governed and not args.prereg:
            raise SystemExit("--governed needs --prereg")
        analyze(args)


if __name__ == "__main__":
    main()
