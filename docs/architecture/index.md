---
title: Architecture
description: Design, vision, and architecture decision records for spec-kitty-open-packs — including the direction for a content-from-code, checksum-tagged docsite.
doc_status: active
updated: '2026-07-18'
type: Architecture
kind: Hub
related:
- architecture/vision
- architecture/docsite-design
- architecture/adr
- research
---
# Architecture

The design and decision surface for `spec-kitty-open-packs`. This repository holds doctrine-pack
**content and packaging**; doctrine **logic** (resolution, the DRG, activation, the manifest
schema, the validator) lives in [`Priivacy-ai/spec-kitty`](https://github.com/Priivacy-ai/spec-kitty)
core. The architecture here is therefore mostly about **how content is organized, published, and
trusted** — not about doctrine mechanics.

## Contents

| Document | Purpose |
| --- | --- |
| [Vision](vision.md) | Why this repository exists and where the docsite fits in the pack-marketplace direction. |
| [Docsite design](docsite-design.md) | The content-from-code docsite: pipeline, generated-vs-authored split, checksum tagging. |
| [ADRs](adr/index.md) | Architecture Decision Records — the durable rationale behind each choice. |

## Grounding research

Every decision here is grounded in the [docsite feasibility research](../research/index.md) run on
2026-07-18: [feasibility & generator](../research/docsite-feasibility-and-generator.md),
[blockers & core dependencies](../research/blockers-and-core-dependencies.md), and
[information architecture](../research/docsite-information-architecture.md).
