"""The papers' own numerical nets (RLD series and the T1 note), for ci/reproduce.py.

Each script lives beside its paper (paper/tit-*/, paper/t1-learn-then-serve/), runs with
that directory as its working directory, and signals its result in one of three ways,
which is why they need a wrapper (plan W1, 2026-11-20):

  "fails0"   prints "FAILS: n" and exits 0 either way (RLD-I): pass iff "FAILS: 0".
  "allpass"  prints "ALL PASS" or "FAIL: ..." and exits 0 either way (T1): pass iff the
             last line is "ALL PASS".
  "verdicts" writes a JSON beside itself with per-check "ok" flags and exits 1 on a
             failed check (RLD-II to IV): pass iff every per-check flag reproduces the
             COMMITTED JSON exactly. A disclosed first-run failure (the papers' appendices
             state each one) must therefore stay failed, and any new failure fails CI.

Tiers, from timings on Atlas (4 BLAS threads, 2026-11-20; atlas:~/go-ci/timings.txt):
  "push"     <= ~40 s each: re-run on every push, sharded with the rest of Tier-A.
  "weekly"   heavy (75 s to 14 min each): re-run by the scheduled workflow
             .github/workflows/weekly-paper-nets.yml.
  verify_iir_holder.py (RLD-IV) did not finish in an hour and is carried as a committed
  artifact only; it is not listed.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (script relative to ROOT, extra args, pass rule, committed JSON beside it or None, tier)
PAPER_NETS = [
    # RLD-I, paper/tit-rate-leakage (five need cvxpy)
    ("paper/tit-rate-leakage/verify_commuting.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_decbounds.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_decsi_identities.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_fixed_read.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_lowdist.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_mm.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_scalar_path.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_tilted.py", [], "fails0", None, "push"),
    ("paper/tit-rate-leakage/verify_decoder_si.py", [], "fails0", None, "weekly"),
    # RLD-II, paper/tit-stationary
    ("paper/tit-stationary/verify_filter_chains.py", [], "verdicts", "verify_filter_chains.json", "push"),
    ("paper/tit-stationary/verify_iir.py", [], "verdicts", "verify_iir.json", "push"),
    ("paper/tit-stationary/verify_whole.py", [], "verdicts", "verify_whole.json", "push"),
    ("paper/tit-stationary/verify_achievability.py", [], "verdicts", "verify_achievability.json", "weekly"),
    ("paper/tit-stationary/verify_filter.py", [], "verdicts", "verify_filter.json", "weekly"),
    ("paper/tit-stationary/verify_filter_colored.py", [], "verdicts", "verify_filter_colored.json", "weekly"),
    ("paper/tit-stationary/verify_filter_lemma.py", [], "verdicts", "verify_filter_lemma.json", "weekly"),
    ("paper/tit-stationary/verify_spectral.py", [], "verdicts", "verify_spectral.json", "weekly"),
    ("paper/tit-stationary/verify_windows.py", [], "verdicts", "verify_windows.json", "weekly"),
    # RLD-III, paper/tit-beyond-stationary
    ("paper/tit-beyond-stationary/verify_unstable.py", [], "verdicts", "verify_unstable.json", "push"),
    ("paper/tit-beyond-stationary/verify_nongauss.py", [], "verdicts", "verify_nongauss.json", "weekly"),
    ("paper/tit-beyond-stationary/verify_cyclo.py", [], "verdicts", "verify_cyclo.json", "weekly"),
    ("paper/tit-beyond-stationary/verify_ls.py", [], "verdicts", "verify_ls.json", "weekly"),
    # RLD-IV, paper/tit-unstable-ergodic
    ("paper/tit-unstable-ergodic/verify_spectral_law.py", [], "verdicts", "verify_spectral_law.json", "push"),
    ("paper/tit-unstable-ergodic/verify_unit_circle.py", [], "verdicts", "verify_unit_circle.json", "weekly"),
    ("paper/tit-unstable-ergodic/verify_ergodic_memory.py", [], "verdicts", "verify_ergodic_memory.json", "weekly"),
    ("paper/tit-unstable-ergodic/verify_unstable_vector.py", [], "verdicts", "verify_unstable_vector.json", "weekly"),
    # verify_vector_ergodic: the pass of record is its --followup mode (criteria written
    # before it ran; the default mode's first-run criteria were too tight, as disclosed).
    ("paper/tit-unstable-ergodic/verify_vector_ergodic.py", ["--followup"], "verdicts",
     "verify_vector_ergodic_followup.json", "weekly"),
    # T1 note, paper/t1-learn-then-serve
    ("paper/t1-learn-then-serve/verify_t1_v4.py", [], "allpass", None, "weekly"),
    ("paper/t1-learn-then-serve/verify_t1_v3.py", [], "allpass", None, "weekly"),
]


def ok_flags(obj, path=""):
    """Every boolean leaf in the JSON by its path (the scripts record per-check results as
    'ok'/'pass' keys or as entries of a 'checks' dict; configuration booleans are constant
    and compare equal), plus the recorded failure count under '_meta/failed'."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}/{k}"
            if isinstance(v, bool):
                out[p] = v
            elif p == "/_meta/failed" and isinstance(v, (int, list)):
                out[p] = v if isinstance(v, int) else len(v)
            else:
                out.update(ok_flags(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(ok_flags(v, f"{path}[{i}]"))
    return out


def run_net(script, args, rule, json_name, timeout):
    """Run one paper net, leaving every JSON in its folder as it found it (some scripts,
    the T1 harnesses among them, rewrite JSON records beside themselves whatever their
    pass rule). Returns (passed, one-line summary)."""
    here = os.path.join(ROOT, os.path.dirname(script))
    snapshot = {f: open(os.path.join(here, f), "rb").read()
                for f in os.listdir(here) if f.endswith(".json")}
    try:
        return _run_net(script, args, rule, json_name, timeout)
    finally:
        for f, data in snapshot.items():
            p = os.path.join(here, f)
            if not os.path.isfile(p) or open(p, "rb").read() != data:
                with open(p, "wb") as fh:
                    fh.write(data)


def _run_net(script, args, rule, json_name, timeout):
    """Run one paper net. Returns (passed, one-line summary).

    For "verdicts", the committed JSON is moved aside before the run, so a script that
    crashes before writing cannot be compared with the committed record itself; the run
    must write a fresh file, and the committed record is restored afterwards in every case,
    so a local run leaves the working tree as it found it."""
    here = os.path.join(ROOT, os.path.dirname(script))
    cmd = [sys.executable, os.path.basename(script)] + args
    if rule in ("fails0", "allpass"):
        t0 = time.monotonic()
        p = subprocess.run(cmd, cwd=here, capture_output=True, text=True, timeout=timeout)
        secs = time.monotonic() - t0
        lines = [l.strip() for l in p.stdout.splitlines() if l.strip()]
        if rule == "fails0":
            good = "FAILS: 0" in lines and p.returncode == 0
            return good, f"[{secs:6.1f} s] {'FAILS: 0' if good else 'no FAILS: 0 line or nonzero exit'}"
        good = bool(lines) and lines[-1] == "ALL PASS" and p.returncode == 0
        return good, f"[{secs:6.1f} s] last line {lines[-1] if lines else '(none)'!r}"
    if rule != "verdicts":
        return False, f"unknown pass rule {rule!r}"
    jp = os.path.join(here, json_name)
    if not os.path.isfile(jp):
        return False, f"committed {json_name} is missing"
    original = open(jp, "rb").read()
    committed = ok_flags(json.loads(original.decode("utf-8")))
    if not committed:
        return False, f"committed {json_name} has no per-check flags"
    os.remove(jp)
    try:
        t0 = time.monotonic()
        p = subprocess.run(cmd, cwd=here, capture_output=True, text=True, timeout=timeout)
        secs = time.monotonic() - t0
        if "Traceback (most recent call last)" in p.stderr:
            return False, f"[{secs:6.1f} s] crashed: {p.stderr.strip().splitlines()[-1]}"
        if not os.path.isfile(jp):
            return False, f"[{secs:6.1f} s] wrote no fresh {json_name} (exit {p.returncode})"
        fresh = ok_flags(json.load(open(jp, encoding="utf-8")))
    finally:
        with open(jp, "wb") as fh:
            fh.write(original)
    diff = sorted(k for k in set(committed) | set(fresh) if committed.get(k) != fresh.get(k))
    failed = sorted(k for k, v in fresh.items() if v is False and k != "/_meta/failed")
    msg = (f"[{secs:6.1f} s] {len(fresh)} per-check flags; "
           f"{'reproduce the committed record' if not diff else 'DIFFER: ' + ', '.join(diff[:4])}"
           + (f"; disclosed failures still failing: {len(failed)}" if failed and not diff else ""))
    return not diff, msg
