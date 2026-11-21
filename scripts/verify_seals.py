#!/usr/bin/env python
"""Verify the content hash of every sealed prereg against its seal commit (CHARTER REG-1/REG-2;
PE-CLS-1.0 s3.2, s7.1). Read-only.

A sealed prereg is any tracked (or untracked, under prereg/) text file carrying a line
`hash: sha256:<64 hex>` and a GO-P registration ID (its `id:` line or its file name), anywhere in
the tree. For each one, its SEAL COMMIT is found from git, following renames: the earliest commit
in the file's history whose version carries a 64-hex seal. Then either

  * no entry in prereg/SEAL-DISCLOSURES.json: the seal commit's text must verify under
    scripts/seal.py's scheme, the current recorded hash must equal the seal commit's, the
    current file must verify whole, and the seal pattern must occur exactly once; or
  * an entry, whose facts are all re-derived from git and must match: the seal commit, the list
    of later commits touching the file, the recorded hash, the hash of the whole current file
    (so ANY later change, an appended amendment included, fails until it is disclosed), and the
    kind-specific check:

      appended              the first `sealed_lines` lines equal the seal-commit text and hash to
                            the recorded value;
      placeholder-replaced  the first `kept_lines` lines plus `placeholder` equal the seal-commit
                            text and hash to the recorded value with the hash line removed;
      harness-hash          the recorded value is the harness's sha256 at the seal commit; the
                            harness's later commits and current hash match; the governed result
                            commit lies between the seal commit and HEAD; the text is unchanged
                            since the seal commit;
      unexplained           the text is unchanged since the seal commit and still fails to verify;
      re-sealed             the seal-commit text verifies to `original_sha256`, the current file
                            verifies whole to a different recorded hash, and whether the file
                            records the original hash matches `prior_hash_in_file`.

Every path that ever held a sealed prereg in this branch's history must still exist (following
renames) or appear under "removed" with the commit that removed it. Entries that match no sealed
prereg, duplicate JSON keys, and an entry whose key is not its file's ID all fail. A shallow clone
fails, because every check needs history (CI checks out with fetch-depth 0). A sealed file with no
committed history (sealed, not yet committed) passes only if it verifies whole and has no entry.
Every entry must say what changed and where it was disclosed before (`what_changed`,
`previously_disclosed`), and every "removed" entry why (`reason`); a `TODO:` left in any of them
fails.

    python scripts/verify_seals.py
    python scripts/verify_seals.py --facts PATH [PATH ...]

--facts (read-only) prints, as JSON, the disclosure entry each named file needs: every fact git
determines is filled in, and the human-written fields are left as `TODO:`, which the check refuses.
It keeps the human-written fields of an existing entry, and marks `what_changed` `TODO:` again if
the facts have moved since. Commit an amendment before running it: the entry records the commits
that touched the file, so the manifest goes in the next commit, and both are pushed together.
For a deleted prereg it prints the "removed" entry instead.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "prereg" / "SEAL-DISCLOSURES.json"
ANY = re.compile(r"hash:\s*sha256:\S*")            # scripts/seal.py's own pattern
SEAL = re.compile(r"(?m)^hash:\s*sha256:([0-9a-f]{64})\b")
IDLINE = re.compile(r"(?m)^id:\s*(GO-P-\d{4}-\d{3})\b")
IDNAME = re.compile(r"(GO-P-\d{4}-\d{3})")
TEXT_EXT = (".md", ".markdown", ".txt", ".yaml", ".yml")
TODO = "TODO:"                                     # placeholder --facts leaves; the check refuses it
HUMAN = ("previously_disclosed", "what_changed", "governed_result_commit")
PYPATH = re.compile(r"[\w./-]+\.py\b")


def sealpy_digest(text: str) -> str:
    return hashlib.sha256(ANY.sub("hash: sha256:", text).encode("utf-8")).hexdigest()


def removed_digest(text: str) -> str:
    return hashlib.sha256(re.sub(r"(?m)^hash:\s*sha256:\S*\n", "", text).encode("utf-8")).hexdigest()


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, cwd=ROOT)


def out(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", "replace").replace("\r\n", "\n")


def show(commit: str, path: str) -> str | None:
    p = git("show", f"{commit}:{path}")
    return p.stdout.decode("utf-8").replace("\r\n", "\n") if p.returncode == 0 else None


def is_ancestor(a: str, b: str) -> bool:
    return git("merge-base", "--is-ancestor", a, b).returncode == 0


def history(path: str) -> list[tuple[str, str]]:
    """[(commit, path at that commit)] newest first, following renames."""
    res, cur = [], None
    for line in out("log", "--follow", "--format=\x01%h", "--name-only", "--", path).splitlines():
        if line.startswith("\x01"):
            cur = line[1:]
        elif line.strip() and cur:
            res.append((cur, line.strip())); cur = None
    return res


def derive(hist):
    """(seal commit, its text, its recorded hash, later commits oldest first), or None when no
    committed version carries a seal. The seal commit is the earliest version with a 64-hex seal."""
    sealed = [(c, p) for c, p in hist if SEAL.search(show(c, p) or "")]
    if not sealed:
        return None
    oc, op = sealed[-1]
    otext = show(oc, op)
    commits = [c for c, _ in hist]
    return oc, otext, SEAL.search(otext).group(1), commits[: commits.index(oc)][::-1]


def written(v) -> bool:
    """A human-written field: a non-empty string with no TODO placeholder left in it."""
    return isinstance(v, str) and bool(v.strip()) and TODO not in v


def no_dupes(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"duplicate key {k!r} in {MANIFEST.name}")
        d[k] = v
    return d


def prereg_log() -> list[tuple[str, list[list[str]]]]:
    """One pass over prereg/'s history, newest first: [(commit, [[status, path...], ...])]."""
    res, commit, changes = [], None, []
    for line in out("log", "-M", "--name-status", "--format=\x01%h", "--", "prereg").splitlines():
        if line.startswith("\x01"):
            if commit:
                res.append((commit, changes))
            commit, changes = line[1:], []
        elif line.strip():
            changes.append(line.split("\t"))
    if commit:
        res.append((commit, changes))
    return res


def histories(log, paths) -> dict[str, list[tuple[str, str]]]:
    """[(commit, path at that commit)] newest first for each current path, following renames
    within prereg/ (equivalent to `git log --follow` there, in one pass)."""
    res = {}
    for p in paths:
        name, h, created = p, [], False
        for commit, changes in log:                 # newest to oldest
            for ch in changes:
                st = ch[0][:1]
                if st == "R" and len(ch) == 3 and ch[2] == name:
                    h.append((commit, name))        # renamed into `name` here
                    name = ch[1]                    # older history is under the old name
                    break
                if st == "M" and len(ch) == 2 and ch[1] == name:
                    h.append((commit, name))
                    break
                if st == "A" and len(ch) == 2 and ch[1] == name:
                    h.append((commit, name))        # created here: nothing older
                    created = True
                    break
            if created:
                break
        res[p] = h
    return res


def sealed_paths_in_history(log) -> tuple[set[str], dict[str, str]]:
    """Every path under prereg/ that held a 64-hex seal when added or renamed into; rename map."""
    sealed, renames = set(), {}
    for commit, changes in log:
        for ch in changes:
            st = ch[0][:1]
            if st == "R" and len(ch) == 3:
                renames[ch[1]] = ch[2]; new = ch[2]
            elif st == "A" and len(ch) == 2:
                new = ch[1]
            else:
                continue
            t = show(commit, new)
            if t and SEAL.search(t):
                sealed.add(new)
    return sealed, renames


def main() -> int:
    problems: list[str] = []
    if out("rev-parse", "--is-shallow-repository").strip() != "false":
        print("verify_seals: FAIL -- shallow or missing git history; every check needs it "
              "(CI: actions/checkout with fetch-depth: 0)")
        return 1
    try:
        man = json.loads(MANIFEST.read_text(encoding="utf-8"), object_pairs_hook=no_dupes)
        entries, removed = man["entries"], man.get("removed", {})
    except Exception as e:                                  # missing, unparsable, duplicate keys
        print(f"verify_seals: FAIL -- cannot read {MANIFEST.name}: {e}")
        return 1

    tracked = [p for p in out("ls-files", "-z").split("\0") if p]
    tracked_set = set(tracked)
    untracked = [p for p in out("ls-files", "-z", "-o", "--exclude-standard", "--", "prereg").split("\0") if p]
    candidates = {}
    for p in tracked + untracked:
        if not p.lower().endswith(TEXT_EXT) or not (ROOT / p).is_file():
            continue
        try:
            text = (ROOT / p).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        m = SEAL.search(text)
        rid = IDLINE.search(text) or IDNAME.search(Path(p).name)
        if m and rid:
            candidates[p] = (rid.group(1), text, m.group(1))

    # 1. nothing sealed has gone missing
    log = prereg_log()
    ever, renames = sealed_paths_in_history(log)
    in_prereg = [p for p in candidates if p in tracked and p.startswith("prereg/")]
    hists = histories(log, in_prereg)
    for p in sorted(ever):
        q = p
        while q in renames:
            q = renames[q]
        if q in candidates and q in tracked_set:        # still sealed, still tracked
            continue
        if p in removed:
            r = removed[p]
            gone = out("log", "--diff-filter=D", "--format=%h", "--", p).split()
            if (ROOT / p).exists() or not gone or gone[0] != r.get("removed_by") \
                    or not (show(r.get("seal_commit", ""), p) or "") or not SEAL.search(show(r["seal_commit"], p)):
                problems.append(f"{p}: 'removed' entry does not match git (removed_by / seal_commit)")
            if not written(r.get("reason")):
                problems.append(f"{p}: 'removed' entry has no reason, or still a {TODO} placeholder")
            continue
        problems.append(f"{p}: a sealed prereg in history is missing or moved, with no 'removed' entry")
    for p in removed:
        if p not in ever:
            problems.append(f"{p}: 'removed' entry names a path that never held a sealed prereg")

    # 2. every sealed prereg
    by_file = {e.get("file"): k for k, e in entries.items()}
    seen = set()
    whole = disclosed = new = 0
    for path, (rid, text, rec) in sorted(candidates.items()):
        key = by_file.get(path)
        e = entries.get(key) if key else None
        if e is not None:
            seen.add(key)
            if key != rid:
                problems.append(f"{path}: entry key {key} is not the file's ID {rid}")
        hist = hists[path] if path in hists else (history(path) if path in tracked else [])
        d = derive(hist)
        verifies_whole = sealpy_digest(text) == rec
        if d is None:
            if e is None and verifies_whole and len(ANY.findall(text)) == 1 and path not in ever:
                new += 1
                print(f"  new (not yet committed)  {path}")
            else:
                problems.append(f"{path}: sealed but with no committed seal")
            continue
        oc, otext, orec, post = d

        if e is None:
            bad = []
            if sealpy_digest(otext) != orec:
                bad.append(f"its seal commit {oc} does not verify")
            if rec != orec:
                bad.append(f"recorded hash differs from the one sealed at {oc} (re-sealed?)")
            if not verifies_whole:
                bad.append("recorded hash does not verify over the file")
            if len(ANY.findall(text)) != 1:
                bad.append("more than one 'hash: sha256:' match (seal.py overwrites them all)")
            if bad:
                problems.append(f"{path}: " + "; ".join(bad) + " -- and no disclosure entry")
            else:
                whole += 1
            continue

        bad = []
        kind = e.get("kind")
        if e.get("seal_commit") != oc:
            bad.append(f"seal_commit {e.get('seal_commit')} is not the seal commit {oc}")
        if e.get("post_seal_commits") != post:
            bad.append(f"post_seal_commits {e.get('post_seal_commits')} != git {post}")
        if e.get("recorded_sha256") != rec:
            bad.append("recorded_sha256 differs from the file")
        if e.get("current_text_sha256") != sealpy_digest(text):
            bad.append("the file changed since its disclosure (current_text_sha256)")
        if kind != "re-sealed" and verifies_whole:
            bad.append("verifies whole: the entry is stale")
        for f in ("what_changed", "previously_disclosed"):
            if not written(e.get(f)):
                bad.append(f"{f} is missing, empty or still a {TODO} placeholder")
        if kind == "appended":
            head = "".join(text.splitlines(keepends=True)[: e.get("sealed_lines", 0)])
            if head != otext or sealpy_digest(head) != rec:
                bad.append(f"first {e.get('sealed_lines')} lines are not the sealed text")
        elif kind == "placeholder-replaced":
            head = "".join(text.splitlines(keepends=True)[: e.get("kept_lines", 0)]) + str(e.get("placeholder")) + "\n"
            if head != otext or removed_digest(head) != rec:
                bad.append("kept lines plus placeholder are not the sealed text")
        elif kind == "harness-hash":
            h = e.get("harness", "")
            hb = git("show", f"{oc}:{h}").stdout
            if hashlib.sha256(hb).hexdigest() != rec:
                bad.append("harness at the seal commit does not hash to the recorded value")
            hchg = out("log", "--format=%h", f"{oc}..HEAD", "--", h).split()[::-1]
            if e.get("harness_changed_after_seal") != hchg:
                bad.append(f"harness_changed_after_seal {e.get('harness_changed_after_seal')} != git {hchg}")
            hp = ROOT / h
            now = hashlib.sha256(hp.read_bytes().replace(b"\r\n", b"\n")).hexdigest() if hp.is_file() else None
            if now != e.get("harness_sha256_now"):
                bad.append("harness changed since the disclosure (harness_sha256_now)")
            g = e.get("governed_result_commit", "")
            if not (g and is_ancestor(oc, g) and is_ancestor(g, "HEAD")):
                bad.append("governed_result_commit is not between the seal commit and HEAD")
            if text != otext or sealpy_digest(otext) != e.get("text_sha256_at_seal"):
                bad.append("registration text changed since the seal commit")
        elif kind == "unexplained":
            if text != otext or sealpy_digest(otext) != e.get("text_sha256_at_seal"):
                bad.append("registration text changed since the seal commit")
        elif kind == "re-sealed":
            if sealpy_digest(otext) != orec or e.get("original_sha256") != orec:
                bad.append("original_sha256 is not the verifying hash at the seal commit")
            if not verifies_whole or rec == orec:
                bad.append("not a re-seal: the current hash must verify whole and differ from the original")
            if e.get("prior_hash_in_file") != (orec in text):
                bad.append("prior_hash_in_file does not match the file")
        else:
            bad.append(f"unknown kind {kind!r}")
        if bad:
            problems.append(f"{key}: " + "; ".join(bad))
        else:
            disclosed += 1
            print(f"  disclosed  {key}  {kind}")

    for k in sorted(set(entries) - seen):
        problems.append(f"{k}: entry matches no sealed prereg in the tree ({entries[k].get('file')})")

    print(f"verify_seals: {len(candidates)} sealed preregs; {whole} verify whole against their seal commit; "
          f"{disclosed} disclosed and checked; {new} new; {len(removed)} removed and accounted for "
          f"({MANIFEST.relative_to(ROOT).as_posix()})")
    for p in problems:
        print("  FAIL", p)
    print("verify_seals:", "FAIL" if problems else "PASS")
    return 1 if problems else 0


def harness_for(oc: str, otext: str, rec: str) -> str | None:
    """A .py path named in the sealed text whose blob at the seal commit hashes to `rec`."""
    for h in dict.fromkeys(PYPATH.findall(otext)):
        p = git("show", f"{oc}:{h}")
        if p.returncode == 0 and hashlib.sha256(p.stdout).hexdigest() == rec:
            return h
    return None


def facts(args: list[str]) -> int:
    """--facts: print the disclosure entries the named files need, as JSON. Read-only."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    def note(msg: str) -> None:
        print(f"  {msg}", file=sys.stderr)

    if not args:
        print("usage: verify_seals.py --facts PATH [PATH ...]", file=sys.stderr)
        return 2
    if out("rev-parse", "--is-shallow-repository").strip() != "false":
        print("verify_seals --facts: needs full git history", file=sys.stderr)
        return 1
    try:
        man = json.loads(MANIFEST.read_text(encoding="utf-8"), object_pairs_hook=no_dupes)
        entries, removed = man["entries"], man.get("removed", {})
    except Exception as e:
        print(f"verify_seals --facts: cannot read {MANIFEST.name}: {e}", file=sys.stderr)
        return 1
    by_file = {e.get("file"): k for k, e in entries.items()}
    tracked = {p for p in out("ls-files", "-z").split("\0") if p}
    log = prereg_log()
    new_entries: dict = {}
    new_removed: dict = {}
    rc = 0

    for arg in args:
        try:
            rel = (Path.cwd() / arg).resolve().relative_to(ROOT).as_posix()
        except ValueError:
            note(f"{arg}: not inside this repository"); rc = 1; continue
        path = ROOT / rel

        if not path.is_file():                              # deleted: a "removed" entry
            gone = out("log", "--diff-filter=D", "--format=%h", "--", rel).split()
            seals = [c for c in out("log", "--format=%h", "--", rel).split()
                     if SEAL.search(show(c, rel) or "")]
            if not gone or not seals:
                note(f"{rel}: no such file, and git shows no sealed prereg deleted there"); rc = 1; continue
            old = removed.get(rel, {})
            new_removed[rel] = {"seal_commit": seals[-1], "removed_by": gone[0],
                                "reason": old.get("reason") or f"{TODO} why it was removed, and where it went"}
            note(f"{rel}: deleted at {gone[0]}: needs a 'removed' entry"
                 + (" (it has one)" if old else ""))
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            note(f"{rel}: cannot read it: {e}"); rc = 1; continue
        m = SEAL.search(text)
        rid = IDLINE.search(text) or IDNAME.search(path.name)
        if not (m and rid):
            note(f"{rel}: not a sealed prereg (no 'hash: sha256:<64 hex>' line, or no GO-P ID)"); rc = 1; continue
        rid, rec = rid.group(1), m.group(1)
        hist = []
        if rel in tracked:
            hist = histories(log, [rel])[rel] if rel.startswith("prereg/") else history(rel)
        d = derive(hist)
        if d is None:
            note(f"{rel}: no committed version carries a seal: a new seal needs no entry if it verifies whole")
            continue
        if git("diff", "--quiet", "HEAD", "--", rel).returncode != 0:
            note(f"{rel}: has uncommitted changes. Commit the amendment first, then run --facts: "
                 "the entry records the commits that touched the file"); rc = 1; continue
        oc, otext, orec, post = d
        cur = sealpy_digest(text)
        key = by_file.get(rel)
        old = entries.get(key) if key else None
        if cur == rec == orec == sealpy_digest(otext) and len(ANY.findall(text)) == 1:
            note(f"{rel}: verifies whole against its seal commit {oc}: needs no entry"
                 + (f" (delete the stale entry {key})" if old else ""))
            continue

        e = {"file": rel, "kind": None, "seal_commit": oc, "recorded_sha256": rec,
             "post_seal_commits": post, "current_text_sha256": cur,
             "previously_disclosed": f"{TODO} where this was disclosed before the entry, or 'none'",
             "what_changed": f"{TODO} what changed after the seal, when, why, and in which commits"}
        lines, olines = text.splitlines(keepends=True), otext.splitlines(keepends=True)
        n = len(olines)
        if "".join(lines[:n]) == otext and sealpy_digest(otext) == rec:
            e.update(kind="appended", sealed_lines=n)
        elif cur == rec != orec == sealpy_digest(otext):
            e.update(kind="re-sealed", original_sha256=orec, prior_hash_in_file=orec in text)
        elif n and otext.endswith("\n") and "".join(lines[: n - 1]) == "".join(olines[:-1]) \
                and removed_digest(otext) == rec:
            e.update(kind="placeholder-replaced", scheme="hash-line-removed", kept_lines=n - 1,
                     placeholder=olines[-1][:-1])
        elif text == otext:
            h = harness_for(oc, otext, rec)
            if h:
                hp = ROOT / h
                e.update(kind="harness-hash", harness=h,
                         harness_changed_after_seal=out("log", "--format=%h", f"{oc}..HEAD", "--", h).split()[::-1],
                         harness_sha256_now=hashlib.sha256(hp.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
                         if hp.is_file() else None,
                         governed_result_commit=f"{TODO} the commit of the governed result")
            else:
                e["kind"] = f"{TODO} 'unexplained', once no cause can be found"
            e["text_sha256_at_seal"] = sealpy_digest(otext)
        else:
            e["kind"] = f"{TODO} none fits: the sealed text is not intact at the start of the file"
            note(f"{rel}: the sealed text is not intact at the start of the file. An edit inside the "
                 "sealed text cannot be disclosed by an entry alone: ask the author")

        if old is None:
            note(f"{rel}: needs an entry ({e['kind']}): replace every {TODO}, and add a note to its "
                 "row in claims/REGISTRY-ACCOUNTING.md")
        else:
            if str(e["kind"]).startswith(TODO) and old.get("kind") == "unexplained" and text == otext:
                e["kind"] = old["kind"]                     # a human judgement, kept
            for f in HUMAN:
                if f in e and f in old:
                    e[f] = old[f]
            moved = sorted(k for k in set(e) | set(old) if k not in HUMAN and e.get(k) != old.get(k))
            if moved:
                newc = [c for c in post if c not in old.get("post_seal_commits", [])]
                e["what_changed"] = (f"{old.get('what_changed', '')} {TODO} extend this for "
                                     f"{', '.join(newc) or 'the change'}").strip()
                note(f"{rel}: entry {key} is out of date ({', '.join(moved)}): extend what_changed, "
                     "and the note in its registry row")
            else:
                note(f"{rel}: entry {key} is current")
            if key != rid:
                note(f"{rel}: its entry is keyed {key}, but the file's ID is {rid}")
        new_entries[rid] = e

    print(json.dumps({"entries": new_entries, "removed": new_removed}, indent=2, ensure_ascii=False))
    print(f"verify_seals --facts: put each object under \"entries\" or \"removed\" in "
          f"{MANIFEST.relative_to(ROOT).as_posix()}, then run verify_seals.py", file=sys.stderr)
    return rc


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--facts":
        sys.exit(facts(sys.argv[2:]))
    if len(sys.argv) > 1:
        print("usage: verify_seals.py [--facts PATH [PATH ...]]", file=sys.stderr)
        sys.exit(2)
    sys.exit(main())
