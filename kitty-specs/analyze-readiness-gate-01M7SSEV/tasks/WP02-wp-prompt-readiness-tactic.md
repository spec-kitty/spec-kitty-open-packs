---
work_package_id: WP02
title: WP prompt readiness tactic
dependencies:
- WP01
requirement_refs:
- FR-006
- FR-007
- FR-008
- FR-009
- FR-010
- C-002
planning_base_branch: feat/analyze-finalize-validate-246
merge_target_branch: feat/analyze-finalize-validate-246
branch_strategy: Planning artifacts for this mission were generated on feat/analyze-finalize-validate-246. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/analyze-finalize-validate-246 unless the human explicitly redirects the landing branch.
subtasks:
- T005
- T006
- T007
- T008
phase: Phase 1 - Doctrine
history:
- at: '2026-11-19T12:07:01Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/tactics/analysis/
create_intent:
- packs/foundation/tactics/analysis/wp-prompt-readiness-review.tactic.yaml
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/tactics/analysis/wp-prompt-readiness-review.tactic.yaml
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP02 - WP prompt readiness tactic

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
- **Report progress** with `spec-kitty agent tasks add-history WP02 --note "..."`.

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks. Use language identifiers in code blocks.

---

## Objectives & Success Criteria

- A new foundation tactic `wp-prompt-readiness-review` exists at `packs/foundation/tactics/analysis/wp-prompt-readiness-review.tactic.yaml` and is the single canonical checklist for reviewing every `tasks/WP*.md` prompt before implementation (#237):
  - pairing both ways between `tasks.md` and the WP prompt files (FR-006);
  - conformance of each WP prompt's frontmatter and body sections to the WP prompt template **as resolved for the Mission** (FR-007), naming no key or section (C-002);
  - the profile-load section comes first in the body; size guidance: target 200-500 lines, warn above 700 lines or more than 10 subtasks (FR-008);
  - dependency and ordering sense; cohesive, independently implementable, not overbroad boundaries; each WP maps to requirements and user value, judged with tactic `requirement-quality-ears` where the mapping wording is weak (FR-009);
  - every observation sorted as a readiness blocker or a quality improvement (FR-010).
- Valid against the tactic schema at the charter pin; ASCII.

## Context & Constraints

- Spec: FR-006..FR-010, C-002. Plan: IC-03; research R4 and R6.
- **Why defer to the template**: this repository's `packs/foundation/missions/software-dev/templates/task-prompt-template.md` and the copy bundled in spec-kitty CLI 4.0.0rc9 already differ (role/profile semantics, the profile-load heading). #230 reconciles the template and the tasks prompts. A list here would drift; the tactic must tell the agent to read the template the Mission resolves and compare against it.
- **Overlap with the validation step**: `finalize-tasks --validate-only` already refuses a WP file with no `tasks.md` section and vice versa (`missing_wp_sections`, `extra_wp_sections`). The tactic says: when that refusal exists, cite it rather than raising the same defect again (R6). The tactic should not name JSON keys (WP03 does); it can say "the finalize validation's pairing refusal".
- Severities and report layout belong to WP03. The tactic says blocker vs improvement, not HIGH/LOW.
- Shape and voice: as WP01 (see `acceptance-criteria-non-vacuity.tactic.yaml` and the doctrine-instruction-voice styleguide). Read the finished `requirement-quality-ears` tactic first.

## Branch Strategy

- **Strategy**: populated by `finalize-tasks`.
- **Planning base branch**: `feat/analyze-finalize-validate-246`
- **Merge target branch**: `feat/analyze-finalize-validate-246`

```bash
spec-kitty agent action implement WP02 --agent claude --mission analyze-readiness-gate-01M7SSEV
```

## Subtasks & Detailed Guidance

### Subtask T005 - Author `wp-prompt-readiness-review` tactic

- **Purpose**: a reusable, template-deferring review of WP prompts.
- **Steps**:
  1. Create the file with `schema_version: "1.0"`, `id: wp-prompt-readiness-review`, `name: WP Prompt Readiness Review`, and a `purpose` that says: the WP prompts, not `tasks.md`, are what implementation agents execute, so each must be ready before implementation; the review is read-only.
  2. Steps, in order:
     - **Pair `tasks.md` with the WP prompt files.** Every WP `tasks.md` names has exactly one prompt file; every prompt file is named in `tasks.md`. Missing and orphaned files are blockers. If the finalize validation already refused the pairing, cite that result.
     - **Resolve the template, then compare.** Read the WP prompt template as the Mission's template resolver returns it (do not assume a path or a copy). Compare each WP prompt's frontmatter keys and body sections to it. A key or section implementation depends on (identity, dependencies, ownership, execution mode, profile or role, objective, guidance, definition of done or success criteria, review guidance) that is missing or empty is a blocker; other gaps are improvements. Name what is missing **as the template names it**; never maintain a list in this tactic. Example: "WP03 lacks the template's review-guidance section - blocker."
     - **Profile first.** The first body section loads the assigned agent profile, before objective and context. Missing or later: improvement (the implementing agent may start without its profile).
     - **Size.** Target 200-500 lines; above 700 lines or more than 10 subtasks: improvement that recommends a split; under about 150 lines with fewer than 3 subtasks: improvement that suggests merging.
     - **Dependencies and order.** Dependencies make delivery sense (foundations first, no WP depending on later-phase work, no needless serialisation). A cycle is already a validation refusal - cite it.
     - **Boundaries.** Each WP is cohesive, independently implementable and reviewable, not overbroad (several unrelated concerns), not a bare chore with no outcome.
     - **Requirement and value mapping.** Each WP maps to at least one requirement and states the user value it serves; judge weak mapping wording with tactic `requirement-quality-ears`. A WP mapped to nothing is a blocker; a WP whose stated value is purely technical with no requirement trace is an improvement.
     - **Sort and report per WP.** One row per WP: blockers apart from improvements. Read-only: never edit a WP file.
  3. ASCII only.
- **Files**: the new tactic (about 70-110 lines).

### Subtask T006 - Prove the template deferral

- **Steps**:
  1. Grep the new tactic for any frontmatter key from either template copy:
     ```bash
     grep -nE "work_package_id|owned_files|authoritative_surface|planning_base_branch|merge_target_branch|branch_strategy|execution_mode|agent_profile|create_intent|shell_pid|task_type" packs/foundation/tactics/analysis/wp-prompt-readiness-review.tactic.yaml && echo "RESTATED - fix" || echo deferral-ok
     ```
  2. Prose names like "ownership" and "dependencies" are fine; literal key names are not.
  3. Record the result in the WP history.

### Subtask T007 - Trace the tactic against #237's list

- Map each #237 "It should validate" bullet and each acceptance criterion to the tactic step that covers it, in a history note. #237's frontmatter key list and section list are covered by "resolve the template, then compare" (C-002); say so explicitly.

### Subtask T008 - Validate WP02 content

```bash
scripts/ci/validate-packs.sh          # with CHARTER_CONTRACT_DIR at the pin locally
python3 scripts/ci/check_vocabulary.py
grep -nP '[^\x00-\x7F]' packs/foundation/tactics/analysis/wp-prompt-readiness-review.tactic.yaml || echo ascii-ok
```

Digests stay stale until WP05; say so in the hand-off note.

## Risks & Mitigations

- Restating the template (C-002): T006 catches literal keys.
- Double-reporting the pairing defect: the tactic tells the agent to cite the validation refusal (R6).

## Review Guidance

- No literal template key names; deferral wording is explicit about resolving the template.
- Blocker vs improvement is defined for each check; no HIGH/LOW words.
- Size thresholds exactly 200-500 target, 700 lines / 10 subtasks warning.
- Read-only stated.

## Progress & Status

- **Record a progress note**: `spec-kitty agent tasks add-history WP02 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP02 --to <status>`
- **View history and status**: `spec-kitty agent tasks status --mission analyze-readiness-gate-01M7SSEV`
