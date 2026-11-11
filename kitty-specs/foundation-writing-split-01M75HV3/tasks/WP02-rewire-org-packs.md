---
work_package_id: WP02
title: Rewire the org packs
dependencies:
- WP01
requirement_refs:
- FR-004
- FR-009
- FR-010
- NFR-002
- SC-003
planning_base_branch: feat/73-foundation-writing-split
merge_target_branch: feat/73-foundation-writing-split
branch_strategy: Planning artifacts for this mission were generated on feat/73-foundation-writing-split. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/73-foundation-writing-split unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-foundation-writing-split-01M75HV3
base_commit: 590f37d039d81bd75134cf41b98de9523b77b3b5
created_at: '2026-11-11T16:33:45.855667+00:00'
subtasks:
- T008
- T009
- T010
- T011
history:
- at: '2026-11-11T15:10:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
owned_files:
- packs/qa/**
- packs/internal/**
- packs/event-driven/**
- packs/cave-kitty/**
- packs/spdd/**
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP02 – Rewire the org packs

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

After WP01, `built-in` holds nothing, so every `built-in::` reference in the org packs is refused (`pack_reference_artifact_missing`). Point each reference at the pack that now holds the artifact. Make each org pack depend on exactly the packs it references (operator ruling DM 01M75HVY66EHV8YYBAY4C4QXAG).

## Branch Strategy

- Planning/base branch and final merge target: `feat/73-foundation-writing-split`.
- The workspace is resolved by `spec-kitty agent action implement WP02 --agent claude --mission foundation-writing-split-01M75HV3`.

## Context

`research/3-consumers.md` §3 counts the references: internal 62, qa 27, event-driven 7, spdd 6, cave-kitty 0 checked (prose only). They appear in `drg/fragment.yaml` edges and in qa's agent profiles.

## Subtasks

### T008 Rewrite references

For every `built-in::<urn>`, look up the urn's pack in membership.json and write `<pack-name>::<urn>`. Use the descriptor names: `foundation`, `writing` and the bundle names. When the target now lives in the same pack as the referrer (a qa or internal item), write it bare.

Prose mentions of "built-in" in prompts stay as they are: they mean the distribution.

### T009 depends_on and versions

- Replace the built-in dependency with one entry per referenced pack:
  - pack ids from membership.json `pack_ids`. qa must also depend on testing (FR-004);
  - range `>=1.0,<2` for each.
- cave-kitty binds built-in profiles only in prose. Keep a dependency on `foundation`, for the same reason it had one on built-in.
- Bump each org pack's `pack_version` minor (ADR-0065 D2/D9).

### T010 Integrate received items

- Add WP01's moved qa/internal items to their packs' README/pack.md lists and PROVENANCE where those lists exist.
- Check that their fragment nodes and edges are present and that qualifiers are correct.

### T011 Validate

- Run `scripts/ci/validate-packs.sh`: 0 errors.
- `grep -rn "built-in::" packs` returns nothing.

## Definition of Done

- validate-packs is green for all packs.
- No `built-in::` remains.
- Each org pack's depends_on matches the packs its references name (verify with a script).
