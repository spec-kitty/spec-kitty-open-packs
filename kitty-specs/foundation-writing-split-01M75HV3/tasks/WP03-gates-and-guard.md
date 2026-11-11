---
work_package_id: WP03
title: Gates and the manifest guard
dependencies:
- WP01
- WP02
requirement_refs:
- FR-011
- FR-012
- FR-013
- NFR-003
- SC-001
- SC-002
planning_base_branch: feat/73-foundation-writing-split
merge_target_branch: feat/73-foundation-writing-split
branch_strategy: Planning artifacts for this mission were generated on feat/73-foundation-writing-split. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/73-foundation-writing-split unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-foundation-writing-split-01M75HV3
base_commit: c161e4f509ce44bd1adf59b9b5e90707bfe1ace3
created_at: '2026-11-11T16:39:54.997151+00:00'
subtasks:
- T012
- T013
- T014
- T015
history:
- at: '2026-11-11T15:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: scripts/ci/
create_intent: []
execution_mode: code_change
owned_files:
- scripts/ci/**
- tests/**
- packs/built-in.source.yaml
- .github/workflows/**
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP03 – Gates and the manifest guard

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Make every gate understand three built-in-level packs, and land the #182 manifest-completeness guard.

## Branch Strategy

- Planning/base branch and final merge target: `feat/73-foundation-writing-split`.
- The workspace is resolved by `spec-kitty agent action implement WP03 --agent claude --mission foundation-writing-split-01M75HV3`.

## Context

`research/4-gates.md` has every hard-coded site with file:line, and the 8-line diff for the service check proven in scratch: `research/exp-charter_service_check.diff` in the session scratchpad. Re-derive it if it is absent.

## Subtasks

### T012 Charter service check

- Stage every pack whose `pack.yaml` declares `pack_level: built-in` into the fixture and registration roots, instead of `packs/built-in` alone (lines ~64, 381-388, 419, 430).
- The "every non-built-in pack is org/project" refusal must exclude the built-in-level packs.
- Compose and register: each built-in-level pack, each org pack (all ten bundles included), and all of them together.

### T013 #182 guard

- In `validate_pack()`, next to the stale-manifest check: for packs with a `pack-manifest.yaml`, every file-backed doctrine artifact on disk must be a constituent, and every constituent path must exist.
- Kinds covered: agent profiles, directives, tactics, procedures, paradigms, styleguides, toolguides, assets, glossary packs, file-backed templates.
- Exempt: actions, anti-patterns, mission types and step contracts.
- Unit tests in `tests/ci/test_validate_pack_schemas.py`, using temp-dir fixtures:
  - missing entry → error naming the file;
  - dangling entry → error naming the entry;
  - pack without a manifest → no finding.

### T014 Digest, vocabulary and tests

- `python3 scripts/ci/built_in_digest.py` to re-record `packs/built-in.source.yaml` `tree_digest`. Update the comment to say built-in is now the distribution pack.
- `check_vocabulary.py:75`: the provenance row names a moved file; point it at its new path.
- `tests/**/test_language_profile_styleguides.py` and `test_software_dev_ascii.py` read built-in paths. Point them at the new packs so they still examine files: add a non-vacuity floor if missing.

### T015 Run every gate

Run each quickstart command. The service check uses `JAVA_HOME=/usr/lib/jvm/temurin-25` and the jar built from the pin. Record the outputs in the WP's review notes.

## Definition of Done

- All gates are green locally (docs-site excepted; it is CI only).
- The guard tests pass and fail on the fixtures as specified.
