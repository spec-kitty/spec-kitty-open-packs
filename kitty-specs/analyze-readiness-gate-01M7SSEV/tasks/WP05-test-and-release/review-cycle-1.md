---
affected_files: []
cycle_number: 1
mission_slug: analyze-readiness-gate-01M7SSEV
reproduction_command:
reviewed_at: '2026-11-19T14:15:55Z'
reviewer_agent: claude::generic-reviewer
wp_id: WP05
---

# WP05 review feedback - changes requested

Reviewed: lane-e @ b8f6c88. Independent reviewer: claude::generic-reviewer (session_019C2Tk5NruMoumnqkuwALns).

## F1 (must fix) - the read-only test exempts any line that merely contains "not run", "do not" or "never"

`_PROHIBITION` matches anywhere on the line, and one match exempts the whole line. The reviewer ran these lines through `writing_finalize_lines`, and all three return `[]` (missed):

- `If the check could not run, run `spec-kitty agent mission finalize-tasks --mission <slug>` to finalize.`
- `Do not forget: spec-kitty agent mission finalize-tasks --mission x --json`
- `Next, run `finalize-tasks` without flags to finalize.`

The first line is the realistic regression: a could-not-run fallback that tells the agent to finalize. It is exactly what the invariant exists to stop, and the word "not run" in the line hides it.

Fix:
1. Count a line as a prohibition only when the prohibition governs the command. For example, the prohibition word comes before the command or flag and is directly attached to it (`never run`, `never pass`, `do not run`, `not ... without --validate-only`). Alternatively, require the prohibited form to appear in an explicit list.
2. Treat a bare `finalize-tasks` (no `spec-kitty agent mission` prefix) without `--validate-only` as a command too. A narrow regex such as "`finalize-tasks` followed by anything but `--validate-only` on an instruction line" is enough.
3. Add the three lines above to the positive control as must-catch cases. Keep the real prompts' prohibition lines (for example "stop here: do not run the check", "never pass `--refresh-planning-commit`") as must-pass cases, so the fix does not over-fit the other way.

## F2 (should fix) - the version-before-command check covers software-dev only

`test_version_check_precedes_the_validation_command` reads only `ANALYZE`. cave-kitty states the same gate ("Run `spec-kitty --version` first"); add it to the check.

## Challenges

1. Non-vacuity: there is a same-fixture positive control and the mutation check is real, but the exemption makes the test bypassable (F1). The other content tests pin ids, prefixes and the cap rather than prose, which is fine.
2. Bump closure: complete. The reviewer resolved every `==` pin against each target's version, and none is stale. The packs at 2.1.0 (drupal, javascript, python) are range-pinned, with no content change. cave-kitty's bump is justified by its own content change.
3. Changelog: accurate. It names the CLI >= 3.1.0a5 requirement and the old-CLI behaviour (HIGH, blocked), lists the bumps matching the source files, and says "nothing in your packs".

## Passed

- Offline gates:
  - `check-pack-digests.sh`: 0;
  - `pack_digest.py --check`: ok;
  - WP05, digest and ASCII tests: 40 passed;
  - vocabulary: 0.
- Not reproduced by the reviewer, because the charter contract returns 404 here: validate-packs, the service check, and the charter-dependent tests/ci.
- The `test_pack_digest.py` BUILT_IN_DIGEST edit outside the owned files is accepted, the same as #301.
- Side finding `PLANNING_BRANCH_NOT_PERSISTED` (classified as a refusal; arguably could-not-run): agreed that it is worth an orchestrator decision. It does not block WP05.
