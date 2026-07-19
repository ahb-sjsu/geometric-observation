# GO-P-2026-037 -- moral-reasoning flip on a FINE-TUNED consumer (ETHICS commonsense).
# Uses the fine-tuned LaBSE representation + classifier head (moral_finetune.py -> moral_ft.npz).
# Consumer = the fine-tuned classifier head; read operator = its margin direction W[1]-W[0] (the moral
# judgment direction, recovered blind), low-rank, exactly the GO-P-2026-036 recipe. Downstream =
# classification ACCURACY on held-out; 3 matched-bit arms on the representation.
import sys
import numpy as np
from legal_flip import recon
from legal_flip_v2 import fit_basis, arms

NPZ = "/home/claude/moral_cache/moral_ft.npz"


def predict(R, W, b):
    return np.argmax(R @ W.T + b, 1)


def evaluate(Rfit, Rev, Yev, W, b, r, base_bits, boots=200, msub=1500):
    wdir = W[1] - W[0]                       # binary margin (logit-difference) direction = blind read op
    S = np.outer(wdir, wdir)
    mu, V, relr, rawvar = fit_basis(Rfit, S, r)
    ar = arms(Rev, V, relr, rawvar, base_bits)
    a0 = float((predict(Rev, W, b) == Yev).mean())
    au = {k: float((predict(ar[k], W, b) == Yev).mean()) for k in ar}
    rc = {k: recon(Rev, ar[k]) for k in ar}
    pr = {k: predict(ar[k], W, b) for k in ar}
    n = len(Yev); rng = np.random.default_rng(0); mb = min(msub, n); flip = anti = 0
    for _ in range(boots):
        idx = rng.choice(n, mb, replace=False)
        aO = (pr["O"][idx] == Yev[idx]).mean(); aR = (pr["R"][idx] == Yev[idx]).mean()
        aA = (pr["A"][idx] == Yev[idx]).mean()
        flip += (aR >= aO); anti += (aA <= min(aR, aO))
    return dict(acc=au, acc_uncompressed=a0, recon=rc, flip=flip, anti=anti, boots=boots,
                recon_trade=rc["O"] <= rc["R"])


def main():
    d = np.load(NPZ); Rtr, Ytr, Rho, Yho, W, b = d["Rtr"], d["Ytr"], d["Rho"], d["Yho"], d["W"], d["b"]
    if "--develop" in sys.argv:
        h = len(Rtr) // 2
        print(f"DEVELOP (fine-tuned consumer): internal fit=Rtr[:{h}], flip on DISJOINT Rtr[{h}:]", flush=True)
        for r in (4, 16, 64):
            for bb in (0.25, 0.4, 0.6):
                res = evaluate(Rtr[:h], Rtr[h:], Ytr[h:], W, b, r, bb)
                print(f"  r={r:3d} bits={bb}: acc R={res['acc']['R']:.3f} O={res['acc']['O']:.3f} "
                      f"A={res['acc']['A']:.3f} (unc {res['acc_uncompressed']:.3f}) | recon O={res['recon']['O']:.3f} "
                      f"R={res['recon']['R']:.3f} | flip {res['flip']}/{res['boots']} | anti {res['anti']}/{res['boots']} "
                      f"| recon-trade {res['recon_trade']}", flush=True)
        return
    if "--confirm" in sys.argv:
        i = sys.argv.index("--confirm"); r = int(sys.argv[i + 1]); bb = float(sys.argv[i + 2])
        res = evaluate(Rtr, Rho, Yho, W, b, r, bb)
        f = lambda a, c: a / c if c else 0
        print(f"CONFIRM (held-out disjoint scenarios, n={len(Yho)}): r={r} bits={bb}")
        print(f"  ACC read-preserving R={res['acc']['R']:.3f}  recon-optimal O={res['acc']['O']:.3f}  "
              f"anti A={res['acc']['A']:.3f}  (uncompressed {res['acc_uncompressed']:.3f})")
        print(f"  recon O={res['recon']['O']:.3f} <= R={res['recon']['R']:.3f} ? {res['recon_trade']}")
        print(f"  flip {res['flip']}/{res['boots']} | anti worst {res['anti']}/{res['boots']}")
        checks = {"flip >= 60% boots": f(res["flip"], res["boots"]) >= 0.60,
                  "recon-trade (O<=R)": res["recon_trade"],
                  "anti worst >= 70% boots": f(res["anti"], res["boots"]) >= 0.70,
                  "read-preserving beats recon-optimal on accuracy": res["acc"]["R"] >= res["acc"]["O"]}
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"\nVERDICT: {'CONFIRMED' if all(checks.values()) else 'NOT CONFIRMED (honest negative)'}")


if __name__ == "__main__":
    main()
