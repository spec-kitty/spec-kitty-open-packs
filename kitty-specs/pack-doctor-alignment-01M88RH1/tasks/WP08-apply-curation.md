---
work_package_id: WP08
title: Apply the curation to packs/
dependencies: []
requirement_refs:
- FR-007
- FR-008
- FR-009
- SC-003
planning_base_branch: feat/pack-doctor-alignment
merge_target_branch: feat/pack-doctor-alignment
branch_strategy: Planning artifacts for this mission were generated on feat/pack-doctor-alignment. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/pack-doctor-alignment unless the human explicitly redirects the landing branch.
subtasks:
- T039
- T040
- T041
- T042
- T043
phase: Phase 3 - Content and derived artifacts
history:
- at: '2026-11-25T07:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator-carla
authoritative_surface: packs/
create_intent:
- packs/writing/anti_pattern.graph.yaml
execution_mode: code_change
model: ''
owned_files:
- packs/*/anti_patterns/**
- packs/*/styleguides/**
- packs/*/procedures/**
- packs/*/drg/fragment.yaml
- packs/*/*.graph.yaml
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP08 - Apply the curation to packs/

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `curator-carla`
- **Agent/tool**: `claude`

---

## IMPORTANT: Review Feedback

Check `review_ref` with `spec-kitty agent tasks status --mission pack-doctor-alignment-01M88RH1`. Address every item.

---

## Objectives & Success Criteria

- The tree carries every approved ledger, applied by `curation/apply_curation.py`. Hand edits are made only where T043 records a fix.
- **SC-003**: 0 styleguides or procedures carry `anti_patterns`, and 0 `anti_pattern` nodes lack a file.
- `apply_curation.py --check --root .` exits 0.
- pack-doctor `validate --round-trip --full` over the set runs `CLOSURE` and `REFERENCES` (nothing is `skipped`). Each remaining violation is either fixed here or listed as owned by WP09: only `manifest_*` and the `round_trip_*` codes caused by unstamped manifests may remain.

## Context & Constraints

- **Depends on**: WP02-WP07, all approved. Every ledger must have no open `operator_question`.
- **Read**: `curation/README.md`, `data-model.md`, `plan.md` IC-03 and IC-04.
- **Do not touch** `pack-manifest.yaml`, `*.source.yaml` or `docs/packs/`. They belong to WP09, which restamps after this WP.

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`; lanes come from `lanes.json`.
- `spec-kitty agent action implement WP08 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T039 - Apply ledger 00

- Run `python3 kitty-specs/pack-doctor-alignment-01M88RH1/curation/apply_curation.py --root . --ledger …/ledger-00-nodes.yaml`, then commit it.
- The 15 `drg_schema_error` are gone.

### Subtask T040 - Apply ledgers A-E

- Apply one ledger per commit, in A-E order, so each commit maps to one approved review.
- After each one, run `git diff --stat`. The changes must touch only that batch's packs.

### Subtask T041 - `--check` over the tree

- `apply_curation.py --check --root .` exits 0.
- `grep -rln "^anti_patterns:" packs` is empty.

### Subtask T042 - Measure

- Run pack-doctor `validate --round-trip --full` over `packs/*` and `tests/fixtures/valid/*`, using the jar from `scripts/ci/charter_pack_doctor_jar.sh` (WP01). If WP01 has not landed in this lane, build it with `quickstart.md` step 1 against the pinned commit.
- Record in the WP history:
  - the `checks` list and `skipped` (which must be empty);
  - the counts per code.
- This is the first time `CLOSURE` and `REFERENCES` run over the set (`research.md` R3). Expect possible new codes, such as `preset_item_*`, `pack_reference_*` or `substep_*`.

### Subtask T043 - Fix or raise each remaining fault

- `manifest_membership`, `manifest_stale` and the knock-on `round_trip_*` are WP09's, so list them and leave them.
- For any other code:
  - **A fault this curation caused** (a bad edge, a wrong owner, a missing `depends_on` for a cross-pack merge): fix it in the ledger, through a review on the owning ledger WP, and re-apply. Never hand-patch around a ledger.
  - **A pre-existing fault the skipped checks hid**: if a fix is within the pack content and its meaning is unambiguous, fix it here in its own commit, with its rationale in history. Otherwise raise it to the dispatcher as an operator question, and record it as a deferral for the PR body.

## Risks & Mitigations

- **Surprises from CLOSURE and REFERENCES.** Budget for them. Each one is either a fix with its own commit or a raised question.

## Review Guidance

- Confirm that each commit equals a pure apply of an approved ledger: re-run the apply on the parent commit, and diff the result.
- Confirm that `--check` passes and that the pack-doctor counts are pasted in the history.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
