# Tasks: Rust and Go stack packs

**Mission**: `rust-go-stack-packs-01M75FYM` · **Planning/merge branch**: `feat/rust-go-packs` (PR → `main`)
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md)

Every relation to `foundation` lives in the DRG fragment, never as a bare reference in a profile's
YAML. So WP01 to WP04 are complete and gate-green without `foundation`, and WP05 adds only the
dependency, the qualified edges and the regenerated pages.

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | Author `rust-conventions` styleguide | WP01 | [P] |
| T002 | Author `rust-review-checks` toolguide | WP01 | [P] |
| T003 | Author `rust-review-checks.guide.md` | WP01 | [P] |
| T004 | Author `rust-ruben` profile | WP01 | |
| T005 | Author the `rust` preset | WP01 | |
| T006 | Author `go-conventions` styleguide | WP02 | [P] |
| T007 | Author `go-review-checks` toolguide | WP02 | [P] |
| T008 | Author `go-review-checks.guide.md` | WP02 | [P] |
| T009 | Author `go-gwen` profile | WP02 | |
| T010 | Author the `go` preset | WP02 | |
| T011 | Mint pack_ids; write both `pack.yaml` | WP03 | |
| T012 | Write `pack.md`, `README.md`, `org-charter.yaml` for both | WP03 | [P] |
| T013 | Write both `PROVENANCE.md` | WP03 | [P] |
| T014 | Write both `drg/fragment.yaml` (local nodes and edges) | WP03 | |
| T015 | Run the pack gates on both packs | WP03 | |
| T016 | README + `packs/README.md` table rows | WP04 | [P] |
| T017 | Catalog-proposal rows and sections | WP04 | [P] |
| T018 | CHANGELOG `Added` entry | WP04 | [P] |
| T019 | Packs hub links, generated pages, docs build | WP04 | |
| T020 | Add `depends_on` foundation to both descriptors | WP05 | |
| T021 | Add qualified `foundation::` edges | WP05 | |
| T022 | Regenerate pages; re-run every gate | WP05 | |

## Phase 1 — Doctrine content (parallel)

### WP01 — Rust doctrine content ([prompt](tasks/WP01-rust-doctrine.md))

**Goal**: real, general-purpose Rust conventions, review checks, a specialist profile and a preset.
**Priority**: P1 (User Story 1). **Independent test**: schema validation of `packs/rust` (after WP03
adds the descriptor), and review by a Rust-idiom reviewer.

T001 Author `rust-conventions` styleguide (WP01)
T002 Author `rust-review-checks` toolguide (WP01)
T003 Author `rust-review-checks.guide.md` (WP01)
T004 Author `rust-ruben` profile (WP01)
T005 Author the `rust` preset (WP01)

Dependencies: none. Risks: idiom correctness, the 255-character principle cap, the guide's block order.

### WP02 — Go doctrine content ([prompt](tasks/WP02-go-doctrine.md))

**Goal**: the same as WP01, for Go. **Priority**: P1 (User Story 2).

T006 Author `go-conventions` styleguide (WP02)
T007 Author `go-review-checks` toolguide (WP02)
T008 Author `go-review-checks.guide.md` (WP02)
T009 Author `go-gwen` profile (WP02)
T010 Author the `go` preset (WP02)

Dependencies: none (parallel with WP01).

## Phase 2 — Pack shells and graph

### WP03 — Pack shells, provenance and local graph ([prompt](tasks/WP03-pack-shells-and-graph.md))

**Goal**: make both directories valid, composable packs.

T011 Mint pack_ids; write both `pack.yaml` (WP03)
T012 Write `pack.md`, `README.md`, `org-charter.yaml` for both (WP03)
T013 Write both `PROVENANCE.md` (WP03)
T014 Write both `drg/fragment.yaml` (local nodes and edges) (WP03)
T015 Run the pack gates on both packs (WP03)

Dependencies: WP01, WP02.

## Phase 3 — Discoverability

### WP04 — Catalog, docs and changelog ([prompt](tasks/WP04-catalog-docs-changelog.md))

T016 README + `packs/README.md` table rows (WP04)
T017 Catalog-proposal rows and sections (WP04)
T018 CHANGELOG `Added` entry (WP04)
T019 Packs hub links, generated pages, docs build (WP04)

Dependencies: WP03.

## Phase 4 — External dependency

### WP05 — Wire the `foundation` dependency ([prompt](tasks/WP05-foundation-wiring.md))

**Blocked** until #73's `foundation` pack has a pack_id on a branch or on `main`.

T020 Add `depends_on` foundation to both descriptors (WP05)
T021 Add qualified `foundation::` edges (WP05)
T022 Regenerate pages; re-run every gate (WP05)

Dependencies: WP04. WP05 edits files WP03 and WP04 created (`pack.yaml`, the fragments, the
generated pages). This is a deliberate, sequenced hand-over: WP05 runs strictly after them.

## MVP

WP01 + WP03 alone deliver a usable Rust pack, apart from the dependency declaration.
