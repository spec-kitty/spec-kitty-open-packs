# Tasks: Citation and docs writing doctrine

**Mission**: `citation-and-docs-writing-01M7YGMQ` · **Planning/merge branch**: `feat/citation-and-docs-writing` (PR → `main`), topology `single_branch`
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [quickstart.md](quickstart.md), issues #219, #150, #238, #240 (folds: #274 slice, #176 slice)

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | Stable-identifier principle, pattern and anti-pattern | WP01 | |
| T002 | Content-anchored principle, pattern and anti-pattern; retrieval-context pointer | WP01 | |
| T003 | specify and plan prompt reminders (ASCII) | WP01 | [P] |
| T004 | adr-drafting-workflow reminder; gates | WP01 | [P] |
| T005 | Squad procedure: first-hand check step and anti-patterns | WP02 | |
| T006 | Squad procedure: no-prototyping sentence; neutral gate example | WP02 | |
| T007 | Internal cloud-session-dispatch: overturned rulings; gates | WP02 | [P] |
| T008 | New writing styleguide ai-writing-tells | WP03 | |
| T009 | report-writing points to it; internal refines edge | WP03 | |
| T010 | Writing graph wiring (docs mission, actions, comms-cleo, citation scope on specify/plan) | WP03 | |
| T011 | Gates | WP03 | |
| T012 | common-docs styleguide: doc-kitty shape | WP04 | |
| T013 | common-docs styleguide: neutral examples, ADR era optional | WP04 | |
| T014 | DIRECTIVE_042 and the three common-docs tactics | WP04 | [P] |
| T015 | declare-page-audience and internal spec-kitty-page-audience; gates | WP04 | [P] |
| T016 | Versions (minor, lockstep) and internal writing range | WP05 | |
| T017 | Manifests, digests, built-in constant, pages | WP05 | |
| T018 | Changelog | WP05 | |
| T019 | All gates incl. docs freshness and the spot-check greps | WP05 | |

## WP01 – Citation rules that survive history rewrites

Prompt: [tasks/WP01-citation-rules.md](tasks/WP01-citation-rules.md). Subtasks:

T001 stable-identifier principle (WP01)
T002 content-anchored principle (WP01)
T003 prompt reminders (WP01)
T004 ADR tactic reminder and gates (WP01)

Requirements FR-001, FR-002, FR-003. No dependencies. Risks: principle descriptions over 255 characters; non-ASCII in prompts.

## WP02 – First-hand checks before a ruling

Prompt: [tasks/WP02-first-hand-checks.md](tasks/WP02-first-hand-checks.md). Subtasks:

T005 first-hand check step (WP02)
T006 no prototyping, neutral example (WP02)
T007 overturned rulings and gates (WP02)

Requirements FR-005, FR-006, FR-007, FR-013 (squad part). No dependencies. Risk: duplicating the findings-disposition contract.

## WP03 – One shared list of AI-writing tells, wired for docs

Prompt: [tasks/WP03-ai-writing-tells.md](tasks/WP03-ai-writing-tells.md). Subtasks:

T008 new styleguide (WP03)
T009 report-writing pointer and refines edge (WP03)
T010 writing graph wiring (WP03)
T011 gates (WP03)

Requirements FR-004, FR-008, FR-009, FR-010. No dependencies. Risks: edge-identity collisions; copying instead of moving the tells.

## WP04 – doc-kitty frontmatter and neutral common-docs examples

Prompt: [tasks/WP04-doc-kitty-frontmatter.md](tasks/WP04-doc-kitty-frontmatter.md). Subtasks:

T012 styleguide shape (WP04)
T013 neutral examples (WP04)
T014 directive and tactics (WP04)
T015 procedures and gates (WP04)

Requirements FR-011, FR-012, FR-013 (docs part). No dependencies. Risk: a sibling surface left teaching the path form.

## WP05 – Release surface

Prompt: [tasks/WP05-release-surface.md](tasks/WP05-release-surface.md). Subtasks:

T016 versions (WP05)
T017 restamp (WP05)
T018 changelog (WP05)
T019 gates (WP05)

Requirements FR-014. Depends on WP01, WP02, WP03, WP04. Risk: a parallel mission bumps the same versions; restamp on rebase.
