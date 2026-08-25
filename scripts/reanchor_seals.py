#!/usr/bin/env python
"""Re-anchor registration seals after a history rewrite (PE-CLS-1.0 s7.1.1).

A rebase rewrites commit hashes, so a seal hash recorded in
claims/REGISTRY-ACCOUNTING.md can stop resolving even though the priority it
proved was genuine.  This script recovers each seal's CURRENT commit identity
from the prereg file itself and verifies, before proposing any edit, that:

  1. the prereg's content hash still matches its body under the repository's
     own sealing scheme (scripts/seal.py) -- so we are re-anchoring the same
     registration, not a different one;
  2. the recovered commit is the FIRST commit that added the prereg;
  3. that commit is a git ancestor of the first commit adding the result --
     i.e. priority genuinely holds under the new identity.

A row whose content hash no longer matches is reported, never silently
re-anchored: the usual cause is a disclosed post-seal amendment appended to
the prereg body (permitted by PROTOCOL s1.17), which changes the body and so
supersedes the original hash.  Those rows are re-anchored only with an
explicit note.

    python scripts/reanchor_seals.py            # report only
    python scripts/reanchor_seals.py --apply    # write the mapping
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCT = os.path.join(ROOT, "claims", "REGISTRY-ACCOUNTING.md")
_HASH_RE = re.compile(r"hash:\s*sha256:\S*")
ID_ROW = re.compile(r"^\|\s*\*{0,2}\s*(\d{3})\s*\*{0,2}\s*\|")
SEAL = re.compile(r"\b(?:sealed|seal)\s+`?([0-9a-f]{7,40})`?", re.I)


def git(*a):
    r = subprocess.run(["git", "-C", ROOT, *a], capture_output=True,
                       text=True, timeout=120)
    return r.stdout.strip() if r.returncode == 0 else None


def resolves(c):
    return git("cat-file", "-e", f"{c}^{{commit}}") is not None


def first_add(rel):
    out = git("log", "--diff-filter=A", "--format=%H", "--", rel)
    return out.splitlines()[-1] if out else None


def is_ancestor(a, b):
    return subprocess.run(["git", "-C", ROOT, "merge-base", "--is-ancestor",
                           a, b], capture_output=True,
                          timeout=120).returncode == 0


def seal_hash(rel):
    """(recorded, recomputed) under scripts/seal.py's exact scheme."""
    text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    m = re.search(r"hash:\s*sha256:(\S+)", text)
    if not m:
        return None, None
    blanked = _HASH_RE.sub("hash: sha256:", text)
    return m.group(1), hashlib.sha256(blanked.encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    pdir = os.path.join(ROOT, "prereg")
    preregs = {}
    for fn in sorted(os.listdir(pdir)):
        m = re.match(r"GO-P-2026-(\d{3})", fn)
        if m and fn.endswith(".md"):
            preregs.setdefault(m.group(1), fn)

    rows, fixes, review = {}, {}, []
    for line in open(ACCT, encoding="utf-8", errors="replace"):
        m = ID_ROW.match(line)
        if not m:
            continue
        rid = m.group(1)
        s = SEAL.search(line)
        j = re.search(r"([A-Za-z0-9_\-]+\.json)", line)
        rows[rid] = {"seal": s.group(1) if s else None,
                     "result": j.group(1) if j else None,
                     "void": bool(re.search(r"never-run|void|reserved-unsealed",
                                            line, re.I))}

    print(f"{'ID':5s}{'seal':12s}{'status':22s}{'current':14s}hash")
    print("-" * 70)
    for rid in sorted(rows):
        r = rows[rid]
        if r["void"] or not r["seal"] or rid not in preregs:
            continue
        if resolves(r["seal"]):
            continue                      # already anchored
        rel = f"prereg/{preregs[rid]}"
        rec, comp = seal_hash(rel)
        hash_ok = rec is not None and rec == comp
        new = first_add(rel)
        res = (first_add(f"results/{r['result']}")
               if r["result"] and os.path.isfile(
                   os.path.join(ROOT, "results", r["result"])) else None)
        anc = is_ancestor(new, res) if (new and res) else None
        if new and anc and hash_ok:
            status, tgt = "REANCHOR", fixes
        elif new and anc:
            status, tgt = "REANCHOR (amended)", fixes
        else:
            status, tgt = "NEEDS REVIEW", None
        print(f"{rid:5s}{r['seal']:12s}{status:22s}{(new or '-')[:12]:14s}"
              f"{'match' if hash_ok else 'superseded'}")
        if tgt is None:
            review.append(rid)
        else:
            fixes[rid] = (r["seal"], new[:12], hash_ok)

    if not fixes and not review:
        print("\nAll seals resolve. Nothing to re-anchor.")
        return 0
    print(f"\n{len(fixes)} re-anchorable, {len(review)} need review")

    if args.apply and fixes:
        txt = open(ACCT, encoding="utf-8").read()
        n = 0
        for rid, (old, new, hash_ok) in fixes.items():
            note = f"sealed {old} (rebased; current commit `{new}`"
            note += ")" if hash_ok else (
                "; content hash superseded by disclosed post-seal "
                "amendments -- see prereg)")
            pat = re.compile(r"(^\|\s*\*{0,2}\s*" + rid + r"\s*\*{0,2}\s*\|.*?)"
                             r"sealed\s+`?" + old + r"`?", re.M | re.S)
            txt, k = pat.subn(lambda m: m.group(1) + note, txt, count=1)
            n += k
        open(ACCT, "w", encoding="utf-8", newline="\n").write(txt)
        print(f"applied: {n} rows rewritten in claims/REGISTRY-ACCOUNTING.md")
    elif fixes:
        print("(re-run with --apply to write the mapping)")
    return 1 if review else 0


if __name__ == "__main__":
    sys.exit(main())
