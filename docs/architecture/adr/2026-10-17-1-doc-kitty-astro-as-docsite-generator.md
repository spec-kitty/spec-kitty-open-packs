---
title: 'ADR: doc-kitty (Astro) as the docsite generator'
description: Decision to build the open-packs docsite with doc-kitty (Astro) for cross-product-line consistency and shared Brain Kitty branding; supersedes ADR-1 (MkDocs Material).
doc_status: active
updated: '2026-10-17'
related:
- architecture/docsite-design
- architecture/adr/2026-07-18-1-mkdocs-material-as-docsite-generator
- research/docsite-feasibility-and-generator
---
# doc-kitty (Astro) as the docsite generator

**Filename:** `2026-10-17-1-doc-kitty-astro-as-docsite-generator.md`

**Status:** Accepted

**Date:** 2026-10-17

**Deciders:** operator direction, with the architect squad — ratifying one shared docs toolchain
across the Spec Kitty product line

**Technical Story:** open-packs docsite epic; supersedes
[ADR-1 (MkDocs Material)](2026-07-18-1-mkdocs-material-as-docsite-generator.md); grounded in the
[feasibility & generator research](../../research/docsite-feasibility-and-generator.md)

---

## Context and Problem Statement

[ADR-1](2026-07-18-1-mkdocs-material-as-docsite-generator.md) chose MkDocs Material as the
static-site generator (SSG) for the open-packs docsite, on the strength of a single Python toolchain
and the largest OSS documentation ecosystem. That ADR explicitly recorded its own
reconsideration trigger: the SSG choice is **decoupled** from the content-from-code generator (the
generator emits Markdown; any SSG consumes it), so the SSG can change without disturbing the real
engineering.

Since that decision, `spec-kitty-charter` adopted **doc-kitty**, an Astro-based docs toolkit, for its
own published site, together with the shared **Brain Kitty** branding. The open question is no longer
"what is the best SSG for a standalone Python repo?" but "what should the Spec Kitty **product line**
standardize on so its sites look, build, and are maintained as one?" MkDocs Material would leave
open-packs on a different SSG, theme, and authoring convention from its sibling repo.

## Decision Drivers

* **Cross-product-line consistency.** `spec-kitty-charter`'s site is already built with doc-kitty
  (Astro). Standardizing open-packs on the same toolkit gives the product line one site system —
  shared navigation model, shared components, shared build and publish pipeline — instead of two
  divergent ones.
* **Shared Brain Kitty branding.** doc-kitty ships the Brain Kitty look-and-feel the sibling site
  already uses; adopting it makes the two sites visibly one family without re-implementing a theme.
* **One shared toolchain to maintain.** A single docs toolkit across repos means one place to learn,
  one place to upgrade, and one place to fix — lower long-term maintenance than two SSGs.
* **The SSG is decoupled from the generator (per the feasibility research).** Content-from-code
  emits Markdown, which doc-kitty consumes as readily as MkDocs would. Switching the SSG therefore
  does **not** touch the generated-vs-authored boundary, the checksum/provenance design, or the CI
  drift gate — only the tool that renders the Markdown changes.

## Considered Options

* **doc-kitty (Astro)** — the toolkit `spec-kitty-charter` already uses; shared Brain Kitty branding,
  one product-line toolchain, Markdown-in content-from-code consumed as-is.
* **MkDocs Material** (ADR-1's choice) — Python-native, large OSS ecosystem, but leaves open-packs on
  a different SSG, theme, and authoring convention from the sibling repo.

## Decision Outcome

**Chosen option:** "doc-kitty (Astro)", because it puts both Spec Kitty docs repos on one toolchain
with one shared Brain Kitty brand, which outweighs MkDocs Material's single-repo Python-ecosystem
advantages now that a sibling site has set the product-line direction. Because the SSG is decoupled
from the content-from-code generator, this is a **generator-of-the-site** change only: the
source-of-truth model, the generated-vs-authored boundary, the build-time checksum/provenance design
([ADR-3](2026-07-18-3-build-time-checksum-tagging.md)), and the regenerate-and-diff CI gate are all
**unchanged** — they are SSG-independent by construction.

This ADR **supersedes [ADR-1 (MkDocs Material)](2026-07-18-1-mkdocs-material-as-docsite-generator.md)**.
ADR-1 is marked Superseded and kept for history.

### Consequences

#### Positive

* One docs toolchain and one Brain Kitty brand across `spec-kitty-charter` and
  `spec-kitty-open-packs` — the product line's sites read as one system.
* Shared components, navigation model, and publish pipeline: learn, upgrade, and fix once.
* No divergence from the sibling site's theme or authoring conventions.

#### Negative

* Introduces an Astro/Node toolchain for the site, where ADR-1 anticipated a single Python toolchain
  end-to-end; the validator and generator stay Python, so the repo now spans two runtimes at the site
  seam (the generator is unaffected — see Neutral).
* The content-from-code generator emits Markdown that must satisfy doc-kitty's frontmatter schema
  (required fields, description length, slug-based `related` refs) rather than MkDocs conventions.

#### Neutral

* The content-from-code generator (the real engineering) is **unaffected**: it emits Markdown either
  way. The [ADR-2](2026-07-18-2-pack-reference-generated-from-source.md) pack-reference generation and
  [ADR-3](2026-07-18-3-build-time-checksum-tagging.md) checksum design are SSG-independent and carry
  over verbatim.
* Navigation is now driven by doc-kitty's `docs/_meta/sections.yaml` section registry; the earlier
  DocFX-shaped `docs/toc.yml` is superseded and no longer the nav source of truth.

### Confirmation

Validated when the repo builds and publishes with doc-kitty (Astro) using the sibling site's shared
toolchain and Brain Kitty theme, with the content-from-code generator wired as a pre-build step and
navigation resolved from `docs/_meta/sections.yaml`. Confidence: high — a sibling site already runs
this toolchain in production, and the SSG swap leaves the generator and integrity design untouched.

## Pros and Cons of the Options

### doc-kitty (Astro)

**Pros:** one shared toolchain and Brain Kitty brand across the Spec Kitty docs repos; shared
components and publish pipeline; consumes the generator's Markdown as-is; a sibling site already
proves the pattern.
**Cons:** adds an Astro/Node runtime at the site seam, so the repo is no longer single-language
end-to-end; generated Markdown must satisfy doc-kitty's frontmatter schema.

### MkDocs Material

**Pros:** Python-native (one language with the validator/generator); largest OSS documentation
ecosystem; purpose-built content-from-code plugins.
**Cons:** leaves open-packs on a different SSG, theme, and authoring convention from
`spec-kitty-charter`; no product-line consistency or shared branding; a second docs toolchain to
maintain.
**Superseded** by this ADR: the product-line consistency and shared-branding drivers now outrank the
single-repo Python-ecosystem advantages, and the low, by-construction cost of an SSG swap makes the
change cheap.
