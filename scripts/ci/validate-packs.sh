#!/usr/bin/env bash
# Validate every Charter Pack in this repository against the charter pack schemas.
#
# The shapes are owned by spec-kitty-charter (contracts/packs/schemas/*.schema.json, mapped
# to files by contracts/packs/file-kinds.yaml), not by the spec-kitty core CLI; this repository
# no longer treats compatibility with core's pack validator as a requirement. The pinned charter
# commit lives in charter.lock.yaml, the one pin of every charter check.
#
# This is the fast pre-check; the charter service is the authority on composition and registration
# and judges every pack in its own job (scripts/ci/charter_service_check.py).
#
#   1. Every file of every pack under packs/ (built-in included) and of tests/fixtures/valid/
#      validates against the schema the contract maps it to, and every asset sidecar names, by a
#      path relative to assets/, a payload the pack holds. A file is classified as the charter does
#      (a root case variant of a ruled file is retired; Markdown nothing models falls to `ignored`):
#      a file no rule models fails as `unmodelled`, and an ignored file other than a README.md note or
#      a *.skill.md body fails as `not_held`, in built-in-level packs too, which no registration sees.
#   2. Non-vacuity: every pack under tests/fixtures/invalid/ must FAIL validation, so a
#      validator that silently passes everything turns this job red. A fixture whose expected-code
#      says `precheck: accepted` is well formed file by file and refused only by the service
#      (a dependency no pack holds); it is left to the service job.
#
#   3. Cross-pack (--cross-pack, all packs together), only what the charter service does not check:
#      a preset naming an id no pack declares (or a must_have id outside the preset pack's depends_on
#      closure, the charter's requiredNotHeld), a bare DRG fragment edge endpoint that resolves to no
#      node, an id re-declared by a pack of another level, an agent-profile reference that is bare but
#      held by another pack or by none, qualified with the profile's own pack, outside its depends_on
#      closure or not held by the named pack, and a prompt fragment whose target step or slot does not
#      exist. Descriptors, depends_on, sibling conflicts and the references of graph edges are the
#      service's, and are no longer judged here.
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

args=(--cross-pack "${packs[@]}")
service_only=()
for pack in "${invalid[@]}"; do
  [[ -f "$pack/expected-code" ]] || { echo "::error::$pack has no expected-code file; an invalid fixture must name the code the service refuses it with"; exit 1; }
  if grep -Eq '^precheck:[[:space:]]*accepted' "$pack/expected-code"; then
    service_only+=("$pack")  # only the service can refuse it; the schema pass must still accept its files
  else
    args+=(--expect-invalid "$pack")
  fi
done

status=0
python3 scripts/ci/validate_pack_schemas.py "${args[@]}" || status=$?
# A `precheck: accepted` fixture claims its files are well formed: prove it, alone (not in the cross-pack set).
if (( ${#service_only[@]} > 0 )); then
  python3 scripts/ci/validate_pack_schemas.py "${service_only[@]}" || status=$?
fi
exit "$status"
