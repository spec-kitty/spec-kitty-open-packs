---
work_package_id: WP03
title: Tracer-bullet TDD, green-mode refactoring and vertical-skeleton-first
dependencies:
- WP01
requirement_refs:
- FR-010
- FR-011
- FR-012
- FR-013
- FR-014
- C-004
- C-006
- NFR-002
- SC-004
- SC-005
planning_base_branch: t3/test-doctrine-2
merge_target_branch: t3/test-doctrine-2
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-2 unless the human explicitly redirects the landing branch.
subtasks:
- T012
- T013
- T014
- T015
- T016
history:
- at: '2026-11-21T08:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/tactics/testing/
create_intent:
- packs/planning-analysis/tactics/analysis/vertical-skeleton-first.tactic.yaml
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/glossaries/spec-kitty-core.glossary.yaml
- packs/foundation/tactics/testing/tdd-red-green-refactor.tactic.yaml
- packs/foundation/tactics/testing/acceptance-test-first.tactic.yaml
- packs/foundation/procedures/test-first-cycle.procedure.yaml
- packs/foundation/procedures/disciplined-refactoring-cycle.procedure.yaml
- packs/foundation/missions/software-dev/steps/plan.guidelines.md
- packs/foundation/missions/software-dev/steps/tasks.guidelines.md
- packs/testing/procedures/test-first-bug-fixing.procedure.yaml
- packs/planning-analysis/tactics/analysis/vertical-skeleton-first.tactic.yaml
- packs/planning-analysis/drg/fragment.yaml
- packs/refactoring/drg/fragment.yaml
role: implementer
tags: []
tracker_refs:
- '#154'
- '#147'
---
# Work Package Prompt: WP03 – Tracer-bullet TDD, green-mode refactoring and vertical-skeleton-first

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

#154 and #147 in one work package with one vocabulary (FR-010 to FR-014): vertical tracer-bullet slicing at test scale, the spine at mission scale, and refactoring as a separate green-mode technique. Read `spec.md`, `plan.md` (IC-03), `research.md` (R5-R7), the #147 issue body and its 2026-11-12 ruling comment.

## Branch Strategy

Planning branch and merge target: `t3/test-doctrine-2`; lanes from `lanes.json`. Implement with `spec-kitty agent action implement WP03 --agent <name> --mission test-doctrine-2-01M7YH30`.

Out-of-map edits (recorded): foundation edges go in `tactic.graph.yaml` and `procedure.graph.yaml` (owned by WP01, a dependency); the `test-first-bug-fixing` edge goes in `packs/testing/drg/fragment.yaml` (owned by WP02; keep the edit small).

## Subtasks

### T012 — Glossary terms (FR-014)

`packs/foundation/glossaries/spec-kitty-core.glossary.yaml`, alphabetical, `status: active`, schema of sibling terms; `tests/ci/test_glossary_content.py` must pass:
- `tracer-bullet`: a thin path through the real system, end to end, kept and grown rather than thrown away; at test scale one test through the public interface per behaviour, at mission scale the spine's first composed path. Not a prototype or spike.
- `horizontal-slicing`: building one layer or one kind of artefact across all behaviours before the next (all tests then all code; all models then all services); the opposite of vertical slices.
- `spine`: the cross-owner flow of a mission whose composed success retires the most integration risk, with its shared transition matrix (see vertical-skeleton-first).
- `green-mode`: the state in which refactoring is allowed: the suite is green and the change keeps behaviour; entered after any green, inside or outside a TDD cycle.

### T013 — TDD tactic (FR-010)

`tdd-red-green-refactor` (id, name kept). Steps: Red (one behaviour, one failing test through the public interface, at a seam named before testing, which the spec or work package records); Green (least code; no speculative features, no anticipated tests); Next slice (repeat; each test a tracer bullet that responds to what the last cycle taught); Hand off to green mode (refactoring is not a step of the loop: once green, switch to green mode per `disciplined-refactoring-cycle`; never refactor on red); keep fast feedback; handle constraints (characterization tests for legacy). `failure_modes`: horizontal slicing (all tests first: they verify imagined behaviour and the shape of things); tautological expected values (recomputed the way the code computes them; use an independent literal or worked example); implementation-coupled tests (mocking owned collaborators, testing private methods, verifying through a side channel; DIRECTIVE_054 owns the seam list). `notes`: "Adapted from mattpocock/skills at commit abeeaf95660ba9e8b7c753eb38f441ca707a8823 (MIT): skills/engineering/tdd/SKILL.md, skills/engineering/tdd/tests.md, skills/engineering/tdd/mocking.md, skills/engineering/codebase-design/SKILL.md ('the interface is the test surface'). Upstream's mocking list is not adopted; DIRECTIVE_054 owns the allow-list." The "block merge when new logic has no corresponding tests" example keeps its carve-out wording from the first mission.

### T014 — Green mode (FR-011)

- `disciplined-refactoring-cycle`: becomes the owner of green mode: entry condition reads "the suite is green and the code is about to be restructured, inside a TDD cycle or on its own"; one sentence defines green mode (no other surface restates it).
- `test-first-cycle` ("Keep red-green-refactor cycles short"), `acceptance-test-first` ("continue with Red-Green-Refactor"), testing `test-first-bug-fixing` ("Refactor after green, scoped to the fix" and its anti-pattern): replace refactor wording with one pointer to green mode / `disciplined-refactoring-cycle`, keeping each artefact's own scope rule (e.g. bug fix: refactor beyond the fix is a separate change).
- Edges (`when` on each; check pairs): `tactic:tdd-red-green-refactor --suggests--> procedure:disciplined-refactoring-cycle`; `procedure:test-first-cycle --suggests--> procedure:disciplined-refactoring-cycle`; testing `procedure:test-first-bug-fixing --suggests--> foundation::procedure:disciplined-refactoring-cycle`; refactoring fragment: `procedure:refactoring` is the catalog; add `foundation::procedure:disciplined-refactoring-cycle --suggests--> procedure:refactoring` (when: the named smell selects a catalog move) if no such edge exists.

### T015 — vertical-skeleton-first (FR-012)

New `packs/planning-analysis/tactics/analysis/vertical-skeleton-first.tactic.yaml` from #147's draft with the 2026-11-12 cuts: steps 1-5 and 7 (identify the spine; define the shared transition matrix with paired examples and counterexamples; land the thinnest real composed path through the real entry point; hold second-wave supplier work until it runs green (four hours without a composed path is a heuristic signal to revisit sequencing, not a gate); hang owner WPs off the running spine; spine event with the five bounds: pause only WPs that consume the amended row (each WP declares the rows it consumes), one re-run per event within the smoke budget recorded in the plan, a second amendment of the same row or more than about three events escalates to replanning / example mapping / DIRECTIVE_040, a flaky composed smoke is no measurement (not a blocking red), the integration owner classifies). Step 6 (one bounded repair per defect class) becomes one sentence pointing to DIRECTIVE_040 and DIRECTIVE_043. No "gates green on the exact SHA", no "review narrowing" rule. Generic examples ("real entry point", not "real dispatcher"); mission-199 specifics only in `notes`. Use "tracer bullet" and "horizontal slicing" as defined in T012. No `references:` block. Wire in the planning-analysis fragment: node; `foundation::action:software-dev/plan --scope--> tactic:vertical-skeleton-first` and tasks action if such action node exists; `suggests` to `foundation::procedure:example-mapping-workshop`, `foundation::directive:DIRECTIVE_040`, `foundation::directive:DIRECTIVE_043`, `foundation::directive:DIRECTIVE_036` (cross-pack, check they resolve), and `foundation::tactic:product-coherence-review --suggests--> tactic:vertical-skeleton-first`.

### T016 — Plan/tasks pointer (FR-013)

One ASCII line each in `plan.guidelines.md` and `tasks.guidelines.md`: "Does this mission have a cross-owner spine? Name it and its first composed path (tactic vertical-skeleton-first), and slice work packages vertically." Run `tests/ci/test_software_dev_ascii.py` and `tests/ci/test_prompt_fragments.py`.

## Definition of Done

- 4 glossary terms; no TDD surface has its own refactor steps (SC-004); tactic validates and is reachable (SC-005); attribution names only verified paths (C-006).
- Gates: validate-packs, pytest, vocabulary.

## Risks and reviewer guidance

- Reviewer: check green-mode wording against DISCIPLINED_REFACTORING (no contradiction); check no directive was added (C-004); grep the upstream paths cited against the abeeaf9 tree.
