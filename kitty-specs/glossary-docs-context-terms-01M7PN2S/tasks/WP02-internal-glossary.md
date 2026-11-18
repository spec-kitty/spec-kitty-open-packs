---
work_package_id: WP02
title: 'Internal glossary: house terms'
dependencies:
- WP01
requirement_refs:
- FR-002
- FR-004
- NFR-002
- NFR-003
- SC-002
planning_base_branch: issue-221-234-glossary-content
merge_target_branch: issue-221-234-glossary-content
branch_strategy: Planning artifacts for this mission were generated on issue-221-234-glossary-content. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-221-234-glossary-content unless the human explicitly redirects the landing branch.
subtasks:
- T005
- T006
history: []
agent_profile: curator-carla
authoritative_surface: packs/internal/glossaries/
create_intent: []
execution_mode: code_change
model: opus
owned_files:
- packs/internal/glossaries/spk-internal-glossary.glossary.yaml
role: implementer
tags: []
tracker_refs: []
---

# WP02 — Internal glossary: house terms

## Objective

Add every `internal` row of `research/ledger.yaml` to `packs/internal/glossaries/spk-internal-glossary.glossary.yaml`.
The same `--write` run of T001 renders both contexts; this WP reviews and validates the internal half.

### Subtask T005: Review the house terms

Read the appended internal terms; fix any name the source heading made awkward (for example multi-marker test rows),
through `research/rewrites.yaml` and a re-render, never by hand-editing generated text only.

### Subtask T006: Validate

`validate-packs.sh` reports no error for internal; `check_vocabulary.py` passes; ids and names unique.
