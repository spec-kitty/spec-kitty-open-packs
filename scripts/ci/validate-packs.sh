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

# Some spec-kitty commands write under $HOME (`init` installs agent skills there, others
# keep locks in ~/.kittify); keep a local run from touching the developer's own files.
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
export HOME="$scratch/home"
mkdir -p "$HOME"

# Validate against the built-in tier this repository authors, not the copy bundled in the
# pinned core: an org pack may reference a built-in node that core has not vendored yet.
# check-built-in.sh validates packs/built-in itself against the pinned core.
export SPEC_KITTY_PACKS_ROOT="$root/packs"

for dir in packs tests/fixtures/valid tests/fixtures/invalid; do
  [[ -d "$dir" ]] || { echo "::error::$dir/ is missing; run from a repository checkout"; exit 1; }
done

spec-kitty --version
spec-kitty charter pack validate --help >/dev/null  # fail fast on a pre-cutover CLI

# packs/built-in is the built-in tier, not an org pack; check-built-in.sh validates it.
mapfile -t packs < <(find packs tests/fixtures/valid -mindepth 1 -maxdepth 1 -type d -not -path packs/built-in | sort)
mapfile -t invalid < <(find tests/fixtures/invalid -mindepth 1 -maxdepth 1 -type d | sort)
(( ${#invalid[@]} > 0 )) || { echo "::error::tests/fixtures/invalid/ holds no fixture; the non-vacuity check would prove nothing"; exit 1; }

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

echo "::group::DRG fragment shape (URN endpoints, no provenance header)"
# Core still resolves bare ids and overwrites the header, so its validator accepts both;
# the charter pack schema refuses them (docs/contracts/index.md). Enforce it here.
if ! python3 - "${packs[@]}" <<'PY'
import sys
from pathlib import Path

import yaml

HEADER = ("pack_name", "source_kind", "source_ref", "layer_index", "provenance_marker")
problems = []
for pack in sys.argv[1:]:
    path = Path(pack) / "drg" / "fragment.yaml"
    if not path.is_file():
        continue
    data = yaml.safe_load(path.read_text()) or {}
    problems += [f"{path}: provenance header field `{key}`" for key in HEADER if key in data]
    for edge in data.get("edges") or []:
        for end in ("source", "target"):
            if ":" not in str(edge.get(end, "")):
                problems.append(f"{path}: bare-id edge {end} `{edge.get(end)}`; write `<kind>:<id>`")
for problem in problems:
    print(f"::error::{problem}")
sys.exit(1 if problems else 0)
PY
then
  failed=1
fi
echo "::endgroup::"

echo "::group::doctor charter-packs (all packs in one consumer)"
consumer="$scratch/consumer"
mkdir -p "$consumer"
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

echo "::group::doctor charter-packs against the pinned core's own built-in"
# The override above hides ids that this repository's built-in has and core's bundled
# built-in lacks: a consumer on a released core would see those edges dangle. Re-run the
# same consumer without the override. Dangling targets listed in pending-core-vendoring.txt
# are warnings; anything else (or an unreadable report) fails.
core_json="$consumer/doctor-core.json"
# doctor exits 1 when it finds errors, so judge the JSON, not the exit code.
(cd "$consumer" && env -u SPEC_KITTY_PACKS_ROOT spec-kitty doctor charter-packs --json) >"$core_json" 2>/dev/null || true
if ! python3 - "$core_json" scripts/ci/pending-core-vendoring.txt <<'PY'
import json, re, sys

try:
    report = json.load(open(sys.argv[1]))
    drg = report["org_drg"]
    errors = list(drg["errors"])
    dangling = list(drg["dangling_endpoints"])
except (OSError, ValueError, KeyError, TypeError) as exc:
    print(f"::error::cannot read the doctor report for the pinned core ({exc!r}); failing closed")
    sys.exit(1)

pending = {
    line.strip()
    for line in open(sys.argv[2])
    if line.strip() and not line.lstrip().startswith("#")
}
target = re.compile(r"references non-existent node '([^']+)'")


def pending_target(message):
    match = target.search(message)
    return match.group(1) if match and match.group(1) in pending else None


failures, seen = [], set()
for message in errors:
    node = pending_target(message)
    if node:
        seen.add(node)
        print(f"::warning::pending core vendoring: {message}")
    else:
        failures.append(message)
# Dangling endpoints are normally also in `errors`; fail on any that were not.
failures += [m for m in dangling if m not in errors and not pending_target(m)]
for stale in sorted(pending - seen):
    print(f"::warning::{stale} no longer dangles against the pinned core; remove it from "
          "scripts/ci/pending-core-vendoring.txt and drop the SPEC_KITTY_PACKS_ROOT override "
          "if the list is now empty")
for message in failures:
    print(f"::error::against the pinned core: {message}")
sys.exit(1 if failures else 0)
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
