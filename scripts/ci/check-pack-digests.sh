#!/usr/bin/env bash
# Check the recorded tree digest of every pack (spec-kitty-open-packs#194).
#
# Every directory packs/<name>/ with a pack.yaml has a sidecar packs/<name>.source.yaml whose
# tree_digest matches the directory. Edit a pack, then run `python3 scripts/ci/pack_digest.py --update`
# in the same change. Schema validation is validate-packs.sh's.
#
# Usage: scripts/ci/check-pack-digests.sh   (from the repository root; needs python3 with pyyaml)
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

python3 scripts/ci/pack_digest.py --check
