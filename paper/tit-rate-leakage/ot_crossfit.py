"""ot_crossfit.py: corrected measurement protocol for the leakage proxy (registered 2026-10-02, after review).

What changes. The original measurement (ot_boundary.leak_with_se) fitted three adversaries (logistic, k-NN, boosting)
on the training half, then CHOSE the lowest-loss adversary on the held-out half and reported that same loss, and its
SE combined two separate bootstraps as if the two codes were independent. Here:
  1. Cross-fitting. The held-out half is split once, at random with a fixed seed, into folds A and B. For each code,
     the adversary is selected by its mean cross-entropy on A and scored on B, and selected on B and scored on A.
     Every held-out sample is therefore scored by an adversary chosen without it.
  2. Paired differences. The two codes of a case are scored on the same samples, and the measured removal is the mean
     of the per-sample loss difference d_i = loss_R(i) - loss_A(i). Its SE is a bootstrap of that mean over samples
     (200 resamples, seed 0).
What does not change. Training/held-out splits (seed 0), the frozen directions, the codes (standard Lloyd-Max and, for
registration 3, equal-occupancy), the three adversary families and their training data, every case list, every
prediction, every criterion, and every scoring script. The quantity is still a cross-entropy PROXY for H(M|S).
Scope of this run (phase A): the boundary test (boundary_predictions.json), the fresh cases of the Gaussian-departure
registration (gauss_predictions.json), and registration 3 (scope_predictions.json). Each is re-scored by its own frozen
scoring script on the re-measured file. The original verdicts stand as the record under the original protocol; the
re-measured verdicts are reported beside them. Registrations 4 and 5 (replicate designs) are phase B.
"""
import math, json, sys
import numpy as np
import ot_boundary as ob
import ot_gaussianity as og
import ot_scope as sc

def per_sample_losses(Mtr, Mte, S, P, folds):
    """Cross-fitted per-sample cross-entropy (bits) of the held-out codes Mte."""
    losses = []
    for mk in ob.ADVERSARIES.values():
        clf = mk().fit(S[P["tr"]], Mtr); Pr = clf.predict_proba(S[P["te"]]); cols = list(clf.classes_)
        pm = np.array([Pr[i, cols.index(k)] if k in cols else 1e-9 for i, k in enumerate(Mte)])
        losses.append(-np.log2(np.clip(pm, 1e-9, 1)))
    L = np.array(losses)                                   # adversaries x held-out samples
    out = np.empty(L.shape[1])
    for sel, sco in ((folds[0], folds[1]), (folds[1], folds[0])):
        best = int(np.argmin(L[:, sel].mean(axis=1))); out[sco] = L[best, sco]
    return out

def folds_for(P):
    r = np.random.default_rng(12345); n = len(P["te"]); perm = r.permutation(n)
    return perm[: n // 2], perm[n // 2:]

def paired(lR, lA):
    d = lR - lA; r = np.random.default_rng(0); n = len(d)
    return float(d.mean()), float(np.std([d[r.integers(0, n, n)].mean() for _ in range(200)])), float(lR.mean()), float(lA.mean())

def view_S(P, Hm):
    return P["Ts"] @ Hm.T + math.sqrt(ob.TAU2) * np.random.default_rng(5).normal(size=(len(P["Ts"]), Hm.shape[0]))

def remeasure(rows, sets, setup, with_eq=False):
    out, cache = [], {}
    for row in rows:
        d = sets[row["dataset"]]; key = (row["dataset"], row["view"])
        if key not in cache:
            P, Sig, m, F, B, b_R, Hm, AS = setup(d, row["view"]); S = view_S(P, Hm); fo = folds_for(P)
            lR = per_sample_losses(ob.encode(P, b_R, P["tr"]), ob.encode(P, b_R, P["te"]), S, P, fo)
            lRe = per_sample_losses(sc.encode_eq(P, b_R, P["tr"]), sc.encode_eq(P, b_R, P["te"]), S, P, fo) if with_eq else None
            cache[key] = (P, S, fo, lR, lRe)
        P, S, fo, lR, lRe = cache[key]; b = np.array(row["b_aware"])
        lA = per_sample_losses(ob.encode(P, b, P["tr"]), ob.encode(P, b, P["te"]), S, P, fo)
        rem, se, mR, mA = paired(lR, lA)
        o = dict(row, measured_removed=rem, se=se, leak_principal=mR, leak_aware=mA, protocol="crossfit-paired")
        if with_eq:
            lAe = per_sample_losses(sc.encode_eq(P, b, P["tr"]), sc.encode_eq(P, b, P["te"]), S, P, fo)
            o["measured_removed_eq"], o["se_eq"], _, _ = paired(lRe, lAe)
        out.append(o)
        print(f"{row['dataset']:16s} {row['view']:>18s} f={row['f']:.2f} pred {row['pred_removed']:+.3f} "
              f"meas {rem:+.3f} +- {se:.3f}", flush=True)
    return out

def setup_main(d, vname): return ob.setup(d, dict(ob.views_for(d))[vname])

if __name__ == "__main__":
    part = sys.argv[1]
    if part == "boundary":
        rows = json.load(open("boundary_predictions.json"))["rows"]
        sets = {d["name"]: d for d in ob.DATA + ob.synthetic_sets()}
        json.dump(remeasure(rows, sets, setup_main), open("boundary_measured_crossfit.json", "w"), indent=1)
    elif part == "fresh":
        rows = json.load(open("gauss_predictions.json"))["fresh_boundary_rows"]
        fresh = [f() for f in og.FRESH_LOADERS] + [og.warped_gauss8()]; ob.DATA = fresh
        sets = {d["name"]: d for d in fresh + ob.synthetic_sets()}
        json.dump(remeasure(rows, sets, setup_main), open("fresh_measured_crossfit.json", "w"), indent=1)
    elif part == "scope":
        rows = json.load(open("scope_predictions.json"))["rows"]
        sets = {d["name"]: d for d in [f() for f in sc.LOADERS] + sc.controls()}
        json.dump(remeasure(rows, sets, sc.setup_view, with_eq=True), open("scope_measured_crossfit.json", "w"), indent=1)
