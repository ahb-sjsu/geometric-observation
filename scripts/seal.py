#!/usr/bin/env python
"""Seal a prereg entry: write sha256 of its body (with the hash line blanked).

The content hash is a tamper-evidence commitment; the *binding* registration
timestamp is the git commit. Usage: python scripts/seal.py prereg/GO-P-....md
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

_HASH_RE = re.compile(r"hash:\s*sha256:\S*")


def seal(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not _HASH_RE.search(text):
        raise SystemExit(f"{path}: no 'hash: sha256:...' line to seal")
    blanked = _HASH_RE.sub("hash: sha256:", text)
    digest = hashlib.sha256(blanked.encode("utf-8")).hexdigest()
    path.write_text(_HASH_RE.sub(f"hash: sha256:{digest}", text), encoding="utf-8")
    return digest


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/seal.py <prereg-entry.md>")
    p = Path(sys.argv[1])
    print(f"sealed {p.name}: sha256:{seal(p)}")
