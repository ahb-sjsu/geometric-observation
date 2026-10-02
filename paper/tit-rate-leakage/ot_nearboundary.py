"""ot_nearboundary.py: registration 5, the corrected near-boundary test (registered 2026-10-02).

Background. Registration 4 (9fa0d23) showed, post hoc, that the near-boundary criterion compared the measured removal
with ZERO although its cases are predicted at 0.03-0.05 bit. Compared with the PREDICTION, the 20-split means sat
within 0.006 bit of it on Gaussian controls, but near zero on real in-scope data (shortfall ~0.04 bit). This
registration tests that reading blind, on six public datasets never loaded by this program, and asks which form the
real-data shortfall takes.

Cases. For each dataset and two new Gaussian controls (seeds 21, 22): views rotated from the decoder's principal read
toward the least-correlated context column by PHIS = 1, 2, 3, 5, 8 degrees, at slack FRACS = 0.02, 0.05, 0.10, 0.20.
Stage "predict" computes on the seed-0 training half the predicted removal, the frozen aware direction, the Gaussian
departure Gamma and the scope flag (Gamma <= CUT = 0.835 bit, frozen in registration 2), and SELECTS the cases with
0 < predicted removal <= 0.15 bit. Only selected cases are measured.
Measurement. Each selected case on R = 10 splits (seeds 0..9): frozen directions, the same 3-bit codes and three
adversaries refit on each split. Reported per case: mean over splits m, its standard error s = SD/sqrt(10).

Criteria.
  P1c  Gaussian controls: |m - pred| <= max(3 s, 0.01 bit) in at least 80% of selected control cases.
  P1r  real in-scope cases: the same agreement in at least 80% (the post hoc reading of registration 4 predicts FAIL).
  SH   real in-scope cases: median shortfall (pred - m) > 0, with its 2.5th bootstrap percentile over cases above 0.
  Form of the shortfall, least squares m = alpha + beta * pred over real in-scope selected cases, bootstrap over cases
  (1000 resamples, seed 0) for the standard errors:
    D1  OFFSET:      alpha + 3 SE(alpha) < 0 and |beta - 1| <= 2 SE(beta)
    A1  ATTENUATION: |alpha| <= 2 SE(alpha) and beta + 3 SE(beta) < 1
    neither -> unresolved form, reported.
  Each real-data criterion is vacuous below 20 selected in-scope cases; P1c is vacuous below 10 control cases.
  Reported: the same fit clustered by dataset (bootstrap over datasets), and every statistic for out-of-scope cases.
Stages: check -> predict (nb_predictions.json, pushed before measure) -> measure (nb_measured.json) -> score.
"""
import math, json, sys
import numpy as np, pandas as pd
from scipy.linalg import eigh
import ot_boundary as ob
import ot_gaussianity as og
import ot_scope as sc

CUT = sc.CUT
PHIS = (1, 2, 3, 5, 8)
FRACS = (0.02, 0.05, 0.10, 0.20)
R = 10
UCI = og.UCI
CTRL = {"GaussCoupled-s21", "Gauss8-s22"}

def load_seoulbike():
    df = pd.read_csv(og._member(ob._zip(UCI + "560/seoul+bike+sharing+demand.zip"), ".csv"), encoding="latin-1")
    df.columns = [c.split("(")[0].strip() for c in df.columns]
    v = [c for c in df.columns if c not in ("Date", "Rented Bike Count", "Seasons", "Holiday", "Functioning Day")]
    return ob.pack("SeoulBike", df[["Rented Bike Count"]].to_numpy(float), df[v].to_numpy(float), [v[0]], ["count"], v)

def load_liver():
    df = pd.read_csv(og._member(ob._zip(UCI + "60/liver+disorders.zip"), "bupa.data"), header=None)
    v = ["mcv", "alkphos", "sgpt", "sgot", "gammagt"]
    return ob.pack("Liver", df[[5]].to_numpy(float), df[[0, 1, 2, 3, 4]].to_numpy(float), ["mcv"], ["drinks"], v)

def load_hardware():
    df = pd.read_csv(og._member(ob._zip(UCI + "29/computer+hardware.zip"), "machine.data"), header=None)
    v = ["MYCT", "MMIN", "MMAX", "CACH", "CHMIN", "CHMAX"]
    return ob.pack("Hardware", df[[8]].to_numpy(float), df[[2, 3, 4, 5, 6, 7]].to_numpy(float), ["MYCT"], ["PRP"], v)

def load_ai4i():
    df = pd.read_csv(og._member(ob._zip(UCI + "601/ai4i+2020+predictive+maintenance+dataset.zip"), ".csv"))
    v = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"]
    names = ["air_temp", "process_temp", "speed", "torque", "tool_wear"]
    return ob.pack("AI4I", df[[v[3]]].to_numpy(float), df[[v[0], v[1], v[2], v[4]]].to_numpy(float),
                   ["air_temp"], ["torque"], [names[0], names[1], names[2], names[4]])

def load_metro():
    df = pd.read_csv(og._member(ob._zip(UCI + "492/metro+interstate+traffic+volume.zip"), ".csv.gz"), compression="gzip")
    v = ["temp", "rain_1h", "snow_1h", "clouds_all"]
    return ob.pack("Metro", df[["traffic_volume"]].to_numpy(float), df[v].to_numpy(float), ["temp"], ["traffic"], v)

def load_pm25():
    df = pd.read_csv(og._member(ob._zip(UCI + "381/beijing+pm2+5+data.zip"), ".csv")).dropna()
    v = ["DEWP", "TEMP", "PRES", "Iws", "Is", "Ir"]
    return ob.pack("PM25", df[["pm2.5"]].to_numpy(float), df[v].to_numpy(float), ["TEMP"], ["pm25"], v)

LOADERS = (load_seoulbike, load_liver, load_hardware, load_ai4i, load_metro, load_pm25)

def controls():
    g = ob.synthetic_sets()
    return [ob.synth("GaussCoupled-s21", g[0]["T"].T @ g[0]["T"] / len(g[0]["T"]), 2, 20000, 21),
            ob.synth("Gauss8-s22", g[1]["T"].T @ g[1]["T"] / len(g[1]["T"]), 2, 20000, 22)]

def predict(out_path):
    rows = []
    for d in [f() for f in LOADERS] + controls():
        for phi in PHIS:
            P, Sig, m, F, B, b_R, Hm, AS = ob.setup(d, ("mix", phi))
            R2R = ob.rayleigh(AS, Sig, b_R); trY = float(np.trace(F @ Sig @ F.T)); DR = trY - ob.GAIN * ob.rayleigh(B, Sig, b_R)
            S = og.view_S(P, Hm); dR = og.departure(P, S, b_R)
            for f in FRACS:
                D0 = DR + f * (trY - DR); need = (trY - D0) / ob.GAIN
                b_aw = ob.exact_aware(AS, B, Sig, need); R2aw = ob.rayleigh(AS, Sig, b_aw); dA = og.departure(P, S, b_aw)
                pred = ob.h_gauss(R2R) - ob.h_gauss(R2aw); G = dR["excess"] + dA["excess"]
                rows.append(dict(dataset=d["name"], view=f"mix{phi}", phi=phi, f=f, pred_removed=pred,
                                 b_aware=[float(x) for x in b_aw], Gamma=G, in_scope=bool(G <= CUT),
                                 selected=bool(0 < pred <= 0.15)))
        print(d["name"], "predicted", flush=True)
    sel = [r for r in rows if r["selected"]]
    print(f"{len(rows)} cases, {len(sel)} selected; real in scope selected "
          f"{sum(r['in_scope'] and r['dataset'] not in CTRL for r in sel)}; control selected {sum(r['dataset'] in CTRL for r in sel)}")
    json.dump(dict(cut=CUT, phis=PHIS, fracs=FRACS, R=R, rows=rows), open(out_path, "w"), indent=1)

def measure(pred_path, out_path):
    pred = json.load(open(pred_path)); sets = {d["name"]: d for d in [f() for f in LOADERS] + controls()}; out = []
    for c in [r for r in pred["rows"] if r["selected"]]:
        vals = []
        for seed in range(R):
            orig = ob.prepare; ob.prepare = lambda dd, s_=seed: orig(dd, seed=s_)
            try:
                P, Sig, m, F, B, b_R, Hm, AS = ob.setup(sets[c["dataset"]], ("mix", c["phi"]))
            finally:
                ob.prepare = orig
            S = og.view_S(P, Hm); b = np.array(c["b_aware"])
            lR, _ = ob.leak_with_se(ob.encode(P, b_R, P["tr"]), ob.encode(P, b_R, P["te"]), S, P)
            lA, _ = ob.leak_with_se(ob.encode(P, b, P["tr"]), ob.encode(P, b, P["te"]), S, P)
            vals.append(lR - lA)
        v = np.array(vals)
        out.append(dict(c, reps=v.tolist(), mean=float(v.mean()), sem=float(v.std(ddof=1) / math.sqrt(R))))
        print(f"{c['dataset']:16s} {c['view']:>6s} f={c['f']:.2f} pred {c['pred_removed']:+.4f} mean {v.mean():+.4f} "
              f"+- {v.std(ddof=1) / math.sqrt(R):.4f} scope {c['in_scope']}", flush=True)
    json.dump(out, open(out_path, "w"), indent=1)

def fit(rows, groups=None, B=1000):
    x = np.array([r["pred_removed"] for r in rows]); y = np.array([r["mean"] for r in rows])
    a, b = np.polyfit(x, y, 1)[::-1]; g = np.random.default_rng(0); est = []
    units = sorted(set(groups)) if groups is not None else None
    for _ in range(B):
        if units is None:
            i = g.integers(0, len(x), len(x))
        else:
            pick = g.choice(units, len(units)); i = np.concatenate([np.flatnonzero(np.array(groups) == u) for u in pick])
        if len(set(x[i])) > 1: est.append(np.polyfit(x[i], y[i], 1)[::-1])
    est = np.array(est); return a, b, est[:, 0].std(), est[:, 1].std()

def score(meas_path):
    rows = json.load(open(meas_path))
    def agree(r): return abs(r["mean"] - r["pred_removed"]) <= max(3 * r["sem"], 0.01)
    show = lambda n, ok, d: print(f"{n}: {ok if isinstance(ok, str) else ('PASS' if ok else 'FAIL')}  {d}")
    ctl = [r for r in rows if r["dataset"] in CTRL]; real = [r for r in rows if r["dataset"] not in CTRL and r["in_scope"]]
    out = [r for r in rows if r["dataset"] not in CTRL and not r["in_scope"]]
    pc = np.mean([agree(r) for r in ctl]) if ctl else float("nan")
    show("P1c", "VACUOUS" if len(ctl) < 10 else bool(pc >= 0.8), f"{pc:.1%} of {len(ctl)} control cases agree with the prediction")
    vac = len(real) < 20
    pr = np.mean([agree(r) for r in real]) if real else float("nan")
    show("P1r", "VACUOUS" if vac else bool(pr >= 0.8), f"{pr:.1%} of {len(real)} real in-scope cases agree with the prediction")
    if real:
        sh = np.array([r["pred_removed"] - r["mean"] for r in real]); g = np.random.default_rng(0)
        meds = [np.median(sh[g.integers(0, len(sh), len(sh))]) for _ in range(2000)]
        show("SH", "VACUOUS" if vac else bool(np.median(sh) > 0 and np.percentile(meds, 2.5) > 0),
             f"median shortfall {np.median(sh):+.4f} bit, bootstrap 2.5th percentile {np.percentile(meds, 2.5):+.4f}")
        a, b, sa, sb = fit(real)
        d1 = a + 3 * sa < 0 and abs(b - 1) <= 2 * sb; a1 = abs(a) <= 2 * sa and b + 3 * sb < 1
        print(f"fit m = {a:+.4f} (SE {sa:.4f}) + {b:.3f} (SE {sb:.3f}) pred over {len(real)} cases")
        show("D1 offset", "VACUOUS" if vac else bool(d1), ""); show("A1 attenuation", "VACUOUS" if vac else bool(a1), "")
        if not vac and not (d1 or a1): print("form: unresolved (neither D1 nor A1)")
        ac, bc, sac, sbc = fit(real, [r["dataset"] for r in real])
        print(f"reported, clustered by dataset: alpha {ac:+.4f} (SE {sac:.4f}), beta {bc:.3f} (SE {sbc:.3f})")
    if out:
        print(f"reported, out of scope: {np.mean([agree(r) for r in out]):.1%} of {len(out)} agree; median shortfall "
              f"{np.median([r['pred_removed'] - r['mean'] for r in out]):+.4f}")
    for ds in sorted({r["dataset"] for r in rows}):
        rs = [r for r in rows if r["dataset"] == ds]
        print(f"   {ds:16s} n={len(rs):3d} in scope {sum(r['in_scope'] for r in rs):3d} agree {np.mean([agree(r) for r in rs]):.0%} "
              f"median shortfall {np.median([r['pred_removed'] - r['mean'] for r in rs]):+.4f}")

if __name__ == "__main__":
    st = sys.argv[1]
    if st == "check":
        for f in LOADERS:
            d = f(); print(f"{d['name']:12s} {d['T'].shape}  Y={d['cols'][:d['m']]}  ctx={d['cols'][d['m']:]}")
    elif st == "predict": predict("nb_predictions.json")
    elif st == "measure": measure("nb_predictions.json", "nb_measured.json")
    else: score("nb_measured.json")
