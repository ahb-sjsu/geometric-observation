"""Scores the Gaussian-departure registration against the criteria frozen in gauss_predictions.json.
Usage: python gauss_score.py [gauss_predictions.json] [boundary_measured.json] [fresh_measured.json]"""
import json, sys
import numpy as np
from scipy.stats import spearmanr

a = sys.argv[1:] + [None] * 3
pred = json.load(open(a[0] or "gauss_predictions.json"))
old = json.load(open(a[1] or "boundary_measured.json"))
fresh_path = a[2] or "fresh_measured.json"
SYN = {"GaussCoupled", "Gauss8"}

def key(r): return (r["dataset"], r["view"], r["f"])
def join(gam, meas):
    m = {key(r): r for r in meas}; out = []
    for g in gam:
        r = m[key(g)]; miss = abs(r["measured_removed"] - r["pred_removed"])
        out.append(dict(g, miss=miss, agree=miss <= 2 * r["se"], meas=r["measured_removed"]))
    return out
def show(name, ok, detail): print(f"{name}: {'PASS' if ok is True else ('FAIL' if ok is False else ok)}  {detail}")
def split(rows):
    z = [r for r in rows if r["Gamma"] == 0]; p = [r for r in rows if r["Gamma"] > 0]
    if len(z) < 15 or len(p) < 15: return "VACUOUS", f"Gamma=0 n={len(z)}, Gamma>0 n={len(p)}"
    az, ap = np.mean([r["agree"] for r in z]), np.mean([r["agree"] for r in p])
    return bool(az >= 0.7 and az - ap >= 0.2), f"agree {az:.1%} (Gamma=0, n={len(z)}) vs {ap:.1%} (Gamma>0, n={len(p)})"

retro = join(pred["retro"], old)
real = [r for r in retro if r["dataset"] not in SYN]
rho = spearmanr([r["Gamma"] for r in real], [r["miss"] for r in real]).correlation
show("R1", bool(rho >= 0.3), f"Spearman(Gamma, miss) {rho:.3f} over {len(real)} cases")
ok, det = split(real); show("R2", ok, det)
syn = [r for r in retro if r["dataset"] in SYN]
k1 = np.mean([r["Gamma"] == 0 for r in syn]); show("K1", bool(k1 >= 0.9), f"Gamma = 0 in {k1:.1%} of {len(syn)} synthetic Gaussian cases")
for ds in sorted({r["dataset"] for r in retro}):
    rs = [r for r in retro if r["dataset"] == ds]
    print(f"   {ds:12s} median Gamma {np.median([r['Gamma'] for r in rs]):.4f}  mean miss {np.mean([r['miss'] for r in rs]):.3f}")

try:
    fm = json.load(open(fresh_path))
except FileNotFoundError:
    print("fresh measurement not present: B1-B3 and K2 not scored"); sys.exit(0)
fresh = join(pred["fresh"], fm)
fr = [r for r in fresh if r["dataset"] != "Gauss8-exp"]
rho = spearmanr([r["Gamma"] for r in fr], [r["miss"] for r in fr]).correlation
show("B1", bool(rho >= 0.3), f"Spearman(Gamma, miss) {rho:.3f} over {len(fr)} cases")
ok, det = split(fr); show("B2", ok, det)
right = 0
for ds, fc in pred["forecast"].items():
    rs = [r for r in fresh if r["dataset"] == ds]
    s = spearmanr([r["pred_removed"] for r in rs], [r["meas"] for r in rs]).correlation
    out = "TRACK" if s >= 0.8 else "MISS"; right += out == fc
    print(f"   {ds:12s} forecast {fc:5s} outcome {out:5s} (Spearman {s:+.3f}, median Gamma {pred['fresh_median_gamma'][ds]:.4f})")
show("B3", bool(right >= 5), f"{right} of {len(pred['forecast'])} forecasts correct")
w = [r for r in fresh if r["dataset"] == "Gauss8-exp"]; g8 = [r for r in retro if r["dataset"] == "Gauss8"]
show("K2", "reported", f"Gauss8-exp median Gamma {np.median([r['Gamma'] for r in w]):.4f}, mean miss {np.mean([r['miss'] for r in w]):.3f}"
     f" vs Gauss8 mean miss {np.mean([r['miss'] for r in g8]):.3f}")
