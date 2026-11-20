#!/usr/bin/env python
"""Drive scripts/verify_seals.py to FIRE (feedback rule: a validator's bugs fail open, so test the
arms that would report a cleaner state than it verified).

Clones this repository (full history, plus one shallow clone), applies one mutation per case to
the working tree and index (no commits), and asserts the verifier's exit code. The working copy's
verifier, seal.py and manifest are copied into the clone, so uncommitted edits to them are what is
tested. Cases include every fail-open path a fresh-context review found on 2026-11-19: re-seals,
a re-pointed seal_commit, deleted / un-tracked / moved / renamed preregs, later appends to a
disclosed file, unchecked manifest metadata, duplicate JSON keys and key/file mismatches.

    python scripts/test_verify_seals.py [workdir]
"""
import hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
WORK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="verify-seals-"))
NEW = ["scripts/verify_seals.py", "scripts/seal.py", "prereg/SEAL-DISCLOSURES.json"]
U = re.compile(r"hash:\s*sha256:\S*")


def sh(*a, cwd=None):
    return subprocess.run(a, capture_output=True, text=True, cwd=cwd)


def clone(name, depth=None):
    d = WORK / name
    args = ["git", "clone", "-q"] + (["--depth", str(depth)] if depth else []) + [SRC.as_uri(), str(d)]
    assert sh(*args).returncode == 0, "clone failed"
    return d


def reset(d):
    sh("git", "reset", "-q", "--hard", "HEAD", cwd=d)
    sh("git", "clean", "-fdq", "--", "prereg", cwd=d)
    for f in NEW:
        shutil.copy(SRC / f, d / f)


def verify(d):
    p = sh(sys.executable, "scripts/verify_seals.py", cwd=d)
    return p.returncode, p.stdout


def pf(d, n):
    return next((d / "prereg").glob(f"GO-P-2026-{n}-*.md"))


def rel(d, p):
    return p.relative_to(d).as_posix()


def edit(path, fn):
    t = path.read_text(encoding="utf-8"); path.write_text(fn(t), encoding="utf-8", newline="\n")


def man(d, fn):
    p = d / "prereg" / "SEAL-DISCLOSURES.json"
    m = json.loads(p.read_text(encoding="utf-8")); fn(m)
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")


def seal(d, path):
    return sh(sys.executable, "scripts/seal.py", str(path), cwd=d).returncode


def sealpy(t):
    return hashlib.sha256(U.sub("hash: sha256:", t).encode("utf-8")).hexdigest()


def new_prereg(d):
    p = d / "prereg" / "GO-P-2026-999-test.md"
    p.write_text("# test\nid: GO-P-2026-999\nhash: sha256:\n", encoding="utf-8", newline="\n")
    assert seal(d, p) == 0


def resealed_021(d):
    p = pf(d, "021"); edit(p, lambda t: t.replace("prediction", "predicti0n", 1)); assert seal(d, p) == 0


def repoint_055(d):
    p = pf(d, "055"); edit(p, lambda t: t.replace("\n", "\n\n", 1))
    head = sh("git", "rev-parse", "--short", "HEAD", cwd=d).stdout.strip()
    t = p.read_text(encoding="utf-8")
    man(d, lambda m: m["entries"]["GO-P-2026-055"].update(
        seal_commit=head, text_sha256_at_seal=sealpy(t), current_text_sha256=sealpy(t), post_seal_commits=[]))


def dup_key(d):
    p = d / "prereg" / "SEAL-DISCLOSURES.json"
    t = p.read_text(encoding="utf-8")
    entry = json.dumps(json.loads(t)["entries"]["GO-P-2026-035"])
    p.write_text(t.replace('"entries": {', '"entries": {\n    "GO-P-2026-035": ' + entry + ",", 1), encoding="utf-8")


def mv(d, n, dest):
    sh("git", "mv", rel(d, pf(d, n)), dest, cwd=d)


cases = [
    ("untouched clone passes", None, 0),
    ("a new, uncommitted sealed prereg passes as 'new'", new_prereg, 0),
    ("edit a sealed line of a whole-verifying prereg (021)",
     lambda d: edit(pf(d, "021"), lambda t: t.replace("prediction", "predicti0n", 1)), 1),
    ("append to a whole-verifying prereg (021)", lambda d: edit(pf(d, "021"), lambda t: t + "\n## Outcome\n"), 1),
    ("edit and RE-SEAL a whole-verifying prereg (021)", resealed_021, 1),
    ("edit inside the sealed prefix of an appended entry (035)",
     lambda d: edit(pf(d, "035"), lambda t: t.replace("\n", "\n ", 3)), 1),
    ("append 'bar lowered, re-scored CONFIRMED' to a disclosed file (034)",
     lambda d: edit(pf(d, "034"), lambda t: t + "\n## Amendment: bar lowered to 10%, re-scored CONFIRMED\n"), 1),
    ("edit a kept line of a placeholder-replaced entry (039)",
     lambda d: edit(pf(d, "039"), lambda t: t.replace("id: GO-P-2026-039", "id: GO-P-2026-039 ", 1)), 1),
    ("change the 090 harness again", lambda d: edit(d / "experiments/go16_verify_partition.py", lambda t: t + "\n#\n"), 1),
    ("change the 091 harness", lambda d: edit(d / "experiments/go16_discrete_twin.py", lambda t: t + "\n#\n"), 1),
    ("edit the unexplained 055 text", lambda d: edit(pf(d, "055"), lambda t: t + "\n"), 1),
    ("edit 055 and re-point its entry's seal_commit and hashes", repoint_055, 1),
    ("edit and re-seal an already re-sealed prereg (069)",
     lambda d: (edit(pf(d, "069"), lambda t: t.replace("\n", "\n\n", 1)), seal(d, pf(d, "069"))), 1),
    ("drop a manifest entry (074)", lambda d: man(d, lambda m: m["entries"].pop("GO-P-2026-074")), 1),
    ("add a stale entry for a whole-verifying file (021)",
     lambda d: man(d, lambda m: m["entries"].__setitem__("GO-P-2026-021", dict(
         m["entries"]["GO-P-2026-035"], file=rel(d, pf(d, "021"))))), 1),
    ("alter a recorded value in the manifest (036)",
     lambda d: man(d, lambda m: m["entries"]["GO-P-2026-036"].__setitem__("recorded_sha256", "0" * 64)), 1),
    ("garbage post_seal_commits (035)",
     lambda d: man(d, lambda m: m["entries"]["GO-P-2026-035"].__setitem__("post_seal_commits", ["deadbee"])), 1),
    ("duplicate JSON key hides an entry", dup_key, 1),
    ("entry key is not its file's ID (036 under 999)",
     lambda d: man(d, lambda m: m["entries"].__setitem__("GO-P-2026-999", m["entries"].pop("GO-P-2026-036"))), 1),
    ("entry for a file that does not exist",
     lambda d: man(d, lambda m: m["entries"].__setitem__("GO-P-2026-998", dict(
         m["entries"]["GO-P-2026-035"], file="prereg/GO-P-2026-998-none.md"))), 1),
    ("tamper with a 'removed' entry (087 removed_by)",
     lambda d: man(d, lambda m: next(iter(m["removed"].values())).__setitem__("removed_by", "0000000")), 1),
    ("blank a seal hash (021)",
     lambda d: edit(pf(d, "021"), lambda t: re.sub(r"(?m)^hash:\s*sha256:[0-9a-f]{64}", "hash: sha256:", t)), 1),
    ("indent the seal line (021)",
     lambda d: edit(pf(d, "021"), lambda t: re.sub(r"(?m)^hash:", " hash:", t)), 1),
    ("add a second 'hash: sha256:' field (021)",
     lambda d: edit(pf(d, "021"), lambda t: t.replace("\nhash: sha256:", "\ncode_hash: sha256:abc\nhash: sha256:", 1)), 1),
    ("git rm a sealed prereg (021)", lambda d: sh("git", "rm", "-q", rel(d, pf(d, "021")), cwd=d), 1),
    ("git rm --cached a sealed prereg, file left on disk (021)",
     lambda d: sh("git", "rm", "-q", "--cached", rel(d, pf(d, "021")), cwd=d), 1),
    ("move a sealed prereg into prereg/archive/ (021)",
     lambda d: ((d / "prereg/archive").mkdir(), mv(d, "021", "prereg/archive/x.md")), 1),
    ("rename a sealed prereg to DRAFT-GO-P-... (021)", lambda d: mv(d, "021", "prereg/DRAFT-GO-P-2026-021-x.md"), 1),
    ("rename a sealed prereg to .MD (021)", lambda d: mv(d, "021", "prereg/GO-P-2026-021-x.MD"), 1),
    ("rename a sealed prereg to a name with a space (021)", lambda d: mv(d, "021", "prereg/GO-P-2026-021 x.md"), 1),
    ("manifest missing", lambda d: (d / "prereg/SEAL-DISCLOSURES.json").unlink(), 1),
    ("manifest not valid JSON", lambda d: (d / "prereg/SEAL-DISCLOSURES.json").write_text("{", encoding="utf-8"), 1),
]
base = clone("base")
ok = True
for name, mut, want in cases:
    reset(base)
    if mut:
        mut(base)
    rc, outp = verify(base)
    good = rc == want
    ok &= good
    tail = [l for l in outp.splitlines() if "FAIL" in l][:1]
    print(f"{'ok ' if good else 'BAD'} want={want} got={rc}  {name}  {tail[0].strip()[:100] if tail else ''}")
shallow = clone("shallow", depth=1)
for f in NEW:
    shutil.copy(SRC / f, shallow / f)
rc, outp = verify(shallow)
print(f"{'ok ' if rc == 1 else 'BAD'} want=1 got={rc}  shallow clone refuses")
ok &= rc == 1
print("ALL FIRE AS EXPECTED" if ok else "SOME CASES WRONG")
sys.exit(0 if ok else 1)
