---
work_package_id: WP02
title: java-conventions rules and release
dependencies:
- WP01
requirement_refs:
- FR-004
- FR-005
- FR-006
planning_base_branch: feat/java-rules-and-language-vocabulary
merge_target_branch: feat/java-rules-and-language-vocabulary
branch_strategy: Planning artifacts for this mission were generated on feat/java-rules-and-language-vocabulary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/java-rules-and-language-vocabulary unless the human explicitly redirects the landing branch.
subtasks:
- T004
- T005
- T006
history:
- at: '2026-11-12T13:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/java/styleguides/
create_intent: []
execution_mode: code_change
owned_files:
- packs/java/styleguides/java-conventions.styleguide.yaml
- packs/java/pack.yaml
- packs/java.source.yaml
- docs/packs/java.md
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
tracker_refs:
- '#204'
---
# Work Package Prompt: WP02 – java-conventions rules and release

## Objective

Add three general business-code rules to `java-conventions` (#204) and release `java` 2.1.0.

## Subtasks

### T004 — Rules
- Principle + pattern: money as `BigDecimal` with an explicit `MathContext` or scale and `RoundingMode`; never
  `double`/`float`; construct from `String`/`valueOf`, compare with `compareTo`.
- Principle + pattern: coded values decode through `fromCode`/`fromByte` that throws a named exception on an
  unknown value; never `values()[ordinal]`, never a silent default.
- Principle + anti-pattern: never put JPA `@Entity` over a positional/wire layout; a codec reads the layout into a
  record, a mapper builds the entity.
Descriptions ≤255 characters; names unique ignoring case.

### T005 — Release
`pack_version: 2.1.0`; `python3 scripts/ci/pack_digest.py --update`; regenerate `docs/packs/java.md` only.

### T006 — CHANGELOG
Under `[Unreleased]`: "Changed" (#204) and "Fixed" (#202, language tags + guard).

## Done when
All mission gates pass (plan.md NFR-001).
