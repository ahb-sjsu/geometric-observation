#!/usr/bin/env python
"""Fire test for scripts/check_custody.py: every way a custody file can be wrong must FAIL.

Builds a small fixture repository in a temporary directory (a ledger with one claim row
and verification-incident rows, a ci/reproduce.py that runs one harness, two harness
files and a results JSON), checks that a correct custody file passes, then breaks it one
way at a time. Each broken case must exit 1; each valid variant must exit 0.

Usage:  python scripts/test_check_custody.py
Exit 0 iff every case behaves as expected."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check_custody.py")

LEDGER = """# Ledger
| ID | Claim | Class |
|---|---|---|
| ROW-X | A claim. | `[exploratory]` |
| **VI-1 (a pass)** | verifier | verdict |
| **VI-3 – VI-5 (merged passes)** | verifier | verdict |
"""
CI = 'REPRODUCIBLE = [("harness_ok.py", "S", "r.json", "flag")]\n'
RESULT = {"a": {"b": 0.12345, "list": [1, 2.5]}, "verdict": "ALL PASS", "big": 1.5e-7}

GOOD = """# Custody: ROW-X

## Claim
A claim, at its stated scope.

## Proof
paper/x.tex, Theorem 1.

## R-IND-5
VI-1, and the merged pass VI-4.

## C3 harness
| Harness | Tier | CI section |
|---|---|---|
| `experiments/harness_ok.py` | re-run | [2/3] |
| `experiments/harness_artifact.py` | committed-artifact | [3/3] |

## Constants and slack
| Constant | Defined at | Proved bound | Measured | Source | Slack |
|---|---|---|---|---|---|
| c1 | Thm 1, eq. (3) | c1 <= 0.2 | 0.1235 | `results/r.json#a.b` | 1.6x |
| c2 | Lemma 2 | c2 >= 2 | 2.5 | `results/r.json#a.list.1` | 1.25x |
| verdict | harness | ALL PASS | ALL PASS | `results/r.json#verdict` | n/a |
| tiny | Rem 3 | <= 1e-6 | 1.5e-7 | `results/r.json#big` | 6.7x |
| gap | Fact 2 | >= 0 | 0.0529 bits | `paper/record.md` | n/a |
| c3 | Prop 4 | exact | 1/3 | — | n/a |

## Known gaps
- The scope excludes the singular case.
"""


def build(root: str, custody: str | None) -> None:
    for d in ("claims/custody", "ci", "experiments", "results", "paper"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    open(os.path.join(root, "claims", "LEDGER.md"), "w", encoding="utf-8").write(LEDGER)
    open(os.path.join(root, "ci", "reproduce.py"), "w", encoding="utf-8").write(CI)
    for h in ("harness_ok.py", "harness_artifact.py"):
        open(os.path.join(root, "experiments", h), "w").write("print('net')\n")
    json.dump(RESULT, open(os.path.join(root, "results", "r.json"), "w"))
    open(os.path.join(root, "paper", "record.md"), "w", encoding="utf-8").write(
        "Outcome: the gap is 0.0529 bits at the governed seed.\n")
    if custody is not None:
        open(os.path.join(root, "claims", "custody", "ROW-X.md"), "w", encoding="utf-8").write(custody)


def run(custody: str | None) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as root:
        build(root, custody)
        p = subprocess.run([sys.executable, CHECK, "--root", root],
                           capture_output=True, encoding="utf-8")
        return p.returncode, p.stdout


def sub(old: str, new: str) -> str:
    assert GOOD.count(old) == 1, old
    return GOOD.replace(old, new)


CASES = [  # (name, custody text or None, expected exit code)
    ("a correct custody file", GOOD, 0),
    ("no custody files at all", None, 0),
    ("a stated tolerance that covers the gap", sub("| 0.1235 |", "| 0.1236 ± 0.0002 |"), 0),
    ("a section is missing (Known gaps)", sub("## Known gaps\n- The scope excludes the singular case.\n", ""), 1),
    ("a section is empty (Proof)", sub("paper/x.tex, Theorem 1.\n", ""), 1),
    ("the title names a row the ledger lacks", sub("# Custody: ROW-X", "# Custody: ROW-Y"), 1),
    ("R-IND-5 cites a VI row the ledger lacks", sub("VI-1, and", "VI-2, and"), 1),
    ("R-IND-5 cites no VI row at all", sub("VI-1, and the merged pass VI-4.", "a pass happened."), 1),
    ("a measured value disagrees with its JSON", sub("| 0.1235 |", "| 0.1236 |"), 1),
    ("a stated tolerance too small for the gap", sub("| 0.1235 |", "| 0.1236 ± 0.0001 |"), 1),
    ("a string value disagrees with its JSON", sub("| ALL PASS | ALL PASS |", "| ALL PASS | PASS |"), 1),
    ("a Source key that is not in the JSON", sub("r.json#a.b`", "r.json#a.c`"), 1),
    ("a Source file that does not exist", sub("`results/r.json#a.b`", "`results/q.json#a.b`"), 1),
    ("a JSON Source without #key", sub("`results/r.json#a.b`", "`results/r.json`"), 1),
    ("a text Source that lacks the measured value", sub("| 0.0529 bits |", "| 0.0530 bits |"), 1),
    ("a text Source file that does not exist", sub("`paper/record.md`", "`paper/missing.md`"), 1),
    ("a re-run harness that CI never runs", sub("harness_ok.py` | re-run", "harness_artifact.py` | re-run"), 1),
    ("a harness file that does not exist", sub("`experiments/harness_ok.py`", "`experiments/gone.py`"), 1),
    ("an unknown tier", sub("| re-run |", "| sometimes |"), 1),
    ("an unresolved [C7] citation flag", sub("Theorem 1.", "Theorem 1 [C7]."), 1),
    ("a TODO: placeholder", sub("- The scope excludes", "- TODO: the scope excludes"), 1),
]


def main() -> int:
    wrong = 0
    for name, text, want in CASES:
        rc, out = run(text)
        ok = rc == want
        wrong += not ok
        print(f"  {'ok  ' if ok else 'WRONG'} exit {rc} (want {want}): {name}")
        if not ok:
            print("    " + out.replace("\n", "\n    "))
    # A committed-artifact harness with no Source JSON at all must fail too.
    no_sources = GOOD.split("## Constants and slack")[0] + (
        "## Constants and slack\n| Constant | Defined at | Proved bound | Measured | Source | Slack |\n"
        "|---|---|---|---|---|---|\n| c3 | Prop 4 | exact | 1/3 | — | n/a |\n\n"
        "## Known gaps\n- none\n")
    rc, out = run(no_sources)
    ok = rc == 1
    wrong += not ok
    print(f"  {'ok  ' if ok else 'WRONG'} exit {rc} (want 1): a committed-artifact harness whose JSON no constant cites")
    total = len(CASES) + 1
    print(f"test_check_custody: {total - wrong}/{total} cases behave as expected")
    print("test_check_custody:", "ALL FIRE AS EXPECTED" if not wrong else "FAILURES")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
