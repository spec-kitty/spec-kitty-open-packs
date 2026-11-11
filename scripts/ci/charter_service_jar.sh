#!/usr/bin/env bash
# Obtain the charter service jar for the pin in charter.lock.yaml and print its path (the last line of
# stdout; every other message goes to stderr).
#
#   scripts/ci/charter_service_jar.sh <work-dir>
#
# - `release_tag` set: download spec-kitty-charter-service-<version>.jar from that service-v* release
#   of spec-kitty/spec-kitty-charter and refuse it unless its SHA-256 is `jar_sha256`.
# - `release_tag` empty (no release exists yet): fetch the pinned `commit` and build the jar with
#   `./gradlew :deployable:bootJar`. Needs Java 25 on the PATH or in JAVA_HOME, and network access to
#   github.com and the Gradle dependency repositories.
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
digest="$(lock jar_sha256)"

if [[ -n "$tag" ]]; then
  version="${tag#service-v}"
  jar="$work/spec-kitty-charter-service-$version.jar"
  url="https://github.com/$repository/releases/download/$tag/spec-kitty-charter-service-$version.jar"
  echo "downloading $url" >&2
  curl --fail --silent --show-error --location --retry 3 --output "$jar" "$url"
  actual="$(sha256sum "$jar" | cut -d' ' -f1)"
  if [[ "$actual" != "$digest" ]]; then
    echo "::error::$jar has SHA-256 $actual, not the jar_sha256 $digest of charter.lock.yaml; refusing to run it" >&2
    exit 1
  fi
  echo "verified SHA-256 $digest" >&2
  printf '%s\n' "$jar"
  exit 0
fi

source_dir="$work/spec-kitty-charter"
if [[ ! -d "$source_dir/.git" ]]; then
  git init --quiet "$source_dir" >&2
  git -C "$source_dir" remote add origin "https://github.com/$repository.git"
fi
echo "fetching $repository at $commit" >&2
git -C "$source_dir" fetch --quiet --depth 1 origin "$commit" >&2
git -C "$source_dir" checkout --quiet --detach FETCH_HEAD >&2
[[ "$(git -C "$source_dir" rev-parse HEAD)" == "$commit" ]] || { echo "::error::the checkout is not at the pinned commit $commit" >&2; exit 1; }

echo "building the service jar (./gradlew :deployable:bootJar)" >&2
(cd "$source_dir" && ./gradlew --console=plain --no-daemon :deployable:bootJar >&2)

shopt -s nullglob
jars=("$source_dir"/service/deployable/build/libs/*.jar)
built=()
for candidate in "${jars[@]}"; do
  [[ "$candidate" == *-plain.jar ]] || built+=("$candidate")
done
(( ${#built[@]} == 1 )) || { echo "::error::expected one boot jar under service/deployable/build/libs/, found ${#built[@]}: ${built[*]:-none}" >&2; exit 1; }
printf '%s\n' "${built[0]}"
