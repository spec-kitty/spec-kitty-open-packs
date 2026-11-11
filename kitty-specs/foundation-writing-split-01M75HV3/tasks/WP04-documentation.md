---
work_package_id: WP04
title: Documentation
dependencies:
- WP01
- WP02
- WP03
requirement_refs:
- FR-014
- C-001
- C-004
planning_base_branch: feat/73-foundation-writing-split
merge_target_branch: feat/73-foundation-writing-split
branch_strategy: Planning artifacts for this mission were generated on feat/73-foundation-writing-split. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/73-foundation-writing-split unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-foundation-writing-split-01M75HV3
base_commit: bc5f1d9a6bb89c22c166de692b4be97bf9ccb18e
created_at: '2026-11-11T16:49:51.296225+00:00'
subtasks:
- T016
- T017
- T018
history:
- at: '2026-11-11T15:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: docs/
create_intent:
- docs/architecture/adr/2026-11-11-1-split-built-in-into-foundation-and-writing.md
- docs/packs/foundation.md
- docs/packs/writing.md
- docs/packs/testing.md
- docs/packs/refactoring.md
- docs/packs/architecture.md
- docs/packs/planning-analysis.md
- docs/packs/adversarial-review.md
- docs/packs/pack-authoring.md
- docs/packs/python.md
- docs/packs/javascript.md
- docs/packs/drupal.md
- docs/packs/java.md
execution_mode: code_change
owned_files:
- docs/**
- CHANGELOG.md
- README.md
- packs/README.md
- site/**
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP04 – Documentation

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Record the split for readers and consumers: why it happened, what moved, and how to migrate. Follow Common Docs (DIRECTIVE_042/047) and SPEC_KITTY_DOCS_CONVENTIONS: touched pages carry `audience:` and `doc_status`.

## Branch Strategy

- Planning/base branch and final merge target: `feat/73-foundation-writing-split`.
- The workspace is resolved by `spec-kitty agent action implement WP04 --agent claude --mission foundation-writing-split-01M75HV3`.

## Subtasks

### T016 ADR and CHANGELOG

ADR `docs/architecture/adr/2026-11-11-1-split-built-in-into-foundation-and-writing.md`, using the repo template. Add it to the ADR index. It records:
- built-in as distribution pack, the pack graph and levels;
- foundation (basis + how-to layer), writing, the ten opt-in bundles and the bundle DAG; the squad research;
- the edge relocation rule;
- the missions/ name kept;
- the java-in-built-in option left open;
- the core consequence: core fetches only built-in, which is out of scope per AGENTS.md.

CHANGELOG `## Unreleased` gets a **💥 Breaking** entry covering:
- built-in 2.0.0 holds nothing;
- deployers must place foundation and writing;
- `built-in::X` references must become `foundation::`/`writing::`/`<bundle>::`;
- `<2` ranges on built-in;
- specialist content (architecture, refactoring, testing, stacks, …) is now opt-in via the bundles.

Add a migration note with numbered steps.

### T017 READMEs and catalog

- Root README pack table.
- `packs/README.md`, which is already stale at lines ~31-33.
- `docs/packs/index.md` and `catalog-proposal.md` status lines.
- Guides that name `packs/built-in/<kind>` paths for content that moved.

### T018 Generated pages

- `python3 scripts/docs/gen_pack_reference.py` to write pages for foundation, writing and the ten bundles, and regenerate built-in and the org packs.
- Add nav entries if the site config lists pages explicitly.
- `--check` must be green.

## Definition of Done

- `gen_pack_reference.py --check` and `check_vocabulary.py` are green.
- The ADR is indexed and the CHANGELOG entry is present.
