---
title: Compose packs
description: How Spec Kitty composes doctrine vertically (built-in, org, project) and horizontally (independent packs and compound depends_on packs), and how conflicts resolve.
doc_status: wip
updated: '2026-07-12'
related:
- docs/guides/use-a-doctrine-pack.md
- docs/packs/catalog-proposal.md
---
# Compose packs

Spec Kitty composes doctrine along two axes. Understanding both is the key to keeping a
project's context lean while still pulling in exactly the governance you want.

> **🚧 WIP.** Horizontal composition via compound `depends_on` packs is being established by
> the keystone [core #2467](https://github.com/Priivacy-ai/spec-kitty/issues/2467). The
> semantics below describe the intended model and will track that work as it lands.

## Vertical composition (today)

Doctrine resolves in layers, later layers overriding earlier ones by artifact `id`:

```
built-in   →   org (packs)   →   project (local overlay)
```

- **built-in** — the corpus shipped with Spec Kitty core.
- **org** — the packs you configure under `doctrine.org.packs` (including open packs from
  this repository).
- **project** — local, in-repo overrides for one project only.

An org pack whose artifact `id` collides with a built-in id performs a **full replace** of
that artifact and surfaces an advisory. Keep such overrides intentional and rare — namespaced
IDs avoid them.

## Horizontal composition (the pack direction)

Two mechanisms let independent packs combine *within* the org layer:

### 1. Multiple independent packs

List several packs under `doctrine.org.packs`. Each contributes its artifacts additively;
there is no dependency between them. This is how you assemble, say, a DDD pack + a Java pack +
a testing pack for a single project.

### 2. Compound packs (`depends_on`)

A pack may declare that it **depends on** other packs. Spec Kitty resolves the dependency
graph (a DAG, with cycle detection) before loading, so a compound pack can bundle a coherent
stack without the consumer having to enumerate every constituent pack.

```yaml
# pack-manifest is written by tooling, not by hand — shown here to illustrate the model
pack_id: java-ddd-stack
version: 0.1.0
depends_on:
  - core-engineering
  - domain-driven-design
  - java-development
  - test-and-bdd
```

Consumers configure only `java-ddd-stack`; the four dependencies resolve transitively.

## Conflict resolution

When two packs contribute the same artifact `id`, or the same DRG edge:

- **Assembly time** (`doctrine pack assemble`) fails by default with a conflict report. Use
  `--conflicts-out` to inspect, or `--force` for last-pack-wins.
- **Resolution time** the layer order (built-in → org → project) decides precedence, and
  colliding org-pack IDs surface as advisories in `charter lint` / `doctor doctrine`.

DRG fragments (`drg/*.graph.yaml`) are **additive only** — a pack may add edges and nodes but
must not remove or modify built-in graph state.

## Keeping context lean

Composition multiplies the doctrine in play. Two habits keep sessions from flooding:

1. **Add only the packs your project's domain needs.** Prefer a focused stack over "activate
   everything."
2. **Author a charter.** The charter constrains which activated doctrine actually resolves per
   action, which is the mechanism that stops multi-pack projects from ballooning context.

## See also

- [Use a doctrine pack](use-a-doctrine-pack.md)
- [Pack catalog proposal](../packs/catalog-proposal.md) — proposed packs and the compound
  stacks built on them.
