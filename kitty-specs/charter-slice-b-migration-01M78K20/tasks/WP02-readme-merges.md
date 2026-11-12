---
work_package_id: WP02
title: One README per pack
dependencies:
- WP01
requirement_refs:
- FR-002
- FR-003
- FR-004
- FR-005
planning_base_branch: feat/slice1-readme-retire-org-charter
merge_target_branch: feat/slice1-readme-retire-org-charter
branch_strategy: Planning artifacts for this mission were generated on feat/slice1-readme-retire-org-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/slice1-readme-retire-org-charter unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-charter-slice-b-migration-01M78K20
base_commit: 0666149f809d62f26d1ef36addecb573b191f2a7
created_at: '2026-11-12T19:31:08.272895+00:00'
subtasks:
- T006
- T007
- T008
- T009
- T010
agent: claude
history:
- at: '2026-11-12T19:25:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
owned_files:
- packs/*/README.md
- packs/*/pack.md
- packs/*/PROVENANCE.md
role: implementer
tags: []
tracker_refs:
- '#241'
- '#242'
---
# Work Package Prompt: WP02 – One README per pack (#241)

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load implementer-ivan` before reading anything else.

## Objective

Every pack's only document is its root `README.md`, merged exactly as #241's "Steps for every pack" and
"Per-pack fixes" say.

## Rules (every pack)

1. Keep the README's H1 and description. Drop the `pack.md` preamble (except go and rust: keep its first
   paragraph as the README's opening paragraph).
2. Add `pack.md`'s H2 sections except "Contents" ("Who opts in"/"Who uses it", "Authored and generated files").
   In "Authored and generated files", "This file" means the README.
3. Delete Level, `pack_id` and Depends-on bullets or sentences. Keep the contents, profile and mission bullets.
4. Fold `PROVENANCE.md` as `## Provenance`: drop its H1, demote its headings one level, replace any pointer
   to the file.
5. Markdown model: one H1, ATX only, no closing `#` on H1/H2, no CR/BOM, closed fences.

## Subtasks

- **T006** The nine carved packs: delete README lines 5-7 (the three descriptor bullets); add "Who opts in"/"Who
  uses it"; replace the `## Provenance` pointer with the two-paragraph body.
- **T007** built-in: `git mv pack.md README.md`. foundation, writing: delete the descriptor bullet, add
  "Authored and generated files" as H2, closing pointer line becomes `## Provenance`.
- **T008** cave-kitty (three H2s → H3s; the fenced `# Voice only` lines stay), event-driven, spdd (preamble
  dropped, no provenance), go and rust (keep the first preamble paragraph; four H2s → H3s; the
  `org-charter.yaml` sentence becomes "Registering the pack activates nothing on its own").
  event-driven's `required_directives` advice becomes the governing-preset advice from #242.
- **T009** internal (three H2s → H3s; layout tree drops `org-charter.yaml`; `presets/base.yaml` comment says
  it carries the org's required floor; "Pack skills" says the `base` preset's must-have items put the five
  skills in force, and that the `kitty-` names are core's rendering). qa (three H2s → H3s; "see Provenance
  below"; the two `required_*` mentions become governing-preset advice).
- **T010** Delete all `pack.md` and `PROVENANCE.md` (any case). Run a shape check over every root README.

## Done when
`find packs -maxdepth 2 -iname pack.md -o -maxdepth 2 -iname provenance.md` is empty; the shape check passes on
19 READMEs; every old `PROVENANCE.md` sentence and every kept `pack.md` H2 sentence is in a README.
