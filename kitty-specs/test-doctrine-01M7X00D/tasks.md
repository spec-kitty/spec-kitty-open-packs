# Tasks: Test doctrine: mock boundary and red-first value

**Mission**: `test-doctrine-01M7X00D` · **Planning/merge branch**: `t3/test-doctrine-mock-boundary` (PR → `main`), topology `single_branch`
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [quickstart.md](quickstart.md), issues #216, #209, #151

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | Author DIRECTIVE_054 (allow-list, anti-pattern, worked example) | WP01 | |
| T002 | Author procedure unfake-an-over-mocked-test | WP01 | [P] |
| T003 | Glossary terms: responsibility boundary, change-detector test | WP01 | [P] |
| T004 | DIRECTIVE_036 scope pointer to 054 | WP01 | [P] |
| T005 | Foundation graph wiring (nodes, directive, action, profile edges) | WP01 | |
| T006 | implementer-ivan reference; gates | WP01 | |
| T007 | test-boundaries-by-responsibility seam list and failure mode | WP02 | |
| T008 | Other foundation testing tactics' seam sentences | WP02 | [P] |
| T009 | Testing styleguides (desiderata, testing-principles) | WP02 | [P] |
| T010 | qa test-designer edge; gates | WP02 | |
| T011 | DIRECTIVE_034 owns the carve-out | WP03 | |
| T012 | Non-vacuity tactic: [evidenced-by-run], long-term-value question | WP03 | |
| T013 | acceptance-test-first, tdd-red-green-refactor, test-first-cycle | WP03 | [P] |
| T014 | testing atdd-adversarial-acceptance | WP03 | [P] |
| T015 | DIRECTIVE_041 minimal edit (two places) | WP03 | |
| T016 | observable-contract-test-authoring and reviewer-renata | WP03 | |
| T017 | Gates | WP03 | |
| T018 | implement.prompt.md | WP04 | |
| T019 | review.prompt.md (4a mock boundary, change detector; 4b evidence exists) | WP04 | |
| T020 | specify.prompt.md and spec-template.md label legend | WP04 | [P] |
| T021 | Gates (ASCII) | WP04 | |
| T022 | red-first-bug-reproduction owns the #151 points | WP05 | |
| T023 | testing test-first-bug-fixing points to it | WP05 | |
| T024 | Gates | WP05 | |
| T025 | Internal CI-workflow evidence exemplar tactic | WP06 | |
| T026 | Internal wiring | WP06 | |
| T027 | Internal surfaces point to the carve-out; gates | WP06 | |
| T028 | Versions (minor, lockstep) | WP07 | |
| T029 | Manifests, digests, built-in constant, pages | WP07 | |
| T030 | Changelog | WP07 | |
| T031 | All gates incl. docs freshness | WP07 | |

## WP01 – Mock-boundary directive, remediation procedure and graph wiring

Prompt: [tasks/WP01-mock-boundary-directive.md](tasks/WP01-mock-boundary-directive.md). Subtasks:

T001 DIRECTIVE_054 (WP01)
T002 remediation procedure (WP01)
T003 glossary terms (WP01)
T004 DIRECTIVE_036 pointer (WP01)
T005 graph wiring (WP01)
T006 profile reference and gates (WP01)

Requirements FR-001, FR-002, FR-004, FR-012, FR-003 (036 part). No dependencies. Risks: edge-identity collisions; enforcement prose in the directive body.

## WP02 – Every seam list agrees with DIRECTIVE_054

Prompt: [tasks/WP02-seam-surfaces-agree.md](tasks/WP02-seam-surfaces-agree.md). Subtasks:

T007 boundaries tactic (WP02)
T008 other foundation tactics (WP02)
T009 testing styleguides (WP02)
T010 qa edge and gates (WP02)

Requirements FR-003, FR-004 (qa edge). Depends on WP01. Risk: a second full copy of the allow-list (NFR-004).

## WP03 – Red-first scoped to lasting regression risk

Prompt: [tasks/WP03-red-first-carve-out.md](tasks/WP03-red-first-carve-out.md). Subtasks:

T011 DIRECTIVE_034 (WP03)
T012 non-vacuity tactic (WP03)
T013 ATDD/TDD tactics and test-first-cycle (WP03)
T014 atdd-adversarial-acceptance (WP03)
T015 DIRECTIVE_041 (WP03)
T016 observable-contract-test-authoring, reviewer-renata (WP03)
T017 gates (WP03)

Requirements FR-005, FR-006, FR-007, FR-010. Depends on WP01 (reviewer-renata names 054). Risk: the carve-out read as "no evidence needed".

## WP04 – Software-dev implement, review and specify surfaces

Prompt: [tasks/WP04-software-dev-mission-surfaces.md](tasks/WP04-software-dev-mission-surfaces.md). Subtasks:

T018 implement prompt (WP04)
T019 review prompt (WP04)
T020 specify prompt and spec template (WP04)
T021 gates (WP04)

Requirements FR-007, FR-008. Depends on WP01, WP03. Risk: non-ASCII characters (NFR-002).

## WP05 – Red for the right reason, verifiably

Prompt: [tasks/WP05-red-for-the-right-reason.md](tasks/WP05-red-for-the-right-reason.md). Subtasks:

T022 red-first-bug-reproduction (WP05)
T023 test-first-bug-fixing (WP05)
T024 gates (WP05)

Requirements FR-009. Depends on WP03 (041 and observable-contract wording). Risk: duplicating DIRECTIVE_034 or delete-the-assertion-not-the-test.

## WP06 – Spec Kitty house specifics in the internal pack

Prompt: [tasks/WP06-internal-house-specifics.md](tasks/WP06-internal-house-specifics.md). Subtasks:

T025 internal exemplar tactic (WP06)
T026 internal wiring (WP06)
T027 internal surfaces and gates (WP06)

Requirements FR-011. Depends on WP03.

## WP07 – Release surface

Prompt: [tasks/WP07-release-surface.md](tasks/WP07-release-surface.md). Subtasks:

T028 versions (WP07)
T029 restamps (WP07)
T030 changelog (WP07)
T031 gates (WP07)

Requirements FR-013. Depends on WP01-WP06.

## Sequencing

WP01 → (WP02, WP03) → (WP04, WP05, WP06) → WP07. Single-branch topology: run WPs one at a time on `t3/test-doctrine-mock-boundary`.
