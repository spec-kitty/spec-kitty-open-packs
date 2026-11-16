---
title: Architecture
description: Design, vision, and architecture decision records for spec-kitty-open-packs — including the direction for a content-from-code, checksum-tagged docsite.
doc_status: active
updated: '2026-11-16'
related:
- architecture/overview
- architecture/vision
- architecture/docsite-design
- architecture/adr
- research
---
# Architecture

The design and decision surface for `spec-kitty-open-packs`. This repository holds Charter Pack
**content and packaging**; charter **logic** (the pack schemas and structure, validation,
resolution, the DRG, activation) is owned by the charter repository,
[`spec-kitty/spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter). Core is the
deployable surface that assembles both into the CLI. The architecture here is therefore mostly about **how content is organized, published, and
trusted** — not about charter mechanics.

## Contents

| Document | Purpose |
| --- | --- |
| [Architectural overview](overview.md) | How a Charter Pack reaches a running Mission: tiers, the Charter Offering, the Active Charter and the charter entry seams. |
| [Vision](vision.md) | Why this repository exists and where the docsite fits in the pack-marketplace direction. |
| [Docsite design](docsite-design.md) | The content-from-code docsite: pipeline, generated-vs-authored split, checksum tagging. |
| [Roadmap](../plans/roadmap.md) | The themes that deliver the vision, their horizon and the epics behind each. |
| [ADRs](adr/index.md) | Architecture Decision Records — the durable rationale behind each choice. |

## Grounding research

Every decision here is grounded in the [docsite feasibility research](../research/index.md) run on
2026-07-18: [feasibility & generator](../research/docsite-feasibility-and-generator.md),
[blockers & core dependencies](../research/blockers-and-core-dependencies.md), and
[information architecture](../research/docsite-information-architecture.md).
