---
work_package_id: WP02
title: Record a sidecar digest for every pack
dependencies:
- WP01
requirement_refs:
- FR-005
- FR-006
- FR-008
- SC-001
- SC-004
- C-005
planning_base_branch: feat/194-pack-digests
merge_target_branch: feat/194-pack-digests
branch_strategy: Planning artifacts for this mission were generated on feat/194-pack-digests. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/194-pack-digests unless the human explicitly redirects the landing branch.
subtasks:
- T007
- T008
- T009
history: []
agent_profile: python-pedro
authoritative_surface: packs/
create_intent:
- packs/architecture.source.yaml
- packs/cave-kitty.source.yaml
- packs/drupal.source.yaml
- packs/event-driven.source.yaml
- packs/foundation.source.yaml
- packs/go.source.yaml
- packs/internal.source.yaml
- packs/java.source.yaml
- packs/javascript.source.yaml
- packs/pack-authoring.source.yaml
- packs/planning-analysis.source.yaml
- packs/python.source.yaml
- packs/qa.source.yaml
- packs/refactoring.source.yaml
- packs/rust.source.yaml
- packs/spdd.source.yaml
- packs/testing.source.yaml
- packs/writing.source.yaml
execution_mode: code_change
model: sonnet
owned_files:
- packs/*.source.yaml
role: implementer
tags: []
tracker_refs: []
---

# WP02 — Record a sidecar digest for every pack

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load the agent profile specified in the frontmatter, and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

Implement with: `spec-kitty agent action implement WP02 --agent claude --mission per-pack-digest-gate-01M75YJ0`

## Objective

Generate `packs/<name>.source.yaml` for all 19 packs with `pack_digest.py --update` (WP01), and
refresh the stale header comments of `packs/built-in.source.yaml` without changing its keys or
value.

## Context

- 19 directories under `packs/` hold a `pack.yaml` (planning-time count; the brief said ~21).
  Only `built-in` has a sidecar today.
- Research D5/D6: sidecar named by **directory** (`packs/internal.source.yaml`, though its
  `pack_id` is `spec-kitty-internal`); `seeded_from` only where true — do not invent provenance
  for unseeded packs (charter identity discipline).
- Core reads `packs/built-in.source.yaml` (path, `seeded_from`, `tree_digest {algorithm, value}`):
  those must not change (FR-006). Only comments may be edited.
- No pack content changes in this WP, so built-in's value stays `ad8412…38ca` (SC-004) and the
  generated docs pages (`docs/packs/`) do not move (sidecars are outside every pack directory).

### Subtask T007: Generate the 18 missing sidecars

**Steps**:
1. From the repo root: `python3 scripts/ci/pack_digest.py --update`.
2. Expect 18 `created:` lines and no `updated:` line for built-in.
3. Inspect two outputs by hand (one member such as `foundation`, one org pack such as `internal`):
   header comment, `tree_digest.algorithm: spec-kitty-snapshot-sha256`, 64-hex value.
4. Do not hand-edit any value. If a value looks wrong, fix WP01, not the file.

**Validation**: `python3 scripts/ci/pack_digest.py --check` exits 0 with 19 `ok:` lines and no orphan.

### Subtask T008: Refresh `packs/built-in.source.yaml` comments

**Purpose**: FR-008 — the header still says built-in "depends on packs/foundation/ and
packs/writing/" (it has six members) and that `scripts/ci/check-built-in.sh` enforces it.

**Steps**:
1. Edit comments only:
   - Line 8-9: "Edit packs/built-in/ here and run `python3 scripts/ci/pack_digest.py --update`;
     scripts/ci/check-pack-digests.sh enforces it." (WP03 creates that script; naming it now is
     intended — WP03 lands before the mission merges.)
   - The #73 paragraph: built-in depends on its six members (foundation, writing, testing,
     refactoring, architecture, planning-analysis); each member now has its own sidecar
     `packs/<member>.source.yaml`; a consumer fetching the members checks each at the same pin.
   - The digest comment: point at `scripts/ci/pack_digest.py` (keep "core's algorithm",
     `built_in_digest.py` remains as compatibility entry point).
2. Do **not** touch `seeded_from`, `tree_digest`, key order or the value.
3. Avoid retired vocabulary (run `python3 scripts/ci/check_vocabulary.py`).

**Validation**: `git diff packs/built-in.source.yaml` shows comment lines only;
`python3 scripts/ci/built_in_digest.py` still prints `ad8412…38ca`.

### Subtask T009: Prove the gate is non-vacuous on real content

**Steps** (do not commit the experiment):
1. Append a byte to any file in `packs/writing/`; `--check` must fail naming
   `packs/writing.source.yaml`; revert.
2. Move `packs/qa.source.yaml` aside; `--check` must fail "has no recorded digest"; restore.
3. `touch packs/ghost.source.yaml`; `--check` must fail as orphan; remove.
4. Run `python3 scripts/ci/check_vocabulary.py` and `scripts/ci/validate-packs.sh` — both green
   with the new files present.
5. Run `python3 scripts/docs/gen_pack_reference.py --check` — green (no generated page moved).

**Validation**: record the three failure lines in the WP's implementation notes for the reviewer.

## Definition of Done

- 19 sidecars present, each fresh; `pack_digest.py --check` exit 0, 19 ok lines.
- `built-in.source.yaml`: comments updated, keys/value byte-identical.
- Vocabulary guard, pack validation and the docs drift check green.
- Subtasks recorded via `spec-kitty agent tasks mark-status`.

## Risks

- **Main moves under you**: any pack change merged to main before this mission lands makes a
  sidecar stale. On rebase, rerun `--update` and commit; never hand-edit.
- **Vocabulary guard** flags header text → keep the WP01 template text.

## Reviewer Guidance

- Recompute one digest independently (`python3 scripts/ci/pack_digest.py foundation`) and compare.
- Confirm no `seeded_from` was invented for any new sidecar.
- Confirm `built-in.source.yaml` value unchanged.
