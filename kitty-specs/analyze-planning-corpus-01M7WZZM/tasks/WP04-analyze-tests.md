---
work_package_id: WP04
title: Tests pin the analyze readiness content
dependencies:
- WP02
- WP03
requirement_refs:
- FR-016
- SC-001
- SC-002
- SC-003
planning_base_branch: t3/analyze-planning-corpus-coherence
merge_target_branch: t3/analyze-planning-corpus-coherence
branch_strategy: Planning artifacts for this mission were generated on t3/analyze-planning-corpus-coherence. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/analyze-planning-corpus-coherence unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-analyze-planning-corpus-01M7WZZM
base_commit: 65afef4b1e71b4fdcf047d890eba0de55c51b64f
created_at: '2026-11-20T17:58:28.409051+00:00'
subtasks:
- T013
- T014
- T015
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: tests/ci/
create_intent: []
execution_mode: code_change
model: sonnet
owned_files:
- tests/ci/test_analyze_readiness_prompts.py
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP04 - Tests pin the analyze readiness content

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, do what the skill does: run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `python-pedro` (empty means: select from the role)
- **Agent/tool**: `claude`

If no profile override is set, use the profile the active preset activates for the role; otherwise run `spec-kitty agent profile list` and load a profile whose `role` is it (or, failing that, whose `alt-roles` include it), preferring one whose specialization context matches this work package's languages and `authoritative_surface`. In this repository the profile YAML lives under `packs/*/agent_profiles/python-pedro.agent.yaml`; read it in full.

---

## IMPORTANT: Review Feedback

**Read this first if you are implementing this task!**

- **Has review feedback?**: Check the `review_ref` field in the event log (via `spec-kitty agent tasks status`).
- **You must address all feedback** before your work is complete. Feedback items are your implementation TODO list.
- **Report progress**: As you address each feedback item, record what you changed with `spec-kitty agent tasks add-history WP04 --note "..."` (stored in the status event log).

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks: `` `<div>` ``, `` `<script>` ``
Use language identifiers in code blocks: ````python`,````bash`

---

## Objectives & Success Criteria

Extend `tests/ci/test_analyze_readiness_prompts.py` (unittest style, run under pytest; 166 lines today) so every contract added in WP01-WP03 and the #247 report content is pinned (FR-016). Tag each new test in its docstring as **red-first** (new contract: must fail on `main` at `3bedeef`) or **ratchet** (pins content that already exists on main — the T015 #247 anti-deletion pins: headings, "two to four", the five quality properties, `Inferred:` in both prompts — and passes on main by design). Every absence/negative check has a same-fixture positive control. For the red-first tests, verify by running the new tests against `git show 3bedeef:<path>` content or by temporarily checking out the old prompt in a scratch copy (never commit that). Update the module docstring to cite (#246, #237, #247, #213, #214).

## Context & Constraints (all WPs)

- Spec: `kitty-specs/analyze-planning-corpus-01M7WZZM/spec.md`; plan: `plan.md` (Design section is the authoritative change list); research: `research.md` (R-01 … R-09); quickstart: `quickstart.md`.
- Charter: `.kittify/charter/charter.md`. This repository aligns to spec-kitty-charter, **not** spec-kitty core (AGENTS.md): core loading or rendering compatibility is never a blocker.
- **Prompt-only, read-only feature**: nothing here changes a CLI. The analyze step must still mutate nothing but `analysis-report.md` through `record-analysis`, and the only `finalize-tasks` form it may name is `--validate-only`.
- **No issue numbers** (open-packs or core) and **no core source paths** in shipped pack text (prompts, tactics, graphs). Issue numbers belong in the CHANGELOG, commit messages and tests' docstrings only.
- **Vocabulary guard** (`scripts/ci/check_vocabulary.py`, `SELF_BINDING`): pack prose must not say a rule or directive "is advisory", "remains advisory", "this is advisory", "advisory context", "advisory posture", or ". Advisory: ... gate". Say "capped at MEDIUM" and "never blocks the verdict" instead.
- Operator ruling (2026-11-20, binding): product-coherence findings are capped at MEDIUM and never block the readiness verdict; a mandatory `Recommendation: revise spec | revise plan | revise tasks | proceed` line is still emitted. Planning-artifact contradictions keep normal severity.
- Commit with a conventional message naming the issues, e.g. `feat(foundation): ... (#213, #214)`, ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Branch Strategy

- **Strategy**: Planning artifacts were generated on `t3/analyze-planning-corpus-coherence`. During implementation this WP works in the lane worktree that `lanes.json` assigns; completed changes merge back into `t3/analyze-planning-corpus-coherence` unless the operator redirects the landing branch.
- **Planning base branch**: t3/analyze-planning-corpus-coherence
- **Merge target branch**: t3/analyze-planning-corpus-coherence

> These fields are populated automatically by `spec-kitty agent mission finalize-tasks`.
> Do NOT change them manually unless you are certain the branch topology has changed.

Implementation command: `spec-kitty agent action implement <WP-id> --agent claude --mission analyze-planning-corpus-01M7WZZM`.

## Subtasks & Detailed Guidance

Read the existing module first: constants (`ANALYZE`, `CAVE_ANALYZE`, `TACTICS`, `QUALITY_TACTIC`, `WP_TACTIC`, `MAX_ANALYZE_LINES = 500`), the `writing_finalize_lines` classifier and its positive control, and the existing tactic-citation / prefix tests (around lines 120-166). Follow their style: small helpers, `subTest` per prompt, clear failure messages. Keep helpers simple (complexity ≤ 15). Add constants `CORPUS_TACTIC = "planning-corpus-consistency"`, `COHERENCE_TACTIC = "product-coherence-review"`, `RECOMMENDATION = "Recommendation: revise spec | revise plan | revise tasks | proceed"`.

### Subtask T013 - Corpus inputs, passes, tactics, prefixes, sections

- **Inputs named** (software-dev analyze): `artifact_files`, `artifact_dirs`, `feature_dir`, `meta.json`, `purpose_tldr`, `purpose_context`, `source_description`, `occurrence_map.yaml`, and "headings first" (case-insensitive).
- **Tactics cited**: both prompts contain `tactic:planning-corpus-consistency` and `tactic:product-coherence-review` (fetch form `--include tactic:<id>`); both tactic files exist under `TACTICS`, parse as YAML, have `id` equal to the file stem, and non-empty `steps`.
- **Tactic content**: `planning-corpus-consistency` mentions `feature_dir`, `meta.json`, `occurrence_map.yaml`, research/decision, data model, contracts, quickstart, ungrounded; `product-coherence-review` mentions MVP, vertical slice / scaffolding, overbuild, sequencing, `Inferred:`, and the four recommendation choices.
- **Graph wiring**: `packs/foundation/action.graph.yaml` has `scope` edges from `action:software-dev/analyze` to both tactics; `packs/cave-kitty/drg/fragment.yaml` has them from `action:cave-dev/analyze` (`foundation::tactic:...`). Parse YAML, do not substring-match.
- **Prefix table**: parse the `| Prefix | Category | Prefix | Category |` table into pairs; assert `X → planning-artifact` and `M → product-coherence` are present, all 12 prefixes distinct, and the existing ten unchanged.
- **Pass labels**: headings `#### H.` and `#### J.` exist and there is no `#### I.` heading.
- **Section order**: find the bold section leads (`**Finalize Validation:**`, `**Per-WP Readiness:**`, `**Requirement Quality:**`, `**Scenario Audit:**`, `**Intent & Planning-Artifact Consistency:**`, `**Product Coherence:**`, `**Clarification Questions:**`, `**Coverage Summary Table:**`, `**Residual Risk:**`, …) and assert their indices are strictly increasing in that order.
- **Ordering rule**: the id-ordering sentence names `H, J` and the one-defect rule says the earliest step owns a defect.

### Subtask T014 - Severity cap, recommendation, positive controls

- The **whole** recommendation literal `RECOMMENDATION` (with its four choices — the report table also has a Recommendation column, so never pin the bare word) appears in the software-dev analyze prompt and in the cave-dev prompt.
- The severity section (text between `### 5. Severity Assignment` and `### 6.`) states product-coherence findings are MEDIUM or LOW, "never higher" / never block. Write a helper `coherence_capped(text) -> bool` and give it a **positive control**: a synthetic severity block that puts product-coherence under HIGH must make the helper return False.
- **Positive control for normal severity**: the severity section names planning-artifact (or step H) findings under **HIGH** — proves `X` findings are not also capped.
- The verdict rule line ("any `high` or `critical` finding -> `blocked`") is unchanged (substring pin).
- `Inferred:` placement sentence names the carrier `summary` and the table Summary cell, and says `V` findings never carry it.

### Subtask T015 - #247 content pins and cave-dev parity

From the Step-0 squad (lens B, gap 3): each of these could be deleted today with no test failing.
- Section headings **Requirement Quality**, **Scenario Audit**, **Clarification Questions** present (order covered by T013).
- The five scenario kinds in order in the Scenario Audit rule: accepted, rejected, missing edge, surprising accepted, surprising rejected; the table header includes `Finding`; the sentence that only missing-edge / surprising rows become `S` findings.
- "two to four" choices, and the question-or-concrete-remediation rule for HIGH/CRITICAL ambiguity or requirement-quality findings.
- `Inferred:` in the software-dev analyze prompt **and** the cave-dev analyze prompt.
- The five quality properties in `requirement-quality-ears.tactic.yaml`: Testable, Solution-free, Unambiguous, Consistent, Complete.
- FR-018 nits: the example table row uses the lowercase category `duplication`; the step-5 HIGH line no longer contains "untestable acceptance criterion".
- cave-dev parity: the cave prompt names `X`, `M`, both tactics, the recommendation literal, and `feature_dir`.
- Keep `MAX_ANALYZE_LINES` test; add a cave-dev size guard at ≤ 90 lines (75 today + the 15 NFR-001 allows).

## Test Strategy

- `.venv/bin/python -m pytest -q tests/ci/test_analyze_readiness_prompts.py` green on the WP02+WP03 content.
- **Red proof**: run the new test classes against `3bedeef` content (e.g. a scratch worktree outside the repo, or monkeypatching the path constants in a throwaway script) and record in add-history which assertions fail on main. Do not commit the scratch.
- Full `.venv/bin/python -m pytest -q tests` green.

## Risks & Mitigations

- Brittle substring pins: pin concepts with short, stable phrases; parse tables/YAML where possible.
- Vacuous checks: every "absence" assertion has a positive control on synthetic text.

## Review Guidance

- Each FR-016 item maps to a named test; positive controls exist for the cap and the writing-finalize classifier; red-first tests fail on main (recorded in add-history), ratchet tests are tagged as such.

## Progress & Status

Progress, history, and status all live in the status event log
(`status.events.jsonl`) - never in this prompt file. Do **not** hand-edit a
history section here.

- **Record a progress note**: `spec-kitty agent tasks add-history WP04 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP04 --to <status>`
- **View history and status**: `spec-kitty agent tasks status`

**Read status only through the CLI** (`spec-kitty agent tasks status --mission analyze-planning-corpus-01M7WZZM`),
which reads the Mission's resolved status surface. Never read `status.events.jsonl` or
`status.json` from the files of a lane worktree, a coordination worktree or any other
checkout: only the CLI's read counts.
