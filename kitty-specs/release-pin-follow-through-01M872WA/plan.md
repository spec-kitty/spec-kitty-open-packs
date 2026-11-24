# Implementation Plan: Release-pin follow-through

**Branch**: `kitty/mission-release-pin-follow-through-01M872WA` → `ci/release-pin-follow-through` | **Date**: 2026-11-24 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/release-pin-follow-through-01M872WA/spec.md`

## Summary

This plan closes the remaining release-pin follow-ups of epic #287, in five work packages:

1. Pin and document the accepted stray-file gap (#331).
2. Make the derived-manifest mirror walk like the charter and pin its wording (#262).
3. Harden the bump job (#310): split the token-holding step so the re-derivation runs with no token, and add a read-only, warn-only provenance job whose result goes into the bump PR body.
4. Anchor the self-binding vocabulary patterns (#304).
5. Refresh the roadmap and add the changelog entry.

Engineering choices are the runner's own. The operator rulings come from the brief (#331 option 3; #310 warn only).

## Technical Context

**Language/Version**: Python 3.12 in CI (`actions/setup-python` in `charter-track.yml` and `validate-packs.yml`); 3.13 locally; the code must hold on both
**Primary Dependencies**: stdlib, `pyyaml==6.0.3`, `jsonschema==4.26.0`; GitHub Actions; `gh` CLI on hosted runners (`gh release download`, `gh attestation verify`). No dependency is added, upgraded or removed.
**Storage**: files (`charter.lock.yaml`, pack manifests, `CHANGELOG.md`)
**Testing**: `python3 -m unittest discover -s tests/ci`; workflow-structure tests in `tests/ci/test_workflows.py` (YAML parsed, steps inspected); red-first per WP
**Target Platform**: GitHub-hosted `ubuntu-latest` runners; maintainers' Linux/macOS checkouts
**Project Type**: single (CI scripts + docs in one repository)
**Performance Goals**: the bump job gains at most 2 jar downloads and 2 verification calls (NFR-003)
**Constraints**: no override of the charter's verdict (C-001); warn only on attestation (C-003); the mirror follows the charter at `cb9b154` (C-002)
**Scale/Scope**: about 6 scripts/workflows, 4 test modules, 3 docs pages

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Charter policy | How this plan meets it |
| --- | --- |
| Aligned to the charter, not core | The mirror follows `ManifestRules.mismatch` and the `PackFileSet` walk at the pin; the #331 gap defers to charter#631 |
| Docs are first-class (DIRECTIVE_037/042/044) | The guide *validate-a-pack.md* and the roadmap change with the behaviour; generated pages are not hand-edited |
| Gates fail closed | Nothing loosens a gate. The attestation check is a new, warn-only signal that the operator ruled must not block |
| Changelog for user-facing change | WP05 adds one entry under `[Unreleased]`, in both `CHANGELOG.md` and `docs/changelog/CHANGELOG.md` (they are kept identical) |
| Tests only where they guard real behaviour (DIRECTIVE_041) | Each test pins a ruling or a bug named in an issue |
| Decisions recorded as ADRs | No new architecture decision. The token split and attestation check implement #310 under the #314 token ruling already recorded in the workflow header |

Re-check after design: pass. No new conflicts.

## Engineering Alignment (runner decisions)

- **Token split (FR-006).** The current "Push the bump branch" step becomes three steps:
  1. **Look up the bump state** (job token; runs only `gh`): lists the open bump PRs, checks for an existing branch or a closed PR, removes an interrupted run's branch, and finds the open `charter:release-red` issue. It writes its findings to `$RUNNER_TEMP` and to step outputs.
  2. **Re-derive the packs at the release** (no token in `env`, and checkout keeps `persist-credentials: false`): runs `charter_pin.py apply`, `changelog` and `commit-payload`, and writes `input.json` and `pr.md`.
  3. **Push the bump branch** (job token; runs only `gh` and `jq`): creates the ref and the signed commit through GraphQL.

  The "Open the bump pull request" step is unchanged.
- **Attestation (FR-007/008).** A new job, `provenance`, gets `contents: read` and `attestations: read` and runs on the same condition as `bump`. It downloads both jars of the release with `gh release download` and runs `gh attestation verify <jar> --repo spec-kitty/spec-kitty-charter` on each. Any non-zero result is recorded as `unverified` with a `::warning::`. The job always exits 0.

  `bump` needs it and runs on `!cancelled()` plus its current condition, so a provenance crash cannot block the bump; in that case the PR body says "not checked".

  The PR-body paragraph comes from a pure function, `attestation_note(service, pack_check)`, in `charter_pin.py`, exposed as the `attestation-note` subcommand and unit tested.
- **Walk (FR-003).** A helper, `pack_files(pack_dir)`, built on `os.walk(followlinks=False)`, yields the regular, non-link files in path order. It follows a pack root that is itself a link, as the charter does (#174). `derived_manifest` uses it. The other `rglob("*")` walks in `validate_pack_schemas.py` and `charter_service_check.py` are each audited in WP02. A walk that mirrors the charter's file set switches to the helper; any other walk is left as it is, with the reason noted in the WP.
- **Mismatch (FR-004).** No code change: the port already equals `ManifestRules.mismatch` at the pin (research R2). A test pins the duplicated, unheld case.
- **#304 (FR-009).** Anchor the four false-positive patterns to the end of a clause (`[.;:,)]|$`). Add patterns for the five false negatives. Shorten the `::error` message to 200 characters or fewer.

## Project Structure

### Documentation (this mission)

```
kitty-specs/release-pin-follow-through-01M872WA/
├── plan.md
├── research.md
├── quickstart.md
└── tasks.md             # /spec-kitty.tasks
```

### Source Code (repository root)

```
scripts/ci/
├── charter_pack_check.py       # WP01: module docstring states the ruling
├── validate_pack_schemas.py    # WP02: pack_files(), derived_manifest
├── charter_service_check.py    # WP02: audited walk
├── charter_pin.py              # WP03: attestation_note + subcommand
└── check_vocabulary.py         # WP04: SELF_BINDING anchors
.github/workflows/charter-track.yml   # WP03: provenance job, bump split
tests/ci/
├── test_charter_pack_check.py  # WP01
├── test_validate_pack_schemas.py  # WP02
├── test_charter_pin.py         # WP03
├── test_workflows.py           # WP03
└── test_check_vocabulary.py    # WP04
docs/guides/validate-a-pack.md  # WP01 (stray-file section), WP03 (bump/attestation section)
docs/plans/roadmap.md           # WP05
CHANGELOG.md, docs/changelog/CHANGELOG.md  # WP05
```

**Structure Decision**: existing layout; no new modules.

## Implementation Concern Map

| IC | Concern | FRs | WP |
| --- | --- | --- | --- |
| IC-01 | Stray-file gap pinned and documented | FR-001, FR-002 | WP01 |
| IC-02 | Manifest mirror parity with the charter | FR-003, FR-004, FR-005 | WP02 |
| IC-03 | Bump hardening (token split, provenance) | FR-006, FR-007, FR-008 | WP03 |
| IC-04 | Vocabulary precision | FR-009 | WP04 |
| IC-05 | Roadmap and changelog | FR-010, FR-011 | WP05 (after WP01–04) |

## Risks

- **The bump path only runs on `main` of this repository**, so it cannot be dispatched from a topic branch. Mitigations: structure tests on the parsed workflow, `actionlint` locally if available, and a note in the PR that the first rc.4 run is the live proof. #310 asks for a fork or test-branch dispatch. That proof needs operator access and is listed as a hand-off item.
- **`gh attestation verify` may need `attestations: read`** on the verifying job's token. The job declares it.
- **WP01 and WP03 both edit `validate-a-pack.md`**, in different sections. Lanes are serialized by the task finalizer if it flags the overlap.
