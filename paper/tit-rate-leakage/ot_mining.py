"""ot_mining.py: deduction then induction on the 20 measured sources (boundary test + Gaussian-departure registration).

Part 1 (DEDUCTION, formula fixed in DEDUCTION-gaussian-defect-2026-10-02.md, c9fcc18, before this file was written):
  per code  e_hat = d_marg(train) - kappa * dep_c(train);  corrected removal = pred + e_hat_R - e_hat_A.
  Mechanism on the held-out half: measured error e_meas = leak - h_gauss(R2) splits into the exact marginal defect
  d_marg(test) and the remainder d_marg(test) - e_meas (dependence defect minus adversary gap).
  Ablation fixed in advance: marginal only, dependence only, both.
Part 2 (INDUCTION, exploratory): residual of the corrected prediction regressed on training-half characteristics of
  both codes, folds grouped by dataset (a dataset is never in its own training fold). Findings are hypotheses only.
Data already measured; nothing here is a test. The blind test is registration 3 (ot_scope.py).
"""
import math, json
import numpy as np
from scipy.stats import spearmanr, skew, kurtosis
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_predict, GroupKFold
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
import ot_boundary as ob
import ot_gaussianity as og

PG = og.PG; HG = float(-np.sum(PG * np.log2(PG)))
def H(p): p = p[p > 0]; return float(-np.sum(p * np.log2(p)))

_null = {}
def null_dep(n, r):
    key = (n, round(abs(r), 2))
    if key not in _null:
        g = np.random.default_rng(hash(key) % (2 ** 32)); rr = key[1]; v = []
        for _ in range(og.NNULL):
            a = g.normal(size=n); b = rr * a + math.sqrt(max(1 - rr * rr, 0.0)) * g.normal(size=n)
            v.append(og.stats(a, b)[0])
        _null[key] = float(np.mean(v))
    return _null[key]

def kappa(R2):
    R2 = min(max(R2, 1e-6), 1 - 1e-9)
    return (HG - ob.h_gauss(R2)) / (-0.5 * math.log2(1 - R2))

def code_stats(P, S, b, R2, leak):
    tr, te = P["tr"], P["te"]
    p_tr = np.bincount(ob.encode(P, b, tr), minlength=8) / len(tr); p_te = np.bincount(ob.encode(P, b, te), minlength=8) / len(te)
    idx = tr[:og.NCAP]; z = P["Ts"][idx] @ b; z = (z - z.mean()) / z.std(); s = S[idx, 0]
    dep_raw, _, r = og.stats(z, s); dep_c = dep_raw - null_dep(len(idx), r)
    k = kappa(R2); lg = ob.h_gauss(R2)
    lin = r * (s - s.mean()) / s.std()
    knn = cross_val_predict(KNeighborsRegressor(n_neighbors=50), s[:, None], z, cv=5)
    r2knn = 1 - np.mean((z - knn) ** 2) / np.var(z)
    res = z - knn
    het = abs(spearmanr(np.abs(res), np.abs(s - np.median(s))).correlation)
    disc = 1 - len(np.unique(np.round(z, 9))) / len(z)
    return dict(d_marg_tr=H(p_tr) - HG, d_marg_te=H(p_te) - HG, dep_c=dep_c, kappa=k, e_hat=H(p_tr) - HG - k * dep_c,
                e_hat_marg=H(p_tr) - HG, e_hat_dep=-k * dep_c, e_meas=leak - lg, skew=float(skew(z)),
                exkurt=float(kurtosis(z)), disc=disc, nonlin=float(r2knn - r * r), het=float(het), r2lin=r * r)

def run():
    sets = {d["name"]: d for d in ob.DATA + ob.synthetic_sets() + [f() for f in og.FRESH_LOADERS] + [og.warped_gauss8()]}
    rows = [r for f in ("boundary_measured.json", "fresh_measured.json") for r in json.load(open(f)) if r["view"] != "principal-copy"]
    out, cache = [], {}
    for row in rows:
        d = sets[row["dataset"]]; key = (row["dataset"], row["view"])
        if key not in cache:
            P, Sig, m, F, B, b_R, Hm, AS = ob.setup(d, dict(ob.views_for(d))[row["view"]]); S = og.view_S(P, Hm)
            cache[key] = (P, S, code_stats(P, S, b_R, row["R2_principal"], row["leak_principal"]))
        P, S, cR = cache[key]
        cA = code_stats(P, S, np.array(row["b_aware"]), row["R2_aware"], row["leak_aware"])
        o = dict(dataset=row["dataset"], view=row["view"], f=row["f"], pred=row["pred_removed"],
                 meas=row["measured_removed"], se=row["se"], R=cR, A=cA)
        for v in ("e_hat", "e_hat_marg", "e_hat_dep"):
            o["corr_" + v] = o["pred"] + cR[v] - cA[v]
        out.append(o)
    json.dump(out, open("mining_cases.json", "w"), indent=1)
    return out

def report(out):
    SYN = {"Gauss8", "GaussCoupled", "Gauss8-exp"}
    real = [o for o in out if o["dataset"] not in SYN]
    meas = np.array([o["meas"] for o in real])
    print(f"cases {len(out)} (real {len(real)})")
    print("\n== Part 1a: mechanism on the held-out half (mean over both codes) ==")
    print(f"{'dataset':13s} {'e_meas':>8s} {'d_marg':>8s} {'dep-gap':>8s}   (e_meas = d_marg - (dep - gap))")
    for ds in sorted({o["dataset"] for o in out}):
        cs = [c for o in out if o["dataset"] == ds for c in (o["R"], o["A"])]
        em = np.mean([c["e_meas"] for c in cs]); dm = np.mean([c["d_marg_te"] for c in cs])
        print(f"{ds:13s} {em:+8.3f} {dm:+8.3f} {dm - em:+8.3f}")
    print("\n== Part 1b: formula and ablation (real datasets) ==")
    for lab, k in (("Gaussian theory", "pred"), ("marginal only", "corr_e_hat_marg"), ("dependence only", "corr_e_hat_dep"),
                   ("both (formula)", "corr_e_hat")):
        x = np.array([o[k] for o in real])
        print(f"{lab:16s} Spearman {spearmanr(x, meas).correlation:.3f}  mean|miss| {np.mean(np.abs(meas - x)):.3f}")
    miss = np.abs(meas - np.array([o["pred"] for o in real]))
    for lab, k in (("marginal only", "e_hat_marg"), ("dependence only", "e_hat_dep"), ("both", "e_hat")):
        pm = np.array([abs(o["R"][k] - o["A"][k]) for o in real])
        print(f"predicted miss ({lab:15s}) vs actual miss: Spearman {spearmanr(pm, miss).correlation:.3f}")
    print("\nper dataset: Spearman(pred, meas) -> Spearman(formula, meas); mean|miss| -> after")
    for ds in sorted({o["dataset"] for o in out}):
        rs = [o for o in out if o["dataset"] == ds]; m = np.array([o["meas"] for o in rs])
        p = np.array([o["pred"] for o in rs]); c = np.array([o["corr_e_hat"] for o in rs])
        print(f"   {ds:13s} {spearmanr(p, m).correlation:+.3f} -> {spearmanr(c, m).correlation:+.3f}   "
              f"{np.mean(np.abs(m - p)):.3f} -> {np.mean(np.abs(m - c)):.3f}")
    print("\n== Part 2: induction on the residual of the formula (folds grouped by dataset) ==")
    feats = ["skew", "exkurt", "disc", "nonlin", "het", "r2lin", "dep_c", "d_marg_tr", "kappa"]
    X = np.array([[o["R"][f] for f in feats] + [o["A"][f] for f in feats] + [o["f"], o["pred"]] for o in real])
    names = [f + "_R" for f in feats] + [f + "_A" for f in feats] + ["slack", "pred"]
    y = meas - np.array([o["corr_e_hat"] for o in real]); g = np.array([o["dataset"] for o in real])
    gkf = GroupKFold(n_splits=len(set(g)))
    yhat = cross_val_predict(HistGradientBoostingRegressor(max_iter=200, early_stopping=False), X, y, cv=gkf, groups=g)
    print(f"residual of formula: variance {np.var(y):.4f}; leave-one-dataset-out R2 of boosting {1 - np.mean((y - yhat) ** 2) / np.var(y):.3f}")
    model = HistGradientBoostingRegressor(max_iter=200, early_stopping=False).fit(X, y)
    pi = permutation_importance(model, X, y, n_repeats=10, random_state=0)
    for i in np.argsort(-pi.importances_mean)[:8]:
        print(f"   {names[i]:12s} importance {pi.importances_mean[i]:.4f}")
    print("\ndataset characteristics (median over codes):")
    print(f"{'dataset':13s} {'miss':>6s} {'skew':>6s} {'exkurt':>7s} {'disc':>6s} {'nonlin':>7s} {'het':>6s} {'d_marg':>7s} {'dep_c':>7s}")
    for ds in sorted({o["dataset"] for o in out}):
        rs = [o for o in out if o["dataset"] == ds]; cs = [c for o in rs for c in (o["R"], o["A"])]
        med = lambda k: np.median([c[k] for c in cs])
        print(f"{ds:13s} {np.mean([abs(o['meas'] - o['pred']) for o in rs]):6.3f} {med('skew'):+6.2f} {med('exkurt'):+7.2f} "
              f"{med('disc'):6.3f} {med('nonlin'):+7.3f} {med('het'):6.3f} {med('d_marg_tr'):+7.3f} {med('dep_c'):+7.3f}")

if __name__ == "__main__":
    report(run())
