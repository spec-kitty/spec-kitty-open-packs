---
work_package_id: WP01
title: The pack-doctor gate at a charter-main pin
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-004
- FR-005
- FR-006
- FR-012
- FR-016
- FR-019
- C-001
- C-002
planning_base_branch: feat/pack-doctor-alignment
merge_target_branch: feat/pack-doctor-alignment
branch_strategy: Planning artifacts for this mission were generated on feat/pack-doctor-alignment. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/pack-doctor-alignment unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
- T007
- T008
phase: Phase 1 - The gate
history:
- at: '2026-11-25T07:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/ci/
create_intent:
- scripts/ci/charter_pack_doctor_jar.sh
- scripts/ci/charter_pack_doctor.py
- tests/ci/test_charter_pack_doctor.py
execution_mode: code_change
model: ''
owned_files:
- charter.lock.yaml
- scripts/ci/charter_lock.py
- scripts/ci/charter_pin.py
- scripts/ci/charter_pack_check_jar.sh
- scripts/ci/charter_pack_doctor_jar.sh
- scripts/ci/charter_pack_check.py
- scripts/ci/charter_pack_doctor.py
- scripts/ci/charter_service_check.py
- scripts/ci/charter_release_asset.sh
- .github/workflows/validate-packs.yml
- .github/workflows/charter-track.yml
- tests/ci/test_charter_pin.py
- tests/ci/test_workflows.py
- tests/ci/test_charter_pack_check.py
- tests/ci/test_charter_pack_doctor.py
- tests/ci/test_charter_service_check.py
- tests/ci/test_pack_digest.py
- tests/fixtures/invalid/*/expected-code
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP01 - The pack-doctor gate at a charter-main pin

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, do what the skill does: run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `python-pedro`
- **Agent/tool**: `claude`

---

## IMPORTANT: Review Feedback

Check the `review_ref` field in the event log (`spec-kitty agent tasks status --mission pack-doctor-alignment-01M88RH1`). Address every feedback item, and record each fix with `spec-kitty agent tasks add-history WP01 --note "..."`.

---

## Objectives & Success Criteria

- `charter.lock.yaml` pins charter `main` HEAD, measured at implementation start, as a main pin: `release_tag`, `jar_sha256` and `pack_doctor_sha256` are all empty (FR-001, C-002).
- The lock key is `pack_doctor_sha256` everywhere. No reader of `pack_check_sha256` remains (FR-002).
- `scripts/ci/charter_pack_doctor_jar.sh` obtains `pack-doctor-<version>.jar` on a release pin, verified against `pack_doctor_sha256`. On a main pin it builds `:pack-doctor:packDoctorJar` and globs `service/pack-doctor/build/pack-doctor/pack-doctor-*.jar` (FR-003).
- `scripts/ci/charter_pack_doctor.py` runs `java -jar <jar> validate --pack … --round-trip --full --report <file>` and judges the `PackDoctorReport` fail-closed (FR-004, FR-005).
- The rc.3 crash branch is gone. `case-variant-readme` expects `case_variant`, `malformed-pack-version` expects `pack_version_invalid`, and every fixture's key is `pack-doctor:` (FR-006, FR-016).
- `charter_pin.py rederive` runs the pinned jar's `remediate` over the packs, not `validate_pack_schemas.py --derive-manifest` (FR-012).
- No live tooling surface in this WP names pack-check. The occurrence map's exceptions stay untouched (FR-019, tooling part).

**Done when**:
- `pytest tests/ci` passes. The one set-run expectation that the curation (WP08) must still clear is marked by a single named `xfail` that WP09 removes.
- A real run against the built jar shows:
  - both migrated fixtures matching;
  - the set refused only with the known codes (`artifact_schema_error`, `drg_schema_error`, `substep_delegation_unresolved`, and the round-trip knock-ons).

## Context & Constraints

- **Read first**: `kitty-specs/pack-doctor-alignment-01M88RH1/spec.md`, `plan.md` (IC-01), `research.md` (R1, R2), `data-model.md` (lock, report), `occurrence_map.yaml`, and issues #345, #349 and #343 in full. #345 gives exact file:line touchpoints, but those lines may have moved after #344, so find each by its name.
- **C-001**: base on `main` **after PR #344 merges**. #344 edits `charter_pin.py`, `charter-track.yml`, `validate-packs.yml` and their tests. Never edit #344's branch.
- **The bulk edit (DIRECTIVE_035)**: follow `occurrence_map.yaml`.
  - Do not touch `docs/changelog/**`, `docs/architecture/adr/**`, `kitty-specs/**` (other missions), `kitty-ops/**` or `site/**`.
  - `docs/guides/**` belongs to WP11. `validate_pack_schemas.py` and `validate-packs.sh` belong to WP10. Leave their pack-check mentions alone.
- **The charter is the authority**:
  - the command line: charter `service/pack-doctor/src/main/java/.../Arguments.java` usage (also `java -jar <jar> --help`);
  - the report: charter `contracts/charter/schemas/PackDoctorReport.yaml`;
  - the guide: charter `docs/guides/check-packs.md`.
- **Java 25** is on the runner. Set `LC_ALL=C.UTF-8` for pack-doctor runs (its usage says that a non-ASCII file name under POSIX is exit 2).

## Branch Strategy

- **Strategy**: computed by `finalize-tasks` (lanes in `lanes.json`)
- **Planning base branch**: `feat/pack-doctor-alignment`
- **Merge target branch**: `feat/pack-doctor-alignment`
- Implement with `spec-kitty agent action implement WP01 --agent <name> --mission pack-doctor-alignment-01M88RH1`. The worktree is allocated per lane.

## Subtasks & Detailed Guidance

### Subtask T001 - Pin charter `main` HEAD and rename the lock key

- **Purpose**: a main pin on demand, by the 2026-11-25 operator ruling.
- **Steps**:
  1. Resolve charter `main` HEAD with `git ls-remote https://github.com/spec-kitty/spec-kitty-charter.git refs/heads/main`. Record the 40-hex commit. At planning time it was `4b95b9151…`.
  2. In `charter.lock.yaml`:
     - set `commit`;
     - empty `release_tag`, `jar_sha256` and `pack_doctor_sha256`;
     - rename the key and rewrite the comments (see the issue #345 item 3 wording). "Releases before `service-v<next>` ship no pack-doctor" stays true. Keep the pin-policy paragraph, and add one line: "Pinned to charter `main` on demand by operator ruling, 2026-11-25 (#345)".
  3. In `scripts/ci/charter_lock.py`, update `KEYS` and the check that sets `release_tag` and both digests together, so they use the new key. Update the docstring and comments.
- **Validation**: `python3 scripts/ci/charter_lock.py pack_doctor_sha256` prints an empty line. A lock that still holds `pack_check_sha256` is refused as an unknown key, fail-closed, as today's unknown keys are.

### Subtask T002 - The jar script

- **Steps**: `git mv scripts/ci/charter_pack_check_jar.sh scripts/ci/charter_pack_doctor_jar.sh`, then:
  - the header comments name pack-doctor and #345;
  - `digest="$(lock pack_doctor_sha256)"`;
  - the release path: `jar="$work/pack-doctor-$version.jar"`, URL `…/releases/download/$tag/pack-doctor-$version.jar`, and `download_verified … pack_doctor_sha256`;
  - the main path: `./gradlew --console=plain --no-daemon :pack-doctor:packDoctorJar`;
  - the glob: `service/pack-doctor/build/pack-doctor/pack-doctor-*.jar`, with its error message.
  - Check `charter_release_asset.sh` for pack-check wording and update it.
- **Validation**: `bash -n`. A real run, `scripts/ci/charter_pack_doctor_jar.sh .charter-work`, prints one jar path.

### Subtask T003 - `charter_pin.py`

- **Steps**:
  - the usage/flag `--pack-doctor-sha256`;
  - `PACK_DOCTOR_JAR = "pack-doctor-{version}.jar"`;
  - `write_lock`'s parameter, check, values and key regex;
  - the changelog line ("pack-doctor `.sha256` assets");
  - `resolve-release` emits `pack_doctor_sha256=…`;
  - `resolve-ref` and `apply` follow.
  - **`rederive` (#347)**:
    - Replace the per-pack `validate_pack_schemas.py --derive-manifest <pack>` call with one run of `java -jar <jar> remediate <pack>...` over every pack under `packs/` and `tests/fixtures/valid/`, from the repository root, with `LC_ALL=C.UTF-8`.
    - Obtain the jar through `charter_pack_doctor_jar.sh` (both pins).
    - A non-zero exit fails the derive and prints its output.
    - Parse the per-pack outcome lines to report `rewritten` or `unchanged`.
- **Notes**: `remediate` writes through hidden siblings. Run it with the repository root as the working directory. A pack that holds the working directory is exit 2.
- **Validation**: `tests/ci/test_charter_pin.py` covers:
  - the new key, flag and jar name;
  - that `rederive` invokes `remediate` with every pack, using a fake `java` that records its argv;
  - that a failing `remediate` fails the derive.

### Subtask T004 - The gate: rename, command line, report file

- **Steps**:
  1. `git mv scripts/ci/charter_pack_check.py scripts/ci/charter_pack_doctor.py`.
  2. Rewrite the module docstring for pack-doctor:
     - the set runs with `--round-trip --full`;
     - what pack-doctor judges (point to charter `docs/guides/check-packs.md`);
     - what stays in the schema pass, namely the house rules (WP10 lists them).
     - Drop the rc.3 paragraphs.
  3. `command_for` returns `[java, "-jar", jar, "validate", *("--pack", p…), "--round-trip", "--full", "--report", <file>]`.
     - The report file lies outside every pack: under `--report-dir`, or a temporary directory.
     - Keep the argument checks (existing files, resolved absolute directories, no shell).
  4. `--report-dir` keeps each run's YAML report from `--report`, plus its stderr. The stdout JSON stays the parsed source.
  5. Rename every message prefix `pack-check:` to `pack-doctor:`.
- **Validation**: unit tests on `command_for`, plus the real-jar test.

### Subtask T005 - Parse `PackDoctorReport`

- **Steps**:
  - `REPORT_KEYS = ("tool", "inputs", "checks", "packs", "skipped", "problems", "summary")`.
  - `CHECKS = ("PACK", "CLOSURE", "REFERENCES", "ROUND_TRIP")`.
  - Require `tool.name == "pack-doctor"`.
  - Require `summary.exit_code == result.exit_code`. A mismatch fails closed with both values.
  - Require `inputs.options.full` and `inputs.options.round_trip` to be true.
  - Keep: the skipped-leads-first behaviour, the packs-equal-given-set check, and the warning rule (only `file_not_held` passes).
- **Validation**: tests feed reports built from the measured shape (see `research.md` R2) for:
  - a clean report, which passes;
  - an unknown key, a missing `REFERENCES`, a `skipped` REFERENCES, an `exit_code` mismatch, and a `tool.name` mismatch, which each fail.

### Subtask T006 - Retire the crash branch; migrate the expectations (#343)

- **Steps**:
  - Delete `CRASH_ISSUE`, `FAILED`, `CRASH_SIGN`, `_crash`'s rc.3 wording and the `failed` branch of `judge_invalid`.
  - Exit 2 stays a failure ("a usage or I/O failure; nothing was judged").
  - The expectation key becomes `pack-doctor:`, both in `charter_pack_doctor.py` (`expected_pack_doctor`) and in `charter_service_check.py` (its reads of `pack-check:`).
  - In all 5 `tests/fixtures/invalid/*/expected-code`:
    - rename the key;
    - `case-variant-readme`: `pack-doctor: case_variant`;
    - `malformed-pack-version`: `pack-doctor: pack_version_invalid`, and rewrite its comment that foresaw the change.
    - The other three keep their codes.
- **Validation**: the real-jar run over the 5 fixtures matches every expectation (issue #345 item 8 gives the measured codes).

### Subtask T007 - Workflows

- **Steps**:
  - `validate-packs.yml`:
    - the `workflow_call` input `charter_pack_doctor_sha256`;
    - the env and apply lines;
    - the step "Check every pack with the charter's pack-doctor";
    - `REPORT_DIR`;
    - the artifact `charter-pack-doctor-report`;
    - the `RealPackDoctor` test env (`PACK_DOCTOR_JAR`);
    - the script paths.
  - `charter-track.yml`: the output, the call input, env, apply, the summary, comments, and the artifact name in the issue-body text (`charter_track_report.sh` reads it, so check it).
  - Make sure the release track handles a lock with an empty `release_tag`. It must skip the bump comparison as today, never fail.
- **Validation**: `tests/ci/test_workflows.py`, updated for the names. `bash -n` on every `run:` script. If available, `actionlint`.

### Subtask T008 - Tests

- **Steps**:
  - `git mv tests/ci/test_charter_pack_check.py tests/ci/test_charter_pack_doctor.py`, then retarget its imports and names. Remove the crash-expectation tests, and add the T005 report tests.
  - Rename the real-jar class to `RealPackDoctor`. It skips without `PACK_DOCTOR_JAR`.
    - It asserts the 5 fixtures.
    - It asserts that the set run's report parses and that its only problem codes are the curation codes listed above. Mark that one assertion as the set's known-red `xfail(strict=True)`, with the reason "cleared by WP08/WP09", and WP09 removes it.
  - Update `test_charter_pin.py`, `test_charter_service_check.py`, `test_workflows.py` and `test_pack_digest.py` for the names.
- **Validation**: `python3 -m pytest tests/ci -q` passes. Run `PACK_DOCTOR_JAR=<jar> python3 -m pytest tests/ci/test_charter_pack_doctor.py -q` and paste its output into the WP history.

## Test Strategy

- `python3 -m pytest tests/ci -q`, plus the real-jar run above.
- `bash -n` on both jar scripts.
- `python3 -m py_compile` on the changed scripts.
- `grep -rn "pack.check\|pack_check\|packCheck" scripts/ci .github tests charter.lock.yaml` returns only `validate_pack_schemas.py`/`validate-packs.sh` (WP10's) and `test_validate_pack_schemas.py` (WP10's).

## Risks & Mitigations

- **#344's changes land under this WP.** Rebase, and re-locate each touchpoint by name.
- **The set run stays red until WP08 and WP09.** Use one strict `xfail` with a named owner, never a skip.
- **The main-pin build needs network access** to Gradle repositories in CI. It does so today on the main track.

## Review Guidance

- Check every touchpoint of #345 items 1-6 and 8, and #349's "What changes".
- Check that the report parser fails closed on each listed fault. Do this with tests, not by reading the code.
- Check that the occurrence map's `do_not_change` paths are untouched: `git diff --stat` on `docs/changelog`, `docs/architecture/adr`, `kitty-ops` and `site` is empty.
- Confirm that the real-jar output is pasted in the history.

## Progress & Status

Use the CLI only: `spec-kitty agent tasks add-history WP01 --note …` and `spec-kitty agent tasks move-task WP01 --to <status>`.
