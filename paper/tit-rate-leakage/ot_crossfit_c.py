"""ot_crossfit_c.py: design correction for the replicate designs (registered 2026-10-02, before any number it produces).

The error. Registrations 4 (ot_s2noise.py) and 5 (ot_nearboundary.py), and phase B of the protocol amendment
(ot_crossfit_b.py), describe the directions as frozen from split 0, but their code recomputed, on every split,
  (i)  the principal read b_R (an eigenvector, whose top eigenspace is nearly degenerate in the GaussCoupled controls),
  (ii) the context column of the rotated views (the column least correlated with Z_R), which changes between splits on
       most real datasets (bR_stability-2026-10-02.txt).
So on most splits a rotated-view case measured the frozen aware code against a different view than the one it was
built for. Single-split registrations (seed 0) are unaffected.

The correction. For every case, b_R and the context column are computed once on split 0 and frozen. On each split the
view is rebuilt from the frozen b_R and column under that split's standardization, and both codes use the frozen
directions. Measurement follows the corrected protocol of ot_crossfit.py (cross-fitted adversary selection, paired
per-sample differences).

Controls. The GaussCoupled sources (GaussCoupled, GaussCoupled-s11, GaussCoupled-s21) standardize two independent
target coordinates to unit variance, which makes the top eigenvalue of the decoder's pencil nearly degenerate (relative
eigengap 0.005 to 0.020 at split 0), so their principal read is not well defined. They are excluded from scoring and
reported separately. The Gauss8 controls (eigengap about 0.27) remain the control group.

Everything else is unchanged: the case rules, seeds, adversary families, criteria, and scoring.
  Registration 4: same cases (ot_s2noise.cases()), seeds 1..20, scoring block copied verbatim from ot_s2noise.py with
  the control group restricted as above; the seed-0 value used by N2 is the phase A cross-fitted measurement.
  Registration 5: same selected cases, seeds 0..9, scored by ot_nearboundary.score on nb_measured_corrected.json, which
  holds every case except GaussCoupled-s21 (written separately to nb_measured_corrected_degenerate.json).
"""
import math, json, sys
import numpy as np
from scipy.linalg import eigh
import ot_boundary as ob
import ot_scope as sc
import ot_s2noise as s2
import ot_nearboundary as nb
from ot_crossfit import per_sample_losses, folds_for, paired, view_S

DEGENERATE = {"GaussCoupled", "GaussCoupled-s11", "GaussCoupled-s21"}

def frozen_parts(d):
    P = ob.prepare(d, seed=0); Sig = P["Sig"]; m = d["m"]; p = Sig.shape[0]
    F = np.zeros((m, p)); F[:, :m] = np.eye(m); B = Sig @ F.T @ F @ Sig
    b_R = eigh(B, Sig)[1][:, -1]; zR = b_R / math.sqrt(b_R @ Sig @ b_R); ctx = list(range(m, p))
    j = ctx[int(np.argmin([abs(float(zR @ Sig[:, k]) / math.sqrt(Sig[k, k])) for k in ctx]))]
    return b_R, j

def setup_frozen(d, view, seed, b_R, j):
    P = ob.prepare(d, seed=seed); Sig = P["Sig"]; p = Sig.shape[0]
    zR = b_R / math.sqrt(b_R @ Sig @ b_R); e = np.zeros(p); e[j] = 1.0 / math.sqrt(Sig[j, j])
    if view.startswith("mix"):
        phi = math.radians(int(view[3:])); Hm = (math.cos(phi) * zR + math.sin(phi) * e)[None, :]
    elif view == "orth":
        e = e - float(zR @ Sig @ e) * zR; Hm = (e / math.sqrt(e @ Sig @ e))[None, :]
    else:                                                   # a context column as the view: no frozen parts needed
        Hm = dict(ob.views_for(d))[view]
    return P, Hm

def measure_seed(d, view, b_aware, seed, parts):
    b_R, j = parts; P, Hm = setup_frozen(d, view, seed, b_R, j); S = view_S(P, Hm); fo = folds_for(P)
    b = np.array(b_aware)
    lR = per_sample_losses(ob.encode(P, b_R, P["tr"]), ob.encode(P, b_R, P["te"]), S, P, fo)
    lA = per_sample_losses(ob.encode(P, b, P["tr"]), ob.encode(P, b, P["te"]), S, P, fo)
    return paired(lR, lA)[:2]

def reg4():
    cs = s2.cases(); sets = s2.datasets(); parts = {}
    seed0 = {}
    for src, f in (("boundary", "boundary_measured_crossfit.json"), ("fresh", "fresh_measured_crossfit.json"),
                   ("scope", "scope_measured_crossfit.json")):
        for r in json.load(open(f)): seed0[(src, r["dataset"], r["view"], r["f"])] = (r["measured_removed"], r["se"])
    out = []
    for c in cs:
        c = dict(c); c["measured_removed"], c["se"] = seed0[(c["src"], c["dataset"], c["view"], c["f"])]
        if c["dataset"] not in parts: parts[c["dataset"]] = frozen_parts(sets[c["dataset"]])
        reps = [measure_seed(sets[c["dataset"]], c["view"], c["b_aware"], s, parts[c["dataset"]]) for s in range(1, s2.R + 1)]
        m = np.array([x[0] for x in reps]); se = np.array([x[1] for x in reps])
        out.append(dict(c, reps=m.tolist(), rep_se=se.tolist(), sd_rep=float(m.std(ddof=1)), mean_rep=float(m.mean()),
                        protocol="crossfit-paired, frozen b_R and context column"))
        print(f"{c['src']:8s} {c['dataset']:13s} {c['view']:>18s} f={c['f']:.2f} pred {c['pred_removed']:+.3f} "
              f"seed0 {c['measured_removed']:+.3f}+-{c['se']:.3f} | reps mean {m.mean():+.3f} sd {m.std(ddof=1):.3f}", flush=True)
    json.dump(out, open("s2noise_measured_corrected.json", "w"), indent=1)
    R = s2.R; SYN = s2.SYN - DEGENERATE
    print("excluded as degenerate (reported only):", sorted({o["dataset"] for o in out if o["dataset"] in DEGENERATE}))
    out = [o for o in out if o["dataset"] not in DEGENERATE]
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
    parts = {k: frozen_parts(v) for k, v in sets.items()}; out = []
    for c in [r for r in pred["rows"] if r["selected"]]:
        v = np.array([measure_seed(sets[c["dataset"]], c["view"], c["b_aware"], s, parts[c["dataset"]])[0] for s in range(nb.R)])
        out.append(dict(c, reps=v.tolist(), mean=float(v.mean()), sem=float(v.std(ddof=1) / math.sqrt(nb.R)),
                        protocol="crossfit-paired, frozen b_R and context column"))
        print(f"{c['dataset']:16s} {c['view']:>6s} f={c['f']:.2f} pred {c['pred_removed']:+.4f} mean {v.mean():+.4f} "
              f"+- {v.std(ddof=1) / math.sqrt(nb.R):.4f} scope {c['in_scope']}", flush=True)
    json.dump([o for o in out if o["dataset"] in DEGENERATE], open("nb_measured_corrected_degenerate.json", "w"), indent=1)
    json.dump([o for o in out if o["dataset"] not in DEGENERATE], open("nb_measured_corrected.json", "w"), indent=1)
    nb.score("nb_measured_corrected.json")

if __name__ == "__main__":
    {"reg4": reg4, "reg5": reg5}[sys.argv[1]]()
