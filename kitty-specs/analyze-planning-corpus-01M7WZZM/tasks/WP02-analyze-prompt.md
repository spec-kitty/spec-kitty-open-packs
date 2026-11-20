---
work_package_id: WP02
title: Software-dev analyze prompt reviews the planning corpus and product coherence
dependencies:
- WP01
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-004
- FR-005
- FR-006
- FR-007
- FR-008
- FR-009
- FR-010
- FR-011
- FR-012
- FR-013
- FR-018
- NFR-001
- NFR-002
- NFR-004
- C-001
- C-002
- C-003
- C-004
planning_base_branch: t3/analyze-planning-corpus-coherence
merge_target_branch: t3/analyze-planning-corpus-coherence
branch_strategy: Planning artifacts for this mission were generated on t3/analyze-planning-corpus-coherence. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/analyze-planning-corpus-coherence unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-analyze-planning-corpus-01M7WZZM
base_commit: 4890cde3810fd8ed84e0e3f0a570419281512a11
created_at: '2026-11-20T17:53:09.062087+00:00'
subtasks:
- T005
- T006
- T007
- T008
- T009
- T010
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/missions/software-dev/steps/
create_intent: []
execution_mode: code_change
model: sonnet
owned_files:
- packs/foundation/missions/software-dev/steps/analyze.prompt.md
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP02 - Software-dev analyze prompt reviews the planning corpus and product coherence

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, do what the skill does: run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `doctrine-daphne` (empty means: select from the role)
- **Agent/tool**: `claude`

If no profile override is set, use the profile the active preset activates for the role; otherwise run `spec-kitty agent profile list` and load a profile whose `role` is it (or, failing that, whose `alt-roles` include it), preferring one whose specialization context matches this work package's languages and `authoritative_surface`. In this repository the profile YAML lives under `packs/*/agent_profiles/doctrine-daphne.agent.yaml`; read it in full.

---

## IMPORTANT: Review Feedback

**Read this first if you are implementing this task!**

- **Has review feedback?**: Check the `review_ref` field in the event log (via `spec-kitty agent tasks status`).
- **You must address all feedback** before your work is complete. Feedback items are your implementation TODO list.
- **Report progress**: As you address each feedback item, record what you changed with `spec-kitty agent tasks add-history WP02 --note "..."` (stored in the status event log).

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks: `` `<div>` ``, `` `<script>` ``
Use language identifiers in code blocks: ````python`,````bash`

---

## Objectives & Success Criteria

Edit `packs/foundation/missions/software-dev/steps/analyze.prompt.md` (380 lines today) so the analyze step:

- loads the **whole planning corpus** from the `check-prerequisites` inventory, `meta.json` and the fixed `occurrence_map.yaml` path, headings-first (FR-001, FR-002, NFR-002, C-002);
- runs **pass H — planning-artifact consistency** (tactic `planning-corpus-consistency`, category `planning-artifact`, prefix `X`, normal severity) (FR-003, FR-004, FR-005);
- runs **pass J — product coherence** (tactic `product-coherence-review`, category `product-coherence`, prefix `M`, capped at MEDIUM, never blocks) ending in one mandatory `Recommendation:` line (FR-006, FR-007, FR-008, FR-012);
- reports both in two new always-present sections placed **immediately after Scenario Audit and before Clarification Questions** (FR-009), with prefix rows, ordering, metrics (FR-010, FR-011);
- carries the **#247 folds**: deterministic scenario findings and `Inferred:` placement (FR-012, FR-013) and the wording nits (FR-018);
- stays **≤ 500 lines** (target ≤ 470) and read-only (NFR-001, C-001).

Pass letters: the existing passes are A-G. The new passes are **H** and **J** — **I is skipped** because `I` is already a finding prefix (inconsistency). Prefixes: **`X`** and **`M`** (research R-08 explains why not P/R/H/O/T/F/N/L).

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

Read the whole current prompt first. Line numbers below refer to `main` at `3bedeef`; re-locate by text. The text in quotes is **guidance for the wording** — keep it tight; adapt to the prompt's voice (short imperative sentences, one rule per line), but every named element must land.

### Subtask T005 - Goal, step 1 and step 2: the planning corpus

1. **Goal** (line 16): replace "across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) and every WP prompt (`tasks/WP*.md`)" with wording naming the planning corpus: spec, plan, tasks, every WP prompt, and the other planning artifacts and creation intent (step 1). Add to the goal: "and judge whether the plan still serves the intent the Mission was created for".
2. **Step 1** (line 38): parse `mission_dir`, **`artifact_files`, `artifact_dirs`**, `target_branch`, `base_branch` (drop sole reliance on `available_docs`; it lists file names only). Add after the SPEC/PLAN/TASKS bullets:
   - "META = mission_dir/meta.json — read `purpose_tldr`, `purpose_context` and `source_description` (the creation intent); note which are absent. `meta.json` is not in the inventory."
   - "PLANNING ARTIFACTS = every `artifact_files` and `artifact_dirs` entry whose path is not already loaded above or in step 2 (spec, plan, tasks, the WP prompts), except `feature_dir`, which is the mission directory itself; plus `mission_dir/occurrence_map.yaml` when it exists (bulk-edit Missions) and the recorded decisions `mission_dir/decisions/DM-*.md` when present (neither is inventoried). A directory whose files are already loaded (the WP prompt directory) counts as loaded. Use no glob and no fixed list of key names."
   - Make clear the existing "Abort … if any required file is missing" line covers spec, plan and tasks only: "`meta.json` missing: say so in the report and compare against what exists; never abort for it." Place the META bullet so the abort line does not read as covering it.
3. **Step 2**: add a block after "From every `tasks/WP*.md`":
   - "**From meta.json:** the three creation-intent fields."
   - "**From every planning artifact:** headings first (for a directory, its file list and then each file's headings); read a body section only when a pass H or J check needs it. Record which inventory entries were read."
   Keep it to ~4 lines.

### Subtask T006 - Pass G folds and the ownership rule

1. **One-defect rule** (line 156): generalise to: "**One defect, one finding.** The earliest step that detects a defect owns it — 2a, 2b, then passes A-G, H, J — and later steps cite its id (in the table's Notes, the Per-WP Readiness row or the section text) instead of raising their own." Keep the existing `V` examples sentence.
2. **Pass G** (lines 192-200):
   - Scenario bullet (198): add "Only missing-edge, surprising-accepted and surprising-rejected rows become `S` findings; accepted and rejected rows are context."
   - `Inferred:` bullet (200): replace with: "a finding reached by judgement starts with `Inferred:` in both its carrier `summary` and its table Summary cell, and never claims proof. This applies to every judgement finding of step 2b and passes A-H and J; a `V` finding quotes the command output and never carries the label."

### Subtask T007 - Pass H and pass J (new, after pass G)

Add two subsections after `#### G. ...` and before `### 5. Severity Assignment`. Target ~10 lines each.

```markdown
#### H. Intent & Planning-Artifact Consistency

Apply tactic `planning-corpus-consistency` (fetch: `spec-kitty charter context --include tactic:planning-corpus-consistency`) to the planning artifacts and creation intent loaded in step 2. Category `planning-artifact`. In one line each:

- each research, plan or recorded (`decisions/`) decision, and each deferred-decision marker, is implemented by a task or WP, explicitly deferred, or flagged; one implemented the other way is a contradiction;
- data-model entities, invariants and state transitions, contract operations and quickstart scenarios agree with the spec and are built or covered by a task or WP;
- `occurrence_map.yaml` (when present): every category's action is reflected in the WPs that own those files;
- any other planning artifact: content it states that no task or WP reflects;
- ungrounded behaviour: a task or WP that builds something no requirement, plan decision, planning artifact or creation-intent field asks for. A WP mapped to no requirement is a `V`, `W` or `C` defect: cite it.

Evidence for an `X` finding sits in a planning artifact or `meta.json`; differences among spec, plan and tasks alone stay with pass F.

#### J. Product Coherence

Apply tactic `product-coherence-review` (fetch: `spec-kitty charter context --include tactic:product-coherence-review`). Category `product-coherence`. Every finding starts with `Inferred:` and is MEDIUM or LOW; it never blocks the verdict. Review against the creation intent:

- intent drift; the MVP slice, read from the MVP Scope note in `tasks.md` or a WP heading marked MVP (neither: "MVP unclear") — never define MVP here;
- whether the first WPs deliver a vertical slice or only scaffolding; overbuild beyond the stated need (work with no trace at all is an `X` finding: cite it);
- user journeys, actors, triggers, outcomes or failure cases lost between spec, plan and tasks; sequencing that delays all value or leaves a risky unknown last; WPs grouped by technical layer rather than user value.

End with exactly one recommendation: revise spec, revise plan, revise tasks, or proceed (step 6).
```

### Subtask T008 - Severity (step 5, lines 202-210)

- **Fold the duplicated "untestable" rule** (FR-018): line 207 lists "untestable acceptance criterion" as HIGH while line 208 makes "an untestable or ambiguous requirement that changes what gets built" HIGH. Remove "untestable acceptance criterion" from line 207 and keep line 208 as the one rule.
- **HIGH** add: "a planning-artifact contradiction or ungrounded behaviour that changes what gets built (step H)".
- **MEDIUM** add: "a planning-artifact decision, element or scenario no task reflects".
- Add a final line: "**Product-coherence findings** (pass J) are MEDIUM or LOW, never higher, so they never block the verdict; their weight goes into the recommendation (step 6)."
- Do **not** write "advisory" in a guarded phrase (see Context).

### Subtask T009 - Report shape (step 6)

1. **Example row** (line 241): change the Category cell `Duplication` to the lowercase id `duplication` (FR-018), and the Location cell to the `file:Lnn` form already used (`spec.md:L120-134`).
2. **Ordering sentence** (line 243): "numbered within each prefix by step (2a, 2b, then passes A-G, H, J), then by artifact (spec.md, plan.md, tasks.md, WP prompts in id order, other planning artifacts in inventory order, meta.json, charter), then by line". Add: "Locations use `file:Lnn` (or `file:Lnn-mm`); use a heading only when no stable line exists."
3. **Prefix table**: add one row (the table has two prefix/category pairs per row): `| X | planning-artifact | M | product-coherence |`. Keep the existing rows.
4. **Scenario Audit** section (lines 266-269): table header becomes `| Kind | Scenario | Location | Finding |`; add: "Rows in this order: accepted, rejected, missing edge, surprising accepted, surprising rejected. Finding is the `S` id, or `—` for accepted and rejected rows."
5. **Two new sections**, inserted after Scenario Audit and before Clarification Questions:
   - "**Intent & Planning-Artifact Consistency:** the inventory entries read (and `meta.json` fields absent), then the `X` findings grouped by artifact. With no planning artifacts beyond spec, plan and tasks, say so."
   - "**Product Coherence:** the creation intent in one line, the `M` findings, then exactly one line: `Recommendation: revise spec | revise plan | revise tasks | proceed` — choose one. Weigh every finding in the report: never `proceed` while the verdict is `blocked`; a `revise` choice is allowed while it is `ready`."
   Write the literal line shape `Recommendation: revise spec | revise plan | revise tasks | proceed` exactly once in the prompt so tests can pin it.
6. **Metrics** (lines 284-296): add "Planning artifacts reviewed", "Planning-artifact findings", "Product-coherence findings", "Coherence recommendation".
7. The "always in this order and always present" rule (line 253) is unchanged and now covers the two new sections.

### Subtask T010 - Next Actions, principles, budget

1. **Next Actions** (step 8): add a bullet "Repeat the Product Coherence recommendation line and name the artifact to revise." Reword "If only LOW/MEDIUM: User may proceed, but provide improvement suggestions" so it defers to that line, e.g. "If only LOW/MEDIUM: the verdict is ready; follow the Product Coherence recommendation (proceed, or the artifact it names to revise)".
2. **Context Efficiency** principles: add "Planning artifacts load headings-first; read a body section only when a check needs it."
3. **NON-REMEDIATING** (line 20, the binding read-only rule): extend its list "Do **not** modify `spec.md`, `plan.md`, `tasks.md`, WP files, …" with the other planning artifacts, `meta.json`, `occurrence_map.yaml` and `decisions/`. The Analysis Guidelines read-only lines (370-371) stay.
4. **Budget**: `wc -l` the file. ≤ 500 is a hard CI cap (`MAX_ANALYZE_LINES`); aim ≤ 470. If over, compress wording, not content: merge bullets, drop examples that the tactics already carry.
5. **Read-only guard**: run `python3 -m pytest -q tests/ci/test_analyze_readiness_prompts.py` — existing tests must stay green (the writing-finalize classifier, the version gate, Q/S prefixes, tactic citations).

## Test Strategy

- `.venv/bin/python -m pytest -q tests/ci/test_analyze_readiness_prompts.py` (existing pins stay green; new pins arrive in WP04).
- `python3 scripts/ci/check_vocabulary.py` → 0.
- `grep -nE "#[0-9]{2,}" packs/foundation/missions/software-dev/steps/analyze.prompt.md` → no new issue numbers.
- `wc -l` ≤ 500.
- Walk quickstart scenarios 1-4 and 6 by reading the edited prompt.

## Risks & Mitigations

- **Line cap**: the passes are one line per check; detail lives in the tactics.
- **Double loading**: step 1 says "not already loaded".
- **Determinism**: ordering sentence and prefix table updated together; section list order fixed.
- **Vocabulary guard**: "capped at MEDIUM; never blocks the verdict".
- **Pass F overlap**: the "Evidence for an `X` finding" sentence.

## Review Guidance

- Every element named in T005-T010 is present; sections in order: Finalize Validation, Per-WP Readiness, Requirement Quality, Scenario Audit, Intent & Planning-Artifact Consistency, Product Coherence, Clarification Questions, Coverage Summary Table, Residual Risk, Charter Alignment Issues, Unmapped Tasks, Metrics.
- `artifact_files`, `artifact_dirs`, `feature_dir`, `meta.json`, `purpose_tldr`, `purpose_context`, `source_description`, `occurrence_map.yaml` all named.
- Prefix table has 12 distinct prefixes; pass letters H and J; the one-defect rule says the earliest step owns a defect.
- The verdict rule (any high/critical → blocked) and the carrier rules are untouched.

## Progress & Status

Progress, history, and status all live in the status event log
(`status.events.jsonl`) - never in this prompt file. Do **not** hand-edit a
history section here.

- **Record a progress note**: `spec-kitty agent tasks add-history WP02 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP02 --to <status>`
- **View history and status**: `spec-kitty agent tasks status`

**Read status only through the CLI** (`spec-kitty agent tasks status --mission analyze-planning-corpus-01M7WZZM`),
which reads the Mission's resolved status surface. Never read `status.events.jsonl` or
`status.json` from the files of a lane worktree, a coordination worktree or any other
checkout: only the CLI's read counts.
