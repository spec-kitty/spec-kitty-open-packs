---
title: 'ADR: MkDocs Material as the docsite generator'
description: Decision to build the spec-kitty-open-packs docsite with MkDocs Material — a single Python toolchain, purpose-built content-from-code plugins, and the largest OSS ecosystem — with DocFX (consistency-with-core) recorded as a considered-but-deferred option and Hugo rejected.
doc_status: active
updated: '2026-07-25'
related:
- docs/architecture/docsite-design.md
- docs/research/docsite-feasibility-and-generator.md
---
# MkDocs Material as the docsite generator

**Filename:** `2026-07-18-1-mkdocs-material-as-docsite-generator.md`

**Status:** Proposed

**Date:** 2026-07-18 (decision revised 2026-07-25)

**Deciders:** architect squad (initial DocFX-leaning draft) → revised to MkDocs Material following
maintainer review ([@zohar](https://github.com/zohar)) and operator direction — pending HiC ratification

**Technical Story:** open-packs docsite epic; grounded in [feasibility & generator research](../../research/docsite-feasibility-and-generator.md)

---

## Context and Problem Statement

`spec-kitty-open-packs` needs a published docsite that is simple to maintain and pulls reference
content from the actual code structure. A static-site generator must be chosen. The task named Hugo
(with a "?"); DocFX and MkDocs Material are the realistic alternatives. The repo is already
half-configured for DocFX: `docs/toc.yml` is DocFX-shaped and every doc carries
`doc_status`/`title`/`description` frontmatter, mirroring core.

**Revision note (2026-07-25).** The initial draft chose DocFX on a single driver — *consistency with
core*. Maintainer review surfaced that this driver is not a technical merit but a **resource-bounded
constraint** ("migrating both repos is out of scope right now"), and that the design deliberately
keeps the SSG choice *portable*: the generator emits Markdown, the IA is SSG-agnostic, and switching
a site's nav is a mechanical `toc.yml` → `nav:` rewrite. With switching cost low and consistency the
only thing DocFX clearly won on, the honest question is **"what should both repos standardize on?"**
— and the answer, for a fundamentally Python product, is MkDocs Material. This ADR records that
revised decision.

## Decision Drivers

* **The SSG choice is decoupled from any implementation language.** Content-from-code emits Markdown,
  which every candidate consumes, so the generator (the real engineering) is reused verbatim under
  any SSG. This also means the decision does **not** bind to core's language direction — see the
  open question below.
* **One Python toolchain end-to-end** — validator, generator, and site all in Python. MkDocs Material
  is purpose-built for exactly this pattern (`mkdocs-gen-files` / `mkdocstrings`), whereas DocFX drags
  a **.NET SDK** into CI for a repo that has no other .NET surface.
* **Largest OSS documentation ecosystem** — matters for a community-facing pack catalog whose readers
  and contributors are far likelier to know MkDocs than DocFX.
* **Consistency with core is real but resource-bounded** — it is the one thing DocFX wins on, and the
  low switching cost (Markdown output + mechanical nav rewrite) makes it a weak reason to inherit a
  .NET toolchain. The stronger long-term move is to standardize **both** repos on MkDocs Material.

## Considered Options

* **MkDocs Material** — Python-native, purpose-built content-from-code plugins, widest OSS contributor
  base, no .NET in CI.
* **DocFX** — same engine, template, and pipeline as core; already half-wired here. Wins only on
  consistency-with-core, which is a resource-bounded constraint, not a technical merit.
* **Hugo** — large community, but Go toolchain + Go templates, new to this stack.

## Decision Outcome

**Chosen option:** "MkDocs Material", because it keeps the entire toolchain — validator, generator,
and site — in one language (Python), it is purpose-built for content-from-code generation, and it
draws on the largest OSS documentation ecosystem for a community-facing catalog. The one dimension
DocFX wins on — consistency with core — is a resource-bounded constraint rather than a technical
merit, and the design's Markdown-portability keeps the cost of diverging (or of later re-converging)
low.

**Considered but deferred — standardize both repos on MkDocs Material.** Core currently publishes with
DocFX. Rather than inherit that toolchain here, the recommendation is that **core also migrate to
MkDocs Material** so both repos share one Python toolchain. That cross-repo migration needs HiC/core
buy-in and its own scoping, so it is recorded here as the deferred long-term target, not a
prerequisite for this repo's decision.

**Rejected — DocFX.** Not adopted: its only advantage here is matching core's *current* generator, at
the cost of a .NET SDK in CI and a smaller contributor ecosystem. If core declines the MkDocs
migration **and** cross-repo pipeline consistency later outranks toolchain simplicity, this ADR should
be revisited — but the interim divergence is cheap by construction.

### Open question / reconsideration trigger

Core has signalled it may move parts of its stack **off Python** in the coming months. That would
weaken the "one Python toolchain end-to-end" driver. It does **not** flip this decision, because the
SSG is decoupled from the generator's language (Markdown in, site out): open-packs can keep MkDocs
regardless of what language core's generator is written in. Revisit only if (a) core commits to a
non-Python stack **and** (b) open-packs' own generator follows it off Python — at which point the
"single toolchain" argument no longer applies and DocFX-vs-MkDocs should be re-weighed on ecosystem
and CI-simplicity alone.

### Consequences

#### Positive

* One Python toolchain for validator, generator, and site; no .NET SDK in CI.
* `mkdocs-gen-files` / `mkdocstrings` are built for content-from-code — less hand-rolled glue.
* Largest OSS doc ecosystem — lowest contributor friction for a public catalog.

#### Negative

* Diverges from core's *current* DocFX site until/unless core migrates — two pipelines short-term.
* The existing DocFX-shaped `docs/toc.yml` must be re-expressed as a MkDocs `nav:` (mechanical; a
  deferred implementation step, not part of this decisions-only PR).
* Frontmatter conventions carry over unchanged; the `docfx.json` groundwork is dropped in favour of
  an `mkdocs.yml`.

#### Neutral

* The generator (the real engineering) is unaffected by this choice and would be reused verbatim
  under DocFX; the ADR-2 pack-reference generation and ADR-3 checksum design are SSG-independent.

### Confirmation

Validated when the repo builds and publishes to a `spec-kitty.ai` Pages presence using `mkdocs build`
(Material theme) + a GitHub Pages workflow, with the pack-reference generator wired as a `mkdocs-gen-files`
pre-build step and the interim `docs/toc.yml` re-expressed as `mkdocs.yml` `nav:`. Confidence: high —
MkDocs Material + gen-files is the canonical content-from-code pattern for Python projects.

## Pros and Cons of the Options

### MkDocs Material

**Pros:** single Python toolchain (matches validator/generator stack); `mkdocs-gen-files`/`mkdocstrings`
purpose-built for content-from-code; largest OSS contributor base; no .NET in CI.
**Cons:** diverges from core's current DocFX pipeline until core migrates; requires a one-time
`toc.yml` → `nav:` rewrite.

### DocFX

**Pros:** consistency with core's *current* site; already half-wired; proven Pages pipeline; reuses
core template.
**Cons:** .NET SDK dependency in an otherwise-Python repo; smaller community; DocFX-specific `toc.yml`
authoring; consistency payoff is resource-bounded, not a durable merit.
**Rejected** (kept as the fallback only if core declines the MkDocs migration and pipeline consistency
later outranks toolchain simplicity).

### Hugo

**Pros:** large community; fast builds.
**Cons:** Go toolchain + Go-template learning curve; zero ecosystem alignment or Python-stack payoff.
**Rejected.**
