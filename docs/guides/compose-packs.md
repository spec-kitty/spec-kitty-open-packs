---
title: Compose packs
description: How Spec Kitty 4.x composes Charter Packs vertically (built-in, org, project) and horizontally (independent packs and compound depends_on packs), and how conflicts resolve.
doc_status: wip
updated: '2026-11-05'
related:
- guides/use-a-charter-pack
- packs/catalog-proposal
---
# Compose packs

Spec Kitty composes charter artefacts along two axes. Understanding both is the key to keeping a
project's context lean while still pulling in exactly the governance you want.

> **🚧 WIP.** The packs here follow the charter service's strict composition rules, and the as-is
> CLI rejects `depends_on` ([ADR 2026-11-04-1](../architecture/adr/2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility.md)).
> The tag `pre-charter-cutover` marks the last commit that was semi-compatible with it. The command
> wording on this page still describes the core-era CLI.

## Vertical composition (today)

Charter artefacts resolve in layers, later layers overriding earlier ones by artifact `id`:

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

A pack may declare that it **depends on** other packs, which it then may reference by name. This
is `packs/qa/pack.yaml`:

```yaml
pack_id: 01M6MF4FV4AMQF4RC8CY6JNESX
pack_version: 1.0.0
parent_pack: null
name: quality-assurance
pack_level: org
active_charter: org-charter.yaml
pack_drg: drg/fragment.yaml
depends_on:
  - pack_id: 01ARWG13C000000000000000FG
    range: ">=1.0,<2"
```

`depends_on` names a pack by its `pack_id`, not its name, and takes a version range. `pack_level` is
required beside it. The dependency must be configured too: the service does not fetch it, and refuses
a `depends_on` that no configured pack answers.

Here, every org pack depends on `built-in` and nothing else.

#### Referencing another pack's artifact

A reference to an artifact another pack holds names that pack. The name is the `name` in its
`pack.yaml`, never its directory, so `packs/qa` answers to `quality-assurance`. There are two forms,
and which one applies depends on where the reference is written:

| Where | Form | Example |
| --- | --- | --- |
| An end of a graph edge | `<pack>::<kind>:<id>` | `built-in::tactic:bdd-scenario-formulation` |
| The `id` of a typed reference | `<pack>::<id>` | `built-in::domain-event-capture` |

```yaml
# An edge in packs/qa/drg/fragment.yaml: the end carries its kind.
- source: procedure:qa-description-to-acceptance-ci
  target: built-in::tactic:bdd-scenario-formulation
  relation: suggests

# A typed reference in an event-driven directive: `type` already says the kind.
references:
  - type: tactic
    id: built-in::domain-event-capture
```

A reference to your own pack's artifact stays bare. The qualified pack must be in your pack's
`depends_on` closure and must hold the artifact. The charter service refuses anything else, and
[this repository's gate](validate-a-pack.md) says so first.

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

Composition multiplies the charter artefacts in play. Two habits keep sessions from flooding:

1. **Add only the packs your project's domain needs.** Prefer a focused stack over "activate
   everything."
2. **Activate only what you use.** The active charter (`activated_<kind>` keys, presets via
   `spec-kitty charter activate --preset`) constrains which offered artifacts resolve, which is
   the mechanism that stops multi-pack projects from ballooning context.

## See also

- [Use a Charter Pack](use-a-charter-pack.md)
- [Pack catalog proposal](../packs/catalog-proposal.md) — proposed packs and the compound
  stacks built on them.
