# Spec — Docsite & README overhaul (Brain Kitty, Charter terminology)

**Mission type:** documentation · **Iteration mode:** gap_filling · **Audience:** pack consumers, pack authors, org administrators, Spec Kitty maintainers.
Grounding: [research.md](research.md).

## Purpose

Make the open-packs README and docsite describe the repository as it now is: the content home of the **Brain Kitty** line, whose Charter Packs reach the Spec Kitty CLI through the **Charter Offering** (the charter service, `spec-kitty-charter`), in canonical **Charter** vocabulary.

## Functional requirements

- **FR-001** Rewrite `README.md`: Brain Kitty positioning, how packs flow into the CLI via the charter, pack tiers, quick start, links to the docsite; canonical terminology; `spec-kitty` org only.
- **FR-002** Landing page (`docs/index.md`) is the overview: what open-packs is, its place among Build/Brain/Team Kitty, and how packs interact with the CLI core through the charter service. No separate docs-root path.
- **FR-003** Add a **Contracts** section: `pack.yaml`, `org-charter.yaml`, presets, `pack-manifest.yaml`, consumer registration in `.kittify/config.yaml`, the validator CLI, and the charter entry seams (`charter.offering.api`, `charter.activation`).
- **FR-004** Add an **architectural overview** page (components, flow from pack source to Active Charter, vendoring of built-in).
- **FR-005** Add a **Charter artefacts** section describing each artefact kind's file naming and structure, grounded in real files.
- **FR-006** Add an **Organisations** section: multi-tier packs (built-in → org → project), `required_<kind>` enforcement, skill namespaces, and the standard provisionings that ship (built-in `default` / `minimal` presets, the opt-in packs).
- **FR-007** Add a **Glossary** page aligned with core `docs/context/` definitions.
- **FR-008** Restructure the nav (`docs/_meta/sections.yaml`): Packs, Guides, Charter artefacts, Organisations, Contracts, Architecture, Research, Glossary, Changelog last. Remove the stale `docs/toc.yml`.
- **FR-009** Replace governing-sense "doctrine" with Charter vocabulary across live docs, site config and the generator; keep domain-sense uses (doctrine artifact, DRG) and historical records unchanged. Rename the two `*-doctrine-pack` guides.
- **FR-010** Bump `@spec-kitty/doc-toolkit` to the latest release (0.3.0) and apply its breaking-change migration.
- **FR-011** Changelog entry under `[Unreleased]`.

## Non-functional

- **NFR-001** `npm run validate`, `npm run build`, `gen_pack_reference.py --check` and generator tests pass.
- **NFR-002** No hosted Team Kitty surfaces are pointed at. No invented fields: every documented field exists in a real file or the core glossary.

## Out of scope

Pack content changes; new generators for contracts (tracked by #24); the core docsite.
