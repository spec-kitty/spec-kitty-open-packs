---
work_package_id: WP05
title: Versions, changelog, digests and pages
dependencies:
- WP01
- WP02
- WP03
- WP04
requirement_refs:
- FR-010
- NFR-001
- C-002
planning_base_branch: issue-233-enforcement-vocabulary
merge_target_branch: issue-233-enforcement-vocabulary
branch_strategy: Planning artifacts for this mission were generated on issue-233-enforcement-vocabulary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-233-enforcement-vocabulary unless the human explicitly redirects the landing branch.
subtasks:
- T018
- T019
- T020
- T021
history:
- at: '2026-11-18T07:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
owned_files:
- packs/*/pack.yaml
- packs/*/pack-manifest.yaml
- packs/*.source.yaml
- docs/packs/**
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
tracker_refs:
- '#233'
---
# Work Package Prompt: WP05 – Versions, changelog, digests and pages

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load implementer-ivan` before reading anything else.

## Objective

The release surface reflects the change and every gate is green (FR-010, NFR-001).

## Subtasks

### T018 Versions (DIRECTIVE_018; operator question Q4)

- Recommendation A (sent to the operator 2026-11-18): the built-in-level packs (foundation, writing, built-in) keep their unreleased `[Unreleased]` versions (2.0.0, 2.0.0, 4.0.0), and the change folds into them as #258 did, so no exact pin moves. The org packs whose tree changes take a bump, because the charter service answers 409 on re-registration at the same version with new content (#194): pack-authoring 1.2.0 -> 1.3.0 (additive principle), and qa 4.0.0 -> 4.0.1, internal 4.0.0 -> 4.0.1, cave-kitty 2.2.0 -> 2.2.1 (wording).
- If the operator picks the lockstep option instead: foundation and writing go to 2.1.0 and built-in to 4.1.0, and every exact pin moves (writing, testing, refactoring, architecture and planning-analysis pin foundation; architecture pins writing; built-in pins all of them), with restamps and bumps for each.
- Derive the changed-pack list from `git diff --stat origin/main -- packs/`.

### T019 Manifests, digests, pages

- `python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/<name>` for each changed pack (titles are in manifests? check), `python3 scripts/ci/pack_digest.py` restamp (see its `--help`), `python3 scripts/docs/gen_pack_reference.py`.

### T020 Changelog

- `CHANGELOG.md` is a symlink to `docs/changelog/CHANGELOG.md`; edit the real file, bump its frontmatter `updated:`, and use the existing emoji headings (`### 🔄 Changed`).

- One `### Changed` (or the section the Unreleased block uses) entry: the levels are defined once; prose is swept; the field stays as the default (ADR); the guard rule; the version list. No upgrade action is needed by adopters; QA_001 is retitled.

### T021 Gates

- `scripts/ci/validate-packs.sh` and `--cross-pack`, `scripts/ci/check-pack-digests.sh`, `check_vocabulary.py`, `gen_pack_reference.py --check`, and the five unittest suites (`tests/release`, `tests/vocabulary`, `tests/ci`, `tests/docs`, `tests/assets`). Record the results in the WP review.
## Branch Strategy

Planning and merge branch: `issue-233-enforcement-vocabulary` (topology `single_branch`, no lane worktree). The pull request goes from `issue-233-enforcement-vocabulary` to `main`. Implement with `spec-kitty agent action implement <WP> --agent claude --mission enforcement-vocabulary-01M7PMJW`.

