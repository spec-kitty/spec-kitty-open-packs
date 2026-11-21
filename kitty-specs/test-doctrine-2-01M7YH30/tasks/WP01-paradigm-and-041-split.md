---
work_package_id: WP01
title: Tests-as-scaffold paradigm, 041 split and anti-pattern nodes
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- C-003
- NFR-003
- SC-001
planning_base_branch: t3/test-doctrine-2
merge_target_branch: t3/test-doctrine-2
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-2 unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
history:
- at: '2026-11-21T08:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/paradigms/
create_intent:
- packs/foundation/paradigms/tests-as-scaffold-not-friction.paradigm.yaml
- packs/foundation/anti_pattern.graph.yaml
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/paradigms/tests-as-scaffold-not-friction.paradigm.yaml
- packs/foundation/directives/041-tests-as-scaffold-not-friction.directive.yaml
- packs/foundation/paradigm.graph.yaml
- packs/foundation/directive.graph.yaml
- packs/foundation/anti_pattern.graph.yaml
- packs/foundation/procedure.graph.yaml
- packs/foundation/tactic.graph.yaml
role: implementer
tags: []
tracker_refs:
- '#216'
---
# Work Package Prompt: WP01 – Tests-as-scaffold paradigm, 041 split and anti-pattern nodes

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

Give the tests-as-scaffold mindset its own foundation paradigm, shrink DIRECTIVE_041 to its binding surface, and declare the two mocking smells as anti-pattern nodes (FR-001, FR-002, FR-003). Read `spec.md`, `plan.md` (IC-01), `research.md` (R1, R2) and `data-model.md` first.

## Branch Strategy

Planning branch and merge target: `t3/test-doctrine-2`. Execution worktrees are allocated per computed lane from `lanes.json`; never choose a base by hand. Implement with `spec-kitty agent action implement WP01 --agent <name> --mission test-doctrine-2-01M7YH30`.

## Subtasks

### T001 — Author the paradigm

File (new): `packs/foundation/paradigms/tests-as-scaffold-not-friction.paradigm.yaml`. Schema: `schema_version`, `id`, `name`, `summary`, optional `principles` (each `{name <=64, description <=255}`); no relationship fields.

- `summary`: tests protect change, they do not obstruct it. Carry DIRECTIVE_041's current intent text (move it, do not paraphrase away its content: earning a place by failing exactly on contract violation; passing for the wrong reason; failing on behaviour-neutral change; friction hides regressions and pressures good changes to be reverted).
- `principles` (one or two sentences each): false confidence vs false friction; the desiderata are the value system (trade-offs; the twelve properties live in the testing pack's checklist asset, name it in words, no id reference needed in prose); a double is a hand-written second copy of a collaborator's contract (connascence of algorithm) kept in step only by discipline, and asserting its calls adds connascence of name, position and execution across the boundary; boundary-only mocking is a project policy choice stronger than its sources (Beck's desiderata never mention mocks); connascence is a diagnostic lens, not proof; removing owned doubles moves residual risk to runtime, so contract tests at real boundaries stay; boundaries are re-audited as the architecture moves.
- Neutral wording; no Spec Kitty incident, issue number or core symbol (NFR-003).

### T002 — Shrink DIRECTIVE_041's intent

File: `packs/foundation/directives/041-tests-as-scaffold-not-friction.directive.yaml`. Replace `intent` with two short sentences: the binding rules for tests as scaffold; the mindset and why live in the paradigm `tests-as-scaffold-not-friction`. Do NOT change id, title, `enforcement`, `scope`, `integrity_rules` or `validation_criteria` (C-003; verify with `git diff` that only `intent` changed). No prose stating binding strength (`check_vocabulary.py`).

### T003 — Declare the anti-pattern nodes

New shard `packs/foundation/anti_pattern.graph.yaml` (same header as sibling shards: `schema_version: '1.0'`, `generated_at: STATIC`, `generated_by: drg-migration-v1`, `nodes`, `edges: []`):

- `anti_pattern:mock-owned-logic-to-pin-a-call-contract`, label "Mock owned logic to pin a call contract".
- `anti_pattern:assert-on-mock-interactions`, label "Assert on mock interactions".

Anti-pattern nodes emit no edges.

### T004 — Wire the edges

Every new edge carries `when` (or `reason` on `rejects`); at most one edge per unordered pair per pack (`tests/ci/test_graph_edge_identity.py`). Check existing pairs before adding.

- `paradigm.graph.yaml`: node `paradigm:tests-as-scaffold-not-friction`; `rejects` both anti-patterns.
- `directive.graph.yaml`: `DIRECTIVE_041 --refines--> paradigm`, `DIRECTIVE_054 --refines--> paradigm`; `DIRECTIVE_054 --rejects-->` both anti-patterns.
- `procedure.graph.yaml`: `unfake-an-over-mocked-test --rejects--> mock-owned-logic-to-pin-a-call-contract`.
- `tactic.graph.yaml`: `test-boundaries-by-responsibility --rejects--> mock-owned-logic-...`; `function-over-form-testing --rejects--> assert-on-mock-interactions`.
- The paradigm is reached via 041/054's `refines` edges (charter cascade walks refines); no action scope edge is added.

### T005 — Validate

`CHARTER_CONTRACT_DIR=... bash scripts/ci/validate-packs.sh`, `python3 -m pytest -q tests`, `python3 scripts/ci/check_vocabulary.py`. Digests are restamped in WP05.

## Definition of Done

- Paradigm validates; 041 diff touches only `intent`; 2 refines edges and 5 rejects edges exist; anti-pattern shard has 2 nodes, no edges.
- Gates above green.

## Risks and reviewer guidance

- First `refines` edges in foundation: confirm the schema enum admits `refines` and no `tension` edge was authored.
- Reviewer: diff 041's integrity rules and validation criteria against `main` (must be identical).
