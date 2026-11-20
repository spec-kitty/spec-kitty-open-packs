---
work_package_id: WP01
title: Planning-corpus and product-coherence tactics
dependencies: []
requirement_refs:
- FR-003
- FR-004
- FR-006
- FR-012
- FR-014
planning_base_branch: t3/analyze-planning-corpus-coherence
merge_target_branch: t3/analyze-planning-corpus-coherence
branch_strategy: Planning artifacts for this mission were generated on t3/analyze-planning-corpus-coherence. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/analyze-planning-corpus-coherence unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-analyze-planning-corpus-01M7WZZM
base_commit: 2347751b877d4bbe7b283641764bad76a60bf53a
created_at: '2026-11-20T17:45:38.789864+00:00'
subtasks:
- T001
- T002
- T003
- T004
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/tactics/analysis/
create_intent:
- packs/foundation/tactics/analysis/planning-corpus-consistency.tactic.yaml
- packs/foundation/tactics/analysis/product-coherence-review.tactic.yaml
execution_mode: code_change
model: sonnet
owned_files:
- packs/foundation/tactics/analysis/planning-corpus-consistency.tactic.yaml
- packs/foundation/tactics/analysis/product-coherence-review.tactic.yaml
- packs/foundation/tactic.graph.yaml
- packs/foundation/action.graph.yaml
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP01 - Planning-corpus and product-coherence tactics

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
- **Report progress**: As you address each feedback item, record what you changed with `spec-kitty agent tasks add-history WP01 --note "..."` (stored in the status event log).

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks: `` `<div>` ``, `` `<script>` ``
Use language identifiers in code blocks: ````python`,````bash`

---

## Objectives & Success Criteria

Two new foundation tactics carry the check detail the analyze prompt cannot hold within its 500-line cap:

1. `planning-corpus-consistency` — how to load the whole planning corpus and check it against spec, tasks and WPs (#213).
2. `product-coherence-review` — how to judge whether the plan still serves the creation intent (#214).

Done when: both files exist under `packs/foundation/tactics/analysis/`, follow the shape of `requirement-quality-ears.tactic.yaml`, are registered as nodes in `packs/foundation/tactic.graph.yaml`, are scoped from `action:software-dev/analyze` in `packs/foundation/action.graph.yaml`, and `bash scripts/ci/validate-packs.sh` plus `python3 scripts/ci/check_vocabulary.py` pass. (The derived `pack-manifest.yaml`, digests and pages are WP05's job; `validate-packs.sh` may report a manifest mismatch until then — if it does, run `python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/foundation` locally only to confirm the content validates, then **revert** the manifest so WP05 owns it. Note the result in add-history.)

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

Read first: `packs/foundation/tactics/analysis/requirement-quality-ears.tactic.yaml` (the model: `schema_version: "1.0"`, `id`, `name`, `purpose`, `steps[]` with `title`, `description`, `examples`, then `failure_modes`, `notes`) and `wp-prompt-readiness-review.tactic.yaml`. Read the current analyze prompt `packs/foundation/missions/software-dev/steps/analyze.prompt.md` so the vocabulary matches (finding, category, `Inferred:`, WP prompt, `tasks.md`).

### Subtask T001 - Author `planning-corpus-consistency.tactic.yaml`

- **Purpose**: say how to load and check every planning artifact besides spec/plan/tasks/WP prompts, and how to spot ungrounded behaviour.
- **File**: `packs/foundation/tactics/analysis/planning-corpus-consistency.tactic.yaml` (new, ~90-110 lines).
- **`name`**: `Planning Corpus Consistency`.
- **`purpose`** (folded `>`): planning produces more than spec, plan and tasks: research decisions, a data model, contracts, quickstart scenarios, checklists, a bulk-edit occurrence map, and the intent recorded when the Mission was created. If one of them contradicts the tasks, or the tasks leave out what it implies, an implementation agent faithfully builds the wrong thing. This tactic checks the whole corpus against the tasks and WP prompts. It reads and judges; it never edits.
- **Steps** (each with `description` and 1-2 concrete `examples`):
  1. **Load the corpus from the inventory** — the inputs are the `artifact_files` and `artifact_dirs` entries `check-prerequisites` prints, every entry whose path has not already been loaded, **except `feature_dir`** (the mission directory itself); `<mission_dir>/meta.json` for `purpose_tldr`, `purpose_context` and `source_description` (meta.json is not in the inventory; state which fields were absent — `source_description` usually is); `<mission_dir>/occurrence_map.yaml` when present, and the recorded decisions under `<mission_dir>/decisions/` (`DM-*.md`) when present (neither is inventoried; both are canonical fixed paths). A directory whose files are already loaded (the WP prompt directory, `tasks_dir`) counts as loaded. No glob and no hard-coded key list. Load headings first (for a directory: its file list, then each file's headings); read a body section only when a check below needs it.
  2. **Decision continuity** — every material decision in `research.md`, `plan.md` and the recorded decisions (`decisions/DM-*.md`) (a `Decision:` line, a chosen alternative) and every deferred-decision marker (`[NEEDS CLARIFICATION: ...]`, "deferred", a decision id) is (a) implemented by a named task or WP, (b) explicitly deferred with a reason, or (c) flagged as open. A decision in none of the three is a finding; a task that implements the rejected alternative is a contradiction. Example: research chooses an event log, WP03 implements polling.
  3. **Data model** — each entity, invariant and state transition in `data-model.md` is consistent with the spec, the contracts and the tasks/WPs, and the work that enforces an invariant or a transition has a task. Example: invariant "an order is never both shipped and cancelled" has no task and no test.
  4. **Contracts** — each operation, message or schema under `contracts/` maps to a user action in the spec, agrees with the data model, appears in a quickstart scenario where one exists, and is built by a task. Example: `cancel` in `contracts/orders.yaml`, no WP builds it.
  5. **Quickstart** — each validation scenario in `quickstart.md` is covered by a task or a WP's acceptance/validation section.
  6. **Occurrence map** — for a bulk-edit Mission, each category's action in `occurrence_map.yaml` (rename, keep, manual review …) is reflected in the WPs that own those files; a category with an action and no owning WP is a finding.
  7. **Any other inventory artifact** — an artifact no step above names is still read headings-first and cross-checked: content it states that no task or WP reflects is a finding. It is never skipped silently.
  8. **Ungrounded behaviour** — a task or WP that builds behaviour with no trace at all to a requirement, a plan decision, a planning artifact or the creation intent. A WP mapped to no requirement is already reported by the finalize validation or the coverage pass: cite that finding, do not raise a second one. Behaviour that does trace to a source but goes beyond what the intent needs is overbuild, which `product-coherence-review` judges, not this tactic.
  9. **Phrase each finding** — name the artifact location (`file:Lnn`, or a heading when no stable line exists) and the task or WP it should appear in; quote the decision or element. A finding reached by judgement starts with `Inferred:`.
- **`failure_modes`**: loading every artifact whole; re-reporting a defect another pass already owns; treating `feature_dir` as an artifact; hard-coding the artifact list; flagging a decision that is explicitly deferred; editing a planning file to "fix" it.
- **`notes`**: the step that cites this tactic decides severities, finding ids and report layout (mirror the `requirement-quality-ears` note).

### Subtask T002 - Author `product-coherence-review.tactic.yaml`

- **Purpose**: the product-owner question — "is this still the right plan for what the user asked for?"
- **File**: `packs/foundation/tactics/analysis/product-coherence-review.tactic.yaml` (new, ~90-110 lines).
- **`name`**: `Product Coherence Review`.
- **`purpose`**: a plan can be internally consistent and still wrong: overbuilt, missing its smallest valuable slice, all scaffolding up front, or drifted from the intent the Mission was created for. This tactic reviews the plan as a whole against that intent. Every finding is a judgement, labelled inferred, and ends in one recommendation.
- **Steps** (allowed step keys: `title`, `description`, `examples` only; top-level: `schema_version`, `id`, `name`, `purpose`, `steps`, `failure_modes`, `notes` — the schema rejects extra keys):
  1. **Restate the creation intent** — from `meta.json` `purpose_tldr`, `purpose_context` and `source_description` (say which were absent), plus the spec's intent summary. Never invent intent.
  2. **Intent drift** — does the planned work, taken together, still deliver that intent? Name what was added, dropped or reshaped.
  3. **Smallest valuable slice (MVP)** — read the MVP slice the task breakdown names (`tasks.md`'s MVP Scope note or a WP heading marked MVP). Do not define MVP yourself. No such note: an "MVP unclear" finding. A named MVP that delivers no user value before the full Mission completes: a finding.
  4. **Vertical slice vs scaffolding** — do the first WPs produce something a user or a test can observe end to end, or only layers (models, config, plumbing) that deliver nothing until later WPs land?
  5. **Overbuild** — work beyond the stated need: extra configurability, admin surfaces, generality nobody asked for. If the work traces to no source at all, the planning-corpus pass owns it (ungrounded behaviour): cite that finding.
  6. **Lost scenarios** — a user journey, actor, trigger, success outcome or failure case present in the spec (or the intent) that disappears between spec, plan and tasks.
  7. **Sequencing risk** — dependency chains that delay all value to the end, a risky unknown scheduled last, or a long serial chain where independent WPs could deliver earlier.
  8. **Grouping by user value** — WPs grouped around a user story or a coherent subsystem rather than arbitrary technical layers ("all models", "all tests").
  9. **Recommend** — choose exactly one: `revise spec` (the intent or requirements are wrong or missing), `revise plan` (the approach does not serve the intent), `revise tasks` (the breakdown, slicing or order is the problem), or `proceed`. Weigh every finding of the report, not only this tactic's; never `proceed` when the report's verdict is blocked; a `revise` choice is allowed while the verdict is ready.
  10. **Label** — every finding starts with `Inferred:`; never claim proof.
- Give each step one example (e.g. "Inferred: WP01-WP04 build the schema, repository, service and API layers; the first user-visible result is WP05 (tasks.md, WP05). Recommend revise tasks: slice US1 end to end first.").
- **`failure_modes`**: redefining MVP instead of reading it; presenting judgement as proof; duplicating an ungrounded-behaviour finding as overbuild; recommending `proceed` over a blocked verdict; inventing intent the Mission never recorded.
- **`notes`**: the citing step decides severities (it caps them), finding ids and report layout.
- **Wording**: do **not** write "advisory" in a phrase the vocabulary guard rejects (see Context). "Judgement", "never blocks the verdict" are fine — and severity/blocking belongs to the citing step anyway, so the tactic need not mention it.

### Subtask T003 - Register both tactics in `packs/foundation/tactic.graph.yaml`

- Add two nodes in alphabetical position among the `urn: tactic:...` nodes (the list is sorted): `tactic:planning-corpus-consistency` (label `Planning Corpus Consistency`) and `tactic:product-coherence-review` (label `Product Coherence Review`), each with `kind: tactic`.
- Add a few `suggests` edges in the edges section, following the existing shape (`source`, `target`, `relation: suggests`, `when:`), placed in sorted order by source like neighbours:
  - `tactic:planning-corpus-consistency` → `tactic:product-coherence-review` — when: "The corpus is consistent; judge whether the plan still serves the creation intent".
  - `tactic:product-coherence-review` → `tactic:acceptance-criteria-non-vacuity` — only if useful; otherwise one edge is enough. Do **not** link `split-brain-authority-detection` (it is about runtime authority, not documents).
- Ordering: nodes are alphabetical — `planning-corpus-consistency` goes before `pr-agent-worktree-isolation`, `product-coherence-review` after `problem-decomposition`. Edges: after the `problem-decomposition` edges, before the `requirement-quality-ears` edges.

### Subtask T004 - Scope from the analyze action in `packs/foundation/action.graph.yaml`

- Next to the existing `source: action:software-dev/analyze` / `target: tactic:requirement-quality-ears` / `relation: scope` edge (around lines 330-335), add the same edge shape for `tactic:planning-corpus-consistency` and `tactic:product-coherence-review`, keeping the file's order convention.
- Do not scope them from `specify` or `tasks` (out of scope).

## Test Strategy

- `bash scripts/ci/validate-packs.sh` (schema + graph references; see Objectives for the manifest note).
- `python3 scripts/ci/check_vocabulary.py` → exit 0.
- `python3 -c "import yaml;[yaml.safe_load(open(p)) for p in ('packs/foundation/tactics/analysis/planning-corpus-consistency.tactic.yaml','packs/foundation/tactics/analysis/product-coherence-review.tactic.yaml')]"`.
- `grep -nE "#[0-9]{2,}|src/specify_cli" packs/foundation/tactics/analysis/{planning-corpus-consistency,product-coherence-review}.tactic.yaml` → nothing.

## Risks & Mitigations

- Schema drift: copy top-level keys from `requirement-quality-ears` exactly; run the validator.
- Vocabulary guard: see Context.
- Overreach into #147/#215: the vertical-slice step names an observation, not a doctrine; cite no other tactic for MVP.

## Review Guidance

- Both tactics: steps match the list above; examples concrete; `feature_dir` exclusion, `meta.json`, `occurrence_map.yaml` fixed path, headings-first and ungrounded-vs-overbuild split present.
- Graph nodes/edges present, sorted, and validate.
- No issue numbers, no core paths, no guarded phrasing.

## Progress & Status

Progress, history, and status all live in the status event log
(`status.events.jsonl`) - never in this prompt file. Do **not** hand-edit a
history section here.

- **Record a progress note**: `spec-kitty agent tasks add-history WP01 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP01 --to <status>`
- **View history and status**: `spec-kitty agent tasks status`

**Read status only through the CLI** (`spec-kitty agent tasks status --mission analyze-planning-corpus-01M7WZZM`),
which reads the Mission's resolved status surface. Never read `status.events.jsonl` or
`status.json` from the files of a lane worktree, a coordination worktree or any other
checkout: only the CLI's read counts.
