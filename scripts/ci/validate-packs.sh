#!/usr/bin/env bash
# Validate every Charter Pack in this repository against the installed spec-kitty.
#
#   1. `charter pack validate` on each pack (and `charter org validate` when it has
#      an org-charter.yaml).
#   2. Register all packs together in a scratch consumer project and run
#      `doctor charter-packs`; fail on ids declared by more than one pack, DRG errors
#      and dangling endpoints, which a per-pack validate cannot see.
#   3. Non-vacuity: every pack under tests/fixtures/invalid/ must FAIL validation,
#      so a validator that silently passes everything turns this job red.
#
# Usage: scripts/ci/validate-packs.sh   (from the repository root)
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$root"

spec-kitty --version
spec-kitty charter pack validate --help >/dev/null  # fail fast on a pre-cutover CLI

mapfile -t packs < <(find packs tests/fixtures/valid -mindepth 1 -maxdepth 1 -type d | sort)
mapfile -t invalid < <(find tests/fixtures/invalid -mindepth 1 -maxdepth 1 -type d | sort)

failed=0

echo "::group::charter pack validate"
for pack in "${packs[@]}"; do
  echo "--- $pack"
  if ! spec-kitty charter pack validate "$pack"; then
    echo "::error file=$pack::charter pack validate failed for $pack"
    failed=1
  fi
  if [[ -f "$pack/org-charter.yaml" ]] && ! spec-kitty charter org validate "$pack"; then
    echo "::error file=$pack/org-charter.yaml::charter org validate failed for $pack"
    failed=1
  fi
done
echo "::endgroup::"

echo "::group::doctor charter-packs (all packs in one consumer)"
consumer="$(mktemp -d)"
trap 'rm -rf "$consumer"' EXIT
# `spec-kitty init` installs agent skills under $HOME; keep a local run from
# rewriting the developer's own ~/.claude and ~/.agents.
export HOME="$consumer/home"
mkdir -p "$HOME"
git -C "$consumer" init -q
(cd "$consumer" && spec-kitty init --ai claude --non-interactive >/dev/null)
{
  echo "charter_packs:"
  echo "  org:"
  echo "    packs:"
  for pack in "${packs[@]}"; do
    echo "      - name: $(basename "$pack")"
    echo "        local_path: $root/$pack"
  done
} >>"$consumer/.kittify/config.yaml"
if ! (cd "$consumer" && spec-kitty doctor charter-packs); then
  echo "::error::doctor charter-packs reported errors with all packs registered together"
  failed=1
fi
# doctor exits 0 when one org pack silently shadows a sibling's id, so read its JSON
# and fail on org-vs-org collisions, DRG errors and dangling endpoints.
if ! (cd "$consumer" && spec-kitty doctor charter-packs --json) >"$consumer/doctor.json" \
  || ! python3 - "$consumer/doctor.json" <<'PY'
import json, sys

report = json.load(open(sys.argv[1]))
problems = [
    f"{c['kind']} {c['item_id']} is declared by more than one org pack"
    for c in report.get("collisions", [])
    if c.get("higher_layer") == "org" and c.get("lower_layer") == "org"
]
drg = report.get("org_drg") or {}
problems += [f"DRG error: {e}" for e in drg.get("errors", [])]
problems += [f"dangling DRG endpoint: {e}" for e in drg.get("dangling_endpoints", [])]
for problem in problems:
    print(f"::error::{problem}")
sys.exit(1 if problems else 0)
PY
then
  failed=1
fi
echo "::endgroup::"

echo "::group::non-vacuity (invalid fixtures must fail)"
# Exit 1 means "validation errors". Anything else (0 = passed, 2 = unknown
# command on a CLI without `charter pack validate`) means the gate proved nothing.
for pack in "${invalid[@]}"; do
  rc=0
  spec-kitty charter pack validate "$pack" >/dev/null 2>&1 || rc=$?
  if [[ "$rc" -eq 1 ]]; then
    echo "ok: $pack fails validation as expected"
  else
    echo "::error file=$pack::$pack is an invalid fixture but validate exited $rc (want 1); the gate is vacuous"
    failed=1
  fi
done
echo "::endgroup::"

exit "$failed"
