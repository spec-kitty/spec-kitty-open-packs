# Tasks: Spec Kitty Open Packs Docsite

**Mission**: docsite-bootstrap-01M55JVF · **Branch**: `mission/docsite-bootstrap`
**Spec**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md)

Work packages execute the plan's Phase 2 breakdown. Dependencies are declared with
`Depends on:` lines and finalized into WP frontmatter via `finalize-tasks`.

## Phase 1 — Foundation

### WP01 — Docsite scaffold + Brain Kitty branding
Depends on: none
- T001 Create `site/` as a doc-kitty (Astro, latest release) app, mirroring `spec-kitty-charter/site` structure and config.
- T002 Copy the Brain Kitty logo + favicon from `spec-kitty-charter/site/src/assets/` and wire them as the theme logo/favicon.
- T003 Wire navigation from the existing `docs/` (Home, Packs, Guides, Architecture, Research, Changelog) per `docs/toc.yml`.
- T004 Build the site locally; resolve errors; confirm the existing authored pages render.

### WP02 — Supersede ADR-1 (MkDocs → doc-kitty/Astro)
Depends on: none
- T005 Add `docs/architecture/adr/2026-10-17-1-doc-kitty-astro-as-docsite-generator.md` (status Accepted) recording the decision and superseding ADR-1.
- T006 Mark ADR-1 `Superseded`; reconcile `docs/architecture/docsite-design.md` wording (SSG = doc-kitty/Astro; the content-from-code design is unchanged).
- T007 Refresh the ADR index / retrieval inventory if the repo generates one.

## Phase 2 — Generated content

### WP03 — Pack-reference generator + packs hub
Depends on: WP01
- T008 Write `scripts/docs/gen_pack_reference.py`: for `built-in` + each `packs/*`, emit `docs/packs/<pack>.md` with artifact inventory + counts, validation status (`spec-kitty charter pack validate --json`), and a content checksum header marking the page generated.
- T009 Handle packs without `pack.yaml` gracefully (derive inventory; omit purpose, do not fabricate).
- T010 Author the hub `docs/packs/index.md` (authored: purpose, when-to-use, links to each pack's generated reference). Replace/retire the `catalog-proposal` framing as appropriate.
- T011 Run the generator; commit generated pages; confirm they render in the site.

## Phase 3 — Guides & tutorial

### WP04 — Guides wiring + getting-started tutorial
Depends on: WP01
- T012 Surface the existing guides (use/author/compose/publish/validate) in the site nav under Guides.
- T013 Add a getting-started tutorial ("adopt your first pack") using the current `spec-kitty` CLI + charter commands.
- T014 Verify every documented `spec-kitty`/charter command against the current CLI; fix any drift.

## Phase 4 — CI & publish

### WP05 — CI: build + drift gate + Pages publish
Depends on: WP01, WP03
- T015 Add `.github/workflows/docs-site.yml` (mirror `spec-kitty-charter`'s): build the site (`DK_DIAGRAM_BUILD_RENDER: client`), run the generator drift check (re-run generator, fail on diff), deploy to GitHub Pages.
- T016 Confirm the drift gate fails on a hand-edited generated page and passes on a clean tree.
- T017 Confirm the site deploys and renders the Brain Kitty branding.
