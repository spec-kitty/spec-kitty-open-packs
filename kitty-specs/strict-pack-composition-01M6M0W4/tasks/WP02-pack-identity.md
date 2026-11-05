---
work_package_id: WP02
title: Pack identity
dependencies:
- WP01
requirement_refs:
- FR-004
- FR-005
- C-002
planning_base_branch: feat/strict-pack-composition
merge_target_branch: feat/strict-pack-composition
branch_strategy: Planning artifacts for this mission were generated on feat/strict-pack-composition. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/strict-pack-composition unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-strict-pack-composition-01M6M0W4
base_commit: cc57e2e39c21acb13e9b7579b8273efa168d5a4f
created_at: '2026-11-04T23:42:08.851117+00:00'
subtasks:
- T006
- T007
- T008
history:
- at: '2026-11-04T20:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent:
- packs/qa/pack.yaml
- packs/event-driven/pack.yaml
- packs/cave-kitty/pack.yaml
- tests/fixtures/valid/example-pack/pack.yaml
execution_mode: code_change
owned_files:
- packs/qa/pack.yaml
- packs/event-driven/pack.yaml
- packs/cave-kitty/pack.yaml
- tests/fixtures/valid/example-pack/pack.yaml
- docs/packs/cave-kitty.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP02 – Pack identity

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Give every pack a compliant descriptor. A pack with none is refused on its own, and `depends_on` needs one. These identities are permanent.

## Branch Strategy

- Planning/base branch: `feat/strict-pack-composition`. Final merge target: `feat/strict-pack-composition`, which reaches `main` by pull request after the mission.
- The workspace is resolved by `spec-kitty agent action implement`; trust the path it prints.

## Context

Read first: `kitty-specs/strict-pack-composition-01M6M0W4/spec.md`, `plan.md`, `data-model.md`, `research.md`. The full site list is `reference-inventory.txt` in the same folder.

Local tools. `python3 -m venv` fails on this machine; use the spec-kitty venv:

```bash
export PATH=~/Documents/code/kitty/spec-kitty/.venv/bin:$PATH
```

Git identity is not configured here. Pass it per command, do not edit config:
`GIT_AUTHOR_NAME="Stijn Dejongh" GIT_AUTHOR_EMAIL="stijn.dejongh@sddevelopment.be" GIT_COMMITTER_NAME="Stijn Dejongh" GIT_COMMITTER_EMAIL="stijn.dejongh@sddevelopment.be"`.

Pause and report, rather than deciding, on: changing an existing test's asserted expectation, any contract change, widening scope past this WP, or a mission runtime failure (C-005).

Implement with:

```bash
spec-kitty agent action implement WP02 --agent claude --mission strict-pack-composition-01M6M0W4
```

## Subtasks

### T006 Mint ids and write the descriptors

Generate four ULIDs with a tool, never typed by hand, and never reuse a value from a research scratch copy:

```bash
python - <<'EOF'
import os, time
ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
def ulid():
    n = (int(time.time() * 1000) << 80) | int.from_bytes(os.urandom(10), "big")
    return "".join(ALPHABET[(n >> (5 * i)) & 31] for i in range(25, -1, -1))
print(ulid())
EOF
```

Follow the shape and comment style of `packs/internal/pack.yaml`:

| File | `name` | Notes |
|---|---|---|
| `packs/qa/pack.yaml` | `quality-assurance` | The directory is **not** renamed |
| `packs/event-driven/pack.yaml` | `event-driven` | |
| `packs/cave-kitty/pack.yaml` | `cave-kitty` | |
| `tests/fixtures/valid/example-pack/pack.yaml` | `example-pack` | Own id: a duplicate is `pack_duplicate_id` |

All have `pack_version: 1.0.0`, `parent_pack: null`, `pack_level: org`. Include `active_charter` and `pack_drg` only where that file exists in the pack; check each. Do not add a `purpose` field: the closed schema forbids it.

### T007 Declare `cave-kitty`'s dependency

Only `cave-kitty` gets `depends_on` here, because it has no references to migrate:

```yaml
depends_on:
  - pack_id: 01ARWG13C000000000000000FG
    range: ">=1.0,<2"
```

Its prompts bind built-in profiles in prose (for example `packs/cave-kitty/missions/cave-dev/steps/review.prompt.md:15`), so the dependency is real. The others get it with their migration, so a pack's dependency and its qualifiers land together.

### T008 Remove the allowance and validate

Remove the descriptor allowance from WP01 (out-of-map edit in `validate_pack_schemas.py`, record the rationale). Regenerate `docs/packs/` and include what changes. Run the gates.

Against the charter contract, confirm with a mutant: remove `name` from a copy of one descriptor and see the gate fail. If `cave-kitty` now fails anything beyond what the research predicted, report it.

```bash
python -m unittest discover -s tests/ci
python -m unittest discover -s tests/docs
bash scripts/ci/validate-packs.sh
bash scripts/ci/check-built-in.sh
```

## Definition of Done

Four descriptors exist with unique, tool-generated ids. All gates pass with the descriptor allowance removed.

Record subtask completion with `spec-kitty agent tasks mark-status <ids> --status done`.

## Reviewer guidance

Check ids are valid ULIDs, unique, and not the research placeholders. Check `git grep` for each id finds only its own descriptor. Check `packs/qa` was not renamed.
