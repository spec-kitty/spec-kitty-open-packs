---
title: 'ADR: DocKitty (Astro + Starlight) as the docsite toolchain'
description: 'Decision to build the docsite with DocKitty (@spec-kitty/doc-toolkit on Astro + Starlight), one docs toolchain across Spec Kitty repos. Supersedes ADR-1.'
doc_status: active
updated: '2026-10-10'
type: ADR
kind: ADR
related:
- architecture/adr/2026-07-18-1-mkdocs-material-as-docsite-generator
- architecture/adr/2026-07-18-2-pack-reference-generated-from-source
- architecture/adr/2026-07-18-4-docsite-information-architecture
- architecture/docsite-design
external_references:
- url: https://github.com/spec-kitty/doc-kitty/blob/main/docs/guides/consumer-setup.md
  title: DocKitty consumer setup guide
- url: https://github.com/spec-kitty/doc-kitty/blob/main/docs/context/convention.md
  title: The DocKitty documentation convention
---
# DocKitty (Astro + Starlight) as the docsite toolchain

**Filename:** `2026-10-10-5-dockitty-docsite.md`

**Status:** Accepted. Supersedes [ADR 2026-07-18-1](2026-07-18-1-mkdocs-material-as-docsite-generator.md)
(MkDocs Material).

**Date:** 2026-10-10

**Deciders:** repository maintainer (operator decision); implemented by an agent

**Technical Story:** docsite epic [#19](https://github.com/spec-kitty/spec-kitty-open-packs/issues/19),
pipeline [#20](https://github.com/spec-kitty/spec-kitty-open-packs/issues/20); toolkit release
[spec-kitty/doc-kitty#108](https://github.com/spec-kitty/doc-kitty/pull/108)

---

## Context and Problem Statement

[ADR-1](2026-07-18-1-mkdocs-material-as-docsite-generator.md) proposed MkDocs Material for the
docsite. It was never implemented: no `mkdocs.yml` landed and the interim nav still lived in a
DocFX-era `docs/toc.yml`. Since then Spec Kitty has built **DocKitty**: a documentation convention
(Common Docs plus a few deliberate twists) and a reusable toolkit, `@spec-kitty/doc-toolkit`, which
renders a repo's `docs/` tree with Astro + Starlight. It also produces `sitemap.xml`, `rss.xml`,
`llms.txt`, and an agent-API.

ADR-1's main driver was "standardize both repos on one toolchain". That driver now points at
DocKitty, because it is the toolchain Spec Kitty repos are converging on. The maintainer decided
that this repository adopts DocKitty, and that the toolkit is published to npm (0.1.1, doc-kitty#108)
before this repository depends on it.

## Decision Drivers

* **One docs toolchain across Spec Kitty repos.** Every repo gets the same convention, theme,
  frontmatter contract, and machine surfaces (feeds, `llms.txt`, agent-API). One fix in the toolkit
  reaches every site.
* **Content-from-code stays SSG-independent.** The pack-reference generator (ADR-2) emits Markdown,
  so it can feed any renderer. Only the page *contract* (frontmatter) has to match.
* **Low migration cost.** The existing tree already follows Common Docs. DocKitty reads it in place,
  including `index.md` section indexes (its `indexBasename` option), so no files have to move.
* **A published, versioned dependency.** We consume a released npm package, not a git checkout.

## Considered Options

* **DocKitty** (`@spec-kitty/doc-toolkit` on Astro + Starlight)
* **MkDocs Material** (ADR-1, never implemented)
* **DocFX** (core's current generator, rejected in ADR-1)

## Decision Outcome

**Chosen option:** "DocKitty", because it is the shared Spec Kitty docs toolchain, it renders the
existing Common Docs tree with no file moves, and it adds the agent-facing surfaces (`llms.txt`,
agent-API) that a pack catalog for AI agents should have.

How it is wired (following doc-kitty's consumer-setup guide):

* **The repo root is the Astro project.** That means `package.json`, `astro.config.mjs`,
  `src/content.config.ts`, `src/pages/**`, and the repo-root `docs/` tree as the content root. The
  guide assumes this layout: the loader's `base: 'docs'` and the integration's `docsDir` resolve
  against the project root and must be plain paths inside it. A `site/` subfolder would need a
  `../docs` content root, which the toolkit's `docsDir` contract does not support.
* **Dependencies:** `@spec-kitty/doc-toolkit@^0.1.1`, `astro@^5.2.0`, `@astrojs/starlight@^0.32.6`
  (the toolkit's peer range is `>=0.32.0 <0.33.0`), and `@astrojs/sitemap@^3.2.0`, managed with
  pnpm as the toolkit does. The integrations come from `defineDocKittyIntegrations` with the
  Spec Kitty theme and `base: /spec-kitty-open-packs` for GitHub Pages.
* **Navigation and section mapping** live in `docs/_meta/charter.yaml` (DocKitty's documentation
  charter, doc-kitty's ADR-0042). It replaces `docs/toc.yml`. The top-level section names and
  order from [ADR-4](2026-07-18-4-docsite-information-architecture.md) are kept: Guides →
  Pack Catalog → Architecture → Research → Changelog, with ADRs still nested under
  `architecture/adr/`. Pages inside a section are ordered with Starlight `sidebar.order`
  frontmatter (section hub first). Nested folders (`architecture/adr/`, `packs/reference/`)
  render as sidebar sub-groups labelled with the raw folder name (`adr`, `reference`):
  Starlight 0.32 autogenerated groups take no label override, so this is a deviation from
  ADR-4's nav, not a faithful copy of it. The charter maps the sections onto DocKitty's
  twelve canonical sections:

  | Folder | Charter type | Note |
  | --- | --- | --- |
  | `guides/` | `Guide` | canonical section |
  | `packs/` | `Plan` | repo section "Pack Catalog" (the catalog is a proposal) |
  | `packs/reference/` | `API` (subtype) | generated pack reference (ADR-2) |
  | `architecture/` | `Architecture` | canonical section |
  | `architecture/adr/` | `ADR` (subtype) | ADR-4 nests ADRs instead of using top-level `adr/` |
  | `research/` | `Context` | repo section "Research" (background investigations) |
  | `changelog/` | `Changelog` | canonical section |

  The unused canonical sections stay deferred, per ADR-4's anti-sprawl rule.
* **`doc_status`.** The DocFX-era `wip` is not a DocKitty status. The guides refreshed for the 4.x
  Charter Pack cutover, the home page, and the changelog become `active`. The catalog proposal
  becomes `draft`: it is explicitly unratified. DocKitty (toolkit 0.1.1) keeps drafts out of the
  sitemap, RSS, `llms.txt` and the agent-API *index* (`/api/index.json`), but still renders the
  page and still publishes its per-page agent-API document (`/api/pages/<slug>.json`, full body).
  Draft therefore means "not advertised", not "not published"; closing that gap is a doc-kitty
  follow-up. The research pages were already `active` and stay that way: they are finished
  investigations, not work in progress. ADR-1 becomes `superseded`. ADR files keep `doc_status: active` as the *document* lifecycle, while
  the *decision* status stays in the body, as the DocKitty convention says.
* **Links.** The tree uses GitHub-style `.md`-relative links, which Starlight emits unchanged (and
  which 404 on a site with a base path). A small local rehype plugin
  (`src/plugins/rehype-repo-links.mjs`) rewrites them at render time. Links to pages and folders
  become site routes. Links to files outside the site, like `SECURITY.md` or `packs/`, become GitHub
  URLs. The Markdown therefore keeps working on both GitHub and the site, and no ADR or research
  prose had to change.
* **ADR-2's generator now targets DocKitty pages.** `scripts/docs/generate_pack_reference.py` writes
  `docs/packs/reference/*.md` with the DocKitty frontmatter contract and a `generated: {by, at}`
  stamp. It runs as a separate drift check in CI, not as an MkDocs `gen-files` plugin. ADR-2's
  decision (generate the reference from source, block drift in CI) is unchanged, and so is ADR-3
  (checksums). ADR-4's decision stands, but its nav is only approximated (see Negative below).
* **The ADR template lives outside the site** at `.github/ADR_TEMPLATE.md`, so its placeholder
  page is not published (the toolkit's loader would publish any `.md` under `docs/`, including
  `docs/_meta/`).

### Consequences

#### Positive

* One docs toolchain and one look across Spec Kitty repos. Toolkit fixes and new surfaces reach
  this site through a version bump.
* Agent-facing surfaces (`llms.txt`, `/api/index.json`, per-page JSON) come for free, which suits a
  catalog that AI coding agents consume.
* No content moves. `index.md` section indexes and the nested ADR folder are kept.

#### Negative

* **A Node toolchain sits next to the Python generator and validator.** CI needs Node 22 and pnpm
  as well as Python. ADR-1 had optimised for a single language. We accept this in exchange for
  cross-repo consistency.
* **Depends on a pre-1.0 toolkit release.** The site cannot build until
  `@spec-kitty/doc-toolkit@0.1.1` is on npm. No lockfile is committed until the package can be
  resolved from the registry.
* **ADRs are not a top-level nav group, and nested groups show folder names.** DocKitty's
  section registry keys sidebar groups by top-level folder, so `architecture/adr/` shows up as a
  sub-group of Architecture labelled `adr` (and the pack reference as `reference`). ADR-4 asked for
  a top-level node. Getting one would mean either a hand-maintained `sidebar` override or moving
  ADRs to `docs/adr/`. ADR-4 already names that move as its migration anchor, and it is left as a
  follow-up decision.
* The link-rewriting plugin is local code. If the toolkit later handles `.md`-relative links
  itself, this plugin should be removed.

#### Neutral

* The frontmatter gains `type` and `kind`, and descriptions are capped at 180 characters (the
  DocKitty contract). `related` refs become docs-root-relative slugs, and repo-file refs move to
  `external_references`.

### Confirmation

This decision is confirmed when the `Docsite` workflow builds the site on pull requests and
publishes to `https://spec-kitty.github.io/spec-kitty-open-packs/` from `main`, and when the
toolkit's `validate-frontmatter` and `check-links` gates and the pack-reference `--check` pass in
CI. Confidence: high. The same wiring is what doc-kitty's own consumption test builds from the
packed tarball.

## Pros and Cons of the Options

### DocKitty

**Pros:** the shared Spec Kitty toolchain; reads the existing tree in place; agent-API, `llms.txt`
and feeds built in; Spec Kitty theme.
**Cons:** adds Node to CI; pre-1.0 dependency that is not on npm until doc-kitty#108 ships; ADRs
render as a nested group.

### MkDocs Material

**Pros:** pure Python; large ecosystem.
**Cons:** a second docs toolchain inside Spec Kitty; nothing was ever built on it here; no
agent-API or `llms.txt` without extra plugins. **Superseded.**

### DocFX

**Pros:** what core's site uses today.
**Cons:** .NET SDK in CI; DocKitty is where Spec Kitty repos are heading. **Rejected** (as in ADR-1).
