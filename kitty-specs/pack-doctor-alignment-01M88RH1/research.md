# Research: Align open-packs to charter main with pack-doctor

All measurements were taken on 2026-11-25:
- open-packs `main` `a7243e2`;
- charter `main` `4b95b9151` (spec-kitty-charter PR #647, merged as `64a3f9539`, plus one docs commit);
- pack-doctor built from that commit with `./gradlew :pack-doctor:packDoctorJar`, giving `pack-doctor-0.1.0-SNAPSHOT.jar`.

## R1. The pin: a charter `main` commit, on demand

- **Decision:** `charter.lock.yaml` pins charter `main` HEAD at implement time, as a commit with `release_tag`,
  `jar_sha256` and `pack_doctor_sha256` empty.
- **Rationale:** the operator ruling of 2026-11-25 says to align to the latest charter now. The pin policy of
  2026-11-18 allows a main pin on demand. No `service-v*` release carries pack-doctor yet (ruling R-w).
- **Consequences:**
  - The gate builds both jars from source, which needs Java 25 and Gradle network access. The existing main-pin
    path already does this.
  - The release track never replaces a lock without `release_tag`.
  - #345's "pins `service-v<version>`" is deferred to the first release after this mission.
- **Alternatives considered:** waiting for the release. The operator ruled it out.

## R2. The checker's surface (#345 items 1-6, #349)

- **Release asset:** `pack-doctor-<version>.jar`, with `.sha256`, listed in `SHA256SUMS`.
- **Main build:** `:pack-doctor:packDoctorJar`, writing `service/pack-doctor/build/pack-doctor/pack-doctor-*.jar`.
  Measured: one jar.
- **Command line:**
  - `validate (--config-root <dir> | --pack <dir>[:<level>][=<id>] ...) [--round-trip] [--full] [--report <file> [--format yaml|xml]]`
  - `remediate <dir>...`
  - The flat form exits 2.
- **Report:** `PackDoctorReport`. The top level is `tool`, `inputs`, `checks`, `packs`, `skipped?`, `problems` and
  `summary`. `checks` is a subset of `[PACK, CLOSURE, REFERENCES, ROUND_TRIP]`.
  - Measured `summary`: `{packs, violations, warnings, notices, exit_code}`.
- **Warnings:** `warning: <pack>: <code> <file>: <detail>` on standard error. The only one measured is `file_not_held`,
  19 times.
- **Decision:** the gate passes `--report <file>` outside `packs/` (under the gate's report directory). That file is the
  uploaded artifact (#349 allows it). The gate still parses standard output.

## R3. What refuses the tree today

The run is `validate --round-trip --full` over the 19 packs:

- exit 1, 144 violations;
- `artifact_schema_error`: 61 (inline `anti_patterns`);
- `drg_schema_error`: 15 (file-less nodes);
- `substep_delegation_unresolved`: 3;
- `round_trip_red`: 40 and `round_trip_written_unpaired`: 25.

`round_trip_red` and `round_trip_written_unpaired` are all knock-ons:
- the manifest lists a refused constituent;
- a mission type is refused because its substep delegate is refused.

`CLOSURE` and `REFERENCES` are skipped. So preset, reference and closure faults (#346, #348) are **unmeasured** until
the curation lands. The plan re-measures after every curation work package.

## R4. Anti-pattern target shape

- **Schema:** `contracts/packs/schemas/anti-pattern.schema.json`. It is closed. It requires `schema_version` (`1.0`),
  `id` (kebab-case, ≤64 characters, equal to the stem), `title`, `description`, `severity` and `bad_example`.
  `good_example` is optional. `severity` is one of `smell`, `severe` or `breaking`:
  - `smell`: worth a remark;
  - `severe`: should block review;
  - `breaking`: must block.
- **Placement:** `anti_patterns/<id>.anti-pattern.yaml` in the pack.
- **Graph:**
  - a node: `urn: anti_pattern:<id>`, `kind: anti_pattern`, `label: <title>`;
  - an edge: `source: <owner urn>`, `target: anti_pattern:<id>`, `relation: rejects`, `reason: …`.
- **Charter's own example** (`service/packs/src/testFixtures/resources/example-packs/built-in`): the
  `adversarial-squad-deployment` entries became files.
  - Their nodes and `rejects` edges sit in `procedure.graph.yaml`.
  - Their severities (for example `averaging-divergent-verdicts: severe`) are **precedent** for open-packs'
    `foundation` copies of the same entries. The ledger cites them.
- **Graph layouts here:**
  - `drg/fragment.yaml`, with `id`/`kind: <plural>`/`title` nodes: 17 packs.
  - Per-kind `*.graph.yaml`, with `urn`/`kind`/`label` nodes: `foundation`, `writing`.
  - The curation tool writes the layout the pack already uses. For `drg/fragment.yaml` nodes it uses the kind spelling
    already accepted for `anti_patterns` nodes there (architecture and refactoring).

## R5. The curation is a ledger-driven, mechanical apply

- **Decision:** curation judgement lives in one ledger per pack:
  `kitty-specs/pack-doctor-alignment-01M88RH1/curation/<pack>.ledger.yaml`.
  - The ledger holds one row per source entry or file-less node.
  - A mission-local tool (`curation/apply_curation.py`) applies the ledgers:
    1. it writes the files;
    2. it adds the nodes and edges;
    3. it deletes the inline blocks.
  - The tool's `--check` mode proves:
    - every file has exactly one ledger row;
    - every row's text equals its file;
    - no inline block remains;
    - every row has a non-empty `severity_grounding` and `bad_example_source`.
- **Rationale:**
  - Reviewers judge about 270 calls as data, not as edits scattered over 61 files.
  - The apply is deterministic and repeatable.
  - NFR-002 is checkable.
- **Alternatives considered:** hand-editing each file. That gives no single review surface, and a call missed by
  review is invisible.

## R6. Dedupe, severity, bad example: operator calls (pending)

The decisions are deferred to the operator:

- `01M88RHDGQSS6R5R5ZCDCH84A2`
- `01M88RHFTS2X5HK1ZNP74G3WZ7`
- `01M88RHJ9HN4N8HDE97SJ6ZBAH`

Measured facts for the operator:

- **Distinct titles:** 270 of 273 entries.
  - The 3 exact duplicates are all within `internal`: `crud-affordance-echo`, `command-named-steps`, `defect-framing`.
  - The near-pairs are `float-money`/`float64-money`, `over-broad-uncheckable-scenario(s)`,
    `shared-mutable-state-between-scenarios`/`-tests`, `meta-tracker-as-canonical-parent`/`-functional-parent`,
    `child-ticket-checklist-in-the-epic-body`/`child-ticket-list-in-the-epic-body`, and
    `treating-a-static-flag-as-a-verdict`/`treating-triage-as-a-verdict`.
  - "About 150" (the #350 estimate) would need merging by meaning across packs.
- **Severity:** no entry states one.
- **Bad examples:** 131 entries (`title`/`content`) have none. Their `content` usually narrates a concrete instance.

The plan supports either dedupe answer: a merge is a ledger row with `merged_into`. The curation work packages wait on
these decisions. The tooling work package does not.

## R7. Remediate (#347)

- `remediate <dir>...` stamps the manifests and rewrites modelled files in canonical form, then validates with
  `--round-trip`.
  - It refuses, writing nothing, a pack with a fault it does not repair. So it runs **after** the curation.
  - It must run from the repository root.
- **Decision:** run it once over `packs/*` and `tests/fixtures/valid/*`.
  - The canonicalisation diff gets a commit of its own.
  - A YAML-load equality check over every rewritten file proves NFR-003.
  - `charter_pin.py rederive` calls the jar's `remediate`, using the jar from `charter_pack_doctor_jar.sh`.

## R8. Python rules (#348, #346)

Retire:

- `cross_pack_violations`'s preset rows;
- `stale_manifest_fields`;
- `derived_manifest`, `derive_manifest`, `membership_mismatch` and `regenerate_manifest`;
- `profile_reference_violations`'s charter-judged parts;
- `prompt_fragment_composition_violations`'s target-step parts;
- the old anti-pattern model (`MANIFEST_EXEMPT_NODE_KINDS` minus `anti_pattern`, node-held `anti_pattern` in
  `held_artifacts`).

Keep, each with a ruling comment:

- the id re-declared at another level (ADR-0053 decision 6);
- the unheld bare DRG endpoint (DIV-007);
- the undeclared prompt slot (C38);
- the `specializes_from` cycle (ruling R-s remainder, charter #636);
- the two non-charter parts of `profile_reference_violations` (`research/rule-coverage.md` row 6). These are kept as
  house rules, which is the conservative choice: they refuse nothing today, and dropping them is a later call.

The #348 line numbers drifted (the file now has 1 762 lines), so the work package locates each rule by name, not by
line.

## R9. Sequencing with PR #344

PR #344 is open and ready. It touches `charter_pin.py`, `charter-track.yml`, `validate-packs.yml` and their tests, which
are the same surfaces as WP01's rename.

- **Decision:** the planning artifacts are written now. WP01's implementation starts on `main` after #344 merges, or on
  the dispatcher's ruling.
- The curation work packages touch only `packs/`, and could start earlier on the dispatcher's word.
