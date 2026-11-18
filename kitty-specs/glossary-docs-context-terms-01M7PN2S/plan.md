# Implementation Plan: Glossary: docs/context terms and the Op term

**Branch**: `issue-221-234-glossary-content` | **Date**: 2026-11-18 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/glossary-docs-context-terms-01M7PN2S/spec.md`

## Summary

Content-only mission. A one-off extraction script (kept in the mission's `tools/`, not shipped) reads the term tables of core's `docs/context/*.md` at `01e577d` and writes a classification ledger (`research/ledger.yaml`). Each row carries a verdict (`foundation`, `internal`, `exists`, `alias`, `excluded`), a target id and a reason; editorial overrides (rewritten definitions, verdict changes) live in the ledger, not in the script. A second step renders the `foundation` and `internal` rows into the two glossary contexts. The Op term, the four mission types and the header fix are authored by hand. Versions, manifests, digests, pages and the changelog follow, then a unit test pins the result.

## Technical Context

**Language/Version**: YAML content; Python 3.11 for the mission tools and the unit test
**Primary Dependencies**: pyyaml (already required by CI)
**Storage**: files under `packs/`
**Testing**: `python3 -m unittest discover -s tests/ci`; `scripts/ci/validate-packs.sh`; `scripts/ci/check-pack-digests.sh`; `python3 scripts/ci/check_vocabulary.py`; `python3 scripts/docs/gen_pack_reference.py --check`; the charter service and drift jobs in CI
**Target Platform**: the charter service at the lock pin `050d780`
**Project Type**: single repository of packs
**Performance Goals**: n/a
**Constraints**: glossary schema at the pin (closed; term fields `id`, `name`, `definition`, `status`, `aliases`, `avoid`, `examples`, `see_also`)
**Scale/Scope**: about 290 source terms; about 170 added to foundation and 70 to internal (measured in the ledger)

## Charter Check

- DIRECTIVE_018 (versioning): additive change → minor bumps; exact pins follow (spec decision 4). Pass.
- DIRECTIVE_053 (Op or Mission): this work runs as a Mission inside a dispatch Op; the Op term is authored consistent with it. Pass.
- Living documentation (DIRECTIVE_037): the changelog and the generated pack pages move with the content. Pass.
- Charter alignment (AGENTS.md): validation is against the charter contract at the pin, not core. Pass.

## Project Structure

### Documentation (this mission)

```
kitty-specs/glossary-docs-context-terms-01M7PN2S/
├── spec.md
├── plan.md
├── research.md              # classification policy and source pin
├── research/ledger.yaml     # one row per source term (FR-002)
├── tools/                   # extraction and render scripts (not shipped)
└── tasks.md, tasks/
```

### Source Code (repository root)

```
packs/foundation/glossaries/spec-kitty-core.glossary.yaml     # consumer terms, Op, header
packs/internal/glossaries/spk-internal-glossary.glossary.yaml # house terms
packs/*/pack.yaml                                             # versions and exact pins
packs/*/pack-manifest.yaml, packs/*.source.yaml               # derived, restamped
docs/packs/*.md                                               # regenerated pages
docs/changelog/CHANGELOG.md
tests/ci/test_glossary_content.py                             # new
```

**Structure Decision**: no new context and no new pack; the two existing contexts grow.

## Classification policy (research.md holds the detail)

- `foundation`: a concept a project meets in its own Missions, charter, packs, CLI output or event logs.
- `internal`: core's code symbols, repository layout, test taxonomy, tracker labels, product lines, retired hosted vocabulary, the tool-vs-agent naming record, docs audience personas.
- `exists`: same id, name or alias already in the target context; kept unchanged (alias added if missing).
- `alias`: a source heading that is an alias row; folded into its canonical term.
- `excluded`: generic technology terms, terms that name something that does not exist (a proposal, a non-directory), duplicates of a cross-reference, and terms retiring with core's seed file.
- Status map: canonical → `active`, candidate → `draft`, deprecated → `deprecated`.
- Definitions for foundation are cleaned of Markdown links, code-path parentheticals, ADR and core issue citations; where cleaning leaves a definition that still leans on core internals, the ledger carries a rewritten definition.
- `see_also` only to terms of the same context.

## Implementation Concern Map

### IC-01 — Ledger and rendering tools

- **Purpose**: one reproducible classification of every source term with reasons.
- **Relevant requirements**: FR-002, FR-005, NFR-002
- **Affected surfaces**: mission `tools/`, `research/ledger.yaml`, `research.md`
- **Sequencing/depends-on**: none
- **Risks**: Markdown table parsing (escaped pipes, multi-paragraph cells); verify counts against a heading count.

### IC-02 — Foundation context content

- **Purpose**: consumer terms, Op, mission types, authoring-source header.
- **Relevant requirements**: FR-001, FR-003, FR-005, FR-006, FR-007, NFR-003
- **Affected surfaces**: `packs/foundation/glossaries/spec-kitty-core.glossary.yaml`
- **Sequencing/depends-on**: IC-01
- **Risks**: the vocabulary guard refuses retired names (`org-charter.yaml`, `spec-kitty merge`, retired doctrine ids) — definitions carrying them must be rewritten; #233 edits the same file.

### IC-03 — Internal context content

- **Purpose**: house terms.
- **Relevant requirements**: FR-004, NFR-003
- **Affected surfaces**: `packs/internal/glossaries/spk-internal-glossary.glossary.yaml`
- **Sequencing/depends-on**: IC-01
- **Risks**: the vocabulary guard scans internal too.

### IC-04 — Versions, derived outputs, changelog, test

- **Purpose**: release hygiene and a pinning test.
- **Relevant requirements**: FR-008, FR-009, FR-010, FR-011, NFR-001
- **Affected surfaces**: `packs/*/pack.yaml`, manifests, sidecars, `docs/packs/`, changelog, `tests/ci/test_glossary_content.py`
- **Sequencing/depends-on**: IC-02, IC-03
- **Risks**: every concurrent slice collides on the changelog and digests; restamp on each rebase.

### IC-05 — Operator wording (#139, folded in)

- **Purpose**: retire "HiC", "Human-in-Charge" and "human-in-command" as role wording in pack prose in favour of "the operator"; the `human-in-charge` profile id stays.
- **Relevant requirements**: FR-012, SC-005
- **Affected surfaces**: the files listed in #139's 2026-11-18 comment (foundation tactics, procedure and software-dev charter prompt; architecture procedure and C4 tactic; writing styleguide, its README, contextive toolguide, tactic graph `when` texts and glossary-maintenance procedure; planning-analysis retrospective-facilitator), the internal procedures that say "HiC", and both glossary contexts (handled with IC-02 and IC-03)
- **Sequencing/depends-on**: IC-02, IC-03
- **Risks**: the retrospective-facilitator mode id `hic` becomes `operator`; nothing in the packs references the mode id (core's runtime may; core compatibility is not this repository's concern, AGENTS.md).

## Complexity Tracking

None.
