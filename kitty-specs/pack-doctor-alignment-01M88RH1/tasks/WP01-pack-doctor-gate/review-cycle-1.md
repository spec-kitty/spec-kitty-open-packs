---
affected_files: []
cycle_number: 1
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-25T20:30:17Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP01
---

# WP01 review cycle 1: changes requested

Reviewer: claude::reviewer-renata (an in-session reviewer subagent, decision 01M8A5ZTVXJ59PNN56PC3WGR3Z). Reviewed 7385886b on lane-a.

## Required

R1. `scripts/ci/charter_pin.py` `REMEDIATE_OUTCOME` refuses a real outcome line.
- The charter prints `<dir>: rewritten, <n> quoted number(s) repaired` (`Remediate.java`). The real jar printed `packs/foundation: rewritten, 1 quoted number repaired`, which the regex does not match.
- So `rederive` raises "gave no outcome" after a restamp that succeeded.
- The outcome lines are on stdout, not stderr as the comment says.
- `FAKE_JAVA` in the tests mirrors the wrong format: stderr, a one-line refusal, and no `repaired` variant.

R2. Java 25 is not set up before any `apply` step, and `apply` now runs pack-doctor `remediate`.
- `validate-packs.yml` job `validate` has no setup-java.
- Job `charter-service` runs the move before its setup-java and Gradle steps.
- `charter-track.yml` job `bump` has no setup-java.
- A failed move skips every later step, so every track that moves the pin goes red before checking anything.

R3. `scripts/ci/charter_pack_doctor.py` `judge_invalid` never calls `report_faults`. An invalid fixture's report with tool.name `pack-check`, an exit-code mismatch, an unknown key, or no options is accepted. This breaks FR-005 and #349.

## Nits

N1. The shape of `checks` is not checked:
- a string passes, by substring;
- an out-of-order list passes;
- an unknown check passes;
- `summary.exit_code: False` passes against exit 0.

N2. A pack listed twice in the report fails with "missing: none; unexpected: none" instead of naming the duplicate.

N3. `run()` creates the report directory before `command_for` refuses a report inside a pack.

N4. Missing tests:
- report containment through a symlink or real path;
- a lock that holds `pack_check_sha256`, and the `--pack-check-sha256` flag, are refused (FR-002).

N5. The `charter_pin.py` docstring understates `remediate`: it rewrites every modelled file in canonical form, not only `pack-manifest.yaml` (decision 01M8A5ZNJTETCBFCC4H5G0VHQ6).

N6. In `charter_pin.py`:
- `remediate()` ignores JAVA_HOME;
- `pack_doctor_jar()`'s work dir differs from the gate step's (`$RUNNER_TEMP/charter-service`), so a main pin builds twice;
- the `mkdtemp` fallback is never removed.

N7. The `expectedFailure` on `test_the_gate_passes_this_checkout` is satisfied by any failure, a crash included. Assert exit 1.

N8. Any red tree now fails the move step, so no report artifact is produced. Make the move tolerate pack-doctor's own refusal (exit 1) of a tree the gate will then judge, or document it.

## For the rebase onto main (not WP01's tree; carried by the rebase)

- `charter-track.yml`:
  - main's provenance, derive and bump jobs carry `pack_check` names, the `--pack-check-sha256` flag, a jq lock check `pack_check_sha256` and artifact texts;
  - main's `derive` job (which now runs `apply`) needs Java 25 too;
  - main's bump path allowlist admits only `pack-manifest.yaml` inside a pack, but `remediate` rewrites `pack.yaml`, presets, directives, drg and tactics, so it must widen.
- `tests/ci/test_workflows.py`: main's new tests carry those names.
- `charter_pack_check.py`: main's #331 docstring paragraph is false at f6f21e4c; WP01's docstring wins.
- `test_charter_pack_check.py`: main's `test_a_stray_note_passes_and_an_unmodelled_stray_file_fails_the_gate` must move to `RealPackDoctor` and flip, because `notes.txt` now passes as a `file_not_held` notice (measured: exit 0).

## Verified

- The `tests/ci` suite passes; the real jar gives 41 passed and 1 xfailed, and unittest OK.
- All five fixtures are refused as expected.
- `judge_set` fails closed on every T005 case.
- `command_for` refuses a report inside a pack, including through symlinks.
- The lock and pin are correct; the release track with an empty tag is fine.
- `bash -n` passes on all 28 `run:` scripts.
- The name grep is clean, and no protected path is touched.
