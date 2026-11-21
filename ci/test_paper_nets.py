"""Fire test for ci/paper_nets.py: each pass rule must reject what it is meant to reject.

Builds throwaway scripts in a temporary directory and points paper_nets.ROOT at it, so it
runs in about a second and touches nothing in the repository. Prints ALL FIRE AS EXPECTED
on success and exits non-zero otherwise. Added 2026-11-20 (plan W1).
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper_nets  # noqa: E402

WRITE_JSON = """import json, sys
json.dump({FLAGS}, open("rec.json", "w"))
sys.exit({RC})
"""
CASES = []  # (name, script body, rule, committed JSON or None, expected pass)

def verdicts(name, committed, written, rc, expect):
    body = WRITE_JSON.replace("{FLAGS}", repr(written)).replace("{RC}", str(rc))
    CASES.append((name, body, "verdicts", committed, expect))

rec = {"a": {"checks": {"x": True, "y": False}}, "_meta": {"failed": 1}}
verdicts("verdicts reproduce, disclosed failure still failing", rec, rec, 1, True)
verdicts("a passing check now fails", rec,
         {"a": {"checks": {"x": False, "y": False}}, "_meta": {"failed": 2}}, 1, False)
verdicts("a disclosed failure now passes", rec,
         {"a": {"checks": {"x": True, "y": True}}, "_meta": {"failed": 0}}, 0, False)
verdicts("a check disappears", rec, {"a": {"checks": {"x": True}}, "_meta": {"failed": 1}}, 1, False)
CASES.append(("crash before writing (stale committed JSON must not pass)",
              "raise RuntimeError('boom')\n", "verdicts", rec, False))
CASES.append(("exits without writing", "import sys; sys.exit(0)\n", "verdicts", rec, False))
CASES.append(("committed JSON has no flags", WRITE_JSON.replace("{FLAGS}", "{}").replace("{RC}", "0"),
              "verdicts", {"_meta": {"seconds": 1}}, False))
CASES.append(("fails0 with FAILS: 0", "print('FAILS: 0')\n", "fails0", None, True))
CASES.append(("fails0 with FAILS: 1", "print('FAILS: 1')\n", "fails0", None, False))
CASES.append(("fails0 crash", "print('FAILS: 0'); raise SystemExit(2)\n", "fails0", None, False))
CASES.append(("allpass passes", "print('x'); print('ALL PASS')\n", "allpass", None, True))
CASES.append(("allpass with a FAIL last", "print('ALL PASS'); print('FAIL: z')\n", "allpass", None, False))
# A script that rewrites a JSON record beside itself under a non-verdicts rule (as the T1
# harnesses do): the run passes, and the committed record must be restored afterwards.
CASES.append(("allpass that rewrites a record beside it",
              "import json; json.dump({'x': 2}, open('side.json', 'w')); print('ALL PASS')\n",
              "allpass", None, True))


def main():
    bad = 0
    with tempfile.TemporaryDirectory() as root:
        paper_nets.ROOT = root
        os.makedirs(os.path.join(root, "p"))
        for i, (name, body, rule, committed, expect) in enumerate(CASES):
            script = f"p/s{i}.py"
            open(os.path.join(root, script), "w").write(body)
            jp = os.path.join(root, "p", "rec.json")
            side = os.path.join(root, "p", "side.json")
            json.dump({"x": 1}, open(side, "w"))          # a record beside the script
            if committed is not None:
                json.dump(committed, open(jp, "w"))
            got, msg = paper_nets.run_net(script, [], rule, "rec.json" if committed is not None else None, 60)
            restored = (committed is None or json.load(open(jp)) == committed) \
                and json.load(open(side)) == {"x": 1}
            ok = (got == expect) and restored
            bad += not ok
            print(f"  {'ok  ' if ok else 'MISS'} {name}: passed={got} (expected {expect})"
                  + ("" if restored else "; committed JSON NOT restored") + f" | {msg}")
            if os.path.exists(jp):
                os.remove(jp)
    print("ALL FIRE AS EXPECTED" if not bad else f"{bad} CASE(S) DID NOT FIRE AS EXPECTED")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
