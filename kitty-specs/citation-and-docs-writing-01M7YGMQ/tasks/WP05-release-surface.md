---
work_package_id: WP05
title: Release surface
dependencies:
- WP01
- WP02
- WP03
- WP04
requirement_refs:
- FR-014
- NFR-001
- SC-005
planning_base_branch: feat/citation-and-docs-writing
merge_target_branch: feat/citation-and-docs-writing
branch_strategy: Planning artifacts for this mission were generated on feat/citation-and-docs-writing. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/citation-and-docs-writing unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-citation-and-docs-writing-01M7YGMQ
base_commit: 268ef773321c49dc02e38d35ae4bff12e97e224c
created_at: '2026-11-21T07:58:15.221397+00:00'
subtasks:
- T016
- T017
- T018
- T019
history:
- at: '2026-11-21T08:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/pack.yaml
- packs/writing/pack.yaml
- packs/testing/pack.yaml
- packs/refactoring/pack.yaml
- packs/architecture/pack.yaml
- packs/planning-analysis/pack.yaml
- packs/built-in/pack.yaml
- packs/internal/pack.yaml
- packs/cave-kitty/pack.yaml
- packs/architecture.source.yaml
- packs/built-in.source.yaml
- packs/cave-kitty.source.yaml
- packs/drupal.source.yaml
- packs/event-driven.source.yaml
- packs/foundation.source.yaml
- packs/go.source.yaml
- packs/internal.source.yaml
- packs/java.source.yaml
- packs/javascript.source.yaml
- packs/pack-authoring.source.yaml
- packs/planning-analysis.source.yaml
- packs/python.source.yaml
- packs/qa.source.yaml
- packs/refactoring.source.yaml
- packs/rust.source.yaml
- packs/spdd.source.yaml
- packs/testing.source.yaml
- packs/writing.source.yaml
- packs/architecture/pack-manifest.yaml
- packs/built-in/pack-manifest.yaml
- packs/cave-kitty/pack-manifest.yaml
- packs/drupal/pack-manifest.yaml
- packs/event-driven/pack-manifest.yaml
- packs/foundation/pack-manifest.yaml
- packs/go/pack-manifest.yaml
- packs/internal/pack-manifest.yaml
- packs/java/pack-manifest.yaml
- packs/javascript/pack-manifest.yaml
- packs/pack-authoring/pack-manifest.yaml
- packs/planning-analysis/pack-manifest.yaml
- packs/python/pack-manifest.yaml
- packs/qa/pack-manifest.yaml
- packs/refactoring/pack-manifest.yaml
- packs/rust/pack-manifest.yaml
- packs/spdd/pack-manifest.yaml
- packs/testing/pack-manifest.yaml
- packs/writing/pack-manifest.yaml
- docs/packs/architecture.md
- docs/packs/built-in.md
- docs/packs/catalog-proposal.md
- docs/packs/cave-kitty.md
- docs/packs/drupal.md
- docs/packs/event-driven.md
- docs/packs/foundation.md
- docs/packs/go.md
- docs/packs/index.md
- docs/packs/internal.md
- docs/packs/java.md
- docs/packs/javascript.md
- docs/packs/pack-authoring.md
- docs/packs/planning-analysis.md
- docs/packs/python.md
- docs/packs/qa.md
- docs/packs/refactoring.md
- docs/packs/rust.md
- docs/packs/spdd.md
- docs/packs/testing.md
- docs/packs/writing.md
- tests/ci/test_pack_digest.py
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
---
# Work Package Prompt: WP05 – Release surface

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Branch Strategy

Planning and merge branch: `feat/citation-and-docs-writing`. Execution worktrees are allocated per computed lane from `lanes.json`.

## Objective

Version per research R5, restamp, regenerate pages, write the changelog, run every gate (spec FR-014, NFR-001).

## Subtasks

### T016 Versions

Lockstep set foundation, writing, testing, refactoring, architecture, planning-analysis 3.3.0 to 3.4.0, with their `==` pins on each other moved; built-in 5.3.0 to 5.4.0 and its `==` pins; internal 4.2.0 to 4.3.0 with its writing range `>=3.4,<4`. Check cave-kitty and every other pack's ranges still admit the new versions (follow the precedent commit "version the planning-corpus analyze checks").

### T017 Restamp

Derive manifests for changed packs, `python3 scripts/ci/pack_digest.py --update`, update the built-in digest constant in `tests/ci/test_pack_digest.py` the way the precedent does (`scripts/ci/built_in_digest.py`), `python3 scripts/docs/gen_pack_reference.py`.

### T018 Changelog

`docs/changelog/CHANGELOG.md` Unreleased: user-visible behaviour only, in the repository's changelog style: citation rules, first-hand checks, shared AI-writing tells, doc-kitty frontmatter default, versions.

### T019 Gates

All of quickstart.md, including `check_docs_freshness.py --base origin/main` and the spot-check greps; record outputs in the WP history.

## Definition of Done

All gates exit 0; versions consistent.
