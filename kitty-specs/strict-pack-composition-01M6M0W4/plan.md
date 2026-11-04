# Implementation Plan: Strict pack composition

**Branch**: `feat/strict-pack-composition` | **Date**: 2026-11-04 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/strict-pack-composition-01M6M0W4/spec.md`; research in [research.md](research.md).

## Summary

Make the gate understand qualified references first, then give every pack an identity, fix the built-in sidecars, and migrate the three packs with cross-pack references, smallest first. `quality-assurance` is the tracer: it proves the method and the real compose before the larger migrations. A companion pull request in spec-kitty-charter holds the authoritative compose test and moves the pin after this mission merges.

## Technical Context

**Language/Version**: Python 3.12 (gate and generator, `scripts/`); YAML and Markdown (pack content). The companion test is Java 25 in spec-kitty-charter.
**Primary Dependencies**: `pyyaml` 6.0.3 and `jsonschema` 4.26.0 (already pinned). No dependency is added, removed or upgraded, so no supply-chain check applies.
**Storage**: Files in the repository.
**Testing**: stdlib `unittest` (`tests/ci`, `tests/docs`, `tests/release`, `tests/vocabulary`); `scripts/ci/validate-packs.sh`; `scripts/ci/check-built-in.sh`; JUnit in the charter's `:packs` Gradle project, runnable locally with `JAVA_HOME=/usr/lib/jvm/temurin-25`.
**Target Platform**: GitHub Actions; the charter service (strict composition).
**Project Type**: Content repository with a validation gate.
**Performance Goals**: The gate grows by under 5 seconds over all packs (NFR-001).
**Constraints**: See spec C-001 to C-008. Local checks stay thin (NFR-002); the charter is the authority.
**Scale/Scope**: 93 reference sites in 3 packs, 3 new descriptors, 6 sidecars; the full list is in [reference-inventory.txt](reference-inventory.txt).

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Charter rule | How this plan meets it |
|---|---|
| Docs are a first-class deliverable | FR-012 and FR-015; generated pages regenerate with each pack change |
| Decisions are recorded as ADRs | One ADR at close-out: the end of CLI compatibility, the two reference forms, and pack names |
| Gates fail closed | The guard is added to the gate; the temporary allowance for unmigrated packs is a named list that only shrinks and is deleted by the end |
| Identity discipline: `pack_id` minted once | C-002; ids are generated once in the identity work and never edited after |
| `NO_FULL_HEAVY_SUITES_IN_MISSION` | Only the suites above and the charter's `:packs` compose test run locally |

No violations. Re-checked after design: unchanged.

## Project Structure

### Documentation (this mission)

```
kitty-specs/strict-pack-composition-01M6M0W4/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── occurrence_map.yaml
└── reference-inventory.txt
```

`meta.json` declares `contracts: none`: the contract is owned by spec-kitty-charter `contracts/packs`, and this mission defines no interface.

### Source Code (repository root)

```
scripts/ci/validate_pack_schemas.py   # contract pin, qualifier parsing, composition checks
scripts/ci/check-built-in.sh, built_in_digest.py  # "re-seed" wording
scripts/docs/gen_pack_reference.py    # depends_on reader
tests/ci/, tests/docs/, tests/fixtures/
packs/{built-in,internal,qa,event-driven,cave-kitty}/
docs/guides/, docs/packs/ (generated), docs/architecture/adr/, docs/changelog/
```

**Structure Decision**: Existing layout, no new top-level paths. Charter-side work lives in spec-kitty-charter, on its own branch and pull request.

## Key decisions

- **Temporary allowance over a late guard.** `validate_pack_schemas.py` holds `PENDING_PACKS`, the packs not yet migrated. The bare-reference check runs from the start for everything else, each migration removes its pack, and close-out deletes the list. A guard added only at the end would leave migrated packs unprotected, and would give no early proof that it works. Rejected: enabling it per pack by flag (more surface for no gain).
- **Two reference forms, one parser.** Edges carry `<pack>::<kind>:<id>`, typed references carry `<pack>::<id>`. Only one split point, on `::`, is added to the gate. The schema already polices each form.
- **Resolve by descriptor name, not directory.** A qualifier names `pack.yaml`'s `name`, so `packs/qa` answers to `quality-assurance`.
- **Sequential work.** Migrations share generated pages and the allowance list, and the tracer must prove the method first, so lanes would save little and risk conflicts.
- **Charter pin order.** A draft charter pull request points `openPacksRef` at this branch's head to prove the compose before merge. It is re-pointed at the final `main` commit afterwards (C-006), because a rebase merge changes the SHA.
- **Migration tool, not hand edits.** Qualifying is scripted from the inventory and rewrites only the matched values, preserving comments and formatting. Robbie's research migration reformatted files through PyYAML and is not reused as is.

## Complexity Tracking

No Charter Check violations.

## Implementation Concern Map

> **Note**: Implementation concerns are NOT work packages and are NOT executable units.
> `/spec-kitty.tasks` translates these into executable WPs.

### IC-01 — Gate understands composition

- **Purpose**: Without this, correct content fails the gate and incorrect content passes it.
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-012
- **Affected surfaces**: `scripts/ci/validate_pack_schemas.py`, `scripts/docs/gen_pack_reference.py`, `tests/ci/`, `tests/docs/`, `tests/fixtures/`, `docs/guides/validate-a-pack.md`
- **Sequencing/depends-on**: none
- **Risks**: Must stay under the NFR-002 line limit; must not drift into reimplementing the charter's resolver.

### IC-02 — Pack identity

- **Purpose**: A pack with no descriptor is refused on its own, and `depends_on` needs one.
- **Relevant requirements**: FR-004, FR-006
- **Affected surfaces**: `packs/{qa,event-driven,cave-kitty}/pack.yaml`, `tests/fixtures/valid/example-pack/pack.yaml`, `packs/internal/glossary_packs/`, `packs/internal/org-charter.yaml`, `packs/internal/drg/fragment.yaml`
- **Sequencing/depends-on**: IC-01
- **Risks**: `pack_id`s and names are permanent. The glossary rename overlaps the `internal` migration's file.

### IC-03 — Built-in sidecars

- **Purpose**: Until these are fixed, every compose with `built-in` is refused, which hides reference refusals.
- **Relevant requirements**: FR-007
- **Affected surfaces**: `packs/built-in/assets/**/*.asset.yaml`, `packs/built-in/pack-manifest.yaml`, `packs/built-in.source.yaml`, `docs/packs/built-in.md`, `scripts/ci/check-built-in.sh`, `scripts/ci/built_in_digest.py`
- **Sequencing/depends-on**: none
- **Risks**: Digest collision with #94 from the separate runner: second to land regenerates. Core's `_anchor_for` breaks at its next pin bump (follow-up issue).

### IC-04 — Tracer and real compose

- **Purpose**: Prove the method and the runtime on the smallest pack before anything larger.
- **Relevant requirements**: FR-005, FR-008, FR-011, FR-013; C-005
- **Affected surfaces**: `packs/qa/`, the migration script; spec-kitty-charter compose test on a draft pull request
- **Sequencing/depends-on**: IC-01, IC-02, IC-03
- **Risks**: Refusals beyond `pack_reference_*` could surface here, and that is the point of doing it early. If `dispatch` or `next` break on migrated content, the run pauses for the operator.

### IC-05 — Migrate remaining packs

- **Purpose**: Bring `event-driven`, `internal` and `cave-kitty` in line.
- **Relevant requirements**: FR-005, FR-009, FR-010
- **Affected surfaces**: `packs/event-driven/`, `packs/internal/`, `packs/cave-kitty/pack.yaml`, `docs/packs/`
- **Sequencing/depends-on**: IC-04
- **Risks**: `internal` is last (C-005). #105, #106 and #92 touch the same `internal` procedures: whichever lands second rebases.

### IC-06 — Close-out

- **Purpose**: Remove the allowance, state the new reality, and correct the record.
- **Relevant requirements**: FR-014, FR-015, FR-016
- **Affected surfaces**: `scripts/ci/validate_pack_schemas.py`, `docs/guides/compose-packs.md`, `docs/architecture/adr/`, `docs/changelog/CHANGELOG.md`, issue text, the charter pull request
- **Sequencing/depends-on**: IC-05
- **Risks**: FR-014's final step happens after this mission's pull request merges, so it is tracked as a follow-through in the hand-off, not left implied.
