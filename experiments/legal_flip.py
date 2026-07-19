# GO-P-2026-035 -- legal-retrieval consumer-relative flip (CourtListener citations, LaBSE embeddings).
# A REAL non-physical retrieval consumer in a new content domain, extending the confirmed GO-2
# instance-2 (embedding retrieval, GO-P-2026-009) to a large real corpus.
#
# Consumer : citation-pair ranking -- score(a,b)=cos(a,b); metric = AUROC (true (citing,cited) pair
#            ranks above a random cross-pairing). Base LaBSE: raw 0.79, centered 0.84 (anisotropy is
#            nuisance -> the read/signal MISALIGNMENT the flip needs, which D4 lacked).
# Read op  : the CENTERED (semantic) covariance of the document embeddings -- the directions that carry
#            the ranking signal; the raw covariance is dominated by the anisotropy/mean cone (nuisance).
# 3 matched-bit arms compress the DOCUMENT embeddings (queries uncompressed):
#   (O) reconstruction-optimal -- bits by RAW variance (protects the anisotropy/mean cone; min ||b-bhat||^2)
#   (R) read-preserving        -- bits by CENTERED/semantic variance (protects the discriminative dirs)
#   (A) anti                   -- bits by raw/centered ratio (protects ONLY the mean-dominated dirs)
# Flip (bootstrap over query pairs): AUROC(R) >= AUROC(O)  AND  recon(O) <= recon(R);  anti: AUROC(A) worst.
# Read operator FIT on calibration docs (pairs_train), FROZEN, applied to held-out (pairs_eval, disjoint
# opinions id%10==7). Config (rate) selected on calibration, sealed, confirmed on held-out.
import sys, json, warnings, os
warnings.filterwarnings("ignore")
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
import numpy as np

CAL_PAIRS = "/archive/courtlistener/pairs_train.jsonl"
HELD_PAIRS = "/archive/courtlistener/pairs_eval.jsonl"
CACHE = "/home/claude/legal_cache"


def load_pairs(path, n):
    A, B = [], []
    for line in open(path, encoding="utf-8"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("a") and d.get("b"):
            A.append(d["a"][:2000]); B.append(d["b"][:2000])
        if len(A) >= n:
            break
    return A, B


def embed_cache(path, n, tag):
    f = f"{CACHE}/{tag}.npz"
    if os.path.exists(f):
        d = np.load(f); return d["A"].astype(np.float64), d["B"].astype(np.float64)
    os.makedirs(CACHE, exist_ok=True)
    from sentence_transformers import SentenceTransformer
    A, B = load_pairs(path, n)
    m = SentenceTransformer("sentence-transformers/LaBSE", device="cuda:0")
    EA = m.encode(A, batch_size=48, convert_to_numpy=True, show_progress_bar=False)
    EB = m.encode(B, batch_size=48, convert_to_numpy=True, show_progress_bar=False)
    np.savez(f, A=EA, B=EB)
    return EA.astype(np.float64), EB.astype(np.float64)


def fit_basis(EB):
    mu = EB.mean(0)
    C = EB - mu
    w, V = np.linalg.eigh((C.T @ C) / len(C))
    return mu, V[:, ::-1], np.maximum(w[::-1], 1e-12)          # descending eigvals


def arms(EB, mu, V, sig2, base_bits):
    Craw = EB @ V                                             # coeffs in semantic basis (uncentered)
    rawvar = np.maximum((Craw ** 2).mean(0), 1e-12)
    D = len(sig2); total = base_bits * D
    G = 4 * np.sqrt(rawvar)                                   # fixed per-direction range (shared by arms)

    def alloc(weight):
        lw = 0.5 * np.log2(weight); b = np.clip(lw - lw.mean() + base_bits, 0, 14)
        if b.sum() > 0:
            b = np.clip(b * (total / b.sum()), 0, 14)
        return b

    def quant(b):
        Cq = Craw.copy()
        for k in range(D):
            lv = 2 ** b[k]
            if lv <= 1:
                Cq[:, k] = Craw[:, k].mean(); continue        # collapse to constant
            step = G[k] / lv
            Cq[:, k] = np.clip(np.round(Craw[:, k] / step), -lv / 2, lv / 2) * step
        return Cq @ V.T

    return {"O": quant(alloc(rawvar)), "R": quant(alloc(sig2)), "A": quant(alloc(rawvar / sig2))}


def _norm(E):
    return E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-12)


def auroc(EA, EB, idx):
    """Vectorised retrieval AUROC: for query i, true doc i should score above every other doc j.
    S[i,j]=cos(a_i,b_j); AUROC = mean over i,j!=i of [S[i,i] > S[i,j]]."""
    na, nb = _norm(EA[idx]), _norm(EB[idx])
    S = na @ nb.T; pos = np.diag(S); m = len(idx)
    wins = int((pos[:, None] > S).sum())                      # diagonal (pos_i>pos_i) contributes 0
    return wins / max(m * (m - 1), 1)


def recon(EB, Bhat):
    return float((np.linalg.norm(Bhat - EB, axis=1) ** 2).mean() / (np.linalg.norm(EB, axis=1) ** 2).mean())


def evaluate(EA, EB, mu, V, sig2, base_bits, boots=200, msub=800):
    ar = arms(EB, mu, V, sig2, base_bits)
    rc = {k: recon(EB, ar[k]) for k in ar}
    n = len(EA); rng = np.random.default_rng(0)
    full = np.arange(n)
    a0 = auroc(EA, EB, full)
    au = {k: auroc(EA, ar[k], full) for k in ar}
    flip = anti = 0
    mb = min(msub, n)
    for _ in range(boots):
        idx = rng.choice(n, mb, replace=False)                # bootstrap query subset (disjoint negs)
        aO = auroc(EA, ar["O"], idx); aR = auroc(EA, ar["R"], idx); aA = auroc(EA, ar["A"], idx)
        flip += (aR >= aO)
        anti += (aA <= min(aR, aO))
    return dict(auroc_uncompressed=a0, auroc=au, recon=rc, flip_boot=flip, anti_boot=anti, boots=boots,
                recon_trade=rc["O"] <= rc["R"])


def main():
    EAc, EBc = embed_cache(CAL_PAIRS, 4000, "cal")
    mu, V, sig2 = fit_basis(EBc)                              # read operator fit on CALIBRATION docs
    if "--develop" in sys.argv:
        print(f"DEVELOP (calibration, n={len(EAc)}; read operator fit here)")
        for bb in (0.15, 0.25, 0.4, 0.6, 1.0):
            r = evaluate(EAc, EBc, mu, V, sig2, bb)
            print(f"  bits={bb}: AUROC O={r['auroc']['O']:.3f} R={r['auroc']['R']:.3f} A={r['auroc']['A']:.3f} "
                  f"(uncompressed {r['auroc_uncompressed']:.3f}) | recon O={r['recon']['O']:.3f} R={r['recon']['R']:.3f} "
                  f"| flip {r['flip_boot']}/{r['boots']} | anti {r['anti_boot']}/{r['boots']} | recon-trade {r['recon_trade']}")
        return
    if "--confirm" in sys.argv:
        bb = int(sys.argv[sys.argv.index("--confirm") + 1])
        EAh, EBh = embed_cache(HELD_PAIRS, 1300, "held")      # DISJOINT opinions
        r = evaluate(EAh, EBh, mu, V, sig2, bb)
        f = lambda a, b: a / b if b else 0
        print(f"CONFIRM (held-out disjoint pairs, n={len(EAh)}): bits={bb}")
        print(f"  AUROC  read-preserving R={r['auroc']['R']:.3f}  recon-optimal O={r['auroc']['O']:.3f}  "
              f"anti A={r['auroc']['A']:.3f}  (uncompressed {r['auroc_uncompressed']:.3f})")
        print(f"  recon  O={r['recon']['O']:.3f} <= R={r['recon']['R']:.3f} ? {r['recon_trade']}")
        print(f"  flip (AUROC_R>=AUROC_O) {r['flip_boot']}/{r['boots']} | anti worst {r['anti_boot']}/{r['boots']}")
        checks = {"flip >= 60% boots": f(r["flip_boot"], r["boots"]) >= 0.60,
                  "recon-trade (O<=R)": r["recon_trade"],
                  "anti worst >= 70% boots": f(r["anti_boot"], r["boots"]) >= 0.70,
                  "read-preserving beats recon-optimal on AUROC": r["auroc"]["R"] >= r["auroc"]["O"]}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
