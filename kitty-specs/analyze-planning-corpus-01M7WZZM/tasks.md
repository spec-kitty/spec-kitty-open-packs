# Work Packages: Analyze: full planning corpus and product coherence

**Inputs**: `kitty-specs/analyze-planning-corpus-01M7WZZM/` — spec.md, plan.md, research.md, quickstart.md
**Prerequisites**: plan.md (Design, Implementation Concern Map), research.md (R-01 … R-09)
**Tests**: required by FR-016 (`tests/ci/test_analyze_readiness_prompts.py`).

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Author tactic `planning-corpus-consistency` | WP01 | [P] |
| T002 | Author tactic `product-coherence-review` | WP01 | [P] |
| T003 | Wire both tactics into `tactic.graph.yaml` (nodes + suggests edges) | WP01 | |
| T004 | Scope both tactics from `action:software-dev/analyze` in `action.graph.yaml` | WP01 | |
| T005 | Analyze step 1-2: corpus inputs, `meta.json`, occurrence map, headings-first loading | WP02 | |
| T006 | Pass G #247 folds and the one-defect ownership rule | WP02 | |
| T007 | Pass H (planning-artifact, `X`) and pass J (product coherence, `M`) | WP02 | |
| T008 | Severity: fold the duplicated untestable rule; `X` normal rules; `M` capped at MEDIUM | WP02 | |
| T009 | Report: prefixes, ordering, sections, Scenario Audit Finding column, recommendation line, metrics, location form | WP02 | |
| T010 | Next Actions, operating principles, line budget check | WP02 | |
| T011 | cave-dev analyze prompt names the new checks | WP03 | [P] |
| T012 | cave-kitty `drg/fragment.yaml` scope edges | WP03 | [P] |
| T013 | Tests: corpus inputs, passes, tactics, prefixes, section order | WP04 | |
| T014 | Tests: severity cap, recommendation line, positive controls | WP04 | |
| T015 | Tests: #247 report content pins and cave-dev parity | WP04 | |
| T016 | Version bump of the foundation lockstep, built-in and cave-kitty | WP05 | |
| T017 | Derive manifests, restamp digests, regenerate pack pages | WP05 | |
| T018 | CHANGELOG `[Unreleased]` entry; run every gate | WP05 | |

## Phase 1 — Foundation

## Work Package WP01: Planning-corpus and product-coherence tactics (Priority: P1)

**Goal**: The two tactics that carry the check detail exist, are valid pack content and are wired to the software-dev analyze action.
**Independent test**: `validate-packs.sh` passes; `spec-kitty charter context --include tactic:planning-corpus-consistency` resolves (best effort); both files carry the steps named in the prompt.
**Prompt**: `tasks/WP01-analysis-tactics.md`
**Requirements**: FR-003, FR-004, FR-006, FR-012, FR-014

Included subtasks:

T001 Author tactic `planning-corpus-consistency` (WP01)
T002 Author tactic `product-coherence-review` (WP01)
T003 Wire both tactics into `tactic.graph.yaml` (WP01)
T004 Scope both tactics from `action:software-dev/analyze` (WP01)

Dependencies: none. Risks: vocabulary guard phrasing ("is advisory"); issue numbers or core paths in pack text.

## Phase 2 — The analyze step (MVP)

## Work Package WP02: Software-dev analyze prompt reviews the planning corpus and product coherence (Priority: P1) MVP

**Goal**: The analyze prompt loads the full corpus, runs passes H and J, reports them in two new sections with prefixes `X`/`M`, ends coherence with the recommendation line, and carries the #247 folds — within 500 lines.
**Independent test**: quickstart scenarios 1-4 and 6 hold on the edited prompt; `wc -l` ≤ 500.
**Prompt**: `tasks/WP02-analyze-prompt.md`
**Requirements**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-018, NFR-001, NFR-002, NFR-004, C-001, C-002, C-003, C-004

Included subtasks:

T005 Analyze steps 1-2: corpus inputs (WP02)
T006 Pass G #247 folds and ownership rule (WP02)
T007 Passes H and J (WP02)
T008 Severity lines (WP02)
T009 Report shape (WP02)
T010 Next Actions, principles, budget (WP02)

Dependencies: WP01 (tactic ids). Risks: 500-line cap; double loading; vocabulary guard.

## Phase 3 — Parity and pins

## Work Package WP03: cave-dev analyze names the same checks (Priority: P3)

**Goal**: The cave-kitty analyze prompt names both passes, the cap and the recommendation line, and its DRG fragment scopes both tactics.
**Prompt**: `tasks/WP03-cave-dev-parity.md`
**Requirements**: FR-015

Included subtasks:

T011 cave-dev analyze prompt (WP03)
T012 cave-kitty fragment edges (WP03)

Dependencies: WP01. Parallel with WP02.

## Work Package WP04: Tests pin the analyze readiness content (Priority: P2)

**Goal**: `tests/ci/test_analyze_readiness_prompts.py` pins every new contract and the #247 content, each with a positive control where a check could pass vacuously.
**Prompt**: `tasks/WP04-analyze-tests.md`
**Requirements**: FR-016, SC-001, SC-002, SC-003

Included subtasks:

T013 Corpus/pass/prefix/section tests (WP04)
T014 Severity cap and recommendation tests (WP04)
T015 #247 pins and cave-dev parity tests (WP04)

Dependencies: WP02, WP03.

## Phase 4 — Release hygiene

## Work Package WP05: Versions, derived outputs and changelog (Priority: P2)

**Goal**: An additive minor bump across the foundation lockstep, built-in and cave-kitty; manifests, digests and pages regenerated by tool; the CHANGELOG entry; every gate green.
**Prompt**: `tasks/WP05-versions-and-changelog.md`
**Requirements**: FR-017, NFR-003, SC-004, C-005, C-006

Included subtasks:

T016 Version bump (WP05)
T017 Derived outputs (WP05)
T018 CHANGELOG, acceptance-criteria trace and gates (WP05)

Dependencies: WP02, WP03, WP04.

## Dependency graph

WP01 → WP02, WP03 → WP04 → WP05

## Parallelization

WP02 and WP03 run in parallel after WP01. WP04 and WP05 are sequential tails.

## MVP Scope

WP01 + WP02 constitute the minimal release: with them the analyze step reviews the planning corpus and product coherence. WP03-WP05 add parity, pins and release hygiene.
