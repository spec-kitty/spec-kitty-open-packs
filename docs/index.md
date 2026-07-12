---
title: Spec Kitty Open Packs
description: Documentation home for the open, free doctrine packs distributed for Spec Kitty — usage guides, authoring guides, and the pack catalog proposal.
doc_status: wip
updated: '2026-07-12'
related:
- docs/guides/index.md
- docs/packs/catalog-proposal.md
- docs/changelog/index.md
---
# Spec Kitty Open Packs

> **🚧 Work in progress.** This repository is an early, in-the-open product-direction shift
> toward *doctrine packs as a marketplace*. Structure, pack boundaries, and the composition
> mechanics are still moving. See the [README](../README.md) for the full status banner.

Open, free **doctrine packs** for [Spec Kitty](https://github.com/Priivacy-ai/spec-kitty):
coherent, composable, opt-in slices of governance behaviour that consumer projects pull in
deliberately — instead of inheriting the entire built-in doctrine corpus and flooding every
LLM session's context.

## Start here

- **Understand the direction** — [README](../README.md) and the
  [pack catalog proposal](packs/catalog-proposal.md).
- **Use a pack** — [Use a doctrine pack](guides/use-a-doctrine-pack.md),
  [Compose packs](guides/compose-packs.md).
- **Author a pack** — [Author a doctrine pack](guides/author-a-doctrine-pack.md),
  [Validate a pack](guides/validate-a-pack.md), [Publish a pack](guides/publish-a-pack.md).

## How this repository is organized

| Path | Contents |
| --- | --- |
| `docs/guides/` | Usage and authoring how-to guides. |
| `docs/packs/` | The pack catalog proposal and (later) per-pack reference. |
| `docs/changelog/` | Canonical changelog (root `CHANGELOG.md` symlinks here). |
| `packs/` | The doctrine packs themselves (materialized incrementally). |

## Relationship to Spec Kitty core

Content and packaging live here; doctrine **logic** — resolution, the DRG, activation, the
manifest schema, and the pack validator — lives in
[`Priivacy-ai/spec-kitty`](https://github.com/Priivacy-ai/spec-kitty). Cross-referencing is
expected. This repository's issues track **pack creation**; core's issues track **doctrine
functionality**.
