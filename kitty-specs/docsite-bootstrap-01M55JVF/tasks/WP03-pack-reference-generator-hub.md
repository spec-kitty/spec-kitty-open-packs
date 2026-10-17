---
work_package_id: "WP03"
title: "Pack-reference generator + packs hub"
dependencies:
  - "WP01"
planning_base_branch: "mission/docsite-bootstrap"
merge_target_branch: "mission/docsite-bootstrap"
branch_strategy: "Planning artifacts were generated on mission/docsite-bootstrap; completed changes must merge back into mission/docsite-bootstrap."
subtasks:
  - "T008"
  - "T009"
  - "T010"
  - "T011"
phase: "Phase 2 - Generated content"
assignee: ""
agent: ""
shell_pid: ""
history:
  - timestamp: "2026-10-17T18:45:00Z"
    agent: "system"
    action: "Prompt authored for docsite-bootstrap mission"
---

# Work Package Prompt: WP03 – Pack-reference generator + packs hub

## Objective
Generate per-pack reference pages from source and author the packs hub, realizing the content-from-code / generated-vs-authored boundary from `docs/architecture/docsite-design.md`.

## Context
- Packs: `built-in` + `packs/{cave-kitty,event-driven,qa,internal}`. Each is a directory of artifact-kind subdirs (directives/tactics/styleguides/toolguides/paradigms/procedures/agent_profiles/assets/glossary_packs/drg), optional `pack.yaml` (name/purpose/depends_on/pack_version) and `org-charter.yaml`.
- `packs/qa` has no `pack.yaml` by design → degrade gracefully.
- Validation status comes from `spec-kitty charter pack validate <dir> --json` (ok/errors/advisories).

## Tasks
- **T008** Write `scripts/docs/gen_pack_reference.py` (stdlib + light YAML): for each pack, emit `docs/packs/<pack>.md` with: a header marking it GENERATED (+ a content checksum over sorted inputs), the pack's purpose (from `pack.yaml` if present), an artifact inventory + per-kind counts, and the validation result. Deterministic output (stable ordering) so the drift gate is meaningful.
- **T009** Packs without `pack.yaml`: derive inventory/counts; omit purpose (never fabricate); still emit a valid page.
- **T010** Author `docs/packs/index.md` — the HUB (authored): what packs are, when to use them, and a table linking each pack to its generated reference. Reconcile with `docs/packs/catalog-proposal.md` (fold its durable content into the hub or link it as the forward-looking catalog).
- **T011** Run the generator; commit the generated `docs/packs/<pack>.md`; confirm they render in the site nav under Packs.

## Acceptance
- `docs/packs/<pack>.md` exists for built-in + every `packs/*` (100% coverage), each marked generated with a checksum.
- Re-running the generator produces no diff (deterministic).
- The hub lists every pack with purpose + link; qa (no pack.yaml) renders without a fabricated purpose.

## Notes
- Authored vs generated: the hub is authored; the per-pack pages are generated and MUST NOT be hand-edited (WP05 adds the CI drift gate).
- Test economy (DIRECTIVE_041): one focused test on the generator's determinism/checksum is worth keeping if it guards real regression; skip redundant tests. Prefer a realistic fixture over a trivial one.
