---
work_package_id: WP07
title: Release surface - versions, restamps, pages, changelog
dependencies:
- WP01
- WP02
- WP03
- WP04
- WP05
- WP06
requirement_refs:
- FR-013
- NFR-001
- C-001
- SC-006
planning_base_branch: t3/test-doctrine-mock-boundary
merge_target_branch: t3/test-doctrine-mock-boundary
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-mock-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-mock-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T028
- T029
- T030
- T031
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: docs/changelog/
create_intent: []
execution_mode: code_change
model: ""
owned_files:
- packs/*/pack.yaml
- packs/*.source.yaml
- packs/*/pack-manifest.yaml
- docs/packs/*.md
- docs/changelog/CHANGELOG.md
- tests/ci/test_pack_digest.py
role: implementer
tags: []
tracker_refs:
- '#216'
- '#209'
- '#151'
---
# Work Package Prompt: WP07 – Release surface

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load implementer-ivan` (file: `packs/foundation/agent_profiles/implementer-ivan.agent.yaml`; read it in full) before reading anything else.

## Objective

Version the changed packs per DIRECTIVE_018 (minor, research.md R4), restamp everything, regenerate the pack pages and write the changelog entry (FR-013, NFR-001). Follow the precedent commit `6dce39c` ("version the readiness gate (additive)") exactly: run `git show 6dce39c` and mirror it.

This WP is glue work: its evidence is the gates (`[evidenced-by-run]`), not new tests.

## Subtasks

### T028 Versions

- Foundation lockstep set (foundation, writing, testing, refactoring, architecture, planning-analysis): `pack_version` 3.1.0 -> 3.2.0; every exact `==3.1.0` pin on them moves to `==3.2.0` (built-in and the lockstep members' own `depends_on`, plus any other pack that pins exactly; grep `==3.1.0` under `packs/`).
- built-in: 5.1.0 -> 5.2.0. qa: 5.0.0 -> 5.1.0, and narrow its foundation range to `>=3.2,<4` (its new edge names DIRECTIVE_054, which exists from foundation 3.2.0). internal: 4.1.0 -> 4.2.0 (its foundation range may stay: the foundation artefact its new edge names exists in 3.1.0). Any other pack whose files changed in this mission (check `git diff --stat origin/main -- packs/`) gets a minor bump. Only lockstep members and built-in carry `==3.1.0` pins.
- `>=2.0,<4` ranges already admit 3.2.0; do not change them.
- The `packs/<name>.source.yaml` sidecars hold only `tree_digest`; `pack_digest.py --update` restamps them.

### T029 Restamp

For every changed pack: `python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/<pack>`, then `python3 scripts/ci/pack_digest.py --update <pack>`; update `BUILT_IN_DIGEST` in `tests/ci/test_pack_digest.py`; `python3 scripts/docs/gen_pack_reference.py`.

### T030 Changelog

`docs/changelog/CHANGELOG.md` (the root `CHANGELOG.md` is a symlink), under `[Unreleased]`, in the house style of the existing entries (read the last three). Bold, impact-first lead with the issue refs, then before -> after. Cover:
- **Tests may mock only at the responsibility boundary (#216).** New foundation `DIRECTIVE_054` with the allow-list, and the `unfake-an-over-mocked-test` procedure; loads at implement and review and for the implementer, reviewer, generic and qa test-designer profiles; the seam lists in the testing tactics and styleguides now agree with it.
- **Red-first where it earns lasting value (#209).** DIRECTIVE_034 requires red-first for product logic, gate and classifier scripts, invariants and security or permission policy; for configuration and glue work a recorded real run or an existing gate is the evidence. New `[evidenced-by-run]` delivery label and the long-term-value question; review flags configuration-restatement tests as waste and checks the cited evidence exists. DIRECTIVE_041 allows retiring a change detector once its evidence is recorded.
- **A red that proves the right thing (#151).** `red-first-bug-reproduction` records the failure text, inverts a test that pins the defect, and splits a reproduction from its fix with a strict expected failure.
- **House example (internal).** The CI-workflow worked example.
- Versions line: the foundation lockstep 3.2.0, built-in 5.2.0, qa 5.1.0, internal 4.2.0 (and any others).
- Remaining #216 items (paradigm, assets, checklist de-duplication, curator profile) stay open.

### T031 Gates

Also run the charter checks if the jar can be fetched: `bash scripts/ci/charter_service_jar.sh` then `python3 scripts/ci/charter_service_check.py --jar <jar path>`, and `bash scripts/ci/charter_drift_test.sh <workdir>` (read each script header for exact usage). If either cannot run locally, say so in the evidence note; CI on the PR runs them, and the orchestrator pushes and opens the PR (SC-006 evidence is that CI run).

All gates, plus `python3 scripts/docs/check_docs_freshness.py --base origin/main` (bump `updated:` on any authored doc you touched; generated pack pages are exempt). Commit as `chore(packs): version the test doctrine (additive): the foundation lockstep 3.2.0, built-in 5.2.0, ... (#216, #209, #151)`.

## Definition of Done

Every changed pack bumped; manifests, digests, built-in constant and pages restamped; changelog entry present; all gates exit 0.
## Branch Strategy

Planning and merge branch: `t3/test-doctrine-mock-boundary` (topology `single_branch`, no lane worktree; you work directly in the repository root checkout on that branch). The pull request goes from `t3/test-doctrine-mock-boundary` to `main`. Start with:

```bash
spec-kitty agent action implement WP07 --agent claude --mission test-doctrine-01M7X00D
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
- Commit with a conventional message ending in the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`, then `spec-kitty agent tasks move-task WP07 --to for_review --mission test-doctrine-01M7X00D --note "<evidence>"`. Do not push.
- Append one line to `kitty-specs/test-doctrine-01M7X00D/traces/tooling-friction.md` or `design-decisions.md` if you hit friction or make a non-obvious call (format `YYYY-MM-DD · claude-implementer · <text>`).
