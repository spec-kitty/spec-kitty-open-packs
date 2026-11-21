---
work_package_id: WP03
title: One shared list of AI-writing tells, wired for docs
dependencies: []
requirement_refs:
- FR-004
- FR-008
- FR-009
- FR-010
- C-004
- NFR-003
- SC-003
planning_base_branch: feat/citation-and-docs-writing
merge_target_branch: feat/citation-and-docs-writing
branch_strategy: Planning artifacts for this mission were generated on feat/citation-and-docs-writing. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/citation-and-docs-writing unless the human explicitly redirects the landing branch.
subtasks:
- T008
- T009
- T010
- T011
history:
- at: '2026-11-21T08:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/
create_intent:
- packs/writing/styleguides/ai-writing-tells.styleguide.yaml
execution_mode: code_change
model: ""
owned_files:
- packs/writing/styleguides/ai-writing-tells.styleguide.yaml
- packs/internal/styleguides/report-writing.styleguide.yaml
- packs/internal/drg/fragment.yaml
- packs/writing/styleguide.graph.yaml
- packs/writing/mission_type.graph.yaml
- packs/writing/action.graph.yaml
- packs/writing/agent_profile.graph.yaml
role: implementer
tags: []
---
# Work Package Prompt: WP03 – One shared list of AI-writing tells, wired for docs

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Branch Strategy

Planning and merge branch: `feat/citation-and-docs-writing`. Execution worktrees are allocated per computed lane from `lanes.json`.

## Objective

Move the seven AI-prose tells out of internal `report-writing` into a shared writing styleguide `ai-writing-tells`, point `report-writing` at it, and wire it for docs work; also add FR-004's scope edges for the citation styleguide (spec FR-004, FR-008 to FR-010; plan decisions 2, 5, 6; research R3).

## Subtasks

### T008 New styleguide

`packs/writing/styleguides/ai-writing-tells.styleguide.yaml`, `schema_version: "1.0"`, `id: ai-writing-tells`, title "AI Writing Tells Styleguide", `scope: docs`, `applies_to_languages: []`. Principles (each <= 255 chars): "Cut the tells of machine writing" (run the list before publishing a page, report or message), "Applies to every page, not only reports". Patterns: the seven tells from report-writing (Ration the em-dash; Say the thing plainly, not "not just X but Y"; Cut empty intensifiers and throat-clearing; Drop the LLM buzzwords; Break the rule of three and the uniform bullet opener; No puffery; Label gathered versus synthesized figures), rewritten for any page (not "a whole report") with neutral examples. Anti-pattern "Em-dash sprawl and buzzword fog" moved here with a neutral example. No Spec Kitty voice or brand rule. A `quality_test` line: a page passes when none of the patterns occurs more than the pattern allows.

### T009 report-writing points at it

`packs/internal/styleguides/report-writing.styleguide.yaml`: replace the principle "Cut the tells of machine writing" with one that points at `writing::styleguide:ai-writing-tells` ("Run the shared AI-writing tells list before circulating; this styleguide adds only report rules and the Spec Kitty voice"), delete the seven tell patterns and the em-dash anti-pattern (they now live in writing), keep everything else. `packs/internal/drg/fragment.yaml`: add edge `styleguide:report-writing refines writing::styleguide:ai-writing-tells` near the existing report-writing edges; update the node title "Report Writing (audience-first, anti-AI-prose, Spec Kitty voice)" to drop "anti-AI-prose" if it no longer owns them (e.g. "audience-first, Spec Kitty voice").

### T010 Writing graph wiring

Per research R3: node in `styleguide.graph.yaml` plus `styleguide:ai-writing-tells suggests styleguide:plain-language`; `mission_type:documentation scope styleguide:ai-writing-tells`; `action:documentation/generate` and `action:documentation/validate` scope it; `agent_profile:comms-cleo suggests styleguide:ai-writing-tells`; `foundation::action:software-dev/specify` and `foundation::action:software-dev/plan` scope `styleguide:research-citation-discipline` (beside the existing retrospect edges at the end of `action.graph.yaml`). Keep each file's ordering convention.

### T011 Gates

`python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/writing` and `packs/internal` if the validator asks for it; `bash scripts/ci/validate-packs.sh`; `python3 -m pytest -q tests/ci/test_graph_edge_identity.py tests/ci/test_validate_pack_schemas.py`; `python3 scripts/ci/check_vocabulary.py`.

## Definition of Done

The seven tells exist in exactly one artefact; report-writing references it; graph edges present and unique; gates pass.

## Reviewer guidance

Diff report-writing and ai-writing-tells side by side: nothing duplicated, nothing lost except house voice staying internal.
