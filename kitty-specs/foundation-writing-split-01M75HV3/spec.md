# Mission Specification: Split built-in into foundation and writing

**Mission Branch**: `feat/73-foundation-writing-split`
**Created**: 2026-11-11
**Status**: Draft
**Input**: Issue #73 (epic #190), re-scoped 2026-11-09 to "foundation/writing split, per-artifact operator rulings". Phase-1 research squad findings are in [research/](research/) (`0-phase1-report.md` is the summary; its membership numbers are superseded by the operator rulings below). Intent and membership confirmed by the operator in Decision Moments `01M75HVG46P3E4KJ4H8XF55C20` … `01M75HWN8RDAAN4WEBD8RRKG27`.

## Purpose

`built-in` ships everything today: 398 doctrine graph nodes, from base profiles to Drupal conventions. Charter ADR-0048 d12 makes `built-in` a *distribution pack* that holds no artifacts of its own and aggregates its members, and ADR-0053 d3/d9 name those members `foundation` and `writing`. The operator ruled `foundation` down to its bare basis: the fallback profile, an implementer, a reviewer, an analyst and the base mission types, plus the cross-cutting directives and the tactics those artifacts name directly. Documentation work goes to `writing`. Everything that is neither is parked in a temporary opt-in pack, `specialist-staging`, which later pull requests carve into specialist bundles one at a time (architecture, refactoring, stacks, …).

Downstream stack packs depend on `foundation`: `java` (#5), `rust`/`go` (PR B) and, through them, the private COBOL packs.

## Domain Language

| Term | Meaning | Avoid |
|---|---|---|
| distribution pack | A pack that holds no artifacts and only aggregates member packs through `depends_on` (ADR-0048 d12). `built-in` is one. | "meta pack", "umbrella" |
| member pack | A pack a distribution pack aggregates: `foundation`, `writing`. | "sub-pack", "child pack" (they are roots, `parent_pack: null`) |
| staging pack | `specialist-staging`: a temporary opt-in org pack that holds artifacts awaiting a specialist bundle. Not a member of `built-in`. | "misc", "leftovers" |
| seed | One of the artifacts the operator named as foundation's basis. | — |
| relocated edge | A graph edge whose source sits in a lower pack but is declared in the graph of the pack that holds its target, with a qualified source (`foundation::<urn>`). | "back-reference" |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A deployer composes the default distribution (Priority: P1)

A charter-service deployer places `built-in`, `foundation` and `writing` and asks for the composed offering. They get the four base profiles, the comms/docs profiles and all four shipped mission types, and the `default` and `minimal` presets still activate.

**Why this priority**: This is the issue's outcome. A broken default distribution blocks every consumer.

**Independent Test**: `scripts/ci/charter_service_check.py` composes and registers each pack, including the three built-in-level packs together, against the charter at the lock pin.

**Acceptance Scenarios**:

1. **Given** `built-in`, `foundation` and `writing`, **When** the offering is composed, **Then** it succeeds; `built-in` contributes no artifacts, and `generic-agent` resolves as the fallback profile.
2. **Given** `built-in` alone, **When** the offering is composed, **Then** it is refused with a dependency error naming `foundation`. This is the documented breaking change.
3. **Given** `foundation` alone, **When** it is composed, **Then** it succeeds: foundation depends on nothing.

---

### User Story 2 - A stack-pack author builds on foundation (Priority: P1)

The author of `java`, `rust` or `go` declares `depends_on: foundation` at `pack_level: org` and writes `foundation::agent_profile:implementer-ivan` or `foundation::directive:DIRECTIVE_034`. The references resolve.

**Why this priority**: Three downstream pull requests are blocked on foundation's pack_id and membership.

**Independent Test**: an org pack in this repository that depends on `foundation` and references foundation artifacts passes the gates and the service check.

**Acceptance Scenarios**:

1. **Given** an org pack depending on `foundation`, **When** it references a foundation artifact with `foundation::`, **Then** composition succeeds.
2. **Given** the same pack referencing `foundation::agent_profile:architect-alphonso` (now in staging), **When** composed, **Then** it is refused because the artifact is missing from foundation.

---

### User Story 3 - Existing org packs keep working (Priority: P2)

`internal`, `quality-assurance`, `event-driven`, `cave-kitty` and `spdd` keep composing after the split. Every `built-in::` reference is rewritten to the pack that now holds the artifact, and each pack's `depends_on` names those packs directly.

**Why this priority**: These packs are in this repository's gate; leaving them broken fails CI.

**Independent Test**: the service check composes each org pack.

**Acceptance Scenarios**:

1. **Given** the split, **When** the repository is searched for `built-in::`, **Then** there are no matches in pack content.
2. **Given** each org pack, **When** composed with its declared dependencies, **Then** it succeeds.

---

### User Story 4 - A pack author learns about manifest drift locally (Priority: P3)

An author adds a doctrine file to a pack that has a `pack-manifest.yaml` but forgets to list it. The pack gate fails and names the file (#182).

**Why this priority**: Two files (`git-flow`, `execution-lanes`) already drifted unnoticed; the split moves hundreds of files and needs this guard.

**Independent Test**: unit tests over fixture packs with a missing and an extra manifest entry.

**Acceptance Scenarios**:

1. **Given** a file-backed doctrine artifact missing from its pack's manifest, **When** the gate runs, **Then** it fails and names the file.
2. **Given** a manifest entry with no file, **When** the gate runs, **Then** it fails and names the entry.
3. **Given** a pack without a manifest, **When** the gate runs, **Then** the guard does not apply.

### Edge Cases

- **foundation → writing or staging edges**: a reference in foundation to a writing or staging artifact would be a cycle or a level violation. Such edges move into the target pack's graph with a `foundation::` source, and are removed from the artifact's own body where the body lists them (e.g. `analyst-annie` → DIRECTIVE_047).
- **writing → staging edges**: writing is built-in level, so it cannot reach an org pack. These edges also move into staging with a `writing::` source.
- **Same id in two sibling packs**: refused as `pack_sibling_conflict`. The partition must be exact.
- **Presets**: `default` activates all four mission types and `minimal` names foundation directives and tactics. Both stay on `built-in` and must resolve through its closure.
- **`missions/` folder name**: the rename to `mission_types/` (ADR-0048 d16) is refused at the charter pin (`file-kinds.yaml` marks it retired), so mission folders move unchanged.
- **Graph-only template nodes with no file** (16 found in research): they move with their referrers. Fixing them is out of scope.
- **The 4 java artifacts**: they land in staging; PR A (#5) takes them from there.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement | Status | Delivery | No-op passable? |
|---|---|---|---|---|
| FR-001 | A new pack `foundation` exists at `packs/foundation/`: `pack_id 01M75HSYR9S9KPA372PHGT0EX3`, `pack_level: built-in`, `parent_pack: null`, no `depends_on`, version 1.0.0. It holds exactly the artifacts listed under `foundation` in [membership.json](membership.json). | Approved | build | no |
| FR-002 | A new pack `writing` exists at `packs/writing/`: `pack_id 01M75HSYS69RYRFPB4WCC5AC9D`, `pack_level: built-in`, root, `depends_on foundation ==1.0.0`, version 1.0.0. It holds exactly the `writing` list, including the whole documentation mission type bundle. | Approved | build | no |
| FR-003 | A new pack `specialist-staging` exists at `packs/specialist-staging/`: `pack_id 01M75HSYSZ96965JHV2GKWCSEA`, `pack_level: org`, root, depending on `foundation` and `writing`, version 1.0.0. It holds exactly the `staging` list, and its pack.md states it is temporary and carved out per bundle. | Approved | build | no |
| FR-004 | The `qa` pack receives the 6 artifacts and the `internal` pack the 4 artifacts listed for them in membership.json. | Approved | build | no |
| FR-005 | `built-in` keeps pack_id `01ARWG13C000000000000000FG` and `pack_level: built-in`, holds no doctrine artifacts, depends on `foundation ==1.0.0` and `writing ==1.0.0`, keeps the `default` and `minimal` presets and `fallback_profile: generic-agent`, and is version 2.0.0. | Approved | build | no |
| FR-006 | Artifacts move with `git mv`, so history follows each file; artifact ids do not change. | Approved | build | no |
| FR-007 | The display name of `generic-agent` becomes "Generic Giannis"; its id does not change. | Approved | build | no |
| FR-008 | Each pack's DRG fragment holds the nodes it owns and the edges whose source it owns. Every edge from a lower pack (foundation < writing < built-in-level < org) to an artifact in a higher pack is re-declared in the higher pack's graph with a qualified source, and removed from the lower pack. | Approved | build | no |
| FR-009 | No artifact body or graph in foundation or writing references an artifact outside its own `depends_on` closure. No reference anywhere names `built-in::`. | Approved | build | no |
| FR-010 | Every org pack (`internal`, `qa`, `event-driven`, `cave-kitty`, `spdd`) has its `built-in::` references rewritten to `foundation::`, `writing::` or `specialist-staging::`. Its `depends_on` names those packs directly. Its own `pack_version` is bumped. | Approved | build | no |
| FR-011 | `charter_service_check.py` composes and registers every built-in-level pack (`built-in`, `foundation`, `writing`) and every org pack, `specialist-staging` included. | Approved | build | no |
| FR-012 | `pack-manifest.yaml` lists exactly its pack's constituents for `built-in`, `foundation` and `writing`. The built-in digest (`built-in.source.yaml`, `check-built-in.sh`) is re-recorded for the new layout. | Approved | build | no |
| FR-013 | The pack gate fails when a file-backed doctrine artifact is missing from, or extra in, a pack's `pack-manifest.yaml` (#182), with unit tests. | Approved | build | no |
| FR-014 | Docs record the split: an ADR, a 💥 Breaking CHANGELOG entry with a migration note, a README per new pack, `packs/README.md`, the catalog and pack index, and generated pack reference pages for the three new packs. | Approved | build | no |
| FR-015 | Moved content that carries upstream attribution keeps a PROVENANCE note in its new pack. | Approved | build | no |

### Non-Functional Requirements

| ID | Requirement | Threshold | Status |
|---|---|---|---|
| NFR-001 | Membership fidelity | 100% of the nodes in membership.json sit in their assigned pack; 0 nodes in two packs; 0 nodes left in built-in | Approved |
| NFR-002 | Reference integrity | 0 dangling or out-of-closure references reported by the pack gate and the charter service check | Approved |
| NFR-003 | Gate health | All repository gates green on the final head (validate-packs, check-built-in, charter service check, vocabulary, pack-reference --check, unittest suites; docs-site build in CI) | Approved |
| NFR-004 | History preservation | ≥ 95% of moved files detected as renames by `git log --follow` | Approved |

### Constraints

| ID | Constraint | Status |
|---|---|---|
| C-001 | The repository aligns to the charter at the `charter.lock.yaml` pin; spec-kitty core compatibility is not a constraint (AGENTS.md). | Approved |
| C-002 | Pack ids are tool-minted ULIDs, never hand-typed, and never edited after minting. | Approved |
| C-003 | `missions/` keeps its folder name (`mission_types/` is retired at the pin). | Approved |
| C-004 | No new specialist bundle (architecture, refactoring, python, …) is created in this mission. The decision to have `built-in` aggregate `java` is left open for the operator (needs a charter ADR amendment). | Approved |
| C-005 | Artifact content is not rewritten beyond reference qualification, edge relocation and the Generic Giannis display name. | Approved |
| C-006 | `pack-manifest.yaml` is never hand-edited for hashes; only the member list is changed, and the tool restamps it. | Approved |

## Success Criteria

- SC-001: A deployer can compose the default distribution from three packs with zero refusals. — [build] · no-op passable: no
- SC-002: A downstream stack pack can depend on foundation alone and resolve all four base profiles and the base mission types. — [build] · no-op passable: no
- SC-003: Zero pack-content occurrences of `built-in::` remain. — [build] · no-op passable: no
- SC-004: Foundation holds 115 nodes, writing 57, staging 217, and built-in 0, matching the approved list. — [build] · no-op passable: no

## Assumptions

- `specialist-staging` is opt-in. Without it, `plan` and `software-dev` lose the guidance carried by relocated edges (C4/DDD paradigms, procedures, architect handoffs). The operator accepted this.
- Open PR #193 edits built-in paradigm files. Whichever lands second rebases.
- The docs-site build cannot run in this container (npm 401 on a private package); CI is the authority for it.

## Out of Scope

- Carving `specialist-staging` into bundles (one follow-up issue per bundle).
- Core spec-kitty fetch/pin changes (#73 item 3, closed out).
- Renaming `missions/` to `mission_types/`.
- Deciding whether `built-in` aggregates `java`.
