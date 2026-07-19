# GO-P-2026-038 -- sealed consumer-relative flip on sperm-whale coda dialect (DSWP).
import sys, warnings; warnings.filterwarnings("ignore"); sys.path.insert(0, "/home/claude")
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import roc_auc_score
from legal_flip import recon
from legal_flip_v2 import fit_basis, arms

D = pd.read_csv("/home/claude/ketos/DominicaCodas.csv", encoding="utf-8-sig")
FEAT = ["nClicks", "Duration"] + [f"ICI{i}" for i in range(1, 10)]
X = StandardScaler().fit_transform(D[FEAT].values.astype(float))
Y = LabelEncoder().fit_transform(D["Clan"].astype(str).values)
p = np.random.default_rng(0).permutation(len(X)); X, Y = X[p], Y[p]
NTR = len(X) * 2 // 3
Xtr, Ytr, Xho, Yho = X[:NTR], Y[:NTR], X[NTR:], Y[NTR:]

def au(clf, Xa, ya): return roc_auc_score(ya, clf.decision_function(Xa))

def evaluate(Xfit, Xev, yev, clf, r, bb, boots=300, msub=1200):
    S = np.outer(clf.coef_[0], clf.coef_[0])
    mu, V, relr, rawvar = fit_basis(Xfit, S, r)
    ar = arms(Xev, V, relr, rawvar, bb)
    auc = {k: au(clf, ar[k], yev) for k in ar}; rc = {k: recon(Xev, ar[k]) for k in ar}
    sc = {k: clf.decision_function(ar[k]) for k in ar}
    n = len(yev); mb = min(msub, n); rng = np.random.default_rng(0); flip = anti = 0
    for _ in range(boots):
        i = rng.choice(n, mb, replace=False)
        aO = roc_auc_score(yev[i], sc["O"][i]); aR = roc_auc_score(yev[i], sc["R"][i]); aA = roc_auc_score(yev[i], sc["A"][i])
        flip += (aR >= aO); anti += (aA <= min(aR, aO))
    return dict(auc=auc, a0=au(clf, Xev, yev), recon=rc, flip=flip, anti=anti, boots=boots, recon_trade=rc["O"] <= rc["R"])

if "--confirm" in sys.argv:
    i = sys.argv.index("--confirm"); r = int(sys.argv[i + 1]); bb = float(sys.argv[i + 2])
    clf = LogisticRegression(max_iter=4000).fit(Xtr, Ytr)
    res = evaluate(Xtr, Xho, Yho, clf, r, bb)
    f = lambda a, b: a / b if b else 0
    print(f"CONFIRM held-out disjoint codas n={len(Yho)}: r={r} bits={bb}")
    print(f"  AUROC  read-preserving R={res['auc']['R']:.3f}  recon-optimal O={res['auc']['O']:.3f}  anti A={res['auc']['A']:.3f}  (uncompressed {res['a0']:.3f})")
    print(f"  recon  O={res['recon']['O']:.3f} <= R={res['recon']['R']:.3f} ? {res['recon_trade']}")
    print(f"  flip {res['flip']}/{res['boots']} | anti worst {res['anti']}/{res['boots']}")
    ch = {"flip >= 60%": f(res["flip"], res["boots"]) >= .6, "recon-trade (O<=R)": res["recon_trade"], "anti worst >= 70%": f(res["anti"], res["boots"]) >= .7, "R >= O AUROC": res["auc"]["R"] >= res["auc"]["O"]}
    for k, v in ch.items(): print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nVERDICT: {'CONFIRMED' if all(ch.values()) else 'NOT CONFIRMED (honest negative)'}")
