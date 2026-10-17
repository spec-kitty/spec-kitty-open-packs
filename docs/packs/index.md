---
title: Packs
description: The open doctrine pack catalog — what packs are, when to use them, and a link to each pack's generated reference page plus the forward-looking catalog.
doc_status: active
updated: '2026-10-17'
kind: Hub
related:
- packs/catalog-proposal
- packs/built-in
- packs/cave-kitty
- packs/event-driven
- packs/qa
- packs/internal
- guides/use-a-doctrine-pack
- guides/compose-packs
- architecture/docsite-design
---
# Packs

This is the landing page for the open **doctrine packs** distributed for
[Spec Kitty](https://github.com/spec-kitty/spec-kitty). A pack is a coherent,
composable, opt-in slice of governance behaviour — directives, tactics,
styleguides, toolguides, paradigms, procedures, agent profiles, glossary packs,
and the DRG edges that wire them together — that a consumer project pulls in
**deliberately** instead of inheriting the entire built-in corpus and flooding
every LLM session's context.

## What a pack is

Each pack is a directory of artifact-kind subdirectories (`directives/`,
`tactics/`, `styleguides/`, …), optionally carrying:

- a `pack.yaml` descriptor (`name`, `pack_version`, `parent_pack`, and — when
  authored — `purpose` / `depends_on`);
- an `org-charter.yaml` declaring activation defaults;
- a hand-written `README.md` with the authored "what it is and why" narrative.

Content and packaging live in this repository; doctrine **logic** — resolution,
the DRG, activation, the manifest schema, and the pack validator — lives in
[`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty).

## When to use which

- **Evaluating the direction?** Read the
  [pack catalog proposal](catalog-proposal.md) — the forward-looking plan for
  carving the built-in monolith into focused, composable packs.
- **Adopting a pack?** Follow [Use a Charter Pack](../guides/use-a-doctrine-pack.md)
  and [Compose packs](../guides/compose-packs.md).
- **Checking exactly what ships in a pack today?** Open its **reference page**
  below. Those pages are generated from source, so their inventories, counts,
  checksums, and validation status are always faithful to the committed packs.

## Pack reference pages

The pages below are **generated** from the pack source by
`scripts/docs/gen_pack_reference.py` (see the
[docsite design](../architecture/docsite-design.md) for the generated-versus-authored
boundary and the checksum design). They are never hand-edited; CI re-runs the
generator and fails on any drift. Purposes in this table are **authored** here —
the generator does not fabricate a purpose when a pack's `pack.yaml` omits one.

| Pack | Purpose | Reference |
| --- | --- | --- |
| `built-in` | Spec Kitty's complete built-in doctrine corpus — the baseline every project starts from, and the source material the focused packs are carved out of. | [built-in reference](built-in.md) |
| `cave-kitty` | A re-voicing pack that compresses agent output into a terse, token-saving "caveman" voice while keeping every payload exact. Inert until a consumer opts in. | [cave-kitty reference](cave-kitty.md) |
| `event-driven` | Event-sourced design doctrine: a schema version on every event, one canonical writer behind an event-bridge port, projections and replay, upcasting, and idempotent consumers. | [event-driven reference](event-driven.md) |
| `qa` | Quality assurance as governed work: a `qa` mission type and a description-to-acceptance CI loop that keeps acceptance tests tied to the product's promises. | [qa reference](qa.md) |
| `internal` | Spec Kitty's own org-tier pack — the dogfooded doctrine that governs how the project's contributors and maintainers land PRs, process the tracker, and keep main honest. Not shipped to consumers. | [internal reference](internal.md) |

## The forward-looking catalog

The materialized packs above are the beginning. The
[pack catalog proposal](catalog-proposal.md) lays out the full intended set —
base packs such as `core-engineering`, `domain-driven-design`, and
`test-and-bdd`, plus compound stacks that bundle them — and maps each proposed
pack to the built-in artifacts it would curate. Names and boundaries there are
subject to change and are refined issue-by-issue as each pack is materialized.
