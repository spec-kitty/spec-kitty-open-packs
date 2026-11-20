---
work_package_id: WP01
title: Mock-boundary directive, remediation procedure and graph wiring
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-004
- FR-012
- FR-003
- C-005
- C-006
- NFR-003
- SC-001
planning_base_branch: t3/test-doctrine-mock-boundary
merge_target_branch: t3/test-doctrine-mock-boundary
branch_strategy: Planning artifacts for this mission were generated on t3/test-doctrine-mock-boundary. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/test-doctrine-mock-boundary unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/directives/
create_intent:
- packs/foundation/directives/054-mock-only-at-the-responsibility-boundary.directive.yaml
- packs/foundation/procedures/unfake-an-over-mocked-test.procedure.yaml
execution_mode: code_change
model: ""
owned_files:
- packs/foundation/directives/054-mock-only-at-the-responsibility-boundary.directive.yaml
- packs/foundation/directives/036-black-box-integration-testing.directive.yaml
- packs/foundation/procedures/unfake-an-over-mocked-test.procedure.yaml
- packs/foundation/directive.graph.yaml
- packs/foundation/procedure.graph.yaml
- packs/foundation/action.graph.yaml
- packs/foundation/agent_profile.graph.yaml
- packs/foundation/glossaries/spec-kitty-core.glossary.yaml
- packs/foundation/agent_profiles/implementer-ivan.agent.yaml
role: implementer
tags: []
tracker_refs:
- '#216'
---
# Work Package Prompt: WP01 – Mock-boundary directive, remediation procedure and graph wiring

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Objective

Create `DIRECTIVE_054` "Mock Only at the Responsibility Boundary" and the `unfake-an-over-mocked-test` procedure in the foundation pack, add the two glossary terms, point DIRECTIVE_036 at 054, and wire 054 into the doctrine graph so it loads when tests are written or reviewed (FR-001, FR-002, FR-004, FR-012; part of FR-003 for 036). Read `kitty-specs/test-doctrine-01M7X00D/spec.md`, `plan.md` and `research.md` (R1, R3, R5, R6) first.

## Subtasks

### T001 Author DIRECTIVE_054

File: `packs/foundation/directives/054-mock-only-at-the-responsibility-boundary.directive.yaml` (new). Shape: same keys as `052-prefer-durable-fixes.directive.yaml` (`schema_version`, `id`, `title`, `intent`, `enforcement`, `scope`, `integrity_rules`, `validation_criteria`). `enforcement: required`. Do not add inline `references:`; relationships are graph edges (T005).

Content (adapt wording to the house style, keep every point):

- **intent**: A test substitutes a collaborator only where control leaves the system under test: at its responsibility boundary. Everything the system under test owns for the behaviour under test runs for real, and assertions target observable outcomes. A double of owned logic couples the test to an implementation shape, and it can manufacture a state the real code path never reaches, so the test raises false alarms or gives false confidence.
- **scope**: all automated tests at every level (unit, integration, acceptance) that use test doubles (mocks, stubs, fakes, spies, monkeypatches). The boundary is drawn by responsibility for the behaviour under test, not by layer, module or class (point to tactic `test-boundaries-by-responsibility` by name for how to draw it, one clause).
- **integrity_rules** (one rule per bullet):
  1. The allow-list, exhaustive. A test may substitute only: another domain or bounded context (a domain-contract seam); the filesystem; a database; the network and external APIs or services; the clock; randomness; git and other processes or subprocesses; and narrow system cases, such as plain DTO validation or sending a hook or notification. Everything else inside the boundary runs for real.
  2. The allow-list permits a substitute; it never requires one. Running a real collaborator from the list (a temporary directory, an in-memory database, a real git repository in a temp dir) is always allowed.
  3. A test must not mock, stub, patch or spy on code the system under test owns in order to pin a call contract (which helper was called, how often, with which arguments). Name this anti-pattern: "pinning a call contract on owned logic".
  4. A substitute at the boundary preserves the observable contract of the real dependency, including the states it can and cannot produce. A substitute shaped only for the one scenario the author imagined moves the anti-pattern one step out.
  5. When a test seems to need a double of owned logic, the boundary is drawn wrong: widen the slice to include the collaborator, or extract a pure seam that takes domain inputs. Do not add the double.
  6. Assertions target observable outcomes (returned values, persisted state, written files, emitted events or messages), not the call graph of owned collaborators. A spy on an allow-listed seam may assert what crossed the boundary (for example the set of paths handed to a git write), because that is an outcome at the boundary.
- **validation_criteria**:
  - Every test double in a new or changed test sits on an allow-listed seam, and the test (name, docstring or an adjacent comment) makes it possible to tell which collaborators run for real and which are substituted.
  - No new or changed test asserts on the call count, call order or call arguments of a collaborator the system under test owns.
  - An over-mocked test found during the change is remediated with `unfake-an-over-mocked-test` (name the procedure once) or recorded as a tracked follow-up.
- **Worked example** (put it in the intent or as the last integrity rule's explanation, neutral wording, no issue numbers, no core paths): A regression test for a merge step stubbed the step that marks finished work packages as done, to assert it was called once with the expected ids. With that step stubbed, the mission under test recorded no status events at all, a state the real merge never produces. A later step correctly skipped the missing event log, the test failed on the missing file, and the failure was investigated as data loss. The remedy was to run the real done-marking step on work packages seeded through the real status pipeline, substitute only the network calls, the git preflight and the git write (spied for the set of paths it was handed), and assert on the persisted event log. No production change was needed.

Mind the vocabulary guard (C-006). Use "boundary" in prose; "border" may appear once as a synonym ("the responsibility boundary, or border").

### T002 Author the remediation procedure

File: `packs/foundation/procedures/unfake-an-over-mocked-test.procedure.yaml` (new). Shape: same keys as `observable-contract-test-authoring.procedure.yaml` (`schema_version: '1.0'`, `id`, `title`, `description`, `entry_condition`, `exit_condition`, `steps` with `title`/`description`). Title "Unfake an Over-Mocked Test". Entry: a test substitutes a collaborator the system under test owns (found in review, in a failing-test triage, or while touching the test). Exit: every remaining double sits on an allow-listed seam of DIRECTIVE_054, owned collaborators run for real on realistic seeded state, assertions target observable outcomes, and the test fails when the behaviour regresses.

Steps (one per bullet, 1-3 sentences each):
1. Name the behaviour under test in one sentence (not the class under test).
2. Draw the responsibility boundary around every collaborator that co-delivers that behaviour, including ones in another layer.
3. Classify each double: keep it only if it sits on a DIRECTIVE_054 allow-listed seam; otherwise mark it for removal.
4. Remove the owned doubles and run the real collaborators. Seed state through the production path (the real creation or status pipeline), not hand-built records, so only reachable states exist.
5. Move assertions from call verification to outcomes: follow `observable-contract-test-authoring` (name it; do not restate it).
6. Check the remaining border doubles keep the real dependency's contract (states it can and cannot produce).
7. Prove the test is not vacuous: break the behaviour (or revert the fix) and watch it go red, then restore. Record the failure text.
8. Budget the cost honestly: a wider slice is slower to set up; if the slice needs heavy scaffolding, extract a pure seam instead (tactic `test-scaffolding-as-design-smell`, by name).

### T003 Glossary terms

File: `packs/foundation/glossaries/spec-kitty-core.glossary.yaml`. Add two terms right after `characterization-test` (the file is not alphabetical), same shape as `characterization-test` (`id`, `name`, `definition`, `status: active`, optional `aliases`, `see_also` if other terms use it):
- `responsibility-boundary` / "responsibility boundary", aliases `["responsibility border"]`: the edge of what the system under test owns for the behaviour under test, drawn by responsibility rather than by layer, module or deployment. Collaborators inside it run for real; only allow-listed dependencies outside it may be substituted (DIRECTIVE_054).
- `change-detector-test` / "change-detector test": a test that restates configuration or structure. It goes red only because the thing does not exist yet and afterwards fails only when someone changes it on purpose, so it guards no lasting behaviour. Where a real run or an existing gate is the evidence, it is not written (DIRECTIVE_034). Note `characterization test` is different.
Read `tests/ci/test_glossary_content.py` in full before writing: its `CORE_CITATION` regex rejects issue numbers, ADR ids, `.py`, requirement ids, `WP` ids, `name()` calls, `::name`, `tests/`, `src/`, `docs/context/` in definitions; names and aliases must be unique across the file; `see_also` uses the `term:spec-kitty-core/<id>` form. So write "DIRECTIVE 054"-style references only if the regex allows them; otherwise say "the mock-boundary directive" and "the test-first directive". Check the term-id format other terms use and whether aliases exist elsewhere in the file.

### T004 DIRECTIVE_036 scope pointer

File: `packs/foundation/directives/036-black-box-integration-testing.directive.yaml`. Change only: scope's last sentence "Unit-level tests and full end-to-end tests are governed by their own directives." becomes a sentence saying where substitutes may sit at every level is set by DIRECTIVE_054 (and drop the claim that unit tests have "their own directives"). The third integrity rule's seam list ("other services, third-party systems, filesystem, network, clock") should say it is a subset of the DIRECTIVE_054 allow-list, or simply refer to it ("an allow-listed seam of DIRECTIVE_054"). Keep everything else.

### T005 Graph wiring (foundation)

Hand-edit (no generator exists). Follow research.md R3 exactly:
- `packs/foundation/directive.graph.yaml`: node `directive:DIRECTIVE_054` (kind `directive`, label = title) in id order; edges in source order: `DIRECTIVE_036 requires DIRECTIVE_054`; `DIRECTIVE_054 requires DIRECTIVE_041`; `DIRECTIVE_054 requires procedure:unfake-an-over-mocked-test` with `when` ("a test substitutes a collaborator the system under test owns") and a one-sentence `reason`; `DIRECTIVE_054 suggests tactic:test-boundaries-by-responsibility`; `DIRECTIVE_054 suggests tactic:function-over-form-testing`.
- `packs/foundation/procedure.graph.yaml`: node `procedure:unfake-an-over-mocked-test`; edges `requires tactic:test-boundaries-by-responsibility`, `suggests procedure:observable-contract-test-authoring`.
- `packs/foundation/action.graph.yaml`: `action:software-dev/implement scope directive:DIRECTIVE_054` and `action:software-dev/review scope directive:DIRECTIVE_054`, placed with the other directive scope edges of each action.
- `packs/foundation/agent_profile.graph.yaml`: `agent_profile:reviewer-renata requires directive:DIRECTIVE_054`; `agent_profile:implementer-ivan suggests directive:DIRECTIVE_054`; `agent_profile:generic-agent suggests directive:DIRECTIVE_054`. Give each `when` and `reason` modelled on the existing 034 and 041 profile edges (do not cite "#3063" or other issue numbers in new reasons).
- Existing edge reason to reword (invariant: no surface reads as unconditional red-first): `directive:DIRECTIVE_039 requires procedure:test-first-cycle` (around line 309) has reason "Starts every production change from a failing test ..."; make it "Starts each production change that carries a lasting regression risk from a failing test (DIRECTIVE_034) ..." and keep the rest of the sentence.
- Constraint: one edge per unordered pair per pack (`tests/ci/test_graph_edge_identity.py`). Check none of these pairs already exists. Do not add any 034-041 edge.
- Check how the existing file orders nodes and edges and keep that order.

### T006 Implementer profile reference, then gates

- `packs/foundation/agent_profiles/implementer-ivan.agent.yaml`: if the profile has a `directive-references` list (as reviewer-renata does), add a `054` entry with name and a one-line rationale ("Substitute only allow-listed seams; run owned collaborators for real"). Keep its format. (reviewer-renata is edited in WP03.)
- Run `spec-kitty charter context --include directive:DIRECTIVE_054` and confirm it resolves (paste the head of its output into the evidence note). If the installed CLI reads packs from its own install rather than this repo, say so in the note instead; the gates are authoritative.
- Restamp foundation (manifest, digest), built-in digest if needed, pages; run all gates (see Working rules).

## Definition of Done

- 054 and the procedure exist, validate, and carry every point above; no core numbers or paths; no enforcement prose.
- `grep -rn "DIRECTIVE_054" packs/foundation/*.graph.yaml` shows the node and the 10 edges listed in T005 (2 action, 3 profile, 5 in the directive graph including 036 requires 054).
- Both glossary terms exist.
- All gates exit 0.

## Risks

- Edge identity collisions (one edge per pair). Check before adding.
- Over-long directive: keep each rule one or two sentences.

## Reviewer guidance

Check the allow-list matches the operator ruling exactly (8 categories), the "permits, never requires" rule, the neutral worked example, the graph edges against research.md R3, and that the procedure points to `observable-contract-test-authoring` rather than restating it.
## Branch Strategy

Planning and merge branch: `t3/test-doctrine-mock-boundary` (topology `single_branch`, no lane worktree; you work directly in the repository root checkout on that branch). The pull request goes from `t3/test-doctrine-mock-boundary` to `main`. Start with:

```bash
spec-kitty agent action implement WP01 --agent claude --mission test-doctrine-01M7X00D
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
- Commit with a conventional message ending in the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`, then `spec-kitty agent tasks move-task WP01 --to for_review --mission test-doctrine-01M7X00D --note "<evidence>"`. Do not push.
- Append one line to `kitty-specs/test-doctrine-01M7X00D/traces/tooling-friction.md` or `design-decisions.md` if you hit friction or make a non-obvious call (format `YYYY-MM-DD · claude-implementer · <text>`).
