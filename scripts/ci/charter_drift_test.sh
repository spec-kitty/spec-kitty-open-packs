#!/usr/bin/env bash
# Run the charter's whole-pack round trip over this repository's packs, at the pin in charter.lock.yaml (#252;
# charter ADR-0070 decision 4, amended 2026-11-13).
#
#   scripts/ci/charter_drift_test.sh <work-dir>
#
# From the pinned spec-kitty-charter checkout at <work-dir>/spec-kitty-charter (fetched when absent, as
# charter_service_jar.sh fetches it for a commit pin), runs
#   ./gradlew --max-workers=1 :packs:driftTest -PopenPacksDir=<this repository>
# which loads every pack with a pack.yaml through the production store, writes it back and compares every file by
# meaning. A load violation, an unmodelled file, a load warning or a file that does not round-trip fails it; a
# pack-manifest.yaml whose lists differ from the derived ones fails as "pack-manifest.yaml: refused: leaves out ...".
# On a release pin, `commit` must be the commit `release_tag` was built from, or the two steps judge different charters.
# The report is at <work-dir>/spec-kitty-charter/service/packs/build/reports/tests/driftTest.
# Needs Java 25 on the PATH or in JAVA_HOME, and network access to github.com and the Gradle dependency repositories.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
repository="spec-kitty/spec-kitty-charter"

(( $# == 1 )) || { echo "usage: $0 <work-dir>" >&2; exit 2; }
work="$1"
mkdir -p "$work"

commit="$(python3 "$here/charter_lock.py" commit)"  # fails closed on a malformed pin
source_dir="$work/spec-kitty-charter"
if [[ "$(git -C "$source_dir" rev-parse HEAD 2>/dev/null || true)" != "$commit" ]] \
   || [[ -n "$(git -C "$source_dir" status --porcelain --untracked-files=no 2>/dev/null)" ]]; then
  if [[ ! -d "$source_dir/.git" ]]; then
    git init --quiet "$source_dir"
    git -C "$source_dir" remote add origin "https://github.com/$repository.git"
  fi
  echo "fetching $repository at $commit" >&2
  git -C "$source_dir" fetch --quiet --depth 1 origin "$commit"
  git -C "$source_dir" checkout --quiet --force --detach FETCH_HEAD  # a reused checkout runs the pin, never local edits
fi
[[ "$(git -C "$source_dir" rev-parse HEAD)" == "$commit" ]] || { echo "::error::the checkout is not at the pinned commit $commit" >&2; exit 1; }

echo "round-tripping every pack of $repo through the charter at $commit (./gradlew :packs:driftTest)" >&2
cd "$source_dir"
./gradlew --console=plain --no-daemon --max-workers=1 :packs:driftTest -PopenPacksDir="$repo"
