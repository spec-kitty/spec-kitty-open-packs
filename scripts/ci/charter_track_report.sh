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
err="$(mktemp)"
trap 'rm -f "$err"' EXIT
# A job log carries ANSI colour codes, and the gh on GitHub's runners refuses to print a response with terminal
# escape sequences unless told to (#323): every log read failed with "the response contains terminal escape
# sequences". An older gh has no such flag and prints them anyway; either way the codes are stripped below.
log_flags=()
if gh api --help 2>/dev/null | grep -q -- '--allow-escape-sequences'; then
  log_flags=(--allow-escape-sequences)
fi

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
  # A log line is "<timestamp> ##[error]<message>"; keep the message. A log that cannot be read says so, with
  # gh's own error (also on stderr, so the job log shows it).
  if log="$(gh api "${log_flags[@]}" "repos/$repo/actions/jobs/$id/logs" 2>"$err")"; then
    # Escape sequences and other control characters go, so none reaches the issue. Backticks become quotes, so no
    # log line can close the fence and render as Markdown (or mention anyone).
    errors="$(sed -E $'s/\x1b\\[[0-9;?]*[A-Za-z]//g' <<< "$log" | tr -d '\000-\010\013-\037\177' \
      | grep -F '##[error]' | sed -E 's/^[^ ]+ ##\[error\]//' | tr '`' "'" | head -n "$max_lines" || true)"
    printf '%s\n' "${errors:-(no error annotation in the log; see the run)}"
  else
    echo "(the job log could not be read; see the run)"
    tr -d '\000-\010\013-\037\177' < "$err" | tr '`' "'" | head -n 5
    sed "s/^/job $id log: /" "$err" >&2
  fi
  echo '```'
done
