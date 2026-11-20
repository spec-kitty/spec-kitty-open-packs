---
work_package_id: WP02
title: Every seam list agrees with DIRECTIVE_054
dependencies:
- WP01
requirement_refs:
- FR-003
- FR-004
- SC-003
- NFR-004
planning_base_branch: t3/test-doctrine-mock-boundary
merge_target_branch: t3/test-doctrine-mock-boundary
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-mock-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-mock-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T007
- T008
- T009
- T010
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/tactics/testing/
create_intent: []
execution_mode: code_change
model: ""
owned_files:
- packs/foundation/tactics/testing/test-boundaries-by-responsibility.tactic.yaml
- packs/foundation/tactics/testing/test-scaffolding-as-design-smell.tactic.yaml
- packs/foundation/tactics/testing/black-box-integration-testing.tactic.yaml
- packs/foundation/tactics/testing/function-over-form-testing.tactic.yaml
- packs/foundation/tactics/testing/testing-select-appropriate-level.tactic.yaml
- packs/testing/styleguides/test-desiderata-and-boundaries.styleguide.yaml
- packs/testing/styleguides/testing-principles.styleguide.yaml
- packs/qa/drg/fragment.yaml
role: implementer
tags: []
tracker_refs:
- '#216'
---
# Work Package Prompt: WP02 – Every seam list agrees with DIRECTIVE_054

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

Every surface that lists mock seams or mocking rules either names `DIRECTIVE_054` as the owner of the seam list or states seams that are a subset of its eight allow-list categories, and none says a seam *must* be mocked (FR-003, SC-003). Wire the qa test designer to 054 (FR-004, cross-pack). Read the new `packs/foundation/directives/054-mock-only-at-the-responsibility-boundary.directive.yaml` (from WP01) and research.md R1/R2 first.

The eight allow-list categories: another domain or bounded context; filesystem; database; network and external APIs; clock; randomness; git and other processes; narrow system cases (DTO validation, hook or notification sends).

## Subtasks

### T007 `test-boundaries-by-responsibility` (foundation)

- Step "Classify dependencies" (line ~15-17): replace "Outside boundary (DO mock/stub): database access, external APIs, filesystem, network, time providers, services outside the current module." with wording that (a) says outside-boundary dependencies *may* be substituted, (b) lists them as the DIRECTIVE_054 allow-list or simply says "the allow-listed seams of DIRECTIVE_054", and (c) drops "services outside the current module" (a module line is not a responsibility line; another bounded context is the allow-listed case).
- Step "Map responsibility boundaries": "Mark ... outside-boundary (stubbed)" becomes "(may be substituted)".
- Step "Verify boundary correctness" question (2): "(No, they are stubbed.)" becomes neutral ("No; they sit outside the boundary").
- `failure_modes` line ~31 "Insufficient isolation: not stubbing external dependencies, causing slow and fragile tests." makes substitution sound required: reword to "Slow or flaky real dependencies: a real external dependency that makes the test slow or nondeterministic; substitute it at an allow-listed seam (substitution is permitted, never required)."
- `failure_modes`: add one entry: "Pinning a call contract on owned logic: a double of a collaborator inside the boundary, asserted on its calls; it can manufacture states the real path never reaches (DIRECTIVE_054)."
- Keep the rest.

### T008 Other foundation tactics

Read each file and change only the sentences that list seams or tell the reader to mock:
- `test-scaffolding-as-design-smell.tactic.yaml` lines 5-8 say a unit test that "needs real infrastructure (files, git, database ...)" is evidence of a missing boundary. This contradicts DIRECTIVE_054 rule 2 (real files and a real git repository are always allowed). Change it: the smell is heavy scaffolding (many doubles, elaborate setup) or any double of owned logic; a real dependency is a problem only when it makes the test slow or flaky, and then the remedy is a pure seam or an allow-listed substitute. Must change; do not skip.
- `black-box-integration-testing.tactic.yaml` line 77 "Insufficient substitution -- refusing to stub ..." makes substitution sound required: reword so the failure is a slow or nondeterministic real dependency left in, and the seam is "an allow-listed seam of DIRECTIVE_054". Must change.
- `function-over-form-testing.tactic.yaml` (around line 57): if it describes the interaction-to-outcome shift, add at most one sentence naming DIRECTIVE_054's anti-pattern; do not restate the allow-list.
- `testing-select-appropriate-level.tactic.yaml` (around lines 13, 20): align level descriptions that say "mock X" to "substitute only allow-listed seams (DIRECTIVE_054)".
If a file has no conflicting sentence, leave it unchanged and say so in the evidence note.

### T009 Testing pack styleguides

- `packs/testing/styleguides/test-desiderata-and-boundaries.styleguide.yaml`:
  - lines 49-50 ("Stub infrastructure at the boundary: external services, data access, and IO (filesystem, database, clock, network, randomness, git) live OUTSIDE the boundary and are replaced by test doubles or pure inputs"): keep, but "may be replaced", and add "the allow-list is owned by DIRECTIVE_054".
  - lines 53-54 ("Heavy scaffolding signals a wrong boundary ... testable without IO"): keep the scaffolding smell, but say real IO itself is allowed (054); the smell is heavy setup or doubles of owned logic.
  - lines 175-179 and 244-248 ("mock only at true system boundaries"; the `quality_test` "at most one mock ... real files, a git repo ... boundary in the wrong place"): make consistent with 054 (real files and a real git repo in a temp dir are allowed; a double of owned logic is the smell).
  - the Beck "Isolated" principle already exists at lines 22-23: extend that entry with one clause (Isolated does not mean isolating the unit from its collaborators with mocks); do not add a duplicate.
  - Keep the file's YAML shape.
- `packs/testing/styleguides/testing-principles.styleguide.yaml` (lines ~26-27, 134-138): it says mock boundaries have "one owner", namely `test-desiderata-and-boundaries`. Change the owner of the seam list to DIRECTIVE_054 (foundation); `test-desiderata-and-boundaries` stays the owner of the desiderata.
- Cross-pack references from testing to foundation are by name in prose; no fragment edge is required here.

### T010 qa test designer edge, then gates

- `packs/qa/drg/fragment.yaml`: add `agent_profile:qa-test-designer-tessa suggests foundation::directive:DIRECTIVE_054` with `when` ("designing tests and choosing which collaborators to substitute") and a one-sentence `reason`. Follow the file's existing cross-pack edge format (look for other `foundation::` edges). One edge per pair.
- Restamp foundation, testing and qa (manifest, digest), built-in digest if needed, pages; run all gates.
- Evidence note: a grep proving no "DO mock" / "services outside the current module" remains: `grep -rn -i "DO mock\|services outside the current module" packs` (expect nothing).

## Definition of Done

- SC-003 holds for every file in owned_files plus DIRECTIVE_036 (done in WP01).
- No surface says a seam must be mocked.
- qa edge present; all gates exit 0.

## Reviewer guidance

Read each changed seam sentence against 054's integrity rule 1. Check no second full copy of the allow-list was introduced (NFR-004): a surface either names 054 or lists a subset.
## Branch Strategy

Planning and merge branch: `t3/test-doctrine-mock-boundary` (topology `single_branch`, no lane worktree; you work directly in the repository root checkout on that branch). The pull request goes from `t3/test-doctrine-mock-boundary` to `main`. Start with:

```bash
spec-kitty agent action implement WP02 --agent claude --mission test-doctrine-01M7X00D
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
- Commit with a conventional message ending in the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`, then `spec-kitty agent tasks move-task WP02 --to for_review --mission test-doctrine-01M7X00D --note "<evidence>"`. Do not push.
- Append one line to `kitty-specs/test-doctrine-01M7X00D/traces/tooling-friction.md` or `design-decisions.md` if you hit friction or make a non-obvious call (format `YYYY-MM-DD · claude-implementer · <text>`).
