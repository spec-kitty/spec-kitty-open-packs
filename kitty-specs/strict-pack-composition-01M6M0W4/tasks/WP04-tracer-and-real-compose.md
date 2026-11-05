---
work_package_id: WP04
title: 'Tracer: quality-assurance and the real compose'
dependencies:
- WP02
- WP03
requirement_refs:
- FR-005
- FR-008
- FR-011
- FR-013
- C-005
planning_base_branch: feat/strict-pack-composition
merge_target_branch: feat/strict-pack-composition
branch_strategy: Planning artifacts for this mission were generated on feat/strict-pack-composition. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/strict-pack-composition unless the human explicitly redirects the landing branch.
subtasks:
- T012
- T013
- T014
- T015
- T016
history:
- at: '2026-11-04T20:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/qa/
create_intent: []
execution_mode: code_change
owned_files:
- packs/qa/**
- docs/packs/qa.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP04 – Tracer: quality-assurance and the real compose

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Prove the method on the smallest pack before anything larger: migrate its 3 references, get a real compose through the service's own code, and find out early whether the mission's own runtime survives migrated content. If surprises exist, this is where they should surface.

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
spec-kitty agent action implement WP04 --agent claude --mission strict-pack-composition-01M6M0W4
```

## Subtasks

### T012 Migrate the 3 references

The three edges are listed in `reference-inventory.txt` under `qa`. Each is `<kind>:<id>` in `packs/qa/drg/fragment.yaml`, and becomes `built-in::<kind>:<id>`.

Use a throwaway script rather than hand edits; do not commit it. It must rewrite only the matched value and keep comments and formatting: do **not** round-trip through PyYAML. It will be reused for the larger packs in WP05 and WP06, so keep it under `.kittify/derived/debriefs/epic-118/evidence/` in the **root checkout**, which git ignores. Handle both forms from `data-model.md`.

Add to `packs/qa/pack.yaml`:

```yaml
depends_on:
  - pack_id: 01ARWG13C000000000000000FG
    range: ">=1.0,<2"
```

Remove `qa` from `PENDING_PACKS` (out-of-map, recorded). Regenerate `docs/packs/qa.md`.

Re-run the independent scan, which must show 0 `bare->other` for this pack:
`python /home/stijn/Documents/code/kitty/spec-kitty-open-packs/.kittify/derived/debriefs/epic-118/evidence/scan.py` (read its header for arguments).

### T013 Check the 24 profile references (FR-011)

`packs/qa/agent_profiles/*` hold 24 references to `built-in` the service does not check today (`AgentProfile.relationships()` is empty, `AgentProfile.java:373`): 13 `tactic-references`, 6 `styleguide-references`, 1 `toolguide-references`, 4 `operating-procedures`.

The operator's ruling: check and corroborate, and log an issue if that proves too much scope. So establish, from the charter's schema and code:

1. Are qualified values valid in each of these four fields? Research saw it accepted on `tactic-references` and `styleguide-references` on one profile only.
2. Would the service ever resolve them, and would a future check refuse them bare?

If qualifying them is valid in all four fields and mechanical, do it here and include them in the inventory count in your report. If not, leave them bare and report what you found, so the follow-up issue can be filed at close-out. Do not change the schema or any charter code.

### T014 Real compose on a charter draft pull request

Spec-kitty-charter is a separate repository: work on a new branch there, not in this mission's tree, and open a **draft** pull request. Do not merge it; it is finished in WP07 and after this mission merges.

1. Add a compose test in `service/packs` beside `OpenPacksCorpus`, tagged as that corpus's tests are. It reads `OpenPacksCorpus.packsDirectory()`, the pinned checkout, not fixtures. The probe at `/home/stijn/Documents/code/kitty/spec-kitty-open-packs/.kittify/derived/debriefs/epic-118/evidence/RealComposeProbeTest.java` is a working seed. Limit it to the packs migrated so far for now: `built-in` + `quality-assurance` + `cave-kitty`; `event-driven` and `internal` follow.
2. Assert the served pack list, not only success: charter #360 warns refusal scenarios can silently become 200s.
3. Add negative controls on throwaway copies: reverting one qualification is refused `pack_reference_unqualified` naming the pack; removing `depends_on` is refused with a `pack_reference_*` code.
4. Point `openPacksRef` at this mission's pushed head. Push the mission's branch only as needed for this.
5. Run locally against the worktree: `JAVA_HOME=/usr/lib/jvm/temurin-25` and `-PopenPacksDir=<worktree>`; see `service/packs/build.gradle.kts:96-100`.

The test can only run with the charter's own conventions; follow them over this brief where they differ, and say so.

Other corpus tests (`OpenPacksCorpus.DIAGNOSTICS`, `FileSystemPackInspectorTest`, `known-failures.yaml`) will object until WP07. Update only what the draft needs in order to run, and list what is left.

### T015 Try the mission runtime on migrated content (C-005)

In a scratch copy whose `packs/` holds this WP's tree, run:

```bash
SK=~/Documents/code/kitty/spec-kitty/.venv/bin/spec-kitty
$SK charter context --action plan --json
$SK doctor charter-packs
$SK dispatch "probe" --profile implementer-ivan
$SK next --mission strict-pack-composition-01M6M0W4 --json
```

Close any Op the probe opens with `--outcome abandoned`. Expected, and accepted by the operator: `depends_on` is `extra_forbidden`, and org packs stop merging. What matters is whether the runtime commands **exit successfully**. **If `next` or `dispatch` fail, stop and report: this mission runs on them.**

### T016 Validate

```bash
python -m unittest discover -s tests/ci
python -m unittest discover -s tests/docs
bash scripts/ci/validate-packs.sh
bash scripts/ci/check-built-in.sh
```

Report: compose results, any refusal beyond `pack_reference_*`, the FR-011 outcome, and the C-005 result.

## Definition of Done

`quality-assurance` composes with `built-in` through the service's own code, negative controls refuse, the runtime check is reported, FR-011 has an outcome, gates pass, and `qa` is out of `PENDING_PACKS`.

Record subtask completion with `spec-kitty agent tasks mark-status <ids> --status done`.

## Reviewer guidance

Check the compose test reads the real checkout. Check the negative controls really fail for the stated code. Check `git diff --stat` shows no reformatting beyond the changed values.
