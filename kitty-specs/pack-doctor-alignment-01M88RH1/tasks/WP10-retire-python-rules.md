---
work_package_id: WP10
title: Retire the Python rules pack-doctor judges; keep the house rules
dependencies: []
requirement_refs:
- FR-013
- FR-014
- FR-015
- FR-017
- C-003
planning_base_branch: feat/pack-doctor-alignment
merge_target_branch: feat/pack-doctor-alignment
branch_strategy: Planning artifacts for this mission were generated on feat/pack-doctor-alignment. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/pack-doctor-alignment unless the human explicitly redirects the landing branch.
subtasks:
- T050
- T051
- T052
- T053
- T054
- T055
- T056
phase: Phase 4 - Retirement and polish
history:
- at: '2026-11-25T07:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/ci/validate_pack_schemas.py
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- scripts/ci/validate_pack_schemas.py
- scripts/ci/validate-packs.sh
- tests/ci/test_validate_pack_schemas.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP10 - Retire the Python rules pack-doctor judges; keep the house rules

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `python-pedro`
- **Agent/tool**: `claude`

---

## IMPORTANT: Review Feedback

Check `review_ref` with `spec-kitty agent tasks status --mission pack-doctor-alignment-01M88RH1`. Address every item.

---

## Objectives & Success Criteria

- Every "Retire" row of issue #348 is gone from `validate_pack_schemas.py`, together with its tests and its help lines (FR-014). The same goes for the two preset rules of #346 (FR-013).
- The old anti-pattern model is retired. An anti-pattern **file** is a manifest constituent, held by its file only. The "Charter Pack validation" job (`validate-packs.sh`) passes over the curated tree at the new pin (FR-017).
- Every house rule of #348 remains, each with a comment naming its charter ruling and a test that fails without it (FR-015).
- `validate-packs.sh`'s header and arguments state the split (#348 "Done when").
- `python3 -m pytest tests/ci -q` passes, and `scripts/ci/validate-packs.sh` exits 0.

## Context & Constraints

- **Depends on**: WP01 (the gate runs `--full`, so the charter covers these rules) and WP09 (`remediate` replaces the Python derivation).
- **Read**: issues #348 and #346 in full, and `research.md` R8. The line numbers in #348 have drifted (the file has 1 762 lines), so find each rule **by name**.
- **The charter's answer is the rule (C-003).** Retire a rule only where the charter judges it. Keep a house rule only where a charter ruling leaves it to open-packs.

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`; lanes come from `lanes.json`.
- `spec-kitty agent action implement WP10 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T050 - Anti-pattern files are constituents

- Remove `anti_pattern` from `MANIFEST_EXEMPT_NODE_KINDS`, and drop the `CONSTITUENT_KIND_BY_SCHEMA` note about graph-only anti-patterns.
- In `held_artifacts`, stop holding `anti_pattern` by its graph node. The file holds it, through the contract's `anti-pattern` kind at the pin.
- Confirm that `classify` maps `anti_patterns/*.anti-pattern.yaml` through the pinned `file-kinds.yaml`. This is data-driven; add a test with a fixture file.
- Validate against the pinned `anti-pattern.schema.json`, so a missing `severity` fails.

### Subtask T051 - Retire the preset rules (#346)

- In `cross_pack_violations`, remove "a preset id no pack declares" and "the `must_have` not held in the `depends_on` closure". Pack-doctor judges these at `CLOSURE` (`preset_item_undeclared`, `preset_item_not_held`).
- Keep "the id re-declared at another level" and "the bare DRG endpoint" (T054).

### Subtask T052 - Retire the manifest derivation and the stale check (#347)

- Remove `stale_manifest_fields` and its call in `validate_pack`, `derived_manifest`, `derive_manifest`, `membership_mismatch`, `regenerate_manifest`, and the `--derived-manifests`, `--derive-manifest` and `--regenerate-manifest` options.
- Remove `REGENERATE_COMMAND`. Where a message names a remedy, it now names `pack-doctor remediate <pack>`.
- `charter_pin.py` no longer calls `--derive-manifest` (WP01). Grep to confirm that no caller remains.

### Subtask T053 - Retire the charter-judged reference and fragment-target rules

- `profile_reference_violations`: remove the bare reference held only by another pack, the qualifier outside the closure, and the named pack that does not hold the reference. Pack-doctor judges these at `REFERENCES`.
- `prompt_fragment_composition_violations`: remove "the target step does not exist" and "the target step's prompt cannot be read".

### Subtask T054 - House rules, each with its ruling

Keep each of these. Above each, add a comment of the form `# House rule (not a charter rule): <ruling>`:

| Rule | Ruling to name |
|---|---|
| The id re-declared at another level | ADR-0053 decision 6: the charter takes it as a layer override (C-005, ADR-0083 decision 18) |
| The bare DRG edge endpoint that resolves to no node | DIV-007 |
| The prompt-fragment slot the target prompt does not declare | C38: the charter refuses it only for a stored activation that has it in force |
| The `specializes_from` cycle (`specialization_cycle_violations`) | The ruling R-s remainder. Pack-doctor does not judge it until charter epic #636 slices 2-4; retire it when a charter release lists it under `REFERENCES`. It pools every pack's edges, which is stricter than per closure. |
| `profile_reference_violations`: the bare reference no pack holds, and the reference qualified with the profile's own pack | Not charter rules (charter `research/rule-coverage.md` row 6). They are kept as house rules by open-packs' call. |

Each rule keeps, or gets, a test that fails if the rule is removed.

### Subtask T055 - Help and the shell header

- Rewrite the `--cross-pack` help to list only the house rules.
- Rewrite `validate-packs.sh`'s header item 3 to the same list, and point to pack-doctor for everything else.
- Drop `--derived-manifests` from its arguments.
- Rename any remaining pack-check mention to pack-doctor (occurrence map).

### Subtask T056 - Tests

- Delete the tests of the retired rules. For each retired preset and reference rule, add **one** test, with an in-test pack, that pack-doctor refuses with the charter code. Put it in `test_charter_pack_doctor.py`'s real-jar class as a recorded out-of-map addition, and skip it without a jar.
- Then run `pytest tests/ci -q`, `scripts/ci/validate-packs.sh`, and `grep -n "pack.check\|pack_check" scripts/ci/validate_pack_schemas.py scripts/ci/validate-packs.sh` (which must be empty).

## Risks & Mitigations

- **A retired rule the charter does not actually fire here.** The paired real-jar test proves it fires.
- **The tests file is large (1 252 lines).** Remove tests by the rule they target, not by line.

## Review Guidance

- Check each #348 table row against the code: is it retired, or kept with a ruling comment?
- Check the paired real-jar tests.
- Confirm that `validate-packs.sh` passes over the curated tree.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
