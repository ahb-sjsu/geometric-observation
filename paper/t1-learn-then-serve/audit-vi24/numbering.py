"""Audit VI-24: the v3 -> v4 numbering map in the title footnote of T1 note v4.

Numbers every theorem-like environment (shared counter: theorem, proposition, lemma,
corollary, remark) in v3 (git: parent of 3b60d31) and v4 (working file), matches them by
title, and compares with the footnote's map. Read-only use of git.
"""
import re
import subprocess
import pathlib

here = pathlib.Path(__file__).resolve().parent
repo = here.parents[2]
v4 = (here.parent / "t1-learn-then-serve.tex").read_text(encoding="utf-8")
v3 = subprocess.run(["git", "-C", str(repo), "show", "3b60d31~1:paper/t1-learn-then-serve/t1-learn-then-serve.tex"],
                    capture_output=True, text=True, encoding="utf-8").stdout
pat = re.compile(r"\\begin\{(theorem|proposition|lemma|corollary|remark)\}(\[([^\]]*)\])?")


def envs(src):
    res = []
    for i, m in enumerate(pat.finditer(src), 1):
        title = (m.group(3) or "").replace("~", " ")
        title = re.sub(r"\\ref\{[^}]*\}", "#", title)
        res.append((i, m.group(1).capitalize(), title))
    return res


E3, E4 = envs(v3), envs(v4)
out = []
P = out.append
P("v3: " + "; ".join(f"{k} {i} [{t}]" for i, k, t in E3))
P("v4: " + "; ".join(f"{k} {i} [{t}]" for i, k, t in E4))
P("")
P("Matched by title (v3 -> v4):")
t4 = {t: (i, k) for i, k, t in E4}
mapping = {}
for i, k, t in E3:
    key = t
    if t not in t4:
        cand = [tt for tt in t4 if "noisy" in t.lower() and "noisy" in tt.lower()]
        P(f"  NOTE: v3 {k} {i} [{t}] was split in v4: its finite-difference part is Proposition 2 [Finite differences]")
        key = cand[0] if cand else None
    if key:
        mapping[(k, i)] = t4[key]
        P(f"  {k} {i} [{t}] -> {t4[key][1]} {t4[key][0]} [{key}]")
    else:
        P(f"  {k} {i} [{t}] -> (no v4 counterpart)")

foot = re.search(r"Numbering, version 3 to version 4:(.*?)\}\}", v4, re.S).group(1)
pairs = re.findall(r"(Lemma|Corollary|Theorem|Remark|Proposition)~(\d+)\s+is\s+(Lemma|Corollary|Theorem|Remark|Proposition)~(\d+)", foot)
P("")
P("Footnote's pairs checked against the matching:")
listed = set()
for k3, n3, k4, n4 in pairs:
    got = mapping.get((k3, int(n3)))
    ok = got == (int(n4), k4)
    listed.add((k3, int(n3)))
    P(f"  '{k3} {n3} is {k4} {n4}': {'correct' if ok else 'WRONG, matching gives ' + str(got)}")
P("v3 results missing from the footnote's map: " + ", ".join(f"{k} {i}->{mapping[(k, i)][1]} {mapping[(k, i)][0]}" for (k, i) in mapping if (k, i) not in listed))
nums4 = {}
for i, k, t in E4:
    nums4.setdefault(i, []).append(k)
clash = [(k, i) for (k, i) in mapping if (k, i) not in listed and mapping[(k, i)] != (i, k) and any(i == j for j, kk, _ in E4 if kk == k)]
P("v3 numbers that are reused in v4 by a different result of the same kind: "
  + ", ".join(f"{k} {i} (v3 '{[t for j, kk, t in E3 if j == i][0]}' vs v4 '{[t for j, kk, t in E4 if j == i][0]}')" for k, i in clash))

open(__file__.replace(".py", ".out.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
