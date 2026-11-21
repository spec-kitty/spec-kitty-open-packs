---
work_package_id: WP05
title: Release surface
dependencies:
- WP01
- WP02
- WP03
- WP04
requirement_refs:
- FR-017
- NFR-001
- C-008
- SC-007
planning_base_branch: t3/test-doctrine-2
merge_target_branch: t3/test-doctrine-2
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-2 unless the human explicitly redirects the landing branch.
subtasks:
- T019
- T020
- T021
history:
- at: '2026-11-21T08:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: docs/changelog/
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/pack.yaml
- packs/testing/pack.yaml
- packs/writing/pack.yaml
- packs/refactoring/pack.yaml
- packs/architecture/pack.yaml
- packs/planning-analysis/pack.yaml
- packs/built-in/pack.yaml
- packs/python/pack.yaml
- packs/java/pack.yaml
- packs/javascript/pack.yaml
- packs/pack-authoring/pack.yaml
- packs/internal/pack.yaml
- packs/*/pack-manifest.yaml
- packs/*.source.yaml
- docs/packs/*.md
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
tracker_refs: []
---
# Work Package Prompt: WP05 – Release surface

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

FR-017 and NFR-001: version, restamp and document. Read `research.md` (R9) and DIRECTIVE_018.

## Branch Strategy

Planning branch and merge target: `t3/test-doctrine-2`. Implement with `spec-kitty agent action implement WP05 --agent <name> --mission test-doctrine-2-01M7YH30`.

## Subtasks

### T019 — Versions

Minor bump: the foundation lockstep set (foundation, writing, testing, refactoring, architecture, planning-analysis) and built-in, including every `==` depends_on range pinned to the lockstep version across all packs; python, java, javascript, pack-authoring, internal to their next minor. Confirm org-pack ranges still admit the new lockstep version.

### T020 — Restamp

Regenerate pack manifests the way the repository does (see CONTRIBUTING and `validate-packs.sh --derived-manifests`), `python3 scripts/ci/pack_digest.py --update`, `python3 scripts/docs/gen_pack_reference.py` (regenerate, never hand-edit `docs/packs/`).

### T021 — Changelog and gates

`docs/changelog/CHANGELOG.md` under `## [Unreleased]`: user-visible behaviour only, citing #216, #154, #147, #152 and the partial #273/#274. Run every NFR-001 gate.

## Definition of Done

All NFR-001 gates exit 0 locally; changelog entry present. If Mission D merged first, rebase and restamp.
