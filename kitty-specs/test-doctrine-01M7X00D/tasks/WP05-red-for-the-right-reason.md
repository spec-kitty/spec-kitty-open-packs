---
work_package_id: WP05
title: Red for the right reason, verifiably (#151)
dependencies:
- WP03
requirement_refs:
- FR-009
- SC-004
planning_base_branch: t3/test-doctrine-mock-boundary
merge_target_branch: t3/test-doctrine-mock-boundary
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-mock-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-mock-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T022
- T023
- T024
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/procedures/red-first-bug-reproduction.procedure.yaml
create_intent: []
execution_mode: code_change
model: ""
owned_files:
- packs/foundation/procedures/red-first-bug-reproduction.procedure.yaml
- packs/testing/procedures/test-first-bug-fixing.procedure.yaml
role: implementer
tags: []
tracker_refs:
- '#151'
- '#216'
---
# Work Package Prompt: WP05 – Red for the right reason, verifiably

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

Fold #151 and the #218 field note into the foundation `red-first-bug-reproduction` procedure, which becomes the single owner of three points (FR-009, SC-004, NFR-004):
(a) record the observed red failure text as evidence;
(b) when an existing characterization test pins the defect, invert that test rather than adding a parallel one;
(c) a reproduction that lands in a different work package from its fix is marked as a strict expected failure (in pytest, `@pytest.mark.xfail(strict=True)`), so intermediate commits stay green; the fix's work package removes the marker, and strictness forces that flip.
The red-shape point (a red that does not break collection; import a fix-introduced symbol lazily inside the test) is already owned by DIRECTIVE_034 integrity rule 3; the procedure cites DIRECTIVE_034 for it and does not restate it beyond one clause. Its current step 1 restates it at length: shorten that to a pointer.

Language-neutral wording; the pytest marker is an example, not the rule.

## Subtasks

### T022 `red-first-bug-reproduction` (foundation)

File: `packs/foundation/procedures/red-first-bug-reproduction.procedure.yaml`.
- Step 1 "Write the reproduction test through the pre-existing entry point": keep the entry-point rule; replace the long red-shape explanation with one clause pointing to DIRECTIVE_034's rule.
- New step before step 1 or merged into it: "Invert a test that pins the defect": if an existing (characterization) test asserts the buggy behaviour, that test is the reproduction anchor: invert its assertion to the correct behaviour instead of writing a parallel test (tactic `delete-the-assertion-not-the-test` covers how; name it, do not restate it).
- Step 2 "Prove red-first, then green": add "record the observed failure text (the assertion message or error output) in the work package's evidence, so a reviewer can confirm it failed for the bug's symptom".
- New step "Split across work packages": when the reproduction lands in an earlier work package than the fix, mark it as a strict expected failure naming the fixing work package; the fix removes the marker, and strictness turns a premature pass into a failure. This is not masking a defect (DIRECTIVE_041).
- Update `exit_condition` to mention the recorded failure text.

### T023 testing `test-first-bug-fixing`

File: `packs/testing/procedures/test-first-bug-fixing.procedure.yaml`.
- Step "Verify the test fails for the right reason": add one sentence: record the failure text, and see procedure `red-first-bug-reproduction` (foundation) for the full rules (red shape, characterization inversion, cross-work-package split).
- Step "Commit test and fix together" and the `exit_condition`: add the second carve-out in one clause: or, in a mission that splits the reproduction and the fix across work packages, the reproduction lands first as a strict expected failure (procedure `red-first-bug-reproduction`).
- Do not restate the rules.

### T024 Gates

Restamp foundation and testing (manifest, digest), built-in, pages; run all gates. Evidence: `grep -rn -i "failure text" packs/foundation packs/testing` shows the owner and only pointers elsewhere.

## Definition of Done

Each of (a), (b), (c) appears fully in exactly one artefact (`red-first-bug-reproduction`); the red-shape point is fully stated only in DIRECTIVE_034; all gates exit 0.

## Reviewer guidance

Check (c) is consistent with DIRECTIVE_041's edited criterion and `observable-contract-test-authoring` (WP03). Check nothing duplicates `delete-the-assertion-not-the-test`.
## Branch Strategy

Planning and merge branch: `t3/test-doctrine-mock-boundary` (topology `single_branch`, no lane worktree; you work directly in the repository root checkout on that branch). The pull request goes from `t3/test-doctrine-mock-boundary` to `main`. Start with:

```bash
spec-kitty agent action implement WP05 --agent claude --mission test-doctrine-01M7X00D
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
- Commit with a conventional message ending in the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`, then `spec-kitty agent tasks move-task WP05 --to for_review --mission test-doctrine-01M7X00D --note "<evidence>"`. Do not push.
- Append one line to `kitty-specs/test-doctrine-01M7X00D/traces/tooling-friction.md` or `design-decisions.md` if you hit friction or make a non-obvious call (format `YYYY-MM-DD · claude-implementer · <text>`).
