---
work_package_id: WP01
title: Stray-file gap pinned (#331)
dependencies: []
requirement_refs:
- FR-001
- C-001
planning_base_branch: ci/release-pin-follow-through
merge_target_branch: ci/release-pin-follow-through
branch_strategy: Planning artifacts for this mission were generated on ci/release-pin-follow-through. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into ci/release-pin-follow-through unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-release-pin-follow-through-01M872WA
base_commit: bda834f985df431b52d40df937204efc6fa24066
created_at: '2026-11-24T15:37:54.893255+00:00'
subtasks:
- T001
- T002
- T003
history:
- at: '2026-11-24T16:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/ci/charter_pack_check.py
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- scripts/ci/charter_pack_check.py
- tests/ci/test_charter_pack_check.py
role: implementer
tags: []
tracker_refs:
- '#331'
---
# Work Package Prompt: WP01 – Stray-file gap pinned (#331)

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load python-pedro` before reading anything else.

## Objective

Pin the operator's ruling on #331 (2026-11-21, option 3: **accept the gap, no override**):
- a stray *ignored-kind* file (`notes.md`) passes the pack-check gate with a `file_not_held` notice;
- an *unmodelled* stray file (`notes.txt`, a log) still fails, because pack-check's own `--round-trip` refuses it as `round_trip_red`;
- open-packs never downgrades that verdict.

The charter fix is spec-kitty-charter#631, which makes the round trip skip the files the store does not hold. When it ships, the real-jar test from T002 flips and must be updated deliberately.

Read `spec.md` (FR-001, FR-002, C-001) and `research.md` (R6) first.

## Branch Strategy

The planning branch and merge target is `ci/release-pin-follow-through`. Execution worktrees are allocated per computed lane from `lanes.json`; never choose a base by hand. Implement with `spec-kitty agent action implement WP01 --agent <name> --mission release-pin-follow-through-01M872WA`.

## Subtasks

### T001 — Gate-judge test with a same-fixture control

File: `tests/ci/test_charter_pack_check.py`, class `JudgeTheSet`.

Add one test, named for the behaviour, for example `test_an_unmodelled_stray_file_still_fails_through_the_round_trip_with_no_override`. Use the existing `report()`, `problem()` and `self.judge()` helpers. Two halves, on the same pack names `("a", "b")`:

1. **Control:** exit 0, a clean report, and stderr `warning: a: file_not_held notes.md: not held (notes)`. Expect `[]`.
2. **Case:** exit 1, `report(["a","b"], problems=[problem("validation_failed", "round_trip_red")])` with detail naming `notes.txt`, and stderr `warning: a: file_not_held notes.txt: not held (no pack file kind models this file)`. Expect a non-empty failure list that contains `round_trip_red`.

Look at `warnings()` in the gate to get the exact stderr shape it parses. Copy the shape from `test_a_clean_complete_verdict_passes`.

The case assertion holds today (`[ratchet]`). **Non-vacuity:** check locally that the test goes red when `judge_set` drops problems whose file is also `file_not_held`, then revert that throwaway mutation. Name the mutation in the commit body.

### T002 — Real-jar case

File: same module, class `RealPackCheck` (it runs only when `PACK_CHECK_JAR` is set; the `Charter service validation` job sets it).

Read the existing `RealPackCheck` tests first and reuse their scratch-copy helpers. Add one test:
- copy one small shipped pack (for example `packs/qa`, or whatever the existing tests use) into a temp dir;
- add `notes.md` and run the gate's run-and-judge path: expect a pass;
- add `notes.txt` instead and run again: expect a failure whose lines include `round_trip_red`.

In the docstring, cite spec-kitty-charter#631: when that lands, this test is expected to flip.

Run it locally only if you have Java 25 and the rc.3 jar (`scripts/ci/charter_pack_check_jar.sh` downloads it). Otherwise CI proves it; say so in the review hand-off.

### T003 — Docstring wording

File: `scripts/ci/charter_pack_check.py`, module docstring, item 1. Replace "pack-check's round trip still refuses an unmodelled stray file as ``round_trip_red``, which #331 tracks." with wording that states:
- the operator ruling (#331, 2026-11-21): the gap is accepted, and the gate does not override pack-check;
- only ignored-kind notes may stay; any other stray file fails until spec-kitty-charter#631.

Plain, short sentences; no code change.

## Definition of Done

- `python3 -m unittest tests.ci.test_charter_pack_check` passes; `RealPackCheck` is skipped without a jar.
- The mutation check from T001 is recorded in the commit body.
- No change to the gate's behaviour.

## Reviewer guidance

Check that no `round_trip_red` is downgraded anywhere (C-001). Check that the control and the case use the same pack set.
