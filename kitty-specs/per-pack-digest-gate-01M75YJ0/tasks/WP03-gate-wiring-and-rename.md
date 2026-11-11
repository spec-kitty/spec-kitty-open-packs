---
work_package_id: WP03
title: Wire the all-pack digest check into the required gate and rename it
dependencies:
- WP02
requirement_refs:
- FR-007
- FR-008
- C-003
- SC-002
planning_base_branch: feat/194-pack-digests
merge_target_branch: feat/194-pack-digests
branch_strategy: Planning artifacts for this mission were generated on feat/194-pack-digests. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/194-pack-digests unless the human explicitly redirects the landing branch.
subtasks:
- T010
- T011
- T012
history: []
agent_profile: python-pedro
authoritative_surface: scripts/ci/
create_intent:
- scripts/ci/check-pack-digests.sh
execution_mode: code_change
model: sonnet
owned_files:
- scripts/ci/check-built-in.sh
- scripts/ci/check-pack-digests.sh
- .github/workflows/validate-packs.yml
- tests/ci/test_workflows.py
role: implementer
tags: []
tracker_refs: []
---

# WP03 — Wire the all-pack digest check into the required gate and rename it

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load the agent profile specified in the frontmatter, and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

Implement with: `spec-kitty agent action implement WP03 --agent claude --mission per-pack-digest-gate-01M75YJ0`

## Objective

Rename `scripts/ci/check-built-in.sh` to `scripts/ci/check-pack-digests.sh` (now running
`pack_digest.py --check` over every pack), rename the CI step, keep it inside the `validate` job
that feeds the required `Validate packs gate`, and guard that wiring with a workflow test.

## Context

- Ruleset 26594729 requires `Validate packs gate` and `Charter service validation`. The `gate` job
  needs `validate`; the digest step lives in `validate`. Keeping it there means no ruleset change
  (C-003).
- This is a classified rename: see `kitty-specs/per-pack-digest-gate-01M75YJ0/occurrence_map.yaml`
  (move `check-built-in.sh` → `check-pack-digests.sh`; ADRs, released changelog sections,
  `kitty-ops/` and other missions are **not** edited). Docs/prose references are WP05's.
- WP01 delivered `scripts/ci/pack_digest.py`; WP02 delivered fresh sidecars, so the gate is green
  when wired.

### Subtask T010: Rename and rewrite the entry script

**Steps**:
1. `git mv scripts/ci/check-built-in.sh scripts/ci/check-pack-digests.sh` (keep the exec bit).
2. Rewrite the header: "Check the recorded tree digest of every pack (spec-kitty-open-packs#194).
   Every directory packs/<name>/ with a pack.yaml has a sidecar packs/<name>.source.yaml whose
   tree_digest matches the directory. Edit a pack, then run
   `python3 scripts/ci/pack_digest.py --update` in the same change. Schema validation is
   validate-packs.sh's." Keep `set -euo pipefail` and the `cd "$root"`.
3. Drop the built-in-only `pack.yaml` existence guard (discovery fails closed instead); body is
   `python3 scripts/ci/pack_digest.py --check`.
4. No compatibility copy of `check-built-in.sh` is kept: nothing outside this repo calls it
   (research B: kitty-stack calls `built_in_digest.py`, which stays).

**Validation**: `scripts/ci/check-pack-digests.sh` exits 0, 19 ok lines.

### Subtask T011: Rename the CI step

**Steps**:
1. In `.github/workflows/validate-packs.yml`, job `validate`, replace
   ```yaml
   - name: Check the built-in pack digest
     if: ${{ !cancelled() }}
     run: scripts/ci/check-built-in.sh
   ```
   with
   ```yaml
   - name: Check every pack's recorded digest
     if: ${{ !cancelled() }}
     run: scripts/ci/check-pack-digests.sh
   ```
2. Keep its position (after "Validate packs against the charter schemas") and `if:`.
3. Search the workflow for other stale "built-in digest" comments and fix them; touch nothing else.
4. `tests/ci` already runs in the "Pack validator tests" step, so WP01's tests run in the gate
   without a new step.

**Validation**: `grep -n "check-built-in" .github/workflows/` returns nothing.

### Subtask T012: Workflow test

**Purpose**: FR-007 — a regression that moves or drops the step fails a test.

**Steps**:
1. In `tests/ci/test_workflows.py`, add to the class that guards required-check coverage (there is
   `test_the_required_check_covers_the_generated_pack_pages` at ~line 240; mirror its style) a test
   `test_the_required_check_covers_every_pack_digest`:
   - load `validate-packs.yml`; find the job the `Validate packs gate` job `needs` that holds the
     pack validation (the `validate` job);
   - assert one step's `run` is `scripts/ci/check-pack-digests.sh`;
   - assert that step's `if` evaluates true on a normal PR event the same way the sibling test
     does (reuse the module's helpers rather than string-matching `!cancelled()` if available);
   - assert the script file exists and is executable, and that its text invokes
     `pack_digest.py --check`.
2. Keep the module docstring's style: assert what the required check needs, not YAML spelling.

**Validation**: `python3 -m unittest discover -s tests/ci -p 'test_workflows.py' -v` green; the
new test fails if you revert the step's `run` to the old script name (try it, then restore).

## Definition of Done

- `scripts/ci/check-built-in.sh` gone; `scripts/ci/check-pack-digests.sh` present, executable, green.
- CI step renamed, still in `validate`, still `if: ${{ !cancelled() }}`.
- New workflow test green and proven non-vacuous.
- NFR-001: `time scripts/ci/check-pack-digests.sh` on the real tree is under 10 s; record the
  measured wall time in the implementation notes for the reviewer.
- Subtasks recorded via `spec-kitty agent tasks mark-status`.

## Risks

- Moving the step into a new job would leave it outside the required context → test guards it.
- `git mv` losing the exec bit on some filesystems → test asserts it.

## Reviewer Guidance

- Confirm the gate job's `needs` still includes the job holding the step.
- Confirm no ADR / released changelog / kitty-ops file was edited (occurrence map exceptions).
