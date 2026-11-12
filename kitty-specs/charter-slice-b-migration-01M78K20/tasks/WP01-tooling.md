---
work_package_id: WP01
title: Tooling follows the slice B file rules
dependencies: []
requirement_refs:
- FR-001
- FR-008
- FR-012
planning_base_branch: feat/slice1-readme-retire-org-charter
merge_target_branch: feat/slice1-readme-retire-org-charter
branch_strategy: Planning artifacts for this mission were generated on feat/slice1-readme-retire-org-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/slice1-readme-retire-org-charter unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-charter-slice-b-migration-01M78K20
base_commit: e5b94f6ab8b40dc3bc8cd16c54658409a0612941
created_at: '2026-11-12T19:21:26.042624+00:00'
subtasks:
- T001
- T002
- T003
- T004
- T005
agent: claude
history:
- at: '2026-11-12T19:25:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: scripts/
create_intent: []
execution_mode: code_change
owned_files:
- scripts/ci/charter_service_check.py
- scripts/ci/validate_pack_schemas.py
- scripts/ci/check_vocabulary.py
- scripts/docs/gen_pack_reference.py
- tests/ci/test_charter_service_check.py
- tests/ci/test_validate_pack_schemas.py
- tests/vocabulary/test_check_vocabulary.py
- tests/docs/test_gen_pack_reference.py
- charter.lock.yaml
role: implementer
tags: []
tracker_refs:
- '#241'
- '#242'
---
# Work Package Prompt: WP01 – Tooling follows the slice B file rules

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load implementer-ivan` before reading anything else.

## Objective

The CI scripts treat the root `README.md` as the pack document and stop excluding retired files, against charter
`17ce3f9` (already pinned in `charter.lock.yaml`).

## Subtasks

### T001 — Baseline service check at the pin
Build the jar (`scripts/ci/charter_service_jar.sh <work>`, Java 25) and run
`scripts/ci/charter_service_check.py --jar <jar>` on the unchanged packs. Expected: `retired` for the 35
`pack.md`/`PROVENANCE.md` files once uploaded, and `pack_unreadable` (`active_charter`) for the 12 packs. Any
other refusal is reported in the PR and fixed here only if small.

### T002 — `NOT_REGISTERED`
Remove `README.md`, `PROVENANCE.md` and `org-charter.yaml`. The two template entries are now excluded by the
charter itself: remove them too if the service check still passes without them, else keep them. Update the
module docstring comment above the tuple and `tests/ci/test_charter_service_check.py`.

### T003 — `validate_pack_schemas.py`
The pre-check at the pack-level-files branch keys on `README.md` instead of `pack.md`; drop
`*/PROVENANCE.md` from `UNCLASSIFIED_ALLOWANCES`; fix the docstring that names `pack.md` as a Markdown
companion. Update `tests/ci/test_validate_pack_schemas.py`.

### T004 — `check_vocabulary.py`
The `PROVENANCE_PHRASES` row for `packs/qa/PROVENANCE.md` reads `packs/qa/README.md`. Update
`tests/vocabulary/test_check_vocabulary.py`.

### T005 — Generator
`read_pack_document` reads `README.md` (same rule: text between the H1 and the first H2, outside fences). Fallback
texts name the README. Update docstrings and `tests/docs/test_gen_pack_reference.py`. Do not regenerate pages
here (WP04).

## Done when
`pytest tests/ci tests/docs tests/vocabulary` passes; `git grep -n "pack\.md\|PROVENANCE" scripts tests` shows no live use.
