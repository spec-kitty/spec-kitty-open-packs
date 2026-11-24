---
affected_files: []
cycle_number: 1
mission_slug: release-pin-follow-through-01M872WA
reproduction_command:
reviewed_at: '2026-11-24T15:52:48Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP03
---

# WP03 review: REJECT (claude::reviewer-renata)

Reviewed lane-c at 7311a464 (`charter-track.yml`, `charter_pin.py`, tests).

Verified: actionlint passes (via actionlint-py). zizmor 1.33.1 `--offline` shows the same single low `self-repository` finding as the base and nothing new. The `tests/ci` suite has 4 `setUpClass` errors, the same 4 as on the base (aed2dfc). The 11 new tests pass, and release, vocabulary, docs and assets are green. The provenance job does no checkout and runs no repository code. Its `permissions` are `{contents: read, attestations: read}`. It never fails (`exit 0`, no `set -e`). `!cancelled()` together with `needs.checks.result == 'success'` cannot run the bump when the checks failed or were skipped. `persist-credentials: false` is set on every checkout. No workflow-level or job-level token env exists. `PR_CREATION_TOKEN` appears only in "Open".

## Blocking

1. **Splitting into steps of one job is not a credential boundary. FR-006's intent ("parsed with no credential in reach") and NFR-002's intent are not met.**
   The derive step runs `charter_pin.py apply` and its third-party parsers over the release's contract. The later steps of the same job hold `GH_TOKEN` (`contents: write`) and `PR_TOKEN`, and the derive step can take control of what those steps run:
   - **`$GITHUB_PATH`**: derive appends a directory that holds a fake `gh`. "Push" and "Open" then run that `gh` with `GH_TOKEN` and `PR_TOKEN` in its environment. This is the only proof needed.
   - **`$GITHUB_ENV`**: derive sets `BASH_ENV` (the `run:` shell is a non-interactive bash, so it sources that file) or `LD_PRELOAD` for every later step.
   - **`$RUNNER_TEMP/request.json`**: "Push" sends this file verbatim to `gh api graphql` with the job token. Derive writes the whole file: the query text (any mutation) and `branch.branchName` (it could be `main`), so the job token's contents:write goes wherever derive points it. `$RUNNER_TEMP/pr.md` is attacker-controlled in the same way, but it is only a PR body.
   - **Process persistence**: a background process started by derive survives until the job ends (orphans are reaped only at job end). It can read `/proc/<pid>/environ` of the later `gh` processes.

   The tests check only the `env:` blocks, so they pass while every route above stays open.

   **Fix**: a job boundary.
   - (a) A `derive` job with `contents: read` and no secrets. It runs apply, changelog, commit-payload and the PR body, and uploads an artifact: the fileChanges JSON, `pr.md` and `head`.
   - (b) The bump/publish job does no checkout, no setup-python and no `pip`. It downloads the artifact and builds the GraphQL request itself:
     - a fixed `createCommitOnBranch` query;
     - `branch` set from the lookup step's value, and `repositoryNameWithOwner` from `github.repository`;
     - `expectedHeadOid` equal to the head that resolve or derive reported, re-checked against `github.sha`;
     - from the artifact, only `fileChanges` and the message. Reject paths outside the derivable set (no `.github/`).

   Also pass `pr.md` only as `--body-file`. Add a test that the token-holding job has no `checkout`/`setup-python` and does not use `python`. Add a test that the request is assembled in the token job from fixed parts, not read verbatim.

   This is the plan's prescribed shape (three steps in one job), so the WP prompt's step design needs amending. The implementer followed it faithfully.

2. **Unsigned implementer commit on the lane.** `aed2dfc` (Merge coordination into lane-c, made before 7311a46) has no signature. 7311a46 is SSH-signed. The spec-kitty bookkeeping commits (`chore(spec-kitty)…`, the CLI's own coord→lane merges) are unsigned across the whole mission. That is tooling and is not counted against WP03, but the landing squash or rewrite needs to account for it.

## Advisory (non-blocking; the WP prompt prescribes the current behaviour)

3. **A SHA mismatch is reported as "not verified: no build attestation was found, or it did not verify".** That wording hides an integrity event: the release asset is not the file the bump pins. The checks job already enforced the pin against the jar it tested, so a bad jar is not silently pinned. Even so, a mismatch should be a distinct state, `mismatch`, with a `::error::`-level annotation and its own PR-body line, separate from "attestation missing". Better still, it should keep the bump PR from opening. The operator ruling covers only the attestation, and this is a different case.

4. `gh attestation verify --repo` accepts an attestation from any workflow in spec-kitty-charter. Consider `--signer-workflow spec-kitty/spec-kitty-charter/.github/workflows/<release>.yml` and/or `--source-ref refs/tags/$RELEASE_TAG` to bind it to the release build.
