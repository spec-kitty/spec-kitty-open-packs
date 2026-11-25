# Implementation Plan: Align open-packs to charter main with pack-doctor

**Branch**: `kitty/mission-pack-doctor-alignment-01M88RH1` → `feat/pack-doctor-alignment` | **Date**: 2026-11-25 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/pack-doctor-alignment-01M88RH1/spec.md`

## Summary

Move open-packs' charter gate from pack-check (charter `service-v0.1.0-rc.3`) to pack-doctor built from charter
`main`, pinned on demand:

- the jar script, the lock field, `validate … --round-trip --full`, and `PackDoctorReport` parsing;
- the two #343 fixture expectations;
- the 273 inline anti-pattern entries and 15 file-less nodes curated into `anti_patterns/<id>.anti-pattern.yaml` files
  with `rejects` edges, driven by per-pack ledgers that make every severity and bad-example call reviewable;
- every pack restamped with `pack-doctor remediate`;
- retirement of the Python rules the charter now judges, keeping the house rules with their rulings.

The rename pack-check → pack-doctor is a bulk edit governed by [`occurrence_map.yaml`](occurrence_map.yaml).

## Technical Context

**Language/Version**: Python 3.11+ (CI scripts, standard library plus PyYAML/jsonschema as today), Bash (jar scripts), Java 25 (runs pack-doctor), YAML pack content
**Primary Dependencies**: spec-kitty-charter `main` (pack-doctor jar and service jar built from the pinned commit), GitHub Actions workflows `validate-packs.yml` and `charter-track.yml`. No new third-party dependency.
**Storage**: files: `packs/**`, `tests/fixtures/**`, `charter.lock.yaml`
**Testing**: pytest under `tests/ci` (with `RealPackCheck`-style tests renamed for pack-doctor and run against the built jar); `validate-packs.sh`, `--cross-pack`; `pack-doctor validate --round-trip --full`; the mission's `apply_curation.py --check`
**Target Platform**: GitHub Actions `ubuntu-latest` and a local Linux checkout
**Project Type**: single (content repository with CI tooling)
**Performance Goals**: the pack-doctor run over 19 packs and the valid fixtures stays within the gate's existing 600 s timeout (measured today: ~25 s)
**Constraints**: a main pin needs network access to github.com and the Gradle repositories in CI (as the main-pin path does today); `remediate` runs from the repository root; the report file lies outside every pack
**Scale/Scope**: 19 packs; 61 files with inline blocks (273 entries); 15 file-less nodes; ~25 tooling files in the rename; about 30 tests touched

## Charter Check

| Charter point | How the plan meets it |
|---|---|
| The charter owns the pack logic; the packs align to the charter, not core | The gate runs the charter's own checker. Python copies of its rules retire (FR-014). Core compatibility is not weighed (AGENTS.md). |
| Pin policy (release by default, main on demand) | A main pin, on demand, by operator ruling (C-002, R1) |
| Gates fail closed | The report parser fails closed on unknown keys, skipped checks, an `exit_code` mismatch and unknown warnings (FR-005) |
| Docs are first-class; generated vs authored | Guides updated (FR-019). Generated pack reference pages regenerated, never hand-edited. Changelog entry (FR-020). |
| ADRs are superseded, never edited | The 2026-11-19-3 ADR stays as history (occurrence-map exception). No new ADR is needed: the decisions are the charter's ADR-0083 and ADR-0052, which this plan follows. |
| Tests only where they guard real behaviour (DIRECTIVE_041) | Retired rules take their tests with them. New tests guard the report parsing, the command line and the ledger check. |
| Identity discipline | No `pack_id` changes. Anti-pattern ids derive from their titles once, recorded in the ledger. |

No violation, so no complexity tracking is needed.

## Project Structure

### Documentation (this mission)

```
kitty-specs/pack-doctor-alignment-01M88RH1/
├── spec.md  plan.md  research.md  data-model.md  quickstart.md  occurrence_map.yaml
├── curation/                 # created in WP02
│   ├── apply_curation.py     # applies and checks the ledgers
│   └── <pack>.ledger.yaml    # one per pack with anti-patterns
└── tasks/
```

### Source Code (repository root)

```
charter.lock.yaml                                  # main pin, pack_doctor_sha256
scripts/ci/charter_pack_doctor_jar.sh              # renamed from charter_pack_check_jar.sh
scripts/ci/charter_pack_doctor.py                  # renamed from charter_pack_check.py
scripts/ci/{charter_lock,charter_pin,charter_service_check,validate_pack_schemas}.py, validate-packs.sh
.github/workflows/{validate-packs,charter-track}.yml
tests/ci/test_{charter_pack_doctor,charter_pin,charter_service_check,validate_pack_schemas,workflows}.py
tests/fixtures/invalid/*/expected-code
packs/<pack>/anti_patterns/*.anti-pattern.yaml     # new
packs/<pack>/{styleguides,procedures}/*.yaml       # inline blocks removed
packs/<pack>/{drg/fragment.yaml | *.graph.yaml}    # nodes + rejects edges
packs/*/pack-manifest.yaml, tests/fixtures/valid/*/pack-manifest.yaml   # restamped
docs/guides/validate-a-pack.md, docs/artefacts/index.md, docs/changelog/CHANGELOG.md
```

**Structure Decision**: a single repository. The curation tool and ledgers are mission records under `kitty-specs/`, not
product code. The product holds only the files they produce.

## Complexity Tracking

None.

## Implementation Concern Map

> **Note**: Implementation concerns are NOT work packages and are NOT executable units.

### IC-01: The pack-doctor gate at a main pin

- **Purpose**: obtain, invoke and judge pack-doctor at the pinned charter `main` commit, with one name per tool.
- **Relevant requirements**: FR-001 to FR-006, FR-016, FR-019 (tooling surfaces)
- **Affected surfaces**:
  - the lock, `charter_lock.py`, `charter_pin.py`;
  - the jar script and the gate script (renamed);
  - `charter_service_check.py` (the `pack-check:` expectation key);
  - both workflows, their tests, the 5 invalid fixtures' `expected-code`.
- **Sequencing/depends-on**: none. Implementation starts after PR #344 merges (C-001).
- **Risks**:
  - #344 overlaps these files. Rebase on it, never edit its branch.
  - The gate is red on the mission branch until the curation lands. That is expected, and is recorded in each review.

### IC-02: The curation tool, ledger format, and the 15 file-less nodes

- **Purpose**: a deterministic apply and check of per-pack ledgers, piloted on the 15 file-less nodes whose text is
  already grounded in `rejects` reasons and tactics. Also, the Python schema pass learns anti-pattern files (a
  constituent, not graph-only).
- **Relevant requirements**: FR-009, FR-010, FR-017, FR-014 (the anti-pattern-model part)
- **Affected surfaces**:
  - `kitty-specs/…/curation/`;
  - `packs/{architecture,refactoring,foundation}`;
  - `validate_pack_schemas.py` (`MANIFEST_EXEMPT_NODE_KINDS`, the `CONSTITUENT_KIND_BY_SCHEMA` note, `held_artifacts`)
    and its tests.
- **Sequencing/depends-on**: none. Severity calls for these 15 still follow the operator's rubric decision.
- **Risks**: the two graph layouts. The tool must write each pack's existing layout.

### IC-03: Curating the inline blocks (five batches, ≤70 entries each)

- **Purpose**: move each entry to its file in its owner's pack, with a `rejects` edge, and delete the inline blocks.
- **Relevant requirements**: FR-007, FR-008, FR-010
- **Batches**:
  - A, language stacks: architecture 6, drupal 14, event-driven 3, go 10, java 6, javascript 15, python 5, rust 9;
    68 in all.
  - B: foundation 23, qa 2, pack-authoring 14, planning-analysis 19; 58 in all.
  - C: internal procedures, 54.
  - D: internal styleguides 16 and testing 38; 54 in all.
  - E: writing, 39.
- **Sequencing/depends-on**: IC-02, and the three operator decisions (dedupe, severity rubric, bad-example source).
- **Risks**:
  - Judgement volume. Every ungroundable call becomes an `operator_question` row, batched to the dispatcher.
  - The ledger's grounding column is the reviewers' surface.

### IC-04: Restamp with `remediate` and the pin's re-derive

- **Purpose**: canonical manifests and file forms from the charter's writer. `charter_pin.py rederive` uses it.
- **Relevant requirements**: FR-011, FR-012, FR-013, FR-018
- **Affected surfaces**: every `pack-manifest.yaml`, the modelled files `remediate` rewrites, `charter_pin.py`, and the
  pin tests.
- **Sequencing/depends-on**: IC-01, IC-03 (remediate refuses packs with unrepaired faults).
- **Risks**:
  - The canonicalisation diff is large. It gets a commit of its own and a YAML-load equality proof (NFR-003).
  - The first full `CLOSURE`/`REFERENCES` run may surface faults the skipped checks hid. Each is fixed here or raised.

### IC-05: Retire the Python rules pack-doctor judges; keep the house rules

- **Purpose**: one answer per rule.
- **Relevant requirements**: FR-013 (the Python side), FR-014, FR-015
- **Affected surfaces**: `validate_pack_schemas.py`, `validate-packs.sh`, `tests/ci/test_validate_pack_schemas.py`
- **Sequencing/depends-on**: IC-01 (the gate covers them), IC-04 (the derivation retires once `remediate` replaces it)
- **Risks**: removing a rule whose charter equivalent does not fire here. Each retirement is paired with an in-test
  pack that pack-doctor refuses with the charter code.

### IC-06: Docs, changelog, and the closing measurement

- **Purpose**:
  - the guides state the split and the anti-pattern file model;
  - no live surface names pack-check;
  - the changelog entry;
  - the final measurement: `validate --round-trip --full` exits 0, and the charter-track `ref` run is green.
- **Relevant requirements**: FR-019, FR-020; SC-001 to SC-004
- **Affected surfaces**: `docs/guides/validate-a-pack.md`, `docs/artefacts/index.md`, the generated reference pages,
  `CHANGELOG.md`
- **Sequencing/depends-on**: all the above
- **Risks**: generated pages must be regenerated, never hand-edited.

## Decisions pending (operator)

[NEEDS CLARIFICATION: Dedupe scope for the curation (IC-03).] <!-- decision_id: 01M88RHDGQSS6R5R5ZCDCH84A2 -->

[NEEDS CLARIFICATION: Severity rubric for the curation (IC-02, IC-03).] <!-- decision_id: 01M88RHFTS2X5HK1ZNP74G3WZ7 -->

[NEEDS CLARIFICATION: bad_example source for title/content entries (IC-03).] <!-- decision_id: 01M88RHJ9HN4N8HDE97SJ6ZBAH -->
