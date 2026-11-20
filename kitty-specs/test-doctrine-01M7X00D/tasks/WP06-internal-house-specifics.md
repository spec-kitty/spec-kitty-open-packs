---
work_package_id: WP06
title: Spec Kitty house specifics in the internal pack
dependencies:
- WP03
requirement_refs:
- FR-011
- C-002
- SC-005
planning_base_branch: t3/test-doctrine-mock-boundary
merge_target_branch: t3/test-doctrine-mock-boundary
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-mock-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-mock-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T025
- T026
- T027
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/internal/
create_intent:
- packs/internal/tactics/spec-kitty-ci-workflow-evidence-exemplar.tactic.yaml
execution_mode: code_change
model: ""
owned_files:
- packs/internal/tactics/spec-kitty-ci-workflow-evidence-exemplar.tactic.yaml
- packs/internal/drg/fragment.yaml
- packs/internal/procedures/cloud-session-dispatch.procedure.yaml
- packs/internal/procedures/landing-contributor-prs.procedure.yaml
- packs/internal/skills/mission-from-issue.skill.md
- packs/internal/presets/base.yaml
- packs/internal/README.md
role: implementer
tags: []
tracker_refs:
- '#209'
---
# Work Package Prompt: WP06 – Spec Kitty house specifics in the internal pack

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

Operator ruling (tier split): the general rule lives in foundation; Spec Kitty's own CI-workflow worked example lives in `internal`. Add an internal tactic with that example, wire it, and align the internal surfaces that say "ATDD-first" or "red-first" to the carve-out by pointer (FR-011, SC-005). Read the WP03 results: `packs/foundation/directives/034-test-first-development.directive.yaml` and `packs/foundation/tactics/testing/acceptance-criteria-non-vacuity.tactic.yaml`.

## Subtasks

### T025 New internal tactic

File: `packs/internal/tactics/spec-kitty-ci-workflow-evidence-exemplar.tactic.yaml`. Shape: like `spec-kitty-gate-non-vacuity-exemplar.tactic.yaml` (`schema_version`, `id`, `name`, `purpose`, `steps`, optional `failure_modes`, `notes`). Name: "Spec Kitty CI Workflow Evidence Exemplar". Purpose: shows, on a Spec Kitty CI change, which red-first pins are change detectors to drop and which tests guard lasting behaviour, applying DIRECTIVE_034's carve-out and the `[evidenced-by-run]` label of `acceptance-criteria-non-vacuity`.

Worked example (from a docs-site build mission in Spec Kitty core that added a shared docs-site build job and a router gate; describe it in prose; Spec Kitty's own pack may name the kind of file, e.g. "the CI test module for the docs-site job", but avoid core issue numbers):
- Drop (change detectors; the first real run of the workflow is the evidence, recorded in `workflow-evidence.md`): pins on the router job's reusable-workflow `uses:` target; the build job's name, `runs-on`, timeout and command substrings; the upload step's `if:` expressions.
- Keep (lasting regression risk): the router gate's behaviour tests (its main entry point, driven with real inputs); the path-to-job routing cases; the invariant "no automated trigger, no secrets, read-only permissions", which is security and fork-safety policy and is better expressed as one general workflow-policy check over every workflow than as a per-file pin.
- Steps: (1) classify each proposed test by the long-term-value question; (2) for workflow shape, push to a draft PR and record the first successful real-runner run (the implement step's workflow-evidence rule); (3) write red-first tests for the scripts the workflow calls; (4) express permission and secret policy as a repository-wide check; (5) label the requirement rows accordingly.
- Note at the end: the general rule lives in foundation DIRECTIVE_034 and `acceptance-criteria-non-vacuity`; this tactic is the house example only.

### T026 Wiring

- `packs/internal/drg/fragment.yaml`: add the node entry (id, `kind: tactics`, title, `body_path`) next to the gate exemplar, and the edge `tactic:spec-kitty-ci-workflow-evidence-exemplar refines foundation::tactic:acceptance-criteria-non-vacuity` (same pattern as the gate exemplar's `refines` edge). Add a `when` if sibling edges have one. Make the node reachable from an activatable internal artefact if the precedent does so (check how `spec-kitty-gate-non-vacuity-exemplar` is reached: an inbound edge, a preset entry, or nothing); follow the precedent, and if it needs a preset entry, edit `presets/base.yaml`.
- `packs/internal/README.md`: if it lists the internal tactics, add the new one in the same format.

### T027 Internal surfaces point to the carve-out, then gates

- `procedures/cloud-session-dispatch.procedure.yaml` line ~39 "feature: ATDD-first, with the canonical mission templates ..." becomes "feature: ATDD-first for behaviour with a lasting regression risk; real-run or gate evidence for configuration and glue (DIRECTIVE_034), with the canonical mission templates ...". The bugfix line (~33) stays.
- `procedures/landing-contributor-prs.procedure.yaml` step "Hold every landing fix to the test economy": add one clause: a test that only restates configuration is a change detector; a real run or existing gate is the evidence (DIRECTIVE_034, and the long-term-value question of `acceptance-criteria-non-vacuity`). Keep the rest.
- `skills/mission-from-issue.skill.md` step 5 "implement red-first with ..." becomes "implement red-first where the change carries a lasting regression risk (record real-run or gate evidence for configuration and glue work) with ...". If a companion `.skill.yaml` holds a digest or hash of the body, update it the way the repo expects (check `scripts/ci/validate_pack_schemas.py` handling of skills).
- Restamp internal (manifest, digest), pages; run all gates.

## Definition of Done

New tactic validates and is wired like its sibling; three internal surfaces point to the carve-out; no Spec Kitty CI wording was added to foundation or testing; all gates exit 0.

## Reviewer guidance

Check the example matches #209's table (drop vs keep) and that the internal tactic does not restate the general rule beyond a pointer.
## Branch Strategy

Planning and merge branch: `t3/test-doctrine-mock-boundary` (topology `single_branch`, no lane worktree; you work directly in the repository root checkout on that branch). The pull request goes from `t3/test-doctrine-mock-boundary` to `main`. Start with:

```bash
spec-kitty agent action implement WP06 --agent claude --mission test-doctrine-01M7X00D
```

## Working rules (every WP)

- This repository aligns to the charter (pin in `charter.lock.yaml`), not to spec-kitty core. Core compatibility is never a blocker (AGENTS.md).
- Read research.md R1 (owner map) before writing. A rule has exactly one owner; any other surface states it in at most one sentence and names the owner (NFR-004).
- Consumer packs (foundation, testing, qa) name no core issue numbers, core PR numbers or core repository paths (NFR-003). Write examples neutrally.
- Directive bodies never say how strictly they bind ("this directive is required/binding/mandatory", "remains advisory", "enforcement `required`"); the `enforcement:` field carries that (C-006, `scripts/ci/check_vocabulary.py`).
- Software-dev mission files (`packs/foundation/missions/software-dev/**`) stay ASCII (NFR-002): no em dashes, curly quotes or arrows there.
- Plain, direct prose; one idea per sentence; no marketing words. Match the house style of the file you edit.
- No new tests (plan design decision 8). The evidence for this content work is the existing gates; record the commands and their result in the WP's evidence note (the move-task `--note`).
- **Gate companions in the same commit.** For every pack you touch: `git add` new files first (the digest counts tracked files only), then `python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/<pack>` and `python3 scripts/ci/pack_digest.py --update <pack>`. If you touch a built-in member pack (foundation, testing, writing, refactoring, architecture, planning-analysis), also run `python3 scripts/ci/pack_digest.py --update built-in` if it reports drift and update `BUILT_IN_DIGEST` in `tests/ci/test_pack_digest.py` when `pytest tests/ci/test_pack_digest.py` says so; regenerate pages with `python3 scripts/docs/gen_pack_reference.py`. Manifests, digests, pages and the digest constant are out-of-map edits for every WP, with the rationale "gate companion, so each commit stays green"; WP07 owns the version bumps.
- Gates before you hand off (activate `.venv` first: `source .venv/bin/activate`): `bash scripts/ci/validate-packs.sh`, `python3 -m pytest -q tests`, `python3 scripts/ci/check_vocabulary.py`, `python3 scripts/docs/gen_pack_reference.py --check`, `bash scripts/ci/check-pack-digests.sh`. All must exit 0.
- Commit with a conventional message ending in the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`, then `spec-kitty agent tasks move-task WP06 --to for_review --mission test-doctrine-01M7X00D --note "<evidence>"`. Do not push.
- Append one line to `kitty-specs/test-doctrine-01M7X00D/traces/tooling-friction.md` or `design-decisions.md` if you hit friction or make a non-obvious call (format `YYYY-MM-DD · claude-implementer · <text>`).
