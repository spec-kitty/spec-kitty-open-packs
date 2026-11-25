# Mission Specification: Align open-packs to charter main with pack-doctor

**Mission Branch**: `kitty/mission-pack-doctor-alignment-01M88RH1` (lands on `feat/pack-doctor-alignment`, then a clean PR branch from `main`)
**Created**: 2026-11-25
**Status**: Draft
**Input**: Dispatcher brief (2026-11-25). Operator ruling: "Open-Packs is to use the pack-doctor cli, and align to the latest version of charter." Issues #343, #345, #346, #347, #348, #349, #350. All except #343 are spec-kitty-charter PR #647's drafts (a) to (f).

## Intent Summary

- **Primary actor:** the open-packs maintainer who runs the pack gate, in a pull request, in the nightly charter-main track, or locally.
- **Trigger:** charter `main` renamed its standalone checker from pack-check to **pack-doctor**, with no alias. It gave the checker a `validate`/`remediate` command line, a `--full` check (`REFERENCES`) and a `PackDoctorReport`. It now refuses inline `anti_patterns`, file-less `anti_pattern` nodes and stale manifests on every surface. Because of this, the nightly main track has been red since 2026-11-22 (#343).
- **Desired outcome:** the gate runs pack-doctor built from charter `main`, which the lock pins on demand, as `validate --round-trip --full` over every pack. It exits 0. Every anti-pattern is its own file with a real `severity` and `bad_example`. Manifests are stamped by `pack-doctor remediate`. The Python copies of rules pack-doctor now judges are gone. The house rules stay, each naming its charter ruling.
- **Invariant:** the charter's answer is the rule (canonical model). Open-packs keeps a Python rule only where the charter, by ruling, does not judge (C-005, ADR-0083 decision 18).
- **Boundary:** alignment is to the charter, not core (AGENTS.md "Alignment"). Core compatibility is not a constraint.

### Baseline (measured 2026-11-25)

Pack-doctor built from charter `main` `4b95b9151`, over the 19 packs of open-packs `main` `a7243e2`, with `validate --round-trip --full`:

- The run exits 1, with 144 violations:
  - `artifact_schema_error`: 61 ("unknown key 'anti_patterns'", one per file).
  - `drg_schema_error`: 15 (file-less `anti_pattern` nodes: 6 in architecture, 7 in refactoring, 2 in foundation).
  - `substep_delegation_unresolved`: 3 (knock-ons).
  - `round_trip_red`: 40 and `round_trip_written_unpaired`: 25 (all knock-ons of the refused files).
- `CLOSURE` and `REFERENCES` are skipped for the whole set.
- The inline blocks hold **273 entries in 61 files**:
  - 142 entries use `name`/`description`/`bad_example`/`good_example`.
  - 131 use `title`/`content`, with no `bad_example`.
  - None carries a severity.
  - There are 270 distinct titles.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The gate runs pack-doctor at the charter-main pin (Priority: P1)

A maintainer opens a pull request. The gate obtains the pack-doctor jar for the pinned charter commit and runs `validate --round-trip --full` over every pack and valid fixture. It reads the report by the `PackDoctorReport` schema and fails closed on any problem.

**Why this priority**: without it, nothing else can be measured. The current gate builds a Gradle task that no longer exists.

**Independent Test**: run the gate's pack-doctor step locally against the pinned commit. It obtains `pack-doctor-*.jar`, invokes `validate`, and parses a report with `tool`, `inputs` and `summary` without an unknown-key failure.

**Acceptance Scenarios**:

1. **Given** a lock pinning a charter `main` commit with empty release fields, **When** the gate runs, **Then** it builds `:pack-doctor:packDoctorJar` at that commit and runs `java -jar <jar> validate --pack … --round-trip --full`.
2. **Given** a lock pinning a release, **When** the gate runs, **Then** it downloads `pack-doctor-<version>.jar` and refuses it unless its SHA-256 equals `pack_doctor_sha256`.
3. **Given** a report whose `summary.exit_code` disagrees with the process exit code, **When** the gate parses it, **Then** the gate fails closed.
4. **Given** a report with `REFERENCES` in `skipped`, **When** the gate runs with `--full`, **Then** the gate fails closed and names the reason.

---

### User Story 2 - Every anti-pattern is its own file, rejected by its guidance (Priority: P1)

A pack author reads a styleguide or procedure. Its anti-patterns are no longer an inline block. Each one is an `anti_patterns/<id>.anti-pattern.yaml` file in the same pack, with a severity that says how much it weighs in review and a concrete bad example. The guidance rejects it through a `rejects` edge.

**Why this priority**: 15 packs cannot be read until this lands, so `CLOSURE` and `REFERENCES` cannot run at all.

**Independent Test**: `pack-doctor validate --full` over the set reports no `artifact_schema_error` for `anti_patterns` and no `drg_schema_error` for a file-less node, and runs both `CLOSURE` and `REFERENCES`.

**Acceptance Scenarios**:

1. **Given** a styleguide that carried N inline entries, **When** the curation lands, **Then** the styleguide has no `anti_patterns` key, its pack holds N files (fewer only where a same-practice duplicate merged), and its graph has one `rejects` edge per file from the styleguide.
2. **Given** a file-less `anti_pattern` node, **When** the curation lands, **Then** the same pack holds its file and the existing `rejects` edge resolves.
3. **Given** any anti-pattern file, **Then** its `severity` and `bad_example` trace to a grounding line in the curation ledger, and neither is a default.

---

### User Story 3 - Manifests are stamped by the charter's own writer (Priority: P2)

After the curation, the maintainer runs `pack-doctor remediate` over every pack. Each manifest gets the charter's derivation, and each modelled file is rewritten in canonical form. That canonicalisation diff is reviewed on its own, for unchanged meaning. `charter_pin.py` re-derives with `remediate` too.

**Independent Test**: `validate` reports no `manifest_stale` or `manifest_membership`. A second `remediate` run reports every pack `unchanged`.

**Acceptance Scenarios**:

1. **Given** the curated tree, **When** `remediate` runs, **Then** each pack's outcome is `rewritten` or `unchanged`, and the follow-up `validate --round-trip` exits 0.
2. **Given** the remediated tree, **When** `remediate` runs again, **Then** every pack is `unchanged`.

---

### User Story 4 - Python rules the charter now judges are retired (Priority: P2)

A maintainer reading `validate_pack_schemas.py` finds no Python copy of a rule pack-doctor judges. Each house rule that remains carries a comment naming the charter ruling that leaves it to open-packs.

**Independent Test**: the rows under "Retire" in #348 are gone with their tests, and each kept house rule has a ruling comment and still has a test that fails without it.

**Acceptance Scenarios**:

1. **Given** a preset `must_have` item no pack of the closure holds, **When** the gate runs, **Then** the failure comes from pack-doctor (`preset_item_not_held`), not from Python.
2. **Given** a bare DRG edge endpoint no pack declares, **When** the gate runs, **Then** the Python house rule still refuses it (DIV-007).

---

### User Story 5 - Fixture expectations follow the charter (Priority: P3)

The invalid fixtures `case-variant-readme` and `malformed-pack-version` expect `case_variant` and `pack_version_invalid`. Nothing expects the rc.3 crash (`failed`).

**Independent Test**: the non-vacuity fixture check passes against the pinned jar, and the `failed` expectation kind is gone.

### Edge Cases

- **A charter merge on `main` moves pack-doctor mid-mission.** The lock pins a commit, never a branch. The pin is refreshed deliberately, and the commit is re-measured at implement time.
- **The release track at a main pin.** A lock with no `release_tag` is never replaced by that track (pin policy). The track must stay green or skip, not fail on the empty release fields.
- **`remediate` and the working directory.** A pack that holds the working directory is a usage fault (exit 2). Run it from the repository root.
- **The report file.** A `--report` file inside a checked pack is a usage fault (exit 2). Write it outside `packs/` and `tests/fixtures/`.
- **Duplicates across files of one pack.** The 3 exact `internal` duplicates and the near-pairs merge into one file only when their text names the same practice. Each former owner still gets its own `rejects` edge.
- **An id collision.** A derived id that collides with an existing node of another kind, or exceeds 64 characters, is shortened deterministically and recorded in the ledger.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Pin charter main on demand | As a maintainer, I want `charter.lock.yaml` to pin a charter `main` commit carrying pack-doctor, with `release_tag` and both digests empty, so that the gate checks against the latest charter now (operator ruling 2026-11-25). | High | Open | [build] | no — the lock commit changes from cb9b154 and the gate's jar step must build that commit |
| FR-002 | Rename the lock field | As a maintainer, I want the lock's `pack_check_sha256` renamed to `pack_doctor_sha256` in every file that carries it (`charter_lock.py`, `charter_pin.py`, both workflows, tests) in one change, so that one name per tool holds (#345 item 3). | High | Open | [build] | no — a test reading the old key must fail |
| FR-003 | Obtain the pack-doctor jar | As a maintainer, I want `charter_pack_doctor_jar.sh` (renamed from `charter_pack_check_jar.sh`) to download and verify `pack-doctor-<version>.jar` on a release pin and to build `:pack-doctor:packDoctorJar` on a main pin, so that the gate gets the checker for the pinned commit (#345 items 1-2). | High | Open | [build] | no — the old task name exits non-zero at the pin |
| FR-004 | Invoke `validate` with `--round-trip --full` | As a maintainer, I want `charter_pack_check.py`'s command builder to emit `validate --pack … --round-trip --full`, so that the gate runs `REFERENCES` and the flat form (exit 2) is never sent (#345 item 4, #348). | High | Open | [build] | no — the flat form exits 2 against the pinned jar |
| FR-005 | Parse the `PackDoctorReport` | As a maintainer, I want the gate to accept exactly the schema's top-level keys (`tool`, `inputs`, `checks`, `packs`, `skipped`, `problems`, `summary`), to require `REFERENCES` among `checks`, and to fail closed when `summary.exit_code` disagrees with the process exit code, so that the report is read by its contract (#349, #345 item 6). | High | Open | [build] | no — today's `REPORT_KEYS` fails closed on `tool` |
| FR-006 | Retire the rc.3 crash branch | As a maintainer, I want `CRASH_ISSUE`, `FAILED`, `CRASH_SIGN`, the `failed` judge branch and the `failed` expectation removed, so that a pack's content is never treated as exit 2 (#345 item 5). | Medium | Open | [build] | no — the `malformed-pack-version` fixture must now expect `pack_version_invalid` |
| FR-007 | Anti-patterns as files | As a pack author, I want every inline `anti_patterns` entry moved to `anti_patterns/<id>.anti-pattern.yaml` in its owner's pack, with `schema_version`, `id` (the stem), `title`, `description`, `severity` and `bad_example`, and `good_example` where the author stated one, so that 15 packs become readable (#350). | High | Open | [build] | no — 61 `artifact_schema_error` at baseline |
| FR-008 | `rejects` edges from former owners | As a pack author, I want a graph node and a `rejects` edge from each former owner to each file (pack-qualified across packs, with the pack in `depends_on`), so that guidance still rejects what it named inline (#350 step 5). | High | Open | [build] | no — `REFERENCES` must resolve every new edge |
| FR-009 | Files for the file-less nodes | As a pack author, I want each of the 15 file-less `anti_pattern` nodes to get its file in the same pack, grounded in its `rejects` edge's `reason` and its rejecting tactic, so that no `drg_schema_error` remains (#350 step 4). | High | Open | [build] | no — 15 `drg_schema_error` at baseline |
| FR-010 | A curation ledger | As a reviewer, I want one ledger row per entry: its source file and index, its target id, a merge note if any, its severity with a one-line grounding, and the bad-example source, so that every judgement call is reviewable and none is defaulted (dispatcher brief). | High | Open | [build] | no — each file must have a ledger row; a check enforces it |
| FR-011 | Restamp with `remediate` | As a maintainer, I want every pack and valid fixture restamped with `pack-doctor remediate` after the curation, with the canonicalisation diff in its own commit, so that the manifests match the charter's own writer (#347). | High | Open | [build] | no — the curation adds constituents the old manifests lack |
| FR-012 | The pin re-derives with `remediate` | As a maintainer, I want `charter_pin.py`'s `rederive` to run the pinned jar's `remediate` over the packs in place of `validate_pack_schemas.py --derive-manifest`, so that the pin uses the charter's derivation (#347). | Medium | Open | [build] | no — a test asserts that the `remediate` invocation and its exit status are honoured |
| FR-013 | Preset items judged by the charter | As a maintainer, I want `validate --full` over every pack and valid fixture to report no `preset_item_*` problem, and the two Python preset rules retired, so that one answer holds (#346). | Medium | Open | [ratchet] | yes — paired with an invalid in-test pack that pack-doctor refuses with `preset_item_not_held` |
| FR-014 | Retire the Python rules pack-doctor judges | As a maintainer, I want the "Retire" rows of #348 removed, with their tests and help lines (`--cross-pack` help, `validate-packs.sh`), and the old anti-pattern model (`MANIFEST_EXEMPT_NODE_KINDS`, the `CONSTITUENT_KIND_BY_SCHEMA` note, node-held `anti_pattern` in `held_artifacts`) retired, so that Python cannot drift from the charter (#348). | Medium | Open | [build] | no — grep for the retired function names must come back empty |
| FR-015 | Keep the house rules, each with its ruling | As a maintainer, I want the house rules of #348 kept, each with a comment naming its charter ruling: the id re-declared at another level, the unheld bare DRG endpoint (DIV-007), the undeclared prompt-fragment slot (C38), the `specializes_from` cycle (R-s remainder, charter #636) and the two non-charter parts of `profile_reference_violations`. That way the split is explicit. | Medium | Open | [ratchet] | yes — each house rule keeps a test that fails without it |
| FR-016 | Fixture expectations | As a maintainer, I want `case-variant-readme` to expect `case_variant` and `malformed-pack-version` to expect `pack_version_invalid`, with the expectation key renamed `pack-doctor:`, so that #343's two fixture lags clear. | Medium | Open | [build] | no — the non-vacuity check fails with today's expectations against the pin |
| FR-017 | The Python schema pass reads anti-pattern files | As a maintainer, I want `validate_pack_schemas.py` (the "Charter Pack validation" job) to validate `anti_patterns/*.anti-pattern.yaml` against the pinned charter's `anti-pattern.schema.json` and to count the file as a manifest constituent, so that both gate jobs agree. | High | Open | [build] | no — the job is red at baseline on the same 61 files |
| FR-018 | The charter service validation passes at the pin | As a maintainer, I want the "Charter service validation" job (registration, composition, non-vacuity) green at the pinned commit, so that #343 can close. | High | Open | [ratchet] | no — it is red at baseline (13 packs refused, `/offering` 500) |
| FR-019 | No live surface names pack-check | As a reader, I want workflows (step names, inputs, the `charter-pack-doctor-report` artifact, env), scripts, tests and the guides (`validate-a-pack.md`, `docs/artefacts/index.md`) to name pack-doctor and describe the anti-pattern file model. Historical ADRs and changelog entries stay as written, and readers are pointed at charter `docs/guides/check-packs.md`. (#345 item 9, #350.) | Medium | Open | [build] | no — a grep over the live surfaces must return no `pack-check`/`pack_check` |
| FR-020 | Changelog | As a reader, I want one changelog entry describing the alignment, the main pin and the anti-pattern model, so that the change is announced (charter gate). | Low | Open | [build] | no |

[NEEDS CLARIFICATION: Dedupe scope. Merge only same-practice duplicates within a pack or an existing depends_on (~265 files), or merge by meaning to ~150 with new cross-pack depends_on.] <!-- decision_id: 01M88RHDGQSS6R5R5ZCDCH84A2 -->

[NEEDS CLARIFICATION: Severity rubric. Per-entry calls by the schema's definitions, each grounded in a ledger line, with ungroundable entries batched to the operator; or an operator-given rubric.] <!-- decision_id: 01M88RHFTS2X5HK1ZNP74G3WZ7 -->

[NEEDS CLARIFICATION: bad_example for the 131 title/content entries. The content's concrete-instance sentence verbatim, with no-instance entries batched to the operator.] <!-- decision_id: 01M88RHJ9HN4N8HDE97SJ6ZBAH -->

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | A clean gate | `pack-doctor validate --round-trip --full` over all 19 packs and the valid fixtures exits 0. It reports 0 violations, `checks` = `[PACK, CLOSURE, REFERENCES, ROUND_TRIP]` and an empty `skipped`. | Reliability | High | Open |
| NFR-002 | No defaulted curation | 100% of anti-pattern files carry a `severity` and a `bad_example` that each trace to a ledger row with a non-empty grounding. 0 rows have the grounding "default". | Quality | High | Open |
| NFR-003 | Meaning kept by `remediate` | In the canonicalisation commit, 0 files change parsed meaning: a YAML-load equality check over every rewritten file, against its pre-remediate form, reports 0 differences. | Quality | High | Open |
| NFR-004 | Idempotent restamp | A second `remediate` run over the restamped tree reports 100% of packs `unchanged`. | Reliability | Medium | Open |
| NFR-005 | Reviewable work packages | No curation work package covers more than about 70 entries, so each review fits one sitting. | Process | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Sequencing with #344 | Do not edit PR #344's branch. Implementation is based on `main` after #344 merges; if it has not merged at implementation start, ask the dispatcher. | Process | High | Open |
| C-002 | Main pin by ruling | Pin charter `main` on demand (pin policy, 2026-11-18; operator ruling, 2026-11-25). #345's "pins `service-v<version>`" is explicitly deferred to the first release after this mission. | Business | High | Open |
| C-003 | The charter's answer is the rule | Never reshape pack content to suit core. Never keep a Python copy of a rule pack-doctor judges. | Technical | High | Open |
| C-004 | Ungrounded calls go to the operator | A curation call that the existing text cannot ground is raised with the dispatcher as an operator question, never guessed. | Process | High | Open |
| C-005 | Independent review | Work packages are reviewed by reviewer sessions the dispatcher dispatches. The implementer never self-approves. | Process | High | Open |
| C-006 | Delivery hygiene | The draft PR comes from a new branch off `main`, with clean, signed history, no model names and a changelog entry. The operator merges. | Process | High | Open |
| C-007 | Live-runner cap | At most 6 live runners for this repository. This runner is one. | Process | Medium | Open |

### Key Entities

- **Anti-pattern file**: `anti_patterns/<id>.anti-pattern.yaml`, closed schema (`schema_version`, `id`, `title`, `description`, `severity` ∈ {smell, severe, breaking}, `bad_example`, optional `good_example`).
- **`rejects` edge**: from guidance (a styleguide, procedure or tactic) to `anti_pattern:<id>`, qualified `<pack>::anti_pattern:<id>` across packs.
- **Curation ledger**: one row per source entry and file-less node. It traces each source to its target file, a merge note, the severity with its grounding, and the bad-example source.
- **Charter lock**: `commit`, `release_tag`, `jar_sha256`, `pack_doctor_sha256`.
- **PackDoctorReport**: `tool`, `inputs`, `checks`, `packs`, `skipped?`, `problems`, `summary`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The nightly charter-main track run on the mission branch's head is green in all three jobs, so #343 can close. — [build] · no-op passable: no
- **SC-002**: The PR gate runs pack-doctor at the pinned commit with `--round-trip --full`, and its report holds 0 violations. — [build] · no-op passable: no
- **SC-003**: 0 styleguides or procedures carry `anti_patterns`, and 0 `anti_pattern` nodes lack a file. — [build] · no-op passable: no
- **SC-004**: Each of the issues #345 to #350 has every "Done when" item met, or explicitly deferred with a reason in the PR body. — [build] · no-op passable: no

## Assumptions

- Charter `main` keeps the pack-doctor contract that `4b95b9151` ships for the life of the mission. At implement time the pin moves to charter `main` HEAD, and the plan re-measures.
- A charter `main` merge that changes pack-doctor's verdicts after the pin is a new alignment, not this mission's scope.
- An anti-pattern's file lives in its former owner's pack (ADR-0052 decision 11), so no new `depends_on` is needed unless a merge crosses packs (pending the dedupe decision).
