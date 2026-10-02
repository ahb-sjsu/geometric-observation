"""ot_radar_induction.py: INDUCTION with Theory Radar (symbolic formula search) on mining_cases.json.

Question: is there a short formula in training-half characteristics of a case's two codes that separates the cases
where the Gaussian theory misses (|measured - predicted| > 2 SE) from those where it holds?
Honesty rules: leave-one-dataset-out. For each held-out dataset the search sees only the other datasets' cases, the
threshold and its direction are tuned on those cases, and the formula is replayed on the held-out dataset. The final
formula (all datasets) is a HYPOTHESIS for registration 3, not a result. Exploratory; data already measured.
Uses theory-radar (github.com/ahb-sjsu/theory-radar, master with the Youden-ceiling correction of 2026-09-03).
"""
import json, sys, time
from collections import Counter
import numpy as np
from symbolic_search import TheoryRadar
from symbolic_search._ops import BINARY_OPS, UNARY_OPS

FEATS = ["d_marg_tr", "dep_c", "kappa", "skew", "exkurt", "disc", "nonlin", "het", "r2lin"]
SYN = {"Gauss8", "GaussCoupled", "Gauss8-exp"}

def table(cases):
    X, y, g, names = [], [], [], [f + "_R" for f in FEATS] + [f + "_A" for f in FEATS] + ["slack", "pred"]
    for o in cases:
        X.append([o["R"][f] for f in FEATS] + [o["A"][f] for f in FEATS] + [o["f"], o["pred"]])
        y.append(abs(o["meas"] - o["pred"]) > 2 * o["se"]); g.append(o["dataset"])
    return np.array(X, float), np.array(y, bool), np.array(g), names

def evaluate(formula, X, names):
    col = {n: X[:, i] for i, n in enumerate(names)}
    def ev(s):
        s = s.strip()
        if s in col: return col[s]
        if s.startswith("(") and s.endswith(")"):
            left, op, right = s[1:-1].rsplit(" ", 2)
            return np.nan_to_num(BINARY_OPS[op](ev(left), col[right]), nan=0.0, posinf=1e10, neginf=-1e10)
        k = s.index("(")
        return np.nan_to_num(UNARY_OPS[s[:k]](ev(s[k + 1:-1])), nan=0.0, posinf=1e10, neginf=-1e10)
    return ev(formula)

def f1(pred, y):
    tp = np.sum(pred & y); fp = np.sum(pred & ~y); fn = np.sum(~pred & y)
    return 2 * tp / max(2 * tp + fp + fn, 1)

def best_threshold(v, y):
    best = (-1, 0.0, 1)
    for t in np.unique(v):
        for d in (1, -1):
            s = f1(d * v >= d * t, y)
            if s > best[0]: best = (s, t, d)
    return best

def radar(X, y, names, depth):
    r = TheoryRadar(X, y, feature_names=names)
    return r.search(mode="youden", max_depth=depth, max_expansions=20000, timeout=120, verbose=False).formula

if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    cases = [o for o in json.load(open("mining_cases.json")) if o["dataset"] not in SYN]
    X, y, g, names = table(cases)
    print(f"{len(y)} real cases, {y.mean():.1%} misses, {len(set(g))} datasets, depth {depth}")
    held, forms = [], Counter()
    for ds in sorted(set(g)):
        tr, te = g != ds, g == ds; t0 = time.time()
        form = radar(X[tr], y[tr], names, depth); forms[form] += 1
        _, t, d = best_threshold(evaluate(form, X[tr], names), y[tr])
        p = d * evaluate(form, X[te], names) >= d * t
        held.append((ds, form, float(np.mean(p == y[te])), float(y[te].mean()), p, y[te]))
        print(f"  held out {ds:13s} acc {np.mean(p == y[te]):.3f} (miss rate {y[te].mean():.2f})  {form}  [{time.time() - t0:.0f}s]", flush=True)
    P = np.concatenate([h[4] for h in held]); Y = np.concatenate([h[5] for h in held])
    print(f"leave-one-dataset-out: accuracy {np.mean(P == Y):.3f}, F1 {f1(P, Y):.3f}, base rate {Y.mean():.3f}")
    print("formula stability across folds:", forms.most_common(5))
    form = radar(X, y, names, depth); _, t, d = best_threshold(evaluate(form, X, names), y)
    print(f"FINAL (hypothesis for registration 3): miss if {'+' if d > 0 else '-'}[{form}] >= {d * t:.4g}")
    json.dump(dict(depth=depth, final=form, threshold=float(t), direction=int(d), folds=[h[:4] for h in held]),
              open(f"radar_induction_d{depth}.json", "w"), indent=1)
