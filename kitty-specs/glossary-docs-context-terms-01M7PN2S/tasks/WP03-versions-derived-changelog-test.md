---
work_package_id: WP03
title: Versions, derived outputs, changelog and the glossary content test
dependencies:
- WP04
requirement_refs:
- FR-008
- FR-009
- FR-010
- FR-011
- NFR-001
- C-003
- C-004
- C-005
- C-006
- SC-004
planning_base_branch: issue-221-234-glossary-content
merge_target_branch: issue-221-234-glossary-content
branch_strategy: Planning artifacts for this mission were generated on issue-221-234-glossary-content. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-221-234-glossary-content unless the human explicitly redirects the landing branch.
subtasks:
- T007
- T008
- T009
- T010
- T011
history: []
agent_profile: python-pedro
authoritative_surface: packs/
create_intent:
- tests/ci/test_glossary_content.py
execution_mode: code_change
model: opus
owned_files:
- packs/*/pack.yaml
- packs/*/pack-manifest.yaml
- packs/*.source.yaml
- docs/packs/*.md
- docs/changelog/CHANGELOG.md
- tests/ci/test_glossary_content.py
role: implementer
tags: []
tracker_refs: []
---

# WP03 — Versions, derived outputs, changelog and the glossary content test

### Subtask T007: Versions (DIRECTIVE_018)

foundation 2.0.0 → 2.1.0, internal 4.0.0 → 4.1.0. Every pack whose `depends_on` pins foundation `==2.0.0` moves the pin
to `==2.1.0` and takes a minor bump; their own exact pinners follow the same way.

### Subtask T008: Derived outputs

`python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/<pack>` for every changed pack;
`python3 scripts/ci/pack_digest.py --update`; `python3 scripts/docs/gen_pack_reference.py`.

### Subtask T009: Changelog

`[Unreleased]` entry: terms added (counts), Op, header, ledger location, versions.

### Subtask T010: Unit test

`tests/ci/test_glossary_content.py`: the Op term (id, active, alias `profile invocation`, sees `mission`); the four
mission types; no `src/`, `tests/` or core ADR citation in `spec-kitty-core`; no "migrated from" in its description;
unique ids and names in both contexts.

### Subtask T011: Full gate run

validate-packs (with `--cross-pack`), `check-pack-digests.sh`, `check_vocabulary.py`, `gen_pack_reference.py --check`,
every `tests/*` unittest suite.
