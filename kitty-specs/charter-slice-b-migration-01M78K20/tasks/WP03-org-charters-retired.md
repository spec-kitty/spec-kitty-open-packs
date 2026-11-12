---
work_package_id: WP03
title: Org charters retired
dependencies:
- WP02
requirement_refs:
- FR-006
- FR-007
planning_base_branch: feat/slice1-readme-retire-org-charter
merge_target_branch: feat/slice1-readme-retire-org-charter
branch_strategy: Planning artifacts for this mission were generated on feat/slice1-readme-retire-org-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/slice1-readme-retire-org-charter unless the human explicitly redirects the landing branch.
subtasks:
- T011
- T012
- T013
- T014
agent: claude
history:
- at: '2026-11-12T19:25:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
owned_files:
- packs/*/org-charter.yaml
- packs/*/pack.yaml
- packs/internal/presets/base.yaml
- packs/go/presets/go.yaml
- packs/rust/presets/rust.yaml
- tests/fixtures/valid/example-pack/**
role: implementer
tags: []
tracker_refs:
- '#242'
---
# Work Package Prompt: WP03 – Org charters retired (#242)

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load implementer-ivan` before reading anything else.

## Objective

No pack or fixture holds `org-charter.yaml`, no `pack.yaml` declares `active_charter`, and `internal`'s
required floor is the `base` preset's must-have items.

## Subtasks

- **T011** `packs/internal/presets/base.yaml`: exactly #242's listing (3 directives, 7 procedures, 1 glossary
  pack, 2 toolguides, 5 skills, all `must_have: true`), header comment rewritten. Verify every id exists in
  `internal`. No `policy.yaml`. `pack.yaml`: drop `active_charter`; header comment (lines 6-9) and the
  provenance pointer (line 3, now the README's Provenance section) rewritten. `skill_namespace` goes with the file.
- **T012** cave-kitty, drupal, event-driven, go, java, javascript, pack-authoring, python, qa, rust, spdd: delete
  `org-charter.yaml` and the `active_charter` line; rewrite header comments that mention the active charter.
- **T013** `presets/go.yaml` and `presets/rust.yaml` descriptions: "Registering the pack activates nothing, so
  this preset is the opt-in".
- **T014** `tests/fixtures/valid/example-pack/`: delete `org-charter.yaml` and `active_charter`; header
  comment rewritten.

## Done when
`git ls-files | grep -i org-charter.yaml` and `git grep -n active_charter -- packs tests` are empty;
`validate_pack_schemas.py` passes.
