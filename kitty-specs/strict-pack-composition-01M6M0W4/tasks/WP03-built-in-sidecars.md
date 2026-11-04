---
work_package_id: WP03
title: Built-in sidecars
dependencies:
- WP01
requirement_refs:
- FR-007
planning_base_branch: feat/strict-pack-composition
merge_target_branch: feat/strict-pack-composition
branch_strategy: Planning artifacts for this mission were generated on feat/strict-pack-composition. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/strict-pack-composition unless the human explicitly redirects the landing branch.
subtasks:
- T009
- T010
- T011
history:
- at: '2026-11-04T20:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/built-in/
create_intent: []
execution_mode: code_change
owned_files:
- packs/built-in/assets/docs_structural_lint.py.asset.yaml
- packs/built-in/assets/audiences/*.asset.yaml
- packs/built-in/pack-manifest.yaml
- packs/built-in.source.yaml
- docs/packs/built-in.md
- scripts/ci/check-built-in.sh
- scripts/ci/built_in_digest.py
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP03 – Built-in sidecars

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Fix the six sidecars whose `path` is anchored at the pack root. The charter requires it relative to `assets/` (`SidecarPayloads.java:46-63`, ADR-0040 decision 6). Until this lands, every compose with `built-in` is refused `pack_unreadable`, which hides all reference refusals.

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
spec-kitty agent action implement WP03 --agent claude --mission strict-pack-composition-01M6M0W4
```

## Subtasks

### T009 Fix the six `path` values, atomically

Drop the leading `assets/` from `path` in exactly these six, and no others (the other 14 sidecars are correct):

- `packs/built-in/assets/docs_structural_lint.py.asset.yaml`
- `packs/built-in/assets/audiences/agentic-framework-core-team.md.asset.yaml`
- `packs/built-in/assets/audiences/automation_agent.md.asset.yaml`
- `packs/built-in/assets/audiences/line_manager.md.asset.yaml`
- `packs/built-in/assets/audiences/nontech_educator.md.asset.yaml`
- `packs/built-in/assets/audiences/software_engineer.md.asset.yaml`

These must land in one commit with:

1. `python scripts/ci/validate_pack_schemas.py --regenerate-manifest packs/built-in`
2. the new `tree_digest` in `packs/built-in.source.yaml`, from `python scripts/ci/built_in_digest.py`
3. the regenerated `docs/packs/built-in.md`

Check other mentions in `packs/built-in/asset.graph.yaml`, `tactic.graph.yaml` and `assets/audiences/README.md`. They may be URNs or prose that should stay; classify each, change only what the rule covers, and report the classification.

### T010 Correct the "re-seed" wording

`scripts/ci/check-built-in.sh:2,5` and `scripts/ci/built_in_digest.py:55` still say "seeded" and "re-seed", while `packs/built-in.source.yaml:7-8` says this is "not a re-seed instruction". Reword to "edit here and record the digest". Keep the `seeded_from` block: it is history.

### T011 Validate

Run the gates. Prove the atomicity: leaving out the manifest restamp must fail with 6 stale entries.

Confirm the fix against the service, using the probe from the research (a throwaway; do not commit it):

```bash
# in a detached worktree of spec-kitty-charter origin/main:
cp /home/stijn/Documents/code/kitty/spec-kitty-open-packs/.kittify/derived/debriefs/epic-118/evidence/RealComposeProbeTest.java service/packs/src/test/java/ai/speckitty/charter/packs/infra/storage/
```

The full command is in `research.md` under "Rerun the compose probe". Expect `built-in` to go from 318 to 324 artifacts with 0 violations.

Do not touch `depends_on` or qualifiers: `built-in` references nothing outside itself. `__init__.py` removal is #94 and belongs to a separate runner; if that has landed first, rebase and regenerate the digest.

```bash
python -m unittest discover -s tests/ci
python -m unittest discover -s tests/docs
bash scripts/ci/validate-packs.sh
bash scripts/ci/check-built-in.sh
```

## Definition of Done

Six paths fixed, manifest, digest and page updated in the same commit, wording corrected, gates pass, and the service reads all six assets.

Record subtask completion with `spec-kitty agent tasks mark-status <ids> --status done`.

## Reviewer guidance

Check exactly six sidecars changed. Check the version is still `1.0.0`. Check the commit is atomic: at no commit does the gate fail.
