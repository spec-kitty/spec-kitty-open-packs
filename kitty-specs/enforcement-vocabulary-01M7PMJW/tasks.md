# Tasks: Directive enforcement vocabulary

**Mission**: `enforcement-vocabulary-01M7PMJW` · **Planning/merge branch**: `issue-233-enforcement-vocabulary` (PR → `main`), topology `single_branch`
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [occurrence_map.yaml](occurrence_map.yaml), issue #233

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | `term:spec-kitty-core/enforcement-level`; a pointer in the `directive` term | WP01 | |
| T002 | adversarial-squad term: drop "and advisory" | WP01 | [P] |
| T003 | Authoring guide and artefact reference point to the term | WP01 | [P] |
| T004 | `doctrine-instruction-voice` principle: state the rule, not its strictness | WP01 | [P] |
| T005 | Re-check the ADR and index against the final term | WP01 | |
| T006 | Guard tests first (red): patterns refused, other-sense controls pass | WP02 | |
| T007 | `SELF_BINDING` rule in `check_vocabulary.py` | WP02 | |
| T008 | Guard green on the swept tree | WP02 | |
| T009 | DIRECTIVE_051 scope and fifth integrity rule | WP03 | |
| T010 | DIRECTIVE_052, DIRECTIVE_049, reconcile-change-scope-tensions; 028 confirmed | WP03 | [P] |
| T011 | internal, qa and writing directives (cloud-session, QA_001 title, QA_002, ACTION_ITEM_ATTRIBUTION, 042) | WP03 | [P] |
| T012 | Re-read all 59 directives; no `enforcement:` value changed | WP03 | |
| T013 | software-dev substeps, `content` header, 6 prompt/guideline files (ASCII) | WP04 | |
| T014 | plan mission-type substep and the supply-chain tactic | WP04 | [P] |
| T015 | Graph edge reasons (5) | WP04 | [P] |
| T016 | cave-kitty steps, README and styleguide; writing agents, styleguides and tactic | WP04 | [P] |
| T017 | Phrase grep empty; ASCII test | WP04 | |
| T018 | Version bumps per DIRECTIVE_018; built-in lockstep | WP05 | |
| T019 | Manifests, digests, pack pages | WP05 | |
| T020 | Changelog entry | WP05 | |
| T021 | All gates | WP05 | |

## WP01 – Level vocabulary defined once

Prompt: [tasks/WP01-level-vocabulary.md](tasks/WP01-level-vocabulary.md). Subtasks:

T001 enforcement-level term (WP01)
T002 adversarial-squad term reword (WP01)
T003 authoring guide and artefact reference (WP01)
T004 styleguide principle (WP01)
T005 ADR re-check (WP01)

Requirements FR-001, FR-002, FR-003, FR-008. No dependencies. Risk: the definition promising core behaviour; keep it to "the adopting charter decides".

## WP02 – Guard keeps the class closed

Prompt: [tasks/WP02-guard.md](tasks/WP02-guard.md). Subtasks:

T006 tests first (WP02)
T007 rule (WP02)
T008 green check (WP02)

Requirement FR-009. No dependencies (red-first; green once WP03 and WP04 are in). Risk: false positives on other senses; the controls guard it.

## WP03 – Directive bodies swept, every pack

Prompt: [tasks/WP03-directive-sweep.md](tasks/WP03-directive-sweep.md). Subtasks:

T009 DIRECTIVE_051 (WP03)
T010 052, 049, reconcile, 028 (WP03)
T011 internal, qa, writing directives (WP03)
T012 full re-read (WP03)

Requirements FR-004, FR-005, NFR-003, C-003, C-004. No dependencies. Risk: losing rule substance; every removal is named in research.md R5 and the PR body.

## WP04 – Steps, prompts, tactic and citing content swept

Prompt: [tasks/WP04-citing-content-sweep.md](tasks/WP04-citing-content-sweep.md). Subtasks:

T013 software-dev steps (WP04)
T014 plan mission type and tactic (WP04)
T015 graph reasons (WP04)
T016 writing and cave-kitty prose (WP04)
T017 check (WP04)

Requirements FR-006, FR-007, NFR-002. No dependencies.

## WP05 – Versions, changelog, digests and pages

Prompt: [tasks/WP05-release-surface.md](tasks/WP05-release-surface.md). Subtasks:

T018 versions (WP05)
T019 manifests, digests, pages (WP05)
T020 changelog (WP05)
T021 gates (WP05)

Requirements FR-010, NFR-001. Depends on WP01, WP02, WP03, WP04.
