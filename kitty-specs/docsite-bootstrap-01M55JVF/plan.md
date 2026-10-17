# Implementation Plan: Spec Kitty Open Packs Docsite

**Branch**: `mission/docsite-bootstrap` | **Date**: 2026-10-17 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/docsite-bootstrap-01M55JVF/spec.md`

## Summary

Stand up the `spec-kitty-open-packs` documentation site with **doc-kitty (Astro, latest release)**, reusing the **Brain Kitty** product-line logo from `spec-kitty-charter`. The site surfaces the existing authored `docs/` (guides, architecture, ADRs, research) and adds two new things: a **packs hub** backed by **generated-from-source per-pack reference** pages, and a short **getting-started tutorial**. The content-from-code generator and a **checksum drift gate** enforce the generated-vs-authored boundary. A new **ADR supersedes ADR-1** (MkDocs Material) to record the doc-kitty/Astro decision.

Divio types: **reference** (generated pack pages), **how-to** (use/author/compose/publish/validate guides + hub), **explanation** (vision, design, ADRs), **tutorial** (adopt-your-first-pack).

## Technical Context

**Documentation Framework**: doc-kitty (Astro-based, latest released version) — mirror the `spec-kitty-charter` `site/` stack for shared Brain Kitty branding and a single toolchain across the product line.
**Content languages**: Markdown (authored docs) + YAML (doctrine artifacts, the generator's input). **Generator**: Python (stdlib + light YAML) emitting Markdown; shells out to `spec-kitty charter pack validate --json` for validation status only.
**Output Format**: Static HTML (Astro build) from Markdown sources.
**Hosting Platform**: GitHub Pages (mirror `spec-kitty-charter`'s `docs-site.yml` workflow, including `DK_DIAGRAM_BUILD_RENDER: client` so the build needs no Chromium).
**Theme / branding**: doc-kitty theme with the Brain Kitty logo (`brain-kitty.png`) copied from `spec-kitty-charter/site/src/assets/` + favicon.
**Accessibility**: heading hierarchy, image alt text, clear language (WCAG-aligned); external-link health non-gating.

## Project Structure

### Mission artifacts
```
kitty-specs/docsite-bootstrap-01M55JVF/
├── spec.md      # goals, user stories, requirements
├── plan.md      # this file
└── tasks/       # Phase 2 work packages (/spec-kitty.tasks)
```

### Repository (target state)
```
site/                         # doc-kitty/Astro app (NEW) — mirrors spec-kitty-charter/site
├── src/assets/brain-kitty.png
├── astro/doc-kitty config
└── (consumes docs/ as content)
docs/
├── index.md                  # home (exists; refreshed)
├── packs/
│   ├── index.md              # Packs HUB (NEW, authored: purpose + links)
│   └── <pack>.md             # per-pack REFERENCE (GENERATED, drift-gated)
├── guides/                   # how-to (exists: use/author/compose/publish/validate) + getting-started (NEW)
├── architecture/             # vision, docsite-design, adr/ (exists; ADR-1 superseded)
├── research/ , changelog/    # exist
scripts/
└── docs/gen_pack_reference.py  # content-from-code generator (NEW)
.github/workflows/
└── docs-site.yml             # build + drift gate + Pages deploy (NEW)
```

## Phase 0: Research (settled)

The generator/IA/design research is already captured and is the authority here:
`docs/architecture/docsite-design.md`, `docs/research/docsite-feasibility-and-generator.md`,
`docs/research/docsite-information-architecture.md`. One correction this mission makes: the
generator decision moves from MkDocs Material (ADR-1) to **doc-kitty/Astro** (operator direction),
recorded as a new superseding ADR. The content-from-code design (generated evidence vs authored
explanation, the `pack.yaml` source-of-truth, the checksum/drift gate) carries over unchanged —
only the SSG differs, and the design is explicitly SSG-agnostic (Markdown output).

## Phase 1: Design

### Information architecture / navigation
Reuse `docs/toc.yml` intent, rendered through doc-kitty nav:
Home → **Packs** (hub + generated per-pack reference) → **Guides** (use/author/compose/publish/validate + getting-started) → **Architecture** (vision, docsite design, ADRs) → **Research** → **Changelog**.

### Generated-vs-authored boundary
- **Authored**: hub `docs/packs/index.md` (purpose, when-to-use, links), all guides, explanation, ADRs.
- **Generated** (by `gen_pack_reference.py`): `docs/packs/<pack>.md` — artifact inventory + counts, validation status (`charter pack validate --json`), and a content checksum. Each generated file carries a header marking it generated + its checksum.
- **Drift gate**: CI re-runs the generator and fails if output differs from committed (no hand-edits to generated pages). Packs without `pack.yaml` (e.g. `qa`) degrade gracefully — derive inventory, omit purpose rather than fabricate.

### Branding
Copy `brain-kitty.png` (+ favicon) from `spec-kitty-charter/site/src/assets/`; wire as the doc-kitty theme logo. Keep the two product-line sites visually consistent.

### ADR supersession
New ADR `docs/architecture/adr/2026-10-17-1-doc-kitty-astro-as-docsite-generator.md` (Accepted): doc-kitty/Astro supersedes ADR-1 (MkDocs Material); mark ADR-1 Superseded; reconcile `docsite-design.md`'s "One Python toolchain / MkDocs" wording to note the SSG change while keeping the content-from-code design.

## Phase 2: Work Breakdown (preview — finalized in tasks.md)

1. **WP01 — Docsite scaffold + Brain Kitty branding**: create `site/` (doc-kitty/Astro, latest), copy the logo/favicon, wire nav from the existing docs, build locally clean.
2. **WP02 — Supersede ADR-1**: new doc-kitty/Astro ADR (Accepted), ADR-1 → Superseded, reconcile design-doc wording.
3. **WP03 — Pack-reference generator + packs hub**: `scripts/docs/gen_pack_reference.py` emitting `docs/packs/<pack>.md` for built-in + each `packs/*`; authored hub `docs/packs/index.md`; checksum header per generated page.
4. **WP04 — Guides wiring + getting-started**: surface the existing guides in nav; add a getting-started tutorial; verify documented `spec-kitty` CLI/charter commands against the current CLI.
5. **WP05 — CI: build + drift gate + Pages publish**: `docs-site.yml` builds the site, runs the generator drift check, deploys to GitHub Pages.

## Success Criteria Validation
- **SC-001** findability: hub + nav put any pack reference ≤3 clicks from home.
- **SC-002** accessibility: heading hierarchy + alt text enforced in authored pages.
- **SC-003** reference completeness: generator covers built-in + every `packs/*` (100%).
- **SC-005** build quality: Astro build zero-error; drift gate green.
- **SC-006** publish/branding: deploys to Pages with Brain Kitty branding.

## Charter Check
Aligns with the charter's documentation directives: Common Docs conventions (`DIRECTIVE_042`), generated-evidence vs authored-explanation single-source (`DIRECTIVE_044`), audience-oriented writing (`DIRECTIVE_047`), living-documentation-sync (`DIRECTIVE_037`), and ADR discipline (`DIRECTIVE_003`, supersede-not-edit). Fail-closed gates: pack validation + generated-content drift. Diagramming via `diagram-daisy` where a picture earns its place.

## Risks & Dependencies
**Risks**: generated/authored drift (mitigated by the checksum gate); CLI commands in guides going stale (verify against current CLI in WP04); doc-kitty version churn (pin the latest release).
**Dependencies**: doc-kitty (Astro) toolchain (Node); `spec-kitty charter pack validate` for status; the Brain Kitty asset in `spec-kitty-charter`; GitHub Pages enabled for the repo.
