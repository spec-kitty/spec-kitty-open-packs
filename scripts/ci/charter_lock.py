#!/usr/bin/env python3
"""Read and check ``charter.lock.yaml``, the one pin of the charter this repository validates against.

Standard library only, so a CI step reads the pin without installing anything::

    python3 scripts/ci/charter_lock.py commit        # the 40-hex commit
    python3 scripts/ci/charter_lock.py release_tag   # service-vX.Y.Z, or empty
    python3 scripts/ci/charter_lock.py jar_sha256    # 64-hex digest, or empty

The file is read fail-closed (exit 2, a message on stderr): ``commit`` must be 40 lowercase hex
characters, never a branch or a tag; ``release_tag`` is empty or ``service-vX.Y.Z[-pre]``;
``jar_sha256`` is empty or 64 lowercase hex characters; a release tag needs its digest and a digest its
release tag; no other key is allowed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LOCK_FILE = Path(__file__).resolve().parents[2] / "charter.lock.yaml"
KEYS = ("commit", "release_tag", "jar_sha256")
COMMIT = re.compile(r"[0-9a-f]{40}")
RELEASE_TAG = re.compile(r"service-v\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?")
SHA256 = re.compile(r"[0-9a-f]{64}")


class LockError(Exception):
    """The pin file is missing or malformed; nothing may be judged against it."""


def parse(text: str) -> dict[str, str]:
    """The ``key: value`` lines of the lock. A flat file: one scalar per key, ``#`` comments, optional quotes."""
    found: dict[str, str] = {}
    for number, raw in enumerate(text.splitlines(), start=1):
        line = re.sub(r"(^|\s)#.*$", "", raw).strip()
        if not line:
            continue
        key, separator, value = (part.strip() for part in line.partition(":"))
        if not separator or key not in KEYS:
            raise LockError(f"line {number}: expected one of {', '.join(KEYS)} as 'key: value', got {raw!r}")
        if key in found:
            raise LockError(f"line {number}: {key} is set twice")
        found[key] = value.strip("'\"")
    return found


def read(path: Path | None = None) -> dict[str, str]:
    """The checked pin: all three keys present as strings (empty when unset)."""
    path = path or LOCK_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise LockError(f"cannot read {path}: {error}") from error
    lock = parse(text)
    commit = lock.get("commit", "")
    if not COMMIT.fullmatch(commit):
        raise LockError(f"commit must be 40 lowercase hex characters (never a branch or a tag), got {commit!r}")
    tag, digest = lock.get("release_tag", ""), lock.get("jar_sha256", "")
    if tag and not RELEASE_TAG.fullmatch(tag):
        raise LockError(f"release_tag must be empty or service-vX.Y.Z[-pre], got {tag!r}")
    if digest and not SHA256.fullmatch(digest):
        raise LockError(f"jar_sha256 must be empty or 64 lowercase hex characters, got {digest!r}")
    if bool(tag) != bool(digest):
        raise LockError("release_tag and jar_sha256 are set together or not at all: a release jar is verified by its digest")
    return {"commit": commit, "release_tag": tag, "jar_sha256": digest}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or args[0] not in KEYS:
        print(f"usage: charter_lock.py {'|'.join(KEYS)}", file=sys.stderr)
        return 2
    try:
        print(read()[args[0]])
    except LockError as error:
        print(f"::error::charter.lock.yaml: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
