---
work_package_id: WP03
title: Ledger A, the language stacks (68 entries)
dependencies:
- WP02
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
- T014
- T015
- T016
- T017
- T018
phase: Phase 2 - Curation
history:
- at: '2026-11-25T07:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: curator-carla
authoritative_surface: kitty-specs/pack-doctor-alignment-01M88RH1/curation/
create_intent:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-a-language-stacks.yaml
execution_mode: planning_artifact
model: ''
owned_files:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-a-language-stacks.yaml
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP03 - Ledger A, the language stacks (68 entries)

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

- `curation/ledger-a-language-stacks.yaml` holds one row for every inline `anti_patterns` entry of the files below. There are 68 entries in all.
- Every row follows `curation/README.md` (the ledger contract from WP02) exactly:
  - `title`, `description` and `good_example` are verbatim from the source;
  - `severity` comes with a `severity_grounding` that quotes the deciding words;
  - `bad_example` comes with a `bad_example_source`;
  - merges follow decision Q1.
- No call is defaulted (NFR-002). Any call the text cannot ground is an `operator_question`, sent to the dispatcher in one batch (C-004).
- `apply_curation.py --check` (with only this ledger and ledger 00 applied to a scratch copy) reports no fault other than the inline blocks of the other batches. The dry-run pack-doctor run shows this batch's `artifact_schema_error` violations gone.

## Context & Constraints

- **Read first**: `curation/README.md` (the contract), `data-model.md` (the ledger row), `research.md` R5 and R6, `spec.md` FR-007, FR-008, FR-010 and C-004, issue #350.
- **This is judgement work, and its review surface is the ledger.** Do not edit `packs/`. WP08 applies every ledger.
- **The three operator decisions govern this WP:** `01M88RHDGQSS6R5R5ZCDCH84A2` (dedupe), `01M88RHFTS2X5HK1ZNP74G3WZ7` (severity rubric) and `01M88RHJ9HN4N8HDE97SJ6ZBAH` (bad example). Do not start drafting severities until the rubric is resolved (`spec-kitty agent decision list --mission pack-doctor-alignment-01M88RH1`). Rows, ids and verbatim text can be drafted before then.
- **Batch note**: Cross-pack near pair: go `Float64 Money` and rust `Float Money`. They stay two files in their own packs unless decision Q1 allows a cross-pack merge (go and rust do not depend on each other). Name the pair in the WP history either way.

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`. This is a planning-artifact WP.
- `spec-kitty agent action implement WP03 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T014 - Rows: architecture, drupal, event-driven (23 entries)

- **Purpose**: draft one ledger row per entry, with verbatim text and a derived id.
- **Sources**:
  - `packs/architecture/procedures/event-storming-discovery.procedure.yaml`: 4 entries, title/content (no bad_example)
  - `packs/architecture/styleguides/aggregate-design-rules.styleguide.yaml`: 2 entries, name/description/bad_example
  - `packs/drupal/styleguides/drupal-conventions.styleguide.yaml`: 9 entries, name/description/bad_example
  - `packs/drupal/styleguides/drupal-security-performance.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/event-driven/styleguides/evd-event-naming-and-payload.styleguide.yaml`: 3 entries, name/description/bad_example
- **Steps**: for each entry, in source order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id`, by the README's id rule.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T015 - Rows: go, java, python, rust (30 entries)

- **Purpose**: draft one ledger row per entry, with verbatim text and a derived id.
- **Sources**:
  - `packs/go/styleguides/go-conventions.styleguide.yaml`: 10 entries, name/description/bad_example
  - `packs/java/styleguides/java-conventions.styleguide.yaml`: 6 entries, name/description/bad_example
  - `packs/python/styleguides/python-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/rust/styleguides/rust-conventions.styleguide.yaml`: 9 entries, name/description/bad_example
- **Steps**: for each entry, in source order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id`, by the README's id rule.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T016 - Rows: javascript (15 entries)

- **Purpose**: draft one ledger row per entry, with verbatim text and a derived id.
- **Sources**:
  - `packs/javascript/styleguides/css-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/javascript/styleguides/html-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
  - `packs/javascript/styleguides/typescript-conventions.styleguide.yaml`: 5 entries, name/description/bad_example
- **Steps**: for each entry, in source order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id`, by the README's id rule.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T017 - Groundings, sources, merges, operator questions

- **Severity**: apply the decided rubric (`curation/README.md`) per row.
  - `severity_grounding` quotes the entry's or its host's deciding words. For example: "a wrong result or an unsafe outcome → breaking"; "defeats the guidance's purpose → severe"; "a readability or style cost → smell".
  - Two reviewers reading the quote should reach the same call. If they could not, raise an `operator_question`.
- **Bad example**:
  - A `name`/`bad_example` entry uses its `bad_example` verbatim, with `bad_example_source: bad_example`.
  - A `title`/`content` entry uses the content's concrete-instance sentence, verbatim, with `bad_example_source: content sentence <n>`. This follows decision Q3; use its exact wording.
  - A content with no concrete instance gets an `operator_question`. Never invent an example.
- **Merges**: per decision Q1 and the batch note above.
- **Operator questions**: collect them into a single message to the dispatcher session (`send_message` to the dispatcher named in the mission brief). The first line is "WP03 operator questions (N)". Number the items, and give each its row `source`, the question, and the 2-3 choices. Record that the questions were sent with `add-history`. Leave the rows' `operator_question` set until they are answered, then fill them in and clear the field.

### Subtask T018 - Dry run and check

- **Steps**:
  1. Copy `packs/` to a scratch directory.
  2. Run `python3 curation/apply_curation.py --root <scratch> --ledger curation/ledger-00-nodes.yaml --ledger curation/ledger-a-language-stacks.yaml`.
  3. Run `--check` with the same ledgers.
  4. Run pack-doctor `validate --round-trip --full` over the scratch packs (see `quickstart.md`).
- **Expect**:
  - this batch's files no longer answer `artifact_schema_error`;
  - no new code from this batch's packs (a new `drg_schema_error` or reference code means a row is wrong);
  - `--check` faults only for the other batches' blocks.
- **Record** the before and after counts per code in the WP history.

## Risks & Mitigations

- **Paraphrase creep.** Text must be verbatim. Review this with a diff of each row's text against its source (`--check` verifies the applied text, not the source; review it here).
- **Severity drift between batches.** Quote the rubric's own examples. Where a practice resembles a row in another batch, cite that row.

## Review Guidance

- Sample at least 20% of the rows, and every `breaking` row. Check that the quote supports the call, and that `bad_example` is a concrete instance, not a restated description.
- Check that every source index is covered: the row count equals 68, minus nothing.
- Check that the operator questions were sent, and that any answered ones are applied.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
