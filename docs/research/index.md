---
title: Research
description: 'Pre-decision investigations for spec-kitty-open-packs: feasibility, blockers, and structure research grounding the ADRs.'
doc_status: active
updated: '2026-07-18'
type: Context
kind: Hub
related:
- architecture
- architecture/vision
- packs/catalog-proposal
---
# Research

Investigations that precede and justify design decisions for this repository. Each research
document is a **findings capture** — grounded in the actual code and tracker state at the time
of writing — that feeds the decisions recorded under
[`docs/architecture/adr/`](../architecture/adr/index.md).

> Research is dated and immutable-ish: it records what was true when the investigation ran.
> When reality moves, supersede a finding with a newer document rather than silently editing
> the old one.

## Docsite feasibility investigation (2026-07-18)

A three-lens research squad investigated whether `spec-kitty-open-packs` can host a **published
docsite that pulls its reference content from the actual code structure** (packs, validator),
with **checksum-tagged packs** for verifiable distribution.

| Lens | Question | Document |
| --- | --- | --- |
| Feasibility & tooling | Can pack/validator pages be generated from source? Which generator? | [Docsite feasibility & generator](docsite-feasibility-and-generator.md) |
| Blockers & dependencies | What missing Spec Kitty core functionality blocks this? | [Blockers & core dependencies](blockers-and-core-dependencies.md) |
| Information architecture | How should the docsite be structured for its audiences? | [Docsite information architecture](docsite-information-architecture.md) |

**Headline conclusion:** the direction is **feasible and largely unblocked for authored + per-artifact
content today**, but the *checksum-tagging* and *stable pack manifest* halves depend on core work
that is planned-but-not-landed. The recommended path decouples the docsite from core's internal
packages and generates its own interim integrity tags. See the
[docsite design](../architecture/docsite-design.md) and the
[ADRs](../architecture/adr/index.md) for the decisions this research produced.
