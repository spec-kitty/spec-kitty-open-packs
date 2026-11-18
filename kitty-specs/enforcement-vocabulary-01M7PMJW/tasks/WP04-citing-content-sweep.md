---
work_package_id: WP04
title: Steps, prompts, tactic and citing content swept
dependencies: []
requirement_refs:
- FR-006
- FR-007
- NFR-002
- C-001
- SC-001
planning_base_branch: issue-233-enforcement-vocabulary
merge_target_branch: issue-233-enforcement-vocabulary
branch_strategy: Planning artifacts for this mission were generated on issue-233-enforcement-vocabulary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-233-enforcement-vocabulary unless the human explicitly redirects the landing branch.
subtasks:
- T013
- T014
- T015
- T016
- T017
history:
- at: '2026-11-18T07:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator-carla
authoritative_surface: packs/foundation/missions/
create_intent: []
execution_mode: code_change
owned_files:
- packs/foundation/missions/software-dev/software-dev.mission-type.yaml
- packs/foundation/missions/software-dev/steps/**
- packs/foundation/missions/plan/plan.mission-type.yaml
- packs/foundation/tactics/security/supply-chain-install-safety.tactic.yaml
- packs/foundation/directive.graph.yaml
- packs/foundation/tactic.graph.yaml
- packs/internal/drg/fragment.yaml
- packs/writing/directive.graph.yaml
- packs/writing/agent_profiles/**
- packs/writing/styleguides/**
- packs/writing/tactics/common-docs-scaffold.tactic.yaml
- packs/cave-kitty/README.md
- packs/cave-kitty/styleguides/**
- packs/cave-kitty/missions/cave-dev/steps/**
role: curator
tags: []
tracker_refs:
- '#233'
---
# Work Package Prompt: WP04 – Steps, prompts, tactic and citing content swept

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load curator-carla` before reading anything else.

## Objective

Content that cites a directive states the checklist and the evidence it requires, never the directive's level (FR-006, FR-007). Software-dev content stays ASCII (NFR-002). Work from research.md R5.

## Subtasks

### T013 software-dev steps (ASCII only)

- `software-dev.mission-type.yaml` substeps `supply-chain-*` (plan, implement, review; around lines 132, 251, 307): drop the "Advisory in v1 ..." clause, but keep "visibility and evidence are required" and, for review, "silence or an unexamined default is a gap in evidence, not a pass".
- `content` header: "Your charter enforces Library-First, CLI Interface, and Test-First principles." becomes "You work to Library-First, CLI Interface and Test-First principles." "Tests before code (non-negotiable)" becomes "Tests before code".
- `steps/{plan,implement,review}.{prompt,guidelines}.md`: remove the advisory-in-v1 sentence from each of the 6 files and keep the evidence rule. In plan.prompt.md, the "**Advisory posture**" bullet becomes "**Evidence**: an unexamined default is a gap in the plan, not a pass. Silence is not compliance." In review.prompt.md, keep "missing or unexamined evidence for a dependency change is a review gap to call out".

### T014 plan mission type and the tactic

- `plan.mission-type.yaml` supply-chain-check: drop "Advisory: ... does not gate the transition."
- `supply-chain-install-safety.tactic.yaml` (about lines 16-17, 95-96 and 132-134): drop the posture clauses; keep "the checklist itself is not optional" only if it is phrased as the rule (prefer "Run the checklist for every dependency change"); rewrite the failure mode as "Treating the checklist as optional: skipping a control or leaving a result unrecorded is a gap, not a pass."

### T015 Graph reasons

- foundation `directive.graph.yaml` (2: "binding rules" becomes "rules"), `tactic.graph.yaml` (1: "the ... rules that DIRECTIVE_045 makes binding" becomes "DIRECTIVE_045's ... rules"; "the enforcement context" becomes "the context"), internal `drg/fragment.yaml` (1), writing `directive.graph.yaml` (1).

### T016 writing and cave-kitty prose

- cave-dev steps (8 prompts): drop "; enforcement `required`" from the CAVE_001 line.
- cave-kitty README (2 places) and `cave-sty-001` styleguide: "is advisory context" becomes "is context an agent applies".
- writing: kitty-glossary-writing ("This is not optional." is dropped); minutes-mahad ("hard constraints" becomes "rules it applies"; "hard gate" becomes "is checked"); comms-cleo ("mandatory before drafting" becomes "happen before drafting"); meeting-minutes-format :83 ("hard gate" becomes "is checked"); common-docs-scaffold ("required by this directive but is not (yet) lint-enforced" becomes "part of this directive's rule, though no lint checks it yet").

### T017 Check

- `grep -rniE "advisory in v1|advisory posture|enforcement `required" packs` is empty; `python3 -m unittest tests/ci/test_software_dev_ascii.py` passes.

## Definition of Done

- The guard (WP02) is green on the tree once WP03 is also in; every R5 FR-006/FR-007 line is handled.
## Branch Strategy

Planning and merge branch: `issue-233-enforcement-vocabulary` (topology `single_branch`, no lane worktree). The pull request goes from `issue-233-enforcement-vocabulary` to `main`. Implement with `spec-kitty agent action implement <WP> --agent claude --mission enforcement-vocabulary-01M7PMJW`.

