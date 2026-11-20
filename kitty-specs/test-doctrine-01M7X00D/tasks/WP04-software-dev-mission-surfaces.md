---
work_package_id: WP04
title: Software-dev implement, review and specify surfaces carry both rules
dependencies:
- WP01
- WP03
requirement_refs:
- FR-007
- FR-008
- NFR-002
- SC-002
planning_base_branch: t3/test-doctrine-mock-boundary
merge_target_branch: t3/test-doctrine-mock-boundary
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-mock-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-mock-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T018
- T019
- T020
- T021
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/missions/software-dev/
create_intent: []
execution_mode: code_change
model: ""
owned_files:
- packs/foundation/missions/software-dev/steps/implement.prompt.md
- packs/foundation/missions/software-dev/steps/review.prompt.md
- packs/foundation/missions/software-dev/steps/specify.prompt.md
- packs/foundation/missions/software-dev/templates/spec-template.md
role: implementer
tags: []
tracker_refs:
- '#209'
- '#216'
---
# Work Package Prompt: WP04 – Software-dev implement, review and specify surfaces carry both rules

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

The software-dev mission's implement, review and specify steps and the spec template carry the carve-out, the `[evidenced-by-run]` label and the mock-boundary rule, by pointer to their owners (FR-007, FR-008, SC-002, NFR-004). **These files must stay ASCII** (NFR-002, `tests/ci/test_software_dev_ascii.py`): use `--` or `-`, straight quotes, no arrows. Read the WP03 results first: `034-test-first-development.directive.yaml` and `acceptance-criteria-non-vacuity.tactic.yaml` (the owners), and `054-mock-only-at-the-responsibility-boundary.directive.yaml`.

Check `tests/ci/test_prompt_fragments.py` and `tests/ci/test_analyze_readiness_prompts.py` for any string these tests pin in these files before you edit near it.

## Subtasks

### T018 implement.prompt.md

- Line 14 "Follow TDD practices, respect file ownership boundaries, ..." becomes "Follow test-first practice where it earns lasting value (DIRECTIVE_034), respect ...".
- Line 159 "2. Write tests first (TDD) when the subtask involves code changes" becomes: write tests first when the subtask changes behaviour with a lasting regression risk (product logic, gate or classifier scripts, invariants, security or permission policy); for configuration and glue work, record the real run or existing gate as `[evidenced-by-run]` evidence instead (DIRECTIVE_034). Keep step 3 ("Implement the code to pass the tests") consistent.
- In the subtask list or nearby, add one line: substitute only allow-listed seams in tests; run code the system under test owns for real (DIRECTIVE_054).
- Section "GitHub Actions Workflow Changes": add one sentence: the recorded run in `workflow-evidence.md` is the `[evidenced-by-run]` evidence for the workflow's shape; do not add tests that restate the workflow YAML. Logic the workflow calls (scripts, routers, gates) still gets red-first tests.

### T019 review.prompt.md

- Section 4a item 2 "Synthetic-fixture test" and item 4 "FR coverage": item 4 currently requires "at least one test assertion" for every FR; add the exception: an FR labelled `[evidenced-by-run]` is covered by the run or gate it names, which must exist; it needs no test.
- Add a new 4a item (keep numbering consistent, update any "A FAIL on any item" text if needed): **Mock boundary**: no test double in this WP's tests sits on code the system under test owns; every double is on an allow-listed seam of DIRECTIVE_054 (load with `spec-kitty charter context --include directive:DIRECTIVE_054`). Flag call-count or call-argument assertions on owned collaborators.
- Add a new 4a item: **Change detector**: no test only restates configuration or structure (it would fail only when someone changes the configuration on purpose). Flag such tests as waste, not as ATDD compliance; the evidence for configuration and glue work is a real run or an existing gate (DIRECTIVE_034; the long-term-value question in tactic `acceptance-criteria-non-vacuity`).
- Section 4b: add a fourth check: **Evidence exists**: for each id in this WP's `requirement_refs` whose spec.md row is labelled `[evidenced-by-run]`, the row names a run or gate, and the record exists (the run ID or URL in `workflow-evidence.md`, or the named gate in CI). State PASS / FAIL / N/A like the others. Update the lead-in at line ~211 ("apply its three rules") so it matches the tactic after WP03 (three rules plus the evidence check), without redefining the label.
- Keep wording short; one sentence per rule, naming the owner.

### T020 specify.prompt.md and spec-template.md

- `specify.prompt.md` line ~687: the summary label list `[build]` / `[ratchet]` / `[folded]` gains `[evidenced-by-run]` (no test; a real run or existing gate is the evidence, named in the row; no-op mark `n/a`). Line ~830: `[build/ratchet/folded]` becomes `[build/ratchet/folded/evidenced-by-run]`.
- `spec-template.md`: comment at line ~94 and the placeholders at lines ~116-118, ~155-160: same change. Keep the template comment saying the labels are defined once in the tactic.
- In the spec template, the no-op placeholder `[yes/no]` becomes `[yes/no/n-a]` (ASCII; match what the tactic says for `[evidenced-by-run]` rows).
- Search both files for any other `[build/ratchet/folded]` occurrence and update it the same way.

### T021 Gates

Restamp foundation (manifest, digest), built-in, pages; run all gates, in particular `python3 -m pytest -q tests/ci/test_software_dev_ascii.py tests/ci/test_prompt_fragments.py`. Evidence: `grep -n "Write tests first (TDD)\|Follow TDD practices" packs/foundation/missions/software-dev/steps/implement.prompt.md` returns nothing.

## Definition of Done

- implement, review, specify and the template agree with 034, the non-vacuity tactic and 054, by pointer.
- ASCII test passes; all gates exit 0.

## Reviewer guidance

Check the review step now checks evidence existence (abuse guard for the carve-out) and flags both defects. Check no label definition is duplicated beyond the one-line summaries that already existed.
## Branch Strategy

Planning and merge branch: `t3/test-doctrine-mock-boundary` (topology `single_branch`, no lane worktree; you work directly in the repository root checkout on that branch). The pull request goes from `t3/test-doctrine-mock-boundary` to `main`. Start with:

```bash
spec-kitty agent action implement WP04 --agent claude --mission test-doctrine-01M7X00D
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
- Commit with a conventional message ending in the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`, then `spec-kitty agent tasks move-task WP04 --to for_review --mission test-doctrine-01M7X00D --note "<evidence>"`. Do not push.
- Append one line to `kitty-specs/test-doctrine-01M7X00D/traces/tooling-friction.md` or `design-decisions.md` if you hit friction or make a non-obvious call (format `YYYY-MM-DD · claude-implementer · <text>`).
