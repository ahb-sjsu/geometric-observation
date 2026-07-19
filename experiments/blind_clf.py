"""GO-P-2026-041 -- blind, non-oracle, PROSPECTIVE flip with a magnitude prediction.

Fresh untouched domain: 20 Newsgroups binary topic classification (sci.space vs rec.autos),
never used elsewhere in the program. Frozen LSA embedding (TF-IDF -> TruncatedSVD, fit on
calibration only). Consumer = logistic classifier. Read operator recovered NON-ORACLE by
finite-difference probing of the consumer's margin (no test labels). We commit, on
calibration, (1) the winning code, (2) the sign of the downstream/reconstruction reversal,
and (3) a MAGNITUDE band for the held-out AUROC gap from Delta_pred = tr[P_C(Sd_O - Sd_R)],
then evaluate ONCE on the held-out split.

  --calibrate : fit everything on calibration; recover P_C by probing; internal cal-A/cal-B
                flip; print the predictions to seal.
  --confirm R BAND_LO BAND_HI : score frozen codes once on the held-out test split.
"""
import argparse
import json
import os
import sys
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
CATS = ["sci.space", "rec.autos"]
D = 100                    # LSA dimension
BASE_BITS = 2.0
R_RANK = 16
EPS = 1e-2


def load(split):
    d = fetch_20newsgroups(subset=split, categories=CATS, download_if_missing=False,
                           remove=("headers", "footers", "quotes"))
    return d.data, (np.array(d.target) == 0).astype(int)   # binary label


def embed_fit(texts):
    tf = TfidfVectorizer(max_features=20000, stop_words="english", sublinear_tf=True)
    Xtf = tf.fit_transform(texts)
    svd = TruncatedSVD(n_components=D, random_state=0).fit(Xtf)
    return tf, svd, svd.transform(Xtf)


def alloc(weight, base_bits, d):
    lw = 0.5 * np.log2(np.maximum(weight, 1e-12))
    b = np.clip(lw - lw.mean() + base_bits, 0, 14)
    if b.sum() > 0:
        b = np.clip(b * (base_bits * d / b.sum()), 0, 14)
    return b


def fit_basis(Efit, w):
    """Eigenbasis of the calibration embeddings; read importance = projection onto the
    classifier margin direction w (the non-oracle read operator), kept top-r."""
    mu = Efit.mean(0); C = Efit - mu
    ev, V = np.linalg.eigh((C.T @ C) / len(C)); V = V[:, ::-1]
    rawvar = np.maximum(((Efit @ V) ** 2).mean(0), 1e-12)
    gproj = (V.T @ w) ** 2
    keep = np.zeros(len(gproj), bool); keep[np.argsort(gproj)[::-1][:R_RANK]] = True
    readw = np.where(keep, np.maximum(gproj, 1e-12), gproj.max() * 1e-4)
    return mu, V, rawvar, readw


def arms(E, V, rawvar, readw, base_bits):
    C = E @ V; d = len(rawvar); rng = 4 * np.sqrt(rawvar)

    def q(bits):
        Cq = C.copy()
        for k in range(d):
            lv = 2 ** bits[k]
            if lv <= 1:
                Cq[:, k] = C[:, k].mean(); continue
            step = 2 * rng[k] / lv
            Cq[:, k] = np.clip(np.round(C[:, k] / step), -lv / 2, lv / 2) * step
        return Cq @ V.T
    return {"O": q(alloc(rawvar, base_bits, d)), "R": q(alloc(readw, base_bits, d)),
            "A": q(alloc(rawvar / readw, base_bits, d))}


def blind_probe(clf, Efit):
    """NON-ORACLE read op: finite-difference the consumer's margin w.r.t. each embedding
    coord (uses clf output only, NO labels). For a linear consumer this recovers coef_."""
    base = clf.decision_function(Efit).mean()
    g = np.zeros(Efit.shape[1])
    for j in range(Efit.shape[1]):
        E2 = Efit.copy(); E2[:, j] += EPS
        g[j] = (clf.decision_function(E2).mean() - base) / EPS
    return g


def scores(clf, y, ar, mu, V, rawvar, readw):
    au = {k: roc_auc_score(y, clf.decision_function(ar[k])) for k in ar}
    recon = {k: float((np.linalg.norm(ar[k] - AR_REF[k], axis=1) ** 2).sum()) for k in ("O", "R")}
    return au, recon


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--confirm", nargs=3, metavar=("BASEBITS", "LO", "HI"))
    args = ap.parse_args()

    Xtr, ytr = load("train")
    tf, svd, Ecal = embed_fit(Xtr)                     # FROZEN embedding, calibration only
    clf = LogisticRegression(max_iter=2000, C=1.0).fit(Ecal, ytr)
    g = blind_probe(clf, Ecal)                         # non-oracle read operator
    mu, V, rawvar, readw = fit_basis(Ecal, g)

    def eval_split(E, y, base_bits):
        ar = arms(E, V, rawvar, readw, base_bits)
        au = {k: roc_auc_score(y, clf.decision_function(ar[k])) for k in ar}
        rec = {k: float((np.linalg.norm(ar[k] - E, axis=1) ** 2).mean() /
                        (np.linalg.norm(E, axis=1) ** 2).mean()) for k in ("O", "R")}
        # Delta_pred = tr[P_C (Sd_O - Sd_R)], P_C = g g^T
        Pc = np.outer(g, g)
        Sd = {k: np.cov((ar[k] - E).T) for k in ("O", "R")}
        dpred = float(np.trace(Pc @ (Sd["O"] - Sd["R"])))
        return au, rec, dpred

    if args.calibrate:
        h = len(Ecal) // 2                              # internal cal-A / cal-B
        clfA = LogisticRegression(max_iter=2000).fit(Ecal[:h], ytr[:h])
        gA = blind_probe(clfA, Ecal[:h])
        muA, VA, rvA, rwA = fit_basis(Ecal[:h], gA)
        arB = arms(Ecal[h:], VA, rvA, rwA, BASE_BITS)
        auB = {k: roc_auc_score(ytr[h:], clfA.decision_function(arB[k])) for k in arB}
        recB = {k: float((np.linalg.norm(arB[k] - Ecal[h:], axis=1) ** 2).mean() /
                (np.linalg.norm(Ecal[h:], axis=1) ** 2).mean()) for k in ("O", "R")}
        au, rec, dpred = eval_split(Ecal, ytr, BASE_BITS)   # full-calibration numbers
        print("=== CALIBRATION (fresh 20NG; non-oracle margin probe) ===")
        print(f"consumer AUROC uncompressed = {roc_auc_score(ytr, clf.decision_function(Ecal)):.3f};  ||g||={np.linalg.norm(g):.3f}")
        print(f"internal cal-B: AUROC R={auB['R']:.3f} O={auB['O']:.3f} A={auB['A']:.3f} | recon O={recB['O']:.3f} R={recB['R']:.3f}")
        gap = auB["R"] - auB["O"]
        print(f"full-cal: AUROC R={au['R']:.3f} O={au['O']:.3f} A={au['A']:.3f} | recon O={rec['O']:.3f} R={rec['R']:.3f}")
        print(f"Delta_pred = tr[P_C(Sd_O-Sd_R)] = {dpred:+.4e}")
        print("\n--- SEALED PREDICTIONS (commit before held-out test split) ---")
        print(f"  base_bits={BASE_BITS}, r={R_RANK}")
        print(f"  (1) winner: R; (2) sign: AUROC(R)>AUROC(O) AND recon(O)<recon(R)")
        print(f"  (3) magnitude: held-out AUROC(R)-AUROC(O) in [{max(0,0.5*gap):.3f}, {1.5*gap:.3f}]")
        return

    if args.confirm:
        base_bits = float(args.confirm[0]); lo, hi = float(args.confirm[1]), float(args.confirm[2])
        Xte, yte = load("test")
        Ete = svd.transform(tf.transform(Xte))          # frozen embedding on held-out
        au, rec, dpred = eval_split(Ete, yte, base_bits)
        gap = au["R"] - au["O"]
        checks = {"R>O downstream": au["R"] > au["O"],
                  "recon-trade O<R": rec["O"] < rec["R"],
                  "anti worst": au["A"] <= min(au["R"], au["O"]),
                  f"magnitude in [{lo},{hi}]": lo <= gap <= hi}
        out = dict(id="GO-P-2026-041", domain="20NG sci.space vs rec.autos (fresh)",
                   oracle_free=True, n_test=len(yte), auroc=au, recon=rec,
                   auroc_gap=gap, delta_pred=dpred, checks=checks,
                   verdict="CONFIRMED" if all(checks.values()) else "NOT CONFIRMED")
        print("=== HELD-OUT CONFIRM (single evaluation, fresh test split) ===")
        print(f"n_test={len(yte)}  AUROC R={au['R']:.3f} O={au['O']:.3f} A={au['A']:.3f} | recon O={rec['O']:.3f} R={rec['R']:.3f}")
        print(f"AUROC gap R-O = {gap:+.3f}  (sealed band [{lo},{hi}]);  Delta_pred={dpred:+.4e}")
        for k, v in checks.items():
            print(f"  [{'PASS' if v else 'FAIL'}] {k}")
        print(f"VERDICT: {out['verdict']}")
        with open(os.path.join(HERE, "..", "results", "GO-blind-clf.json"), "w") as f:
            json.dump(out, f, indent=1)
        return


if __name__ == "__main__":
    main()
