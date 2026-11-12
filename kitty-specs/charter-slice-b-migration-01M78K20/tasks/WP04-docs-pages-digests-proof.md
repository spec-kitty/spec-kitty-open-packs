---
work_package_id: WP04
title: Docs, generated pages, digests and proof
dependencies:
- WP01
- WP02
- WP03
requirement_refs:
- FR-009
- FR-010
- FR-011
- FR-013
planning_base_branch: feat/slice1-readme-retire-org-charter
merge_target_branch: feat/slice1-readme-retire-org-charter
branch_strategy: Planning artifacts for this mission were generated on feat/slice1-readme-retire-org-charter. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/slice1-readme-retire-org-charter unless the human explicitly redirects the landing branch.
base_branch: kitty/mission-charter-slice-b-migration-01M78K20
base_commit: 19dfbeaa3ab3a137d57e75f1c180360fb95d27e6
created_at: '2026-11-12T19:40:22.818171+00:00'
subtasks:
- T015
- T016
- T017
- T018
agent: claude
history:
- at: '2026-11-12T19:25:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: docs/
create_intent: []
execution_mode: code_change
owned_files:
- docs/**
- README.md
- packs/README.md
- CHANGELOG.md
- packs/*.source.yaml
- packs/foundation/glossary_packs/spec-kitty-core.glossary-pack.yaml
- .kittify/config.yaml
- .kittify/charter/charter.md
role: implementer
tags: []
tracker_refs:
- '#241'
- '#242'
---
# Work Package Prompt: WP04 – Docs, generated pages, digests and proof

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load implementer-ivan` before reading anything else.

## Objective

No live doc presents `pack.md`, `PROVENANCE.md`, `org-charter.yaml`, `active_charter`, `required_<kind>`
lists or `skill_namespace` as live; generated pages and digests are current; every gate passes.

## Subtasks

- **T015** Every file listed in #241 item 6 and #242 item 6 (root README 102-104; `docs/packs/index.md`,
  `catalog-proposal.md`; `docs/architecture/docsite-design.md`, `overview.md`; the four guides;
  `docs/contracts/index.md`; `docs/organisations/index.md`; `docs/glossary/index.md` "Org charter";
  `docs/research/docsite-feasibility-and-generator.md`; `docs/artefacts/index.md` 121-123;
  `docs/_meta/sections.yaml`; `.kittify/charter/charter.md`; `.kittify/config.yaml`), plus `packs/README.md`.
  Point org enforcement at the charter's `docs/guides/enforce-org-presets.md`. ADRs and the CHANGELOG history stay.
  Re-grep for anything the issues missed.
- **T016** Glossary "Charter Pack": "An org pack enforces activations through a governing preset: a preset whose
  items carry must_have: true."
- **T017** `python3 scripts/docs/gen_pack_reference.py`; `python3 scripts/ci/pack_digest.py --update`; the
  `built-in.source.yaml` comment (line 16) names the README; CHANGELOG "Changed"/"Removed" entries.
- **T018** Run `check-pack-digests.sh`, `validate_pack_schemas.py`, `check_vocabulary.py`,
  `gen_pack_reference.py --check`, `pytest`, and `charter_service_check.py` at the pin. Record counts.

## Done when
All gates exit 0 and the service check registers 19 of 19 packs.
