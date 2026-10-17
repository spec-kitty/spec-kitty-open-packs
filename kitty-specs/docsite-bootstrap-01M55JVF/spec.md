# Mission Specification: Documentation Project - Spec Kitty Open Packs Docsite

**Mission Branch**: `mission/docsite-bootstrap`
**Created**: 2026-10-17
**Status**: Draft
**Mission**: documentation
**Input**: Stand up the `spec-kitty-open-packs` documentation site with doc-kitty (Astro), reusing the Brain Kitty product-line logo from `spec-kitty-charter`; add a packs overview/hub and guides on how packs work with the spec-kitty CLI and charter; supersede ADR-1 (MkDocs) with a doc-kitty/Astro ADR.

## Documentation Scope

**Iteration Mode**: initial — there is no published site yet; it builds on the existing authored `docs/` tree (guides, architecture, ADRs, research, pack catalog proposal).
**Target Audience**: pack **users** (developers adopting packs into a project), pack **authors** (contributors writing/validating/publishing packs), and **operators** (wiring packs through the spec-kitty CLI + charter).
**Selected Divio Types**: reference (generated per-pack reference), how-to (the use/author/compose/publish/validate guides + a packs hub), explanation (vision, docsite design, ADRs), tutorial (a short "adopt your first pack" getting-started).
**Languages Detected**: Content is YAML (doctrine artifacts) + Markdown (docs). Site toolchain: doc-kitty (Astro, latest release). Content-from-code generator: Python.
**Generators to Use**: doc-kitty/Astro for the site; a Python content-from-code generator that emits per-pack reference Markdown from `packs/<name>/**` (+ the author-facing `pack.yaml`), with a checksum drift gate so generated pages are never hand-edited.

### Gap Analysis Results

**Existing Documentation**:

- `docs/index.md`, `docs/toc.yml` — home + nav (explanation, authored).
- `docs/guides/{use,author,compose,publish,validate}-a-doctrine-pack.md` — how-to (authored, present).
- `docs/architecture/{vision,docsite-design}.md` + `docs/architecture/adr/*` — explanation + decisions (authored).
- `docs/packs/catalog-proposal.md` — the pack hub, as a *proposal* (needs realizing as a live catalog/hub).
- `docs/research/*` — pre-decision research (explanation).

**Identified Gaps**:

- No built site (no `site/`), no generator, no publish pipeline.
- No Brain Kitty branding wired in.
- No live **packs hub** (only a proposal) and no **per-pack reference** generated from source.
- ADR-1 selects MkDocs Material, which the operator has superseded in favour of doc-kitty/Astro — needs a new ADR; design docs reference the old generator.

**Coverage Percentage**: authored explanation/how-to ~60% present; reference 0% (ungenerated); site/publish 0%.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A developer evaluating packs can see what's on offer (Priority: P1)

A developer considering Spec Kitty packs lands on the site and wants to understand, quickly, which packs exist, what each is for, and what it contains.

**Why this priority**: Without a browsable catalog/hub, the marketplace direction is invisible; this is the site's core job.

**Independent Test**: From the published home, a first-time visitor reaches a packs hub listing every shipped pack (built-in, cave-kitty, event-driven, qa) with a one-line purpose, and drills into a per-pack page showing its artifacts, in under 3 clicks.

**Acceptance Scenarios**:

1. **Given** the published site, **When** the visitor opens the packs hub, **Then** every pack in `packs/` (plus `built-in`) is listed with its purpose and a link to its reference page.
2. **Given** a pack page, **When** the visitor reads it, **Then** the pack's artifact inventory and validation status are shown and are **generated from source** (not hand-maintained).

---

### User Story 2 - A pack user can use and compose packs with the CLI + charter (Priority: P2)

A developer adopting packs needs to know how to pull a pack into a project, activate it through the charter, and compose multiple packs.

**Why this priority**: Adoption fails without clear usage guidance tied to the real `spec-kitty` CLI and charter surface.

**Independent Test**: A reader follows the "use a pack" and "compose packs" guides end to end against the current CLI and reaches a working, activated pack.

**Acceptance Scenarios**:

1. **Given** the guides are published, **When** a user follows "use a Charter Pack", **Then** the documented `spec-kitty` commands match the current CLI and succeed.
2. **Given** a getting-started tutorial, **When** a new user follows it, **Then** they adopt and activate one pack without prior knowledge.

---

### User Story 3 - A pack author can author, validate and publish a pack (Priority: P3)

A contributor wants to write a new pack, validate it against the canonical rules, and publish it.

**Why this priority**: The marketplace grows only if authoring is well documented; the guides exist but are not surfaced in a site.

**Independent Test**: A contributor follows the author/validate/publish guides and produces a pack that passes `scripts/ci/validate-packs.sh`.

**Acceptance Scenarios**:

1. **Given** the author + validate guides, **When** a contributor follows them, **Then** their pack passes `charter pack validate` with zero errors.

---

### User Story 4 - The site is branded and published (Priority: P2)

Readers see a coherent Brain Kitty-branded site at a stable URL.

**Why this priority**: Branding + a real published URL make the open direction credible and shareable.

**Independent Test**: The site builds clean and deploys to GitHub Pages, carrying the Brain Kitty logo and theme.

**Acceptance Scenarios**:

1. **Given** the doc-kitty/Astro site, **When** CI builds it, **Then** it builds with zero errors and carries the Brain Kitty logo taken from `spec-kitty-charter`.

---

### Edge Cases

- Generated pack-reference drifts from source → a checksum/drift gate fails the build (generated pages are never hand-edited).
- A pack has no `pack.yaml` (e.g. `qa`) → the generator degrades gracefully (derives what it can; purpose absent rather than fabricated).
- The old MkDocs/DocFX references in existing docs → reconciled; the superseding ADR is the authority.

## Requirements *(mandatory)*

### Functional Requirements

#### Documentation Content

- **FR-001**: The site MUST provide a **packs hub** (how-to/reference) listing every pack under `packs/` plus `built-in`, each with purpose and a link to its reference page.
- **FR-002**: The site MUST publish the existing **how-to guides** (use/author/compose/publish/validate) and a short **getting-started tutorial** for adopting one pack.
- **FR-003**: The site MUST include **explanation** pages (vision, docsite design) and the **ADRs**, with heading hierarchy and alt text (accessibility).
- **FR-004**: Guides MUST show working `spec-kitty` CLI + charter commands that match the current CLI surface.

#### Generation Requirements

- **FR-006**: The system MUST **generate** per-pack reference pages from `packs/<name>/**` (artifact inventory, counts, validation status) — never hand-authored.
- **FR-007**: Generated reference MUST integrate with the authored guides/explanation without restating the same datum (generated-evidence vs authored-explanation boundary).
- **FR-008**: The generator + site config MUST be version-controlled and reproducible; a **checksum/drift gate** MUST fail the build if a generated page is edited by hand.

#### Branding & Publish

- **FR-012**: The site MUST carry the **Brain Kitty logo** sourced from `spec-kitty-charter` (`site/src/assets/brain-kitty.png`) as the theme logo/favicon.
- **FR-013**: The site MUST build in CI and **publish to GitHub Pages**.
- **FR-014**: A new **ADR MUST supersede ADR-1** (MkDocs Material) recording the doc-kitty/Astro decision; design docs referencing the old generator MUST be reconciled.

### Key Entities

- **Pack**: a directory under `packs/` (or `built-in`) of doctrine artifacts + optional `pack.yaml`/`org-charter.yaml`.
- **Pack reference page**: generated page per pack (inventory, counts, validation status, checksum).
- **Guide**: an authored how-to (use/author/compose/publish/validate) or tutorial.
- **ADR**: a decision record under `docs/architecture/adr`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: From the home page a visitor reaches any pack's reference in ≤ 3 clicks.
- **SC-002**: The site passes accessibility checks (heading hierarchy, image alt text, clear language).
- **SC-003**: Every pack under `packs/` + `built-in` has a generated reference page (100% coverage).
- **SC-005**: The site build completes with zero warnings or errors, and the generated-content drift gate passes.
- **SC-006**: The site deploys to GitHub Pages and renders the Brain Kitty branding.

### Quality Gates

- All images have descriptive alt text; heading hierarchy is proper.
- No broken internal links; external link health is non-gating.
- Documented CLI commands match the current `spec-kitty` surface.
- `scripts/ci/validate-packs.sh` stays green; the docs/terminology gates stay green.
- Spelling/grammar correct.

## Assumptions

- **ASM-001**: doc-kitty (Astro, latest release) is the chosen generator (supersedes ADR-1).
- **ASM-002**: The Brain Kitty logo asset in `spec-kitty-charter` may be reused here.
- **ASM-003**: The site hosts on GitHub Pages.
- **ASM-004**: Pack reference is generated from in-repo pack YAML + the author-facing `pack.yaml`; packs without `pack.yaml` degrade gracefully.

## Out of Scope

- Doctrine **logic** (resolution, DRG, activation, manifest schema, validator) — stays upstream in `spec-kitty/spec-kitty`.
- Required/recommended **tooling-list** support in packs — tracked separately (open-packs #37) and not built here.
- Documentation analytics, AI content generation, interactive consoles, i18n, video, PDF/print.
- Changing pack **content** for consumers (this mission publishes what exists; it does not re-author packs).

## Constraints

- Generated vs authored boundary is strict; a drift gate enforces it.
- The site toolchain should stay coherent with `spec-kitty-charter`'s doc-kitty stack (shared Brain Kitty branding).
- Guides must track the real CLI; outdated commands are worse than none.
