# Mission Specification: Glossary: docs/context terms and the Op term

**Mission Branch**: `issue-221-234-glossary-content`
**Created**: 2026-11-18
**Status**: Draft
**Input**: Issues #139 (narrowed 2026-11-18: retire the HiC / human-in-command role wording; folded in by the orchestrator), #221 ("author the docs/context bounded-context terminology as glossary-context content: consumer half in foundation, house half in internal") and #234 ("add the Op term and make the core glossary yaml the authoring source"), epic #288, dispatched by the orchestrator with operator-approved scope.

## Intent Summary (confirmed by the dispatch brief and the issues)

- **Primary actor**: a project that activates the `foundation` pack's glossary context (`spec-kitty-core`) and reads its terms while writing or reviewing its own Missions, charter and packs. Secondary actor: a Spec Kitty maintainer who reads the internal context (`spk-internal-glossary`).
- **Trigger**: core's `docs/context/` pages define about 290 terms in bounded-context tables; the shipped glossary context holds 138, the central term of DIRECTIVE_053 ("Op") has no entry, and the context still describes itself as migrated from a retired seed file.
- **Outcome**: every consumer-facing canonical concept from `docs/context/` is a term of `spec-kitty-core`; every house concept (core's own code, repository, tests, tracker labels, product lines, retired hosted vocabulary) is a term of `spk-internal-glossary`; "Op" is defined consistently with DIRECTIVE_053; the pack yaml is stated to be the authoring source.
- **Invariant**: no consumer-facing definition cites core's source tree (`src/`, `tests/`), core issue numbers or core ADRs, and every source term is accounted for exactly once in a classification ledger (added, already present, internal, or excluded with a reason).

The four editorial calls were recorded as Decision Moments and resolved from the brief and #221 (see Decisions); no question was left open.

## Domain Language

| Term | Meaning | Avoid |
|------|---------|-------|
| glossary context | One `glossaries/<id>.glossary.yaml` file: a bounded context with its terms (charter ADR-0049). `spec-kitty-core` in foundation, `spk-internal-glossary` in internal. | "glossary pack" (retired kind) |
| consumer term | A concept a project activating foundation needs to understand its own Missions, charter, packs or CLI output. | "public term" |
| house term | A concept about how the Spec Kitty team builds core: its code, repository layout, tests, tracker and product lines. | "private term" |
| source term | One term table under a `###` heading in core's `docs/context/*.md` (at core `01e577d`), or a canonical vocabulary row on a page without tables. | |
| classification ledger | The mission's record of every source term's verdict and reason. | |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A consumer looks up the Op term (Priority: P1)

A project activates DIRECTIVE_053 (choose Op or Mission) and meets the word "Op". Today no glossary defines it.

**Why this priority**: the central term of a shipped directive is undefined (#234).

**Independent Test**: `term:spec-kitty-core/op` exists, is active, carries "profile invocation" as an alias and sees `mission`, and its definition matches DIRECTIVE_053's (opened by `spec-kitty dispatch`, closed by `spec-kitty profile-invocation complete`, no spec, plan, work package or worktree).

**Acceptance Scenarios**:

1. **Given** the foundation context, **When** a reader looks up `op`, **Then** it is defined, aliased `profile invocation`, and links to `mission`.
2. **Given** DIRECTIVE_053's text, **When** compared with the Op definition, **Then** neither contradicts the other on how an Op opens, closes or what it does not create.

### User Story 2 - A consumer finds the docs/context concepts in the glossary (Priority: P1)

A project reads a Mission's `meta.json` (topology, target branch), consolidate output (gap report) or a charter (activation ledger, required floor) and looks the word up in its active glossary.

**Why this priority**: #221's core ask; the consumer gets the flat terms but not the bounded-context content.

**Independent Test**: for every ledger row with verdict `foundation`, a term with that id exists in `spec-kitty-core` with a definition free of core source paths.

**Acceptance Scenarios**:

1. **Given** the ledger, **When** each `foundation` row is checked, **Then** its term exists in `spec-kitty-core`.
2. **Given** the foundation context, **When** scanned for `src/`, `tests/`, core issue (`#NNNN`) and ADR citations, **Then** none are found in the added terms.

### User Story 3 - A maintainer finds the house terms in the internal context (Priority: P2)

A maintainer meets "Cat-7 grandfathered orphan" or the `priority:P2` label scheme and looks it up.

**Independent Test**: for every ledger row with verdict `internal`, the term exists in `spk-internal-glossary`.

**Acceptance Scenarios**:

1. **Given** the ledger, **When** each `internal` row is checked, **Then** its term exists in `spk-internal-glossary` and not in `spec-kitty-core`.

### User Story 4 - The authoring source is stated truthfully (Priority: P2)

A contributor opens `spec-kitty-core.glossary.yaml` and reads that it is the authoring source, edited by hand through the glossary-curation workflow, not a migration output.

**Independent Test**: the context's `description` and file header no longer say "migrated from spec_kitty_core.yaml"; they name the file as the source and point at the curation workflow.

### Edge Cases

- A source term already present in a context (same id, name or alias): verdict `exists`; the existing entry is kept, and a missing alias may be added.
- A source heading that is an alias of another term ("WorkPackage (Alias)", "Tracker Connector Boundary (Alias)"): folded into the canonical term's `aliases`.
- A source term with status `deprecated` ("Feature", "feature branch", `in_tension_with`): carried with status `deprecated`, pointing at its successor.
- A source term defined as "not a code type" or "intended, not implemented": status `draft`.
- A `see_also` target that is not in the same context: dropped rather than written as a broken or cross-pack reference.
- Two source terms whose names slug to the same id: the second gets a qualified id; ids stay unique within a context.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Op term | As a consumer, I want an active `op` term aliased "profile invocation", seeing `mission`, consistent with DIRECTIVE_053, so that the directive's central term is defined. | High | Open | [build] | no — the term is absent today; the check asserts id, alias and see_also |
| FR-002 | Classification ledger | As a reviewer, I want every source term recorded once with a verdict (`foundation`, `internal`, `exists`, `alias`, `folded` (same concept as another source row), `excluded`) and a page- or row-specific reason, so that nothing is silently dropped. | High | Open | [build] | no — the ledger row count must equal the source term count |
| FR-003 | Consumer terms in foundation | As a consumer, I want every `foundation` ledger row present in `spec-kitty-core` with a consumer-safe definition, mapped status (canonical→active, candidate→draft, deprecated→deprecated) and same-context `see_also`. | High | Open | [build] | no — each row is checked for presence |
| FR-004 | House terms in internal | As a maintainer, I want every `internal` ledger row present in `spk-internal-glossary`. | High | Open | [build] | no — each row is checked for presence |
| FR-005 | Consumer-safe wording | As a consumer, I want every foundation definition, added or pre-existing, free of core source paths (`src/`, `tests/`), core issue numbers, core ADR citations and core `docs/context` page references. | High | Open | [build] | no — a scan of the added terms returns zero hits while the raw source text has hits |
| FR-006 | Mission types | As a consumer, I want the four shipped mission types (`software-dev`, `research`, `documentation`, `plan`) defined as terms, from `docs/context/mission-types.md`. | Medium | Open | [build] | no — four ids asserted |
| FR-007 | Authoring source stated | As a contributor, I want the `spec-kitty-core` description and header to state that the file is the authoring source, curated through the glossary-curation workflow, replacing "migrated from spec_kitty_core.yaml". | Medium | Open | [build] | no — grep for "migrated from" in the context returns nothing |
| FR-008 | Versions follow DIRECTIVE_018 | As a pinner, I want foundation and internal minor-bumped and every exact pin on foundation moved with its pack minor-bumped. | High | Open | [build] | no — the validator and charter service refuse a stale exact pin |
| FR-009 | Derived outputs current | As CI, I want manifests derived, digests restamped and pack pages regenerated after the content change. | High | Open | [build] | no — the digest and pages gates fail on stale output |
| FR-010 | Changelog | As a reader, I want an `[Unreleased]` entry naming the added terms, the Op term, the header fix and the version bumps. | Medium | Open | [build] | no — entry names #221 and #234 |
| FR-012 | Operator wording (#139) | As a consumer, I want pack prose and both glossary contexts to name the accountable human "the operator", so that the retired "HiC", "Human-in-Charge" and "human-in-command" role wording disappears: `grep -rniE "\bHiC\b|human-in-command" packs` finds nothing, "human-in-charge" appears only as the agent profile id, the kitty-glossary-writing rule that requires "HiC" is retired, and the retrospective-facilitator `hic` mode becomes `operator`. | High | Open | [build] | no — the grep finds 40+ hits on today's main |
| FR-011 | Unit test | As a maintainer, I want a unit test that pins the Op term (id, status, alias, see_also) and the absence of core source paths in the foundation context. | Medium | Open | [build] | no — the test fails on today's main |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Validity | `validate-packs.sh` (with `--cross-pack`), the digest gate, the pages gate, the vocabulary guard, the unit tests and the charter service and drift jobs report 0 errors. | Reliability | High | Open |
| NFR-002 | Coverage | 100% of source terms appear in the ledger; 0 ledger rows lack a reason. | Completeness | High | Open |
| NFR-003 | Uniqueness | 0 duplicate term ids and 0 duplicate names within each context. | Integrity | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | One consumer context | Consumer terms extend `spec-kitty-core`; no new glossary context is added. | Technical | High | Open |
| C-002 | Existing terms kept | Existing term ids are not changed. An existing definition changes only to remove core citations (FR-005) or retired role wording (FR-012); a missing alias may be added. The one existing-shape change is the `human-in-charge` glossary term added by this mission, renamed `operator` (FR-012). | Technical | High | Open |
| C-003 | Core half out of scope | Retiring core's `.kittify/glossaries` seed, core's `docs/context/` fate and the Contextive generator stay in core (#3024, #5269). | Business | High | Open |
| C-004 | Charter alignment | The schema is the charter's at the lock pin; core loading compatibility does not block this work (AGENTS.md). | Technical | High | Open |
| C-005 | Generated files by tool | Manifests, digests and `docs/packs/` pages change only through their generators. | Technical | Medium | Open |
| C-006 | Coordinate with #233 | #233 adds an enforcement-level term to foundation; whichever lands second rebases and restamps versions, digests and the changelog. | Business | Medium | Open |

### Key Entities

- **Glossary context**: `id`, `name`, `description`, `terms[]`.
- **Term**: `id` (slug), `name`, `definition`, `status` (`draft`/`active`/`deprecated`), optional `aliases`, `avoid`, `see_also` (`term:<context>/<id>`).
- **Ledger row**: source page, source heading, source status, verdict, target id, reason.

## Decisions (recorded Decision Moments, resolved)

1. **One context** (`01M7PN8BRB951MCEC2M5DXPFHP`): consumer terms extend `spec-kitty-core`; the brief names the foundation context, and one context needs no cross-context uniqueness story.
2. **Core code-level terms go to internal** (`01M7PN8EBAANW2PYHMVW7FXGZN`): #221's binding constraint sends core code, repository layout and team practice to the internal pack, which is not shipped.
3. **Generic technology terms** (`01M7PN8GR51G0YAS30CRRJ0NWP`, reversed on 2026-11-18): first excluded; now added to foundation as drafts, because the writing pack's glossary styleguide and the curation-interview tactic require foundational terms such as API, CLI, YAML and JSON to be defined.
4. **Versioning** (`01M7PN8K3TZZP603TE4CHA41ZA`, superseded by the operator's ruling of 2026-11-18): one shared bump for #300, #302 and #303. This mission lands last, inside foundation and writing 2.1.0, the core bundles 2.2.0 and built-in 4.1.0 (#302) and internal 4.0.1 (#303), with no bump of its own.

## Decisions added on review (WP01, 2026-11-18)

5. Status deviations from the FR-003 map are deliberate and recorded in `research/rewrites.yaml`: `vocabulary`, `delegates_to` and `refines` are canonical in core but emitted by no shipped artifact (core says "intended-but-dormant"), so `draft`; `agent-profile` is candidate in core but is a shipped artifact kind of every pack, so `active`; `op` is `active` per FR-001.
6. #139 is folded in (orchestrator, 2026-11-18): the glossary term for the accountable human is `operator`; "human in charge" and "human in command" are its `avoid` forms.

## Assumptions

- Source is core `docs/context/` at `01e577d` (core `main`, 2026-11-18).
- `see_also` stays within one context; cross-pack qualified references are not introduced.
- Core's "Do NOT use when" and "Note" rows are guidance prose, not taboo forms; they are not mapped to `avoid`.

## Issue Matrix

| Issue | Verdict | Note |
|-------|---------|------|
| #221 | in scope | Anchor: consumer and house halves. |
| #234 | in scope | Op term and authoring-source header. |
| #288 | parent | Epic. |
| #233 | related, not in scope | Coordination only (C-006). |
| #139 | in scope | Operator wording (FR-012), folded in by the orchestrator on 2026-11-18. |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader finds "Op" in the active foundation glossary, with its alias and link to Mission — [build] · no-op passable: no
- **SC-002**: Every source term has exactly one recorded verdict, and every `foundation` and `internal` verdict is backed by a term in the named context — [build] · no-op passable: no
- **SC-003**: Zero added consumer definitions cite core source paths, issue numbers or ADRs — [build] · no-op passable: no
- **SC-004**: Every required gate passes on the pull request head — [build] · no-op passable: no
- **SC-005**: No pack prose names the operator "HiC" or "human-in-command" — [build] · no-op passable: no
