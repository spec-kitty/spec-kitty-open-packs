---
work_package_id: WP02
title: First-hand checks before a ruling
dependencies: []
requirement_refs:
- FR-005
- FR-006
- FR-007
- FR-013
- NFR-003
- SC-002
planning_base_branch: feat/citation-and-docs-writing
merge_target_branch: feat/citation-and-docs-writing
branch_strategy: Planning artifacts for this mission were generated on feat/citation-and-docs-writing. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/citation-and-docs-writing unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-citation-and-docs-writing-01M7YGMQ
base_commit: a4ea7a159600130a63c618806f40454af267003f
created_at: '2026-11-21T07:48:41.395923+00:00'
subtasks:
- T005
- T006
- T007
history:
- at: '2026-11-21T08:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/procedures/adversarial-squad-deployment.procedure.yaml
- packs/internal/procedures/cloud-session-dispatch.procedure.yaml
role: implementer
tags: []
---
# Work Package Prompt: WP02 – First-hand checks before a ruling

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Branch Strategy

Planning and merge branch: `feat/citation-and-docs-writing`. Execution worktrees are allocated per computed lane from `lanes.json`.

## Objective

#150 rules 2-3 and #176's procedure part in the foundation squad procedure, #274's `StatusGateError` example neutralised, and #150 rule 4 in internal (spec FR-005 to FR-007, FR-013; plan decisions 3-4).

## Subtasks

### T005 First-hand check step

In `adversarial-squad-deployment.procedure.yaml`, add a step after "Synthesize, and get a second opinion on divergence", titled "Check claims first-hand before a ruling": a brief, synthesis or ruling that calls a blocker resolved reproduces it against the current head first and records how (command and result); a ruling that relies on a named acceptance test first checks the test exists and runs, and records that. Cite code and changes per the writing pack's `research-citation-discipline` (one clause). Add anti-patterns "Resolved on paper" and "Ruling on an unreachable test" (one line each). Add the rule to the `notes` invariants list ("first-hand checks before a ruling").

### T006 No prototyping; neutral gate example

In the dispatch step, after "Each delegate is read-only unless ...": one sentence: a delegate validates instructions or claims by reading code and running existing tests; it does not prototype, simulate or dry-run the change, in the repository or a scratch copy; that work belongs to implementation. In anti-pattern "Hard-wiring the squad as a gate", replace "e.g. raising a StatusGateError before a work package can be claimed" with a neutral example, e.g. "a status transition that refuses to run until a squad report is attached". Replace any em-dash you touch with plain punctuation.

### T007 Overturned rulings, then gates

`packs/internal/procedures/cloud-session-dispatch.procedure.yaml`: after "Post every operator ruling on the governing issue; runners cite that issue comment rather than chat." add: "When a measurement overturns a ruling, post the overturn on the same issue with the measurement that overturned it (the command and its result) and a link to the earlier ruling; do not edit the earlier ruling." Run `bash scripts/ci/validate-packs.sh` and `python3 scripts/ci/check_vocabulary.py`.

## Definition of Done

Each of the three squad rules appears once; the overturn rule appears once in internal; `StatusGateError` gone; gates pass.

## Reviewer guidance

The squad still never gates the work; the new step is about the content of a ruling, not a mission gate.
