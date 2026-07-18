# GO-P-2026-027: prospective confirmation that Appendix-E's omission floor bites DOWNSTREAM on
# trained Llama read operators, as an asymptotic (infinite read-rate) phenomenon. Sealed BEFORE
# running. Design + bar were calibrated on GO-P-2026-026's EXPLORATORY follow-up (layers {8,16});
# this run is OUT-OF-SAMPLE on HELD-OUT layers {4,20} and a different corpus, so a pass is a genuine
# prospective generalization, not a replay.
#
#   Per head: P = Q^T Q / n (true read operator), Sx = Cov(K), P_hat = projector onto the top-R
#   eigvecs of P (a rank-R truncation -> omits P's tail directions). Floor covariance (infinite
#   read-rate limit of the P_hat water-filling family) = Sx^{1/2} Pi Sx^{1/2}, Pi = whitened kernel
#   of P_hat. Measure softmax-KL under that floor error (kl_floor) vs under the matched operator's
#   deep water-fill (~0 error, kl_matched). The omission floor manifests downstream iff kl_floor is a
#   large multiple of kl_matched. Also verify the READ-metric floor is reached (deep P_hat water-fill
#   drives tr(P Sigma_delta) to the predicted tr(P~ Pi)). Atlas GPU 1, thread-capped. MIT License.
"""Does the omission distortion floor manifest downstream on HELD-OUT trained Llama read operators?"""
from __future__ import annotations
import json
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.llama import modeling_llama

MODEL = "unsloth/Llama-3.2-3B"
LAYERS = [4, 20]            # HELD OUT from GO-P-2026-026's exploratory {8,16}
R_SUB = 16
# sealed bars (calibrated on the exploratory follow-up, which saw ratios ~1e5):
BAR_RATIO = 100.0          # asymptotic kl_floor / kl_matched
BAR_KLFLOOR = 0.01         # nats; floor must be a non-negligible downstream divergence
BAR_HEADS = 14             # of 16 heads must clear both, and median ratio must clear BAR_RATIO

TEXT = ("In the beginning the Universe was created. This has made a lot of people very angry and "
        "been widely regarded as a bad move. It was the best of times, it was the worst of times. "
        "Stately, plump Buck Mulligan came from the stairhead, bearing a bowl of lather. Mother died "
        "today. Or maybe yesterday, I don't know. The past is a foreign country; they do things "
        "differently there. Who is John Galt? Ships at a distance have every man's wish on board. "
        "You don't know about me without you have read a book by the name of Tom Sawyer, but that "
        "ain't no matter. It was a bright cold day in April, and the clocks were striking thirteen. ")


def sm(z): z = z - z.max(-1, keepdims=True); e = np.exp(z); return e / e.sum(-1, keepdims=True)
def sqrtm(M): w, U = np.linalg.eigh((M + M.T) / 2); w = np.clip(w, 0, None); return U @ np.diag(np.sqrt(w)) @ U.T
def kl(K, Kq, Q, d):
    p = sm(Q @ K.T / np.sqrt(d)); q = sm(Q @ Kq.T / np.sqrt(d))
    return float((p * np.log((p + 1e-12) / (q + 1e-12))).sum(-1).mean())
def wf_sigma(P_read, Sx, theta):
    Sh = sqrtm(Sx); Pt = (Sh @ P_read @ Sh); p, V = np.linalg.eigh((Pt + Pt.T) / 2); p = np.clip(p, 0, None)
    s = np.where(p > 1e-12, np.minimum(1.0, theta / np.maximum(p, 1e-300)), 1.0)
    return (Sh @ (V @ np.diag(s) @ V.T) @ Sh)


def main():
    cap, ctr = {}, {"i": 0}
    orig = modeling_llama.apply_rotary_pos_emb
    def patched(q, k, cos, sin, *a, **kw):
        q2, k2 = orig(q, k, cos, sin, *a, **kw)
        if ctr["i"] in LAYERS: cap[ctr["i"]] = (q2.detach().float().cpu().numpy(), k2.detach().float().cpu().numpy())
        ctr["i"] += 1
        return q2, k2
    modeling_llama.apply_rotary_pos_emb = patched

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(MODEL)
    m = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16).to(dev).eval()
    d = m.config.head_dim; nkv = m.config.num_key_value_heads; grp = m.config.num_attention_heads // nkv
    ids = tok(TEXT, return_tensors="pt").input_ids
    S = 256; ids = ids.repeat(1, int(np.ceil(8 * S / ids.shape[1])))[:, :8 * S].reshape(8, S).to(dev)
    with torch.no_grad(): m(ids)
    print(f"captured layers {list(cap)}; d={d} n_kv={nkv} grp={grp}", flush=True)

    rng = np.random.default_rng(27); rows = []
    for L in LAYERS:
        q, k = cap[L]
        for h in range(nkv):
            K = k[0, h].astype(np.float64); Q = q[0, h * grp:(h + 1) * grp].reshape(-1, d).astype(np.float64)
            P = Q.T @ Q / Q.shape[0]; Sx = np.cov(K, rowvar=False) + 1e-6 * np.eye(d)
            w, V = np.linalg.eigh((P + P.T) / 2); Vtop = V[:, -R_SUB:]; Phat = Vtop @ Vtop.T
            Sh = sqrtm(Sx); Pht = Sh @ Phat @ Sh; wk, Vk = np.linalg.eigh((Pht + Pht.T) / 2)
            ker = Vk[:, wk <= 1e-9 * max(wk.max(), 1)]; Pi = ker @ ker.T
            D_floor = float(np.trace((Sh @ P @ Sh) @ Pi))
            # read-metric floor reached under deep P_hat water-fill?
            pmax = float(np.clip(np.linalg.eigvalsh(Pht), 0, None).max() or 1.0)
            Sig_deep = wf_sigma(Phat, Sx, pmax * 1e-6); d_read = float(np.trace(P @ Sig_deep))
            read_reached = abs(d_read - D_floor) <= 0.5 * max(D_floor, 1e-9)
            # downstream: floor error vs matched-operator deep water-fill (~0)
            Ss = sqrtm(Sh @ Pi @ Sh)
            kl_floor = np.mean([kl(K, K + rng.standard_normal(K.shape) @ Ss.T, Q, d) for _ in range(6)])
            pmaxP = float(np.clip(np.linalg.eigvalsh((Sh @ P @ Sh)), 0, None).max() or 1.0)
            Ssm = sqrtm(wf_sigma(P, Sx, pmaxP * 1e-6))
            kl_match = np.mean([kl(K, K + rng.standard_normal(K.shape) @ Ssm.T, Q, d) for _ in range(6)])
            ratio = kl_floor / max(kl_match, 1e-12)
            rows.append({"layer": L, "head": h, "D_floor": D_floor, "d_read_deep": d_read,
                         "read_reached": bool(read_reached), "kl_floor": kl_floor,
                         "kl_matched": kl_match, "ratio": ratio,
                         "head_pass": bool(ratio >= BAR_RATIO and kl_floor >= BAR_KLFLOOR)})
            print(f"L{L}h{h} read_reached={read_reached} D_floor={D_floor:.2e} kl_floor={kl_floor:.3e} "
                  f"kl_matched={kl_match:.3e} ratio={ratio:.0f} pass={rows[-1]['head_pass']}", flush=True)

    n = len(rows)
    read_ok = sum(r["read_reached"] for r in rows)
    heads_pass = sum(r["head_pass"] for r in rows)
    med_ratio = float(np.median([r["ratio"] for r in rows]))
    med_klfloor = float(np.median([r["kl_floor"] for r in rows]))
    verdict = {"read_floor_reached_frac": [read_ok, n],
               "downstream_heads_pass_frac": [heads_pass, n],
               "median_ratio": med_ratio, "median_kl_floor": med_klfloor,
               "read_floor_ok": bool(read_ok >= BAR_HEADS),
               "downstream_floor_ok": bool(heads_pass >= BAR_HEADS and med_ratio >= BAR_RATIO)}
    out = {"claim": "GO-P-2026-027: omission floor manifests downstream on held-out Llama layers {4,20}",
           "prereg": "GO-P-2026-027", "model": MODEL, "layers": LAYERS, "n_instances": n,
           "bars": {"ratio": BAR_RATIO, "kl_floor": BAR_KLFLOOR, "heads": BAR_HEADS},
           "median_ratio": med_ratio, "median_kl_floor": med_klfloor, "rows": rows, "verdict": verdict}
    out["GateB_asymptotic_floor_supported"] = bool(verdict["read_floor_ok"] and verdict["downstream_floor_ok"])
    print("===GATEBAF-JSON==="); print(json.dumps(out, indent=2)); print("===END===")
    print("\nVERDICT:", "ALL PASS" if out["GateB_asymptotic_floor_supported"] else
          f"NOT SUPPORTED (read {read_ok}/{n}, downstream {heads_pass}/{n}, med_ratio {med_ratio:.0f})")


if __name__ == "__main__":
    main()
