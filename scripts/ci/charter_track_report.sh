#!/usr/bin/env bash
# Print, as Markdown, what the charter checks of one workflow run concluded (#253): every finished job with its
# conclusion, and for each failed one the error annotations its log carries (the validators and the round trip name
# the failing pack and file in them). charter-track.yml writes it to the job summary and into the red-release issue.
#
#   scripts/ci/charter_track_report.sh <run-id>
#
# Needs `gh` with a token that may read the repository's Actions (GH_TOKEN), and GITHUB_REPOSITORY.
# Only jobs whose name starts with "Charter checks / " are reported (the called gate's jobs).
set -euo pipefail

(( $# == 1 )) || { echo "usage: $0 <run-id>" >&2; exit 2; }
run_id="$1"
repo="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is not set}"
prefix="Charter checks / "
max_lines=40

jobs="$(gh api --paginate "repos/$repo/actions/runs/$run_id/jobs?per_page=100" \
  --jq '.jobs[] | select(.status == "completed") | [.id, .conclusion, .name] | @tsv')"

echo "| Job | Conclusion |"
echo "| --- | --- |"
failed=()
while IFS=$'\t' read -r id conclusion name; do
  [[ -n "$id" && "$name" == "$prefix"* ]] || continue
  echo "| ${name#"$prefix"} | $conclusion |"
  [[ "$conclusion" == failure ]] && failed+=("$id"$'\t'"${name#"$prefix"}")
done <<< "$jobs"

for entry in "${failed[@]}"; do
  id="${entry%%$'\t'*}"
  name="${entry#*$'\t'}"
  echo
  echo "#### $name: errors"
  echo
  echo '```text'
  # A log line is "<timestamp> ##[error]<message>"; keep the message. A log that cannot be read says so.
  if log="$(gh api "repos/$repo/actions/jobs/$id/logs" 2>/dev/null)"; then
    errors="$(grep -F '##[error]' <<< "$log" | sed -E 's/^[^ ]+ ##\[error\]//' | head -n "$max_lines" || true)"
    printf '%s\n' "${errors:-(no error annotation in the log; see the run)}"
  else
    echo "(the job log could not be read; see the run)"
  fi
  echo '```'
done
