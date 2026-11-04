---
work_package_id: WP05
title: Migrate event-driven
dependencies:
- WP04
requirement_refs:
- FR-005
- FR-009
planning_base_branch: feat/strict-pack-composition
merge_target_branch: feat/strict-pack-composition
branch_strategy: Planning artifacts for this mission were generated on feat/strict-pack-composition. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/strict-pack-composition unless the human explicitly redirects the landing branch.
subtasks:
- T017
- T018
- T019
history:
- at: '2026-11-04T20:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/event-driven/
create_intent: []
execution_mode: code_change
owned_files:
- packs/event-driven/**
- docs/packs/event-driven.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP05 – Migrate event-driven

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Qualify `event-driven`'s 12 references to `built-in`, in both reference forms, and declare the dependency.

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
spec-kitty agent action implement WP05 --agent claude --mission strict-pack-composition-01M6M0W4
```

## Subtasks

### T017 Qualify the references

From `reference-inventory.txt`: 7 graph edges take `built-in::<kind>:<id>`. 5 typed references (2 directive, 2 paradigm, 1 tactic) take `built-in::<id>`. **The form differs by context**, and #116's text gives the wrong one for typed references; the schema pattern is `^([a-z0-9][a-z0-9_-]*::)?[A-Za-z][A-Za-z0-9_-]*$`. Reuse the WP04 script.

A reference to `event-driven`'s own artifact stays bare. The preset's 12 entries reference nothing external (presets are self-contained), so leave them.

### T018 Declare the dependency

Add `depends_on` to `packs/event-driven/pack.yaml` as in `data-model.md`. Remove `event-driven` from `PENDING_PACKS` (out-of-map, recorded). Regenerate `docs/packs/event-driven.md`.

### T019 Validate

Re-run the scan: 0 `bare->other`. Extend the charter draft's compose test to `event-driven`, and run it. Report any refusal.

```bash
python -m unittest discover -s tests/ci
python -m unittest discover -s tests/docs
bash scripts/ci/validate-packs.sh
bash scripts/ci/check-built-in.sh
```

## Definition of Done

0 bare cross-pack references in the pack by the independent scan, compose succeeds in the charter draft, gates pass.

Record subtask completion with `spec-kitty agent tasks mark-status <ids> --status done`.

## Reviewer guidance

Check each typed reference uses the short form and each edge the long form. Check nothing else in the pack changed.
