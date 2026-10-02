"""ot_gaussianity.py: does a measured departure from Gaussianity predict where the Gaussian boundary theory misses?

Registered 2026-10-02, after the boundary test (boundary_measured.json, scored by boundary_score.py) came in with
C1 and C3 passed and C2 and C5 not met. The leakage predictions of that test use the Gaussian model: the leakage of a
3-bit index of a standardized projection Z depends on the second party's view S only through the linear R2(Z; S).
That is exact when (Z, S) is jointly Gaussian. This registration measures, on TRAINING halves only, how far each code's
(Z, S) pair departs from that model, and predicts that the boundary test's misses fall where the departure is large.

Gaussian departure of one direction b (training half, at most NCAP rows, Z = Ts b standardized, S as in the test):
  dep  = I_np(Z; S) - I_G(Z; S), I_np the mixed k-NN estimator of Gao, Kannan, Oh, Viswanath (NeurIPS 2017, valid with
         ties), I_G = -1/2 log2(1 - r^2) with r the Pearson correlation. The estimator is biased (about -0.06 bit for
         a Gaussian pair at n = 2000, r = 0.6, measured by stage "check"); the null below has the same n and r, so the
         bias cancels in the excess.
  marg = KL(p_hat || p_G) in bits, p_hat the occupancy of the code's 3-bit cells, p_G their Gaussian design probabilities.
  Both are compared with a Gaussian null: NNULL bivariate Gaussian samples with the same n and r. The excess of each over
  the null's 95th percentile, floored at zero, is the departure in bits ("thresholds in noise units").
Case index:  Gamma = sum over the two codes of the case (principal read b_R, aware direction b_aware) of
             excess(dep) + excess(marg).   Gamma = 0 means indistinguishable from Gaussian on both counts.
Outcome:     miss = |measured removal - predicted removal|, agree = miss <= 2 bootstrap SE (the boundary test's rule).

Two parts.
  RETRODICTION on the 13 measured sources (boundary_measured.json). The datasets that missed are already known, so this
  part is not blind at the dataset level. The case-level index has not been computed by anyone before this file is
  committed.
  BLIND on six public datasets never measured in this program, plus a warped Gaussian positive control. Stage "predict"
  freezes the boundary predictions AND Gamma for them and is pushed before stage "measure" runs.

Stages: predict -> gauss_predictions.json (pushed first); measure -> fresh_measured.json; score with gauss_score.py.
Reuses ot_boundary.py verbatim (loaders, splits, codes, adversaries, exact aware direction).
"""
import math, json, argparse, io, zipfile
import numpy as np, pandas as pd
from scipy.special import digamma
from scipy.spatial import cKDTree
from scipy.stats import norm
import ot_boundary as ob

LN2 = math.log(2)
NCAP, NNULL, KNN = 2000, 100, 5
PG = np.diff(norm.cdf(np.r_[-np.inf, ob.BND, np.inf]))      # Gaussian design probabilities of the 8 cells

def mi_mixed(x, y, k=KNN):
    """Gao-Kannan-Oh-Viswanath mixed k-NN mutual information, in bits (raw, not floored)."""
    x = np.asarray(x, float).reshape(-1, 1); y = np.asarray(y, float).reshape(-1, 1); n = len(x)
    xy = np.hstack([x, y]); tj = cKDTree(xy); d, _ = tj.query(xy, k=k + 1, p=np.inf); rho = d[:, -1]
    kt = np.full(n, float(k)); z = rho == 0
    if z.any():
        kt[z] = tj.query_ball_point(xy[z], r=0.0, p=np.inf, return_length=True) - 1
    nx = cKDTree(x).query_ball_point(x, r=rho, p=np.inf, return_length=True) - 1
    ny = cKDTree(y).query_ball_point(y, r=rho, p=np.inf, return_length=True) - 1
    return float(np.mean(digamma(kt) + math.log(n) - np.log(nx + 1) - np.log(ny + 1))) / LN2

def stats(z, s):
    z = (z - z.mean()) / z.std(); r = float(np.corrcoef(z, s)[0, 1])
    dep = mi_mixed(z, s) + 0.5 * math.log2(max(1 - r * r, 1e-12))
    ph = np.bincount(np.searchsorted(ob.BND, z), minlength=len(PG)) / len(z)
    marg = float(np.sum(ph[ph > 0] * np.log2(ph[ph > 0] / PG[ph > 0])))
    return dep, marg, r

_null = {}
def null_q95(n, r):
    key = (n, round(abs(r), 2))
    if key not in _null:
        g = np.random.default_rng(hash(key) % (2 ** 32)); rr = key[1]; out = []
        for _ in range(NNULL):
            a = g.normal(size=n); b = rr * a + math.sqrt(max(1 - rr * rr, 0.0)) * g.normal(size=n)
            out.append(stats(a, b)[:2])
        out = np.array(out); _null[key] = (float(np.quantile(out[:, 0], 0.95)), float(np.quantile(out[:, 1], 0.95)))
    return _null[key]

def departure(P, S, b):
    idx = P["tr"][:NCAP]; z = P["Ts"][idx] @ b; s = S[idx, 0]
    dep, marg, r = stats(z, s); qd, qm = null_q95(len(idx), r)
    return dict(dep=dep, marg=marg, r=r, q95_dep=qd, q95_marg=qm, excess=max(dep - qd, 0.0) + max(marg - qm, 0.0))

def view_S(P, Hm):   # the second party's view exactly as ot_boundary.measure builds it
    return P["Ts"] @ Hm.T + math.sqrt(ob.TAU2) * np.random.default_rng(5).normal(size=(len(P["Ts"]), Hm.shape[0]))

def gamma_rows(rows, sets):
    out, cache = [], {}
    for row in rows:
        d = sets[row["dataset"]]; vrows = dict(ob.views_for(d))[row["view"]]
        key = (row["dataset"], row["view"])
        if key not in cache:
            P, Sig, m, F, B, b_R, Hm, AS = ob.setup(d, vrows); S = view_S(P, Hm)
            cache[key] = (P, S, departure(P, S, b_R))
        P, S, dR = cache[key]; dA = departure(P, S, np.array(row["b_aware"]))
        out.append(dict(dataset=row["dataset"], view=row["view"], f=row["f"], cls=row["cls"],
                        pred_removed=row["pred_removed"], principal=dR, aware=dA, Gamma=dR["excess"] + dA["excess"]))
    return out

# ---------------------------------------------------------------------------------------------------------------
# Fresh datasets, fixed before any of them was loaded for this program. Target and context columns as published.
# ---------------------------------------------------------------------------------------------------------------
UCI = "https://archive.ics.uci.edu/static/public/"
def _member(z, suffix): return z.open([n for n in z.namelist() if n.lower().endswith(suffix)][0])

def load_ccpp():
    df = pd.read_excel(_member(ob._zip(UCI + "294/combined+cycle+power+plant.zip"), ".xlsx")).dropna()
    return ob.pack("PowerPlant", df[["PE"]].to_numpy(float), df[["AT", "V", "AP", "RH"]].to_numpy(float),
                   ["AT"], ["PE"], ["AT", "V", "AP", "RH"])

def load_airfoil():
    df = pd.read_csv(_member(ob._zip(UCI + "291/airfoil+self+noise.zip"), ".dat"), sep=r"\s+", header=None)
    v = ["frequency", "angle", "chord", "velocity", "thickness"]
    return ob.pack("Airfoil", df[[5]].to_numpy(float), df[[0, 1, 2, 3, 4]].to_numpy(float), ["velocity"], ["sound"], v)

def load_yacht():
    df = pd.read_csv(_member(ob._zip(UCI + "243/yacht+hydrodynamics.zip"), ".data"), sep=r"\s+", header=None).dropna()
    v = ["buoyancy", "prismatic", "displacement", "beam-draught", "length-beam", "froude"]
    return ob.pack("Yacht", df[[6]].to_numpy(float), df[[0, 1, 2, 3, 4, 5]].to_numpy(float), ["froude"], ["resistance"], v)

def load_fires():
    df = pd.read_csv(_member(ob._zip(UCI + "162/forest+fires.zip"), "forestfires.csv"))
    v = ["X", "Y", "FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain"]
    return ob.pack("Fires", df[["area"]].to_numpy(float), df[v].to_numpy(float), ["temp"], ["area"], v)

def load_redwine():
    df = pd.read_csv(_member(ob._zip(UCI + "186/wine+quality.zip"), "winequality-red.csv"), sep=";")
    v = [c for c in df.columns if c != "quality"]
    return ob.pack("RedWine", df[["quality"]].to_numpy(float), df[v].to_numpy(float), ["alcohol"], ["quality"], v)

def load_realestate():
    df = pd.read_excel(_member(ob._zip(UCI + "477/real+estate+valuation+data+set.zip"), ".xlsx")).iloc[:, 1:]
    v = ["date", "age", "MRT", "stores", "lat", "lon"]
    return ob.pack("RealEstate", df.iloc[:, 6:7].to_numpy(float), df.iloc[:, :6].to_numpy(float), ["age"], ["price"], v)

def warped_gauss8():   # positive control: Gauss8 with every coordinate passed through exp(0.8 x)
    d = ob.synthetic_sets()[1]; d = dict(d); d["T"] = np.exp(0.8 * d["T"]); d["name"] = "Gauss8-exp"; return d

FRESH_LOADERS = (load_ccpp, load_airfoil, load_yacht, load_fires, load_redwine, load_realestate)

CRITERIA = {
    "R1": "Retrodiction, real datasets of the boundary test (synthetic and principal-copy views excluded): Spearman "
          "correlation of Gamma and miss at least 0.3.",
    "R2": "Retrodiction: agreement rate (miss <= 2 SE) among cases with Gamma = 0 at least 70 percent and at least 20 "
          "points above the rate among cases with Gamma > 0. Vacuous if either group has fewer than 15 cases.",
    "B1": "Blind, fresh datasets (control excluded, principal-copy views excluded): Spearman correlation of Gamma and miss "
          "at least 0.3.",
    "B2": "Blind: as R2 on the fresh cases, same vacuity rule.",
    "B3": "Blind forecast of the theory's own boundary. A dataset tracks when the Spearman correlation of predicted and "
          "measured removal over its cases is at least 0.8. The cut on median Gamma is calibrated on the eleven real "
          "datasets of the boundary test: the midpoint between the largest median Gamma among those that tracked and the "
          "smallest among those that did not, or the median of the eleven medians if the two ranges overlap. Each fresh "
          "dataset is forecast TRACK if its median Gamma is at or below the cut, else MISS (written below). At least five "
          "of six forecasts correct.",
    "K1": "Calibration control: Gamma = 0 in at least 90 percent of the synthetic Gaussian cases of the boundary test.",
    "K2": "Positive control, reported: Gauss8-exp has median Gamma > 0 and a larger mean miss than Gauss8.",
}

def predict(out_path, measured_path):
    old = json.load(open(measured_path))
    sets = {d["name"]: d for d in ob.DATA + ob.synthetic_sets()}
    retro = gamma_rows([r for r in old if r["view"] != "principal-copy"], sets)
    print("retrodiction Gamma computed for", len(retro), "cases", flush=True)
    fresh_sets = [f() for f in FRESH_LOADERS] + [warped_gauss8()]
    for d in fresh_sets:
        print(f"{d['name']:12s} {d['T'].shape}  Y={d['cols'][:d['m']]}", flush=True)
    keep = ob.DATA; ob.DATA = fresh_sets
    ob.predict("fresh_boundary_predictions.json")
    ob.DATA = keep
    fb = json.load(open("fresh_boundary_predictions.json"))
    rows = [r for r in fb["rows"] if r["dataset"] not in ("GaussCoupled", "Gauss8")]
    fsets = {d["name"]: d for d in fresh_sets + ob.synthetic_sets()}
    fresh = gamma_rows([r for r in rows if r["view"] != "principal-copy"], fsets)
    med = {ds: float(np.median([r["Gamma"] for r in fresh if r["dataset"] == ds]))
           for ds in [d["name"] for d in fresh_sets[:-1]]}
    from scipy.stats import spearmanr
    tracked, missed, retro_med = [], [], {}
    for ds in sorted({r["dataset"] for r in old} - {"GaussCoupled", "Gauss8"}):
        rs = [r for r in old if r["dataset"] == ds and r["view"] != "principal-copy"]
        sp = spearmanr([r["pred_removed"] for r in rs], [r["measured_removed"] for r in rs]).correlation
        retro_med[ds] = float(np.median([r["Gamma"] for r in retro if r["dataset"] == ds]))
        (tracked if sp >= 0.8 else missed).append(ds)
    hi_t = max(retro_med[d] for d in tracked); lo_m = min(retro_med[d] for d in missed) if missed else float("inf")
    cut = 0.5 * (hi_t + lo_m) if hi_t < lo_m else float(np.median(list(retro_med.values())))
    forecast = {ds: ("TRACK" if g <= cut else "MISS") for ds, g in med.items()}
    json.dump(dict(criteria=CRITERIA, ncap=NCAP, nnull=NNULL, knn=KNN, retro=retro, fresh=fresh,
                   fresh_boundary_rows=rows, fresh_median_gamma=med, retro_median_gamma=retro_med,
                   retro_tracked=tracked, retro_missed=missed, forecast_cut=cut, forecast=forecast),
              open(out_path, "w"), indent=1)
    print("forecast:", forecast); print("wrote", out_path)

def measure(pred_path, out_path):
    pred = json.load(open(pred_path))
    fresh_sets = [f() for f in FRESH_LOADERS] + [warped_gauss8()]
    ob.DATA = fresh_sets
    tmp = "fresh_boundary_frozen.json"
    json.dump(dict(rows=pred["fresh_boundary_rows"]), open(tmp, "w"))
    ob.measure(tmp, out_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["check", "predict", "measure"])
    ap.add_argument("--measured", default="boundary_measured.json")
    ap.add_argument("--pred", default="gauss_predictions.json"); ap.add_argument("--out", default="fresh_measured.json")
    a = ap.parse_args()
    if a.stage == "check":
        for f in FRESH_LOADERS:
            d = f(); print(f"{d['name']:12s} {d['T'].shape}  Y={d['cols'][:d['m']]}  ctx={d['cols'][d['m']:]}")
        g = np.random.default_rng(0); x = g.normal(size=2000); y = 0.6 * x + 0.8 * g.normal(size=2000)
        print("estimator on a Gaussian pair r=0.6: I_np", round(mi_mixed(x, y), 4), "I_G", round(-0.5 * math.log2(1 - 0.36), 4))
    elif a.stage == "predict":
        predict(a.pred, a.measured)
    else:
        measure(a.pred, a.out)
