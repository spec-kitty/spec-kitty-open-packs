# Mission Specification: Split built-in into foundation, writing and opt-in bundles

**Mission Branch**: `feat/73-foundation-writing-split`
**Created**: 2026-11-11 (re-specified the same day after the bundle research squad)
**Status**: Draft
**Input**: Issue #73 (epic #190), re-scoped 2026-11-09 to "foundation/writing split, per-artifact operator rulings".
- Phase-1 squad reports: [research/](research/).
- Bundle squad reports: [research/bundle-squad/](research/bundle-squad/). `E-synthesis.md` is the summary.
- Approved per-node map: [membership.json](membership.json).
- Operator rulings: Decision Moments `01M75HVG46P3E4KJ4H8XF55C20` … `01M75HWN8RDAAN4WEBD8RRKG27`, refined by `01M75PEBPTKXHKAFXT4P6FY977` … `01M75PF7Q7V98Z2PGV7NRT8QM5`. Where they conflict, the later ones win.

## Purpose

Today `built-in` ships everything: 398 doctrine graph nodes, from base profiles to Drupal conventions.
- Charter ADR-0048 d12 makes `built-in` a *distribution pack* that holds no artifacts and aggregates its members. ADR-0053 d3/d9 name those members `foundation` and `writing`.
- ADR-0048 d14 makes stack and topical packs opt-in at `pack_level: org`.

The operator ruled `foundation` down to the basis and its own how-to layer:
- **Profiles**: the fallback profile ("Generic Giannis"), an implementer, a reviewer, an analyst and the human-in-charge.
- **Missions**: the software-dev, plan and research mission types.
- **Doctrine**: every cross-cutting directive, with the procedures, tactics and toolguides those directives and the mission steps name.

Documentation and glossary work go to `writing`. Everything else is carved now into ten opt-in org bundles: testing, refactoring, architecture, planning-analysis, adversarial-review, pack-authoring, python, javascript, drupal and java. Each depends on foundation and, where needed, on other bundles, with no cycles. A research squad of four lenses (graph clustering, curation, adversarial review, consumer journeys) grounded this map.

Downstream: `rust`/`go` (PR B) depend on `foundation` and `testing`. The private COBOL packs build on those. `java` (#5) is carved here.

## Domain Language

| Term | Meaning | Avoid |
|---|---|---|
| distribution pack | A pack that holds no artifacts and aggregates member packs through `depends_on` (ADR-0048 d12). `built-in` is one. | "meta pack", "umbrella" |
| member pack | A pack the distribution pack aggregates: `foundation`, `writing`. Both are roots (`parent_pack: null`). | "sub-pack", "child pack" |
| bundle | An opt-in org-level pack carved from built-in content (ADR-0048 d14), e.g. `testing`, `java`. | "plugin", "extension" |
| how-to layer | The procedures, tactics and toolguides that foundation's directives `require` and its mission steps name. | — |
| relocated edge | A graph edge declared in the graph of the pack holding its target, with a qualified source (`foundation::<urn>`), because the source's pack cannot see the target's pack. | "back-reference" |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A deployer composes the default distribution (Priority: P1)

A charter-service deployer places `built-in`, `foundation` and `writing` and composes the offering. They get:
- the five foundation profiles and the seven comms/docs profiles;
- all four shipped mission types, with their step hooks intact;
- the `default` and `minimal` presets.

**Why this priority**: A broken default distribution blocks every consumer.

**Independent Test**: `scripts/ci/charter_service_check.py` composes and registers every pack, including the three built-in-level packs together.

**Acceptance Scenarios**:

1. **Given** `built-in`, `foundation` and `writing`, **When** composed, **Then** composition succeeds, `built-in` contributes no artifacts, and `generic-agent` resolves as the fallback profile.
2. **Given** `built-in` alone, **When** composed, **Then** it is refused with a dependency error naming `foundation`. This is the documented breaking change.
3. **Given** `foundation` alone, **When** composed, **Then** it succeeds.
4. **Given** the default distribution, **When** a mission step asks for a role no installed profile has (e.g. `researcher`), **Then** the fallback profile answers.

---

### User Story 2 - A team opts into specialist bundles (Priority: P1)

A Java team places the default distribution plus `java`, and gets java-jenny with her testing practices. A Python team adds `python` and `refactoring`.

**Why this priority**: This is the d14 outcome, and the stack PRs (rust/go) follow the same pattern.

**Independent Test**: The service check composes each bundle with its `depends_on` closure.

**Acceptance Scenarios**:

1. **Given** foundation, writing, testing and java, **When** composed, **Then** composition succeeds, and java-jenny's references to testing practices resolve.
2. **Given** java without testing, **When** composed, **Then** it is refused with a dependency error naming `testing`.
3. **Given** every pack together, **When** composed, **Then** there are no sibling conflicts and no cycles.

---

### User Story 3 - Existing org packs keep working (Priority: P2)

`internal`, `quality-assurance`, `event-driven`, `cave-kitty` and `spdd` keep composing. Every `built-in::` reference is rewritten to the pack that now holds the artifact, and each pack's `depends_on` names exactly the packs it references.

**Independent Test**: The service check composes each org pack.

**Acceptance Scenarios**:

1. **Given** the split, **When** the repository's pack content is searched for `built-in::`, **Then** nothing is found.
2. **Given** each org pack, **When** composed with its declared dependencies, **Then** it succeeds.

---

### User Story 4 - A pack author learns about manifest drift locally (Priority: P3)

An author adds a doctrine file to a pack that has a `pack-manifest.yaml` but forgets to list it there. The pack gate fails and names the file (#182).

**Independent Test**: Unit tests over fixture packs with a missing manifest entry and an extra one.

**Acceptance Scenarios**:

1. **Given** a file-backed doctrine artifact missing from its pack's manifest, **When** the gate runs, **Then** it fails and names the file.
2. **Given** a manifest entry with no file, **When** the gate runs, **Then** it fails and names the entry.
3. **Given** a pack without a manifest, **When** the gate runs, **Then** the guard does not apply.

### Edge Cases

- **Upward edges.** An edge from a lower pack to an artifact in a pack outside its closure is declared in the target pack's graph with a qualified source. The ranks are foundation < writing < built-in < org bundles, ordered by the bundle DAG. 110 edges are affected (computed).
- **Body references** (profile `*-references`, step-contract `delegates_to`) cannot be relocated. Exactly four leave their pack's closure. Each is dropped from the body, with its edge relocated:
  - analyst-annie → DIRECTIVE_047, relocated to writing (operator ruling);
  - diagram-daisy → USE_C4_MODEL_TECHNIQUES, relocated to architecture (operator ruling);
  - implementer-ivan's operating procedure test-first-bug-fixing, relocated to testing (same rule);
  - reviewer-renata's operating procedure adversarial-squad-deployment, relocated to adversarial-review (same rule).
- **Sibling conflicts.** foundation, writing and built-in are siblings at one level, and so are the org bundles. No id may be held twice.
- **Presets.** `default` activates the four mission types and `minimal` names foundation directives and tactics. Both stay on built-in and resolve through its closure.
- **Folder layout.** `missions/` keeps its name. `mission_types/` is retired at the charter pin.
- **Graph-only nodes.** 16 template nodes and 13 anti-pattern nodes have no file. They move as nodes with their bundle. Fixing them is out of scope.
- **Service-only refusals** (found by WP03's charter service check; the local precheck cannot see them), recorded in membership.json `service_check_folds`:
  - A bundle may not add a relationship to the locked fallback profile (ADR-0063), so one edge is dropped.
  - A graph-only node is not held for a cross-pack reference. Four weak edges to such nodes are dropped, and `template:glossary-template` moves to its only referrer, architecture.
- **Cut candidates** (DIRECTIVE_039, small-explicit-code-shaping, brownfield-onboarding) are parked, not cut: 039 and small-explicit-code-shaping in foundation, brownfield-onboarding in planning-analysis.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement | Status | Delivery | No-op passable? |
|---|---|---|---|---|
| FR-001 | `packs/foundation/` exists with `pack_id 01M75HSYR9S9KPA372PHGT0EX3`, `pack_level: built-in`, root, no `depends_on`, version 1.0.0. It holds exactly the `foundation` list in membership.json. | Approved | build | no |
| FR-002 | `packs/writing/` exists with `pack_id 01M75HSYS69RYRFPB4WCC5AC9D`, `pack_level: built-in`, root, `depends_on foundation ==1.0.0`, version 1.0.0. It holds exactly the `writing` list, including the documentation mission bundle and the glossary group. | Approved | build | no |
| FR-003 | Each of the ten bundles exists at `packs/<name>/` with the pack_id in membership.json, `pack_level: org`, root, version 1.0.0, and `depends_on` as in membership.json. Each holds exactly its list. | Approved | build | no |
| FR-004 | `quality-assurance` receives `sonar` and depends on `testing`. `spec-kitty-internal` receives its 4 items. | Approved | build | no |
| FR-005 | `built-in` keeps pack_id `01ARWG13C000000000000000FG` and `pack_level: built-in`. It holds no doctrine artifacts, depends on `foundation ==1.0.0` and `writing ==1.0.0`, keeps the `default` and `minimal` presets, and is version 2.0.0. | Approved | build | no |
| FR-006 | Artifacts move with `git mv`. Artifact ids do not change. | Approved | build | no |
| FR-007 | `generic-agent`'s display name becomes "Generic Giannis". Its id does not change. | Approved | build | no |
| FR-008 | Each pack's graph holds the nodes it owns. Each edge is homed in its source's pack when the target is in that pack's closure, and otherwise in the target's pack with a qualified source. Endpoints outside the home pack are qualified `<pack-name>::<urn>`. | Approved | build | no |
| FR-009 | No body or graph reference names a pack outside its writer's closure, and none names `built-in::`. The four body references listed under Edge Cases are dropped. | Approved | build | no |
| FR-010 | Every org pack (`internal`, `qa`, `event-driven`, `cave-kitty`, `spdd`) has its `built-in::` references rewritten, its `depends_on` set to the packs it references, and its `pack_version` bumped. | Approved | build | no |
| FR-011 | `charter_service_check.py` composes and registers every built-in-level pack and every org pack. | Approved | build | no |
| FR-012 | `pack-manifest.yaml` lists exactly its pack's constituents for built-in, foundation and writing. The built-in digest is re-recorded. | Approved | build | no |
| FR-013 | The pack gate fails when a file-backed doctrine artifact is missing from, or extra in, a pack's `pack-manifest.yaml` (#182). Unit tests cover it. | Approved | build | no |
| FR-014 | Docs record the split: an ADR, a 💥 Breaking CHANGELOG entry with a migration note, a README per new pack, `packs/README.md`, the catalog/index, and generated pack reference pages for every new pack. | Approved | build | no |
| FR-015 | Moved content that carries upstream attribution keeps a PROVENANCE note in its new pack. | Approved | build | no |
| FR-016 | foundation declares `fallback_profile: generic-agent` and locks it in its own `policy.yaml`, so org packs that depend only on foundation see the fallback, if the descriptor schema allows it. Otherwise the reason is recorded in the ADR. | Approved | build | no |

### Non-Functional Requirements

| ID | Requirement | Threshold | Status |
|---|---|---|---|
| NFR-001 | Membership fidelity | 100% of membership.json nodes sit in their assigned pack; 0 nodes are in two packs; 0 nodes are left in built-in | Approved |
| NFR-002 | Reference integrity | 0 dangling or out-of-closure references, per the pack gate and the charter service check | Approved |
| NFR-003 | Gate health | All repository gates are green on the final head; the docs-site build is green in CI | Approved |
| NFR-004 | History preservation | ≥ 95% of moved files are detected as renames by `git log --follow` | Approved |

### Constraints

| ID | Constraint | Status |
|---|---|---|
| C-001 | Align to the charter at the `charter.lock.yaml` pin. spec-kitty core compatibility is not a constraint (AGENTS.md). | Approved |
| C-002 | Pack ids are tool-minted ULIDs and are never edited. The abandoned specialist-staging id `01M75HSYSZ96965JHV2GKWCSEA` is not reused. | Approved |
| C-003 | `missions/` keeps its folder name. | Approved |
| C-004 | Whether built-in should aggregate `java` is not decided here; that needs a charter ADR amendment. | Approved |
| C-005 | Artifact content is not rewritten beyond reference qualification, edge relocation, the four body-reference drops and the display name. | Approved |
| C-006 | `pack-manifest.yaml` hashes are written only by the tool. | Approved |

## Success Criteria

- SC-001: The default distribution composes from three packs with zero refusals. — [build] · no-op passable: no
- SC-002: Each bundle composes with its declared closure. java composes on foundation + testing. — [build] · no-op passable: no
- SC-003: Pack content contains zero occurrences of `built-in::`. — [build] · no-op passable: no
- SC-004: Node counts per pack match membership.json (after the pre-PR folds recorded there): foundation 183, writing 67 (including one non-node file entry), testing 24, refactoring 35, architecture 36, planning-analysis 16, pack-authoring 7, python 5, javascript 13, drupal 4, java 4; built-in 0. — [build] · no-op passable: no

## Assumptions

- Without `planning-analysis`, the `researcher` and `facilitator` roles fall back to Generic Giannis. Without `architecture`, the documentation `design` step's `architect` role falls back the same way.
- Open PR #193 edits built-in paradigm files. Whichever of the two lands second rebases.
- The docs-site build cannot run in this container; CI is the authority.

## Out of Scope

- Cutting the parked cut candidates; merging the overlap clusters the curation lens found.
- Core spec-kitty fetch/pin changes.
- Renaming `missions/` to `mission_types/`.
- Deciding whether built-in aggregates `java`.
