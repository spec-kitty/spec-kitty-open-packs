---
work_package_id: WP03
title: 'Merge map, and ledger A: homes in foundation'
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
- at: '2026-11-25T12:00:00Z'
  actor: claude::implementer-ivan
  action: Re-batched by home pack per decision 01M88RHDGQSS6R5R5ZCDCH84A2 (Q1)
agent_profile: curator-carla
authoritative_surface: kitty-specs/pack-doctor-alignment-01M88RH1/curation/
create_intent:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/merge-map.yaml
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-a-foundation.yaml
execution_mode: planning_artifact
model: ''
owned_files:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/merge-map.yaml
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-a-foundation.yaml
role: curator
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP03 - Merge map, and ledger A: homes in foundation

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

- `curation/merge-map.yaml` assigns each of the 273 inline entries (61 files) to exactly one cluster, with its home pack, per decision Q1 and the README's merge-map contract. Every merge that may join different meanings, and every case where the home rule would move a stack- or domain-specific practice into a more general pack, is an `operator_question`, sent in one batch.
- `curation/ledger-a-foundation.yaml` holds one row for every entry the merge map homes in `foundation`: the home row of each cluster, and one `merged_into` row for each other member. The origin entries of these packs number 23 before merging; members merged in from downstream packs add to that, and members merged upstream leave.
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
- **Batch order**: the ledgers follow the home-pack order of the pack `depends_on` graph, so a home file exists before any dependent pack's `rejects` edge. This WP depends on WP02.
- **Batch note**: this WP opens with the merge map, which every later ledger WP reads. `foundation` is upstream of every pack, so the home rule can pull a stack- or domain-specific practice into it (for example go `float64 Money` with rust `Float Money`: their only common upstreams are `foundation` and `testing`). Raise each such case as an `operator_question` in the map, in one batch; do not decide it (dispatcher ruling 2026-11-25). Precedent: charter `service/packs/src/testFixtures/resources/example-packs/built-in/anti_patterns/` holds curated copies of `adversarial-squad-deployment` entries (for example `averaging-divergent-verdicts: severe`). Cite that severity as `severity_grounding: "charter example-pack precedent: <file> severity <x>"` where the entry is the same text, and say if the texts differ. `example-mapping-workshop` is a substep delegate of `qa`'s mission type: applying its row clears one of the 3 `substep_delegation_unresolved`. `foundation` already holds `assert-on-mock-interactions` and `mock-owned-logic-to-pin-a-call-contract` (ledger 00): a matching entry elsewhere merges into them.

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`. This is a planning-artifact WP.
- `spec-kitty agent action implement WP03 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T014 - The merge map over all 273 entries

- **Purpose**: decide, once and before any ledger row, which entries are one practice and where each practice lives (Q1).
- **Steps**:
  1. List every source index of the 61 files (`packs/*/{styleguides,procedures}/**`), with its verbatim title and text.
  2. Group by meaning: entries whose texts make the same claim. Exact and near titles are a hint, not a rule; record `merge_reason` as the shared claim, quoted from both texts.
  3. Pick each cluster's home pack: the most foundational pack upstream of every member's pack, preferring one an existing `depends_on` already reaches. Add `depends_on` only where needed, never a cycle, and record it.
  4. Pick each cluster's id by the README's id rule, unique within its home pack.
  5. Raise an `operator_question` for each cluster whose members' meanings may differ, and for each that the home rule would move into a more general pack than any member (see the batch note). Send them in one batch, first line "WP03 merge-map operator questions (N)".
- **Expect**: about 150 clusters (the target, not a quota). Record the cluster count and the per-home counts in the WP history; WP04-WP07 read their row counts from it.

### Subtask T015 - Rows: foundation

- **Purpose**: draft one ledger row per entry the merge map homes in these packs, with verbatim text. Entries of these packs that the map homes upstream are written in the earlier ledger, not here.
- **Origin files** (23 entries before merging):
  - `packs/foundation/procedures/adversarial-squad-deployment.procedure.yaml`: 11 entries, title/content (no bad_example)
  - `packs/foundation/procedures/example-mapping-workshop.procedure.yaml`: 4 entries, title/content (no bad_example)
  - `packs/foundation/procedures/post-merge-arch-gate-adjudication.procedure.yaml`: 5 entries, title/content (no bad_example)
  - `packs/foundation/styleguides/boring-code-review.styleguide.yaml`: 3 entries, name/description/bad_example
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks.

### Subtask T016 - Rows merged into a foundation home from downstream packs

- **Purpose**: write the member rows of every cluster homed in `foundation` whose source lies in a downstream pack.
- **Sources**: the merge map, filtered to these home packs.
- **Steps**: for each row, in merge-map order:
  1. `source: <pack-relative path>#/anti_patterns/<index>`.
  2. `source_title`, `pack`, and `owner`: `styleguide:<id>` or `procedure:<id>`, from the owner file's `id`.
  3. `id` from the merge map (the README's id rule); `merged_into` and `merge_reason` for a non-home member.
  4. `title` and `description`: verbatim. A `title`/`content` entry gives `title` → `title` and `content` → `description`.
  5. `good_example`: verbatim, or omitted.
  6. Leave `severity`, `bad_example` and their sources to the grounding subtask.
- **Parallel?**: yes, with the other row subtasks, once the map exists.

### Subtask T017 - Groundings, sources, merges, operator questions

- **Severity**: apply the operator's rubric (Q2, `curation/README.md`) per row: `smell` is worth a remark, `severe` should block review, `breaking` must block.
  - `severity_grounding` is one line that quotes the entry's or its host's deciding words. For example: "totals drift and equality checks fail" → a wrong result → `breaking`.
  - Two reviewers reading the quote should reach the same call. If they could not, or the text gives no signal, raise an `operator_question`. Never guess.
- **Bad example** (Q3):
  - A `name`/`bad_example` entry uses its `bad_example` verbatim, with `bad_example_source: bad_example`.
  - A `title`/`content` entry gets a short, concrete bad example the curator writes, grounded in the content, with `bad_example_source: authored, grounded in <content clause>`. It is new doctrine: keep it minimal and faithful to the content.
- **Merges**: check each row's `merged_into`, `merge_reason` and home against the merge map.
- **Operator questions**: collect them, including every no-signal severity, into a single message to the dispatcher session (`send_message` to the dispatcher named in the mission brief). The first line is "WP03 operator questions (N)". Number the items, and give each its row `source`, the question, and the 2-3 choices. Record that the questions were sent with `add-history`. Leave the rows' `operator_question` set until they are answered, then fill them in and clear the field.

### Subtask T018 - Dry run and check

- **Steps**:
  1. Copy `packs/` to a scratch directory.
  2. Run `python3 curation/apply_curation.py --root <scratch> --ledger curation/ledger-00-nodes.yaml --ledger curation/ledger-a-foundation.yaml`.
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
- Check coverage against the merge map: every source index the map homes in `foundation` has exactly one row here.
- Check the merge map itself: all 273 source indexes once each; every `merge_reason` quotes both texts; every home is upstream of its members; no new `depends_on` makes a cycle.
- Check that the operator questions were sent, and that any answered ones are applied.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
