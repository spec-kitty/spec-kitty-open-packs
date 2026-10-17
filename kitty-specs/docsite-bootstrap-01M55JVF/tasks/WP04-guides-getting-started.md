---
work_package_id: "WP04"
title: "Guides wiring + getting-started tutorial"
dependencies:
  - "WP01"
planning_base_branch: "mission/docsite-bootstrap"
merge_target_branch: "mission/docsite-bootstrap"
branch_strategy: "Planning artifacts were generated on mission/docsite-bootstrap; completed changes must merge back into mission/docsite-bootstrap."
subtasks:
  - "T012"
  - "T013"
  - "T014"
phase: "Phase 3 - Guides & tutorial"
assignee: ""
agent: ""
shell_pid: ""
history:
  - timestamp: "2026-10-17T18:45:00Z"
    agent: "system"
    action: "Prompt authored for docsite-bootstrap mission"
---

# Work Package Prompt: WP04 – Guides wiring + getting-started tutorial

## Objective
Surface the existing pack guides in the site and add a short getting-started tutorial, all tied to the current `spec-kitty` CLI + charter surface.

## Context
- Existing how-to guides: `docs/guides/{use,author,compose,publish,validate}-a-doctrine-pack.md`.
- These explain how packs work and are used with the CLI/charter — the mission's "how packs work with the CLI and charter" requirement.
- The CLI is `spec-kitty` 4.x (charter pack fetch/activate, doctor charter-packs, etc.).

## Tasks
- **T012** Ensure the existing guides appear in the site nav under **Guides**; add a one-paragraph Guides landing/index if missing.
- **T013** Add a **getting-started tutorial** (`docs/guides/getting-started.md` or `tutorials/`): adopt-your-first-pack end to end — fetch a pack, activate it through the charter, verify it is in force — using current commands. Keep it <15-minute, no-prior-knowledge.
- **T014** Verify EVERY documented `spec-kitty`/charter command in the guides against the current CLI (run `--help` / dry commands); fix any drift (renamed flags, removed subcommands). Living-documentation-sync (DIRECTIVE_037).

## Acceptance
- Guides are reachable in the site nav; a getting-started tutorial exists and is followable against the current CLI.
- No documented command is stale vs the current `spec-kitty` surface.

## Notes
- Audience-oriented writing (DIRECTIVE_047): pack USERS for use/compose/getting-started; pack AUTHORS for author/validate/publish.
- Prose + nav wiring only; no generated pages (WP03) or CI (WP05).
