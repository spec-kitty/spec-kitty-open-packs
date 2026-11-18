---
work_package_id: WP03
title: Directive bodies swept, every pack
dependencies: []
requirement_refs:
- FR-004
- FR-005
- NFR-003
- C-003
- C-004
- SC-002
- SC-004
planning_base_branch: issue-233-enforcement-vocabulary
merge_target_branch: issue-233-enforcement-vocabulary
branch_strategy: Planning artifacts for this mission were generated on issue-233-enforcement-vocabulary. The mission is single_branch, so this WP is implemented on issue-233-enforcement-vocabulary and lands there; the pull request goes from issue-233-enforcement-vocabulary to main.
subtasks: [T009, T010, T011, T012]
agent: claude
history:
- at: '2026-11-18T07:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator-carla
authoritative_surface: packs/foundation/directives/
create_intent: []
execution_mode: code_change
owned_files:
- packs/foundation/directives/**
- packs/internal/directives/**
- packs/qa/directives/**
- packs/writing/directives/**
role: curator
tags: []
tracker_refs:
- '#233'
---
# Work Package Prompt: WP03 – Directive bodies swept, every pack

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load curator-carla` before reading anything else.

## Objective

No directive body claims its own level, criticality or gate posture, and every rule's substance stays (FR-004, FR-005, NFR-003, C-003, C-004). Work from research.md R5 ("directive bodies"); its verdicts are binding for this WP.

## Subtasks

### T009 DIRECTIVE_051

- scope: remove "This directive is advisory at the transition-gate level in v1 ... must not silently hard-block on it." Keep "It requires visibility and explicit evidence: silence or an unexamined default is not compliance."
- integrity_rules: remove the fifth rule (level-only; its substance is rule 1). Record the removal in the PR body.

### T010 DIRECTIVE_052, DIRECTIVE_049, reconcile-change-scope-tensions

- 052: "The mandatory output is the diagnosis, not merely a green test." becomes "What the fix must produce is the diagnosis, not merely a green test."
- 049: drop the sentence "This is advisory guidance, not a runtime gate: no mechanism blocks work when the declaration is absent."
- reconcile: "an acceptable lenient-adherence allowance" becomes "an acceptable allowance".
- 028: no level prose in the body (its rules say "should"); confirm, and change nothing (C-003).

### T011 internal, qa and writing

- cloud-session-orchestration: intent "Makes the integrity rules for parallel cloud sessions binding charter content." becomes "Sets the integrity rules for parallel cloud sessions." Scope "... remain advisory in the cloud-session-dispatch procedure." becomes "... stay with the cloud-session-dispatch procedure, outside this directive."
- QA_001: title "QA Requirement Traceability"; the id and the file name stay.
- QA_002: drop "This is not a recommendation" and the "mandatory" framing; keep the seven fields and "no partial credit".
- ACTION_ITEM_ATTRIBUTION: "This rule is enforced as a hard validation gate: minutes containing ownerless actions are refused ..." becomes "Minutes containing ownerless actions are refused ...".
- 042: "This directive binds the conventions" becomes "This directive carries the conventions"; keep the live checks.

### T012 Full re-read

- Re-read the intent and scope of all 59 directives once more after the edits; confirm `enforcement:` values are unchanged (`git diff` shows no `enforcement:` line).

## Definition of Done

- `git diff --stat` touches only the files in R5; `git diff | grep '^[-+]enforcement:'` is empty; `validate-packs.sh` is clean.
## Branch Strategy

Planning and merge branch: `issue-233-enforcement-vocabulary` (topology `single_branch`, no lane worktree). The pull request goes from `issue-233-enforcement-vocabulary` to `main`. Implement with `spec-kitty agent action implement <WP> --agent claude --mission enforcement-vocabulary-01M7PMJW`.

