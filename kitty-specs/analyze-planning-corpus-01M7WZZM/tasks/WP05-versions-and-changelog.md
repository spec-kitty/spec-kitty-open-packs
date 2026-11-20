---
work_package_id: WP05
title: Versions, derived outputs and changelog
dependencies:
- WP02
- WP03
- WP04
requirement_refs:
- FR-017
- NFR-003
- SC-004
- C-005
- C-006
planning_base_branch: t3/analyze-planning-corpus-coherence
merge_target_branch: t3/analyze-planning-corpus-coherence
branch_strategy: Planning artifacts for this mission were generated on t3/analyze-planning-corpus-coherence. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into t3/analyze-planning-corpus-coherence unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-analyze-planning-corpus-01M7WZZM
base_commit: c6a07eacca31c5dc70b33bf2640540c2c418f108
created_at: '2026-11-20T18:08:22.008992+00:00'
subtasks:
- T016
- T017
- T018
history:
- at: '2026-11-20T18:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
model: sonnet
owned_files:
- packs/foundation/pack.yaml
- packs/architecture/pack.yaml
- packs/planning-analysis/pack.yaml
- packs/refactoring/pack.yaml
- packs/testing/pack.yaml
- packs/writing/pack.yaml
- packs/built-in/pack.yaml
- packs/cave-kitty/pack.yaml
- packs/foundation.source.yaml
- packs/architecture.source.yaml
- packs/planning-analysis.source.yaml
- packs/refactoring.source.yaml
- packs/testing.source.yaml
- packs/writing.source.yaml
- packs/built-in.source.yaml
- packs/cave-kitty.source.yaml
- packs/foundation/pack-manifest.yaml
- packs/cave-kitty/pack-manifest.yaml
- docs/packs/*.md
- tests/ci/test_pack_digest.py
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP05 - Versions, derived outputs and changelog

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, do what the skill does: run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `implementer-ivan` (empty means: select from the role)
- **Agent/tool**: `claude`

If no profile override is set, use the profile the active preset activates for the role; otherwise run `spec-kitty agent profile list` and load a profile whose `role` is it (or, failing that, whose `alt-roles` include it), preferring one whose specialization context matches this work package's languages and `authoritative_surface`. In this repository the profile YAML lives under `packs/*/agent_profiles/implementer-ivan.agent.yaml`; read it in full.

---

## IMPORTANT: Review Feedback

**Read this first if you are implementing this task!**

- **Has review feedback?**: Check the `review_ref` field in the event log (via `spec-kitty agent tasks status`).
- **You must address all feedback** before your work is complete. Feedback items are your implementation TODO list.
- **Report progress**: As you address each feedback item, record what you changed with `spec-kitty agent tasks add-history WP05 --note "..."` (stored in the status event log).

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks: `` `<div>` ``, `` `<script>` ``
Use language identifiers in code blocks: ````python`,````bash`

---

## Objectives & Success Criteria

Release hygiene for an **additive** pack change (DIRECTIVE_018; `docs/guides/contribute-a-pack.md`; precedent commit `6dce39c`): minor-bump the foundation lockstep, built-in and cave-kitty; regenerate every derived output with its tool; add the CHANGELOG entry; run every gate green (FR-017, NFR-003, SC-004, C-005).

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

Read `git show 6dce39c --stat` and `git show 6dce39c` first — it is the exact template for this WP.

### Subtask T016 - Version bump

- Lockstep packs at `pack_version: 3.1.0` → **`3.2.0`**: foundation, architecture, planning-analysis, refactoring, testing, writing (`packs/<p>/pack.yaml`). Verify the set with `grep -n "pack_version" packs/*/pack.yaml` and `grep -rln '"==3.1.0"' packs/*/pack.yaml`.
- Every exact pin `range: "==3.1.0"` on a lockstep pack → `"==3.2.0"` (in built-in and the lockstep packs). Ranges like `>=2.0,<4` stay.
- `packs/built-in/pack.yaml` `5.1.0` → **`5.2.0`**; `packs/cave-kitty/pack.yaml` `2.3.0` → **`2.4.0`** (if cave-kitty pins foundation exactly, move that pin too).
- Tighten cave-kitty's foundation dependency range from `">=2.0,<4"` to `">=3.2,<4"`: its fragment now scopes tactics that exist only from foundation 3.2.0. Check other cave-kitty references to foundation-only content still hold under that range.
- Never touch a `pack_id`.
- Versioning note for the PR body: the 2026-11-18 "share one bump" ruling covered the #300/#302/#303 batch; the latest analyze precedent (`6dce39c`) bumped while unreleased. If the operator prefers to fold into 3.1.0/5.1.0/2.3.0, the bump commit drops cleanly.

### Subtask T017 - Derived outputs (tools only, C-006)

- Manifests: `python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/foundation` and `... packs/cave-kitty` (and any other pack whose files changed, e.g. a version-only change does not alter constituents but run it for every bumped pack if the manifest records the version; check `git diff`).
- Digests (only git-tracked files count — commit content first, then restamp): `python3 scripts/ci/pack_digest.py --update <pack>` for every changed pack (each `packs/<p>.source.yaml`). Then update `BUILT_IN_DIGEST` in `tests/ci/test_pack_digest.py` to the new `packs/built-in.source.yaml` value (the test hard-codes it).
- Pages: `python3 scripts/docs/gen_pack_reference.py` (then `--check`).

### Subtask T018 - CHANGELOG and gates

- `docs/changelog/CHANGELOG.md` (the root `CHANGELOG.md` is a symlink): add under `## [Unreleased]` → `### ✨ Added` (at the top of that subsection) an entry in the house style — bold impact-first lead with the issue refs, then before → after:
  - **Analyze reviews the whole planning corpus and product coherence** (#213, #214, #247; epic #244). Before: the analyze step read only spec, plan, tasks and WP prompts. After: it reads every `check-prerequisites` inventory artifact (`feature_dir` excluded), `meta.json` creation intent and `occurrence_map.yaml`, headings-first; pass H (`X`, tactic `planning-corpus-consistency`) reports decision continuity, data-model/contract/quickstart gaps and ungrounded work at normal severity; pass J (`M`, tactic `product-coherence-review`) judges intent drift, MVP slice, vertical slice, overbuild, lost scenarios, sequencing and grouping, capped at MEDIUM so it never blocks, and ends in one `Recommendation:` line. #247 folds: only missing-edge/surprising scenario rows become `S` findings (Finding column, fixed order), `Inferred:` placement stated, duplicated untestable rule folded; tests pin the #247 content. cave-dev names the same checks. Versions: foundation lockstep 3.2.0, built-in 5.2.0, cave-kitty 2.4.0.
  - Do not write a guarded "advisory" phrase (the vocabulary guard scans `packs/` only, but keep the wording consistent anyway).
- Bump the CHANGELOG front-matter `updated:` to today (`2026-11-20` already; keep it current). Bump `updated:` on any other touched doc page with front matter if `check_docs_freshness.py` asks.
- **Issue matrix (SC-003)**: if `kitty-specs/analyze-planning-corpus-01M7WZZM/issue-matrix.json` exists (the CLI may scaffold it), the orchestrator fills it at review time; you do **not** own `kitty-specs/`. Instead, append to the CHANGELOG entry nothing extra — but write a short acceptance-criteria trace (each #213/#214/#247 acceptance criterion → prompt line or test name) into add-history so the orchestrator can paste it into the PR body and the matrix.
- Gates (all must pass; paste the tail of each into add-history):
  - `bash scripts/ci/validate-packs.sh`
  - `.venv/bin/python -m pytest -q tests`
  - `python3 scripts/ci/check_vocabulary.py`
  - `python3 scripts/docs/gen_pack_reference.py --check`
  - `bash scripts/ci/check-pack-digests.sh`
  - `python3 scripts/docs/check_docs_freshness.py --base origin/main`
  - If available: `bash scripts/ci/charter_drift_test.sh` and `python3 scripts/ci/charter_service_check.py` (report "not run" with the reason if their prerequisites — Java/the charter jar — are missing).

## Risks & Mitigations

- Missed exact pin → validator/charter service refuses: grep before and after.
- Hand-edited digest/manifest/page → CI drift: only tools write them.
- Digest constant: run `pytest tests/ci/test_pack_digest.py` after updating it.

## Review Guidance

- Versions match the plan; every `==3.1.0` pin moved; no `pack_id` changed; derived files match their tools (`--check` modes pass); CHANGELOG entry present with issue refs; all gates green.

## Progress & Status

Progress, history, and status all live in the status event log
(`status.events.jsonl`) - never in this prompt file. Do **not** hand-edit a
history section here.

- **Record a progress note**: `spec-kitty agent tasks add-history WP05 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP05 --to <status>`
- **View history and status**: `spec-kitty agent tasks status`

**Read status only through the CLI** (`spec-kitty agent tasks status --mission analyze-planning-corpus-01M7WZZM`),
which reads the Mission's resolved status surface. Never read `status.events.jsonl` or
`status.json` from the files of a lane worktree, a coordination worktree or any other
checkout: only the CLI's read counts.
