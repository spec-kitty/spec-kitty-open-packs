---
work_package_id: WP04
title: Catalog, docs and changelog
dependencies:
- WP03
requirement_refs:
- FR-011
- FR-012
- C-005
planning_base_branch: feat/rust-go-packs
merge_target_branch: feat/rust-go-packs
branch_strategy: Planning artifacts for this mission were generated on feat/rust-go-packs. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/rust-go-packs unless the human explicitly redirects the landing branch.
subtasks:
- T016
- T017
- T018
- T019
history:
- at: '2026-11-11T15:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: docs/packs/
create_intent:
- docs/packs/rust.md
- docs/packs/go.md
execution_mode: code_change
owned_files:
- README.md
- packs/README.md
- docs/packs/index.md
- docs/packs/catalog-proposal.md
- docs/packs/rust.md
- docs/packs/go.md
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP04 – Catalog, docs and changelog

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill:
`implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Make both packs discoverable (FR-011, FR-012). Keep each shared-file change to added rows and
lines only (C-005), because concurrent work (#73) edits the same files.

## Branch Strategy

Planning/base and merge target `feat/rust-go-packs`. Implement with
`spec-kitty agent action implement WP04 --agent claude --mission rust-go-stack-packs-01M75FYM`.

## Subtasks

### T016 — Tables

- `README.md`, the "The packs" table: add `rust` and `go` rows (org, opt-in). The Status table
  lists the existing packs in prose; add the two names there.
- `packs/README.md`: its first paragraph enumerates the shipped packs. Add the two links and fix the
  count.

### T017 — Catalog proposal

`docs/packs/catalog-proposal.md`:

- add rows 18 `rust` and 19 `go` to the Base packs table, with `depends_on` `foundation`;
- add `### 18. rust` and `### 19. go` sections marked **Materialized**, as the `event-driven`
  section does.

Do not renumber the existing rows.

### T018 — CHANGELOG

`docs/changelog/CHANGELOG.md` (the root `CHANGELOG.md` is a symlink to it; check this with `ls -l`):
under `## [Unreleased]`, add to `### Added` (create the heading in Keep-a-Changelog order if it is
missing) one entry per pack, citing #191 / #192 and noting opt-in, MIT, and not aggregated by
`built-in`.

### T019 — Hub, generated pages, docs build

- `docs/packs/index.md`: add `packs/rust` and `packs/go` to `related:`. Add them to any hand-authored
  pack list in the body, and bump the `updated:` date.
- Run `python3 scripts/docs/gen_pack_reference.py` (with `CHARTER_CONTRACT_DIR`). It writes
  `docs/packs/rust.md` and `docs/packs/go.md`. Never hand-edit them. Then run `--check` to confirm.
- Check whether `docs/_meta/sections.yaml` needs per-page entries (it probably lists sections only).
- Build the docsite: `cd site && npm ci && npm run build`. If network or tooling blocks this, record
  the exact failure.

## Definition of Done

- [ ] `gen_pack_reference.py --check` exits 0.
- [ ] The docs build is green (or the failure is reported with the reason).
- [ ] `git diff origin/main -- README.md packs/README.md docs/packs/catalog-proposal.md docs/changelog/CHANGELOG.md`
      shows only added lines, plus the minimal count and prose fixes.
