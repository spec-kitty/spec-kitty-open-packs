# Mission Specification: Charter slice B migration

**Mission Branch**: `feat/slice1-readme-retire-org-charter`
**Created**: 2026-11-12
**Status**: Accepted for planning
**Input**: Issues #241 (README is the pack document) and #242 (retire `org-charter.yaml` and `active_charter`), plus
the bump of `charter.lock.yaml` to a charter commit that carries slice B (spec-kitty-charter PR #501). Slice 1 of
`docs/plans/next-slices-2026-11.md`. The operator ruled on 2026-11-12 that all three land in one pull request on a
commit pin.

## Intent Summary

- **Primary actor:** the open-packs CI ("Charter service validation"), acting for a pack maintainer, and any org that
  registers a pack with the charter service.
- **Trigger:** the charter's slice B refuses `pack.md`, `PROVENANCE.md` and `org-charter.yaml` by name (`retired`), and
  cannot read a `pack.yaml` that declares `active_charter` (`pack_unreadable`). Against slice B, 0 of the 12 packs with
  an org charter and 7 more packs with only the Markdown files register today.
- **Outcome:** with the pin moved to charter `17ce3f9`, all 19 packs register with no `retired`, `unreadable` or
  `pack_unreadable` refusal. Each pack's documentation is one root `README.md`, and `internal`'s org enforcement is the
  must-have floor of its `base` preset.
- **Invariant:** nothing a pack enforced is lost. Every one of `internal`'s 18 required ids is a must-have item of
  `presets/base.yaml`. Every `PROVENANCE.md` body survives as a `## Provenance` section.
- **Operator decisions** (Decision Moments `01M78K2D…` and `01M78K2G…`): pin charter `17ce3f9` (main tip, no release
  exists); replace the core-seeded glossary sentence with the governing-preset wording and track it with core.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Every pack registers against slice B (Priority: P1)

**Acceptance Scenarios**:

1. **Given** `charter.lock.yaml` at `17ce3f9`, **When** `charter_service_check.py` runs over `packs/` and the fixtures,
   **Then** composition answers 200, all 19 packs register, and no registration is refused with `retired`,
   `unreadable` or `pack_unreadable`.
2. **Given** a pack's root `README.md`, **When** the pack is uploaded, **Then** the README is in the archive (it is
   the pack document) and is not left out.

### User Story 2 - A reader finds a pack's documentation in one file (Priority: P1)

**Acceptance Scenarios**:

1. **Given** any pack, **When** a reader opens its root, **Then** there is one `README.md`, with exactly one H1, ATX
   headings only, and no `pack.md` or `PROVENANCE.md` in any letter case.
2. **Given** a pack that had a `PROVENANCE.md`, **When** a reader opens its README, **Then** a `## Provenance` section
   holds that content, with the file's H2s demoted to H3s, and no link to the deleted file.
3. **Given** any README, **When** a reader looks for Level, `pack_id` or Depends-on facts, **Then** none is restated as
   a descriptor bullet: the service serves them from `pack.yaml`.
4. **Given** the generated pack reference, **When** it is regenerated, **Then** each page's Purpose comes from the
   README preamble.

### User Story 3 - An org enforces its floor with a governing preset (Priority: P1)

**Acceptance Scenarios**:

1. **Given** `internal`, **When** a project's closure holds it, **Then** `presets/base.yaml` lists the 18 required ids
   (3 directives including the two already there, 7 procedures, 1 glossary pack, 2 toolguides, 5 skills), each with
   `must_have: true`.
2. **Given** any pack or fixture, **When** it is listed, **Then** it holds no `org-charter.yaml` and its `pack.yaml`
   declares no `active_charter`.
3. **Given** the docs, **When** a reader looks for how an org makes artifacts mandatory, **Then** they are pointed at
   a governing preset and `policy.yaml` (the charter's `enforce-org-presets` guide), never at `org-charter.yaml`,
   `required_<kind>` lists or `skill_namespace`.

### Edge Cases

- A copied `# Provenance` H1, a setext heading, a closing `#` sequence, a CR or BOM, or an unclosed fence makes the
  README unreadable to the charter's Markdown model. The merge must not introduce one.
- `cave-kitty`'s `# Voice only, …` lines sit inside a fenced block and stay.
- `built-in` has no README: `pack.md` is renamed, and "This file" now means the README.
- `go` and `rust` keep the first `pack.md` paragraph as the README's opening, since it is the generated Purpose.
- ADRs and `CHANGELOG.md` keep their history; they are not rewritten.
- Spec Kitty core still reads `org-charter.yaml`; after this change core no longer sees `internal`'s lists until it
  aligns with the charter (recorded, not fixed here: AGENTS.md alignment rule).

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Pin slice B | As CI, I want `charter.lock.yaml` to pin charter `17ce3f9` with empty `release_tag` and `jar_sha256`, so that the checks run against slice B. | High | Open | [build] | no — the pin value changes and the service check builds that commit |
| FR-002 | One README per pack | As a reader, I want each of the 19 packs to hold one root `README.md` that merges `pack.md` per #241's per-pack steps, so that the pack has one document. | High | Open | [build] | no — a file census finds 19 `pack.md` today |
| FR-003 | Provenance folded | As a reader, I want each of the 16 `PROVENANCE.md` bodies under a `## Provenance` H2 with headings demoted one level, and the file deleted, so that provenance survives in the document. | High | Open | [build] | no — 16 files exist today |
| FR-004 | Descriptor facts dropped | As a maintainer, I want no README bullet to restate Level, `pack_id` or Depends-on, so that `pack.yaml` is the single authority. | Medium | Open | [build] | no — nine READMEs carry the bullets today |
| FR-005 | Markdown model safe | As CI, I want every README to have exactly one H1, ATX headings, no closing `#` on H1/H2, no CR/BOM and no open fence, so that the service reads it. | High | Open | [ratchet] | yes — paired with the registration run on the same tree (FR-012), which refuses an unreadable README |
| FR-006 | internal's floor | As an org, I want `internal`'s 18 required ids as `must_have: true` items of `presets/base.yaml`, so that the floor is enforced by the service. | High | Open | [build] | no — 16 of the 18 ids are absent from the preset today |
| FR-007 | Org charters retired | As CI, I want no `org-charter.yaml` in any pack or fixture and no `active_charter` in any `pack.yaml`, so that no pack is `retired` or `pack_unreadable`. | High | Open | [build] | no — 12 packs and one fixture carry it today |
| FR-008 | Scripts follow | As CI, I want `NOT_REGISTERED` to drop `README.md`, `PROVENANCE.md` and `org-charter.yaml`; `validate_pack_schemas.py` to key on `README.md` and drop the `PROVENANCE.md` allowance; `check_vocabulary.py` to read `packs/qa/README.md`; and the reference generator to read the README preamble; each with updated tests. | High | Open | [build] | no — each test asserts the new value |
| FR-009 | Generated pages | As a reader, I want `docs/packs/*.md` regenerated so that `gen_pack_reference.py --check` passes. | Medium | Open | [build] | no — the check fails on drift |
| FR-010 | Live docs corrected | As a reader, I want no file outside ADRs and the changelog to present `pack.md`, `PROVENANCE.md`, `org-charter.yaml`, `active_charter`, `required_<kind>` lists or `skill_namespace` as live, per both issues' lists. | Medium | Open | [build] | no — a repository grep finds them today |
| FR-011 | Glossary wording | As core's glossary consumer, I want the "Charter Pack" definition to say an org pack enforces activations through a governing preset whose items carry `must_have: true`, so that the seed is not stale. | Low | Open | [build] | no — the old sentence is present |
| FR-012 | Registration proof | As the charter's drift watch, I want the service check at the pin to register every pack, so that charter #509 can close. | High | Open | [build] | no — it fails at the old content |
| FR-013 | Digests restamped | As release, I want every `packs/<pack>.source.yaml` digest restamped so that `check-pack-digests.sh` passes. | High | Open | [ratchet] | no — the edits change every touched pack's tree |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Gates green | `check-pack-digests.sh`, `validate_pack_schemas.py`, `check_vocabulary.py`, `gen_pack_reference.py --check` and the pytest suite exit 0 (0 failures). | Reliability | High | Open |
| NFR-002 | Registration count | The service check reports 19 of 19 packs registered and every invalid fixture refused with its expected code. | Reliability | High | Open |
| NFR-003 | No content loss | 100% of `PROVENANCE.md` text and of `pack.md` H2 sections other than "Contents" is present in the READMEs after the merge. | Reliability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Charter alignment | The repo aligns to the charter, not to core: core's reading of `org-charter.yaml` does not block the change. | Business | High | Open |
| C-002 | History kept | ADRs and `CHANGELOG.md` entries already written are not rewritten. | Technical | High | Open |
| C-003 | No private packs | The work touches only the public packs in this repository. | Business | High | Open |
| C-004 | Generated pages | `docs/packs/*.md` are regenerated, never hand-edited. | Technical | High | Open |
| C-005 | Optional policy | No `policy.yaml` is added to `internal`: none of its lists meant "must not change" (#242 step 2). | Technical | Medium | Open |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0 files named `pack.md`, `PROVENANCE.md` or `org-charter.yaml` (any case) under `packs/` and the fixtures, and 0 `active_charter` keys. — [build] · no-op passable: no
- **SC-002**: 19 of 19 packs register against charter `17ce3f9`. — [build] · no-op passable: no
- **SC-003**: The four named gates and the test suite pass. — [ratchet] · no-op passable: no

## Assumptions

- Charter `17ce3f9` equals `1d244f3` plus docs and plan commits, so it behaves as the ruled tip.
- The core glossary mirror is filed as a core issue by the operator (this session cannot write to core).
