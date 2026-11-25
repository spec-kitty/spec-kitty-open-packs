---
work_package_id: WP06
title: 'Ledger D: homes in the language stacks'
dependencies:
- WP04
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
- T029
- T030
- T031
- T032
- T033
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
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-d-language-stacks.yaml
execution_mode: planning_artifact
model: ''
owned_files:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-d-language-stacks.yaml
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP06 - Ledger D: homes in the language stacks

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
- `curation/ledger-d-language-stacks.yaml` holds one row for every entry the merge map homes in `go`, `java`, `python`, `rust`, `javascript`, `drupal`: the home row of each cluster, and one `merged_into` row for each other member. The origin entries of these packs number 59 before merging; members merged in from downstream packs add to that, and members merged upstream leave.
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
- **Batch order**: the ledgers follow the home-pack order of the pack `depends_on` graph, so a home file exists before any dependent pack's `rejects` edge. This WP depends on WP04.
- **Batch note**: the stacks do not depend on each other, so a practice shared by two stacks cannot be homed in either; the map either homes it upstream (an operator question, see WP03) or keeps one file per stack. Rows the map homes upstream are already in ledgers A or B; this ledger holds only the stack-homed ones, plus a `rejects` reference for the rest (see the README).

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`. This is a planning-artifact WP.
- `spec-kitty agent action implement WP06 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T029 - Rows: go, java, python, rust

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (30 entries before merging):
  - `packs/go/styleguides/go-conventions.styleguide.yaml`: 10 entries, name/description/bad_example
  - `packs/java/styleguides/java-conventions.styleguide.yaml`: 6 entries, name/description/bad_example
  - `packs/python/styleguides/python-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/rust/styleguides/rust-conventions.styleguide.yaml`: 9 entries, name/description/bad_example
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T030 - Rows: javascript

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (15 entries before merging):
  - `packs/javascript/styleguides/css-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/javascript/styleguides/html-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/javascript/styleguides/typescript-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T031 - Rows: drupal

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (14 entries before merging):
  - `packs/drupal/styleguides/drupal-conventions.styleguide.yaml`: 9 entries, name/description/bad_example
  - `packs/drupal/styleguides/drupal-security-performance.styleguide.yaml`: 5 entries, name/description/bad_example
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T032 - Groundings, sources, merges, operator questions

- **Severity**: apply the operator's rubric (Q2, `curation/README.md`) per row: `smell` is worth a remark, `severe` should block review, `breaking` must block.
  - `severity_grounding` is one line that quotes the entry's or its host's deciding words. For example: "totals drift and equality checks fail" → a wrong result → `breaking`.
  - Two reviewers reading the quote should reach the same call. If they could not, or the text gives no signal, raise an `operator_question`. Never guess.
- **Bad example** (Q3):
  - A `name`/`bad_example` entry uses its `bad_example` verbatim, with `bad_example_source: bad_example`.
  - A `title`/`content` entry gets a short, concrete bad example the curator writes, grounded in the content, with `bad_example_source: authored, grounded in <content clause>`. It is new doctrine: keep it minimal and faithful to the content.
- **Merges**: check each row's `merged_into`, `merge_reason` and home against the merge map.
- **Operator questions**: collect them, including every no-signal severity, into a single message to the dispatcher session (`send_message` to the dispatcher named in the mission brief). The first line is "WP06 operator questions (N)". Number the items, and give each its row `source`, the question, and the 2-3 choices. Record that the questions were sent with `add-history`. Leave the rows' `operator_question` set until they are answered, then fill them in and clear the field.

### Subtask T033 - Dry run and check

- **Steps**:
  1. Copy `packs/` to a scratch directory.
  2. Run `python3 curation/apply_curation.py --root <scratch> --ledger curation/ledger-00-nodes.yaml --ledger curation/ledger-a-foundation.yaml --ledger curation/ledger-b-testing-writing.yaml --ledger curation/ledger-d-language-stacks.yaml`.
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
- Check coverage against the merge map: every source index the map homes in `go`, `java`, `python`, `rust`, `javascript`, `drupal` has exactly one row here.
- Check that the operator questions were sent, and that any answered ones are applied.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
