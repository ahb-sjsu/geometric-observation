"""diag_s21.py (diagnostic, 2026-10-02): per-seed anatomy of the GaussCoupled-s21 mix1 outliers in registration 5."""
import json, math
import numpy as np
import ot_boundary as ob
import ot_gaussianity as og
import ot_nearboundary as nb

d = [c for c in nb.controls() if c["name"] == "GaussCoupled-s21"][0]
row = [r for r in json.load(open("nb_predictions.json"))["rows"] if r["dataset"] == d["name"] and r["view"] == "mix1" and r["f"] == 0.02][0]
b_aw = np.array(row["b_aware"])
P0, Sig0, m, F, B, bR0, Hm0, AS = ob.setup(d, ("mix", 1))
for seed in range(10):
    orig = ob.prepare; ob.prepare = lambda dd, s_=seed: orig(dd, seed=s_)
    try:
        P, Sig, m, F, B, b_R, Hm, AS = ob.setup(d, ("mix", 1))
    finally:
        ob.prepare = orig
    S = og.view_S(P, Hm)
    zA = P["Ts"][P["te"]] @ b_aw; zR = P["Ts"][P["te"]] @ b_R; s = S[P["te"], 0]
    lR, _ = ob.leak_with_se(ob.encode(P, b_R, P["tr"]), ob.encode(P, b_R, P["te"]), S, P)
    lA, _ = ob.leak_with_se(ob.encode(P, b_aw, P["tr"]), ob.encode(P, b_aw, P["te"]), S, P)
    cA = ob.encode(P, b_aw, P["te"]); occ = np.bincount(cA, minlength=8) / len(cA)
    print(f"seed {seed}: bR.Sig0.bR0 {float(b_R @ Sig0 @ bR0):+.3f} | corr(zR,S) {np.corrcoef(zR, s)[0,1]:+.3f} "
          f"corr(zA,S) {np.corrcoef(zA, s)[0,1]:+.3f} | leak R {lR:.3f} A {lA:.3f} | Hm row {np.round(Hm[0], 3)} "
          f"| aware cell occupancy {np.round(occ, 3)}")
