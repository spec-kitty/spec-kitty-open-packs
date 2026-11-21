---
work_package_id: WP01
title: Citation rules that survive history rewrites
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- C-003
- C-005
- NFR-002
- SC-001
planning_base_branch: feat/citation-and-docs-writing
merge_target_branch: feat/citation-and-docs-writing
branch_strategy: Planning artifacts for this mission were generated on feat/citation-and-docs-writing. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/citation-and-docs-writing unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
history:
- at: '2026-11-21T08:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
model: ""
owned_files:
- packs/writing/styleguides/research-citation-discipline.styleguide.yaml
- packs/foundation/missions/software-dev/steps/specify.prompt.md
- packs/foundation/missions/software-dev/steps/plan.prompt.md
- packs/foundation/tactics/communication/adr-drafting-workflow.tactic.yaml
role: implementer
tags: []
---
# Work Package Prompt: WP01 – Citation rules that survive history rewrites

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Branch Strategy

Planning and merge branch: `feat/citation-and-docs-writing`. Execution worktrees are allocated per computed lane from `lanes.json`.

## Objective

State #219's stable-identifier rule and #150 rule 1 (content-anchored citations) once each in `research-citation-discipline`, cross-referenced, and put a one-sentence reminder in the three authoring surfaces (spec FR-001 to FR-003; plan design decisions 1-2; research R1, R4).

## Subtasks

### T001 Stable-identifier principle

In `packs/writing/styleguides/research-citation-discipline.styleguide.yaml`, after "Cite the specific locus, not the whole source", add principle "Cite changes by a stable identifier". Description (<= 255 chars, C-003): cite a change by PR or issue number, ADR id, release tag or a description of the change, never a bare commit SHA; rebases and squashes rewrite SHAs (pattern of the same name has the full rule; see "Anchor code citations to content"). Add a same-named pattern with the full text: history is rewritten at mandated steps (squash or compaction at close-out, rebase onto a moving upstream), so a SHA written during the work is expected to dangle; a rewritten SHA can still exist as an unreachable object, so a lookup that reports "commit" proves nothing; a SHA is acceptable only when necessary and annotated as ephemeral or pre-rewrite, with a symbolic description beside it. Add anti-pattern "Bare SHA citation" with neutral bad/good examples (bad: "renamed in a1b2c3d"; good: "renamed in PR #412 (the `Order -> Purchase` rename)"; and a good annotated-ephemeral example).

### T002 Content-anchored principle

Principle "Anchor code citations to content" (<= 255 chars): cite code as `path::qualname` or a path plus a quoted anchor, not a bare line range; a cited count carries the command that produced it; see "Cite changes by a stable identifier". Same-named pattern with the full text (line numbers drift within one review round; a qualname or quoted string survives edits and can be searched; a count without its command cannot be re-derived). Anti-pattern "Drifting line citation" with neutral examples. In "Record retrieval context" description, keep it under 255 chars and make clear a commit recorded as retrieval context follows the stable-identifier principle (e.g. replace "commit" with "release or tag" or add a short pointer).

### T003 Prompt reminders (ASCII only)

In `packs/foundation/missions/software-dev/steps/specify.prompt.md` and `plan.prompt.md`, add one sentence each where the prompt talks about writing the artifact's content (find the spec/plan generation guidance): "Cite earlier changes by PR or issue number, ADR id, release tag or a description of the change, not a bare commit SHA: the lifecycle rewrites history at close-out, so a SHA written now will not resolve later. Cite code by `path::qualname` or a quoted anchor, not a line range. The writing pack's `research-citation-discipline` styleguide holds the rule." Plain ASCII (no em-dash, no arrows). Prose only, no graph edge (C-005).

### T004 ADR tactic reminder, then gates

`packs/foundation/tactics/communication/adr-drafting-workflow.tactic.yaml`, step "Cross-link and commit": add a sentence and an example: link related ADRs, PRs and issues by number, not by commit SHA (the writing pack's `research-citation-discipline`). Run `bash scripts/ci/validate-packs.sh`, `python3 -m pytest -q tests/ci/test_software_dev_ascii.py tests/ci/test_validate_pack_schemas.py`, `python3 scripts/ci/check_vocabulary.py`.

## Definition of Done

Two new principles, each <= 255 chars, each naming the other; patterns and anti-patterns carry the full text with neutral examples; three reminders point at the styleguide; ASCII test and validation pass.

## Reviewer guidance

Check the rule is stated once (styleguide) and the reminders do not restate the exceptions; check no foundation graph edge into writing was added.
