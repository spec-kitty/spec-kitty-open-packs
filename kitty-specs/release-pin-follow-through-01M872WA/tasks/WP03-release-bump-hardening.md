---
work_package_id: WP03
title: Release bump hardening (#310)
dependencies: []
requirement_refs:
- FR-006
- FR-007
- FR-008
- NFR-002
- NFR-003
- C-003
- SC-003
- SC-004
planning_base_branch: ci/release-pin-follow-through
merge_target_branch: ci/release-pin-follow-through
branch_strategy: Planning artifacts for this mission were generated on ci/release-pin-follow-through. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into ci/release-pin-follow-through unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-release-pin-follow-through-01M872WA
base_commit: f7b0b27254f245ee25d01fe420a60786b1fc79a7
created_at: '2026-11-24T15:42:58.365687+00:00'
subtasks:
- T009
- T010
- T011
- T012
- T013
- T014
history:
- at: '2026-11-24T16:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: .github/workflows/charter-track.yml
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- .github/workflows/charter-track.yml
- scripts/ci/charter_pin.py
- tests/ci/test_charter_pin.py
- tests/ci/test_workflows.py
role: implementer
tags: []
tracker_refs:
- '#310'
---
# Work Package Prompt: WP03 – Release bump hardening (#310)

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load python-pedro` before reading anything else.

## Objective

1. **Token scoping (FR-006, #310 item 2).** In `.github/workflows/charter-track.yml`, job `bump`, the step "Push the bump branch" (≈l.304–371) holds `GH_TOKEN: ${{ github.token }}` (`contents: write`) while it runs `charter_pin.py apply`, `changelog` and `commit-payload`. `apply` parses the new release's contract content. Split the step so that no step holding a token runs repository Python.
2. **Attestation (FR-007/008, #310 item 1).** Operator ruling: **warn only**. Verify the build attestation of the release's service jar *and* its pack-check jar. On a missing or failing attestation, annotate a warning, open the bump PR anyway, and say so in the PR body.

Read `plan.md` (Engineering Alignment) and `research.md` (R4, R5) first. Keep every existing guarantee of the job:
- one branch per release;
- an interrupted run's branch is deleted;
- a closed-unmerged PR is not re-proposed;
- the commit is signed by GitHub through `createCommitOnBranch`;
- `PR_CREATION_TOKEN` is held only by the "Open" step;
- the missing-secret check fails before any push;
- `Closes #<red issue>` stays in the PR body.

## Branch Strategy

The planning branch and merge target is `ci/release-pin-follow-through`. Worktrees are allocated per lane from `lanes.json`. Implement with `spec-kitty agent action implement WP03 --agent <name> --mission release-pin-follow-through-01M872WA`.

## Subtasks

### T009 — `attestation_note()` (red-first)

`scripts/ci/charter_pin.py`: add a pure function and a subcommand.

```python
ATTESTATION_STATES = ("verified", "unverified", "")  # "" = not checked (the provenance job did not report)

def attestation_note(service: str, pack_check: str) -> str:
    """The PR-body paragraph on the two jars' build attestations (#310; operator ruling: warn only)."""
```

The output is Markdown lines. There is one bullet per jar, naming the jar (service jar, pack-check jar) and its state:
- verified: "verified against `spec-kitty/spec-kitty-charter` (`gh attestation verify`)";
- unverified: "**not verified**: no build attestation was found, or it did not verify";
- not checked: "**not checked**: the provenance job did not report".

When any jar is not verified, add one bold line asking the reviewer to compare the digests with the release assets by hand. An unknown state raises `PinError`.

Subcommand: `attestation-note --service STATE --pack-check STATE` prints the note.

Write the tests first, in `tests/ci/test_charter_pin.py`: all-verified, one unverified, both not checked, and an unknown state that is refused (exit 2 through `main`).

### T010 — Red workflow-structure tests

File: `tests/ci/test_workflows.py`. Extend `CharterTrackBumpTokens`, or add a sibling class `CharterTrackBumpProvenance`.
- **No token beside Python:** in `bump`, no step whose `run` mentions `charter_pin.py` or `python3` may have a key matching `TOKEN|SECRET` in its `env`, or `${{ secrets.` / `github.token` anywhere in its `env` values. This must fail on the current file.
- The token-holding steps of `bump` run only `gh`, `jq`, `echo`, `awk`, `git rev-parse`, shell builtins and `tee`. Assert at least that they never contain `python`.
- **`provenance` job:**
  - `permissions` are exactly `{contents: read, attestations: read}`;
  - it runs on the same condition as `bump`, minus `needs.checks.result` (it may run alongside checks: `needs: resolve` only);
  - its steps never `exit 1`: grep each `run` for `exit 1` and require none, or require `continue-on-error: true`;
  - its outputs are `service` and `pack_check`.
- **`bump`:** `needs` includes `provenance`; `if` starts with `!cancelled()` and still requires `needs.checks.result == 'success'`; the re-derive step's env passes `needs.provenance.outputs.service` and `.pack_check` into `charter_pin.py attestation-note`.
- Update the existing holder lists, such as `test_the_pat_lives_only_in_the_step_that_runs_nothing_but_gh` and `test_only_the_acting_jobs_hold_a_secret_or_a_write_permission`, to the new step names. Keep their intent.
- Re-run `CharterTrack.test_a_newer_release_on_main_opens_one_pull_request_when_green_and_one_issue_when_red` (`self.runs("bump", …)`). Add `provenance` to the simulated needs if the simulator requires it, and assert that bump still runs when provenance's result is `failure`, as required by `!cancelled()`.

### T011 — Split the bump step

Replace "Push the bump branch" with three steps:

1. **`lookup`, "Look up the bump state"**: env has `GH_TOKEN: ${{ github.token }}`, `REPO` and `RELEASE_TAG`. It runs only `gh` and shell:
   - the `open-prs.tsv` listing, the already-open check and the closed-unmerged check;
   - the interrupted-branch delete;
   - the open `charter:release-red` issue number.

   It writes `branch=` and `red=` to `$GITHUB_OUTPUT` and sets `go=true` only when a bump should be made. Move the early `exit 0` paths here.
2. **`derive`, "Re-derive the packs at the release"** (`if: steps.lookup.outputs.go == 'true'`): **no `GH_TOKEN` and no secret in `env`**. It runs:
   - `charter_pin.py apply`, then `changelog`;
   - `head="$(git rev-parse HEAD)"`, then `charter_pin.py commit-payload … > "$RUNNER_TEMP/input.json"`;
   - the `jq` GraphQL request build into `$RUNNER_TEMP/request.json`.

   It then writes `pr.md`. That is the body from today's step plus the `attestation-note` output inserted after the digest bullets, using `RED` from the lookup step. It writes `head=` to its outputs.

   Checkout already uses `persist-credentials: false`; keep it.
3. **`push`, "Push the bump branch"**: env has `GH_TOKEN: ${{ github.token }}`, `REPO`, `BRANCH` and `HEAD`. It runs only `gh api` (create the ref, run the GraphQL commit) and `echo`. It sets `branch=` as the output the "Open" step reads (`steps.push.outputs.branch`). Update the "Open" step's `if` and env accordingly.

Keep the step comments factual. Keep `set -euo pipefail` in each step.

### T012 — `provenance` job

The new job sits before `bump`:

```yaml
  provenance:
    name: Release provenance
    needs: resolve
    if: <the bump condition's resolve/main parts>
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: read
      attestations: read
    outputs:
      service: ${{ steps.verify.outputs.service }}
      pack_check: ${{ steps.verify.outputs.pack_check }}
```

It has one step, `verify`, with env `GH_TOKEN: ${{ github.token }}`, `RELEASE_TAG` and `CHARTER: spec-kitty/spec-kitty-charter`. No checkout is needed, and no repository code is run.
- For each jar: `version="${RELEASE_TAG#service-v}"`, then `gh release download "$RELEASE_TAG" --repo "$CHARTER" --pattern "spec-kitty-charter-service-$version.jar"` (and `pack-check-$version.jar`) into `$RUNNER_TEMP`.
- Then `gh attestation verify "$jar" --repo "$CHARTER"`.
- On any failure, of the download or the verification, emit `::warning::` naming the jar and the release, and record `unverified`. Otherwise record `verified`.
- Also check that the downloaded jar's `sha256sum` equals `needs.resolve.outputs.jar_sha256` / `pack_check_sha256`. On a mismatch, record `unverified` with a warning: the attestation covers a different file than the one pinned.
- Write both states to `$GITHUB_OUTPUT` and to the step summary. Never exit non-zero: no `set -e` around the checks, or use `if ! …; then`.

### T013 — Wire into `bump`

- `needs: [resolve, checks, provenance]`.
- `if: ${{ !cancelled() && <existing condition> }}`. The existing condition already requires `needs.checks.result == 'success'`, so a failed check still blocks. A failed or skipped provenance job yields empty outputs, and the note then says "not checked".
- The derive step's env adds `ATTEST_SERVICE: ${{ needs.provenance.outputs.service }}` and `ATTEST_PACK_CHECK: ${{ needs.provenance.outputs.pack_check }}`, and calls `python3 scripts/ci/charter_pin.py attestation-note --service "$ATTEST_SERVICE" --pack-check "$ATTEST_PACK_CHECK"`.

Change "**Check the two digests yourself before merging.** They were copied from the release's own `.sha256` assets, so nothing independent stands behind them" so that it now refers to the attestation lines above it.

### T014 — Header comment

Update the "Tokens" block at the top of the workflow:
- the bump job's token is held only by the lookup, push and open steps, and never by the step that runs the pin tooling;
- add a "Provenance" line: the read-only `provenance` job verifies both jars' build attestations, warn only (operator ruling on #310), and the bump PR body states the outcome.

If `actionlint` is available (`which actionlint`, or `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.7`), run it on the file and fix its findings. Otherwise say so in the hand-off.

## Definition of Done

- `python3 -m unittest tests.ci.test_charter_pin tests.ci.test_workflows` passes. The T010 tests were red before T011–T013; record this in the commit body.
- `grep -n "GH_TOKEN\|secrets\." .github/workflows/charter-track.yml` shows no token in any step that runs `python3`, except the `resolve` job's existing read-only lookup, which is out of scope (NFR-002).
- The hand-off names the live-proof gap: the bump only runs on `main`. #310 asks for a proof by dispatch from a fork or test branch, which is an operator action.

## Reviewer guidance

Trace each of the existing guarantees listed under Objective through the new three-step split. Confirm that the `provenance` job cannot fail the run, and that a failed `checks` still blocks `bump`.
