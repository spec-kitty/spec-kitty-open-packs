---
work_package_id: WP04
title: Operator wording in pack prose (#139)
dependencies:
- WP02
requirement_refs:
- FR-012
- SC-005
planning_base_branch: issue-221-234-glossary-content
merge_target_branch: issue-221-234-glossary-content
branch_strategy: Planning artifacts for this mission were generated on issue-221-234-glossary-content. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into issue-221-234-glossary-content unless the human explicitly redirects the landing branch.
subtasks:
- T012
- T013
history: []
agent_profile: curator-carla
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
model: opus
owned_files:
- packs/foundation/tactics/stopping-conditions.tactic.yaml
- packs/foundation/tactics/communication/glossary-curation-interview.tactic.yaml
- packs/foundation/missions/software-dev/steps/charter.prompt.md
- packs/foundation/procedures/example-mapping-workshop.procedure.yaml
- packs/architecture/procedures/event-storming-discovery.procedure.yaml
- packs/architecture/tactics/architecture/c4-zoom-in-architecture-documentation.tactic.yaml
- packs/writing/styleguides/writing/kitty-glossary-writing.styleguide.yaml
- packs/writing/styleguides/writing/README.md
- packs/writing/toolguides/contextive.guide.md
- packs/writing/tactic.graph.yaml
- packs/writing/procedures/glossary-maintenance-workflow.procedure.yaml
- packs/planning-analysis/agent_profiles/retrospective-facilitator.agent.yaml
- packs/internal/procedures/*.procedure.yaml
role: implementer
tags: []
tracker_refs: []
---

# WP04 — Operator wording in pack prose (#139)

## Objective

Retire "HiC", "Human-in-Charge" and "human-in-command" as role wording in pack prose in favour of "the operator"
(#139's 2026-11-18 list). The `human-in-charge` agent profile id and its catalog entries stay.

### Subtask T012: Reword the listed files

- Drop the glossary-curation-interview step "Apply HiC terminology consistently"; reword the rest.
- Retire the kitty-glossary-writing rule that requires "HiC" in every definition (and its good example); update its
  README row; drop the core path citation ("Sources: glossary/README.md; docs/context/").
- Rename the retrospective-facilitator mode `hic` to `operator` (no pack references the mode id).
- Reword the tactic graph `when` texts, the contextive toolguide, procedures, prompts and tactics.

### Subtask T013: Verify

`grep -rniE "\bHiC\b|human-in-command" packs` finds nothing; `grep -rni "human-in-charge" packs` finds only the
profile id and its catalog entries; validate-packs and the vocabulary guard pass.
