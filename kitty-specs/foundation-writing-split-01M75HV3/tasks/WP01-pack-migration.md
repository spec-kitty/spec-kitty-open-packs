---
work_package_id: WP01
title: Pack migration
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-005
- FR-006
- FR-007
- FR-008
- FR-009
- FR-015
- NFR-001
- NFR-004
- C-002
- C-003
- C-005
- C-006
- SC-004
- FR-016
planning_base_branch: feat/73-foundation-writing-split
merge_target_branch: feat/73-foundation-writing-split
branch_strategy: Planning artifacts for this mission were generated on feat/73-foundation-writing-split. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/73-foundation-writing-split unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-foundation-writing-split-01M75HV3
base_commit: e0c56da4ca5f3bab2a10eeee194f45648eb868a1
created_at: '2026-11-11T15:05:25.854071+00:00'
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
- T007
history:
- at: '2026-11-11T15:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent:
- packs/foundation/pack.yaml
- packs/writing/pack.yaml
- packs/testing/pack.yaml
- packs/refactoring/pack.yaml
- packs/architecture/pack.yaml
- packs/planning-analysis/pack.yaml
- packs/adversarial-review/pack.yaml
- packs/pack-authoring/pack.yaml
- packs/python/pack.yaml
- packs/javascript/pack.yaml
- packs/drupal/pack.yaml
- packs/java/pack.yaml
execution_mode: code_change
owned_files:
- packs/built-in/**
- packs/foundation/**
- packs/writing/**
- packs/testing/**
- packs/refactoring/**
- packs/architecture/**
- packs/planning-analysis/**
- packs/adversarial-review/**
- packs/pack-authoring/**
- packs/python/**
- packs/javascript/**
- packs/drupal/**
- packs/java/**
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP01 – Pack migration

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Turn `packs/built-in` into a distribution pack, and create `foundation`, `writing` and the ten opt-in bundles, holding exactly the nodes [membership.json](../membership.json) assigns them. A deterministic tool does the moves, so the result is reproducible and reviewable.

## Branch Strategy

- Planning/base branch: `feat/73-foundation-writing-split`. Final merge target: `feat/73-foundation-writing-split`, which reaches `main` by a draft pull request after the mission.
- The execution workspace comes from `lanes.json` via `spec-kitty agent action implement WP01 --agent claude --mission foundation-writing-split-01M75HV3`. Trust the path it prints.

## Context

Read first: `spec.md`, `plan.md`, `research.md` (D1–D10) and `data-model.md`. `research/1-inventory.md` lists every node's inbound referrers. Its group rulings are superseded: membership.json is the authority.

## Subtasks

### T001 Descriptors and pack docs

Pack ids were minted by tool on 2026-11-11 and are recorded in the spec. Never re-mint them.

| Pack | pack_id | level | depends_on | version |
|---|---|---|---|---|
| foundation | 01M75HSYR9S9KPA372PHGT0EX3 | built-in | — | 1.0.0 |
| writing | 01M75HSYS69RYRFPB4WCC5AC9D | built-in | foundation `==1.0.0` | 1.0.0 |
| each of the 10 bundles | `pack_ids` in membership.json | org | `depends_on` in membership.json, each `>=1.0,<2` | 1.0.0 |

- Follow the comment style of `packs/built-in/pack.yaml` (built-in level) and `packs/internal/pack.yaml` (org: `active_charter`, `pack_drg`).
- foundation also declares `fallback_profile: generic-agent` and `mutability_policy: policy.yaml` (locking generic-agent). Check whether the descriptor schema allows these on a non-built-in-named pack; drop them if the schema refuses.
- pack.md: a Purpose section (the docs generator reads it). For each bundle, say who opts in and what it builds on.
- README.md per pack.
- PROVENANCE.md where moved content had upstream attribution: copy the relevant lines from `packs/built-in` docs, or note "moved from packs/built-in in #73".
- org-charter.yaml for each bundle: copy internal's shape.
- foundation also gets `fallback_profile: generic-agent` and a `policy.yaml` lock if the schema allows them (FR-016).

### T002 Migration tool

Write `kitty-specs/foundation-writing-split-01M75HV3/tools/split_built_in.py`. This is an out-of-map edit; rationale: traceability of a one-off mechanical migration.
- **Node → files**: the manifest `path` for that `kind`/`id`, plus sidecars sharing the stem (`*.guide.md` for toolguides, `.asset.yaml` sidecars, config files).
- **Mission bundles**: the whole `missions/<type>/` tree goes to the mission type's pack. Step contracts live under `missions/built_in_step_contracts/` or similar; map each by the mission prefix of its id.
- **Templates**: graph `template:` nodes map to `templates/**` files by stem. Graph-only template nodes with no file just move as nodes.
- **Non-node files**: READMEs per directory (copy to every receiving pack, adapted), `assets/audiences/*` with sidecars, `templates/writing/meeting-*.md` → writing, `styleguides/writing/README.md` → writing.
- `skills/.gitkeep` is dropped.
- **Refuse to run** when any file under `packs/built-in` is neither mapped nor in the keep-list (pack.yaml, pack.md, policy.yaml, presets/*, pack-manifest.yaml). Print the list.

### T003 Moves

- Run the tool. It uses `git mv` so `git log --follow` keeps history (NFR-004).
- Items for `qa` and `internal` move into those packs' kind directories. This is an out-of-map edit; rationale: one atomic move. WP02 integrates them.

### T004 Graph split

- **Built-in-level packs** keep root `<kind>.graph.yaml` files. **Org packs** use `drg/fragment.yaml` (append to qa/internal; create for each bundle).
- Node entries go to their owner pack.
- For each edge (D4): home it in the source's pack when the target is in that pack's closure. Otherwise home it in the target's pack, with the source written `<pack-name>::<urn>`.
- Write any endpoint not owned by the home pack as `<pack-name>::<urn>`, using the descriptor `name`. For qa that is `quality-assurance`, for internal `spec-kitty-internal`.
- Closures:
  - foundation = {foundation}
  - writing = {writing, foundation}
  - each bundle: itself plus its transitive depends_on (membership.json)
  - qa and internal: whatever WP02 declares (compute from their references).
- Keep `when`/`reason` text unchanged.

### T005 Body references

- Profiles: drop `directive-references`, `tactic-references` and similar entries whose target is outside the pack's closure. Exactly four cases (FR-009): analyst-annie → DIRECTIVE_047 (writing), diagram-daisy → USE_C4_MODEL_TECHNIQUES (architecture), and the operating procedures of implementer-ivan (test-first-bug-fixing, testing) and reviewer-renata (adversarial-squad-deployment, adversarial-review); each edge is relocated. Keep collaboration role names; they are not references.
- Step contracts: drop `delegates_to` candidates outside the closure.
- Run `validate-packs.sh`. `profile_reference_violations` lists the rest. Fix only what it and the service report.

### T006 built-in as distribution pack

- `pack_version: 2.0.0`; `depends_on` foundation `==1.0.0` and writing `==1.0.0`.
- Keep `fallback_profile: generic-agent`, `policy.yaml` and the `default` and `minimal` presets.
- Remove every artifact directory.
- Set generic-agent's `name:` to `Generic Giannis` and its graph label to match. The id does not change.

### T007 Manifests

- Write member lists for built-in (empty constituents), foundation and writing.
- Restamp with `python3 scripts/ci/validate_pack_schemas.py --regenerate-manifest <pack>`.
- Staging gets no manifest (org layout).
- Run `scripts/ci/validate-packs.sh` with `CHARTER_CONTRACT_DIR` set. Errors for the new packs must be 0. Errors in org packs are WP02's.

## Definition of Done

- Node counts per pack match membership.json: those in SC-004 (foundation 178, writing 68, testing 24, refactoring 35, architecture 35, planning-analysis 16, adversarial-review 5, pack-authoring 7, python 5, javascript 13, drupal 4, java 4); qa +1; internal +4; built-in 0.
- No file is left in `packs/built-in` beyond the keep-list.
- validate-packs reports 0 errors for built-in, foundation, writing and every bundle.

## Reviewer guidance

- Spot-check five moved files with `git log --follow`.
- Diff the node sets against membership.json with a script, not by eye.
- Confirm no `built-in::` appears in the new packs.
