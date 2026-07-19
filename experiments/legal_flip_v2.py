# GO-P-2026-036 -- rehabilitation of the legal-retrieval flip (GO-P-2026-035 honest negative).
# Fix the registered flaw: the ESTIMATED read operator (centered doc covariance) overfit calibration.
# Replace it with the GO-1 BLIND-PROBE read operator (GO-P-2026-011): recover what the ranking CONSUMER
# is actually sensitive to, black-box. For cosine ranking the margin-sensitivity is
#   d cos(a,b)/db  ~  a_hat - cos(a,b)*b_hat   (the query component ORTHOGONAL to the doc)
# which automatically strips the anisotropy (it lives in the subtracted cos*b_hat term) and is tied to
# the ranking TASK rather than the doc-sample variance. Two anti-overfit guards: (1) keep it LOW-RANK
# (top-r sensitivity directions); (2) select r + rate on an INTERNAL calibration split (fit on cal-A,
# test the flip on DISJOINT cal-B) so only a config that already generalises once is sealed.
#
#   --develop            : blind-probe recovery + internal cal-A/cal-B generalisation sweep (r x rate)
#   --confirm R BITS     : frozen config on the true held-out (pairs_eval, disjoint opinions)
import sys, os
import numpy as np
from legal_flip import embed_cache, auroc, recon, _norm, CAL_PAIRS, HELD_PAIRS


def blind_S(EA, EB):
    """GO-1 blind margin-sensitivity operator: S = mean_i g_i g_i^T, g_i = a_hat - cos(a,b) b_hat."""
    na, nb = _norm(EA), _norm(EB)
    cosd = (na * nb).sum(1, keepdims=True)
    G = na - cosd * nb
    return (G.T @ G) / len(G)


def fit_basis(EBfit, S, r):
    """Quantise in the doc semantic-PCA basis; read-importance per direction = its blind sensitivity,
    cut to the top-r directions (low rank for robustness)."""
    mu = EBfit.mean(0); C = EBfit - mu
    w, V = np.linalg.eigh((C.T @ C) / len(C)); V = V[:, ::-1]
    rel = np.einsum("dk,dj,jk->k", V, S, V)                      # diag(V^T S V) >= 0
    rel = np.maximum(rel, 0) + 1e-12
    order = np.argsort(rel)[::-1]
    keep = np.zeros(len(rel), bool); keep[order[:r]] = True
    relr = np.where(keep, rel, rel.max() * 1e-4)                 # top-r protected, rest starved
    Craw = EBfit @ V
    rawvar = np.maximum((Craw ** 2).mean(0), 1e-12)
    return mu, V, relr, rawvar


def arms(EB, V, relr, rawvar, base_bits):
    Craw = EB @ V; D = len(rawvar); total = base_bits * D
    G = 4 * np.sqrt(rawvar)

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
                Cq[:, k] = Craw[:, k].mean(); continue
            step = G[k] / lv
            Cq[:, k] = np.clip(np.round(Craw[:, k] / step), -lv / 2, lv / 2) * step
        return Cq @ V.T

    return {"O": quant(alloc(rawvar)), "R": quant(alloc(relr)), "A": quant(alloc(rawvar / relr))}


def evaluate(EAf, EBf, EAe, EBe, r, base_bits, boots=200, msub=800):
    """Fit read op on (EAf,EBf); score the flip on (EAe,EBe) -- disjoint from the fit."""
    S = blind_S(EAf, EBf)
    mu, V, relr, rawvar = fit_basis(EBf, S, r)
    ar = arms(EBe, V, relr, rawvar, base_bits)
    rc = {k: recon(EBe, ar[k]) for k in ar}
    n = len(EAe); rng = np.random.default_rng(0); full = np.arange(n)
    au = {k: auroc(EAe, ar[k], full) for k in ar}
    a0 = auroc(EAe, EBe, full)
    flip = anti = 0; mb = min(msub, n)
    for _ in range(boots):
        idx = rng.choice(n, mb, replace=False)
        aO = auroc(EAe, ar["O"], idx); aR = auroc(EAe, ar["R"], idx); aA = auroc(EAe, ar["A"], idx)
        flip += (aR >= aO); anti += (aA <= min(aR, aO))
    return dict(auroc=au, auroc_uncompressed=a0, recon=rc, flip=flip, anti=anti, boots=boots,
                recon_trade=rc["O"] <= rc["R"])


def main():
    EAc, EBc = embed_cache(CAL_PAIRS, 4000, "cal")
    h = len(EAc) // 2
    A_A, A_B = (EAc[:h], EBc[:h]), (EAc[h:], EBc[h:])            # cal-A (fit) / cal-B (internal held-out)
    if "--develop" in sys.argv:
        print(f"DEVELOP blind-probe + internal split: fit on cal-A (n={h}), flip scored on DISJOINT cal-B (n={len(EAc)-h})")
        for r in (16, 32, 64, 128):
            for bb in (0.25, 0.4, 0.6):
                res = evaluate(A_A[0], A_A[1], A_B[0], A_B[1], r, bb)
                print(f"  r={r:3d} bits={bb}: AUROC R={res['auroc']['R']:.3f} O={res['auroc']['O']:.3f} "
                      f"A={res['auroc']['A']:.3f} (unc {res['auroc_uncompressed']:.3f}) | recon O={res['recon']['O']:.3f} "
                      f"R={res['recon']['R']:.3f} | flip {res['flip']}/{res['boots']} | anti {res['anti']}/{res['boots']} "
                      f"| recon-trade {res['recon_trade']}", flush=True)
        return
    if "--confirm" in sys.argv:
        i = sys.argv.index("--confirm"); r = int(sys.argv[i + 1]); bb = float(sys.argv[i + 2])
        EAh, EBh = embed_cache(HELD_PAIRS, 1300, "held")
        res = evaluate(EAc, EBc, EAh, EBh, r, bb)               # fit on ALL calibration, score on true held-out
        f = lambda a, b: a / b if b else 0
        print(f"CONFIRM (held-out disjoint pairs, n={len(EAh)}): r={r} bits={bb}")
        print(f"  AUROC read-preserving R={res['auroc']['R']:.3f}  recon-optimal O={res['auroc']['O']:.3f}  "
              f"anti A={res['auroc']['A']:.3f}  (uncompressed {res['auroc_uncompressed']:.3f})")
        print(f"  recon O={res['recon']['O']:.3f} <= R={res['recon']['R']:.3f} ? {res['recon_trade']}")
        print(f"  flip {res['flip']}/{res['boots']} | anti worst {res['anti']}/{res['boots']}")
        checks = {"flip >= 60% boots": f(res["flip"], res["boots"]) >= 0.60,
                  "recon-trade (O<=R)": res["recon_trade"],
                  "anti worst >= 70% boots": f(res["anti"], res["boots"]) >= 0.70,
                  "read-preserving beats recon-optimal on AUROC": res["auroc"]["R"] >= res["auroc"]["O"]}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
