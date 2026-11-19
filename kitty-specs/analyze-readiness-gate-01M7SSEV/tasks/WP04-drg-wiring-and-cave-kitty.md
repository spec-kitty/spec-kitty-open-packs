---
work_package_id: WP04
title: DRG wiring and cave-kitty parity
dependencies:
- WP03
requirement_refs:
- FR-017
- C-003
- SC-005
planning_base_branch: feat/analyze-finalize-validate-246
merge_target_branch: feat/analyze-finalize-validate-246
branch_strategy: Planning artifacts for this mission were generated on feat/analyze-finalize-validate-246. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/analyze-finalize-validate-246 unless the human explicitly redirects the landing branch.
subtasks:
- T015
- T016
- T017
- T018
- T019
phase: Phase 3 - Wiring and parity
history:
- at: '2026-11-19T12:07:01Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/foundation/
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- packs/foundation/tactic.graph.yaml
- packs/foundation/action.graph.yaml
- packs/cave-kitty/missions/cave-dev/steps/analyze.prompt.md
- packs/cave-kitty/drg/fragment.yaml
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP04 - DRG wiring and cave-kitty parity

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
- **Report progress** with `spec-kitty agent tasks add-history WP04 --note "..."`.

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks. Use language identifiers in code blocks.

---

## Objectives & Success Criteria

- `packs/foundation/tactic.graph.yaml` has nodes `tactic:requirement-quality-ears` and `tactic:wp-prompt-readiness-review` (kind `tactic`, label = the tactic `name`), in the file's sort order, plus `suggests` edges where they help an agent move between related tactics (at least `wp-prompt-readiness-review` -> `requirement-quality-ears`; consider `requirement-quality-ears` -> `acceptance-criteria-non-vacuity`), each with a `when`.
- `packs/foundation/action.graph.yaml` has `scope` edges: `action:software-dev/specify` -> `tactic:requirement-quality-ears`; `action:software-dev/analyze` -> `tactic:requirement-quality-ears`; `action:software-dev/analyze` -> `tactic:wp-prompt-readiness-review`.
- `packs/cave-kitty/missions/cave-dev/steps/analyze.prompt.md` names the finalize validation (with the read-only rule and the 3.1.0a5 gate), the per-WP readiness review, the requirement-quality and scenario-audit sections, and the two tactics, in caveman voice, keeping its "inherits the software-dev contract" framing and exact payloads (FR-017).
- cave-kitty's DRG fragment scopes the two foundation tactics to `action:cave-dev/analyze` (and `requirement-quality-ears` to `action:cave-dev/specify`) **if** the fragment already scopes doctrine to cave-dev actions in a shape the validator accepts for foundation-qualified targets; otherwise record why not.
- `validate-packs.sh` (including cross-pack checks) reports 0 violations.

## Context & Constraints

- Spec FR-017, C-003. Plan IC-04 and the WP02/WP03 outputs.
- Graph shapes: read the top of `packs/foundation/tactic.graph.yaml` (nodes then edges; `suggests` edges carry `when`) and `packs/foundation/action.graph.yaml` (nodes for actions; `scope` edges from `action:software-dev/<step>` to `tactic:<id>`). Foundation-local references are unqualified.
- cave-kitty: `packs/cave-kitty/pack.yaml` depends on foundation (`>=2.0,<3`); a foundation tactic is referenced from its fragment as `foundation::tactic:<id>` (see how `packs/testing/drg/fragment.yaml` references `foundation::tactic:acceptance-criteria-non-vacuity`). The cave-dev actions are declared in the cave-kitty fragment (`action:cave-dev/analyze`, `action:cave-dev/specify`).
- cave-kitty voice: read `packs/cave-kitty/styleguides/` and the existing analyze prompt. Terse, verdict first, every negation kept, payload exact; blockers stated in full sentences ("cliff edge -> full sentences").
- cave-kitty is not under the software-dev ASCII test, but keep commands, ids and severities byte-exact.

## Branch Strategy

- **Strategy**: populated by `finalize-tasks`.
- **Planning base branch**: `feat/analyze-finalize-validate-246`
- **Merge target branch**: `feat/analyze-finalize-validate-246`

```bash
spec-kitty agent action implement WP04 --agent claude --mission analyze-readiness-gate-01M7SSEV
```

## Subtasks & Detailed Guidance

### Subtask T015 - Tactic graph nodes and edges

- **Steps**: add the two nodes in the existing order (check whether nodes are sorted by urn; keep it). Add the `suggests` edges with `when` text in the house style ("Judge a WP's requirement mapping wording", ...). Do not touch `generated_at` / `generated_by`.

### Subtask T016 - Action graph scope edges

- **Steps**: add the three `scope` edges near the other edges of the same source action (follow the file's grouping). Confirm both action nodes exist (`action:software-dev/specify`, `action:software-dev/analyze`).

### Subtask T017 - cave-kitty analyze prompt parity

- **Steps**:
  1. Keep the existing sections (Role, Requested role, Directive citation, Canonical artifact, Voice).
  2. Add a section `## Readiness checks (inherited, named here)` that says, tersely: run `spec-kitty agent mission finalize-tasks --validate-only --mission <slug> --json` only (never the writing form; never `--refresh-planning-commit`); check `spec-kitty --version` first and do not run below 3.1.0a5; refusal = CRITICAL; could not run = HIGH, name `spec-kitty CLI >= 3.1.0a5`; review every `tasks/WP*.md` with `foundation` tactic `wp-prompt-readiness-review`; check requirements and audit scenarios with tactic `requirement-quality-ears`; label judgement findings `Inferred:`. The report sections and ids are software-dev's (point at the software-dev analyze step).
  3. Voice rules: add one bullet that a CRITICAL or HIGH finding (refusal, could-not-run, WP blocker) is a cliff edge -> full sentences.
  4. Update the opening paragraph that says the rubric reads "spec.md, plan.md and tasks.md": it now also reads every WP prompt and the finalize validation.
- **Files**: `packs/cave-kitty/missions/cave-dev/steps/analyze.prompt.md`.

### Subtask T018 - cave-kitty DRG fragment edges

- **Steps**:
  1. Read `packs/cave-kitty/drg/fragment.yaml` fully. If it already has `scope` edges from `action:cave-dev/*` or `mission_type:cave-dev` to doctrine, add `action:cave-dev/analyze` -> `foundation::tactic:wp-prompt-readiness-review` and -> `foundation::tactic:requirement-quality-ears`, and `action:cave-dev/specify` -> `foundation::tactic:requirement-quality-ears`.
  2. If the cross-pack validator refuses a qualified target here (outside the closure, or an edge kind it does not allow), revert and record the reason in the WP history; the prompt citation (T017) still delivers FR-017.

### Subtask T019 - Cross-pack validation of the wiring

```bash
scripts/ci/validate-packs.sh           # 0 violations, cross-pack included
python3 -m pytest -q tests/ci/test_graph_edge_identity.py tests/ci/test_prompt_fragments.py
python3 scripts/ci/check_vocabulary.py
```

The charter service (composition and registration) runs in CI; if you can run `scripts/ci/charter_service_check.py` locally, do. Digests stay stale until WP05.

## Risks & Mitigations

- Edge-identity test: duplicate or mis-shaped edges fail `test_graph_edge_identity.py`.
- Qualified references outside `depends_on` closure: cave-kitty depends on foundation, so `foundation::` is inside the closure; anything else is not.

## Review Guidance

- Two nodes, three scope edges, at least one `suggests` edge with `when`.
- cave-kitty prompt: same checks, severities and commands as software-dev, terse, payload exact, "inherits" framing kept.
- Fragment edges added or a recorded reason why not.
- Validation green.

## Progress & Status

- **Record a progress note**: `spec-kitty agent tasks add-history WP04 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP04 --to <status>`
- **View history and status**: `spec-kitty agent tasks status --mission analyze-readiness-gate-01M7SSEV`
