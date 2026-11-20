# Implementation Plan: Test doctrine: mock boundary and red-first value

**Branch**: `t3/test-doctrine-mock-boundary` | **Date**: 2026-11-20 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/test-doctrine-01M7X00D/spec.md`

Branch contract: the current branch, the planning/base branch and the merge target are all `t3/test-doctrine-mock-boundary` (`branch_matches_target: true`). The pull request goes from that branch to `main`.

## Summary

Add a foundation directive, `DIRECTIVE_054` "Mock Only at the Responsibility Boundary", with the operator's widened allow-list, plus a remediation procedure, and wire both into the doctrine graph so they load at implement and review. Bring every surface that lists mock seams into line with it. Scope DIRECTIVE_034's red-first rule to lasting regression risk; the non-vacuity tactic gains an `[evidenced-by-run]` delivery label and the long-term-value question, and the ATDD, TDD and review surfaces point to those owners. Fold #151 into the `red-first-bug-reproduction` procedure. Edit DIRECTIVE_041 minimally so it does not contradict either change. Put the Spec Kitty CI worked example in the `internal` pack. Then version, restamp and document.

## Technical Context

**Language/Version**: YAML and Markdown pack content (`schema_version: "1.0"`), validated against the charter contract at the pin in `charter.lock.yaml` (charter `33f3ad4`)
**Primary Dependencies**: `pyyaml==6.0.3`, `jsonschema==4.26.0`, `tree-sitter==0.25.2`, `tree-sitter-java==0.23.5`, `pytest` (already used by CI; nothing added)
**Storage**: files under `packs/`, `docs/`, `tests/ci/test_pack_digest.py` (built-in digest constant)
**Testing**: no new tests. This is content work; under the mission's own carve-out the evidence is the existing gates (`validate-packs.sh` with derived manifests, `pytest tests` including `test_graph_edge_identity.py`, `test_glossary_content.py`, `test_software_dev_ascii.py`, `test_prompt_fragments.py`, `check_vocabulary.py`, `gen_pack_reference.py --check`, `check-pack-digests.sh`, `check_docs_freshness.py`) and the charter-service check
**Target Platform**: the charter service at the pin, and the docs site
**Project Type**: content repository (doctrine packs)
**Performance Goals**: N/A (content only)
**Constraints**: one edge per unordered pair per pack (C-004); no core references in consumer packs (NFR-003); no enforcement prose in directive bodies (C-006); software-dev content ASCII-only (NFR-002); one owner per rule (NFR-004)
**Scale/Scope**: 2 new artefacts in foundation, 1 in internal; about 25 edited artefacts across foundation, testing, qa and internal; 4 graph files; 2 glossary terms; the lockstep version set

## Charter Check

- **Docs are a first-class deliverable**: pack pages regenerated, never hand-edited; changelog entry; touched authored docs get a fresh `updated:`. PASS.
- **Decisions are recorded**: the operator rulings are recorded as decision moments in the mission; no ADR, because no pack schema, layout or repository-level decision changes. The versioning call (minor) is recorded in research.md R4. PASS.
- **Gates fail closed**: all gates run locally before push and in CI. PASS.
- **Tests only where they guard real behaviour (DIRECTIVE_041)**: no new tests; the existing gates are the evidence, which is exactly the carve-out this mission writes. PASS.
- **Identity discipline**: no `pack_id`, artefact id or file name changes; one new directive id minted (054). PASS.
- **DIRECTIVE_018**: minor bumps (research.md R4). PASS.
- **DIRECTIVE_051 (supply chain)**: no dependency is added, upgraded or removed. N/A.
- **Alignment**: charter, not core (AGENTS.md); core wording (its charter's ATDD section) aligns at its own pin bump. PASS.

## Design decisions

1. **Directive plus procedure, not a tactic extension.** The rule must be citable as binding (the issue asks for a reviewer lens), so it is a directive. The how-to (classify mocks, seed real state, move assertions) is a procedure that the directive requires. `test-boundaries-by-responsibility` stays the tactic for drawing the boundary and points to 054 for the seam list.
2. **"Boundary", not "border".** Existing doctrine uses "responsibility boundary" (DIRECTIVE_036 and the black-box family). The directive title and text use "boundary"; the glossary records "responsibility border" as an alias.
3. **Allow-list permits, never requires.** Every seam surface says the listed seams *may* be substituted. A test that runs a real filesystem in a temp dir is fine.
4. **Owner map (NFR-004).** Allow-list and anti-pattern: DIRECTIVE_054. Carve-out: DIRECTIVE_034. Label and long-term-value question: `acceptance-criteria-non-vacuity`. Failure text, characterization inversion, cross-work-package strict expected failure: `red-first-bug-reproduction`. Red shape: DIRECTIVE_034 (already there). CI example: internal tactic. Every other surface uses at most one sentence and names the owner.
5. **Evidence record location.** `[evidenced-by-run]` names the run or gate inline in the requirement row (or the WP's evidence note); for workflows, the existing `kitty-specs/<mission>/workflow-evidence.md` from the implement prompt is the record. The review step checks the cited record exists.
6. **DIRECTIVE_041, minimal.** Rule 3 ("Deleting a test deletes its coverage ...") gains the exception for a change-detector test whose evidence is recorded; the "no new xfail" criterion gains the exception for a strict expected failure on a reproduction whose fix is planned in a named sibling work package. Intent, title and other rules unchanged. No tension edge: the reconciliation is in the text.
7. **Graph edges (research.md R3)** are hand-edited in the per-kind foundation graph files and in the testing, qa and internal fragments with `foundation::` URNs. No new 034-041 edge (one already exists).
8. **No new tests.** Each WP's acceptance is shown by the existing gates and by greps recorded in the WP's evidence note.

## Project Structure

### Documentation (this mission)

```
kitty-specs/test-doctrine-01M7X00D/
├── spec.md
├── plan.md               # this file
├── research.md           # owner map, surface inventory, edge map, versioning
├── quickstart.md         # gate commands
├── checklists/requirements.md
├── decisions/            # operator-ruling decision moments
├── traces/               # tracer files
└── tasks.md              # /spec-kitty.tasks output
```

### Source (repository root)

```
packs/foundation/directives/054-mock-only-at-the-responsibility-boundary.directive.yaml   (new)
packs/foundation/procedures/unfake-an-over-mocked-test.procedure.yaml                     (new)
packs/foundation/directives/{034,036,041}-*.directive.yaml
packs/foundation/tactics/testing/*.tactic.yaml   (non-vacuity, acceptance-test-first, tdd, boundaries, scaffolding smell, black-box, function-over-form, select-level)
packs/foundation/procedures/{red-first-bug-reproduction,test-first-cycle,observable-contract-test-authoring}.procedure.yaml
packs/foundation/agent_profiles/reviewer-renata.agent.yaml
packs/foundation/missions/software-dev/{steps/implement.prompt.md,steps/review.prompt.md,steps/specify.prompt.md,templates/spec-template.md}
packs/foundation/{directive,procedure,action,agent_profile}.graph.yaml
packs/foundation/glossaries/spec-kitty-core.glossary.yaml
packs/testing/{tactics/testing/atdd-adversarial-acceptance.tactic.yaml,procedures/test-first-bug-fixing.procedure.yaml,styleguides/test-desiderata-and-boundaries.styleguide.yaml,styleguides/testing-principles.styleguide.yaml,drg/fragment.yaml}
packs/qa/drg/fragment.yaml
packs/internal/{tactics/spec-kitty-ci-workflow-evidence-exemplar.tactic.yaml (new),drg/fragment.yaml,procedures/cloud-session-dispatch.procedure.yaml,procedures/landing-contributor-prs.procedure.yaml,skills/mission-from-issue.skill.md}
packs/*/pack.yaml, packs/*.source.yaml, packs/*/pack-manifest.yaml, docs/packs/*.md, tests/ci/test_pack_digest.py, docs/changelog/CHANGELOG.md
```

## Implementation Concern Map

### IC-01 — Mock-boundary rule and wiring (FR-001, FR-002, FR-004, FR-012)
New directive 054 and the remediation procedure; nodes and edges in the foundation graph (actions implement and review, three foundation profiles, 054 requires 041 and the procedure, 036 requires 054); the two glossary terms; DIRECTIVE_036 scope pointer.

### IC-02 — Seam surfaces agree (FR-003)
Every surface that lists seams or mocking rules either names 054 as the owner or lists a subset of its categories, with "may", never "must". Cross-pack: testing styleguides, and the qa test-designer profile edge.

### IC-03 — Red-first carve-out (FR-005 to FR-008, FR-010)
034 owns the carve-out; the non-vacuity tactic owns the label and the question; ATDD/TDD surfaces, the implement prompt, the spec template and specify legend, the review step, 041, `observable-contract-test-authoring` and reviewer-renata align.

### IC-04 — Red for the right reason (FR-009)
`red-first-bug-reproduction` gains the three owned points; testing `test-first-bug-fixing` points to it and allows the cross-WP case.

### IC-05 — House specifics (FR-011)
Internal tactic with the CI-workflow example; internal surfaces point to the carve-out.

### IC-06 — Release surface (FR-013)
Versions, manifests, digests, built-in digest constant, pack pages, changelog.

## Complexity Tracking

No charter violations to justify.
