"""POST HOC (written 2026-10-02 after gauss_score.py was run; not a registered test).
Re-reads the boundary criteria C2 and C5 split by the Gaussian-departure index Gamma, on the boundary test's real
datasets (old) and on the fresh datasets, using the B3 cut frozen in gauss_predictions.json. Descriptive only: any
claim it suggests needs a new registration on data not yet measured."""
import json
import numpy as np
from scipy.stats import spearmanr

pred = json.load(open("gauss_predictions.json")); cut = pred["forecast_cut"]
SYN = {"GaussCoupled", "Gauss8", "Gauss8-exp"}
def join(gam, meas):
    m = {(r["dataset"], r["view"], r["f"]): r for r in meas}
    return [dict(m[(g["dataset"], g["view"], g["f"])], Gamma=g["Gamma"]) for g in gam]
sets = {"old": join(pred["retro"], json.load(open("boundary_measured.json"))),
        "fresh": join(pred["fresh"], json.load(open("fresh_measured.json")))}
print(f"cut on case Gamma = {cut:.3f} bit (the frozen B3 cut, applied per case here)")
for name, rows in sets.items():
    rows = [r for r in rows if r["dataset"] not in SYN]
    for lab, sel in (("Gamma <= cut", lambda r: r["Gamma"] <= cut), ("Gamma >  cut", lambda r: r["Gamma"] > cut)):
        rs = [r for r in rows if sel(r)]
        small = [r for r in rs if r["pred_removed"] < 0.05]
        c2 = np.mean([abs(r["measured_removed"]) <= 2 * r["se"] for r in small]) if small else float("nan")
        mix = [r for r in rs if r["view"].startswith("mix")]
        c5 = spearmanr([r["pred_removed"] for r in mix], [r["measured_removed"] for r in mix]).correlation if len(mix) > 2 else float("nan")
        big = [r for r in rs if r["pred_removed"] >= 0.10]
        c1 = np.mean([r["measured_removed"] > 0 for r in big]) if big else float("nan")
        print(f"{name:5s} {lab}: n={len(rs):3d}  C1-pos {c1:.1%} (n={len(big)})  C2 {c2:.1%} (n={len(small)})  "
              f"C5 Spearman {c5:.3f} (n={len(mix)})")
