---
work_package_id: WP04
title: Measurement discipline for shared machines
dependencies:
- WP02
requirement_refs:
- FR-015
- SC-006
planning_base_branch: t3/test-doctrine-2
merge_target_branch: t3/test-doctrine-2
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-2 unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-test-doctrine-2-01M7YH30
base_commit: cdd2b851ad2e5669e52a25358f76a1e2e9584488
created_at: '2026-11-21T08:22:40.700220+00:00'
subtasks:
- T017
- T018
history:
- at: '2026-11-21T08:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/testing/tactics/testing/
create_intent:
- packs/testing/tactics/testing/shared-machine-test-measurement.tactic.yaml
execution_mode: code_change
model: ''
owned_files:
- packs/testing/tactics/testing/shared-machine-test-measurement.tactic.yaml
- packs/internal/procedures/targeted-mission-test-run.procedure.yaml
- packs/internal/drg/fragment.yaml
role: implementer
tags: []
tracker_refs:
- '#152'
---
# Work Package Prompt: WP04 – Measurement discipline for shared machines

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

FR-015 (#152): a testing tactic so agents sharing one machine stop reading contended, killed or piped runs as results. Read `spec.md`, `research.md` (R8), the #152 issue and its triage comment.

## Branch Strategy

Planning branch and merge target: `t3/test-doctrine-2`; lanes from `lanes.json`. Implement with `spec-kitty agent action implement WP04 --agent <name> --mission test-doctrine-2-01M7YH30`. Out-of-map edit (recorded): node and edges in `packs/testing/drg/fragment.yaml` (owned by WP02); keep it to the new node and its edges.

## Subtasks

### T017 — The tactic

`packs/testing/tactics/testing/shared-machine-test-measurement.tactic.yaml`, generic (no ports, quotas, make targets, repository paths):
1. Cap heavy suites per machine: before starting a heavy suite (integration, end-to-end, a whole-repository run), check how many are already running on the machine; above the cap the team sets (default: one heavy suite per machine), wait or serialise; bound worker counts explicitly.
2. A run is a measurement only if it finished and its exit status was captured: a killed, timed-out or out-of-memory run, or one whose status a pipe swallowed (capture the test command's own status, e.g. `set -o pipefail` or the shell's pipe-status array), is no measurement (the foundation glossary term, WP03); never report it as pass or fail; re-run when the machine is quiet.
3. Put test temp and cache directories on storage with enough quota; a disk-full or quota error during a run is an environment failure, not a test result.
4. Attribute a red against the mission's recorded base commit: re-run the same test there before claiming the work package caused it (red on base: pre-existing, record it); never diff against your own first commit.
5. Record the command, the worker count and the outcome category with the result.
`failure_modes` mirror these. `notes`: complements no-parallel-duplicate-test-runs (one run per suite) and the no-fake-green reporting rule of the qa pack where it is active.

Fragment: node (`kind: tactics`, `body_path`); `tactic:no-parallel-duplicate-test-runs --suggests--> tactic:shared-machine-test-measurement`; `foundation::action:software-dev/implement --scope-->` and `.../review --scope-->` the tactic (no testing tactic is action-scoped today; scope this one directly, which SC-006 needs). `when` on each.

### T018 — Internal pointer

`targeted-mission-test-run` step "Bound parallel test runs": add one sentence pointing to the tactic for the machine-wide cap, no-measurement and base-commit attribution rules; this repository's host specifics stay there. Add the internal fragment edge `procedure:targeted-mission-test-run --suggests--> testing::tactic:shared-machine-test-measurement` (when).

## Definition of Done

Tactic validates, reachable at implement and review (SC-006); internal pointer present; gates green.
