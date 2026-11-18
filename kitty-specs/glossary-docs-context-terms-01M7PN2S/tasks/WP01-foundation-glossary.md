---
work_package_id: WP01
title: 'Foundation glossary: consumer terms, the Op term and the authoring-source header'
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-005
- FR-006
- FR-007
- NFR-002
- NFR-003
- C-001
- C-002
- SC-001
- SC-002
- SC-003
planning_base_branch: issue-221-234-glossary-content
merge_target_branch: issue-221-234-glossary-content
branch_strategy: Planning artifacts for this mission were generated on issue-221-234-glossary-content. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-221-234-glossary-content unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
history: []
agent_profile: curator-carla
authoritative_surface: packs/foundation/glossaries/
create_intent: []
execution_mode: code_change
model: opus
owned_files:
- packs/foundation/glossaries/spec-kitty-core.glossary.yaml
role: implementer
tags: []
tracker_refs: []
---

# WP01 — Foundation glossary: consumer terms, the Op term and the authoring-source header

## Objective

Add every `foundation` row of `research/ledger.yaml` to `packs/foundation/glossaries/spec-kitty-core.glossary.yaml`,
including the Op term (#234) and the four mission types, and replace the stale "migrated from spec_kitty_core.yaml"
description with one that names the file as the authoring source.

### Subtask T001: Render the consumer terms

Run `python3 tools/render_terms.py <core>/docs/context . <repo> --write` from the mission directory (core checkout at
`01e577d`). It appends the new terms as text, so existing terms keep their bytes. Check `--flag` lists nothing first.

### Subtask T002: Add the alias of an existing term by hand

The tool prints `alias of an existing term`: add `WorkPackage` to the `aliases` of `work-package`.

### Subtask T003: Authoring-source description and header

Replace `description` and the header comment: the file is the authoring source, edited by hand through the
glossary-curation workflow (`writing::procedure glossary-maintenance-workflow`, tactic `glossary-curation-interview`).

### Subtask T004: Validate

`validate-packs.sh` reports no error for foundation; `check_vocabulary.py` passes; ids and names unique; every
`see_also` resolves.
