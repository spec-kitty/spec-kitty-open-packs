---
work_package_id: WP04
title: doc-kitty frontmatter and neutral common-docs examples
dependencies: []
requirement_refs:
- FR-011
- FR-012
- FR-013
- NFR-004
- NFR-005
- SC-004
planning_base_branch: feat/citation-and-docs-writing
merge_target_branch: feat/citation-and-docs-writing
branch_strategy: Planning artifacts for this mission were generated on feat/citation-and-docs-writing. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/citation-and-docs-writing unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-citation-and-docs-writing-01M7YGMQ
base_commit: bcc1e74aca1bff0721459efd656e1ded14f26689
created_at: '2026-11-21T07:52:01.989054+00:00'
subtasks:
- T012
- T013
- T014
- T015
history:
- at: '2026-11-21T08:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: doctrine-daphne
authoritative_surface: packs/
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- packs/writing/styleguides/common-docs.styleguide.yaml
- packs/writing/directives/042-common-docs.directive.yaml
- packs/writing/tactics/common-docs-write.tactic.yaml
- packs/writing/tactics/common-docs-scaffold.tactic.yaml
- packs/writing/tactics/common-docs-find.tactic.yaml
- packs/writing/procedures/declare-page-audience.procedure.yaml
- packs/internal/procedures/spec-kitty-page-audience.procedure.yaml
role: implementer
tags: []
---
# Work Package Prompt: WP04 – doc-kitty frontmatter and neutral common-docs examples

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load doctrine-daphne` (file: `packs/pack-authoring/agent_profiles/doctrine-daphne.agent.yaml`; read it in full) before reading anything else.

## Branch Strategy

Planning and merge branch: `feat/citation-and-docs-writing`. Execution worktrees are allocated per computed lane from `lanes.json`.

## Objective

Make doc-kitty's frontmatter the consumer default across every common-docs surface, name the path form only as legacy, and neutralise the Spec Kitty examples (spec FR-011 to FR-013; plan decisions 7-8; research R1-R2).

## Subtasks

### T012 Styleguide shape

`common-docs.styleguide.yaml`: principles "Cross-references use related" and "Audience is named in an audience" (both the short principle and the long same-named pattern) teach: `related` lists page slugs (the page path under the docs root without `.md`, or `{ref, note}`), and doc-kitty fails the build on a slug that does not resolve; links outside the docs tree go under `external_references` as `{url, title, note}` or `{type, id}`; `audience` is a list of `{profile, guidance_text}` where `profile` names a persona page (doc-kitty resolves it under `context/audience/`) and `guidance_text` says what that reader gets from the page; a project with no persona pages still names the profile in plain words and records the gap. Mention the path form once as legacy ("a project whose own validator still reads repo-relative paths keeps them until it migrates"). Rewrite patterns `related cross-reference` and `audience-resolvable` and their examples; rewrite tooling rows `related-resolvable-paths` (rename key if useful, e.g. `related-resolvable-slugs`) and `audience-resolvable`, and the `quality_test`.

### T013 Neutral examples

ADR principle and pattern: "filed under `adr/`, or under `adr/<era>/` if the project versions its ADRs"; no `adr/1.x`..`adr/4.x`. The anti-pattern example `docs/adr/<era>/...` becomes `docs/adr/...`. Replace "Charter Activation" with a neutral page (e.g. "Payment Retries"); the `citation_refs` comment becomes "rarely populated, so effectively dead"; the "565-row" example becomes "a hand-maintained page-inventory.yaml". Tooling row `adr-era-layout` keeps meaning but says the era subdirectory is optional.

### T014 DIRECTIVE_042 and the three tactics

`042-common-docs.directive.yaml`: integrity rules and validation criteria on `related:` and `audience:` follow T012 (slugs; `{profile, guidance_text}`; legacy path form named once). `common-docs-write.tactic.yaml`: step "Express cross-references as related: resolvable paths" becomes slugs plus `external_references`, examples neutral; failure modes follow. `common-docs-scaffold.tactic.yaml`: frontmatter step and examples (`related: []` fine), ADR steps with optional era and neutral examples. `common-docs-find.tactic.yaml`: check only; edit if it implies paths.

### T015 Procedures, then gates

`declare-page-audience.procedure.yaml`: the field holds `{profile, guidance_text}` entries pointing at persona pages; drop "linked by repo-relative path". Internal `spec-kitty-page-audience.procedure.yaml`: exit condition and step say `audience:` entries are `{profile, guidance_text}` whose profile names a persona page in the repository's persona location. Run `bash scripts/ci/validate-packs.sh`, `python3 scripts/ci/check_vocabulary.py`, and the two greps in quickstart.md.

## Definition of Done

No writing or internal surface recommends the path form; NFR-004 and NFR-005 greps clean; gates pass.

## Reviewer guidance

Read the styleguide, directive and tactics together: one shape, same words.
