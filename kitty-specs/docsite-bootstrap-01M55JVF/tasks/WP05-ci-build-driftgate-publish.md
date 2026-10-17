---
work_package_id: "WP05"
title: "CI: build + generated-content drift gate + Pages publish"
dependencies:
  - "WP01"
  - "WP03"
planning_base_branch: "mission/docsite-bootstrap"
merge_target_branch: "mission/docsite-bootstrap"
branch_strategy: "Planning artifacts were generated on mission/docsite-bootstrap; completed changes must merge back into mission/docsite-bootstrap."
subtasks:
  - "T015"
  - "T016"
  - "T017"
phase: "Phase 4 - CI & publish"
assignee: ""
agent: ""
shell_pid: ""
history:
  - timestamp: "2026-10-17T18:45:00Z"
    agent: "system"
    action: "Prompt authored for docsite-bootstrap mission"
---

# Work Package Prompt: WP05 – CI: build + drift gate + Pages publish

## Objective
Add CI that builds the doc-kitty/Astro site, enforces the generated-vs-authored boundary with a drift gate, and publishes to GitHub Pages.

## Context
- Reference: `spec-kitty-charter`'s `.github/workflows/docs-site.yml` (build + Pages deploy; uses `DK_DIAGRAM_BUILD_RENDER: client`). Mirror it.
- The existing `validate-packs.yml` stays as-is; this is a new workflow.
- Generator: `scripts/docs/gen_pack_reference.py` (WP03) is deterministic, enabling a drift check.

## Tasks
- **T015** Add `.github/workflows/docs-site.yml`: install the site toolchain, build `site/` (env `DK_DIAGRAM_BUILD_RENDER: client`), run the generator drift check (re-run `gen_pack_reference.py`, `git diff --exit-code docs/packs/` → fail on drift), and deploy to GitHub Pages on `main` (skip deploy on PRs, like charter).
- **T016** Verify the drift gate: a hand-edit to a generated `docs/packs/<pack>.md` makes the job RED; a clean tree is green.
- **T017** Verify the site deploys and renders Brain Kitty branding (or, if Pages is not yet enabled for the repo, document the one-time enable step in the PR and leave the deploy job ready).

## Acceptance
- `docs-site.yml` builds the site clean and runs the drift gate.
- Drift gate proven to fail on a hand-edited generated page and pass on a clean tree.
- Pages deploy configured (and succeeds, or the enable step is documented).

## Notes
- This is a MAIN-branch-only deploy class of workflow — the deploy job runs on `main`, not PR heads; confirm the drift/build steps run on PRs so the gate protects the mission PR.
- Test economy (DIRECTIVE_041): the drift gate IS the test; no extra tests for the sake of it.
