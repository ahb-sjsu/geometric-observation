#!/usr/bin/env python3
"""Debug-loop harness (v2): iterate generate -> run -> self-check -> feedback until the
candidate's OWN output satisfies the spec's stated success condition, or max_iters.

Feedback is fair: only the candidate's crash traceback or its own output measured against the
spec's success condition (the flip). It never reveals the hidden oracle (grade.py) or the
analytic read operator. The self-check instance (SELF) is deliberately DIFFERENT from the hidden
grading instance (M=16, -7deg, 4), so a model debugs against train-like signal and is scored
out-of-sample.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = (HERE / "spec_doa.md").read_text(encoding="utf-8")

# self-check instance (train-like; NOT the grading instance)
SELF = dict(M=12, theta0_deg=5.0, kappa=3.0,
            s0sq_list=[0.1, 0.03, 0.01, 0.003], n_trials=300, seed=1)

_RUN = (
    "import json,sys,numpy as np\n"
    "sys.path.insert(0, sys.argv[1])\n"
    "import impl\n"
    "r = impl.solve(**json.loads(sys.argv[2]))\n"
    "print('__R__' + json.dumps(r))\n"
)
SYS_PROMPT = ("You are an expert in array signal processing and numerical Python. Output ONLY one "
              "Python code block containing the complete impl.py with a solve(...) function exactly "
              "as specified. Pure numpy + stdlib, deterministic, no file/network access.")


def extract_code(text):
    blocks = re.findall(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return (max(blocks, key=len).strip() if blocks else text.strip())


def run_solve(cand_dir, params):
    try:
        proc = subprocess.run([sys.executable, "-c", _RUN, str(cand_dir), json.dumps(params)],
                              capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT (>300s): solve() is too slow — vectorize or reduce per-trial cost."
    if proc.returncode != 0:
        return None, "Runtime error (traceback):\n" + proc.stderr.strip()[-1500:]
    for line in proc.stdout.splitlines():
        if line.startswith("__R__"):
            return json.loads(line[5:]), None
    return None, "solve() returned no parseable result. stdout tail:\n" + proc.stdout[-500:]


def self_check(r, M, s0sqs):
    probs = []
    need = {"read_dir", "mse", "recon_energy", "omission_floor_mult", "shuffled_flip"}
    miss = need - set(r)
    if miss:
        return False, f"return dict is missing required keys: {sorted(miss)}"
    if len(r["read_dir"]) != 2 * M:
        probs.append(f"read_dir has length {len(r['read_dir'])}, but must be length 2*M = {2*M} "
                     f"(the [Re; Im] embedding of your informative direction w_hat).")
    for arm in ("invariant", "recon", "anti"):
        for k in ("mse", "recon_energy"):
            v = r[k].get(arm)
            if v is None or len(v) != len(s0sqs):
                probs.append(f"{k}['{arm}'] must be a list of length {len(s0sqs)} (one per s0sq).")
            elif any((x != x) or x in (float("inf"), float("-inf")) for x in v):
                probs.append(f"{k}['{arm}'] contains NaN/inf.")
    if not probs:
        mi, mr, ma = r["mse"]["invariant"], r["mse"]["recon"], r["mse"]["anti"]
        ri, rr, ra = r["recon_energy"]["invariant"], r["recon_energy"]["recon"], r["recon_energy"]["anti"]
        bad = [i for i in range(len(s0sqs))
               if not (mi[i] <= mr[i] <= ma[i] and rr[i] <= ri[i] and rr[i] <= ra[i])]
        if bad:
            probs.append(
                f"the flip does NOT hold at rate indices {bad}: at every rate you need angle "
                f"MSE invariant <= recon <= anti AND recon to have the smallest reconstruction "
                f"energy. If this fails, your informative direction w_hat is likely wrong (it is "
                f"NOT the signal subspace) or your arm variance allocation is off.")
    return (len(probs) == 0), "; ".join(probs)


def debug_loop(generate, out_dir, max_iters=4):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    messages = [{"role": "system", "content": SYS_PROMPT}, {"role": "user", "content": SPEC}]
    history = []
    for it in range(1, max_iters + 1):
        text = generate(messages)
        code = extract_code(text)
        (out_dir / "impl.py").write_text(code, encoding="utf-8")
        r, err = run_solve(out_dir, SELF)
        ok, fb = (False, err) if err else self_check(r, SELF["M"], SELF["s0sq_list"])
        history.append({"iter": it, "ok": ok, "feedback": fb, "code_len": len(code)})
        if ok:
            break
        messages.append({"role": "assistant", "content": text})
        messages.append({"role": "user", "content":
                         "Your impl.py has a problem. Running solve(M=12, theta0_deg=5, kappa=3, "
                         "s0sq_list=[0.1,0.03,0.01,0.003], n_trials=300, seed=1) gave:\n\n"
                         + fb + "\n\nFix it and return the COMPLETE corrected impl.py as one "
                         "python code block."})
    (out_dir / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    return history
