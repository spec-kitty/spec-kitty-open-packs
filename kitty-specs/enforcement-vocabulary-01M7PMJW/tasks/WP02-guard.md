---
work_package_id: WP02
title: Guard keeps the class closed
dependencies: []
requirement_refs:
- FR-009
- SC-005
planning_base_branch: issue-233-enforcement-vocabulary
merge_target_branch: issue-233-enforcement-vocabulary
branch_strategy: Planning artifacts for this mission were generated on issue-233-enforcement-vocabulary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-233-enforcement-vocabulary unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
- T008
history:
- at: '2026-11-18T07:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: scripts/ci/
create_intent: []
execution_mode: code_change
owned_files:
- scripts/ci/check_vocabulary.py
- tests/vocabulary/test_check_vocabulary.py
role: implementer
tags: []
tracker_refs:
- '#233'
---
# Work Package Prompt: WP02 – Guard keeps the class closed

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load implementer-ivan` before reading anything else.

## Objective

`scripts/ci/check_vocabulary.py` refuses self-binding phrasing in any tracked pack file, so the defect class cannot silently reopen (DIRECTIVE_043; FR-009). Red-first: the rule must report findings on the unswept tree before WP03 and WP04 make it green.

## Subtasks

### T006 Tests first (red)

In `tests/vocabulary/test_check_vocabulary.py`, add a `SelfBindingTest` class:
- Each pattern is refused by `findings_in(text, rel)`: "This directive is advisory at the transition-gate level in v1", "Advisory in v1: evidence is required", "This is advisory guidance, not a runtime gate", "Makes the integrity rules for X binding charter content", "**Advisory posture**:", "governs this step's output prose; enforcement `required`.", "the rule is advisory".
- Controls that must pass (other senses): "npm audit reports an advisory", "Owner is mandatory", "enforcement tiers (advisory, acknowledgment-required, hard-failure)", "`qa-traceability/v1`", "CTRF not implemented in v1", "enforcement: required" as a YAML key line.
- One test runs the guard over the real tree and expects no self-binding findings. It is red until WP03 and WP04 land; the WP02 review records the red run.

### T007 The rule

- Add `SELF_BINDING: tuple[tuple[re.Pattern[str], str], ...]` with case-insensitive patterns and a message per pattern, a module docstring paragraph naming #233 and the ADR, and a line-wise check in `findings_in`. Skip a line whose stripped form starts with `enforcement:` (the YAML field).
- Patterns (phrases, never single words): `\badvisory\s+(?:in|at\s+the\s+[\w-]+\s+level\s+in)\s+v\d`; `\b(?:this|the)\s+(?:directive|rule|guidance)\s+is\s+(?:advisory|required|mandatory|binding|lenient)\b`; `\bthis\s+is\s+advisory\b`; `\bnot\s+a\s+runtime\s+gate\b`; `\bbinding\s+charter\s+content\b`; `\badvisory\s+posture\b`; ``\benforcement\s+`(?:required|advisory|lenient-adherence)`` (prose, backticked).

### T008 Green check

- After WP03 and WP04, `python3 scripts/ci/check_vocabulary.py` exits 0 and `python3 -m unittest discover -s tests/vocabulary` passes.

## Definition of Done

- Tests prove every pattern is caught and every control passes; stdlib only; the real-tree run is green after the sweep.
## Branch Strategy

Planning and merge branch: `issue-233-enforcement-vocabulary` (topology `single_branch`, no lane worktree). The pull request goes from `issue-233-enforcement-vocabulary` to `main`. Implement with `spec-kitty agent action implement <WP> --agent claude --mission enforcement-vocabulary-01M7PMJW`.

