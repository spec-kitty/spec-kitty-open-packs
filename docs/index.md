---
title: Spec Kitty Open Packs
description: Documentation home for the open, free doctrine packs distributed for Spec Kitty — usage guides, authoring guides, and the pack catalog proposal.
doc_status: active
updated: '2026-10-10'
okf_version: '0.2'
kind: Hub
# The bundle root is exempt from `type` by the DocKitty convention (it carries
# okf_version instead). It sits in no section, so llms.txt would list it under an
# empty heading; the llms.txt header already carries the site title/description.
agent:
  discoverable: false
related:
- guides
- packs/catalog-proposal
- architecture
- research
- changelog
---
# Spec Kitty Open Packs

> **🚧 Work in progress.** This repository is an early, in-the-open product-direction shift
> toward *doctrine packs as a marketplace*. Structure, pack boundaries, and the composition
> mechanics are still moving. See the [README](../README.md) for the full status banner.

Open, free **doctrine packs** for [Spec Kitty](https://github.com/spec-kitty/spec-kitty):
coherent, composable, opt-in slices of governance behaviour that consumer projects pull in
deliberately — instead of inheriting the entire built-in doctrine corpus and flooding every
LLM session's context.

## Start here

- **Understand the direction** — [README](../README.md) and the
  [pack catalog proposal](packs/catalog-proposal.md).
- **Use a pack** — [Use a Charter Pack](guides/use-a-doctrine-pack.md),
  [Compose packs](guides/compose-packs.md).
- **Author a pack** — [Author a Charter Pack](guides/author-a-doctrine-pack.md),
  [Validate a pack](guides/validate-a-pack.md), [Publish a pack](guides/publish-a-pack.md).

## How this repository is organized

This tree is published as the docsite at
<https://spec-kitty.github.io/spec-kitty-open-packs/>, built with DocKitty
([ADR-5](architecture/adr/2026-10-10-5-dockitty-docsite.md)).

| Path | Contents |
| --- | --- |
| `docs/guides/` | Usage and authoring how-to guides. |
| `docs/packs/` | The pack catalog proposal and the generated per-pack [reference](packs/reference/index.md). |
| `docs/architecture/` | Vision, docsite design, and decision records (`adr/`). |
| `docs/research/` | Pre-decision investigations that ground the architecture. |
| `docs/changelog/` | Canonical changelog (root `CHANGELOG.md` symlinks here). |
| `docs/_meta/charter.yaml` | Docsite navigation and section mapping (DocKitty documentation charter). |
| `packs/` | The doctrine packs themselves (materialized incrementally). |

## Relationship to Spec Kitty core

Content and packaging live here; doctrine **logic** — resolution, the DRG, activation, the
manifest schema, and the pack validator — lives in
[`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty). Cross-referencing is
expected. This repository's issues track **pack creation**; core's issues track **doctrine
functionality**.
