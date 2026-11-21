#!/usr/bin/env python
"""Fire test for Paper V's two C3 nets (CHARTER T-CUST-1: a net must be built to fail).

Paper V is `paper/consumer-relative-landauer.tex` (the rate-work-distortion region). Its
nets are sealed instruments and are never edited here:
  experiments/verify_consumer_landauer.py   (GO-P-2026-042; "CL" below)
  experiments/verify_gaussian_sideinfo.py   (GO-P-2026-044; "GS" below)

Method. Each mutation copies one harness to a temporary directory, replaces exact source
text with a wrong version of one claim (or of one check's threshold), runs the copy, and
reads its last line, "VERDICT: ALL PASS" or "VERDICT: FAIL: [tags]". The original files
are only read. Every replacement must match its source text the stated number of times,
or the mutation is refused before it runs.

  control  the unmutated copy must print ALL PASS.
  gate     a wrong version of a paper claim; the net must FAIL with the named tag.
           Gates are the evidence that a check can fail at all.
  probe    a shift ladder on a check whose power is not obvious (random-search nets,
           loose tolerances). Probes are recorded, not gated: they measure resolution,
           and the custody table reports it.

The verdict is controls_pass and gates_fire. A mutation that crashes, or prints no
VERDICT line, counts as not fired.

Numbering. The CL claims below use the CL harness's own section names, which predate the
paper's Section VI: CL's "Prop 3" is the paper's Proposition 5 (prop:thermal-waterfill)
and CL's "Prop 4" is Proposition 6 (prop:stale). The paper's Propositions 3 and 4
(prop:scalar-corner, prop:vector-frontier) are GS's subject. Every other number matches
the compiled paper.

What the mutations mean (~ marks a check that cannot fail for a mathematical reason, so
that its gate only shows the code path is live):
  CL1  Prop 2 converse: the closed-form lower boundary raised by s (probe s = 1e-3, 1e-2;
       gate s = 5e-2). Caught by the optimizer-driven support-line net.
  CL2  Prop 2 achievability: the closed form lowered by 1e-3 (not attained). Gate.
  CL3  Prop 2's matched-rate example: L = 0.9 claimed for the second code. Gate.
  CL4  Prop 1, eq. (20) wrong in its S-term, in the optimizer and in the check alike
       (factor 1/2). Probe: only optimality nets can see it.
  CL4b Prop 1, eq. (20) wrong in its marginal term (exponent alpha/2). Probe.
  CL5  Prop 1's convexity premise: probe -I(X;Xh|S) instead (concave). Gate.
  CL6a Thm 1 converse, boundary raised by 1e-3 at every D. Gate (the identity code sits
       on the D = 0 corner).
  CL6b Thm 1 converse, boundary raised by s only where D >= 0.05 (s = 1e-2, 5e-2, 0.1).
       Probe: power away from the corner.
  CL7  ~Thm 2: the description made randomized (hypothesis dropped). Gate.
  CL8  Cor 2: R_C(0) = H(X) claimed instead of H(U). Gate.
  CL9  Cor 3: total correlation's sign flipped (coordinated reset costs more). Gate.
  CL10 Cor 4: the optimal Gaussian rate claimed (1+s) times higher, seen only by the
       random-code net (s = 0.01, 0.05, 0.2). Probe.
  CL11 Cor 4: VI-4's bug, Sigma^-1 = Sx^-1 + lam P, in sigma_star. Gate.
  CL12 Prop 3: d_i* = min{lam_i, nu sqrt(T_i)} claimed. Gate.
  CL13 Prop 4: I(M;X_t), which decreases, put where H(M|X_t) is claimed to increase. Gate.
  CL14 Prop 4's binary example: q_t with (1-p)^t. Gate.
  GS1  scalar converse's LMMSE formula with rho for rho^2. Gate.
  GS2  scalar L bound with rho D for rho^2 D. Gate.
  GS3  quantizer net, both bounds raised by s (s = 0.01, 0.1, 0.3). Probe.
  GS4  single-curve identity with (1-rho) for (1-rho^2). Gate.
  GS5  discrete-corner net, analytic corner shifted by s (s = 0.05, 0.1). Probe.
  GS6  vector allocation: the quadratic's linear term with alpha/2. Gate.
  GS7  registered strict-frontier example made symmetric (both modes rho = 0.95):
       the claim then predicts no gap. Gate.
  GS8  separability net, per-mode envelope raised by s (s = 0.01, 0.05). Probe.
  GS9  side-information discount's limit claimed as log2(1/(1-rho^2)) (twice I(X;S)). Gate.

The kinds and the expected tags were fixed before the first run (2026-11-21).

History. Attempt 1 (2026-11-21, Atlas, 8 jobs, 1009 s) FAILED as executed: both controls
passed and 17 of 18 gates fired, but GS9 crashed. Its replacement text appended a comment
in the middle of a source line, which swallowed the line's "< 2e-3" and left a bool &= float
that raised a TypeError, so no VERDICT line was printed. That was a defect in this file, not
in the net. Its output is kept as results/PAPER5-fire-attempt1.json. For attempt 2, GS9's
replacement carries no comment, and mutate() refuses any replacement whose added comment
would not end at a line end. No other mutation, kind or expected tag changed.
(An earlier launch the same day was stopped by hand after about two minutes, before any
mutation had finished, to add the saving of the controls' output; it produced no results.)
Attempt 2 (2026-11-21, Atlas, 8 jobs, 1020 s) PASSED: controls pass, 18/18 gates, 9/17
probes. Every outcome but GS9's is identical to attempt 1, and the two controls' logs are
byte-identical across the attempts. Its output is results/PAPER5-fire.json.

What the probes found (the nets' resolution; the custody table carries it):
  CL1   Prop 2's support-line net catches a boundary raised by 1e-2 bits, not by 1e-3.
  CL4   a wrong eq. (20) is caught by the optimality nets (both variants).
  CL6b  Thm 1's finite-n converse net catches nothing away from the D = 0 corner, even a
        boundary raised by 0.1 bits where D >= 0.05: random codes at n <= 2 are far from
        the frontier. Its power is the corner alone (CL6a).
  CL10  Cor 4's random-code net catches a rate claimed 20% high, not 5%.
  GS3   the quantizer net catches bounds raised by 0.1 bits, not by 0.01.
  GS5   the discrete-corner net catches a shift of 0.1 bits, not 0.05 (its tolerance is
        0.06).
  GS8   the separability net catches an envelope raised by 0.01.

Usage:  python experiments/fire_paper5_nets.py [--jobs N] [--only ID,ID] [--no-write] [--check]
Writes results/PAPER5-fire.json and the two controls' output verbatim,
results/PAPER5-CL-control.log and results/PAPER5-GS-control.log (unless --no-write or
--only). MIT License."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CL = "experiments/verify_consumer_landauer.py"
GS = "experiments/verify_gaussian_sideinfo.py"
OUT = os.path.join(ROOT, "results", "PAPER5-fire.json")

VI4_BUG = '''def sigma_star(P, Dq, Cap):   # MUTATED: VI-4's bug, Sigma^-1 = Cap^-1 + lam P
    Ci = np.linalg.inv((Cap + Cap.T) / 2)
    S = lambda lam: np.linalg.inv(Ci + lam * P)
    if float(np.trace(P @ Cap)) <= Dq:
        return Cap
    lo, hi = 1e-12, 1e12
    for _ in range(300):
        mid = (lo * hi) ** 0.5
        if float(np.trace(P @ S(mid))) > Dq:
            lo = mid
        else:
            hi = mid
    return S((lo * hi) ** 0.5)

def waterfill_rate(lams, Dq):'''


def M(mid, harness, kind, expect, claim, edits):
    return {"id": mid, "harness": harness, "kind": kind, "expect": expect, "claim": claim,
            "edits": edits}


def ladder(prefix, harness, expect, claim, values, make, gate_at=None):
    return [M(f"{prefix}[{v:g}]", harness, "gate" if v == gate_at else "probe", expect,
              f"{claim} (s = {v:g})", make(v)) for v in values]


FG = "Fgrid = np.array([frontier(D, t) for t in tgrid])        # (R, L) rows"
FGRID = "    return np.stack([2.0 - h2v(t) - h2v(2 * D - t), 1.0 - h2v(2 * D - t)], axis=1)"
SQ = "(1 - alpha) * (psx @ np.log(np.maximum(qs, 1e-300)))"
RAND = "        if 0.5 * (logdet(Sx) - logdet(C)) / LOG2 < Rf - 1e-7:"
QZ = "    if R < Rmin(Dq) - 1e-9 or L < Lmin(Dq, rho) - 1e-9:"
CORNER = "    worst4 = max(worst4, abs(Rr - Rmin(D)), abs(Ll - Lmin(D, rho)))"
ENV = "    env = permode_env(alpha)"

MUTATIONS = (
    ladder("CL1", CL, "prop2-converse-violations", "Prop 2 boundary raised", (1e-3, 1e-2, 5e-2),
           lambda s: [(FG, f"Fgrid = np.array([frontier(D, t) for t in tgrid]) + {s!r}  # MUTATED", 1)],
           gate_at=5e-2)
    + [
        M("CL2", CL, "gate", "prop2-achievability", "Prop 2 closed form lowered by 1e-3",
          [("    return 2 - h2(t) - h2(2 * D - t), 1 - h2(2 * D - t)",
            "    return 2 - h2(t) - h2(2 * D - t) - 1e-3, 1 - h2(2 * D - t)  # MUTATED", 1)]),
        M("CL3", CL, "gate", "prop2-inversion", "Prop 2 example: L = 0.9 for the second code",
          [("and abs(L2 - 1.0) < 1e-12)", "and abs(L2 - 0.9) < 1e-12)  # MUTATED", 1)]),
        M("CL4", CL, "probe", "prop1-fixed-point", "eq. (20) S-term halved",
          [(SQ, "0.5 * " + SQ, 2)]),
        M("CL4b", CL, "probe", "prop1-fixed-point", "eq. (20) marginal exponent alpha/2",
          [("lq = alpha * np.log(np.maximum(qm, 1e-300))[None, :]",
            "lq = 0.5 * alpha * np.log(np.maximum(qm, 1e-300))[None, :]", 1),
           ("num = (qm[None, :] ** alpha)", "num = (qm[None, :] ** (0.5 * alpha))", 1)]),
        M("CL5", CL, "gate", "prop1-convexity-violations", "convexity probed on -I(X;Xh|S)",
          [("or Lm > 0.5 * (La + Lb) + 1e-10:", "or -Lm > -0.5 * (La + Lb) + 1e-10:  # MUTATED", 1)]),
        M("CL6a", CL, "gate", "thm1-converse-violations", "Thm 1 boundary raised by 1e-3",
          [(FGRID, FGRID + " + 1e-3  # MUTATED", 1)]),
    ]
    + ladder("CL6b", CL, "thm1-converse-violations", "Thm 1 boundary raised where D >= 0.05",
             (1e-2, 5e-2, 1e-1),
             lambda s: [(FGRID, FGRID + f" + {s!r} * (D >= 0.05)  # MUTATED", 1)])
    + [
        M("CL7", CL, "gate", "thm2-identity", "Thm 2 with a randomized description",
          [("        pam[r_ * K + fmap[r_], :] += pj[r_, :]",
            "        pam[r_ * K + fmap[r_], :] += 0.5 * pj[r_, :]  # MUTATED\n"
            "        pam[r_ * K + (fmap[r_] + 1) % K, :] += 0.5 * pj[r_, :]", 1)]),
        M("CL8", CL, "gate", "cor2-endpoints", "Cor 2: R_C(0) = H(X)",
          [("    HU = Hb(pu)\n", "    HU = Hb(pX)  # MUTATED\n", 1)]),
        M("CL9", CL, "gate", "cor3-total-correlation", "Cor 3: total correlation sign flipped",
          [("    tc = Hsum - Hjoint", "    tc = Hjoint - Hsum  # MUTATED", 1)]),
    ]
    + ladder("CL10", CL, "cor4-waterfilling", "Cor 4 rate claimed (1+s)x, random codes only",
             (0.01, 0.05, 0.2),
             lambda s: [(RAND, RAND.replace("< Rf - 1e-7", f"< Rf * {1 + s!r} - 1e-7"), 1)])
    + [
        M("CL11", CL, "gate", "cor4-waterfilling", "VI-4's bug in sigma_star",
          [("def waterfill_rate(lams, Dq):", VI4_BUG, 1)]),
        M("CL12", CL, "gate", "prop3-het-waterfilling", "Prop 3: d* = min{lam, nu sqrt(T)}",
          [("if float(np.minimum(lams, mid * Ts).sum()) < Dq:",
            "if float(np.minimum(lams, mid * np.sqrt(Ts)).sum()) < Dq:", 1),
           ("    dstar = np.minimum(lams, nu * Ts)", "    dstar = np.minimum(lams, nu * np.sqrt(Ts))", 1)]),
        M("CL13", CL, "gate", "prop4-monotonicity", "Prop 4 tested on I(M;X_t)",
          [("        Ls.append(Hb(J) - Hb(J.sum(0)))                   # H(M|X_t)",
            "        Ls.append(Hb(J.sum(1)) - (Hb(J) - Hb(J.sum(0))))  # MUTATED: I(M;X_t)", 1)]),
        M("CL14", CL, "gate", "prop4-binary", "Prop 4 example: q_t with (1-p)^t",
          [("    qt = 0.5 * (1 - (1 - 2 * p) ** t)", "    qt = 0.5 * (1 - (1 - p) ** t)  # MUTATED", 1)]),
        M("GS1", GS, "gate", "lmmse-algebra", "LMMSE formula with rho for rho^2",
          [("/ (v - rho * rho * c * c)\n", "/ (v - rho * c * c)  # MUTATED\n", 1)]),
        M("GS2", GS, "gate", "moment-minimum", "scalar L bound with rho D for rho^2 D",
          [("Lmin = lambda D, rho: 0.5 * np.log2(((1 - rho * rho) + rho * rho * D) / D)",
            "Lmin = lambda D, rho: 0.5 * np.log2(((1 - rho * rho) + rho * D) / D)  # MUTATED", 1)]),
    ]
    + ladder("GS3", GS, "quantizer-violations", "quantizer net, both bounds raised", (0.01, 0.1, 0.3),
             lambda s: [(QZ, QZ.replace("Rmin(Dq) - 1e-9", f"Rmin(Dq) + {s!r} - 1e-9")
                         .replace("Lmin(Dq, rho) - 1e-9", f"Lmin(Dq, rho) + {s!r} - 1e-9"), 1)])
    + [
        M("GS4", GS, "gate", "single-curve", "single-curve identity with (1-rho)",
          [("abs(L - 0.5 * np.log2(1 + (1 - rho * rho) * (2 ** (2 * R) - 1)))",
            "abs(L - 0.5 * np.log2(1 + (1 - rho) * (2 ** (2 * R) - 1)))", 1)]),
    ]
    + ladder("GS5", GS, "discrete-corner", "discrete-corner net, analytic corner shifted", (0.05, 0.1),
             lambda s: [(CORNER, f"    worst4 = max(worst4, abs(Rr - Rmin(D) - {s!r}), "
                                 f"abs(Ll - Lmin(D, rho) - {s!r}))  # MUTATED", 1)])
    + [
        M("GS6", GS, "gate", "vector-allocation", "vector quadratic's linear term with alpha/2",
          [("Bq = 2 * mu * p[i] * c[i] - alpha * rho2[i]",
            "Bq = 2 * mu * p[i] * c[i] - 0.5 * alpha * rho2[i]  # MUTATED", 1)]),
        M("GS7", GS, "gate", "strictness", "strict-frontier example made symmetric",
          [("rho2 = np.array([0.95 ** 2, 0.0])", "rho2 = np.array([0.95 ** 2, 0.95 ** 2])  # MUTATED", 1)]),
    ]
    + ladder("GS8", GS, "full-channel-separability", "separability envelope raised", (0.01, 0.05),
             lambda s: [(ENV, ENV + f" + {s!r}  # MUTATED", 1)])
    + [
        M("GS9", GS, "gate", "discount", "discount limit claimed as log2(1/(1-rho^2))",
          [("abs(disc[0] - 0.5 * np.log2(1 / (1 - rho * rho)))",
            "abs(disc[0] - np.log2(1 / (1 - rho * rho)))", 1)]),
    ]
)
CONTROLS = [M("CL0", CL, "control", None, "unmutated", []),
            M("GS0", GS, "control", None, "unmutated", [])]


def mutate(src: str, edits) -> str:
    for old, new, count in edits:
        n = src.count(old)
        if n != count:
            raise ValueError(f"expected {count} match(es), found {n}: {old[:70]!r}")
        # A comment added by the replacement must end at a line end, or it swallows the rest
        # of the source line (attempt 1's GS9 crashed that way).
        if "#" in new.split("\n")[-1] and "#" not in old.split("\n")[-1]:
            i = 0
            while (i := src.find(old, i)) >= 0:
                tail = src[i + len(old):i + len(old) + 1]
                if tail not in ("\n", ""):
                    raise ValueError(f"comment would swallow the line's tail: {old[:70]!r}")
                i += len(old)
        src = src.replace(old, new)
    return src


def run_one(m, sources, timeout):
    src = mutate(sources[m["harness"]], m["edits"])
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, os.path.basename(m["harness"]))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src)
        try:
            p = subprocess.run([sys.executable, "-I", path], cwd=tmp, env=env,
                               capture_output=True, text=True, timeout=timeout)
            out, rc = p.stdout, p.returncode
            err = p.stderr.strip().splitlines()[-3:]
        except subprocess.TimeoutExpired:
            out, rc, err = "", None, ["timeout"]
    lines = [l for l in out.splitlines() if l.startswith("VERDICT:")]
    verdict = lines[-1][len("VERDICT:"):].strip() if lines else None
    tags = []
    if verdict and verdict.startswith("FAIL:"):
        try:
            tags = list(ast.literal_eval(verdict[len("FAIL:"):].strip()))
        except (ValueError, SyntaxError):
            tags = [verdict]
    if m["kind"] == "control":
        ok = verdict == "ALL PASS"
    else:
        ok = any(str(t).startswith(m["expect"]) for t in tags)
    rec = {k: m[k] for k in ("id", "harness", "kind", "expect", "claim")}
    rec.update({"fired" if m["kind"] != "control" else "passed": ok, "verdict": verdict,
                "tags": tags, "returncode": rc, "seconds": round(time.time() - t0, 1)})
    if verdict is None:
        rec["stderr_tail"] = err
    if m["kind"] == "control":
        rec["stdout"] = out
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--check", action="store_true", help="validate the edits only; run nothing")
    a = ap.parse_args()
    sources, sha = {}, {}
    for h in (CL, GS):
        raw = open(os.path.join(ROOT, h), "rb").read()
        sha[h] = hashlib.sha256(raw).hexdigest()
        sources[h] = raw.decode("utf-8").replace("\r\n", "\n")
    todo = list(CONTROLS + MUTATIONS)
    if a.only:
        keep = set(a.only.split(","))
        todo = [m for m in todo if m["id"] in keep or m["id"].split("[")[0] in keep]
    for m in todo:                      # refuse a stale mutation before anything runs
        mutate(sources[m["harness"]], m["edits"])
    if a.check:
        for m in todo:
            print(f"  {m['id']:12s} {m['kind']:7s} {os.path.basename(m['harness']):30s} {m['claim']}")
        print(f"{len(todo)} runs; every edit matches its source text")
        return
    todo.sort(key=lambda m: m["harness"] != GS)        # the slow harness first
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        recs = list(ex.map(lambda m: run_one(m, sources, a.timeout), todo))
    order = {m["id"]: i for i, m in enumerate(CONTROLS + MUTATIONS)}
    recs.sort(key=lambda r: order[r["id"]])
    for r in recs:
        flag = r.get("passed", r.get("fired"))
        print(f"  {r['id']:12s} {r['kind']:7s} {'FIRED ' if r['kind'] != 'control' and flag else ''}"
              f"{'ok' if flag else 'NO'}  {r['seconds']:7.1f}s  {r['claim']}  -> {r['verdict']}")
    controls = [r for r in recs if r["kind"] == "control"]
    gates = [r for r in recs if r["kind"] == "gate"]
    verdict = {"controls_pass": all(r["passed"] for r in controls) and len(controls) == 2,
               "gates_fire": all(r["fired"] for r in gates) and len(gates) > 0}
    res = {
        "_meta": {"script": "experiments/fire_paper5_nets.py", "harness_sha256": sha,
                  "python": platform.python_version(), "numpy": _numpy_version(),
                  "platform": platform.platform(), "jobs": a.jobs,
                  "wall_seconds": round(time.time() - t0, 1),
                  "date": time.strftime("%Y-%m-%d")},
        "controls": [r for r in recs if r["kind"] == "control"],
        "mutations": [r for r in recs if r["kind"] != "control"],
        "counts": {"gates": len(gates), "gates_fired": sum(r["fired"] for r in gates),
                   "probes": sum(r["kind"] == "probe" for r in recs),
                   "probes_fired": sum(r.get("fired", False) for r in recs if r["kind"] == "probe")},
        "verdict": verdict,
        "PAPER5FIRE_supported": all(verdict.values()),
    }
    print(f"\ngates fired {res['counts']['gates_fired']}/{res['counts']['gates']}; probes fired "
          f"{res['counts']['probes_fired']}/{res['counts']['probes']}; controls "
          f"{'pass' if verdict['controls_pass'] else 'FAIL'}; {res['_meta']['wall_seconds']} s")
    if not a.no_write and not a.only:
        logs = {}
        for r in res["controls"]:       # the unmutated runs' output, verbatim: custody cites it
            name = f"PAPER5-{r['id'][:2]}-control.log"
            with open(os.path.join(ROOT, "results", name), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(r["stdout"])
            logs[name] = hashlib.sha256(r["stdout"].encode("utf-8")).hexdigest()
        res["_meta"]["control_logs_sha256"] = logs
    for r in res["controls"]:
        r.pop("stdout", None)
    if not a.no_write and not a.only:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
            fh.write("\n")
    print("ALL PASS" if res["PAPER5FIRE_supported"] else "FAIL")
    sys.exit(0 if res["PAPER5FIRE_supported"] else 1)


def _numpy_version():
    try:
        import numpy
        return numpy.__version__
    except ImportError:
        return None


if __name__ == "__main__":
    main()
