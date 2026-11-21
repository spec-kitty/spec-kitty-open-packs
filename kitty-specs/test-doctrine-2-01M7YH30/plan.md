# Implementation Plan: Test doctrine 2: tests-as-scaffold paradigm, tracer bullets and measurement discipline

**Branch**: `t3/test-doctrine-2` | **Date**: 2026-11-21 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/test-doctrine-2-01M7YH30/spec.md`

## Summary

Doctrine content mission over five packs plus the release surface. The #216 residue goes first: a foundation paradigm takes DIRECTIVE_041's mindset (041 and 054 refine it), two anti-pattern nodes are declared in a new foundation `anti_pattern.graph.yaml` shard, two exemplar assets go to `packs/foundation/assets/` (new `asset.graph.yaml` shard), two checklist assets go to `packs/testing/assets/` (testing fragment nodes), and the restated desiderata list and Quad-A definition shrink to pointers. Then the #154/#147 work package sharpens `tdd-red-green-refactor` with tracer-bullet slicing (re-grounded at mattpocock/skills `abeeaf9`), moves refactoring out of the TDD loop into green mode (owned by the existing `disciplined-refactoring-cycle`), adds `vertical-skeleton-first` to planning-analysis and four shared glossary terms. #152 (measurement discipline, testing) runs in parallel. A final work package versions and restamps.

## Technical Context

**Language/Version**: YAML doctrine artefacts (schema_version 1.0) and Markdown assets, validated against the charter pack contracts at the commit pinned in `charter.lock.yaml` (`33f3ad46`)
**Primary Dependencies**: the charter pack schemas (`contracts/packs/`), Python 3 with pyyaml and jsonschema for the repository gates
**Storage**: files in `packs/` (pack content, graph shards and fragments), `docs/packs/` (generated pages), `docs/changelog/`
**Testing**: `scripts/ci/validate-packs.sh`, `pytest tests` (edge identity, glossary content, ASCII, digests), `scripts/ci/check_vocabulary.py`, `scripts/docs/gen_pack_reference.py --check`, `scripts/ci/check-pack-digests.sh`, docs freshness; charter service and drift test in CI
**Target Platform**: charter-service-composed Charter Packs consumed by Spec Kitty projects
**Project Type**: single (content repository)
**Performance Goals**: n/a (content)
**Constraints**: no new directive; no id renames; ASCII in software-dev mission files; no core references in consumer packs; at most one edge per unordered pair per pack; new edges carry `when` (or `reason` on `rejects`)
**Scale/Scope**: about 35 files across foundation, testing, planning-analysis, python, java, javascript, pack-authoring and internal, plus the release surface

**Structure Decision**: edit the packs in place; new artefacts follow each pack's layout (`paradigms/`, `assets/`, `tactics/<category>/`); foundation relationships go in its per-kind `*.graph.yaml` shards (hand-edited, as the previous mission did), other packs' in `drg/fragment.yaml`. A cross-pack edge is authored in the depending pack (testing authors `foundation::` sources; planning-analysis authors the `product-coherence-review` link; the refactoring pack authors the TDD-to-catalog links).

## Charter Check

- **DIRECTIVE_042 / 044 / 037 (docs)**: pack reference pages are generated (regenerated, never hand-edited); the changelog entry is authored. Pass.
- **DIRECTIVE_003 (decisions)**: rulings are decision moments; design calls are in research.md and the design-decisions tracer. Pass.
- **DIRECTIVE_018 (versioning)**: minor bumps, lockstep for the foundation set and built-in. Pass.
- **DIRECTIVE_041 (tests only where they guard real behaviour)**: no new repository test is planned; the existing gates (schema, edge identity, glossary content, digest, ASCII) cover the change. The new rules are content, evidenced by the gates (`[evidenced-by-run]` only for the release surface). Pass.
- **Identity discipline**: no pack_id minted or changed. Pass.
- **Alignment (AGENTS.md)**: charter pin only; no core gating. Pass.

## Project Structure

### Documentation (this mission)

```
kitty-specs/test-doctrine-2-01M7YH30/
├── spec.md, plan.md, research.md, data-model.md, quickstart.md
├── checklists/requirements.md
├── decisions/            # five resolved operator rulings
├── traces/               # approach, design-decisions, tooling-friction
└── tasks.md, tasks/      # from /spec-kitty.tasks
```

### Source Code (repository root)

```
packs/foundation/
├── paradigms/tests-as-scaffold-not-friction.paradigm.yaml        (new)
├── assets/exemplar-slicing-user-registration.md(+.asset.yaml)     (new)
├── assets/exemplar-unfake-an-over-mocked-test.md(+.asset.yaml)    (new)
├── anti_pattern.graph.yaml, asset.graph.yaml                      (new shards)
├── directives/041-..., directives/034-...                         (edit)
├── tactics/testing/{test-boundaries-by-responsibility,function-over-form-testing,tdd-red-green-refactor,acceptance-test-first}.tactic.yaml
├── procedures/{test-first-cycle,disciplined-refactoring-cycle}.procedure.yaml
├── glossaries/spec-kitty-core.glossary.yaml
├── missions/software-dev/steps/{plan,tasks}.guidelines.md (or prompts)
└── {paradigm,directive,procedure,tactic}.graph.yaml
packs/testing/
├── assets/{test-desiderata-checklist,quad-a-test-structure}.md(+.asset.yaml)  (new)
├── tactics/testing/shared-machine-test-measurement.tactic.yaml    (new)
├── styleguides/{test-desiderata-and-boundaries,testing-principles,quadruple-a-test-format}.styleguide.yaml
├── procedures/test-first-bug-fixing.procedure.yaml
└── drg/fragment.yaml
packs/planning-analysis/tactics/analysis/vertical-skeleton-first.tactic.yaml (new) + drg/fragment.yaml
packs/{python,java,javascript}/styleguides/*-conventions.styleguide.yaml + drg/fragment.yaml
packs/refactoring/drg/fragment.yaml
packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml
packs/internal/procedures/targeted-mission-test-run.procedure.yaml + drg/fragment.yaml
release: packs/*/pack.yaml, pack-manifest.yaml, packs/*.source.yaml, built-in digest, docs/packs/*.md, docs/changelog/CHANGELOG.md
```

## Complexity Tracking

No charter violation.

## Implementation Concern Map

### IC-01 — Mindset split and named smells

- **Purpose**: give the tests-as-scaffold mindset its own paradigm, keep DIRECTIVE_041 as the binding rule, and name the two mocking smells as graph nodes.
- **Relevant requirements**: FR-001, FR-002, FR-003
- **Affected surfaces**: foundation paradigm (new), 041, paradigm/directive/procedure/tactic shards, new `anti_pattern.graph.yaml`
- **Sequencing/depends-on**: none (operator: first)
- **Risks**: first `refines` edges in foundation shards; must not author an accidental tension; 041's rules must stay byte-identical.

### IC-02 — Reference assets, dedup and slicing content

- **Purpose**: move duplicated checklists and long worked examples into four assets, cut the restatements to pointers, add slicing heuristics, pin the curator layout, and clear the fold-in residue.
- **Relevant requirements**: FR-004 to FR-009, FR-016
- **Affected surfaces**: foundation and testing `assets/`, foundation `asset.graph.yaml`, testing/python/java/javascript styleguides and fragments, two foundation tactics, `doctrine-daphne`, DIRECTIVE_034 comment
- **Sequencing/depends-on**: IC-01 (the paradigm suggests assets; tactics reject the anti-patterns)
- **Risks**: styleguide principle descriptions cap at 255 characters; the desiderata styleguide's own patterns reference properties by name, so it must still read without the per-property list; foundation ships no assets today (first asset shard).

### IC-03 — Tracer bullets, green mode, spine

- **Purpose**: one coordinated vertical-slicing vocabulary at test and mission scale, with refactoring as a separate green-mode technique.
- **Relevant requirements**: FR-010 to FR-014
- **Affected surfaces**: `tdd-red-green-refactor`, `test-first-cycle`, `acceptance-test-first`, `disciplined-refactoring-cycle`, testing `test-first-bug-fixing`, planning-analysis tactic (new), plan/tasks guidance, `product-coherence-review` link, foundation glossary, refactoring fragment
- **Sequencing/depends-on**: IC-01 (operator order); shares foundation shards with IC-01 and IC-02
- **Risks**: software-dev files must stay ASCII; prose "red-green-refactor" in profiles stays (the tactic id is stable); green-mode wording must not contradict `DISCIPLINED_REFACTORING`.

### IC-04 — Measurement discipline

- **Purpose**: agents sharing a machine stop treating contended or killed runs as results.
- **Relevant requirements**: FR-015
- **Affected surfaces**: testing tactic (new) and fragment; internal `targeted-mission-test-run` pointer
- **Sequencing/depends-on**: none (parallel)
- **Risks**: overlap with QA_003 (no fake green) and `no-parallel-duplicate-test-runs`; reference, do not restate.

### IC-05 — Release surface

- **Purpose**: version, restamp and document the change.
- **Relevant requirements**: FR-017, NFR-001
- **Affected surfaces**: pack descriptors, manifests, digests, built-in digest constant, generated pack pages, changelog
- **Sequencing/depends-on**: IC-01 to IC-04
- **Risks**: Mission D overlaps in the foundation digest and version restamp; rebase and restamp after whichever merges first.
