# Mission Specification: Strict pack composition

**Mission Branch**: `feat/strict-pack-composition`
**Created**: 2026-11-04
**Status**: Draft
**Input**: Epic #118, grounded by the squad findings in [research.md](research.md); intent confirmed in Decision Moment `01M6M0WCAN8C95TEJCF5JS6NSC`.

## Purpose

The charter service refuses to compose the packs in this repository, because they predate its strict composition rules. This mission brings every pack in line and proves it with a real compose run by the service's own code. It ends the packs' compatibility with the as-is CLI on purpose; the tag `pre-charter-cutover` marks the last commit that was semi-compatible.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The service composes the real packs (Priority: P1)

An operator configures any pack from this repository together with `built-in`, and the charter service serves the composed offering.

**Why this priority**: This is the epic's outcome. Until it holds, no real pack can be served.

**Independent Test**: The charter repository's compose test reads this repository's real pack files at a pinned commit and composes each pack with `built-in`, and all of them together.

**Acceptance Scenarios**:

1. **Given** `built-in` and all four other packs are configured, **When** the offering is read, **Then** it succeeds and lists all five packs.
2. **Given** one of `internal`, `quality-assurance`, `event-driven` or `cave-kitty` is configured with `built-in`, **When** the offering is read, **Then** it succeeds and lists those two packs.
3. **Given** a migrated pack with one reference put back to its bare form, **When** the offering is read, **Then** it is refused `pack_reference_unqualified`, naming that pack.
4. **Given** a migrated pack with its `depends_on` removed, **When** the offering is read, **Then** it is refused with a `pack_reference_*` code.

---

### User Story 2 - An author learns about a bad reference here, not later (Priority: P2)

A pack author changes a reference and opens a pull request here. This repository's gate tells them when it no longer resolves, without waiting for the next charter pin bump.

**Why this priority**: The service is the authority, but it only sees this content at a pin bump. Without a local signal, regressions surface far from the change that caused them.

**Independent Test**: Run the pack gate over fixtures holding each defect, and over the real packs.

**Acceptance Scenarios**:

1. **Given** a correct qualified reference, **When** the gate runs, **Then** it passes.
2. **Given** a bare reference held only by another pack, a qualifier naming a pack outside the referrer's `depends_on`, a qualified target that pack does not hold, or a pack with no descriptor, **When** the gate runs, **Then** it fails and names the file and the reference.

---

### User Story 3 - The charter service pins the fixed packs (Priority: P3)

A charter maintainer moves the charter's open-packs pin to the merged result, and the charter's known-failure lists shrink to nothing for these packs.

**Why this priority**: It turns a one-off proof into a standing one in the charter's CI, and it is the epic's second done criterion.

**Independent Test**: The companion charter change is green with its pin on this repository's final `main` commit.

**Acceptance Scenarios**:

1. **Given** the charter pin moves to the merged commit, **When** charter CI runs, **Then** it is green with the six sidecar known-failures and the missing-descriptor diagnostics removed.

### Edge Cases

- `cave-kitty` holds no machine-checked reference to another pack, but still needs a descriptor: a pack with none is refused on its own. It also declares `depends_on`, because its prompts bind built-in profiles in prose.
- `built-in` references no other pack and gets no `depends_on`.
- Bare references that no pack holds (prose `procedures` entries, `action` targets) are not refused and stay as they are.
- A reference from a pack to its own artifact stays bare.
- `quality-assurance` is the pack's name and qualifier; its directory stays `packs/qa`.
- A partial landing in this repository regresses nothing for the charter, because the charter's pin insulates it. A pin bump onto a partial state would fail the charter's exact-match gate, so the charter bump comes last.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement | Status | Delivery | No-op passable? |
|----|-------------|--------|----------|-----------------|
| FR-001 | The pack gate validates against a charter contract that includes strict composition (at or after charter `88ed36e4`), pinned to a specific commit. | Approved | [build] | no |
| FR-002 | The pack gate accepts a correct qualified reference in both forms: `<pack>::<kind>:<id>` on graph edges and `<pack>::<id>` on typed references. | Approved | [build] | no |
| FR-003 | The pack gate fails on: a bare reference held only by another pack; a qualifier naming a pack outside the referrer's `depends_on` closure; a qualified target the named pack does not hold; a pack with no descriptor; duplicate pack ids or names. Each has a fixture that fails and a real-pack run that passes. | Approved | [build] | no |
| FR-004 | Every pack has a compliant `pack.yaml` with a unique, once-minted `pack_id`, a version and a name: `quality-assurance` (in `packs/qa`), `event-driven` and `cave-kitty`, each at version `1.0.0`. The valid example fixture has its own. (#47) | Approved | [build] | no |
| FR-005 | `quality-assurance`, `event-driven`, `cave-kitty` and `internal` declare `depends_on` on `built-in` at range `>=1.0,<2`. (#47, #113, #116, #117) | Approved | [build] | no |
| FR-006 | The remaining #47 items are delivered: the glossary stem rename and the guard against a pack without a descriptor (FR-003). (#47) | Approved | [build] | no |
| FR-007 | The six built-in asset sidecars name their payload relative to `assets/`, and the manifest, recorded digest and generated page are updated in the same change. (#75) | Approved | [build] | no |
| FR-008 | All 3 references from `quality-assurance` to `built-in` are qualified. (#117) | Approved | [build] | no |
| FR-009 | All 12 references from `event-driven` to `built-in` are qualified. (#116) | Approved | [build] | no |
| FR-010 | All 78 references from `internal` to `built-in`, across 31 targets, are qualified, including the 5 `agent_profile` edges. (#113) | Approved | [build] | no |
| FR-011 | The 24 references to `built-in` in `quality-assurance`'s agent profiles, which the service does not check today, are checked during the mission. They are either qualified, if that is corroborated as correct and in proportion, or logged in a follow-up issue with the reason. | Approved | [build] | no |
| FR-012 | The generated pack reference reads `depends_on` correctly and publishes it accurately, and no longer describes a `pack.yaml` field the schema forbids. | Approved | [build] | no |
| FR-013 | The charter's compose test reads the real packs from the pinned checkout and composes each pack with `built-in` and all five together, asserting the served pack list rather than only success, with the negative controls of User Story 1. (spec-kitty-charter#363) | Approved | [build] | no |
| FR-014 | The charter's pin, lockfile, corpus diagnostics, inspector test and known-failure list move to the final merged commit in one change, and the guide's typed-reference example is corrected. | Approved | [build] | no |
| FR-015 | Documentation states the new reality: the contract pin, `depends_on` usage, and the digest wording that still says "re-seed". The changelog records the break with the as-is CLI. | Approved | [build] | no |
| FR-016 | Issue text the research found stale (#47, #113, the epic's table, spec-kitty-charter#363 and #365) is corrected, #72's retired target is noted on that issue, and a core issue links `_anchor_for` with spec-kitty#7153. | Approved | [build] | no |

### Non-Functional Requirements

| ID | Requirement | Threshold | Status |
|----|-------------|-----------|--------|
| NFR-001 | The added composition checks do not noticeably slow the pack gate. | The gate's run over all packs grows by under 5 seconds on a developer machine. | Approved |
| NFR-002 | Local composition checks stay thin; the charter remains the authority. | Under 150 added production lines in the validator, with no reimplementation of ordering, level rules, version-range overlap or sibling logic. | Approved |
| NFR-003 | Every changed reference is classified before it is edited. | 100% of the 93 sites appear in the occurrence map, by category. | Approved |

### Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | No backwards compatibility with the as-is CLI. Its loss of `packs/internal` and `packs/qa` in this repository's own governance at merge is accepted by the operator. | Approved |
| C-002 | `pack_id` values are generated once by a tool, never typed by hand, and never reused from a scratch run. | Approved |
| C-003 | `CHARTER_COMMIT` is bumped deliberately to a specific commit, never floated to a branch. | Approved |
| C-004 | The contract bump and qualifier-aware parsing land before or with the first qualified reference. | Approved |
| C-005 | `internal` is migrated late. `dispatch` and `next` are tried against migrated content on a scratch copy early, and the run pauses if the mission's own runtime breaks. | Approved |
| C-006 | The charter's pin moves only after this mission's work is merged to `main`. | Approved |
| C-007 | #72, #73, #93, #114, #92 and #94 are out of scope. #92 and #94 belong to a separate runner; whichever lands second regenerates the digest. | Approved |
| C-008 | Semi-auto mode: the deliverable is a green pull request ready for review. The operator merges it. | Approved |

### Key Entities

- **Pack**: a directory of doctrine files, identified by its descriptor's `pack_id` and `name`.
- **Bare reference**: an artifact reference with no pack qualifier.
- **Qualified reference**: a reference that names the pack holding its target.
- **Composition**: the service's resolution of a set of configured packs into one offering, or a refusal.

## Domain Language

- `quality-assurance` is the pack name and qualifier. `qa` remains only its directory name.
- "Compose" means the service's own resolution. A local gate pass is not a compose.

## Success Criteria *(mandatory)*

- **SC-001**: All 5 configurations of User Story 1 (each pack with `built-in`, and all five) succeed in the charter's own test against the real files, with 0 refusals. — [build] · no-op passable: no
- **SC-002**: Reverting any one qualification or removing any one `depends_on` turns that test red, in 100% of the sampled negative controls. — [build] · no-op passable: no
- **SC-003**: All 93 cross-pack references are qualified, and an independent re-scan finds 0 bare references held only by another pack. — [build] · no-op passable: no
- **SC-004**: The charter's known-failure and diagnostics lists hold 0 entries for these packs. — [build] · no-op passable: no
- **SC-005**: Each defect class in FR-003 is caught by the local gate, and the real packs pass it with the temporary allowance for unmigrated packs removed. — [build] · no-op passable: no

## Assumptions

- Findings were measured at open-packs `f85cf23` and charter `85c20fa1`. Later commits to either are re-checked at plan time.
- The compose probe ran on scratch copies without the HTTP layer and with levels set by its harness. Surprises beyond `pack_reference_*` are possible with the real test, which is why the `quality-assurance` tracer runs early.
- A draft charter pull request pinned to this mission's branch head can prove the compose before merge.

## Dependencies

- spec-kitty-charter `main` holds the strict composition contract (#365, closed).
- spec-kitty-charter#363 is widened by the companion change.
- spec-kitty/spec-kitty#7153 tracks the core side. It is not a gate for this mission.
