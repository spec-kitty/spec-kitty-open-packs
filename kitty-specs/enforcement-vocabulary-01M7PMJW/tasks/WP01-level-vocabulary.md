---
work_package_id: WP01
title: Level vocabulary defined once
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-008
- SC-003
planning_base_branch: issue-233-enforcement-vocabulary
merge_target_branch: issue-233-enforcement-vocabulary
branch_strategy: Planning artifacts for this mission were generated on issue-233-enforcement-vocabulary. The mission is single_branch, so this WP is implemented on issue-233-enforcement-vocabulary and lands there; the pull request goes from issue-233-enforcement-vocabulary to main.
subtasks: [T001, T002, T003, T004, T005]
agent: claude
history:
- at: '2026-11-18T07:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator-carla
authoritative_surface: packs/foundation/glossaries/
create_intent: []
execution_mode: code_change
owned_files:
- packs/foundation/glossaries/spec-kitty-core.glossary.yaml
- packs/pack-authoring/styleguides/doctrine-instruction-voice.styleguide.yaml
- docs/guides/author-a-charter-pack.md
- docs/artefacts/index.md
- docs/architecture/adr/2026-11-18-1-directive-enforcement-is-a-pack-supplied-default.md
- docs/architecture/adr/index.md
role: curator
tags: []
tracker_refs:
- '#233'
---
# Work Package Prompt: WP01 – Level vocabulary defined once

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load curator-carla` (or `spec-kitty agent profile show curator-carla`) before reading anything else.

## Objective

`required`, `lenient-adherence` and `advisory` are defined in exactly one place: the term `enforcement-level` in the foundation `spec-kitty-core` glossary context. The authoring guidance points to it, and the field decision is recorded (ADR, Proposed). Requirements: FR-001, FR-002, FR-003, FR-008.

## Context

- At pin `050d780`, the directive schema requires `enforcement` (enum `required | lenient-adherence | advisory`, `additionalProperties: false`); see research.md R1. The field stays.
- Glossary term shape at the pin: `id`, `name`, `definition`, `status` are required; `examples`, `aliases`, `avoid` and `see_also` are optional. `see_also` entries are `term:<context>/<term-id>`.
- Keep this vocabulary distinct from activation presets' `must_have` items and `policy.yaml` levels (#242, #201).

## Subtasks

### T001 Add `term:spec-kitty-core/enforcement-level`

- Insert the term in alphabetical position (after `drg`, before `evidence-bundle`; check the neighbours).
- The definition must say: how strictly an in-force directive binds; the three values, each in one clause (`required`: conformance is expected and a deviation is a defect; `lenient-adherence`: conform by default, a recorded, justified deviation is acceptable; `advisory`: guidance an agent weighs, and deviating needs no record); the directive's `enforcement:` value is the pack-supplied default; the adopting project's charter decides the level that applies; the term is distinct from activation-preset `must_have` and `policy.yaml` levels, which decide which artefacts are in force; and directive prose never restates the level.
- `avoid`: `criticality`, `binding level`. `see_also`: `term:spec-kitty-core/directive`, `term:spec-kitty-core/charter`, `term:spec-kitty-core/activation-preset`. `status: active`.
- In the `directive` term, add one sentence that it carries a default enforcement level (see `enforcement-level`).

### T002 Reword the adversarial-squad term

- "Optional and advisory, never a gate" becomes "Optional, never a gate": the level word clashes with the new term (research.md R5).

### T003 Authoring guide and artefact reference

- `docs/guides/author-a-charter-pack.md`: under the directive example, add a short paragraph: the value is the pack-supplied default level; an adopting charter decides the level that applies; link the glossary term (docs/glossary page, if the term is rendered there; otherwise name `term:spec-kitty-core/enforcement-level`); the directive body states what the rule requires, never how strictly it binds ("advisory in v1", "this is mandatory", "binding").
- `docs/artefacts/index.md`: the directive row reads "A rule, with a default enforcement level."; check the example near line 51 for a matching comment.

### T004 Styleguide principle

- `doctrine-instruction-voice.styleguide.yaml`: add one principle `{name: State the rule, not its strictness, description: ...}` (description of at most 255 characters): the level lives in the enforcement field and the adopting charter, never in the directive's prose or in content that cites it.

### T005 ADR

- The ADR file and index row already exist (drafted at plan time). Re-read them against the final term wording and fix any drift.

## Definition of Done

- `validate-packs.sh` is clean for foundation and pack-authoring.
- Exactly one glossary term defines the three values (`grep -rn "lenient-adherence" packs/*/glossaries` shows only that term).
- The docs frontmatter validates (`site`: `npm run validate`, if available; otherwise a frontmatter shape check against a sibling page).

## Reviewer guidance

- Check the definition against R1: nothing in it promises core behaviour beyond "the adopting charter decides".
## Branch Strategy

Planning and merge branch: `issue-233-enforcement-vocabulary` (topology `single_branch`, no lane worktree). The pull request goes from `issue-233-enforcement-vocabulary` to `main`. Implement with `spec-kitty agent action implement <WP> --agent claude --mission enforcement-vocabulary-01M7PMJW`.

