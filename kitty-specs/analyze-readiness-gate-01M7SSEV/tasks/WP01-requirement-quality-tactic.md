---
work_package_id: WP01
title: Requirement-quality tactic and the specify quality bar
dependencies: []
requirement_refs:
- FR-011
- FR-012
- FR-013
- FR-014
- FR-015
- FR-016
- NFR-001
- C-004
planning_base_branch: feat/analyze-finalize-validate-246
merge_target_branch: feat/analyze-finalize-validate-246
branch_strategy: Planning artifacts for this mission were generated on feat/analyze-finalize-validate-246. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/analyze-finalize-validate-246 unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-analyze-readiness-gate-01M7SSEV
base_commit: 54608f18fdb26fc9e2b0ed44bdca0e1f8a4c8c77
created_at: '2026-11-19T12:15:53.240919+00:00'
subtasks:
- T001
- T002
- T003
- T004
phase: Phase 1 - Doctrine
history:
- at: '2026-11-19T12:07:01Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/tactics/analysis/
create_intent:
- packs/foundation/tactics/analysis/requirement-quality-ears.tactic.yaml
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/tactics/analysis/requirement-quality-ears.tactic.yaml
- packs/foundation/missions/software-dev/steps/specify.prompt.md
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP01 - Requirement-quality tactic and the specify quality bar

## Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, do what the skill does: run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `curator`
- **Profile override**: `doctrine-daphne`
- **Agent/tool**: `claude`

If no profile override is set, use the profile the active preset activates for the role; otherwise run `spec-kitty agent profile list` and load a profile whose `role` is it.

---

## IMPORTANT: Review Feedback

- **Has review feedback?**: Check the `review_ref` field in the event log (via `spec-kitty agent tasks status --mission analyze-readiness-gate-01M7SSEV`).
- **You must address all feedback** before your work is complete.
- **Report progress** with `spec-kitty agent tasks add-history WP01 --note "..."`.

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks. Use language identifiers in code blocks.

---

## Objectives & Success Criteria

- A new foundation tactic `requirement-quality-ears` exists at `packs/foundation/tactics/analysis/requirement-quality-ears.tactic.yaml` and is the **single canonical definition** of:
  1. the five requirement-quality properties: testable, solution-free, unambiguous, consistent, complete (FR-011);
  2. the EARS patterns and the observable-behaviour check (FR-012);
  3. the five scenario-audit kinds: accepted, rejected, missing edge, surprising accepted, surprising rejected, each citing a `spec.md`, `plan.md` or `tasks.md` location (FR-013);
  4. how a clarification question is written: one question, concrete answer choices with their implications, or a concrete remediation proposal instead (FR-014);
  5. inferred labelling: a finding reached by judgement is labelled inferred and never claims formal proof (FR-015).
- The software-dev specify prompt names the tactic and the five properties so requirements are written to the bar analyze later checks (FR-016).
- Both files are ASCII-only and pass the tactic schema at the charter pin.

## Context & Constraints

- Spec: `kitty-specs/analyze-readiness-gate-01M7SSEV/spec.md` (FR-011..FR-016, NFR-001, C-004).
- Plan: `kitty-specs/analyze-readiness-gate-01M7SSEV/plan.md` (IC-02), research R3 and R5, data-model severity map.
- Issue #247 lists the original scope; core #1131 keeps the deterministic checker and fixture tests (C-004). Solver-backed analysis is out of scope: the tactic must not promise proof.
- Operator ruling (Decision Moment `01M7SV0083VK137H0ZRRHHAC58`): the checklists live in tactics; the prompts keep report sections, severities and carrier rules. So the tactic says **what** to check and how to phrase a finding; it does **not** fix severities or report layout (WP03 owns those).
- House voice for doctrine: imperative, concrete, no marketing words. Read `packs/pack-authoring/styleguides/doctrine-instruction-voice.styleguide.yaml` before writing. Look at `packs/foundation/tactics/testing/acceptance-criteria-non-vacuity.tactic.yaml` for the shape (`schema_version`, `id`, `name`, `purpose`, `steps[]` with `title`, `description`, `examples`).
- AGENTS.md: align to the charter, not core. Whether core surfaces tactic context to the analyze step does not block this work.

## Branch Strategy

- **Strategy**: populated by `finalize-tasks`.
- **Planning base branch**: `feat/analyze-finalize-validate-246`
- **Merge target branch**: `feat/analyze-finalize-validate-246`

> These fields are populated automatically by `spec-kitty agent mission finalize-tasks`. Execution worktrees, if any, are allocated per computed lane from `lanes.json`.

Implement with:

```bash
spec-kitty agent action implement WP01 --agent claude --mission analyze-readiness-gate-01M7SSEV
```

## Subtasks & Detailed Guidance

### Subtask T001 - Author `requirement-quality-ears` tactic

- **Purpose**: one source for the requirement-quality bar that specify (writing) and analyze (checking) both cite.
- **Steps**:
  1. Create `packs/foundation/tactics/analysis/requirement-quality-ears.tactic.yaml` with `schema_version: "1.0"`, `id: requirement-quality-ears`, `name: Requirement Quality and EARS`, a `purpose` of two to four sentences that says it is used both when writing requirements (specify) and when checking them (analyze), and that judgement-based results are inferred, never proof.
  2. Steps, in this order (each with `title`, `description`, and one or two `examples`):
     - **Check the five quality properties.** Define each in one sentence:
       - *testable*: a reviewer can name the observation that passes or fails it;
       - *solution-free*: it states the need, not the mechanism (no framework, library, schema or code structure unless the requirement is itself about that interface);
       - *unambiguous*: one reading; no vague adjectives (fast, robust, intuitive, scalable, secure) without a measure; no unresolved placeholder;
       - *consistent*: it does not contradict another requirement, the plan or the charter, and uses the canonical term;
       - *complete*: actor, trigger or condition, response and, where it matters, a measurable threshold are all present.
       Example: "FR-003 'The page loads fast' fails testable and unambiguous; propose 'The dashboard renders its first view within 2 s for 95% of loads.'"
     - **Read the requirement against the EARS patterns.** Name the five patterns with their keywords in ASCII:
       - ubiquitous: "The <system> shall <response>";
       - event-driven: "When <trigger>, the <system> shall <response>";
       - state-driven: "While <state>, the <system> shall <response>";
       - unwanted behaviour: "If <condition>, then the <system> shall <response>";
       - optional feature: "Where <feature is included>, the <system> shall <response>".
       Say plainly that EARS is a **lens**, not a required template: a requirement in another clear, testable form is not a finding; a requirement that fits no pattern because its trigger, state or response is missing is (research R5).
     - **Check for observable behaviour.** The response must be something an actor or a test can observe (an output, a state change, a refusal with a message), not an internal intention ("the system handles errors gracefully").
     - **Audit scenarios per user story.** For each user story, list scenarios in five kinds: accepted (the spec says it succeeds), rejected (the spec says it is refused), missing edge (a plausible input or state the spec does not cover), surprising accepted (the spec as written lets through something a reader would expect refused), surprising rejected (the spec as written refuses something a reader would expect accepted). Every row cites a location: `spec.md`, `plan.md` or `tasks.md` with a line or heading. A story with no rejected scenario is itself worth a missing-edge row. A spec with no user stories: say so; do not invent stories.
     - **Ask clarification questions with concrete choices.** For a finding that needs a human decision, write one question, two to four concrete answer choices each with its implication, and a recommended choice; or, when the fix is not a judgement call, a concrete remediation (the reworded requirement). Example in the style of the specify prompt's "Question [N]" block.
     - **Label inferred findings.** A finding reached by reading and judgement (not by a command or a mechanical match) starts with `Inferred:`. Never write "proven", "verified" or "formally" about an inferred finding; this tactic offers no formal proof.
  3. Keep every character ASCII (use `-` not dashes, `->` not arrows, straight quotes). The tactic itself is not under the ASCII test path, but it is quoted into software-dev prompts and must not introduce non-ASCII there.
- **Files**: `packs/foundation/tactics/analysis/requirement-quality-ears.tactic.yaml` (new, about 80-120 lines).
- **Parallel?**: no (T002 cites it).
- **Notes**: do not add severities, finding ids or report headings; WP03 owns them. Do not add DRG edges here; WP04 owns the graphs. Do not add a `references:` block unless the schema at the pin allows it and the target exists in foundation (check `acceptance-criteria-non-vacuity` for precedent).

### Subtask T002 - Cite the quality bar from the specify prompt

- **Purpose**: specify writes requirements to the bar analyze checks (FR-016).
- **Steps**:
  1. Open `packs/foundation/missions/software-dev/steps/specify.prompt.md`. Find where requirements are generated (the step that says to generate separated requirement tables and label every FR row) and the "DO NOT" list.
  2. Add one short block (5-12 lines) titled `### Requirement quality bar` near the requirement-generation guidance. It must: name tactic `requirement-quality-ears` and how to fetch it (`spec-kitty charter context --include tactic:requirement-quality-ears`), list the five properties in one line, say the EARS patterns are the default phrasing for behavioural requirements and a lens rather than a mandate, and say `/spec-kitty.analyze` checks the same properties.
  3. Optionally add one line to the quality checklist block ("Requirements meet the requirement-quality bar (tactic requirement-quality-ears)"). Keep the existing checklist items unchanged.
- **Files**: `packs/foundation/missions/software-dev/steps/specify.prompt.md`.
- **Parallel?**: no.
- **Notes**: do not restate the tactic's definitions in the prompt; one line per concept at most. The prompt already references tactic `acceptance-criteria-non-vacuity` the same way; mirror that style.

### Subtask T003 - Trace the tactic against #247's list

- **Purpose**: prove coverage of the issue before review.
- **Steps**: make a short table in your WP history note (`spec-kitty agent tasks add-history WP01 --note ...`) mapping each #247 bullet to the tactic step that covers it: quality checks (five properties), EARS and observable behaviour, scenario audit tables (five kinds), clarification questions with concrete choices, inferred labelling and no formal proof. Also record FR-016 -> specify block.
- **Files**: none (event log only).

### Subtask T004 - Validate WP01 content

- **Steps**:
  ```bash
  export CHARTER_CONTRACT_DIR=<path to spec-kitty-charter at the lock pin>/contracts/packs   # CI fetches it itself
  scripts/ci/validate-packs.sh
  python3 -m pytest -q tests/ci/test_software_dev_ascii.py
  python3 scripts/ci/check_vocabulary.py
  grep -nP '[^\x00-\x7F]' packs/foundation/tactics/analysis/requirement-quality-ears.tactic.yaml || echo ascii-ok
  ```
  Do **not** restamp digests or bump versions here; WP05 does that once. The digest gate will be red locally until WP05; that is expected and must be stated in your hand-off note.
- **Notes**: the tactic is not reachable from any action until WP04 adds edges; schema validation still covers it.

## Risks & Mitigations

- The vocabulary guard refuses retired names: run it and reword.
- Over-long tactic: keep each step's description to what an agent needs; examples carry the detail.
- Severity creep: if you find yourself writing "HIGH", move it out; WP03 owns severities.

## Review Guidance

- The five properties, five EARS patterns, observable behaviour, five scenario kinds, clarification questions and inferred labelling are all present and defined once.
- EARS is stated as a lens, not a mandate.
- No severities, ids or report headings in the tactic.
- specify cites the tactic in a short block and does not restate it.
- ASCII in both files; `validate-packs.sh` green.

## Progress & Status

Progress, history, and status all live in the status event log - never in this prompt file.

- **Record a progress note**: `spec-kitty agent tasks add-history WP01 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP01 --to <status>`
- **View history and status**: `spec-kitty agent tasks status --mission analyze-readiness-gate-01M7SSEV`
