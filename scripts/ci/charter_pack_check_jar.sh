#!/usr/bin/env bash
# Obtain the charter's pack-check jar for the pin in charter.lock.yaml and print its path, the only line on stdout
# (every other message goes to stderr). #252; charter ADR-0075 decision 9.
#
#   scripts/ci/charter_pack_check_jar.sh <work-dir>
#
# - `release_tag` set: download pack-check-<version>.jar from that service-v* release of spec-kitty/spec-kitty-charter
#   and refuse it unless its SHA-256 is `pack_check_sha256`. Never a floating "latest". The tag must point at the
#   lock's `commit`, the commit the schema pass reads its schemas at, so a hand-edited lock cannot judge the packs
#   against two charters.
# - `release_tag` empty (a main pin, or the charter track's on-demand run): fetch the pinned `commit` and build the jar
#   with `./gradlew :pack-check:packCheckJar`. Needs Java 25 on the PATH or in JAVA_HOME, and network access to
#   github.com and the Gradle dependency repositories. The checkout is shared with charter_service_jar.sh.
#
# <work-dir> is created if needed and holds the download, or the checkout and the build.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repository="spec-kitty/spec-kitty-charter"

(( $# == 1 )) || { echo "usage: $0 <work-dir>" >&2; exit 2; }
work="$1"
mkdir -p "$work"

lock() { python3 "$here/charter_lock.py" "$1"; }  # fails closed on a malformed pin
commit="$(lock commit)"
tag="$(lock release_tag)"
digest="$(lock pack_check_sha256)"

if [[ -n "$tag" ]]; then
  refs="$(git ls-remote "https://github.com/$repository.git" "refs/tags/$tag" "refs/tags/$tag^{}")"
  tagged="$(awk -v peeled="refs/tags/$tag^{}" '$2 == peeled { print $1 }' <<< "$refs")"  # an annotated tag's commit
  [[ -n "$tagged" ]] || tagged="$(awk -v ref="refs/tags/$tag" '$2 == ref { print $1 }' <<< "$refs")"
  if [[ "$tagged" != "$commit" ]]; then
    echo "::error::$repository tag $tag points at ${tagged:-nothing}, not at the commit $commit of charter.lock.yaml; refusing a pin that names two charters" >&2
    exit 1
  fi
  version="${tag#service-v}"
  jar="$work/pack-check-$version.jar"
  url="https://github.com/$repository/releases/download/$tag/pack-check-$version.jar"
  echo "downloading $url" >&2
  part="$jar.part"  # an unverified download never carries the jar's name, and never outlives a failure
  trap 'rm -f -- "$part"' EXIT
  if ! curl --proto "=https" --proto-redir "=https" --fail --silent --show-error --location --retry 3 --output "$part" "$url"; then
    echo "::error::could not download $url; removed the partial download" >&2
    exit 1
  fi
  actual="$(sha256sum "$part" | cut -d' ' -f1)"
  if [[ "$actual" != "$digest" ]]; then
    echo "::error::$jar had SHA-256 $actual, not the pack_check_sha256 $digest of charter.lock.yaml; deleted it, refusing to run it" >&2
    exit 1
  fi
  mv -f -- "$part" "$jar"
  echo "verified SHA-256 $digest" >&2
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

echo "building the pack-check jar (./gradlew :pack-check:packCheckJar)" >&2
(cd "$source_dir" && ./gradlew --console=plain --no-daemon :pack-check:packCheckJar >&2)

shopt -s nullglob
built=("$source_dir"/service/pack-check/build/pack-check/pack-check-*.jar)
(( ${#built[@]} == 1 )) || { echo "::error::expected one jar under service/pack-check/build/pack-check/, found ${#built[@]}: ${built[*]:-none}" >&2; exit 1; }
printf '%s\n' "${built[0]}"
