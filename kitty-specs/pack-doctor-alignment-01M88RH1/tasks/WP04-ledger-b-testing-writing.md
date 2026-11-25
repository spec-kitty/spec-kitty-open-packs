---
work_package_id: WP04
title: 'Ledger B: homes in testing and writing'
dependencies:
- WP03
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
- T019
- T020
- T021
- T022
- T023
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
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-b-testing-writing.yaml
execution_mode: planning_artifact
model: ''
owned_files:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-b-testing-writing.yaml
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP04 - Ledger B: homes in testing and writing

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
- `curation/ledger-b-testing-writing.yaml` holds one row for every entry the merge map homes in `testing`, `writing`: the home row of each cluster, and one `merged_into` row for each other member. The origin entries of these packs number 77 before merging; members merged in from downstream packs add to that, and members merged upstream leave.
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
- **Batch order**: the ledgers follow the home-pack order of the pack `depends_on` graph, so a home file exists before any dependent pack's `rejects` edge. This WP depends on WP03.
- **Batch note**: near pair within `testing`: `Shared mutable state between scenarios` (procedure `bdd-scenario-lifecycle`) and `Shared mutable state between tests` (styleguide `testing-principles`); the merge map decides it. `writing` uses the per-kind graph layout (`styleguide.graph.yaml`, `procedure.graph.yaml`; no `anti_pattern.graph.yaml` yet: the apply creates it). `ai-writing-tells` is the 61st file the issue table omitted; check its shape before drafting.

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`. This is a planning-artifact WP.
- `spec-kitty agent action implement WP04 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T019 - Rows: testing

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (38 entries before merging):
  - `packs/testing/procedures/bdd-scenario-lifecycle.procedure.yaml`: 4 entries, title/content (no bad_example)
  - `packs/testing/procedures/development-assist-test-cleanup.procedure.yaml`: 5 entries, title/content (no bad_example)
  - `packs/testing/procedures/disciplined-defect-diagnosis.procedure.yaml`: 5 entries, title/content (no bad_example)
  - `packs/testing/procedures/test-first-bug-fixing.procedure.yaml`: 5 entries, title/content (no bad_example)
  - `packs/testing/styleguides/given-when-then-authoring.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/testing/styleguides/mutation-aware-test-design.styleguide.yaml`: 4 entries, name/description/bad_example
  - `packs/testing/styleguides/quadruple-a-test-format.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/testing/styleguides/test-desiderata-and-boundaries.styleguide.yaml`: 7 entries, name/description/bad_example
  - `packs/testing/styleguides/testing-principles.styleguide.yaml`: 4 entries, name/description/bad_example
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T020 - Rows: writing

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (39 entries before merging):
  - `packs/writing/procedures/meeting-minutes-pipeline.procedure.yaml`: 7 entries, title/content (no bad_example)
  - `packs/writing/styleguides/ai-writing-tells.styleguide.yaml`: 1 entries, name/description/bad_example
  - `packs/writing/styleguides/common-docs.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/writing/styleguides/divio-type-discipline.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/writing/styleguides/docs-accessibility.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/writing/styleguides/docs-freshness-sla.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/writing/styleguides/meeting-minutes-format.styleguide.yaml`: 6 entries, name/description/bad_example
  - `packs/writing/styleguides/plain-language.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/writing/styleguides/professional-communications.styleguide.yaml`: 3 entries, name/description/bad_example
  - `packs/writing/styleguides/publication-authority.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/writing/styleguides/research-citation-discipline.styleguide.yaml`: 6 entries, name/description/bad_example
  - `packs/writing/styleguides/writing/kitty-glossary-writing.styleguide.yaml`: 4 entries, name/description/bad_example
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T021 - Rows merged into a testing or writing home from downstream packs

- **Purpose**: write the member rows of every cluster homed in `testing`, `writing` whose source lies in a downstream pack.
- **Sources**: the merge map, filtered to these home packs.
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks, once the map exists.

### Subtask T022 - Groundings, sources, merges, operator questions

- **Severity**: apply the operator's rubric (Q2, `curation/README.md`) per row: `smell` is worth a remark, `severe` should block review, `breaking` must block.
  - `severity_grounding` is one line that quotes the entry's or its host's deciding words. For example: "totals drift and equality checks fail" → a wrong result → `breaking`.
  - Two reviewers reading the quote should reach the same call. If they could not, or the text gives no signal, raise an `operator_question`. Never guess.
- **Bad example** (Q3):
  - A `name`/`bad_example` entry uses its `bad_example` verbatim, with `bad_example_source: bad_example`.
  - A `title`/`content` entry gets a short, concrete bad example the curator writes, grounded in the content, with `bad_example_source: authored, grounded in <content clause>`. It is new doctrine: keep it minimal and faithful to the content.
- **Merges**: check each row's `merged_into`, `merge_reason` and home against the merge map.
- **Operator questions**: collect them, including every no-signal severity, into a single message to the dispatcher session (`send_message` to the dispatcher named in the mission brief). The first line is "WP04 operator questions (N)". Number the items, and give each its row `source`, the question, and the 2-3 choices. Record that the questions were sent with `add-history`. Leave the rows' `operator_question` set until they are answered, then fill them in and clear the field.

### Subtask T023 - Dry run and check

- **Steps**:
  1. Copy `packs/` to a scratch directory.
  2. Run `python3 curation/apply_curation.py --root <scratch> --ledger curation/ledger-00-nodes.yaml --ledger curation/ledger-a-foundation.yaml --ledger curation/ledger-b-testing-writing.yaml`.
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
- Check coverage against the merge map: every source index the map homes in `testing`, `writing` has exactly one row here.
- Check that the operator questions were sent, and that any answered ones are applied.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
