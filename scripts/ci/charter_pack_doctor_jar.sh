#!/usr/bin/env bash
# Obtain the charter's pack-doctor jar for the pin in charter.lock.yaml and print its path, the only line on stdout
# (every other message goes to stderr). #252, #345; charter ADR-0075 decision 9, ADR-0083 decisions 6 and 7.
#
#   scripts/ci/charter_pack_doctor_jar.sh <work-dir>
#
# - `release_tag` set: download pack-doctor-<version>.jar from that service-v* release of spec-kitty/spec-kitty-charter
#   and refuse it unless its SHA-256 is `pack_doctor_sha256`. Never a floating "latest". The tag must point at the
#   lock's `commit`, the commit the schema pass reads its schemas at, so a hand-edited lock cannot judge the packs
#   against two charters.
# - `release_tag` empty (a main pin, or the charter track's on-demand run): fetch the pinned `commit` and build the jar
#   with `./gradlew :pack-doctor:packDoctorJar`. Needs Java 25 on the PATH or in JAVA_HOME, and network access to
#   github.com and the Gradle dependency repositories. The checkout is shared with charter_service_jar.sh.
#
# <work-dir> is created if needed and holds the download, or the checkout and the build.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repository="spec-kitty/spec-kitty-charter"
# shellcheck source=charter_release_asset.sh
source "$here/charter_release_asset.sh"

(( $# == 1 )) || { echo "usage: $0 <work-dir>" >&2; exit 2; }
work="$1"
mkdir -p "$work"

lock() { python3 "$here/charter_lock.py" "$1"; }  # fails closed on a malformed pin
commit="$(lock commit)"
tag="$(lock release_tag)"
digest="$(lock pack_doctor_sha256)"

if [[ -n "$tag" ]]; then
  require_tag_at_commit "$repository" "$tag" "$commit"
  version="${tag#service-v}"
  jar="$work/pack-doctor-$version.jar"
  url="https://github.com/$repository/releases/download/$tag/pack-doctor-$version.jar"
  download_verified "$url" "$jar" "$digest" pack_doctor_sha256
  printf '%s\n' "$jar"
  exit 0
fi

source_dir="$work/spec-kitty-charter"
if [[ "$(git -C "$source_dir" rev-parse HEAD 2>/dev/null || true)" != "$commit" ]] \
   || [[ -n "$(git -C "$source_dir" status --porcelain --untracked-files=no 2>/dev/null)" ]]; then
  if [[ ! -d "$source_dir/.git" ]]; then
    git init --quiet "$source_dir" >&2
    git -C "$source_dir" remote add origin "https://github.com/$repository.git"
  fi
  echo "fetching $repository at $commit" >&2
  git -C "$source_dir" fetch --quiet --depth 1 origin "$commit" >&2
  git -C "$source_dir" checkout --quiet --force --detach FETCH_HEAD >&2  # a reused checkout runs the pin, never local edits
fi
[[ "$(git -C "$source_dir" rev-parse HEAD)" == "$commit" ]] || { echo "::error::the checkout is not at the pinned commit $commit" >&2; exit 1; }

echo "building the pack-doctor jar (./gradlew :pack-doctor:packDoctorJar)" >&2
(cd "$source_dir" && ./gradlew --console=plain --no-daemon :pack-doctor:packDoctorJar >&2)

shopt -s nullglob
built=("$source_dir"/service/pack-doctor/build/pack-doctor/pack-doctor-*.jar)
(( ${#built[@]} == 1 )) || { echo "::error::expected one jar under service/pack-doctor/build/pack-doctor/, found ${#built[@]}: ${built[*]:-none}" >&2; exit 1; }
printf '%s\n' "${built[0]}"
