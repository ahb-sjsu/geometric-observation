"""ot_scope.py: the boundary theory inside its Gaussian scope, and the onset order by pencil class. Third registration.

Drafted 2026-10-02 after the Gaussian-departure registration (gauss_predictions.json, ec3300d; scored 9f2a61b: blind
forecast 6 of 6) and a POST HOC split (posthoc_gamma.py) suggesting that the boundary test's unmet criteria C5 (and
perhaps C2) hold where the departure index Gamma is at most the frozen cut 0.835 bit. Post hoc readings are not results.
This registration tests them on six public datasets never loaded by this program, with the cut frozen in advance.

Scope. A case is IN SCOPE when its Gamma (ot_gaussianity.py, training halves only) is at most CUT = 0.835 bit, the B3
cut frozen in gauss_predictions.json. Nothing about the scope is refit here.

Onset order. With slack f, the aware code's removal grows to first order in f when the decoder's principal read b_R is
not an eigenvector of the view's pencil (Theorem misalign), and only to second order when it is a non-top eigenvector.
Two view families probe this on every dataset, both built from the context column least correlated with b_R:
  mix15  S = cos(15 deg) Z_R + sin(15 deg) X_j      (not an eigenvector: first-order onset)
  orth   S = X_j made Sigma-orthogonal to Z_R        (b_R is a non-top eigenvector, eigenvalue 0: second-order onset)
Both are evaluated at ONSET_FRACS = 0.02, 0.05, 0.10, 0.20 (mix15 also at the main fractions 0.15 and 0.4). The squared correlation of orth with Z_R is zero, which is
the "uncorrelated view" of the refuted onset test, now with the pencil class that predicts its behaviour.

Stages: check (loaders only) -> predict -> scope_predictions.json (pushed first) -> measure -> scope_measured.json;
score with scope_score.py. Reuses ot_boundary.py and ot_gaussianity.py verbatim.
"""
import math, json, argparse
import numpy as np, pandas as pd
from scipy.linalg import eigh
import ot_boundary as ob
import ot_gaussianity as og

CUT = 0.8347225398139835           # forecast_cut in gauss_predictions.json (sha256 c66ddf4a...)
ONSET_FRACS = (0.02, 0.05, 0.10, 0.20)
UCI = og.UCI

# ---------------------------------------------------------------------------------------------------------------
# Six datasets, none loaded by this program before this file. Targets and context columns as documented by UCI.
# ---------------------------------------------------------------------------------------------------------------
def load_gasturbine():
    df = pd.read_csv(og._member(ob._zip(UCI + "551/gas+turbine+co+and+nox+emission+data+set.zip"), "gt_2015.csv"))
    v = ["AT", "AP", "AH", "AFDP", "GTEP", "TIT", "TAT", "TEY", "CDP"]
    return ob.pack("GasTurbine", df[["CO", "NOX"]].to_numpy(float), df[v].to_numpy(float), ["AT"], ["CO", "NOX"], v)

def load_grid():
    df = pd.read_csv(og._member(ob._zip(UCI + "471/electrical+grid+stability+simulated+data.zip"), ".csv"))
    v = ["tau1", "tau2", "tau3", "tau4", "p1", "p2", "p3", "p4", "g1", "g2", "g3", "g4"]
    return ob.pack("Grid", df[["stab"]].to_numpy(float), df[v].to_numpy(float), ["tau1"], ["stab"], v)

def load_qsar_fish():
    df = pd.read_csv(og._member(ob._zip(UCI + "504/qsar+fish+toxicity.zip"), ".csv"), sep=";", header=None)
    v = ["CIC0", "SM1_Dz", "GATS1i", "NdsCH", "NdssC", "MLOGP"]
    return ob.pack("QSARFish", df[[6]].to_numpy(float), df[[0, 1, 2, 3, 4, 5]].to_numpy(float), ["MLOGP"], ["LC50"], v)

def load_qsar_aquatic():
    df = pd.read_csv(og._member(ob._zip(UCI + "505/qsar+aquatic+toxicity.zip"), ".csv"), sep=";", header=None)
    v = ["TPSA", "SAacc", "H050", "MLOGP", "RDCHI", "GATS1p", "nN", "C040"]
    return ob.pack("QSARAquatic", df[[8]].to_numpy(float), df[list(range(8))].to_numpy(float), ["MLOGP"], ["LC50"], v)

def load_tempforecast():
    z = ob._zip(UCI + "514/bias+correction+of+numerical+prediction+model+temperature+forecast.zip")
    df = pd.read_csv(og._member(z, ".csv")).drop(columns=["station", "Date"]).dropna()
    v = [c for c in df.columns if c not in ("Next_Tmax", "Next_Tmin")]
    return ob.pack("TempForecast", df[["Next_Tmax", "Next_Tmin"]].to_numpy(float), df[v].to_numpy(float),
                   ["Present_Tmax"], ["Next_Tmax", "Next_Tmin"], v)

def load_appliances():
    df = pd.read_csv(og._member(ob._zip(UCI + "374/appliances+energy+prediction.zip"), ".csv"))
    v = [c for c in df.columns if c not in ("date", "Appliances", "rv1", "rv2")]
    return ob.pack("Appliances", df[["Appliances"]].to_numpy(float), df[v].to_numpy(float), ["T_out"], ["Appliances"], v)

LOADERS = (load_gasturbine, load_grid, load_qsar_fish, load_qsar_aquatic, load_tempforecast, load_appliances)

def controls():   # Gaussian calibration sources with seeds not used before (the earlier ones used seeds 1 and 2)
    g = ob.synthetic_sets()
    return [ob.synth("GaussCoupled-s11", g[0]["T"].T @ g[0]["T"] / len(g[0]["T"]), 2, 20000, 11),
            ob.synth("Gauss8-s12", g[1]["T"].T @ g[1]["T"] / len(g[1]["T"]), 2, 20000, 12)]

# ---------------------------------------------------------------------------------------------------------------
def views(d):
    out = [(n, n) for n, _ in ob.views_for(d) if n != "principal-copy"]
    return out + [("orth", "orth")]

def setup_view(d, vname):
    if vname != "orth":
        return ob.setup(d, dict(ob.views_for(d))[vname])
    P, Sig, m, F, B, b_R, _, _ = ob.setup(d, dict(ob.views_for(d))["mix15"])
    zR = b_R / math.sqrt(b_R @ Sig @ b_R); p = Sig.shape[0]; ctx = list(range(m, p))
    corr = [abs(float(zR @ Sig[:, j]) / math.sqrt(Sig[j, j])) for j in ctx]; j = ctx[int(np.argmin(corr))]
    e = np.zeros(p); e[j] = 1.0 / math.sqrt(Sig[j, j]); e = e - float(zR @ Sig @ e) * zR; e = e / math.sqrt(e @ Sig @ e)
    Hm = e[None, :]
    SS = Hm @ Sig @ Hm.T + ob.TAU2 * np.eye(1); AS = Sig @ Hm.T @ np.linalg.inv(SS) @ Hm @ Sig
    return P, Sig, m, F, B, b_R, Hm, AS

def fracs_for(vname):
    if vname == "orth": return ONSET_FRACS
    if vname == "mix15": return tuple(sorted(set(ONSET_FRACS) | set(ob.FRACS)))
    return ob.FRACS

def predict_rows(d):
    rows = []
    for vname, _ in views(d):
        P, Sig, m, F, B, b_R, Hm, AS = setup_view(d, vname)
        w, V = eigh(AS, Sig); R2max = float(w[-1]); R2R = ob.rayleigh(AS, Sig, b_R)
        resid = AS @ b_R - R2R * (Sig @ b_R); mis = float(np.linalg.norm(resid) / max(np.linalg.norm(AS @ b_R), 1e-15))
        cls = "top" if (R2max - R2R) < 1e-9 else ("eigenvector" if mis < 1e-6 or np.linalg.norm(AS @ b_R) < 1e-12
                                                     else "not-eigenvector")
        trY = float(np.trace(F @ Sig @ F.T)); DR = trY - ob.GAIN * ob.rayleigh(B, Sig, b_R)
        S = og.view_S(P, Hm); dR = og.departure(P, S, b_R)
        for f in fracs_for(vname):
            D0 = DR + f * (trY - DR); need = (trY - D0) / ob.GAIN
            b_aw = ob.exact_aware(AS, B, Sig, need); R2aw = ob.rayleigh(AS, Sig, b_aw)
            dA = og.departure(P, S, b_aw)
            rows.append(dict(dataset=d["name"], view=vname, f=f, cls=cls, R2_principal=R2R, R2_max=R2max,
                             misalignment=mis, R2_aware=R2aw, pred_removed=ob.h_gauss(R2R) - ob.h_gauss(R2aw),
                             b_aware=[float(x) for x in b_aw], Gamma=dR["excess"] + dA["excess"],
                             in_scope=bool(dR["excess"] + dA["excess"] <= CUT)))
    print(d["name"], "predicted", len(rows), "cases", flush=True)
    return rows

CRITERIA = {
    "S0": "Replication of B3. Each fresh dataset is forecast TRACK if its median Gamma (all its cases) is at most CUT, "
          "else MISS. It tracks when the Spearman correlation of predicted and measured removal over its main-view "
          "cases (context columns and mix families at 0.05, 0.15, 0.4) is at least 0.8. At least five of six correct.",
    "S1": "In scope, main-view cases: measured removal > 0 in at least 80 percent of those predicted >= 0.10 bit, and "
          "Spearman of predicted and measured removal at least 0.6.",
    "S2": "In scope, main-view cases predicted < 0.05 bit: |measured| <= 2 SE in at least 80 percent. Vacuous below 15 cases.",
    "S3": "In scope, mix families (5, 15, 30, 60 degrees) at 0.05, 0.15, 0.4: Spearman of predicted and measured at "
          "least 0.6. Vacuous below 15 cases.",
    "S4a": "In scope, onset families (mix15, orth) at 0.02 to 0.20: measured within 2 SE of predicted in at least 80 "
           "percent. Vacuous below 15 cases.",
    "S4b": "Onset order at the smallest slack (f = 0.02), in scope: among orth cases predicted < 0.02 bit, |measured| "
           "<= 2 SE in at least 80 percent, and among mix15 cases predicted >= 0.05 bit, measured > 2 SE in at least "
           "80 percent. Vacuous if either group has fewer than 3 cases.",
    "K1": "Calibration on the new Gaussian controls: Gamma = 0 in at least 70 percent of their cases (four tests at the "
          "95th percentile give about 81 percent when every null holds).",
    "K2": "Reported: out-of-scope cases under S1-S3, side by side with in-scope.",
}

def predict(out_path):
    sets = [f() for f in LOADERS] + controls(); rows = []
    for d in sets: rows += predict_rows(d)
    med = {d["name"]: float(np.median([r["Gamma"] for r in rows if r["dataset"] == d["name"]])) for d in sets[:6]}
    forecast = {k: ("TRACK" if g <= CUT else "MISS") for k, g in med.items()}
    theory = {}
    for ds in med:
        for fam in ("mix15", "orth"):
            pr = {r["f"]: r["pred_removed"] for r in rows if r["dataset"] == ds and r["view"] == fam}
            if pr.get(0.02, 0) > 0 and pr.get(0.10, 0) > 0:
                theory[f"{ds}/{fam}"] = math.log(pr[0.10] / pr[0.02]) / math.log(5)
    json.dump(dict(criteria=CRITERIA, cut=CUT, onset_fracs=ONSET_FRACS, rows=rows, median_gamma=med,
                   forecast=forecast, predicted_onset_slope=theory), open(out_path, "w"), indent=1)
    print("forecast:", forecast); print("predicted onset slopes (log-log, 0.02 to 0.10):",
                                      {k: round(v, 2) for k, v in theory.items()}); print("wrote", out_path)

def measure(pred_path, out_path):
    pred = json.load(open(pred_path)); sets = {d["name"]: d for d in [f() for f in LOADERS] + controls()}
    cache, out = {}, []
    for row in pred["rows"]:
        d = sets[row["dataset"]]; key = (row["dataset"], row["view"])
        P, Sig, m, F, B, b_R, Hm, AS = setup_view(d, row["view"]); S = og.view_S(P, Hm)
        if key not in cache:
            cache[key] = ob.leak_with_se(ob.encode(P, b_R, P["tr"]), ob.encode(P, b_R, P["te"]), S, P)
        lR, seR = cache[key]; b = np.array(row["b_aware"])
        lA, seA = ob.leak_with_se(ob.encode(P, b, P["tr"]), ob.encode(P, b, P["te"]), S, P)
        out.append(dict(row, measured_removed=lR - lA, se=math.sqrt(seR ** 2 + seA ** 2)))
        print(f"{row['dataset']:13s} {row['view']:>14s} f={row['f']:.2f} {row['cls']:>15s} pred {row['pred_removed']:+.3f} "
              f"meas {lR - lA:+.3f} +- {math.sqrt(seR**2 + seA**2):.3f}", flush=True)
    json.dump(out, open(out_path, "w"), indent=1); print("wrote", out_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["check", "predict", "measure"])
    ap.add_argument("--pred", default="scope_predictions.json"); ap.add_argument("--out", default="scope_measured.json")
    a = ap.parse_args()
    if a.stage == "check":
        for f in LOADERS:
            d = f(); print(f"{d['name']:13s} {d['T'].shape}  Y={d['cols'][:d['m']]}  ctx={d['cols'][d['m']:]}")
        for d in controls(): print(f"{d['name']:13s} {d['T'].shape}")
    elif a.stage == "predict":
        predict(a.pred)
    else:
        measure(a.pred, a.out)
