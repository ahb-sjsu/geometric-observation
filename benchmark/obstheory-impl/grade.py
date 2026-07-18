#!/usr/bin/env python3
"""Grade an ObsTheory-Impl DOA candidate against the hidden oracle.

Usage: python grade.py <candidate_dir>   # dir must contain impl.py with solve(...)
Runs solve() in a subprocess (fixed held-out params), computes the analytic read
operator itself, and scores the five sealed criteria. Emits <candidate_dir>/score.json.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

# fixed held-out grading instance (matches GO-P-2026-031)
M = 16
THETA0_DEG = -7.0
KAPPA = 4.0
S0SQS = list(np.geomspace(1e-1, 1e-4, 6))
N_TRIALS = 2000
SEED = 20260718

COS_MIN = 0.99
RATIO_LO, RATIO_HI = 2.4, 6.4
OMIT_MIN = 100.0

_RUNNER = (
    "import json,sys,numpy as np\n"
    "sys.path.insert(0, sys.argv[1])\n"
    "import impl\n"
    "r = impl.solve(M={M}, theta0_deg={t}, kappa={k}, s0sq_list={s}, n_trials={n}, seed={seed})\n"
    "print('__RESULT__' + json.dumps(r))\n"
)


def analytic_ghat():
    m = np.arange(M)
    th = np.deg2rad(THETA0_DEG)
    a = np.exp(1j * np.pi * m * np.sin(th))
    da = a * (1j * np.pi * m * np.cos(th))
    g = da - a * (np.vdot(a, da) / np.vdot(a, a))
    v = np.concatenate([g.real, g.imag])
    return v / np.linalg.norm(v)


def run_candidate(cand_dir: Path):
    code = _RUNNER.format(M=M, t=THETA0_DEG, k=KAPPA, s=S0SQS, n=N_TRIALS, seed=SEED)
    proc = subprocess.run(
        [sys.executable, "-c", code, str(cand_dir)],
        capture_output=True, text=True, timeout=600,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"candidate crashed:\n{proc.stderr[-2000:]}")
    for line in proc.stdout.splitlines():
        if line.startswith("__RESULT__"):
            return json.loads(line[len("__RESULT__"):])
    raise RuntimeError(f"no __RESULT__ in output:\n{proc.stdout[-1000:]}\n{proc.stderr[-1000:]}")


def score(r):
    checks, detail = {}, {}
    ghat = analytic_ghat()
    w = np.asarray(r["read_dir"], float)
    w = w / (np.linalg.norm(w) + 1e-15)
    cos = abs(float(w @ ghat))
    checks["geometry_cos>0.99"] = cos > COS_MIN
    detail["cos_read_ghat"] = round(cos, 4)

    mi = np.asarray(r["mse"]["invariant"], float)
    mr = np.asarray(r["mse"]["recon"], float)
    ma = np.asarray(r["mse"]["anti"], float)
    ri = np.asarray(r["recon_energy"]["invariant"], float)
    rr = np.asarray(r["recon_energy"]["recon"], float)
    ra = np.asarray(r["recon_energy"]["anti"], float)
    flip = int(np.sum((mi <= mr) & (mr <= ma) & (rr <= ri) & (rr <= ra)))
    checks["flip_6of6"] = flip == len(S0SQS)
    detail["flip"] = f"{flip}/{len(S0SQS)}"

    r1 = float(np.median(mr / mi))
    r2 = float(np.median(ma / mr))
    checks["mse_ratio_band"] = (RATIO_LO <= r1 <= RATIO_HI) and (RATIO_LO <= r2 <= RATIO_HI)
    detail["mse_step_ratios"] = [round(r1, 2), round(r2, 2)]

    checks["shuffled_collapses"] = int(r["shuffled_flip"]) <= 1
    detail["shuffled_flip"] = int(r["shuffled_flip"])

    om = float(r["omission_floor_mult"])
    checks["omission_floor>=100x"] = om >= OMIT_MIN
    detail["omission_floor_mult"] = round(om, 1)

    return checks, detail


def main():
    cand_dir = Path(sys.argv[1])
    out = {"candidate": cand_dir.name}
    try:
        r = run_candidate(cand_dir)
        checks, detail = score(r)
        out["checks"] = checks
        out["detail"] = detail
        out["passed"] = sum(checks.values())
        out["total"] = len(checks)
        out["verdict"] = "ALL PASS" if all(checks.values()) else "PARTIAL/FAIL"
    except Exception as e:
        out["error"] = str(e)
        out["passed"], out["total"], out["verdict"] = 0, 5, "ERROR"
    (cand_dir / "score.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
