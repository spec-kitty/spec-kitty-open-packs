---
work_package_id: WP04
title: Manifest lists every file-backed graph node (#182 residual)
dependencies: []
requirement_refs:
- FR-009
- FR-010
- SC-005
planning_base_branch: feat/194-pack-digests
merge_target_branch: feat/194-pack-digests
branch_strategy: Planning artifacts for this mission were generated on feat/194-pack-digests. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/194-pack-digests unless the human explicitly redirects the landing branch.
subtasks:
- T013
- T014
- T015
- T016
history: []
agent_profile: python-pedro
authoritative_surface: scripts/ci/
create_intent: []
execution_mode: code_change
model: sonnet
owned_files:
- scripts/ci/validate_pack_schemas.py
- tests/ci/test_validate_pack_schemas.py
role: implementer
tags: []
tracker_refs: []
---

# WP04 — Manifest lists every file-backed graph node (#182 residual)

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load the agent profile specified in the frontmatter, and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

Implement with: `spec-kitty agent action implement WP04 --agent claude --mission per-pack-digest-gate-01M75YJ0`

## Objective

In every pack that ships a `pack-manifest.yaml`, every graph node the pack declares must be a
manifest constituent, except nodes of an explicitly exempt kind. Add this beside the existing
file-based #182 guard in `scripts/ci/validate_pack_schemas.py`, with tests.

## Context

- #182 is closed (53df95d added `unlisted_constituents`, the file-based guard). Its residual: a
  node declared in `*.graph.yaml` or `drg/fragment.yaml` with no constituent is not reported.
- Existing code to reuse (read it first):
  - `MANIFEST_CONSTITUENT_SCHEMAS` and its comment (~line 68-76): graph-only kinds (actions,
    anti-patterns) have no file; mission types, step contracts and templates are not listed in
    this repository's manifests.
  - `declared_nodes(pack_dir, contract=None)` (~line 867): `(kind, id)` from `drg/fragment.yaml`
    (plural kinds singularised by `_singular`) and root `*.graph.yaml` (`urn` = `kind:id`).
    Call it **without** `contract` so only graph nodes are returned.
  - `unlisted_constituents` (~line 378) and its call site (~line 824-835) — the message shape
    and `REGENERATE_COMMAND` remedy to mirror.
- Planning-time measurement (research.md): with exempt kinds
  `{action, anti_pattern, template, mission_type, mission_step_contract}` all seven manifest-bearing
  packs (architecture, built-in, foundation, planning-analysis, refactoring, testing, writing)
  report **zero** missing nodes. Manifest `kind` values use the same singular snake_case
  (`agent_profile`, `glossary_pack`, `tactic`, ...).
- Research D4: exemptions are an explicit set, so an unknown new node kind fails closed instead of
  being silently exempt.

### Subtask T013: Exempt set and pure function

**Steps**:
1. Next to `MANIFEST_CONSTITUENT_SCHEMAS`, add
   ```python
   #: Graph-node kinds a manifest does not list (#182 residual, #194). ``action`` and
   #: ``anti_pattern`` are graph-only: no file backs them. Mission types, step contracts and
   #: templates are deliberately not manifest constituents in this repository (see above).
   #: Any other declared node must be a constituent; a new kind fails closed until listed here.
   MANIFEST_EXEMPT_NODE_KINDS = frozenset({"action", "anti_pattern", "template", "mission_type", "mission_step_contract"})
   ```
2. Add `unlisted_nodes(manifest: dict, nodes: set[tuple[str, str]]) -> list[str]`: constituents'
   `(kind, id)` pairs (skip non-dict entries, as `unlisted_constituents` does); return sorted
   `f"{kind}:{id}"` for nodes whose kind is not exempt and that are not listed.

**Validation**: direct unit test in T015.

### Subtask T014: Call it from the pack check

**Steps**:
1. In the block that already reports "incomplete manifest" (only when `manifest is not None`),
   append violations:
   `f"{pack_dir.name}/{MANIFEST_NAME}: incomplete manifest: graph node {node} is not a constituent; add its entry, then run \`{REGENERATE_COMMAND} {pack_dir}\`"`
   for each `unlisted_nodes(manifest, declared_nodes(pack_dir))`.
2. Packs without a manifest are not held to this (same as today; operator decision scopes it to
   manifest-bearing packs).
3. Avoid double reporting where the file guard already names the same artifact: acceptable if both
   fire (different evidence), but keep messages distinct ("graph node …" vs file path).

**Validation**: `scripts/ci/validate-packs.sh` on the real repo stays green (zero new findings).

### Subtask T015: Tests

Add to `tests/ci/test_validate_pack_schemas.py`, using the existing `write_contract`,
`write_pack`, `run_validator` helpers (see `test_a_pack_without_a_manifest_is_not_held_to_one`,
~line 256):
1. **Negative**: a pack with a valid manifest (use the regenerate helper or build one the way
   existing manifest tests do) and `drg/fragment.yaml` declaring `{kind: tactics, id: ghost}` with
   no file and no constituent → output contains
   `incomplete manifest: graph node tactic:ghost is not a constituent`, exit invalid.
2. **Positive control, same fixture**: add a constituent for `tactic:ghost` (and its file), then
   regenerate the manifest hashes the way the regenerate tests (~lines 180-209) do — the
   `manifest_pack` helper (~line 136) writes zero hashes, which would trip
   `stale_manifest_fields`. Assert **exit code `EXIT_OK`**, not merely that the message is absent.
3. **Exempt**: the same fixture declaring `actions`/`templates`/`mission_types`/
   `mission_step_contracts`/`anti_patterns` nodes only → no message.
4. **Root graph shard**: a `tactic.graph.yaml` with `nodes: [{urn: "tactic:ghost"}]` → reported.
5. **Pure function**: `unlisted_nodes({"constituents":[{"kind":"tactic","id":"a"}]}, {("tactic","a"),("tactic","b"),("action","x")}) == ["tactic:b"]`;
   and assert the exempt set equals exactly the five kinds (guards silent widening).

**Validation**: `python3 -m unittest discover -s tests/ci -p 'test_validate_pack_schemas.py' -v` green.

### Subtask T016: Real-repo proof

**Steps** (do not commit the experiment):
1. Run `scripts/ci/validate-packs.sh` — green.
2. Remove one tactic constituent from `packs/testing/pack-manifest.yaml` **and** rerun: both the
   file guard and the new node guard report it (node guard because `drg/fragment.yaml` declares
   it). Revert.
3. Note results in implementation notes.

## Definition of Done

- `MANIFEST_EXEMPT_NODE_KINDS` and `unlisted_nodes` exist, documented, wired into the pack check.
- Real repository: zero new violations (`scripts/ci/validate-packs.sh` green — the planning-time
  zero-findings measurement used a scratch script, not the validator, so this run is the proof).
- The **whole** suite `python3 -m unittest discover -s tests/ci` stays green: existing fixtures
  combine `pack.yaml`, a manifest and graph nodes (~lines 122, 143, 448, 506, 536); fix fixtures,
  not the rule, if they declare nodes without constituents.
- New tests green, each with a same-fixture positive control.
- Subtasks recorded via `spec-kitty agent tasks mark-status`.

## Risks

- Kind spelling mismatch (fragment plural → `_singular`; e.g. `glossary_packs` → `glossary_pack`)
  → the real-repo run proves alignment (0 findings measured at planning).
- `declared_nodes` with a contract also returns file-classified ids → call it without contract.

## Reviewer Guidance

- Confirm the exempt set is explicit and matches the documented rationale.
- Confirm a node of an unknown kind (e.g. `widget:x`) is reported, not ignored.
