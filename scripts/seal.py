#!/usr/bin/env python
"""Seal a prereg entry: write sha256 of its body (with the hash line blanked).

The content hash is a tamper-evidence commitment; the *binding* registration
timestamp is the git commit. Usage: python scripts/seal.py prereg/GO-P-....md

The file must contain the pattern exactly once. The pattern also matches inside
any other `*hash: sha256:` field (a `code_hash:` line, say), and sealing would
overwrite that field with this digest; 039 and 041 had to be sealed by hand for
that reason. So a second match is refused, and so is a lone match that is not a
`hash:` line at the start of a line (added 2026-11-19, VI-25): name other hashes
`code_sha256:` or list them under `instruments_sha256:`. The digest scheme is
unchanged, so every existing seal still verifies (scripts/verify_seals.py).
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

_HASH_RE = re.compile(r"hash:\s*sha256:\S*")


def seal(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    n = len(_HASH_RE.findall(text))
    if n == 0:
        raise SystemExit(f"{path}: no 'hash: sha256:...' line to seal")
    if n > 1:
        raise SystemExit(f"{path}: {n} matches of 'hash: sha256:' -- sealing would overwrite every one; "
                         "rename the other hash fields (e.g. code_sha256:) and keep one seal line")
    if not re.search(r"(?m)^hash:\s*sha256:", text):
        raise SystemExit(f"{path}: the only match is not a 'hash:' line at the start of a line "
                         "(a code_hash: field, say); sealing would overwrite it")
    blanked = _HASH_RE.sub("hash: sha256:", text)
    digest = hashlib.sha256(blanked.encode("utf-8")).hexdigest()
    path.write_text(_HASH_RE.sub(f"hash: sha256:{digest}", text), encoding="utf-8")
    return digest


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/seal.py <prereg-entry.md>")
    p = Path(sys.argv[1])
    print(f"sealed {p.name}: sha256:{seal(p)}")
