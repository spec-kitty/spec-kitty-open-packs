---
title: Packs
description: The open Charter Pack catalog — what packs are, when to use them, and a link to each pack's generated reference page plus the forward-looking catalog.
doc_status: active
updated: '2026-11-11'
kind: Hub
related:
- packs/catalog-proposal
- packs/built-in
- packs/foundation
- packs/writing
- packs/testing
- packs/refactoring
- packs/architecture
- packs/planning-analysis
- packs/pack-authoring
- packs/python
- packs/javascript
- packs/drupal
- packs/java
- packs/rust
- packs/go
- packs/cave-kitty
- packs/event-driven
- packs/qa
- packs/spdd
- packs/internal
- guides/use-a-charter-pack
- guides/compose-packs
- architecture/docsite-design
---
# Packs

This is the landing page for the open **Charter Packs** distributed for
[Spec Kitty](https://github.com/spec-kitty/spec-kitty). A pack is a coherent,
composable, opt-in slice of governance behaviour — directives, tactics,
styleguides, toolguides, paradigms, procedures, agent profiles, glossary packs,
and the DRG edges that wire them together — that a consumer project pulls in
**deliberately** instead of inheriting the entire built-in corpus and flooding
every LLM session's context.

## What a pack is

Each pack is a directory of artifact-kind subdirectories (`directives/`,
`tactics/`, `styleguides/`, …), optionally carrying:

- a `pack.yaml` descriptor (`pack_id`, `name`, `pack_version`, `parent_pack`, and —
  when authored — `pack_level` / `depends_on`);
- a `pack.md` — the pack's description, whose preamble the generated reference
  page renders under its Purpose heading;
- an `org-charter.yaml` declaring activation defaults;
- a hand-written `README.md` with the authored "what it is and why" narrative.

Content and packaging live in this repository; charter **logic** — resolution,
the DRG, activation, the manifest schema, and the pack validator — lives in
[`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty).

## When to use which

- **Evaluating the direction?** Read the
  [pack catalog proposal](catalog-proposal.md) — the forward-looking plan for
  carving the built-in monolith into focused, composable packs.
- **Adopting a pack?** Follow [Use a Charter Pack](../guides/use-a-charter-pack.md)
  and [Compose packs](../guides/compose-packs.md).
- **Checking exactly what ships in a pack today?** Open its **reference page**
  below. Those pages are generated from source, so their inventories, counts,
  checksums, and validation status are always faithful to the committed packs.

## Pack reference pages

The pages below are **generated** from the pack source by
`scripts/docs/gen_pack_reference.py` (see the
[docsite design](../architecture/docsite-design.md) for the generated-versus-authored
boundary and the checksum design). They are never hand-edited; CI re-runs the
generator and fails on any drift. Each page's Purpose section is the preamble of
the pack's authored `pack.md` — the charter's pack description. The summaries in
this table are authored **here**.

| Pack | Purpose | Reference |
| --- | --- | --- |
| `built-in` | The default distribution pack: holds no artifacts of its own and aggregates `foundation`, `writing`, `testing`, `refactoring`, `architecture` and `planning-analysis`; keeps the `default` and `minimal` presets (#73). | [built-in reference](built-in.md) |
| `foundation` | The basis every project builds on: Generic Giannis and the implementer, reviewer, analyst and human-in-charge profiles; the software-dev, plan and research missions; every cross-cutting directive with its how-to procedures, tactics and toolguides, including the adversarial-review squad practice. A member of built-in. | [foundation reference](foundation.md) |
| `writing` | Documentation, communication and glossary doctrine, and the documentation mission. A member of built-in. | [writing reference](writing.md) |
| `testing` | Test design, BDD and mutation testing, and debugger-debbie; the base for the stack packs. A member of built-in. | [testing reference](testing.md) |
| `refactoring` | Refactoring catalogue, semantic compression and code-smell anti-patterns. A member of built-in. | [refactoring reference](refactoring.md) |
| `architecture` | Domain-driven design and C4 modelling, with architect-alphonso and paula-patterns. A member of built-in. | [architecture reference](architecture.md) |
| `planning-analysis` | Planning, research, operator-led retrospectives and brownfield analysis. A member of built-in. | [planning-analysis reference](planning-analysis.md) |
| `pack-authoring` | Opt-in doctrine and Charter Pack authoring, with doctrine-daphne. | [pack-authoring reference](pack-authoring.md) |
| `python` | The opt-in Python stack. | [python reference](python.md) |
| `javascript` | The opt-in JavaScript, TypeScript and frontend stack. | [javascript reference](javascript.md) |
| `drupal` | The opt-in Drupal stack. | [drupal reference](drupal.md) |
| `java` | The opt-in Java stack. | [java reference](java.md) |
| `rust` | The opt-in Rust stack. | [rust reference](rust.md) |
| `go` | The opt-in Go stack. | [go reference](go.md) |
| `cave-kitty` | A re-voicing pack that compresses agent output into a terse, token-saving "caveman" voice while keeping every payload exact. Inert until a consumer opts in. | [cave-kitty reference](cave-kitty.md) |
| `event-driven` | Event-sourced design guidance: a schema version on every event, one canonical writer behind an event-bridge port, projections and replay, upcasting, and idempotent consumers. | [event-driven reference](event-driven.md) |
| `qa` | Quality assurance as governed work: a `qa` mission type and a description-to-acceptance CI loop that keeps acceptance tests tied to the product's promises. | [qa reference](qa.md) |
| `spdd` | Opt-in Structured-Prompt-Driven Development and REASONS canvas guidance, including step-specific prompt fragments for `software-dev`. | [spdd reference](spdd.md) |
| `internal` | Spec Kitty's own org-tier pack — the dogfooded charter that governs how the project's contributors and maintainers land PRs, process the tracker, and keep main honest. Not shipped to consumers. | [internal reference](internal.md) |

## The forward-looking catalog

The materialized packs above are the beginning: #73 carved `built-in` into `foundation`,
`writing` and the bundles listed above (built-in aggregates `foundation`, `writing`, `testing`, `refactoring`, `architecture` and `planning-analysis`), guided by this catalog and the charter's census. The
[pack catalog proposal](catalog-proposal.md) lays out the full intended set —
base packs such as `core-engineering`, `domain-driven-design`, and
`test-and-bdd`, plus compound stacks that bundle them — and maps each proposed
pack to the built-in artifacts it would curate. Names and boundaries there are
subject to change and are refined issue-by-issue as each pack is materialized.
