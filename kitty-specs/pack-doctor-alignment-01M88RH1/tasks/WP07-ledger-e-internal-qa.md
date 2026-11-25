---
work_package_id: WP07
title: 'Ledger E: homes in qa and internal'
dependencies:
- WP05
requirement_refs:
- FR-007
- FR-008
- FR-010
- NFR-002
- NFR-005
- C-004
planning_base_branch: feat/pack-doctor-alignment
merge_target_branch: feat/pack-doctor-alignment
branch_strategy: Planning artifacts for this mission were generated on feat/pack-doctor-alignment. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/pack-doctor-alignment unless the human explicitly redirects the landing branch.
subtasks:
- T034
- T035
- T036
- T037
- T038
phase: Phase 2 - Curation
history:
- at: '2026-11-25T07:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
- at: '2026-11-25T12:00:00Z'
  actor: claude::implementer-ivan
  action: Re-batched by home pack per decision 01M88RHDGQSS6R5R5ZCDCH84A2 (Q1)
agent_profile: curator-carla
authoritative_surface: kitty-specs/pack-doctor-alignment-01M88RH1/curation/
create_intent:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-e-internal-qa.yaml
execution_mode: planning_artifact
model: ''
owned_files:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-e-internal-qa.yaml
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP07 - Ledger E: homes in qa and internal

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `curator`
- **Profile override**: `curator-carla`
- **Agent/tool**: `claude`

---

## IMPORTANT: Review Feedback

Check `review_ref` with `spec-kitty agent tasks status --mission pack-doctor-alignment-01M88RH1`. Address every item.

---

## Objectives & Success Criteria
- `curation/ledger-e-internal-qa.yaml` holds one row for every entry the merge map homes in `qa`, `internal`: the home row of each cluster, and one `merged_into` row for each other member. The origin entries of these packs number 72 before merging; members merged in from downstream packs add to that, and members merged upstream leave.
- Every row follows `curation/README.md` (the ledger contract from WP02) exactly:
  - `title`, `description` and `good_example` are verbatim from the source;
  - `severity` comes with a `severity_grounding` that quotes the deciding words (Q2);
  - `bad_example` comes with a `bad_example_source`; authored ones are marked `authored, grounded in <content clause>` (Q3);
  - `merged_into`, `merge_reason` and the home agree with the merge map (Q1).
- No call is defaulted (NFR-002). Any call the text cannot ground is an `operator_question`, sent to the dispatcher in one batch (C-004).
- The dry run (ledger 00, the earlier ledgers, then this one, on a scratch copy) shows this batch's `artifact_schema_error` violations gone and no new code. `--check` faults only for the later batches' blocks.

## Context & Constraints

- **Read first**: `curation/README.md` (the contract), `data-model.md` (the ledger row), `research.md` R5 and R6, `spec.md` FR-007, FR-008, FR-010 and C-004, issue #350.
- **This is judgement work, and its review surface is the ledger.** Do not edit `packs/`. WP08 applies every ledger.
- **The three operator decisions govern this WP** (all resolved 2026-11-25): `01M88RHDGQSS6R5R5ZCDCH84A2` (Q1, merge by meaning into one home pack), `01M88RHFTS2X5HK1ZNP74G3WZ7` (Q2, severity rubric) and `01M88RHJ9HN4N8HDE97SJ6ZBAH` (Q3, authored bad examples). Quote them from `decisions/`.
- **Batch order**: the ledgers follow the home-pack order of the pack `depends_on` graph, so a home file exists before any dependent pack's `rejects` edge. This WP depends on WP05.
- **Batch note**: exact duplicates, all in `internal`: `CRUD / affordance echo`, `Command-named steps` and `Defect framing` appear in both `procedures/charter-offering-scenario-extraction` and `styleguides/feature-and-scenario-authoring`; `Over-broad, uncheckable scenario(s)` is a near pair across the same two files. One file per practice: the second row is `merged_into` the first, both owners keep a `rejects` edge, and `merge_reason` quotes the shared claim. If the two texts differ in substance, do not merge; raise it. The qa entries' owners are substep delegates of `qa`'s mission type: once applied, they clear 2 of the 3 `substep_delegation_unresolved` (`example-mapping-workshop`, in ledger A, clears the third).

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`. This is a planning-artifact WP.
- `spec-kitty agent action implement WP07 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T034 - Rows: internal procedures

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (54 entries before merging):
  - `packs/internal/procedures/charter-offering-scenario-extraction.procedure.yaml`: 6 entries, title/content (no bad_example)
  - `packs/internal/procedures/cloud-session-dispatch.procedure.yaml`: 9 entries, title/content (no bad_example)
  - `packs/internal/procedures/issue-to-mission-delivery.procedure.yaml`: 2 entries, title/content (no bad_example)
  - `packs/internal/procedures/issue-triage-pass.procedure.yaml`: 5 entries, title/content (no bad_example)
  - `packs/internal/procedures/landing-contributor-prs.procedure.yaml`: 5 entries, title/content (no bad_example)
  - `packs/internal/procedures/mission-tracer-files.procedure.yaml`: 3 entries, title/content (no bad_example)
  - `packs/internal/procedures/mission-wrap-up-sequence.procedure.yaml`: 7 entries, title/content (no bad_example)
  - `packs/internal/procedures/semi-auto-delivery.procedure.yaml`: 6 entries, title/content (no bad_example)
  - `packs/internal/procedures/test-suite-quality-assessment.procedure.yaml`: 4 entries, title/content (no bad_example)
  - `packs/internal/procedures/tracker-organisation-workflow.procedure.yaml`: 7 entries, title/content (no bad_example)
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T035 - Rows: internal styleguides, with the feature-and-scenario-authoring duplicates

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (16 entries before merging):
  - `packs/internal/styleguides/executive-debrief.styleguide.yaml`: 6 entries, name/description/bad_example
  - `packs/internal/styleguides/feature-and-scenario-authoring.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/internal/styleguides/report-writing.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/internal/styleguides/tiered-standards.styleguide.yaml`: 3 entries, name/description/bad_example
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T036 - Rows: qa

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (2 entries before merging):
  - `packs/qa/procedures/qa-go-no-go-readiness-review.procedure.yaml`: 1 entries, title/content (no bad_example)
  - `packs/qa/procedures/qa-test-plan-review-workshop.procedure.yaml`: 1 entries, title/content (no bad_example)
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T037 - Groundings, sources, merges, operator questions

- **Severity**: apply the operator's rubric (Q2, `curation/README.md`) per row: `smell` is worth a remark, `severe` should block review, `breaking` must block.
  - `severity_grounding` is one line that quotes the entry's or its host's deciding words. For example: "totals drift and equality checks fail" → a wrong result → `breaking`.
  - Two reviewers reading the quote should reach the same call. If they could not, or the text gives no signal, raise an `operator_question`. Never guess.
- **Bad example** (Q3):
  - A `name`/`bad_example` entry uses its `bad_example` verbatim, with `bad_example_source: bad_example`.
  - A `title`/`content` entry gets a short, concrete bad example the curator writes, grounded in the content, with `bad_example_source: authored, grounded in <content clause>`. It is new doctrine: keep it minimal and faithful to the content.
- **Merges**: check each row's `merged_into`, `merge_reason` and home against the merge map.
- **Operator questions**: collect them, including every no-signal severity, into a single message to the dispatcher session (`send_message` to the dispatcher named in the mission brief). The first line is "WP07 operator questions (N)". Number the items, and give each its row `source`, the question, and the 2-3 choices. Record that the questions were sent with `add-history`. Leave the rows' `operator_question` set until they are answered, then fill them in and clear the field.

### Subtask T038 - Dry run and check

- **Steps**:
  1. Copy `packs/` to a scratch directory.
  2. Run `python3 curation/apply_curation.py --root <scratch> --ledger curation/ledger-00-nodes.yaml --ledger curation/ledger-a-foundation.yaml --ledger curation/ledger-b-testing-writing.yaml --ledger curation/ledger-c-architecture-planning.yaml --ledger curation/ledger-e-internal-qa.yaml`.
  3. Run `--check` with the same ledgers.
  4. Run pack-doctor `validate --round-trip --full` over the scratch packs (see `quickstart.md`).
- **Expect**:
  - this batch's files no longer answer `artifact_schema_error`;
  - no new code (a new `drg_schema_error` or reference code means a row or an edge is wrong; a `rejects` target outside the owner's `depends_on` closure is a merge-map fault);
  - `--check` faults only for the later batches' blocks.
- **Record** the before and after counts per code in the WP history.

## Risks & Mitigations

- **Paraphrase creep.** `title`, `description` and `good_example` must be verbatim. Review this with a diff of each row's text against its source (`--check` verifies the applied text, not the source; review it here).
- **Merges that change meaning.** A merge joins texts that make the same claim. Where they differ in substance, the cluster splits or becomes an operator question.
- **Severity drift between batches.** Quote the rubric's own examples. Where a practice resembles a row in another batch, cite that row.

## Review Guidance

- Read every authored `bad_example` (Q3). Sample at least 20% of the other rows, and every `breaking` row. Check that the quote supports the call.
- Check coverage against the merge map: every source index the map homes in `qa`, `internal` has exactly one row here.
- Check that the operator questions were sent, and that any answered ones are applied.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
