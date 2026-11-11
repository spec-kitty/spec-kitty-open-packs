# Mission Specification: Rust and Go stack packs

**Mission Branch**: `feat/rust-go-packs`
**Created**: 2026-11-11
**Status**: Draft
**Input**: Issues #191 (rust) and #192 (go), epic #190, with #73's design and the operator rulings below.

## Purpose

Spec Kitty gives teams building in Rust or Go no stack doctrine today: built-in holds none, and only
two profiles name Rust as a keyword. This mission adds two opt-in org packs, `rust` and `go`. Each
holds real, general-purpose language conventions, a review-checks guide and a specialist implementer
profile, authored here under MIT. A project brings its stack's guidance into force by registering the
pack and activating one preset.

### Operator rulings (2026-11-11, binding)

- `built-in` does **not** aggregate `rust` or `go`. Stack packs are opt-in (#73, charter ADR-0048 d14,
  ADR-0053 q1). They are new, so no existing consumer loses anything.
- `rust` and `go` depend on the `foundation` pack from #73's split, not on `built-in`. Amended
  2026-11-11 (operator): they also depend on `testing`, for parity with `java`. `foundation`
  does not exist yet. The dependency and its qualified `foundation::` edges are wired last, and the
  draft pull request waits until `foundation` exists.
- All content is Spec Kitty-authored MIT. The seed idiom tables in `charter-cobol-migrations` are
  re-authored, never copied. Their contradictions are resolved, not carried over. No COBOL-specific
  content.
- The intent summary was confirmed, with both specialist profiles (decision
  `01M75G1RYC02T2PSRH5A67WQFV`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A Rust team brings Rust conventions into force (Priority: P1)

A team maintains a Rust service under Spec Kitty. They register the `rust` pack and activate its
`rust` preset. From then on, implement and review steps receive Rust guidance on these points:

- how to model validated values, errors and money;
- which checks a reviewer runs, and in which order;
- a Rust specialist profile that requires the conventions.

**Why this priority**: This is the pack's whole reason to exist. Without it, Rust work gets only
generic guidance.

**Independent Test**: Compose and register the `rust` pack with its dependency through the charter
service, then read its styleguide, toolguide, profile and preset.

**Acceptance Scenarios**:

1. **Given** a project with the `rust` pack registered, **When** the `rust` preset is activated,
   **Then** the `rust-conventions` styleguide, the `rust-review-checks` toolguide and the `rust-ruben`
   profile are in force.
2. **Given** the `rust` pack registered and no preset activated, **When** the charter is read,
   **Then** nothing from the pack is in force (its org-charter activates nothing).
3. **Given** a reviewer reading `rust-conventions`, **When** they check how money is modelled,
   **Then** the guidance is unambiguous: a decimal type, or a newtype over integer minor units that
   carries its currency. Never a float, never a bare integer.

### User Story 2 - A Go team brings Go conventions into force (Priority: P1)

The same journey as User Story 1, for Go with the `go` pack, the `go` preset, `go-conventions`,
`go-review-checks` and `go-gwen`.

**Why this priority**: It is the second deliverable of the same epic, and is independent of Rust.

**Independent Test**: As for User Story 1, for the `go` pack.

**Acceptance Scenarios**:

1. **Given** a project with the `go` pack registered, **When** the `go` preset is activated,
   **Then** `go-conventions`, `go-review-checks` and `go-gwen` are in force.
2. **Given** a reviewer reading `go-conventions`, **When** they check how a closed set of values is
   modelled, **Then** the guidance is a typed constant plus a validated set with an explicit check
   for unknown values, not untyped integers.

### User Story 3 - A reader finds the packs in the catalog and docs (Priority: P2)

A maintainer browsing the repository or the docsite sees `rust` and `go` in these places:

- the pack tables;
- the catalog proposal;
- the changelog;
- a generated reference page each.

They can see what each pack holds and how to adopt it.

**Why this priority**: Discoverability. The packs work without it, but nobody finds them.

**Independent Test**: Run the pack-page generator in check mode and build the docsite.

**Acceptance Scenarios**:

1. **Given** the merged change, **When** the pack-page generator runs in check mode, **Then** it
   reports no drift and `docs/packs/rust.md` and `docs/packs/go.md` exist.

### Edge Cases

- `foundation` is not on `main` when authoring finishes. The packs are complete except for the
  dependency, and the pull request is held, not opened with a dangling or interim dependency.
- `foundation`'s final membership differs from the proposal. Each `foundation::` edge is checked
  against the landed pack, and an edge to an artifact `foundation` does not hold is dropped or
  re-targeted.
- A Rust or Go artifact id collides with an id in another pack. Ids are unique across all packs; the
  cross-pack check catches a collision.
- `built-in` is touched by accident. Its digest gate (`check-built-in.sh`) must stay green and
  unchanged.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Requirement | Status | Delivery | No-op passable? |
| --- | --- | --- | --- | --- |
| FR-001 | `packs/rust` exists as an org pack with a tool-minted `pack_id`, `pack.yaml`, `pack.md`, `README.md`, `PROVENANCE.md`, an `org-charter.yaml` that activates nothing, a `rust` preset and `drg/fragment.yaml`. | Approved | [build] | no |
| FR-002 | `packs/rust` holds the styleguide `rust-conventions`, which covers: newtypes for bounded or validated values; raw `[u8; N]` only for unvalidated bytes at I/O boundaries; typed errors (`thiserror` in libraries, `anyhow` at binary edges); money as a decimal or a currency-carrying minor-units newtype, never a float or a bare integer; enums over magic integers; domain types free of storage or format dependencies; ownership and borrowing; `unsafe` discipline; and doc comments on public items. | Approved | [build] | no |
| FR-003 | `packs/rust` holds the toolguide `rust-review-checks` with its guide: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`, `cargo doc`, and `cargo deny` / `cargo audit` for the supply chain, in cheapest-first order. | Approved | [build] | no |
| FR-004 | `packs/rust` holds the specialist implementer profile `rust-ruben`, which `requires` `rust-conventions` (#131) and uses `rust-review-checks`. | Approved | [build] | no |
| FR-005 | `packs/go` exists as an org pack with the same files as FR-001 and a `go` preset. | Approved | [build] | no |
| FR-006 | `packs/go` holds the styleguide `go-conventions`, which covers: money as a decimal or integer minor units, never `float64`; typed constants plus a validated set with an explicit check for unknown values; an explicit context or environment struct instead of package globals; small functions with an explicit state type instead of long fall-through flows; `goto` only for error cleanup; errors wrapped with `%w` and checked with `errors.Is` / `errors.As`; `context.Context` as the first parameter; small consumer-side interfaces; and goroutine lifecycle ownership. | Approved | [build] | no |
| FR-007 | `packs/go` holds the toolguide `go-review-checks` with its guide: `gofmt`, `go vet`, `staticcheck` or `golangci-lint`, `go test -race`, and `govulncheck`, in cheapest-first order. | Approved | [build] | no |
| FR-008 | `packs/go` holds the specialist implementer profile `go-gwen`, which `requires` `go-conventions` and uses `go-review-checks`. | Approved | [build] | no |
| FR-009 | Each pack `depends_on` `foundation` (range `>=1.0,<2`). Every cross-pack edge is written `foundation::<kind>:<id>` and targets an artifact the landed `foundation` holds. Each profile `specializes_from` `foundation::agent_profile:implementer-ivan`. | Approved | [build] | no |
| FR-010 | `built-in` is unchanged: no file under `packs/built-in/` and no `built-in.source.yaml` change. | Approved | [ratchet] | yes — the positive control is FR-001/FR-005 adding pack files while `check-built-in.sh` still passes |
| FR-011 | `docs/packs/rust.md` and `docs/packs/go.md` are generated by `scripts/docs/gen_pack_reference.py`, and the docs nav lists them. | Approved | [build] | no |
| FR-012 | The `README.md` pack table and status row, `packs/README.md`, the catalog proposal and the CHANGELOG `Added` section name both packs. Vocabulary entries are added only where the vocabulary guard needs them. | Approved | [build] | no |
| FR-013 | Each pack's `PROVENANCE.md` records the seed material (charter-cobol-migrations at `2c4ce2a`, its Rust/Go READMEs), states that nothing was copied, and lists each seed contradiction and how it was resolved. | Approved | [build] | no |

### Non-Functional Requirements

| ID | Requirement | Threshold | Status |
| --- | --- | --- | --- |
| NFR-001 | Every styleguide rule is concrete enough for a reviewer to apply. | Every pattern and anti-pattern entry has a compilable-in-spirit bad and good example; 0 rules without an example or a stated reason. | Approved |
| NFR-002 | The packs are general-purpose. | 0 occurrences of COBOL, ACAS or legacy-port terms in either pack outside `PROVENANCE.md`. | Approved |
| NFR-003 | The packs pass every repository gate. | `validate-packs.sh`, `check-built-in.sh`, `check_vocabulary.py`, `gen_pack_reference.py --check`, every `tests/*` unittest suite and the docsite build all exit 0; the charter service check exits 0 in CI. | Approved |

### Constraints

| ID | Constraint | Status |
| --- | --- | --- |
| C-001 | MIT, authored for this repository. No verbatim text from charter-cobol-migrations. | Approved |
| C-002 | `built-in` does not aggregate `rust` or `go`, and PR B does not touch `built-in`. | Approved |
| C-003 | The dependencies are `foundation` and `testing` (java parity, operator ruling 2026-11-11), not `built-in`. No interim `built-in` dependency is shipped. | Approved |
| C-004 | Org packs carry no `pack-manifest.yaml` (the repository's convention: only `built-in` has one). If `foundation` or #182 introduces an org-pack manifest convention before merge, the packs follow it. | Approved |
| C-005 | Shared files (README tables, catalog proposal, CHANGELOG, nav) change by minimal added rows only, so a concurrent pull request can rebase over them. | Approved |
| C-006 | The charter service jar cannot be built in this session: the permission classifier refused it as external code. The service check is proven in CI only, and the PR says so. | Approved |

### Key Entities

- **Stack pack**: an opt-in org pack (`pack_level: org`) named after its stack, holding that stack's
  doctrine.
- **Conventions styleguide**: the stack's rules for code shape, with principles, patterns,
  anti-patterns and tooling.
- **Review-checks toolguide**: the commands a reviewer runs, and their order.
- **Specialist profile**: an implementer that specializes `implementer-ivan` for one language and
  requires that language's conventions.

## Domain Language

- **`foundation`**: the #73 root pack (ADR-0053 d9). It is not called "fundamentals" or
  "foundations".
- **Minor units**: an integer count of a currency's smallest unit (cents). It is always held in a
  type that carries the currency.

## Success Criteria *(mandatory)*

- **SC-001**: A project can bring Rust or Go guidance into force with one preset activation, and
  nothing is in force without it. — [build] · no-op passable: no
- **SC-002**: Both packs pass 100% of the repository gates on the final head (NFR-003). — [build] · no-op passable: no
- **SC-003**: The pre-PR review squad (pack format, Rust idiom, Go idiom) leaves 0 unaddressed findings: each is folded, or deferred with a rationale and an issue. — [build] · no-op passable: no
- **SC-004**: 0 files under `packs/built-in/` change. — [ratchet] · no-op passable: yes (control: SC-002)

## Assumptions

- `foundation` lands with the membership the orchestrator relayed (implementer-ivan, the
  cross-cutting directives 010/024/025/030/034/…, the dependency-hygiene and
  supply-chain-install-safety tactics). Edges are re-checked against the landed pack.
- The docs nav is generated or listed in `docs/_meta/sections.yaml` the way the other packs are.

## Dependencies

- #73 / `feat/73-foundation-writing-split` (session `session_01E5wJUCYwZWDSZZ3496hAyS`): provides
  `foundation`'s `pack_id`. This blocks FR-009 and the draft pull request.
- The charter at the commit pinned in `charter.lock.yaml`: schemas and the service.
