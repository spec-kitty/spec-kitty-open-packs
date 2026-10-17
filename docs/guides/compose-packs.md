---
title: Compose packs
description: How Spec Kitty 4.x composes Charter Packs vertically (built-in, org, project) and horizontally (independent packs and compound depends_on packs), and how conflicts resolve.
doc_status: wip
updated: '2026-10-10'
related:
- guides/use-a-doctrine-pack
- packs/catalog-proposal
---
# Compose packs

Spec Kitty composes doctrine along two axes. Understanding both is the key to keeping a
project's context lean while still pulling in exactly the governance you want.

> **🚧 WIP.** Horizontal composition via compound `depends_on` packs is being established by
> the keystone [core #2467](https://github.com/spec-kitty/spec-kitty/issues/2467). The
> semantics below describe the intended model and will track that work as it lands.

## Vertical composition (today)

Doctrine resolves in layers, later layers overriding earlier ones by artifact `id`:

```
built-in   →   org (packs)   →   project (local overlay)
```

- **built-in** — the corpus shipped with Spec Kitty core.
- **org** — the packs you configure under `charter_packs.org.packs` (including open packs
  from this repository).
- **project** — local, in-repo overrides under `.kittify/charter-packs/` for one project only.

An org pack artifact whose `id` collides with a built-in id field-merges into it and the
validator raises a `same_id_collision` advisory. Declare the intent as a DRG edge in the pack's
`drg/fragment.yaml` (`relation: enhances` to keep the merge, `overrides` for a full replacement);
`doctor charter-packs` fails on an override that the pack does not sanction in its
`replaceable-builtins.yaml`. Keep such overrides intentional and
rare — namespaced IDs avoid them.

## Horizontal composition (the pack direction)

Two mechanisms let independent packs combine *within* the org layer:

### 1. Multiple independent packs

List several packs under `charter_packs.org.packs`. Each contributes its artifacts additively;
there is no dependency between them. This is how you assemble, say, a DDD pack + a Java pack +
a testing pack for a single project.

Two packs must not declare the same artifact id: the later-listed pack silently shadows the
earlier one, and `doctor charter-packs` only reports it (this repository's CI fails on it).

> **Known gap ([spec-kitty#5779](https://github.com/spec-kitty/spec-kitty/issues/5779)).** Up to
> 4.0.0rc7, `charter context --include` and `charter activate KIND ID` see only the
> first-listed org pack; the action context and `doctor charter-packs` see all of them. Fixed by
> spec-kitty#6005.

### 2. Compound packs (`depends_on`)

A pack may declare that it **depends on** other packs. Spec Kitty resolves the dependency
graph (a DAG, with cycle detection) before loading, so a compound pack can bundle a coherent
stack without the consumer having to enumerate every constituent pack.

```yaml
# Illustrative only: no pack file carries depends_on yet (core #2467).
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

- **Assembly time** (`charter pack assemble`) fails by default with a conflict report. Use
  `--conflicts-out` to inspect, or `--force` for last-pack-wins.
- **Resolution time** the layer order (built-in → org → project) decides precedence.
  `doctor charter-packs` reports collisions between packs; duplicate `asset` or `template`
  ids across packs are a hard error. Do not re-declare a sibling pack's artifact.

A pack's DRG fragment (`drg/fragment.yaml`) is **additive only** — it may add edges and nodes
but must not remove or modify built-in graph state. An edge into a sibling pack raises a
`drg_external_endpoint` advisory; register both packs and run `doctor charter-packs` to check
the assembled graph.

## Keeping context lean

Composition multiplies the doctrine in play. Two habits keep sessions from flooding:

1. **Add only the packs your project's domain needs.** Prefer a focused stack over "activate
   everything."
2. **Activate only what you use.** The active charter (`activated_<kind>` keys, presets via
   `spec-kitty charter activate --preset`) constrains which offered artifacts resolve, which is
   the mechanism that stops multi-pack projects from ballooning context.

## See also

- [Use a Charter Pack](use-a-doctrine-pack.md)
- [Pack catalog proposal](../packs/catalog-proposal.md) — proposed packs and the compound
  stacks built on them.
