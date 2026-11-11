# Implementation Plan: Split built-in into foundation, writing and opt-in bundles

**Branch**: `feat/73-foundation-writing-split` | **Date**: 2026-11-11 | **Spec**: [spec.md](spec.md)
**Input**: [spec.md](spec.md), [membership.json](membership.json), [research/](research/)

## Summary

This mission moves 398 graph nodes and their files out of `packs/built-in/` into `foundation`, `writing`, ten opt-in org bundles (testing, refactoring, architecture, planning-analysis, adversarial-review, pack-authoring, python, javascript, drupal, java), `qa` and `internal`, per [membership.json](membership.json). It is driven by one deterministic, re-runnable migration tool that reads [membership.json](membership.json) and does four things:

1. `git mv`s each artifact's files.
2. Splits the 14 `*.graph.yaml` fragments per owning pack, relocating every upward edge into the higher pack with a qualified source.
3. Rewrites `built-in::` references in the org packs.
4. Strips out-of-closure references from artifact bodies, such as profile `*-references` and step-contract delegation candidates.

Descriptors, manifests, digest, CI staging, the #182 guard and docs are then done by hand or with the existing tools. The charter service check is the arbiter, run locally with Java 25 against the pin.

## Technical Context

**Language/Version**: Python 3.12 (migration tool, CI scripts, unittest); YAML pack data; Java 25 only to run the pinned charter service jar locally
**Primary Dependencies**: PyYAML / ruamel-free plain-text edits (as the existing scripts do); existing `scripts/ci/*`; the charter service jar built from `charter.lock.yaml` commit `fb24052`
**Storage**: Files in git (pack trees under `packs/`)
**Testing**: `scripts/ci/validate-packs.sh`, `scripts/ci/check-built-in.sh`, `scripts/ci/charter_service_check.py` (compose + whole-pack registration of every pack), `scripts/ci/check_vocabulary.py`, `scripts/docs/gen_pack_reference.py --check`, `python3 -m unittest discover` per `tests/*` directory, plus new unit tests for the #182 guard; docs-site build in CI only
**Target Platform**: Charter service at the lock pin (packs are data); GitHub Actions CI
**Project Type**: single (content repository with CI tooling)
**Performance Goals**: Gates finish within their current CI budgets (validate-packs < 30 s locally; the service check < 2 min with a prebuilt jar)
**Constraints**: Charter-only alignment (C-001); tool-minted ids (C-002); `missions/` name kept (C-003); no content rewrites beyond reference surgery and the display name (C-005); manifest hashes only by tool (C-006)
**Scale/Scope**: About 460 files moved; 1091 edges re-homed (110 relocated upward); about 102 qualified references rewritten across 5 org packs; 12 new packs

## Charter Check

| Charter rule | Status | Note |
|---|---|---|
| Docs are a first-class deliverable (DIRECTIVE_042/047, SPEC_KITTY_DOCS_CONVENTIONS) | Pass (planned) | ADR, CHANGELOG, READMEs and generated pages are in scope (FR-014); touched docs pages carry `audience:` and `doc_status`. |
| Decisions recorded as ADRs under `docs/architecture/adr` | Pass (planned) | A new ADR `2026-11-11-1-split-built-in-into-foundation-and-writing.md`. |
| Gates fail-closed: pack validation errors = 0 and built-in parity | Pass (planned) | All gates on the final head; the digest is re-recorded. |
| Identity discipline: pack_id minted once, never edited | Pass | Ids minted by tool before the spec; built-in keeps its id. |
| BDD first-class for pack behaviour | Pass | Acceptance scenarios in the spec are exercised by the service check and the guard's tests. |
| NO_FULL_HEAVY_SUITES_IN_MISSION | Pass | Gates run once per WP boundary and in full on the final head only. |

Post-design re-check: no violations, so no Complexity Tracking entries.

## Project Structure

### Documentation (this mission)

```
kitty-specs/foundation-writing-split-01M75HV3/
├── spec.md
├── plan.md
├── research.md            # decisions (Phase 0)
├── research/              # phase-1 squad reports (inputs)
├── data-model.md          # pack graph, membership rules, edge-relocation rule
├── quickstart.md          # how to run the tool and the gates
├── membership.json        # approved per-node ruling (input to the tool)
└── tools/split_built_in.py  # the migration tool (kept for traceability)
```

### Source Code (repository root)

```
packs/
├── built-in/            # distribution pack: pack.yaml, pack.md, policy.yaml, presets/, pack-manifest.yaml (empty constituents)
├── foundation/          # NEW, built-in level: agent_profiles/, directives/, tactics/, glossary_packs/, missions/{software-dev,plan,research}, templates/, *.graph.yaml, pack-manifest.yaml, policy.yaml
├── writing/             # NEW, built-in level: missions/documentation, styleguides/, toolguides/, assets/, ..., *.graph.yaml, pack-manifest.yaml
├── testing/ refactoring/ architecture/ planning-analysis/ adversarial-review/
├── pack-authoring/ python/ javascript/ drupal/ java/   # NEW org bundles: drg/fragment.yaml + doctrine dirs (org layout, no manifest)
├── qa/ internal/        # receive their items; drg/fragment.yaml updated
└── event-driven/ cave-kitty/ spdd/   # references and depends_on updated
scripts/ci/charter_service_check.py   # stage every built-in-level pack
scripts/ci/validate_pack_schemas.py   # #182 manifest-completeness guard
scripts/ci/built_in_digest.py, check-built-in.sh, packs/built-in.source.yaml
tests/ci/test_validate_pack_schemas.py  # guard tests
docs/architecture/adr/, CHANGELOG.md, README.md, packs/README.md, docs/packs/*.md
```

**Structure Decision**: Built-in-level packs keep the built-in layout (`*.graph.yaml` at the pack root plus a `pack-manifest.yaml`), so the existing manifest and parity tooling applies. The ten bundles follow the org-pack layout (`drg/fragment.yaml`, `org-charter.yaml`, no manifest), like `qa` and `internal`. The tool decides each pack's graph layout from its level.

## Complexity Tracking

None.

## Implementation Concern Map

### IC-01 — Pack skeletons and the aggregator

- **Purpose**: Create the twelve new pack descriptors, pack.md, README and PROVENANCE, and rewrite built-in into a distribution pack, so downstream PRs can depend on the ids early.
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-005, FR-007, FR-015, FR-016
- **Affected surfaces**: `packs/{foundation,writing,built-in,<10 bundles>}/pack.yaml`, `pack.md`, `README.md`, `PROVENANCE.md`, `policy.yaml`, `org-charter.yaml` (bundles)
- **Sequencing/depends-on**: none
- **Risks**: Is `fallback_profile` + policy lock on built-in valid when the profile lives in foundation? Research says the closure resolves it; the service check confirms. Foundation also carries its own policy lock.

### IC-02 — Membership move (the migration tool)

- **Purpose**: Deterministically move every node's files and every non-node file (mission bundles, READMEs, toolguide `.guide.md`, asset sidecars) to its approved pack with `git mv`.
- **Relevant requirements**: FR-004, FR-006, NFR-001, NFR-004
- **Affected surfaces**: `packs/built-in/**` → `packs/{foundation,writing,<10 bundles>,qa,internal}/**`
- **Sequencing/depends-on**: IC-01
- **Risks**: Node→file mapping (the manifest covers 310 of 459 files); files with no node. The tool must fail on any unmapped file rather than guess.

### IC-03 — Graph split and reference surgery

- **Purpose**: Split each graph fragment by node owner and relocate upward edges with qualified sources. Strip out-of-closure body references from moved artifacts. Rewrite every `built-in::` reference in the org packs and set their `depends_on`.
- **Relevant requirements**: FR-008, FR-009, FR-010, NFR-002
- **Affected surfaces**: `*.graph.yaml`, `drg/fragment.yaml`, agent-profile `*-references`, step-contract `delegates_to`, org-pack fragments and profiles
- **Sequencing/depends-on**: IC-02
- **Risks**: The precheck does not catch every out-of-closure edge; the service check is the arbiter. `pack_sibling_conflict` if a node lands twice. Org-pack version bumps (ADR-0065 D2/D9).

### IC-04 — Tooling and the #182 guard

- **Purpose**: Make the gates understand three built-in-level packs, regenerate manifests and the digest, fix hard-coded paths, and land the manifest-completeness guard with tests.
- **Relevant requirements**: FR-011, FR-012, FR-013, NFR-003
- **Affected surfaces**: `scripts/ci/charter_service_check.py`, `validate_pack_schemas.py`, `built_in_digest.py`, `check-built-in.sh`, `check_vocabulary.py`, `packs/built-in.source.yaml`, `tests/ci/*`, `tests/docs/*` (language-profile and ascii tests)
- **Sequencing/depends-on**: IC-02 (paths), IC-03 (for a green service run)
- **Risks**: The guard must ignore graph-only kinds (template, action, anti_pattern, step contract, mission type) or it goes red on day one.

### IC-05 — Documentation and release notes

- **Purpose**: Record the split for readers and consumers.
- **Relevant requirements**: FR-014
- **Affected surfaces**: `docs/architecture/adr/`, `CHANGELOG.md`, `README.md`, `packs/README.md`, `docs/packs/index.md`, `docs/packs/catalog-proposal.md`, generated `docs/packs/<pack>.md` for every new pack and built-in, guides that name built-in paths
- **Sequencing/depends-on**: IC-01…IC-04
- **Risks**: The docs-site build only runs in CI (npm 401 locally).
