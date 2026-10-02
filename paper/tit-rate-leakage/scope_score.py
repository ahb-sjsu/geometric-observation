"""Scores the third registration (ot_scope.py) against the criteria frozen in scope_predictions.json.
Usage: python scope_score.py [scope_predictions.json] [scope_measured.json]"""
import json, sys
import numpy as np
from scipy.stats import spearmanr

a = sys.argv[1:] + [None] * 2
pred = json.load(open(a[0] or "scope_predictions.json")); rows = json.load(open(a[1] or "scope_measured.json"))
CTRL = {"GaussCoupled-s11", "Gauss8-s12"}
MAIN_F = (0.05, 0.15, 0.4)
data = [r for r in rows if r["dataset"] not in CTRL]
def main(r): return r["view"] != "orth" and r["f"] in MAIN_F
def show(name, ok, detail): print(f"{name}: {'PASS' if ok is True else ('FAIL' if ok is False else ok)}  {detail}")
def rho(rs): return spearmanr([r["pred_removed"] for r in rs], [r["measured_removed"] for r in rs]).correlation

def s123(rs, tag):
    big = [r for r in rs if r["pred_removed"] >= 0.10]; pos = np.mean([r["measured_removed"] > 0 for r in big]) if big else float("nan")
    s1 = bool(pos >= 0.8 and rho(rs) >= 0.6) if big else "VACUOUS"
    small = [r for r in rs if r["pred_removed"] < 0.05]
    w = np.mean([abs(r["measured_removed"]) <= 2 * r["se"] for r in small]) if small else float("nan")
    s2 = bool(w >= 0.8) if len(small) >= 15 else "VACUOUS"
    mix = [r for r in rs if r["view"].startswith("mix")]; r5 = rho(mix) if len(mix) > 2 else float("nan")
    s3 = bool(r5 >= 0.6) if len(mix) >= 15 else "VACUOUS"
    return [("S1" + tag, s1, f"positive {pos:.1%} of {len(big)} predicted >= 0.10; Spearman {rho(rs):.3f} over {len(rs)}"),
            ("S2" + tag, s2, f"|measured| <= 2 SE in {w:.1%} of {len(small)}"),
            ("S3" + tag, s3, f"mix-family Spearman {r5:.3f} over {len(mix)}")]

right = 0
for ds, fc in pred["forecast"].items():
    s = rho([r for r in data if r["dataset"] == ds and main(r)]); out = "TRACK" if s >= 0.8 else "MISS"; right += out == fc
    print(f"   {ds:13s} forecast {fc:5s} outcome {out:5s} (Spearman {s:+.3f}, median Gamma {pred['median_gamma'][ds]:.4f})")
show("S0", bool(right >= 5), f"{right} of {len(pred['forecast'])} forecasts correct")
ins = [r for r in data if r["in_scope"] and main(r)]
for n, ok, det in s123(ins, ""): show(n, ok, det)
on = [r for r in data if r["in_scope"] and r["view"] in ("mix15", "orth")]
cal = np.mean([abs(r["measured_removed"] - r["pred_removed"]) <= 2 * r["se"] for r in on]) if on else float("nan")
show("S4a", bool(cal >= 0.8) if len(on) >= 15 else "VACUOUS", f"within 2 SE of predicted in {cal:.1%} of {len(on)} onset cases")
o = [r for r in on if r["view"] == "orth" and r["f"] == 0.02 and r["pred_removed"] < 0.02]
m = [r for r in on if r["view"] == "mix15" and r["f"] == 0.02 and r["pred_removed"] >= 0.05]
fo = np.mean([abs(r["measured_removed"]) <= 2 * r["se"] for r in o]) if o else float("nan")
fm = np.mean([r["measured_removed"] > 2 * r["se"] for r in m]) if m else float("nan")
show("S4b", bool(fo >= 0.8 and fm >= 0.8) if (len(o) >= 3 and len(m) >= 3) else "VACUOUS",
     f"orth at 0.02 within 2 SE of zero {fo:.1%} (n={len(o)}); mix15 at 0.02 above 2 SE {fm:.1%} (n={len(m)})")
ctrl = [r for r in rows if r["dataset"] in CTRL]
k1 = np.mean([r["Gamma"] == 0 for r in ctrl]); show("K1", bool(k1 >= 0.7), f"Gamma = 0 in {k1:.1%} of {len(ctrl)} control cases")
outs = [r for r in data if not r["in_scope"] and main(r)]
for n, ok, det in s123(outs, " (out of scope, reported)"): print(f"{n}: {det}  [would be {ok}]")
for ds in pred["forecast"]:
    rs = [r for r in data if r["dataset"] == ds]
    print(f"   {ds:13s} in scope {sum(r['in_scope'] for r in rs)}/{len(rs)}")

# ---- marginal-correction law and equal-occupancy codes ----
def miss(r, k): return abs(r["measured_removed"] - r[k])
m1r = spearmanr([r["pred_removed_marg"] for r in data], [r["measured_removed"] for r in data]).correlation
mm, mg = np.mean([miss(r, "pred_removed_marg") for r in data]), np.mean([miss(r, "pred_removed") for r in data])
show("M1", bool(m1r >= 0.8 and mm < mg), f"Spearman {m1r:.3f} over {len(data)}; mean|miss| {mm:.3f} vs Gaussian {mg:.3f}")
def eqmiss(r): return abs(r["measured_removed_eq"] - r["pred_removed_eq"])
outs_all = [r for r in data if not r["in_scope"]]
if len(outs_all) >= 15:
    ae = np.mean([eqmiss(r) <= 2 * r["se_eq"] for r in outs_all]); al = np.mean([miss(r, "pred_removed") <= 2 * r["se"] for r in outs_all])
    re = spearmanr([r["pred_removed_eq"] for r in outs_all], [r["measured_removed_eq"] for r in outs_all]).correlation
    show("E1", bool(ae - al >= 0.15 and re >= 0.6), f"out of scope n={len(outs_all)}: agree {ae:.1%} (equal-occupancy) vs {al:.1%} (standard); Spearman {re:.3f}")
else:
    show("E1", "VACUOUS", f"{len(outs_all)} out-of-scope cases")
r2 = spearmanr([r["pred_removed_eq"] for r in data], [r["measured_removed_eq"] for r in data]).correlation
me = np.mean([eqmiss(r) for r in data])
show("E2", bool(r2 >= 0.8 and me < mg), f"Spearman {r2:.3f} over {len(data)}; mean|miss| {me:.3f} vs standard-Gaussian {mg:.3f}")
missf = [ds for ds, fc in pred["forecast"].items() if fc == "MISS"]
if missf:
    tr = 0
    for ds in missf:
        rs = [r for r in data if r["dataset"] == ds and main(r)]
        s_ = spearmanr([r["pred_removed_eq"] for r in rs], [r["measured_removed_eq"] for r in rs]).correlation
        tr += s_ >= 0.8; print(f"   {ds:13s} equal-occupancy Spearman {s_:+.3f}")
    show("E3", bool(tr >= len(missf) / 2), f"{tr} of {len(missf)} MISS-forecast datasets track with equal-occupancy codes")
else:
    show("E3", "VACUOUS", "no dataset forecast MISS")

# ---- Theory Radar formulas, reported only ----
def rep_formula(name, flag, ref):
    yv = np.array([miss(r, ref) > 2 * r["se"] for r in data]); pv = np.array([flag(r) for r in data])
    tp = np.sum(pv & yv); fp = np.sum(pv & ~yv); fn = np.sum(~pv & yv)
    print(f"{name}: reported  accuracy {np.mean(pv == yv):.3f} (base rate of misses {yv.mean():.3f}), F1 {2*tp/max(2*tp+fp+fn,1):.3f}")
rep_formula("T0", lambda r: -(r["d_marg_R"] / r["kappa_A"]) >= 0.1757, "pred_removed")
rep_formula("T1", lambda r: (r["dep_c_R"] - r["dep_c_A"]) ** 2 >= 0.005175, "pred_removed_marg")
