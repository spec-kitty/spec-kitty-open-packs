#!/usr/bin/env bash
# Check the seeded built-in pack (spec-kitty-open-packs#31).
#
#   1. `charter pack validate built-in` reports no errors. built-in/ sits outside
#      packs/ on purpose: validate-packs.sh registers every packs/* directory as an
#      org pack, and built-in is not one (it would shadow the CLI's own built-in).
#   2. The tree digest matches built-in.source.yaml, so built-in/ only changes
#      through a deliberate re-seed that also updates the recorded digest.
#
# Usage: scripts/ci/check-built-in.sh   (from the repository root; needs spec-kitty)
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
export HOME="$scratch/home"
mkdir -p "$HOME"

[[ -f built-in/pack.yaml ]] || { echo "::error::built-in/pack.yaml is missing"; exit 1; }

failed=0
if ! spec-kitty charter pack validate built-in; then
  echo "::error file=built-in::charter pack validate failed for built-in"
  failed=1
fi

# Use the spec-kitty install's own interpreter so the hash function is the one core uses.
python_bin="$(head -1 "$(command -v spec-kitty)" | sed -e 's/^#!//')"
if ! "$python_bin" - <<'PY'
import sys
from pathlib import Path

import yaml
from charter.offering.packs.pack_manifest import snapshot_sha256

expected = yaml.safe_load(Path("built-in.source.yaml").read_text())["tree_digest"]["value"]
actual = snapshot_sha256(Path("built-in"))
if actual != expected:
    print(f"::error file=built-in.source.yaml::built-in/ digest {actual} != recorded {expected}; "
          "re-seed from core and update built-in.source.yaml")
    sys.exit(1)
print(f"ok: built-in/ digest matches {expected}")
PY
then
  failed=1
fi

exit "$failed"
