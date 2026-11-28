# Sourced by charter_pack_doctor_jar.sh and charter_service_jar.sh: the two checks every release jar of the charter
# passes before a later step runs it. #252. Not run on its own; the sourcing script sets `set -euo pipefail`.

# require_tag_at_commit <repository> <tag> <commit>
# Refuse a release tag that does not point at the lock's `commit` (an annotated tag is read through to its commit), so a
# hand-edited lock cannot judge the packs against two charters.
require_tag_at_commit() {
  local repository="$1" tag="$2" commit="$3" refs tagged
  refs="$(git ls-remote "https://github.com/$repository.git" "refs/tags/$tag" "refs/tags/$tag^{}")"
  tagged="$(awk -v peeled="refs/tags/$tag^{}" '$2 == peeled { print $1 }' <<< "$refs")"  # an annotated tag's commit
  [[ -n "$tagged" ]] || tagged="$(awk -v ref="refs/tags/$tag" '$2 == ref { print $1 }' <<< "$refs")"
  if [[ "$tagged" != "$commit" ]]; then
    echo "::error::$repository tag $tag points at ${tagged:-nothing}, not at the commit $commit of charter.lock.yaml; refusing a pin that names two charters" >&2
    exit 1
  fi
}

# download_verified <url> <dest> <sha256> <lock-key>
# Download over https to <dest> and keep it only when its SHA-256 is <sha256> (the lock's <lock-key>). The download goes
# to <dest>.part, so an unverified or partial file never carries the jar's name and never outlives a failure.
download_verified() {
  local url="$1" dest="$2" digest="$3" key="$4" actual
  part="$dest.part"
  trap 'rm -f -- "$part"' EXIT
  echo "downloading $url" >&2
  if ! curl --proto "=https" --proto-redir "=https" --fail --silent --show-error --location --retry 3 --output "$part" "$url"; then
    echo "::error::could not download $url; removed the partial download" >&2
    exit 1
  fi
  actual="$(sha256sum "$part" | cut -d' ' -f1)"
  if [[ "$actual" != "$digest" ]]; then
    echo "::error::$dest had SHA-256 $actual, not the $key $digest of charter.lock.yaml; deleted it, refusing to run it" >&2
    exit 1
  fi
  mv -f -- "$part" "$dest"
  echo "verified SHA-256 $digest" >&2
}
