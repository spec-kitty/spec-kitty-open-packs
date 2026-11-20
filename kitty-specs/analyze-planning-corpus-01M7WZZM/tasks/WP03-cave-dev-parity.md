---
work_package_id: WP03
title: cave-dev analyze names the same checks
dependencies:
- WP01
requirement_refs:
- FR-015
planning_base_branch: t3/analyze-planning-corpus-coherence
merge_target_branch: t3/analyze-planning-corpus-coherence
branch_strategy: Planning artifacts for this mission were generated on t3/analyze-planning-corpus-coherence. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/analyze-planning-corpus-coherence unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-analyze-planning-corpus-01M7WZZM
base_commit: 6cb2cec922e2b3393ca58974254c5fc1bab56825
created_at: '2026-11-20T17:53:32.656237+00:00'
subtasks:
- T011
- T012
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/cave-kitty/
create_intent: []
execution_mode: code_change
model: sonnet
owned_files:
- packs/cave-kitty/missions/cave-dev/steps/analyze.prompt.md
- packs/cave-kitty/drg/fragment.yaml
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP03 - cave-dev analyze names the same checks

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
- **Report progress**: As you address each feedback item, record what you changed with `spec-kitty agent tasks add-history WP03 --note "..."` (stored in the status event log).

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks: `` `<div>` ``, `` `<script>` ``
Use language identifiers in code blocks: ````python`,````bash`

---

## Objectives & Success Criteria

cave-dev's analyze step inherits the software-dev contract but keeps a short "Readiness checks (inherited, named here)" list so nothing is skipped under the caveman voice. Add the two new checks there and scope both tactics from `action:cave-dev/analyze` (FR-015, a repository invariant: the cave-dev copy must name the same checks). Growth ≤ 15 lines (NFR-001).

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

### Subtask T011 - Name the checks in `packs/cave-kitty/missions/cave-dev/steps/analyze.prompt.md`

- **Role in the lifecycle** paragraph (lines ~5-12): where it says it confirms `spec.md`, `plan.md`, `tasks.md` and every WP prompt are coherent, add "and the other planning artifacts and the Mission's creation intent", and "and whether the plan still serves that intent". Keep it one sentence longer at most.
- **Readiness checks (inherited, named here)**: add two bullets in the existing style (bold lead, then one or two lines), after "Requirement quality" and before "Judgement findings start with `Inferred:`":
  - "**Planning corpus.** Read every `artifact_files` / `artifact_dirs` entry not already loaded (never `feature_dir`), `meta.json` creation intent and `occurrence_map.yaml` when present, headings first, with `foundation` tactic `planning-corpus-consistency` (`spec-kitty charter context --include tactic:planning-corpus-consistency`). Contradictions and ungrounded work are `X` findings at normal severity."
  - "**Product coherence.** Judge the plan against the creation intent with `foundation` tactic `product-coherence-review` (`spec-kitty charter context --include tactic:product-coherence-review`). `M` findings are MEDIUM or LOW and never block. End with exactly one `Recommendation: revise spec | revise plan | revise tasks | proceed` line."
- **Voice at this step**: add a line: "The `Recommendation:` line is payload — exact wording, one choice."
- Keep "Judgement findings start with `Inferred:`" (pinned by tests).
- Do not change the runtime note or the role section.

### Subtask T012 - Scope edges in `packs/cave-kitty/drg/fragment.yaml`

- Next to the existing `source: action:cave-dev/analyze` → `target: foundation::tactic:requirement-quality-ears` `relation: scope` edge (lines ~80-82), add the same shape for `foundation::tactic:planning-corpus-consistency` and `foundation::tactic:product-coherence-review`. Follow the file's indentation and ordering.

## Test Strategy

- `bash scripts/ci/validate-packs.sh` (cross-pack references resolve once WP01 is merged into the lane base).
- `python3 scripts/ci/check_vocabulary.py` → 0.
- `git diff --stat` shows ≤ 15 added lines in the cave prompt.
- `.venv/bin/python -m pytest -q tests/ci/test_analyze_readiness_prompts.py` stays green (the writing-finalize classifier also scans this prompt).

## Risks & Mitigations

- Cross-pack reference before WP01 lands: this WP depends on WP01; base the lane on it.
- Voice drift: keep bold-lead bullets; commands and ids are payload.

## Review Guidance

- Both tactics named with their fetch commands; `X`/`M`; cap; recommendation line literal; `feature_dir` excluded; growth ≤ 15 lines; fragment edges valid.

## Progress & Status

Progress, history, and status all live in the status event log
(`status.events.jsonl`) - never in this prompt file. Do **not** hand-edit a
history section here.

- **Record a progress note**: `spec-kitty agent tasks add-history WP03 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP03 --to <status>`
- **View history and status**: `spec-kitty agent tasks status`

**Read status only through the CLI** (`spec-kitty agent tasks status --mission analyze-planning-corpus-01M7WZZM`),
which reads the Mission's resolved status surface. Never read `status.events.jsonl` or
`status.json` from the files of a lane worktree, a coordination worktree or any other
checkout: only the CLI's read counts.
