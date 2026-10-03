"""ot_crossfit_b.py: phase B of the corrected measurement protocol (REGISTRATION-crossfit-2026-10-02.md, 1f1a0ac).

Registered 2026-10-02 before phase A finished and before any phase B number existed. Same protocol as ot_crossfit.py
(cross-fitted adversary selection on two held-out folds, paired per-sample loss differences, bootstrap SE of the mean
difference); here applied to the two replicate designs.

Registration 4 (ot_s2noise.py, fec42f0). Same frozen case rule (ot_s2noise.cases(), which uses predictions and Gamma
only), same 20 replicate splits (seeds 1..20), same criteria N1, N2, B1 and the same fixed reading, computed by the
code below, which copies ot_s2noise's scoring block verbatim. The seed-0 measurement used by N2 is the phase A
cross-fitted value of the same case (boundary/fresh/scope *_crossfit.json). Output s2noise_measured_crossfit.json.

Registration 5 (ot_nearboundary.py, ae487c4; predictions 3f9d1aa). Same selected cases and 10 splits (seeds 0..9),
scored by ot_nearboundary.score on nb_measured_crossfit.json, so P1c, P1r, SH, D1 and A1 are unchanged.
"""
import math, json, sys
import numpy as np
import ot_boundary as ob
import ot_gaussianity as og
import ot_scope as sc
import ot_s2noise as s2
import ot_nearboundary as nb
from ot_crossfit import per_sample_losses, folds_for, paired, view_S

def measure_seed(d, view, b_aware, seed, setup):
    orig = ob.prepare; ob.prepare = lambda dd, s_=seed: orig(dd, seed=s_)
    try:
        P, Sig, m, F, B, b_R, Hm, AS = setup(d, view)
    finally:
        ob.prepare = orig
    S = view_S(P, Hm); fo = folds_for(P); b = np.array(b_aware)
    lR = per_sample_losses(ob.encode(P, b_R, P["tr"]), ob.encode(P, b_R, P["te"]), S, P, fo)
    lA = per_sample_losses(ob.encode(P, b, P["tr"]), ob.encode(P, b, P["te"]), S, P, fo)
    rem, se, _, _ = paired(lR, lA); return rem, se

def reg4():
    cs = s2.cases(); sets = s2.datasets()
    seed0 = {}
    for src, f in (("boundary", "boundary_measured_crossfit.json"), ("fresh", "fresh_measured_crossfit.json"),
                   ("scope", "scope_measured_crossfit.json")):
        for r in json.load(open(f)): seed0[(src, r["dataset"], r["view"], r["f"])] = (r["measured_removed"], r["se"])
    out = []
    for c in cs:
        c = dict(c); c["measured_removed"], c["se"] = seed0[(c["src"], c["dataset"], c["view"], c["f"])]
        reps = [measure_seed(sets[c["dataset"]], c["view"], c["b_aware"], s, sc.setup_view) for s in range(1, s2.R + 1)]
        m = np.array([x[0] for x in reps]); se = np.array([x[1] for x in reps])
        out.append(dict(c, reps=m.tolist(), rep_se=se.tolist(), sd_rep=float(m.std(ddof=1)), mean_rep=float(m.mean()),
                        protocol="crossfit-paired"))
        print(f"{c['src']:8s} {c['dataset']:13s} {c['view']:>18s} f={c['f']:.2f} pred {c['pred_removed']:+.3f} "
              f"seed0 {c['measured_removed']:+.3f}+-{c['se']:.3f} | reps mean {m.mean():+.3f} sd {m.std(ddof=1):.3f}", flush=True)
    json.dump(out, open("s2noise_measured_crossfit.json", "w"), indent=1)
    R, SYN = s2.R, s2.SYN
    # ---- scoring block copied verbatim from ot_s2noise.py ----
    for grp, rows in (("REAL (scored)", [o for o in out if o["dataset"] not in SYN]),
                      ("CONTROL (reported)", [o for o in out if o["dataset"] in SYN])):
        if not rows: print(grp, "no cases"); continue
        ratio = float(np.median([o["sd_rep"] / np.mean(o["rep_se"]) for o in rows]))
        n2 = float(np.mean([abs(o["measured_removed"]) <= 2 * o["sd_rep"] for o in rows]))
        b1 = float(np.mean([abs(o["mean_rep"]) > 3 * o["sd_rep"] / math.sqrt(R) for o in rows]))
        orig2 = float(np.mean([abs(o["measured_removed"]) <= 2 * o["se"] for o in rows]))
        pos = float(np.mean([o["mean_rep"] > 0 for o in rows]))
        vac = len(rows) < 15
        tag = (lambda ok: "VACUOUS" if vac else ("PASS" if ok else "FAIL")) if grp.startswith("REAL") else (lambda ok: "reported")
        print(f"== {grp}: n={len(rows)}; original criterion {orig2:.1%}")
        print(f"N1 {tag(ratio >= 1.5)}: median SD_rep / bootstrap SE {ratio:.2f}")
        print(f"N2 {tag(n2 >= 0.8)}: |original| <= 2 SD_rep in {n2:.1%}")
        print(f"B1 {tag(b1 >= 0.5)}: |replicate mean| > 3 SD_rep/sqrt(20) in {b1:.1%}; replicate mean positive in {pos:.1%}")

def reg5():
    pred = json.load(open("nb_predictions.json")); sets = {d["name"]: d for d in [f() for f in nb.LOADERS] + nb.controls()}
    out = []
    setup = lambda d, view: ob.setup(d, ("mix", int(view[3:])))
    for c in [r for r in pred["rows"] if r["selected"]]:
        v = np.array([measure_seed(sets[c["dataset"]], c["view"], c["b_aware"], s, setup)[0] for s in range(nb.R)])
        out.append(dict(c, reps=v.tolist(), mean=float(v.mean()), sem=float(v.std(ddof=1) / math.sqrt(nb.R)),
                        protocol="crossfit-paired"))
        print(f"{c['dataset']:16s} {c['view']:>6s} f={c['f']:.2f} pred {c['pred_removed']:+.4f} mean {v.mean():+.4f} "
              f"+- {v.std(ddof=1) / math.sqrt(nb.R):.4f} scope {c['in_scope']}", flush=True)
    json.dump(out, open("nb_measured_crossfit.json", "w"), indent=1)
    nb.score("nb_measured_crossfit.json")

if __name__ == "__main__":
    {"reg4": reg4, "reg5": reg5}[sys.argv[1]]()
