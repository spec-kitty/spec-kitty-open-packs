# Tasks: Strict pack composition

**Branch**: `feat/strict-pack-composition` | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

All work is sequential on one lane: migrations share generated pages and the allowance list, and the tracer must prove the method first. WP02 and WP03 could run together, but nothing is gained.

**Next required step**: `/spec-kitty.analyze`, then implementation.

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Bump the contract pin and correct validate-a-pack.md | WP01 | |
| T002 | Parse qualifiers in cross_pack_violations, tests first | WP01 | |
| T003 | Add the composition checks and PENDING_PACKS | WP01 | |
| T004 | Fix the depends_on reader and purpose wording in the docs generator | WP01 | |
| T005 | Validate, including half-by-half reverts | WP01 | |
| T006 | Mint ids and write four descriptors | WP02 | |
| T007 | Declare cave-kitty's dependency | WP02 | |
| T008 | Remove the descriptor allowance and validate | WP02 | |
| T009 | Fix six sidecar paths with manifest, digest and page, atomically | WP03 | |
| T010 | Correct the re-seed wording | WP03 | |
| T011 | Validate, including through the service | WP03 | |
| T012 | Migrate quality-assurance's 3 references and declare depends_on | WP04 | |
| T013 | Check the 24 profile references | WP04 | |
| T014 | Real compose on a charter draft pull request | WP04 | |
| T015 | Try the mission runtime on migrated content | WP04 | |
| T016 | Validate | WP04 | |
| T017 | Qualify event-driven's 12 references in both forms | WP05 | |
| T018 | Declare the dependency and regenerate its page | WP05 | |
| T019 | Validate, and extend the compose test | WP05 | |
| T020 | Qualify internal's 78 references, including 5 agent_profile edges | WP06 | |
| T021 | Declare the dependency | WP06 | |
| T022 | Rename the glossary pack file | WP06 | |
| T023 | Validate, with all five composing, and repeat the runtime check | WP06 | |
| T024 | Delete PENDING_PACKS and prove the guard | WP07 | |
| T025 | Write the ADR and changelog entry | WP07 | |
| T026 | Correct the guides | WP07 | |
| T027 | Correct stale issue text and file follow-ups | WP07 | |
| T028 | Finish the charter draft for re-pointing | WP07 | |

## WP01: Gate understands composition

**Prompt**: [tasks/WP01-gate-understands-composition.md](tasks/WP01-gate-understands-composition.md)

**Goal**: Teach the gate the strict composition rules, so correct qualified references pass and incorrect ones fail, while nothing has been migrated yet. Today it does the opposite: `validate_pack_schemas.py:782-783` reads `built-in::tactic:x` as kind `built-in`, so 67 correct edges would fail, and it passes everything the service refuses.

**Dependencies**: None

**Requirements**: FR-001, FR-002, FR-003, FR-012, NFR-001, NFR-002, C-003, C-004

**Subtasks**:

T001 Bump the contract pin and correct validate-a-pack.md (WP01)
T002 Parse qualifiers in cross_pack_violations, tests first (WP01)
T003 Add the composition checks and PENDING_PACKS (WP01)
T004 Fix the depends_on reader and purpose wording in the docs generator (WP01)
T005 Validate, including half-by-half reverts (WP01)

**Independent test**: All gates pass on as-is content. Each FR-003 defect has a test that fails without its check. `PENDING_PACKS` exists and is documented. Added production lines reported, under 150.

## WP02: Pack identity

**Prompt**: [tasks/WP02-pack-identity.md](tasks/WP02-pack-identity.md)

**Goal**: Give every pack a compliant descriptor. A pack with none is refused on its own, and `depends_on` needs one. These identities are permanent.

**Dependencies**: Depends on WP01

**Requirements**: FR-004, FR-005, C-002

**Subtasks**:

T006 Mint ids and write four descriptors (WP02)
T007 Declare cave-kitty's dependency (WP02)
T008 Remove the descriptor allowance and validate (WP02)

**Independent test**: Four descriptors exist with unique, tool-generated ids. All gates pass with the descriptor allowance removed.

## WP03: Built-in sidecars

**Prompt**: [tasks/WP03-built-in-sidecars.md](tasks/WP03-built-in-sidecars.md)

**Goal**: Fix the six sidecars whose `path` is anchored at the pack root. The charter requires it relative to `assets/` (`SidecarPayloads.java:46-63`, ADR-0040 decision 6). Until this lands, every compose with `built-in` is refused `pack_unreadable`, which hides all reference refusals.

**Dependencies**: Depends on WP01

**Requirements**: FR-007

**Subtasks**:

T009 Fix six sidecar paths with manifest, digest and page, atomically (WP03)
T010 Correct the re-seed wording (WP03)
T011 Validate, including through the service (WP03)

**Independent test**: Six paths fixed, manifest, digest and page updated in the same commit, wording corrected, gates pass, and the service reads all six assets.

## WP04: Tracer: quality-assurance and the real compose

**Prompt**: [tasks/WP04-tracer-and-real-compose.md](tasks/WP04-tracer-and-real-compose.md)

**Goal**: Prove the method on the smallest pack before anything larger: migrate its 3 references, get a real compose through the service's own code, and find out early whether the mission's own runtime survives migrated content. If surprises exist, this is where they should surface.

**Dependencies**: Depends on WP02, WP03

**Requirements**: FR-005, FR-008, FR-011, FR-013, C-005

**Subtasks**:

T012 Migrate quality-assurance's 3 references and declare depends_on (WP04)
T013 Check the 24 profile references (WP04)
T014 Real compose on a charter draft pull request (WP04)
T015 Try the mission runtime on migrated content (WP04)
T016 Validate (WP04)

**Independent test**: `quality-assurance` composes with `built-in` through the service's own code, negative controls refuse, the runtime check is reported, FR-011 has an outcome, gates pass, and `qa` is out of `PENDING_PACKS`.

## WP05: Migrate event-driven

**Prompt**: [tasks/WP05-migrate-event-driven.md](tasks/WP05-migrate-event-driven.md)

**Goal**: Qualify `event-driven`'s 12 references to `built-in`, in both reference forms, and declare the dependency.

**Dependencies**: Depends on WP04

**Requirements**: FR-005, FR-009

**Subtasks**:

T017 Qualify event-driven's 12 references in both forms (WP05)
T018 Declare the dependency and regenerate its page (WP05)
T019 Validate, and extend the compose test (WP05)

**Independent test**: 0 bare cross-pack references in the pack by the independent scan, compose succeeds in the charter draft, gates pass.

## WP06: Migrate internal

**Prompt**: [tasks/WP06-migrate-internal.md](tasks/WP06-migrate-internal.md)

**Goal**: Qualify `internal`'s 78 references to 31 `built-in` targets, and finish #47's glossary rename. This is the largest migration, and it goes last because `internal` carries this repository's own governance (C-005).

**Dependencies**: Depends on WP05

**Requirements**: FR-005, FR-006, FR-010

**Subtasks**:

T020 Qualify internal's 78 references, including 5 agent_profile edges (WP06)
T021 Declare the dependency (WP06)
T022 Rename the glossary pack file (WP06)
T023 Validate, with all five composing, and repeat the runtime check (WP06)

**Independent test**: 78 references qualified, scan shows 0 `bare->other` across all packs, all five packs compose, runtime check reported, gates pass, `PENDING_PACKS` is empty.

## WP07: Close-out

**Prompt**: [tasks/WP07-close-out.md](tasks/WP07-close-out.md)

**Goal**: Remove the allowance, record the decision, state the new reality, correct the stale record, and hand off a draft charter pull request that is ready to re-point.

**Dependencies**: Depends on WP06

**Requirements**: FR-014, FR-015, FR-016, C-001, C-006, C-007, C-008, NFR-003

**Subtasks**:

T024 Delete PENDING_PACKS and prove the guard (WP07)
T025 Write the ADR and changelog entry (WP07)
T026 Correct the guides (WP07)
T027 Correct stale issue text and file follow-ups (WP07)
T028 Finish the charter draft for re-pointing (WP07)

**Independent test**: No allowance remains, the ADR and changelog exist, guides are true, stale issues are corrected with URLs reported, and the charter draft is green against this mission's head with the re-pointing step named in the hand-off.

