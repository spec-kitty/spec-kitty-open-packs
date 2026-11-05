#!/usr/bin/env bash
# Check the recorded digest of the built-in pack (spec-kitty-open-packs#31).
#
# The tree digest of packs/built-in/ matches packs/built-in.source.yaml. This repository authors
# the pack: edit it here and record the digest in the same change. The schema
# validation of the pack's files is done by validate-packs.sh.
#
# Usage: scripts/ci/check-built-in.sh   (from the repository root; needs python3 with pyyaml)
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

[[ -f packs/built-in/pack.yaml ]] || { echo "::error::packs/built-in/pack.yaml is missing"; exit 1; }

python3 scripts/ci/built_in_digest.py --check
