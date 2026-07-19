# GO-P-2026-037 -- moral-reasoning consumer-relative flip (ETHICS commonsense, LaBSE embeddings).
# A JUDGMENT-CLASSIFIER consumer (not a ranker), testing whether the GO-1 blind-probe recipe that
# rehabilitated legal retrieval (GO-P-2026-036) transfers to a moral-judgment read operator.
#
# Consumer : logistic-regression moral classifier (scenario -> wrong/acceptable) trained on calibration.
# Read op  : GO-1 blind margin-sensitivity of the CLASSIFIER -- S = w w^T (w = the recovered judgment
#            direction; the classifier's input-sensitivity), low-rank top-r. This is the direction the
#            consumer reads; the embedding anisotropy is nuisance (read/signal misalignment).
# 3 matched-bit arms on the scenario embeddings (O recon-optimal / R read-preserving / A anti);
# downstream = classification ACCURACY on held-out (same fixed classifier applied to compressed embs).
# Flip: acc(R) >= acc(O)  AND  recon(O) <= recon(R);  anti: acc(A) worst. Config on internal split; seal; confirm.
import sys, os, json, warnings
warnings.filterwarnings("ignore")
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
import numpy as np
from sklearn.linear_model import LogisticRegression
from legal_flip import recon, _norm
from legal_flip_v2 import fit_basis, arms

DATA = "/archive/ethics-corpora/ethics/commonsense.jsonl"
CACHE = "/home/claude/moral_cache"


def load(n):
    T, Y = [], []
    for line in open(DATA, encoding="utf-8"):
        d = json.loads(line)
        if d.get("text"):
            T.append(d["text"][:1000]); Y.append(int(d["label"]))
        if len(T) >= n:
            break
    return T, np.array(Y)


def embed_cache(n):
    f = f"{CACHE}/emb.npz"
    if os.path.exists(f):
        d = np.load(f); return d["E"].astype(np.float64), d["Y"]
    os.makedirs(CACHE, exist_ok=True)
    from sentence_transformers import SentenceTransformer
    T, Y = load(n)
    m = SentenceTransformer("sentence-transformers/LaBSE", device="cuda:0")
    E = m.encode(T, batch_size=64, convert_to_numpy=True, show_progress_bar=False)
    np.savez(f, E=E, Y=Y)
    return E.astype(np.float64), Y


def blind_read_S(clf):
    """GO-1 blind probe of the classifier: its input-sensitivity (margin gradient) is w -> S = w w^T."""
    w = clf.coef_[0]
    return np.outer(w, w)


def evaluate(Efit, Eev, Yev, clf, r, base_bits, boots=200, msub=1500):
    S = blind_read_S(clf)
    mu, V, relr, rawvar = fit_basis(Efit, S, r)
    ar = arms(Eev, V, relr, rawvar, base_bits)
    a0 = float((clf.predict(Eev) == Yev).mean())
    au = {k: float((clf.predict(ar[k]) == Yev).mean()) for k in ar}
    rc = {k: recon(Eev, ar[k]) for k in ar}
    pr = {k: clf.predict(ar[k]) for k in ar}
    n = len(Yev); rng = np.random.default_rng(0); mb = min(msub, n)
    flip = anti = 0
    for _ in range(boots):
        idx = rng.choice(n, mb, replace=False)
        aO = (pr["O"][idx] == Yev[idx]).mean(); aR = (pr["R"][idx] == Yev[idx]).mean()
        aA = (pr["A"][idx] == Yev[idx]).mean()
        flip += (aR >= aO); anti += (aA <= min(aR, aO))
    return dict(acc=au, acc_uncompressed=a0, recon=rc, flip=flip, anti=anti, boots=boots,
                recon_trade=rc["O"] <= rc["R"])


def main():
    E, Y = embed_cache(16000)
    ntr = len(E) // 2
    Etr, Ytr = E[:ntr], Y[:ntr]                                # calibration (train consumer + read op + config)
    Eho, Yho = E[ntr:], Y[ntr:]                                # held-out (disjoint scenarios)
    clf = LogisticRegression(max_iter=2000, C=1.0).fit(Etr, Ytr)
    if "--develop" in sys.argv:
        h = ntr // 2
        EA, YA, EB, YB = Etr[:h], Ytr[:h], Etr[h:], Ytr[h:]    # internal cal-A (fit basis) / cal-B (flip)
        clfA = LogisticRegression(max_iter=2000, C=1.0).fit(EA, YA)
        print(f"DEVELOP: consumer uncompressed acc (cal-B) = {float((clfA.predict(EB)==YB).mean()):.3f}; "
              f"internal split fit=cal-A n={h}, flip=cal-B n={len(EB)}", flush=True)
        for r in (4, 16, 64):
            for bb in (0.25, 0.4, 0.6):
                res = evaluate(EA, EB, YB, clfA, r, bb)
                print(f"  r={r:3d} bits={bb}: acc R={res['acc']['R']:.3f} O={res['acc']['O']:.3f} "
                      f"A={res['acc']['A']:.3f} (unc {res['acc_uncompressed']:.3f}) | recon O={res['recon']['O']:.3f} "
                      f"R={res['recon']['R']:.3f} | flip {res['flip']}/{res['boots']} | anti {res['anti']}/{res['boots']} "
                      f"| recon-trade {res['recon_trade']}", flush=True)
        return
    if "--confirm" in sys.argv:
        i = sys.argv.index("--confirm"); r = int(sys.argv[i + 1]); bb = float(sys.argv[i + 2])
        res = evaluate(Etr, Eho, Yho, clf, r, bb)              # consumer+read op fit on all calibration
        f = lambda a, b: a / b if b else 0
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
