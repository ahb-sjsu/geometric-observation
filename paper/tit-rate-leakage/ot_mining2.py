"""ot_mining2.py: follow-up to ot_mining.py (EXPLORATORY, written after its output was read).
ot_mining.py found that of the three pre-fixed variants the marginal-only correction tracks best. This reports that
variant per dataset, its agreement rate, and redoes the grouped-fold induction on ITS residual (the induction in
ot_mining.py was on the residual of the 'both' variant, whose dependence term was mostly noise)."""
import json
import numpy as np
from scipy.stats import spearmanr
from sklearn.model_selection import cross_val_predict, GroupKFold
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance

SYN = {"Gauss8", "GaussCoupled", "Gauss8-exp"}
out = json.load(open("mining_cases.json"))
real = [o for o in out if o["dataset"] not in SYN]
for lab, k in (("Gaussian theory", "pred"), ("marginal-corrected", "corr_e_hat_marg")):
    agree = np.mean([abs(o["meas"] - o[k]) <= 2 * o["se"] for o in real])
    print(f"{lab:19s} agree (|miss| <= 2 SE) {agree:.1%} of {len(real)} real cases")
print("\nper dataset, marginal-corrected: Spearman(pred, meas) -> Spearman(corr, meas); mean|miss| -> after; agree -> after")
for ds in sorted({o["dataset"] for o in out}):
    rs = [o for o in out if o["dataset"] == ds]; m = np.array([o["meas"] for o in rs]); se = np.array([o["se"] for o in rs])
    p = np.array([o["pred"] for o in rs]); c = np.array([o["corr_e_hat_marg"] for o in rs])
    print(f"   {ds:13s} {spearmanr(p, m).correlation:+.3f} -> {spearmanr(c, m).correlation:+.3f}   "
          f"{np.mean(np.abs(m - p)):.3f} -> {np.mean(np.abs(m - c)):.3f}   "
          f"{np.mean(np.abs(m - p) <= 2 * se):.0%} -> {np.mean(np.abs(m - c) <= 2 * se):.0%}")
feats = ["skew", "exkurt", "disc", "nonlin", "het", "r2lin", "dep_c", "d_marg_tr", "kappa"]
X = np.array([[o["R"][f] for f in feats] + [o["A"][f] for f in feats] + [o["f"], o["pred"]] for o in real])
names = [f + "_R" for f in feats] + [f + "_A" for f in feats] + ["slack", "pred"]
y = np.array([o["meas"] - o["corr_e_hat_marg"] for o in real]); g = np.array([o["dataset"] for o in real])
yhat = cross_val_predict(HistGradientBoostingRegressor(max_iter=200, early_stopping=False), X, y,
                         cv=GroupKFold(n_splits=len(set(g))), groups=g)
print(f"\nresidual of marginal-corrected: variance {np.var(y):.4f}; leave-one-dataset-out R2 of boosting "
      f"{1 - np.mean((y - yhat) ** 2) / np.var(y):.3f}")
pi = permutation_importance(HistGradientBoostingRegressor(max_iter=200, early_stopping=False).fit(X, y), X, y,
                            n_repeats=10, random_state=0)
for i in np.argsort(-pi.importances_mean)[:8]:
    print(f"   {names[i]:12s} importance {pi.importances_mean[i]:.4f}")
print("\nper-code check of the mechanism: Spearman over all codes of e_meas against d_marg (train) and dep_c")
cs = [c for o in out for c in (o["R"], o["A"])]
print(f"   e_meas vs d_marg_tr {spearmanr([c['e_meas'] for c in cs], [c['d_marg_tr'] for c in cs]).correlation:.3f};  "
      f"e_meas - d_marg_te vs dep_c {spearmanr([c['e_meas'] - c['d_marg_te'] for c in cs], [c['dep_c'] for c in cs]).correlation:.3f}")
