---
work_package_id: WP06
title: Migrate internal
dependencies:
- WP05
requirement_refs:
- FR-005
- FR-006
- FR-010
planning_base_branch: feat/strict-pack-composition
merge_target_branch: feat/strict-pack-composition
branch_strategy: Planning artifacts for this mission were generated on feat/strict-pack-composition. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/strict-pack-composition unless the human explicitly redirects the landing branch.
subtasks:
- T020
- T021
- T022
- T023
history:
- at: '2026-11-04T20:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/internal/
create_intent:
- packs/internal/glossary_packs/spk-internal-glossary.glossary-pack.yaml
execution_mode: code_change
owned_files:
- packs/internal/**
- docs/packs/internal.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP06 – Migrate internal

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Qualify `internal`'s 78 references to 31 `built-in` targets, and finish #47's glossary rename. This is the largest migration, and it goes last because `internal` carries this repository's own governance (C-005).

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
spec-kitty agent action implement WP06 --agent claude --mission strict-pack-composition-01M6M0W4
```

## Subtasks

### T020 Qualify the references

From `reference-inventory.txt`: 57 edges in `packs/internal/drg/fragment.yaml` take `built-in::<kind>:<id>`, including the 5 `agent_profile` edges (`planner-priti` x4, `reviewer-renata` x1) that the epic missed; leaving those bare is refused `pack_reference_unqualified`, as an executed research mutant shows. 19 procedure references and 2 tactic references across 7 files take `built-in::<id>`. Reuse the WP04 script.

Leave alone: `internal`'s own 155 bare references, the 13 bare references no pack holds (all prose), and prose mentions. The issue's "13 references" is out of date; use the inventory.

### T021 Declare the dependency

Add `depends_on` to `packs/internal/pack.yaml` as in `data-model.md`. It already has `pack_level: org`, despite what #47 says. Keep `name: spec-kitty-internal` and the existing `pack_id`. Remove `internal` from `PENDING_PACKS` (out-of-map, recorded).

### T022 Rename the glossary pack (#47)

`packs/internal/org-charter.yaml:15-16` requires `spk-internal-glossary`, but the file's stem is `spk-internal`. Rename `packs/internal/glossary_packs/spk-internal.glossary-pack.yaml` to `spk-internal-glossary.glossary-pack.yaml` with `git mv`, leaving its `id` alone. Update the references to it: `git grep -n "spk-internal.glossary-pack\|glossary_packs/spk-internal"`, and #47 says `packs/internal/drg/fragment.yaml` has some. Classify each hit and report them. This causes no refusal; it is here to close #47.

### T023 Validate

Regenerate `docs/packs/internal.md`. Re-run the scan: 0 `bare->other` for every pack. Extend the charter draft's compose test to `internal`, and to all five together. Repeat the C-005 runtime check from WP04 (T015) with this tree. Same rule: if `next` or `dispatch` fail, stop and report.

#92, #105 and #106 touch `semi-auto-delivery.procedure.yaml` and the fragment. If any has landed, whoever is second rebases. Do not run them alongside this WP.

```bash
python -m unittest discover -s tests/ci
python -m unittest discover -s tests/docs
bash scripts/ci/validate-packs.sh
bash scripts/ci/check-built-in.sh
```

## Definition of Done

78 references qualified, scan shows 0 `bare->other` across all packs, all five packs compose, runtime check reported, gates pass, `PENDING_PACKS` is empty.

Record subtask completion with `spec-kitty agent tasks mark-status <ids> --status done`.

## Reviewer guidance

Spot-check the 5 `agent_profile` edges. Compare a sample of typed references with the schema pattern. Check the diff has no reformatting. Check the governance consequence is reported as accepted (C-001), not hidden.
