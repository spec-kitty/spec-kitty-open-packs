---
work_package_id: "WP02"
title: "Supersede ADR-1 (MkDocs) with the doc-kitty/Astro decision"
dependencies: []
planning_base_branch: "mission/docsite-bootstrap"
merge_target_branch: "mission/docsite-bootstrap"
branch_strategy: "Planning artifacts were generated on mission/docsite-bootstrap; completed changes must merge back into mission/docsite-bootstrap."
subtasks:
  - "T005"
  - "T006"
  - "T007"
phase: "Phase 1 - Foundation"
assignee: ""
agent: ""
shell_pid: ""
history:
  - timestamp: "2026-10-17T18:45:00Z"
    agent: "system"
    action: "Prompt authored for docsite-bootstrap mission"
---

# Work Package Prompt: WP02 – Supersede ADR-1 (MkDocs → doc-kitty/Astro)

## Objective
Record the operator decision to build the docsite with doc-kitty/Astro, superseding ADR-1 (MkDocs Material), and reconcile the design docs — without discarding the content-from-code design.

## Context
- `docs/architecture/adr/2026-07-18-1-mkdocs-material-as-docsite-generator.md` (ADR-1) chose MkDocs Material. The operator superseded that in favour of doc-kitty/Astro (for cross-product-line consistency with `spec-kitty-charter`'s site and shared Brain Kitty branding).
- ADRs are superseded, never silently edited (charter DIRECTIVE_003).
- Check the day's highest ADR index for the correct `-N-` suffix on main before naming the new file.

## Tasks
- **T005** Add `docs/architecture/adr/2026-10-17-1-doc-kitty-astro-as-docsite-generator.md` (status **Accepted**): context (cross-repo consistency + shared toolchain/branding), decision (doc-kitty/Astro), consequences, and an explicit "Supersedes ADR-1" link. Keep the content-from-code design intact (SSG choice is decoupled from the generator per the feasibility research).
- **T006** Mark ADR-1 **Superseded** (status line + a pointer to the new ADR); reconcile `docs/architecture/docsite-design.md`'s "One Python toolchain / MkDocs Material" wording to name doc-kitty/Astro as the SSG while preserving the generated-vs-authored / checksum design.
- **T007** Regenerate the ADR/docs index or retrieval inventory if the repo generates one; keep the docs-freshness/terminology gates green.

## Acceptance
- New ADR present, Accepted, superseding ADR-1; ADR-1 marked Superseded.
- `docsite-design.md` no longer claims MkDocs as the chosen SSG; the content-from-code design is unchanged.
- Docs gates (freshness/terminology/links) green.

## Notes
- Prose only; no site code here. Follow the repo's ADR frontmatter + description-length conventions.
