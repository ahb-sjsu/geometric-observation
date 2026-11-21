#!/usr/bin/env python
"""Check the custody files that back `[proved]` ledger rows (CHARTER T-CUST-1).

A `[proved]` row needs four things: a complete written proof, a logged R-IND-5 pass, a
C3 harness that is committed, CI-run and built to fail, and a table of constants, slack
and known gaps. The proof is for people to judge; this script checks the accounting.

Each `claims/custody/<row>.md` file has these sections:

  # Custody: <ledger row ID>
  ## Claim                   one or two sentences, the row's scope
  ## Proof                   where the proof is (file and theorem labels)
  ## R-IND-5                 the VI rows that log its fresh-context passes, e.g. VI-16
  ## C3 harness              | Harness | Tier | CI section |
  ## Constants and slack     | Constant | Defined at | Proved bound | Measured | Source | Slack |
  ## Known gaps              a bullet list; "none" must be said explicitly

The checks:
  * every section is present, and the ledger row named in the title exists;
  * every VI-n cited under R-IND-5 is a row of the ledger's verification-incident table;
  * every harness exists; Tier is `re-run` (its file name must appear in ci/reproduce.py)
    or `committed-artifact` (it then needs a Source JSON below);
  * every Measured value with a JSON Source `path.json#key.path` matches the committed JSON:
    numbers to within half a unit in their last printed digit, or the stated `± tol`;
    anything else as an exact string. A JSON Source must name a key;
  * a Measured value whose Source is a text file (`.md`, `.txt`, `.tex`, `.log`), for
    harnesses that print rather than write JSON, must appear verbatim in that file; a sealed
    prereg's recorded outcome is such a file, and verify_seals.py guards its text;
  * no unresolved citation flag (`[C7]`, T-CUST-3) and no `TODO:` anywhere.

Usage:  python scripts/check_custody.py [--root DIR]
Exit 0 if every custody file passes (zero files passes), 1 otherwise."""
from __future__ import annotations

import json
import os
import re
import sys

SECTIONS = ("Claim", "Proof", "R-IND-5", "C3 harness", "Constants and slack", "Known gaps")
TIERS = ("re-run", "committed-artifact")
TEXT_SOURCES = (".md", ".txt", ".tex", ".log")
FLAG = re.compile(r"\[C\d+\]")
VI = re.compile(r"\bVI-\d+\b")
VI_RANGE = re.compile(r"\bVI-(\d+)\s*[–-]\s*VI-(\d+)\b")
NUM = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


def table(body: str) -> list[list[str]]:
    """Rows of the first markdown table in `body`, header and separator excluded."""
    rows = [l.strip() for l in body.splitlines() if l.strip().startswith("|")]
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    return [r for r in cells[2:] if any(r)]


def sections(text: str) -> dict[str, str]:
    out, name, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            if name is not None:
                out[name] = "\n".join(buf)
            name, buf = m.group(1), []
        elif name is not None:
            buf.append(line)
    if name is not None:
        out[name] = "\n".join(buf)
    return out


def ledger_ids(root: str) -> tuple[set[str], set[str]]:
    """(row IDs of claims/LEDGER.md, VI IDs that head a row of its incident table)."""
    rows, vis = set(), set()
    path = os.path.join(root, "claims", "LEDGER.md")
    for line in open(path, encoding="utf-8", errors="replace"):
        if not line.startswith("|"):
            continue
        first = line.strip().strip("|").split("|")[0].strip().strip("*").strip()
        if first:
            rows.add(first)
        vis.update(VI.findall(first))
        for a, b in VI_RANGE.findall(first):  # "VI-18 – VI-21" heads VI-18, 19, 20 and 21
            vis.update(f"VI-{n}" for n in range(int(a), int(b) + 1))
    return rows, vis


def resolve(obj, keypath: str):
    for part in keypath.split("."):
        if isinstance(obj, list):
            obj = obj[int(part)]
        elif isinstance(obj, dict) and part in obj:
            obj = obj[part]
        else:
            raise KeyError(part)
    return obj


def matches(written: str, actual) -> tuple[bool, str]:
    w = written.replace("−", "-").strip()
    tol = None
    if "±" in w:
        w, t = (s.strip() for s in w.split("±", 1))
        tol = float(t)
    if NUM.match(w) and isinstance(actual, (int, float)) and not isinstance(actual, bool):
        if tol is None:
            mant = w.lower().split("e")[0]
            decimals = len(mant.split(".")[1]) if "." in mant else 0
            exp = int(w.lower().split("e")[1]) if "e" in w.lower() else 0
            tol = 0.5 * 10.0 ** (exp - decimals)
        ok = abs(float(w) - float(actual)) <= tol * (1 + 1e-9)
        return ok, f"{w} vs {actual!r} (tol {tol:g})"
    ok = w == str(actual)
    return ok, f"{w!r} vs {str(actual)!r}"


def check_file(root: str, path: str, rows: set[str], vis: set[str], ci_text: str) -> list[str]:
    rel = os.path.relpath(path, root)
    text = open(path, encoding="utf-8").read()
    bad: list[str] = []
    m = re.search(r"^#\s+Custody:\s*(.+?)\s*$", text, re.M)
    if not m:
        return [f"{rel}: no '# Custody: <row>' title"]
    row = m.group(1)
    if row not in rows:
        bad.append(f"{rel}: ledger row {row!r} not found in claims/LEDGER.md")
    sec = sections(text)
    for s in SECTIONS:
        if s not in sec or not sec[s].strip():
            bad.append(f"{rel}: section '## {s}' is missing or empty")
    if FLAG.search(text):
        bad.append(f"{rel}: unresolved citation flag {FLAG.search(text).group(0)} (T-CUST-3)")
    if "TODO:" in text:
        bad.append(f"{rel}: a TODO: placeholder remains")
    cited = set(VI.findall(sec.get("R-IND-5", "")))
    if "R-IND-5" in sec and not cited:
        bad.append(f"{rel}: R-IND-5 cites no VI row")
    for v in sorted(cited - vis):
        bad.append(f"{rel}: {v} is not a row of the ledger's verification-incident table")
    sources = 0
    for r in table(sec.get("Constants and slack", "")):
        if len(r) < 6:
            bad.append(f"{rel}: constants row has {len(r)} cells, needs 6: {r}")
            continue
        name, measured, source = r[0], r[3], r[4].strip("` ")
        if not source or source in ("—", "-"):
            continue
        if source.lower().endswith(TEXT_SOURCES):
            full = os.path.join(root, source)
            if not os.path.isfile(full):
                bad.append(f"{rel}: {name}: Source file {source} does not exist")
                continue
            sources += 1
            if measured.strip("` ") not in open(full, encoding="utf-8", errors="replace").read():
                bad.append(f"{rel}: {name}: Measured {measured.strip('` ')!r} does not appear in {source}")
            continue
        if "#" not in source:
            bad.append(f"{rel}: {name}: Source {source!r} is not 'path.json#key.path' or a text file")
            continue
        fpath, key = source.split("#", 1)
        full = os.path.join(root, fpath)
        if not os.path.isfile(full):
            bad.append(f"{rel}: {name}: Source file {fpath} does not exist")
            continue
        try:
            actual = resolve(json.load(open(full, encoding="utf-8")), key)
        except (KeyError, IndexError, ValueError) as e:
            bad.append(f"{rel}: {name}: key {key!r} not found in {fpath} ({e})")
            continue
        sources += 1
        ok, how = matches(measured.strip("` "), actual)
        if not ok:
            bad.append(f"{rel}: {name}: Measured disagrees with {fpath}#{key}: {how}")
    harnesses = table(sec.get("C3 harness", ""))
    if "C3 harness" in sec and not harnesses:
        bad.append(f"{rel}: C3 harness table has no rows")
    for r in harnesses:
        if len(r) < 3:
            bad.append(f"{rel}: harness row has {len(r)} cells, needs 3: {r}")
            continue
        h, tier = r[0].strip("` "), r[1].strip("` ")
        if not os.path.isfile(os.path.join(root, h)):
            bad.append(f"{rel}: harness {h} does not exist")
        if tier not in TIERS:
            bad.append(f"{rel}: harness {h}: Tier {tier!r} is not one of {TIERS}")
        elif tier == "re-run" and os.path.basename(h) not in ci_text:
            bad.append(f"{rel}: harness {h} is tier re-run but ci/reproduce.py never runs it")
        elif tier == "committed-artifact" and sources == 0:
            bad.append(f"{rel}: harness {h} is committed-artifact but no constant cites its JSON")
    return bad


def main(argv: list[str]) -> int:
    root = argv[argv.index("--root") + 1] if "--root" in argv else \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rows, vis = ledger_ids(root)
    ci_text = open(os.path.join(root, "ci", "reproduce.py"), encoding="utf-8").read()
    d = os.path.join(root, "claims", "custody")
    files = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".md") and f != "README.md") \
        if os.path.isdir(d) else []
    problems = [p for f in files for p in check_file(root, f, rows, vis, ci_text)]
    for p in problems:
        print("  FAIL", p)
    print(f"check_custody: {len(files)} custody file(s); {len(problems)} problem(s)")
    print("check_custody:", "PASS" if not problems else "FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
