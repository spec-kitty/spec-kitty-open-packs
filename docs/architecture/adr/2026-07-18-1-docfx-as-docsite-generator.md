---
title: 'ADR: DocFX as the docsite generator'
description: Decision to build the spec-kitty-open-packs docsite with DocFX for consistency with core and lowest new maintenance, with MkDocs Material as the named fallback and Hugo rejected.
doc_status: active
updated: '2026-07-18'
related:
- docs/architecture/docsite-design.md
- docs/research/docsite-feasibility-and-generator.md
---
# DocFX as the docsite generator

**Filename:** `2026-07-18-1-docfx-as-docsite-generator.md`

**Status:** Proposed

**Date:** 2026-07-18

**Deciders:** architect squad (proposed) — pending HiC ratification

**Technical Story:** open-packs docsite epic; grounded in [feasibility & generator research](../../research/docsite-feasibility-and-generator.md)

---

## Context and Problem Statement

`spec-kitty-open-packs` needs a published docsite that is simple to maintain and pulls reference
content from the actual code structure. A static-site generator must be chosen. The task named Hugo
(with a "?"); DocFX and MkDocs Material are the realistic alternatives. The repo is already
half-configured for DocFX: `docs/toc.yml` is DocFX-shaped and every doc carries
`doc_status`/`title`/`description` frontmatter, mirroring core.

## Decision Drivers

* **Content-from-code is SSG-agnostic** — the generator emits Markdown, which all three candidates
  consume, so generation ergonomics do not distinguish them. The choice turns on consistency,
  maintenance, and contributor familiarity.
* **Consistency with core is a stated goal** — one look, one publishing pipeline, one
  `docs.spec-kitty.ai` presence.
* **Lowest *new* maintenance for a small OSS team.**
* Core already operates the exact target pattern: a Python generator emits Markdown, then
  `docfx docfx.json`, then GitHub Pages (`.github/workflows/docs-pages.yml`).

## Considered Options

* **DocFX** — same engine, template, and pipeline as core; already half-wired here.
* **MkDocs Material** — Python-native, widest OSS contributor base, purpose-built generation plugins.
* **Hugo** — large community, but Go toolchain + Go templates, new to this stack.

## Decision Outcome

**Chosen option:** "DocFX", because it delivers the lowest *new* maintenance (the generate → build →
Pages pattern is already operated by the core team and directly reusable), it is already wired into
this repo, and it is the only option that satisfies the consistency-with-core driver. The
content-from-code investment is SSG-agnostic, so DocFX costs nothing extra on the dimension the task
cares most about.

**Named fallback:** adopt **MkDocs Material** if the repo later prioritizes contributor familiarity
and toolchain independence over brand/pipeline consistency — it aligns with the Python stack the
generator and validator already live in.

### Consequences

#### Positive

* One doc toolchain, template, and domain shared with core; the Pages workflow is a copy.
* `toc.yml` + frontmatter conventions already in place — only `docfx.json`, the generator, and a
  Pages workflow remain.

#### Negative

* DocFX needs the .NET SDK in CI, and its community is smaller than MkDocs' — contributors must learn
  `toc.yml`/DocFX conventions (mitigated: contributors add packs, not docs).
* Couples the docsite's look-and-feel evolution to core's DocFX template choices.

#### Neutral

* The generator (the real engineering) is unaffected by this choice and would be reused verbatim
  under the MkDocs fallback.

### Confirmation

Validated when the repo builds and publishes to a `spec-kitty.ai` Pages presence using a copied
`docs-pages.yml` + `docfx.json`, with the pack-reference generator wired as a pre-build step.
Confidence: high — the pattern is already proven in core.

## Pros and Cons of the Options

### DocFX

**Pros:** consistency with core; already wired; proven Pages pipeline; reuses core template.
**Cons:** .NET SDK dependency; smaller community; DocFX-specific `toc.yml` authoring.

### MkDocs Material

**Pros:** Python-native (matches validator/generator stack); `mkdocs-gen-files`/`mkdocstrings`;
largest OSS contributor base.
**Cons:** a second, divergent look and pipeline vs core; no consistency payoff.

### Hugo

**Pros:** large community; fast builds.
**Cons:** Go toolchain + Go-template learning curve; zero ecosystem alignment or consistency payoff.
**Rejected.**
