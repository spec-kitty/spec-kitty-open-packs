---
work_package_id: WP02
title: Manifest mirror parity (#262)
dependencies: []
requirement_refs:
- FR-003
- FR-004
- FR-005
- C-002
- SC-002
planning_base_branch: ci/release-pin-follow-through
merge_target_branch: ci/release-pin-follow-through
branch_strategy: Planning artifacts for this mission were generated on ci/release-pin-follow-through. Completed changes merge back into ci/release-pin-follow-through; execution worktrees are allocated per computed lane from lanes.json.
subtasks:
- T004
- T005
- T006
- T007
- T008
history:
- at: '2026-11-24T16:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/ci/validate_pack_schemas.py
execution_mode: code_change
model: ''
owned_files:
- scripts/ci/validate_pack_schemas.py
- scripts/ci/charter_service_check.py
- tests/ci/test_validate_pack_schemas.py
- tests/ci/test_charter_service_check.py
role: implementer
tags: []
tracker_refs:
- '#262'
---
# Work Package Prompt: WP02 – Manifest mirror parity (#262)

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load python-pedro` before reading anything else.

## Objective

Close the three remaining #262 items. #329 already removed the drift-step items.
1. `derived_manifest` must not descend into a symlinked directory (FR-003).
2. `membership_mismatch` is checked against the charter wording and pinned (FR-004).
3. The derive-then-check test must prove that the derive wrote something (FR-005).

The reference is the charter at the pin, `cb9b154`:
- `ManifestRules.mismatch`, in `service/packs/src/main/java/ai/speckitty/charter/packs/infra/storage/rules/ManifestRules.java`, l.97–118;
- the `PackFileSet` walk, which uses `Files.walkFileTree` and does not follow links, enters a root configured through a link (#174), and skips link files.

See `research.md` R2 and R3.

## Branch Strategy

The planning branch and merge target is `ci/release-pin-follow-through`. Worktrees are allocated per lane from `lanes.json`. Implement with `spec-kitty agent action implement WP02 --agent <name> --mission release-pin-follow-through-01M872WA`.

## Subtasks

### T004 — Red test: symlinked directory

File: `tests/ci/test_validate_pack_schemas.py`, in the `#255` derived-manifest class (the one holding `test_the_derived_lists_hold_every_artifact_file_and_preset_in_path_order`). Build a pack with the existing helpers (`write_contract`, `write_pack`) holding:
- `tactics/a.tactic.yaml` (a real artifact);
- a directory `elsewhere/tactics/b.tactic.yaml` *outside* the pack;
- a symlink `pack/linked -> elsewhere/tactics`.

Assert that `derived_manifest` lists `a` and not `b`. Under Python 3.12 (`rglob` follows links) this is red today. Under 3.13 it may already be green, so also assert through a helper that is independent of the Python version (T005). Run the test on 3.12 if it is available (`uv run --python 3.12` or `python3.12`). Otherwise rely on CI's 3.12, and make sure T005's helper is called directly by a test that fails on any Python version without it. For example, a test of `pack_files()` itself: it must exist and must exclude the linked directory.

### T005 — `pack_files()` helper

In `validate_pack_schemas.py`, add:

```python
def pack_files(pack_dir: Path) -> list[Path]:
    """Every regular file the pack holds, in sorted path order, as the charter's PackFileSet walks it: links (files or
    directories) are not followed and not listed; a pack root that is itself a link is entered (#174)."""
```

Implement it with `os.walk(pack_dir.resolve(), followlinks=False)`. Skip link files. Map each result back to `pack_dir / relative`, so that callers' `relative_to(pack_dir)` keeps working. Return the list sorted by path. Replace the loop head in `derived_manifest` (`for path in sorted(pack_dir.rglob("*")):` plus its `is_symlink`/`is_file` guard) with `for path in pack_files(pack_dir):`.

### T006 — Audit the other walks

The other walks are `validate_pack_schemas.py` l.~998, 1062, 1120, 1286, 1318 and 1384, and `charter_service_check.py` l.298. For each, decide whether it enumerates the pack's file set as the charter would (switch it to `pack_files`) or does something else, such as a schema pass over YAML, where following a link is a separate concern (leave it).

Record each decision as a one-line list in the commit body. Switching changes behaviour only when a pack holds a linked directory, and no shipped pack does. Confirm with `find packs tests/fixtures -type l`.

### T007 — Pin the duplicated-and-unheld case

Add a test to the same class as `test_mismatch_is_worded_and_ordered_like_the_charter`. A listed entry `tactic:x at x.yaml` appears twice and is not derived. Expected reasons, in order:
1. `lists constituent tactic:x at x.yaml, which the pack does not hold`
2. `lists constituent tactic:x at x.yaml twice`

The docstring cites `ManifestRules.mismatch` at the pin: the charter reports both, so the port does too. This is `[ratchet]`. Non-vacuity: locally, mutate `membership_mismatch` to skip repeated entries that are unheld, watch the test fail, and revert. Note it in the commit body.

### T008 — Derive test proves a write

Find the derive-then-check test (around l.1144–1160: `--derive-manifest` then `--derived-manifests`). Before the derive, capture the manifest's bytes, or `None` when it is absent. After the derive, assert that the bytes differ and that the file exists. A no-op derive must now fail this test: show it with a local mutation that makes `derive_manifest` return early, then revert.

## Definition of Done

- `python3 -m unittest tests.ci.test_validate_pack_schemas tests.ci.test_charter_service_check` passes on the local Python. CI's 3.12 run is the second proof.
- `scripts/ci/validate-packs.sh` and `--cross-pack` stay green. No manifest or digest under `packs/` changes (`git status packs/` is clean).
- The commit body lists the audit decisions (T006) and the mutation checks (T007, T008).

## Reviewer guidance

Diff `pack_files` against the charter's walk semantics in R3. Make sure the root-link case (#174) still enters the root.
