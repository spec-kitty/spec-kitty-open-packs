#!/usr/bin/env python3
"""Compatibility entry point for the tree digest of packs/built-in/.

Kept for external callers (kitty-stack ``open-packs digest``); the implementation for every pack
lives in ``pack_digest.py``.

    python3 scripts/ci/built_in_digest.py            # print the digest (one hex line)
    python3 scripts/ci/built_in_digest.py --check    # fail unless it equals the recorded one
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pack_digest import PACKS, check, snapshot_sha256  # noqa: E402

BUILT_IN = PACKS / "built-in"

__all__ = ["BUILT_IN", "main", "snapshot_sha256"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="compare with packs/built-in.source.yaml")
    if parser.parse_args(argv).check:
        return check(PACKS, ["built-in"])
    print(snapshot_sha256(BUILT_IN))
    return 0


if __name__ == "__main__":
    sys.exit(main())
