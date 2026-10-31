#!/usr/bin/env python3
"""Tree digest of packs/built-in/, as recorded in packs/built-in.source.yaml.

The algorithm is spec-kitty core's ``snapshot_sha256`` (charter.offering.packs.pack_manifest),
reimplemented here so no core install is needed: SHA-256 over every regular file except the
top-level ``pack-manifest.yaml``, in order of POSIX relative path, each contributing an 8-byte
big-endian path length, the UTF-8 path, an 8-byte big-endian size and the raw bytes. A symlink
or a special file refuses.

    python3 scripts/ci/built_in_digest.py            # print the digest
    python3 scripts/ci/built_in_digest.py --check    # fail unless it equals the recorded one
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILT_IN = REPO_ROOT / "packs" / "built-in"
SOURCE = REPO_ROOT / "packs" / "built-in.source.yaml"
MANIFEST = "pack-manifest.yaml"


def snapshot_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if path.is_symlink():
            raise OSError(f"Snapshot contains unsupported symlink: {relative}")
        if relative.as_posix() == MANIFEST or path.is_dir():
            continue
        if not path.is_file():
            raise OSError(f"Snapshot contains unsupported file type: {relative}")
        name = relative.as_posix().encode("utf-8")
        digest.update(len(name).to_bytes(8, "big") + name)
        digest.update(path.stat().st_size.to_bytes(8, "big") + path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="compare with packs/built-in.source.yaml")
    actual = snapshot_sha256(BUILT_IN)
    if not parser.parse_args().check:
        print(actual)
        return 0
    expected = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))["tree_digest"]["value"]
    if actual != expected:
        print(f"::error file=packs/built-in.source.yaml::packs/built-in/ digest {actual} != recorded {expected}; "
              "re-seed: run `python3 scripts/ci/built_in_digest.py` and record the value as tree_digest.value")
        return 1
    print(f"ok: packs/built-in/ digest matches {expected}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
