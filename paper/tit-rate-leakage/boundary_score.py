"""Scores boundary_measured.json against the criteria frozen in boundary_predictions.json (written before measurement)."""
import json, math, sys
import numpy as np
from scipy.stats import spearmanr

pred = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "boundary_predictions.json"))
meas = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "boundary_measured.json"))
crit = pred["criteria"]
real = [r for r in meas if r["view"] != "principal-copy"]
synthetic = {"GaussCoupled", "Gauss8"}

def frac(xs): return sum(xs) / len(xs) if xs else float("nan")
def show(name, ok, detail): print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")

# C1
big = [r for r in real if r["pred_removed"] >= 0.10]
pos = frac([r["measured_removed"] > 0 for r in big])
rho = spearmanr([r["pred_removed"] for r in real], [r["measured_removed"] for r in real]).correlation
show("C1", pos >= 0.8 and rho >= 0.6, f"positive in {pos:.1%} of {len(big)} cases with prediction >= 0.10 bit; Spearman {rho:.3f} over {len(real)} cases")
# C2
small = [r for r in real if r["pred_removed"] < 0.05]
within = frac([abs(r["measured_removed"]) <= 2 * r["se"] for r in small])
show("C2", within >= 0.8, f"|measured| <= 2 SE in {within:.1%} of {len(small)} near-boundary cases")
# C3
syn = [r for r in real if r["dataset"] in synthetic]
cal = frac([abs(r["measured_removed"] - r["pred_removed"]) <= 2 * r["se"] for r in syn])
show("C3", cal >= 0.8, f"measured within 2 SE of predicted in {cal:.1%} of {len(syn)} synthetic Gaussian cases")
# C4
for ds in ("Wine", "Zoo"):
    rs = [r for r in real if r["dataset"] == ds]
    print(f"C4 {ds}: positive where predicted >= 0.10 bit in {frac([r['measured_removed'] > 0 for r in rs if r['pred_removed'] >= 0.10]):.1%}; "
          f"Spearman {spearmanr([r['pred_removed'] for r in rs], [r['measured_removed'] for r in rs]).correlation:.3f} over {len(rs)} cases")
# C5
mix = [r for r in real if r["view"].startswith("mix")]
rho5 = spearmanr([r["pred_removed"] for r in mix], [r["measured_removed"] for r in mix]).correlation
show("C5", rho5 >= 0.6, f"Spearman {rho5:.3f} over {len(mix)} mix-family cases")
# consistency
pc = [r for r in meas if r["view"] == "principal-copy"]
print(f"consistency: principal-copy max |measured| {max(abs(r['measured_removed']) for r in pc):.2e} over {len(pc)} cases (zero by construction)")
# descriptive: calibration slope and per-dataset agreement
x = np.array([r["pred_removed"] for r in real]); y = np.array([r["measured_removed"] for r in real])
print(f"descriptive: least-squares slope of measured on predicted {np.polyfit(x, y, 1)[0]:.3f}, intercept {np.polyfit(x, y, 1)[1]:+.3f}")
for ds in sorted({r["dataset"] for r in real}):
    rs = [r for r in real if r["dataset"] == ds]
    print(f"   {ds:12s} n={len(rs):3d} Spearman {spearmanr([r['pred_removed'] for r in rs], [r['measured_removed'] for r in rs]).correlation:+.3f}  "
          f"mean pred {np.mean([r['pred_removed'] for r in rs]):.3f}  mean meas {np.mean([r['measured_removed'] for r in rs]):+.3f}")
