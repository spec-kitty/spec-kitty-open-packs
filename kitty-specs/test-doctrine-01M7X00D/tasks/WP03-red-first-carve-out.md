---
work_package_id: WP03
title: Red-first scoped to lasting regression risk (directives, tactics, profile)
dependencies:
- WP01
requirement_refs:
- FR-005
- FR-006
- FR-007
- FR-010
- C-003
- C-004
- SC-002
planning_base_branch: t3/test-doctrine-mock-boundary
merge_target_branch: t3/test-doctrine-mock-boundary
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-mock-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-mock-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T011
- T012
- T013
- T014
- T015
- T016
- T017
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/directives/034-test-first-development.directive.yaml
create_intent: []
execution_mode: code_change
model: ""
owned_files:
- packs/foundation/directives/034-test-first-development.directive.yaml
- packs/foundation/directives/041-tests-as-scaffold-not-friction.directive.yaml
- packs/foundation/tactics/testing/acceptance-criteria-non-vacuity.tactic.yaml
- packs/foundation/tactics/testing/acceptance-test-first.tactic.yaml
- packs/foundation/tactics/testing/tdd-red-green-refactor.tactic.yaml
- packs/foundation/procedures/test-first-cycle.procedure.yaml
- packs/foundation/procedures/observable-contract-test-authoring.procedure.yaml
- packs/foundation/agent_profiles/reviewer-renata.agent.yaml
- packs/foundation/directives/039-lynn-cole-engineering-culture.directive.yaml
- packs/testing/tactics/testing/atdd-adversarial-acceptance.tactic.yaml
role: implementer
tags: []
tracker_refs:
- '#209'
---
# Work Package Prompt: WP03 – Red-first scoped to lasting regression risk

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

DIRECTIVE_034 owns the carve-out: red-first is required for behaviour with a lasting regression risk; for configuration and glue work a recorded real run or an existing gate is the evidence instead of a test. The non-vacuity tactic owns the `[evidenced-by-run]` label and the long-term-value question. The ATDD/TDD tactics, the test-first procedure, DIRECTIVE_041, `observable-contract-test-authoring`, reviewer-renata and the testing pack's `atdd-adversarial-acceptance` agree, each in at most one sentence naming the owner (FR-005, FR-006, FR-007 part, FR-010, NFR-004, SC-002). Operator ruling (binding): evidence REPLACES the test for config/glue work; reviewers flag pure config-restatement tests as waste. Non-vacuity still applies to every test that is written.

Read research.md R1 and R2 first.

## Subtasks

### T011 DIRECTIVE_034 (owner of the carve-out)

File: `packs/foundation/directives/034-test-first-development.directive.yaml`. Keep id, title, `enforcement`, and integrity rule 3 (the bug-reproduction shape rule, which owns the "red shape that keeps collection working" point) word for word. Rewrite:
- `intent`: test-first where it earns lasting value: the test defines the contract before production code for behaviour a future edit could break unnoticed. Where a real run or an existing gate already proves configuration or glue work, that evidence stands in for the test.
- `scope`: add configuration and glue work (CI workflow shape, wiring, settings files) to the scope, so the carve-out is inside the directive, not outside it.
- integrity rule 1 (line 13, "Production code must not be written ahead of a failing test that motivates it.") becomes: red-first is required for behaviour with a lasting regression risk: product logic, gate and classifier scripts, invariants that must hold across future edits, and security or permission policy. For that behaviour, production code is not written ahead of a failing test that motivates it.
- new rule: for configuration and glue work without that risk, a recorded real run (for example the first run of a new workflow on a real runner) or an existing gate is the evidence; no test is written to restate the configuration. The requirement is labelled `[evidenced-by-run]` and names the run or gate (tactic `acceptance-criteria-non-vacuity`). Configuration that encodes a security or permission policy carries lasting regression risk and is not glue: it gets red-first or a general policy check.
- integrity rule 2 (line 14, "Skipping the test-first cycle requires explicit justification in the commit or PR.") is replaced (one mechanism): work that takes the carve-out names its evidence; work with neither a test nor named evidence does not conform.
- `validation_criteria` line 17 ("Each new behavior has a corresponding test that was written before the production code.") becomes: each new behaviour with a lasting regression risk has a test written before the production code, and each `[evidenced-by-run]` item cites a run or gate that exists. Keep the bug-fix criterion (line 18).
- Keep the trailing YAML comment block. No enforcement prose (C-006).

### T012 `acceptance-criteria-non-vacuity` (owner of the label and the question)

File: `packs/foundation/tactics/testing/acceptance-criteria-non-vacuity.tactic.yaml`.
- `purpose` (line ~10) says "the delivery labels, the no-op-passable mark, and the three rules": update it to cover four labels and the added "does red mean broken" question (keep "the three rules" for the three non-vacuity rules if they stay three, and say the new step is a question, not a fourth rule).
- Step "Label every criterion": add `[evidenced-by-run]` (no test is written; a real run or an existing gate is the evidence; name it, and where the record lives: for a workflow, the mission's `workflow-evidence.md`; for a gate, the gate's name). Only for work without lasting regression risk (DIRECTIVE_034). Its no-op mark is `n/a` with the evidence named.
- New step after "Ask no-op passable?", title "Ask whether red means broken": next to "could this test fail?" (no-op passable), ask "when it fails, does that mean something is broken?" and the long-term-value question: "Would this test still catch a real regression in six months, or would it only fail when someone changes the configuration on purpose?" A test that only restates configuration or structure is a change detector: do not write it; where one exists and the evidence is recorded, retire it (DIRECTIVE_041). Example: a test pinning a CI job's name, runner and timeout is a change detector; a test of the routing logic that job calls is not.
- `failure_modes`: add "Change detector: a test that restates configuration, goes red only because the configuration does not exist yet, and afterwards fails only on intentional change." and "Evidence by assertion: an `[evidenced-by-run]` row that names no run or gate, or one that does not exist."
- `notes` canonical legend: add the `[evidenced-by-run]` definition and the `n/a` no-op mark; add the long-term-value question there too (it is the canonical home).

### T013 ATDD and TDD tactics, test-first procedure

- `acceptance-test-first.tactic.yaml`: purpose gains "for behaviour with a lasting regression risk (DIRECTIVE_034)". Step "Document manual fallbacks": add one sentence: where a real run or existing gate is the evidence (configuration and glue work), record it under `[evidenced-by-run]` instead of writing an acceptance test (tactic `acceptance-criteria-non-vacuity`).
- `tdd-red-green-refactor.tactic.yaml`: line 25 example "block merge when new code has no corresponding tests" becomes "block merge when new logic has no corresponding tests". Step "Red": nothing else; the tactic applies to logic.
- `test-first-cycle.procedure.yaml`: description "Drive every production change from a failing test." becomes "Drive each production change that carries a lasting regression risk from a failing test; record real-run or gate evidence for configuration and glue work (DIRECTIVE_034)." Entry/exit conditions and step 2 aligned in the same way (one clause each). Step 1 "Select the test-first tactic for the scope": first decide whether the change carries a lasting regression risk; if not, record the evidence and skip the test.

### T014 testing `atdd-adversarial-acceptance`

File: `packs/testing/tactics/testing/atdd-adversarial-acceptance.tactic.yaml`. Step "Triage failure scenarios": add to the selection criteria that a candidate must carry a lasting regression risk, and apply the long-term-value question (tactic `acceptance-criteria-non-vacuity`, by name). `failure_modes`: add "Pinning configuration shape as an acceptance test: a change detector, not an adversarial boundary." Keep the C-006 note as it is.

### T015 DIRECTIVE_041 (minimal, C-003)

File: `packs/foundation/directives/041-tests-as-scaffold-not-friction.directive.yaml`. Only two edits:
- integrity rule line 18: keep "never delete a test to dodge a failure — replace the assertion red-first with coverage preserved" and add: a change-detector test (it restates configuration and guards no lasting behaviour) may be retired once the real-run or gate evidence that replaces it is recorded (DIRECTIVE_034); retiring it is not dodging a failure.
- validation criterion line 23: "No new xfail or skip masks a known defect" gains: a strict expected failure on a bug reproduction whose fix is planned in a named sibling work package is not a mask (procedure `red-first-bug-reproduction`).
Do not change intent, title, enforcement or other rules. No new graph edge (041 requires 034 already exists).

### T016 `observable-contract-test-authoring`, reviewer-renata and DIRECTIVE_039

- `packs/foundation/directives/039-lynn-cole-engineering-culture.directive.yaml` line ~15 ("three rules of TDD, and hold them sacred"): add one clause pointing to DIRECTIVE_034 for scope (TDD for behaviour with a lasting regression risk; real-run or gate evidence for configuration and glue). Change nothing else in 039.

- `packs/foundation/procedures/observable-contract-test-authoring.procedure.yaml` step "Pin desired behavior instead of masking defects": add the same cross-work-package strict expected failure exception in one sentence, naming `red-first-bug-reproduction`.
- `packs/foundation/agent_profiles/reviewer-renata.agent.yaml`:
  - `041` rationale (line ~132): "no defect-masking xfails" gains "(a strict expected failure on a reproduction whose fix is planned in a sibling work package is not a mask)" and "flag pure configuration-restatement tests as waste, not ATDD compliance".
  - add a `054` directive-reference entry (name "Mock Only at the Responsibility Boundary", rationale: reject doubles of code the system under test owns; accept only allow-listed seams).
  - if a `034` entry exists, align its rationale with the carve-out (accept `[evidenced-by-run]` evidence for config/glue work; require red-first for lasting regression risk); if it does not, add one.
  - `test-scaffolding-as-design-smell` rationale (line ~154): "many infrastructure mocks" becomes "many doubles, or any double of owned logic (DIRECTIVE_054)".
  - Keep the YAML format of the list.

### T017 Gates

Restamp foundation and testing (manifest, digest), built-in digest and constant if needed, pages; run all gates. Evidence: `grep -n "every production change\|Each new behavior has" packs/foundation -r` returns nothing.

## Definition of Done

- 034 states the scope, the carve-out and the evidence rule; its old "explicit justification" rule is gone; rule 3 unchanged.
- Non-vacuity tactic defines four labels and owns the long-term-value question; no other file in this WP restates the question in full.
- 041 changed in exactly two places.
- All gates exit 0.

## Reviewer guidance

Check the carve-out cannot be read as "config work needs no evidence". Check a security or permission policy in config is explicitly kept under red-first. Check NFR-004 (the label legend is defined only in the non-vacuity tactic). Diff 041 and confirm only the two edits.
## Branch Strategy

Planning and merge branch: `t3/test-doctrine-mock-boundary` (topology `single_branch`, no lane worktree; you work directly in the repository root checkout on that branch). The pull request goes from `t3/test-doctrine-mock-boundary` to `main`. Start with:

```bash
spec-kitty agent action implement WP03 --agent claude --mission test-doctrine-01M7X00D
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
- Commit with a conventional message ending in the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`, then `spec-kitty agent tasks move-task WP03 --to for_review --mission test-doctrine-01M7X00D --note "<evidence>"`. Do not push.
- Append one line to `kitty-specs/test-doctrine-01M7X00D/traces/tooling-friction.md` or `design-decisions.md` if you hit friction or make a non-obvious call (format `YYYY-MM-DD · claude-implementer · <text>`).
