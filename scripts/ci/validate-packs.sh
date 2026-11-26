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
#      a file no rule models is warned as `file_not_held` (#309), and so is an ignored file other than a README.md
#      note (operator ruling R34, #331: a stray file warns; a skill body its skill's body_path names is held), in
#      built-in-level packs too, which no registration sees.
#   2. Non-vacuity: every pack under tests/fixtures/invalid/ must FAIL validation, so a
#      validator that silently passes everything turns this job red. A fixture whose expected-code
#      says `precheck: accepted` is well formed file by file and refused only by the service
#      (a dependency no pack holds); it is left to the service job.
#
#   3. Cross-pack (--cross-pack, all packs together): only the house rules, what the charter does not judge by
#      ruling (#348; C-005, ADR-0083 decision 18), each named in validate_pack_schemas.py with its ruling:
#      - an id re-declared by a pack of another level (ADR-0053 decision 6: the charter takes it as a layer override);
#      - a bare DRG fragment edge endpoint that resolves to no node of any pack (DIV-007);
#      - a prompt-fragment slot the target step's prompt does not declare (C38);
#      - a cycle among the agent profiles' specializes_from edges (the ruling R-s remainder, until charter #636);
#      - the agent-profile references: a bare one no pack holds and one qualified with the profile's own pack (not
#        charter rules, charter research/rule-coverage.md row 6), and a bare one only another pack holds, one outside
#        the depends_on closure or not held by the named pack (pack-doctor does not judge a profile's references at
#        the pin; kept until it does).
#      Everything else across packs is pack-doctor's (`validate --round-trip --full`, scripts/ci/charter_pack_doctor.py,
#      charter docs/guides/check-packs.md): composition, the preset items (preset_item_undeclared, preset_item_not_held),
#      the graph references, the step enhancements' targets and the manifests (manifest_stale, manifest_membership;
#      `pack-doctor remediate <pack>` writes a manifest).
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

# A manifest's membership and hashes are pack-doctor's (manifest_membership, manifest_stale), not this pass's (#347).
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
