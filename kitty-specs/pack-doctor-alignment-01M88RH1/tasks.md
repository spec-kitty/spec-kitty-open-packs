# Work Packages: Align open-packs to charter main with pack-doctor

**Mission**: `pack-doctor-alignment-01M88RH1` · **Planning base**: `feat/pack-doctor-alignment` · **Merge target**: `feat/pack-doctor-alignment`
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md), [occurrence_map.yaml](occurrence_map.yaml)

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Pin charter `main` HEAD and rename the lock key to `pack_doctor_sha256` (lock, `charter_lock.py`) | WP01 | |
| T002 | Rename the jar script to `charter_pack_doctor_jar.sh`; release asset `pack-doctor-<v>.jar`; main build `:pack-doctor:packDoctorJar` | WP01 | |
| T003 | `charter_pin.py`: key, flag, jar name, changelog line; `rederive` runs the jar's `remediate` | WP01 | |
| T004 | Rename the gate to `charter_pack_doctor.py`; `validate … --round-trip --full`; `--report` file | WP01 | |
| T005 | Parse `PackDoctorReport`: keys, `REFERENCES`, `summary.exit_code` agreement | WP01 | |
| T006 | Retire the rc.3 crash branch; migrate the invalid fixtures' expectation lines to `pack-doctor:` (#343) | WP01 | |
| T007 | Workflows: inputs, env, step names, `charter-pack-doctor-report` artifact | WP01 | |
| T008 | Tests for T001-T007, including a real-jar run | WP01 | |
| T009 | `curation/apply_curation.py`: apply ledgers (files, nodes, edges, inline-block removal) for both graph layouts | WP02 | |
| T010 | `--check` mode: one row per file, text equality, no inline block, grounding non-empty, no open operator question | WP02 | |
| T011 | `curation/README.md`: the ledger contract and the authoring rules (rubric per the operator's decision) | WP02 | |
| T012 | `ledger-00-nodes.yaml`: the 15 file-less nodes, grounded in their `rejects` reasons and tactics | WP02 | |
| T013 | Dry run on a scratch copy: pack-doctor's `drg_schema_error` count drops by 15 | WP02 | |
| T014 | Merge map: all 273 entries → clusters by meaning, home pack, id; homing and meaning questions (Q1) | WP03 | |
| T015 | Ledger A rows: foundation | WP03 | [P] |
| T016 | Ledger A rows: members merged into a foundation home from downstream packs | WP03 | [P] |
| T017 | Ledger A: severity groundings (Q2), bad examples (Q3), merges, operator questions | WP03 | |
| T018 | Ledger A dry run and `--check` | WP03 | |
| T019 | Ledger B rows: testing | WP04 | [P] |
| T020 | Ledger B rows: writing (incl. `ai-writing-tells`) | WP04 | [P] |
| T021 | Ledger B rows: members merged into a testing or writing home from downstream packs | WP04 | [P] |
| T022 | Ledger B: groundings, bad examples, merges, operator questions | WP04 | |
| T023 | Ledger B dry run and `--check` | WP04 | |
| T024 | Ledger C rows: architecture, event-driven | WP05 | [P] |
| T025 | Ledger C rows: pack-authoring | WP05 | [P] |
| T026 | Ledger C rows: planning-analysis, and members merged in from qa and internal | WP05 | [P] |
| T027 | Ledger C: groundings, bad examples, merges, operator questions | WP05 | |
| T028 | Ledger C dry run and `--check` | WP05 | |
| T029 | Ledger D rows: go, java, python, rust | WP06 | [P] |
| T030 | Ledger D rows: javascript | WP06 | [P] |
| T031 | Ledger D rows: drupal | WP06 | [P] |
| T032 | Ledger D: groundings, bad examples, merges, operator questions | WP06 | |
| T033 | Ledger D dry run and `--check` | WP06 | |
| T034 | Ledger E rows: internal procedures | WP07 | [P] |
| T035 | Ledger E rows: internal styleguides, with the `feature-and-scenario-authoring` duplicates | WP07 | [P] |
| T036 | Ledger E rows: qa | WP07 | [P] |
| T037 | Ledger E: groundings, bad examples, merges, operator questions | WP07 | |
| T038 | Ledger E dry run and `--check` | WP07 | |
| T039 | Apply ledger 00 to `packs/` | WP08 | |
| T040 | Apply ledgers A-E to `packs/` | WP08 | |
| T041 | `apply_curation.py --check` over the tree | WP08 | |
| T042 | Measure: `validate --full` runs CLOSURE and REFERENCES; record every remaining code | WP08 | |
| T043 | Fix or raise each remaining fault | WP08 | |
| T044 | Run `pack-doctor remediate` over `packs/*` and `tests/fixtures/valid/*`; commit the manifests | WP09 | |
| T045 | Commit the canonicalisation diff on its own, with a YAML-load equality proof | WP09 | |
| T046 | Second `remediate` run: every pack `unchanged` | WP09 | |
| T047 | `gen_pack_reference.py` lists `anti_patterns`; regenerate `docs/packs/*.md` | WP09 | |
| T048 | Update the pack digests (`pack_digest.py --update`) | WP09 | |
| T049 | Closing measurement: gate exits 0; the charter service check is green at the pin | WP09 | |
| T050 | Schema pass: anti-pattern file is a constituent; retire node-held `anti_pattern` | WP10 | |
| T051 | Retire the preset rules of `cross_pack_violations` (#346) | WP10 | [P] |
| T052 | Retire `stale_manifest_fields`, the derivation, `membership_mismatch`, `regenerate_manifest`, `--derived-manifests` | WP10 | [P] |
| T053 | Retire the charter-judged parts of `profile_reference_violations` and `prompt_fragment_composition_violations` | WP10 | [P] |
| T054 | House rules: a ruling comment on each, and a test that fails without it | WP10 | |
| T055 | `--cross-pack` help, `validate-packs.sh` header and arguments state the split | WP10 | |
| T056 | Tests: remove the retired rules' tests; full `tests/ci` green | WP10 | |
| T057 | `validate-a-pack.md`: pack-doctor, the command line, the coverage table, the split, the main pin | WP11 | |
| T058 | `docs/artefacts/index.md`: the anti-pattern file kind | WP11 | [P] |
| T059 | `docs/plans/roadmap.md` "Waits on" and the live-surface grep for pack-check | WP11 | [P] |
| T060 | Changelog entry | WP11 | |
| T061 | Docs gates: freshness, links, terminology, vocabulary | WP11 | |

## Phase 1: The gate (setup)

### WP01: The pack-doctor gate at a charter-main pin

- **Prompt**: [tasks/WP01-pack-doctor-gate.md](tasks/WP01-pack-doctor-gate.md)
- **Goal**: the gate obtains pack-doctor for the pinned `main` commit, runs `validate … --round-trip --full`, and judges the `PackDoctorReport` fail-closed. One name per tool. The #343 fixture lags are cleared.
- **Priority**: P1. **Independent test**: `charter_pack_doctor.py --jar <built jar>` runs. The report parses with no unknown-key failure. Both migrated fixtures match. The set run fails only on the known curation faults.
- **Depends on**: none. **Starts after PR #344 merges** (C-001).
- **Subtasks**:

T001 Pin charter `main` HEAD and rename the lock key (WP01)
T002 Rename and retarget the jar script (WP01)
T003 `charter_pin.py` follows, with `rederive` via `remediate` (WP01)
T004 Rename the gate; the `validate` command line and `--report` (WP01)
T005 Parse `PackDoctorReport` (WP01)
T006 Retire the crash branch; migrate the fixture expectations (WP01)
T007 Workflows follow (WP01)
T008 Tests (WP01)

- **Risks**:
  - Overlap with #344. Rebase after it merges.
  - The set run stays red until WP08 and WP09. Reviews judge the parser and the command line, not a green set.

## Phase 2: Curation (foundational, then batches)

### WP02: Curation tool, ledger contract, and the 15 file-less nodes

- **Prompt**: [tasks/WP02-curation-tool-and-nodes.md](tasks/WP02-curation-tool-and-nodes.md)
- **Goal**: a deterministic, checkable apply of per-batch ledgers, piloted on the 15 file-less nodes.
- **Priority**: P1. **Independent test**: the dry run over a scratch copy clears exactly the 15 `drg_schema_error`, and `--check` passes.
- **Depends on**: none. The severity calls follow decision `01M88RHFTS2X5HK1ZNP74G3WZ7`.
- **Subtasks**:

T009 `apply_curation.py`, both graph layouts (WP02)
T010 `--check` mode (WP02)
T011 Ledger contract and authoring rules (WP02)
T012 Ledger 00 for the file-less nodes (WP02)
T013 Dry run and measurement (WP02)

### WP03: Merge map, and ledger A: homes in foundation (23 origin entries)

- **Prompt**: [tasks/WP03-merge-map-and-ledger-a-foundation.md](tasks/WP03-merge-map-and-ledger-a-foundation.md). **Depends on**: WP02.
- **Goal**: one merge map for all 273 entries (decision Q1), then the rows homed in `foundation`. Every later ledger reads its rows from the map.

T014 merge map (WP03)
T015 foundation (WP03)
T016 members merged into foundation homes (WP03)
T017 groundings, bad examples, merges, questions (WP03)
T018 dry run and check (WP03)

### WP04: Ledger B: homes in testing and writing (77 origin entries)

- **Prompt**: [tasks/WP04-ledger-b-testing-writing.md](tasks/WP04-ledger-b-testing-writing.md). **Depends on**: WP03.

T019 testing (WP04)
T020 writing (WP04)
T021 members merged into testing and writing homes (WP04)
T022 groundings, bad examples, merges, questions (WP04)
T023 dry run and check (WP04)

### WP05: Ledger C: homes in architecture, pack-authoring, planning-analysis and event-driven (42 origin entries)

- **Prompt**: [tasks/WP05-ledger-c-architecture-planning.md](tasks/WP05-ledger-c-architecture-planning.md). **Depends on**: WP04.

T024 architecture, event-driven (WP05)
T025 pack-authoring (WP05)
T026 planning-analysis, with members from qa and internal (WP05)
T027 groundings, bad examples, merges, questions (WP05)
T028 dry run and check (WP05)

### WP06: Ledger D: homes in the language stacks (59 origin entries)

- **Prompt**: [tasks/WP06-ledger-d-language-stacks.md](tasks/WP06-ledger-d-language-stacks.md). **Depends on**: WP04.

T029 go, java, python, rust (WP06)
T030 javascript (WP06)
T031 drupal (WP06)
T032 groundings, bad examples, merges, questions (WP06)
T033 dry run and check (WP06)

### WP07: Ledger E: homes in qa and internal (72 origin entries)

- **Prompt**: [tasks/WP07-ledger-e-internal-qa.md](tasks/WP07-ledger-e-internal-qa.md). **Depends on**: WP05.

T034 internal procedures (WP07)
T035 internal styleguides and the duplicates (WP07)
T036 qa (WP07)
T037 groundings, bad examples, merges, questions (WP07)
T038 dry run and check (WP07)

**Batch order** (decision Q1): the ledgers follow the home-pack order of the pack `depends_on` graph, so a home file exists before any dependent pack's `rejects` edge: WP03 → WP04 → {WP05, WP06}; WP07 after WP05. Origin counts are before merging; the merge map sets the final row counts. **Parallel opportunities**: WP05 and WP06 run in parallel; WP01 is independent of all ledger WPs.

## Phase 3: Content and derived artifacts

### WP08: Apply the curation to `packs/`

- **Prompt**: [tasks/WP08-apply-curation.md](tasks/WP08-apply-curation.md). **Depends on**: WP02, WP03, WP04, WP05, WP06, WP07.

T039 apply ledger 00 (WP08)
T040 apply ledgers A-E (WP08)
T041 `--check` over the tree (WP08)
T042 measure CLOSURE and REFERENCES (WP08)
T043 fix or raise remaining faults (WP08)

### WP09: Restamp with `remediate`, and the derived artifacts

- **Prompt**: [tasks/WP09-remediate-and-derived.md](tasks/WP09-remediate-and-derived.md). **Depends on**: WP01, WP08.

T044 remediate and manifests (WP09)
T045 the canonicalisation commit and its equality proof (WP09)
T046 idempotence (WP09)
T047 pack reference pages (WP09)
T048 pack digests (WP09)
T049 closing measurement (WP09)

## Phase 4: Retirement and polish

### WP10: Retire the Python rules pack-doctor judges; keep the house rules

- **Prompt**: [tasks/WP10-retire-python-rules.md](tasks/WP10-retire-python-rules.md). **Depends on**: WP01, WP09.

T050 anti-pattern constituent (WP10)
T051 preset rules (WP10)
T052 manifest derivation and stale check (WP10)
T053 reference and fragment-target rules (WP10)
T054 house rules with rulings (WP10)
T055 help and the shell header (WP10)
T056 tests (WP10)

### WP11: Docs and changelog

- **Prompt**: [tasks/WP11-docs-and-changelog.md](tasks/WP11-docs-and-changelog.md). **Depends on**: WP10.

T057 validate-a-pack guide (WP11)
T058 artefacts index (WP11)
T059 roadmap and the live-surface grep (WP11)
T060 changelog (WP11)
T061 docs gates (WP11)

## MVP

WP01 is the MVP. It is the only work package that moves the gate. Everything else makes the gate green.
