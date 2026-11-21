---
work_package_id: WP02
title: Reference assets, checklist dedup, slicing content and curator
dependencies:
- WP01
requirement_refs:
- FR-004
- FR-005
- FR-006
- FR-007
- FR-008
- FR-009
- FR-016
- NFR-004
- NFR-005
- SC-002
- SC-003
planning_base_branch: t3/test-doctrine-2
merge_target_branch: t3/test-doctrine-2
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-2 unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
- T008
- T009
- T010
- T011
history:
- at: '2026-11-21T08:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/testing/assets/
create_intent:
- packs/foundation/assets/exemplar-slicing-user-registration.md
- packs/foundation/assets/exemplar-slicing-user-registration.md.asset.yaml
- packs/foundation/assets/exemplar-unfake-an-over-mocked-test.md
- packs/foundation/assets/exemplar-unfake-an-over-mocked-test.md.asset.yaml
- packs/foundation/asset.graph.yaml
- packs/testing/assets/test-desiderata-checklist.md
- packs/testing/assets/test-desiderata-checklist.md.asset.yaml
- packs/testing/assets/quad-a-test-structure.md
- packs/testing/assets/quad-a-test-structure.md.asset.yaml
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/assets/**
- packs/foundation/asset.graph.yaml
- packs/foundation/tactics/testing/test-boundaries-by-responsibility.tactic.yaml
- packs/foundation/directives/034-test-first-development.directive.yaml
- packs/testing/assets/**
- packs/testing/styleguides/test-desiderata-and-boundaries.styleguide.yaml
- packs/testing/styleguides/testing-principles.styleguide.yaml
- packs/testing/styleguides/quadruple-a-test-format.styleguide.yaml
- packs/testing/drg/fragment.yaml
- packs/python/styleguides/python-conventions.styleguide.yaml
- packs/python/drg/fragment.yaml
- packs/java/styleguides/java-conventions.styleguide.yaml
- packs/java/drg/fragment.yaml
- packs/javascript/styleguides/typescript-conventions.styleguide.yaml
- packs/javascript/drg/fragment.yaml
- packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml
role: implementer
tags: []
tracker_refs:
- '#216'
- '#273'
- '#274'
---
# Work Package Prompt: WP02 – Reference assets, checklist dedup, slicing content and curator

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

Ship the four reference assets, cut the restated checklists to pointers, add the test-slicing content, pin the curator's canonical structure, and clear the #273/#274 residue in DIRECTIVE_034 and testing-principles (FR-004 to FR-009, FR-016). Read `spec.md`, `plan.md` (IC-02), `research.md` (R2-R4) and `data-model.md` first.

## Branch Strategy

Planning branch and merge target: `t3/test-doctrine-2`; lanes from `lanes.json`. Implement with `spec-kitty agent action implement WP02 --agent <name> --mission test-doctrine-2-01M7YH30`.

Out-of-map edits (recorded): the `suggests` edges from foundation artefacts to the exemplar assets go in `packs/foundation/directive.graph.yaml`, `procedure.graph.yaml` and `tactic.graph.yaml`, owned by WP01, on which this WP depends.

## Subtasks

### T006 — Foundation exemplar assets

Asset = Markdown payload under `assets/` plus `<file>.asset.yaml` sidecar (`id`, `mime: text/markdown`, `path` relative to `assets/`, `title`); declare nodes in a new `packs/foundation/asset.graph.yaml` shard (model: `packs/writing/asset.graph.yaml`).

- `exemplar-slicing-user-registration.md`: the functional-slicing case after Clear Test Boundaries (https://patterns.sddevelopment.be/practices/define_test_boundaries/): an API-level registration test mocks the internal business service and verifies one `createUser` call; adding a Captcha step breaks most API-level tests though registration still works; the re-scoped `UserRegistrationTest` covers the whole functional slice, lets the business service and the email validation run for real, substitutes only the database proxy (an allow-listed seam of DIRECTIVE_054), and asserts the registration outcome. Include short before/after code, the boundary statement, the two boundary-check questions, and state honestly that the case is analogical (it supports the argument, it is not proof). Attribute the source.
- `exemplar-unfake-an-over-mocked-test.md`: full before/after of the order-fulfilment example summarised in `unfake-an-over-mocked-test` (stubbed shipment recording -> no shipment stored -> a later step fails like data loss; after: real recording on orders created through the real pipeline, only the carrier network call substituted, assert on stored shipments). Walk the procedure's steps against it. No Spec Kitty incident (NFR-003).
- Edges (WP01's shards, out-of-map): `tactic:test-boundaries-by-responsibility --suggests--> asset:exemplar-slicing-user-registration`; `procedure:unfake-an-over-mocked-test --suggests--> asset:exemplar-unfake-an-over-mocked-test`; `directive:DIRECTIVE_054 --suggests--> asset:exemplar-unfake-...`; `paradigm:tests-as-scaffold-not-friction --suggests--> asset:exemplar-slicing-...` (paradigm shard). Each with `when`.

### T007 — Testing checklist assets

In `packs/testing/assets/`, nodes declared in `packs/testing/drg/fragment.yaml` with `kind: assets`, `body_path: assets/<file>.asset.yaml` (model: event-driven pack).

- `test-desiderata-checklist.md`: Beck's twelve desiderata, one checklist line each (the current styleguide wording, kept), plus the "Isolated is order independence, not isolation from collaborators via mocks" note; cite https://testdesiderata.com/.
- `quad-a-test-structure.md`: language-neutral four-phase skeleton (Arrange, Assumption check, Act, Assert, labelled) and a short review checklist (one action per test, the assumption check fails on a wrong fixture, the assert targets an observable outcome, two Act phases mean two tests).
- Edges: `styleguide:test-desiderata-and-boundaries --requires--> asset:test-desiderata-checklist`; `styleguide:testing-principles --requires--> asset:test-desiderata-checklist`; `styleguide:quadruple-a-test-format --requires--> asset:quad-a-test-structure`; `foundation::paradigm:tests-as-scaffold-not-friction --suggests--> asset:test-desiderata-checklist`.

### T008 — Dedup the restatements

- `test-desiderata-and-boundaries`: replace the twelve per-property principles (Isolated ... Inspiring) with one principle pointing to the checklist asset; keep "Desiderata are trade-offs", the boundary principles and the rest. Patterns that name properties stay readable.
- `quadruple-a-test-format`: keep principles and language examples; add a pointer that the skeleton and checklist live in the asset.
- `python-conventions`, `java-conventions`, `typescript-conventions`: the Quad-A principle becomes one pointer line ("Quad-A, as the testing pack's quad-a-test-structure asset and quadruple-a-test-format styleguide define"); the Quad-A pattern keeps only its language-specific example. Each pack's fragment gains `styleguide:<x>-conventions --requires--> testing::asset:quad-a-test-structure` with `when`. Each pack already depends on testing (check the range covers the WP05 version).

### T009 — Slicing content

- `test-boundaries-by-responsibility`: in step 1 say identify the functionality, not the class; add a step or failure mode: a well-scoped unit test needs few substitutes (needing a double of owned logic means a misdrawn boundary), write tests as if unaware of internal structure (extracting a helper must not change the suite), and re-audit boundaries when the architecture moves. Keep within tactic schema.
- `test-desiderata-and-boundaries`: one-line anti-pattern or principle each for the gold-plating misread ("avoid gold plating" is not licence to double owned logic for speed) and the connascence of a mock (a stub is a second copy of the contract). Principle descriptions max 255 characters.

### T010 — Curator profile

`doctrine-daphne`: add once (secondary-awareness or avoidance-boundary): assets live under the pack's `assets/` (a category subdirectory allowed) with a `<file>.asset.yaml` sidecar and an asset node; anti-patterns are nodes, `rejects` targets, emitting no edges; worked examples are referenced from the good artefacts, never emitted from anti-pattern nodes. The inbound-edge rule already exists; do not duplicate it.

### T011 — Fold-ins (#273, #274; files limited to these two)

- DIRECTIVE_034: delete the trailing provenance comment block (mission/WP/#3009 overlay history).
- `testing-principles`: remove "PR #2308 ... (commit 50abe2fdc) ... (commit 052d465e9)" keeping the lesson (a re-pinned literal scan was retired with surviving-coverage proof; a single-file LOC ceiling was replaced by a project-wide metric); replace `resolve_planning_read_dir` / `primary_feature_dir_for_mission` with neutral symbols.

## Definition of Done

- 4 asset payloads + sidecars + nodes, each with an inbound edge (NFR-005); the twelve desiderata and the Quad-A skeleton appear in full once (SC-003).
- Gates: validate-packs, pytest, vocabulary.

## Risks and reviewer guidance

- Reviewer: grep for the twelve property names across packs to confirm one full list; check every asset sidecar `path` resolves; confirm no core references were added.
