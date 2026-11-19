---
work_package_id: WP03
title: 'Analyze prompt: validation gate, per-WP readiness, requirement quality'
dependencies:
- WP02
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-004
- FR-005
- FR-010
- FR-013
- FR-014
- FR-015
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-005
- SC-001
- SC-002
- SC-003
- SC-004
- FR-006
- FR-007
- FR-008
- FR-009
planning_base_branch: feat/analyze-finalize-validate-246
merge_target_branch: feat/analyze-finalize-validate-246
branch_strategy: Planning artifacts for this mission were generated on feat/analyze-finalize-validate-246. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/analyze-finalize-validate-246 unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-analyze-readiness-gate-01M7SSEV
base_commit: d7de2256aff4a365db42dca2f5e16a60ce1ff1e6
created_at: '2026-11-19T13:51:24.523380+00:00'
subtasks:
- T009
- T010
- T011
- T012
- T013
- T014
phase: Phase 2 - Step prompt
history:
- at: '2026-11-19T12:07:01Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/missions/software-dev/steps/
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/missions/software-dev/steps/analyze.prompt.md
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP03 - Analyze prompt: validation gate, per-WP readiness, requirement quality

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
- **Report progress** with `spec-kitty agent tasks add-history WP03 --note "..."`.

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks. Use language identifiers in code blocks.

---

## Objectives & Success Criteria

`packs/foundation/missions/software-dev/steps/analyze.prompt.md` after this WP:

- Step 2a (#246, drafted in commit 59e1574) checks `spec-kitty --version` first and never runs the check below **3.1.0a5**; every could-not-run outcome (old CLI, command missing, no JSON, mission or repository resolution `error_code`) is a **HIGH** finding naming `spec-kitty CLI >= 3.1.0a5` and the installed version, plus a Residual Risk entry (FR-004; operator ruling D6). No "MEDIUM" for could-not-run remains anywhere.
- Refusal handling (FR-002), passing-run signals (FR-003) and the read-only rule (FR-005) from the draft are kept and still accurate.
- A new step 2b reviews every WP prompt by citing tactic `wp-prompt-readiness-review`, and the report gains a **Per-WP Readiness** section (FR-006..FR-010).
- A new detection pass G checks requirement quality and EARS, audits scenarios per user story, writes clarification questions with concrete choices and labels inferred findings, by citing tactic `requirement-quality-ears`; the report gains **Requirement Quality**, **Scenario Audit** and **Clarification Questions** sections (FR-011..FR-015).
- The report has one fixed section order and fixed finding-id prefixes (NFR-002; operator accepted the prefixes): D duplication, B ambiguity, U underspecification, K charter, C coverage, I inconsistency, V finalize-validation, W wp-readiness, Q requirement-quality, S scenario.
- All findings still go through the `analysis-findings/v1` carrier with `low|medium|high|critical` (NFR-003).
- At most 500 lines (NFR-004); ASCII (NFR-001); analyze stays read-only (C-001); no WP template key or section list (C-002).

## Context & Constraints

- Spec FR-001..FR-015, NFR-001..NFR-004, C-001, C-002. Plan IC-01, IC-02, IC-03 and "Design notes". data-model.md has the category/prefix table and the severity map: follow it exactly.
- Read the two tactics WP01 and WP02 produced; cite them by id with the fetch command `spec-kitty charter context --include tactic:<id>`. Also give each check a one-line summary in the prompt so the step works where tactic context is not surfaced (plan "Prompt vs tactic split").
- The current draft (lines around the `### 2a.` heading) says MEDIUM for could-not-run and lists `MISSION_AMBIGUOUS_SELECTOR` / `MISSION_CONTEXT_UNRESOLVED` as could-not-run examples: keep the examples, change the severity.
- The CLI evidence lives in research.md R1/R2. Do not invent payload keys.
- The prompt starts at about 310 lines. Budget: about +150 lines for steps 2b, G and the report sections. Trim the draft where it repeats itself before adding.

## Branch Strategy

- **Strategy**: populated by `finalize-tasks`.
- **Planning base branch**: `feat/analyze-finalize-validate-246`
- **Merge target branch**: `feat/analyze-finalize-validate-246`

```bash
spec-kitty agent action implement WP03 --agent claude --mission analyze-readiness-gate-01M7SSEV
```

## Subtasks & Detailed Guidance

### Subtask T009 - Step 2a: CLI version gate and HIGH could-not-run

- **Steps**:
  1. At the start of step 2a, add: run `spec-kitty --version`. If the version is below 3.1.0a5 (where `--validate-only` became non-writing; it first shipped in 3.0.0), do **not** run the check; record the could-not-run finding.
  2. Rewrite the "could not run" paragraph: severity **HIGH** (blocks the verdict, fail closed), category `finalize-validation`, summary names `spec-kitty CLI >= 3.1.0a5` and the installed version (or "not installed"), and how to get the check running (upgrade the CLI; pass an unambiguous `--mission` handle for resolution errors). Keep "do not re-implement the CLI's checks by hand".
  3. Grep the whole prompt for `MEDIUM` near "could not run" / "not run" and fix every one (severity heuristic, metrics).
  4. Keep the payload-key table; re-read it against research R1 (non-empty keys; ownership overlap only between WPs that can run in parallel).
- **Files**: the analyze prompt.

### Subtask T010 - Fixed report layout and finding-id prefixes

- **Steps**:
  1. Replace "generate stable IDs prefixed by category initial" with the fixed prefix table (one compact table or one line).
  2. In step 6, state the body's section order exactly: findings table; Finalize Validation; Per-WP Readiness; Requirement Quality; Scenario Audit; Clarification Questions; Coverage Summary; Residual Risk; Charter Alignment Issues; Unmapped Tasks; Metrics. Next Actions (step 8) follows. Sections with nothing to report say "None." rather than disappearing, so the layout is stable.
  3. Keep the carrier rules block unchanged except where it must mention the new categories.

### Subtask T011 - Step 2b: per-WP readiness pass and section

- **Steps**:
  1. Add `### 2b. Review Every WP Prompt` after 2a: read every `tasks/WP*.md` and apply tactic `wp-prompt-readiness-review` (fetch command). One-line summaries of its checks: pairing both ways; compare to the WP prompt template as resolved for this Mission (name gaps as the template names them; never from a list); profile load first; size (200-500 target; warn above 700 lines or 10 subtasks); dependency order; cohesive boundaries; requirement and value mapping.
  2. Severities: blocker -> `high` (missing or orphaned WP prompt; a template section or key implementation depends on is missing; a WP mapped to no requirement); quality improvement -> `medium` or `low` (profile not first, size, overbroad, weak mapping wording). Category `wp-readiness`, prefix W.
  3. Dedupe rule (R6): if step 2a reported a pairing refusal, the Per-WP Readiness rows cite that V finding id instead of raising W findings for the same files.
  4. Report section format: `| WP | Prompt file | In tasks.md | Blockers | Improvements |` with finding ids in the last two columns.
  5. Load-artifacts step: add "every `tasks/WP*.md`" to what is read (#237 asks that analyze stop relying on `tasks.md` alone). Keep progressive disclosure: read frontmatter and section headings first, body only where a check needs it.

### Subtask T012 - Pass G: requirement quality, EARS, scenario audit, clarification questions, inferred labels

- **Steps**:
  1. Add detection pass `#### G. Requirement Quality and Scenario Audit` citing tactic `requirement-quality-ears` (fetch command), with one-line summaries: five properties; EARS as a lens; observable behaviour; per-story scenario audit in five kinds with a location on every row; clarification questions with concrete choices; `Inferred:` labels and no claim of proof.
  2. Categories: `requirement-quality` (Q) and `scenario` (S). Severities per data-model.md.
  3. Rule: every HIGH or CRITICAL ambiguity or requirement-quality finding gets an entry in **Clarification Questions** (question, 2-4 choices with implications, a recommendation) or a concrete remediation in its Recommendation cell (FR-014).
  4. Scenario Audit section: one table per user story, `| Kind | Scenario | Location |`; "None." when the spec has no user stories (do not invent).
  5. Make pass B (ambiguity) and pass G not double-report: B keeps vague adjectives and placeholders; G judges the five properties and EARS. Say which owns what in one line.

### Subtask T013 - Severity heuristic, metrics, next actions

- **Steps**:
  1. Severity section: add the new sources compactly (could-not-run HIGH, refusal CRITICAL, stale finalization HIGH, WP blockers HIGH, scenario gaps on security or data-loss paths HIGH).
  2. Metrics: add `Finalize Validation (passed | refused | not run)` (exists), `WP prompts reviewed`, `WP blockers`, `Requirement-quality findings`, `Scenarios audited`, `Inferred findings`.
  3. Next Actions: a refusal or could-not-run names the command to fix it (`/spec-kitty.tasks-finalize`, CLI upgrade); WP blockers name the WP.
  4. Operating Principles: one line "Label judgement-based findings `Inferred:`; never claim formal proof."

### Subtask T014 - Line budget and ASCII check

```bash
wc -l packs/foundation/missions/software-dev/steps/analyze.prompt.md      # must be <= 500
python3 -m pytest -q tests/ci/test_software_dev_ascii.py
grep -nE "finalize-tasks" packs/foundation/missions/software-dev/steps/analyze.prompt.md   # every command form carries --validate-only, or is in a "never run" sentence
scripts/ci/validate-packs.sh
python3 scripts/ci/check_vocabulary.py
```

Record the line count in the WP history.

## Risks & Mitigations

- Line cap: trim duplication in the draft (the read-only rule is stated in three places; keep one constraint line and one guideline line).
- Determinism: a section that can be empty must still appear ("None.").
- Restating tactics: one line per check; the definitions live in the tactics.

## Review Guidance

- Could-not-run is HIGH everywhere, names `spec-kitty CLI >= 3.1.0a5`, and the check is not run below it.
- No writing finalize form is instructed; `--refresh-planning-commit` / `--allow-orphaned` appear only in the prohibition.
- Section order and id prefixes match data-model.md exactly.
- Both tactics are cited by id with the fetch command; no template key list.
- <= 500 lines, ASCII.
- Walk the spec's user stories 1-4 against the prompt: each acceptance scenario is reachable by following it.

## Progress & Status

- **Record a progress note**: `spec-kitty agent tasks add-history WP03 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP03 --to <status>`
- **View history and status**: `spec-kitty agent tasks status --mission analyze-readiness-gate-01M7SSEV`
