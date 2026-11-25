---
work_package_id: WP02
title: Curation tool, ledger contract, and the 15 file-less nodes
dependencies: []
requirement_refs:
- FR-009
- FR-010
- NFR-002
- C-004
planning_base_branch: feat/pack-doctor-alignment
merge_target_branch: feat/pack-doctor-alignment
branch_strategy: Planning artifacts for this mission were generated on feat/pack-doctor-alignment. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/pack-doctor-alignment unless the human explicitly redirects the landing branch.
subtasks:
- T009
- T010
- T011
- T012
- T013
phase: Phase 2 - Curation
history:
- at: '2026-11-25T07:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: kitty-specs/pack-doctor-alignment-01M88RH1/curation/
create_intent:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/apply_curation.py
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/test_apply_curation.py
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/README.md
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-00-nodes.yaml
execution_mode: planning_artifact
model: ''
owned_files:
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/apply_curation.py
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/test_apply_curation.py
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/README.md
- kitty-specs/pack-doctor-alignment-01M88RH1/curation/ledger-00-nodes.yaml
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP02 - Curation tool, ledger contract, and the 15 file-less nodes

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `python-pedro`
- **Agent/tool**: `claude`

---

## IMPORTANT: Review Feedback

Check `review_ref` with `spec-kitty agent tasks status --mission pack-doctor-alignment-01M88RH1`, and address every item.

---

## Objectives & Success Criteria

- `curation/apply_curation.py` reads every `curation/ledger-*.yaml` and applies it to a pack tree, deterministically and idempotently:
  1. it writes each `anti_patterns/<id>.anti-pattern.yaml`;
  2. it adds each graph node and `rejects` edge, in the layout the pack already uses;
  3. it deletes the inline `anti_patterns` block from each owner file.
- Its `--check` mode proves the data-model invariants (FR-010, NFR-002).
- `curation/README.md` is the single contract every ledger WP (WP03-WP07) follows. It covers:
  - the row fields;
  - the id rule;
  - the severity rubric, as the operator decided;
  - the bad-example rule;
  - the merge rule;
  - how to raise an `operator_question`.
- `ledger-00-nodes.yaml` holds the 15 file-less nodes (FR-009), each grounded.
- A dry run over a scratch copy of `packs/` clears exactly the 15 `drg_schema_error` violations and introduces no new code (T013).

## Context & Constraints

- **Read first**: `spec.md`, `plan.md` IC-02, `research.md` R4-R6, `data-model.md` (the anti-pattern file, the graph additions, the ledger row), issue #350.
- **The target shape is the charter's own example pack**: `spec-kitty-charter/service/packs/src/testFixtures/resources/example-packs/built-in/` (`anti_patterns/`, `procedure.graph.yaml` nodes and `rejects` edges, the `pack-manifest.yaml` entries). The schema is charter `contracts/packs/schemas/anti-pattern.schema.json`.
- **Two graph layouts here**:
  - `drg/fragment.yaml`, in 17 packs. Its nodes are `{id, kind: <plural>, title, body_path?}` and its edges are `{source, target, relation, reason|when}`. The existing `anti_patterns` nodes in `packs/architecture` and `packs/refactoring` show the anti-pattern spelling.
  - Per-kind `*.graph.yaml`, in `foundation` and `writing`. Their nodes are `{urn, kind, label}`. Anti-pattern nodes go in `anti_pattern.graph.yaml`; create it if missing, mirroring `foundation`'s header. Edges go in the owner kind's file (`procedure.graph.yaml` or `styleguide.graph.yaml`), as the charter example does.
- **The decisions this WP depends on**:
  - `01M88RHFTS2X5HK1ZNP74G3WZ7` (the severity rubric) and `01M88RHJ9HN4N8HDE97SJ6ZBAH` (the bad-example source). If either is unresolved when you reach T011/T012, write the README's rubric section as "pending operator decision" and put an `operator_question` on every row whose severity it governs.
  - The tool and `--check` do not depend on them.
- The tool lives in `kitty-specs/` because it is mission tooling, not a product surface (plan, Structure Decision). Standard library plus PyYAML only.

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`. Lanes come from `lanes.json`.
- `spec-kitty agent action implement WP02 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T009 - `apply_curation.py` (apply)

- **CLI**:
  - `python3 apply_curation.py --root <repo-or-scratch> [--ledger <file> ...]`. The default is every `ledger-*.yaml` beside the script, sorted.
  - `--check` (T010).
  - `--dry-run`, which prints the planned writes.
- **For each row**:
  - **A source `<file>#/anti_patterns/<i>`:**
    - Verify that the source entry still exists and that its title text equals the row's `source_title`. This catches drift.
    - Write the file (unless the row has `merged_into`), with keys in schema order: `schema_version: '1.0'`, `id`, `title`, `description`, `severity`, `bad_example`, then `good_example` when present. Use the block style the repo uses (`yaml.safe_dump(sort_keys=False, allow_unicode=True, width=120)`). Multi-line text uses a literal block.
    - Add a node, unless one for the id already exists in the pack.
    - Add a `rejects` edge from the owner URN (`styleguide:<owner-id>` / `procedure:<owner-id>`, where the owner id is the owner file's `id`) to `anti_pattern:<id>`, unless it already exists.
      - The `reason` is `the <kind> <owner-id> names this anti-pattern`, the charter example's wording.
      - For a merged row, the edge targets the `merged_into` id. Across packs, it is qualified as `<pack>::anti_pattern:<id>`, and the tool refuses unless that pack is in the owner pack's `depends_on`.
  - **A source `<graph doc>#/nodes/<i>` (a file-less node):** write the file only. The node and its edges already exist.
- **Deleting inline blocks** happens after all rows of a file are applied, and only when every index of that block has a row.
  - Remove the top-level `anti_patterns:` key and its block **textually**: from the line `anti_patterns:` at column 0 to the line before the next column-0 key, or EOF. Comments and formatting elsewhere survive.
  - Then re-parse, and assert that the document equals the original minus that key.
- **Idempotent**: a second run writes nothing. Assert this in the tests.
- **Refuse, with a clear message and nothing written**:
  - a row with an open `operator_question`;
  - an id clash between two rows that do not merge;
  - an id longer than 64 characters or not kebab-case;
  - a source that does not resolve;
  - a block index without a row.

### Subtask T010 - `--check`

- **Prove over `--root`**:
  - every `packs/*/anti_patterns/*.anti-pattern.yaml` has exactly one non-merged row;
  - every non-merged row has its file, with field-for-field equal text;
  - every file's node and its `rejects` edges exist;
  - no `styleguides/**` or `procedures/**` file carries `anti_patterns`;
  - no `anti_pattern` node in any graph lacks a file in its pack;
  - every row has a non-empty `severity_grounding` and `bad_example_source`, and neither contains "default";
  - no row has an open `operator_question`.
- **Exit code**: 0 when clean, 1 with one line per fault.
- **Tests** (`test_apply_curation.py`, pytest): use a tiny two-pack fixture built in `tmp_path`, with one layout each. Cover:
  - apply and idempotence;
  - deleting a block keeps neighbouring comments;
  - a merge, both within a pack and across packs;
  - each refusal;
  - each `--check` fault.

### Subtask T011 - `curation/README.md`: the ledger contract

- **Ledger file**: `ledger-<NN>-<name>.yaml` with `batch: <name>` and `entries: [rows]`. Each row has these fields:
  - `source`, `source_title`, `pack`, `owner` (`styleguide:<id>` or `procedure:<id>`; null for a node);
  - `id`, `merged_into`, `merge_reason`;
  - `title`, `description`, `severity`, `severity_grounding`;
  - `bad_example`, `bad_example_source`, `good_example`;
  - `operator_question`.
- **The id rule**:
  - kebab-case of the title;
  - ASCII-fold, drop punctuation, collapse hyphens;
  - ≤64 characters, cut at a word boundary;
  - on a clash within the pack, prefer the owner's distinguishing word, and record it.
- **Text rules**:
  - `title` and `description` are **verbatim** from the source (`name`/`title`, `description`/`content`).
  - Never rewrite or "improve" doctrine text. If a description needs a change for the schema, add an `operator_question`.
  - `good_example` is verbatim, when present.
- **Severity**: state the operator's rubric (decision `01M88RHFTS2X5HK1ZNP74G3WZ7`) exactly. Until it is decided, use the proposal under review:
  - The schema's meaning: `smell`, worth a remark; `severe`, should block review; `breaking`, must block.
  - `severity_grounding` quotes the words of the entry or its host that decide the call. Examples: "totals drift and equality checks fail" means a wrong result, so `breaking`; "sends the runner after stale scope" means defeating the guidance's purpose, so `severe`; "harder to scan" means `smell`.
  - Where the charter's example pack curated the same entry, its severity is cited as precedent.
  - No signal in the text means an `operator_question`, not a guess.
- **Bad example** (decision `01M88RHJ9HN4N8HDE97SJ6ZBAH`; the proposal until it is decided):
  - Use the source `bad_example` verbatim.
  - For a `title`/`content` entry, use the content's concrete-instance sentence, verbatim, and name it in `bad_example_source` as `content sentence <n>`.
  - No concrete instance means an `operator_question`.
- **Merge** (decision `01M88RHDGQSS6R5R5ZCDCH84A2`): the rule as decided. Until then, merge only exact-title duplicates within a pack. The `merge_reason` quotes both texts' shared claim.
- **Operator questions**: one line, answerable with a choice. The WP collects them, and the implementer sends them to the dispatcher in one batch per WP.

### Subtask T012 - `ledger-00-nodes.yaml`: the 15 file-less nodes

- **Sources**:
  - `packs/architecture/drg/fragment.yaml`: big-upfront-design, code-is-the-documentation, single-diagram-architecture, anemic-domain-model, big-ball-of-mud, database-driven-design;
  - `packs/refactoring/drg/fragment.yaml`: big-bang-rewrite, feature-envy, global-data, implicit-concept, misplaced-field, repeated-switches-on-state, unencapsulated-record;
  - `packs/foundation/anti_pattern.graph.yaml`: assert-on-mock-interactions, mock-owned-logic-to-pin-a-call-contract.
- **Each row**:
  - `title`: the node's `title`/`label`.
  - `description`: the practice clause of its `rejects` edge `reason`. For example, Feature Envy gives "a method that uses more of another class's data and behaviour than its own host's".
    - Quote the text, and name the edge in `severity_grounding`.
    - Where a node has several rejecting edges, use the most specific, and list the others.
  - `bad_example`: a concrete instance from the rejecting tactic's or directive's own text (its `when`, examples, or steps), named in `bad_example_source`. Where the tactic gives none, raise an `operator_question`.
- **Severity**: per the rubric. The `reason` texts already say "smell" for the refactoring ones, which is grounding for `smell` unless the text says the outcome is wrong.

### Subtask T013 - Dry run

- **Steps**:
  1. Copy `packs/` to a scratch directory.
  2. Apply ledger 00 there.
  3. Run the pack-doctor jar (built from the pin; see `quickstart.md`), `validate --round-trip --full`, over the scratch packs.
- **Expect**:
  - `drg_schema_error` goes from 15 to 0;
  - no new code appears;
  - the round-trip knock-ons stay unchanged, because the manifests are not restamped yet.
- **Record** both counts in the WP history.

## Risks & Mitigations

- **Textual deletion can eat a neighbouring key.** The re-parse equality assertion catches it.
- **The two layouts.** Test both in T010.

## Review Guidance

- Run the tool's tests, and run `--dry-run` against the real tree.
- Read every ledger-00 row: is each `description` verbatim from its source? Is each grounding a quote?
- Confirm the README rubric matches the operator's decision text exactly, or is marked pending.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
