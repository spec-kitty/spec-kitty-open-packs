---
work_package_id: "WP01"
title: "Docsite scaffold + Brain Kitty branding"
dependencies: []
planning_base_branch: "mission/docsite-bootstrap"
merge_target_branch: "mission/docsite-bootstrap"
branch_strategy: "Planning artifacts were generated on mission/docsite-bootstrap; completed changes must merge back into mission/docsite-bootstrap."
subtasks:
  - "T001"
  - "T002"
  - "T003"
  - "T004"
phase: "Phase 1 - Foundation"
assignee: ""
agent: ""
shell_pid: ""
history:
  - timestamp: "2026-10-17T18:45:00Z"
    agent: "system"
    action: "Prompt authored for docsite-bootstrap mission"
---

# Work Package Prompt: WP01 – Docsite scaffold + Brain Kitty branding

## Objective
Stand up a doc-kitty (Astro, latest released version) site for `spec-kitty-open-packs`, mirroring the `spec-kitty-charter/site` stack, branded with the Brain Kitty logo, rendering the existing `docs/` content.

## Context
- Reference implementation: the sibling repo `spec-kitty-charter` has a working doc-kitty/Astro site under `site/` (examine its `package.json`, Astro/doc-kitty config, theme wiring, and `site/src/assets/brain-kitty.png`). Mirror it; do not reinvent.
- Existing content to render: `docs/` (index, guides, architecture, research, changelog) and `docs/toc.yml` nav.

## Tasks
- **T001** Create `site/` as a doc-kitty/Astro app pinned to the latest released doc-kitty version, matching charter's structure/config.
- **T002** Copy `brain-kitty.png` (+ favicon) from `spec-kitty-charter/site/src/assets/` into this repo's `site/src/assets/`; wire as the theme logo/favicon.
- **T003** Wire nav from `docs/toc.yml`: Home → Packs → Guides → Architecture → Research → Changelog.
- **T004** Build locally; fix errors; confirm existing authored pages render.

## Acceptance
- `site/` builds with zero errors; the home page and existing authored pages render.
- The Brain Kitty logo + favicon appear.
- Nav covers all existing sections.

## Notes
- Mirror charter's build env, including `DK_DIAGRAM_BUILD_RENDER: client` (no Chromium needed) — but the CI workflow itself is WP05.
- Do not author the packs hub or generated pages here (WP03). This WP is scaffold + branding + nav only.
- Test economy (DIRECTIVE_041): no tests for the sake of tests; a successful build is the guard here.
