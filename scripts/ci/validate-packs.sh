#!/usr/bin/env bash
# Validate every Charter Pack in this repository against the charter pack schemas.
#
# The shapes are owned by spec-kitty-charter (contracts/packs/schemas/*.schema.json, mapped
# to files by contracts/packs/file-kinds.yaml), not by the spec-kitty core CLI; this repository
# no longer treats compatibility with core's pack validator as a requirement. The pinned charter
# commit lives in scripts/ci/validate_pack_schemas.py.
#
#   1. Every file of every pack under packs/ (built-in included) and of tests/fixtures/valid/
#      validates against the schema the contract maps it to.
#   2. Non-vacuity: every pack under tests/fixtures/invalid/ must FAIL validation, so a
#      validator that silently passes everything turns this job red.
#
# The validator fails closed (exit 2) on an unloadable schema, a known-kind file with no schema
# mapping, or a pack with zero files checked.
#
# Needs python3 with pyyaml and jsonschema. Usage: scripts/ci/validate-packs.sh (repository root)
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

for dir in packs tests/fixtures/valid tests/fixtures/invalid; do
  [[ -d "$dir" ]] || { echo "::error::$dir/ is missing; run from a repository checkout"; exit 1; }
done

mapfile -t packs < <(find packs tests/fixtures/valid -mindepth 1 -maxdepth 1 -type d | sort)
mapfile -t invalid < <(find tests/fixtures/invalid -mindepth 1 -maxdepth 1 -type d | sort)
(( ${#packs[@]} > 0 )) || { echo "::error::no pack found under packs/ or tests/fixtures/valid/; the validation would prove nothing"; exit 1; }
(( ${#invalid[@]} > 0 )) || { echo "::error::tests/fixtures/invalid/ holds no fixture; the non-vacuity check would prove nothing"; exit 1; }

args=("${packs[@]}")
for pack in "${invalid[@]}"; do args+=(--expect-invalid "$pack"); done

python3 scripts/ci/validate_pack_schemas.py "${args[@]}"
