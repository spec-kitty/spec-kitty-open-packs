# Tasks: Test doctrine 2

**Mission**: `test-doctrine-2-01M7YH30` · **Planning branch**: `t3/test-doctrine-2` · **Merge target**: `t3/test-doctrine-2`
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md)

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Author the `tests-as-scaffold-not-friction` paradigm | WP01 | |
| T002 | Shrink DIRECTIVE_041's intent to a pointer (rules unchanged) | WP01 | |
| T003 | Declare the two anti-pattern nodes (new `anti_pattern.graph.yaml`) | WP01 | |
| T004 | Wire paradigm, refines and rejects edges in the foundation shards | WP01 | |
| T005 | Validate WP01 (schema, edge identity, vocabulary) | WP01 | |
| T006 | Foundation exemplar assets (slicing, unfake) + `asset.graph.yaml` + suggests edges | WP02 | [P] |
| T007 | Testing checklist assets (desiderata, Quad-A) + fragment nodes and requires edges | WP02 | [P] |
| T008 | Dedup: desiderata styleguide, quadruple-a styleguide, python/java/typescript conventions + their fragments | WP02 | |
| T009 | Slicing content in `test-boundaries-by-responsibility` and two traps in the desiderata styleguide | WP02 | |
| T010 | Curator profile (`doctrine-daphne`) canonical structure | WP02 | [P] |
| T011 | Fold-ins: DIRECTIVE_034 comment, testing-principles core residue | WP02 | [P] |
| T012 | Foundation glossary terms: tracer bullet, horizontal slicing, spine, green mode | WP03 | |
| T013 | `tdd-red-green-refactor`: vertical slices, anti-patterns, seams, green-mode hand-off, attribution | WP03 | |
| T014 | Green mode owned by `disciplined-refactoring-cycle`; pointers in test-first-cycle, acceptance-test-first, test-first-bug-fixing; refactoring-catalog links | WP03 | |
| T015 | `vertical-skeleton-first` tactic in planning-analysis + fragment wiring | WP03 | |
| T016 | Spine pointer in software-dev plan and tasks guidance; product-coherence-review link | WP03 | |
| T017 | `shared-machine-test-measurement` tactic in testing + wiring | WP04 | [P] |
| T018 | Internal pointer for host specifics | WP04 | [P] |
| T019 | Version bumps (DIRECTIVE_018) | WP05 | |
| T020 | Manifests, digests, built-in digest constant, generated pack pages | WP05 | |
| T021 | Changelog entry and full gate run | WP05 | |

## Phase 1 — Mindset split (operator: first)

### WP01 — Tests-as-scaffold paradigm, 041 split and anti-pattern nodes ([prompt](tasks/WP01-paradigm-and-041-split.md))

- **Goal**: FR-001, FR-002, FR-003. **Priority**: P1. **Independent test**: the paradigm validates; 041 and 054 refine it; 041's rules are byte-identical; the anti-pattern nodes are rejected by five artefacts.
- **Subtasks**:

T001 Author the paradigm (WP01)
T002 Shrink 041's intent (WP01)
T003 Declare anti-pattern nodes (WP01)
T004 Wire the edges (WP01)
T005 Validate (WP01)

- **Dependencies**: none.
- **Risks**: first `refines` edges in foundation; must not create a tension edge.

## Phase 2 — Reference assets and tracer bullets

### WP02 — Reference assets, checklist dedup, slicing content and curator ([prompt](tasks/WP02-assets-dedup-slicing-curator.md))

- **Goal**: FR-004 to FR-009, FR-016. **Priority**: P1. **Independent test**: four asset nodes with inbound edges; desiderata list and Quad-A skeleton stated in full once.
- **Subtasks**:

T006 Foundation exemplar assets (WP02)
T007 Testing checklist assets (WP02)
T008 Dedup the restatements (WP02)
T009 Slicing content (WP02)
T010 Curator profile (WP02)
T011 Fold-ins (WP02)

- **Dependencies**: Depends on WP01 (paradigm and anti-pattern nodes are edge endpoints).
- **Risks**: 255-character cap on styleguide principle descriptions; first foundation asset shard.

### WP03 — Tracer-bullet TDD, green-mode refactoring and vertical-skeleton-first ([prompt](tasks/WP03-tracer-bullets-green-mode-spine.md))

- **Goal**: FR-010 to FR-014 (#154 and #147 together). **Priority**: P2. **Independent test**: no TDD surface carries its own refactor steps; the tactic exists and is reachable from plan, tasks and product-coherence-review; four glossary terms.
- **Subtasks**:

T012 Glossary terms (WP03)
T013 TDD tactic (WP03)
T014 Green mode (WP03)
T015 vertical-skeleton-first (WP03)
T016 Plan/tasks pointer (WP03)

- **Dependencies**: Depends on WP01 (operator order; shares foundation shards).
- **Risks**: ASCII in software-dev files; wording must agree with DISCIPLINED_REFACTORING.

## Phase 3 — Parallel

### WP04 — Measurement discipline for shared machines ([prompt](tasks/WP04-measurement-discipline.md))

- **Goal**: FR-015 (#152). **Priority**: P2. **Independent test**: tactic validates, reachable at implement and review, no host specifics in testing.
- **Subtasks**:

T017 Measurement tactic (WP04)
T018 Internal pointer (WP04)

- **Dependencies**: none (may run in parallel).
- **Risks**: overlap with `no-parallel-duplicate-test-runs` and QA_003.

## Phase 4 — Release

### WP05 — Release surface ([prompt](tasks/WP05-release-surface.md))

- **Goal**: FR-017, NFR-001. **Priority**: P1.
- **Subtasks**:

T019 Version bumps (WP05)
T020 Restamp and regenerate (WP05)
T021 Changelog and gates (WP05)

- **Dependencies**: Depends on WP01, WP02, WP03, WP04.
- **Risks**: Mission D overlap in the foundation digest and version restamp (rebase and restamp).

## MVP

WP01 (the paradigm and the 041 split) is the smallest slice with standalone value.
