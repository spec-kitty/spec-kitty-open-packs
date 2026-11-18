---
work_package_id: WP05
title: Versions, changelog, digests and pages
dependencies: [WP01, WP02, WP03, WP04]
requirement_refs:
- FR-010
- NFR-001
- C-002
planning_base_branch: issue-233-enforcement-vocabulary
merge_target_branch: issue-233-enforcement-vocabulary
branch_strategy: Planning artifacts for this mission were generated on issue-233-enforcement-vocabulary. The mission is single_branch, so this WP is implemented on issue-233-enforcement-vocabulary and lands there; the pull request goes from issue-233-enforcement-vocabulary to main.
subtasks: [T018, T019, T020, T021]
agent: claude
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
- CHANGELOG.md
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

### T018 Versions (DIRECTIVE_018)

- Minor bump for every pack whose tree changed (nothing is removed or renamed; no rule is tightened): expected foundation 2.0.0 -> 2.1.0, writing 2.0.0 -> 2.1.0, qa, internal and cave-kitty (whose README is in the digest), and pack-authoring. Derive the actual list from `git diff --stat origin/main -- packs/`.
- built-in: lockstep. Its `depends_on` pins (`==2.0.0` for foundation and writing) move to `==2.1.0`, and built-in itself takes a minor bump. Check every dependant's range (`>=2.0,<3`) still admits the new versions.

### T019 Manifests, digests, pages

- `python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/<name>` for each changed pack (titles are in manifests? check), `python3 scripts/ci/pack_digest.py` restamp (see its `--help`), `python3 scripts/docs/gen_pack_reference.py`.

### T020 Changelog

- One `### Changed` (or the section the Unreleased block uses) entry: the levels are defined once; prose is swept; the field stays as the default (ADR); the guard rule; the version list. No upgrade action is needed by adopters; QA_001 is retitled.

### T021 Gates

- `scripts/ci/validate-packs.sh` and `--cross-pack`, `scripts/ci/check-pack-digests.sh`, `check_vocabulary.py`, `gen_pack_reference.py --check`, and the four unittest suites. Record the results in the WP review.
## Branch Strategy

Planning and merge branch: `issue-233-enforcement-vocabulary` (topology `single_branch`, no lane worktree). The pull request goes from `issue-233-enforcement-vocabulary` to `main`. Implement with `spec-kitty agent action implement <WP> --agent claude --mission enforcement-vocabulary-01M7PMJW`.

