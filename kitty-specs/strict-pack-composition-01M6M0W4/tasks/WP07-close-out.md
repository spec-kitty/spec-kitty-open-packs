---
work_package_id: WP07
title: Close-out
dependencies:
- WP06
requirement_refs:
- FR-014
- FR-015
- FR-016
- C-001
- C-006
- C-007
- C-008
- NFR-003
planning_base_branch: feat/strict-pack-composition
merge_target_branch: feat/strict-pack-composition
branch_strategy: Planning artifacts for this mission were generated on feat/strict-pack-composition. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/strict-pack-composition unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-strict-pack-composition-01M6M0W4
base_commit: 5383238a02f4e91a7d41bd52fbad4d1f3e9d968a
created_at: '2026-11-05T01:18:51.077495+00:00'
subtasks:
- T024
- T025
- T026
- T027
- T028
history:
- at: '2026-11-04T20:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: docs/
create_intent:
- docs/architecture/adr/2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility.md
execution_mode: code_change
owned_files:
- docs/guides/compose-packs.md
- docs/architecture/adr/index.md
- docs/changelog/CHANGELOG.md
- docs/guides/index.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP07 – Close-out

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Remove the allowance, record the decision, state the new reality, correct the stale record, and hand off a draft charter pull request that is ready to re-point.

## Branch Strategy

- Planning/base branch: `feat/strict-pack-composition`. Final merge target: `feat/strict-pack-composition`, which reaches `main` by pull request after the mission.
- The workspace is resolved by `spec-kitty agent action implement`; trust the path it prints.

## Context

Read first: `kitty-specs/strict-pack-composition-01M6M0W4/spec.md`, `plan.md`, `data-model.md`, `research.md`. The full site list is `reference-inventory.txt` in the same folder.

Local tools. `python3 -m venv` fails on this machine; use the spec-kitty venv:

```bash
export PATH=~/Documents/code/kitty/spec-kitty/.venv/bin:$PATH
```

Git identity is not configured here. Pass it per command, do not edit config:
`GIT_AUTHOR_NAME="Stijn Dejongh" GIT_AUTHOR_EMAIL="stijn.dejongh@sddevelopment.be" GIT_COMMITTER_NAME="Stijn Dejongh" GIT_COMMITTER_EMAIL="stijn.dejongh@sddevelopment.be"`.

Pause and report, rather than deciding, on: changing an existing test's asserted expectation, any contract change, widening scope past this WP, or a mission runtime failure (C-005).

Implement with:

```bash
spec-kitty agent action implement WP07 --agent claude --mission strict-pack-composition-01M6M0W4
```

## Subtasks

### T024 Delete the allowance

`PENDING_PACKS` should be empty after WP06. Delete it and the code that consults it (out-of-map, recorded). Run the gates: this is SC-005. Prove it works by planting one bare cross-pack reference in a scratch copy and seeing the gate fail.

### T025 ADR and changelog

Write an ADR under `docs/architecture/adr/` from `adr-template.md`, and add it to `index.md`: the packs follow strict composition, the as-is CLI is no longer supported, the tag `pre-charter-cutover` marks the last semi-compatible commit, the two reference forms, the pack names including why `quality-assurance` differs from its directory, and the `>=1.0,<2` range. It should state the accepted consequence: this repository's own `.kittify/config.yaml` packs stop loading under the as-is CLI.

Add a `### 💥 Breaking` changelog entry in `docs/changelog/CHANGELOG.md`. Say what a consumer must now do. Bump `updated:` on any page you edit.

### T026 Guides

`docs/guides/compose-packs.md:64` says no pack carries `depends_on` yet. Replace the illustrative example with the real one, and state both reference forms. Check `docs/` for other statements this mission made false: `git grep -n "depends_on\|pack.yaml" -- docs ':!docs/packs'`. The older core-era command wording is a separate follow-up, so leave that alone and say so.

### T027 Correct the record

Update issue text, which research found stale. This is an outward action in scope of FR-016:

- #47: `internal` already has `pack_level`; correct the state table.
- #113: 78 sites, 31 targets; and the two forms.
- #116: the two forms.
- #118: the table, plus the validator work no issue tracked.
- #72: comment that its target `missions/<type>/mission.yaml` matches a retired, refused rule in `contracts/packs/file-kinds.yaml`.
- spec-kitty-charter#363: scope is every pack and reads the corpus checkout. spec-kitty-charter#365 is closed; add a comment rather than editing its body.
- File an issue in spec-kitty/spec-kitty linking core's `_anchor_for` (`src/charter/offering/assets/repository.py:164-173`) with spec-kitty/spec-kitty#7153: core's asset resolver breaks at its next pin bump.
- File the FR-011 follow-up if WP04 left the profile references bare.

Report the URLs.

### T028 Finish the charter draft

On the draft pull request: fix the guide's typed-reference example (`docs/guides/compose-packs.md` there), and make the atomic bump ready: `openPacksRef`, `packs/open-packs.lock.yaml`, the three `OpenPacksCorpus.DIAGNOSTICS` entries, the 6-finding assertion in `FileSystemPackInspectorTest`, the six `whole-pack/known-failures.yaml` entries, the compose test. Widen #363's scope per the above. Check whether charter #360 changes the compose's roots.

**Do not merge it, and do not point it at `main` yet** (C-006): it cannot be re-pointed until this mission's pull request merges, because a rebase merge changes the SHA. Say this plainly in the hand-off, because it is the last step of FR-014 and the operator must trigger it.

```bash
python -m unittest discover -s tests/ci
python -m unittest discover -s tests/docs
bash scripts/ci/validate-packs.sh
bash scripts/ci/check-built-in.sh
```

## Definition of Done

No allowance remains, the ADR and changelog exist, guides are true, stale issues are corrected with URLs reported, and the charter draft is green against this mission's head with the re-pointing step named in the hand-off.

Record subtask completion with `spec-kitty agent tasks mark-status <ids> --status done`.

## Reviewer guidance

Run SC-003's independent scan once more. Read the ADR as a stranger would. Check the follow-through for FR-014 is explicit, not implied.
