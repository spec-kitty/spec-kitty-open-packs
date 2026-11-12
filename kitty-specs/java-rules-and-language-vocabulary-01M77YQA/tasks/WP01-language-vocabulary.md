---
work_package_id: WP01
title: Language vocabulary
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
planning_base_branch: feat/java-rules-and-language-vocabulary
merge_target_branch: feat/java-rules-and-language-vocabulary
branch_strategy: Planning artifacts for this mission were generated on feat/java-rules-and-language-vocabulary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/java-rules-and-language-vocabulary unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
history:
- at: '2026-11-12T13:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/java/toolguides/
create_intent: []
execution_mode: code_change
owned_files:
- packs/java/toolguides/java-supply-chain.toolguide.yaml
- packs/java/toolguides/maven-review-checks.toolguide.yaml
- scripts/ci/check_vocabulary.py
- tests/vocabulary/test_check_vocabulary.py
- docs/guides/author-a-charter-pack.md
role: implementer
tags: []
tracker_refs:
- '#202'
---
# Work Package Prompt: WP01 – Language vocabulary

## Objective

A Java project filtered to `languages: [java]` keeps every Java toolguide in force (#202), and no pack can
reintroduce a runtime-family language name.

## Subtasks

### T001 — Retag the toolguides
`java-supply-chain`: `applies_to_languages: [java, kotlin]`. `maven-review-checks`: `[java]`.

### T002 — Guard
In `scripts/ci/check_vocabulary.py`, report any `applies_to_languages` entry (block or flow list) that names a
runtime family (`jvm`, `dotnet`, `clr`, `beam`, `node`, `nodejs`, `web`). Unit tests: block form, flow form, a
language name passes, a `jvm` elsewhere in prose passes.

### T003 — Authoring guide
`docs/guides/author-a-charter-pack.md`: a short "Language names" note: the language's own lowercase name, one per
language, never a runtime family, `[]` for language-neutral; the guard enforces the family rule.

## Done when
`python3 scripts/ci/check_vocabulary.py` and `python3 -m unittest discover -s tests/vocabulary -t .` pass; `git grep -w jvm packs` shows no language entry.
