---
title: Guides
description: Usage and authoring how-to guides for Spec Kitty open doctrine packs — consuming a pack, composing packs, and authoring, validating, and publishing your own.
doc_status: wip
updated: '2026-07-12'
related:
- docs/index.md
- docs/packs/catalog-proposal.md
- docs/guides/author-a-doctrine-pack.md
- docs/guides/use-a-doctrine-pack.md
---
# Guides

Task-oriented how-tos for working with Spec Kitty open doctrine packs. Two audiences:

## Using packs

For teams who want to *consume* packs in their own Spec Kitty projects.

- [Use a doctrine pack](use-a-doctrine-pack.md) — configure `.kittify/config.yaml`, fetch a
  pack, and confirm it participates in context resolution.
- [Compose packs](compose-packs.md) — vertical (built-in → org → project) and horizontal
  (independent packs + compound `depends_on` packs) composition, and how conflicts resolve.

## Authoring packs

For maintainers who want to *produce* and distribute packs.

- [Author a doctrine pack](author-a-doctrine-pack.md) — lay out the directory, write
  artifacts, namespace IDs, and add DRG fragments.
- [Validate a pack](validate-a-pack.md) — run the canonical validator, read its output, and
  wire it into CI.
- [Publish a pack](publish-a-pack.md) — git, HTTPS bundle, or API distribution; versioning
  and trust considerations.

## Canonical upstream reference

The mechanics these guides drive live in Spec Kitty core. The most complete upstream
reference is
[How to Create an Org Doctrine Pack](https://github.com/Priivacy-ai/spec-kitty/blob/main/docs/guides/create-an-org-doctrine-pack.md).
These guides adapt that material for the open-packs marketplace direction and will track it
as the pack ecosystem (`#2466`) evolves.
