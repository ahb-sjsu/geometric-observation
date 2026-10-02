"""ot_s2noise.py: why do near-zero predictions fail? Registered 2026-10-02 after registration 3 (S2 FAIL, 34.8% of 23).

The near-boundary criterion (|measured removal| <= 2 SE where the predicted removal is below 0.05 bit) failed in the
boundary test (56%), in the post hoc in-scope split (64%), and blind in scope in registration 3 (35%). Two accounts
compete.
  NOISE: the SE understates the measurement's variability. It is a bootstrap over held-out points for a FIXED split
         and FIXED fitted adversaries, so it omits the variability of the split and of the adversaries' training.
  BIAS:  near the boundary the measured removal is systematically nonzero (the theory misses there).
Design. The near-zero in-scope cases of all three registrations are fixed by the rule below. Each is measured again on
R = 20 fresh random splits (seeds 1..20), with the frozen directions b_R and b_aware, the same codes, the same three
adversaries refit on each split, and the same bootstrap SE. Seed 0 is the original measurement.
Case rule (no outcome used beyond what is already published): predicted removal < 0.05 bit; in scope (Gamma <= CUT,
from gauss_predictions.json for the boundary-test and fresh cases, and the frozen in_scope flag for registration 3);
not a principal-copy view; not the orth family; registration-3 cases at slack 0.05, 0.15, 0.4 (its S2 set).
Real datasets form the test group (71 cases); synthetic Gaussian sources form the control group (14 cases, reported,
not scored). The warped Gauss8-exp control is dropped (deliberately non-Gaussian, so it is neither).
Criteria (real group; vacuous below 15 cases):
  N1  median over cases of SD_rep / mean bootstrap SE >= 1.5           (the bootstrap SE understates the variability)
  N2  |original measured| <= 2 SD_rep in at least 80% of cases           (with the full SE, the criterion would hold)
  B1  |mean of the 20 replicates| > 3 SD_rep / sqrt(20) in at least 50%  (systematic nonzero removal near the boundary)
Reading fixed in advance: N1 and N2 pass and B1 fails -> NOISE. B1 passes -> BIAS (whatever N1, N2 say about noise).
Neither -> unresolved, reported as such.
"""
import math, json, sys
import numpy as np
import ot_boundary as ob
import ot_gaussianity as og
import ot_scope as sc

CUT, R = sc.CUT, 20
SYN = {"Gauss8", "GaussCoupled", "GaussCoupled-s11", "Gauss8-s12"}   # Gaussian controls
DROP = {"Gauss8-exp"}   # deliberately non-Gaussian synthetic control: neither test nor Gaussian control

def cases():
    gp = json.load(open("gauss_predictions.json"))
    gam = {(r["dataset"], r["view"], r["f"]): r["Gamma"] for r in gp["retro"] + gp["fresh"]}
    out = []
    for src, f in (("boundary", "boundary_measured.json"), ("fresh", "fresh_measured.json")):
        for r in json.load(open(f)):
            k = (r["dataset"], r["view"], r["f"])
            if r["dataset"] not in DROP and r["view"] != "principal-copy" and r["pred_removed"] < 0.05 and k in gam and gam[k] <= CUT:
                out.append(dict(src=src, **{x: r[x] for x in ("dataset", "view", "f", "pred_removed", "measured_removed", "se", "b_aware")}))
    for r in json.load(open("scope_measured.json")):
        if r["in_scope"] and r["view"] != "orth" and r["f"] in (0.05, 0.15, 0.4) and r["pred_removed"] < 0.05:
            out.append(dict(src="scope", **{x: r[x] for x in ("dataset", "view", "f", "pred_removed", "measured_removed", "se", "b_aware")}))
    return out

def datasets():
    ds = ob.DATA + ob.synthetic_sets() + [f() for f in og.FRESH_LOADERS] + [og.warped_gauss8()] + [f() for f in sc.LOADERS] + sc.controls()
    return {d["name"]: d for d in ds}

def measure_case(d, c, seed):
    orig = ob.prepare
    ob.prepare = lambda dd, seed_=seed: orig(dd, seed=seed_)          # every split in setup uses this seed
    try:
        P, Sig, m, F, B, b_R, Hm, AS = sc.setup_view(d, c["view"])
    finally:
        ob.prepare = orig
    S = og.view_S(P, Hm); b = np.array(c["b_aware"])
    lR, seR = ob.leak_with_se(ob.encode(P, b_R, P["tr"]), ob.encode(P, b_R, P["te"]), S, P)
    lA, seA = ob.leak_with_se(ob.encode(P, b, P["tr"]), ob.encode(P, b, P["te"]), S, P)
    return lR - lA, math.sqrt(seR ** 2 + seA ** 2)

if __name__ == "__main__":
    cs = cases()
    real = [c for c in cs if c["dataset"] not in SYN]
    print(f"{len(cs)} near-zero in-scope cases: {len(real)} real, {len(cs) - len(real)} synthetic control")
    if len(sys.argv) > 1 and sys.argv[1] == "count":
        from collections import Counter
        print(Counter((c["src"], c["dataset"]) for c in cs)); sys.exit(0)
    sets = datasets(); out = []
    for c in cs:
        reps = [measure_case(sets[c["dataset"]], c, s) for s in range(1, R + 1)]
        m = np.array([x[0] for x in reps]); se = np.array([x[1] for x in reps])
        out.append(dict(c, reps=m.tolist(), rep_se=se.tolist(), sd_rep=float(m.std(ddof=1)), mean_rep=float(m.mean())))
        print(f"{c['src']:8s} {c['dataset']:13s} {c['view']:>18s} f={c['f']:.2f} pred {c['pred_removed']:+.3f} "
              f"orig {c['measured_removed']:+.3f}+-{c['se']:.3f} | reps mean {m.mean():+.3f} sd {m.std(ddof=1):.3f} "
              f"boot se {se.mean():.3f}", flush=True)
    json.dump(out, open("s2noise_measured.json", "w"), indent=1)
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
